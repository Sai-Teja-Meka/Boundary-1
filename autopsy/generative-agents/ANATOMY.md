# ANATOMY — Generative Agents (Park et al. 2023)

Subject of `[L0] [AUTOPSY]`. Traced from source (call paths, not READMEs) in a
read-only clone outside this repo. Nothing here changes the frozen constitution;
a **Constitutional note** at the end records that no law-change objection arose.

## License + commit hash examined

- **License:** Apache License 2.0 (`LICENSE`, lines 1–3).
- **Repo:** `github.com/joonspk-research/generative_agents`
- **Commit examined:** `fe05a71d3e4ed7d10bf68aa4eda6dd995ec070f4` (default branch, shallow clone).
- **Code root:** `reverie/backend_server/` (the "reverie" simulation server).

## Core data model (file:line citations)

The paper's "Memory Stream" is `AssociativeMemory`, a bag of `ConceptNode`s.

- **`ConceptNode`** — `persona/memory_structures/associative_memory.py:19–47`.
  Fields (`:25–43`): `node_id`, `node_count`, `type_count`, `type` (`"event"` /
  `"thought"` / `"chat"`, `:28`), `depth` (`:29`), `created` / `expiration` /
  `last_accessed` (`:31–33`, `last_accessed` initialized to `created`), an SPO
  triple `subject`/`predicate`/`object` (`:35–37`), `description`,
  `embedding_key`, **`poignancy`** (the importance score, 1–10), `keywords`, and
  **`filling`** (`:43`) — for a thought, the list of source `node_id`s it was
  derived from (its evidence).
- **`AssociativeMemory`** — `associative_memory.py:50–109`. Three parallel
  sequences `seq_event` / `seq_thought` / `seq_chat` (`:54–56`), keyword inverted
  indexes `kw_to_event/thought/chat` (`:58–60`), keyword-frequency maps
  `kw_strength_event/thought` (`:62–63`), and a side `embeddings` dict
  (`embedding_key → vector`, `:65`) persisted in `embeddings.json`.
- **`depth` is the derivation distance:** events/chats are `depth = 0`
  (`:161`, `:251`); a thought is `depth = 1 + max(depth of its filling nodes)`
  (`add_thought`, `:207–210`). Reflections-on-reflections climb in depth.
- **Persistence:** three JSON files — `nodes.json`, `kw_strength.json`,
  `embeddings.json` (`save`, `:112–150`; load, `:65–109`). All floats, all
  wall-clock `datetime` strings (`%Y-%m-%d %H:%M:%S`).
- **Short-term store / hyperparameters:** `memory_structures/scratch.py` —
  `att_bandwidth = 3` (`:21`), `retention = 5` (`:23`), `recency_w = relevance_w
  = importance_w = 1` (`:57–59`), `recency_decay = 0.99` (`:60`),
  `importance_trigger_max = 150` (`:61`).

## Write path (ingestion → storage) — as traced

`cognitive_modules/perceive.py :: perceive()`:

1. From the events in the agent's view, keep the `att_bandwidth = 3` spatially
   closest (`perceive.py:97–102`).
2. **Novelty filter, not dedup:** compare against only the latest `retention = 5`
   events (`:119–123`, via `associative_memory.get_summarized_latest_events`,
   `associative_memory.py:274–278`). An event whose SPO summary is not in that
   5-item window is treated as new.
3. For each new event: `event_poignancy = generate_poig_score(...)` — an **LLM
   call** returning an integer 1–10 (`perceive.py:147–148`, `:15–20`). Then
   `a_mem.add_event(curr_time, None, s, p, o, desc, keywords, poignancy, …)`
   (`:175–176`). Note the `expiration = None` for events.
4. `add_event` (`associative_memory.py:153–196`) prepends the node to `seq_event`
   (`self.seq_event[0:0] = [node]`, `:177`), updates the keyword indexes
   (`:178–184`) and `kw_strength` (unless `"is idle"`, `:187–192`), and writes the
   embedding (`:194`).
5. **Reflection accounting:** `importance_trigger_curr -= event_poignancy` and
   `importance_ele_n += 1` (`perceive.py:178–179`). This is the only "pressure"
   signal in the system.

Storage is **append-only and unbounded**: every `add_*` prepends; nothing is ever
removed.

## Read path (query → answer) — as traced, not as marketed

The marketed formula is "retrieval = recency × importance × relevance." The
traced formula (`cognitive_modules/retrieve.py :: new_retrieve`, `:199–271`):

1. Pool = `seq_event + seq_thought` (events **and** reflections together),
   dropping any node with `"idle"` in its `embedding_key`; sort **ascending by
   `last_accessed`** (`:224–228`).
2. Three component scores, each then **min–max normalized to [0,1] over the whole
   pool** (`:231–236`, `normalize_dict_floats` `:70–104`):
   - **recency** (`extract_recency`, `:132–152`): `recency_vals =
     [recency_decay ** i for i in range(1, N+1)]` assigned in sorted order
     (`:145–150`). Because the pool is oldest-first and `decay = 0.99 < 1`, the
     **oldest** node gets `0.99¹` (→ normalizes to 1) and the **newest** gets
     `0.99ᴺ` (→ normalizes to 0). As written, recency is computed over
     **chronological rank, not elapsed time, and is inverted** — it rewards the
     least-recently-accessed memory. (Recorded here as traced; dampened by its low
     weight below.)
   - **importance** (`extract_importance`, `:155–172`): raw `node.poignancy`.
   - **relevance** (`extract_relevance`, `:175–196`): `cos_sim(node_embedding,
     focal_embedding)` (`:189–194`), embeddings via an LLM.
3. Weighted sum (`:244–249`): `gw = [0.5, 3, 2]`; score `= recency_w·rec·0.5 +
   relevance_w·rel·3 + importance_w·imp·2`. With the scratch defaults (`w = 1`)
   the effective weights are **recency 0.5, relevance 3, importance 2** —
   relevance dominates; the comment at `:239–243` admits the weights are
   hand-picked ("test out different weights… should likely be learned").
4. Take the top `n_count = 30` (`:262`), set each returned node's `last_accessed =
   curr_time` (`:266–267`), and return a **flat list of `ConceptNode`s**.

There is **no "answer."** Retrieval hands 30 node `description` strings to a
downstream LLM prompt (planning / conversation); the "answer" is an LLM
completion. No typed value, no confidence, and — crucially — no obligation to
cite which retrieved nodes were used.

## Forgetting / consolidation mechanism — **ABSENT**

Search performed (all under `reverie/backend_server/persona/`):
`grep -nwE 'expiration|evict|forget|prune|del |\.pop\(|remove\(|delete'`.

Findings: `expiration` is **written** (`created + 30 days` for every thought —
`reflect.py:124,220,236`, `converse.py:247,284`, `plan.py:506`; `None` for
events) and round-tripped through save/load (`associative_memory.py:79–82,
125–128`), but it is **never read to evict**. No `pop`, `del`, `remove`, prune,
or capacity check exists on `seq_event/seq_thought/seq_chat`. `retention = 5` and
`att_bandwidth = 3` bound **perception**, not storage. Reflection only *adds*
nodes. So there is no forgetting, no eviction, and no compaction: the stream
grows without bound (see failure #171). Consolidation-by-compression is likewise
absent — reflection *summarizes into new nodes on top of* the originals, it does
not replace or shrink them.

## Calibration / provenance handling

- **Calibration — ABSENT.** `poignancy` is *importance*, not confidence; it never
  expresses uncertainty about correctness. Retrieved nodes enter an LLM prompt
  with no confidence, no abstention path, and no calibration of any kind. There is
  no place in `retrieve.py`/`plan.py` where an answer's reliability is scored.
- **Provenance — PARTIAL (the ancestor, un-enforced).** The *write* path records
  real provenance: a thought stores `filling` = the `node_id`s it was derived from
  (`reflect.py:130–132`, `run_reflect` builds `evidence` from retrieved nodes),
  and `depth` marks how many inference hops from observation
  (`associative_memory.py:207–210`). So reflections **are** distinguishable from
  observations in storage — by `type`, by `depth ≥ 1`, and by non-empty
  `filling`. **But the read path throws this away:** `new_retrieve` pools events
  and thoughts, scores them identically, and returns a flat list; nothing consults
  `filling`/`depth`, and no answer is required to cite its support. A reflection
  (or a reflection-of-a-reflection) can be retrieved and consumed exactly as if it
  were an observed fact. This is precisely our provenance-law question
  (`BOUNDARY.md §4.2`), and Generative Agents answers it only halfway: the
  citation graph exists but is never binding.

## Prospective memory — **ABSENT** (as expected)

There is no `intend(condition → event)` construct and nothing that fires on a
future write. The closest thing is **time-indexed** daily scheduling in
`cognitive_modules/plan.py` (`generate_hourly_schedule` / `f_daily_schedule`,
around `plan.py:400–520`): the agent pre-generates a clock-keyed plan and executes
by wall-clock time. That is a *schedule*, not a trigger — no condition is watched,
nothing fires exactly-once when a matching event is later perceived. Where a real
prospective memory would live: a pending-intention store consulted inside
`perceive.py` / `execute.py` on every new write, keyed on a triggering predicate.
No such store exists.

## Three failure modes (issue tracker)

1. **Unhandled lookup crash — location absent from spatial memory throws.**
   `KeyError: 'kitchen'` in `spatial_memory.py:107`
   (`get_str_accessible_arena_game_objects`): the LLM emitted an action location
   that does not exist as a key in the agent's spatial tree, and the lookup raises
   instead of degrading. *Absence throws instead of scoring.*
   https://github.com/joonspk-research/generative_agents/issues/192

2. **Silent write-path durability failure — memory not persisting.** Over a
   15,000+ step run, `nodes.json`, `kw_strength.json`, and `embeddings.json` stay
   effectively empty; new memories are not durably written. The store fails
   silently rather than surfacing the loss.
   https://github.com/joonspk-research/generative_agents/issues/171

3. **Ingestion parse crash on malformed generator output.** `string index out of
   range` at `run_gpt_prompt.py:380` (`__func_clean_up`), accessing `task[-1]` on
   an empty string when the LLM's task-decomposition response is blank. Unvalidated
   payload from a stochastic producer crashes the pipeline instead of being
   rejected or defaulted.
   https://github.com/joonspk-research/generative_agents/issues/154

## ONE technique worth stealing

**The `filling` + `depth` derivation DAG.** Every reflection stores the exact set
of `node_id`s it was built from (`filling`) and a `depth` equal to
`1 + max(depth of its sources)`, so observations sit at depth 0 and each inferential
hop increments depth. For almost no cost this yields (a) a citation set per derived
memory and (b) a single integer that says "how far from raw observation is this?"
That is a ready-made provenance graph. It lands squarely in **our Layer 7
(Provenance)**: `filling` is our provenance `support` list, and `depth` is a cheap
lineage marker that our `kind` vocabulary can encode (`observed` at depth 0,
`derive` above) — and it usefully feeds **Layer 6 (Meta-memory)**, where `depth`
is a natural prior on confidence (deeper = more inference = more room to be wrong).
The lesson we take that Generative Agents did not: *record it AND make it binding
at read time.*

## ONE mistake worth codifying (as a strain-trial idea)

**Mistake: per-query global min–max normalization makes retrieval unstable — an
irrelevant memory reorders unrelated results, and the distortion grows with memory
size.** `normalize_dict_floats` (`retrieve.py:70–104`) rescales each component
using the **global min and max over the entire pool** every query
(`:232,234,236`). So the normalized score of a fixed memory depends on the
extremes present in the whole store: inserting one distant, high-poignancy,
freshly-accessed decoy shifts the min/max and can **reorder the top-k of a
completely unrelated query** — a violation of independence-of-irrelevant-
alternatives, compounding without bound because nothing is ever evicted.

**Strain-trial idea (targets our determinism law + Layer 2/Layer 3 retrieval
stability):**
- *Corpus:* take a fixed cue `q` and a small set `T` of target items that are its
  correct top-k, plus filler. Freeze the expected ranked top-k for `q`.
- *Manipulation:* produce a second corpus identical to the first plus `M` injected
  **decoys that are maximally far from `q` in embedding space** but carry extreme
  importance and extreme recency (the values that dominate the global min/max).
  Record them in a murk-style `ground_truth.json` as `irrelevant_to=q`.
- *Assertion:* ingest each corpus, query `q` on both, and require the returned
  top-k **ranking for `q` to be identical** — importance/recency/relevance of items
  unrelated to `q` must not change `q`'s answer. Sweep `M` upward and require the
  invariance to hold at every scale (this is where global normalization visibly
  breaks and where our per-item, non-normalized scoring must not).
- *Why it bites:* a Generative-Agents-style scorer fails immediately (the decoys
  move the normalization endpoints); our engine must score each item on an
  absolute, memory-size-independent scale so retrieval is a pure function of `(q,
  the relevant items)`, not of the rest of the store.

## Constitutional note (no law-change objection)

The autopsy raised no objection to the frozen `BOUNDARY.md`. If anything it
affirms four of our laws by showing their absence in a landmark system: the
**budget law + Layer 3 forgetting** (GA has none — unbounded growth, failure
#171); the **provenance law, Layer 7** (GA records `filling`/`depth` but never
binds them at read time); the **cardinal interface rule §7.3**, capability/lookup
absence must surface as a score, never an exception (GA's `KeyError`, failure
#192); and **canonical, typed payloads §2.4** against unvalidated generator output
(GA's empty-string crash, failure #154). No change is warranted.

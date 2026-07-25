# ANATOMY — Mem0

> **Erratum — 2026-07-25 (`[L3] [PULSE]`).** The text below uses **pre-ratification
> layer names**. It is left exactly as written; this note maps it, and nothing
> beneath it is rewritten.
>
> | as written below | ratified ladder (`BOUNDARY.md §5`) |
> |---|---|
> | "Layer 6 (Contradiction & Dedup)" / "Layer 6 (contradiction/dedup)" / "what Layer 6 certifies" | **there is no standalone Contradiction layer.** Supersession, contradiction and "the current value among conflicts" are facets of **L4 Consolidation** (attribute histories: newest entry = current value, conflicting entries = the contradiction, as-of query = L4 reconstruction) |
> | ratified **L6** | **Meta-memory** — so the one correct L6 reference below is *"calibration (Layer 6)"*, which stands |
>
> `"the provenance law (Layer 7)"` also stands: §4.2 is dormant until Layer 7 and
> binding forever after, though ratified **L7 is Generation**, not "Provenance".
>
> Reconciled in `autopsy/GAPMAP.md` ("Naming reconciliation", read before the
> matrix), which flagged this as an erratum in non-frozen documentation to be
> fixed at the next doc pass. This is that pass.

Subject of `[L0] [AUTOPSY]`. Traced from source (call paths, not READMEs) in a
read-only clone outside this repo, scoped to the **core open-source `Memory`
class** (`mem0/memory/main.py`) — not SDKs, integrations, or platform client
code. A **Constitutional note** at the end records that no law-change objection
arose.

## License + commit hash examined (+ open-core boundary)

- **License:** Apache License 2.0 (`LICENSE`, lines 1–3) for the core `mem0/`
  package.
- **Repo:** `github.com/mem0ai/mem0`
- **Commit examined:** `d6d89c987bddf580870db14c69db974edfc5263c` (default branch, shallow clone).
- **Open-core boundary observed:** the Apache-2.0 core is the local `Memory`
  engine (`mem0/memory/`, `mem0/configs/`, vector/embeddings/LLM adapters). The
  **hosted platform** lives behind `mem0/client/*` and `mem0/proxy/*`
  (`MemoryClient` → the managed API). Several capabilities are **platform-only
  and refuse in OSS**: `mem0/memory/notices.py:49`
  `DECAY_FEATURE_ERROR_MESSAGE = "The decay parameter is not supported by the OSS
  Memory SDK."`; `:46–47` the same for `timestamp` and `reference_date`;
  `main.py:762` (`timestamp` is "Platform-only… Not supported in OSS");
  `main.py:444–445` raises if `decay=True`. So **decay, server-side timestamps,
  and project policy live on the proprietary side**; the OSS core is a
  vector-store + LLM-extraction memory with no lifecycle management.

## Core data model (file:line citations)

Mem0 has no bespoke node type; a memory is a **row in a vector store** plus a
**history row** in a SQLite DB, keyed by a random `uuid4`.

- A stored memory's payload (`main.py:999–1007`, surfaced at read
  `:1660–1669`): `data` (the fact **text** — an LLM paraphrase, not the raw
  message), `hash` = `md5(text)` (`:990`), `created_at`/`updated_at`
  (`:1003–1005`), scope ids `user_id`/`agent_id`/`run_id`, `actor_id`, `role`,
  `attributed_to` (optional), `text_lemmatized` (for BM25), and optional
  `expiration_date`.
- **History DB:** every write appends a row with an `event` label
  (`add_history`, e.g. `:1035–1045`) — in the add path always `"ADD"`.
- **Auxiliary stores:** an entity store (entities extracted per memory,
  `:1056–1068`) and an optional graph memory; neither changes the additive core.
- `MemoryItem` (`mem0/configs/base.py`) is the read-side shape: `id`, `memory`
  (=`data`), `hash`, `created_at`, `updated_at`, `score`.

There is **no field distinguishing an observed fact from an inferred one** (see
Provenance verdict).

## Write path (ingestion → storage) — as traced, not as marketed

`Memory.add(...)` (`main.py:735`, `infer=True` by default `:745`) →
`_add_to_vector_store` (`:849`). Two branches:

- **`infer=False` (raw, `:850–884`):** each message is stored verbatim as one
  memory; `role` and `actor_id` are copied into metadata (`:864–869`); event
  `"ADD"`. No extraction, no dedup.
- **`infer=True` (the default) — the "V3 PHASED BATCH PIPELINE" (`:886–1068`):**
  1. **Retrieve existing** (`:893–901`): vector search `top_k=10` over the same
     scope.
  2. **UUID→int remap** (`:903–908`): existing memories are handed to the LLM as
     integer ids `"0","1",…` ("anti-hallucination") mapped back afterward.
  3. **Single LLM extraction** (`:910–932`) with
     `system_prompt = ADDITIVE_EXTRACTION_PROMPT` (`:912`); response parsed as
     `json.loads(...).get("memory", [])` (`:948`).
  4. **Dedup = exact md5 only** (`:990–994`): skip a candidate if its
     `md5(text)` matches an existing or already-seen hash. Nothing else.
  5. **Batch insert ALL survivors** (`:1015–1025`) with fresh `uuid4`s; every
     history row is `event="ADD"` (`:1035–1045`).

**The ADD/UPDATE/DELETE decision the paper (and this method's own docstring,
`:765–767`, "decide whether to **add, update, or delete** related memories")
describes is not in this code path.** `_update_memory` (`:1988`) and
`_delete_memory` (`:2050`) are called **only** from the public `update()`
(`:1835`) / `delete()` (`:1852`) APIs — explicit caller actions — never from
`add`. The legacy decision machinery still exists but is **dead**:
`DEFAULT_UPDATE_MEMORY_PROMPT` (`prompts.py:176`) and `get_update_memory_messages`
(`prompts.py:406`) are self-referenced only (`:408–409`) and **not imported** by
`main.py`.

**Focus #2 verdict (ADD-only accumulation) — CONFIRMED from code + prompt.** The
extraction prompt states its "**sole operation is ADD**" (`prompts.py:472`) and
uses existing memories "**ONLY for deduplication and linking**" (`:511`); a
related existing memory gets its UUID appended to the new memory's
`linked_memory_ids` (`:513`) — a *link*, never a supersession. The only
suppression is exact-md5 (code) or LLM-judged verbatim-equivalence (prompt).

**Focus #3 verdict (contradiction) — silent coexistence.** A new fact that
contradicts a stored one is extracted as a **separate ADD** and (if related)
linked; the contradicted memory is neither updated nor deleted. "User's name is
LGY" then "User's name is LGS" yields **two** coexisting memories (tracker
#4896). Paraphrases of the same fact (different bytes → different md5) also both
persist.

**Focus #4 (provenance) at write:** the extracted `text` is an LLM paraphrase;
the prompt instructs the model to *reword* assistant-generated content into
user-framed statements ("User was recommended X", `prompts.py:488`). `role` /
`actor_id` are attached **only** in the `infer=False` raw path (`:864–869`); in
the default `infer=True` path an extracted fact carries at most an optional
`attributed_to` subject tag (`:1006–1007`) — not a source flag.

## Read path (query → answer) — as traced

`Memory.search(...)` (`main.py:1349`) → `_search_vector_store` (`:1598`), a
**hybrid** retriever:

1. Dense semantic search over the vector store + **BM25** over `text_lemmatized`
   + **entity boosts** from the entity store, fused by `score_and_rank`
   (`:1649–1657`) to `top_k`.
2. Expired memories are filtered at read time
   (`_payload_is_expired`, `:417`, applied `:1640`) unless `show_expired=True`.
3. Each result is a `MemoryItem` (`:1678–1685`) with a retrieval `score`, plus
   promoted keys `user_id/agent_id/run_id/actor_id/role/attributed_to/
   expiration_date` (`:1660–1668`).

There is no "answer" — `search` returns ranked memory texts + scores; any
answer is produced by the caller's LLM. The `score` is a **retrieval similarity**,
not a calibrated confidence in the fact's truth, and there is no abstention path.

## Forgetting / consolidation — **ABSENT** (automatic); manual soft-hide only

Search performed across `mem0/memory` and `mem0/configs`:
`grep -niE 'ttl|expire|expiry|evict|decay|forget|prune|retention'`.

- **Automatic decay / TTL / eviction: ABSENT in OSS, and explicitly gated to the
  platform.** `decay` raises `"not supported by the OSS Memory SDK"`
  (`notices.py:49`, `main.py:444–445`). There is even a **delete-counting upsell
  nag**: `detect_decay_usage_from_delete` fires a notice after
  `DECAY_USAGE_DELETE_THRESHOLD = 5` manual deletes in a 7-day window
  (`notices.py:30–32`, `main.py:1853–1855`) — the engine notices you doing its
  forgetting by hand and points you at the paid feature. Tracker #5330 (a user
  proposal for lifetime-based cleanup) corroborates: no built-in decay.
- **Manual `expiration_date`: present but non-destructive.** A caller may pass
  `expiration_date` to `add` (`main.py:744`, docstring `:763–764`); expired
  memories are **hidden** at read (`_payload_is_expired`, `:417/1325/1640`), not
  deleted — `show_expired=True` reveals them. Opt-in, per-add, reversible hide.
- **Consolidation: ABSENT.** No summarization-into-fewer-records; the pipeline
  only inserts. Memory grows monotonically (tracker #4573: an audit of 10,134
  entries found 97.8% "junk," >5,500 duplicates).

## Calibration / provenance

- **Calibration — ABSENT.** The only number attached to a memory at read is a
  retrieval `score` (`main.py:1684`) — semantic/BM25 similarity, thresholded
  (`:1654`). It expresses *how well the text matched the query*, never *how
  likely the fact is true*. No confidence, no abstention.
- **Provenance — ABSENT at the fact level (claim VERIFIED).** In the default
  `infer=True` path a stored memory is an LLM paraphrase with **no structural
  marker of whether it was user-stated or assistant-generated/inferred**. The
  extraction prompt folds assistant recommendations into user-framed statements
  (`prompts.py:488`); `role`/`actor_id` are set only in the raw `infer=False`
  path (`main.py:864–869`), and `attributed_to` is a subject tag, not a source
  flag. So the claim to verify — *generated facts are treated as first-class
  observations* — holds: an inferred fact and a user-stated fact occupy the same
  schema, rank in the same pool, and are indistinguishable at retrieval.

## Prospective memory — **ABSENT** (as expected)

No `intend(condition → event)` and nothing that fires on a future write. `search`
and `add` have no trigger registry; the nearest construct is the passive
`expiration_date` hide (`main.py:744, 417`), which is a *read-time filter*, not
an active trigger. Where a real prospective memory would live: a
condition-indexed pending-intention store consulted inside `add()`/
`_add_to_vector_store` on every new write. No such store exists.

## Three failure modes (tracker)

1. **ADD-only architecture stores contradictions/near-duplicates instead of
   resolving them.** Adding "my name is LGY" then "my name is LGS" returns an ADD
   for both → two memories, not one UPDATE; the implementation does not match the
   documented conflict-resolution behavior. Directly the marketing-vs-code gap
   traced above.
   https://github.com/mem0ai/mem0/issues/4896

2. **Hash-dedup TOCTOU race → permanent duplicate memories under concurrency.**
   The only dedup is an exact-md5 check taken against a *stale Phase-1 snapshot*
   and re-checked in Phase 4/5 after the LLM round-trip; two concurrent `add()`
   calls both pass the guard and both insert, silently and permanently. Confirms
   exact-hash is the sole dedup, with no semantic merge/update.
   https://github.com/mem0ai/mem0/issues/6515

3. **Unbounded accumulation of junk/duplicates at scale.** An audit of 10,134
   mem0 entries reported 97.8% "junk," with >5,500 hash-duplicate and
   cosine-cluster duplicate entries — the direct consequence of ADD-only +
   exact-hash dedup + no eviction.
   https://github.com/mem0ai/mem0/issues/4573

## ONE technique worth stealing

**The deterministic hybrid retrieval channel: BM25 over a lemmatized copy of the
text, fused with entity-match boosts, ranked alongside the semantic score
(`main.py:1649–1657`, `text_lemmatized` written at `:1001`).** The lexical (BM25)
and entity channels are **pure, LLM-free, and reproducible** — exactly the kind
of deterministic index our constitution names for **Layer 2 (Recall — "token
n-grams, MinHash")**. Mem0 shows a clean way to *combine* a deterministic lexical
recall signal with an entity-adjacency boost and rank them together; we can lift
the fusion (sparse lexical + entity-graph boost) into L2's scorer verbatim, keep
it exact-arithmetic, and get cue-based recall that does not depend on an embedding
model's whims. (The `attributed_to`/`linked_memory_ids` linking is a weaker,
LLM-driven cousin that would inform L4 association, but the deterministic BM25 +
entity fusion is the piece worth stealing outright.)

## ONE mistake worth codifying (as a strain-trial idea)

**Mistake: exact-hash-only dedup + ADD-only means the current value of a fact is
undefined — supersessions and paraphrases both accumulate, and a query for
"the current X" returns contradictions.** This is our **Layer 6 (Contradiction &
Dedup)** failure, and our murk corpus already injects `contradiction` and
`near_duplicate` families — the strain trial extends them to expose exactly
mem0's blind spot.

**Strain-trial idea (targets Layer 6, reuses/extends `corpora/murk/`):**
- *Corpus manipulation:* for a set of `(entity, key)` slots, emit **supersession
  chains** — a sequence of value assertions where each later one supersedes the
  earlier (`name = LGY` → `name = LGS`; `city = Paris` → `city = Berlin`) — and
  **paraphrase near-duplicates**: the *same* fact restated with different wording
  (and therefore a different `md5`), e.g. "User's dog is named Max" vs "Max is the
  user's dog." Record in `ground_truth.json`, per slot: the ordered chain, which
  assertions are supersessions vs paraphrases, and the **single correct current
  value** (the last non-superseded assertion).
- *Assertions:* after ingesting the stream, query "current value of
  `(entity,key)`?" and require the engine to (a) return the **latest
  non-superseded** value, not a set and not a stale one; (b) **collapse
  paraphrases** (count-once, no growth in stored distinct facts per slot); and
  (c) keep the store size **bounded by the number of live slots**, not by the
  number of assertions.
- *Why it bites:* a mem0-style engine fails all three — paraphrases differ in
  `md5` so both persist, contradictory assertions both ADD, and "current value"
  is ambiguous. Our engine must resolve to a single current value (supersession)
  and dedup on meaning, not bytes — which is precisely what Layer 6 certifies.

## Constitutional note (no law-change objection)

No objection to the frozen `BOUNDARY.md`. Mem0 affirms our laws by their absence:
**Layer 6 (contradiction/dedup)** — mem0 has exact-hash dedup only and no
supersession (#4896, #6515); **Layer 3 forgetting + the budget law** — no OSS
decay/eviction, unbounded growth (#4573, #5330); **the provenance law (Layer 7)**
— inferred and user-stated facts share one schema with no source marker; and
**calibration (Layer 6)** — a retrieval similarity score is not a calibrated
confidence. Mem0's open-core split (decay/timestamps behind the platform wall) is
itself a reminder that *lifecycle management is the hard part we are not allowed
to skip*. No change is warranted.

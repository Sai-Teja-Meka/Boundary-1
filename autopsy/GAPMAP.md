# GAPMAP — Phase 0.5 synthesis

`[L0] [GAPMAP]`. Reads all six `autopsy/*/ANATOMY.md` and
`autopsy/theory-actr-soar/BRIEF.md`, plus two pre-write verifications. Closes
Phase 0.5. **Verdict: PROCEED to Phase 1** — two of three novelty axes are
traced-and-verified and jointly sufficient; the third carries a single unverified
dependency (WRIT), flagged below, that must be closed before publication but does
not collapse the positioning.

## Verifications (verify twice, claim once)

- **V1 — "Selective Forgetting" definition.** arXiv 2507.05257 was **not
  fetchable** here (403 on abs and html; egress policy). Grounded instead on the
  in-repo README (fourth competency named **"Conflict Resolution (CR)"**,
  `README.md:19`, commit `455306d`), the query template
  (`utils/templates.py:80`: "find the newest fact with larger serial number"), and
  a consistent secondary characterization (FactConsolidation = counterfactual with
  higher serial; "newer facts have larger serial numbers"). **Ruling:** the field
  defines Selective Forgetting as **supersession / knowledge-update** (answer with
  the newest value), **not** deletion. No code-vs-paper deletion-gap is claimed.
  Therefore: **what the field calls "selective forgetting" is supersession
  reasoning; removal-under-pressure is untested anywhere in the six subjects.**
  (Softer wording used because the paper text itself was unreadable — see the flag
  in §4.)
- **V2 — Generative Agents recency (re-traced).** Re-read `retrieve.py`:
  `new_retrieve` builds `nodes` and calls `sorted(nodes, key=lambda x: x[0])` on
  `x[0] = last_accessed` — **ascending, oldest-accessed first** (`:224–228`);
  `extract_recency` sets `recency_vals = [recency_decay**i for i in range(1, N+1)]`
  (`:145–146`), so with `decay = 0.99` the **first (oldest)** node gets `0.99¹`
  (largest) and the **last (newest)** gets `0.99ᴺ` (smallest); min–max
  normalization then maps **oldest→1, newest→0**. **Confirmed: recency is
  rank-based (not elapsed-time) and inverted.** Claim stands, publishable.

## Naming reconciliation (read before the matrix)

Three ANATOMY files (mem0, graphiti, letta) and some shorthand in this GAPMAP's
inputs say **"L6 Contradiction & Dedup"** and **"L8 Revision & Forgetting."**
Those are **pre-ratification** layer names. In the frozen ladder (`BOUNDARY.md §5`,
post FORGE-CORRECTION) **L6 = Meta-memory** and **L8 = Self-description**, and there
is **no standalone Contradiction or Revision layer.** In the ratified ladder:
- **Supersession / contradiction / "current value among conflicts"** is a facet of
  **L4 Consolidation** (its definition includes *attribute histories*: the newest
  entry is the current value, conflicting entries are the contradiction, and the
  as-of query is L4 reconstruction).
- **Commanded / principled forgetting** is **L3 Forgetting** (eviction under
  pressure), with as-of audit supplied by L4.

This GAPMAP uses the **frozen names** throughout. The pre-correction references in
the committed ANATOMY files are a **documentation erratum** to correct at the next
non-frozen doc pass — **not this session** (autopsies unchanged; frozen is frozen).

---

## 1. THE MATRIX

Legend: **IMPL** implemented · **PART** partial (what's missing noted) · **ABS**
absent (search performed). Cells cite `file:line` at the column's commit. Engine
columns are scoped to the traced core.

**Engines × our nine layers**

| Layer | GA — `fe05a71` (reverie/backend_server) | Mem0 **OSS core** — `d6d89c9` (mem0/memory) | Graphiti **core** — `3bb2d0b` (graphiti_core defaults) | Letta — `b76da90` (letta/) |
|---|---|---|---|---|
| **L1 Retention** | PART — append-only store (`associative_memory.py:153–196`), persisted (`:112–150`); no budget-refuse, unbounded | PART — vector rows (`main.py:999–1025`), raw store (`:850–884`); no budget-refuse; `expiration_date` **hides** (`:417`) | PART — episodic+entity store, bitemporal ts (`nodes.py:318`, `edges.py:263`); read-by-time via `valid_at`; no budget-refuse | PART — 3 tiers (core Blocks / recall msgs / archival passages); char-limit **advisory, not enforced** (`core_tool_executor.py:319–344`); no budget-refuse |
| **L2 Recall** | PART — keyword inverted index (`associative_memory.py:58–60`), but ranking is embedding-LLM + **rank-inverted recency** (`retrieve.py:132–152`, V2) | PART — deterministic **BM25 + entity-boost** present (`main.py:1649–1657`, `text_lemmatized :1001`) but fused w/ semantic; no isolated deterministic mode | **IMPL** (closest of all) — no-LLM-default hybrid **BM25+cosine+BFS** reranked RRF/MMR/node-distance (`search.py:50–65, 98`); default still uses embedding cosine | PART — `conversation_search` + archival vector search (`core_tool_executor.py:81, 278`); vector = model-dependent; no deterministic index |
| **L3 Forgetting** | ABS — `expiration` written, never read (grep; ANATOMY) | ABS (OSS) — decay platform-gated, **raises** (`notices.py:49`, `main.py:444`); hide≠evict | ABS — invalidate-not-evict, no TTL/decay (`edge_operations.py:569–570`; grep) | PART — overflow **demotion** (`summarizer.py:244–342`): evict-from-context, retain-in-recall; **no** importance/age/budget auto-eviction |
| **L4 Consolidation** (incl. supersession) | PART — reflection derives thought nodes w/ `filling`/`depth` (`reflect.py:99–132`); ADD-on-top, no compression, no fidelity-floor, no supersession | ABS — additive only; contradictions **coexist** (`prompts.py:472`; #4896); no summarize-into-fewer | PART — community `label_propagation`+LLM summaries (`community_operations.py:80,174`) **and** bitemporal attribute-histories/supersession (`edge_operations.py:538–573`); summaries LLM, membership drifts, default read ignores `invalid_at` | PART — sleeptime `rethink` reorganizes blocks (`sleeptime_v2` prompt) — **destructive**, unversioned; no fidelity-floor reconstruction |
| **L5 Prospection** | ABS — time-indexed schedule only (`plan.py:400–520`); no condition trigger | ABS — no trigger registry | ABS — `valid_at`/`invalid_at` are past times, not future triggers | ABS (certified) — schedule/turn-count sleeptime, not content-conditioned (grep `base.py`/`memory.py`) |
| **L6 Meta-memory** | ABS — `poignancy` = importance, not confidence; no calibration | ABS — retrieval `score` ≠ calibrated confidence (`main.py:1684`) | ABS — RRF/cosine scores ≠ calibrated confidence | ABS — no confidence on edits or reads |
| **L7 Generation** (tagged+provenance) | PART — `filling`/`depth` provenance DAG at write (`associative_memory.py:207–210`), **unbound at read**; no generation/tagging | ABS — inferred≡stated, source erased (`main.py:864–869`); no generation/tagging | PART — first-class bidirectional provenance (`edges.py:267 ↔ nodes.py:325`), **carried not enforced**; no generation/tagging | ABS — only actor-id (`block.py:73–74`); summary masquerades as user turn (`summarizer.py:220`); no generation/tagging |
| **L8 Self-description** | ABS — no introspection-from-state query construct | ABS | ABS | ABS |
| **L9 Birth** | ABS | ABS | ABS | ABS |

**One-line reading:** every engine is a **PART-L1 / PART-or-IMPL-L2 /
mostly-ABS-below** system. No subject reaches L5, L6, L8, or L9 at all; L3 and L7
are PART at best and never *bound*; L4 is where the strongest prior art lives
(Graphiti's bitemporal supersession, GA's derivation DAG).

**Evaluators (separate — they score capabilities, they do not implement layers)**

| Evaluator (commit) | Layers it exercises | Judge mechanism | Abstention scored? | Impossibility gate expressible? |
|---|---|---|---|---|
| **MemoryAgentBench** `455306d` (MIT code; dataset license separate) | L1/L2 (Accurate Retrieval), **L4-supersession** (Conflict Resolution / FactConsolidation), L2/L4 (Long-Range), test-time-learning (ICL) | **code** substring/exact/Recall@5 for the 4 competencies (reproducible) **+ gpt-4o LLM-judge** for LongMemEval/InfBench (uncached, `'yes'`-substring, `longmem_qa_evaluate.py:168` — **not** reproducible) | **NO** — no abstention/humility category | **NO** — flat `accuracy(method,task)` across independent tracks; per-baseline dispatch (`agent.py:64+`), no capability-cap, no upper-bound assertion |
| **LoCoMo** `3eb6f2c` (CC BY-NC 4.0) | L2 (single/multi-hop), L1 (temporal/as-of), open-domain (world-knowledge leak), **adversarial** (abstention) | **official = token-F1 overlap** (`evaluation.py:209–214`) + open-domain scores only first `;`-clause (`:203–204`) + adversarial **containment** (`:217–221`); **downstream = gpt-4o-mini LLM-judge** (external, not in-repo; Penfield-measured) | **Tested but retired** — adversarial (cat 5) scores abstention, yet the headline F1 is over **1540 = cats 1–4**, excluding the 446 adversarial items | **NO** — static answer-key dataset; no capability tiers |

---

## 2. THE TWO THESES

**Engines — "recorded but never binding."** Every engine writes the metadata that
would make it correct, then never reads it where it counts.
- **GA:** `expiration` is written on every thought and round-tripped through
  save/load (`associative_memory.py:79–82, 125–128`) but **never read to evict** —
  the field exists solely to be ignored.
- **Mem0:** provenance is **erased at the door** — the extraction prompt rewrites
  assistant content into user-framed statements and the default path keeps no
  source flag (`main.py:864–869`; `prompts.py:488`); and the paper's whole
  ADD/UPDATE/DELETE machinery is **dead code** (`prompts.py:176, 406`, not imported
  by `main.py`; #4896).
- **Graphiti:** a full bitemporal model is maintained on write, but **default reads
  surface superseded edges** — the temporal `SearchFilters` default `None`
  (`search_filters.py:62–65`), no default `WHERE`; and `reference_time` is
  write-only (#1661).
- **Letta:** the overflow summary is injected **as a `role=user` message**
  (`summarizer.py:220`) — a lossy machine artifact wearing a human turn's clothes —
  and self-edits get **no semantic validation** (`core_tool_executor.py:328–344`;
  #3388, #3397).

The four codebases, traced independently, fail the *same* way: the citation graph,
the source tag, the `invalid_at`, the derived-vs-original marker all **exist and
none is binding at read or write time.** Our provenance law (§4.2), L6 answer
contract, and L7 tagging exist precisely to make these bindings mandatory.

**Evaluators — "overlap-or-LLM graded, abstention retired."** The two benchmarks
grade *overlap* or defer to an *unreproducible model*, and both sideline the one
thing that tests honesty.
- **MemoryAgentBench** keeps its four headline competencies on deterministic code
  judges (good) but still routes LongMemEval/InfBench through an **uncached,
  single-call, `'yes'`-substring gpt-4o judge** (`longmem_qa_evaluate.py:96, 163,
  168`), and it has **no abstention category** at all.
- **LoCoMo's official judge is token-F1 overlap** (`evaluation.py:209–214`), with
  open-domain scoring only the first `;`-clause (`:203–204`) and adversarial scored
  by **containment** on two magic phrases (`:217–221`); its **adversarial category
  — the only one testing calibrated abstention — is excluded from the headline
  1540**. The **gpt-4o-mini judge is downstream, not in-repo** (Penfield-measured:
  62.81% of wrong-but-adjacent answers accepted). *Keep this attribution split
  exact: official LoCoMo = F1; the lenient LLM judge is a third-party add-on.*

Our answer: exact, exclusive, deterministic code grading (the run.py rule below),
abstention scored first-class by the §3.0 table, and the abstention/humility
trials **central**, not retired.

---

## 3. THE STEAL LIST (deduplicated; commit-pinned; ratified target layer)

| # | Technique | Source (commit) | Target (ratified) | Rederivation constraints |
|---|---|---|---|---|
| S1 | `filling` + `depth` derivation DAG | GA `fe05a71` `associative_memory.py:207–210` | **L7** (provenance/tagging) + **L6** (depth→confidence prior) | `filling` = our provenance `support` (sorted non-neg int `t`'s, §4.2 schema); `depth` = integer derivation distance; **binding at read** (an answer must carry support — unlike GA's un-read graph); no floats |
| S2 | BM25 + entity-boost hybrid recall | Mem0 `d6d89c9` `main.py:1649–1657`, `:1001` | **L2** | **lemmatization → our grammar-vocabulary token normalization** (no NLTK/spaCy — import whitelist §2.5 forbids them); tokens from our fixed grammar vocab, normalized by exact rules; BM25 term-freqs integer, idf rational — scored in `Fraction`, no floats; entity-boost = exact adjacency from our event graph |
| S3 | Bitemporal **invalidate-not-delete** | Graphiti `3bb2d0b` `edges.py:263–280`, `edge_operations.py:538–573` | **L4** (attribute histories: current-value + as-of reconstruction), informing **L3** (invalidate = demote-not-destroy) | the four marks become **integer logical-`t` stamps** set by deterministic comparison (§2 — no wall clock, no floats); **the LLM date-interpretation cost Graphiti pays, we never incur** (`t` assigned at ingest, §1.3); supersession decision is deterministic (max-`t` / interval compare), never a model call *(pre-correction autopsies said "L6/L8")* |
| S4 | Hot/cold **demotion, not deletion** | Letta `b76da90` `summarizer.py:244–342` | **L3 / L4** | **UNCONSTITUTIONAL as-is** — an unbounded cold tier violates the budget law (§4.1 binds total occupancy). Two constitutional forms, **ASCEND chooses**: **(a) two-budget design** — bounded hot-tier budget *and* bounded cold-tier budget, both refuse-on-exceed; or **(b) demotion-into-consolidated-form** — eviction compresses the item into an L4 schema so cold-tier growth is bounded by consolidation (L3 feeds L4). Record both; do not pick now |
| S5 | Serial-supersession facts, exact integer answer key | MAB `455306d` `templates.py:80` | **L4 corpus** (attribute histories / conflict) | serial = our integer logical `t`; `ground_truth` = value at **max-`t`**; exact code-checkable key (no LLM); counterfactual framing ("answer only from the pool") *(pre-correction: "L6 corpus")* |
| S6 | Adversarial construction (mis-attribution / false-presupposition → abstain) | LoCoMo `3eb6f2c` (CC BY-NC) | **abstention corpus family** (humility, §3.0) | **techniques rederived from OUR grammar, never their text** (CC BY-NC bars content reuse): fact by speaker B + question about speaker A; question presupposing an absent fact — generated over chronicle/sessions entities, keyed **unanswerable**, deterministic + code-graded |
| S7 | ACT-R base-level activation | BRIEF (Anderson & Schooler 1991; Anderson & Lebiere 1998) | **L3** | **ordering/threshold rederivation only** — importance = exact `Fraction` recency×frequency surrogate (harmonic `d=1`: `w = Σ 1/(T−t_j+1)`); only the induced ordering + retention threshold bind L3; the float `d` and numeric activation are never reproduced |
| S8 | Activation → retrieval-probability (pedigree) | BRIEF (Anderson & Lebiere 1998) | **L6** | inherit the *form* confidence = f(structural evidence); **calibrate to trial ground truth** (Brier/ECE/AUROC, §3.4), **not** fit-to-human parameters |

---

## 4. POSITIONING vs MemoryAgentBench and WRIT

Three novelty axes, each with its now-verified (or flagged) evidence.

**(a) Impossibility-gated ordered layers.** *Verified.* MemoryAgentBench is a
**flat, parallel-track leaderboard**: four independent dataset configs scored as
`accuracy(method, task)`, dispatched per-baseline (`agent.py:64+`
`_initialize_{…}_agent`), with **no capability-cap on the system under test and no
upper-bound assertion**. It therefore **cannot express an impossibility gate** —
"a system frozen at capability N−1 must score ≤ a ceiling on task N" has no analog
in its architecture. Our humility trial class (`make_engine(layer_cap = N−1)` must
score ≤ ceiling, §5/§6) is a construct the field's leading benchmark structurally
lacks. **This axis stands on a traced finding.**

**(b) Self-tagged recall-vs-generation provenance.** *Provisional — flagged.* Our
design makes self-tagging a **law**: L7 requires `tagging = 1000` and
`self-pollution promotion = 0` (three deep), enforced by a deterministic check, and
§4.2 makes provenance binding. The closest prior art is **WRIT**, which — *per the
characterization supplied to this task* — is **proposal-stage, flat, and uses
external scoring** (a judge decides whether a system distinguished recall from
generation), rather than an engine-internal self-tagging obligation checked
deterministically. **Honest flag (phase-gate):** I **could not independently verify
WRIT** in this environment (arXiv/web egress limits; no search hit), so this axis
rests on the *provided* characterization, not my own reading. If a future check
finds WRIT already specifies a self-tagging *law* with a gated/deterministic check,
axis (b) weakens from "novel framing" to "we operationalize WRIT's proposal" —
still a contribution, but a **re-scope, not a quiet reword.** The positioning does
**not collapse** without (b): it stands on (a), (c), and the removal-untested axis.

**(c) Prospective memory as a scored capability.** *Verified.* No subject
implements it; **Letta is certified ABSENT** with the precise distinction —
**schedule/turn-count-triggered** sleeptime maintenance vs **condition-triggered**
`intend(condition → event)` (grep over `functions/function_sets/base.py`,
`schemas/memory.py`, the sleeptime group → nothing). The other three are ABSENT
too. Our L5 gates it as an exact capability (trigger-precision = trigger-recall =
1000, exactly-once, dup-fire = miss = 0). **This axis stands.**

**(+ a fourth, from V1) Forgetting-under-pressure is untested anywhere.** The
field's "Selective Forgetting" (MAB Conflict Resolution) is **supersession
reasoning**, and every other subject only *invalidates* or *demotes* — **no
subject or evaluator tests eviction/removal under a hard budget.** Our L3
(importance-weighted coverage ≥ 850‰ at 10× budget) scores a capability the
literature does not.

**Phase-gate check, stated plainly:** axes (a), (c), and (+) survive V1/V2 and the
traced findings. Axis (b) is sound under the supplied WRIT characterization but
carries **one unverified dependency**; the required action before publication is to
fetch/verify WRIT, not to reword. Because the positioning is over-determined by the
verified axes, **the verdict is PROCEED**, with WRIT-verification logged as the one
open pre-publication item.

---

## 5. LANGMEM RULING

**LangMem stands; it enters at PACKAGE as an adapter stub — no ecosystem-default
7th autopsy next session.** Reasoning from the matrix, not completism: the four
engine columns already **saturate the "LLM-extraction + vector store,
recorded-but-not-binding" design cell** — four independent codebases converge on
PART-L1 / PART-L2 / ABS-L3,L5,L6 / PART-or-ABS-L7. From its public documentation
LangMem is another instance of exactly that cell (LLM-extracted memories, vector
retrieval, prompt-driven updates), so a seventh autopsy would **confirm, not
extend**, the pattern — the matrix's marginal information gain is ~0. The only
thing that would justify a column is structural novelty (a *typed* provenance, a
*real* eviction policy, a *condition-triggered* intention) that the matrix does not
already contain; there is no evidence LangMem has any of those. Decision: adapter
stub at PACKAGE, and revisit **only** if a later DOGFOOD/ASCEND session finds
LangMem doing something the matrix has not already saturated.

---

## Appendix — LoCoMo corpus-rule compliance

The three rules from `autopsy/locomo/ANATOMY.md` are corpus-doctrine compliance
checks (they land on `corpora/`, not the engine or `run.py`). Status of the frozen
Phase-0 corpora (`chronicle`, `sessions`, `murk`, `l3stream`) — **no corpus edits
now; frozen is frozen**:

1. **Grounding** (answer entailed by non-empty cited evidence `t`'s). Existing
   corpora are **event streams, not answerable-QA sets**, so the rule has no
   answerable items to violate yet; `murk/ground_truth.json` already demonstrates
   the discipline (every injected defect paired with its event `t`'s and refs).
   **Compliance ops trial to be authored at the first answerable-QA corpus**
   (ASCEND L1/L2): `assert len(support) > 0 and answer_derivable(answer,
   events[support])`.
2. **Canonical keys** (canonical strings; temporal answers absolute integer-`t`).
   Existing corpora **comply by construction**: `corpora/canon.py` enforces
   canonical JSON + the no-float type gate, byte-match freezes it, and all string
   values come from **fixed ASCII grammar vocabularies** (no free text → no
   zero-width/run-together defects possible). No corpus yet carries a *temporal
   answer key*. **Add a string-content canonicalization + `is_absolute_t` ops trial
   at the first free-text / temporal-answer corpus.**
3. **Closed-world + structurally-derived category + exact/exclusive grading.**
   Existing corpora **comply by construction**: entities are synthetic integer ids
   (no world-knowledge shortcut); `murk` defect *types* are structurally generated
   and recorded (not hand-labeled); and the suite already grades by exact code
   assertion (the run.py rule). **Add `assert declared_category == derived_category`
   + synthetic-id + scalar-exact-key ops trials at the first categorized-QA
   corpus.**

**The run.py grading rule (from MemoryAgentBench), restated for the record:**
correctness is decided **only** by exact, exclusive, deterministic code comparison
— never substring/containment, never an LLM judge; a response containing the
correct answer *alongside* a contradicting one is **WRONG** (§3.0). This binds the
runner at first ascension; it is not a corpus rule but is recorded here so the
compliance story is complete.

---

## Constitutional note

No objection to the frozen `BOUNDARY.md`; the one integrity item found — the
pre-correction "L6/L8" labels in three ANATOMY files — is an **erratum in
non-frozen documentation**, reconciled above and to be fixed at the next doc pass,
not a fault in the constitution. Phase 0.5 closes: the field records the right
metadata and never binds it, grades overlap and retires abstention, tests
supersession and never removal, and cannot gate capability — and every one of those
gaps is a law we already wrote. **Proceed.**

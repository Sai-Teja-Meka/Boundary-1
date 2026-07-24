# Layer 2 — Recall (the deterministic floor of association)

`[L2] [ASCEND]`. The second capability of Boundary-1: Memory. Layer 1 could
return an event only by the `t` it was assigned; Layer 2 returns an event by
**what it contains** — `recall(cue)` against a deterministic associative index.
This document states **exactly what Layer 2 can and cannot express**. Layer 3's
humility trial is written against the boundary drawn here.

Intellectual pedigree: cue-dependent retrieval and spreading activation (Tulving
& Thomson 1973; Anderson 1974), rederived as the **surface/base-level** half
only — see the deterministic-floor note below (THEORY §2). The index architecture
is Mem0's **BM25 + entity-boost** hybrid (GAPMAP S2), rebuilt under our physics:
no lemmatizer, no embedding, no float.

Code (frozen after this session, §9):
- `core/layers/l2_recall.py` — the `L2State` (Layer-1 fields **plus** the index),
  the deterministic index (atoms, id-anchored n-grams, MinHash), `recall`, and
  the generic-interface binding + checksummed snapshot/restore (index included).
- `trials/adapters/l2.py` — the Layer-2 adapter. The Layer-1 engine
  (`core/engine.py`, `core/layers/l1_retention.py`) is **untouched**; its adapter
  still binds `core.engine`, and `anchors/l1.json` replays through it unchanged.

## The recall verb (§5 L2)

| verb | signature | meaning |
|------|-----------|---------|
| `recall` | `(state, cue) -> Answer` | recover the single stored event that contains the whole content **probe** `cue`; abstain if none does or several do |

`cue` is a partial payload — e.g. `{"entity":7,"key":"region","val":"north"}` —
and **never carries `t`**. The Answer is the §7.2 object: a hit returns the exact
event record `{"payload":…,"t":…}` with a `recall` provenance tag
(`support=[t]`); a miss or an ambiguity returns a scored **abstention**, never an
exception (§7.3). The five Layer-1 verbs remain available and unchanged.

## The index (lives in state, counts against budget)

  * **Atoms** — field-qualified tokens (`kind=attr`, `entity=7`, `key=region`,
    `val=north`) plus a cross-field adjacency atom `id#7` for the id-bearing
    fields (`entity`/`src`/`dst`/`sid`). Field-qualification replaces NLTK
    lemmatization (whitelist, §2.5): the grammar vocabularies are fixed lowercase
    ASCII, so normalization is lowercase + qualify + id-adjacency — deterministic,
    library-free, derived from `corpora/*/grammar.md`.
  * **n-grams** — id-anchored bigrams `id#7^key=region` couple an entity to each
    fact about it (Mem0's entity-boost as co-occurrence), rarer and more
    discriminative than either atom alone.
  * **MinHash** — K salted-SHA-256 minima per event (integer-only), so verbatim
    near-duplicates collide exactly and the ambiguous case is recognizable.
  * **Per-item scoring** — a candidate scores `Σ_{a ∈ cue ∩ item} idf(a)` in exact
    `Fraction`, `idf(a) = 1/df(a)` a function of the atom's own document frequency
    **alone**. Rare atoms dominate (BM25's shape); irrelevant decoys cannot move a
    fixed cue's ranking (the GA decoy-invariance strain).

The index is **state**: every posting cell and signature cell is added to
`occupancy`, and a write whose event **plus its index cost** would exceed the cap
is refused deterministically (§4.1). B = 1000 at the ascension scale, and the
budget-refusal path is exercised with the index counted (`ops/l2`). The snapshot
checksum covers **all** of state; `restore` also rederives the index from the log
and rejects any divergence (`strain/l2`).

## What Layer 2 CAN express

- **Associative recall.** From a `t`-free content cue against grammar-controlled
  distractors (unique target; ≥2 same-entity / same-key / same-val distractors),
  recall recovers the exact target: **cue-C = 1000, F = 1000, B = 1000** on the
  ascension task set (gate: cue-C ≥ 900, F ≥ 950, B = 1000). Matching any single
  shared atom would land on a distractor — only combining the whole probe wins.
- **Honest abstention over guessing.** A cue matching no event abstains
  (unanswerable → 1000 under §3.0); a cue matching a verbatim near-duplicate
  abstains rather than fabricate one `t` (its MinHash collision is the tell). No
  cue task is ever answered wrongly (fabrication = 0).
- **Determinism under the index.** Two identical ingest sequences produce
  byte-identical snapshots (index included); the index is a pure function of the
  stored bytes. Recorded as `anchors/l2.json` (replay under `layer_cap = 2`).
- **The budget still binds.** The index is affordable: it counts against
  occupancy and the cap holds absolutely, refusing deterministically under
  pressure — Layer 2 never evicts to make room.

## What Layer 2 CANNOT express (the boundary for Layer 3+)

- **The deterministic floor — surface overlap, deliberately not semantic spread**
  (lifted from THEORY §2). ACT-R's spreading activation adds, on top of base
  level, learned real-valued associative strengths `S_ji` — graded semantic
  relatedness accumulated from experience. Our index models only the
  **base-level / surface** half: it recovers a cue's target by **lexical /
  structural overlap** (shared qualified atoms and id-anchored n-grams), and it
  stops there. It does **not** estimate learned semantic association, does not
  spread activation through a graded network, and assigns no float strengths.
  This is intentional. Semantic spread is exactly the component that makes recall
  model-dependent and non-reproducible — the failure our engine autopsies found
  again and again, retrieval quality riding on an embedding model's whims.
  Excluding it is what makes Layer 2 a **deterministic floor**: an LLM-free,
  exactly-reproducible recall channel a later layer may *augment* but must never
  *depend on* for correctness. A cue that shares no surface atom with its target
  (a synonym, a paraphrase, a semantic neighbor) will not be recalled — and that
  is the honest boundary, not a bug.
- **No forgetting / eviction — the likely L3 humility seam.** Under pressure
  Layer 2, like Layer 1, **refuses**: a write whose event-plus-index cost would
  exceed the cap returns `t = None`, and nothing admitted is ever dropped.
  Fed a stream larger than the budget, a recall engine therefore **fills to the
  cap and then refuses the rest**, keeping the *earliest* items regardless of
  their importance. It has no eviction policy, no importance ranking, no decay —
  so it cannot preserve a late-arriving important mass at the expense of early
  unimportant fill. That **fill-then-refuse-under-pressure** behavior is the exact
  gap **Layer 3 (Forgetting)** must cross, and it is the seam its humility trial
  will cap against (`make_engine(layer_cap = 2)` must score weighted-C ≤ 300 on
  the 10× pressure stream, per §5 L3 and `humility/l3/IMPOSSIBILITY.md`).
- **No consolidation.** Near-duplicates and contradictions are indexed and stored
  **verbatim and side by side**; recall abstains on a near-duplicate rather than
  reconciling it into a single current value. Deriving entity summaries,
  attribute histories, or a "current value among conflicts" is **Layer 4**.
- **No prospection, meta-memory, generation, or binding provenance.** Confidence
  is emitted (a structural margin) but **ungated** until Layer 6 (§3.4); the
  `recall` provenance tag is attached but neither required nor scored until Layer
  7 (§4.2). No `intend`, no calibrated confidence model, no `generate`, no
  `generated` lineage tag — Layers 5, 6, 7.

## Reading list for the next session

Per `CLAUDE.md §1`, the next session reads this README before acting. The one
sentence to carry forward: **Layer 2 recalls by surface overlap through a
deterministic index that lives in state and counts against budget, answering only
when one event matches the whole cue and abstaining otherwise — it associates but
does not spread semantically, and under pressure it still refuses rather than
forgets.**

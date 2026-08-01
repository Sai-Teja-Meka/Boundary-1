# core/layers/

Per-layer engine code, one module per claimed layer (`l1_retention.py`, …), each
with its own `README-lN.md`. A layer is laid down by the `FORGE` that first
builds it and claimed by the `ASCEND` that clears its gate.

Claimed layers:
- **Layer 1 — Retention** — `l1_retention.py` (`README-l1.md`). The honest floor:
  write / read-by-time / read_range / snapshot / restore, budget law binding.
- **Layer 2 — Recall** — `l2_recall.py` (`README-l2.md`). Associative
  `recall(cue)` via a deterministic index (field-qualified atoms, id-anchored
  n-grams, MinHash) that lives in state and counts against budget. Built on the
  frozen Layer-1 primitives; edits none of them.
- **Layer 3 — Forgetting** — `l3_forgetting.py` (`README-l3.md`). Principled
  eviction under 10× pressure: an exact ACT-R base-level importance ordering
  (grammar weight × distinct-reference count × harmonic logical-`t` recency), a
  total tie-break, a single-posting handle index, and an aggregated per-`t`-range
  forgetting record — all inside a budget the state-composition arithmetic of
  `README-l3.md §0` fixed before the code was written. Built on the frozen
  Layer-1 primitives; edits none of them, and does not edit Layer 2.
- **Layer 4 — Consolidation** — `l4_consolidation.py` (`README-l4.md`).
  Episodic→semantic derived schemas with reconstruction: every event is folded at
  the door into an interval chain (when it supersedes something) or a typed row
  against a learned shape (when it does not), and only if the fold **inverts** to
  the byte-exact payload; the episode is then released — *demotion*, GAPMAP S4
  form B, the debt `README-l3 §0.4` recorded — so at a quarter of the raw
  episodic footprint the whole semantic battery is answered exactly and
  reconstruction still returns 19 286 of 20 000 events. Built on the frozen
  Layer-1 primitives and the frozen Layer-3 eviction law; edits neither, and
  `make_engine(3)` **is** the Layer-3 engine (§7.4).
- **Layer 5 — Prospection** — `l5_prospection.py` (`README-l5.md`). The first
  capability that is not a fold over the past: an intention arrives as an
  ingested payload under a declared reading of the frozen grammar, is armed only
  if its condition is **readable** and its payload **inverts**, and is evaluated
  against every later event — firing **exactly once**, emitting the intended
  payload at a logical time of its own (`R6` clause 2: one caller `ingest`
  advances `next_t` by `1 + f`). The pending set and the fired ledger are outside
  every eviction phase, because `miss = 0` and `dup-fire = 0` are identities;
  what gives way is the episodic tier, and the promise's own episode is booked as
  a loss the moment firing makes it unregenerable. `L5State` is a **subclass** of
  the frozen `L4State`, so Layer 4 is inherited rather than re-implemented, and
  `make_engine(4)` **is** the Layer-4 engine (§7.4).

Once a layer is claimed its code is **frozen**: it is never edited (§9). A newer
layer builds on the frozen layers beneath it.

Per `CLAUDE.md §1`, every session reads the most recent layer's README
(currently `README-l5.md`) before acting.

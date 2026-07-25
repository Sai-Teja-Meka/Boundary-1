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

Once a layer is claimed its code is **frozen**: it is never edited (§9). A newer
layer builds on the frozen layers beneath it.

Per `CLAUDE.md §1`, every session reads the most recent layer's README
(currently `README-l3.md`) before acting.

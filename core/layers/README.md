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

Once a layer is claimed its code is **frozen**: it is never edited (§9). A newer
layer builds on the frozen layers beneath it.

Per `CLAUDE.md §1`, every session reads the most recent layer's README
(currently `README-l2.md`) before acting.

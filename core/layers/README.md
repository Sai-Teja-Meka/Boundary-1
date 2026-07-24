# core/layers/

Per-layer engine code, one module per claimed layer (`l1_retention.py`, …), each
with its own `README-lN.md`. A layer is laid down by the `FORGE` that first
builds it and claimed by the `ASCEND` that clears its gate.

Claimed layers:
- **Layer 1 — Retention** — `l1_retention.py` (`README-l1.md`). The honest floor:
  write / read-by-time / read_range / snapshot / restore, budget law binding.

Once a layer is claimed its code is **frozen**: it is never edited (§9). A newer
layer builds on the frozen layers beneath it.

Per `CLAUDE.md §1`, every session reads the most recent layer's README
(currently `README-l1.md`) before acting.

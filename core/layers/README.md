# core/layers/

Per-layer engine code, one subdirectory per claimed layer (`layer1/`, `layer2/`,
…), each with its own `README.md`. Added one layer at a time by `ASCEND` moves.

Empty at Phase 0 — the engine does not exist yet. Once a layer is claimed its
code is **frozen**: it is never edited (§9). A newer layer builds on the frozen
layers beneath it.

Per `CLAUDE.md §1`, every session reads the most recent layer's `README.md`
before acting.

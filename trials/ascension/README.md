# trials/ascension/

Capability trials. Passing a layer's ascension trials at or above its
`BOUNDARY.md §5` gate entitles the engine to claim that layer. Scored by the
four measures (§3).

Populated by `ASCEND` moves, one layer at a time. Each layer's ascension trials
are paired with a humility trial (`trials/humility/`) that runs the **same tasks**
against `make_engine(layer_cap = N−1)` and asserts the capped engine scores at or
below the layer's humility ceiling (§6), proving the gate requires the new
capability.

Present:

- `l1/t_retention.py` — Layer 1, Retention.
- `l2/t_recall.py` — Layer 2, Recall.
- `l3/t_forgetting.py` — Layer 3, Forgetting, with `l3/ATTAINABILITY.md`.
- `l4/` — Layer 4, Consolidation, **Stage A only**: `ATTAINABILITY.md`,
  `t_attainability.py` and `RULING-R4-DRAFT.md`. There is **no ascension battery
  and no engine** here. The arithmetic found the ratified gate unattainable on
  the frozen chronicle family under any policy (oracle `C ≤ 735`, `F ≤ 683`
  against `850` / `900`), froze `corpora/l4stream` as the corpus that admits it
  (an *exhibited* state scores `C = 1000`, `F = 984` at footprint `250‰`, against
  a best baseline of `249` / `327`), and stopped — the corpus binding is a
  human's to settle, and the proposed holding is the R4 draft. Until a ruling
  exists, no Layer-4 gate binds on anything.

**`ATTAINABILITY.md` is mandatory from `BOUNDARY-RULINGS.md` R2**: a gate must be
shown to lie strictly below the oracle ceiling and strictly above every named
capability-free baseline on its binding corpus, and that arithmetic must be
computed and recorded **before the gate binds** — the ascension-side counterpart of
`humility/`'s `IMPOSSIBILITY.md`. R2 also fixes the standing order of an `ASCEND`:
attainability arithmetic → trials → engine. R2 binds every *future* gate, so
Layers 1–2 predate it and are not retroactively invalidated by it.

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
- `l4/` — Layer 4, Consolidation, **Stages A, B and C; the gate is cleared.**
  - Stage A (`ATTAINABILITY.md`, `t_attainability.py`, `RULING-R4-DRAFT.md`):
    the arithmetic found the ratified gate unattainable on the frozen chronicle
    family under any policy (oracle `C ≤ 735`, `F ≤ 683` against `850` / `900`),
    froze `corpora/l4stream` as the corpus that admits it (an *exhibited* state
    scores `C = 1000`, `F = 984` at footprint `250‰`, against a best baseline of
    `249` / `327`), and stopped for a human. `BOUNDARY-RULINGS.md R4` has since
    ratified all three questions it put up, and the draft is superseded by the
    frozen entry.
  - Stage B (`t_consolidation.py`): the Q1–Q4 battery, applying the ratified
    gate (`footprint ≤ 250`, `F ≥ 900`, `C ≥ 850`, `B = 1000`) to an engine on
    `corpora/l4stream`, with chronicle and murk as ungated diagnostics on R1
    clause 5's conditional arithmetic-skip. Every trial in it was engine-gated
    and skipped until Stage C. It deliberately does not re-assert Stage A's
    witness or baselines — one fixture, one truth — and its docstring names the
    trial that owns each.
  - Stage C (`core/layers/l4_consolidation.py`, `core/layers/README-l4.md`):
    the engine. The battery above measures **footprint 250‰, C = 1000,
    reconstruction F = 968, B = 1000** on `corpora/l4stream` against a gate of
    `250 / 850 / 900 / 1000`, with `wrong = 0` and `fabricated = 0`; chronicle
    and murk stay ungated diagnostics and are scored (`671 / 699` and
    `695 / 708`) with the budget law and the no-fabrication rule binding on them.
    The design arithmetic is `ops/l4/t_l4_composition.py`; the strains are
    `strain/l4/`; the state is anchored in `anchors/l4.json`.

**`ATTAINABILITY.md` is mandatory from `BOUNDARY-RULINGS.md` R2**: a gate must be
shown to lie strictly below the oracle ceiling and strictly above every named
capability-free baseline on its binding corpus, and that arithmetic must be
computed and recorded **before the gate binds** — the ascension-side counterpart of
`humility/`'s `IMPOSSIBILITY.md`. R2 also fixes the standing order of an `ASCEND`:
attainability arithmetic → trials → engine. R2 binds every *future* gate, so
Layers 1–2 predate it and are not retroactively invalidated by it.

# `trials/inheritance/` — the layers below, re-asked of the engine above

**Debuted by `[L3] [ASCEND]` layer-4 consolidation, Stage B.** The class is
standing from that session forward: **every future ASCEND extends it**, and
nothing in it is ever removed.

## The charter, in one sentence

For each layer `N` being ascended to, the inheritance battery replays the
**ratified batteries of layers `1 … N−1`** against the *current* engine at
`layer_cap = N`, on **in-budget** substrates, and re-applies those layers' own
`§5` gates — so a new capability can never be bought with an old one.

## Why the §6 classes do not already cover this

`BOUNDARY.md §6` names six classes, and the gap between three of them is exactly
this one:

| class | what it proves | why it is not this |
|---|---|---|
| `ascension/` | layer `N` clears layer `N`'s gate | says nothing about layers below `N` |
| `humility/` | `make_engine(N−1)` cannot clear layer `N`'s gate | the *capped* engine, on the *new* battery — the opposite direction |
| `anchors/` | the older engines' exact behaviour never changed | replays through the **older adapters** (`anchors/l1.json` runs against `adapters/l1`), so a Layer-4 engine that lost `read_range` would leave every anchor green |

The hole is specific and it is not hypothetical: at Layer 3 the eviction path is
*allowed* to drop, at Layer 4 the consolidation path is *designed* to summarize.
An engine that folded in-budget episodes into a derived schema would score well
on its own layer's battery, keep every anchor green (those replay a different
program), and have silently repealed `§5 L1`'s `F = 1000`. Inheritance is the
trial that goes red for it.

## The rules of the class

1. **In-budget, always.** Each substrate is replayed at a cap that is a declared
   multiple of its own raw episodic footprint (`INBUDGET_MULTIPLE`), so no
   refusal, eviction or lossy answer can be blamed on the budget law. Pressure
   is the *other* classes' business. **No pressure, no excuse.**
2. **The frozen batteries, imported — never re-expressed.** The Layer-2 cue
   tasks are `_l2tasks`/`_l2score`, the Layer-3 tasks are `_l3tasks`/`_l3score`
   — the very modules the ascension and humility trials of those layers score
   with. Where a layer has no shared task module (Layer 1's verbs live in the
   frozen `ops/l1/t_verbs.py`, which speaks to `adapters/l1` directly), the
   battery is re-expressed against the generic interface and the file says so.
3. **The old gates, not new ones.** Every threshold this class applies is a
   ratified `§5` clause of an *older* layer, registered in
   `laws/t_rulings.py`'s `AUTHORIZED_GATES` against that clause. The class
   introduces no measure and no threshold of its own — where a layer's inherited
   claim is exactness rather than a threshold (nothing is under pressure, so
   everything must be recalled), it is asserted as an identity and not as a
   gate.
4. **Engine-gated until the layer's engine exists.** A battery for layer `N`
   skips until `trials/adapters/l<N>.py` exists, then holds forever. Each class
   directory also carries at least one **engine-free** trial asserting that the
   inherited batteries are the frozen ones, so the class cannot sit entirely
   skipped while quietly pointing at a softer substrate.

## Its constitutional standing, stated plainly

`§6` enumerates six trial classes and does not forbid a seventh; `§9.1` reserves
one move per session and `§9.2` forbids editing frozen artifacts, neither of
which this class touches. It adds trials, and additive trials are in-session
authority — no ruling is needed for a class that applies only thresholds a
ruling or the constitution has already authorized, and `laws/t_rulings.py`
enforces exactly that: a gate constant here without a §5 clause behind it is a
red suite.

If a future session comes to believe the class needs constitutional standing of
its own, the procedure is `CLAUDE.md §5` — log the objection and stop. It is not
to be quietly deleted; a deleted inheritance battery is indistinguishable from a
passed one.

## Contents

| path | layer | contents |
|---|---|---|
| `l4/t_inheritance.py` | Layer 4 | the Layer-1 verbs, the Layer-2 cue battery and the Layer-3 retention battery at `layer_cap = 4`, in budget — **engaged at Stage C and green**: the consolidation engine returns byte-exact events, clears `cue-C ≥ 900` / `F ≥ 950`, and recalls both frozen pressure streams at `weighted-C = unweighted-C = 1000` when nothing forces a drop — plus the engine-free wiring check |
| `l5/t_inheritance.py` | Layer 5 | the same three batteries at `layer_cap = 5`, **plus the Layer-4 consolidation battery** on `corpora/l4stream` in budget, where `§5 L4`'s `C ≥ 850` and reconstruction `F ≥ 900` become identities (`1000 / 1000`, `wrong = 0`, `fabricated = 0`) — **engine-gated skips** until Stage C, plus the engine-free wiring check. The Layer-4 row is the one prospection could actually break: a pending set, an evaluator on the write path and the engine's own emitted events compete for the same cells as the interval table, and the cheapest way to buy room for them is a lossier derived view, which `§5 L5`'s four firing clauses would never notice. `footprint ≤ 250` is deliberately **not** re-applied — it is a claim about compression under pressure, and this class is defined by there being none |

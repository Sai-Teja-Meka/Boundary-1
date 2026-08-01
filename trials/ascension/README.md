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

- `l5/` — Layer 5, Prospection, **Stage A only; no gate binds and no engine
  exists.** (`ATTAINABILITY.md`, `t_attainability.py`, `RULING-R5-DRAFT.md`,
  with `corpora/l5stream` frozen and pinned by `ops/l5/t_l5stream.py`.) The
  arithmetic exhibits a witness ATTAINING the ratified identity
  (`trigger-precision = trigger-recall = 1000`, `dup-fire = miss = 0`, `F = 1000`)
  at 230‰ of the raw footprint with a 3 687-cell margin, against a best
  capability-free baseline of `375 / 379 / F 397`. It stops for a human on a
  **constitutional collision**: four of `§5 L5`'s six clauses are identities, so
  the oracle ceiling **is** the gate and R2's *"strictly below"* is undischargeable
  by the Layer-3/Layer-4 method; and two of them are **minimizing**, so R2's
  *"strictly above"* is undischargeable clause-wise and holds only over the
  conjunction. `RULING-R5-DRAFT.md` proposes how both are read. Until a human
  ratifies it, no Layer-5 gate binds on anything.

  > **Note added 2026-07-31 (`[L4] [RULING]`).** The draft is ratified as
  > **`BOUNDARY-RULINGS.md R5`**, which settles both readings — an identity
  > clause discharges R2 obligation 1 by an exhibited **attainment** (clause 1);
  > a minimizing clause is read direction-aware and over the **conjunction**
  > (clause 2) — and adds two forward-binding methodology clauses (a ceiling
  > declares its **policy class**, clause 3; a priced state prices its
  > **bookkeeping and loss reserves**, clause 4). **The last sentence above still
  > holds**: R5 authorizes a reading, not a substrate, and the corpus binding
  > (`ATTAINABILITY.md §6` question 4) was deliberately not taken — so no Layer-5
  > gate binds on `corpora/l5stream` or on anything else, and Stage B is still
  > unwritten.

  > **Note added 2026-07-31 (`[L4] [ASCEND]`, Stage B).** Stage B is now
  > written: `STAGE-B.md` (the record), `t_prospection.py` (the gate battery,
  > **engine-gated skips** plus two engine-free trials) and
  > `RULING-R6-DRAFT.md`, beside `trials/humility/l5/` (green) and
  > `trials/inheritance/l5/` (skips). **The sentence above still holds** — no
  > Layer-5 gate binds on anything, because `R6` is a draft and appending is what
  > freezes. What Stage B settles is the question `R5` left open: `STAGE-B.md §1`
  > derives from `§1.3`, `§1.4`, `§2.2`, `§5 L5` and `§7.1` that **a firing is an
  > event and occupies a logical `t` of its own**, so one caller `ingest` advances
  > `next_t` by `1 + f` — with `f = 0`, and therefore Layers 1–4 unmoved, on
  > every corpus that carries no intention, asserted over the bytes of all seven.

  > **Note added 2026-07-31 (`[L4] [RULING]`).** `R6` is ratified and appended to
  > `BOUNDARY-RULINGS.md`, so **the sentence above no longer holds and this is
  > where it stops**: the Layer-5 ascension gate — and, in the same clause, the
  > Layer-5 humility ceiling — **binds on `corpora/l5stream`** (clause 1), a
  > firing is an event occupying a logical `t` of its own so one caller `ingest`
  > advances `next_t` by `1 + f` (clause 2, which also records what it does *not*
  > decide: cascades, and what an engine owes when the budget cannot house a
  > firing), a machine-checked quantity beats a prose one and the divergence is
  > recorded rather than edited away (clause 3), and `budget_cap = raw_cells // 4
  > = 45 638` (clause 4). What does **not** change: no threshold moved, Layer 5
  > is **not** claimed, and Stage C — the engine, its README, its strains and its
  > anchor — is unwritten under R2's standing step.

  > **Note added 2026-08-01 (`[L5] [ASCEND]`, Stage C+D+E).** Stage C is written
  > and **the gate is CLEARED**, so the last sentence above is where the
  > unwritten-engine note stops: `core/layers/l5_prospection.py`,
  > `trials/adapters/l5.py` and `core/layers/README-l5.md` exist, all eight
  > engine-gated trials in `l5/t_prospection.py` are engaged and green, and
  > **Layer 5 is claimed**. Measured on `corpora/l5stream` at the ratified cap:
  > trigger-precision **1000**, trigger-recall **1000**, dup-fire **0**, miss
  > **0**, `F` **1000** against a gate of 980, `B` **1000** with `refused = 0`,
  > at 45 628 of 45 638 cells (250‰); `next_t` 20 765 with the last firing at
  > `t = 20 760`, audited against the engine's own clock. Nothing here is
  > rewritten and no number in `ATTAINABILITY.md` or `STAGE-B.md` moved.

- `l5/STAGE-B.md` — the Stage-B record: the `t` decision and its derivation
  (§1, with the contradiction check against every text that could object), the
  declared query vocabulary the battery asks (§2), what the battery binds and
  what it defers to Stage A (§3), and the four questions `RULING-R6-DRAFT.md`
  puts to a human (§7).

**`ATTAINABILITY.md` is mandatory from `BOUNDARY-RULINGS.md` R2**: a gate must be
shown to lie strictly below the oracle ceiling and strictly above every named
capability-free baseline on its binding corpus, and that arithmetic must be
computed and recorded **before the gate binds** — the ascension-side counterpart of
`humility/`'s `IMPOSSIBILITY.md`. R2 also fixes the standing order of an `ASCEND`:
attainability arithmetic → trials → engine. R2 binds every *future* gate, so
Layers 1–2 predate it and are not retroactively invalidated by it.

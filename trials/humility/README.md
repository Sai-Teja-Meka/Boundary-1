# trials/humility/

Humility is a **trial class**, not an abstention gimmick. For each layer `N`, the
humility trial takes **layer `N`'s own ascension tasks** and runs them, through
the same generic interface (`trials/adapters/INTERFACE.md`), against
**`make_engine(layer_cap = N−1)`** — the engine built with capability capped one
layer below.

It asserts the capped engine's scores are **at or below** the layer's declared
**humility failure ceiling** (`BOUNDARY.md §5`). This proves the ascension gate is
**load-bearing**: it cannot be cleared by the previous layer's capability alone.
If a `layer_cap = N−1` engine could pass layer `N`'s tasks, the gate would be
measuring nothing.

**Every humility trial ships an `IMPOSSIBILITY.md`** giving a *structural*
argument (not an empirical observation) for why the capped engine cannot exceed
the ceiling.

The per-layer fabrication ceiling of earlier drafts is **not** a constitutional
measure; it survives only as a component of the abstention-aware scoring
(`§3.0`) that Layer 6+ calibration relies on.

Populated alongside ascension trials, one layer at a time. Present:

- `l2/t_recall.py` + `l2/IMPOSSIBILITY.md` — the capped `layer_cap = 1` engine
  against Layer 2's cue tasks (ceiling: cue-C ≤ 100).
- `l3/t_forgetting.py` + `l3/IMPOSSIBILITY.md` — the capped `layer_cap = 2` engine
  against Layer 3's pressure tasks (ceiling: weighted-C ≤ 300).
- `l4/t_consolidation.py` + `l4/IMPOSSIBILITY.md` — the capped `layer_cap = 3`
  engine against Layer 4's Q1–Q4 battery at footprint 250‰ (ceiling:
  reconstruction F ≤ 400). Measured **0 / 302** where the ceiling allows 400 and
  the gate demands `C ≥ 850`, `F ≥ 900`. Its `IMPOSSIBILITY.md` is the first to
  carry an **information-theoretic** argument beside the behavioral one: the
  frozen Layer-3 `l4-seam` strain witnesses two streams differing only in
  evicted content producing byte-identical states, so thousands of evicted
  payloads map into a ≤ 35-cell aggregate record and reconstruction over the
  evicted set is unanswerable by pigeonhole — not merely unaffordable. §4 of
  that document records where each number was measured, including the one
  whole-stream run the suite does not carry and why.

- `l5/t_prospection.py` + `l5/IMPOSSIBILITY.md` — the capped `layer_cap = 4`
  engine against Layer 5's own P1/P2 battery (ceiling: `trigger-recall ≤ 50`).
  Measured **0**, on the whole 20 000-event stream through the generic interface
  — no prefix ladder is declared or needed, the capped engine here being the
  frozen Layer-4 one rather than Layer 3's `O(retained)` eviction path. Its
  `IMPOSSIBILITY.md` argues an **absence of machinery** rather than an absence of
  information, and says so: the `l4` pigeonhole is *not* borrowed, because in
  budget the capped engine holds all 945 intentions byte-exact and still scores
  0. The sharpest form is read off `§1.3` alone — a firing consumes a logical
  `t`, so an engine that fired anything ends past the caller stream, and this one
  ends exactly on it. **The corpus (`corpora/l5stream`) is PENDING**: no ruling
  binds it to the humility side any more than to the ascension side, and
  `ascension/l5/RULING-R6-DRAFT.md` clause 1 asks for both bindings together.

  > **Note added 2026-07-31 (`[L4] [RULING]`).** No longer pending: `R6` clause 1
  > is ratified and **binds `corpora/l5stream` to this ceiling and to the
  > ascension gate in one clause**, for exactly the reason the sentence above
  > gives. The measurement does not move — `trigger-recall` **0** against a
  > ceiling of 50 — and both conditions of `IMPOSSIBILITY.md §3` (945 of 945
  > intentions held in budget, 30 of 945 at the ratified cap, 0 either way) are
  > carried into R6's Stage-B evidence.

  > **Note added 2026-08-01 (`[L5] [ASCEND]`, Stage C).** The engine-gated §7.4
  > confirmation is now engaged and green: `make_engine(4)` built from the
  > **Layer-5** engine measures what `make_engine(4)` built from the Layer-4
  > engine measures, field for field — and by construction rather than by
  > imitation, since `l5_prospection.new_state` returns the frozen Layer-4 state
  > below its own layer. The ceiling does not move: **0** against 50.

- `l6/t_meta_memory.py` + `l6/IMPOSSIBILITY.md` — the capped `layer_cap = 5`
  engine against Layer 6's own battery on `corpora/l6batteryb` (ceiling:
  `AUROC ≤ 600`). Measured **500** against a gate of 900 — *neither breached nor
  vacuous*, and sat at from below by arithmetic rather than approached: `AUROC`
  is a ranking statistic and a constant confidence ranks nothing, so every
  correct×incorrect pair ties, ties count ½, and the value is exactly `1/2`. The
  artifact is bound to this ceiling **and** to the ascension gate by one clause,
  `BOUNDARY-RULINGS.md R7` clause 1, for `R6` clause 1's reason.

  Two things this one settles that earlier layers could leave alone. First,
  `§5.1 L6`'s *"the harness scores it confident-by-default"* needs **no
  convention**: the frozen Layer-5 engine emits `{0, 1000}` through `§7.2`
  itself, so the harness reads the engine's own field and supplies nothing — the
  `[L5] [PULSE]` pre-read flagged that sentence as the half of its prediction
  most likely to be wrong, and the measurement is what answers it. Second, the
  ceiling is not vacuous, which `README-l5 §4` said the battery would have to
  buy: *"the Layer-6 humility battery needs a query class this engine gets
  wrong."* The forcing region is that class, and the capped engine errs on
  exactly one member of every one of its 100 mirror pairs **for any reading of
  the frozen bytes**, which is why `R7` demoted round 1's artifact and bound
  this one. Its `IMPOSSIBILITY.md` argues the **third** kind of impossibility in
  the ladder — neither `l4`'s pigeonhole (information) nor `l5`'s absence of
  machinery: the capped engine holds both halves of every tie and answers all
  200 forcing queries, and what it lacks is a **ranking**. *Confidence emitted is
  not confidence calibrated; that is the layer.* It clears two of the five
  clauses (`F 955`, `B 1000`) and fails three, and `§3.0` cannot see the
  difference, being confidence-blind.

**Layer 1 has no humility trial** and never will: it is the floor, so there is no
lower layer to cap against. Its null-engine (`layer_cap = 0`) baseline lives in
`trials/ops/l1/t_capped0_baseline.py` as a sanity check (§5 L1, §6).

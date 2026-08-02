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

- `l6/PRE-READ.md` — Layer 6, Meta-memory. **A `PULSE` finding document, not an
  `ATTAINABILITY.md`**: it binds nothing, names no corpus, applies no gate and
  declares no constant, and this directory holds no trial. Deposited by
  `[L5] [PULSE]` (2026-08-01) in the shape `[L4] [PULSE]` used for its Layer-5
  risk note — read the ratified clauses one layer ahead and **predict the shape
  of the collision** so Stage A meets it rather than discovers it. It sorts
  `§5 L6`'s six clauses into `R5`'s kinds (four ordinary graded gates, one
  identity in `B`, both minimizing clauses already read by `R5` clause 2, which
  named Layer 6 in its own text — **so Layer 6 needs no `R5`-shaped reading of
  its own**); confirms Brier, ECE and AUROC are exactly computable in `Fraction`
  under `§2.2` at `§3.4`'s ten-bin structure, with one reading to declare
  (`permille(x) ≤ 40` and `x ≤ 40/1000` differ on `(40/1000, 81/2000]`); and
  records the collision it predicts Stage A will stop on — `§3.0` is
  confidence-blind and `§3.4` is abstention-blind, so `ECE ≤ 30` discriminates
  against no base-rate constant at any error rate (`ECE = 0` exactly), `Brier`
  discriminates only in a nine-permille band bounded above by `§5 L6`'s own
  `F ≥ 950`, and `R2` obligation 2 therefore rests entirely on `AUROC`, the one
  clause `§3.4` leaves **undefined** when `n_neg = 0` — which is every score this
  project has ever recorded. R2's standing step is untouched: a Layer-6 `ASCEND`
  still owes its own `ATTAINABILITY.md` before any Layer-6 gate has authority.

  > **Note added 2026-08-01 (`[L5] [ASCEND]`, Layer-6 Stage A).** That
  > `ATTAINABILITY.md` now exists, beside this file and answering it rather than
  > rewriting it. The pre-read's prediction is **scored** in its §7 — five hits,
  > three misses and one hit sharpened — and the two misses that matter are:
  > `R2` obligation 2 does **not** rest entirely on `AUROC` (`Brier` fails both
  > named constants at 45 and 43, and `F` fails the key-blind abstainer at 829),
  > and the capped engine's confidence is **not** a `§5.1` convention (the frozen
  > Layer-5 engine emits `{0, 1000}` through `§7.2` itself, so `capped AUROC`
  > measures 500 against the ratified 600 and the humility side is a measurement
  > of an engine after all). The pre-read's own flagged half was the wrong one.
  > **Still true, and unchanged: no Layer-6 gate binds on anything.**

- `l6/ATTAINABILITY.md` + `l6/t_attainability.py` — Layer 6, Meta-memory,
  Stage A. The `R2` arithmetic over the newly frozen `corpora/l6battery` (3 905
  queries over the frozen murk corpus, answer keys derived from murk's frozen
  `ground_truth.json`), computed with **no Layer-6 engine in existence**: the
  ceiling **exhibited** as a concrete confidence assignment at
  `Brier 0 / ECE 7 / AUROC 1000 / F 955 / B 1000`, both policy classes declared
  (`O` oracle, `E` evidence-only) and measured against each other, every named
  capability-free baseline scored, and `R5` clause 2's conjunction reading
  applied **first** — which discharges `R2` obligation 2 without a new clause of
  law. `n_neg = 158`, measured on the frozen Layer-5 engine through `§7`'s own
  interface, so both AUROC classes are non-empty and the calibration triple is
  **defined** — the thing that was true on no artifact this project had before.
- `l6/RULING-R7-DRAFT.md` — the draft, **not appended** to
  `BOUNDARY-RULINGS.md` because appending is what freezes: the binding (clause
  1), the calibration denominator stated explicitly (clause 2), `AUROC`'s domain
  including the finding that `n/a` must **disqualify** rather than excuse — since
  a capability-free abstainer otherwise clears every evaluable clause (clause 3)
  — and the exact-not-permille reading (clause 4). **No Layer-6 gate binds on
  `corpora/l6battery` or on anything else**, and `laws/t_rulings.py` carries the
  six `§5 L6` constants with a `§5` clause and no companion ruling, which is what
  that says in the registry's own structure.

  > **Note added 2026-08-01 (`[L5] [ASCEND]`, Layer-6 Stage A ROUND 2.)** The two
  > entries above are **round 1**, and their substrate is superseded while their
  > arithmetic is not: `t_attainability.py` still computes and asserts every one
  > of those figures on `corpora/l6battery`, green. What the human ruled on is the
  > fork round 1's clause 3 put to them — **`AUROC = n/a` DISQUALIFIES**, and a
  > binding artifact must make `n_neg > 0` a **THEOREM** rather than a fact
  > relative to a declared reading. Round 1's own §6 is the reason it cannot:
  > `§8.7` injects every murk defect by visible construction, so a stream-only
  > rule recovers each family exactly and a first-wins reader would have driven
  > `n_neg` to 0.

- `l6/ATTAINABILITY-B.md` + `l6/t_attainability_b.py` — Layer 6, **Stage A round
  2**, over the newly frozen `corpora/l6batteryb` (12 000 events + 2 400 queries,
  one artifact carrying substrate, key and query set together). Its **forcing
  region** is 100 mirror pairs whose two members are observationally identical —
  equal event histories once the entity id is blanked, logical times differing by
  exactly `+1` — with one member's truth its FIRST assertion and the other's its
  LAST, and the resolving coin **withheld at generation**: regenerating with every
  bit flipped produces a **byte-identical stream**. So every reader on a six-reader
  bench, `first-wins` included, errs on exactly 100 forcing queries and
  **`n_neg = 100` is a theorem**. Ceiling **exhibited** at
  `Brier 23 / ECE 0 / AUROC 976 / F 955 / B 1000`; the feasible window for the
  region size recorded exactly (`A/r ∈ [10, (25 + 5√21)/4)`, sitting at 11); and
  the round-1 collision **closed by arithmetic** — the detect-and-abstain hedger
  measures `F 918` and fails under BOTH readings of `n/a`, and no policy clearing
  `F ≥ 950` can reach `n_neg = 0` (floor 87). The key-blind ranker is re-measured
  at `AUROC 911` and its scope statement updated; one round-1 finding is
  **reversed** and recorded (the witness attains `ECE = 0`, so the base-rate
  constant no longer beats a real model).
- `l6/RULING-R7-DRAFT.md` — **round 2 stands above round 1's body**, which is
  preserved verbatim under a dated note and never edited. Still **not appended**
  to `BOUNDARY-RULINGS.md`, because appending is what freezes. Nine clauses: the
  binding on `corpora/l6batteryb` for both sides **and the fourth substrate kill**
  (`corpora/l6battery` DEMOTED to an ungated diagnostic, its cause recorded
  verbatim in the `R4`-clause-1 form, its bytes and its trials untouched); the
  denominator law; `AUROC`'s domain with the **instrument-range** framing — a gate
  is an instrument and declines to certify what it cannot measure — and the
  **forcing-region theorem** as the domain guarantee that replaces round 1's
  declared-reading proviso; the exact reading; the ECE **bin** reading; the
  key-blind scope statement; the `§3.0` price-list tension **recorded for Layer
  7's eyes** and ruled on by nobody; and the **declined commitment clause**, held
  in reserve with its four objections. **No Layer-6 gate binds on either
  artifact**, and `laws/t_rulings.py` now carries the six `§5 L6` constants
  **twice**, once per round, each with a `§5` clause and no companion ruling.

  > **Note added 2026-08-02 (`[L5] [RULING]`, `R7` recorded).** The last two
  > sentences above are where *"no Layer-6 gate binds on either artifact"* stops
  > holding, and this index says so rather than being rewritten. A human ratified
  > the round-2 draft and a `RULING` session appended it as **`R7`**, **as
  > drafted**: all nine clauses, normative text unaltered, checked mechanically
  > against the draft. **The Layer-6 gate now binds on `corpora/l6batteryb`,
  > BOTH sides**, in one clause (`R6` clause 1's shape), and **`corpora/l6battery`
  > is DEMOTED to an ungated diagnostic** — the fourth substrate kill, its cause
  > quoted verbatim from round 1's own `ATTAINABILITY.md §6`, its bytes and both
  > trials that score it untouched and still green. In `laws/t_rulings.py` the six
  > battery-b constants now carry `R7`; round 1's six keep their `§5` clause and
  > carry **no** ruling, which is that registry recording the demotion in its own
  > structure — and a registry edit restoring one is red.
  >
  > `R7` also settles what the arithmetic in both files had to assume: the
  > calibration denominator excludes abstentions and is stated beside the triple
  > (clause 2), `AUROC = n/a` **disqualifies** with a **forcing region** required
  > of any artifact a gate citing `AUROC` binds on and priced inside a recorded
  > window (clause 3), the reading is **exact, not permille** (clause 4), and the
  > ECE bin index is ruled (clause 5). `R5` still carries the READINGS of `R2`'s
  > obligations here without an entry of its own; `R7` carries the **substrate**
  > and the **`n/a` law**.
  >
  > **Authority, not behaviour**: no score moved, no threshold, ceiling or corpus
  > binding other than Layer 6's own changed, and **no Layer-6 engine exists**.
  > `trials/humility/l6/` with its mandatory `IMPOSSIBILITY.md`,
  > `trials/inheritance/l6/`, and only then `core/layers/l6_meta_memory.py`, are
  > what `R2`'s standing step orders next.

- `l6/STAGE-B.md` + `l6/t_meta_memory.py` — **Stage B**
  (`[L5] [ASCEND]`, 2026-08-02): the ratified `§5 L6` gate applied to an
  **engine** on `corpora/l6batteryb`, and **every trial in it is an engine-gated
  skip**. The standing checkpoint of a trials-before-engine session is *humility
  green + ascension skipped*, and that is what this session leaves behind. The
  battery carries `Brier ≤ 40` and `ECE ≤ 30` exact (`R7` clause 4) under
  clause 5's bin index; `AUROC ≥ 900` with **`n/a` DISQUALIFIES asserted as law**
  — an engine whose battery-b scores yield `n_neg = 0` fails the clause, in `R7`
  clause 3(a)'s own instrument-range words; `F ≥ 950` under the literal `§3.0`
  table over the **answerable core**, with `F` over the whole query set reported
  as the ungated diagnostic; `B = 1000` after **every** write; the denominator
  declared class by class (`R7` clause 2); `§7.2`'s `confidence` read as an
  integer permille, a float or a `bool` there being a harness-level failure and
  not a low score; the forcing region measured, where **no pair may be resolved**
  because the coin is in the answer key and in no function of the stream
  (Theorem 2); and `corpora/l6battery` **scored and reported UNGATED**, the
  chronicle pattern one layer up, per its demotion's recorded duty. It
  deliberately re-asserts none of Stage A's witness, baselines or tie proof —
  one fixture, one truth — and names the owning trial for each. `STAGE-B.md`
  records the declared query vocabulary, the denominator law as applied, the
  restraint (the tie confidence of 500 is **expected and reported, never
  required** — `§5 L6` gates a score, not a policy's shape), and §7's explicit
  report that **no `R8` was needed and none is drafted**.
  `ops/l6/t_stage_b.py` checks engine-free what a fully engine-gated battery
  otherwise could not: one instrument, the bin reading, the vocabulary, the
  denominator declaration and this document.

**`ATTAINABILITY.md` is mandatory from `BOUNDARY-RULINGS.md` R2**: a gate must be
shown to lie strictly below the oracle ceiling and strictly above every named
capability-free baseline on its binding corpus, and that arithmetic must be
computed and recorded **before the gate binds** — the ascension-side counterpart of
`humility/`'s `IMPOSSIBILITY.md`. R2 also fixes the standing order of an `ASCEND`:
attainability arithmetic → trials → engine. R2 binds every *future* gate, so
Layers 1–2 predate it and are not retroactively invalidated by it.

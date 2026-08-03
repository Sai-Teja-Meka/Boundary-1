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

> **Note added 2026-08-02 (`[L6] [ASCEND]`, Layer-6 **Stage C**). Layer 6 is
> CLAIMED, and the Layer-6 index above is where the last "engine-gated" stops
> holding.** `core/layers/l6_meta_memory.py` and `trials/adapters/l6.py` exist,
> and every one of `l6/t_meta_memory.py`'s eight engine-gated skips is flipped
> and green: the ratified `§5 L6` gate CLEARS on `corpora/l6batteryb` at
> **Brier 1/44 → 23, ECE 0 exactly, AUROC 41/42 → 976, F 21/22 → 955 over the
> answerable core (23/24 → 958 over the whole set, ungated), B 1000** with
> `A 2200 / n_pos 2100 / n_neg 100`, `refused 0` and `fabricated 0` — clause for
> clause the figures `ATTAINABILITY-B.md` exhibited before any engine existed,
> which is `R2` obligation 1 discharged rather than a coincidence. No pair of the
> forcing region is resolved. `corpora/l6battery` is replayed, scored and
> reported ungated beside it, where the same model measures `AUROC 1000` because
> there evidence that ranks also resolves — the demotion's cause, on an engine.
>
> Both files' closing checks are **advanced** one step along `R2`'s order rather
> than deleted, each under a dated note with no historical line rewritten:
> `t_attainability_b.py` moves the engine and the adapter from its absence list
> to its presence list and replaces the absence check with the one only Stage C
> could carry — the engine's own source may not import the artifact, its
> generator, its answer key or the battery module, because *the generator is part
> of the answer key, not part of the substrate* (`R7` clause 3(b)); and round 1's
> `t_attainability.py` now asserts that the **demotion survived the engine's
> arrival**, naming the battery that scores its artifact ungated, since an
> artifact nobody scores has been retired by silence.

- `l7/PRE-READ.md` — Layer 7, Generation. **A `PULSE` finding document, not an
  `ATTAINABILITY.md`**: it binds nothing, names no corpus, applies no gate and
  declares no constant, and `l7/` holds no trial (`run.py` walks it for `t_*.py`
  and finds none). Deposited by `[L6] [PULSE]` (2026-08-02) in the shape
  `[L5] [PULSE]` used for `l6/PRE-READ.md` — read the ratified clauses one layer
  ahead and **predict the shape of the collision** so Stage A meets it rather
  than discovers it, with both prior pre-reads' scored records (Layer 5: one
  unpredicted half; Layer 6: three misses) carried as the standard it expects to
  be held to. It sorts `§5 L7`'s **seven** clauses into `R5`'s kinds — five
  identities, the highest count in the ladder, so `R5` clause 1's exhibited
  attainment is the dominant instrument and Layer 7 needs no `R5`-shaped reading
  of its own; finds that a **retrieval-only policy (which is `make_engine(6)`)
  ties three of the seven at the gate** (`validity 1000`, `promotion 0`,
  `B 1000`) while `ECE ≤ 40` is the one clause Layer 6 *measured* to
  discriminate against nothing, so `R2` obligation 2 rests over the conjunction
  on **`novelty`** (0 for retrieval-only, by arithmetic) and on `F`; names the
  **fourth species** of gate clause after `R5` clause 1's identity, `R5`
  clause 2's minimizing clause and `R7` clause 3's empty domain — **the
  SELF-REPORTED DENOMINATOR**, since `§5` states no denominator for
  `validity`/`novelty`/`tagging` and the tempting one is the engine's own
  testimony, which is WRIT's null-exemption (`evaluator.ts:545-548`) in a new
  costume; examines `§4.2` as it wakes (shape-valid, and blind to
  **recoverability**, to **relevance**, and to **lineage** — there is no
  `"generated"` kind in the closed four-kind vocabulary, and a re-ingested
  generation is an actually-ingested `t` whose citation `§4.2.3` cannot
  distinguish from an observed one); prices `R7` clause 7's bequest against
  `§3.0`'s five ways to score, finding the blanket hedger killed iff the
  generation class exceeds **`1/18`** of the answerable core — the *same
  constant* as `R7` clause 3(c), because it is `50/900`, `§5`'s `F` slack over
  `§3.0`'s abstention price — with Layer 7 inheriting the window's upper bound
  and **not** its lower one, no error being forced here; records that
  `generate(cue)` must be read as a `query` op under `§7.1`'s three doors, the
  argument `ATTAINABILITY.md`'s Reading 1 made for `intend` and `R6` clause 2
  ratified for *"appends one event"*; and predicts the stop at the denominators
  and at **an artifact where tagging is not free** — the Layer-7 form of the
  defect that killed `corpora/l6battery` one session after it was frozen.
  R2's standing step is untouched: a Layer-7 `ASCEND` still owes its own
  `ATTAINABILITY.md` before any Layer-7 gate has authority.

- `l7/ATTAINABILITY.md` + `l7/t_attainability.py` — Layer 7, Generation,
  **Stage A**. The `R2` arithmetic, computed and machine-checked with **no
  Layer-7 engine in existence**, and **NO LAYER-7 GATE BINDS ON ANYTHING**:
  `trial_no_layer_7_gate_binds_on_anything` asserts it from the other side
  (no `core/layers/l7_generation.py`, no `trials/adapters/l7.py`, no
  `humility/l7/`, no `inheritance/l7/`, no `strain/l7/`, and no `R8` in
  `BOUNDARY-RULINGS.md`), and `laws/t_rulings.py` carries the eight `§5 L7`
  constants with a `§5` clause and no companion ruling, which is the same
  absence said in the registry's own structure.

  **THE FIFTH SUBSTRATE KILL, measured.** Across every artifact in
  `corpora/registry.py` and `§8.8`'s one `REAL` entry — 85 954 answerable
  queries drawn from the frozen batteries those artifacts already carry — **not
  one answer is absent from its own stream**, so on all of them the
  generation-required class is empty and a gate citing `novelty` or `tagging`
  measures nothing. `§8.7`'s *dirt is always paired with the answer key* is the
  cause. It is the first kill to fall on the whole existing stock rather than on
  one artifact, and nothing is demoted, because nothing here was ever a Layer-7
  candidate: what is recorded is a refusal to bind, in `R4` clause 1's form.

  **The artifact it forces:** `corpora/l7compose` — a closed compositional
  grammar with a withheld item, 100 mirror pairs under a balanced coin, the
  three-generation self-pollution ladder, and 100 generation-shaped
  unanswerable probes. Theorem 1 (the class is not readable from the query —
  every labeller that does not consult the store mislabels exactly one member
  of every pair, exhibited against a bench of six) and Theorem 2 (novelty, by
  exhaustive canonical-byte comparison) are asserted in `ops/l7/t_l7compose.py`.

  **The witness** is class E and attains `validity = novelty = tagging = 1000`,
  `promotion = 0` at all three rungs, `F 1000` against 950, `ECE 0` against 40,
  `B 1000`. No capability-free baseline clears more than **three of the seven**
  clauses; the untagged generator is correct on every value it returns and dies
  at `tagging = 0/160`; the over-tagger clears six and dies at `novelty 615`.

- `l7/RULING-R8-DRAFT.md` — the draft, **not appended** to
  `BOUNDARY-RULINGS.md`, because appending is what freezes. Nine clauses: the
  binding and the fifth substrate kill; `generate` as a `query` op; **the
  self-reported denominator**, the fourth species, with `R7` clause 3(a)'s
  instrument-range ground extended to a general holding; `generated` as
  item-lineage orthogonal to `§4.2.3`'s closed kinds; `§4.2`'s three
  blindnesses; `ECE` over `§3.4`'s own denominator; the humility conjunction
  defined; **`R7` clause 7's bequest settled pre-claim**; and the record that
  nothing else is added.

> **Note added 2026-08-03 (`[L6] [RULING]`, `R8` recorded). The two entries
> above are where *"no Layer-7 gate binds on anything"* stops holding.**
>
> A human ratified `l7/RULING-R8-DRAFT.md` and a `RULING` session appended it to
> `BOUNDARY-RULINGS.md` as **`R8`**, **as drafted** — all nine clauses in the
> draft's order with their normative text unaltered, and the question, the
> rationale and the *"what this ruling does not do"* list carried across
> byte-for-byte and checked mechanically. **`R8` clause 1 binds BOTH sides of the
> Layer-7 gate — ascension and humility — on `corpora/l7compose`**, in one
> clause, for `R6` clause 1's reason, and in the same clause records the **fifth
> substrate kill** as a **refusal to bind** rather than a demotion: nothing is
> demoted, no byte moves, and every trial that scores the refused stock keeps
> running.
>
> The index entries above are **not rewritten**. What changes under them is
> authority and one trial name: the eight `§5 L7` constants now carry `R8` in
> `laws/t_rulings.py` where they carried no companion ruling, a new registry
> check there forbids that authority to be moved to any artifact the fifth kill
> refused, and `l7/t_attainability.py`'s closing trial is **advanced one step
> rather than weakened** —
> `trial_no_layer_7_gate_binds_on_anything` becomes
> `trial_the_layer_7_gate_binds_on_this_artifact_under_r8_clause_1`, which
> requires the entry to bind the artifact **and** record the refusal in the same
> clause, and goes on requiring the engine, the adapter and the `humility/l7`,
> `inheritance/l7` and `strain/l7` directories to be **absent**, because `R2`'s
> standing step orders Stage B and Stage C after this entry and not inside it.
> That is the form `l6/t_attainability_b.py`'s closing trial took at `R7`.
>
> `R5`, `R7` and `R8` are kept **distinct**: `R5` authorizes the readings of
> `R2`'s obligations (the identities, the direction-aware conjunction, the
> declared policy class, the pricing) and is in force here without an entry of
> its own; `R7` authorizes the `n/a` law's instrument-range ground and the two
> `§3.4` readings `R8` clause 6 applies unchanged; `R8` authorizes the
> substrate, the three denominators `§5` does not state, and the reading of
> `§4.2`.

> **Note added 2026-08-03 (`[L6] [ASCEND]`, Layer-7 Stage B).** The middle step
> of `R2`'s standing order is taken: `l7/t_generation.py` is the ratified `§5 L7`
> gate — `validity = 1000`, `novelty = 1000`, `tagging = 1000`, self-pollution
> `promotion = 0` three deep, `F ≥ 950`, `B = 1000`, `ECE ≤ 40` — applied to an
> **engine** on `corpora/l7compose` per `R8` clause 1, and **every trial in it is
> an engine-gated skip**. `core/layers/l7_generation.py`, `trials/adapters/l7.py`
> and `trials/strain/l7/` still do not exist; the standing checkpoint this
> session leaves is the one Layers 4, 5 and 6 left at the same point — **humility
> green + ascension skipped**. `l7/STAGE-B.md` is the record: the declared query
> vocabulary, the three denominators applied with `R8` clause 3(a)'s holding
> asserted as law, `ECE` under both of clause 6's readings with the declined one
> computed and gating nothing, the **three over-tightenings caught and removed**
> before freezing, and the mock-engine validation that shows the battery
> clearable — including that the lawful `k = 111` hedger `R8` clause 3(e) admits
> clears the whole battery while `k = 112` dies on `F` alone, at `R7` clause 4's
> exact-reading seam. Its `§7` reports **no `R9`**: every question Stage B had to
> answer was already settled, and the two items left open are engine-design
> questions no in-budget battery can decide.
>
> `l7/t_attainability.py`'s closing trial is **advanced one step rather than
> weakened**, in the form `l6/t_attainability_b.py`'s took at Stage B:
> `trials/humility/l7/` (with its mandatory `IMPOSSIBILITY.md`) and
> `trials/inheritance/l7/` move from its absence list to its presence list, and
> the engine, the adapter and `trials/strain/l7/` stay on the absence list. No
> historical line above is rewritten, and nothing frozen moved.

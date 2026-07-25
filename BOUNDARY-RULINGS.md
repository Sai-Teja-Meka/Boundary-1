# BOUNDARY-RULINGS.md — the rulings that bind alongside the constitution

> **Append-only.** Entries are added at the end and never rewritten. **Each entry
> is frozen the moment it is committed** — from then on it is a frozen artifact
> under `BOUNDARY.md §9.2` and `CLAUDE.md §5`, exactly like a frozen layer or a
> frozen corpus. An entry is never edited, never renumbered, and never deleted.
> A ruling that turns out to be wrong is superseded by a **later entry that says
> so**; the original text stays on the record, wrong, forever. That is the point.
>
> Enforced by `trials/laws/t_rulings.py`, which checks against git history that
> every committed version of this file is a byte-exact prefix of the current one.

---

## What this document is, and is not

`BOUNDARY.md` is frozen and has no amendment mechanism. **This document does not
amend it and cannot.** A ruling that contradicts a ratified sentence of
`BOUNDARY.md` is **void on its face** — the constitutional procedure for a wrong
rule remains what `CLAUDE.md §5` says it is: log the objection and stop.

What a ruling *does* is settle a question the constitution leaves open:

- which **corpus** a stated gate binds on, when the constitution states a
  threshold but names no substrate;
- which **reading** of a ratified defense sentence the trials implement, when the
  sentence admits more than one;
- what **procedure** binds future gates, in the space the constitution leaves to
  convention rather than to law.

Every ruling below is one of those three. None changes a ratified number.

## Where the authority comes from

`BOUNDARY.md §5` itself anticipates that binding thresholds may be written
**outside** `BOUNDARY.md`, in a document that does not yet exist:

> Layers 8–9 receive laws but **not thresholds** yet — thresholds are
> **specified at the Phase 3→4 gate**.

The Layer-8 and Layer-9 rows of the §5 table say `*specified at Phase 3→4 gate*`
where every other row states a gate. So the constitution, in its own frozen text,
concedes two things at once: that some gates will be specified later, and that
the specifying document will not be `BOUNDARY.md`, because `BOUNDARY.md` is
frozen and cannot receive them. That deferred document — call it
**`BOUNDARY-HIGH.md`**; the constitution defers to the *Phase 3→4 gate* and does
not name a filename — is the mechanism this document invokes. **A frozen
supplement may bind.** `BOUNDARY-RULINGS.md` is such a supplement, held to the
same freezing discipline as the thing it supplements, and subordinate to
`BOUNDARY.md` wherever the two could ever be read against each other.

## Precedent

- **FORGE-CORRECTION** (`BOUNDARY.log` L0, twice): the constitution was realigned
  and then ratified *before* it was frozen — establishing that structural error
  is corrected by an explicit, logged, human-sanctioned act, never by quiet
  drift.
- **The ratification amendments** (`BOUNDARY.log` L0): four amendments applied at
  ratification — calibration made dormant until L6, L1 declared the floor, the L3
  pressure-stream corpus precondition added, grammar prose scrubbed — establishing
  that a gate's *binding conditions* are a legitimate object of decision separate
  from the gate's *number*.

This session — move **RULING** — is the post-freeze form of that same act: the
numbers are untouchable, so what gets decided is what they bind to.

## Entry format

Each entry carries an ID (`R<n>`, assigned in order and never reused), a
one-line holding, the question it answers, the ruling itself, the rationale, an
explicit statement of what it does **not** do, and where it is enforced.

---

# R1 — The Layer 3 ascension gate binds on `corpora/l3streamb`

**Status:** FROZEN on commit.
**Binds:** the Layer-3 ascension trial (`trials/ascension/l3/`).
**Authority:** `BOUNDARY.md §5 L3`, `§5.1 L3`; resolves the objection recorded in
`trials/ascension/l3/ATTAINABILITY.md`.
**Holding:** the ratified L3 thresholds stand **unchanged**; the gate binds on
`corpora/l3streamb`; `corpora/l3stream` remains the humility corpus and is
scored in ascension as an **ungated diagnostic**.

## The question

`BOUNDARY.md §5 L3` states the Layer-3 ascension gate as

```
weighted-C ≥ 850,  unweighted-C ≥ 90,  F ≥ 950,  B = 1000
```

with a corpus **precondition** — importance distributed *uniformly-to-late, never
front-loaded* — but it names **no corpus**. The Layer-3 `ASCEND-ATTEMPT` session
measured, and froze into a machine-checked trial, that on `corpora/l3stream` —
the corpus that happened to exist — the gate is **unsatisfiable by any engine
whatsoever**: the mass of the budget-worth of heaviest items, which bounds
`weighted-C` over *all* retain-or-drop policies, is **190‰** against an **850‰**
gate. Reaching 850‰ there would require retaining 6145 items, 6.1× the budget.

That session correctly refused to edit a frozen artifact, recorded the objection
in `ATTAINABILITY.md`, and stopped for a human. This is the ruling.

## The ruling

1. **The ratified thresholds stand, unchanged.** `weighted-C ≥ 850`,
   `unweighted-C ≥ 90`, `F ≥ 950`, `B = 1000` are ratified text and are not
   touched, softened, rescaled, or read as a fraction of anything.

2. **The Layer-3 ascension gate binds on `corpora/l3streamb`.** That corpus
   satisfies the same §5 L3 precondition — importance is never front-loaded — and
   on it the arithmetic is:

   | quantity | value | |
   |---|---|---|
   | oracle ceiling (top-1000 by importance; a bound over **all** policies) | **918‰** | |
   | the ratified gate | **850‰** | **≈ 92.6% of the oracle** |
   | keep-latest (ring buffer, a contiguous window) | **100‰** | 8.5× under the gate |
   | fill-then-refuse (arithmetic, a full budget-worth) | **100‰** | 8.5× under the gate |
   | fill-then-refuse (**measured**, the capped `layer_cap=2` engine) | **34‰** | it pays for its index out of the same cap |

   The gate therefore **discriminates**: it sits strictly below what a perfect
   importance ordering can reach and strictly above what every policy containing
   no importance reasoning can reach. Both order-based baselines are pinned not by
   measurement at one seed but by the window bound — *every* contiguous
   budget-sized window in `l3streamb` holds 100‰ ± 10‰ of the mass, all 9001 of
   them checked exhaustively.

3. **`corpora/l3stream` remains the humility corpus.** Its `IMPOSSIBILITY.md`
   argument — importance non-decreasing in `t`, so the earliest budget-worth is
   the *least* important tenth — is sound, unaffected, and untouched. It stays the
   substrate on which the capped engine's ceiling is argued.

4. **`corpora/l3stream` is scored in ascension as an ungated diagnostic.** Its
   numbers are computed, recorded, and machine-checked; they do not gate. Its
   ascension gate trial reports `SKIPPED-BY-DESIGN` with its measured ceiling in
   the reason, and `trial_forgetting_budget_holds_throughout_both_streams` and
   `trial_attainable_ceilings_are_as_recorded` continue to bind on it. The
   diagnostic is not decoration: `B = 1000` binds on `l3stream` too, and a drift
   in its recorded ceiling is red.

5. **The conditional arithmetic-skip is endorsed as the permanent mechanism.**
   The `l3stream` gate trial does not hard-code its skip. It computes that
   stream's attainable ceiling and skips **only while the ceiling lies below the
   gate** — so if the corpus family ever changes such that the arithmetic admits
   the gate, the trial engages by itself, with no session's permission. This is
   ruled the correct and permanent form for a gate deferred on arithmetic
   grounds: *a deferral must state the condition that lifts it, in code.*

## Rationale — recorded verbatim

> The 850‰ number was ratified under a defense that presupposed a mass
> distribution `l3stream` does not have — the error was in gate-to-corpus
> binding, not in the threshold; the ceiling is arithmetic over ALL policies
> including the oracle, which is a category apart from engine difficulty. No
> engine's inability motivated this ruling; no engine existed.

Each clause of that sentence is load-bearing, so each is stated again in its own
right:

- **The defense presupposed a distribution.** `§5.1 L3` defends the threshold as
  *"under a stream of 10× the budget, importance-weighted eviction must keep at
  least 85% of the total importance mass recoverable."* That is a coherent demand
  only of a stream whose heaviest budget-worth *holds* 85% of the mass. It is
  satisfiable by a skewed profile and unsatisfiable by a linear ramp.
  `l3stream`'s weights ramp from 1 to 4886, so its heaviest tenth holds 19% — the
  top decile of a linear ramp holds about a fifth of it, and no more. The
  threshold was ratified against the distribution its defense imagined, and
  `l3stream` is not that distribution.

- **The error was in the binding, not the number.** Nothing in §5 L3 mandates a
  linear ramp. It requires only that importance be *uniformly-to-late, never
  front-loaded* — which a two-tier profile on a stratified grid also satisfies.
  The conflict was never between the gate and the constitution. It was between
  the gate and one generator's free choice of weight distribution, made before
  anyone computed what that choice implied. So the repair belongs at the binding,
  and touching the number would have been the wrong repair even if the number
  were editable, which it is not.

- **The ceiling is arithmetic over all policies, including the oracle.** The 190‰
  figure is not a score anything achieved. It is an upper bound: an L3 engine
  answers only from what it **retained** (deriving an answer for a dropped event
  is Layer 4 — Consolidation — which §5 gates separately), the retained set holds
  at most `budget_items` items, so `weighted-C` cannot exceed the mass of the
  `budget_items` heaviest items. A perfect oracle that knows every future weight
  scores 190‰ on `l3stream`. This is **a category apart from engine difficulty**:
  a hard gate is a gate an engine might fail; this was a gate the arithmetic
  forbids anything from passing. Lowering a hard gate would be cowardice.
  Rebinding an arithmetically-void one is not the same act, and the distinction
  is the whole of this ruling.

- **No engine's inability motivated this.** At the moment the objection was
  raised, `core/layers/l3_forgetting.py` **did not exist**. There was no engine to
  be embarrassed by, no score to rescue, no failing run to explain away. The
  finding came out of the corpus and the budget law alone, in a session that
  deliberately withheld the engine. Had an engine existed, this ruling would have
  been unavailable to it in this form, and it should have been harder to obtain.

## What this ruling does not do

- It does **not** amend `BOUNDARY.md`. No ratified sentence is edited or reread.
- It does **not** change any threshold, in either direction, on any layer.
- It does **not** retire `corpora/l3stream`, weaken its ops trial, or touch its
  frozen bytes or its `IMPOSSIBILITY.md`.
- It does **not** license "score it on an easier corpus" as a general move. The
  discrimination arithmetic of **R2** is what makes this rebinding legitimate,
  and R2 binds every future gate to compute that arithmetic *first*.
- It does **not** lower the Layer-3 bar. `l3streamb` is the **harder** corpus in
  the sense that matters: on `l3stream` a keep-latest ring buffer with no
  importance reasoning at all scores the arithmetic optimum, so that corpus
  cannot tell an importance-ranking engine from an arrival-order one. On
  `l3streamb` that same policy is pinned at 100‰.

## Enforcement

- `trials/ascension/l3/t_forgetting.py` — the gate on `l3streamb`; the
  conditional arithmetic-skip on `l3stream`; the recorded ceilings (918‰ / 190‰);
  the permanent keep-latest anti-gaming check.
- `trials/humility/l3/t_forgetting.py` — the 300‰ ceiling on both streams and the
  fill-then-refuse arithmetic.
- `trials/ops/l3/t_l3streamb.py` — the corpus properties the discrimination rests
  on: declared mass, exhaustive window bound, importance/position decorrelation.
- `trials/laws/t_rulings.py` — that this ruling exists and that the gate bindings
  the trials apply are authorized by §5 or by an entry here.

---

# R2 — The discrimination principle

**Status:** FROZEN on commit.
**Binds:** **every future ascension gate**, at every layer, including the
Layer-8 and Layer-9 thresholds deferred by §5 to the Phase 3→4 gate — that is,
including `BOUNDARY-HIGH.md` when it is written.
**Authority:** `BOUNDARY.md §5` (the gate/ceiling structure), `§6` (the humility
class and its `IMPOSSIBILITY.md` requirement), `§9.1` (the ASCEND move).
**Holding:** a gate must be shown to discriminate **before** it binds.

## The question

R1 exists because a gate was ratified without anyone computing whether it could
be reached. The humility side of the ladder has had a standing guard against the
mirror error since ratification — every layer ships an `IMPOSSIBILITY.md`
arguing *structurally* that the capped engine cannot exceed its ceiling (§6). The
ascension side had no such requirement. `ATTAINABILITY.md` was invented ad hoc,
by the session that needed it, after the damage was already frozen into a
threshold.

A gate is only a test if it lies between what capability can reach and what
capability-free policy can reach. Nothing required anyone to check.

## The ruling

**Every ascension gate must lie strictly below the oracle ceiling and strictly
above every capability-free baseline on its binding corpus, and this arithmetic
must be computed and recorded in an `ATTAINABILITY.md` BEFORE the gate binds.**

Unpacked into four obligations:

1. **Below the oracle.** The gate must lie **strictly below** the *oracle
   ceiling*: the best score achievable by any policy the layer's capability
   permits, given the corpus, the budget law, and nothing else — a bound derived
   from the corpus, not a measurement of an implementation. A gate at or above the
   oracle ceiling is **void**: it forbids what it purports to test.

2. **Above every capability-free baseline.** The gate must lie **strictly above**
   the score of every **named** baseline that lacks the layer's capability —
   including at minimum the policy the budget law forces on the capped engine, and
   every trivial policy that could pass by accident on that corpus (for Layer 3:
   fill-then-refuse and keep-latest). A gate a capability-free policy can clear
   tests nothing. Baselines must be **named and scored**, not waved at; an
   unnamed baseline is an unchecked one.

3. **Recorded before it binds.** The arithmetic — the oracle ceiling, and each
   named baseline's score, on the corpus the gate will bind on — is computed and
   written into that layer's `ATTAINABILITY.md`, and machine-checked by a trial
   that goes red if any recorded number drifts, **before** the gate is treated as
   binding. `ATTAINABILITY.md` is hereby the ascension-side counterpart of
   `IMPOSSIBILITY.md`, and is required of every layer on the same footing.

4. **Attainability precedes authority.** A gate that has not had this arithmetic
   computed **has no authority yet**. It is a number in a table, not a test. It
   acquires authority when the arithmetic is on the record and shows that it
   discriminates.

### The standing step added to the ASCEND convention

The `ASCEND` move (§9.1) gains one step, before the two it already has:

```
   attainability arithmetic   →   trials   →   engine
```

- **attainability arithmetic before trials** — the oracle ceiling and the named
  baselines are computed from the corpus and recorded, so the corpus is known to
  admit the gate and known to defeat the trivial policies before a trial is
  written against it;
- **trials before engine** — the existing discipline, unchanged: the ascension
  and humility trials are written and run (engine-gated, skipping) before any
  engine code exists;
- **engine last** — so that no threshold, no corpus choice, and no reading of a
  measure can be tuned to something an engine already does.

The ordering is the whole safeguard. Each step is fixed before the step that
could be tempted to bend it.

## Rationale

The Layer-3 finding was recoverable only because the arithmetic happened to be
computed by a session that had no engine yet and no stake in the outcome. That
was luck of sequencing, not process. R2 removes the luck.

The asymmetry it corrects is stark. Since ratification the constitution has
demanded a *structural* argument that a gate cannot be cleared **too easily** —
that is what `IMPOSSIBILITY.md` is, and §6 makes it mandatory at every layer. It
has demanded nothing at all about whether a gate can be cleared **at all**. Both
failures void a gate. Only one of them was guarded.

And the arithmetic must precede the engine specifically because an oracle ceiling
computed *after* an engine exists is no longer a neutral fact about a corpus.
It is a number someone can already see the consequences of. The whole value of
the Layer-3 measurement is that nobody knew what it would cost when it was taken.

The obligation is deliberately stated as *strict* inequalities on **both** sides.
A gate equal to its oracle ceiling demands perfection from an engine that must
also be honest under §3.0 — and a gate equal to a baseline's score is cleared by
the baseline. Neither is a test.

## What this ruling does not do

- It does **not** set, move, or reinterpret any threshold. It governs what must
  be **known** before a threshold binds.
- It does **not** apply retroactively to invalidate Layers 1 and 2. Those gates
  bind and their layers are claimed. The arithmetic they were never required to
  produce is owed to them the next time either is reopened, not before.
- It does **not** make a gate legitimate merely by being computed. Discrimination
  is necessary, never sufficient: the humility ceiling, the `IMPOSSIBILITY.md`
  argument, and the layer's own defense sentence in §5.1 all still bind.
- It does **not** authorize choosing a corpus *because* it makes a gate reachable.
  The §5 corpus preconditions bind first; the arithmetic is a check applied to a
  corpus already admissible, never a search for one that scores well.

## Enforcement

- `trials/ascension/l3/ATTAINABILITY.md` — the first instance, and the model:
  the oracle ceiling and both baselines, per corpus, machine-checked.
- `trials/ascension/l3/t_forgetting.py::trial_attainable_ceilings_are_as_recorded`
  — the drift check that gives a recorded number teeth.
- `trials/ascension/l3/t_forgetting.py::trial_keep_latest_baseline_cannot_clear_the_gate_on_l3streamb`
  — the named-baseline obligation, asserted permanently and as a trial fixture so
  the policy it guards against never exists in `core/`.
- `trials/laws/t_rulings.py` — that every gate binding a trial applies is
  authorized by §5 or by a ruling here.

---

# R3 — The F measure under eviction

**Status:** FROZEN on commit.
**Binds:** every layer at which `F` is scored under eviction pressure — Layer 3
now, and any later layer whose trials run a stream against a binding budget.
**Authority:** `BOUNDARY.md §3.1`, `§3.0`, and the ratified defense sentence
`§5.1 L3`.
**Holding:** `F` binds as `§5.1` defends it — fidelity over retained/answerable
items, the **corruption** measure. `F_strict` is reported as an ungated
diagnostic wherever `F` binds under eviction.

## The question

`§3.1` defines `F` as the mean per-query score over the query set under the
`§3.0` table, in which an answerable query answered by an abstention scores 100.
`§5.1 L3` defends the `F ≥ 950` threshold in one sentence:

> *"Forgetting may drop items but must never corrupt the ones it keeps, so
> surviving recalls stay exact."*

Under eviction those two sentences pull apart, and the arithmetic is not close.
At 10× pressure and a 1-in-10 budget, an engine is **required by the gate itself**
to forget nine items in ten. Applying the §3.0 table literally — every ingested
item is answerable, so each honest abstention on an evicted item scores 100 —
caps `F` at

```
(1000·1000 + 9000·100 + 100·1000) / (10100 · 1000)  =  198‰
```

for **any** engine, on either stream, however perfect. The ratified `F ≥ 950` is
unreachable under that reading — and unreachable for a reason that has nothing to
do with fidelity: the engine is penalized precisely for obeying the coverage
gate. Read literally, §3.1 and §5 L3 would demand that a Layer-3 engine both
forget nine items in ten and not forget them.

## The ruling

1. **`F` binds as `§5.1` defends it.** Under eviction, `F` is the **corruption**
   measure — fidelity over retained/answerable items:

   | situation | `F` |
   |---|---|
   | item cue, exact stored event returned | **1000** (and *recovered*) |
   | item cue, engine abstains (honest forgetting) | **1000** |
   | item cue, engine returns something else | **0** (corruption) |
   | never-ingested cue, engine abstains | **1000** |
   | never-ingested cue, engine answers | **0** (fabrication) |

   *"May drop items, must never corrupt what it keeps"*: dropping is scored by
   **coverage**, which is the gated measure built to carry that loss, and
   corrupting is scored by **F**. Each loss is counted once, by the measure whose
   job it is.

2. **Abstention is never a way to gain.** Every abstention on an item is a target
   lost from `weighted-C` and `unweighted-C`, both of which gate. An engine cannot
   buy `F` with silence; it pays for the silence in coverage at the same instant.
   This is the property that makes the reading safe, and it is why the reading is
   available at Layer 3 and must not be assumed elsewhere without re-checking it.

3. **`F_strict` is reported wherever `F` binds under eviction.** The literal
   §3.0 reading — every ingested item answerable, an abstention worth 100 — is
   computed over the same query set and **reported in every result**, ungated.
   Reporting it is mandatory, not optional: it keeps the choice of reading visible
   in the output rather than buried in a scorer, and it is the number that would
   expose the reading if it were ever being used to hide something.

4. **This is interpretation, not amendment.** `F ≥ 950` is untouched. §3.0 and
   §3.1 are untouched. What is settled is **which of two readings the ratified
   defense sentence licenses**, in the one situation where they diverge.

## Rationale

Where a ratified threshold and a ratified definition can only be reconciled one
way, that way is the reading — and here only one reading leaves the threshold
meaning anything. Under the literal reading `F ≥ 950` is not a demanding test
that engines will struggle with; it is arithmetically unpassable at 10× pressure,
by the same category of defect R1 addresses. The defense sentence in §5.1 is
itself ratified text, adopted in the same act as the number, and it says plainly
what the number is *for*: not corrupting what is kept. That sentence is the
tiebreak, and it was written into the constitution to be one.

The narrow scope is deliberate. This ruling reaches **only** the situation where
eviction is compulsory — where the gate itself requires the engine to drop most
of the stream. Nowhere else does honest abstention become mandatory rather than
chosen, and nowhere else is the literal §3.0 table anything but exactly right. At
Layer 1, an abstention is a failure to retain and scoring it 100 is correct. At
Layer 6, discriminating a confident answer from a hedge is the entire capability
under test, and the 100 is doing the most important work in the constitution.
**This ruling does not touch either.**

`F_strict` is mandatory for the same reason the ruling is narrow. A reading that
improves a score should have to show the number it replaced, every run, in the
same output. If `F` and `F_strict` ever diverge in a way that flatters the engine
beyond what eviction accounts for, the diagnostic is where it will show.

## What this ruling does not do

- It does **not** change `F ≥ 950`, or any other threshold.
- It does **not** amend `§3.0` or `§3.1`. The table is the table; this settles
  which query set it is applied over when eviction is compulsory.
- It does **not** reach layers where eviction is not compulsory. Layers 1, 2, 4,
  5, 6 and 7 score `F` under the literal §3.0 table unless and until a later
  ruling says otherwise about a specific one of them.
- It does **not** permit the corruption reading without the diagnostic.
  `F_strict` is a condition of the ruling, not a courtesy. `F` read this way
  without `F_strict` reported alongside it is unauthorized.
- It does **not** weaken abstention. Fabrication still scores 0, wrong content
  still scores 0, and both are additionally asserted to be exactly zero by the
  Layer-3 gate trial, independently of `F`.

## Enforcement

- `trials/_l3score.py` — the scorer: `F` as the corruption measure, `F_strict`
  computed alongside and returned in every result dict.
- `trials/ascension/l3/t_forgetting.py` — the `F ≥ 950` gate, plus the
  independent `wrong == 0` and `fabricated == 0` assertions.
- `trials/ascension/l3/ATTAINABILITY.md` — the 198‰ arithmetic, on the record.
- `trials/laws/t_rulings.py` — that this ruling exists and is cited by the trials
  that apply it.

---

# R4 — The Layer 4 ascension gate binds on `corpora/l4stream`

**Status:** FROZEN on commit.
**Binds:** the Layer-4 ascension trials (`trials/ascension/l4/`) and the Layer-4
humility trial (`trials/humility/l4/`), when it exists; clauses 2, 3 and 5 bind
wider, and say so in their own text.
**Authority:** `BOUNDARY.md §5 L4`, `§5.1 L4`, `§3` (the permille unit and §3.5's
rounding rule), `§4.1` (the budget law and its cost model), `§8` (the corpora
doctrine); `BOUNDARY-RULINGS.md R1` (the precedent for binding a stated threshold
to a corpus), `R2` (which required the arithmetic this ruling rests on to exist
first), `R3` (whose scope this ruling deliberately does **not** extend). Resolves
the three questions put for decision in `trials/ascension/l4/ATTAINABILITY.md §6`
and drafted in `trials/ascension/l4/RULING-R4-DRAFT.md`.
**Holding:** the ratified L4 thresholds stand **unchanged**; `footprint ≤ 250` is
read in **permille of the raw episodic footprint**; state is priced under
**rule P**, one cell per grammar atom; the gate binds on **`corpora/l4stream`**;
`corpora/chronicle` and `corpora/murk` are scored as **ungated diagnostics**;
`F` at Layer 4 binds under the **literal §3.0 table**, no extension of R3 taken.

## The question

`BOUNDARY.md §5 L4` states the Layer-4 ascension gate as

```
footprint≤250 (≥4× compression) at reconstruction F≥900, C≥850, B=1000
```

and leaves three things open, each of the kind this document's own preamble names
as legitimately rulable — *which reading of a ratified defense sentence the trials
implement*, *which corpus a stated gate binds on*, and *what procedure binds
future gates*:

1. **In what unit is `250`?** The constitution gives a bare number.
2. **On which corpus?** §5 L4 names none, exactly as §5 L3 named none.
3. **How is a state priced?** §4.1 charges one cell per scalar and per key and
   says nothing about what a scalar may *contain*, so an unconstrained state
   could pack a corpus into one integer and price it at one cell.

The Layer-4 `ASCEND` session answered all three in arithmetic before any engine
existed — R2's obligation, discharged in the order R2 fixed — found that **the
frozen chronicle family cannot admit the ratified gate under any policy
whatsoever**, froze `corpora/l4stream` on the append-only path `l3streamb` took,
stopped at the Stage-A boundary, and deliberately did **not** append its own
ruling. This is that ruling.

## The ruling

### 1. The thresholds stand, and the gate binds on `corpora/l4stream`

**The ratified thresholds stand, unchanged.** `footprint ≤ 250`,
`reconstruction F ≥ 900`, `C ≥ 850`, `B = 1000`, and the humility ceiling
`capped reconstruction F ≤ 400 at footprint ≤ 250` are ratified text and are not
touched, softened, rescaled, or read as a fraction of anything.

**The Layer-4 ascension gate binds on `corpora/l4stream`** (seed `6006`,
`n = 20 000`, `raw_cells = 173 200`, `budget_cap = 43 300`), where the
discrimination R2 requires holds on both sides — and the upper side is
**exhibited, not argued**: a concrete state (the exact interval table, the global
counters, and 854 of the 1 212 irreducible `note` events) fills 43 299 of the
43 300 cells the footprint allows and answers the whole battery.

| policy | C | reconstruction F |
|---|---|---|
| **exhibited oracle state** (43 299 cells, footprint 250‰) | **1000** | **984** |
| **the ratified gate** | **850** | **900** |
| verbatim-truncation at 250‰, keep-latest | 247 | 325 |
| verbatim-truncation at 250‰, keep-first | 249 | 327 |
| current-value-table-only (6 102 cells, 35‰) | 155 | 100 |
| `make_engine(layer_cap = 3)` at 250‰, arithmetic upper bound | 200 | **325** |

- **Strictly below the oracle** (R2 obligation 1): `850 < 1000`, `900 < 984`.
- **Strictly above every named baseline** (R2 obligation 2): `850 > 249`,
  `900 > 327`.
- **The §5 L4 humility ceiling is honest and not vacuous**: the capped engine's
  arithmetic bound is **325**, under the ratified **400** and above the 100
  abstention floor. The ceiling binds without being unreachable.

`F = 984` and not 1000 because the corpus declares an **irreducible tier**: 1 212
`note` events carrying globally unique `text_id`s, which no schema regenerates and
which the footprint cannot wholly afford. The `F ≥ 900` gate therefore measures
honest lossy compression rather than a corpus with nothing to lose.

**`corpora/chronicle` and `corpora/murk` remain, and are scored as ungated
diagnostics**, on the conditional-arithmetic-skip mechanism R1 clause 5 endorsed
as permanent: their ceilings are computed, recorded and drift-checked; a Layer-4
gate trial on them skips **only while** the ceiling lies below the gate, and
engages by itself if that ever changes. Neither corpus is retired, neither's
bytes change, and murk keeps its Layer-4 obligation in full — its **305 recorded
contradictions** (`corpora/murk/ground_truth.json`) are the answer key against
which consolidation must resolve or abstain per §3.0, which is a **strain**
obligation and not a gate. A corpus can be the right dirt without being the right
ruler.

### The two causes, recorded verbatim

> Chronicle's exact history schema costs **151 780 cells = 384‰** against a
> **98 908**-cell budget — short by **52 872** — because **identification does not
> compress**: **35 947 of its 41 785 `(entity, key)` pairs are asserted exactly
> once and never superseded**, so `9 985 + 41 785 = 51 770` cells of any exact
> history schema go on naming pairs rather than on their values. **AND** chronicle
> cannot tell consolidation from a table of last-writes: **a current-value table
> with no history whatsoever scores 697 against a 735 optimum — 95%** (on murk,
> 647 against 754, 86%). **Either cause alone voids a gate bound there.**

Each half is load-bearing and neither is a restatement of the other, so each is
stated again in its own right:

- **The footprint arithmetic is a bound over all policies, not a difficulty.**
  Consolidation buys compression from **redundancy**, and chronicle has
  **1.197×** where the gate demands **4×**; `836‰` of its assertions are their
  pair's latest. Its oracle ceiling at 250‰ is `C ≤ 735` against an 850 gate and
  `F ≤ 683` against a 900 gate — short by 115‰ and 217‰. This is R1's category:
  not a gate an engine might fail, but a gate the arithmetic forbids anything from
  passing. Murk inherits chronicle's grammar and therefore its shape: 364‰,
  `C ≤ 754`, `F ≤ 711`, short by 9 088 cells.

- **The discrimination failure is independent of it, and would survive its
  repair.** Even if chronicle's ceiling somehow reached the gate, R2 obligation 2
  would void a gate bound there, because a policy containing **no consolidation at
  all** — no history, no as-of, no interval, no pattern fold — comes within 38‰ of
  the best any state in the family can do. That is R1's `l3stream` finding
  arriving one layer up: there a keep-latest ring buffer *tied* the optimum, so
  the corpus could not distinguish an importance ordering from an arrival
  ordering. On `l4stream` that same history-free policy is pinned at **155 against
  a 1000 ceiling — 16%**.

Recording both is not belt-and-braces. A later session that repairs the first
cause — a denser chronicle, a re-forged grammar — must not read this entry as
licensing a Layer-4 gate there, because the second cause is untouched by that
repair and voids the binding on its own.

### 2. `footprint ≤ 250` is 250 permille of the raw episodic footprint

```
raw_cells   = Σ_t event_cost(payload_t)        the episodic footprint (§4.1)
footprint‰  = permille(state_cells / raw_cells)
the gate    = footprint‰ ≤ 250   ==   state_cells ≤ raw_cells // 4
budget_cap  = raw_cells // 4                   (§4.1, the same number)
```

This is **the only reading under which three ratified sentences agree**, and each
of the three says something different under any absolute reading:

- §5 L4's own parenthetical, `(≥4× compression)`: `1000 / 250 = 4`.
- §5.1 L4's defense: *"shrink the episodic footprint to at most a quarter of the
  raw bytes"* — a quarter is 250‰.
- §5.1 L4's humility defense: *"a forget-only engine squeezed to a quarter of the
  bytes has simply **lost three-quarters of its episodes**."* Measured, the
  `layer_cap = 3` engine at this cap holds **250‰ of `l4stream`'s episodes**
  (5 010 of 20 000) — three-quarters lost, exactly as defended. Under an absolute
  reading of `250` *units* the same engine holds `250 // 12 = 20` episodes of
  20 000, has lost 99.9% of them, and the ratified defense sentence describes
  nothing that happens.

§3 is also the constitution's own answer to *"in what unit"*: every measure it
defines is calibrated to an integer **in permille**, and §3.5 supplies the one
rounding rule. Under this reading the footprint gate and the §4.1 budget cap are
one number certified twice — `B = 1000` after every write (§3.3, §4.1.2),
`footprint ≤ 250` on the final state — and the two ratified clauses stop being
redundant beside each other.

**The erratum.** `core/layers/README-l3.md §4` reads the same clause as
*"`≤ 250` units"* and derives `250 // 12 = 20` items from it. That README is
frozen (§9.2). Its **historical text is not edited**; a **dated erratum note** is
placed above it recording that this ruling supersedes the parenthetical, in the
form the `PULSE` session established for the `autopsy/*/ANATOMY.md` errata. The
seam that section actually draws is untouched and in fact sharper under this
reading: a forget-only engine at 250‰ retains 5 010 of `l4stream`'s episodes and
still cannot reconstruct the other 14 990.

### 3. Pricing rule P — one cell, one grammar atom

> **Rule P.** Every stored cell holds exactly one **grammar atom** — an entity id,
> a vocabulary token, an attribute value, or a logical `t`. A composite key
> (`"7:status"`), a bit-packed integer, or any concatenation carrying more than
> one atom is priced at the **number of atoms it carries**, not at one cell.

Without rule P no footprint number means anything: §4.1's cost model charges per
scalar and per key without constraining what a scalar contains, so a state could
serialize a corpus into a single integer and claim a footprint of one cell, and
every ceiling in `ATTAINABILITY.md` would be a wish rather than a bound.

Rule P is ruled as a **general** pricing rule, not a Layer-4 one: it makes every
footprint and occupancy figure in the project mean what it has always been read to
mean. It is the smallest constraint that closes the hole while changing no
ratified sentence — it does not alter `payload_cost`, it states what a *lawful*
state may put in a cell, and it is checkable structurally rather than by
inspection. Layers 1–3 already satisfy it (they store grammar values verbatim), so
this clause changes no existing score, and the Layer-4 engine is to be held to it
structurally when it is written.

### 4. `F` at Layer 4 binds under the literal §3.0 table — the concession is declined

R3 excludes Layer 4 in its own text: *"Layers 1, 2, 4, 5, 6 and 7 score F under
the literal §3.0 table unless and until a later ruling says otherwise about a
specific one of them."* **This ruling is not that ruling and does not ask to be.**
At Layer 4 an honest abstention on an answerable reconstruction scores **100**, so

```
F ≥ 9/10   ⟺   at least 8/9 of all events reconstructed EXACTLY
```

exactly on the `Fraction`, which is where §3.1 defines `F`; §3.5's permille
calibration concedes half a permille point on top — 11 events of 20 000 on
`l4stream` — and that concession is asserted **in the measure** rather than
rounded past.

The exhibited witness clears that gate under the literal table — **984 ≥ 900** —
**without any extension**. The layer does not need the friendlier reading, so it
does not take it. The corruption reading is computed alongside as the ungated
diagnostic `F_corruption` (1000 on the witness): **R3's pairing inverted**, so the
**stricter** number binds and the looser one is merely on display.

**No slack was taken here, and none is available to re-litigate.** A later session
that finds Layer 4 hard must not cite this entry as a precedent for extending R3
to it: the record shows the concession was available, examined, and declined
because the gate was attainable without it. Reopening it would require a new
ruling arguing that the arithmetic changed — not that the engine did.

### 5. Methodology: exhibit the ceiling where a witness can be built

**Forward-binding alongside R2, at every layer, including `BOUNDARY-HIGH.md` when
it is written.** Where a concrete witness state can be constructed, a Stage-A
oracle ceiling is to be **EXHIBITED, not merely argued**: the `ATTAINABILITY.md`
must name a state, price it against the budget, score it, and assert that state in
the drift trial — not only bound what some declared family of states could reach.

The Layer-4 form **supersedes the Layer-3 form as preferred practice.** R1's
918‰ ceiling is a maximization over a family of retain-or-drop policies: sound,
and it remains sound. Layer 4's is a state that exists, whose cells are counted,
and whose scores are computed. The difference matters twice over. An argued
ceiling is only as good as the family it quantifies over, and a mis-declared
family is a silent error that flatters the corpus; an exhibited one needs no
family assumption on the side where R2 obligation 1 bites. And a family
maximization that *agrees* with an exhibited witness — as it does here, `C ≤ 1000`
and `F ≤ 984` — is a check on the maximization rather than a substitute for it.

The obligation is conditional by design, and the condition is the honest part:
where no witness can be constructed — because the gate is unattainable there, as
on the chronicle family, or because the construct family is genuinely infinite —
the argued form remains legitimate and R2 is satisfied by it. What is ruled out is
arguing a ceiling when a witness was available and simply not built.

## Rationale

The repair belongs at the binding, not at the number, and for the same reason as
in R1: nothing in §5 L4 or §5.1 L4 mandates a write-once world. The conflict was
never between the gate and the constitution — it was between the gate and one
generator's free choice of *history shape*, made before anyone computed what that
choice implied. Chronicle was forged at Phase 0 to be a large, plausible event
log; nobody asked it to be redundant, and it is not. `footprint ≤ 250` demands 4×
redundancy and chronicle supplies 1.197×.

**No engine's inability motivated this.** `core/layers/l4_consolidation.py` does
not exist. The Layer-4 ASCEND session withheld it at the sanctioned Stage-A
boundary precisely so that this ruling would be decided against arithmetic rather
than against a score, and the ordering R2 fixed — *attainability arithmetic →
trials → engine* — is what made that withholding a rule rather than a virtue. As
in R1: had an engine existed, this ruling should have been harder to obtain.

**And this ruling is harder to obtain than R1 was, deliberately.** R1 rebound a
gate whose binding corpus made it unreachable. Here the reachability finding is
**paired with an exhibited witness on the new corpus** and with a second,
independent ground — the discrimination failure — that would void the old binding
even if the first were repaired. Clause 5 makes that pairing the standing
expectation rather than this session's good manners.

The two readings ratified in clauses 2 and 3 are of a different character from the
binding, and are stated separately for that reason. Neither is a choice between
defensible alternatives: clause 2 is the only reading under which three ratified
sentences are one sentence, and clause 3 is the difference between a footprint
measure and a number that can be driven to 1 by encoding. Ratifying them settles
what the trials implement; it does not add to what the constitution demands.

## What this ruling does not do

- It does **not** amend `BOUNDARY.md`. No ratified sentence is edited or reread.
- It does **not** change any threshold, in either direction, on any layer.
- It does **not** retire `corpora/chronicle` or `corpora/murk`, weaken their ops
  trials, or touch their frozen bytes; murk's Layer-4 strain obligation is
  unchanged and its 305 contradictions still bind as an answer key.
- It does **not** edit `core/layers/README-l3.md`'s historical text. Clause 2
  supersedes one parenthetical in a frozen document by stating the better reading
  on the record and placing a dated erratum note above it; the historical text
  stays as it is, wrong on that point, forever.
- It does **not** extend R3 to Layer 4, or to anything (clause 4).
- It does **not** license "score it on an easier corpus". R1 refused that reading
  of itself and the refusal is repeated here: the §5 corpus preconditions bind
  first, the arithmetic is a check applied to a corpus already admissible, and
  `l4stream` is *harder* in the sense that matters — chronicle cannot distinguish
  consolidation from a table of last-writes, and `l4stream` pins that same policy
  at 155 against a 1000 ceiling.
- It does **not** claim Layer 4, grant a Layer-4 capability, or license an engine.
  It settles what the Layer-4 trials measure and on what. Stage B onward —
  `trials/ascension/l4/t_consolidation.py`, `trials/humility/l4/` and its
  mandatory `IMPOSSIBILITY.md` (§6), and only then the engine — is unwritten, and
  R2's standing step still orders it.

## Enforcement

- `trials/ascension/l4/ATTAINABILITY.md` — the recorded arithmetic this ruling
  rests on, now citing R4 as the authority that ratified its three questions.
- `trials/ascension/l4/t_attainability.py` — the exhibited witness, the
  discrimination check on `l4stream`, the chronicle-family finding stated as the
  condition that lifts its own deferral, and the drift check over every recorded
  number.
- `trials/ops/l4/t_l4stream.py` — the corpus properties the discrimination rests
  on: bounded population, declared redundancy, the irreducible tier, and the
  contrast with the chronicle family.
- `trials/laws/t_rulings.py` — the gate registry, where the five Layer-4 constants
  now carry this entry beside their §5 L4 clauses, and the completeness check that
  forbids an unregistered gate constant anywhere under `trials/`.

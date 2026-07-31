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

---

# R5 — Identity gates, minimizing clauses, and what an `ATTAINABILITY.md` must price

**Status:** FROZEN on commit.
**Binds:** `BOUNDARY-RULINGS.md R2` itself — how its two discrimination
obligations are discharged — at **every layer, including `BOUNDARY-HIGH.md`**
when it is written; and, as its immediate application, the Layer-5 ascension and
humility trials when they exist.
**Authority:** `BOUNDARY.md §5 L5`, `§5.1 L5`, `§3.0` (the abstention-aware
table), `§3.3` (the budget measure), `§3.4` (the `n/a` convention for an
undefined statistic), `§4.1` (the budget law and its cost model), `§7.1` (the
three operations); `BOUNDARY-RULINGS.md R2` (whose obligations this ruling
reads), `R3` (whose scope this ruling deliberately does **not** extend), `R4`
clauses 3 and 5 (pricing rule P; the exhibited-ceiling methodology this ruling
continues). Ratifies `trials/ascension/l5/RULING-R5-DRAFT.md`, which resolves
questions 1 and 2 of `trials/ascension/l5/ATTAINABILITY.md §6`.
**Holding:** for a gate stated as an **identity over discrete correctness**,
R2's upper obligation is discharged by an **exhibited witness attaining** the
identity; R2's lower obligation is read **direction-aware** and over the
**conjunction** of a gate's clauses; every future `ATTAINABILITY.md` declares the
**policy class** its ceiling is exact over; and attainability pricing includes
**operational bookkeeping** and **loss-accounting reserves**, or disclaims them
with reasons.

Every number cited below is measured in `trials/ascension/l5/ATTAINABILITY.md`
and machine-checked in `trials/ascension/l5/t_attainability.py`. **Nothing in
this entry is argued from anywhere else.**

## The question

R2 says a gate must lie *"strictly below the oracle ceiling and strictly above
every capability-free baseline on its binding corpus."* At Layers 3 and 4 both
halves were satisfiable by measurement: `850 < 918`, `850 > 249`, `900 < 984`,
`900 > 327`.

`§5 L5` is the first gate the constitution states as an **identity**:

```
trigger-precision=1000, trigger-recall=1000, dup-fire=0, miss=0, F≥980, B=1000
```

Four of those six clauses admit no strict inequality on the upper side, on any
corpus, ever. `trigger-precision` is a ratio of a subset to its superset and
cannot exceed 1000; `dup-fire` and `miss` are cardinalities and cannot fall below
0. The oracle ceiling **is** the gate. And two of them admit no strict inequality
on the *lower* side either, because they are **minimizing** clauses: R2's
*"strictly above"* would demand a baseline with a negative count.

The `[L4] [PULSE]` session named this as the biggest risk to Layer 5 before any
Layer-5 code existed (`BOUNDARY.log` line 24). Stage A has now measured it, and
found the lower-side half of the problem as well, which was not predicted.

**This is not a Layer-5 anomaly.** `B = 1000` has been an identity gate at every
layer **since Layer 1** — `§3.3` makes any value below 1000 *"a breach of the
budget law and … disqualifying"*, so its ceiling is exactly 1000 — and neither
`trials/ascension/l3/ATTAINABILITY.md` nor `trials/ascension/l4/ATTAINABILITY.md`
subjected it to obligation 1. `footprint ≤ 250` is a minimizing clause and R4's
discrimination table scores its baselines on `C` and `F` only. **What is new at
Layer 5 is not the problem but the impossibility of leaving it unexamined**, since
four of this layer's own characteristic measures are identities rather than one
incidental budget law. Ratifying this entry regularizes practice the ladder has
already been following without saying so; it does not invent an exemption.

## The ruling

### 1. For a gate stated as an identity, the upper obligation is discharged by an EXHIBITED ATTAINMENT

**Where a `§5` clause states an identity over discrete correctness — an exact
count, an exact ratio, a `0` or a `1000` that admits no better value — R2
obligation 1 is discharged by exhibiting a concrete witness that ATTAINS it: a
named policy, priced against the budget, scored, and asserted in the layer's
drift trial. The strict inequality is not required of such a clause and never
was reachable for one.**

The mischief R2 names is stated in its own rationale: *"A gate at or above the
oracle ceiling is **void**: it forbids what it purports to test."* An attaining
witness is precisely the proof that the mischief is absent. A gate nothing can
reach forbids what it tests; a gate something demonstrably reaches does not,
whether or not a strict inequality is available.

**The counter-argument, recorded rather than answered away.** R2's rationale also
says: *"A gate equal to its oracle ceiling demands perfection from an engine that
must also be honest under §3.0."* That objection is real and this ruling does not
dismiss it. Three things answer it here, and the second and third are why the
ruling is stated for a *class* of clause rather than for Layer 5:

- `§5.1 L5` asks for exactly the thing R2 worries about, in the constitution's own
  words: ***"prospection is exact or it is broken."*** The demand for perfection
  is ratified text, not a session's ambition.
- The §3.0 tension **does not arise** for these four clauses. `§3.0` governs
  answering versus abstaining on a query; `trigger-precision`, `trigger-recall`,
  `dup-fire` and `miss` count **firings**, and abstention is not one of the
  available behaviours — an intention fires or it does not. The honesty an engine
  is asked for here is *not firing when nothing satisfies the condition*, and the
  corpus tests exactly that with 180 never-fires intentions whose correct handling
  is scored.
- Where the tension **does** arise, the constitution already gave slack. The one
  clause of `§5 L5` that scores answers under §3.0 is `F`, and `F` was ratified at
  **980, not 1000** — a margin of 35 wrong answers or 38 abstentions out of the
  1 710-query battery. `F` discharges R2 obligation 1 by the ordinary Layer-3/
  Layer-4 method (`980 < 1000`) and is deliberately **not** covered by this clause.
  One `§5` clause therefore contains both kinds of sub-gate at once, which is the
  strongest available evidence that the distinction this ruling draws is the
  constitution's own and not an invention.

**The evidence, measured at Stage A.** The exhibited witness over
`corpora/l5stream` — fire each intention exactly at its satisfaction point, in
`iid` order where several fall at one caller index — scores

```
trigger-precision 1000    trigger-recall 1000    dup-fire 0    miss 0    F 1000
at 41 951 of 45 638 cells (230 permille), a margin of 3 687
```

and its firing trace is recorded, not summarized. The 41 951 cells are priced
with the operational bookkeeping and the loss reserve clause 4 requires — 633
cells carried by name and a 35-cell aggregated forgetting record reserved because
the witness genuinely releases content it cannot regenerate — so the margin this
entry freezes is a margin after the two items Layer 4 learned to price, not
before them.

**One property of identity ceilings that makes this clause safer than R2's
argued-ceiling case.** `[L4] [ASCEND]` recorded that the Layer-4 engine passed
**through** Layer 3's 918‰ oracle ceiling, because that ceiling was a maximization
over *retain-or-drop* policies and a consolidating engine is not in that family.
No such pass-through is possible here: `precision ≤ 1000`, `recall ≤ 1000`,
`dup-fire ≥ 0` and `miss ≥ 0` are **logical maxima over every policy whatsoever**,
not maximizations over a declared family. There is nothing on the other side to
pass through to, and that is a property of the measures rather than a promise
about engines.

### 2. The lower obligation is read direction-aware, and over the conjunction

**R2 obligation 2 binds unchanged in substance and is clarified in two respects.
First, for a MINIMIZING clause — one where a lower value is better — "strictly
above" reads as "strictly better", i.e. strictly below. Second, where a
capability-free baseline TIES a single clause, the obligation is discharged over
the gate's CONJUNCTION: what must be shown is that no named capability-free policy
clears the gate, not that none ties any one clause of it. Every clause's
arithmetic is recorded either way.**

Read clause by clause, obligation 2 fails at Layer 5 for a reason that has nothing
to do with the corpus: `dup-fire = 0` is tied by three of four named baselines and
`miss = 0` by two, because a policy that fires exactly once per intention gets
`dup-fire = 0` for free and a policy that fires every intention gets `miss = 0`
for free. Neither is a capability. What is a capability is getting them **at the
same time as** precision and recall.

The measured table, from `ATTAINABILITY.md §5`:

| policy | precision | recall | dup-fire | miss | F | clauses cleared |
|---|---|---|---|---|---|---|
| the gate | 1000 | 1000 | 0 | 0 | 980 | — |
| `make_engine(layer_cap = 4)` | *n/a* | 0 | **0** | 765 | 270 | 1 of 5 |
| fire-on-every-write | 0 | 0 | 9 183 176 | **0** | 0 | 1 of 5 |
| fire-immediately | 116 | 144 | **0** | **0** | 116 | 2 of 5 |
| fire-on-`kind`-atom-only | 375 | 379 | **0** | 77 | 397 | 1 of 5 |

**No named baseline clears more than two of the five scored clauses**, and the
best of them is 621‰ short on precision and 621‰ short on recall. The drift trial
asserts the bound at three, so that a future policy clearing four would reopen the
corpus binding rather than pass unnoticed.

> **One number stated exactly, because this entry freezes it.** The `capped-4`
> row's `F` reads **270** in the Stage-A draft and in `ATTAINABILITY.md §5`;
> `t_attainability.py`, which is what a drift turns red, pins it at **271** — the
> capped policy abstains on all 945 P1 queries, which §3.0 scores 100 on the 765
> answerable ones and 1000 on the 180 unanswerable ones, i.e. 256 500 / 945 000.
> The difference is one permille of a policy that clears one clause of five under
> either figure, so no holding here turns on it. The Stage-A numbers are left
> exactly as they were written; this note records which of the two the trial
> enforces, so the discrepancy is on the record rather than in a diff nobody runs.

This clause is stated forward-binding because Layer 6 needs it immediately:
`Brier ≤ 40` and `ECE ≤ 30` are both minimizing, and `§5 L4`'s `footprint ≤ 250`
already was.

### 3. Every `ATTAINABILITY.md` declares the policy class its ceiling is exact over

**Forward-binding at every layer, including `BOUNDARY-HIGH.md`: a Stage-A ceiling
is stated together with the class of policies it is exact over. Where the ceiling
is a logical maximum over all policies, that is what is declared, and the
declaration is short. Where it is a maximization or a price over a family, the
family is named and its edge is stated.**

This is the **Form-B pass-through lesson**, made a standing obligation. Layer 3's
918‰ ceiling was sound and remains sound — and the Layer-4 engine scored 924
through it, because the ceiling was exact over *retain-or-drop* policies, the
family Layer 3 could choose from, and the consolidating engine was not in it. No
Layer-3 number moved and none should have; what was missing was a sentence saying
what the number was a maximum over. R4 clause 5 already made an *exhibited* ceiling
preferred practice where a witness can be built; this clause adds the half that
applies whether or not one can.

`ATTAINABILITY.md §3` is the model: it declares **two** classes, because it makes
two kinds of claim — the identity ceiling is class-independent (a logical maximum),
while the budget price of 41 951 cells is exact only over *"states that answer the
P1/P2 battery and maintain the Layer-4 assertion facet of `corpora/l5stream`
exactly, under rule P, with the fired events' own storage counted inside the
cap"*. A cheaper state outside that class is exhibited beside it — the
prospection-only witness at 4 505 cells, which attains the same identity while
carrying nothing of the world at all — precisely so that the class is not a
formality.

### 4. Attainability pricing includes operational bookkeeping and loss-accounting reserves, or disclaims them with reasons

**Forward-binding at every layer: an `ATTAINABILITY.md` that prices a state prices
(a) the operational bookkeeping that state's own design requires — indices,
atlases, counters, shape headers — and (b) any reserve the loss-accounting
discipline requires under that corpus's pressure profile; or it states explicitly
that an item is not priced, and why. An unpriced item is not a saving; it is a
margin that has already been spent.**

Both halves are paid for by measured failures, not by prudence:

- **Operational bookkeeping.** `[L4] [ASCEND]` (`BOUNDARY.log` line 23) recorded
  that Stage A's declared 2 563-cell working room contained **656 cells the
  witness never priced** — 600 per-entity irreducible counts, a 32-cell key atlas,
  a 23-cell forgetting record, a demotion counter — leaving five cells at the end.
  The margin was a real number and it was already spoken for.
- **The loss-accounting reserve.** `[L4] [STRAIN]` (line 26) turned GAPMAP §2's
  *"recorded but never binding"* thesis on this project's own engine: a
  non-invertible fold was booked as a **lossless demotion** while `read(t)`
  abstained on it forever — 7 demotions, 0 recorded losses, content gone. The fix
  demanded truthful accounting rather than a policy, and truthful accounting costs
  cells that a Stage-A price must reserve on every path that can record a loss.

`ATTAINABILITY.md §4` prices both by name — 633 cells of bookkeeping computed from
this corpus's own shape, and a 35-cell aggregated forgetting record reserved
**because the witness genuinely releases content it cannot regenerate**, which the
drift trial asserts rather than assumes. It also states, separately, that its
4 493-cell prospection line is a **bound** (peak pending set plus final fired-row
count — two maxima that do not occur at the same moment) against a measured joint
peak of 4 448, so neither number can be quoted as the other.

## The historical instances are REGULARIZED, not errata

This ruling reaches practice that already existed, so the record must say exactly
what happens to it. **Nothing previously stated was false.** No number, no
ceiling, no baseline table and no verdict of an earlier `ATTAINABILITY.md` is
corrected, withdrawn, or reread by this entry. What ends is an **omission** — a
class of clause that was never subjected to the obligation, in documents that
never claimed it had been.

The instances, named so that "already the practice" is a checkable statement and
not a comfort:

- **`B = 1000`, at every layer since Layer 1.** `§3.3` makes any value below 1000
  disqualifying, so its ceiling is exactly 1000 and it has always been an identity
  clause. `trials/ascension/l3/ATTAINABILITY.md` and
  `trials/ascension/l4/ATTAINABILITY.md` recorded it as a gate and did not score it
  against an oracle. Under clause 1 it is discharged the way it always in fact was:
  by states that attain it — Layer 3's retained set inside 11 000 units, Layer 4's
  exhibited witness at 43 299 of 43 300 cells — now said out loud.
- **`footprint ≤ 250`, at Layer 4.** A minimizing clause, and R4's discrimination
  table scored its named baselines on `C` and `F` only. Under clause 2 that table
  is read direction-aware and over the conjunction, which is how R4 clause 1 in
  fact applied it: every named baseline is priced *at* 250‰ and beaten on the
  clauses that discriminate. The table is not restated and does not move.
- **`dup-fire = 0` and `miss = 0`, at Layer 5.** The first instance where the
  omission cannot be carried, because these are the layer's own characteristic
  measures rather than one incidental budget law. They are governed by clauses 1
  and 2 from this entry forward, and Stage A's arithmetic for them is already on
  the record.

**From here the obligation is explicit.** A future `ATTAINABILITY.md` that meets
an identity clause discharges obligation 1 by exhibiting an attaining witness, and
one that meets a minimizing clause reads obligation 2 direction-aware and over the
conjunction — and both say so in their own text. R2 obligations 3 and 4 are
unchanged and reach these clauses exactly as they reach every other: the
arithmetic is computed, recorded and machine-checked before the gate binds, and a
gate without it has no authority.

## Rationale

**The repair belongs at the reading of R2, not at any `§5` number.** No threshold
moves in either direction, on any layer. `§5 L5`'s identity stands exactly as
ratified, and `§5.1 L5` defends it in terms this ruling quotes rather than
reinterprets. What is decided is what R2 — itself a ruling, not the constitution —
requires of a session before such a gate acquires authority.

**No engine's inability motivated this.** `core/layers/l5_prospection.py` does not
exist. Stage A was delivered as its own session and stopped at the sanctioned
boundary precisely so that this ruling would be decided against arithmetic rather
than against a score, which is R2's own standing step — *attainability arithmetic →
trials → engine* — doing the work it was installed to do. As in R1 and R4: had an
engine existed, this ruling should have been harder to obtain.

**And the finding is larger than the prediction, which is recorded as such.** The
`[L4] [PULSE]` session predicted the upper-obligation collision. It did not predict
the lower one, and the lower one is in some ways the sharper finding: R2's
obligation 2 is *written in a direction*, and three of the four gates the ladder
has ratified since include a clause that runs the other way. The prediction was
right about Layer 5 and incomplete about R2. Clause 2 exists because the
measurement said so.

**What this ruling deliberately does not make easier.** Clause 1 discharges an
obligation only for a clause the constitution states as an identity — not for a
threshold a session finds hard. `F ≥ 980` is inside `§5 L5` and is expressly
excluded from clause 1, because it discharges obligation 1 normally and a layer
that does not need a concession does not get one. That is R4 clause 4's discipline
applied to a different obligation: *the concession was available, examined, and
declined where it was not needed.*

## What this ruling does not do

- It does **not** amend `BOUNDARY.md`. No ratified sentence is edited or reread.
- It does **not** change any threshold, in either direction, on any layer. In
  particular it does not lower `trigger-precision`, `trigger-recall`, `dup-fire`,
  `miss` or `F`, and does not propose that any of them should have been stated
  differently.
- It does **not** weaken R2. Obligations 3 and 4 are untouched: the arithmetic
  must still be computed, recorded and machine-checked before a gate binds, and a
  gate without it still has no authority. Obligation 2 keeps its full force over
  the conjunction, and clause 3 adds an obligation R2 did not have.
- It does **not** exempt a clause from obligation 1 merely because a session
  found it hard. The exemption is available only to a clause whose ceiling is
  provably the gate by arithmetic — and where it applies, an *attaining witness*
  is required, which is a stronger evidentiary burden than a strict inequality,
  not a weaker one.
- It does **not** extend R3 to Layer 5. `F` binds under the literal `§3.0` table,
  as R3's own text provides, and no extension is requested because the oracle
  reaches 1000.
- It does **not**, by itself, bind the Layer-5 gate to `corpora/l5stream`. That
  binding is question 4 of `ATTAINABILITY.md §6` and remains a separate decision in
  the shape R1 and R4 established; it is not taken here, and the Layer-5 constants
  in `trials/laws/t_rulings.py` carry this entry for the *reading* of R2 they are
  scored under, not for a corpus binding.
- It does **not** correct anything. The historical instances above are
  **regularized**, not errata: no earlier document said something false, and none
  is edited, annotated or reread.
- It does **not** settle the engine-`t` question. `§1.3` gives every event its own
  logical `t` and a fired event is an event, so over `corpora/l5stream` the
  exhibited witness turns 20 000 caller writes into 20 765 logical times, the last
  firing landing at `t = 20 760` — **one caller `ingest` advancing `next_t` by more
  than one**, which every anchor and the whole `inheritance/` class currently
  assume it cannot. That is measured and asserted at Stage A
  (`trial_one_caller_ingest_can_advance_next_t_by_more_than_one`) and deliberately
  left open: it is a Stage-B and Stage-C design question, and settling it in a
  ruling written before those trials exist would be exactly the ordering R2 forbids.
- It does **not** claim Layer 5, grant a Layer-5 capability, or license an engine.
  Stage B onward — `trials/ascension/l5/t_prospection.py`, `trials/humility/l5/`
  and its mandatory `IMPOSSIBILITY.md` (§6), `trials/inheritance/l5/`, and only
  then the engine — is unwritten, and R2's standing step still orders it.

## Enforcement

- `trials/ascension/l5/ATTAINABILITY.md` — the recorded arithmetic this entry
  rests on, and the model for clauses 3 and 4; it now carries a dated ratification
  note above its Stage-A text, which is unedited.
- `trials/ascension/l5/RULING-R5-DRAFT.md` — the draft a human ratified, retained
  unedited beneath a dated note naming **this entry** the binding text.
- `trials/ascension/l5/t_attainability.py` — the exhibited witness
  (`trial_the_exhibited_witness_attains_the_identity`), the two obligations stated
  as findings so they cannot be quietly restated
  (`trial_r2_obligation_1_is_not_dischargeable_by_a_strict_reading`,
  `trial_r2_obligation_2_ties_on_the_minimizing_clauses_and_holds_on_the_conjunction`),
  the priced bookkeeping and reserve
  (`trial_both_layer4_lessons_are_priced_rather_than_disclaimed`), the bound-versus-
  measurement pairing (`trial_the_prospection_price_is_a_bound_and_the_bound_is_stated`),
  and the drift check over every recorded number.
- `trials/ops/l5/t_l5stream.py` — the corpus properties the arithmetic rests on,
  including the GUARDEDNESS induction that makes satisfaction points a property of
  the frozen bytes rather than of an engine.
- `trials/laws/t_rulings.py` — the gate registry, where the seven Layer-5
  constants now carry this entry beside their `§5 L5` clauses, and the
  completeness check that forbids an unregistered gate constant anywhere under
  `trials/`.

---

# R6 — The Layer 5 gate binds on `corpora/l5stream`; a firing's logical time

**Status:** FROZEN on commit.
**Binds:** the Layer-5 ascension trials (`trials/ascension/l5/`) and the Layer-5
humility trial (`trials/humility/l5/`); clause 2 binds **every layer from here
on**, including `BOUNDARY-HIGH.md` when it is written, and clause 3 binds the
ATTAINABILITY/ruling practice at every layer.
**Authority:** `BOUNDARY.md §1.1`, `§1.3`, `§1.4`, `§2.1`, `§2.2`, `§2.3`,
`§4.1`, `§5 L5`, `§5.1 L5`, `§7.1`, `§7.2`, `§7.3`, `§8`;
`BOUNDARY-RULINGS.md R1` and `R4` (the precedent for binding a stated threshold
to a corpus), `R2` (whose obligations this rests on), `R3` (whose scope this
does **not** extend), `R4` clauses 3 and 5, `R5` (whose four clauses govern how
R2's obligations are discharged here, and which expressly left the `t` question
to Stage B). Resolves question 4 of `trials/ascension/l5/ATTAINABILITY.md §6`,
the question `R5` recorded as open, and question 3 of the same section. Ratifies
`trials/ascension/l5/RULING-R6-DRAFT.md`, drafted at Stage B from measurements
and the tabulated contradiction check in `trials/ascension/l5/STAGE-B.md §1.5`.
**Holding:** the ratified `§5 L5` thresholds stand **unchanged**; the Layer-5
ascension gate **and** the Layer-5 humility ceiling both bind on
`corpora/l5stream`; a **firing is an event and occupies a logical `t` of its
own**, so one caller `ingest` advances `next_t` by `1 + f`; where a prose figure
and a machine-checked one diverge, **the machine-checked one is the enforced
one** and the divergence is recorded rather than edited away; and
`budget_cap = raw_cells // 4` is the Layer-5 budget reading.

## The question

`§5 L5` states the Layer-5 ascension gate as

```
trigger-precision=1000, trigger-recall=1000, dup-fire=0, miss=0, F≥980, B=1000
```

with a humility ceiling of `capped trigger-recall ≤ 50`, and — exactly as `§5 L3`
and `§5 L4` did — names **no corpus**, no budget ratio, and no rule for what
happens to logical time when a trigger fires.

`R5` settled the two *methodological* questions Stage A put (how R2's obligations
are discharged for an identity clause and for a minimizing one) and deliberately
took neither of the two *substantive* ones: it does not bind the gate to a
corpus, and it does not settle the engine-`t` question. Stage B has now written
the ascension, humility and inheritance batteries, engine-free, which is the
point in R2's standing step at which both may be decided. This is that ruling.

## The ruling

### 1. The thresholds stand, and both sides of the Layer-5 gate bind on `corpora/l5stream`

**The ratified thresholds stand, unchanged.** `trigger-precision = 1000`,
`trigger-recall = 1000`, `dup-fire = 0`, `miss = 0`, `F ≥ 980`, `B = 1000` and
the humility ceiling `capped trigger-recall ≤ 50` are ratified text and are not
touched, softened, rescaled, or read as a fraction of anything.

**The Layer-5 ascension gate binds on `corpora/l5stream`** (seed `7007`,
`n = 20 000`, `raw_cells = 182 555`), and **so does the Layer-5 humility
ceiling.** The two are bound together in one clause because binding them apart
would discriminate nothing: a ceiling measured on one corpus beside a gate
cleared on another is two facts about two worlds.

**The upper side is EXHIBITED, per R5 clause 1** — the discharge that clause
makes available to an identity gate, and the stronger evidentiary burden it
imposes rather than the weaker one:

| policy | precision | recall | dup-fire | miss | F | clauses cleared |
|---|---|---|---|---|---|---|
| **exhibited witness** (fire each intention at its own satisfaction point, `iid` order), 41 951 of 45 638 cells = 230‰ | **1000** | **1000** | **0** | **0** | **1000** | 5 of 5 |
| **the ratified gate** | 1000 | 1000 | 0 | 0 | 980 | — |
| `make_engine(layer_cap = 4)` — no trigger machinery | *n/a* | 0 | **0** | 765 | 271 | 1 of 5 |
| fire-on-every-write | 0 | 0 | 9 183 176 | **0** | 0 | 1 of 5 |
| fire-immediately (condition unread) | 116 | 144 | **0** | **0** | 116 | 2 of 5 |
| fire-on-`kind`-atom-only | 375 | 379 | **0** | 77 | 397 | 1 of 5 |

**The lower side holds over the conjunction, per R5 clause 2**: no named
capability-free policy clears more than **two of the five** scored clauses, and
the strongest of them is 621‰ short on precision and 621‰ short on recall. The
two clauses baselines do tie — `dup-fire = 0` and `miss = 0` — are minimizing,
and a policy that fires once per intention gets the first for free while one that
fires everywhere gets the second. Neither is a capability. What is a capability is
holding both **at the same time as** precision and recall. `t_attainability.py`
asserts the conjunction bound at **three**, so a policy clearing four would reopen
this binding rather than pass unnoticed.

**The humility side is measured on an engine, not only on a policy — which is
what Stage B adds to the record.** Stage A scored `capped-4` as a *policy* that
never fires. Stage B runs `make_engine(layer_cap = 4)` — the frozen Layer-4
engine — over the whole 20 000-event stream through the generic interface (§7)
and measures **trigger-recall 0** against the ratified ceiling of 50, with
precision `n/a` (§3.4's convention for an empty class), dup-fire 0, miss 765,
`F` 271, `wrong = 0`, `fabricated = 0`, `B = 1000`. The ceiling is not breached,
is not vacuous, and is **loose for a structural reason**: firing is not a
behaviour that engine has, so the numerator is empty by construction.

**Why there is no alternative substrate, and why that is not a corpus search.**
R2 warns that its arithmetic *"does not authorize choosing a corpus because it
makes a gate reachable"*. That mischief cannot arise here. `§5 L5` states no
corpus precondition; an intention is an ingested payload under a declared grammar
reading (`ATTAINABILITY.md`'s Reading 1, forced by `§7.1` and `§1.1`); and **no
other frozen corpus contains an `intend` payload at all** — chronicle, sessions,
murk, l3stream, l3streamb and l4stream have no intentions, so on them the
`trigger-recall` denominator is 0 and every Layer-5 measure is undefined rather
than low. `l5stream` was frozen at Stage A, before any Layer-5 trial and before
any engine, on the append-only path `l3streamb` and `l4stream` took.

**There is consequently no diagnostic corpus family at Layer 5**, and this entry
does not invent one. R1 clause 5's conditional arithmetic-skip kept `l3stream`
and later `chronicle`/`murk` as *ungated diagnostics* because those corpora could
still be **scored** — their ceilings were low, not undefined. A corpus with no
intentions cannot be scored for prospection at any value; reporting `n/a` from
six corpora would be six ways of saying the same nothing. What replaces the
diagnostic here is `ops/l5/t_l5stream.py`'s declared corpus properties and the
four named policies, all of which run every suite.

### 2. A firing is an event and occupies a logical `t` of its own

**Ruled, and forward-binding at every layer that emits an event of its own:**

> **A trigger's firing is an event (`§5 L5`: `intend(condition → event)`). Under
> `§1.4` an in-engine event record is exactly `{payload, t}`, and under `§1.3`
> `t` is unique within a state and strictly increasing in ingestion order.
> Therefore a firing consumes a logical `t` of its own, assigned in the same pure
> transition as the caller write that satisfied it, immediately after that write
> and before any later caller write, consecutively and in `iid` ascending order
> where one write satisfies several pending intentions. `ingest` returns the
> **caller** event's `t`. One caller `ingest` therefore advances `next_t` by
> `1 + f`, where `f` is the number of firings that write caused.**

**`§7.1`'s "appends one event" is read as describing the caller's payload** — one
payload, one event, one returned `t` — and **not** as a cardinality limit on the
transition. That is the only reading under which `§5 L5` and `§7.1` are both
true: under the other, a fired event could never be appended at all, `§7.1`
declares only three operations, and prospection would be unreachable by any
lawful engine. It is the same argument, in the same place, that
`ATTAINABILITY.md`'s Reading 1 already made when it held that an intention cannot
be a fourth verb — and it is a **reading of ratified text, not an amendment of
it**.

**Layers 1–4 do not move, and not by exception.** The rule is *one caller event
plus the firings it caused*; on a stream with nothing pending, `f = 0`, and
*"one ingest, one `t`"* is that rule's `f = 0` case. No anchor's recorded
`next_t` changes, no frozen trial's `t = 0, 1, 2` changes, and the
`inheritance/` class replays unchanged — because **no corpus any of them replays
carries an intention**, which is asserted over the bytes of every corpus in the
registry
(`ascension/l5/t_prospection.py::trial_one_caller_ingest_advances_next_t_by_exactly_one_on_an_intention_free_stream`)
rather than assumed. A corpus frozen later that carried intentions turns that
trial red and forces the question to be answered again, in the open.

**Two things are expressly NOT decided by this clause**, and a later session may
not cite it as having decided them:

- **Cascades.** Whether an engine-emitted event is itself a "write" that pending
  conditions are tested against is not forced by any ratified text, and is
  **unobservable** on `corpora/l5stream` by construction: the GUARDEDNESS
  induction makes it impossible for any condition in the grammar to be satisfied
  by a `fired` payload, asserted as an induction and over the whole 945 × 945
  cross product. Both readings produce the identical schedule here. The `t` rule
  above holds under either.
- **What an engine owes when the budget cannot house a firing.** The gate fixes
  the invariants — `B = 1000` after every write, the `t` partition, exactly-once
  — and one consequence: a firing is not discretionary, since `miss = 0` means an
  intention whose condition is satisfied fires. Whether an engine makes room by
  the inherited Layer-3/Layer-4 eviction path or refuses the whole transition
  under `§4.1.2` is a Stage-C design question this entry leaves open.

The full derivation, the alternatives and the contradiction check against every
text that could object are `trials/ascension/l5/STAGE-B.md §1`, which this clause
ratifies rather than summarizes.

### 3. Where a prose figure and a machine-checked one diverge, the machine-checked one binds

**Forward-binding at every layer:**

> **Where a document states a quantity that a trial also computes, the trial's
> value is the enforced one. A prose figure that differs is NOT edited into
> agreement: the historical text stands as written, the divergence is recorded —
> in the ruling that freezes the entry where one exists, and otherwise by a dated
> erratum note above the text naming the machine-checked source of record — and
> the session that finds it says so in `BOUNDARY.log`. An unrecorded divergence
> is the failure; a recorded one is a document doing its job.**

`R5` performed exactly this once, as a boxed note, for the `capped-4` baseline's
`F`: `ATTAINABILITY.md §5` reads **270**, `t_attainability.py` pins **271**, and
R5 recorded which the trials enforce *"so the discrepancy is on the record rather
than in a diff nobody runs."* Two things since make the one-off worth
generalizing:

- **A third artifact now reports it.** `humility/l5/t_prospection.py` measures the
  capped **engine** — not a policy — through the generic interface and gets
  **271**: 945 P1 abstentions, 100 on each of the 765 answerable and 1000 on each
  of the 180 unanswerable, `256 500 / 945 000`. The figure is arithmetic and the
  seam is documentation. No holding turns on it under either number.
- **A second, larger instance was found this session.**
  `corpora/l5stream/grammar.md`'s closing block claims *"Every number below is a
  `DECLARED_*` constant in `generator.py` and is asserted by
  `trials/ops/l5/t_l5stream.py`"* — and **not one of them is**: it reads 956 / 775
  / 181 intentions, 26 multi-satisfaction indices at fan-out 6, 164 `count_ge`
  conditions and 181 043 raw cells against the frozen instance's 945 / 765 / 180,
  34 indices at fan-out 3, 169 conditions and 182 555 raw cells. The cause is on
  the record: Stage A's first corpus draft was not guarded, its ops trial went red,
  and *"the CORPUS was changed, not the trial"* (`BOUNDARY.log` line 28) — the
  prose was re-derived and that block was not. Handled under this clause: a dated
  erratum note above it, no historical line rewritten, no corpus byte touched, and
  `generator.py`'s `DECLARED_*` constants named as the record.

The clause is deliberately **not** a licence to edit. It settles which number is
in force and requires the other to remain visible, which is the same discipline
`R3` applied to `F_strict` and `R4` clause 4 to `F_corruption`: *a reading that
supersedes another should have to show the one it replaced.*

### 4. The Layer-5 budget reading: `budget_cap = raw_cells // 4`

`§5 L5` cites `B = 1000` and declares **no pressure ratio of its own**, unlike
`§5 L3` (*"stream = 10× budget"*) and `§5 L4` (`footprint ≤ 250`); `§5.1 L5` says
only that *"Pending intentions live within the hard budget like any other
state."* A budget must nonetheless be named before an oracle ceiling means
anything, because R2 obligation 1 derives the ceiling from *"the corpus, the
budget law, and nothing else"*.

**Ruled:** the Layer-4 footprint ratio carries forward —
`budget_cap = raw_cells // 4 = 45 638` on `corpora/l5stream` — and the events the
engine **emits** compete for cells inside that cap without enlarging it, which is
what `§5.1 L5`'s *"like any other state"* means here.

This ratifies the strictest defensible reading, which Stage A chose deliberately
and for a reason that survives ratification: a layer above consolidation should
not be handed a looser budget than consolidation, and a witness that fits at 250‰
fits at every looser reading *a fortiori*. A looser ruling would move the recorded
margin (3 687 cells, 8.1%) and nothing else. It is ruled rather than left open
because three batteries now replay at that number rather than merely computing
against it.

**No footprint gate is created.** `§5 L5` states none, and this clause states
none; what is ruled is the cap the budget law binds at, certified the way `§3.3`
and `§4.1.2` certify every cap — after every write.

## The Stage-B evidence, carried verbatim

Every number in this section is measured by a trial that runs every suite, and
none of it is argued from anywhere else. Clause 1 rests on the first three
blocks; clause 2 on the fourth; clause 3 on the fifth.

**The `t` layout.** On `corpora/l5stream` the ruled semantics turn **20 000
caller writes into 20 765 logical times, the last firing at `t = 20 760`** —
asserted engine-free at Stage A
(`t_attainability.py::trial_one_caller_ingest_can_advance_next_t_by_more_than_one`,
which already required that the caller events and the firings **partition**
`0 .. next_t − 1` and that *"a firing is ingested where it fires"*) and asserted
of an engine by
`t_prospection.py::trial_the_engine_t_layout_is_the_one_the_written_texts_force`,
the half Stage A could not reach. `_l5score.assert_t_identity` closes it from the
other side: `next_t − |caller stream|` must equal the number of firings P1
reports, so an engine that fired twice and reported once fails, and so does one
that emitted an event nobody asked for.

**The ascension battery.** `trials/ascension/l5/t_prospection.py` applies the
ratified gate to an engine in **eight engine-gated skips** — the sanctioned
checkpoint shape, humility green and ascension skipped — with the four exactness
clauses written as `require_equal` **identities** per R5 clause 1 (an identity
clause has no margin, so there is no inequality here to widen later), `F ≥ 980`
as the one graded clause under the **literal §3.0 table** (R3 excludes Layer 5
and no extension is requested), `B = 1000` after **every** write with
`refused = 0`, and the footprint priced under rule P. Two trials are engine-free
and green today: the intention-free theorem over every corpus in the registry,
and the docs-are-checked trial that `STAGE-B.md §2`'s declared query vocabulary
is the one `_l5score` speaks.

**One restraint is recorded because it is where a Stage-B battery could have
silently tightened a ratified gate.** The first draft asserted `wrong = 0` beside
`F ≥ 980`; a mock engine firing everything correctly with **one** wrong payload
scores `F = 999`, clears the ratified gate, and would have been failed by an
assertion `§5 L5` does not make. Given the four identities the only possible
wrong answer *is* a payload differing at the right `t`, which is exactly what `F`
measures, and `F ≥ 980` admits **35** of them out of 1 710. `§5 L5` ratified 980
and not 1000 and R5 clause 1 records that slack as the constitution's own answer
to R2's perfection objection. It is computed and reported, never required.

**The humility side, measured in BOTH conditions.** `trials/humility/l5/` is
green today, `make_engine(layer_cap = 4)` being the frozen Layer-4 engine, and
the whole 20 000-event replay costs ~21 s (no prefix ladder declared or needed —
worth contrasting with `humility/l4`, where the capped engine was Layer 3's
`O(retained)` eviction path and the whole-stream run cost 663 s). The
`IMPOSSIBILITY.md` first draft was **refuted by its own mandatory measurement**
and the corrected form is sharper, so both conditions are on the record and
neither rescues the other:

| condition | intentions returned byte-exact by `read(t)` | `trigger-recall` |
|---|---|---|
| **in budget** (4× the raw episodic footprint — nothing forces a drop) | **945 of 945** | **0** |
| **at the ratified Layer-5 cap** (`raw_cells // 4`) | **30 of 945** | **0** |

In budget, GAPMAP §2's *"recorded but never binding"* thesis holds in its clean
form: every intention is retained perfectly and not one is ever read as a
condition. At the pressure the gate is stated at, the capped engine does not even
**record** the thing it would fail to read — an `intend` payload has no Layer-4
facet, its condition AST is expensive, and the inherited Layer-3 forgetting law
releases it. **`trigger-recall` is 0 either way**, which is why the ceiling does
not depend on which condition is quoted, and why quoting only the flattering one
would have been the omission R5 clause 4 was written about. The sharpest form
needs no score at all: a firing consumes a `t`, so an engine that fired anything
ends past the caller stream, and this one ends at exactly 20 000. `humility/l4`'s
information-theoretic pigeonhole is **not** borrowed and the document says so:
in budget the capped engine holds every intention byte-exact and still scores 0,
so the failure is an absence of **machinery**, not of information.

**The inheritance side.** `trials/inheritance/l5/` extends the standing class at
cap 5 on in-budget substrates — the Layer-1 verbs, the Layer-2 cue battery at
`§5 L2`'s own gate, the Layer-3 retention battery on both frozen pressure streams
as identities, and, new at this layer, the **Layer-4 consolidation battery** on
`corpora/l4stream` as identities (`C = 1000`, reconstruction `F = 1000`,
`wrong = 0`, `fabricated = 0`), verified attainable before being frozen by
measuring `adapters/l4` at an in-budget cap. The Layer-4 row is the one
prospection could actually break: a pending set, an evaluator on the write path
and the engine's own emitted events all compete for the same cells as the
interval table, and the cheapest way to buy room for them is a lossier derived
view — which `§5 L5`'s four firing clauses would never notice.

**The 270 / 271 seam and the `grammar.md` block.** Both instances clause 3 rests
on are stated in that clause with their numbers; the third artifact is
`humility/l5/t_prospection.py`'s engine-measured **271**, and the second, larger
instance is `corpora/l5stream/grammar.md`'s closing block, whose declared numbers
never matched the frozen bytes and which is handled by a dated erratum note above
it rather than by an edit.

## Rationale

**The repair belongs at the binding, not at the number** — R1's rule and R4's,
applied a third time. No `§5 L5` threshold moves in either direction. What is
decided is what the ratified numbers attach to, which is the one thing this
document's own preamble says a ruling is for.

**No engine's inability motivated this.** `core/layers/l5_prospection.py` does not
exist and `trials/adapters/l5.py` does not exist. Stage A stopped at the
attainability boundary, `R5` was decided against arithmetic, and Stage B has
written every battery — ascension, humility, inheritance — before any engine, so
that the corpus binding and the `t` semantics are fixed before anything can be
tuned to them. As in R1, R4 and R5: had an engine existed, this ruling should have
been harder to obtain.

**Clause 2 is the one clause here that could not have been written earlier, and
R5 said so.** Settling logical time in a ruling written before the trials existed
would have been exactly the ordering R2 forbids — the semantics would have been a
guess that the trials were then built to satisfy. Written in this order, the
decision is derived from six ratified sentences, checked against every frozen
trial that could contradict it, and *already asserted* by a Stage-A trial that
was written before anyone proposed a clause: `t_attainability.py::trial_one_caller_ingest_can_advance_next_t_by_more_than_one`
requires that the caller events and the firings **partition** `0 .. next_t − 1`
and that *"a firing is ingested where it fires"*. The ruling states what the
suite was already enforcing, which is the weakest possible way for a clause of
this reach to be introduced, and deliberately so.

**Clause 2 also refuses the two easy generalizations.** Cascades and
budget-refused firings are adjacent, tempting, and under-determined by the
ratified text — and one of them is unobservable on the binding corpus by
construction. Deciding an unobservable question would set a precedent no
measurement could ever have corrected. `grammar.md`'s own `No cancellation`
section made the same refusal at Stage A (*"R2's Stage-A discipline is to compute
against the ratified gate rather than to enrich it"*), and this is that discipline
at Stage B.

## What this ruling does not do

- It does **not** amend `BOUNDARY.md`. No ratified sentence is edited or reread.
  Clause 2 reads `§7.1`; it does not rewrite it, and the sentence it reads keeps
  its literal force for the caller's payload.
- It does **not** change any threshold, in either direction, on any layer. In
  particular it does not lower `trigger-precision`, `trigger-recall`, `dup-fire`,
  `miss`, `F` or the `≤ 50` ceiling.
- It does **not** weaken `R2`. Obligations 3 and 4 are untouched — the arithmetic
  is computed, recorded and machine-checked before the gate binds — and `R5`'s
  four clauses continue to govern *how* obligations 1 and 2 are discharged here.
- It does **not** create a Layer-5 footprint gate, extend `R3` to Layer 5, or
  request the corruption reading of `F`. The oracle reaches 1000, so the layer
  does not need the friendlier reading and declines to ask for it — R4 clause 4's
  discipline, third instance.
- It does **not** settle cascades, or what an engine owes when the budget cannot
  house a firing (clause 2's two express non-decisions).
- It does **not** authorize a `cancel`, `revoke`, `expire` or `re-arm`
  construct. `§5 L5` names none and the corpus invents none.
- It does **not** licence editing a frozen or historical document. Clause 3
  settles which number is enforced and requires the other to stay visible.
- It does **not** claim Layer 5, grant a Layer-5 capability, or license an engine.
  Stage C — `core/layers/l5_prospection.py`, `trials/adapters/l5.py`,
  `core/layers/README-l5.md`, the strain class, the anchor — is unwritten, and
  R2's standing step still orders it.

## Enforcement

- `trials/ascension/l5/ATTAINABILITY.md` and `t_attainability.py` — the Stage-A
  arithmetic clause 1 rests on: the exhibited witness, the four named baselines,
  the conjunction bound asserted at three, and the `t` layout asserted
  engine-free.
- `trials/ascension/l5/STAGE-B.md` — clause 2's derivation, its contradiction
  check (§1.5), and clause 3's second instance; it now carries a dated
  ratification note above its Stage-B text, which is unedited.
- `trials/ascension/l5/RULING-R6-DRAFT.md` — the draft a human ratified, retained
  unedited beneath a dated note naming **this entry** the binding text.
- `trials/ascension/l5/t_prospection.py` — the gate applied to an engine
  (engine-gated), the `t` layout asserted of an engine, and the intention-free
  theorem over every corpus in the registry (engine-free).
- `trials/humility/l5/t_prospection.py` and `IMPOSSIBILITY.md` — the ceiling
  measured on `make_engine(4)` through the generic interface in both conditions,
  and the structural argument for it.
- `trials/inheritance/l5/t_inheritance.py` — Layers 1–4 re-asked at cap 5, so the
  new capability cannot be bought with an old one.
- `trials/ops/l5/t_l5stream.py` — the corpus properties clause 1 rests on,
  including the GUARDEDNESS induction clause 2's first non-decision turns on.
- `trials/laws/t_rulings.py` — the gate registry, where the Layer-5 constants now
  carry this entry beside their `§5 L5` clauses, and the completeness check that
  forbids an unregistered gate constant anywhere under `trials/`.

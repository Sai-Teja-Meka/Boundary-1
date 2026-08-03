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

---

# R7 — The Layer 6 gate binds on `corpora/l6batteryb`; AUROC's domain; the demotion of `corpora/l6battery`

**Status:** FROZEN on commit.
**Binds:** the Layer-6 ascension trials (`trials/ascension/l6/`) and the Layer-6
humility trial (`trials/humility/l6/`) when it exists; clause 2 binds every
`ATTAINABILITY.md` and every Layer-6-or-later battery, clause 3 binds **every
gate that cites `AUROC`** at any layer, including `BOUNDARY-HIGH.md` when it is
written, and clauses 4 and 5 bind the reading of `§3.4`'s quantities wherever
they are scored.
**Authority:** `BOUNDARY.md §3.0`, `§3.4`, `§3.5`, `§4.1`, `§5 L6`, `§5.1 L6`,
`§8.3`, `§8.7`, `§8.8`; `BOUNDARY-RULINGS.md R1` clause 5 and `R4` clause 1 (the
precedent for keeping a corpus as an ungated diagnostic rather than retiring
it), `R2` (whose four obligations this rests on and does not weaken), `R3`
(whose scope this deliberately does **not** extend), `R4` clauses 2, 3 and 5,
`R5` clauses 1–4 (which carry the identity, the direction-aware conjunction
reading, the declared policy class and the pricing discipline here without an
entry of their own), `R6` clauses 1 and 3. Resolves the four questions put in
`trials/ascension/l6/ATTAINABILITY.md §8` and re-put, after the human's ruling
on them, in `trials/ascension/l6/ATTAINABILITY-B.md §7`. Ratifies the round-2
draft of `trials/ascension/l6/RULING-R7-DRAFT.md`, written at Stage A round 2
from the arithmetic in `ATTAINABILITY-B.md` and machine-checked by
`t_attainability_b.py`.
**Holding:** the ratified `§5 L6` thresholds stand **unchanged**; both sides of
the Layer-6 gate — ascension **and** humility — bind on **`corpora/l6batteryb`**,
and **`corpora/l6battery` is DEMOTED to an ungated diagnostic**, the fourth
substrate kill, its bytes untouched and its trials still running; abstentions
are **outside** the calibration denominator, and every battery states its `A`,
its `n_pos` and its `n_neg` beside the triple; **`AUROC = n/a` DISQUALIFIES**,
and a gate citing `AUROC` binds only on an artifact where both classes non-empty
is a **theorem** carried by a forcing region priced inside a recorded window;
`§5 L6`'s `40 / 30 / 900` are read **exact**, not permille; and `§3.4`'s ECE bin
index is `bin(conf) = 9 if conf == 1000 else conf // 100`.

## The question, restated after the ruling on round 1

Round 1 put four questions to a human and the human answered them. The answers
are the charter of round 2 and they are recorded here as the premises of this
draft rather than re-argued as its conclusions:

**(i) `AUROC = n/a` DISQUALIFIES.** Vacuous satisfaction of a calibration clause
is the **null-exemption defect this project's own autopsies convicted**:
`autopsy/writ/ANATOMY.md` records that declaring a capability false sets the
score `null` and null is dropped from **both** numerator and denominator
(`evaluator.ts:545-548`, `docs/metrics.md:204`), so a system exempts itself
exactly where `make_engine(layer_cap = N−1)` is scored against a ceiling. A gate
that let `n/a` excuse its own clause would commit, in this project's own trials,
the defect this project published about somebody else's.

**(ii) The binding artifact must make `n_neg > 0` a THEOREM**, not a fact
relative to a declared reading — via an irreducible-ambiguity forcing region
whose resolving signal the generator **withholds**.

**(iii) `corpora/l6battery` is DEMOTED** to an ungated diagnostic, with its cause
recorded verbatim in the `R4`-clause-1 form.

**(iv) A commitment clause was considered and held in RESERVE**, and is recorded
below as the declined alternative with its reason.

Round 2 built the artifact, redid the band arithmetic, re-exhibited the witness
and re-scored every baseline. What follows is what that produced.

## The ruling

### Clause 1 — the binding, and the fourth substrate kill

The ratified `§5 L6` thresholds stand **UNCHANGED** — `Brier ≤ 40`, `ECE ≤ 30`,
`AUROC ≥ 900`, `F ≥ 950`, `B = 1000`, capped `AUROC ≤ 600` — and **both sides of
the Layer-6 gate, ascension and humility, bind on `corpora/l6batteryb`**, in one
clause, for `R6` clause 1's reason: a ceiling measured on one artifact beside a
gate cleared on another is two facts about two worlds.

The **upper side is EXHIBITED** (`R4` clause 5, `R5` clause 1 for the `B = 1000`
identity): a concrete confidence assignment over the frozen artifact — structural
evidence in, integer permille out, no engine and no answer key — attains
`Brier 23 / ECE 0 / AUROC 976 / F 955 / B 1000` against the gate, and it is
**provably non-resolving**, pricing the forcing region at the tie's own
confidence of 500 because the region's own theorem forbids it from doing better.

The **lower side holds over the CONJUNCTION** (`R5` clause 2), and four of the
five clauses do work clause-wise:

| capability-free policy | Brier | ECE | AUROC | F | clears |
|---|---|---|---|---|---|
| confident-always (= `make_engine(5)`, measured) | **45** | **45** | **500** | 955 | no |
| base-rate constant | **43** | 0 | **500** | 955 | no |
| detect-and-abstain | 0 | 0 | n/a | **918** | **no — killed by `F`** |
| abstain-on-conflict | 0 | 0 | n/a | **766** | no — killed by `F` |

`Brier` fails both constants, `AUROC` fails both by 400 permille and by
arithmetic rather than margin, and — the round-2 change — **`F` fails both
abstainers outright**, so no clause of `R2` obligation 2 rests on what `n/a`
means on this artifact.

**THE FOURTH SUBSTRATE KILL. `corpora/l6battery` is DEMOTED to an ungated
diagnostic** — after `corpora/l3stream` (`R1` clause 1), the chronicle family at
Layer 4 (`R4` clause 1), and now this. Its bytes are untouched, its generator is
untouched, `trials/ops/l6/t_l6battery.py` and
`trials/ascension/l6/t_attainability.py` are untouched and keep running green: a
corpus is retired only by ceasing to gate on it, never by changing its bytes, and
nothing here is deleted. Its cause is recorded **verbatim**, from the round-1
document's own §6, and it is independently sufficient:

> `n_neg > 0` **for the declared reading**, measured at 158 on the engine this
> project has frozen — and **not** against an arbitrary reader.

with the mechanism measured rather than argued in the same section: `§8.7` pairs
every injected murk defect with its answer key **and injects it by visible
construction**, so a stream-only rule recovers each family **exactly** —
symmetric difference **0** against the frozen key on contradiction (305),
near-duplicate (393), ambiguity (205) and malformed (257). **On murk, evidence
that ranks also resolves.** A gate citing `AUROC` bound there would be a gate
whose evaluability depended on the engine under test not having thought of
first-wins, and clause 3(b) below is what forbids that in general.

What `corpora/l6battery` remains is not nothing, and the demotion says so: it is
the artifact that first gave `§3.4` a denominator at all, its capped measurement
of 500 against the 600 ceiling was the first defined `AUROC` in this project's
history, and its arithmetic is the diagnostic against which battery-b's is read.
`corpora/murk` likewise stays exactly what `R4` clause 1 left it — an ungated
Layer-4 diagnostic and this project's dirt corpus — and battery-b takes nothing
away from it.

**No alternative substrate was passed over in silence.** `§8.8`'s REAL corpus is
25 events, three orders of magnitude too small to fill ten ECE bins; no other
frozen corpus carries an answer key at all, so on them the correctness of an
answer is whatever the engine's own reading says it is and `n_neg` is 0 by
construction rather than by capability.

### Clause 2 — the calibration denominator, stated

**Abstentions are outside the calibration denominator, and the exclusion is
stated rather than inferred.** `§3.4`'s `A` is the count of **answered** queries;
an abstention contributes to `§3.0`'s fidelity and to no calibration quantity.
Every `ATTAINABILITY.md` and every Layer-6-or-later battery states its `A`, its
`n_pos` and its `n_neg` explicitly beside the triple, and a battery declares for
each query class whether it scores inside the denominator and why.

This clause adds no arithmetic — `§3.4` already implies all of it. What it adds
is that the implication may no longer be left implicit, because the whole of
clause 3's problem is invisible until `A` is written down next to `N`. It is
carried across from round 1's draft unchanged, and round 2 honoured it before it
was ratified.

### Clause 3 — AUROC's domain

**(a) `AUROC = n/a` DISQUALIFIES; it does not excuse the clause.** A policy or an
engine whose `AUROC` is undefined has not cleared a gate that cites `AUROC`, and
`§3.4`'s own sentence — *"any gate that cites AUROC requires both classes
present"* — is ruled to mean exactly that.

**The framing is instrument range, and it is the reason rather than a
decoration.** A gate is an instrument. An instrument has a range, and outside it
the honest output is not a pass but a refusal to certify: a balance that reads
`----` under an out-of-range load has not weighed the object, and nobody records
the `----` as a weight. `§3.4` says `AUROC` is *undefined* when a class is empty
and instructs the harness to report `n/a`; a gate that treated that report as
satisfaction would be certifying a quantity it had just declared itself unable to
measure. **The instrument declines to certify what it cannot measure.**

The alternative reading is not merely worse in principle; it was **measured**.
Round 1's `detect-and-abstain` — a policy with no confidence model whatsoever,
flat 1000 on everything it answers, which hedged exactly the queries the
structural evidence flagged and thereby deleted them from `§3.4`'s denominator —
scored `Brier 0 / ECE 0 / F 960 / B 1000`, *better than the exhibited witness on
three clauses*, and would have cleared every evaluable clause of `§5 L6` with no
capability at all. And this is the **null-exemption defect this project's own
autopsy convicted WRIT of** (`autopsy/writ/ANATOMY.md`, commit `3c0900a`):
declaring a capability false sets the score `null`, and null is dropped from
**both** numerator and denominator, so a system exempts itself precisely where
this project scores a capped engine against a ceiling. A project that published
that finding cannot write the same exemption into its own gate.

**(b) A gate citing `AUROC` binds only on an artifact where both classes
non-empty is a THEOREM, and the artifact must carry the proof.** This is the
Layer-6 analogue of `§5 L3`'s corpus precondition — *"importance uniformly-to-late
(never front-loaded)"*, the one ratified gate cell in the whole table that names a
property its corpus must have — and it is stated here because `§5 L6` does not
state one and needs it more.

**The guarantee may NOT be relative to a declared reading**, and this is where
this draft departs from round 1's, on the human's ruling. Round 1's clause 3(c)
proposed that the guarantee *may* be relative to a declared reading provided the
artifact declares it. That is now refused, for the reason round 1's own §6 made
plain: a guarantee relative to a reading is a guarantee that the engine under
test has not thought of a different reading, and a gate whose evaluability
depends on the engine's ignorance is not a gate. What is required instead is a
**forcing region**: a region of the artifact on which

> **every** committing policy definable from the artifact's own substrate — not
> merely the one the session declared — is wrong on a stated number of queries,

proved from the frozen bytes and machine-checked. `corpora/l6batteryb` supplies
one, and the proof has two halves, both asserted in
`trials/ops/l6/t_l6batteryb.py`:

* **the tie.** The region is 100 **mirror pairs**. The two members of a pair have
  equal event histories once the entity id is blanked, and logical times
  differing by exactly `+1` at every position; one member's truth is its FIRST
  assertion and the other's is its LAST. So any reader that does not read the raw
  id or an absolute `t` answers both identically and is wrong on exactly one —
  **exactly 100 errors, for every such reader.** Exhibited against a bench of six
  readers built to break it, `first-wins` included, all measuring 100;
* **the withholding.** Regenerating with every coin bit flipped produces a
  **byte-identical stream** and an answer key that differs on all 200 forcing
  queries and on nothing else. So the stream carries **zero** bits about the
  coin, every class-E policy's answers, confidences and scores are unmoved by the
  flip while its error set is exactly complemented, and a policy that resolves
  the region has read the answer key — class **O** by definition. The two handles
  the tie leaves, the raw id and the absolute `t`, are closed by the coin's
  **balance**: a rule keyed on either takes both members of a pair or neither and
  is right on exactly half the pairs, which is 100 errors again.

**(c) The forcing region's price is a ratified-clause arithmetic and must be
recorded as a window, not as a number.** A forcing region of size `r` inside an
answerable core of size `A` is admissible only where three ratified clauses hold
at once, and `ATTAINABILITY-B.md §2.2` records the window exactly:

```
A >= 10r                          the honest committer clears F >= 950
A <  18r                          blanket abstention on the region BREAKS F >= 950
A <  (25 + 5*sqrt(21))/4 * r      Brier <= 40 still beats the base-rate constant
```

`corpora/l6batteryb` sits at `A = 11r = 2200`, `r = 200`, `w = 1/22`. The
irrational bound is checked as the exact rational predicate `25u² − 50u + 4 < 0`
in `u = r/A` and never as a float (§2.2). Where no `r` satisfies every ratified
clause simultaneously, that is an ATTEMPT-shaped constitutional finding and the
session stops rather than bending a constant; it did not arise here, which is
also why clause 8's reserve instrument was not needed.

**(d) The consequence is stated rather than hidden — and on this artifact it
costs nothing.** Round 1's draft accepted, with reasons, the second horn of the
same reading: *"a gate citing `AUROC` cannot be cleared by an engine that answers
everything correctly."* It called the consequence unattractive and took it
anyway. On `corpora/l6batteryb` **that engine cannot exist**: answering
everything correctly requires resolving the forcing region, and (b)'s second half
says the resolving signal is not in the stream. The disqualifying reading locks
out nothing reachable here. It remains the right general rule, and clause 3(b) is
what keeps it from ever being expensive again: an artifact that carries a forcing
region cannot be outgrown by a correct engine, because being correct on it is not
a thing an engine can be.

The residue is stated rather than smoothed over. A **binding artifact is
outgrown** when an engine's own answers move `n_neg` on the region, which by the
tie is impossible, and when they move it elsewhere, which is ordinary and is what
the rest of the battery measures. And a policy that has **memorised** the answer
key resolves the region trivially; that policy is class **O**, and the coin is
what makes the class definition bite — it exists in the key and in the generator,
and in no function of the stream. **The generator is part of the answer key, not
part of the substrate**, and this draft says so in as many words so a later
session does not have to rediscover it.

### Clause 4 — the reading: EXACT, not permille

`§5 L6`'s `40`, `30` and `900` are bounds on the quantity `§3.4` defines in
`[0,1]`, not on its `§3.5` permille rounding:

```
Brier ≤ 40/1000        ECE ≤ 30/1000        AUROC ≥ 900/1000
```

The two readings differ on `(40/1000, 81/2000]`, `(30/1000, 61/2000]` and
`[1799/2000, 900/1000)` — the endpoints exact, because `§3.5` rounds a half to
the **even** neighbour and 40 is even. `§5.1 L6`'s own defense sentences favour
the exact reading in its own words: *"at or under 0.04"* and *"to within 3%"* are
bounds on the quantity. `F ≥ 950` is read the same way, and round 2 is where that
stops being an afterthought.

Round 1 asked for this reading while recording that **nothing turned on it**.
Round 2 found the first place a reading moves a **number**, and it is an `F`
instance: a policy hedging 13 of battery-b's mirror pairs scores
`F = 1306/1375 = 0.94981…`, which is `950` in permille — **affordable under one
reading and not under the other**. It still moves no verdict, and the theorem
that matters survives both (`n_neg ≥ 88` exact, `≥ 87` permille, `> 0` either
way), which is precisely the moment to settle it: cheap now, and expensive the
first time a verdict rather than a ladder row lands in the interval.

### Clause 5 — the bin reading

`§3.4`'s ten ECE bins are `[0,100)`, `[100,200)`, …, `[900,1000]` with the last
bin **closed**. On an integer permille confidence the bin index is ruled to be
exactly

```
bin(conf) = 9 if conf == 1000 else conf // 100
```

— a total order and a partition at once: no boundary is ambiguous, no value falls
outside, and empty bins contribute 0 as `§3.4` already says. This is the reading
every Layer-6 instrument in the tree already implements (`_l6tasks.ece`, used
unchanged by both rounds), ruled rather than left as an implementation detail
because it is the one place a `§3.4` quantity could be computed two defensible
ways from the same numbers, and because the exhibited witness's `ECE = 0` depends
on it: its 500s land in bin 5 and its 1000s in bin 9, and a reading that put 1000
in an eleventh bin or split the closed interval would move the witness's headline
figure without moving anything it measures.

### Clause 6 — the key-blind scope statement

Round 1's sharpest positive result is **preserved, re-measured, and re-scoped**,
because it is the kind of finding that travels further than its evidence if
nobody restates it.

Round 1 recorded that *a policy that RANKS without RESOLVING clears the gate*,
measuring the key-blind `conflict-rank` at `Brier 31 / ECE 0 / AUROC 945 /
F 955`. On `corpora/l6batteryb` the same policy measures
`Brier 36 / ECE 0 / AUROC 911 / F 955` and still clears. The scope statement is
ruled to read, henceforth:

> On an artifact carrying a forcing region, **ranking without resolving is not
> merely sufficient for the Layer-6 gate; it is the only thing available**, since
> the region is by construction unresolvable and the exhibited witness is itself
> non-resolving. And **key-blindness costs a measurable margin**: a policy that
> cannot tell a set-once tie from an ordinary chain that was legally updated
> clears `AUROC ≥ 900` on 11 permille where the set-once-aware witness clears it
> on 76.

Two caveats travel with it and are ruled to travel with it. `conflict-rank`'s
levels are the artifact's own measured accuracy per conflict count, so its scores
are a **ceiling for the key-blind sub-family** and not an attainable policy —
round 1's caveat, carried forward unweakened. And the fit is **coin-invariant**
on battery-b, because the tie pins the region's accuracy at exactly one half
under either coin, which is asserted rather than assumed.

### Clause 7 — the §3.0 price-list tension, RECORDED for Layer 7's eyes

**This clause rules nothing. It records a tension so that the layer that will
have to live with it inherits the item rather than rediscovering it.**

`§3.0` prices an abstention on an answerable query at 100 and a confident error
at 0, and `§3.4` computes calibration over answered queries only. The two point
the same query in opposite directions: `§3.0` pays an engine to convert an error
into an abstention, and `§3.4` needs those errors to survive as answers or its
whole triple evaporates. Round 1 measured a capability-free policy that followed
the incentive to its end and beat the exhibited witness on three clauses. Round 2
closes it **on this artifact and by arithmetic** — hedging the forcing region
costs 90 permille out of `F ≥ 950`'s 50-permille budget, so every policy that
clears `F` leaves `n_neg ≥ 87` — and that closure is a property of a *sizing*,
not of a law. A future artifact whose forcing region is a smaller share of its
core would reopen it exactly.

**Layer 7 is where it bites next and it will bite harder**, which is why this is
recorded now and in this document. `§5 L7` gates `novelty = 1000`,
`tagging = 1000`, `validity = 1000` and `ECE ≤ 40` together, and `§4.2` becomes
**binding** there: an answer without a valid provenance tag scores as **wrong
(0)**, *"regardless of whether its value is correct"*. So at Layer 7 the price
list acquires a third way to reach 0 that has nothing to do with being wrong, and
an engine facing an untaggable answer is offered the same escape `§3.0` offers
here — abstain, keep 100, and leave the calibration denominator behind. Two
existing findings meet exactly there and are named so the Layer-7 session finds
them together: the `[L5] [PULSE]` question of whether a support entry must be
**recoverable** or merely **ingested** (`BOUNDARY.log` line 34 — Layer 5 already
produces, lawfully, a correct scored answer whose natural support names an
unrecoverable `t`), and this clause's tension, which will decide whether the
honest response to that gap is an abstention `§3.4` cannot see or a tagged answer
`§4.2` scores as wrong.

Nothing above is a holding. It is a bequest.

### Clause 8 — the DECLINED ALTERNATIVE: the commitment clause, held in reserve

A **commitment clause** was drafted and is **declined**, and it is recorded here
with its reason so that a later session finds an examined instrument rather than
an idea nobody had.

**What it would have said.** *On a query class an artifact declares as a
commitment class — one where the engine's own state holds the material to answer
and the artifact's key names an answer — an abstention is scored **0** rather
than `§3.0`'s 100, so that hedging a declared tie earns exactly what a confident
error earns and the `§3.4` denominator cannot be emptied by declining to use it.*

**Why it was drafted.** It closes the `§3.0`/`§3.4` collision *directly* and at
the level of law, rather than through a sizing that a future artifact could get
wrong. It is the smallest instrument that makes clause 3(a) unnecessary: with it,
`n/a` could not be reached by any policy at all, on any artifact.

**Why it is declined.** Four reasons, in descending order of how much they bind.

1. **It rewrites `§3.0`'s price list, and `§3.0` is frozen.** The table is the
   constitution's own five-row statement of what knowing-that-you-do-not-know is
   worth, and `BOUNDARY.md` has no amendment mechanism. A ruling may settle which
   corpus a stated gate binds on and which reading of a ratified sentence the
   trials implement — that is what `R1`, `R4` clause 2, `R5` and `R6` did — but a
   ruling that changed 100 to 0 for a declared class would be an amendment
   wearing a supplement's clothes. `§9` says the procedure for a rule that seems
   wrong is to log the objection and stop, and it is not clear this rule is even
   wrong.
2. **It is not needed on the artifact it would bind.** `ATTAINABILITY-B.md §5`
   measures the closure the ratified constants already produce: the hedger dies
   at `F 918`, and no policy clearing `F` reaches `n_neg = 0`. `R5`'s own
   discipline — draft new law only for what the existing rulings cannot carry —
   forbids adding a clause to do work `§5 L6`'s own `F` clause is already doing.
3. **It would make a good property of an artifact into a duty of every engine.**
   Under it, an engine that abstained on a declared commitment class would be
   punished for a behaviour `§3.0` elsewhere rewards, and the line between the
   two would be drawn by whoever declared the class. Clause 3(b)'s forcing region
   puts the burden on the **artifact**, where `R2` obligation 4 already puts the
   corpus binding, and leaves the engine's incentives exactly as ratified.
4. **It is the wrong instrument for the failure it fears.** What it protects
   against is an artifact whose forcing region is too small a share of its core
   for `F` to price hedging out. The window in clause 3(c) is where that is
   caught, before a gate binds, by arithmetic — and an artifact that cannot be
   sized into the window is an ATTEMPT-shaped finding for a human, not a case for
   changing what an abstention is worth.

**When it should get its hearing.** If a future Layer-6-or-later artifact cannot
be sized into clause 3(c)'s window while satisfying every ratified clause — the
ATTEMPT-shaped case, which round 2 checked for and did not find — or if Layer 7's
`§4.2` binding makes abstention the dominant strategy on a class the gate needs
answered (clause 7), then this reserve instrument is the one that was already
examined, and this is the record of what it says and of the four objections it
must answer first.

### Clause 9 — nothing else is added

`R5` clause 2 is forward-binding in its own text *"because Layer 6 needs it
immediately"*, and it carries the whole of `R2` obligation 2 here: the minimizing
clauses are read direction-aware, the lower obligation is read over the
conjunction, and the round-2 arithmetic discharges it without a new clause. `R5`
clause 1 carries `B = 1000` as an identity, as it has since Layer 1. `R5`
clause 3's policy-class declaration and clause 4's pricing discipline are both
satisfied by `ATTAINABILITY-B.md §3` and are not restated. `R4` clause 5's
exhibit-don't-argue obligation is satisfied by the witness and, unusually, twice
over: the forcing region's tie is exhibited against a reader bench as well as
proved.

**So this draft proposes no ruling on `Brier` beyond the readings in clauses 4
and 5**, and says so explicitly, because the session was instructed to draft new
law only for what `R5` cannot already carry.

## The round-2 evidence, carried verbatim

Every number in this section is computed by `trials/_l6btasks.py` from the frozen
artifact alone and asserted by `trials/ascension/l6/t_attainability_b.py` or
`trials/ops/l6/t_l6batteryb.py`, both of which run every suite; none of it is
argued from anywhere else. Clause 1 rests on the first four blocks and the last
two, clause 3 on the first three and the fifth, clause 4 on the fifth, clauses 5
and 6 on the sixth.

**THEOREM 1 — THE TIE, the first half of clause 3(b)'s proof.** The forcing
region is `PAIRS = 100` **mirror pairs**, `r = 200` forcing queries, class **K0,
the whole region, unsampled** — a battery that sampled its forcing class could be
tuned by choosing which ties to ask about. Each pair is two entities spawned at
adjacent logical times with the same class, each carrying exactly **two** `origin`
assertions with the **same ordered value pair**, and **nothing else in the stream
ever touches either of them** (region ids are allocated outside the base world,
so no link, move or retire can reach them). Each member's entire event history is
therefore `[spawn, attr origin x, attr origin y]`; blank the entity id and the two
members' histories are **equal as sequences**, their logical times differing by
exactly `+1` at every position. A **withheld, balanced coin** — exactly 50 pairs
each way, shuffled from the same PRNG *after* the stream is complete — makes one
member's **FIRST** assertion true and the other's **LAST**. So any reader that
does not read the raw entity id or an absolute `t` receives identical input for
the two members, returns the same value, and is wrong on **exactly one** of them:
**exactly 100 errors, under either coin, for every such reader.** Exhibited
rather than argued, against a bench of **six readers built to break it** —
`latest-wins`, `first-wins`, `canonical-min`, `canonical-max` and two id-keyed
rules — **every one measuring exactly 100**. `first-wins` is the specific reader
that made round 1's guarantee relative: on `corpora/l6battery` it would have
answered the whole commitment class correctly.

**THEOREM 2 — THE WITHHOLDING, the second half.** The generator builds the region
layout and the whole 12 000-event stream **before the coin is drawn**, and the
stream path never reads it; regenerating with every coin bit flipped produces a
**byte-identical stream** and an answer key that differs on **all 200** forcing
queries and on nothing else. So the stream carries **zero** bits about the coin;
every class-E policy's answers, confidences and every one of its scores are
**identical** under the flip while the set of its region errors is exactly
complemented — `n_neg` does not move, the 100 errors are a different 100 — and a
policy that resolves the region has obtained the coin from the answer key, which
is class **O** by definition. The two handles Theorem 1 leaves, the raw entity id
and the absolute `t`, are closed by the coin's **balance**: a rule keyed on either
takes both members of a pair or neither and is right on exactly half the pairs,
which is 100 errors again — measured on the bench's two id-keyed readers. The
declared evidence vocabulary excludes both handles for that reason, so every
feature is **equal** on the two members of a pair and a class-E policy provably
cannot split a tie. **`n_neg = 100` is therefore a theorem for every committing
policy definable from the frozen stream, and not a fact relative to a declared
reading** — which is the whole of what round 2 was built to produce.

**THE COMPOSITION, AND THE FEASIBLE WINDOW.** `corpora/l6batteryb`, seed 9009:
12 000 events and 2 400 queries in **one** canonical JSON object carrying the
substrate, the answer key and the query set together, because the guarantee is a
**joint** property of the three and three separately byte-matched files could be
paired across generations while every individual check stayed green. K0 200
forcing / K2 1 400 current-value / K3 600 as-of = **`A` 2 200**, the answerable
core and `§3.4`'s denominator; K4 200 absence probes, unanswerable and
deliberately **outside** the denominator because an abstention carries no
confidence to calibrate; `N` 2 400. `n_pos = 2 100`, `n_neg = 100`,
`w = 1/22 = 45.45` permille. The base stream is **clean** — no near-duplicate, no
ambiguity, no malformed knob — so all of the error mass is the forcing region by
construction. Theorem 1 pins `w = (r/2)/A` for **any** committing reader, so the
window below is a property of the **artifact** and not of a policy:

| requirement | arithmetic | window |
|---|---|---|
| the honest committer clears `F ≥ 950` | `1000w ≤ 50` | `A ≥ 10r` |
| blanket abstention on the region **breaks** `F ≥ 950` | `900(r/A) > 50` | `A < 18r` |
| `Brier ≤ 40` still beats the base-rate constant (`Brier = w(1−w)`) | `25u² − 50u + 4 < 0`, `u = r/A` | `A < (25 + 5√21)/4 · r ≈ 11.978r` |

**The feasible window is `A/r ∈ [10, (25 + 5√21)/4)`**, i.e. `[10, 11.9782…)`;
under the three literal requirements alone it is `[10, 18)` and the third row is
what tightens it. `corpora/l6batteryb` sits at **`A = 11r = 2 200`**, with `1r` of
margin below and `0.978r` above. The irrational bound is never evaluated as a
float (`§2.2`): it is checked as the exact rational predicate above, and the
trial additionally requires `A = 10r − 1` to fail the lower bound and `A = 12r`
the upper, so a resized artifact is checked against the arithmetic rather than
against this instance's numbers. **No `r` was refused** and no ATTEMPT-shaped
finding arose: all three bounds scale with `r`, so every `r` admits a feasible
`A`, and `r = 200` was chosen so that `A = 11r` is a clean `1 : 7 : 3 : 1`
composition and one pair is one permille of `A`.

**THE WITNESS, AND EVERY NAMED BASELINE.** The exhibited witness `W` is a pure map
from the declared evidence to an integer permille — structural evidence in, no
engine, no answer key — and attains

```
Brier 1/44 → 23    ECE 0 exactly    AUROC 41/42 → 976    F 21/22 → 955    B 1000
```

against a ratified gate of `≤ 40 / ≤ 30 / ≥ 900 / ≥ 950 / = 1000`. It is
**provably non-resolving**: it prices the forcing region at the tie's own
confidence of **500**, which is **derived** — `permille(1/2)`, with the region's
measured accuracy asserted to be exactly one half — and not chosen, any other
value scoring worse on Brier. Class **O**, which may read the answer key, attains
`Brier 0 / ECE 0 / AUROC 1000`, so the distance between the two declared classes
(`R5` clause 3) is now the tie itself and is exactly `1/42` on AUROC — on round
1's battery class E *met* class O there, because murk's evidence resolved as well
as it ranked. The named capability-free policies, scored on every clause and read
over the **conjunction** (`R5` clause 2):

| policy | class | Brier ≤40 | ECE ≤30 | AUROC ≥900 | F ≥950 | B =1000 | clears |
|---|---|---|---|---|---|---|---|
| oracle | O | 0 | 0 | 1000 | 955 | 1000 | yes — not capability-free |
| **witness `W`** | E | **23** | **0** | **976** | **955** | **1000** | **yes** |
| conflict-rank | E | 36 | 0 | 911 | 955 | 1000 | **yes** |
| confident-always (= `make_engine(5)`, measured) | E, capability-free | **45** | **45** | **500** | 955 | 1000 | no |
| base-rate constant | E, capability-free | **43** | 0 | **500** | 955 | 1000 | no |
| detect-and-abstain | E, capability-free | 0 | 0 | **n/a** | **918** | 1000 | no |
| abstain-on-conflict | E, capability-free | 0 | 0 | **n/a** | **766** | 1000 | no |

**THE KILL, MEASURED, AND ITS GENERALIZATION.** `detect-and-abstain` is round 1's
`abstain-on-set-once` under its true name: the policy with **no confidence model
whatsoever** that follows `§3.0`'s incentive to its end, hedging exactly what the
structural evidence flags and thereby deleting its own errors from `§3.4`'s
denominator. On round 1's battery it scored `Brier 0 / ECE 0 / F 960 / B 1000`
with `AUROC n/a` — *better than the exhibited witness on three clauses* — and
cleared every evaluable clause of `§5 L6` with no capability at all. On
`corpora/l6batteryb` it measures **`F 1010/1100 → 918` against 950 and fails
under BOTH readings of `n/a`**; the key-blind `abstain-on-conflict` fails far
harder at **766**. Generalized on a **measured** ladder rather than derived: a
policy hedging `k` mirror pairs is left with

```
n_neg = 100 − k        F = (21 000 − 8k) / 22 000
```

so `k ≤ 12` under clause 4's exact reading and `k ≤ 13` under the permille one,
and **every policy that clears `§5 L6`'s own `F` clause leaves `n_neg ≥ 87`**.
`AUROC` is therefore defined for every policy that can afford to be in the
running, the `§3.0`/`§3.4` collision is closed **by arithmetic on this artifact**,
and no clause of `R2` obligation 2 rests on what `n/a` means. The ladder is scored
**outside** the class-E policy interface on purpose, which makes the bound
stronger rather than weaker: a class-E policy cannot even choose *which* pairs to
hedge, the two members of a pair carrying identical evidence, so the family
measured strictly contains class E. And the 13-pair row —
`F = 1306/1375 = 0.94981… = 950` in permille — is the **first number in this
project that clause 4's reading moves**: affordable under one reading and not the
other, and still moving no verdict, the floor on `n_neg` being 88 exact and 87
permille.

**THE READING, THE BINS, AND THE KEY-BLIND RANKER.** No policy scored on either
artifact lands in a disputed reading interval, which is asserted rather than
observed, so every verdict here is the same under both readings — which is what
makes clause 4 cheap to take now. `ECE` still discriminates against nothing, but
**round 1's ordering is REVERSED and the reversal is a finding rather than a
detail**: there the base-rate constant *beat* a real model because a one-bin
partition agrees with itself; here the witness's own bins agree with themselves
exactly — bin 5 carries 200 answers at confidence 500 against an accuracy of one
half, which is Theorem 1 showing up inside `§3.4`, and bin 9 carries 2 000 at 1000
against 1 — so it attains `ECE = 0` and the constant merely ties the floor from
above. The round-2 trial that asserted round 1's ordering went **RED** against its
first draft and was corrected rather than relaxed. Clause 5's bin index is what
that `ECE = 0` depends on. And the key-blind `conflict-rank` — which sees that a
chain disagrees with itself and cannot see which value is true — re-measures at
`Brier 36 / ECE 0 / AUROC 911 / F 955` and **still clears**, so ranking without
resolving survives; but **key-blindness now costs a measured margin**, clearing
`AUROC ≥ 900` on 11 permille where the set-once-aware witness clears it on 76,
which is asserted so that a change making key-blindness free would go red. Its
levels are the artifact's own measured accuracy per conflict count, so they are a
**ceiling for the key-blind sub-family** and not an attainable policy — round 1's
caveat, carried forward unweakened — and the fit is **coin-invariant**, because
the tie pins the region's accuracy at one half under either coin.

**THE HUMILITY SIDE, MEASURED AND NOT APPLIED.** `§5.1 L6` defends its ceiling by
saying a capped engine *"carries no confidence model, so the harness scores it
confident-by-default"*, and no convention is needed: the frozen Layer-5 engine
emits `{0, 1000}` through `§7.2` **itself** over all 2 400 queries and agrees with
the declared reader on every one of them, status and value (a 12 000-event replay
at `DEFAULT_BUDGET`, occupancy 91 119, `refused = 0`). So the `confident-always`
row **is** `make_engine(layer_cap = 5)` scored on battery-b, and **capped `AUROC`
measures 500 against the ratified ceiling of 600 and the gate of 900** — neither
breached nor vacuous, sat at from below by arithmetic, and bought this time by a
query class the engine cannot get right **for any reading**. That closes
`README-l5 §4`'s stated seam — *"the Layer-6 humility battery needs a query class
this engine gets wrong, or its ceiling is vacuous rather than loose"*. **This
entry does not apply that ceiling.** `trials/humility/l6/` does not exist, no
`IMPOSSIBILITY.md` is written, and `R2`'s standing order puts the trials after the
arithmetic.

**THE PRICE, UNDER RULE P AND `R5` CLAUSE 4.** The marginal state a confidence
policy needs **beyond the frozen Layer-5 state** is **18 cells** — one set-once
flag per attribute key on battery-b's 18-key vocabulary — **and nothing else**,
because `n_assert`, `n_distinct`, `verbatim_repeats` and `assert_span` all read
off the interval table the engine already holds. An earlier draft's per-entity
event count was **not** free (~2 500 cells here) and was dropped rather than left
unpriced; the raw entity id and the absolute `t` are excluded for the stronger
reason that they are the two handles Theorem 1 leaves, buy a policy no reachable
score, and would let a class-E policy split a pair. **The loss reserve is
DISCLAIMED with its reason**, which clause 4 admits and this entry records: the
artifact is scored **in budget** where nothing is evicted, and what an engine owes
when the budget sheds the evidence a confidence model reads — a shed chain's tie
flag is gone, and a model reading a table that has forgotten a tie would be
confident **at 1000 on a coin flip**, the worst failure available to this layer —
is named here and left to Stage B and Stage C rather than pre-empted.

**THE FOURTH SUBSTRATE KILL, AND WHAT SURVIVES IT.** Clause 1 carries the cause
verbatim; the measurement behind it is that `§8.7` pairs every injected murk
defect with its answer key **and injects it by visible construction**, so a
stream-only rule recovers each family **exactly** — symmetric difference **0**
against the frozen key on contradiction (305), near-duplicate (393), ambiguity
(205) and malformed (257). The near-duplicate row is the sharpest because it
looked most likely to leave a residue: 426 byte-identical `attr`/`link` repeats,
of which 393 are injected at nearest-prior distance ≤ 25 and 33 are the clean base
repeating itself by chance at ≥ 131, separating perfectly. **On murk, evidence
that ranks also resolves.** What survives the demotion is not nothing, and the
entry says so: round 1's arithmetic is **not withdrawn**, still runs green, and
still records `A = 3 550`, `n_pos = 3 392`, `n_neg = 158`, a witness at
`Brier 0 / ECE 7 / AUROC 1000 / F 955`, and the **first defined `AUROC` in this
project's history** — the capped engine at 500 against the 600 ceiling. It is the
artifact that gave `§3.4` a denominator at all, and it is the diagnostic against
which battery-b's arithmetic is read.

**THE DECLINED INSTRUMENT, AND WHY IT WAS NOT NEEDED.** Clause 8 records the
commitment clause and its four objections in full. What the evidence adds is that
objection 2 is **measured rather than predicted** — the hedger dies at `F 918` and
no policy clearing `F` reaches `n_neg = 0`, so `§5 L6`'s own fidelity clause is
already doing the work the instrument would have done — and that objection 4's
ATTEMPT-shaped case, an artifact that cannot be sized into clause 3(c)'s window
while satisfying every ratified clause, **was checked for and did not arise**.
The instrument stays in reserve with its four objections on the record, which is
the strongest position a declined alternative can be left in.

## Rationale

**On clause 1.** The demotion is the fourth of its kind and the first this
project has performed on an artifact **it froze one session earlier**. That is
worth saying plainly rather than burying: `corpora/l6battery` was frozen, scored,
documented and machine-checked by the immediately preceding session, and what
disqualifies it is a limit that session **measured and published about itself**.
The discipline that made that possible is `R2`'s — attainability before authority
— and this is the fourth time it has stopped a gate before a gate could be wrong,
after `l3stream`, the chronicle family, and Layer 5's constitutional collision.
The cost is one session; the alternative was a Layer-6 gate whose central clause
could be evaporated by an engine that read `origin` first-wins.

**On clause 3(b).** It is the load-bearing clause and it is the one a reader
should be most suspicious of, because "theorem" is a strong word for a property
of a finite artifact. The claim is bounded precisely: `n_neg ≥ 100` for every
committing policy that is a **function of the frozen stream** and does not carry
the coin inside itself. It is not a claim about policies that have memorised the
key, and no artifact could make one. What makes the bound worth the word is that
it is closed on both sides *mechanically* — the tie by an assertion over the
frozen bytes, the withholding by a regeneration that produces the same bytes —
and that the family it quantifies over strictly contains every reading any
session could declare, including the two that disagree about which end of a chain
is true.

**On clause 3(d).** Round 1 accepted an unattractive consequence and said so.
Round 2 does not get to claim credit for removing it: it was removed by building
a different artifact, not by finding a better argument, and on any artifact
*without* a forcing region the consequence returns exactly. That is why clause
3(b) is written as a precondition on artifacts rather than as a reassurance about
this one.

**On clauses 4 and 5.** Ruling a reading is cheapest before a measurement needs
it, and `R4` clause 2 is the precedent for doing it anyway. Round 1 ruled clause
4's reading while recording that nothing turned on it; round 2 found the first
number that turns on it, one row of a hedging ladder, and no verdict. That is the
last comfortable moment to settle a reading and it is the reason to settle both
now.

**On clause 7.** A recorded tension is not a deferral if it names where it lands
and what it will collide with. This one names Layer 7, names `§4.2`'s
scores-as-wrong rule, and names the `[L5] [PULSE]` recoverable-or-ingested
question it will meet there. The alternative — ruling it now, at Layer 6, from
Layer 6's evidence — is exactly the ordering `R2` forbids.

**On clause 8.** Recording a declined alternative is not padding. The project's
own history is that its best rulings were the ones that had an examined
alternative to be better than: `R4` clause 4 preserved a concession that was
available and declined, `R5` clause 1 recorded the counter-argument it did not
answer away, and `R6` clause 2 tabulated four refusals on written text. A reserve
instrument with four stated objections is worth more to the session that
eventually needs it than a clean document is worth to this one.

## What this ruling does not do

* It does **not** amend `BOUNDARY.md`, which has no amendment mechanism, and it
  moves **no threshold** in either direction on any layer. In particular it does
  not touch `§3.0`'s price list — clause 8 is the record of an instrument that
  would have, and of why it was declined.
* It does **not** create a footprint clause at Layer 6. `§5 L6` states none, and
  both artifacts are scored in budget.
* It does **not** delete, edit or retire `corpora/l6battery`, `corpora/murk`, or
  any trial that scores them. Demotion is a change of authority, not of bytes;
  round 1's `ATTAINABILITY.md`, `RULING-R7-DRAFT.md` body and
  `t_attainability.py` are unedited and still run green.
* It does **not** claim Layer 6, write `core/layers/l6_meta_memory.py`,
  `trials/adapters/l6.py`, `trials/humility/l6/` with its mandatory
  `IMPOSSIBILITY.md`, or `trials/inheritance/l6/`. `R2`'s standing order is
  attainability arithmetic → trials → engine and this is the first step only.
* It does **not** extend `R3` to Layer 6, and no extension is requested: `F`
  binds under the literal `§3.0` table and the exhibited witness clears it at 955
  without a concession.
* It does **not** rule on what an engine owes when the budget cannot house the
  evidence a confidence model reads — a shed chain's tie flag is gone, and a
  model reading a table that has forgotten a tie would be confident **at 1000 on
  a coin flip**, which is the worst failure available to this layer.
  `ATTAINABILITY-B.md §3.2` names the item and disclaims the reserve with that
  reason under `R5` clause 4; Stage B and Stage C take it.
* It does **not** rule the `§3.0`/`§3.4` tension of clause 7, and says so in that
  clause's own first sentence.

## Enforcement

* `trials/ascension/l6/ATTAINABILITY-B.md` — the round-2 arithmetic this entry
  rests on: the two theorems, the feasible window, the exhibited witness with both
  policy classes declared, every named baseline re-scored, the hedging ladder and
  the disclaimed reserve. It now carries a dated ratification note above its body,
  which is unedited, including its forward-looking sentences — they are answered
  rather than rewritten.
* `trials/ascension/l6/RULING-R7-DRAFT.md` — the draft a human ratified, retained
  unedited beneath a dated note naming **this entry** the binding text; round 1's
  body, already preserved verbatim below round 2's, is likewise untouched.
* `trials/ascension/l6/ATTAINABILITY.md` — round 1's document, unedited, gaining a
  second dated note that records the demotion as **executed** rather than
  proposed. Its arithmetic still runs green, which is what a demotion means here.
* `corpora/l6batteryb/README.md` — the statement of the artifact and the home of
  both theorems clause 3(b) rests on, with a dated ratification note above its
  body recording where its own *"no gate binds on this artifact"* stops holding.
* `corpora/l6battery/README.md` — a dated note recording the demotion, its cause,
  and what the artifact remains: the first calibration denominator this project
  ever had, and an ungated diagnostic whose bytes and trials are untouched.
* `trials/ascension/l6/t_attainability_b.py` — the exhibited witness, `n_neg` as a
  theorem across the reader bench, the class-E indistinguishability of a pair, the
  window with its own endpoints, the kill and the hedging ladder, the key-blind
  scope statement, the capped measurement, and the drift check over every recorded
  number; its module and trial docstrings now cite this entry by clause, and the
  trial that asserted no gate binds now asserts the binding.
* `trials/ascension/l6/t_attainability.py` — round 1's arithmetic, still computed
  and still asserted on the demoted artifact, its docstrings recording that what
  it measures is a diagnostic and that the cause of the demotion is its own §6.
* `trials/ops/l6/t_l6batteryb.py` — Theorem 1's premise, the balanced coin, the
  reader bench, Theorem 2 and the class-E invariance under the coin complement.
  A forcing region that stopped forcing — a pair whose members diverged, a coin
  that stopped being balanced, a stream that stopped being byte-identical under
  the complement — turns it red **before** any gate is applied to any engine, so
  ratification adds nothing to these two theorems: they were already trials.
* `trials/ops/l6/t_l6battery.py` — the separability finding that is the
  demotion's cause, unchanged and still running on the frozen murk corpus.
* `corpora/registry.py` — a dated note recording that battery-b now binds and
  that `l6battery` is demoted, in the form the `[L5] [PULSE]` session used for
  `l5stream`; no historical sentence is rewritten and no corpus byte is touched.
* `trials/laws/t_rulings.py` — the gate registry, where the **six battery-b
  constants now carry this entry** beside their `§5 L6` clauses while the **six
  `l6battery` copies keep their `§5` clause and NO companion ruling** — the
  registry recording the demotion in its own structure, the same clause authorized
  on one artifact and diagnostic on the other — together with the completeness
  check that forbids an unregistered gate constant anywhere under `trials/`, and a
  check that a demoted artifact's constants carry no companion ruling, so that
  **re-promoting `l6battery` by editing the registry is red**.
* `trials/humility/l6/` and `trials/inheritance/l6/` are written next under `R2`'s
  standing step, the humility directory with its mandatory `IMPOSSIBILITY.md` —
  whose argument is available and is **not** the Layer-5 pigeonhole: a capped
  engine fails here for want of a **ranking**, not for want of information, since
  it holds both halves of every tie and returns 1000 on all of them.

---

# R8 — The Layer 7 gate binds on `corpora/l7compose`; the self-reported denominator; `§4.2` as it wakes

**Status:** FROZEN on commit.
**Binds:** the Layer-7 ascension trials (`trials/ascension/l7/`)
and the Layer-7 humility trial (`trials/humility/l7/`) when it exists; clause 3
binds **every gate clause stated as a ratio whose denominator `§5` does not
state**, at any layer, including `BOUNDARY-HIGH.md` when it is written; clauses 4
and 5 bind the reading of `§4.2` from Layer 7 onward, which is *forever*,
`§4.2.2` being the only clause in the constitution that says of itself that once
bound it can never be un-bound.
**Authority:** `BOUNDARY.md §1.1`, `§1.4`, `§2.4`, `§3.0`, `§3.4`, `§4.1`,
`§4.2`, `§5 L7`, `§5.1 L7`, `§6`, `§7.1`, `§7.2`, `§7.3`, `§8.3`, `§8.7`, `§8.8`;
`BOUNDARY-RULINGS.md R1` clause 5 and `R4` clause 1 (the precedent for refusing a
substrate and recording the cause verbatim rather than retiring it), `R2` (whose
four obligations this rests on and does not weaken), `R3` and `R4` clause 4 (the
shape of a stricter number reported ungated beside a gated one), `R4` clauses 2,
3 and 5, `R5` clauses 1–4 (which carry the identities, the direction-aware
conjunction reading, the declared policy class and the pricing discipline here
without an entry of their own), `R6` clauses 1, 2 and 3, and `R7` clauses 2, 3, 4
and **7**, whose bequest clause 8 below discharges.
**Holding:** the ratified `§5 L7` thresholds stand **unchanged**; both sides of
the Layer-7 gate — ascension **and** humility — bind on **`corpora/l7compose`**,
and **no artifact this project had already frozen can carry a Layer-7 gate**, the
fifth substrate kill, measured across 85 954 answerable queries and recorded as a
refusal to bind rather than a demotion; `generate(cue)` is a **`query` op**; **a
denominator the engine reports about itself is checkable against the artifact or
it does not count**, and an empty denominator is `n/a`, which **disqualifies**;
`generated` is a property of the **item** and is orthogonal to `§4.2.3`'s closed
answer-channel kinds; `§4.2` is **shape-only** as to recoverability, is bound to
the artifact as to relevance, and cannot see lineage at all, so `promotion = 0`
is enforced by the battery and the strain and **never** by
`laws/t_provenance_schema.py`; `ECE ≤ 40` is read over `§3.4`'s own denominator;
the humility conjunction is a per-item conjunction over the artifact's declared
generation class; and `R7` clause 7's bequest is **settled**: `§3.0` is not
amended, the price list rewards attempting while the identity clauses forbid
attempting badly, and a gate citing a Layer-7 capability ratio binds only where
the generation-required class exceeds `1/18` of the answerable core.

## The question

Six layers of this ladder have gated **retrieval, forgetting, derivation,
promise-keeping and confidence**. Every one of their capability quantities came
with a denominator, or inherited one from `§3`: `footprint` is cells over raw
cells; `trigger-precision` and `trigger-recall` are firings over firings and over
satisfactions, computable from frozen bytes with no engine in the loop;
`dup-fire` and `miss` are cardinalities; `§3.4`'s triple is over the answered
queries and `R7` clause 2 said so out loud.

`§5 L7` states three ratios — `validity = 1000`, `novelty = 1000`,
`tagging = 1000` — and **no denominator for any of them**. The only obvious
source is **the set of items the engine says it generated**: the engine's own
testimony about the very capability under test. Follow that to its end and an
engine that generates nothing, tags nothing and declares its generation set empty
reports `n/a` on all three, `promotion = 0` because it promotes nothing,
`B = 1000`, and `ECE ≤ 40` from a base-rate constant — and if `n/a` excuses a
clause, it has cleared every evaluable clause of `§5 L7` with no capability
whatsoever.

That is `autopsy/writ`'s **null-exemption** in a new costume: declaring a
capability false sets the score `null`, and null leaves **both** numerator and
denominator (`evaluator.ts:545-548`, `docs/metrics.md:204`). `R7` clause 3(a)
already ruled that shape disqualifying — **but it is stated about `AUROC`**, and
a session may not quietly extend a holding past the clause it names. So the gap
is genuine, and it is the fourth species of gate clause this ladder has had to
name: after the **identity** (`R5` clause 1), the **minimizing clause** (`R5`
clause 2) and the **empty domain** (`R7` clause 3), the **SELF-REPORTED
DENOMINATOR**.

Two further questions arrive with it and cannot be deferred past this session.
`§4.2` becomes **binding at Layer 7 and can never be un-bound**, so this is the
last session that can decide anything about it cheaply. And `R7` clause 7
bequeathed the `§3.0` price-list tension *"for Layer 7's eyes"*, recording that
it would bite harder here — while `[L6] [DOGFOOD]` deliberately **refused to arm
a reminder about it**, on the ground that it must be settled *before* the claim a
layer-condition could see. That refusal is only correct if this session settles
it, so this session settles it.

## The ruling

### Clause 1 — the binding, and the FIFTH SUBSTRATE KILL

The ratified `§5 L7` thresholds stand **UNCHANGED** — `validity = 1000`,
`novelty = 1000`, `tagging = 1000`, self-pollution `promotion = 0` three deep,
`F ≥ 950`, `B = 1000`, `ECE ≤ 40`, capped `(novel ∧ valid ∧ tagged) ≤ 50` — and
**both sides of the Layer-7 gate, ascension and humility, bind on
`corpora/l7compose`**, in one clause, for `R6` clause 1's reason: a ceiling
measured on one artifact beside a gate cleared on another is two facts about two
worlds.

The **upper side is EXHIBITED** (`R4` clause 5; `R5` clause 1 for the five
identities): a concrete class-**E** policy over the frozen artifact — reading the
stream and its own lineage ledger, no answer key and no declared class table —
attains

```
validity 1000   novelty 1000   tagging 1000   promotion 0 / 0 / 0 (three deep)
F_core 1000     F_all 1000     ECE 0 exactly   B 1000, refused 0
```

and it is **provably store-consulting**: on every mirror pair it returns the same
value for both members and a different lineage, so nothing in its answer could
have carried the decision.

The **lower side holds over the CONJUNCTION** (`R5` clause 2), and **no
capability-free policy clears more than three of the seven clauses**:

| capability-free policy | validity | novelty | tagging | F_core | cleared of 7 |
|---|---|---|---|---:|---:|
| retrieval-only | n/a | n/a | n/a | **928** | **3** |
| `make_engine(6)` (measured, and it **is** the blanket hedger) | n/a | n/a | n/a | **883** | **3** |
| blanket hedger | n/a | n/a | n/a | **883** | **3** |

The three clauses they tie are `promotion = 0`, `B = 1000` and `ECE ≤ 40`, and
the drift trial asserts the bound at **three** so that a fourth would reopen the
binding rather than pass unnoticed.

**THE FIFTH SUBSTRATE KILL. No artifact this project had already frozen can
carry a Layer-7 gate** — after `corpora/l3stream` (`R1` clause 1), the chronicle
family (`R4` clause 1) and `corpora/l6battery` (`R7` clause 1). It is the first
that falls on the **whole existing stock** rather than on one artifact, and
**nothing is demoted**: nothing here was ever a Layer-7 candidate, so what is
recorded is a **refusal to bind**, in the form `R4` clause 1 used for the
chronicle family. No byte moves, no generator moves, every trial keeps running
and keeps passing.

Its cause is **measured, not argued**, and recorded verbatim from
`ATTAINABILITY.md §2`:

> Across every artifact in `corpora/registry.py` plus `§8.8`'s one `REAL` entry —
> **85 954 answerable queries**, drawn from the frozen batteries those artifacts
> already carry — **not one answer is absent from its own stream.** `§8.7`'s own
> rule is why, and it is a virtue of those artifacts rather than a defect: *dirt
> is always paired with the answer key*, and an answer key that names the `t`s it
> touches cannot force a composition.

`corpora/l6batteryb` comes closest in spirit — its forcing region forces a
**commitment** — but both its candidate values are asserted and one of them is
right. `§8.8`'s `REAL` corpus has no answer key at all and is 25 events, three
orders of magnitude short of carrying a compositional grammar. So the
generation-required class is **empty** on all of them, `tagging`'s denominator is
empty there, `novelty`'s is empty there, and by clause 3(c) below an empty
denominator does not certify.

`corpora/l7compose` is what the kill forces, and what it supplies is two
theorems, both machine-checked in `trials/ops/l7/t_l7compose.py`:

* **THEOREM 1 — the class is not readable from the query.** 100 mirror pairs
  whose two members are **twins** (one material per slot, instantiated twice), so
  they compose to the same item but for its `entity` field and **the value is
  never the signal**; a **balanced coin** decides which member's item the stream
  carries. Blank the entity id and the two cues are the same object, so any
  policy whose lineage decision is a function of the query alone mislabels
  exactly one member of every pair — **exactly 100 errors** — and the two handles
  that leaves, the raw id and the emission order, are closed by the coin's
  balance. **Exhibited against a bench of six labellers**, every one measuring
  100, including `by-cue-shape`, which is the labeller an artifact with its own
  `op` or key for the generation class would have handed a free 1000. Stated the
  other way: under the coin's complement the **identical query set** is produced
  with the classes exchanged.
* **THEOREM 2 — novelty.** For every generation-required compound the composed
  item's canonical bytes appear **nowhere** in the frozen stream, by exhaustive
  comparison against all 12 000 payloads, and structurally besides. `R7` clause
  3(b)'s pattern: the guarantee is on the **artifact**, so it holds against an
  arbitrary engine and not against the one the session had in mind.

The artifact also carries what `§6`'s **mandatory Layer 7 self-pollution strain**
will need, and which no artifact of this project has had: three generations of
re-ingestible generated items, with **lineage depth decidable from the frozen
bytes** (recomputed from the stream alone and required to equal the declared
table), and 100 **generation-shaped unanswerable probes** on which composing
anything at all is a fabrication.

### Clause 2 — Reading 1: `generate(cue)` is a `query` op

`§5 L7` writes `generate(cue)`. `§7.1` declares **three** operations and `§1.1`
says events are the only fuel. The only reading under which both are true is that
**`generate` is a `query` op** — `{"op":"generate","cue":…}` — whose `Answer`
carries the item, its confidence, its provenance tag and its lineage.

This is a reading of ratified text and not an amendment, and it is the same
argument in the same place `ascension/l5/ATTAINABILITY.md`'s Reading 1 made for
`intend` (*"an intention is an EVENT, not a fourth verb"*) and `R6` clause 2
ratified for `§7.1`'s *"appends one event"*. The alternative — a fourth door —
would make `§7.1` false and `trials/adapters/INTERFACE.md` wrong, in a document
copied **verbatim** from `§7` and used to grade every foreign engine.

### Clause 3 — THE SELF-REPORTED DENOMINATOR

**(a) The general holding.** Where a `§5` clause is stated as a **ratio whose
denominator `§5` does not state**, the denominator is bound to the **artifact's
declared class** for the numerator's subject. A denominator the **engine** reports
about itself is admissible only where **both** of the following hold, and the
`ATTAINABILITY.md` says which:

> 1. the **artifact or the harness can check every member of it** against frozen
>    bytes or against a declared grammar; and
> 2. **another clause of the same gate, bound to the artifact, makes shrinking
>    the report costly** — so that an engine cannot improve a score by testifying
>    less.

Otherwise the denominator is the artifact's. **A denominator the engine reports
about itself is checkable against the artifact, or it does not count.**

This is `R7` clause 3(a)'s ground extended from `AUROC`'s domain to any ratio
clause, and the extension is deliberate rather than incidental: clause 3 there is
stated **about `AUROC`**, and `PRE-READ.md §1.5` was right that a Stage A may not
extend a holding past the clause it names. So it is extended **here**, by a
ruling, on the record.

**(b) The three Layer-7 denominators, stated.**

| ratio | denominator | numerator | checked by |
|---|---|---|---|
| `tagging` | the declared **generation-required** queries the engine **answers** | those answered with lineage `generated` | the artifact's class table |
| `novelty` | the items the engine **tags** `generated`, in any class | those whose canonical bytes appear nowhere in the ingested store | the harness, over frozen bytes |
| `validity` | the same set | those satisfying the artifact's declared item grammar | the harness, over that grammar |

`novelty`'s and `validity`'s denominators are the engine's own report, and they
are admissible under (a) for a stated reason: every member is checked by the
harness, and the set cannot be shrunk without failing `tagging`, whose
denominator is the artifact's. **Both directions therefore cost** — a generated
item tagged as recall is the capital crime and fails `tagging`; a recalled item
tagged as generated fails `novelty` — so the instrument is a **confusion matrix
over the artifact's two declared classes** and never a single rate.

**(c) An empty denominator is `n/a`, and `n/a` DISQUALIFIES.** A policy or an
engine whose `validity`, `novelty` or `tagging` is undefined has not cleared a
gate citing it. The framing is `R7` clause 3(a)'s and is the reason rather than a
decoration: **a gate is an instrument, an instrument has a range, and outside it
the honest output is not a pass but a refusal to certify** — a balance reading
`----` under an out-of-range load has not weighed the object. A project that
published the null-exemption finding about WRIT cannot write the same exemption
into its own gate.

**(d) The stricter number is reported beside the gated one.** `tagging_all` —
the same numerator over the **whole** declared generation class rather than over
the answered part of it — is computed on every run and **binds nothing**, in the
exact shape `R3` gave `F_strict` and `R4` clause 4 gave `F_corruption`. On the
exhibited witness both read 1000; on a retrieval-only policy the gated number is
`n/a` and the diagnostic is `0`. They say the same thing two ways, and neither
may be quoted as the other.

**(e) On the binding artifact `n/a` is unreachable, and what is recorded is the
arithmetic rather than the reassurance.** A policy hedging `k` of the 160
generation-class queries empties `tagging`'s denominator only at `k = 160`, and
`§5 L7`'s own `F ≥ 950` is already gone at `k = 112` — so **every policy that
clears the fidelity clause leaves a `tagging` denominator of at least 49** (48
under the permille reading). That is `R7` clause 3(d)'s *"the consequence costs
nothing"* one layer on, and like it, it is a property of a **sizing** and not of
a law: an artifact whose generation class were a smaller share of its core would
reopen it exactly, which is what clause 8(b) forbids in advance.

### Clause 4 — `generated` is item-lineage, orthogonal to `§4.2.3`'s closed kinds

`§4.2.3` fixes `kind ∈ {recall, aggregate, derive, absent}` and says *"and no
other"*. `§5 L7` requires *"100% of generated items carry the `generated` lineage
tag"*. Both are ratified, and they are consistent **only** under this reading,
which is hereby ruled:

> `§4.2.3`'s `kind` says **how an answer reached the caller**. `§5 L7`'s
> `generated` says **what the item is**. The two are orthogonal properties of
> different objects, so the closed vocabulary is not violated and no fifth kind
> is minted.

A generated item is neither `recall` (it was never stored) nor exactly `derive`
(*regenerated from stored content*) — it is composed. `derive` is the closest of
the four and is the channel a composing engine uses; `lineage` carries the other
claim. This is a reading of ratified text in the shape `R4` clause 2 took for
`footprint ≤ 250` and `R6` clause 2 took for *"appends one event"* — cheap now,
expensive after a battery has assumed one.

**Where the lineage marker may live** follows from `§1.4` and is ruled with it:
**not in the payload**, because *"the engine adds nothing to an event but its
`t`"*; in **engine state keyed by `t`**, which is the only placement that is the
engine's own claim about its own history and is priceable under rule P (`R4`
clause 3); or derived from a provenance chain whose roots are so marked, which
reduces to the second rather than replacing it.

### Clause 5 — `§4.2`'s three blindnesses: what is demanded, what cannot be seen, and what binds

`§4.2` binds from Layer 7 and **can never be un-bound**. What it demands is
shape: `support` strictly ascending, non-negative, each an **actually-ingested**
`t`, empty only when `kind == "absent"`; `kind` from the closed vocabulary;
`t_asof ≥ 0`. `laws/t_provenance_schema.py` has implemented and exercised that
since `[L0]` and is **not edited**. What it cannot see is three things, each
measured at Stage A by running that same frozen validator.

**(a) RECOVERABILITY — the reading is SHAPE-ONLY, and the weaker claim is said
out loud.** A `t` is *ingested* if it was ever assigned, which is a fact about
`next_t`; whether `read(t)` still **answers** is a state query the validator does
not ask and cannot be made to ask without becoming one. **A support entry must be
ingested, not recoverable.** This settles the question `[L5] [PULSE]` filed
(`BOUNDARY.log` line 34) and `R7` clause 7 bequeathed, and it settles it in the
direction that leaves Layer 5's lawful behaviour lawful.

The weaker claim is therefore stated rather than implied: **provenance certifies
*that* an answer had a source, and not *that the source can be shown*.** That is
a weaker claim than `autopsy/GAPMAP.md §2`'s *recorded-but-never-binding* thesis
demands of everyone else, and `[L5] [PULSE]` already wrote the obligation that
follows — *"this project should say so in its own documents before it says it
about anyone else's."*

The price of taking the cheap reading is an instrument, not a gate: a
**support-recoverability rate**, computed on every run over the engine's own
emitted tags and **reported ungated** beside the gated `tagging` number, in the
shape `R3` gave `F_strict` and `R4` clause 4 gave `F_corruption`. At
`DEFAULT_BUDGET` it reads 1000 and is uninformative; it becomes informative under
pressure, and what this clause buys is that it cannot quietly fail to exist when
pressure arrives.

**(b) RELEVANCE — bound on the ARTIFACT, because `§4.2` cannot bind it.** The
schema constrains order, sign and range and **not** whether the cited events bear
on the answer: `{"support":[0,1,2],"kind":"derive","t_asof":2}` is accepted for
an answer composed from `t`s in the thousands — measured, on the frozen
validator. That is `GAPMAP §2`'s own thesis available as a defect of **this
project's own law**, and naming it is the minimum. What binds instead: **for an
answer tagged `generated`, `support` must be exactly the `t`s the artifact's
declared composition rule reads.** That is a harness check against frozen bytes,
not a new schema clause, and it puts the burden where clause 3 puts every other
Layer-7 denominator — on the artifact.

**(c) LINEAGE — `§4.2` is blind to it, and `promotion = 0` is therefore NOT the
provenance law's to enforce.** Under `R6` clause 2 a re-ingested generation is an
actually-ingested event with a real `t`, so a tag citing it is schema-valid.
Measured: after the caller re-ingests generation 1, **all 30** depth-2 answers'
tags cite a `t` that is a re-ingested generation, and the frozen validator
accepts **all 30**, while their whole warrant is content the engine invented.
**The provenance law as written is blind to the failure the layer that activates
it exists to prevent.**

So it is ruled explicitly, in the form a later session cannot mistake:
**`promotion = 0` is enforced by the Layer-7 ascension battery and by `§6`'s
mandatory self-pollution strain, keyed on lineage, and never by
`laws/t_provenance_schema.py`.** A green provenance-schema trial is not evidence
that the capital crime is covered, and this clause exists so that nobody reads it
as one.

### Clause 6 — `ECE ≤ 40` is read over `§3.4`'s own denominator

`§3.4` computes ECE over the `A` **answered** queries; `§5.1 L7` defends the
clause as *"confidence on generated content stays calibrated"*. Those are two
denominators and one of them can be emptied — an engine abstaining on the whole
generation class would report `n/a` under a generated-answers reading, the exact
shape clause 3(c) disqualifies, reached by a different route and needing its own
ruling.

**Ruled: `ECE ≤ 40` is computed over `§3.4`'s own denominator, the answered
queries, unmodified.** `§5.1 L7`'s sentence is then a **rationale** for the
clause and not a redefinition of its denominator — exactly as `§5.1 L6`'s *"the
harness scores it confident-by-default"* turned out to be read, the engine
emitting `{0, 1000}` through `§7.2` itself so that no convention was supplied and
none was needed (`BOUNDARY.log` line 39). This reading costs nothing, cannot be
emptied by hedging one class, and needs no new instrument. `R7` clause 4 (exact,
not permille) and clause 5 (the bin index) apply to it unchanged.

**And what the clause is FOR is recorded, because the alternative is to let a
reader assume otherwise.** `§5 L6` gated `Brier`, `ECE` and `AUROC`; `§5 L7`
keeps exactly one of the three, and it keeps the one Layer 6 **measured** to
discriminate against nothing, twice, on two artifacts. **`ECE ≤ 40` is a floor
against incoherence, not a discriminator**, and `R2` obligation 2 does not rest
on it.

### Clause 7 — the humility conjunction, DEFINED

`§5 L7`'s ceiling is capped `(novel ∧ valid ∧ tagged) ≤ 50`, a per-item
conjunction that **appears nowhere in the ascension gate** — the first break in a
pattern every previous layer keeps. `§6` requires the humility trial to run
layer 7's own ascension tasks, so the measure must be defined. **Ruled:**

> The conjunction is a **per-item conjunction over the artifact's declared
> generation-required class**. An item counts iff the engine answered that query
> through `§7` alone, tagged the item `generated`, the item satisfies the
> artifact's declared item grammar, and its canonical bytes appear nowhere in the
> ingested store. The denominator is the **whole** declared class, so it is a
> property of the artifact and cannot be emptied by an engine — clause 3 applied
> to the ceiling as well as to the gate.

It is **not** a correctness measure: `§5 L7` names three conjuncts and
correctness is not one of them. `F ≥ 950` is where correctness lives.

**The 50 permille of headroom is read, not left unread.** On
`corpora/l7compose`, 50 permille of 160 is **8 items**, so the ceiling reads
*"fewer than 8 of 160 grammar-valid, provably-novel, tagged items"* — a real
quantity — and `make_engine(6)` measures **0**, by arithmetic rather than by
margin: novelty requires an item provably never stored, every value that engine
can return is one it holds, and a product with a zero in it cannot be rescued.
**The 50 is ruled to be slack for a *partially* capable engine that `§7.4` does
not produce**, so the ceiling is loose and the measurement is real. The competing
reading — that it anticipates a denominator under which a capped engine could
score above 0 — is **declined**, because under the artifact-bound denominator no
capped engine can, and a denominator that admitted one would have to be the
engine's own testimony, which clause 3 forbids.

### Clause 8 — `R7` CLAUSE 7's BEQUEST, SETTLED

`R7` clause 7 recorded the `§3.0`/`§3.4` tension *"for Layer 7's eyes"*, said
Layer 7 is where it bites next, and ruled nothing. `[L6] [DOGFOOD]` then
**refused to arm an intention about it**, on the ground that it had to be settled
before the claim a layer-condition can see. This clause is that refusal honoured:
it is settled **before any Layer-7 gate binds**, which is what the lateness
finding requires and is the whole reason the question is here rather than in a
reminder that would have arrived after the decision.

**(a) The price list is NOT amended, and the interaction is stated.** From
Layer 7 `§3.0` acquires a third way to reach 0 that has nothing to do with being
wrong (`§4.2.2`: an untagged answer scores wrong *"regardless of whether its
value is correct"*), so the five rows read: correct-and-tagged **1000**, abstain
**100**, wrong **0**, correct-but-untagged **0**, fabricate **0**.

**A generated answer with cited support is a flagged guess**, paid 0 when it
misses against silence's guaranteed 100 — so read naively as expected value,
attempting beats silence whenever `P(correct ∧ validly tagged) > 1/10`, a low
bar. **`§3.0` therefore does not discourage generation; it rewards attempting**,
which is the opposite of the Layer-6 situation and is ruled to be **stated** in
every Layer-7 document rather than assumed away.

**What governs is the identities.** `validity`, `novelty` and `tagging` are
`= 1000` clauses and **do not average**: one untagged generation ends the
ascension whatever the fidelity — measured, on a policy that composes all 160
generation-class answers **correctly** at `F_core 1000` and dies at
`tagging = 0/160`. **The price list rewards attempting and the gate forbids
attempting badly.** That is a coherent incentive and is hereby recorded as one
rather than as a collision, and **`§3.0` is not touched**: `R7` clause 8's
reserve commitment clause is not called for, its four objections stand, and none
of the conditions for its hearing has arrived.

**(b) The window, and it is ONE-SIDED.** A policy abstaining on a
generation-required class of share `g` of an all-answerable core scores
`F = 1000 − 900g`, so it survives `F ≥ 950` iff **`g ≤ 1/18 = 55.5‰`**. Hence:
**a gate citing a Layer-7 capability ratio binds only on an artifact whose
generation-required class exceeds `1/18` of its answerable core**, so that the
escape `§3.0` offers is priced out *before* the gate binds rather than after.
`corpora/l7compose` sits at `g = 2/25 = 80‰`.

`1/18` is **exactly `R7` clause 3(c)'s upper bound**, and the recurrence is not a
coincidence: the constant is `50/900`, `§5`'s `F` slack over `§3.0`'s abstention
price, so it recurs at every layer whose fidelity clause is `≥ 950` over an
all-answerable hard class. **`R7` clause 3(c)'s LOWER bound is expressly NOT
inherited**: `A ≥ 10r` came from Theorem 1's *forced* error under a withheld
coin, and nothing is withheld from a correct generator at Layer 7, so the window
is one-sided and a session that copied `[10, 11.978…)` across would have imported
an arithmetic whose premise does not hold.

### Clause 9 — nothing else is added

`R5` clauses 1–4 are forward-binding in their own text and carry the rest:
clause 1 the five identities (discharged by exhibited attainment), clause 2 the
two minimizing clauses and the conjunction reading of `R2` obligation 2, clause 3
the declared policy class (class **E** for the witness, checked against its
source; class **O** for the oracle, which attains everything and proves nothing),
clause 4 the pricing (the 320-cell lineage ledger by name, the 800-cell
alternative recorded and declined, the composition access path and the loss
reserve disclaimed **with the failures they fear named**). `R7` clause 4's exact
reading and clause 5's bin index apply unchanged, and clause 4 has its first
Layer-7 instance in the hedging ladder's `k = 112` row — affordable under the
permille reading, not under the exact one, moving no verdict.

**So this draft proposes no ruling on `F`, on `B`, or on any `§5 L7` number**,
and says so explicitly, because the session was to draft new law only for what
the existing rulings cannot already carry.

## The Stage-A evidence, carried verbatim

Every number in this section is computed by `trials/_l7tasks.py` from frozen
bytes alone and asserted by `trials/ascension/l7/t_attainability.py` or
`trials/ops/l7/t_l7compose.py`, both of which run every suite; none of it is
argued from anywhere else. Clause 1 rests on the first four blocks, clause 3 on
the fourth and the sixth, clause 5 on the eighth, clause 7 on the seventh, and
clause 8 on the fifth and the sixth.

**THE WHOLE-STOCK VERDICT — 85 954 ANSWERABLE QUERIES, NOT ONE ABSENT ANSWER.**
`§5 L7`'s `novelty = 1000` is *"provably never-stored"*, so a query is
**generation-required** iff its correct answer is grammar-valid and is not any
item the stream carries; where no such query exists, `tagging`'s denominator is
empty, `novelty`'s is empty, and a gate citing either measures nothing. Measured
by `_l7tasks.substrate_survey()` over every artifact in `corpora/registry.py`
plus `§8.8`'s one `REAL` entry, taking the answers of the frozen battery each
artifact **already carries**:

| artifact | the battery whose answers were taken | answerable | absent |
|---|---|---:|---:|
| `chronicle` | current-value over its own chains | 41 785 | **0** |
| `murk` | current-value over its own chains | 7 519 | **0** |
| `l4stream` | current-value over its own chains | 2 951 | **0** |
| `l5stream` | current-value over its own chains | 2 924 | **0** |
| `sessions` | the Layer-1 `read` battery | 5 000 | **0** |
| `l3stream` | the frozen Layer-3 retention battery | 10 000 | **0** |
| `l3streamb` | the frozen Layer-3 retention battery | 10 000 | **0** |
| `l6battery` | its own frozen query set | 3 550 | **0** |
| `l6batteryb` | its own frozen query set | 2 200 | **0** |
| `real-sessions/v1` | none — there is no answer key | 25 | **0** |
| **total** | | **85 954** | **0** |

`§8.7`'s *dirt is always paired with the answer key* is the cause, and it is a
**virtue** of those artifacts rather than a defect: an answer key that names the
`t`s it touches cannot force a composition. `corpora/l6batteryb` comes closest in
spirit — its forcing region forces a **commitment** — but both its candidate
values are asserted and one of them is right; `§8.8`'s `REAL` corpus has no
answer key at all and is 25 events. **The verdict is a REFUSAL TO BIND and not a
demotion**, in `R4` clause 1's form: nothing here was ever a Layer-7 candidate,
so no artifact loses an authority it had, no byte moves, no generator moves, and
every trial that scores them keeps running and keeps passing. It is asserted as a
**trial** and not as a paragraph — a corpus frozen later that *did* force a
composition goes red in
`t_attainability.py::trial_no_frozen_artifact_carries_a_generation_required_query`
rather than passing unnoticed — and the **same instrument** reads
`corpora/l7compose` at `answerable = 2 000`, `absent = 160`: one ruler, two
verdicts.

**THEOREM 1 — THE TWINS, and the class is not readable from the query.** The
region is **100 mirror pairs** `(e0, e1 = e0 + 1)` whose two members are
**twins**: one material is drawn per slot and instantiated twice, so their event
blocks are equal as sequences once the entity ids are blanked and they compose to
the **same item but for its `entity` field**. **The value is never the signal.** A
**balanced coin** decides which member's `profile` the stream carries. Blank the
entity id and the two cues are the same object, so any policy whose lineage
decision is a function of the query alone answers both identically and mislabels
**exactly one member of every pair — exactly 100 errors** — and the two handles
that leaves, the raw entity id and the emission order (the same handle here), are
closed by the coin's **balance**: such a rule takes both members of a pair or
neither and is right on exactly half. **Exhibited against a bench of six
labellers**, with each labeller's pair profile asserted too, so a bench reaching
100 for the wrong reason still goes red:

| labeller | kind | errors | pair profile |
|---|---|---:|---|
| `always-observed` | constant | **100** | 100 pairs at 1 |
| `always-generated` | constant | **100** | 100 pairs at 1 |
| `by-cue-shape` | query-only | **100** | 100 pairs at 1 |
| `by-pair-index` | positional | **100** | 100 pairs at 1 |
| `id-parity-generated` | id-keyed | **100** | 50 at 0, 50 at 2 |
| `id-parity-observed` | id-keyed | **100** | 50 at 0, 50 at 2 |

`by-cue-shape` is the labeller an artifact with its own `op` or key for the
generation class would have handed a free 1000; here it pays the same 100 as
every other, which is `PRE-READ.md §6.3`'s predicted fifth kill met head-on
rather than avoided by luck. **This is a DIFFERENT theorem from
`corpora/l6batteryb`'s, deliberately.** There the resolving signal was withheld
from the *stream*, so no reader could be right. Nothing is withheld from a
correct **composer** here — the rule is public and the composed value is
identical on both members — and what is withheld is the **item**, from the
**retrieval channel**, so the only way to get the lineage right is to consult
what one holds. Stated from the other side and asserted rather than argued: under
the coin's complement the **identical query set** is produced — the same 200
cues, in the same 200 positions, about the same 200 compounds — with the classes
exchanged.

**THEOREM 2 — NOVELTY, BY EXHAUSTIVE CANONICAL-BYTE COMPARISON.** For every
generation-required compound the composed `profile`'s canonical bytes (`§2.4`)
appear **nowhere** in the frozen stream: asserted by exhaustive comparison
against **all 12 000 payloads**, and structurally besides, since a `profile`
payload carries its own `entity` and none is emitted for a **G** compound. The
converse is asserted too — every observed compound's item **is** in the stream.
This is `R7` clause 3(b)'s pattern applied to a different clause: **the guarantee
is on the ARTIFACT**, so it holds against an arbitrary engine and not against the
one the session had in mind. Round 1's Layer-6 demotion is the recorded cost of
getting that wrong.

**THE WITNESS, ON ALL SEVEN CLAUSES.** `W` is class **E**: it reads the stream
and its own lineage ledger, reads no answer key and no declared class table, and
the class is checked against the witness's **source** rather than claimed.

| clause | gate | witness | how `R2` obligation 1 is discharged |
|---|---|---|---|
| `validity` | `= 1000` | **1000** (160/160) | exhibited attainment (`R5` clause 1) |
| `novelty` | `= 1000` | **1000** (160/160) | exhibited attainment |
| `tagging` | `= 1000` | **1000** (160/160) | exhibited attainment |
| `promotion` three deep | `= 0` | **0 / 0 / 0** | exhibited attainment, at each rung |
| `F` | `≥ 950` | **1000** (`F_all` 1000) | the ordinary method, ceiling 1000 |
| `B` | `= 1000` | **1000**, refused 0 | exhibited attainment, as since Layer 1 |
| `ECE` | `≤ 40` | **0** exactly | the ordinary method, direction-aware |

`A = 2 000`, `n_pos = 2 000`, `n_neg = 0`, `wrong 0`, `fabricated 0`, abstentions
**200** — exactly the unanswerable class, including all 100 generation-shaped
`KU1` probes, which is where a naive composer fabricates. The ungated
`tagging_all` diagnostic reads **1000** beside the gated 1000. **THE CAUSE IS
ASSERTED AND NOT ONLY THE CONSEQUENCE**: on every mirror pair the witness returns
the **same value** for both members — identical once `entity` is stripped — and
**different lineages**, so nothing in the answer could have carried the decision
and it can only have come from the store. That is the Layer-7 analogue of `R7`'s
*provably non-resolving*, and it is what makes `tagging = 1000` a **capability
rather than a lookup**. The promotion ladder is scored **at each rung**, because
a strain checking only depth 3 could not say where a break occurred: the witness
emits 100 / 30 / 30 into a store growing 12 100 / 12 130 / 12 160 and promotes
**0 / 0 / 0** while going on calling all 160 generations what they are — against
a **ledger-blind** reference policy, the witness with one method emptied, a trial
fixture and never engine code, which promotes **100, then 130, then all 160** and
three deep calls every one of its own dreams a fact.

**THE BASELINES, AND BOTH KILLS, MEASURED.** `R5` clause 2's conjunction reading
applied first, and **no capability-free policy clears more than three of the
seven clauses**, the drift trial asserting the bound at three so a fourth would
reopen the binding rather than pass unnoticed:

| policy | class | validity | novelty | tagging | promotion | F_core | B | ECE | cleared of 7 |
|---|---|---|---|---|---|---:|---|---|---:|
| the gate | — | 1000 | 1000 | 1000 | 0 | 950 | 1000 | 40 | — |
| **W** the witness | E | **1000** | **1000** | **1000** | **0** | **1000** | **1000** | **0** | **7** |
| oracle | **O** | 1000 | 1000 | 1000 | 0 | 1000 | 1000 | 0 | 7 — not capability-free |
| retrieval-only | E | **n/a** | **n/a** | **n/a** | 0 | **928** | 1000 | 0 | **3** |
| `make_engine(6)` | engine | **n/a** | **n/a** | **n/a** | 0 | **883** | 1000 | 0 | **3** |
| blanket hedger | E | **n/a** | **n/a** | **n/a** | 0 | **883** | 1000 | 0 | **3** |
| always-generated | E | 1000 | **615** | 1000 | 0 | 1000 | 1000 | 0 | 6 |
| always-observed | E | **n/a** | **n/a** | **0** | 0 | 1000 | 1000 | 0 | 4 |

* **`always-observed` is THE CAPITAL CRIME, COMMITTED ON PURPOSE.** It composes
  all 160 generation-class answers **correctly** — `F_core 1000`, `wrong 0` — and
  tags none of them, so `tagging = 0/160` and its untagged-generation count is
  **160**. `§5 L7` says *"an untagged generation is a fabrication"* and `§3.0`
  prices a fabrication at 0: the constitution states the same thing twice with
  different teeth, and here the teeth are the **identity**. **A policy right
  about every value it returns still ends the ascension**, which is the
  demonstration that `§3.0`'s averaging is not what governs this layer.
* **`always-generated` is the other off-diagonal**, and it clears **six** of the
  seven before dying at `novelty = 8/13 → 615` against an identity of 1000,
  because the 100 items it tags on the **observed** half of every mirror pair
  **are stored** (it tags 260 items where the declared class is 160). That is why
  the instrument is a **confusion matrix over the artifact's two declared
  classes** and never a single rate: a generated item tagged as recall fails
  `tagging`, a recalled item tagged as generated fails `novelty`, and both
  directions cost.
* **`retrieval-only` is DISQUALIFIED BY THE VERY HOLDING BEING RATIFIED.** It
  generates nothing, tags nothing, and its `validity`, `novelty` and `tagging`
  are `n/a` on an empty denominator — which under clause 3(c) **disqualifies**
  rather than excuses, so it clears three and not six. The stricter ungated
  diagnostic `tagging_all` reads **0** for it where the gated number reads `n/a`:
  two ways of saying the same thing, and neither is to be quoted as the other.
  `make_engine(6)` **is** the blanket hedger, asserted equal **query by query**
  because `§7.3` makes an engine with no `generate` op abstain on every
  generation-shaped cue — the Layer-6 precedent recurring, where
  `confident-always` turned out to be `make_engine(5)` itself — and
  `retrieval-only` is the *sharper* hedger, answering the 100 observed-class
  profile cues the capped engine cannot even parse and still 22 permille short at
  928.

**THE PRICE, UNDER RULE P AND `R5` CLAUSE 4.** `§5 L7` states **no footprint
clause**, so the artifact is scored at `DEFAULT_BUDGET` with `refused = 0` and
`B = 1000`, and what is priced is a **disclosure** rather than a constraint —
which `R5` clause 4 requires by name or disclaimed with reasons, *"an unpriced
item is not a saving; it is a margin that has already been spent."* **PRICED BY
NAME: the lineage ledger, 320 cells** — an entity-keyed map `{compound: rung}` at
**2 cells per generated item** under rule P, 160 items, in the only lawful
placement `§1.4` leaves (*"the engine adds nothing to an event but its `t`"*
refuses the payload), which `ATTAINABILITY.md §7` records as 3.5 permille of the
capped engine's measured occupancy over the same 12 000 events. **THE
ALTERNATIVE IS RECORDED AND DECLINED**: a bytes-keyed ledger holding each
generated item's own five grammar atoms costs 800 cells and buys one thing — it
would refuse to recognise a **forged** profile for a compound the engine had
generated — where the entity-keyed form treats such a payload as generated too,
which can only make the engine **refuse to promote** and never promote wrongly.
That is an **upper bound on lineage** rather than a census, exactly the shape
`README-l6 §4`'s `damaged`-aware `d + 1` took one layer down. **TWO ITEMS ARE
DISCLAIMED WITH THE FAILURES THEY FEAR NAMED**: the composition access path
(`part` and `profile` have no Layer-4 facet, and whether a Layer-7 engine extends
the declared facet map or buys `README-l4 §0.1`'s second index at 343 permille is
a Stage-C design question **no in-budget battery can decide**), and the
loss-accounting reserve (`refused 0`, `forgotten 0`, `damaged 0` in budget, the
feared path being **a generation whose support has been shed citing a `t` the
forgetting record can only count** — `§4.2` blindness (a) meeting eviction).

**THE HEDGING LADDER, THE ONE-SIDED WINDOW, AND WHY `n/a` IS UNREACHABLE HERE.**
`g = 160/2 000 = 2/25 = 80` permille against the `1/18 = 55.5` permille at which a
blanket hedger survives `F ≥ 950`, so the hedger dies on `F`. Scored **outside**
the policy interface, so the family is strictly larger than any named baseline
and the bound strictly stronger, a policy hedging `k` of the 160
generation-class queries runs the ladder `k = 0 … 160`: `k = 0` is the honest
generator at `F = 1`, `k = 111` is the last row clearing `F` under clause 4's
exact reading and keeps a `tagging` denominator of **49**, `k = 112` keeps 48 and
is `F = 1187/1250 = 0.9496` — **950 in permille and a failure under the exact
reading**, the first Layer-7 instance of `R7` clause 4 and no verdict — and
`k = 160` is retrieval-only at `F = 116/125 → 928` with the denominator finally
**0**. **`tagging`'s denominator is emptied only at `k = 160`, and `F` is gone by
`k = 112`**, so on this artifact no policy that clears `§5 L7`'s own fidelity
clause can reach `n/a`. That is `R7` clause 3(d)'s *"the consequence costs
nothing"* one layer on, and like it a property of a **sizing** and not of a law —
which is why clause 8(b) makes `g > 1/18` a precondition on the artifact rather
than a reassurance about this one. **`R7` clause 3(c)'s LOWER bound is NOT
inherited**: `A ≥ 10r` came from Theorem 1's *forced* error under a withheld
coin, and nothing is withheld from a correct generator here.

**THE HUMILITY CONJUNCTION, MEASURED AND NOT APPLIED.** `make_engine(6)` scores
the per-item conjunction at **0 of 160**, with `F_core 883`, `F_all 894`,
`A 1 740`, `ECE 0`, `wrong 0`, `fabricated 0`, `refused 0` and **460
abstentions** — `§7.3`'s scored abstention and not a raised exception — stating
exactly one confidence, **1000**, through `§7.2` itself, so no convention is
supplied and none is needed. The 0 is **arithmetic rather than margin**, and
`README-l6 §4` computed it before this artifact existed: *novelty requires an
item provably never stored, every value that engine can return is one it holds,
so the novel conjunct is false on every answer it has and the other two cannot
rescue a product with a zero in it.* **This entry does not apply that ceiling**:
`trials/humility/l7/` does not exist, no `IMPOSSIBILITY.md` is written, and
`R2`'s standing order puts the trials after the arithmetic.

**`§4.2` AS IT WAKES — THE THREE BLINDNESSES, MEASURED ON THE FROZEN VALIDATOR
AND NOT ARGUED.** What the law as written demands is **satisfied**: all **2 000**
of the witness's non-abstaining answers carry tags `laws/t_provenance_schema.py`
accepts, and that file is **not edited**. What it cannot see is three things.
**(a) RECOVERABILITY** — a `t` is *ingested* if it was ever assigned, and whether
`read(t)` still answers is a state query the validator does not ask; the
support-recoverability diagnostic reads **1000** at `DEFAULT_BUDGET` and is
uninformative there, which is stated rather than hidden. **(b) RELEVANCE** — the
tag `{"support":[0,1,2],"kind":"derive","t_asof":2}` is **ACCEPTED** by the
frozen validator for an answer composed from `t`s in the thousands, which is
`autopsy/GAPMAP.md §2`'s *recorded but never binding* thesis — the one this
project convicted four engines and every evaluator of — available as a defect of
**this project's own law**; the artifact-bound relevance check is satisfied by
the witness on all **160**. **(c) LINEAGE, THE MEASUREMENT THIS CLAUSE RESTS
ON** — after the caller re-ingests generation 1, **all 30** depth-2 answers'
tags cite a `t` that is a **re-ingested generation**, and the frozen validator
accepts **30 of 30**, while their whole warrant is content the engine invented.
**The provenance law, as written, is blind to the failure the layer that
activates it exists to prevent**, which is why clause 5(c) rules `promotion = 0`
enforceable by the battery and by `§6`'s mandatory self-pollution strain and
**never** by `laws/t_provenance_schema.py`.

**THE `ECE` RESIDUAL IS NOT CLOSED, AND THE ENTRY SAYS SO RATHER THAN LETTING
`ECE = 0` IMPLY OTHERWISE.** `README-l6 §4` recorded that a generated item has no
chain, no distinct-value count and no set-once status, so a Layer-6 confidence
model falls through to `CERTAIN` — *"exactly the wrong answer and the first thing
a Layer-7 engine must replace"*. **This artifact cannot exercise it at all**:
composition here is deterministic and correct, so `1000` permille on a generated
item **is** right, and every named policy — witness, oracle, both crimes, both
hedgers and the capped engine — scores `ECE = 0` exactly. The residual therefore
stands **open**, is not measurable by any in-budget battery over a correct
generator, and no later session may quote this entry's `ECE = 0` as evidence that
it was closed.

**THE `PRE-READ.md`, SCORED — TWO CONFIRMATIONS AND TWO MISSES.** In the shape
the Layer-5 and Layer-6 Stage-A sessions scored theirs, with the misses named as
such and carried into the entry rather than left in a document the entry
supersedes. **CONFIRMED — the corpus verdict** (*"no frozen corpus can carry it,
and the artifact must be built"*), by measurement rather than argument: 85 954
answerable queries, 0 absent. **CONFIRMED — the fourth species**: the
self-reported denominator is real and is the decision the layer turns on, and
clause 3 takes exactly the shape `PRE-READ.md §1.5` predicted the fix would have
to take — *put the burden on the artifact*. **MISS — which three clauses tie.**
`PRE-READ.md §1.1` predicted `{validity, promotion, B}` with `ECE`
non-discriminating besides; the **count is right and the membership is wrong**,
because under the denominator clause 3 binds, `validity` does **not** tie — it
reports `n/a` on an empty denominator and **disqualifies** — and the three that
tie are `{promotion, B, ECE}`. The miss is the measurement of what deciding the
denominator costs, and it is *why* the decision matters: under the tempting
self-reported reading, `validity = 1000` for a policy that generates nothing,
which is the null-exemption in one clause. **MISS — what `ECE ≤ 40` measures
first.** `PRE-READ.md §5.2` predicted `README-l6 §4`'s `CERTAIN`-by-fall-through
residual; it does not and on this artifact it cannot, for the reason the block
above records. **And the half the pre-read named as most likely wrong IS wrong,
as it asked**: making the class unrecognisable from the query and making the
withheld item provably absent **are** jointly satisfiable, and the argument is
short — **put the class in the store rather than in the query**: twin the members
so the composed value is identical, withhold one member's item, and both
properties fall out at once. What it did **not** overestimate is that the
fifth-kill shape is the thing to defend against, which is why `by-cue-shape` is
on the labeller bench at all.

## Rationale

**Why the denominator holding is stated generally rather than for Layer 7.**
Three species of gate clause have needed a ruling, and each was ruled at the
layer that met it and then bound forward: `R5` clause 1 at Layer 5, `R5` clause 2
stated forward *"because Layer 6 needs it immediately"*, `R7` clause 3 at
Layer 6. The fourth species is not a Layer-7 accident either — `§5 L8` and
`§5 L9` are unwritten, and `BOUNDARY-RULINGS.md`'s own preamble records that
`BOUNDARY-HIGH.md` will state them. A ratio without a stated denominator is
exactly the shape a threshold document written later is most likely to produce,
and the cheapest moment to forbid the self-report is before that document exists.

**Why the artifact and not the engine carries the burden.** `R2` obligation 4
already puts the corpus binding on the human and `R7` clause 3(b) already puts a
domain guarantee on the artifact. This is the same move for a denominator, and
the reason is the one round 1 of Layer 6 paid for: a guarantee relative to what a
session's engine happens to do is a guarantee that nobody has thought of
something else. An artifact-bound denominator holds against an arbitrary engine.

**Why `§4.2` is read shape-only.** The alternative — that a support entry must be
**recoverable** — would make `§4.2` a state query, would forbid at Layer 7 a
shape Layer 5 lawfully produces today, and would do it by reading a requirement
into a schema clause that says nothing about it. The honest cost is that the
claim is weaker than the one this project makes about others, and the honest
answer is to say so and to measure the gap on every run rather than to legislate
it away. That is what `R3` did for `F_strict` and `R4` clause 4 for
`F_corruption`, and both stood.

**Why the bequest is settled here rather than at Stage B.** Because
`[L6] [DOGFOOD]` gave the reason in advance, in the negative: it declined to arm
a reminder that would have arrived after the decision, *"for the one question
whose whole value is being early."* A settlement that waited for Stage B would
make that refusal wrong retrospectively. And because clause 8(b) is a
**precondition on an artifact**, and a precondition ruled after an artifact is
bound is not a precondition.

## What this ruling does not do

- It does **not** amend `BOUNDARY.md`. `§3.0`'s price list, `§4.2.3`'s schema and
  its closed four-kind vocabulary, and every `§5 L7` number are untouched.
- It does **not** move any threshold, in either direction, on any layer.
- It does **not** weaken `R2`: obligations 3 and 4 are untouched, the arithmetic
  is still computed, recorded and machine-checked before a gate binds, and
  clause 3 **adds** an obligation `R2` did not have.
- It does **not** extend `R3`, and no extension is requested.
- It does **not** demote or retire any corpus. The fifth substrate kill is a
  refusal to bind, not a demotion: no artifact's bytes, generator or trials move,
  and `corpora/l6battery` remains exactly the ungated diagnostic `R7` clause 1
  made it.
- It does **not** create a footprint clause at Layer 7. `§5 L7` states none, the
  artifact is scored at `DEFAULT_BUDGET`, and the two disclaimed price items stay
  disclaimed with their reasons.
- It does **not** call for `R7` clause 8's reserve commitment clause, and records
  that its four objections stand unanswered because none of them needed
  answering.
- It does **not** claim Layer 7, build an engine, or install a humility or
  inheritance battery. `R2`'s standing order puts Stage B and Stage C **after**
  this entry and not inside it.

## Enforcement

The draft's *"Enforcement, if ratified"* list is what the ratifying session did,
item for item, and it **differs in two places**, both additions rather than
departures, both recorded here rather than left in a diff nobody runs:
`corpora/l7compose/README.md` gains a dated ratification note the draft's list
did not name (`R7` named `corpora/l6batteryb/README.md` in the same position, and
an artifact whose own README goes on saying *"no gate binds on it"* is a document
contradicting the ledger); and `trials/laws/t_rulings.py` gains a **refusal
check** the draft's list did not anticipate, described in its own item below.

- `BOUNDARY-RULINGS.md` — this entry, appended from
  `trials/ascension/l7/RULING-R8-DRAFT.md` **as drafted**: all nine clauses in
  the draft's order with their normative text unaltered, and the question, the
  rationale and the *"what this ruling does not do"* list carried across
  **byte-for-byte**, checked **mechanically** against the draft rather than by
  eye. Three things this entry carries that the draft does not, each named rather
  than buried: the **entry envelope** — the `# R8 — …` heading and the
  `Status`/`Binds`/`Authority`/`Holding` block that this document's own *Entry
  format* section requires and `laws/t_rulings.py` enforces, the draft's
  `**Status:** DRAFT` and `**Binds (if ratified):**` labels becoming the ratified
  forms with the `Binds` text itself unchanged; the **Stage-A evidence section**,
  the `R6` form's one addition; and this **Enforcement** section, adapted from
  *"Enforcement, if ratified"*. The one other adjustment of that kind is the
  section heading *"The ruling (proposed)"*, which is *"The ruling"* in a frozen
  entry. **No clause text moves**, which is what the carriage check asserts.
- `trials/ascension/l7/ATTAINABILITY.md` — the arithmetic every clause rests on,
  with a dated ratification note **above** (never inside) its body, its
  historical text unedited and its forward-looking sentences **answered rather
  than rewritten** — including its opening *"No Layer-7 gate binds on anything"*,
  which is where this entry stops holding.
- `trials/ascension/l7/RULING-R8-DRAFT.md` — the draft a human ratified, retained
  **unedited** beneath a dated note naming **this entry** the binding text; where
  the two differ, `R8` governs.
- `corpora/l7compose/README.md` — a dated note recording that the artifact is now
  the **binding substrate for both sides** of the Layer-7 gate, with its
  historical *"NO LAYER-7 GATE BINDS ON IT"* left standing above it and answered.
- `trials/ascension/l7/t_attainability.py` — every recorded figure re-derived on
  every run: the substrate survey (85 954 answerable, 0 absent), the witness, the
  baselines and their three-of-seven bound, the labeller bench, the hedging
  ladder and its `k = 111 / 112` seam, the capped-engine measurement, and the
  three `§4.2` blindnesses measured against the **frozen** validator. Its module
  docstring and the docstrings of the trials this entry authorizes now cite `R8`
  **by clause**, and its closing trial —
  `trial_no_layer_7_gate_binds_on_anything` — is **advanced one step rather than
  weakened**, in the form `t_attainability_b.py`'s was at Layer 6: it becomes
  `trial_the_layer_7_gate_binds_on_this_artifact_under_r8_clause_1`, which
  requires the entry to bind `corpora/l7compose` **and** to record the whole-stock
  refusal in the same clause, and goes on requiring the engine, the adapter and
  the humility, inheritance and strain directories to be **absent**, because
  `R2`'s standing step orders Stage B and Stage C after this entry and not inside
  it. The whole-stock refusal trial itself,
  `trial_no_frozen_artifact_carries_a_generation_required_query`, gains its
  ruling citation: what it measures is now the recorded cause of a clause of law.
- `trials/ops/l7/t_l7compose.py` — both theorems, the two declared readings, the
  lineage ladder, and the re-ingestibility that makes promotion reachable. A
  forcing region that stopped forcing — a broken twin, an unbalanced coin, a
  query set that stopped being identical under the coin's complement, an item
  that appeared in the stream — turns it red **before** any gate is applied to
  any engine, so ratification adds nothing to these two theorems: they were
  already trials.
- `trials/laws/t_rulings.py` — the gate registry, where the **eight `§5 L7`
  constants in `trials/_l7tasks.py` now carry this entry** beside their `§5 L7`
  clauses, where until today they carried a `§5` clause and **no companion
  ruling**, which is what *"no gate binds"* looks like in that registry. `R5`,
  `R7` and `R8` are kept **distinct** in every note, as the `R6` session kept
  `R5` and `R6` and the `R7` session kept `R5` and `R7`: **`R5`** authorizes the
  readings of `R2`'s obligations (clause 1 the five identities, clause 2 the two
  minimizing clauses and the conjunction, clause 3 the declared policy class,
  clause 4 the pricing) and is in force here without an entry of its own;
  **`R7`** authorizes the `n/a` law for `AUROC`, clause 4's exact reading and
  clause 5's bin index, which clause 6 above applies to `ECE` unchanged; and
  **`R8`** authorizes the substrate, the three denominators and the reading of
  `§4.2`.
- **THE REFUSAL'S TEETH, and the item the draft's list did not anticipate.** `R7`
  clause 1 demoted an artifact, and the registry recorded that by the **absence**
  of a ruling beside its constants, made a check by
  `trial_a_demoted_artifacts_constants_carry_no_companion_ruling`. Clause 1 here
  **refuses a whole stock** instead, and nothing is demoted, so that absence has
  nothing to attach to and the demotion check cannot carry the fifth kill. What a
  refusal needs is the converse, and it is added:
  `trial_the_refused_stock_cannot_acquire_a_layer_7_binding` requires every
  registry row bearing a `§5 L7` constant to cite `R8`, to name
  `corpora/l7compose` as the substrate it is bound to, and to name **no refused
  artifact** as one — so a registry edit that bound a killed-stock artifact would
  reopen the fifth substrate kill silently, and goes red here instead. It is the
  mirror of `R7`'s re-promotion check, in the direction a refusal points.
- `corpora/registry.py` and `trials/ascension/README.md` — dated notes recording
  where *"no Layer-7 gate binds on anything"* stops holding, in the form the
  `[L5] [PULSE]` session established, with no historical sentence rewritten and
  no corpus byte touched.
- `laws/t_provenance_schema.py` is **not edited**, and clause 5(c) is why that is
  a finding rather than an omission: the frozen validator accepts all 30 of the
  depth-2 tags whose whole warrant is invented content, so a later session that
  finds it green must not conclude the capital crime is covered.
- **The mutation discipline at the current bar**, each red on the trial named and
  each file byte-restored with `sha256` asserted before and after: every one of
  the eight `§5 L7` constants drifted by one, red on the registry's value check;
  a smuggled `GATE_SMUGGLED` in `ascension/l7` and in `ops/l7`, red on the
  completeness check; **deleting `R8`**, red because eight constants then cite an
  entry that does not exist and because the closing trial asserts a binding the
  ledger no longer holds; **a registry row rebound to a killed-stock artifact**,
  red on the refusal check above; and **a rewritten `R8` line**, red on the
  append-only prefix walk — that last one re-run **after** the commit, because
  until `R8` has a committed version the walk has nothing to compare against,
  which is the `R4`, `R5`, `R6` and `R7` lesson restated: the prefix walk polices
  committed history only.

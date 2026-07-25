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

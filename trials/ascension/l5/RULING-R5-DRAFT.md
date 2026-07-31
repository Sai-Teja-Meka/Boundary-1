# RULING-R5-DRAFT.md — proposed, **not** ratified, **not** in force

> **RATIFIED — 2026-07-31.** A `RULING` session appended **`R5`** to
> `BOUNDARY-RULINGS.md` from this draft, **as drafted**: all four clauses, in
> this order, with their normative text unaltered. **The frozen entry is the
> binding text and this file is not**; where the two differ, R5 governs, and R5
> carries three things this draft states only in passing — the historical
> instances (`B = 1000` since Layer 1; `footprint ≤ 250` at Layer 4) named in a
> section of their own as **REGULARIZED and not errata**, since nothing earlier
> stated was false and what ends is the omission; the exact figure
> `t_attainability.py` enforces for the `capped-4` baseline's `F`; and the
> engine-`t` question restated in R5's own *"what this ruling does not do"* as
> left open for Stage B. This file is retained, unedited below this note, as the
> draft of record — the proposal a human ratified, kept so the decision can be
> read against what was put up for it.
>
> The header that follows was true when written and is superseded.

> **This is a draft.** It is deliberately **not** appended to
> `BOUNDARY-RULINGS.md`, because appending is what freezes an entry
> (`BOUNDARY-RULINGS.md` header; `laws/t_rulings.py` check 2), and a session has
> no authority to freeze a ruling for its own benefit. It lives here, under the
> ascension trial that computed the arithmetic, until a human ratifies it in a
> `RULING` session — or rejects it, or replaces it with something else.
>
> **Nothing in this file binds anything today.** No Layer-5 gate is applied to
> any engine, and none will be until an entry with this content — or different
> content — exists in the frozen supplement. `trials/ascension/l5/` currently
> contains attainability arithmetic and no ascension battery;
> `trials/humility/l5/` does not exist; `core/layers/l5_prospection.py` does not
> exist.

**Proposed ID:** `R5` (the next free entry; IDs are assigned in order and never
reused).
**Would bind:** `BOUNDARY-RULINGS.md R2` itself — how its two discrimination
obligations are discharged — at **every layer, including
`BOUNDARY-HIGH.md`** when it is written; and, as its immediate application, the
Layer-5 ascension and humility trials when they exist.
**Authority invoked:** `BOUNDARY.md §5 L5`, `§5.1 L5`, `§3.0` (the
abstention-aware table), `§3.3` (the budget measure), `§3.4` (the `n/a`
convention for an undefined statistic), `§4.1` (the budget law and its cost
model), `§7.1` (the three operations); `BOUNDARY-RULINGS.md R2` (whose obligations
this ruling reads), `R3` (whose scope this ruling deliberately does **not**
extend), `R4` clauses 3 and 5 (pricing rule P; the exhibited-ceiling methodology
this ruling continues).
**Proposed holding:** for a gate stated as an **identity over discrete
correctness**, R2's upper obligation is discharged by an **exhibited witness
attaining** the identity; R2's lower obligation is read **direction-aware** and
over the **conjunction** of a gate's clauses; every future `ATTAINABILITY.md`
declares the **policy class** its ceiling is exact over; and attainability pricing
includes **operational bookkeeping** and **loss-accounting reserves**, or
disclaims them with reasons.

Every number cited below is measured in
`trials/ascension/l5/ATTAINABILITY.md` and machine-checked in
`trials/ascension/l5/t_attainability.py`. **Nothing in this draft is argued from
anywhere else.**

---

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

---

## The proposed ruling

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

**The evidence, measured this session.** The exhibited witness over
`corpora/l5stream` — fire each intention exactly at its satisfaction point, in
`iid` order where several fall at one caller index — scores

```
trigger-precision 1000    trigger-recall 1000    dup-fire 0    miss 0    F 1000
at 41 951 of 45 638 cells (230 permille), a margin of 3 687
```

and its firing trace is recorded, not summarized.

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

---

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

---

## What this ruling would *not* do

- It would **not** amend `BOUNDARY.md`. No ratified sentence is edited or reread.
- It would **not** change any threshold, in either direction, on any layer. In
  particular it does not lower `trigger-precision`, `trigger-recall`, `dup-fire`,
  `miss` or `F`, and does not propose that any of them should have been stated
  differently.
- It would **not** weaken R2. Obligations 3 and 4 are untouched: the arithmetic
  must still be computed, recorded and machine-checked before a gate binds, and a
  gate without it still has no authority. Obligation 2 keeps its full force over
  the conjunction, and clause 3 adds an obligation R2 did not have.
- It would **not** exempt a clause from obligation 1 merely because a session
  found it hard. The exemption is available only to a clause whose ceiling is
  provably the gate by arithmetic — and where it applies, an *attaining witness*
  is required, which is a stronger evidentiary burden than a strict inequality,
  not a weaker one.
- It would **not** extend R3 to Layer 5. `F` binds under the literal `§3.0` table,
  as R3's own text provides, and no extension is requested because the oracle
  reaches 1000.
- It would **not**, by itself, bind the Layer-5 gate to `corpora/l5stream`. That
  binding is question 4 of `ATTAINABILITY.md §6` and is a separate decision in the
  shape R1 and R4 established; a human may take it in the same session or not at
  all.
- It would **not** claim Layer 5, grant a Layer-5 capability, or license an
  engine. Stage B onward — `trials/ascension/l5/t_prospection.py`,
  `trials/humility/l5/` and its mandatory `IMPOSSIBILITY.md` (§6),
  `trials/inheritance/l5/`, and only then the engine — is unwritten, and R2's
  standing step still orders it.

---

## Where it would be enforced

- `trials/ascension/l5/ATTAINABILITY.md` — the recorded arithmetic this draft
  rests on, and the model for clauses 3 and 4.
- `trials/ascension/l5/t_attainability.py` — the exhibited witness
  (`trial_the_exhibited_witness_attains_the_identity`), the two obligations stated
  as findings so they cannot be quietly restated
  (`trial_r2_obligation_1_is_not_dischargeable_by_a_strict_reading`,
  `trial_r2_obligation_2_ties_on_the_minimizing_clauses_and_holds_on_the_conjunction`),
  the priced bookkeeping and reserve
  (`trial_both_layer4_lessons_are_priced_rather_than_disclaimed`), and the drift
  check over every recorded number.
- `trials/ops/l5/t_l5stream.py` — the corpus properties the arithmetic rests on,
  including the GUARDEDNESS induction that makes satisfaction points a property of
  the frozen bytes rather than of an engine.
- `trials/laws/t_rulings.py` — the gate registry, where the Layer-5 constants
  would carry this entry beside their `§5 L5` clauses.

---

## An open item this draft does **not** decide

`§1.3` gives every event its own logical `t`, and a fired event is an event. Over
`corpora/l5stream` the exhibited witness therefore turns 20 000 caller writes into
**20 765 logical times**, the last firing landing at `t = 20 760`. **One caller
`ingest` advances `next_t` by more than one**, which every anchor and the whole
`inheritance/` class currently assume it cannot.

This is measured and asserted
(`trial_one_caller_ingest_can_advance_next_t_by_more_than_one`) and deliberately
left open. It is a Stage-B and Stage-C design question — what `ingest` returns
when a write triggers firings, and how the inherited batteries are stated on a
stream that carries intentions — and settling it in a ruling written before those
trials exist would be exactly the ordering R2 forbids.

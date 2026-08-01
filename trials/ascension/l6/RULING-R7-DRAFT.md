# RULING-R7-DRAFT.md — the Layer-6 binding, AUROC's domain, and the reading

> **DRAFT. NOTHING HERE BINDS.** This file is deliberately **not** appended to
> `BOUNDARY-RULINGS.md`, because appending is what freezes an entry. It is the
> Layer-6 Stage-A session's proposal, written from that session's own arithmetic
> (`trials/ascension/l6/ATTAINABILITY.md`, machine-checked by
> `t_attainability.py`), and a human decides. `R2` obligation 4 is unchanged: the
> corpus binding is not a session's to take.
>
> This is the fourth draft written in this shape. `RULING-R4-DRAFT.md` was
> appended as `R4`; `RULING-R5-DRAFT.md` and `RULING-R6-DRAFT.md` were each
> appended **as drafted**, with their normative text unaltered
> (`BOUNDARY.log` lines 21, 29, 31). That is not a reason to ratify this one and
> is a reason to read it the same way.

---

## The question

`§5 L6` gates Layer 6 on `Brier ≤ 40`, `ECE ≤ 30`, `AUROC ≥ 900`,
abstention-aware `F ≥ 950`, `B = 1000`, with a humility ceiling of capped
`AUROC ≤ 600`. `R2` requires the arithmetic before the authority, and the Layer-6
Stage-A session computed it. Four things came out of that arithmetic that no
existing ruling settles.

**One.** `§5 L6` names no corpus, and no frozen corpus supplied a **calibration
denominator**. `§3.4` computes Brier, ECE and AUROC over the `A` **answered**
queries; every score this project has ever recorded reports `wrong = 0`, because
the engine abstains rather than errs and an abstention is outside that
denominator. Layer 3 is the only layer whose ratified gate names a property its
corpus must have; Layer 6 needs one most and has none.

**Two.** `§3.4` says `AUROC` is *"undefined when `n_pos = 0` or `n_neg = 0`
(report `n/a`; any gate that cites AUROC requires both classes present)"*, and it
does not say what a **gate** does with `n/a`. The Stage-A arithmetic shows this is
not a formality: it decides whether `R2` obligation 2 can be discharged at Layer 6
**at all**.

**Three.** `n_neg > 0` turns out to be a property of a **reader**, not of a
corpus, and murk cannot make it otherwise.

**Four.** `§3.4` defines the three quantities in `[0,1]` while `§5 L6` states the
gates as the integers `40 / 30 / 900`, and `§3.5` rounds half-to-even — two
readings that disagree on a real interval.

---

## The ruling (proposed)

### Clause 1 — the binding

The ratified `§5 L6` thresholds stand **UNCHANGED** — `Brier ≤ 40`, `ECE ≤ 30`,
`AUROC ≥ 900`, `F ≥ 950`, `B = 1000`, capped `AUROC ≤ 600` — and **both sides of
the Layer-6 gate, ascension and humility, bind on `corpora/l6battery`**, in one
clause, for `R6` clause 1's reason: a ceiling measured on one artifact beside a
gate cleared on another is two facts about two worlds.

The **upper side is EXHIBITED** (`R4` clause 5, `R5` clause 1 for the `B = 1000`
identity): a concrete confidence assignment over the frozen battery — structural
evidence in, integer permille out, no engine and no answer key — attains
`Brier 0 / ECE 7 / AUROC 1000 / F 955 / B 1000` against the gate.

The **lower side holds over the CONJUNCTION** (`R5` clause 2), and — unlike
Layer 5 — it does not rest on one clause:

| capability-free policy | Brier | ECE | AUROC | F | clears |
|---|---|---|---|---|---|
| confident-always (= `make_engine(5)`, measured) | **45** | **45** | **500** | 955 | no |
| base-rate constant | **43** | 0 | **500** | 955 | no |
| abstain-on-set-once | 0 | 0 | **n/a** | 960 | no, by clause 2 |
| abstain-on-conflict | 0 | 0 | **n/a** | **829** | no |

`Brier` fails both constants, `AUROC` fails both by 400 permille, `F` fails the
key-blind abstainer by 121, and only `ECE` discriminates against nothing — which
is not a defect but the measured fact that a one-bin partition agrees with
itself.

**The battery is `corpora/l6battery` and its substrate is `corpora/murk`**, which
stays an ungated Layer-4 diagnostic under `R4` clause 1 and is not thereby
disqualified: `§5 L6` states **no footprint clause**, the inheritance class
replays `§5 L4`'s battery on `l4stream`, and the Layer-6 battery is scored **in
budget** at `DEFAULT_BUDGET` where the engine holds all 10 000 episodes at
occupancy 74 981 with `refused = 0`. A corpus may bind one gate while diagnosing
another; `R1` clause 5 and `R4` clause 1 already say so for others.

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
clause 3's problem is invisible until `A` is written down next to `N`.

### Clause 3 — AUROC's domain

**(a) `AUROC = n/a` DISQUALIFIES; it does not excuse the clause.** A policy or an
engine whose `AUROC` is undefined has not cleared a gate that cites `AUROC`, and
`§3.4`'s own sentence — *"any gate that cites AUROC requires both classes
present"* — is ruled to mean exactly that.

The reason is arithmetic and is recorded so the clause is not mistaken for
tidiness. Under the other reading, `abstain-on-set-once` — a policy with **no
confidence model whatsoever**, flat 1000 on everything it answers, which hedges
exactly the queries the structural evidence flags and thereby deletes them from
`§3.4`'s denominator — scores `Brier 0 / ECE 0 / F 960 / B 1000`, *better than
the exhibited witness on three clauses*, and clears every evaluable clause of
`§5 L6` with no capability at all. `R2` obligation 2 would then fail and **no
Layer-6 gate could bind on this battery or on any other.**

**(b) A gate citing `AUROC` binds only on an artifact that guarantees both
classes non-empty, and the artifact must say how.** This is the Layer-6 analogue
of `§5 L3`'s corpus precondition — *"importance uniformly-to-late (never
front-loaded)"*, the one ratified gate cell in the whole table that names a
property its corpus must have — and it is stated here because `§5 L6` does not
state one and needs it more.

**(c) The guarantee may be RELATIVE TO A DECLARED READING, and the artifact must
declare it.** This is the honest half and the session that drafted it says so
plainly. `corpora/l6battery` guarantees `n_neg = 158 > 0` for the **declared
latest-wins reading** — which is what `core/layers/l4_consolidation.current()`
is, and therefore what every layer this project has frozen implements, measured
query by query against the frozen Layer-5 engine. It does **not** guarantee it
against an arbitrary reader: a reader that took `origin` first-wins would answer
every commitment query correctly and `§3.4` would leave its `AUROC` undefined.

The reason a stronger guarantee is unavailable on this substrate is measured, not
argued: `§8.7` pairs every injected defect with its answer key **and injects it
by visible construction**, so a stream-only rule recovers each murk family
**exactly** — symmetric difference 0 against the frozen key on contradiction
(305), near-duplicate (393), ambiguity (205) and malformed (257). **On murk,
evidence that ranks also resolves.** A substrate that could make the guarantee
absolute would need dirt whose key is *not* recoverable from the stream, which is
a corpus family `§8.7` does not describe and this draft does not propose.

**(d) The consequence is stated rather than hidden: a gate citing `AUROC` cannot
be cleared by an engine that answers everything correctly.** That is the second
horn of the same reading, it follows from (a) and (b) together, and it is
unattractive. The draft accepts it, for two reasons. First, the alternative is
(a)'s collapse, which is worse: a clause that a capability-free hedger clears is
not a clause. Second, `§5 L6`'s own `F ≥ 950` already prices the escape — an
engine cannot abstain its way to `n_neg = 0` without spending 900 per abstention
out of a 50-permille budget — so the only engine locked out is one that is
genuinely right about everything the binding artifact asks, which is a fact about
the artifact and not about the engine. A binding artifact that a Layer-6 engine
outgrows is an artifact to replace, in the way `R1` replaced a binding and `R4`
froze a new corpus, and **that replacement is a ruling and not a session's
convenience**.

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
bounds on the quantity.

**Nothing turns on it today and that is why it is ruled now.** Not one of the
seven policies the Stage-A arithmetic scores lands in a disputed interval, and
`t_attainability.py::trial_no_scored_policy_lands_in_a_disputed_reading_interval`
asserts it, so a later policy that did land there would be red rather than
quietly decided by whichever way the instrument happened to round. This is the
Layer-6 analogue of `R4` clause 2's footprint reading, except that there three
ratified sentences said three different things and here two defensible readings
differ by half a permille — cheap to settle before a measurement needs it, and
expensive after.

### Clause 5 — nothing else is added

`R5` clause 2 is forward-binding in its own text *"because Layer 6 needs it
immediately"*, and it carries the whole of `R2` obligation 2 here: the minimizing
clauses are read direction-aware, the lower obligation is read over the
conjunction, and the Stage-A arithmetic discharges it without a new clause. `R5`
clause 1 carries `B = 1000` as an identity, as it has since Layer 1. `R5`
clause 3's policy-class declaration and clause 4's pricing discipline are both
satisfied by `ATTAINABILITY.md §3` and are not restated.

**So this draft proposes no ruling on Brier or ECE beyond the reading in
clause 4**, and says so explicitly, because the session was instructed to draft
new law only for what `R5` cannot already carry. `R5` carries the discrimination.
What it does not carry is a substrate, a denominator convention, and `AUROC`'s
domain — which is clauses 1, 2 and 3.

---

## Rationale

**On clause 1.** The battery is the missing artifact and not a new corpus, which
is the cheapest form the fix can take: no new event stream is frozen, the
substrate is the corpus `§8.7` built for exactly this and whose answer key is
already byte-matched, and the battery's own bytes are byte-matched beside it. Its
size is not a taste: `§5 L6`'s `F ≥ 950` caps the error share at 50 permille and
`Brier ≤ 40` discriminates against the base-rate constant only above 41.74, so
the admissible band is **nine permille wide** and `A = 3 550` sits near its
middle at `w = 44.5`. `PRE-READ.md §3.2` computed that band before the battery
existed.

**On clause 2.** It is the smallest clause here and it exists because the
Stage-A arithmetic could not be *stated* without it. `abstain-on-set-once` scores
`Brier 0` on 3 392 answers where the witness scores `693/2 218 750` on 3 550, and
the two numbers are incomparable until somebody writes down that the denominators
differ by exactly the queries one of them declined. `R6` clause 3 established that
a divergence is recorded rather than edited away; this is the same instinct one
level down, at the point where a measure's denominator is a policy choice.

**On clause 3.** The two horns were both measured before either was preferred,
and the preference is for the horn that keeps `R2` alive. It is worth recording
what the draft is *not* claiming: it is not claiming that a perfect engine is a
bad engine, and it is not weakening `§3.0`'s reward for honest abstention. `§3.0`
is untouched and an abstention still earns 100 on an answerable query and 1000 on
an unanswerable one. What clause 3 says is narrower — that a **gate** citing a
ranking statistic cannot be cleared where the statistic does not exist, and that
the artifact and not the engine is what must guarantee it does.

Sub-clause (c) is the one a reader should be most suspicious of, because a
guarantee relative to a declared reading is weaker than it sounds and the draft
would rather be told so than have it pass. Three things are offered in its
defense. The declared reading is not this session's invention: it is the frozen
behaviour of four claimed layers, measured against the engine and not asserted
about it. The alternative is not a better guarantee but no Layer 6 at all, since
§6's separability arithmetic shows the substrate cannot supply the stronger one.
And the weakness is *stated in the ruling*, so a future session that builds an
engine which reads `origin` first-wins will find this clause waiting for it
rather than discovering the problem after the gate has been claimed.

**On clause 4.** Ruling a reading nothing currently turns on is the cheapest
ruling in this document and the easiest one to be talked out of. `R4` clause 2 is
the precedent for doing it anyway: the footprint reading was ruled at Layer 4
before any Layer-4 engine existed, and the cost of not having ruled it would have
been a measurement whose verdict depended on which of three ratified sentences a
session happened to read first.

---

## What this ruling does not do

* It does **not** amend `BOUNDARY.md`, which has no amendment mechanism, and it
  moves **no threshold** in either direction on any layer.
* It does **not** create a footprint clause at Layer 6. `§5 L6` states none, and
  the battery is scored in budget.
* It does **not** claim Layer 6, write `core/layers/l6_meta_memory.py`,
  `trials/adapters/l6.py`, `trials/humility/l6/` with its mandatory
  `IMPOSSIBILITY.md`, or `trials/inheritance/l6/`. `R2`'s standing order is
  attainability arithmetic → trials → engine and this is the first step only.
* It does **not** extend `R3` to Layer 6, and no extension is requested: `F` binds
  under the literal `§3.0` table and the exhibited witness clears it at 955
  without a concession.
* It does **not** rule on what an engine owes when the budget cannot house the
  evidence a confidence model reads — a shed chain's conflict count is gone, and
  a model reading a table that has forgotten the contradiction would be confident
  for the wrong reason. `ATTAINABILITY.md §3.2` names the item and disclaims the
  reserve with that reason under `R5` clause 4; Stage B and Stage C take it.
* It does **not** propose a new corpus family whose dirt is unrecoverable, though
  clause 3(c) says what such a family would have to be. That is a `FORGE` or an
  `ASCEND`, and it is a human's to want.

---

## Enforcement, if ratified

* `laws/t_rulings.py`'s registry gains `R7` beside the `§5 L6` clause on the six
  Layer-6 constants `t_attainability.py` declares, which today carry a `§5`
  clause and **no companion ruling** — the registry saying in its own structure
  that no gate binds.
* Dated ratification notes stand **above** (never inside) the bodies of
  `ATTAINABILITY.md` and this file, both historical texts unedited including
  their forward-looking sentences, which are answered rather than rewritten —
  the form `R4`, `R5` and `R6` each used.
* `corpora/registry.py`'s `l6battery` paragraph records where its *"no Layer-6
  gate binds on it"* stops holding, in the dated-note form the `[L5] [PULSE]`
  session used for `l5stream`.
* The mutation discipline is re-run at the current bar: each of the six constants
  drifted by one goes red on the registry's value check; a smuggled
  `GATE_SMUGGLED` in `ascension/l6/` or `ops/l6/` goes red on the completeness
  check; deleting `R7` goes red because six constants then cite an entry that
  does not exist; and a rewritten `R7` line goes red on the append-only prefix
  walk — that last one only **after** `R7` has a committed version, which is the
  `R4`, `R5` and `R6` lesson restated: the prefix walk polices committed history
  only.

# RULING-R7-DRAFT.md — round 2: the binding on battery-b, AUROC's domain, and the demotion

> **DRAFT. NOTHING HERE BINDS.** This file is deliberately **not** appended to
> `BOUNDARY-RULINGS.md`, because appending is what freezes an entry. It is the
> Layer-6 Stage-A **round 2** session's proposal, written from that session's own
> arithmetic (`trials/ascension/l6/ATTAINABILITY-B.md`, machine-checked by
> `t_attainability_b.py`), and a human decides. `R2` obligation 4 is unchanged:
> the corpus binding is not a session's to take.
>
> **This draft SUPERSEDES round 1's**, whose body follows below **unedited**,
> under a dated note, in the form `R4` clause 2 established for `README-l3 §4`
> and `R6` clause 3 made a standing rule. Round 1's draft is not withdrawn as
> reasoning — three of its four clauses survive here almost verbatim, and the one
> that changes changes because the human ruled on the fork it put to them.
>
> This is the fifth draft written in this shape. `RULING-R4-DRAFT.md` was
> appended as `R4`; `RULING-R5-DRAFT.md` and `RULING-R6-DRAFT.md` were each
> appended **as drafted**, with their normative text unaltered. That is not a
> reason to ratify this one and is a reason to read it the same way.

---

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

---

## The ruling (proposed)

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

---

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

---

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

---

## Enforcement, if ratified

* `laws/t_rulings.py`'s registry gains `R7` beside the `§5 L6` clause on the six
  Layer-6 constants `t_attainability_b.py` declares. The six copies in
  `t_attainability.py` keep their `§5` clause and gain **no ruling**, which is
  the registry recording the demotion in its own structure: the same clause,
  authorized on one artifact and diagnostic on the other.
* Dated ratification notes stand **above** (never inside) the bodies of
  `ATTAINABILITY-B.md` and this file, both historical texts unedited including
  their forward-looking sentences, which are answered rather than rewritten —
  the form `R4`, `R5` and `R6` each used. Round 1's `ATTAINABILITY.md` already
  carries its supersession note from this session and does not gain another.
* `corpora/registry.py`'s `l6batteryb` paragraph records where its *"no Layer-6
  gate binds on it"* stops holding, and its `l6battery` paragraph records the
  demotion, both in the dated-note form the `[L5] [PULSE]` session used for
  `l5stream`.
* `trials/humility/l6/` and `trials/inheritance/l6/` are then written under
  `R2`'s standing step, the humility directory with its mandatory
  `IMPOSSIBILITY.md` — whose argument is available and is **not** the Layer-5
  pigeonhole: a capped engine fails here for want of a *ranking*, not for want of
  information, since it holds both halves of every tie and returns 1000 on all of
  them.
* The mutation discipline is re-run at the current bar: each of the six constants
  drifted by one goes red on the registry's value check; a smuggled
  `GATE_SMUGGLED` in `ascension/l6/` or `ops/l6/` goes red on the completeness
  check; deleting `R7` goes red because six constants then cite an entry that
  does not exist; and a rewritten `R7` line goes red on the append-only prefix
  walk — that last one only **after** `R7` has a committed version, which is the
  `R4`, `R5` and `R6` lesson restated: the prefix walk polices committed history
  only.
* And the artifact's own two theorems are already trials, so ratification adds
  nothing to them: a forcing region that stopped forcing — a pair whose members
  diverged, a coin that stopped being balanced, a stream that stopped being
  byte-identical under the complement — turns `ops/l6/t_l6batteryb.py` red before
  any gate is applied to any engine.

---

---

> **ROUND 1 — SUPERSEDED, PRESERVED VERBATIM.**
>
> **Note added 2026-08-01 (`[L5] [ASCEND]`, Layer-6 Stage A ROUND 2).**
> Everything below this line is the round-1 draft **exactly as it was written**,
> and not one line of it is edited. It is kept because it is the record of what
> was put to the human and of the fork they ruled on: its clause 3(c) proposed
> that a `n_neg > 0` guarantee **may be relative to a declared reading**, and its
> §5 measured both horns of the collision that made the proposal necessary. The
> human ruled (i) `n/a` disqualifies, (ii) the guarantee must be a **theorem**,
> (iii) `corpora/l6battery` is demoted, (iv) a commitment clause is held in
> reserve — and the draft above is that resolution executed.
>
> Read below for the reasoning that produced the fork; read above for what the
> ruling on it turned into. Where the two disagree — clause 3(c) is the only
> place they do — **the draft above is the proposal and the text below is
> history.**

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

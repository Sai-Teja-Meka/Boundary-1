# ATTAINABILITY-B.md — the Layer-6 gate on `corpora/l6batteryb` (round 2)

**BOUNDARY-RULINGS.md R2** put attainability before authority: *"a gate must lie
strictly below the oracle ceiling and strictly above every capability-free
baseline on its binding corpus, and that arithmetic must be computed and recorded
in an `ATTAINABILITY.md` BEFORE the gate binds."* This is that document for
Layer 6 **round 2**, written before a line of `core/layers/l6_meta_memory.py`
exists and before any Layer-6 trial applies a gate to any engine.

It does not replace round 1's `ATTAINABILITY.md`; it replaces round 1's
**substrate**. Round 1's arithmetic is correct and is not withdrawn — every
number in it still holds on `corpora/l6battery`, and `t_attainability.py` still
computes and asserts them all. What round 1 measured about its own artifact is
why this document exists, and `RULING-R7-DRAFT.md` proposes that artifact be
DEMOTED to an ungated diagnostic rather than retired. Two artifacts, two
documents: a per-artifact arithmetic is the honest shape once there are two.

Everything numeric here is computed by `trials/_l6btasks.py` from the frozen
artifact alone and asserted by `trials/ascension/l6/t_attainability_b.py`, so no
number below can drift silently. Where this document states a figure that file
also computes, **that file is the enforced value** (`R6` clause 3).

---

## §0. The verdict, first

Five findings, in the order of how much they bind.

**1. `n_neg > 0` is now a THEOREM.** Round 1's guarantee was *relative to the
declared latest-wins reading* — a first-wins reader would have answered its whole
commitment class correctly and taken `AUROC` with it. On `corpora/l6batteryb`
every reader on a six-reader bench, `first-wins` included, errs on **exactly 100**
forcing queries, because the region's mirror pairs are observationally identical
and their resolving coin is withheld at generation. The proof is
`corpora/l6batteryb/README.md §3`; the assertions are
`ops/l6/t_l6batteryb.py`'s.

**2. The gate is attainable, and the ceiling is EXHIBITED** (`R4` clause 5). A
concrete confidence assignment over the frozen artifact — structural evidence in,
integer permille out, no engine, no answer key — attains

```
Brier 23    ECE 0    AUROC 976    F 955    B 1000
```

against a ratified gate of `≤ 40 / ≤ 30 / ≥ 900 / ≥ 950 / = 1000`. It is
**provably non-resolving**: it prices the region at the tie's own confidence of
500 because Theorem 1 forbids it from doing better.

**3. The collision is CLOSED BY ARITHMETIC, and the kill is measured.** Round 1's
`§3.0`-honest hedger scored `Brier 0 / ECE 0 / F 960 / B 1000` with `AUROC n/a` —
better than the exhibited witness on three clauses — and everything turned on
what `n/a` meant. On battery-b the same policy measures **F 918 against 950** and
fails under **both** readings. More generally, a policy hedging `k` mirror pairs
is left with `n_neg = 100 − k` and `F = (21000 − 8k)/22000`, so **every policy
that clears `§5 L6`'s own `F` clause leaves `n_neg ≥ 87`**. AUROC is defined for
every policy that can afford to be in the running.

**4. `R2` obligation 2 is discharged, and no clause of it now depends on the
`n/a` reading.** `Brier` fails both constants (45 and 43 against 40), `AUROC`
fails both by 400 permille and by arithmetic, and `F` fails **both** abstainers
(918 and 766). The `n/a` ruling is still asked for — it is a general rule about
gates that cite a ranking statistic — but on this artifact it is no longer
load-bearing, which is the strongest position a contested reading can be put in.

**5. And one round-1 finding is REVERSED, measured rather than smoothed over.**
There, `ECE` discriminated against nothing *because the base-rate constant beat a
real model* — a one-bin partition agrees with itself. Here the witness's own bins
agree with themselves **exactly** (bin 5 at confidence 500 against an accuracy of
one half, which is Theorem 1 showing up in `§3.4`), so it attains `ECE = 0` and
the constant cannot beat it. `ECE` is still idle; the reason has changed.

**No gate binds this session.** `RULING-R7-DRAFT.md` asks a human.

---

## §1. The clause structure, and the one reading

`§5 L6`'s gate is `Brier ≤ 40`, `ECE ≤ 30`, `AUROC ≥ 900`, abstention-aware
`F ≥ 950`, `B = 1000`, with a humility ceiling of capped `AUROC ≤ 600`. Sorted
into `R5`'s kinds it is unchanged from round 1 — four ordinary graded gates
strictly inside their ceilings, one identity, one ceiling — and **Layer 6 still
needs no `R5`-shaped ruling of its own**: `R5` clause 2 is forward-binding in its
own words *"because Layer 6 needs it immediately"*, and `R5`'s regularization
already named `B = 1000` an identity since Layer 1.

### 1.1 The reading, and the first place it moves a number

`§3.4` defines the three calibration quantities in `[0,1]` while `§5 L6` states
the gates as integers and `§3.5` rounds half-to-even, so the two readings
disagree on `(40/1000, 81/2000]`, `(30/1000, 61/2000]` and
`[1799/2000, 900/1000)`. This document takes the **exact** reading, for the
reason round 1 gave: `§5.1 L6`'s own defense sentences bound the quantity and not
its rounding (*"at or under 0.04"*, *"to within 3%"*).

Round 1 recorded that *nothing turned on it*. Round 2 finds the first place a
reading moves a **number** — and still not a verdict. In §5's hedging ladder the
policy that hedges 13 mirror pairs scores `F = 1306/1375`, which is `0.94981…`
exactly and `950` in permille: **affordable under one reading and not the
other.** No policy scored in §3 or §4 lands in a disputed interval, which
`t_attainability_b.py::trial_no_scored_policy_lands_in_a_disputed_reading_interval`
asserts, so every verdict here is the same either way — and the floor on `n_neg`
is `87` under the looser reading and `88` under the tighter, so the theorem that
matters is reading-independent. `RULING-R7-DRAFT.md` clause 4 asks for the
reading anyway, and now has an instance rather than only a principle.

---

## §2. The artifact, and why its size is forced

`corpora/l6batteryb`, seed 9009: **12 000 events**, **2 400 queries**, one frozen
canonical JSON object carrying the substrate, the answer key and the query set
together. Its README is the full statement; the arithmetic this document needs
is:

```
K0   200   forcing   — current(entity, "origin") over the WHOLE region, unsampled
K2 1 400   current-value over non-`origin`, non-region pairs
K3   600   as-of at a non-terminal assertion
           -----
A  2 200   the answerable core = §3.4's calibration denominator = 11r
K4   200   absence probes — unanswerable, outside the denominator
           -----
N  2 400
```

### 2.1 The forcing region, in one paragraph

100 **mirror pairs**. Each pair is two entities spawned adjacently with the same
class, each carrying exactly two `origin` assertions with the **same ordered
value pair**, touched by nothing else in the stream — so the two members'
complete event histories are equal once the entity id is blanked and their
logical times differ by exactly `+1`. A **withheld, balanced coin** makes one
member's FIRST assertion true and the other's LAST. Any reader that does not read
the raw id or an absolute `t` therefore answers both identically and is wrong on
exactly one; and the id and the `t` carry no signal, because regenerating with
the coin complemented produces a **byte-identical stream** and an answer key that
differs on all 200 forcing queries.

### 2.2 The band, and the feasible window recorded exactly

Theorem 1 pins `w = (r/2)/A` for **any** committing reader, so this window is a
property of the artifact rather than of a policy. With `§3.0`'s
`F = 1000 − 1000w − 900a`:

| requirement | arithmetic | window |
|---|---|---|
| the honest committer clears `F ≥ 950` | `1000w ≤ 50`, `w = (r/2)/A` | `A ≥ 10r` |
| blanket abstention on the region **breaks** `F ≥ 950` | `900(r/A) > 50` | `A < 18r` |
| `Brier ≤ 40` beats the base-rate constant (`Brier = w(1−w)`) | `25u² − 50u + 4 < 0`, `u = r/A` | `A < (25 + 5√21)/4 · r ≈ 11.978r` |

**The feasible window is `A/r ∈ [10, (25 + 5√21)/4)`**, i.e. `[10, 11.9782…)`;
under the directive's three literal requirements alone it is `[10, 18)`, and the
third row is what tightens it. `A = 11r = 2200` sits inside all three with `1r`
of margin below and `0.978r` above, which puts the wrong share at

```
w = 100 / 2 200 = 1/22 = 45.45 permille
```

The irrational bound is never evaluated as a float (§2.2): it is checked as the
exact rational predicate above, and the trial also asserts that `A = 10r − 1`
fails the lower bound and `A = 12r` fails the upper one, so a resized artifact is
checked against the same arithmetic rather than against this instance's numbers.

**No `r` was refused.** Every `r` admits a feasible `A`, because all three bounds
scale with `r`; what `r` buys is granularity (`r/2` is the error count, and `A`
must be an integer multiple that keeps the classes whole). `r = 200` was chosen
so that `A = 11r` is a clean composition `1 : 7 : 3 : 1` and the region is 100
pairs — large enough that one pair is one permille of `A` and no single pair can
move a verdict.

### 2.3 `n_neg = 100`, measured on the engine this project has

| class | answered correctly | answered wrongly | abstained |
|---|---|---|---|
| K0 forcing | 100 | **100** | 0 |
| K2 current-value | 1 400 | 0 | 0 |
| K3 as-of | 600 | 0 | 0 |
| K4 absence probe | — | 0 (fabricated) | 200 |

The base stream is clean — no near-duplicate, ambiguity or malformed knob — so
**all of the error mass is the forcing region, by construction**. The frozen
Layer-5 engine, replayed over the 12 000-event stream at `DEFAULT_BUDGET`
(occupancy 91 119, `refused = 0`) and asked all 2 400 queries through `§7`'s
ordinary interface, agrees with `_l6btasks.declared_reader` on **every** query,
status and value. So `n_pos = 2 100`, `n_neg = 100`, `A = 2 200`: both AUROC
classes non-empty, and non-empty for **every** reader rather than for the one
this project happens to implement.

---

## §3. `R2` obligation 1 — the ceilings, with their policy classes declared

`R5` clause 3 requires every `ATTAINABILITY.md` to declare the **policy class**
its ceiling is exact over.

* **class O (oracle)** — a policy that may read the artifact's `ground_truth` or
  a query's `value` field. It is the logical maximum over all policies.
* **class E (evidence-only)** — a policy that is a function of
  `_l6btasks.evidence()` and nothing else: the closed five-feature vocabulary
  `n_assert`, `n_distinct`, `set_once_tie`, `verbatim_repeats`, `assert_span`,
  every one computed from the frozen stream alone.

| ceiling | class | Brier | ECE | AUROC | F |
|---|---|---|---|---|---|
| **O** — confidence = correctness | all policies | **0** | **0** | **1000** | 955 |
| **E** — the exhibited witness `W` | evidence-only | **1/44 → 23** | **0** | **41/42 → 976** | 955 |
| the ratified gate | — | ≤ 40 | ≤ 30 | ≥ 900 | ≥ 950 |

**The distance between the classes is now the tie itself, and that is the
round-2 change.** On round 1's battery class E *met* class O exactly on AUROC,
because murk's evidence resolved as well as it ranked. Here it cannot: the oracle
reads the coin and reaches 1000, the evidence-only witness reaches `41/42`, and
the gap `1/42` is exactly what the withheld signal is worth. The gate at
`40 / 30 / 900` lies strictly inside both, so obligation 1 is discharged under
either family — but the family is now doing work, which is what `R5` clause 3
exists to make visible.

### 3.1 The witness, exhibited

`W` is `_l6btasks.policy_witness`: a pure map from the declared evidence to an
integer permille.

```
set_once_tie        ->  500      200 queries   (the forcing region)
otherwise           -> 1000    2 000 queries
```

Two things about it are worth stating plainly.

**The 500 is derived, not chosen.** Theorem 1 pins the accuracy of any committing
reader on the region at exactly one half, so `permille(1/2) = 500` is the region
stating its own number — asserted by
`::trial_the_tie_confidence_is_the_regions_own_arithmetic`. Any other value
scores worse on Brier, so `§3.4`'s arithmetic and the construction agree.

**The witness cannot resolve, and does not pretend to.** Round 1 recorded the
honest fact that its witness's ranking *coincided* with the oracle's because
`set_once_conflict` had an accuracy of exactly `0/158` on that substrate. Here
there is no such coincidence available: the witness is 50% accurate on everything
it flags, by theorem. This is a confidence model and not a second reader, which
is `§5 L6`'s own distinction — it asks for *"confidence permille from structural
evidence"*, not for a better answer.

### 3.2 The price, under rule P (`R5` clause 4)

`R5` clause 4: *"an unpriced item is not a saving; it is a margin that has
already been spent."* The marginal state a confidence policy needs **beyond the
frozen Layer-5 state**, priced at one cell per grammar atom (`R4` clause 3):

| item | cells | why |
|---|---|---|
| `n_assert`, `n_distinct`, `verbatim_repeats`, `assert_span` | **0** | read off the interval table the engine already holds — it carries every assertion's `t` and value |
| `set_once_tie` | **18** | one flag per attribute key, on battery-b's 18-key vocabulary — the declared grammar reading, priced as state because that is where it would live |
| **operational bookkeeping, named** | **18** | and nothing else |

The vocabulary was chosen with this in mind: an earlier draft carried a per-entity
event count, which is **not** free (one counter per entity, ~2 500 cells here) and
which no policy used. It was dropped rather than left unpriced. The two features
it would have been most tempting to add — the raw entity id and the absolute
logical time — are excluded for a different and stronger reason, recorded in
`_l6btasks.FEATURES`: they are the two handles Theorem 1 leaves, they buy a
policy no reachable score (both id-keyed readers on the bench measure the same
100 errors), and excluding them makes every feature **equal on the two members of
a pair**, so a class-E policy provably cannot split a tie.

`§5 L6` states **no footprint clause**; the only budget clause is `B = 1000`, and
at `DEFAULT_BUDGET` occupancy is 91 119 with `refused = 0`, so `B = 1000` is
attained rather than approached.

**The loss-accounting reserve is DISCLAIMED, with its reason** — `R5` clause 4
admits a disclaimer and requires the reason, and the reason is unchanged from
round 1 because the question is unchanged. This artifact is scored **in budget**
where nothing is evicted. Under pressure the *evidence itself* becomes lossy: a
shed chain's `set_once_tie` is gone, and a model reading a table that has
forgotten the tie would be confident for the wrong reason — and it would be
confident **at 1000 on a coin flip**, which is the worst failure this layer has.
That is a Stage-B and Stage-C question this document does not take and does not
pre-empt; it is named here so a later session inherits the item.

---

## §4. `R2` obligation 2 — every named baseline, re-scored

`R5` clause 2 applied first: direction-aware (*strictly better*) and over the
gate's **conjunction**, with every clause's arithmetic recorded either way. All
figures are exact `Fraction`s rendered at `§3.5` permille; `n/a` is `§3.4`'s own
report for an undefined AUROC.

| policy | class | Brier ≤40 | ECE ≤30 | AUROC ≥900 | F ≥950 | B =1000 | clears |
|---|---|---|---|---|---|---|---|
| oracle | O | 0 | 0 | 1000 | 955 | 1000 | yes — not capability-free |
| **witness `W`** | E | **23** | **0** | **976** | **955** | **1000** | **yes** |
| conflict-rank `P_d` | E | 36 | 0 | 911 | 955 | 1000 | **yes** |
| confident-always (= `make_engine(5)`, measured) | E, capability-free | **45** | **45** | **500** | 955 | 1000 | no — fails three |
| base-rate constant | E, capability-free | **43** | 0 | **500** | 955 | 1000 | no — fails two |
| detect-and-abstain | E, capability-free | 0 | 0 | **n/a** | **918** | 1000 | **no — fails `F`** |
| abstain-on-conflict | E, capability-free | 0 | 0 | **n/a** | **766** | 1000 | no — fails `F` |

(**bold** = that policy fails, or cannot be evaluated on, that clause.)

### 4.1 Clause by clause, which is what `R5` clause 2 asks for

* **`F ≥ 950` now discriminates against BOTH abstainers, and that is the round-2
  result.** `detect-and-abstain` — the policy that follows `§3.0`'s incentive to
  its end, hedging exactly what the evidence flags and thereby deleting it from
  `§3.4`'s denominator — measures `1010/1100 → 918`. On round 1's battery the
  same policy scored 960 and cleared. The region is 200 of 2 200 answerable
  queries and each hedge costs 900 out of a 50-permille budget; the arithmetic
  §5 generalises is what makes the kill structural rather than lucky. The
  key-blind `abstain-on-conflict` fails far harder at 766, hedging 772 queries.
* **`Brier ≤ 40` discriminates against BOTH constants.** `confident-always`
  scores `1/22 → 45`; the base-rate constant scores `19091/440000 → 43`. Both
  exceed 40. This is §2.2's upper bound **occupied**, and it is occupied because
  the band was chosen to occupy it.
* **`AUROC ≥ 900` fails both constants by arithmetic, not by margin.** A constant
  confidence ranks nothing: every correct×incorrect pair ties, ties count ½, so
  `AUROC = 1/2` **exactly** — 400 permille short, at every error rate.
* **`ECE ≤ 30` discriminates against nothing, with round 1's ordering
  REVERSED.** The base-rate constant scores `1/2200 → 0` with no model at all.
  What has changed is that it no longer *beats* a real model: the witness's
  partition agrees with itself exactly — bin 5 carries 200 answers at confidence
  500 against an accuracy of one half, bin 9 carries 2 000 at 1000 against 1 — so
  `ECE = 0` and the constant merely ties the floor from above. The clause is idle
  either way; the reason it is idle is not the reason round 1 recorded, and the
  trial that asserted round 1's ordering went RED here and was corrected rather
  than relaxed.
* **`B = 1000` is attained by every policy**, none of them touching the write
  path.

**So the conjunction discriminates, and four of the five clauses do work
clause-wise** — one more than round 1, and the new one is `F`.

### 4.2 `confident-always` is not a policy: it is the capped engine, measured

`§5.1 L6` defends the humility ceiling by saying a capped engine *"carries no
confidence model, so the harness scores it confident-by-default"*. No convention
is needed and none is supplied: the frozen Layer-5 engine emits confidence
through `§7.2` itself, and over all 2 400 queries the distinct confidences it
returns are exactly `{0, 1000}`. So the `confident-always` row **is**
`make_engine(layer_cap = 5)` scored on battery-b:

```
capped AUROC   500   against the ratified ceiling of 600 and the gate of 900
```

**neither breached nor vacuous** — sat at from below by arithmetic, 100 permille
under the ceiling, and *defined*, which is what `README-l5 §4` said the Layer-6
humility battery would need a query class to buy. Round 1 bought it with K1;
battery-b buys it with a query class the engine cannot get right **for any
reading**, which is the stronger form of the same purchase.

This document does **not** apply that ceiling. `trials/humility/l6/` does not
exist, no `IMPOSSIBILITY.md` is written, and `R2`'s standing order puts the
trials after the arithmetic.

### 4.3 The key-blind ranker, re-measured, and the scope statement updated

Round 1's sharpest positive result was that *a policy that RANKS without
RESOLVING clears the gate* — the key-blind `conflict-rank`, which sees that a
chain disagrees with itself and cannot see which value is true, scoring
`Brier 31 / ECE 0 / AUROC 945 / F 955`. Re-measured on battery-b:

```
conflict-rank   Brier 36   ECE 0   AUROC 911   F 955   — still clears
```

The scope statement changes twice over, and both changes matter.

**It is no longer a contingent result.** On round 1's substrate, resolving was
*available* and the finding was that the gate did not demand it. Here resolving
is **impossible**, so the exhibited witness is itself non-resolving and the gate
is reachable only by ranking. The finding is promoted from *"Layer 6 does not
require the resolving reading"* to *"on this artifact Layer 6 cannot require
it"* — which is a claim about the gate rather than about a lucky policy.

**And key-blindness now costs something measurable.** `conflict-rank` cannot tell
a set-once tie from an ordinary chain that was legally updated, so it prices both
at the same level and its AUROC falls from 945 to **911 against a gate of 900** —
it clears on 11 permille where the set-once-aware witness clears on 76. That gap
is the honest measure of what the declared set-once reading is worth, and it is
asserted (`::trial_ranking_without_resolving_clears_the_gate_and_the_scope_is_restated`
requires the key-blind policy to score strictly below the witness, so a future
change that made key-blindness free would go red rather than pass unnoticed).

Round 1's caveat carries forward unchanged and is not weakened: `conflict-rank`'s
levels are the artifact's own measured accuracy per conflict count, so its scores
are a **ceiling for the key-blind sub-family** rather than an attainable policy.
What is new is that the fit is **coin-invariant** — Theorem 1 pins the region's
accuracy at one half under either coin, so the levels do not move, which
`ops/l6/t_l6batteryb.py` asserts along with every other class-E score.

---

## §5. The collision, closed by arithmetic

`PRE-READ.md §3` predicted that `§3.0` and `§3.4` do not compose: `§3.0` pays an
engine to turn errors into abstentions (0 → 100) and `§3.4` puts abstentions
outside its denominator entirely. Round 1 measured both horns and could resolve
neither, because on its artifact the honest hedger cleared every evaluable clause
and the whole of `R2` obligation 2 hung on the meaning of `n/a`.

On battery-b the incentive still exists and **it is no longer affordable**. A
policy hedging `k` mirror pairs is left with

```
n_neg = 100 − k        F = (21000 − 8k) / 22000
```

because each hedged pair converts two answers worth 1000-and-0 into two
abstentions worth 100 each. The ladder, **measured** rather than derived
(`::trial_no_policy_clearing_f_can_reach_n_neg_zero`):

| pairs hedged `k` | `n_neg` | `F` exact | `F` permille | clears `F ≥ 950`? |
|---|---|---|---|---|
| 0 | 100 | 21/22 | 955 | yes |
| 12 | 88 | 2613/2750 | 950 | yes, under both readings |
| 13 | 87 | 1306/1375 | 950 | **exact: no. permille: yes.** |
| 14 | 86 | 2611/2750 | 949 | no |
| 50 | 50 | 103/110 | 936 | no |
| 100 | **0** | 101/110 | **918** | no |

**Every policy that clears `§5 L6`'s own fidelity clause has `n_neg ≥ 87`.** So
on this artifact `AUROC` is defined for every policy that can afford to be in the
running, and `R2` obligation 2 is discharged by `F`, `Brier` and `AUROC` together
without any clause of it resting on what `n/a` means.

Two honesties about that ladder. It is scored **outside** the class-E policy
interface, on purpose: a class-E policy cannot even choose *which* pairs to
hedge, because the two members of a pair carry identical evidence — so the family
measured here strictly contains class E and the bound is stronger for it. And the
13-pair row is the disputed-reading instance §1.1 records: affordable under the
permille reading, not under the exact one. Neither reading changes a verdict, and
the floor `n_neg ≥ 87` holds under both.

**The second horn is defused too, and this is the part that makes the
`n/a`-disqualification cheap.** Round 1's draft accepted, with reasons, that
*"a gate citing AUROC cannot be cleared by an engine that answers everything
correctly"* — an unattractive consequence it took because the alternative was
worse. On battery-b that engine **does not exist**: answering everything
correctly requires resolving the region, and Theorem 2 says the resolving signal
is not in the stream. The disqualifying reading locks out nothing reachable here.
It is still the right general rule, and `RULING-R7-DRAFT.md` clause 3 still asks
for it — but it now costs this artifact nothing, and a rule that costs nothing on
the artifact it binds is a rule a human can take without buying a consequence.

---

## §6. What round 1 measured, and what it means for its artifact

`corpora/l6battery` is not wrong and this document does not say it is. It
supplied the first calibration denominator this project ever had, it measured
the capped engine at a defined AUROC of 500, and its arithmetic still runs green
in `t_attainability.py`. What it also did — and this is the property that
disqualifies it as a **binding** artifact rather than as a diagnostic — is
measure its own limit:

> `n_neg > 0` **for the declared reading**, measured at 158 on the engine this
> project has frozen — and **not** against an arbitrary reader.
> — `ATTAINABILITY.md §6`

with the cause measured rather than argued: `§8.7` pairs every murk defect with
its answer key **and injects it by visible construction**, so a stream-only rule
recovers each family exactly (symmetric difference **0** on contradiction 305,
near-duplicate 393, ambiguity 205, malformed 257). **On murk, evidence that ranks
also resolves.** A gate citing `AUROC` bound there would be a gate whose
evaluability depended on the engine under test not having thought of first-wins.

`RULING-R7-DRAFT.md` clause 1 therefore proposes the **fourth substrate kill** in
this project's history — after `l3stream` (R1), the chronicle family at Layer 4
(R4) and murk-as-queried (round 1's own finding) — and proposes it in the same
form: DEMOTED to an **ungated diagnostic**, its bytes untouched, its trials still
running, its cause recorded verbatim. Nothing is retired by deletion here; a
corpus is retired only by ceasing to gate on it.

---

## §7. What a human must decide

Four questions. Nothing below is taken by this session.

1. **Does the Layer-6 gate bind on `corpora/l6batteryb`, both sides?** `R6`
   clause 1's shape — ascension and humility in one clause, because a ceiling
   measured on one artifact beside a gate cleared on another is two facts about
   two worlds. §4.2 has the humility measurement ready at 500 against 600.
2. **Is `corpora/l6battery` DEMOTED to an ungated diagnostic?** §6 gives the
   cause. The draft records it verbatim in the `R4`-clause-1 form.
3. **Does `AUROC = n/a` disqualify?** The draft still proposes *disqualifies*,
   with the instrument-range framing, and now records that on the binding
   artifact the reading is not load-bearing — §5.
4. **Exact or permille?** §1.1, which now has an instance: the maximum
   affordable hedge is 12 pairs or 13 depending on the reading.

`R2` obligation 4 is unchanged and is the reason this document stops here: the
corpus binding is the human's. `RULING-R7-DRAFT.md` is deliberately **not**
appended to `BOUNDARY-RULINGS.md`, because appending is what freezes.

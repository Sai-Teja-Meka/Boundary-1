# ATTAINABILITY.md — what the Layer-6 gate can and cannot reach on `corpora/l6battery`

**BOUNDARY-RULINGS.md R2** put attainability before authority: *"a gate must lie
strictly below the oracle ceiling and strictly above every capability-free
baseline on its binding corpus, and that arithmetic must be computed and recorded
in an `ATTAINABILITY.md` BEFORE the gate binds."* This is that document for
Layer 6, written **before a line of `core/layers/l6_meta_memory.py` exists** and
before any Layer-6 trial applies a gate to any engine.

Everything numeric here is computed by `trials/_l6tasks.py` from the frozen
battery, the frozen murk corpus and the frozen murk answer key alone, and
asserted by `trials/ascension/l6/t_attainability.py`, so no number below can
drift silently. Where this document states a figure that file also computes,
**that file is the enforced value** (`R6` clause 3).

`trials/ascension/l6/PRE-READ.md` is this session's charter and predicted its
shape. **The prediction is scored in §7**, hit and miss, the way `[L4] [PULSE]`'s
Layer-5 prediction was scored at `BOUNDARY.log` line 28.

---

## §0. The verdict, first

Four findings, in the order of how much they bind.

**1. The gate is attainable, and the ceiling is EXHIBITED** (`R4` clause 5). A
concrete confidence assignment over the frozen battery — structural evidence in,
integer permille out, no engine, no answer key — attains

```
Brier 0    ECE 7    AUROC 1000    F 955    B 1000
```

against a ratified gate of `≤ 40 / ≤ 30 / ≥ 900 / ≥ 950 / = 1000`. Every clause
is cleared with room, direction-aware (`R5` clause 2).

**2. `R2` obligation 2 is discharged, and it is NOT carried by one clause.**
`PRE-READ.md §3.2` predicted the whole lower obligation would rest on `AUROC`
alone. On this battery it does not: `Brier ≤ 40` fails **both** named constants
(45 and 43 against 40), `AUROC ≥ 900` fails both by 400 permille, and `F ≥ 950`
fails the key-blind abstainer by 121. Only `ECE ≤ 30` discriminates against
nothing, exactly as predicted. **`R5` clause 2's conjunction reading carries the
obligation without needing a single new clause of law** — which is the first
thing this session was told to check and the answer is that R5 already carries
it.

**3. A policy that RANKS without RESOLVING clears the gate.** The key-blind
`conflict-rank` policy — it can see that a chain disagrees with itself and cannot
see which value is true — scores `Brier 31 / ECE 0 / AUROC 945 / F 955`. This is
the sharpest positive result of the session and it answers `PRE-READ.md §4.3`'s
first worry directly: the evidence-only family is **not** too weak to reach a
gate the oracle reaches.

**4. And the collision is real, unmoved, and now exact.** `§3.4` makes `AUROC`
undefined at `n_neg = 0`, and the arithmetic below shows what that costs in both
directions at once:

* a **capability-free abstainer with no confidence model at all** scores
  `Brier 0 / ECE 0 / F 960 / B 1000` — *better than the witness on three
  clauses* — and its `AUROC` is `n/a`. If `n/a` excuses the clause, that policy
  clears every evaluable clause of `§5 L6` and **`R2` obligation 2 fails**, so no
  Layer-6 gate can bind anywhere;
* if `n/a` disqualifies, obligation 2 holds — and the same reading locks out any
  engine good enough to answer everything correctly, which is every engine this
  project has ever measured.

`RULING-R7-DRAFT.md` clause (iii) is that question and it is a human's. **No gate
binds this session.**

---

## §1. The clause structure, settled in advance

`§5 L6`'s gate is `Brier ≤ 40`, `ECE ≤ 30`, `AUROC ≥ 900`, abstention-aware
`F ≥ 950`, `B = 1000`, with a humility ceiling of capped `AUROC ≤ 600`. Sorted
into `R5`'s kinds:

| clause | kind | direction | ceiling | obligation 1 discharged by |
|---|---|---|---|---|
| `Brier ≤ 40` | graded | minimizing | 0 | the ordinary method, direction-aware (`R5` clause 2) |
| `ECE ≤ 30` | graded | minimizing | 0 | the ordinary method, direction-aware |
| `AUROC ≥ 900` | graded | maximizing | 1000 | the ordinary method — **where it is defined** |
| `F ≥ 950` | graded | maximizing | 1000 | the ordinary method |
| `B = 1000` | **identity** | — | 1000 | exhibited attainment (`R5` clause 1) |
| capped `AUROC ≤ 600` | ceiling | minimizing | — | measured, §5 |

**Layer 6 needs no `R5`-shaped ruling of its own** and this document requests
none. `R5` clause 2 is forward-binding in its own words — *"stated
forward-binding because Layer 6 needs it immediately: `Brier ≤ 40` and
`ECE ≤ 30` are both minimizing"* — and `R5`'s regularization already named
`B = 1000` an identity since Layer 1. Four of the six clauses are ordinary graded
gates strictly inside their ceilings and the Layer-3/Layer-4 method applies
unchanged.

### 1.1 The one reading this document declares

`§3.4` defines all three calibration quantities *in `[0,1]`* while `§5 L6` states
the gates as the integers `40 / 30 / 900`, and `§3.5`'s `permille` rounds
half-to-even. The two readings disagree on a real interval:

| gate | exact reading | permille reading | they differ on |
|---|---|---|---|
| `Brier ≤ 40` | `Brier ≤ 40/1000` | `permille(Brier) ≤ 40` | `(40/1000, 81/2000]` |
| `ECE ≤ 30` | `ECE ≤ 30/1000` | `permille(ECE) ≤ 30` | `(30/1000, 61/2000]` |
| `AUROC ≥ 900` | `AUROC ≥ 900/1000` | `permille(AUROC) ≥ 900` | `[1799/2000, 900/1000)` |

This document takes the **exact** reading, because `§5.1 L6`'s own defense
sentences state bounds on the quantity and not on its rounding — *"at or under
0.04"*, *"to within 3%"*. **And it records the fact that makes the choice cheap:
not one of the seven policies scored below lands in a disputed interval**, so
every verdict in §3 and §4 is the same under either reading. That is asserted
rather than observed
(`t_attainability.py::trial_no_scored_policy_lands_in_a_disputed_reading_interval`),
so a later policy that *did* land there would be red rather than quiet.
`RULING-R7-DRAFT.md` clause (iv) asks for the reading anyway, because it is cheap
to settle before a measurement needs it and expensive after.

---

## §2. The battery, and why its size is forced

`corpora/l6battery`, seed 8008, **3 905 queries** over the frozen murk corpus
with answer keys derived from murk's frozen `ground_truth.json`. Its README is
the full statement; the arithmetic this document needs is:

```
K1   355   commitment  — current(entity, "origin"), EVERY entity carrying one
K2 2 130   current-value over non-`origin` pairs
K3 1 065   as-of at a non-terminal assertion
           -----
A  3 550   the answerable core = §3.4's calibration denominator
K4   355   absence probes — unanswerable, outside the denominator
           -----
N  3 905
```

**Why murk, and why a battery rather than a new corpus.** `§5 L6` asks for
*"confidence permille from **structural evidence**"*, and `§8.7`'s murk layer is
the only frozen corpus whose defects are injected on purpose and **always paired
with an answer key**. `§8.8`'s single REAL corpus is 25 events — three orders of
magnitude too small to fill ten ECE bins. What murk lacked was not evidence but a
**denominator**: at Layer 4 it scored `C 695 / F 708` with `wrong = 0`, so its
305 permille of missing coverage were abstentions, and abstentions are outside
`§3.4`. `PRE-READ.md §4` named this and it is confirmed.

**Recorded so it is not rediscovered as a surprise:** murk is an *ungated
diagnostic* at Layer 4 under `R4` clause 1 (footprint 364‰ against 250,
`C ≤ 754 / F ≤ 711`). That does not disqualify it here — `§5 L6` states **no
footprint clause**, the inheritance class replays `§5 L4`'s battery on
`l4stream` and not on murk, and this battery is scored **in budget** at
`DEFAULT_BUDGET` where the engine holds all 10 000 episodes at occupancy 74 981
with `refused = 0`. A corpus may bind one gate while diagnosing another; `R1`
clause 5 and `R4` clause 1 both already say so for other corpora.

### 2.1 The size is forced by two ratified clauses pulling opposite ways

On an all-answerable core with wrong share `w` and abstention share `a`, `§3.0`
gives `F = 1000 − 1000w − 900a`, so:

```
F ≥ 950   ⟺   1000w + 900a ≤ 50          a total error-and-hedging budget of 50‰
```

and with `a = 0` that caps `w ≤ 50‰`, so `A ≥ 158/0.050 = 3 160`.

The other side is `Brier`. A **base-rate constant** policy — stating the corpus's
own accuracy flat on every answer, which costs nothing to state — scores
`Brier = w(1 − w)` exactly. For `Brier ≤ 40` to discriminate against it,

```
w(1 − w) > 40/1000   ⟺   w > (1 − √(21/25))/2 = 41.74‰    so   A ≤ 3 784
```

`A = 3 550` puts the declared reader's error rate at

```
w = 158 / 3 550 = 44.5‰
```

near the middle of a band **nine permille wide**, and the band's upper end is
`§5 L6`'s own `F` clause. `PRE-READ.md §3.2` computed that band before the
battery existed; this is the band **occupied**.

### 2.2 `n_neg = 158`, measured on the engine this project has

`PRE-READ.md §4.3` item 3 required the recorded arithmetic to include *"the error
rate of the engine under test on the binding battery, because that single number
decides whether three of the five clauses discriminate at all and whether AUROC
is defined"*. It does:

| class | answered correctly | answered wrongly | abstained |
|---|---|---|---|
| K1 commitment | 197 | **158** | 0 |
| K2 current-value | 2 130 | 0 | 0 |
| K3 as-of | 1 065 | 0 | 0 |
| K4 absence probe | — | 0 (fabricated) | 355 |

The frozen **Layer-5 engine**, replayed over murk at `DEFAULT_BUDGET` and asked
all 3 905 queries through `§7`'s ordinary interface, agrees with
`_l6tasks.declared_reader` on **every** query, status and value
(`t_l6battery.py::trial_the_declared_reader_is_what_the_frozen_engine_does`). So
the engine-free arithmetic below is about the engine this project actually has,
and `n_pos = 3 392`, `n_neg = 158`, `A = 3 550`: **both AUROC classes are
non-empty and the calibration triple is defined.** That is the thing this
battery exists to produce.

---

## §3. `R2` obligation 1 — the ceilings, with their policy classes declared

`R5` clause 3 requires every `ATTAINABILITY.md` to declare the **policy class**
its ceiling is exact over, and `PRE-READ.md §4.3` warned that at Layer 6 the
declaration is load-bearing rather than a formality. It is made mechanical here:

* **class O (oracle)** — a policy that may read `corpora/murk/ground_truth.json`
  or the battery's answer keys.
* **class E (evidence-only)** — a policy that is a function of
  `_l6tasks.evidence()` and nothing else: the closed six-feature vocabulary
  `n_assert`, `n_distinct`, `set_once_conflict`, `verbatim_repeats`,
  `reused_entity`, `unreadable_touching`, every one computed from the murk event
  stream alone.

`§5 L6` asks for confidence from **structural evidence**, so class E is the
family that matters and class O is scored only to measure the distance between
them.

| ceiling | class | Brier | ECE | AUROC | F |
|---|---|---|---|---|---|
| **O** — confidence = correctness | all policies | **0** | **0** | **1000** | 955 |
| **E** — the exhibited witness `W` | evidence-only | **693/2 218 750 → 0** | **127/17 750 → 7** | **1000** | 955 |
| the ratified gate | — | ≤ 40 | ≤ 30 | ≥ 900 | ≥ 950 |

**The finding `PRE-READ.md §4.3` asked for.** It warned that the evidence-only
family's ceiling *"is strictly lower, and nobody knows by how much until it is
exhibited"* — the Form-B pass-through lesson pointing the other way, a family too
**large** making a gate look comfortably attainable. Measured: on this battery
class E **meets** the all-policy ceiling exactly on `AUROC`, and misses it by
`693/2 218 750` on `Brier` and `127/17 750` on `ECE` — three ten-thousandths and
seven thousandths. The gate at `40 / 30 / 900` lies strictly inside both, so
obligation 1 is discharged under either family and the choice of family does not
change a verdict. **The warning was right to demand the measurement and the
measurement came out benign.**

### 3.1 The witness, exhibited

`W` is `_l6tasks.policy_witness`: a pure map from the declared evidence to an
integer permille, no engine, no answer key.

```
set_once_conflict          ->   20      158 queries
n_distinct == 1            -> 1000    2 875 queries
n_distinct in {2, 3}       ->  960      491 queries
otherwise                  ->  900       26 queries
```

It occupies ECE bins 0 and 9. It is **not** the oracle wearing a costume in
form — it reads six declared features and no key — but this document records the
honest fact that on **this** battery the feature `set_once_conflict` has an
accuracy of exactly `0/158`, so `W`'s ranking and the oracle's coincide. That is
not a property of `W`; it is §6's finding about murk, and it is why §6 exists.

### 3.2 The price, under rule P (`R5` clause 4)

`R5` clause 4: *"an unpriced item is not a saving; it is a margin that has
already been spent."* The marginal state a confidence policy needs **beyond the
frozen Layer-5 state**, priced at one cell per grammar atom (`R4` clause 3):

| item | cells | why |
|---|---|---|
| `n_assert`, `n_distinct`, `verbatim_repeats` | **0** | read off the interval table the engine already holds |
| `reused_entity` | **0** | a re-spawn after a retire is two assertions already in the table (`class`, `live`) |
| `unreadable_touching` | **0** | the per-entity irreducible counts Layer 4 already carries (`README-l5 §0.3`) |
| `set_once_conflict` | **18** | one flag per attribute key, on murk's 18-key atlas — the declared grammar reading, priced as state because that is where it would live |
| **operational bookkeeping, named** | **18** | and nothing else |

`§5 L6` states **no footprint clause**; the only budget clause is `B = 1000`, and
at `DEFAULT_BUDGET` occupancy is 74 981 with `refused = 0`, so `B = 1000` is
attained rather than approached.

**The loss-accounting reserve is DISCLAIMED, with its reason** — `R5` clause 4
admits a disclaimer and requires the reason. This battery is scored **in budget**
where nothing is evicted, so there is no loss to reserve against. Under pressure
the *evidence itself* becomes lossy — a shed chain's conflict count is gone, and
a confidence model reading a table that has forgotten the contradiction would be
confident for the wrong reason — and what an engine owes then is a Stage-B and
Stage-C question this document does not take and does not pre-empt. It is named
here so a later session inherits the item rather than rediscovering it, which is
exactly what clause 4 was written for.

---

## §4. `R2` obligation 2 — every named baseline, scored

`R5` clause 2 is applied **first**, as this session was instructed: the obligation
is read direction-aware (*strictly better*) and over the gate's **conjunction**,
with every clause's arithmetic recorded either way. All figures are exact
`Fraction`s rendered at `§3.5` permille; `n/a` is `§3.4`'s own report for an
undefined AUROC.

| policy | class | Brier ≤40 | ECE ≤30 | AUROC ≥900 | F ≥950 | B =1000 | clears the gate |
|---|---|---|---|---|---|---|---|
| oracle | O | 0 | 0 | 1000 | 955 | 1000 | yes — not capability-free |
| **witness `W`** | E | **0** | **7** | **1000** | **955** | **1000** | **yes** |
| conflict-rank `P_d` | E | 31 | 0 | 945 | 955 | 1000 | **yes** |
| confident-always | E, capability-free | **45** | **45** | **500** | 955 | 1000 | no — fails three |
| base-rate constant | E, capability-free | **43** | 0 | **500** | 955 | 1000 | no — fails two |
| abstain-on-set-once | E, capability-free | 0 | 0 | **n/a** | 960 | 1000 | **not evaluable** |
| abstain-on-conflict | E, capability-free | 0 | 0 | **n/a** | **829** | 1000 | no — fails `F` |

(**bold** = that policy fails, or cannot be evaluated on, that clause.)

### 4.1 Clause by clause, which is what `R5` clause 2 asks for

* **`ECE ≤ 30` discriminates against nothing.** The base-rate constant scores
  `ECE = 7/14 200 → 0`, *better than the witness's 7*, with no model at all: one
  constant confidence puts every answer in one bin whose mean confidence is its
  own accuracy, and a one-bin partition agrees with itself. `PRE-READ.md §3.2`
  predicted this exactly, including the rounding caveat — the battery's accuracy
  `3 392/3 550` is not expressible in permille, so the policy states 955 and its
  ECE is `7/14 200` rather than 0. Against a gate of 30 the distinction is not
  worth a ruling.
* **`Brier ≤ 40` discriminates against BOTH constants.** `confident-always`
  scores `w = 79/1 775 → 45`; the base-rate constant scores
  `4 831/113 600 → 43`. Both exceed 40. This is the nine-permille band of
  `PRE-READ.md §3.2` **occupied**, and it is occupied because §2.1 sized the
  battery to occupy it.
* **`AUROC ≥ 900` fails both constants by arithmetic, not by margin.** A constant
  confidence ranks nothing: every correct×incorrect pair ties, ties count ½, so
  `AUROC = 1/2` **exactly** — 400 permille short, at every error rate, for every
  constant.
* **`F ≥ 950` discriminates against the key-blind abstainer** at `1 177/1 420 →
  829`, 121 permille short, which is §2.1's arithmetic biting a policy rather
  than a table: it abstains on 1 030 of 3 905 queries at 900 apiece. It does
  **not** discriminate against the set-once abstainer, which abstains on only 513
  and scores 960.
* **`B = 1000` is attained by every policy**, none of them touching the write
  path.

**So the conjunction discriminates, and three of the five clauses do work
clause-wise.** `R5` clause 2 carries the whole of `R2` obligation 2 here without
a new clause of law — which is the first thing this session was told to check.

### 4.2 `confident-always` is not a policy: it is the capped engine, measured

`§5.1 L6` defends the humility ceiling by saying *"a capped engine below Layer 6
carries no confidence model, so the harness scores it **confident-by-default**"*,
and `PRE-READ.md §3.4` named this the half of its prediction most likely to be
wrong — because a convention living in a `§5.1` defense sentence is not `§3.4`
and not `§7.2`, and *"either way the humility side of Layer 6 may turn out not to
be a measurement of an engine at all."*

**Measured, and no convention is needed.** The frozen Layer-5 engine emits
confidence through `§7.2` itself: over all 3 905 queries the distinct
confidences it returns are exactly `{0, 1000}` — 1000 on every answer, 0 on
every abstention — asserted in
`t_l6battery.py::trial_the_declared_reader_is_what_the_frozen_engine_does`. The
harness reads the engine's own field; it supplies nothing. So the
`confident-always` row above **is** `make_engine(layer_cap = 5)` scored on this
battery, and its `AUROC = 500` is a measurement of an engine:

```
capped AUROC   500   against the ratified ceiling of 600 and the gate of 900
```

**neither breached nor vacuous** — the ceiling is sat at from below by
arithmetic, 100 permille under it, and it is *defined*, which on any battery this
project had before today it would not have been. `README-l5 §4` wrote that *"the
Layer-6 humility battery needs a query class this engine gets wrong, or its
ceiling is vacuous rather than loose."* That query class is K1 and this is the
number it buys. **The humility side of Layer 6 is a measurement of an engine
after all**, and the prediction's flagged half is scored a miss in the direction
that costs nothing.

This document does **not** apply that ceiling. `trials/humility/l6/` does not
exist, no `IMPOSSIBILITY.md` is written, and `R2`'s standing order puts the
trials after the arithmetic.

---

## §5. The collision, exact

`PRE-READ.md §3` predicted that `§3.0` and `§3.4` do not compose, and the
prediction stands. What this battery adds is that the tension is now a **pair of
measured policies** rather than an argument.

**`§3.0` pays an engine to turn errors into abstentions** (0 → 100) and `§3.4`
puts abstentions outside its denominator entirely. Follow that incentive to its
end and you get `abstain-on-set-once`: a policy with **no confidence model
whatsoever** — flat 1000 on everything it answers — which hedges exactly the 158
queries the evidence flags and thereby deletes them from the calibration
denominator. It scores

```
Brier 0    ECE 0    F 960    B 1000    AUROC n/a       A = 3 392, n_neg = 0
```

Three of those are *better than the exhibited witness*. The only thing standing
between a capability-free policy and the Layer-6 gate is what `n/a` means:

* **if `n/a` disqualifies** — the natural reading of `§3.4`'s own sentence, *"any
  gate that cites AUROC requires both classes present"* — the policy does not
  clear, `R2` obligation 2 holds, and the gate can bind. **And the same reading
  locks out any engine that answers everything correctly**, because a perfect
  engine has `n_neg = 0` for the same reason the abstainer does. Every engine
  this project has ever scored is in that position on every corpus it was scored
  against (`BOUNDARY.log` lines 17, 23, 32);
* **if `n/a` excuses the clause**, the abstainer clears `Brier`, `ECE`, `F` and
  `B` — every evaluable clause of `§5 L6` — with no capability at all, `R2`
  obligation 2 fails, and **no Layer-6 gate can bind on this battery or on any
  other**.

Both horns are arithmetic, both are recorded, and neither is this session's to
choose. `RULING-R7-DRAFT.md` clause (iii) puts the question to a human, and it is
the reason that draft exists.

---

## §6. Why this battery cannot guarantee `n_neg > 0`, measured

The battery's 158 errors are the errors of the **declared latest-wins reading** —
`_l6tasks.declared_reader`, which is what `core/layers/l4_consolidation.current()`
is and therefore what every layer this project has frozen implements. A reader
that took `origin` first-wins would score `n_neg = 0` on this battery and take
`AUROC` with it.

That is not a gap this session could close by trying harder, and the reason is
arithmetic rather than argument. **`§8.7`'s own discipline is what closes it.**
The murk doctrine pairs every injected defect with its answer key *and injects it
by visible construction*, and the consequence is that a **stream-only** rule
recovers each family **exactly**:

| family | size | events a stream-only rule misclassifies |
|---|---|---|
| contradiction | 305 | **0** — a set-once key asserted with two different values |
| near-duplicate | 393 | **0** — an `attr`/`link` repeated verbatim within 100 events |
| ambiguity | 205 | **0** — a `spawn` of an id already retired |
| malformed | 257 | **0** — a payload the declared grammar reading rejects |

(asserted by
`t_l6battery.py::trial_every_murk_defect_family_is_perfectly_separable_from_the_stream`;
symmetric difference against the frozen key, not a rate.) The near-duplicate row
is the sharpest, because it is the one that looked most likely to leave a
residue: 426 byte-identical `attr`/`link` repeats, of which 393 are injected and
33 are the clean base repeating itself by chance — and they separate perfectly,
the injected ones at nearest-prior distance ≤ 25 and the coincidental ones at
≥ 131.

**On murk, evidence that ranks also resolves.** There is no query class in this
substrate where the structural evidence says *"this is risky"* without also
saying *what the answer is* — which is exactly the class a calibration battery
wants, and exactly the class a corpus built under `§8.7` cannot contain, because
a defect whose key could not be recovered from the stream would be a defect not
paired with its answer key.

So the honest statement of what this battery guarantees is:

> `n_neg > 0` **for the declared reading**, measured at 158 on the engine this
> project has frozen — and **not** against an arbitrary reader.

`PRE-READ.md §3.3` predicted the session would have to state a *corpus-and-battery
precondition* that both AUROC classes be non-empty. This is that precondition,
and it turns out to be **relative to a reader** rather than absolute, which is one
clause sharper than the prediction and is the finding that replaces it.
`RULING-R7-DRAFT.md` clause (iii) asks whether a binding artifact may guarantee
`n_neg > 0` relative to a declared reading, or whether Layer 6 needs a substrate
whose dirt is *not* recoverable — a corpus family `§8.7` does not describe and
this session does not propose.

---

## §7. The pre-read's prediction, scored

`PRE-READ.md §3.4` stated its prediction so it could be scored right or wrong.
Recorded here in the shape `BOUNDARY.log` line 28 used for Layer 5.

| prediction | verdict |
|---|---|
| obligation 1 discharges the ordinary way on every clause; no `R5`-shaped reading problem | **HIT** (§1, §3) |
| all three measures exactly computable in `Fraction` at the declared bin structure | **HIT** (`_l6tasks` computes them; no float anywhere) |
| `ECE ≤ 30` undischargeable at any error rate | **HIT** (§4.1: base-rate constant scores 0) |
| `Brier ≤ 40` undischargeable outside a nine-permille band | **HIT**, and the band is **occupied** (§2.1, §4.1) |
| obligation 2 discharged **only** over the conjunction and **only** through AUROC | **MISS.** Brier fails both constants and `F` fails one abstainer; three clauses do work (§4.1) |
| the evidence-only ceiling is strictly lower than the oracle's, by an unknown amount | **MISS**, benignly: class E meets class O on AUROC and misses by ≤ 7 permille elsewhere (§3) |
| the session must state a corpus-and-battery precondition that both AUROC classes be non-empty | **HIT in form, sharper in substance**: the precondition is relative to a declared reading and murk cannot make it absolute (§6) |
| the predicted ruling is `R4`-shaped — a reading plus a substrate | **HIT** (`RULING-R7-DRAFT.md` proposes both) |
| **the half flagged as most likely wrong** — the capped engine's confidence is a `§5.1` convention, so the humility side may not be a measurement of an engine at all | **MISS, and flagged in advance.** The frozen Layer-5 engine emits `{0, 1000}` through `§7.2` itself; no convention is needed, `AUROC` is defined, and the capped measurement is 500 against a 600 ceiling (§4.2) |

Five hits, three misses and one hit-with-a-sharpening. The flagged half was
wrong, which is what flagging it was for.

---

## §8. What a human must decide

Four questions. Nothing below is taken by this session.

1. **Does `AUROC = n/a` disqualify a policy, or excuse the clause?** §5 shows the
   two horns and shows that one of them voids `R2` obligation 2 outright. The
   draft proposes *disqualifies*, and proposes the consequence be stated in the
   same breath: a gate citing AUROC binds only on an artifact that guarantees
   both classes non-empty.
2. **May a binding artifact guarantee `n_neg > 0` relative to a DECLARED
   READING?** §6 shows murk cannot make the guarantee absolute, and shows why
   `§8.7`'s own discipline is the reason.
3. **Does the Layer-6 gate bind on `corpora/l6battery`, both sides?** `R6` clause
   1's shape — ascension and humility in one clause, because a ceiling measured
   on one artifact beside a gate cleared on another is two facts about two
   worlds. §4.2 has the humility measurement ready at 500 against 600.
4. **Exact or permille?** §1.1. Nothing turns on it today and every verdict here
   is the same under both, which is precisely why it is cheap to settle now.

`R2` obligation 4 is unchanged and is the reason this document stops here: the
corpus binding is the human's. `RULING-R7-DRAFT.md` is deliberately **not**
appended to `BOUNDARY-RULINGS.md`, because appending is what freezes.

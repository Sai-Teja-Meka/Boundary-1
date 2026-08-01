# PRE-READ.md — Layer 6 (Meta-memory), read before Stage A exists

`[L5] [PULSE]`, 2026-08-01. **This is not an `ATTAINABILITY.md`.** It binds
nothing, rules nothing, names no corpus, and applies no gate to any engine.
`core/layers/l6_meta_memory.py` does not exist, no Layer-6 constant appears in
any trial, and `laws/t_rulings.py` is untouched by this document — a gate
constant is what that registry governs, and this file declares none.

`BOUNDARY-RULINGS.md R2` fixes the standing order of an `ASCEND`: **attainability
arithmetic → trials → engine**, with the arithmetic recorded and machine-checked
*before* the gate is treated as binding. A `PULSE` cannot discharge R2 and does
not try to. What it can do is what the `[L4] [PULSE]` (`BOUNDARY.log` line 24)
did for Layer 5 — read the ratified clauses one layer ahead, say which of R2's
obligations the existing rulings already discharge and which they do not, and
**predict the shape of the collision** so the Stage-A session meets it with its
arithmetic ready instead of discovering it. That prediction was confirmed at
Layer 5 (line 28), including one half it got wrong, and the record of the miss
was worth as much as the record of the hit.

Every figure below is exact `Fraction` arithmetic over `§3.4`'s own definitions.
Where a later `ATTAINABILITY.md` computes one of these quantities, **that file is
the enforced value** and this one is prose (`R6` clause 3).

---

## §1. The clause structure of `§5 L6`, read against R2 and R5

`§5 L6`'s gate is **`Brier ≤ 40`, `ECE ≤ 30`, `AUROC ≥ 900`, abstention-aware
`F ≥ 950`, `B = 1000`**, with a humility ceiling of **capped `AUROC ≤ 600`**.
`R5` classified gate clauses into three kinds; sorting Layer 6's into them is the
first thing Stage A owes, and it comes out differently from Layer 5:

| clause | kind | direction | ceiling | R2 obligation 1 discharged by |
|---|---|---|---|---|
| `Brier ≤ 40` | graded | **minimizing** | 0 | the ordinary method, read direction-aware (`R5` clause 2) |
| `ECE ≤ 30` | graded | **minimizing** | 0 | the ordinary method, read direction-aware (`R5` clause 2) |
| `AUROC ≥ 900` | graded | maximizing | 1000 | the ordinary method — **when it is defined at all** (§3) |
| `F ≥ 950` | graded | maximizing | 1000 | the ordinary method |
| `B = 1000` | **identity** | — | 1000 | exhibited attainment (`R5` clause 1) |
| capped `AUROC ≤ 600` | ceiling | minimizing | — | measured, `§6` |

**Layer 6's clause-shape question is already settled, and was settled in
advance.** `R5` clause 2 says so in its own words — *"This clause is stated
forward-binding because Layer 6 needs it immediately: `Brier ≤ 40` and
`ECE ≤ 30` are both minimizing…"* (`BOUNDARY-RULINGS.md`, R5 clause 2) — and
`R5`'s regularization section already names `B = 1000` an identity **since Layer
1**. So Layer 6 inherits both readings ratified and needs no `R5`-shaped ruling
of its own. Four of its six clauses are ordinary graded gates strictly inside
their ceilings — the Layer-3/Layer-4 method applies unchanged. **This is not
where Layer 6 gets hard.**

---

## §2. Are Brier, ECE and AUROC exactly computable under the physics?

**Yes — all three, with no float anywhere, at the declared bin structure.**
`§2.2` prohibits floats in `core/` and `§3.4` already says *"all exact"*; this
section confirms the arithmetic actually closes, because a measure that needed a
float would make `§5 L6` unimplementable under `§2.2` and that is worth knowing
before an engine is designed rather than after.

Confidence is an **integer permille** `conf ∈ [0, 1000]` (`§3.4`, `§7.2`) and
`correct ∈ {0, 1}`. Then:

* **Brier** `= (1/A) · Σ (conf_i/1000 − correct_i)²`. Each term is a `Fraction`
  with denominator dividing `10⁶`; the sum over `A` terms divides `10⁶·A`. Exact,
  and the denominator is bounded by the battery size — no growth in `A` beyond
  linear.
* **ECE** `= Σ_b (n_b/A)·|mean_conf_b − acc_b|`. The ten bins of `§3.4` are
  `[0,100), … , [900,1000]` with the last **closed**, so bin assignment on an
  integer permille is exactly `conf // 100`, with the single special case
  `conf = 1000 → bin 9`. Both a total order and a partition, computed by integer
  division: no boundary is ambiguous and no value falls outside. `mean_conf_b`
  and `acc_b` are rational means of exact quantities. Exact.
* **AUROC** `= U / (n_pos · n_neg)` with ties counting ½, so `U` is a half-integer
  and the quotient has denominator dividing `2·n_pos·n_neg`. Exact — **when both
  classes are non-empty**, which `§3.4` states as a precondition and this document
  takes as the central finding (§3).

**The one physics-level item Stage A must declare — the reading, not the
arithmetic.** `§3.4` defines all three quantities *in `[0,1]`*; `§5 L6` states
the gates as the **integers 40, 30, 900**, and `§3.5`'s `permille` maps `[0,1]`
to `[0,1000]` by round-half-to-even. Two readings are then available and they
disagree on a real interval:

| gate | exact reading | permille reading | they differ on |
|---|---|---|---|
| `Brier ≤ 40` | `Brier ≤ 40/1000` | `permille(Brier) ≤ 40` | `(40/1000, 81/2000]` |
| `ECE ≤ 30` | `ECE ≤ 30/1000` | `permille(ECE) ≤ 30` | `(30/1000, 61/2000]` |
| `AUROC ≥ 900` | `AUROC ≥ 900/1000` | `permille(AUROC) ≥ 900` | `[1799/2000, 900/1000)` |

The upper endpoints are exact: `permille(81/2000) = permille(40.5‰) = 40`,
because `§3.5` rounds a half to the **even** neighbour and 40 is even. This is
the Layer-6 analogue of `§5 L4`'s `footprint ≤ 250`, which `R4` clause 2 had to
rule on because three ratified sentences otherwise said three different things —
except that here the two readings are both defensible and differ by half a
permille rather than by three orders of magnitude. It is small, and it is exactly
the sort of item that is cheap to rule on before a measurement and expensive
after. **`§5.1 L6`'s own defense sentences favour the exact reading** — *"at or
under 0.04"* and *"to within 3%"* are stated as bounds on the quantity, not on its
rounding — and Stage A should say so in its own text rather than let the
instrument decide by accident.

---

## §3. The collision: `§3.0`'s table and the calibration triple are not one law

`§3.0` scores a query **1000 / 1000 / 100 / 0** (correct answer / correct
abstention / hedged abstention on an answerable query / confident error or
fabrication). `§3.4` computes Brier, ECE and AUROC **over the `A` answered
queries** — abstentions are outside the calibration denominator entirely. Those
two sentences are both ratified and they do not compose:

> **`§3.0` is confidence-blind.** A wrong answer scores **0** whatever confidence
> it carries. An engine that answers *"X, and I am 50‰ sure"* and is wrong scores
> exactly what a confident liar scores. Under `§3.4` those are opposite
> behaviours — the hedge is the one that makes `AUROC` computable and high.

> **`§3.4` is abstention-blind.** An abstention contributes nothing to Brier, ECE
> or AUROC. Under `§3.0` an abstention on an answerable query is a small loss
> (100 rather than 1000); under `§3.4` it is a **free deletion of the query from
> the calibration denominator**.

So the two laws point the same query in opposite directions, and the tension is
quantifiable from the ratified numbers alone.

### 3.1 What `F ≥ 950` costs, exactly

On an all-answerable battery with wrong share `w` and abstention share `a`
(permille), `§3.0` gives `F = 1000 − 1000w − 900a`, so `F ≥ 950` is

```
1000w + 900a ≤ 50
```

— a **total error-and-hedging budget of 50 permille**, spent at 1000 per wrong
answer and 900 per abstention:

| `w` | max `a` |
|---|---|
| 0 | 56 |
| 10 | 44 |
| 20 | 33 |
| 30 | 22 |
| 40 | 11 |
| **50** | **0** |

An engine that abstains its way out of every uncertain query has at most 56
permille of room, and one that answers and errs has at most 50.

### 3.2 What the capability-free baselines score — the identity that bites

`§5.1 L6` supplies its own baseline in its own words: *"a capped engine below
Layer 6 carries no confidence model, so the harness scores it
**confident-by-default**"* — and `README-l5 §4` already verified the engine that
exists is exactly that, every answer carrying `confidence = 1000`
(`core/layers/l5_prospection.py`). For a constant confidence `c ≡ 1000` over `A`
answers with wrong share `w`:

```
Brier = w        ECE = w        AUROC = 500   (exactly; ties count ½)
```

Brier and ECE **are the error rate itself**. And a second capability-free policy
that costs nothing to state — **base-rate constant confidence**, answering
`c ≡ 1000 − w` on every query, the corpus's own accuracy rate stated flat — does
better still:

```
Brier = w(1 − w)   ECE = 0 (one bin, agreeing with itself)   AUROC = 500
```

Both AUROC figures assume `w > 0`; at `w = 0` AUROC is **`n/a`** for every policy
(§3.3), which is the whole of §3.3.

| baseline | `w=10` | `w=20` | `w=30` | `w=40` | `w=50` | `w=80` |
|---|---|---|---|---|---|---|
| confident-by-default — Brier / ECE | 10 / 10 | 20 / 20 | 30 / 30 | 40 / **40** | **50** / **50** | **80** / **80** |
| base-rate constant — Brier / ECE | 10 / 0 | 20 / 0 | 29 / 0 | 38 / 0 | **48** / 0 | **74** / 0 |
| both — AUROC | **500** | **500** | **500** | **500** | **500** | **500** |

(**bold** = that baseline **fails** that clause; everything unbolded is a
capability-free policy **clearing** a ratified Layer-6 clause.) Read the table
against `R2` obligation 2, which
requires the gate to lie **strictly better** than every named capability-free
baseline (`R5` clause 2, direction-aware):

* **`ECE ≤ 30` discriminates against nothing.** A single constant confidence
  equal to the corpus's base rate puts every answer in **one** bin whose mean
  confidence *is* its accuracy, so `ECE = 0` **at every error rate** — better
  than any real confidence model can do and achieved with no model at all. ECE
  measures bin-wise agreement and a one-bin partition agrees with itself. (The
  one exactness caveat, stated so it is not mistaken for a loophole: confidence
  is an **integer** permille, so the policy can state its base rate exactly only
  when the battery's accuracy is expressible in permille. Otherwise it rounds,
  and `ECE ≤ 1/2000` — `permille(ECE) ∈ {0, 1}`. Against a gate of 30 the
  distinction is not worth a ruling.)
* **`Brier ≤ 40` discriminates only in a band.** Confident-by-default clears it
  for every `w ≤ 40‰`; the base-rate policy clears it for every `w ≤ 41‰`
  (exactly, `w(1−w) ≤ 1/25 ⟺ w ≤ (1 − √(21/25))/2 ≈ 41.7‰`). To discriminate
  against **both**, `w` must exceed both, so the band where Brier is load-bearing
  is `w ∈ (41, 50]‰` — **nine permille wide, and bounded above by `§5 L6`'s own
  `F ≥ 950` clause** (§3.1), which caps `w` at 50‰. Nine permille, and only with
  zero abstentions; every abstention spent narrows it further at 900 apiece.
* **`AUROC ≥ 900` is the only clause both baselines fail**, and it fails them by
  arithmetic rather than by margin: a constant confidence ranks nothing, every
  correct×incorrect pair ties, ties count ½, so `AUROC = 500` **exactly** — 400
  permille short, at every error rate, for every constant.

**Therefore `R5` clause 2's conjunction reading is not a convenience at Layer 6;
it is the whole lower obligation, and it rests on one clause.**

### 3.3 …and that one clause is the one `§3.4` lets evaporate

`§3.4`: *"[AUROC] is **undefined** when `n_pos = 0` or `n_neg = 0` (report `n/a`;
any gate that cites AUROC requires both classes present)."*

`n_neg` is the count of **answered-and-wrong** queries. `§3.0` pays an engine to
turn exactly those into abstentions (0 → 100), and abstentions are outside the
denominator. So the better an engine is at the behaviour `§3.0` rewards, the
closer `n_neg` gets to zero — and at `n_neg = 0`:

* the **ascension** side's `AUROC ≥ 900` cannot be evaluated, so the clause
  carrying `R2` obligation 2 cannot be discharged;
* the **humility** side's ceiling `capped AUROC ≤ 600` is **vacuous rather than
  loose** — `README-l5 §4` named this seam already and this document only widens
  it from the humility side to both sides;
* `Brier` and `ECE` both go to 0 for *every* policy including the two
  capability-free ones, so the remaining clauses discriminate nothing either.

This is not hypothetical for this project. Every layer claimed so far reports
**`wrong = 0` and `fabricated = 0`** on every corpus it was scored against —
Layer 3 (`BOUNDARY.log` line 17), Layer 4 (line 23, including the murk and
chronicle diagnostics at C 695 / F 708 and 671 / 699), Layer 5 (line 32, F 1000
with its whole 35-answer slack unspent). The engine's standing behaviour is to
**abstain rather than err**, and `strain/l4::trial_murk_under_pressure_abstains_
rather_than_answering_from_a_shed_chain` makes that structural rather than lucky.
An engine whose entire recorded history is `n_neg = 0` is an engine for which the
Layer-6 gate, as ratified, has no defined AUROC on any corpus this repository has
ever frozen.

### 3.4 The predicted shape

Stated the way `[L4] [PULSE]` stated Layer 5's, so that it can be scored right or
wrong by the session that meets it:

> **Layer 6's Stage A will find `R2` obligation 1 discharged the ordinary way on
> every clause (no `R5`-shaped reading problem: `R5` clause 2 already settled the
> minimizing clauses and `R5`'s regularization already settled `B`), and `R2`
> obligation 2 undischargeable on `ECE` at any error rate, undischargeable on
> `Brier` outside a nine-permille band, and discharged **only over the
> conjunction, and only through `AUROC`** — which `§3.4` leaves undefined for
> exactly the engine this project has built. The session will therefore have to
> state a **corpus-and-battery precondition** — that both AUROC classes are
> non-empty on the ascension run *and* on the humility run — of exactly the kind
> `§5`'s own Layer-3 gate cell carries in the table (*"corpus: importance
> uniformly-to-late (never front-loaded)"*), expanded by `§5.1 L3` into a reason
> (*"…so a fill-then-refuse capped engine cannot exceed the 300 ceiling by
> luck"*), and which **neither `§5` nor `§5.1` states for Layer 6**. Layer 3 is
> the only layer whose ratified gate names a property its corpus must have; Layer
> 6 is the layer that needs one most and does not have one. The predicted stop is at that
> precondition, and the predicted ruling is **`R4`-shaped, not `R5`-shaped**: a
> reading *plus* a substrate, because unlike Layer 5 the reading is already
> ratified and it is the substrate that is missing.

**The half most likely to be wrong, named in advance so the miss is on the
record.** `§5.1 L6` says *"the harness scores it confident-by-default"* — so the
capped engine's confidence is supplied by the **harness**, not by the engine, and
its AUROC is therefore a property of a convention that lives in a `§5.1` defense
sentence rather than in `§3.4` or `§7.2`. If Stage A takes that convention
literally it inherits `AUROC = 500` for free and the humility ceiling is
discharged before it is measured; if it declines to, the capped engine has *no*
confidence to rank and AUROC is undefined for a third reason. Either way the
humility side of Layer 6 may turn out not to be a measurement of an engine at
all — and `R6` clause 1's insistence that both sides bind on **one** corpus is
what will make that visible.

---

## §4. Corpus candidacy — is the murk family the natural calibration substrate?

**Verdict: the substrate is right and the battery is missing.** `corpora/murk/`
is the natural home for Layer 6's *evidence*, and it does not, as currently
exercised, supply Layer 6's *denominator*.

### 4.1 Why murk is the natural evidence substrate

`§5 L6` asks for *"confidence permille from **structural evidence**"*, and
`§8.7`'s murk layer is the only frozen corpus whose defects are (a) injected on
purpose, (b) **always paired with an answer key** — *"no defect is ever injected
without being recorded"* — and (c) exactly the structures a confidence model
would read. Frozen instance `murk.s3003.n10000`, 10 000 events, 1 160 defects:

| family | count | the structural signal it offers |
|---|---|---|
| contradiction | **305** | a set-once key (`origin`) asserted twice with different values — two conflicting assertions the engine can *see* it holds |
| near-duplicate | **393** | a fact restated verbatim — corroboration, the evidence that should *raise* confidence |
| ambiguity | **205** | a retired entity id reused for a fresh spawn — one id, two incarnations, references after it genuinely underdetermined |
| malformed | **257** | a grammar-violating payload that is still canonical JSON — evidence the engine should refuse to answer from at all |

That is a signal for each direction confidence can move, with a frozen
`ground_truth.json` naming every event `t` each defect touches. No other frozen
corpus has an answer key at all, and `§8.8`'s single REAL corpus
(`real-sessions/v1`, 25 events) is three orders of magnitude too small to fill
ten ECE bins.

### 4.2 Why murk is not sufficient as currently queried

The measured fact, not a prediction: at Layer 4 the engine scored murk at
**C 695 / F 708 with `wrong = 0`, `fabricated = 0`** (`BOUNDARY.log` line 23) —
and the 305 permille of missing coverage are **abstentions, not errors**. murk
makes this engine *abstain*; abstentions are outside `§3.4`'s denominator; so on
murk-as-queried `n_neg = 0` and AUROC is undefined (§3.3). Worse for the F
clause: `F 708` on that battery is 242 permille below `§5 L6`'s `F ≥ 950`,
because each abstention costs 900 — so a Layer-6 battery cannot simply be
"murk's existing queries with confidences attached."

**What is missing is a query class that forces an answer where the evidence is
ambiguous**, and murk already contains two families shaped for it:

* **contradiction (305)** — ask for the current value of a set-once key the
  corpus contradicted. The engine's `current()` returns the later assertion; the
  answer key says the key is set-once, so one of the two is wrong under *any*
  declared reading. A forced-answer query with a ground-truth answer.
* **ambiguity (205)** — ask about a reused retired id. Two incarnations, one
  answer, the key knows which.

510 candidate error sources against a band that needs `w ∈ (41, 50]‰` (§3.2).
On a battery the size of Layer 5's (1 710 queries) that band is **71 to 85 wrong
answers** — so the substrate is roughly six to seven times richer than the band
needs, and the binding artifact is the **battery's clean-to-dirty mix**, not a
new corpus. A `≈95 : 5` composition is what `§5 L6`'s own `F ≥ 950` clause
forces.

**One caveat recorded so it is not rediscovered as a surprise:** murk is
currently an **ungated diagnostic** at Layer 4 under `R4` clause 1 (footprint
364‰ against 250, `C ≤ 754 / F ≤ 711`). That does not disqualify it for Layer 6 —
`§5 L6` states no footprint clause, and the inheritance class replays `§5 L4`'s
battery on `l4stream`, not on murk — but a Stage-A session should say so in its
own text rather than leave a reader to wonder whether a corpus can bind one gate
while diagnosing another. `R1` clause 5 and `R4` clause 1 both already do
exactly that for other corpora.

### 4.3 What `R2`'s discrimination check would demand of either choice

Of **murk-plus-a-new-battery** and of **a new frozen corpus** alike, `R2`
obligations 1–4 demand the same four things, and two of them are sharper at
Layer 6 than they have been at any previous layer:

1. **An oracle ceiling — with its policy class declared (`R5` clause 3), and here
   the declaration is load-bearing rather than a formality.** A confidence oracle
   that reads `ground_truth.json` attains `Brier 0 / ECE 0 / AUROC 1000` — a
   logical maximum over *all* policies, trivially exhibited, and **useless**,
   because `§5 L6` does not ask for confidence derived from the answer key; it
   asks for confidence derived from **structural evidence**. The family that
   matters is strictly smaller and its ceiling is strictly lower, and nobody
   knows by how much until it is exhibited. This is the Form-B pass-through
   lesson (`R5` clause 3) pointing the *other way*: at Layer 3 a sound ceiling was
   too **small** a family and an engine passed through it at 924 against 918; at
   Layer 6 the danger is a ceiling whose family is too **large**, making a gate
   look comfortably attainable when the reachable family may not reach it. `R4`
   clause 5 prefers an exhibited ceiling wherever a witness can be built — at
   Layer 6, *which* witness is the whole question.
2. **Every named capability-free baseline scored on the binding corpus.** §3.2
   names two that cost nothing to state and one of them (base-rate constant)
   **beats every real confidence model on ECE, permanently**. A Stage A that
   names only confident-by-default will report a discrimination that does not
   exist.
3. **The arithmetic recorded and machine-checked before the gate binds** — and at
   Layer 6 the recorded arithmetic must include the **error rate of the engine
   under test on the binding battery**, because that single number decides
   whether three of the five clauses discriminate at all (§3.2) and whether AUROC
   is defined (§3.3). No previous layer had a gate whose discriminating power was
   a function of the engine's own accuracy.
4. **The corpus binding is the human's.** Unchanged, and this document takes no
   step toward it.

---

## §5. The kept-promise finding, filed

`BOUNDARY.log` line 33 and `shell/dogfood/FIELD.md` (2026-08-01) record it as a
measured field note: **a promise is readable exactly as long as it is unkept.**
An armed intention's own `intend` episode is released at the door because the
pending entry regenerates it (`README-l5 §1.3`); firing consumes that derivation;
where the budget cannot take the episode back, it is booked into the forgetting
record and `read(t0)` abstains — while a still-**pending** intention beside it
stays byte-exact at the same cap. Keeping a promise is what destroys the record
of having made it.

**No current law is violated, and this section states that for the record rather
than raising it as a defect:**

* **`§5 L1`'s `F = 1000`** is a Layer-1 gate on Layer-1's battery **in budget**;
  under pressure, eviction is a lawful Layer-3 capability and the ascension and
  inheritance batteries both apply the Layer-1 identities only where there is
  room. `l5stream` at `DEFAULT_BUDGET` returns all 20 000 caller events
  byte-exact with `forgotten = 0` (line 32).
* **`§3.0`** scores the abstention correctly: the event is genuinely gone, the
  query is unanswerable, and abstaining earns 1000. The forgetting record is what
  makes it unanswerable *honestly* rather than silently —
  `strain/l3::trial_evicted_and_never_ingested_both_abstain_and_the_record_tells_
  them_apart` is the standing precedent and `strain/l5::trial_an_intention_
  survives_to_fire_or_its_loss_is_booked` is its Layer-5 form.
* **`§4.1`** holds: the budget law is asserted after every write with
  `refused = 0`.
* **`§5 L5`** scores firings, not `intend` events — which is exactly why the
  first Stage-C engine draft could lose 765 `intend` events without any clause
  noticing (line 32). The take-back rule exists because that was a **Layer-1
  regression**, not because a Layer-5 clause demanded it.
* **`§4.2`** is **dormant until Layer 7**.

**It is an L7-era provenance question, and this is its precise shape.** From
Layer 7 `§4.2` binds forever: every non-abstaining answer must carry a tag whose
`support` is *"[a list of] actually-ingested event `t`"*. `§4.2.3` validates the
tag's **shape** — ascending, non-negative, non-empty unless `kind == "absent"` —
and says nothing about whether the events it names are still **recoverable**. So:

> A fired event's answer cites its own `t` with `kind: "derive"`
> (`README-l5 §4`). The natural support for *"why did this fire"* is `t0`, the
> `intend` event — which is **actually-ingested**, so the tag is schema-valid,
> and **unrecoverable**, so the engine cannot produce what its own provenance
> names. `§4.2` permits this and does not discuss it.

Layer 5 is the **first layer at which an ordinary, lawful, in-gate execution
reaches that gap.** At Layers 3 and 4 a forgotten event's `t` could also be cited
in principle, but the answer that would cite it is an answer *about the forgotten
content*, and the engine abstains — so the tag is never built. At Layer 5 the
fired event is **answerable** (its own `t`, held or regenerable) while its causal
antecedent is not: the first case where a produced, correct, scored answer's
natural support names an unrecoverable `t`. The question for the Layer-7 session,
recorded here and ruled on by nobody:

> **Must a `support` entry be recoverable, or only ingested?** If recoverable,
> Layer 7 forbids a shape Layer 5 lawfully produces today and the interaction is
> a design constraint on the L7 engine. If only ingested, then provenance at
> Layer 7 certifies *that* an answer had a source and not *that the source can be
> shown* — which is a weaker claim than `autopsy/GAPMAP.md §2`'s *recorded but
> never binding* thesis was written to demand of everyone else, and the project
> should say so in its own documents before it says it about anyone else's.

---

## §6. What this document does not do

No gate binds. No corpus is named as a substrate. No threshold moves, in either
direction, on any layer. No ruling is drafted and none is proposed for appending
— appending is what freezes, and a `PULSE` has no business near it. `R2`'s
standing step is untouched: a Layer-6 `ASCEND` still owes its own
`ATTAINABILITY.md` with the arithmetic computed, recorded and machine-checked
before any Layer-6 gate acquires authority, and every number in this file is
prose that such a file would supersede.

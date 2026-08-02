# STAGE-B.md — the Layer-6 Stage-B record: the batteries, the denominator, the restraint

`[L5] [ASCEND]` meta-memory, **Stage B**. `BOUNDARY-RULINGS.md R2`'s standing step
orders an ascension *attainability arithmetic → trials → engine*, and this is the
middle step: the ascension battery, the humility battery and the inheritance
battery are written and run against an engine that **does not exist**, so that no
threshold, no reading and no denominator can be tuned to something an engine
already does.

`core/layers/l6_meta_memory.py` does not exist. `trials/adapters/l6.py` does not
exist. The standing checkpoint this session leaves behind is the one Layers 4 and
5 left behind at the same point: **humility green + ascension skipped**.

**Nothing here asks a human for anything.** `R7` is ratified and settles the
substrate, the denominator, `AUROC`'s domain and both readings; §7 records
explicitly that this session found no binding gap R7 does not cover, and drafted
no `R8`.

---

## §1. What Stage A left, and what only Stage B can add

Stage A round 2 scored **policies**: pure maps from declared evidence to an
integer permille, computed from the frozen artifact with no engine in the loop.
`R7` clause 1 then bound both sides of the Layer-6 gate to `corpora/l6batteryb`.
What a policy cannot exhibit, and what these batteries are for:

1. **`§7.2`'s `confidence` field stops being decorative.** `§3.4` is dormant
   until Layer 6, so every engine this project has frozen emits a confidence
   nobody scores. From here the harness reads that field — and reads it as the
   **integer permille** `§7.2` declares. `_l6score._ask` refuses a float, a
   `bool` and an out-of-range value: a confidence that is not a permille is a
   harness-level failure and not a low score (`§7.3`'s categorical distinction),
   and `§2.2` forbids the float independently of anything Layer 6 wants.
2. **`B = 1000` after every write.** A confidence model is state (`§4.1`), priced
   at 18 cells beyond the frozen Layer-5 state by `ATTAINABILITY-B.md §3.2`. The
   budget law refuses mid-stream, so it is certified mid-stream.
3. **The forcing region is asked of an engine.** A policy could be *declared*
   class E; an engine has to *be* it, and `§2.1`/`§2.3` make an engine a pure
   function of the frozen bytes. Theorem 2 then says an engine right on **both**
   members of a mirror pair read something it was never handed.
4. **The layers below are re-asked at cap 6** (`trials/inheritance/l6/`),
   including — new at this layer — `§5 L5`'s prospection battery. Nothing in
   `ascension/l6` scores a firing, so that is the only place a Layer-6 engine
   that paid for its calibration out of prospection goes red.

## §2. The declared query vocabulary

Both artifacts speak two query shapes, and both are **Layer-4 verbs**:

| | query | answer |
|---|---|---|
| **current** | `{"op":"current","entity":E,"key":K}` | the value in force at the end of the stream |
| **asof** | `{"op":"asof","entity":E,"key":K,"t":T}` | the value in force at `T` |

That is deliberate, and it is `§5 L6`'s own distinction: the layer asks for
*"confidence permille from structural evidence"* — a **confidence model, not a
second reader**. The battery therefore asks questions the layer below already
answers and scores the confidence attached to them. On `corpora/l6batteryb` the
choice is load-bearing rather than stylistic: the forcing region is exactly the
class no reader can get right, so a battery that rewarded a better answer there
would be rewarding an engine that had read the answer key.

`ops/l6/t_stage_b.py::trial_the_declared_query_vocabulary_is_the_one_the_battery_speaks`
asserts the vocabulary over the frozen records of both artifacts, engine-free.

## §3. The denominator law, applied (`R7` clause 2)

> *Abstentions are outside the calibration denominator, and the exclusion is
> stated rather than inferred.*

`§3.4`'s `A` is the count of **answered** queries. An abstention contributes to
`§3.0`'s fidelity and to no calibration quantity. `_l6score.DENOMINATOR` carries
the per-class declaration with its reason, for **both** artifacts — a demotion is
a change of authority and not of duty — and `_l6score.assert_denominator_declared`
reconciles the reported `A` against it on every scored run:

| artifact | class | in `§3.4`'s denominator | why |
|---|---|---|---|
| `l6batteryb` | **K0** forcing, 200 | yes | answerable, and the whole region unsampled; a committing engine's answers land in `A` and exactly one member of every committed pair is wrong |
| | **K2** current-value, 1 400 | yes | answerable |
| | **K3** as-of, 600 | yes | answerable |
| | **K4** absence probes, 200 | **no** | unanswerable: the only correct behaviour is an abstention, and an abstention carries no confidence to calibrate |
| `l6battery` | **K1** commitment, 355 | yes | answerable, and the whole class |
| | **K2** 2 130 / **K3** 1 065 | yes | answerable |
| | **K4** 355 | **no** | for battery-b's reason, in the artifact that first stated it |

A class declared outside is **not a hiding place.** An engine that answers one has
fabricated, and a fabrication enters `A` as an error exactly as
`_l6btasks.score` scores it — being outside the denominator is a property of the
honest behaviour, not an exemption from measurement. `ops/l6/t_stage_b.py`
asserts the other half engine-free: *outside* means *unanswerable* and never
*inconvenient*, class by class, on both artifacts.

**`F`'s denominator is the answerable core**, and that is the stricter of the two
available. Every piece of the ratified band arithmetic is stated in it (`R7`
clause 3(c): `1000w ≤ 50` with `w = (r/2)/A`, and the hedging ladder
`F = (21000 − 8k)/22000`), and the exhibited witness's `955` is that number.
`F` over the whole 2 400-query set reads `958` — the 200 unanswerable probes pay
1000 apiece for an abstention — and is computed and reported as the **ungated
diagnostic**. A battery that gated on the looser one would be spending a margin
the window arithmetic never granted.

## §4. `AUROC = n/a` DISQUALIFIES, asserted as law (`R7` clause 3(a))

`trial_auroc_clears_the_gate_and_an_undefined_auroc_disqualifies` is the clause
written as the entry writes it, not as a paraphrase of it. The rule is stated as
law and not as a preference — **n/a DISQUALIFIES; it does not excuse the
clause** — so **an engine whose battery-b scores yield `n_neg = 0` fails**, and
the trial's failure message says why in `R7`'s own words:

> *A gate is an instrument. An instrument has a range, and outside it the honest
> output is not a pass but a refusal to certify: a balance that reads `----`
> under an out-of-range load has not weighed the object, and nobody records the
> `----` as a weight.*

The ground is a defect this project published about somebody else.
`autopsy/writ/ANATOMY.md` records that declaring a capability false sets the
score `null`, and null is dropped from **both** numerator and denominator
(`evaluator.ts:545-548`, `docs/metrics.md:204`) — a system exempts itself exactly
where `make_engine(layer_cap = N−1)` is scored against a ceiling. A project that
published that finding cannot write the same exemption into its own gate.

On this artifact the reading **costs nothing**, which `R7` clause 3(d) records
and this battery does not have to re-derive: every policy that clears `§5 L6`'s
own `F` clause leaves `n_neg ≥ 87`
(`t_attainability_b.py::trial_no_policy_clearing_f_can_reach_n_neg_zero`), and an
engine that answers everything correctly cannot exist, because the resolving coin
is not in the stream. So an engine reaching `n_neg = 0` has either broken `F` —
caught by its own clause — or resolved the forcing region, which is the answer
key.

## §5. The restraint, recorded now rather than discovered later

`ATTAINABILITY-B.md §3.1` prices the forcing region at **500**, the tie's own
arithmetic — `permille(1/2)`, derived and not chosen — and the exhibited witness
does the same. **This battery does not require it.**

`§5 L6` gates `Brier`, `ECE`, `AUROC`, `F` and `B`. It does not ratify a
confidence value on a query class, and an engine that priced the region at 480 or
520 and still cleared all five clauses would have cleared the ratified gate.
Requiring 500 would gate a **policy** where the constitution **gates a score**.

That is the Layer-5 Stage-B lesson applied before it cost anything: there a first
draft asserted `wrong = 0` beside `F ≥ 980`, a mock engine firing everything
correctly with one wrong payload scored `F 999` and cleared the ratified gate,
and the assertion `§5 L5` does not make was dropped — `R5` clause 1 records the
ratified slack as the constitution's own answer to `R2`'s perfection objection.
The region's confidences are therefore **computed and reported on every run** and
required only where `§3.4`'s own arithmetic already forces them.

Three things in the battery **look** like additions and are not:

* **no pair is resolved.** This is not a tightening of `§5 L6`; it is the class
  boundary `R7` clause 3(b) draws. An engine right on both members of a mirror
  pair obtained the coin from the answer key, and a gate it cleared measured
  nothing. It is the one check here that catches an engine for being *too good*.
* **`region_wrong ≥ committed`.** Theorem 1 gives one error per committed pair as
  a floor. Asserting it is asserting the theorem of the frozen bytes, not a
  demand on the engine.
* **`fabricated = 0`.** `§7.3` is the cardinal rule and `§3.0` prices a
  fabrication at 0 while paying 1000 for the abstention it displaced. The
  battery states it; the price list already did.

## §5.1 The battery was validated against a MOCK `§7` engine before it was frozen

A fully engine-gated battery is a battery nobody has run, and a gate never shown
attainable is exactly what `R2` exists to prevent. So the Layer-5 Stage-B
discipline was repeated: a mock `§7` engine — the frozen Layer-5 engine wearing
the exhibited witness's confidence model, `set_once_tie -> 500` and 1000
otherwise — was bound as `adapters.l6` **in the scratchpad, never committed**, and
the whole of Stage B was run against it.

* **Clean mock: every ascension trial GREEN**, every inheritance trial GREEN at
  cap 6, and `humility/l6`'s `§7.4` confirmation GREEN. That is the check that
  matters — a battery the exhibited witness could not clear would be measuring
  something `ATTAINABILITY-B.md` never showed reachable.
* **Four deliberate breaks, each RED on the right trial**:

| break | what goes red |
|---|---|
| the mock **resolves** the forcing region (reads the key) | the region trial (100 pairs resolved), `ECE` at 45, **and** the `AUROC` domain — `n_neg` falls to 0 and `n/a` disqualifies |
| the mock **hedges** the region (`§3.0`'s incentive) | `F` at 918, and the `AUROC` domain at `n_neg = 0` |
| the mock states a **constant** 1000 | `Brier` at 45 and `AUROC` at 500 — the capped engine's own failure, reproduced |
| the mock returns a **float** confidence | every trial, at the `§7.2` read: a confidence that is not an integer permille is a harness-level failure and not a low score |

Two things that came out of the breaks are worth recording rather than
discovering later. The **hedger is killed by `F` and not by the region trial** —
hedging the whole region leaves nothing committed, so the region trial is
correctly silent and `§5 L6`'s own fidelity clause does the work, which is `R7`
clause 3(d)'s arithmetic and not a second instrument. And the **resolver is
caught three ways**, one of which is `ECE`: an engine that reads the key answers
the region correctly while still pricing it at 500, so its bin 5 carries a mean
confidence of one half against an accuracy of 1. The `n/a` disqualification is
therefore not only the hedger's clause — it is also what stops a cheating engine
from clearing a gate on an empty denominator.

## §6. The recorded figures

Measured this session on `adapters/l5` — `make_engine(layer_cap = 5)`, the capped
engine — through `§7` alone, and identical to `t_attainability_b.py`'s
`confident-always` policy row, because `ATTAINABILITY-B.md §4.2` establishes that
that row **is** the capped engine rather than a model of it. Recomputed and
required verbatim by `ops/l6/t_stage_b.py::trial_stage_b_records_the_figures_the_instrument_computes`;
under `R6` clause 3 the instrument is the enforced value.

```
CAPPED brier 45 ece 45 auroc 500 F_core 955 F_all 958
DENOM A 2200 n_pos 2100 n_neg 100 N 2400
REGION pairs 100 forcing_queries 200
```

The capped engine's occupancy at `DEFAULT_BUDGET` is 91 119 with `refused = 0` —
the baseline `ATTAINABILITY-B.md §3.2`'s 18-cell price is stated against — and its
confidence vocabulary through `§7.2` is exactly `{0, 1000}`. The ceiling is
`capped AUROC ≤ 600`: **neither breached nor vacuous**, sat at from below by
arithmetic, and 400 permille short of the gate. `humility/l6/IMPOSSIBILITY.md` is
the structural argument `§6` requires for it.

The inheritance identities were verified attainable before being frozen, by
measuring `adapters/l5` at the same in-budget cap the cap-6 battery will use:
`precision = recall = 1000`, `dup-fire = miss = 0`, `F = 1000`, `refused = 0`,
`B = 1000` on `corpora/l5stream` at 4× its own raw episodic footprint. A battery
whose identities no engine had ever been shown to reach would be a battery that
had never been checked.

## §7. No `R8` is drafted, and the absence is reported rather than left unstated

The directive's fourth item is conditional: *only if a genuine binding gap
surfaces that `R7` does not cover*. **None surfaced.** Every question this
session had to answer was already answered, and by whom is worth recording,
because the whole point of `R2`'s ordering is that Stage B should not be
discovering law:

| what Stage B needed | where it was already settled |
|---|---|
| which artifact both sides bind on | `R7` clause 1 |
| what happens to `corpora/l6battery` | `R7` clause 1 — demoted, ungated, still scored |
| whether an abstention is inside `§3.4`'s denominator | `R7` clause 2 |
| what `AUROC = n/a` means for a gate | `R7` clause 3(a), with 3(b)'s theorem and 3(c)'s window |
| exact or permille | `R7` clause 4 |
| which bin an integer permille falls in | `R7` clause 5 |
| how `R2`'s two obligations are read at this layer | `R5` clauses 1–4, forward-binding in their own text |
| what a firing does to `next_t` on the inherited Layer-5 row | `R6` clause 2 |
| whether `F` takes a concession under eviction | `R3` does not reach Layer 6, and none is requested |

Two items are **open and deliberately not taken**, both by the ruling's own
words, and neither is a gap in `R7`:

* **what an engine owes when the budget sheds the evidence a confidence model
  reads.** `R7`'s *"what this ruling does not do"* names it and leaves it to
  Stages B and C; `ATTAINABILITY-B.md §3.2` disclaims the loss reserve with that
  reason. Stage B does not take it either, and the reason is that it is an
  **engine design** question and not a reading: the artifact is scored in budget,
  where nothing is evicted, so no battery here can measure an answer to it. What
  is recorded for Stage C is the shape of the failure — *a model reading a table
  that has forgotten a tie would be confident **at 1000 on a coin flip**, which is
  the worst failure available to this layer.*
* **the `§3.0`/`§3.4` price-list tension**, which `R7` clause 7 records *for
  Layer 7's eyes* and rules on by nobody. Nothing at Layer 6 needs it: the
  collision is closed on this artifact by arithmetic.

## §8. Where Stage B lives

| file | what it carries |
|---|---|
| `trials/_l6score.py` | the shared instrument: replay, `§7.2`-enforcing observation, the `§3.4` triple and `§3.1` fidelity, the denominator declaration, the region profile. Imports its measures from `_l6tasks` unchanged — one ruler for an engine and a policy |
| `ascension/l6/t_meta_memory.py` | the gate on `corpora/l6batteryb`, **all engine-gated skips** |
| `humility/l6/t_meta_memory.py` + `IMPOSSIBILITY.md` | the ceiling on `make_engine(5)`, **green this session** |
| `inheritance/l6/t_inheritance.py` | Layers 1–5 re-asked at cap 6, in budget — engine-gated, plus the class's engine-free wiring check |
| `ops/l6/t_stage_b.py` | the half of Stage B that can be run without an engine: one instrument, the bin reading, the vocabulary, the denominator declaration, this document |

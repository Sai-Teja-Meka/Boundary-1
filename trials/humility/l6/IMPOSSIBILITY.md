# IMPOSSIBILITY.md — why `make_engine(layer_cap = 5)` cannot reach the Layer-6 ceiling

`BOUNDARY.md §6` requires every humility trial to ship a **structural** argument —
not an empirical observation — for why the capped engine cannot exceed its
declared ceiling. The ceiling is `§5 L6`'s:

```
capped AUROC ≤ 600
```

and the measurement, on `corpora/l6batteryb` at `DEFAULT_BUDGET`, is **500**,
against an ascension gate of 900.

**The artifact is bound, both sides, by one clause.** `BOUNDARY-RULINGS.md R7`
clause 1 binds the Layer-6 ascension gate **and** this ceiling to
`corpora/l6batteryb`, for `R6` clause 1's reason: a ceiling measured on one
artifact beside a gate cleared on another is two facts about two worlds.
`corpora/l6battery` is demoted to an ungated diagnostic by the same clause, and
nothing here is measured there.

---

## §1. The two prongs, both measured

`R5` clause 4 is the reason both are here rather than the flattering one alone:
*"an unpriced item is not a saving; it is a margin that has already been spent"*,
and the Layer-5 document's first draft was refuted by its own mandatory
measurement. Both of these are asserted by
`t_meta_memory.py`, on the engine, through `§7`.

### Prong 1 — the confidence the capped engine emits is a CONSTANT PAIR

Over all 2 400 queries the distinct confidences `make_engine(5)` returns through
`§7.2` are exactly

```
{ 0, 1000 }        1000 on every answer, 0 on every abstention
```

This is **the engine's own field**, not a harness convention, and that matters
more than it looks. `§5.1 L6` defends this ceiling by saying the harness scores a
capped engine *"confident-by-default"*, and the `[L5] [PULSE]` pre-read
(`BOUNDARY.log` line 34) named that sentence the half of its prediction most
likely to be wrong: a convention living in a defense sentence, taken literally,
would hand the ceiling its number before anything was measured, and declining it
would leave the capped engine with no confidence to rank at all. Neither branch
is taken, because neither is needed. The engine fills the field itself, and
`README-l5 §4` wrote down why one layer early:

> *"Every answer this engine returns carries `confidence = 1000`, and it is
> ungated (§3.4: calibration is dormant until Layer 6). That is not a placeholder
> an engine could tighten; it is what the state can support. … There is no
> quantity in this state that varies with how likely an answer is to be right,
> because every answer it gives is one it has proved."*

### Prong 2 — `AUROC` is exactly `1/2`, and it is sat at rather than approached

`§3.4` defines `AUROC` as the Mann–Whitney statistic: `U` counts, over all
correct×incorrect answer pairs, those whose correct answer carried the **higher**
confidence, with ties counting ½. A constant confidence makes **every** such pair
a tie, so

```
U = ½ · n_pos · n_neg        AUROC = U / (n_pos · n_neg) = 1/2   exactly
```

with `n_pos = 2 100` and `n_neg = 100` on this artifact. The ceiling of 600 is
therefore not approached from below by a poor model; it is **arithmetic**, and
the 100 permille between 500 and 600 is slack the constitution left and this
engine cannot spend.

## §2. The structural argument: emitted is not calibrated

A constant is a value, not a model. Written out, the capped engine's confidence
function is

```
conf(q)  =  1000  if the engine answers q
            0     otherwise
```

— a function of the **status** of the answer and of nothing else. It reads no
evidence, because there is no evidence for it to read: `§3.4` is dormant below
Layer 6, so nothing in the frozen Layer-5 state was ever built to vary with the
likelihood that an answer is right. `README-l5 §4` states the boundary in the
engine's own terms and it is exact: *"the evidence this layer keeps is binary —
an event is regenerated exactly or it is not; an intention has fired or it has
not; a fold is exact or its entity is damaged."*

`AUROC` is a **ranking** statistic, and ranking is precisely what a constant
cannot do. Three sentences and the ceiling is closed:

1. a constant assigns the same confidence to every answered query;
2. so every correct×incorrect pair ties, and `§3.4` counts a tie as ½;
3. so `AUROC = 1/2` for **any** constant, at **any** error rate, on **any**
   artifact where both classes are non-empty.

Nothing about the artifact enters steps 1–3. What the artifact has to supply is
only that the two classes are non-empty — which is §3's subject.

## §3. Why the ceiling is not vacuous, and why no reading available to the capped engine moves it

A ceiling stated on `AUROC` is a ceiling only where `AUROC` is defined, and
`README-l5 §4` said so before this battery existed:

> *"the honest residual is that `§3.4` makes AUROC **undefined when either class
> is empty** — so `humility/l6/IMPOSSIBILITY.md` will have to say what a battery
> does with an engine whose answers are all correct … **the Layer-6 humility
> battery needs a query class this engine gets wrong**, or its ceiling is vacuous
> rather than loose."*

That query class is the **forcing region** of `corpora/l6batteryb`, and this is
where the argument stops being about constants and becomes about the artifact.
The region is 100 **mirror pairs**, and the capped engine errs on **exactly one
member of every one of them** — 100 errors, measured, all of the engine's error
mass, because the base stream is clean by construction.

The two properties that make those 100 errors unremovable are theorems of the
frozen bytes, proved in `corpora/l6batteryb/README.md §3` and machine-checked by
`trials/ops/l6/t_l6batteryb.py` — this document cites them and does not restate
their proofs:

* **Theorem 1 (the tie).** The two members of a pair have equal event histories
  once the entity id is blanked, with logical times differing by exactly `+1` at
  every position, and one member's truth is its FIRST `origin` assertion while
  the other's is its LAST. So any reader that does not read the raw entity id or
  an absolute `t` returns the same value for both and is wrong on exactly one.
  Exhibited against a bench of six readers built to break it — `latest-wins`,
  `first-wins`, `canonical-min`, `canonical-max` and two id-keyed rules — **every
  one measuring exactly 100**.
* **Theorem 2 (the withholding).** Regenerating the artifact with every coin bit
  flipped produces a **byte-identical stream** and an answer key differing on all
  200 forcing queries. The stream carries **zero** bits about the coin, and the
  two handles Theorem 1 leaves — the raw id and the absolute `t` — are closed by
  the coin's **balance**: a rule keyed on either takes both members of a pair or
  neither, and is right on exactly half.

The capped engine is the bench's `latest-wins` reader; `core/layers/
l4_consolidation.current()` is exactly that, and `ops/l6/t_l6batteryb.py`
measures the frozen Layer-5 engine agreeing with the declared reader on every one
of the 2 400 queries. **So no reading of the frozen bytes available to the capped
engine moves the number.** Not first-wins, not canonical-min, not an id-keyed
rule: the bench measures 100 for all of them, and a rule that did better would
have obtained the coin, which is in the answer key and in the generator and in no
function of the stream.

That is the round-2 strengthening, and it is why round 1's artifact was demoted
rather than kept. There the ceiling was defined **for the declared latest-wins
reading**, and a first-wins reader would have answered the whole commitment class
correctly and taken `AUROC` with it (`ATTAINABILITY.md §6`). Here the ceiling is
defined for every reader definable from the stream, so the capped engine sits at
500 not because it reads the artifact one particular way but because **every way
of reading it is worth the same 100 errors**.

## §4. Which argument this is NOT making, and saying so is the honest part

`humility/l4/IMPOSSIBILITY.md §3` argues an **information-theoretic**
impossibility: thousands of distinct evicted payloads map into an aggregated
forgetting record of at most 35 integer cells, so no injective map exists and the
answers are unreachable in principle. `humility/l5/IMPOSSIBILITY.md §4` argues an
**absence of machinery**: in budget the capped engine holds every intention
byte-exact and still fires nothing, because it has no operation that consults a
stored condition on the write path.

**Layer 6 is the third kind, and it is neither of those.** Nothing is missing
from the state and no operation is absent from the write path: the capped engine
**holds both halves of every tie** — both `origin` assertions of both members of
every mirror pair, returned byte-exact by `read(t)` — and answers `current` on
all 200 forcing queries without hesitating. It is not short of information and it
is not short of a verb. It is short of a **ranking**: a quantity that varies with
how likely its own answer is to be right, which is what `§5 L6` calls *confidence
permille from structural evidence*.

Stating which of the three applies is what keeps the `§6` obligation from
degenerating into a template. It also names the layer in one line:

> **Confidence emitted is not confidence calibrated.**

The capped engine emits a confidence on every answer and always has. `§3.4` was
dormant, so nobody scored it; Layer 6 scores it, and the field turns out to carry
no information at all. That is the boundary, and it is the reason `§3.4` binds
from Layer 6 and stays bound above it.

One consequence is worth recording because it is the shape of the whole layer:
the capped engine **clears two of the five clauses**. `F = 955` against 950 and
`B = 1000` — it answers 2 100 of 2 200 answerable queries correctly, abstains on
all 200 unanswerable ones, fabricates nothing and holds the budget. It fails
`Brier`, `ECE` and `AUROC`. A Layer-6 gate stated on fidelity would have been
cleared by an engine with no meta-memory whatsoever, and `§3.0` could not have
told the difference: it is **confidence-blind**, scoring a calibrated hedge and a
confident lie identically. That is the collision `R7` clause 7 records for Layer
7's eyes, seen from the humility side.

## §5. What would falsify this argument

Stated so the argument is refutable rather than decorative. The ceiling claim
fails if any of these becomes true:

* `make_engine(5)` emits a **third** confidence value through `§7.2` on any
  corpus — a confidence model would then exist below Layer 6, where `§3.4` is
  dormant and `README-l5 §4` says the state cannot support one;
* the capped engine's `AUROC` on this artifact is anything other than exactly
  `1/2` while its confidence remains constant — that would be an arithmetic
  error in `§3.4`'s tie convention, not an engine improvement;
* `n_neg` on the capped run reaches 0, which would make `AUROC` undefined and the
  ceiling vacuous rather than loose — Theorems 1 and 2 forbid it, and `R7`
  clause 3(b) is the standing requirement that every artifact a gate citing
  `AUROC` binds on must forbid it;
* the capped engine **resolves** a mirror pair — right on both members — which by
  Theorem 2 means it read something that is not in the stream.

## §6. Where this is enforced

* `trials/humility/l6/t_meta_memory.py` — the ceiling against `make_engine(5)` on
  the whole 12 000-event artifact through the generic interface (`AUROC 500 ≤
  600`, and strictly below the gate's 900); the constant pair read off `§7.2`
  itself; the three-failed / two-cleared split of `§5 L6`'s clauses; the
  denominator (`A 2 200`, `n_pos 2 100`, `n_neg 100`) and the region profile with
  no pair resolved; the budget law and the recorded occupancy; and the
  engine-gated `§7.4` confirmation against the Layer-6 engine *capped to 5*,
  which skips until Stage C.
* `trials/ascension/l6/t_attainability_b.py::trial_the_capped_engine_is_measured_and_the_ceiling_is_neither_breached_nor_vacuous`
  — the same 500, from the arithmetic side, since Stage A: the `confident-always`
  row of that scoreboard **is** `make_engine(5)`, measured and not modelled.
* `trials/ops/l6/t_l6batteryb.py` — Theorem 1's premise, the balanced coin, the
  six-reader bench, Theorem 2, and the frozen Layer-5 engine agreeing with the
  declared reader on all 2 400 queries while emitting `{0, 1000}`.
* `trials/laws/t_rulings.py` — `CEILING_AUROC = 600` bound to its `§5 L6` clause
  and to `R7`, whose clause 1 binds this ceiling and the ascension gate to
  `corpora/l6batteryb` together.

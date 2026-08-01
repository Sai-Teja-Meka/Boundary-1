# `corpora/l6batteryb` — battery-b, and the forcing region

`[L5] [ASCEND]`, Layer-6 Stage A **round 2**, 2026-08-01. Frozen instance
**`l6batteryb.s9009.e12000.q2400.json`** (seed 9009, 12 000 events, 2 400
queries, 888 897 bytes).

**No gate binds on this artifact.** `trials/ascension/l6/ATTAINABILITY-B.md`
computes the Layer-6 arithmetic on it and `RULING-R7-DRAFT.md` asks a human
whether it should bind; appending a ruling is what freezes, and this session does
not append. `laws/t_rulings.py` carries the six `§5 L6` constants twice — once
for each round's arithmetic — with a `§5` clause and **no companion ruling**,
which is what *"no gate binds"* looks like in that registry.

---

## §1. Why it exists: round 1's measured limit

`corpora/l6battery` was frozen one session earlier and was the right shape. It
supplied `§3.4` with a **calibration denominator** where murk-as-previously-
queried had none: `n_neg` went from 0 to 158 and `AUROC` became computable for
the first time in this project's history.

It also measured its own limit, and recorded it rather than hiding it:

> *"On murk, **evidence that ranks also resolves**. A reader that used the same
> structural evidence to answer rather than to hedge would take `origin`
> first-wins, score `n_neg = 0`, and take AUROC with it. So this battery's 158
> errors are the errors of the **declared latest-wins reading**, and its
> guarantee is relative to that reading."*
> — `corpora/l6battery/README.md §4`

The cause is `§8.7` itself: the murk doctrine pairs every injected defect with
its answer key **and injects it by visible construction**, so a stream-only rule
recovers each family exactly — symmetric difference **0** on all four. A corpus
whose dirt is always recoverable cannot contain a query class where the evidence
says *"this is risky"* without also saying *what the answer is*.

That is the defect battery-b removes, and it removes it the only way available:
by generating a substrate whose ambiguity is **irreducible**, with the resolving
signal **withheld at generation**.

## §2. The forcing region

`PAIRS = 100` **mirror pairs**, `r = 200` forcing queries. For pair `p`:

* two entities `e0 = 500000 + 2p` and `e1 = e0 + 1`, spawned at **adjacent**
  logical times with the **same** class;
* each receives exactly **two** `origin` assertions carrying the **same ordered
  value pair** `(x_p, y_p)` with `x_p != y_p`, emitted at adjacent logical times,
  so the two members share one gap schedule;
* **nothing else ever touches either entity.** Region ids are allocated outside
  the base world, so no link, move or retire can reach them. Each member's
  ENTIRE event history is `[spawn, attr origin x, attr origin y]`;
* a **withheld coin** `b_p` decides which member's FIRST assertion is the true
  `origin`:

  ```
  b_p = 0  ->  true(e0) = x_p (its FIRST)   true(e1) = y_p (its LAST)
  b_p = 1  ->  true(e0) = y_p (its LAST)    true(e1) = x_p (its FIRST)
  ```

  The coin is **balanced** — exactly 50 pairs each way — and is shuffled from the
  same PRNG **after** the stream is complete.

`origin` is asserted by nothing else in this corpus: the clean base draws its
attribute keys from the chronicle vocabulary, which carries no set-once key. So
every `origin` chain in the frozen stream is a region chain and the region is
perfectly **identifiable**.

**Identifiable is not resolvable, and the difference is the design.** An honest
engine must be able to SEE a tie in order to price it at the tie's own
confidence; what it must not be able to do is break it. Round 1's substrate got
this exactly backwards: its evidence resolved as well as it ranked.

## §3. The tie, proved

### Theorem 1 — the tie

*The two members of a mirror pair are observationally identical, and their truths
sit at opposite ends of their chains. Therefore every reader that does not read
the raw entity id or the absolute logical time is wrong on **exactly one** member
of **every** pair: exactly `PAIRS = 100` errors on the region, under either coin.*

**Proof.** By construction each member's complete event history is `[spawn, attr
origin x, attr origin y]` and nothing else in the stream mentions it. Blank the
entity id and the two members' histories are **equal as sequences**; their
logical times differ by exactly `+1` at every position. So for any query function
`R` of the stream that does not read the id or an absolute `t`, `R` receives
identical input for the two members and returns the same value. One member's
truth is its first assertion and the other's is its last (the coin assigns
exactly one of each per pair), and the two assertions carry different values, so
`R` is right on exactly one and wrong on exactly one. ∎

Asserted, not argued:
`t_l6batteryb.py::trial_the_two_members_of_every_mirror_pair_are_observationally_identical`
(histories equal, times `+1`, three events each),
`::trial_exactly_one_member_of_every_pair_is_first_true_and_the_coin_is_balanced`,
and — **exhibited against readers built to break it** —
`::trial_every_reader_on_the_bench_errs_on_exactly_one_member_of_every_pair`,
which scores `latest-wins`, `first-wins`, `canonical-min`, `canonical-max` and
two id-keyed rules and measures **100 errors for every one of them**.
`first-wins` is the specific reader that made round 1's guarantee relative: on
`corpora/l6battery` it would have answered the whole commitment class correctly.

### Theorem 2 — the withholding

*The frozen stream is byte-identical under the coin and its complement, while the
answer key differs on every one of the 200 forcing queries. Therefore the stream
carries **zero** bits about the coin, and a policy that resolves the region has
obtained the coin from the answer key — which is class **O** by definition.*

**Proof.** `generate_full` builds the region layout and the whole 12 000-event
stream **before the coin is drawn**, and the stream path never reads it;
`complement=True` flips every bit afterwards and touches nothing else.
Regenerating both ways produces the same stream bytes and an answer key whose
value differs on every forcing query and on no other query. ∎

Asserted by `::trial_the_stream_is_byte_identical_under_the_coin_complement` and
— the consequence, on the policies that matter —
`::trial_every_class_e_policy_is_unmoved_by_the_coin_complement`, which requires
every class-E policy's answers, confidences and every one of its scores to be
**identical** under the flip while the SET of its region errors is exactly
complemented. `n_neg` does not move; the 100 errors are a different 100.

### What the two theorems close between them

Theorem 1 leaves exactly two handles: the **raw entity id** and the **absolute
`t`**. Theorem 2 shows neither carries signal, because the coin is independent of
the stream — and the coin's **balance** makes that concrete rather than abstract:
a rule keyed on id parity or emission order takes both members of a pair or
neither, and is right on exactly half the pairs, which is 100 errors again. Both
id-keyed readers on the bench measure exactly that.

The declared evidence vocabulary (`trials/_l6btasks.FEATURES`) therefore
**excludes** the raw id and the absolute `t` deliberately — not to flatter the
theorem, but because including them would let a class-E policy split a pair while
buying it no reachable score, and excluding them buys the property that makes the
class meaningful: every feature is **equal** on the two members of a pair, so a
class-E policy cannot tell them apart. That is asserted too.

**Consequence.** `n_neg >= 100 > 0` for first-wins, last-wins and every other
policy definable from the stream. `AUROC` is defined **by theorem**, not relative
to a reading a session declared.

## §4. The band, redone

With `w` the wrong share and `a` the abstained share of the answerable core,
`§3.0` gives `F = 1000 - 1000w - 900a`. Theorem 1 pins `w = (r/2)/A` for **any**
committing reader, so the following is a property of the artifact and not of a
policy:

| requirement | arithmetic | window |
|---|---|---|
| the honest committer clears `F >= 950` | `1000w <= 50` | `A >= 10r` |
| blanket abstention on the region **breaks** `F >= 950` | `900(r/A) > 50` | `A < 18r` |
| `Brier <= 40` beats the base-rate constant | `w(1-w) > 40/1000` | `A < (25 + 5*sqrt(21))/4 * r ≈ 11.978r` |

**`A = 11r = 2200`** sits inside all three, with 1 r of margin below and 0.978 r
above. The irrational bound is checked as the exact rational predicate
`25u² - 50u + 4 < 0` in `u = r/A`, never as a float (§2.2).

## §5. The four classes

| class | n | query | answer key | in `§3.4`'s denominator |
|---|---|---|---|---|
| **K0** forcing | 200 | `current(e, "origin")`, the whole region, **unsampled** | the WITHHELD-coin value | **yes** |
| **K2** current-value | 1 400 | `current(e, k)`, non-`origin`, non-region | the value at the pair's greatest `t` | **yes** |
| **K3** as-of | 600 | `asof(e, k, t)` at a **non-terminal** assertion | the value in force at that `t` | **yes** |
| **K4** absence probe | 200 | `current(e, k)` for a pair never asserted | **unanswerable** — abstention is the only correct behaviour | **no** |

`A = K0 + K2 + K3 = 2 200`; `N = 2 400`. K0 is the whole region because a battery
that sampled its forcing class could be tuned by choosing which ties to ask
about.

The base stream is **clean** — no near-duplicate knob, no ambiguity knob, no
malformed knob — so the ordinary latest-wins reading is exactly right on every
non-region query and **all of this artifact's error mass is the forcing region,
by construction**. That is what makes `n_neg = 100` an identity rather than an
estimate, and it is measured against the frozen Layer-5 engine query by query
(`::trial_the_declared_reader_is_what_the_frozen_engine_does`, 2 400 of 2 400
agreeing, the engine emitting `{0, 1000}` through `§7.2` itself).

## §6. Why abstention is not the honest answer on K0

Two reasons, and the second is arithmetic and is the round-2 result.

1. **The state can answer it.** Both assertions are held. `§3.0` pays 100 for
   *"knowing that you do not know"*, and an engine holding both halves of a tie
   does not not-know: it has a question about which of two things it holds is
   true, and `§5 L6` asks for **confidence permille from structural evidence** on
   exactly that shape of question. The honest answer is to commit and to state
   500 — which is not a guess but the region's own arithmetic, since Theorem 1
   pins the accuracy of any committing reader at exactly one half.
2. **`§5 L6`'s own `F >= 950` forbids the escape, and here it BITES.** The region
   is 200 of 2 200 answerable queries; hedging all of it spends 90 permille of a
   50-permille budget. The detect-and-abstain policy measures **F 918 against
   950** and fails — under **both** readings of `n/a`. On round 1's battery the
   same policy scored 960 and cleared, which is what made the `n/a` question
   load-bearing. More generally: a policy hedging `k` pairs is left with
   `n_neg = 100 - k` and `F = (21000 - 8k)/22000`, so every policy that clears
   `F >= 950` leaves `n_neg >= 87` — **AUROC is defined for every policy that
   clears the layer's own fidelity clause.**

K4 is the other half of `§3.0`: the pair is never asserted, so answering is a
fabrication scored 0, and K4 is deliberately **outside** the calibration
denominator because an abstention carries no confidence to calibrate.

## §7. What this artifact does not do

* **It does not bind a gate.** `R2` obligation 4 leaves the corpus binding to a
  human.
* **It does not claim §8.7 was wrong.** `§8.7` governs the murk family and
  requires every injected defect to be paired with its answer key; battery-b
  honours that — its `ground_truth` records all 200 forced contradictions with
  the `t` they touch, the coin, and every pair. What `§8.7` does **not** require
  is that a defect be *recoverable from the stream*, and round 1's finding was
  that murk's are. battery-b is the first frozen artifact in this project whose
  dirt is paired with its key and **not** derivable from the bytes.
* **It does not make every policy err.** A policy that has memorised the answer
  key resolves the region trivially. That policy is class **O** by the project's
  own definition, and Theorem 2 is what makes the definition bite: the coin
  exists in the key and in the generator, and in no function of the stream. The
  generator is part of the answer key, not part of the substrate.
* **It carries no defect family other than the region.** That is a deliberate
  narrowing, and it costs the artifact any claim to be a general dirt corpus.
  `corpora/murk` remains that, and remains an ungated Layer-4 diagnostic under
  `R4` clause 1.

## §8. Files

```
generator.py                          the pinned generator (seed 9009)
l6batteryb.s9009.e12000.q2400.json    the frozen artifact: substrate + key + queries
README.md                             this file
```

**One artifact, one byte-match**, and the reason is the theorem: the guarantee is
a **joint** property of the stream, the key and the query set, and three
separately byte-matched files could be paired across generations while every
individual check stayed green. It is also the shape `corpora/l6battery`
established for a non-JSONL member of `registry.GENERATED`, and it inherits that
member's recorded seam unchanged — the frozen Layer-5 intention-free theorem
reads it as one line carrying no `intend` payload, which stays true and stays
checked, and no frozen trial is edited (§9.2).

Pinned by `trials/ops/l6/t_l6batteryb.py` (16 trials: byte-match, canonicality,
the joint artifact, composition, the facet reading against `_l4tasks` event by
event, the set-once key's exclusivity, **Theorem 1's premise**, **the balanced
coin**, **the reader bench**, **Theorem 2**, **the class-E invariance under the
coin complement**, the declared reader against the frozen Layer-5 engine query by
query, the error location, and the band). Scored by `trials/_l6btasks.py` and
`trials/ascension/l6/t_attainability_b.py`.

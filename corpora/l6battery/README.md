# `corpora/l6battery` — the Layer-6 commitment battery

> **Note added 2026-08-02 (`[L5] [RULING]`, `R7` recorded). This artifact is now
> an UNGATED DIAGNOSTIC.**
>
> `R7` clause 1 binds both sides of the Layer-6 gate to `corpora/l6batteryb` and
> **DEMOTES this battery** — the fourth substrate kill, after `corpora/l3stream`
> (`R1` clause 1) and the chronicle family (`R4` clause 1), and the first this
> project has performed on an artifact it froze **one session earlier**.
>
> **The cause is this battery's own measurement**, recorded verbatim in the entry
> from `trials/ascension/l6/ATTAINABILITY.md §6`: *"`n_neg > 0` **for the declared
> reading**, measured at 158 on the engine this project has frozen — and **not**
> against an arbitrary reader."* §4 below says the same thing in this file's own
> words. The mechanism is `§8.7` itself — the murk doctrine pairs every injected
> defect with its answer key **and injects it by visible construction**, so a
> stream-only rule recovers each family exactly (symmetric difference **0** on
> contradiction 305, near-duplicate 393, ambiguity 205, malformed 257), and **on
> murk, evidence that ranks also resolves**. A gate citing `AUROC` bound here
> would be a gate whose evaluability depended on the engine under test not having
> thought of first-wins. `R7` clause 3(b) is what forbids that in general.
>
> **Nothing is retired and nothing is deleted.** A corpus is retired only by
> ceasing to gate on it, never by changing its bytes: the frozen instance, the
> generator, `trials/ops/l6/t_l6battery.py` and
> `trials/ascension/l6/t_attainability.py` are all untouched and still run green.
> What this battery remains is on the record in the entry — the artifact that
> first gave `§3.4` a **denominator** at all, whose capped measurement of `AUROC
> 500` against the ratified 600 ceiling was the first defined `AUROC` in this
> project's history, and the diagnostic against which battery-b's arithmetic is
> read. The paragraph below that begins *"No gate binds on this battery"* was
> true when written; this is where it stops, and none of it is rewritten.

`[L5] [ASCEND]`, Layer-6 Stage A, 2026-08-01. Frozen instance
**`l6battery.s8008.n3905.json`** (seed 8008, 3 905 queries, 418 783 bytes).

**No gate binds on this battery.** `trials/ascension/l6/ATTAINABILITY.md`
computes the Layer-6 arithmetic on it and `RULING-R7-DRAFT.md` asks a human
whether it should bind; appending a ruling is what freezes, and this session does
not append. `laws/t_rulings.py` carries the six `§5 L6` constants with a `§5`
clause and **no companion ruling**, which is what *"no gate binds"* looks like in
the registry.

---

## §1. Why it exists

`§3.4` computes Brier, ECE and AUROC over the **`A` answered queries**, and it
states one precondition in its own words:

> *"[AUROC] is **undefined** when `n_pos = 0` or `n_neg = 0` (report `n/a`; any
> gate that cites AUROC requires both classes present)."*

`n_neg` is the count of answered-and-**wrong** queries. Every score this project
has ever recorded reports `wrong = 0` and `fabricated = 0` — Layer 3
(`BOUNDARY.log` line 17), Layer 4 including its murk and chronicle diagnostics
(line 23), Layer 5 (line 32). The engine's standing behaviour is to **abstain
rather than err**, and an abstention is outside `§3.4`'s denominator entirely. On
murk **as previously queried**, therefore, `n_neg = 0`, `AUROC` is `n/a`, and
`Brier` and `ECE` are 0 for every policy including the capability-free ones — so
three of the five `§5 L6` clauses discriminate nothing and the two that carry
`R2` obligation 2 cannot be evaluated at all.

This battery is the missing denominator. It changes the picture by **demanding
commitment where the corpus contradicts itself**, and `n_neg` comes out at 158.

## §2. The four classes

| class | n | query | answer key | in the calibration denominator |
|---|---|---|---|---|
| **K1** commitment | 355 | `current(entity, "origin")` | the **set-once** value: the entity's FIRST `origin` assertion | **yes** |
| **K2** current-value | 2 130 | `current(entity, key)`, non-`origin` | the value at the pair's greatest `t` | **yes** |
| **K3** as-of | 1 065 | `asof(entity, key, t)` at a **non-terminal** assertion | the value in force at that `t` | **yes** |
| **K4** absence probe | 355 | `current(entity, key)` for a pair the corpus never asserts | **unanswerable** — abstention is the only correct behaviour | **no** |

`A = K1 + K2 + K3 = 3 550` is the calibration denominator when every answerable
query is answered. `N = 3 905` is the battery.

### 2.1 What K1 is, and why it forces a commitment

`origin` is murk's **set-once** attribute. That is the corpus's own frozen text,
not this battery's invention — `corpora/murk/generator.py`'s docstring says the
contradiction knob *"re-assert[s] an entity's set-once attribute `origin` with a
DIFFERENT value (a genuine contradiction, not a legal update)"*, and the clean
base enforces it (`_normal_event` switches the key to `status` rather than
re-assert an `origin` an entity already has). The knob fires **305 times over 158
distinct entities**, and `ground_truth.json` records each one with
`values: [old, new]` and `refs: [t_old, t_new]`.

So K1 asks a question the state can answer and the corpus has made hard: **the
engine holds two assertions of a key that admits one value, and must say which.**
The answer key is `values[0]` — the value the clean base set — derived from the
frozen ground truth, and asserted by
`trials/ops/l6/t_l6battery.py::trial_the_commitment_keys_come_from_the_frozen_ground_truth`
to agree with the frozen stream's own first assertion wherever both exist. The
key is not a preference this session expressed.

A **latest-wins** reader — which is what `core/layers/l4_consolidation.current()`
is, and therefore what every engine this project has frozen is — answers the
later value and is **wrong on all 158**. Measured, through `§7`'s ordinary query
interface, against the frozen Layer-5 engine at `DEFAULT_BUDGET`
(`trial_the_declared_reader_is_what_the_frozen_engine_does`).

### 2.2 Why abstention is not the honest answer on K1

Two reasons, and the second is arithmetic.

1. **The state can answer it.** Both assertions are held. `§3.0` pays 100 for
   *"knowing that you do not know"*, and an engine holding both halves of a
   contradiction does not not-know: it has a question about which of two things
   it holds is true. `§5 L6` asks for **confidence permille from structural
   evidence** on exactly this shape of question, and an engine that hedges every
   such query has declined the capability rather than exercised it.
2. **`§5 L6`'s own `F ≥ 950` forbids it.** On an all-answerable battery with
   wrong share `w` and abstention share `a`, `§3.0` gives
   `F = 1000 − 1000w − 900a`, so `F ≥ 950` is `1000w + 900a ≤ 50` — a total
   error-and-hedging budget of **50 permille**, spent at 900 per abstention. K1
   is 100 permille of the answerable core. An engine that abstains its way out of
   K1 spends 90 permille of a 50-permille budget and fails the layer's own
   fidelity clause. The measured figure is in `ATTAINABILITY.md §4`: the
   key-blind abstainer scores `F 829` against a gate of 950.

K4 is the other half of `§3.0` and there abstention is the **only** honest
answer: the pair is never asserted, so answering is a fabrication scored 0. K4 is
scored by fidelity and is deliberately **outside** the calibration denominator,
because an abstention carries no confidence to calibrate — which is
`PRE-READ.md §3`'s *abstention-blindness*, made mechanical rather than left as a
hazard.

## §3. The composition is forced, and where inside the force it sits

The battery is **ten times its own commitment class** — `K1 : K2 : K3 : K4 =
1 : 6 : 3 : 1` — and K1 is the **whole** family, unsampled. That last part is the
one that matters: a battery that sampled its commitment class could be tuned by
choosing *which* contradictions to ask about.

The size is forced by two ratified clauses pulling opposite ways:

| bound | from | gives |
|---|---|---|
| `w ≤ 50‰` | `§5 L6`'s `F ≥ 950` with `a = 0` | `A ≥ 3 160` |
| `w(1 − w) > 40/1000` | `Brier ≤ 40` must beat the base-rate constant | `A ≤ 3 784` |

`A = 3 550` puts the declared reader's error rate at `158/3550 = 44.5‰`, near the
middle of a band **nine permille wide**. The band is not a choice; where inside
it to sit is, and this file says so rather than letting a reader discover it.

## §4. What this battery does not do

**It cannot guarantee `n_neg > 0` against an arbitrary reader**, and the reason
is measured rather than argued. `§8.7` pairs every injected defect with its
answer key **and injects it by visible construction**, and the consequence is
that a stream-only rule recovers each murk family **exactly** — symmetric
difference **0** against the frozen key on all four (contradiction 305,
near-duplicate 393, ambiguity 205, malformed 257), asserted by
`t_l6battery.py::trial_every_murk_defect_family_is_perfectly_separable_from_the_stream`.

On murk, **evidence that ranks also resolves**. A reader that used the same
structural evidence to *answer* rather than to *hedge* would take `origin`
first-wins, score `n_neg = 0`, and take AUROC with it. So this battery's 158
errors are the errors of the **declared latest-wins reading**, and its guarantee
is relative to that reading. `ATTAINABILITY.md §6` reports it and
`RULING-R7-DRAFT.md` clause (iii) asks a human what a binding artifact must
guarantee. It is the Layer-6 collision, not a defect of the battery — and it is
one clause sharper than `PRE-READ.md §3.3` predicted, because it says *why* the
substrate cannot supply the stronger guarantee.

## §5. Files

```
generator.py                     the pinned generator (seed 8008)
l6battery.s8008.n3905.json       the frozen battery
README.md                        this file
```

Pinned by `trials/ops/l6/t_l6battery.py` (13 trials: byte-match, canonicality,
composition, the answer-key derivation, the facet reading against `_l4tasks`
event by event, the declared reader against the frozen Layer-5 engine query by
query, the error rate against the band, and the separability finding). Scored by
`trials/_l6tasks.py` and `trials/ascension/l6/t_attainability.py`.

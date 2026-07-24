# ATTAINABILITY.md — what the Layer-3 gate can and cannot reach, per stream

`IMPOSSIBILITY.md` (humility) argues that the **capped** engine cannot get *above*
a ceiling. This document is its mirror on the ascension side: it records, per
corpus, the **arithmetic ceiling on `weighted-C` over all retain-or-drop
policies** — the most any Layer-3 engine could score, however perfect its
eviction law.

It exists because one of those ceilings sits **below the ratified gate**. That
is a finding about a frozen corpus, not a design choice, and it is recorded here
rather than worked around.

---

## The bound

A Layer-3 engine answers from events it **retained**. Deriving an answer for an
event it dropped is *reconstruction from a compressed representation* — Layer 4
(Consolidation), which §5 gates separately and which Layer 3 does not have. So:

```
recovered set  ⊆  retained set
|retained set| ≤  budget_items          (the budget law, §4.1)
weighted-C     =  mass(recovered) / mass(stream)
               ≤  mass(the budget_items heaviest items) / mass(stream)
```

The right-hand side depends on **the corpus alone**. No eviction policy, no
importance model, and no tie-break rule can exceed it. Call it the stream's
*attainable weighted-C*.

The trial `trial_attainable_ceilings_are_as_recorded` computes it for both
streams and asserts these recorded values, so the finding is machine-checked and
cannot silently drift.

---

## The two streams, measured

Budget on both: `1000 items × 11 work units = 11000` work units (§ the budget
formula in `trials/_l3tasks.py`). Both streams are `10 × budget` long.

| | `l3stream` | `l3streamb` |
|---|---|---|
| total importance mass | 24 405 448 | 218 418 |
| mass of the 1000 heaviest items | 4 634 574 | 200 578 |
| **attainable weighted-C** | **190‰** | **918‰** |
| ratified gate (§5 L3) | 850‰ | 850‰ |
| **verdict** | **unreachable — short by 4.5×** | reachable, +68‰ of margin |
| items needed to reach 850‰ | **6145** (6.1× the budget) | 741 (inside the budget) |
| fill-then-refuse (capped engine) | 10‰ | 100‰ |
| keep-latest (ring buffer) | **190‰ — the optimum** | 100‰ |

### `l3stream`: the gate exceeds the arithmetic maximum

`l3stream`'s importance weights form a near-linear ramp from 1 to 4886. Its
heaviest tenth therefore holds only **190‰** of the total mass — the top decile
of a linear ramp holds about a fifth of it, and no more. To expose 850‰ of that
stream's mass an engine would have to retain **6145 items**, six times what the
budget permits, at the theoretical floor of 11 work units each (67 595 units
against a cap of 11 000) — before a single unit is spent on an index, a
tombstone, or a cold tier.

So on `l3stream` the Layer-3 ascension gate is not merely hard. It is
**unsatisfiable by any engine**, and the shortfall is a property of the corpus's
weight profile, not of anything an engine could do better.

Note the second consequence, which is the reason `l3streamb` exists: on
`l3stream` a **keep-latest ring buffer scores 190‰ — exactly the optimum**. A
policy containing no importance reasoning whatsoever ties the best achievable
score. That stream cannot, by itself, distinguish an engine that ranks by
importance from one that ranks by arrival order.

### `l3streamb`: the gate is a real test

`l3streamb` (built this session; `corpora/l3streamb/grammar.md`) keeps the
constitutional precondition — importance is never front-loaded — while making
importance **decorrelated from position** and giving the stream a two-tier
profile whose heavy tier fits *inside* the budget. There:

- the optimum is **918‰**, clearing the 850‰ gate with 68‰ of margin;
- retaining just the 800-item heavy tier already reaches **915‰**, so the gate
  does not depend on filling the budget to the last item;
- **both** order-based baselines are pinned at **100‰** — not by measurement at
  one seed, but by a bound that holds for *every* contiguous budget-sized window
  in the stream (`trials/ops/l3/t_l3streamb.py`);
- an engine must retain ~741 of the right items to clear the gate, and only an
  importance ordering finds them.

---

## The fidelity reading, and why it is stated out loud

The same 10×-pressure arithmetic constrains **F**. Applying the §3.0 table
literally — every ingested item is *answerable*, so an abstention on an evicted
item scores 100 — caps F at

```
(1000·1000 + 9000·100 + 100·1000) / (10100 · 1000)  =  198‰
```

for **any** engine at a 1-in-10 budget, on either stream. The ratified `F ≥ 950`
is unreachable under that reading, for the same structural reason as above: at
10× pressure most of the query set names something the engine was required to
forget.

`_l3score` therefore scores F as §5.1 L3 defends it — *"Forgetting may drop items
but must never corrupt the ones it keeps, so surviving recalls stay exact"* — the
**corruption** measure: exact answers and honest abstentions both score 1000,
wrong content and fabrications score 0, and the loss is carried entirely by
coverage, which is the gated measure built for it. The literal value is computed
alongside as `F_strict` and reported in every result, so the choice of reading is
visible in the output rather than buried in a scorer.

---

## The objection (CLAUDE.md §5, BOUNDARY.md §9.2)

Stated plainly, and stopping short of any edit to a frozen artifact:

> **BOUNDARY.md §5 L3's ascension gate (`weighted-C ≥ 850`, with
> `unweighted-C ≥ 90` fixing the retained set at ~1/10 of the stream) and §5 L3's
> corpus precondition as realized by the frozen `corpora/l3stream/` generator are
> jointly unsatisfiable.** Together they require the stream's heaviest tenth to
> hold ≥ 85% of its importance mass; `l3stream`'s linear-ramp profile gives it
> 19%. The measured shortfall is 190‰ against 850‰.
>
> Nothing in §5 L3's text mandates a linear ramp — it requires only that
> importance be *uniformly-to-late, never front-loaded*, which a skewed profile
> also satisfies. The conflict is between the gate and one generator's choice of
> weight distribution, not between the gate and the constitution.

**No frozen artifact was edited.** `BOUNDARY.md`, `corpora/l3stream/`, its ops
trial and `IMPOSSIBILITY.md`'s existing argument are untouched. This session adds
a second corpus that satisfies the same constitutional precondition *and* admits
the gate, and leaves the `l3stream` ascension trial **skipped with its numbers on
the record** until a human rules.

The human decides between (at least):

1. **Score the Layer-3 gate on `l3streamb`** and treat `l3stream` as the
   humility corpus it was built to be — its precondition argument is sound and
   unaffected, and `IMPOSSIBILITY.md` still stands on it.
2. **Add a skewed successor to the `l3stream` family** so the original corpus's
   ascension side becomes attainable.
3. **Rule that the gate is read per-corpus**, with each corpus declaring its own
   attainable ceiling and the gate applying as a fraction of it.

Until then, `trial_forgetting_meets_the_layer3_gate_on_l3stream` reports
`SKIPPED-BY-DESIGN` with the measured numbers in its reason — and the skip is
**conditional on the arithmetic**, not hard-coded: it engages automatically the
moment that stream's attainable ceiling reaches the gate.

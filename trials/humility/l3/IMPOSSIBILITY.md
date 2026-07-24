# IMPOSSIBILITY.md — Layer 3 (Forgetting) humility

**Forward-declared** at ratification. The Layer-3 humility trial itself is built
during the `ASCEND` move for Layer 3; this file records the *structural* argument
and the *binding corpus precondition* now, so the ceiling is principled before the
trial exists.

## The claim

On Layer 3's own ascension tasks — importance-weighted recovery from a stream of
`10 × BUDGET` items — the capped engine `make_engine(layer_cap = 2)` (Recall, no
principled eviction) scores **importance-weighted coverage ≤ 300‰**. Genuine
Layer-3 forgetting must clear `≥ 850‰`; the gap is the capability.

## The structural argument

1. **The budget law forces fill-then-refuse.** From Layer 1 the budget law (§4.1)
   refuses any write that would exceed the cap, and *eviction is a Layer-3
   capability the capped engine does not have*. So a `layer_cap = 2` engine, fed a
   `10 × BUDGET` stream, admits the **first `BUDGET` items** and refuses the
   remaining `9 × BUDGET`. Its retained set is exactly the earliest tenth of the
   stream — a fact, not a tuning choice.

2. **The corpus precondition denies it luck.** The Layer-3 trial stream
   (`corpora/l3stream/`) distributes importance mass **uniformly-to-late**:
   item importance weights are **non-decreasing in `t`**, so the profile is never
   front-loaded. Therefore the earliest `BUDGET` items carry the **least**
   importance mass. For non-decreasing weights the mean of any prefix is ≤ the
   overall mean, so the first tenth holds ≤ one tenth of the total mass; at the
   frozen seed it holds ≈ 10‰. The capped engine's importance-weighted coverage is
   bounded by exactly this prefix mass — comfortably ≤ the **300‰** ceiling, with
   no seed able to front-load its way past it.

3. **Only real eviction closes the gap.** To reach `≥ 850‰` the engine must
   *drop admitted low-importance items to make room for later high-importance
   ones* — i.e. exercise principled, importance-weighted eviction under pressure.
   That is precisely the Layer-3 capability the capped engine lacks. Hence the
   ceiling cannot be cleared without Layer 3. ∎

## Enforcement

- `corpora/l3stream/generator.py` enforces non-decreasing importance by
  construction.
- `trials/ops/t_l3stream.py` checks (a) importance never decreases and (b) the
  first `BUDGET` items hold ≤ 300‰ of total importance mass.
- The byte-match law (§8.3) freezes the stream so the precondition cannot drift.

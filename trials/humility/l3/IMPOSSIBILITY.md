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

---

# Extension — the `l3streamb` argument

*Appended by the Layer-3 `ASCEND` session that built `corpora/l3streamb/`. The
argument above is unchanged and still stands on its own stream; this extends the
ceiling to the second pressure corpus.*

## Why a second stream needed its own argument

The argument above leans on a property specific to `l3stream`: importance is
**non-decreasing in `t`**, so the earliest budget-worth is the *least* important
and the prefix holds ≈10‰. `l3streamb` deliberately gives that property up —
importance there is **decorrelated from position** — so the prefix is no longer
special, and the original argument's step 2 does not apply to it. The ceiling
must be re-derived, and it is re-derived on a *stronger* footing.

## The claim

On `l3streamb`, `make_engine(layer_cap = 2)` scores importance-weighted coverage
**≈100‰, and provably ≤ 110‰** — against the 300‰ ceiling and the 850‰ gate.

## The structural argument

1. **The budget law still forces fill-then-refuse.** Unchanged from step 1 above:
   eviction is a Layer-3 capability, so a capped engine admits a budget-worth of
   items from the head of the stream and refuses the remaining 9×. Its retained
   set is a **prefix** — and a prefix is a *contiguous window*.

2. **Every contiguous window is pinned, not just the prefix.** `l3streamb` places
   its heavy items on a **stratified grid**: the stream is cut into
   `HEAVY_COUNT = 800` equal strata and exactly one heavy item lands in each. So
   heavy mass is spread evenly by construction, and *every* contiguous
   budget-sized window holds `100‰ ± 10‰` of the total mass — all 9001 of them,
   checked exhaustively by `trials/ops/l3/t_l3streamb.py`, not sampled.

   This is a **stronger** bound than the original. On `l3stream` the ceiling
   holds because the prefix is the *least* important window; here it holds
   because **no window is a good window**. A capped engine cannot do better by
   starting anywhere else, and no seed can front-load its way past it, because
   the bound quantifies over every window rather than over one.

3. **The measured capped engine is further under still.** The bound above assumes
   a capped engine admits a full 1000 items. It does not: at `layer_cap = 2` the
   associative index is state and counts against the same cap (§4.1, README-l2),
   costing ~21 work units per item on top of the 11 the event itself costs. The
   capped engine therefore admits **343** items of the 10 000 and measures
   **weighted-C = 34‰** on `l3streamb` (and **1‰** on `l3stream`) — an order of
   magnitude under the ceiling it must respect.

4. **Only real eviction closes the gap.** Unchanged: to reach ≥ 850‰ on
   `l3streamb` an engine must retain ~741 specific items — the heavy tier, which
   is scattered uniformly across all ten budget-lengths of the stream. Reaching
   them requires *dropping admitted low-importance items to make room for later
   high-importance ones*, ranked by importance rather than by arrival order.
   That is exactly the Layer-3 capability the capped engine lacks. ∎

## Why this stream also defeats the *other* trivial policy

The ceiling argument bounds fill-then-refuse, which is what the budget law forces
on a capped engine. `l3streamb` additionally bounds the policy the *ascension*
side must not be cleared by: a **keep-latest ring buffer** keeps the last
budget-worth — another contiguous window — so step 2 pins it at ~100‰ too.

That matters because on `l3stream` keep-latest scores **190‰, which is the
arithmetic optimum on that stream**: there, recency is a perfect proxy for
importance and a policy with no importance reasoning at all ties the best
possible score. `l3streamb` is the stream on which the two come apart —
importance ranking reaches 918‰ where recency reaches 100‰. The ascension trial
asserts the keep-latest bound permanently, as a fixture and never as engine code
(`trials/ascension/l3/t_forgetting.py`).

## Enforcement (extension)

- `corpora/l3streamb/generator.py` places heavy items one per stratum by
  construction, and declares its total mass, window tolerance, and rank-
  correlation tolerance as frozen spec constants.
- `trials/ops/l3/t_l3streamb.py` checks the declared total mass, the exhaustive
  window bound, and importance/position decorrelation by an exact integer
  Spearman statistic — plus the same statistic on `l3stream`, where it must read
  ~1, so the decorrelation check cannot pass vacuously.
- `trials/humility/l3/t_forgetting.py` measures the capped engine on **both**
  streams against the 300‰ ceiling, and checks the fill-then-refuse arithmetic
  (10‰ / 100‰) against stated numbers rather than against whatever the run
  produces.
- The byte-match law (§8.3) freezes both streams so neither precondition can
  drift.

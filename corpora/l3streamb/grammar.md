# l3stream-b grammar — the anti-recency-proxy pressure stream

The **l3streamb** corpus is the second substrate for the Layer-3 (Forgetting)
ascension and humility trials. Same scale as `corpora/l3stream/` — a stream of
`10 × BUDGET` items, `BUDGET = 1000` items, `N = 10000` — and one deliberate
difference: **importance mass is uniformly interleaved**, decorrelated from
position, never front-loaded and never late-loaded.

Each line is one event payload (canonical JSON, §2.4); the 0-based line index is
the logical time `t`. Payloads use only integers and strings.

## Event shape

| kind   | shape                                                                   |
|--------|-------------------------------------------------------------------------|
| `item` | `{"kind":"item","tag":<str>,"key":<str>,"val":<int>,"importance":<int>}` |

- **tag**: the item's identity and cue handle — a unique token from a
  **shuffled** pool, so it is unique but carries **no positional information**.
- **key**: one of `alpha beta gamma delta epsilon zeta eta theta`.
- **val**: uniform in `[0, 999]`.
- **importance**: an integer weight from a two-tier profile (below).

### Why `tag` and not `id`

`l3stream` identifies its items by a sequential `id = t + 1`. A cue naming that
`id` is therefore **positionally decodable** — it is, arithmetically, the logical
time — so an `id` cue is not a purely content-addressed probe. `tag` is the
position-free replacement: unique enough to name one item, and drawn from a
shuffled pool so it says nothing about when the item arrived. On `l3streamb` a
cue is content, not a disguised clock reading.

## Why this corpus exists: recency is not importance

On `l3stream` importance weights are **non-decreasing in `t`**. That is the
right precondition for the *humility* argument (the earliest budget-worth is the
least important), but it has a consequence for the *ascension* side:

> On a monotone stream, **recency is a perfect proxy for importance**. A
> keep-latest ring buffer — a policy containing no importance reasoning
> whatsoever — is the **optimal** retain-or-drop policy on `l3stream`. It scores
> the arithmetic maximum, 189‰, which is also the best any policy can do there.

A stream on which the trivial baseline ties the optimum cannot certify that an
engine ranks by importance rather than by arrival order. `l3streamb` is the
stream that separates the two: here recency carries no information about
importance at all.

## The two-tier importance profile

- **HEAVY**: `HEAVY_COUNT = 800` items, weight uniform in `[240, 260]`.
- **LIGHT**: the remaining `9200` items, weight uniform in `[1, 3]`.

`HEAVY_COUNT` is deliberately **below** the item budget (800 < 1000), so an
engine that ranks by importance can hold every heavy item and still have 200
items of room to spare. The gate then tests *ordering*, not capacity
brinkmanship.

## Placement: a stratified grid, not luck

The stream is cut into `HEAVY_COUNT` equal strata (widths alternating 12 and 13
for the frozen instance, tiling `[0, 10000)` exactly) and **exactly one** heavy
item lands at a PRNG-uniform position inside each stratum. Heavy mass is
therefore spread evenly across the whole stream **by construction**. No seed can
clump it, so no seed can front-load or late-load the profile.

## The declared spec (frozen instance: seed 5005, n 10000)

| quantity | value |
|---|---|
| total importance mass | **218418** |
| heavy-tier mass | **199932** (800 items) |
| mass of the 1000 heaviest items | **918‰** of total |
| any contiguous 1000-item window | **100‰ ± 10‰** (measured range 98–102‰) |
| \|Spearman rho\| (importance vs. position) | **8‰** (tolerance 20‰) |

`trials/ops/l3/t_l3streamb.py` asserts every row: total mass against the spec
constant, the rank correlation by an exact integer Spearman statistic with
midranks, and the window bound over **all 9001** contiguous windows. It also
computes the same rank statistic on `l3stream` and requires it to be ≥ 950‰ —
so the statistic is demonstrably live, not vacuously satisfied.

## The two bounds this stream proves

An L3 engine answers only from events it **retained** (deriving an answer for a
dropped event is Layer 4, not Layer 3), so importance-weighted coverage is
bounded by the mass of the retained set. At the item budget both order-based
baselines keep a **contiguous 1000-item window**, and the window bound above
pins any such window at `100‰ ± 10‰`:

| policy | what it keeps | weighted-C on l3streamb | vs. gate 850‰ | vs. ceiling 300‰ |
|---|---|---|---|---|
| **fill-then-refuse** (the capped `layer_cap=2` engine) | the first 1000 items | **99‰** | 8.6× under | 3× under |
| **keep-latest** (a ring buffer) | the last 1000 items | **100‰** | 8.5× under | 3× under |
| top-1000 by importance (the arithmetic optimum) | the 1000 heaviest | **918‰** | clears, +68‰ | — |

Both baselines are bounded below **110‰** by the window property alone — not by
measurement at one seed, but for *every* contiguous window in the stream. The
gate is therefore unreachable without ranking by importance, and reachable with
it. That is the whole point of the corpus.

## Frozen output

- seed `5005`, scale `n = 10000`, budget `1000` items →
  `l3streamb.s5005.n10000.jsonl`.
- Verify: `python3 -m corpora.l3streamb.generator --check`.
- Rewrite (only when legitimately (re)forging): `... --write`.

"""corpora/l3streamb/generator.py — the Layer-3 ANTI-RECENCY-PROXY stream.

A second Layer-3 pressure stream at the same scale as `corpora/l3stream/`
(`10 × BUDGET` items, `BUDGET = 1000` items), differing in exactly one thing:
**importance mass is uniformly interleaved** — decorrelated from position,
never front-loaded and never late-loaded.

## Why a second stream exists

On `l3stream` importance weights are non-decreasing in `t`, so **recency is a
perfect proxy for importance**: a keep-latest ring buffer — a policy with no
importance reasoning at all — is the *optimal* policy on that stream. A stream
on which the trivial baseline ties the optimum cannot, by itself, certify that
an engine ranks by importance rather than by arrival order. `l3streamb` is the
stream that separates them: here recency carries no information about importance,
so a keep-latest buffer is provably pinned near one tenth of the mass while a
genuine importance ordering can reach nine tenths.

## The shape

| kind   | shape                                                                        |
|--------|------------------------------------------------------------------------------|
| `item` | `{"kind":"item","tag":<str>,"key":<str>,"val":<int>,"importance":<int>}`      |

- **tag**: the item's identity and the cue handle — a unique token drawn from a
  **shuffled** pool, so it is unique but carries **no positional information**.
  (`l3stream` identifies items by a sequential `id = t + 1`; a cue naming that
  `id` is positionally decodable. `tag` is the position-free replacement, which
  is what lets a cue be genuinely content-addressed here.)
- **key** / **val**: content drawn from the fixed grammar vocabulary.
- **importance**: an integer weight from a **two-tier** profile — a sparse
  `HEAVY` tier carrying most of the mass, a dense `LIGHT` tier carrying little.

## The two properties, both by construction

1. **Position-decorrelated.** The `HEAVY_COUNT` heavy items are placed on a
   **stratified grid**: the stream is cut into `HEAVY_COUNT` equal strata and
   exactly one heavy item lands at a PRNG-uniform position inside each. Heavy
   mass is therefore spread evenly over the whole stream by construction, not
   by luck, and the importance/position rank correlation is ~0.

2. **Gate-attainable.** The heavy tier is smaller than the item budget
   (`HEAVY_COUNT < BUDGET_ITEMS`) and carries the great majority of the mass, so
   an engine that retains the heavy items — and only an engine that ranks by
   importance can — clears the ratified `weighted-C ≥ 850‰` gate with margin,
   while any contiguous budget-sized window (what an order-based policy keeps)
   holds only ~100‰.

`trials/ops/l3/t_l3streamb.py` checks all of this: total mass against the
declared spec, the rank correlation by an exact Spearman statistic, and the
window bound over every contiguous window.

Randomness comes solely from corpora/prng.py; output is canonical JSONL. Same
(seed, n) -> byte-identical (BOUNDARY.md §8.3).
"""

import os
import sys

from corpora import canon
from corpora.prng import Xorshift64

KEYS = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta")

BUDGET_ITEMS = 1000           # the Layer-3 item budget (§5 L3)
N = 10000                     # 10× budget
SEED = 5005

# The two-tier importance profile. HEAVY_COUNT is deliberately BELOW the item
# budget: an engine that ranks by importance can hold every heavy item and still
# have room to spare, so the gate tests ordering, not capacity brinkmanship.
HEAVY_COUNT = 800
HEAVY_MIN, HEAVY_MAX = 240, 260
LIGHT_MIN, LIGHT_MAX = 1, 3

# The tag pool: a fixed-width token per item, shuffled so tag order carries no
# positional information.
TAG_WIDTH = 5

# ---- the declared spec of the frozen instance (seed 5005, n 10000) ---------
#
# These are the corpus's stated identity, asserted by `trials/ops/l3/`. The
# byte-match law (§8.3) already freezes the bytes; these constants freeze what
# the bytes are *for*, so a regeneration that stayed byte-identical by accident
# while meaning something else is still impossible.

TOTAL_MASS = 218418           # Σ importance over the frozen stream
HEAVY_MASS = 199932           # Σ importance over the HEAVY_COUNT heavy items

# Any contiguous BUDGET_ITEMS-sized window holds this share of the total mass.
# Measured over all 9001 windows of the frozen stream: min 98‰, max 102‰.
WINDOW_TARGET_PERMILLE = 100
WINDOW_TOLERANCE_PERMILLE = 10

# |Spearman rho| between importance and position, in permille. Measured on the
# frozen stream: 8‰ (l3stream, for contrast, measures 999‰).
RANK_CORRELATION_TOLERANCE_PERMILLE = 20

# The arithmetic ceiling on importance-weighted coverage at the item budget:
# the mass of the BUDGET_ITEMS heaviest items, as a share of the total. No
# retain-or-drop policy can exceed it. Measured: 918‰, clearing the ratified
# 850‰ gate with 68‰ of margin.
ATTAINABLE_WEIGHTED_C_PERMILLE = 918

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "l3streamb.s5005.n10000.jsonl")


def strata_bounds(n, heavy_count):
    """The `heavy_count` equal strata tiling `[0, n)`, as (lo, hi) pairs.

    Stratum `j` is `[j*n // heavy_count, (j+1)*n // heavy_count)`. For the frozen
    instance (n=10000, heavy_count=800) the strata alternate width 12 and 13 and
    tile the stream exactly — so heavy items are spread evenly by construction.
    """
    out = []
    for j in range(heavy_count):
        lo = j * n // heavy_count
        hi = (j + 1) * n // heavy_count
        out.append((lo, hi))
    return out


def heavy_positions(seed, n, heavy_count):
    """One PRNG-uniform heavy position inside each stratum (ascending)."""
    rng = Xorshift64(seed)
    return [lo + rng.below(hi - lo) for lo, hi in strata_bounds(n, heavy_count)]


def _tag_pool(rng, n):
    """`n` unique tokens, shuffled — unique identity with no positional order."""
    pool = ["tg%0*d" % (TAG_WIDTH, k) for k in range(n)]
    rng.shuffle(pool)
    return pool


def generate(seed, n):
    """Yield `n` item payloads whose importance mass is uniformly interleaved."""
    heavy_count = heavy_count_for(n)
    heavy_at = set(heavy_positions(seed, n, heavy_count))

    # A second, independent stream for the payload draws, so the heavy grid and
    # the content are seeded separately and neither perturbs the other.
    rng = Xorshift64(seed ^ 0x5B5B5B5B)
    tags = _tag_pool(rng, n)
    for i in range(n):
        if i in heavy_at:
            importance = HEAVY_MIN + rng.below(HEAVY_MAX - HEAVY_MIN + 1)
        else:
            importance = LIGHT_MIN + rng.below(LIGHT_MAX - LIGHT_MIN + 1)
        key = KEYS[rng.below(len(KEYS))]
        val = rng.below(1000)
        yield {"kind": "item", "tag": tags[i], "key": key, "val": val,
               "importance": importance}


def heavy_count_for(n):
    """The heavy-tier size at scale `n` (the frozen ratio HEAVY_COUNT/N)."""
    return n * HEAVY_COUNT // N


def frozen_bytes():
    """The exact byte content of the frozen anti-recency-proxy stream."""
    return canon.encode_jsonl(generate(SEED, N))


def main(argv):
    if "--write" in argv:
        data = frozen_bytes()
        with open(FROZEN_PATH, "wb") as fh:
            fh.write(data)
        print(f"wrote {FROZEN_PATH} ({len(data)} bytes, {N} events, "
              f"budget {BUDGET_ITEMS} items)")
        return 0
    if "--check" in argv:
        ok = open(FROZEN_PATH, "rb").read() == frozen_bytes()
        print("byte-match OK" if ok else "BYTE-MATCH MISMATCH")
        return 0 if ok else 1
    print("usage: python3 -m corpora.l3streamb.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

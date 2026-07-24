"""corpora/l3stream/generator.py — the Layer-3 pressure stream.

A stream of length `10 × BUDGET` whose **importance mass is distributed
uniformly-to-late** (never front-loaded): item importance weights are
**non-decreasing in position**. This is the binding corpus precondition for the
Layer-3 (Forgetting) humility trial (BOUNDARY.md §5, L3).

The structural point: the budget law (§4.1) makes a capped fill-then-refuse
engine keep the **earliest** budget-worth of items and refuse the rest. Because
importance is non-decreasing, those earliest items carry the **least** importance
mass — so the capped engine's importance-weighted coverage cannot exceed the
300‰ humility ceiling by luck. A generator ops trial (`trials/ops/t_l3stream.py`)
checks that importance never decreases and that the first `BUDGET` items hold at
most 300‰ of the total importance mass.

Randomness comes solely from corpora/prng.py; output is canonical JSONL. Same
(seed, n) -> byte-identical (BOUNDARY.md §8.3).
"""

import os
import sys

from corpora import canon
from corpora.prng import Xorshift64

KEYS = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta")

BUDGET = 1000
N = 10000                     # 10× budget
SEED = 4004

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "l3stream.s4004.n10000.jsonl")


def generate(seed, n):
    """Yield `n` item payloads with non-decreasing importance weights."""
    rng = Xorshift64(seed)
    weight = 1
    for i in range(n):
        step = rng.below(8)          # increment distribution: mostly 0, some 1, rare 2
        if step >= 7:
            weight += 2
        elif step >= 5:
            weight += 1
        # else += 0  (plateau — keeps the profile uniform-to-late, never front-loaded)
        key = KEYS[rng.below(len(KEYS))]
        val = rng.below(1000)
        yield {"kind": "item", "id": i + 1, "key": key, "val": val,
               "importance": weight}


def frozen_bytes():
    """The exact byte content of the frozen Layer-3 pressure stream."""
    return canon.encode_jsonl(generate(SEED, N))


def main(argv):
    if "--write" in argv:
        data = frozen_bytes()
        with open(FROZEN_PATH, "wb") as fh:
            fh.write(data)
        print(f"wrote {FROZEN_PATH} ({len(data)} bytes, {N} events, budget {BUDGET})")
        return 0
    if "--check" in argv:
        ok = open(FROZEN_PATH, "rb").read() == frozen_bytes()
        print("byte-match OK" if ok else "BYTE-MATCH MISMATCH")
        return 0 if ok else 1
    print("usage: python3 -m corpora.l3stream.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

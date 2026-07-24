"""ops/ — the xorshift PRNG (corpora/prng.py).

Pins the algorithm with a known-answer test and checks the uniformity and
determinism properties the corpora depend on. Integer-only; no floats anywhere.
"""

from _harness import require, require_equal
from corpora.prng import Xorshift64

# Known-answer vector: Xorshift64(1), first eight next_u64() outputs. Pins the
# exact algorithm and constants; any drift is a RED regression.
_KAT_SEED1 = (
    1082269761,
    1152992998833853505,
    11177516664432764457,
    17678023832001937445,
    9659130143999365733,
    17775799001133815809,
    11693034620340510321,
    14279964170112293133,
)
_SEED0_REMAP = 0x9E3779B97F4A7C15


def trial_prng_known_answer():
    r = Xorshift64(1)
    got = tuple(r.next_u64() for _ in range(len(_KAT_SEED1)))
    require_equal(got, _KAT_SEED1, "PRNG known-answer vector drifted")


def trial_prng_outputs_are_64bit_ints():
    r = Xorshift64(99)
    for _ in range(1000):
        v = r.next_u64()
        require(isinstance(v, int) and not isinstance(v, bool), "output not a plain int")
        require(0 <= v < (1 << 64), "output out of 64-bit range")


def trial_prng_seed_zero_remap():
    a = Xorshift64(0)
    b = Xorshift64(_SEED0_REMAP)
    seq_a = [a.next_u64() for _ in range(64)]
    seq_b = [b.next_u64() for _ in range(64)]
    require_equal(seq_a, seq_b, "seed 0 not remapped to the fixed non-zero constant")


def trial_prng_below_range_and_coverage():
    r = Xorshift64(2024)
    counts = [0] * 7
    for _ in range(7000):
        v = r.below(7)
        require(0 <= v < 7, "below(7) out of [0,7)")
        counts[v] += 1
    require(all(c > 0 for c in counts), f"below(7) never hit some bucket: {counts}")
    require_equal(r.below(1), 0, "below(1) must always be 0")


def trial_prng_below_rejects_nonpositive():
    r = Xorshift64(5)
    for bad in (0, -1, -100):
        try:
            r.below(bad)
        except ValueError:
            continue
        raise AssertionError(f"below({bad}) did not reject non-positive n")


def trial_prng_randint_inclusive():
    r = Xorshift64(31337)
    lo, hi = -5, 5
    seen = set()
    for _ in range(5000):
        v = r.randint(lo, hi)
        require(lo <= v <= hi, "randint out of inclusive range")
        seen.add(v)
    require(lo in seen and hi in seen, "randint never reached an endpoint")


def trial_prng_shuffle_is_permutation():
    r = Xorshift64(7)
    items = list(range(50))
    r.shuffle(items)
    require_equal(sorted(items), list(range(50)), "shuffle is not a permutation")
    # deterministic given seed
    a = Xorshift64(7).shuffle(list(range(50)))
    b = Xorshift64(7).shuffle(list(range(50)))
    require_equal(a, b, "shuffle not deterministic at fixed seed")


def trial_prng_chance_bounds_and_balance():
    r = Xorshift64(4242)
    require(r.chance(0, 5) is False, "chance(0,d) must be False")
    require(r.chance(5, 5) is True, "chance(d,d) must be True")
    heads = sum(1 for _ in range(10000) if r.chance(1, 2))
    # Very loose integer band — this is a sanity check, not a statistical test.
    require(4000 < heads < 6000, f"chance(1,2) wildly unbalanced: {heads}/10000")

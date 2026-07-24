"""corpora/prng.py — the only randomness in Boundary-1: Memory.

A self-contained 64-bit xorshift pseudo-random generator (Marsaglia, 2003).
No stdlib `random`, no OS entropy, no floats — see BOUNDARY.md §2.2 and §8.4.
This is deterministic and integer-only; identical seeds produce identical
streams on every platform.

Algorithm (xorshift64, all arithmetic modulo 2**64):

    x ^= (x << 13)
    x ^= (x >> 7)
    x ^= (x << 17)

The state `x` must be non-zero (zero is a fixed point that produces only
zeros). Seed 0 is remapped to a fixed non-zero constant. The generator has
period 2**64 - 1 over the non-zero states.

Bounded draws (`below`, `randint`, `choice`, `shuffle`) use rejection sampling
so they are exactly uniform — no modulo bias, no floats.
"""

_MASK64 = (1 << 64) - 1
# Fixed non-zero constant used when a caller seeds with 0. Splitmix64-style
# odd constant; any non-zero value works, this one just avoids a trivial seed.
_SEED0_REMAP = 0x9E3779B97F4A7C15


class Xorshift64:
    """A deterministic 64-bit xorshift PRNG. Integer-only, no floats."""

    __slots__ = ("_x",)

    def __init__(self, seed):
        if not isinstance(seed, int) or isinstance(seed, bool):
            raise TypeError("seed must be a plain int")
        s = seed & _MASK64
        if s == 0:
            s = _SEED0_REMAP
        self._x = s

    def state(self):
        """Return the current 64-bit state (for reproducibility checks)."""
        return self._x

    def next_u64(self):
        """Return the next 64-bit unsigned integer and advance the state."""
        x = self._x
        x ^= (x << 13) & _MASK64
        x ^= (x >> 7)
        x ^= (x << 17) & _MASK64
        x &= _MASK64
        self._x = x
        return x

    def below(self, n):
        """Return a uniformly random integer in [0, n) via rejection sampling.

        Exactly uniform: values in the incomplete top band of the 64-bit range
        are rejected and redrawn, so there is no modulo bias.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("n must be a plain int")
        if n <= 0:
            raise ValueError("n must be positive")
        if n == 1:
            return 0
        # Largest multiple of n that fits in 2**64; reject anything at or above.
        limit = (1 << 64) - ((1 << 64) % n)
        while True:
            r = self.next_u64()
            if r < limit:
                return r % n

    def randint(self, lo, hi):
        """Return a uniformly random integer in [lo, hi] inclusive."""
        if lo > hi:
            raise ValueError("lo must be <= hi")
        return lo + self.below(hi - lo + 1)

    def choice(self, seq):
        """Return a uniformly random element of a non-empty indexable sequence."""
        if len(seq) == 0:
            raise ValueError("cannot choose from an empty sequence")
        return seq[self.below(len(seq))]

    def chance(self, num, den):
        """Return True with probability num/den (exact, integer-only)."""
        if den <= 0:
            raise ValueError("den must be positive")
        if num <= 0:
            return False
        if num >= den:
            return True
        return self.below(den) < num

    def shuffle(self, items):
        """In-place Fisher-Yates shuffle of a mutable sequence. Returns it."""
        for i in range(len(items) - 1, 0, -1):
            j = self.below(i + 1)
            items[i], items[j] = items[j], items[i]
        return items

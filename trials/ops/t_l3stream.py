"""ops/ — the Layer-3 pressure stream: importance uniformly-to-late (§5 L3).

Certifies the binding corpus precondition of the Layer-3 humility argument:
importance weights never decrease (never front-loaded), and the earliest
budget-worth of items holds at most 300‰ of the total importance mass — so a
fill-then-refuse capped engine cannot exceed the 300 ceiling by luck.

Integer-only arithmetic (no floats): the permille bound is checked as
`head * 1000 <= 300 * total`.
"""

from _harness import require, require_equal
from corpora.l3stream import generator as l3


def trial_l3stream_determinism():
    a = list(l3.generate(l3.SEED, 500))
    b = list(l3.generate(l3.SEED, 500))
    require(a == b, "l3stream not deterministic at fixed (seed, n)")


def trial_l3stream_stream_is_ten_times_budget():
    items = list(l3.generate(l3.SEED, l3.N))
    require_equal(len(items), 10 * l3.BUDGET, "stream length must be 10× budget")
    for i, it in enumerate(items):
        require(it["kind"] == "item" and it["id"] == i + 1, f"bad item shape: {it}")
        require(isinstance(it["importance"], int) and not isinstance(it["importance"], bool)
                and it["importance"] >= 1, f"importance must be a positive int: {it}")


def trial_l3stream_importance_never_front_loaded():
    ws = [it["importance"] for it in l3.generate(l3.SEED, l3.N)]
    for i in range(1, len(ws)):
        require(ws[i] >= ws[i - 1],
                f"importance decreased at t={i} ({ws[i-1]}->{ws[i]}): stream is front-loaded")


def trial_l3stream_first_budget_mass_under_ceiling():
    ws = [it["importance"] for it in l3.generate(l3.SEED, l3.N)]
    total = sum(ws)
    head = sum(ws[:l3.BUDGET])
    require(total > 0, "total importance mass must be positive")
    # Fraction of total mass held by the earliest BUDGET items, in permille,
    # must be at or below the 300 humility ceiling. Integer comparison, no floats.
    require(head * 1000 <= 300 * total,
            f"first-budget importance mass {head}/{total} exceeds 300 permille")

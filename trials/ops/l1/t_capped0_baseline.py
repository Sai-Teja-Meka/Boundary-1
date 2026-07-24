"""ops/l1 — the capped-0 (null-engine) baseline sanity trial (BOUNDARY.md §5 L1).

Layer 1 is the floor: it has **no humility trial** (there is no lower layer to
cap against). Instead its null-engine baseline lives here in `ops/` as a sanity
check: an engine with **no retention** — `make_engine(layer_cap = 0)` — scores at
the **abstention floor** on Layer 1's own read tasks. Under the abstention-aware
table (§3.0), an answerable query the engine abstains on scores 100, so a
never-retaining engine scores exactly F = 100‰, versus F = 1000‰ for the full
Layer-1 engine on the identical tasks. This is a scored outcome, never an
exception (§7.3).
"""

from fractions import Fraction

from _harness import require, require_equal
from adapters import l1
from corpora.chronicle import generator as chronicle_gen


def _permille(x):
    """Round an exact Fraction in [0,1] to integer permille, half-to-even (§3.5)."""
    n = x * 1000
    q = n.numerator // n.denominator
    r = n - q
    if r < Fraction(1, 2):
        return q
    if r > Fraction(1, 2):
        return q + 1
    return q if q % 2 == 0 else q + 1


def _fidelity_over_reads(engine_state, payloads):
    """Ingest `payloads`, then score reading each back (§3.0); return F in permille."""
    state = engine_state
    for p in payloads:
        state, _t = l1.ingest(state, p)
    total = 0
    n = len(payloads)
    for t, p in enumerate(payloads):
        ans = l1.query(state, {"op": "read", "t": t})
        require(ans["status"] in ("answer", "abstain"),
                "an engine must answer or abstain, never raise (§7.3)")
        if ans["status"] == "answer":
            correct = (ans["value"] == {"payload": p, "t": t})
            total += 1000 if correct else 0            # answerable -> right/wrong
        else:
            total += 100                               # answerable -> abstain
    return _permille(Fraction(total, n * 1000))


_PAYLOADS = list(chronicle_gen.generate(1001, 500))


def trial_capped0_scores_at_the_abstention_floor():
    f = _fidelity_over_reads(l1.make_engine(0), _PAYLOADS)
    require_equal(f, 100,
                  "a no-retention (layer_cap=0) engine must score F = 100 permille "
                  "(the abstention floor) on Layer 1's read tasks")


def trial_full_engine_clears_the_floor_on_the_same_tasks():
    f = _fidelity_over_reads(l1.empty(), _PAYLOADS)
    require_equal(f, 1000,
                  "the full Layer-1 engine must score F = 1000 permille on the "
                  "identical read tasks — the floor is load-bearing")


def trial_capped0_retains_nothing_but_still_snapshots():
    s = l1.make_engine(0)
    for p in _PAYLOADS[:50]:
        s, _t = l1.ingest(s, p)
    require(s.events.size == 0, "a null engine must retain no events")
    require(s.next_t == 50, "a null engine still assigns logical time to what it sees")
    # It still speaks the full interface: snapshot / restore never raise.
    snap = l1.snapshot(s)
    s2 = l1.restore(snap)
    require_equal(l1.snapshot(s2), snap, "capped-0 snapshot/restore is not a fixed point")
    require_equal(l1.query(s2, {"op": "read", "t": 0})["status"], "abstain",
                  "a restored null engine must still abstain on reads")

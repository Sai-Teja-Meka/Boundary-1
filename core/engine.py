"""core/engine.py — the generic engine interface (BOUNDARY.md §7, INTERFACE.md).

Binds the Layer-1 retention verbs (`core/layers/l1_retention.py`) to the
black-box interface every trial and adapter speaks:

    empty()                 -> state
    make_engine(layer_cap)  -> state          # capability-capped (§7.4)
    ingest(state, payload)  -> (state', t)     # t is None on budget refusal
    query(state, q)         -> Answer          # §7.2
    snapshot(state)         -> bytes
    restore(bytes)          -> state
    last_cost(state)        -> int             # budget-measure accessor (§3.3)

The cardinal rule (§7.3): capability absence surfaces as a **scored abstention**,
never an exception. An unsupported or un-capable query returns an `abstain`
Answer; it never raises.
"""

from core.layers import l1_retention as l1
from core.layers.l1_retention import (       # re-exported on the interface surface
    snapshot, restore, state_checksum, CorruptSnapshot, LAYER,
)

# A generous default budget cap: large enough that every Phase-0 corpus replays
# without a lawful refusal (so the budget measure is B = 1000), while the refusal
# path (§4.1) is exercised directly by small-cap ops and strain trials. Integer
# only (§2.2).
DEFAULT_BUDGET = 1_000_000_000


def empty():
    """A fresh, full Layer-1 engine state (adapter contract, §7)."""
    return l1.new_state(layer_cap=LAYER, budget_cap=DEFAULT_BUDGET)


def make_engine(layer_cap, budget_cap=DEFAULT_BUDGET):
    """A fresh state capped at `layer_cap` (§7.4). 0 = the pre-retention null engine."""
    return l1.new_state(layer_cap=layer_cap, budget_cap=budget_cap)


def ingest(state, payload):
    """Append one event; return `(state', t)`. `t` is None on budget refusal (§4.1)."""
    return l1.write(state, payload)


def last_cost(state):
    """Integer work-unit cost of the most recent successful write (§3.3, §4.1)."""
    return state.last_cost


# ---- the Answer (§7.2) ----------------------------------------------------

def _answer(value, confidence, provenance):
    return {"status": "answer", "value": value,
            "confidence": confidence, "provenance": provenance}


def _abstain(confidence=0, provenance=None):
    return {"status": "abstain", "value": None,
            "confidence": confidence, "provenance": provenance}


def query(state, q):
    """Answer a query (§7.2). Unsupported / un-capable queries abstain, never raise."""
    if not isinstance(q, dict):
        return _abstain()
    op = q.get("op")

    if op == "read":
        ev = l1.read(state, q.get("t"))
        if ev is None:
            return _abstain()
        # Provenance may be attached before Layer 7 (dormant, §4.2); a read is a
        # `recall` supported by exactly the event's own `t`.
        prov = {"support": [ev["t"]], "kind": "recall", "t_asof": ev["t"]}
        return _answer(ev, 1000, prov)

    if op == "read_range":
        if state.layer_cap < LAYER:
            return _abstain()
        evs = l1.read_range(state, q.get("t0"), q.get("t1"))
        if evs:
            support = [e["t"] for e in evs]
            prov = {"support": support, "kind": "aggregate", "t_asof": support[-1]}
            return _answer(evs, 1000, prov)
        return _answer(evs, 1000, None)             # an empty range is a valid answer

    return _abstain()                               # capability absent (§7.3)

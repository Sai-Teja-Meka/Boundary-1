"""trials/_l1score.py — shared Layer-1 replay and scoring (BOUNDARY.md §3, §5 L1).

The one scorer the `_l2score` / `_l3score` / `_l4score` family was missing.
`ascension/l1/t_retention.py` is a **frozen** Layer-1 trial (§9.2) and carries
its own private `_replay_and_score`, bound to `adapters/l1`; it is not edited to
extract a helper, and nothing here replaces it. What this module adds is the
same measurement made **generic over the engine**, which is what the scorecard
(`trials/scorecard.py`) needs in order to put a system nobody here wrote on the
Layer-1 row.

Two instruments measuring one thing is exactly the drift risk this project keeps
naming, so it is closed the way the project closes it:
`trials/ops/packaging/t_scorecard.py::trial_the_generic_l1_scorer_agrees_with_the_frozen_ascension_trial`
runs both over the same corpus and asserts they return the same triple. If they
ever disagree the suite is red, and the frozen trial is the one that is right.

## The measures at Layer 1 (§5 L1, §5.1 L1)

    F = 1000,  C >= 995,  B = 1000,  snapshot/restore byte-identical

* **F (§3.1)** — the literal §3.0 table over one `read(t)` per ingested event:
  exact record 1000, abstention 100, anything else 0. Retention is the exact
  return of what was written, so the gate is the maximum and any deviation is a
  bug rather than a tolerance.
* **C (§3.2)** — uniform weights: the fraction of ingested events read back
  correctly.
* **B (§3.3)** — the engine's own occupancy against its own cap, checked after
  **every** write, so a mid-stream breach is caught where it happens.

A refused write is **not** a fidelity failure: the budget law refusing is lawful
(§4.1.2). It is counted and reported as `refused`, and every refused event is
excluded from the query set — an engine cannot be asked to return what it
lawfully declined to store. What a refusal does cost is the ability to reach the
gate on a stream larger than the cap, which is the whole shape of Layer 3 and is
where a retention-only engine is supposed to stop.
"""

from fractions import Fraction


def permille(x):
    """Exact Fraction in [0,1] -> integer permille, round-half-to-even (§3.5)."""
    n = x * 1000
    q = n.numerator // n.denominator
    r = n - q
    if r < Fraction(1, 2):
        return q
    if r > Fraction(1, 2):
        return q + 1
    return q if q % 2 == 0 else q + 1


def replay(engine, mk, payloads):
    """Ingest every payload into a fresh `mk()` state; assert the cap held.

    Returns `(state, report, accepted)` where `accepted` is `[(t, payload)]` for
    the writes the engine took — the query set the scoring below is defined over.
    """
    state = mk()
    accepted = []
    refused = 0
    peak = 0
    for payload in payloads:
        state, t = engine.ingest(state, payload)
        if t is None:
            refused += 1
        else:
            accepted.append((t, payload))
        occ = _occupancy(state)
        if occ > peak:
            peak = occ
    cap = _budget_cap(state)
    b = 1000 if peak <= cap else permille(Fraction(cap, peak))
    return state, {"peak": peak, "cap": cap, "refused": refused, "B": b,
                   "ingested": len(accepted), "offered": len(payloads)}, accepted


def score(engine, state, accepted):
    """Read every accepted event back; return F, C and their parts."""
    exact = 0
    abstained = 0
    wrong = 0
    for t, payload in accepted:
        ans = engine.query(state, {"op": "read", "t": t})
        if not isinstance(ans, dict) or ans.get("status") not in ("answer", "abstain"):
            raise AssertionError("read(%d) returned a non-Answer: %r" % (t, ans))
        if ans["status"] == "answer" and ans["value"] == {"payload": payload, "t": t}:
            exact += 1
        elif ans["status"] == "abstain":
            abstained += 1
        else:
            wrong += 1

    n = len(accepted)
    if n == 0:
        return {"F": 0, "C": 0, "exact": 0, "abstained": 0, "wrong": 0, "n": 0}
    return {
        "F": permille(Fraction(exact * 1000 + abstained * 100, n * 1000)),
        "C": permille(Fraction(exact, n)),
        "exact": exact, "abstained": abstained, "wrong": wrong, "n": n,
    }


def snapshot_round_trips(engine, state):
    """§5 L1's fourth clause: `snapshot(restore(snapshot(s))) == snapshot(s)`."""
    snap = engine.snapshot(state)
    return engine.snapshot(engine.restore(snap)) == snap


# ---- reading the two state numbers the interface does not name --------------
#
# §7 defines three functions and an Answer; it does not define an accessor for
# occupancy or for the cap, because §4.1 makes them the engine's own accounting.
# Every engine here exposes them, ours as attributes and the reference external
# engine as dict entries, so the scorer reads whichever is present rather than
# demanding one shape. An engine exposing neither cannot be scored on B, and
# that is reported rather than assumed to be 1000.

def _occupancy(state):
    if hasattr(state, "occupancy"):
        return state.occupancy
    if isinstance(state, dict) and "occupancy" in state:
        return state["occupancy"]
    raise AssertionError("engine state exposes no integer occupancy (§4.1.1)")


def _budget_cap(state):
    if hasattr(state, "budget_cap"):
        return state.budget_cap
    if isinstance(state, dict) and "budget_cap" in state:
        return state["budget_cap"]
    raise AssertionError("engine state exposes no integer budget cap (§4.1.1)")

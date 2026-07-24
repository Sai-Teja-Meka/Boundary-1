"""trials/_l2score.py — shared abstention-aware scoring for the L2 cue tasks.

The ascension trial and the humility trial score the **same tasks** through the
**same generic interface** (BOUNDARY.md §6, §7) — the only difference is the
engine behind `mk`: the full recall engine (`layer_cap = 2`) for ascension, the
capped read-by-time engine (`layer_cap = 1`) for humility. Keeping the scorer in
one place guarantees they measure identically; the gate lives in the trials.

Scoring follows the abstention-aware per-query table (§3.0):

  * answerable → correct recall            = 1000   (and *recovered* for cue-C)
  * unanswerable → abstain                 = 1000
  * answerable → abstain                   =  100
  * answerable → wrong / unanswerable → answered (fabrication) = 0

`cue_C` (§3.2, uniform weights) is the fraction of **answerable** targets
recovered; `F` (§3.1) is the mean per-query score over all cue tasks.
"""

from fractions import Fraction

import _l2tasks


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


def ingest_store(engine, mk):
    """Ingest the shared cue-task store into a fresh `mk()` state; return it."""
    state = mk()
    for p in _l2tasks.store_payloads():
        state, t = engine.ingest(state, p)
        if t is None:
            raise AssertionError("cue-task store ingest was refused — budget too small")
    return state


def score(engine, state):
    """Run every cue task against `state`; return a result dict.

    Never lets a query raise: a raised query is a harness-level failure (§7.3),
    surfaced here as an AssertionError so the trial goes RED loudly.
    """
    answerable = _l2tasks.answerable_tasks()
    unanswerable = _l2tasks.unanswerable_tasks()

    recovered = 0
    wrong = 0
    abstained_answerable = 0
    fscore_sum = 0

    for task in answerable:
        cue = task["cue"]
        if "t" in cue:
            raise AssertionError("a cue leaked t (README-l1: L1 answers by exact t)")
        ans = engine.query(state, {"op": "recall", "cue": cue})
        st = ans["status"]
        if st not in ("answer", "abstain"):
            raise AssertionError("recall returned a non-Answer status: %r" % (st,))
        if st == "answer" and ans["value"] == task["target_event"]:
            recovered += 1
            fscore_sum += 1000
        elif st == "abstain":
            abstained_answerable += 1
            fscore_sum += 100
        else:
            wrong += 1
            fscore_sum += 0

    fabricated = 0
    for task in unanswerable:
        cue = task["cue"]
        ans = engine.query(state, {"op": "recall", "cue": cue})
        st = ans["status"]
        if st not in ("answer", "abstain"):
            raise AssertionError("recall returned a non-Answer status: %r" % (st,))
        if st == "abstain":
            fscore_sum += 1000
        else:
            fabricated += 1
            fscore_sum += 0

    n_ans = len(answerable)
    total = n_ans + len(unanswerable)
    cue_c = permille(Fraction(recovered, n_ans)) if n_ans else 0
    f = permille(Fraction(fscore_sum, total * 1000)) if total else 0

    peak = state.occupancy
    cap = state.budget_cap
    b = 1000 if peak <= cap else permille(Fraction(cap, peak))

    return {
        "cue_C": cue_c,
        "F": f,
        "B": b,
        "recovered": recovered,
        "wrong": wrong,
        "abstained_answerable": abstained_answerable,
        "fabricated": fabricated,
        "n_answerable": n_ans,
        "n_unanswerable": len(unanswerable),
    }

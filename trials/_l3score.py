"""trials/_l3score.py — shared Layer-3 replay and scoring (BOUNDARY.md §3).

The ascension trial and the humility trial replay the **same streams** and score
the **same tasks** through the **same generic interface** (§6, §7) — the only
difference is the engine behind `mk`: the forgetting engine (`layer_cap = 3`)
for ascension, the capped recall engine (`layer_cap = 2`) for humility. Keeping
replay and scoring in one place guarantees they measure identically; the gate
and the ceiling live in the trials.

## The measures, and how each is read at Layer 3

**Coverage (§3.2)** — the target set is **every item in the stream**, weighted by
its `importance`; an item is *recovered* when the engine returns its exact stored
event for its cue. `weighted-C` is recovered mass over total mass; `unweighted-C`
is recovered count over count. Nothing about this is engine-defined: the
denominator is the whole 10× stream, fixed by the corpus.

**Budget (§3.3)** — occupancy is checked against the cap **after every single
write**, not once at the end, and `peak` is the running maximum. `B = 1000` iff
the cap held throughout. A breach is disqualifying (§3.3).

**Fidelity (§3.1)** — read as §5.1 L3 defends it: *"Forgetting may drop items but
must never corrupt the ones it keeps, so surviving recalls stay exact."* F is
therefore the **corruption** measure, over a query set of every item cue plus
`N_UNANSWERABLE` never-ingested cues:

  * item cue, exact stored event returned         → 1000  (and *recovered*)
  * item cue, engine abstains                     → 1000  (honest forgetting:
        the engine no longer holds it, and says so instead of inventing)
  * item cue, engine returns something else       →    0  (corruption)
  * never-ingested cue, engine abstains           → 1000
  * never-ingested cue, engine answers            →    0  (fabrication)

Abstaining is never a way to *gain*: every abstention on an item is a target
lost from coverage, and coverage is the gated measure that carries the loss.

`F_strict` is also computed and reported: the literal §3.0 table applied to the
same query set with **every** ingested item counted answerable, so an abstention
scores 100 rather than 1000. It is reported, not gated, because at a 10× stream
and a 1-in-10 budget it is arithmetically capped near 190‰ for *any* engine —
see `trials/ascension/l3/ATTAINABILITY.md`. Reporting both keeps the choice of
reading visible instead of silent.

## The keep-latest baseline is a fixture, never engine code

`keep_latest_baseline` simulates a ring buffer that keeps the most recent
budget-worth of items. It lives here, in the trials, so the anti-gaming check
runs forever without any such policy existing in `core/`.
"""

from fractions import Fraction

import _l3tasks
from _l3tasks import permille   # the one §3.5 rounding, shared with the bound


def replay(engine, mk, name):
    """Ingest a whole pressure stream; assert the cap held after every write.

    Returns `(state, report)`. `report` carries the running peak occupancy, the
    number of writes the engine refused, and the budget measure B (§3.3).
    """
    bundle = _l3tasks.stream(name)
    cap = bundle["budget_cap"]
    state = mk(cap)
    peak = 0
    refused = 0
    for i, payload in enumerate(bundle["payloads"]):
        state, t = engine.ingest(state, payload)
        if t is None:
            refused += 1
        occ = state.occupancy
        if occ > cap:
            raise AssertionError(
                "%s: occupancy %d exceeded the budget cap %d at write %d — the "
                "budget law broke mid-stream (§4.1), not merely at the end"
                % (name, occ, cap, i))
        if occ > peak:
            peak = occ
    b = 1000 if peak <= cap else permille(Fraction(cap, peak))
    return state, {"peak": peak, "cap": cap, "refused": refused, "B": b}


def score(engine, state, name):
    """Run every cue task for `name` against `state`; return a result dict.

    Never lets a query raise: a raised query is a harness-level failure (§7.3),
    surfaced here as an AssertionError so the trial goes RED loudly.
    """
    bundle = _l3tasks.stream(name)
    targets = bundle["targets"]
    total_mass = bundle["total_mass"]

    recovered = 0
    recovered_mass = 0
    wrong = 0
    abstained = 0
    fscore_sum = 0
    fstrict_sum = 0

    for target in targets:
        cue = target["cue"]
        if not _l3tasks.cue_has_no_t(cue):
            raise AssertionError("%s: a cue leaked t" % (name,))
        ans = engine.query(state, {"op": "recall", "cue": cue})
        st = ans["status"]
        if st not in ("answer", "abstain"):
            raise AssertionError("recall returned a non-Answer status: %r" % (st,))
        if st == "answer" and ans["value"] == target["event"]:
            recovered += 1
            recovered_mass += target["weight"]
            fscore_sum += 1000
            fstrict_sum += 1000
        elif st == "abstain":
            abstained += 1
            fscore_sum += 1000          # honest forgetting (see module docstring)
            fstrict_sum += 100          # the literal §3.0 reading, reported only
        else:
            wrong += 1                  # corruption: kept it, returned it wrong

    fabricated = 0
    for cue in bundle["absent_cues"]:
        ans = engine.query(state, {"op": "recall", "cue": cue})
        st = ans["status"]
        if st not in ("answer", "abstain"):
            raise AssertionError("recall returned a non-Answer status: %r" % (st,))
        if st == "abstain":
            fscore_sum += 1000
            fstrict_sum += 1000
        else:
            fabricated += 1

    n_targets = len(targets)
    n_queries = n_targets + len(bundle["absent_cues"])

    return {
        "stream": name,
        "weighted_C": permille(Fraction(recovered_mass, total_mass)),
        "unweighted_C": permille(Fraction(recovered, n_targets)),
        "F": permille(Fraction(fscore_sum, n_queries * 1000)),
        "F_strict": permille(Fraction(fstrict_sum, n_queries * 1000)),
        "recovered": recovered,
        "recovered_mass": recovered_mass,
        "total_mass": total_mass,
        "wrong": wrong,
        "abstained": abstained,
        "fabricated": fabricated,
        "n_targets": n_targets,
        "n_absent": len(bundle["absent_cues"]),
    }


def keep_latest_baseline(name):
    """The keep-latest ring buffer, as a TRIAL FIXTURE — never engine code.

    Simulates the cheapest possible order-based policy: hold the most recent
    `budget_items` items, drop the rest. Returns its weighted / unweighted
    coverage, so the ascension trial can assert forever that this policy — which
    contains no importance reasoning at all — cannot clear the Layer-3 gate on a
    stream where recency is not a proxy for importance.
    """
    bundle = _l3tasks.stream(name)
    width = bundle["budget_items"]
    kept = bundle["targets"][-width:]
    mass = sum(tg["weight"] for tg in kept)
    return {
        "stream": name,
        "policy": "keep-latest",
        "weighted_C": permille(Fraction(mass, bundle["total_mass"])),
        "unweighted_C": permille(Fraction(len(kept), len(bundle["targets"]))),
        "kept": len(kept),
    }


def fill_then_refuse_baseline(name):
    """The fill-then-refuse policy, as a trial fixture: keep the earliest worth.

    This is what the budget law (§4.1) forces on any engine below Layer 3, so it
    is the arithmetic the humility ceiling is built on — computed here from the
    corpus alone, independent of any engine, as the reference the measured capped
    engine is checked against.
    """
    bundle = _l3tasks.stream(name)
    width = bundle["budget_items"]
    kept = bundle["targets"][:width]
    mass = sum(tg["weight"] for tg in kept)
    return {
        "stream": name,
        "policy": "fill-then-refuse",
        "weighted_C": permille(Fraction(mass, bundle["total_mass"])),
        "unweighted_C": permille(Fraction(len(kept), len(bundle["targets"]))),
        "kept": len(kept),
    }

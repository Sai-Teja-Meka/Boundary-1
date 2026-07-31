"""trials/_l5score.py — shared Layer-5 replay, observation and scoring (§3, §7).

`_l5tasks` is the engine-free Stage-A module: it computes every satisfaction
point from the frozen bytes, prices the witnesses, and **scores a firing
multiset**. This module adds only what an *engine* is needed for — the replay,
the queries, the observation of what the engine actually fired, and the
assembly of the §3.0 numerator/denominator that `_l5tasks.score` then turns into
the six `§5 L5` numbers.

**One instrument.** The four exactness quantities and `F` are computed by
`_l5tasks.score`, the same function `ATTAINABILITY.md`'s oracle and its four
named baselines are scored by. Nothing here re-derives precision, recall,
`dup-fire`, `miss` or the permille calibration; this module produces the
`fires` multiset and the `answers` pair that function already takes, and hands
them over. An engine and a policy are therefore measured by one ruler, which is
the discipline `_l4score` set one layer down.

## The battery, as queries (the reading STAGE-B.md §2 declares)

| | query | answer |
|---|---|---|
| **P1** | `{"op":"fired","iid":I}` | the **list** of event records this intention fired, `t` ascending; abstain iff it never fired |
| **P2** | `{"op":"read","t":T}` | the event record `{"payload":…,"t":T}` — the Layer-1 verb |

P1 answers with a **list** and not a single record for one reason, and it is the
reason `dup-fire` is a gate clause at all: an intention that fired twice must be
visible **through the query interface**, not only in an engine's own
bookkeeping. A correct answer is a one-element list; a two-element list is a
wrong answer *and* a `dup-fire`, and both are scored.

P2 is deliberately the **Layer-1 `read` verb** (`ATTAINABILITY.md §2`): it asks
the engine to hand back the event it emitted at the `t` it assigned, which is
what makes *"the payload matched"* a measurement rather than a definition.

## The `t` identity, and why the self-report cannot lie

Under the `t` semantics settled in `STAGE-B.md §1` — a firing is an event, `§1.3`
gives it a `t` of its own, and nothing else in the stream consumes one — the
engine's own `next_t` counts the firings for us:

```
next_t  −  |caller stream|  ==  the number of firings the engine emitted
```

`observe` asserts that identity against the engine's P1 report. An engine that
fired twice and reported once fails it; so does one that emitted an event the
battery never asked for. The report is checked against the clock the constitution
gives the engine, not taken on trust.

## What this module does not do

It applies no gate and declares no threshold. The gates live in
`ascension/l5/t_prospection.py`, the ceiling in `humility/l5/t_prospection.py`,
and their authority in `laws/t_rulings.py`.
"""

import collections
from fractions import Fraction

import _l4score
import _l5tasks
from _l5tasks import permille

# The rule-P atom audit's header allowance, shared verbatim with Layer 4 rather
# than restated: it is the same audit of the same §4.1 accounting (R4 clause 3).
RULE_P_HEADER_ALLOWANCE = _l4score.RULE_P_HEADER_ALLOWANCE

# A caller index no satisfaction point can equal, used to carry a firing that
# landed at a logical `t` the corpus does not put a firing at. `_l5tasks.score`
# compares against `sigma`, a non-negative caller index, so a negative sentinel
# is a firing that is counted, never correct, and never silently re-aligned.
def _misplaced(t):
    return -(t + 1)


# ---- replay -----------------------------------------------------------------

def replay(engine, mk, b=None, cap=None):
    """Ingest the whole caller stream; assert the cap held after **every** write.

    Returns `(state, report)`. The cap is `ATTAINABILITY.md §1`'s Reading 2 —
    `raw_cells // 4`, the Layer-4 footprint ratio carried forward because `§5 L5`
    declares no pressure ratio of its own. That reading is **ratified**:
    `BOUNDARY-RULINGS.md R6` clause 4 rules `budget_cap = raw_cells // 4 =
    45 638` on `corpora/l5stream`, and rules with it that the events the engine
    emits compete for cells inside that cap without enlarging it. No footprint
    gate is created by it — `§5 L5` states none. The battery still reads the
    number from `_l5tasks` rather than hard-coding one, so the ruled ratio is
    applied to whatever corpus is measured rather than to a constant.

    `B = 1000` is certified after every single write, never once at the end: the
    budget law refuses mid-stream (§4.1.2), so a state that would exceed the cap
    must be caught where it happens.

    `cap` overrides the declared cap. The only caller that passes one is the
    Layer-5 humility trial, which measures the capped engine a second time
    **in budget** to separate two different incapacities — not recording an
    intention, and not reading one as a condition — and says so in its own text.
    """
    if b is None:
        b = _l5tasks.corpus()
    if cap is None:
        cap = b["budget_cap"]
    state = mk(cap)
    peak = 0
    refused = 0
    for i, payload in enumerate(b["payloads"]):
        state, t = engine.ingest(state, payload)
        if t is None:
            refused += 1
        occ = state.occupancy
        if occ > cap:
            raise AssertionError(
                "l5stream: occupancy %d exceeded the Layer-5 cap %d at caller "
                "write %d — the budget law broke mid-stream (§4.1), not merely "
                "at the end" % (occ, cap, i))
        if occ > peak:
            peak = occ
    return state, {
        "peak": peak, "cap": cap, "refused": refused,
        "B": 1000 if peak <= cap else permille(Fraction(cap, peak)),
        "occupancy": state.occupancy,
        "next_t": state.next_t,
    }


# ---- observation ------------------------------------------------------------

def _ask(engine, state, query):
    """One query through the generic interface; a raised query is a hard failure (§7.3)."""
    ans = engine.query(state, query)
    if not isinstance(ans, dict) or ans.get("status") not in ("answer", "abstain"):
        raise AssertionError("query %r returned a non-Answer: %r" % (query, ans))
    return ans


def observe(engine, state, b=None):
    """What the engine fired, read off its own §7 answers, with the `t` identity checked.

    Returns a dict carrying, per intention, the raw P1 Answer and the list of
    logical `t` it reports firing at — plus the totals the `t` identity is
    asserted over. Nothing here scores; `score` does.
    """
    if b is None:
        b = _l5tasks.corpus()

    p1 = collections.OrderedDict()
    total_fires = 0
    malformed = []
    for iid in b["intents"]:
        ans = _ask(engine, state, {"op": "fired", "iid": iid})
        ts = []
        if ans["status"] == "answer":
            value = ans["value"]
            if (isinstance(value, list) and value
                    and all(isinstance(e, dict) and isinstance(e.get("t"), int)
                            and not isinstance(e.get("t"), bool)
                            and "payload" in e for e in value)):
                ts = [e["t"] for e in value]
            else:
                # An answered P1 that is not a non-empty list of event records
                # is a wrong answer, not an unreadable one: it is scored 0 and
                # recorded here so the trial can say which shape broke.
                malformed.append((iid, value))
        p1[iid] = {"answer": ans, "t": ts}
        total_fires += len(ts)

    return {
        "p1": p1,
        "total_fires": total_fires,
        "malformed": malformed,
        "next_t": state.next_t,
        "n": b["n"],
        "emitted_by_clock": state.next_t - b["n"],
    }


def assert_t_identity(obs):
    """`next_t − |caller stream|` == the firings the engine reports (STAGE-B.md §1).

    The engine's own logical clock is the auditor of its own firing report. This
    is the one check in the battery that no bookkeeping can satisfy by being
    tidy: a firing is an event, `§1.3` gives it a `t` of its own and forbids two
    events sharing one, and no other event in a Layer-5 replay consumes a `t`.
    """
    if obs["emitted_by_clock"] != obs["total_fires"]:
        raise AssertionError(
            "the engine advanced `next_t` to %d over a %d-event caller stream — "
            "%d logical times spent on events it did not receive — while "
            "reporting %d firings. Under §1.3 a firing is an event and consumes "
            "exactly one `t`, and nothing else in this stream consumes one, so "
            "the two numbers are the same number (STAGE-B.md §1). They are not."
            % (obs["next_t"], obs["n"], obs["emitted_by_clock"],
               obs["total_fires"]))


# ---- scoring ----------------------------------------------------------------

def score(engine, state, b=None):
    """The six `§5 L5` numbers, plus the honesty counters, through `_l5tasks.score`."""
    if b is None:
        b = _l5tasks.corpus()
    obs = observe(engine, state, b)
    assert_t_identity(obs)

    fire_t = b["fire_t"]
    sat = b["sat"]
    t_to_caller = dict((fire_t[iid], sat[iid]) for iid in b["fireable"])

    fires = []
    p1_total = 0
    wrong = 0
    fabricated = 0
    p2_total = 0
    p2_exact = 0

    for iid, rec in obs["p1"].items():
        ans = rec["answer"]
        ts = rec["t"]
        expected_t = fire_t.get(iid)
        expected_payload = b["intents"][iid]["fire"]

        for t in ts:
            fires.append((iid, t_to_caller.get(t, _misplaced(t))))

        # ---- P1, one query per intention, scored under the literal §3.0 table
        if sat[iid] is None:
            # Unanswerable: the only correct behaviour is to abstain.
            if ans["status"] == "abstain":
                p1_total += 1000
            else:
                p1_total += 0
                fabricated += 1
        elif ans["status"] == "abstain":
            p1_total += 100                      # honest, and still a loss
        elif (len(ts) == 1 and ts[0] == expected_t
              and ans["value"] == [{"payload": expected_payload, "t": expected_t}]):
            p1_total += 1000
        else:
            p1_total += 0
            wrong += 1

        # ---- P2, one query per firing the engine actually emitted
        for t in ts:
            p2_total += 1
            got = _ask(engine, state, {"op": "read", "t": t})
            if (got["status"] == "answer"
                    and got["value"] == {"payload": expected_payload, "t": t}
                    and t == expected_t and len(ts) == 1):
                p2_exact += 1

    n = len(b["intents"]) + p2_total
    row = _l5tasks.score(fires, (p1_total + p2_exact * 1000, n))
    row.update({
        "wrong": wrong,
        "fabricated": fabricated,
        "n_p1": len(b["intents"]),
        "n_p2": p2_total,
        "battery": n,
        "next_t": obs["next_t"],
        "emitted": obs["emitted_by_clock"],
        "malformed": len(obs["malformed"]),
    })
    return row


# ---- the footprint, priced under rule P (R4 clause 3) -----------------------

def footprint(state, b=None):
    """`permille(occupancy / raw_cells)` — the engine's own §4.1 accounting."""
    if b is None:
        b = _l5tasks.corpus()
    return permille(Fraction(state.occupancy, b["raw_cells"]))


def snapshot_atoms(engine, state):
    """The half of rule P a trial can see from outside an engine (`_l4score`'s audit).

    Shared verbatim with Layer 4 rather than re-expressed: it is the same audit
    of the same §4.1 accounting, and R4 clause 3 ruled rule P general and not
    Layer-4-only. The packing half — a composite scalar carrying two atoms — is
    structural and remains the engine's obligation.
    """
    return _l4score.snapshot_atoms(engine, state)

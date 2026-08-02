"""ops/l6 — the Layer-6 engine's composition: one reading, one ruler, no new state.

The Layer-6 analogue of `ops/l4/t_l4_composition.py` and
`ops/l5/t_l5_composition.py`. Those two priced a design before its code and then
asserted the price; this one has almost nothing to price, and asserting *that* is
the work — `§5.1 L6` defends `B = 1000` with *"meta-memory derives confidence
from **existing state** within budget"*, and an engine that quietly grew a
structure would have moved a sentence of the constitution rather than a number.

Five things, and every one of them is a place a Layer-6 engine could drift
silently:

1. **The declared set-once reading is one reading with two implementations.**
   `core.layers.l6_meta_memory.SET_ONCE_KEYS` and `_l6btasks.SET_ONCE_KEYS` must
   agree, and the engine's `set_once` must agree with the battery's
   `set_once_tie` feature **query by query** over the whole frozen artifact. A
   divergence here does not merely change a score: it moves the CONFIDENCE on a
   query whose answer is a coin flip, which is the one thing this layer is for.
2. **`§3.5`'s permille is one function with three implementations**, and they are
   checked against each other on a declared grid that includes both half-way
   cases — the engine's, the battery instrument's, and `l2_recall`'s, which has
   been in `core/` since Layer 2.
3. **No new state.** The canonical body of a Layer-6 state equals the Layer-5
   state's over the same stream in every branch but the recorded `layer_cap`, and
   `accounted_occupancy` is Layer 5's function unchanged, so the engine's own
   accounting and the atoms a reader can count in its serialized state are still
   the same number (rule P, `R4` clause 3).
4. **The model is readable through `§7` alone.** The `calibration` op reports the
   declared vocabulary, the ties the engine currently holds and the confidence it
   would state at each — the shape `consolidation` (L4) and `prospection` (L5)
   established — so a trial never has to reach into the state to see the model.
5. **The confidence is a function of the chain's SHAPE and of nothing else.**
   Two observationally identical chains get the identical number. That is `R7`
   clause 3(b)'s class-E boundary stated of the engine, and `strain/l6` turns it
   into the assertion that no mirror pair is resolved.

Nothing here applies a gate. `§5 L6`'s clauses live in `ascension/l6`, the
ceiling in `humility/l6`, and their authority in `laws/t_rulings.py`; this file
declares no `GATE_*` or `CEILING_*` constant at all.
"""

from fractions import Fraction

from _harness import require, require_equal
from adapters import l5, l6

import _l6btasks
import _l6tasks

from core.layers import l2_recall as l2m
from core.layers import l5_prospection as l5m

# The declared grid §3.5's rounding is checked on. It carries both half-way
# cases on purpose: 1/2000 rounds DOWN to the even neighbour 0 and 3/2000 rounds
# UP to the even neighbour 2, which is the only place a "round half up"
# implementation and a "round half to even" one disagree.
PERMILLE_GRID = (
    Fraction(0), Fraction(1), Fraction(1, 2), Fraction(1, 3), Fraction(2, 3),
    Fraction(1, 22), Fraction(21, 22), Fraction(41, 42), Fraction(1, 44),
    Fraction(1, 2000), Fraction(3, 2000), Fraction(5, 2000), Fraction(7, 2000),
    Fraction(1999, 2000), Fraction(1997, 2000),
)

_RUN = {}


def _replayed():
    """battery-b through both engines, once per process."""
    if "pair" not in _RUN:
        payloads = _l6btasks.stream()
        s6 = l6.make_engine(6, l6.DEFAULT_BUDGET)
        s5 = l5.make_engine(5, l5.DEFAULT_BUDGET)
        for payload in payloads:
            s6, t6 = l6.ingest(s6, payload)
            s5, t5 = l5.ingest(s5, payload)
            require(t6 is not None and t5 is not None,
                    "an in-budget write was refused at DEFAULT_BUDGET")
            require_equal(t6, t5,
                          "the Layer-6 engine assigned a different logical time "
                          "than the Layer-5 engine on the same payload — Layer 6 "
                          "adds no state and must add no event either")
        _RUN["pair"] = (s6, s5)
    return _RUN["pair"]


# ---- 1. one reading, two implementations ------------------------------------

def trial_the_declared_set_once_reading_is_one_reading_with_two_implementations():
    """The engine's `SET_ONCE_KEYS` and the battery's, agreeing query by query.

    `ASSERTION_FORMS` at Layer 4 and `INTENTION_FORM` at Layer 5 are each a
    declared reading of a frozen grammar checked against the battery's
    independent copy event by event, *"because unlike a coverage miss a
    divergence here moves a firing"*. At Layer 6 a divergence moves a
    **confidence** — and it moves it on exactly the class where the answer is a
    coin flip, so the two halves would disagree precisely where it mattered most
    and nowhere else.

    The check is stronger than equal constants: for **every** query in the frozen
    artifact, the engine's `set_once(key) and n_distinct > 1` must equal the
    battery's `evidence(q)["set_once_tie"]`, computed by different code from the
    same bytes.
    """
    require_equal(list(l6.SET_ONCE_KEYS), list(_l6btasks.SET_ONCE_KEYS),
                  "the engine's declared set-once reading and the battery's "
                  "have drifted apart")

    state, _s5 = _replayed()
    seen_tie = 0
    for record in _l6btasks.queries():
        q = record["q"]
        horizon = q["t"] if q["op"] == "asof" else None
        steps = l6.visible_chain(state, q["entity"], q["key"], horizon)
        engine_tie = 1 if (l6.set_once(q["key"]) and l6.n_distinct(steps) > 1) else 0
        battery_tie = _l6btasks.evidence(q)["set_once_tie"]
        require_equal(engine_tie, battery_tie,
                      "qid %d (%s %r/%r): the engine reads set_once_tie = %d "
                      "where the battery's declared evidence reads %d — one "
                      "reading, two implementations, and they have diverged"
                      % (record["qid"], q["op"], q["entity"], q["key"],
                         engine_tie, battery_tie))
        seen_tie += engine_tie
    require_equal(seen_tie, _l6btasks.REGION_QUERIES,
                  "the tie is no longer exactly the forcing region — battery-b's "
                  "`origin` is asserted by nothing but the region, so a tie "
                  "elsewhere means the reading or the artifact moved")


def trial_the_permille_function_is_one_function_with_three_implementations():
    """`§3.5`, in `core/` twice and in the instrument once — checked, not assumed.

    `§3.5` is a procedure and not a preference: round-half-to-**even** on the
    exact rational, *"so the result is platform-independent"*. The engine states
    its confidence through it, `_l6tasks` renders every score in this project
    through it, and `l2_recall` has carried a copy since Layer 2. Three copies of
    one ratified paragraph is two chances to drift, so the grid below includes
    the half-way cases where a round-half-**up** implementation would disagree.
    """
    for x in PERMILLE_GRID:
        want = _l6tasks.permille(x)
        require_equal(l6.permille(x), want,
                      "the engine's permille(%s) differs from the instrument's"
                      % (x,))
        require_equal(l2m._permille(x), want,
                      "l2_recall's permille(%s) differs from the instrument's"
                      % (x,))
    require_equal(l6.permille(Fraction(1, 2000)), 0,
                  "§3.5 rounds a half to the EVEN neighbour: 1/2000 is 0.5 "
                  "permille and must round DOWN to 0")
    require_equal(l6.permille(Fraction(3, 2000)), 2,
                  "§3.5 rounds a half to the EVEN neighbour: 3/2000 is 1.5 "
                  "permille and must round UP to 2")


# ---- 2. no new state ---------------------------------------------------------

def trial_layer_6_adds_no_state_to_layer_5():
    """`§5.1 L6`: *"meta-memory derives confidence from existing state"*, as bytes.

    The canonical body of the Layer-6 state after the whole 12 000-event artifact
    equals the Layer-5 state's branch for branch, with exactly one atom
    different — the recorded `layer_cap`, which is the cap and not the content.
    `ATTAINABILITY-B.md §3.2` priced the marginal state at 18 cells and disclaimed
    nothing; the engine spends 0, and this is where that is a measurement rather
    than a claim.

    It is also the assertion that keeps `inheritance/l6`'s Layer-5 row honest for
    a structural reason instead of an empirical one: a confidence model that cost
    cells would compete with a pending set and a fired ledger that `README-l5
    §0.1` puts outside every eviction phase, and one that costs none cannot.
    """
    s6, s5 = _replayed()
    body6 = l5m._body(s6)
    body5 = l5m._body(s5)
    differing = sorted(k for k in body6 if body6[k] != body5[k])
    require_equal(differing, ["layer_cap"],
                  "the Layer-6 state differs from the Layer-5 state in branches "
                  "other than the recorded cap: %r" % (differing,))
    require_equal((body5["layer_cap"], body6["layer_cap"]), (5, 6),
                  "the two states no longer record the caps they were built at")
    require_equal(s6.occupancy, s5.occupancy,
                  "the Layer-6 engine's occupancy diverged from the Layer-5 "
                  "engine's on the same stream — a confidence model that cost "
                  "cells is one that competes with the prospection tiers")
    require_equal(l6.accounted_occupancy(s6), s6.occupancy,
                  "the engine's incremental accounting drifted from the cost "
                  "recomputed from the state alone (rule P, R4 clause 3)")
    require_equal(l6.snapshot(l6.restore(l6.snapshot(s6))), l6.snapshot(s6),
                  "the Layer-6 snapshot does not round-trip byte-identically")
    require(isinstance(l6.restore(l6.snapshot(s6)), l6.L6State),
            "restoring a Layer-6 snapshot did not produce a Layer-6 state — a "
            "state restored through the Layer-5 reader would answer every query "
            "correctly and state 1000 on a tie")


def trial_a_layer_5_snapshot_still_restores_through_the_layer_6_reader():
    """A capped engine's state round-trips exactly as it always did (§7.4, §9.2).

    `restore` dispatches on the envelope's `magic`, so an older snapshot takes the
    frozen path below and is not reinterpreted by a layer that did not write it.
    """
    _s6, s5 = _replayed()
    older = l5.snapshot(s5)
    back = l6.restore(older)
    require(isinstance(back, l6.L5State) and not isinstance(back, l6.L6State),
            "a Layer-5 snapshot restored through the Layer-6 reader came back as "
            "a Layer-6 state — the cap a snapshot records is the cap it keeps")
    require_equal(l5.snapshot(back), older,
                  "a Layer-5 snapshot did not survive the Layer-6 reader")


# ---- 3. the model, read through §7 -------------------------------------------

def trial_the_confidence_model_is_readable_through_the_query_interface():
    """The `calibration` op: the declared vocabulary, the ties, and the levels.

    `§7.1` declares three operations and a trial speaks to an engine through them
    alone. `consolidation` (L4) and `prospection` (L5) each surfaced their layer's
    own bookkeeping this way; this is Layer 6's, and it is what lets `strain/l6`
    watch the model move without reaching into the state.
    """
    state, _s5 = _replayed()
    answer = l6.query(state, {"op": "calibration"})
    require_equal(set(answer), {"status", "value", "confidence", "provenance"},
                  "the Answer contract (§7.2)")
    require_equal(answer["status"], "answer", "the calibration op abstained")
    value = answer["value"]
    require_equal(sorted(value), ["set_once_keys", "tie_levels", "ties"],
                  "the calibration report's declared shape drifted")
    require_equal(value["set_once_keys"], list(l6.SET_ONCE_KEYS),
                  "the reported vocabulary is not the declared one")
    require_equal(value["ties"], _l6btasks.REGION_QUERIES,
                  "the engine reads %d ties on battery-b where the forcing "
                  "region is %d chains" % (value["ties"], _l6btasks.REGION_QUERIES))
    require_equal(value["tie_levels"], [[2, 500]],
                  "every mirror pair carries exactly two `origin` assertions "
                  "with two distinct values, so the only level the engine holds "
                  "is permille(1/2) = 500 — the tie's own arithmetic")


def trial_the_tie_confidence_is_derived_from_the_chain_and_not_typed():
    """`permille(1/d)`, exhibited at every `d` a chain could reach.

    `ATTAINABILITY-B.md §3.1` records that the witness's 500 is *derived* —
    `permille(1/2)`, the region's measured accuracy — *and not chosen*. The engine
    states the same number for the same reason, and the reason generalises: `d`
    mutually exclusive claimants for a slot that admits one, a reading that
    commits to one of them, `1/d`.

    Built as a fixture rather than measured on the frozen artifact, because
    battery-b holds only `d = 2` — and a level nothing exercises is a level that
    could be wrong.
    """
    state = l6.make_engine(6, l6.DEFAULT_BUDGET)
    key = l6.SET_ONCE_KEYS[0]
    entity = 7
    want = (1000, 1000, 500, 333, 250, 200)
    values = ("a", "a", "b", "c", "d", "e")
    for i, value in enumerate(values):
        state, t = l6.ingest(state, {"kind": "attr", "entity": entity,
                                     "key": key, "val": value})
        require(t is not None, "an in-budget write was refused")
        answer = l6.query(state, {"op": "current", "entity": entity, "key": key})
        require_equal(answer["status"], "answer",
                      "the engine abstained on a chain it holds")
        require_equal(answer["confidence"], want[i],
                      "after %d assertions (%d distinct) the engine states %d, "
                      "not permille(1/d) = %d"
                      % (i + 1, l6.n_distinct(l6.visible_chain(state, entity, key)),
                         answer["confidence"], want[i]))
        require_equal(answer["value"], value,
                      "the answer is the frozen Layer-4 reader's: latest wins. "
                      "Layer 6 attaches a number; it does not answer differently")


def trial_a_key_the_reading_does_not_call_set_once_is_never_a_tie():
    """The discrimination half: a legal update is not a contradiction.

    A chain that disagrees with itself is a contradiction only where the key
    admits one value. On an ordinary key the latest assertion IS what is in force,
    so the engine is right and says so — and an engine that hedged there would be
    the key-blind `conflict-rank` policy, which `ATTAINABILITY-B.md §4.3` measures
    65 permille of AUROC margin worse than the set-once-aware witness.
    """
    state = l6.make_engine(6, l6.DEFAULT_BUDGET)
    key = "colour"
    require(not l6.set_once(key), "the fixture key must not be a declared "
                                  "set-once key or it tests nothing")
    for value in ("red", "green", "blue", "amber"):
        state, t = l6.ingest(state, {"kind": "attr", "entity": 11,
                                     "key": key, "val": value})
        require(t is not None, "an in-budget write was refused")
        answer = l6.query(state, {"op": "current", "entity": 11, "key": key})
        require_equal(answer["confidence"], l6.CERTAIN,
                      "the engine hedged on an ordinary chain that was legally "
                      "updated four times — %r" % (answer,))
        require_equal(answer["value"], value, "latest wins on an ordinary key")


def trial_as_of_prices_the_evidence_the_answer_actually_had():
    """The horizon is the prefix, because a later assertion is not evidence at `t`.

    `_l6btasks.evidence` takes the `as-of` prefix and so does the engine. The
    consequence is visible and worth pinning: an `as-of` asked before a set-once
    key's second, contradicting assertion sees one value, is right, and says
    1000 — while `current` on the same chain sees two, is a coin flip, and says
    500. Confidence that ignored the horizon would understate the first and
    overstate nothing.
    """
    state = l6.make_engine(6, l6.DEFAULT_BUDGET)
    key = l6.SET_ONCE_KEYS[0]
    state, t0 = l6.ingest(state, {"kind": "attr", "entity": 3,
                                  "key": key, "val": "first"})
    state, t1 = l6.ingest(state, {"kind": "attr", "entity": 3,
                                  "key": key, "val": "second"})
    early = l6.query(state, {"op": "asof", "entity": 3, "key": key, "t": t0})
    late = l6.query(state, {"op": "asof", "entity": 3, "key": key, "t": t1})
    now = l6.query(state, {"op": "current", "entity": 3, "key": key})
    require_equal(early["confidence"], l6.CERTAIN,
                  "an as-of before the contradiction saw one value and must say "
                  "so — %r" % (early,))
    require_equal(early["value"], "first", "as-of honours supersession (§ L4)")
    require_equal(late["confidence"], 500,
                  "an as-of after the contradiction sees the tie")
    require_equal(now["confidence"], 500, "current sees the tie")


# ---- 4. the class-E boundary, of the engine ----------------------------------

def trial_the_confidence_reads_the_chains_shape_and_never_the_id_or_the_time():
    """`R7` clause 3(b)'s class-E boundary, asserted of the ENGINE.

    Theorem 1 leaves exactly two handles — the raw entity id and the absolute
    logical time — and Theorem 2 shows neither carries signal. The declared
    evidence vocabulary excludes both *"because including them would let a
    class-E policy split a pair"*. An engine has to **be** class E rather than be
    declared it, and this is the mechanical statement of that: rebuild each
    member of a mirror pair as a standalone chain under a different entity id and
    at different logical times, and the confidence must not move.

    `strain/l6` asserts the consequence on the frozen artifact — that no pair is
    resolved. This asserts the cause.
    """
    key = l6.SET_ONCE_KEYS[0]
    confidences = set()
    values = set()
    for entity, offset in ((500000, 0), (500001, 1), (12, 40), (99999, 7)):
        state = l6.make_engine(6, l6.DEFAULT_BUDGET)
        for _pad in range(offset):
            state, t = l6.ingest(state, {"kind": "spawn", "entity": 1,
                                         "class": "node"})
            require(t is not None, "an in-budget write was refused")
        for value in ("x", "y"):
            state, t = l6.ingest(state, {"kind": "attr", "entity": entity,
                                         "key": key, "val": value})
            require(t is not None, "an in-budget write was refused")
        answer = l6.query(state, {"op": "current", "entity": entity, "key": key})
        confidences.add(answer["confidence"])
        values.add(answer["value"])
    require_equal(sorted(confidences), [500],
                  "the engine's confidence moved with the entity id or with the "
                  "absolute logical time: %r. Those are the two handles Theorem 1 "
                  "leaves, and a model that read either could split a mirror pair "
                  "— which would make it class O by R7 clause 3(b)'s definition"
                  % (sorted(confidences),))
    require_equal(sorted(values), ["y"],
                  "the reading moved with the id or the time as well")

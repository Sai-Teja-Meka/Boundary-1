"""inheritance/l4 — Layer 4 must still be Layers 1, 2 and 3 (BOUNDARY.md §5).

The debut of the **inheritance** class (see `trials/inheritance/README.md`). It
replays the older layers' own ratified batteries against the *current* engine at
`layer_cap = 4`, on **in-budget** streams — no pressure, no excuse:

| what | battery | gate re-applied |
|---|---|---|
| Layer 1 verbs | `write` / `read` / `read_range` / `snapshot` / `restore` / the Answer contract | exact IO, byte-identical round trip, deterministic refusal |
| Layer 2 cues | `_l2tasks` / `_l2score`, the same store and probes `ascension/l2` uses | `cue-C ≥ 900`, `F ≥ 950`, `B = 1000` |
| Layer 3 retention | `_l3tasks` / `_l3score`, both frozen pressure streams | everything recalled: no drop is *permitted*, so none is excused |

Engine-gated: every trial that needs an engine SKIPS until
`trials/adapters/l4.py` exists (Stage C), then holds forever.

## Why "in-budget" is the whole point

Layer 3's gate is scored under 10× pressure, where dropping is lawful and the
question is *which* items survive. Inheritance asks the opposite question: when
**nothing forces a drop**, does the new layer still do what the old ones
promised? A consolidation engine that quietly summarized in-budget events —
because summarizing is what it now does — would score beautifully on Layer 4's
own battery while having silently repealed Layer 1's `F = 1000`. So the streams
are replayed at a cap `INBUDGET_MULTIPLE ×` their own raw episodic footprint,
which is generous **by declaration**: at that cap a refusal, an eviction or a
lossy answer is not a budget consequence, it is a regression. Every recall must
return the exact stored event, and `weighted-C`, `unweighted-C` and `F` must all
read 1000 — asserted as identities rather than as thresholds, because there is
no threshold to argue about when nothing was under pressure.

## What this class is not

It is not `anchors/`. Anchors freeze the exact past behaviour of the *older
engines*, replayed through their *own* adapters (`anchors/l1.json` still runs
against `adapters/l1`), and they prove those engines never changed. Inheritance
proves something anchors structurally cannot: that the **new** engine, which is
a different program, still answers the old questions. Nor is it `ascension/`,
which scores layer N's own capability against layer N's own gate.

The three batteries are the frozen ones, imported rather than re-expressed —
`_l2tasks`/`_l2score` and `_l3tasks`/`_l3score` are the very modules the L2 and
L3 ascension trials score with, so an inherited battery cannot drift into an
easier one. The Layer-1 verbs have no shared task module (their trial is
`ops/l1/t_verbs.py`, which speaks to `adapters/l1` directly and is frozen), so
they are re-expressed here against the generic interface and their agreement
with the frozen file is a reading obligation, stated here rather than implied.
"""

from _harness import require, require_equal, try_import
import _l2score
import _l2tasks
import _l3score
import _l3tasks
from core.state import event_cost

# The ratified gates of the layers being inherited, re-applied at cap 4. Every
# one is §5 text, quoted in `laws/t_rulings.py`'s registry against this file.
GATE_L2_CUE_C = 900          # §5 L2
GATE_L2_F = 950              # §5 L2
GATE_B = 1000                # §5 L1/L2/L3 — the budget law, absolute at every layer

LAYER_CAP = 4

# The in-budget cap, as a multiple of a stream's own raw episodic footprint.
# Four times is generous by declaration: it leaves room for an index, a derived
# schema, and whatever bookkeeping Layer 4 needs, so that nothing the engine
# drops here can be blamed on the budget law.
INBUDGET_MULTIPLE = 4

# ...and a floor, so a battery of three events is not starved by an engine's
# fixed structures. A multiple alone would make the smallest batteries the
# tightest, which is the opposite of this class's intent.
INBUDGET_FLOOR = 4096

# Fixed payloads for the Layer-1 verb battery (uniform shape => predictable,
# uniform cost), the same shapes `ops/l1/t_verbs.py` uses.
_P0 = {"kind": "spawn", "entity": 1, "class": "node"}
_P1 = {"kind": "spawn", "entity": 2, "class": "agent"}
_P2 = {"kind": "spawn", "entity": 3, "class": "vault"}

_ANSWER_KEYS = {"status", "value", "confidence", "provenance"}


def _engine():
    return try_import(
        "adapters.l4",
        "no L4 engine yet; the inheritance battery engages when built "
        "(Stage C) and stands from then on")


def _fresh(engine, cap):
    return engine.make_engine(LAYER_CAP, cap)


def _inbudget_cap(payloads):
    return max(INBUDGET_MULTIPLE * sum(event_cost(p) for p in payloads),
               INBUDGET_FLOOR)


def _replay_in_budget(engine, cap, payloads, name):
    """Ingest a whole stream at `cap`, asserting the cap held after every write.

    `_l3score.replay` does exactly this at Layer 3's own **pressure** cap, which
    it reads from the frozen task bundle. That module is a frozen Layer-3 trial
    helper (§9.2) and is not edited to take a second cap, so the in-budget
    replay is expressed here — six lines, the same contract, and the *scoring*
    still goes through `_l3score.score` so the measurement itself is shared.
    """
    state = engine.make_engine(LAYER_CAP, cap)
    peak = 0
    refused = 0
    for i, payload in enumerate(payloads):
        state, t = engine.ingest(state, payload)
        if t is None:
            refused += 1
        occ = state.occupancy
        if occ > cap:
            raise AssertionError(
                "%s: occupancy %d exceeded the in-budget cap %d at write %d — "
                "the budget law broke mid-stream (§4.1)" % (name, occ, cap, i))
        peak = max(peak, occ)
    return state, {"peak": peak, "cap": cap, "refused": refused,
                   "B": 1000 if peak <= cap else 0}


# ---- Layer 1: the verbs -----------------------------------------------------

def trial_layer4_inherits_the_layer1_verbs():
    """`write` / `read` / `read_range` at cap 4: exact IO, or Layer 1 is repealed.

    §5 L1 gates Retention at `F = 1000` — *"the exact return of what was
    written, read by time and by range, so any deviation is a bug, not a
    tolerance"*. A consolidation engine derives; it must still return.
    """
    l4 = _engine()
    cap = _inbudget_cap([_P0, _P1, _P2])
    s = _fresh(l4, cap)

    s, t0 = l4.ingest(s, _P0)
    s, t1 = l4.ingest(s, _P1)
    s, t2 = l4.ingest(s, _P2)
    require_equal((t0, t1, t2), (0, 1, 2),
                  "t must begin at 0 and increase by one per successful write "
                  "(§1.3) — logical time is engine-owned at every layer")

    for t, payload in ((0, _P0), (1, _P1), (2, _P2)):
        ans = l4.query(s, {"op": "read", "t": t})
        require_equal(ans["status"], "answer",
                      "an in-budget read(t=%d) abstained at cap 4" % (t,))
        require_equal(ans["value"], {"payload": payload, "t": t},
                      "read(t=%d) is not byte-exact at cap 4 — Layer 1's F=1000 "
                      "is not a tolerance" % (t,))

    e0 = {"payload": _P0, "t": 0}
    e1 = {"payload": _P1, "t": 1}
    e2 = {"payload": _P2, "t": 2}
    got = l4.query(s, {"op": "read_range", "t0": 0, "t1": 2})
    require_equal(got["status"], "answer", "read_range abstained on a full range")
    require_equal(got["value"], [e0, e1, e2], "read_range is not exact at cap 4")
    require_equal(l4.query(s, {"op": "read_range", "t0": 1, "t1": 99})["value"],
                  [e1, e2], "read_range is not clamped to the log end at cap 4")
    require_equal(l4.query(s, {"op": "read_range", "t0": 1, "t1": 0})["value"],
                  [], "an inverted range must be empty at cap 4")

    # Out of range abstains, and does not raise (§7.3).
    miss = l4.query(s, {"op": "read", "t": 9})
    require_equal(miss["status"], "abstain",
                  "an out-of-range read must abstain, not raise (§7.3)")
    require(miss["value"] is None, "an abstention carries a null value")

    # The Answer contract (§7.2) survives the new layer.
    hit = l4.query(s, {"op": "read", "t": 0})
    require_equal(set(hit.keys()), _ANSWER_KEYS,
                  "Answer keys must be exactly status/value/confidence/provenance")
    require(isinstance(hit["confidence"], int) and 0 <= hit["confidence"] <= 1000,
            "confidence must be an integer permille in [0,1000] (§3.4)")

    # An unsupported query is still a scored abstention, never an exception.
    for q in ({"op": "no_such_op"}, {"nonsense": 1}, "not-a-dict", 42):
        require_equal(l4.query(s, q)["status"], "abstain",
                      "an unsupported query must abstain, never raise: %r" % (q,))


def trial_layer4_inherits_the_budget_law_and_the_snapshot_round_trip():
    """The budget law at cap 4, and §5 L1's byte-identical round trip.

    **What is inherited here is the law, not one layer's response to it.** §4.1.2
    makes a write that would breach the cap a deterministic refusal *and* says
    eviction is a Layer-3 capability rather than a budget side-effect — so a
    Layer-4 engine, which has Layer 3, may lawfully evict where a Layer-1 engine
    must refuse. What may never differ is the invariant both responses serve:
    **occupancy never exceeds the cap, and a refusal is total.**

    So the assertions are exactly that, and no more: at a cap too small for the
    stream the engine may refuse or may evict, but if it refuses the state must
    come back byte-identical (no partial write), and either way the cap holds. A
    payload that could never fit *any* state at this cap must be refused, since
    there is nothing to evict that would make room.
    """
    l4 = _engine()

    # The cap is taken from the engine's OWN accounting of two events — an
    # engine that keeps an index or a schema charges more per event than the raw
    # payload costs, and a cap computed from `event_cost` alone would starve it
    # and test the fixture instead of the law.
    probe = _fresh(l4, _inbudget_cap([_P0, _P1, _P2]))
    probe, _t = l4.ingest(probe, _P0)
    probe, _t = l4.ingest(probe, _P1)
    cap = probe.occupancy

    s = _fresh(l4, cap)
    s, t0 = l4.ingest(s, _P0)
    s, t1 = l4.ingest(s, _P1)
    require_equal((t0, t1), (0, 1),
                  "two events did not fit a cap set to their own measured cost")

    before = l4.snapshot(s)
    occ_before = s.occupancy
    after, t2 = l4.ingest(s, _P2)
    require(after.occupancy <= cap,
            "a write past a full budget left occupancy %d above the cap %d — "
            "the budget law is absolute at every layer (§4.1)"
            % (after.occupancy, cap))
    if t2 is None:
        require_equal(after.occupancy, occ_before,
                      "a refused write must not change occupancy")
        require_equal(l4.snapshot(after), before,
                      "a refused write must leave the state UNCHANGED — no "
                      "partial write, at any layer")
    else:
        require(l4.snapshot(after) != before,
                "the write reported a `t` but changed nothing — an accepted "
                "write must be observable")

    # Unwritable at any occupancy: no eviction can make room for a payload that
    # exceeds the whole cap, so this must be a refusal at every layer.
    tiny = _fresh(l4, 2)
    tiny_after, t_ref = l4.ingest(tiny, _P0)
    require(t_ref is None,
            "a payload costing more than the entire cap must be refused — there "
            "is nothing eviction could free that would make room")
    require_equal(l4.snapshot(tiny_after), l4.snapshot(tiny),
                  "a refused write must leave the state unchanged")

    payloads = _l2tasks.store_payloads()
    s = _fresh(l4, _inbudget_cap(payloads))
    for p in payloads:
        s, t = l4.ingest(s, p)
        require(t is not None, "an in-budget write was refused at cap 4")
    snap = l4.snapshot(s)
    require(isinstance(snap, bytes), "snapshot must return bytes (§7.1)")
    restored = l4.restore(snap)
    require_equal(l4.snapshot(restored), snap,
                  "snapshot/restore is not byte-identical at cap 4 — §5 L1's "
                  "round-trip clause holds at every layer above it")
    for t in (0, 7, 61, len(payloads) - 1):
        require_equal(l4.query(s, {"op": "read", "t": t}),
                      l4.query(restored, {"op": "read", "t": t}),
                      "the restored state answered read(t=%d) differently" % (t,))


# ---- Layer 2: the cue battery ----------------------------------------------

def trial_layer4_inherits_the_layer2_cue_battery():
    """§5 L2's own gate, on §5 L2's own tasks, at cap 4.

    `_l2score` is the scorer the Layer-2 ascension and humility trials share, so
    this is that battery and not a friendlier copy of it. The store is a few
    hundred events and the cap is generous, so a miss here is an associative
    regression rather than a budget one.
    """
    l4 = _engine()
    payloads = _l2tasks.store_payloads()
    cap = _inbudget_cap(payloads)
    state = _l2score.ingest_store(l4, lambda: _fresh(l4, cap))
    r = _l2score.score(l4, state)

    require(r["cue_C"] >= GATE_L2_CUE_C,
            "cue-C=%d at cap 4, below the §5 L2 gate cue-C≥%d (recovered %d/%d) "
            "— associative recall regressed under consolidation"
            % (r["cue_C"], GATE_L2_CUE_C, r["recovered"], r["n_answerable"]))
    require(r["F"] >= GATE_L2_F,
            "F=%d at cap 4, below the §5 L2 gate F≥%d (wrong=%d, fabricated=%d)"
            % (r["F"], GATE_L2_F, r["wrong"], r["fabricated"]))
    require(r["B"] >= GATE_B,
            "B=%d at cap 4 — the budget law broke on an in-budget store"
            % (r["B"],))
    require_equal(r["wrong"], 0, "recall returned a wrong target at cap 4")
    require_equal(r["fabricated"], 0,
                  "recall fabricated on an unanswerable cue at cap 4 — a derived "
                  "answer to a cue nothing satisfies is still a fabrication (§3.0)")


# ---- Layer 3: retention, with nothing forcing a drop ------------------------

def trial_layer4_inherits_the_layer3_retention_battery_in_budget():
    """Both frozen pressure streams, replayed with **no pressure** at cap 4.

    Under 10× pressure Layer 3 keeps ~914 of 10 000 items and that is lawful.
    Here the cap is four times each stream's whole raw episodic footprint, so
    nothing may be dropped and the scores are asserted as identities: every item
    recalled, exactly, and nothing invented. A consolidation engine that folded
    in-budget episodes into a summary would fail this and should.
    """
    l4 = _engine()
    for name in _l3tasks.STREAMS:
        bundle = _l3tasks.stream(name)
        cap = _inbudget_cap(bundle["payloads"])
        state, budget = _replay_in_budget(l4, cap, bundle["payloads"], name)
        r = _l3score.score(l4, state, name)

        require_equal(budget["refused"], 0,
                      "%s: %d writes were refused at a cap %d× the stream's own "
                      "footprint — nothing here is under pressure"
                      % (name, budget["refused"], INBUDGET_MULTIPLE))
        require(budget["B"] >= GATE_B,
                "%s: B=%d at cap 4 — peak occupancy %d exceeded the cap %d"
                % (name, budget["B"], budget["peak"], budget["cap"]))
        require_equal(r["unweighted_C"], 1000,
                      "%s: unweighted-C=%d with nothing forcing a drop — %d of "
                      "%d items were not returned for their own cue"
                      % (name, r["unweighted_C"], r["n_targets"] - r["recovered"],
                         r["n_targets"]))
        require_equal(r["weighted_C"], 1000,
                      "%s: weighted-C=%d in budget — importance may not decide "
                      "anything when nothing is under pressure"
                      % (name, r["weighted_C"]))
        require_equal(r["wrong"], 0,
                      "%s: recall returned wrong content at cap 4" % (name,))
        require_equal(r["fabricated"], 0,
                      "%s: recall fabricated on a never-ingested cue at cap 4"
                      % (name,))


# ---- the class's own wiring, engine-free ------------------------------------

def trial_the_inherited_batteries_are_the_frozen_ones():
    """The batteries replayed above are the older layers' own, not softer copies.

    Green today and forever, with no engine: it asserts the shape of the task
    modules this file imports — the same modules `ascension/l2` and
    `ascension/l3` score with. An inheritance class that quietly built its own,
    smaller store or its own, gentler stream would prove nothing, and that
    failure would be invisible while every engine-gated trial above sat skipped.
    """
    require_equal(len(_l2tasks.answerable_tasks()), _l2tasks.N_ANSWERABLE,
                  "the inherited Layer-2 cue battery changed size")
    require(len(_l2tasks.unanswerable_tasks()) >= _l2tasks.N_UNANSWERABLE,
            "the inherited Layer-2 unanswerable probes fell below the %d the "
            "frozen builder selects for" % (_l2tasks.N_UNANSWERABLE,))
    for task in _l2tasks.answerable_tasks():
        require(_l2tasks.cue_has_no_t(task["cue"]),
                "an inherited Layer-2 cue leaked `t` — the probe must be content "
                "only, or the battery tests read-by-time instead of recall")

    require_equal(_l3tasks.STREAMS, ("l3stream", "l3streamb"),
                  "the inherited Layer-3 battery no longer covers both frozen "
                  "pressure streams")
    for name in _l3tasks.STREAMS:
        bundle = _l3tasks.stream(name)
        require_equal(len(bundle["targets"]), 10 * bundle["budget_items"],
                      "%s: the inherited stream is no longer 10× the Layer-3 "
                      "budget — it is the corpus Layer 3 was gated on" % (name,))
        require(_inbudget_cap(bundle["payloads"]) > bundle["budget_cap"],
                "%s: the in-budget cap is not larger than Layer 3's own pressure "
                "cap, so the replay above would not be in budget at all"
                % (name,))

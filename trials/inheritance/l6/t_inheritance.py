"""inheritance/l6 — Layer 6 must still be Layers 1–5 (BOUNDARY.md §5).

The standing class, extended (`trials/inheritance/README.md`: *"every future
ASCEND extends it, and nothing in it is ever removed"*). It replays the older
layers' own ratified batteries against the current engine at `layer_cap = 6`, on
**in-budget** substrates — no pressure, no excuse:

| what | battery | re-applied as |
|---|---|---|
| Layer 1 verbs | `write` / `read` / `read_range` / `snapshot` / `restore` / the Answer contract | exact IO, byte-identical round trip, deterministic refusal |
| Layer 2 cues | `_l2tasks` / `_l2score` | `cue-C ≥ 900`, `F ≥ 950`, `B = 1000` (§5 L2) |
| Layer 3 retention | `_l3tasks` / `_l3score`, both frozen pressure streams | identities: everything recalled, nothing invented |
| Layer 4 consolidation | `_l4tasks` / `_l4score` on `corpora/l4stream` | identities: `C = 1000`, reconstruction `F = 1000` |
| Layer 5 prospection | `_l5tasks` / `_l5score` on `corpora/l5stream` | identities: `precision = recall = 1000`, `dup-fire = miss = 0`, `F = 1000` |

Engine-gated: every trial that needs an engine SKIPS until
`trials/adapters/l6.py` exists (Stage C), then holds forever.

## The Layer-5 row is new here, and it is the one this layer could break

`inheritance/l5` added the Layer-4 row and said why: prospection competes for the
same cells as the interval table, and the cheapest way to buy room is a lossier
derived view that `§5 L5`'s firing clauses would never notice. The Layer-5 row is
the same argument one layer up, with a sharper edge. A confidence model is state
(`§4.1`), and `ATTAINABILITY-B.md §3.2` prices it at 18 cells beyond the frozen
Layer-5 state — small, but not zero, and it competes with a **pending set** and a
**fired ledger** that `README-l5 §0.1` puts outside every eviction phase on
purpose. An engine that paid for calibration out of prospection would keep every
Layer-6 clause green while silently repealing `§5 L5`'s four identities, and
nothing in `ascension/l6` scores a firing.

So the **seeded-promise pattern is now two layers deep in the class**: the
Layer-4 battery it was first asserted beside is replayed here for the second
time, and the Layer-5 battery joins it — intentions must still fire **exactly
once** under a cap-6 engine. In budget, where nothing forces a drop, `§5 L5`'s
one graded clause (`F ≥ 980`) becomes an identity at 1000 alongside its four
ratified ones, which is this class's rule 3: *the old gates, not new ones — and
where the inherited claim is exactness rather than a threshold, it is asserted as
an identity.* Verified attainable before being frozen, by measuring `adapters/l5`
at the same in-budget cap: `1000 / 1000 / 0 / 0`, `F 1000`, `refused 0`.

`§5 L4`'s `footprint ≤ 250` is deliberately **not** re-applied, for the reason
`inheritance/l5` gives: it is a claim about compression under pressure and this
class is defined by there being none. `§5 L6` states no footprint clause at all.

## Two notes on what this class does NOT re-apply at Layer 6

**No calibration clause appears here.** `§3.4` is dormant below Layer 6 and binds
from it; there is no *older* layer's calibration gate to inherit, and inventing
one would be the class introducing a measure of its own. The confidence field is
read by `ascension/l6` and by `humility/l6`, on the artifact `R7` binds, and
nowhere else.

**The `t` semantics need no change and are not re-derived.** `R6` clause 2's rule
is *one caller event plus the firings it caused*; `f = 0` on a stream with nothing
pending, and only `corpora/l5stream` carries an intention — asserted over the
bytes of every corpus in `corpora/registry.py` by
`ascension/l5/t_prospection.py::trial_one_caller_ingest_advances_next_t_by_exactly_one_on_an_intention_free_stream`,
which is why the Layer-1 through Layer-4 rows below re-use the frozen batteries
unchanged and the Layer-5 row expects `next_t` past the caller stream.
"""

from _harness import require, require_equal, try_import
import _l2score
import _l2tasks
import _l3score
import _l3tasks
import _l4score
import _l4tasks
import _l5score
import _l5tasks
from core.state import event_cost
from corpora.l5stream import generator as l5gen

# The ratified gates of the layers being inherited, re-applied at cap 6. Every
# one is §5 text, quoted in `laws/t_rulings.py`'s registry against this file.
GATE_L2_CUE_C = 900          # §5 L2
GATE_L2_F = 950              # §5 L2
GATE_B = 1000                # §5 L1/L2/L3/L4/L5 — the budget law, absolute everywhere

LAYER_CAP = 6

# The in-budget cap and floor, the same declarations `inheritance/l4` and
# `inheritance/l5` make and for the same reason: at four times a stream's own raw
# episodic footprint, a refusal, an eviction or a lossy answer is not a budget
# consequence, it is a regression. The floor keeps a three-event battery from
# being starved by an engine's fixed structures — and a Layer-6 engine has more
# of those than a Layer-5 one, which is why the floor is declared and not computed.
INBUDGET_MULTIPLE = 4
INBUDGET_FLOOR = 4096

L4_CORPUS = "l4stream"       # the corpus R4 clause 1 binds the Layer-4 gate on
L5_CORPUS = "l5stream"       # the corpus R6 clause 1 binds both sides of L5 to

_P0 = {"kind": "spawn", "entity": 1, "class": "node"}
_P1 = {"kind": "spawn", "entity": 2, "class": "agent"}
_P2 = {"kind": "spawn", "entity": 3, "class": "vault"}

_ANSWER_KEYS = {"status", "value", "confidence", "provenance"}


def _engine():
    return try_import(
        "adapters.l6",
        "no L6 engine yet; the Layer-6 inheritance battery engages when built "
        "(Stage C) and stands from then on")


def _fresh(engine, cap):
    return engine.make_engine(LAYER_CAP, cap)


def _inbudget_cap(payloads):
    return max(INBUDGET_MULTIPLE * sum(event_cost(p) for p in payloads),
               INBUDGET_FLOOR)


def _replay_in_budget(engine, cap, payloads, name):
    """Ingest a whole stream at `cap`, asserting the cap held after every write."""
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

def trial_layer6_inherits_the_layer1_verbs():
    """`write` / `read` / `read_range` at cap 6: exact IO, or Layer 1 is repealed.

    §5 L1 gates Retention at `F = 1000` — *"the exact return of what was written,
    read by time and by range, so any deviation is a bug, not a tolerance."* A
    meta-memory engine states how sure it is; it must still return.
    """
    l6 = _engine()
    cap = _inbudget_cap([_P0, _P1, _P2])
    s = _fresh(l6, cap)

    s, t0 = l6.ingest(s, _P0)
    s, t1 = l6.ingest(s, _P1)
    s, t2 = l6.ingest(s, _P2)
    require_equal((t0, t1, t2), (0, 1, 2),
                  "t must begin at 0 and increase by one per successful write on "
                  "a stream that fires nothing (§1.3, R6 clause 2's f = 0 case) — "
                  "logical time is engine-owned at every layer")

    for t, payload in ((0, _P0), (1, _P1), (2, _P2)):
        ans = l6.query(s, {"op": "read", "t": t})
        require_equal(ans["status"], "answer",
                      "an in-budget read(t=%d) abstained at cap 6" % (t,))
        require_equal(set(ans), _ANSWER_KEYS,
                      "the Answer contract (§7.2) is not honoured at cap 6")
        require_equal(ans["value"], {"payload": payload, "t": t},
                      "read(t=%d) is not byte-exact at cap 6 — Layer 1's F=1000 "
                      "is not a tolerance" % (t,))

    e0 = {"payload": _P0, "t": 0}
    e1 = {"payload": _P1, "t": 1}
    e2 = {"payload": _P2, "t": 2}
    got = l6.query(s, {"op": "read_range", "t0": 0, "t1": 2})
    require_equal(got["status"], "answer", "read_range abstained on a full range")
    require_equal(got["value"], [e0, e1, e2], "read_range is not exact at cap 6")
    require_equal(l6.query(s, {"op": "read_range", "t0": 1, "t1": 99})["value"],
                  [e1, e2],
                  "read_range does not clamp its upper bound at cap 6")
    require_equal(l6.query(s, {"op": "read", "t": 99})["status"], "abstain",
                  "a read past the end of the log must abstain, never fabricate")
    require_equal(l6.query(s, {"op": "no_such_op"})["status"], "abstain",
                  "an unsupported query must abstain, never raise (§7.3)")


def trial_layer6_inherits_the_budget_law_and_the_snapshot_round_trip():
    """The budget law at cap 6, and §5 L1's byte-identical round trip.

    What is inherited is the **law**, not one layer's response to it (§4.1.2): a
    Layer-6 engine has Layer 3, so it may lawfully evict where a Layer-1 engine
    must refuse. What may never differ is the invariant both responses serve —
    occupancy never exceeds the cap, and a refusal is total.

    The round trip has one more thing to carry at this layer, and it carries it
    without a new assertion: whatever state a confidence model keeps is inside
    `snapshot`, so a restored state that answered identically but rated itself
    differently would fail the equality below rather than pass unnoticed.
    """
    l6 = _engine()

    # The cap is taken from the engine's OWN accounting of two events: a Layer-6
    # engine charges for structures no `event_cost` sum knows about, and a cap
    # computed from the payloads alone would starve it and test the fixture
    # instead of the law.
    probe = _fresh(l6, _inbudget_cap([_P0, _P1, _P2]))
    probe, _t = l6.ingest(probe, _P0)
    probe, _t = l6.ingest(probe, _P1)
    cap = probe.occupancy

    s = _fresh(l6, cap)
    s, t0 = l6.ingest(s, _P0)
    s, t1 = l6.ingest(s, _P1)
    require_equal((t0, t1), (0, 1),
                  "two events did not fit a cap set to their own measured cost")

    before = l6.snapshot(s)
    occ_before = s.occupancy
    after, t2 = l6.ingest(s, _P2)
    require(after.occupancy <= cap,
            "a write past a full budget left occupancy %d above the cap %d — the "
            "budget law is absolute at every layer (§4.1)"
            % (after.occupancy, cap))
    if t2 is None:
        require_equal(after.occupancy, occ_before,
                      "a refused write must not change occupancy")
        require_equal(l6.snapshot(after), before,
                      "a refused write must leave the state UNCHANGED — no "
                      "partial write, at any layer")
    else:
        require(l6.snapshot(after) != before,
                "the write reported a `t` but changed nothing")

    tiny = _fresh(l6, 2)
    tiny_after, t_ref = l6.ingest(tiny, _P0)
    require(t_ref is None,
            "a payload costing more than the entire cap must be refused — there "
            "is nothing eviction could free that would make room")
    require_equal(l6.snapshot(tiny_after), l6.snapshot(tiny),
                  "a refused write must leave the state unchanged")

    payloads = _l2tasks.store_payloads()
    s = _fresh(l6, _inbudget_cap(payloads))
    for p in payloads:
        s, t = l6.ingest(s, p)
        require(t is not None, "an in-budget write was refused at cap 6")
    snap = l6.snapshot(s)
    require(isinstance(snap, bytes), "snapshot must return bytes (§7.1)")
    restored = l6.restore(snap)
    require_equal(l6.snapshot(restored), snap,
                  "snapshot/restore is not byte-identical at cap 6 — §5 L1's "
                  "round-trip clause holds at every layer above it")
    for t in (0, 7, 61, len(payloads) - 1):
        require_equal(l6.query(s, {"op": "read", "t": t}),
                      l6.query(restored, {"op": "read", "t": t}),
                      "the restored state answered read(t=%d) differently — the "
                      "Answer carries `confidence` (§7.2), so a state whose "
                      "confidence did not survive serialization fails here"
                      % (t,))


# ---- Layer 2: the cue battery ----------------------------------------------

def trial_layer6_inherits_the_layer2_cue_battery():
    """§5 L2's own gate, on §5 L2's own tasks, at cap 6.

    `_l2score` is the scorer the Layer-2 ascension and humility trials share, so
    this is that battery and not a friendlier copy of it.
    """
    l6 = _engine()
    payloads = _l2tasks.store_payloads()
    cap = _inbudget_cap(payloads)
    state = _l2score.ingest_store(l6, lambda: _fresh(l6, cap))
    r = _l2score.score(l6, state)

    require(r["cue_C"] >= GATE_L2_CUE_C,
            "cue-C=%d at cap 6, below the §5 L2 gate cue-C≥%d (recovered %d/%d)"
            % (r["cue_C"], GATE_L2_CUE_C, r["recovered"], r["n_answerable"]))
    require(r["F"] >= GATE_L2_F,
            "F=%d at cap 6, below the §5 L2 gate F≥%d (wrong=%d, fabricated=%d)"
            % (r["F"], GATE_L2_F, r["wrong"], r["fabricated"]))
    require(r["B"] >= GATE_B,
            "B=%d at cap 6 — the budget law broke on an in-budget store"
            % (r["B"],))
    require_equal(r["wrong"], 0, "recall returned a wrong target at cap 6")
    require_equal(r["fabricated"], 0,
                  "recall fabricated on an unanswerable cue at cap 6")


# ---- Layer 3: retention, with nothing forcing a drop ------------------------

def trial_layer6_inherits_the_layer3_retention_battery_in_budget():
    """Both frozen pressure streams, replayed with **no pressure** at cap 6."""
    l6 = _engine()
    for name in _l3tasks.STREAMS:
        bundle = _l3tasks.stream(name)
        cap = _inbudget_cap(bundle["payloads"])
        state, budget = _replay_in_budget(l6, cap, bundle["payloads"], name)
        r = _l3score.score(l6, state, name)

        require_equal(budget["refused"], 0,
                      "%s: %d writes were refused at a cap %d× the stream's own "
                      "footprint — nothing here is under pressure"
                      % (name, budget["refused"], INBUDGET_MULTIPLE))
        require(budget["B"] >= GATE_B,
                "%s: B=%d at cap 6 — peak occupancy %d exceeded the cap %d"
                % (name, budget["B"], budget["peak"], budget["cap"]))
        require_equal(r["unweighted_C"], 1000,
                      "%s: unweighted-C=%d with nothing forcing a drop"
                      % (name, r["unweighted_C"]))
        require_equal(r["weighted_C"], 1000,
                      "%s: weighted-C=%d in budget — importance may not decide "
                      "anything when nothing is under pressure"
                      % (name, r["weighted_C"]))
        require_equal(r["wrong"], 0, "%s: recall returned wrong content" % (name,))
        require_equal(r["fabricated"], 0,
                      "%s: recall fabricated on a never-ingested cue" % (name,))


# ---- Layer 4: consolidation, with nothing forcing a fold --------------------

def trial_layer6_inherits_the_layer4_consolidation_battery_in_budget():
    """§5 L4's own battery on §5 L4's own binding corpus, at cap 6, in budget.

    In budget the ratified `C ≥ 850` and reconstruction `F ≥ 900` are
    **identities**: nothing forces a fold, so every semantic query must be
    answered and every event returned. `footprint ≤ 250` is not re-applied and the
    module docstring says why.
    """
    l6 = _engine()
    b = _l4tasks.corpus(L4_CORPUS)
    cap = _inbudget_cap(b["payloads"])
    state, budget = _replay_in_budget(l6, cap, b["payloads"], L4_CORPUS)
    r = _l4score.score(l6, state, b)

    require_equal(budget["refused"], 0,
                  "%s: %d writes were refused at a cap %d× the corpus's own "
                  "footprint" % (L4_CORPUS, budget["refused"], INBUDGET_MULTIPLE))
    require(budget["B"] >= GATE_B,
            "%s: B=%d at cap 6 — peak occupancy %d exceeded the cap %d"
            % (L4_CORPUS, budget["B"], budget["peak"], budget["cap"]))
    require_equal(r["C"], 1000,
                  "%s: C=%d in budget — Q1 %d/%d, Q2 %d/%d, Q3 %d/%d"
                  % (L4_CORPUS, r["C"], r["q1"], r["n_q1"], r["q2"], r["n_q2"],
                     r["q3"], r["n_q3"]))
    require_equal(r["F"], 1000,
                  "%s: reconstruction F=%d in budget — %d of %d events did not "
                  "come back byte-exact"
                  % (L4_CORPUS, r["F"], r["n_q4"] - r["reconstructed"], r["n_q4"]))
    require_equal(r["reconstruction_wrong"], 0,
                  "%s: reconstruction returned wrong content at cap 6 — "
                  "`wrong = 0` is structural at Layer 4 (README-l4 §1: fold only "
                  "what inverts), so a non-zero count is a repeal" % (L4_CORPUS,))
    require_equal(r["coverage_wrong"], 0,
                  "%s: a semantic query was answered wrongly at cap 6" % (L4_CORPUS,))
    require_equal(r["fabricated"], 0,
                  "%s: %d unanswerable probes were answered at cap 6"
                  % (L4_CORPUS, r["fabricated"]))


# ---- Layer 5: prospection, with nothing forcing a loss ----------------------

def trial_layer6_inherits_the_layer5_prospection_battery_in_budget():
    """§5 L5's own battery on §5 L5's own binding corpus, at cap 6, in budget.

    The row this class gains at Layer 6, and the one meta-memory could actually
    break. `§5 L5`'s four exactness clauses are already identities and stay so;
    its one graded clause, `F ≥ 980`, becomes an identity at **1000** here,
    because in budget nothing forces a loss and `README-l5 §1.3`'s take-back rule
    returns every fired intention's own episode to the store.

    **Intentions must still fire exactly once under a cap-6 engine.** A pending
    set and a fired ledger are outside every eviction phase by design
    (`README-l5 §0.1`) precisely so that an engine cannot be made to break a
    ratified gate by being poor — and a confidence model is new state competing
    for the same cells. Nothing in `ascension/l6` scores a firing, so this is the
    only place a Layer-6 engine that paid for calibration out of prospection goes
    red.

    The `t` identity is asserted from the other side too: `_l5score.observe`
    checks `next_t − |caller stream|` against the firings the engine reports
    through `§7.1` (`R6` clause 2), so an engine that fired twice and reported
    once fails here on the constitution's own clock rather than on a score.
    """
    l6 = _engine()
    b = _l5tasks.corpus()
    cap = _inbudget_cap(b["payloads"])
    state, budget = _l5score.replay(
        l6, lambda c: _fresh(l6, c), b, cap)
    r = _l5score.score(l6, state, b)

    require_equal(budget["refused"], 0,
                  "%s: %d writes were refused at a cap %d× the corpus's own "
                  "footprint" % (L5_CORPUS, budget["refused"], INBUDGET_MULTIPLE))
    require(budget["B"] >= GATE_B,
            "%s: B=%d at cap 6 — peak occupancy %d exceeded the cap %d"
            % (L5_CORPUS, budget["B"], budget["peak"], budget["cap"]))

    require_equal(r["precision"], 1000,
                  "%s: trigger-precision=%r at cap 6 — an identity at §5 L5 and "
                  "an identity here" % (L5_CORPUS, r["precision"]))
    require_equal(r["recall"], 1000,
                  "%s: trigger-recall=%r at cap 6 — %d of %d fireable intentions "
                  "fired exactly once at their own satisfaction point"
                  % (L5_CORPUS, r["recall"], r["correct"], len(b["fireable"])))
    require_equal(r["dup_fire"], 0,
                  "%s: dup-fire=%d at cap 6 — exactly-once is a property of an "
                  "INTENTION and the fired ledger is read on every later "
                  "satisfaction" % (L5_CORPUS, r["dup_fire"]))
    require_equal(r["miss"], 0,
                  "%s: %d fireable intentions never fired at cap 6"
                  % (L5_CORPUS, r["miss"]))
    require_equal(r["F"], 1000,
                  "%s: F=%d in budget, where §5 L5's one graded clause (F≥980) "
                  "is an identity — a fired payload is the caller's own bytes "
                  "(§1.4) and every intend event is still readable"
                  % (L5_CORPUS, r["F"]))
    require_equal(r["wrong"], 0, "%s: a P1/P2 answer was wrong at cap 6" % (L5_CORPUS,))
    require_equal(r["fabricated"], 0,
                  "%s: a never-fires intention was answered at cap 6"
                  % (L5_CORPUS,))
    require_equal(r["malformed"], 0,
                  "%s: an answered P1 was not a list of event records"
                  % (L5_CORPUS,))
    require_equal(state.next_t, b["n"] + r["fires"],
                  "%s: the engine's clock does not account for its own firings — "
                  "R6 clause 2 makes a firing an event that consumes a `t` of "
                  "its own" % (L5_CORPUS,))


# ---- the class's own wiring, engine-free ------------------------------------

def trial_the_inherited_layer5_battery_is_the_frozen_one():
    """The batteries replayed above are the older layers' own, not softer copies.

    Green today and forever, with no engine — the class's rule 4, which exists so
    that a class sitting entirely skipped cannot also be quietly pointing at a
    softer substrate. `inheritance/l4` asserts the shape of the Layer-2 and
    Layer-3 batteries and `inheritance/l5` the Layer-4 one; this asserts the
    Layer-5 battery it adds, on the corpus `R6` clause 1 binds that gate to.
    """
    b = _l5tasks.corpus()
    require_equal(b["n"], l5gen.N,
                  "the inherited Layer-5 battery is not the whole frozen "
                  "%s caller stream" % (L5_CORPUS,))
    require_equal(len(b["intents"]), l5gen.DECLARED_INTENTIONS,
                  "the inherited Layer-5 battery no longer carries the corpus's "
                  "own declared intention count")
    require(len(b["intents"]) > 0 and len(b["fireable"]) > 0,
            "the inherited Layer-5 battery carries no fireable intention, which "
            "would make every identity above vacuously true")
    require(len(b["fireable"]) < len(b["intents"]),
            "the inherited battery has no never-fires intentions left, so the "
            "fabrication half of §3.0 would go unasked")

    cap = _inbudget_cap(b["payloads"])
    require(cap > b["budget_cap"],
            "the in-budget cap (%d) is not larger than the ratified Layer-5 cap "
            "(%d) — this class asserts identities that only hold when nothing is "
            "under pressure, and it must be measurably not under pressure"
            % (cap, b["budget_cap"]))
    require_equal(cap, INBUDGET_MULTIPLE * b["raw_cells"],
                  "the in-budget cap for %s is no longer the declared multiple "
                  "of its own raw episodic footprint" % (L5_CORPUS,))
    require_equal(b["budget_cap"], b["raw_cells"] // 4,
                  "the ratified Layer-5 cap is R6 clause 4's raw_cells // 4, and "
                  "the in-budget multiple is stated against it")

"""inheritance/l7 — Layer 7 must still be Layers 1–6 (BOUNDARY.md §5).

The standing class, extended (`trials/inheritance/README.md`: *"every future
ASCEND extends it, and nothing in it is ever removed"*). It replays the older
layers' own ratified batteries against the current engine at `layer_cap = 7`, on
**in-budget** substrates — no pressure, no excuse:

| what | battery | re-applied as |
|---|---|---|
| Layer 1 verbs | `write` / `read` / `read_range` / `snapshot` / `restore` / the Answer contract | exact IO, byte-identical round trip, deterministic refusal |
| Layer 2 cues | `_l2tasks` / `_l2score` | `cue-C ≥ 900`, `F ≥ 950`, `B = 1000` (§5 L2) |
| Layer 3 retention | `_l3tasks` / `_l3score`, both frozen pressure streams | identities: everything recalled, nothing invented |
| Layer 4 consolidation | `_l4tasks` / `_l4score` on `corpora/l4stream` | identities: `C = 1000`, reconstruction `F = 1000` |
| Layer 5 prospection | `_l5tasks` / `_l5score` on `corpora/l5stream` | identities: `precision = recall = 1000`, `dup-fire = miss = 0`, `F = 1000` |
| Layer 6 calibration | `_l6btasks` / `_l6score` on `corpora/l6batteryb` | **§5 L6's own gate**: `Brier ≤ 40`, `ECE ≤ 30`, `AUROC ≥ 900`, `F ≥ 950`, `B = 1000` |

Engine-gated: every trial that needs an engine SKIPS until
`trials/adapters/l7.py` exists (Stage C), then holds forever.

## The Layer-6 row is new here, and it is the one this layer could break

`inheritance/l6` added the Layer-5 row and said why: a confidence model is state
competing with a pending set and a fired ledger that `README-l5 §0.1` puts
outside every eviction phase on purpose. The Layer-6 row is the same argument one
layer up, and its edge is different in kind.

**It is the first inherited row whose gate is not an identity in budget.** Every
other row above becomes an identity when nothing is under pressure — everything
recalled, everything reconstructed, every intention fired exactly once — because
those capabilities are exact and pressure is the only thing that can cost them
anything. Layer 6's is not: on `corpora/l6batteryb` the engine is **wrong exactly
100 times by theorem** (`R7` clause 3(b)), whatever the budget, because the
forcing region's two members are observationally identical and the coin that
separates them is in no function of the stream. So what is re-applied here is
`§5 L6`'s **own ratified gate**, unchanged — `Brier ≤ 40`, `ECE ≤ 30`,
`AUROC ≥ 900`, `F ≥ 950`, `B = 1000` — and not a stricter in-budget reading of
it. The class's rule 3 is *the old gates, not new ones*; where the inherited
claim is exactness it is asserted as an identity, and where it is a threshold the
threshold is what is inherited.

**What a Layer-7 engine could break here is the ranking.** `AUROC ≥ 900` requires
the confidence to rank the engine's 100 forced errors below its 2 100 correct
answers, and a generation construct arrives with a new class of answer that has
**no chain, no distinct-value count and no set-once status** — `README-l6 §4`'s
recorded residual, *"`confidence_for` returns `CERTAIN` on it by falling through,
which is exactly the wrong answer and is the first thing a Layer-7 engine must
replace."* An engine that replaced it carelessly — by widening the tie reading,
or by pricing the whole answer surface through a new model — would move
confidences on chains that have nothing to do with generation, and `Brier`, `ECE`
and `AUROC` would move with them. Nothing in `ascension/l7` scores a Layer-6
quantity except `ECE`, and `ECE` is the one clause Layer 6 **measured** to
discriminate against nothing (`R8` clause 6). So this is the only place a Layer-7
engine that paid for its generation out of its calibration goes red.

`corpora/l6battery` — the artifact `R7` clause 1 demoted — is **not** replayed
here. A demoted artifact keeps its duty in the battery that owns it
(`ascension/l6` still scores and reports it ungated); this class inherits gates,
and there is no gate on that artifact to inherit.

## Two notes on what this class does NOT re-apply at Layer 7

**No `§5 L7` clause appears here**, and none could: this class re-applies the
gates of the layers *below* the current one, and Layer 7's own gate is
`ascension/l7`'s. In particular the three capability ratios, whose denominators
`R8` clause 3 had to bind, are nowhere in this file — an inherited battery that
scored a Layer-7 ratio would be the class introducing a measure of its own.

**No footprint clause is re-applied.** `§5 L4`'s `footprint ≤ 250` is a claim
about compression under pressure and this class is defined by there being none;
`§5 L5`, `§5 L6` and `§5 L7` state none at all.

## The class now carries six layers of history per replay

Worth stating because it is what the rows silently stand on. The Layer-3 rows run
above an aggregated forgetting record; the Layer-4 rows above an interval table
and a demotion counter; the Layer-5 rows above a **two-tier prospection ledger**
— a pending set and a fired ledger, both outside every eviction phase — and the
Layer-6 rows above a **zero-state confidence view**, a model that adds no field
to the state it reads (`README-l6 §0`). A Layer-7 engine inherits all of it at
once, and every row here is one of those histories being asked to still be true.
"""

from fractions import Fraction

from _harness import require, require_equal, try_import
import _l2score
import _l2tasks
import _l3score
import _l3tasks
import _l4score
import _l4tasks
import _l5score
import _l5tasks
import _l6btasks
import _l6score
from core.state import event_cost
from corpora.l5stream import generator as l5gen

# The ratified gates of the layers being inherited, re-applied at cap 7. Every
# one is §5 text, quoted in `laws/t_rulings.py`'s registry against this file.
GATE_L2_CUE_C = 900          # §5 L2
GATE_L2_F = 950              # §5 L2
GATE_B = 1000                # §5 L1..L6 — the budget law, absolute everywhere

# §5 L6, the first inherited row whose clauses are thresholds rather than
# in-budget identities: the forcing region's 100 errors are a theorem and not a
# pressure consequence, so no budget makes them go away.
GATE_L6_BRIER = 40           # §5 L6
GATE_L6_ECE = 30             # §5 L6
GATE_L6_AUROC = 900          # §5 L6
GATE_L6_F = 950              # §5 L6

LAYER_CAP = 7

# The in-budget cap and floor, the same declarations `inheritance/l4`, `l5` and
# `l6` make and for the same reason: at four times a stream's own raw episodic
# footprint, a refusal, an eviction or a lossy answer is not a budget
# consequence, it is a regression. The floor keeps a three-event battery from
# being starved by an engine's fixed structures — and a Layer-7 engine has more
# of those than a Layer-6 one, which is why the floor is declared and not computed.
INBUDGET_MULTIPLE = 4
INBUDGET_FLOOR = 4096

L4_CORPUS = "l4stream"       # the corpus R4 clause 1 binds the Layer-4 gate on
L5_CORPUS = "l5stream"       # the corpus R6 clause 1 binds both sides of L5 to
L6_CORPUS = "l6batteryb"     # the artifact R7 clause 1 binds both sides of L6 to

_P0 = {"kind": "spawn", "entity": 1, "class": "node"}
_P1 = {"kind": "spawn", "entity": 2, "class": "agent"}
_P2 = {"kind": "spawn", "entity": 3, "class": "vault"}

_ANSWER_KEYS = {"status", "value", "confidence", "provenance"}


def _engine():
    return try_import(
        "adapters.l7",
        "no L7 engine yet; the Layer-7 inheritance battery engages when built "
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

def trial_layer7_inherits_the_layer1_verbs():
    """`write` / `read` / `read_range` at cap 7: exact IO, or Layer 1 is repealed.

    §5 L1 gates Retention at `F = 1000` — *"the exact return of what was written,
    read by time and by range, so any deviation is a bug, not a tolerance."* An
    engine that can compose an item it never held must still return the ones it
    did, byte for byte.
    """
    l7 = _engine()
    cap = _inbudget_cap([_P0, _P1, _P2])
    s = _fresh(l7, cap)

    s, t0 = l7.ingest(s, _P0)
    s, t1 = l7.ingest(s, _P1)
    s, t2 = l7.ingest(s, _P2)
    require_equal((t0, t1, t2), (0, 1, 2),
                  "t must begin at 0 and increase by one per successful write on "
                  "a stream that fires nothing (§1.3, R6 clause 2's f = 0 case) — "
                  "logical time is engine-owned at every layer, and a GENERATION "
                  "is returned through `query` rather than ingested, so it may "
                  "not advance the clock either (R8 clause 2)")

    for t, payload in ((0, _P0), (1, _P1), (2, _P2)):
        ans = l7.query(s, {"op": "read", "t": t})
        require_equal(ans["status"], "answer",
                      "an in-budget read(t=%d) abstained at cap 7" % (t,))
        require(set(ans) >= _ANSWER_KEYS,
                "the Answer contract (§7.2) is not honoured at cap 7: %r"
                % (sorted(ans),))
        require_equal(ans["value"], {"payload": payload, "t": t},
                      "read(t=%d) is not byte-exact at cap 7 — Layer 1's F=1000 "
                      "is not a tolerance" % (t,))

    e0 = {"payload": _P0, "t": 0}
    e1 = {"payload": _P1, "t": 1}
    e2 = {"payload": _P2, "t": 2}
    got = l7.query(s, {"op": "read_range", "t0": 0, "t1": 2})
    require_equal(got["status"], "answer", "read_range abstained on a full range")
    require_equal(got["value"], [e0, e1, e2], "read_range is not exact at cap 7")
    require_equal(l7.query(s, {"op": "read_range", "t0": 1, "t1": 99})["value"],
                  [e1, e2],
                  "read_range does not clamp its upper bound at cap 7")
    require_equal(l7.query(s, {"op": "read", "t": 99})["status"], "abstain",
                  "a read past the end of the log must abstain, never fabricate")
    require_equal(l7.query(s, {"op": "no_such_op"})["status"], "abstain",
                  "an unsupported query must abstain, never raise (§7.3)")


def trial_layer7_inherits_the_budget_law_and_the_snapshot_round_trip():
    """The budget law at cap 7, and §5 L1's byte-identical round trip.

    What is inherited is the **law**, not one layer's response to it (§4.1.2): a
    Layer-7 engine has Layer 3, so it may lawfully evict where a Layer-1 engine
    must refuse. What may never differ is the invariant both responses serve —
    occupancy never exceeds the cap, and a refusal is total.

    The round trip has one more thing to carry at this layer, and it carries it
    without a new assertion: a lineage ledger is state (`ATTAINABILITY.md §7`
    prices it at 320 cells, in the only placement `§1.4` leaves — engine state
    keyed by `t`, never the payload), so it is inside `snapshot`. A restored state
    that answered identically but had forgotten **which items were its own** would
    fail the equality below rather than pass unnoticed, and forgetting that is
    exactly how `§5 L7`'s `promotion = 0` breaks.
    """
    l7 = _engine()

    probe = _fresh(l7, _inbudget_cap([_P0, _P1, _P2]))
    probe, _t = l7.ingest(probe, _P0)
    probe, _t = l7.ingest(probe, _P1)
    cap = probe.occupancy

    s = _fresh(l7, cap)
    s, t0 = l7.ingest(s, _P0)
    s, t1 = l7.ingest(s, _P1)
    require_equal((t0, t1), (0, 1),
                  "two events did not fit a cap set to their own measured cost")

    before = l7.snapshot(s)
    occ_before = s.occupancy
    after, t2 = l7.ingest(s, _P2)
    require(after.occupancy <= cap,
            "a write past a full budget left occupancy %d above the cap %d — the "
            "budget law is absolute at every layer (§4.1)"
            % (after.occupancy, cap))
    if t2 is None:
        require_equal(after.occupancy, occ_before,
                      "a refused write must not change occupancy")
        require_equal(l7.snapshot(after), before,
                      "a refused write must leave the state UNCHANGED — no "
                      "partial write, at any layer")
    else:
        require(l7.snapshot(after) != before,
                "the write reported a `t` but changed nothing")

    tiny = _fresh(l7, 2)
    tiny_after, t_ref = l7.ingest(tiny, _P0)
    require(t_ref is None,
            "a payload costing more than the entire cap must be refused — there "
            "is nothing eviction could free that would make room")
    require_equal(l7.snapshot(tiny_after), l7.snapshot(tiny),
                  "a refused write must leave the state unchanged")

    payloads = _l2tasks.store_payloads()
    s = _fresh(l7, _inbudget_cap(payloads))
    for p in payloads:
        s, t = l7.ingest(s, p)
        require(t is not None, "an in-budget write was refused at cap 7")
    snap = l7.snapshot(s)
    require(isinstance(snap, bytes), "snapshot must return bytes (§7.1)")
    restored = l7.restore(snap)
    require_equal(l7.snapshot(restored), snap,
                  "snapshot/restore is not byte-identical at cap 7 — §5 L1's "
                  "round-trip clause holds at every layer above it")
    for t in (0, 7, 61, len(payloads) - 1):
        require_equal(l7.query(s, {"op": "read", "t": t}),
                      l7.query(restored, {"op": "read", "t": t}),
                      "the restored state answered read(t=%d) differently — the "
                      "Answer carries `confidence` (§7.2) and, from this layer, "
                      "`lineage` (R8 clause 2), so a state whose model or ledger "
                      "did not survive serialization fails here" % (t,))


# ---- Layer 2: the cue battery ----------------------------------------------

def trial_layer7_inherits_the_layer2_cue_battery():
    """§5 L2's own gate, on §5 L2's own tasks, at cap 7.

    `_l2score` is the scorer the Layer-2 ascension and humility trials share, so
    this is that battery and not a friendlier copy of it.
    """
    l7 = _engine()
    payloads = _l2tasks.store_payloads()
    cap = _inbudget_cap(payloads)
    state = _l2score.ingest_store(l7, lambda: _fresh(l7, cap))
    r = _l2score.score(l7, state)

    require(r["cue_C"] >= GATE_L2_CUE_C,
            "cue-C=%d at cap 7, below the §5 L2 gate cue-C≥%d (recovered %d/%d)"
            % (r["cue_C"], GATE_L2_CUE_C, r["recovered"], r["n_answerable"]))
    require(r["F"] >= GATE_L2_F,
            "F=%d at cap 7, below the §5 L2 gate F≥%d (wrong=%d, fabricated=%d)"
            % (r["F"], GATE_L2_F, r["wrong"], r["fabricated"]))
    require(r["B"] >= GATE_B,
            "B=%d at cap 7 — the budget law broke on an in-budget store"
            % (r["B"],))
    require_equal(r["wrong"], 0, "recall returned a wrong target at cap 7")
    require_equal(r["fabricated"], 0,
                  "recall fabricated on an unanswerable cue at cap 7")


# ---- Layer 3: retention, with nothing forcing a drop ------------------------

def trial_layer7_inherits_the_layer3_retention_battery_in_budget():
    """Both frozen pressure streams, replayed with **no pressure** at cap 7."""
    l7 = _engine()
    for name in _l3tasks.STREAMS:
        bundle = _l3tasks.stream(name)
        cap = _inbudget_cap(bundle["payloads"])
        state, budget = _replay_in_budget(l7, cap, bundle["payloads"], name)
        r = _l3score.score(l7, state, name)

        require_equal(budget["refused"], 0,
                      "%s: %d writes were refused at a cap %d× the stream's own "
                      "footprint — nothing here is under pressure"
                      % (name, budget["refused"], INBUDGET_MULTIPLE))
        require(budget["B"] >= GATE_B,
                "%s: B=%d at cap 7 — peak occupancy %d exceeded the cap %d"
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

def trial_layer7_inherits_the_layer4_consolidation_battery_in_budget():
    """§5 L4's own battery on §5 L4's own binding corpus, at cap 7, in budget.

    In budget the ratified `C ≥ 850` and reconstruction `F ≥ 900` are
    **identities**: nothing forces a fold, so every semantic query must be
    answered and every event returned. `footprint ≤ 250` is not re-applied and the
    module docstring says why.
    """
    l7 = _engine()
    b = _l4tasks.corpus(L4_CORPUS)
    cap = _inbudget_cap(b["payloads"])
    state, budget = _replay_in_budget(l7, cap, b["payloads"], L4_CORPUS)
    r = _l4score.score(l7, state, b)

    require_equal(budget["refused"], 0,
                  "%s: %d writes were refused at a cap %d× the corpus's own "
                  "footprint" % (L4_CORPUS, budget["refused"], INBUDGET_MULTIPLE))
    require(budget["B"] >= GATE_B,
            "%s: B=%d at cap 7 — peak occupancy %d exceeded the cap %d"
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
                  "%s: reconstruction returned wrong content at cap 7 — "
                  "`wrong = 0` is structural at Layer 4 (README-l4 §1: fold only "
                  "what inverts), so a non-zero count is a repeal" % (L4_CORPUS,))
    require_equal(r["coverage_wrong"], 0,
                  "%s: a semantic query was answered wrongly at cap 7" % (L4_CORPUS,))
    require_equal(r["fabricated"], 0,
                  "%s: %d unanswerable probes were answered at cap 7"
                  % (L4_CORPUS, r["fabricated"]))


# ---- Layer 5: prospection, with nothing forcing a loss ----------------------

def trial_layer7_inherits_the_layer5_prospection_battery_in_budget():
    """§5 L5's own battery on §5 L5's own binding corpus, at cap 7, in budget.

    `§5 L5`'s four exactness clauses are identities and stay so; its one graded
    clause, `F ≥ 980`, is an identity at **1000** here, because in budget nothing
    forces a loss and `README-l5 §1.3`'s take-back rule returns every fired
    intention's own episode to the store.

    **Intentions must still fire exactly once under a cap-7 engine**, and the row
    stands above a **two-tier ledger** — a pending set and a fired ledger, both
    outside every eviction phase by design (`README-l5 §0.1`) precisely so that an
    engine cannot be made to break a ratified gate by being poor. A lineage ledger
    is new state beside them, and the cheapest place to find room for it is
    somewhere `§5 L7` does not look. Nothing in `ascension/l7` scores a firing.

    The `t` identity is asserted from the other side too: `_l5score.observe`
    checks `next_t − |caller stream|` against the firings the engine reports
    through `§7.1` (`R6` clause 2), and at this layer it does one thing more —
    `R8` clause 2 makes a generation a `query` answer and **not** an event, so
    nothing a Layer-7 engine composes may appear on this clock.
    """
    l7 = _engine()
    b = _l5tasks.corpus()
    cap = _inbudget_cap(b["payloads"])
    state, budget = _l5score.replay(l7, lambda c: _fresh(l7, c), b, cap)
    r = _l5score.score(l7, state, b)

    require_equal(budget["refused"], 0,
                  "%s: %d writes were refused at a cap %d× the corpus's own "
                  "footprint" % (L5_CORPUS, budget["refused"], INBUDGET_MULTIPLE))
    require(budget["B"] >= GATE_B,
            "%s: B=%d at cap 7 — peak occupancy %d exceeded the cap %d"
            % (L5_CORPUS, budget["B"], budget["peak"], budget["cap"]))

    require_equal(r["precision"], 1000,
                  "%s: trigger-precision=%r at cap 7 — an identity at §5 L5 and "
                  "an identity here" % (L5_CORPUS, r["precision"]))
    require_equal(r["recall"], 1000,
                  "%s: trigger-recall=%r at cap 7 — %d of %d fireable intentions "
                  "fired exactly once at their own satisfaction point"
                  % (L5_CORPUS, r["recall"], r["correct"], len(b["fireable"])))
    require_equal(r["dup_fire"], 0,
                  "%s: dup-fire=%d at cap 7 — exactly-once is a property of an "
                  "INTENTION and the fired ledger is read on every later "
                  "satisfaction" % (L5_CORPUS, r["dup_fire"]))
    require_equal(r["miss"], 0,
                  "%s: %d fireable intentions never fired at cap 7"
                  % (L5_CORPUS, r["miss"]))
    require_equal(r["F"], 1000,
                  "%s: F=%d in budget, where §5 L5's one graded clause (F≥980) "
                  "is an identity — a fired payload is the caller's own bytes "
                  "(§1.4) and every intend event is still readable"
                  % (L5_CORPUS, r["F"]))
    require_equal(r["wrong"], 0, "%s: a P1/P2 answer was wrong at cap 7" % (L5_CORPUS,))
    require_equal(r["fabricated"], 0,
                  "%s: a never-fires intention was answered at cap 7"
                  % (L5_CORPUS,))
    require_equal(r["malformed"], 0,
                  "%s: an answered P1 was not a list of event records"
                  % (L5_CORPUS,))
    require_equal(state.next_t, b["n"] + r["fires"],
                  "%s: the engine's clock does not account for its own firings — "
                  "R6 clause 2 makes a firing an event that consumes a `t` of "
                  "its own, and R8 clause 2 makes a GENERATION a query answer "
                  "that does not" % (L5_CORPUS,))


# ---- Layer 6: calibration, and the first inherited row that is not an identity

def trial_layer7_inherits_the_layer6_calibration_battery_in_budget():
    """§5 L6's own gate, on §5 L6's own binding artifact, at cap 7, in budget.

    The row this class gains at Layer 7, and the one generation could actually
    break. It is also the first inherited row whose clauses stay **thresholds**:
    `corpora/l6batteryb`'s forcing region makes the engine wrong exactly 100 times
    **by theorem** (`R7` clause 3(b)), whatever the budget, so `Brier`, `ECE` and
    `AUROC` cannot become identities the way retention, reconstruction and
    firing do when nothing is under pressure. `§5 L6`'s ratified numbers are
    therefore re-applied unchanged — the class's rule 3, in the direction it is
    less often read.

    What a Layer-7 engine is most likely to break here is the **ranking**.
    `README-l6 §4` records the residual in advance: a generated item has no
    chain, no distinct-value count and no set-once status, so a Layer-6
    `confidence_for` falls through to `CERTAIN` on it — *"exactly the wrong answer
    and the first thing a Layer-7 engine must replace."* Replacing it by widening
    the tie reading, or by routing the whole answer surface through a new model,
    would move confidences on chains that have nothing to do with generation, and
    `AUROC ≥ 900` is where that lands. `ascension/l7` scores `ECE` and nothing
    else of `§3.4`'s triple, and `R8` clause 6 records that `ECE` is a floor
    against incoherence rather than a discriminator — so this row is the only
    place the ranking is still asked for.

    Read **exact** under `R7` clause 4 and binned under its clause 5, unchanged.
    """
    l7 = _engine()
    b = _l6score.BATTERIES[L6_CORPUS]()
    cap = _inbudget_cap(b["payloads"])
    state, budget = _l6score.replay(l7, lambda c: _fresh(l7, c), b, cap)
    rows = _l6score.observe(l7, state, b)
    r = _l6score.score(rows, b)

    require_equal(budget["refused"], 0,
                  "%s: %d writes were refused at a cap %d× the artifact's own "
                  "footprint" % (L6_CORPUS, budget["refused"], INBUDGET_MULTIPLE))
    require(budget["B"] >= GATE_B,
            "%s: B=%d at cap 7 — peak occupancy %d exceeded the cap %d"
            % (L6_CORPUS, budget["B"], budget["peak"], budget["cap"]))

    require(r["brier"] <= Fraction(GATE_L6_BRIER, 1000),
            "%s: Brier %s (permille %d) at cap 7, above §5 L6's ratified bound "
            "of %d/1000 — read EXACT under R7 clause 4"
            % (L6_CORPUS, r["brier"], _l6score.permille(r["brier"]),
               GATE_L6_BRIER))
    require(r["ece"] <= Fraction(GATE_L6_ECE, 1000),
            "%s: ECE %s (permille %d) at cap 7, above §5 L6's ratified bound of "
            "%d/1000, binned under R7 clause 5"
            % (L6_CORPUS, r["ece"], _l6score.permille(r["ece"]), GATE_L6_ECE))
    require(r["auroc"] is not None,
            "%s: AUROC is n/a at cap 7 — the engine answered A = %d queries of "
            "which %d were wrong. R7 clause 3(a) rules n/a DISQUALIFYING for a "
            "gate that cites AUROC, and this row cites it. An engine reaching "
            "n_neg = 0 here has either hedged the forcing region — which R7 "
            "clause 3(c)'s arithmetic prices out — or resolved a region whose "
            "coin is not in the stream" % (L6_CORPUS, r["A"], r["n_neg"]))
    require(r["auroc"] >= Fraction(GATE_L6_AUROC, 1000),
            "%s: AUROC %s (permille %d) at cap 7, below §5 L6's ratified bound "
            "of %d/1000 — the confidence no longer ranks the engine's forced "
            "errors below its correct answers, which is what a carelessly "
            "replaced README-l6 §4 residual looks like from outside"
            % (L6_CORPUS, r["auroc"], _l6score.permille(r["auroc"]),
               GATE_L6_AUROC))
    require(r["F_core"] >= Fraction(GATE_L6_F, 1000),
            "%s: F %s (permille %d) over the answerable core at cap 7, below "
            "§5 L6's ratified gate of %d/1000 (%d wrong, %d hedged)"
            % (L6_CORPUS, r["F_core"], _l6score.permille(r["F_core"]),
               GATE_L6_F, r["wrong"], r["abstentions"]))
    require_equal(r["fabricated"], 0,
                  "%s: %d unanswerable probes were answered at cap 7"
                  % (L6_CORPUS, r["fabricated"]))

    _l6score.assert_denominator_declared(r, rows, b)
    profile = _l6score.region_profile(rows, b)
    require_equal(_l6score.resolved_pairs(profile), [],
                  "%s: the engine resolved a mirror pair at cap 7, which "
                  "Theorem 2 makes impossible from the stream alone — a Layer-7 "
                  "engine that composes must still not read a coin the artifact "
                  "withholds" % (L6_CORPUS,))


# ---- the class's own wiring, engine-free ------------------------------------

def trial_the_inherited_layer6_battery_is_the_frozen_one():
    """The batteries replayed above are the older layers' own, not softer copies.

    Green today and forever, with no engine — the class's rule 4, which exists so
    that a class sitting entirely skipped cannot also be quietly pointing at a
    softer substrate. `inheritance/l4` asserts the shape of the Layer-2 and
    Layer-3 batteries, `inheritance/l5` the Layer-4 one and `inheritance/l6` the
    Layer-5 one; this asserts the Layer-6 battery it adds, on the artifact `R7`
    clause 1 binds that gate to — **and asserts that the demoted artifact is not
    the one being replayed**, which is the way this row could be made to look
    green while measuring the wrong thing.
    """
    b = _l6score.BATTERIES[L6_CORPUS]()
    require_equal(b["name"], L6_CORPUS,
                  "the inherited Layer-6 battery is not the artifact R7 clause 1 "
                  "binds")
    require(b["region_pairs"] is not None,
            "the inherited Layer-6 battery has lost its forcing region — the "
            "region is what makes AUROC evaluable at all, and R7 clause 1 "
            "DEMOTED round 1's artifact for having none")
    require_equal(len(b["region_pairs"]), _l6btasks.PAIRS,
                  "the inherited Layer-6 battery no longer carries the whole "
                  "declared forcing region")
    require_equal(b["n"], len(_l6btasks.queries()),
                  "the inherited Layer-6 battery is not the whole frozen query "
                  "set")
    require_equal(b["n_events"], len(_l6btasks.stream()),
                  "the inherited Layer-6 battery is not the whole frozen stream")
    require("l6battery" in _l6score.BATTERIES and L6_CORPUS != "l6battery",
            "the DEMOTED artifact (corpora/l6battery, R7 clause 1) must still "
            "exist as a bundle — a demotion is a change of authority and not of "
            "bytes, and `ascension/l6` still scores it ungated — and it must not "
            "be the substrate this class replays, because there is no gate on it "
            "to inherit")

    cap = _inbudget_cap(b["payloads"])
    require(cap > sum(event_cost(p) for p in b["payloads"]),
            "the in-budget cap (%d) is not larger than the artifact's own raw "
            "episodic footprint — this class asserts that nothing is under "
            "pressure, and it must be measurably not under pressure" % (cap,))
    require_equal(cap,
                  INBUDGET_MULTIPLE * sum(event_cost(p) for p in b["payloads"]),
                  "the in-budget cap for %s is no longer the declared multiple "
                  "of its own raw episodic footprint" % (L6_CORPUS,))

    l5b = _l5tasks.corpus()
    require_equal(l5b["n"], l5gen.N,
                  "the inherited Layer-5 battery is not the whole frozen %s "
                  "caller stream" % (L5_CORPUS,))
    require(len(l5b["fireable"]) < len(l5b["intents"]),
            "the inherited Layer-5 battery has no never-fires intentions left, "
            "so the fabrication half of §3.0 would go unasked")

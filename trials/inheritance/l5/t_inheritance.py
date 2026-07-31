"""inheritance/l5 — Layer 5 must still be Layers 1, 2, 3 and 4 (BOUNDARY.md §5).

The standing class, extended (`trials/inheritance/README.md`: *"every future
ASCEND extends it, and nothing in it is ever removed"*). It replays the older
layers' own ratified batteries against the current engine at `layer_cap = 5`, on
**in-budget** substrates — no pressure, no excuse:

| what | battery | re-applied as |
|---|---|---|
| Layer 1 verbs | `write` / `read` / `read_range` / `snapshot` / `restore` / the Answer contract | exact IO, byte-identical round trip, deterministic refusal |
| Layer 2 cues | `_l2tasks` / `_l2score` | `cue-C ≥ 900`, `F ≥ 950`, `B = 1000` (§5 L2) |
| Layer 3 retention | `_l3tasks` / `_l3score`, both frozen pressure streams | identities: everything recalled, nothing invented |
| Layer 4 consolidation | `_l4tasks` / `_l4score` on `corpora/l4stream` | identities: `C = 1000`, reconstruction `F = 1000` |

Engine-gated: every trial that needs an engine SKIPS until
`trials/adapters/l5.py` exists (Stage C), then holds forever.

## The Layer-4 row is new here, and it is the row this layer could break

Layer 4's inheritance battery replayed Layers 1–3. This one adds Layer 4, and it
is not a formality: prospection adds a **pending set**, an **evaluator on the
write path** and **events the engine emits itself**, all of which compete for the
same cells as the interval table. The cheapest way to buy room for them would be
to let the derived view get lossier — which would score beautifully on `§5 L5`'s
four firing clauses while quietly repealing `§5 L4`. In budget, where nothing
forces a drop, the consolidation battery must therefore read **1000 / 1000**
exactly, as an identity and not as the ratified `850 / 900` threshold. That is
this class's rule 3: *the old gates, not new ones — and where the inherited claim
is exactness rather than a threshold, it is asserted as an identity.*

`footprint ≤ 250` is deliberately **not** re-applied. It is a gate about
compression under pressure, and the whole discipline of this class is that
nothing here is under pressure; re-applying it in budget would be asserting a
different claim under a ratified number's name.

## The `t` semantics, and why this class does not have to change for them

`STAGE-B.md §1` settles that a firing is an event and consumes a logical `t` of
its own, so one caller `ingest` can advance `next_t` by more than one. Every
battery below assumes the opposite, and every battery below is still correct: the
general rule is *one caller event plus the firings it caused*, and none of these
substrates carries an intention, so the second term is zero. That is asserted
over the frozen bytes rather than assumed —
`ascension/l5/t_prospection.py::trial_one_caller_ingest_advances_next_t_by_exactly_one_on_an_intention_free_stream`
— and it is the reason this file re-uses the frozen batteries unchanged instead
of forking them for a Layer-5 clock.
"""

from _harness import require, require_equal, try_import
import _l2score
import _l2tasks
import _l3score
import _l3tasks
import _l4score
import _l4tasks
from core.state import event_cost

# The ratified gates of the layers being inherited, re-applied at cap 5. Every
# one is §5 text, quoted in `laws/t_rulings.py`'s registry against this file.
GATE_L2_CUE_C = 900          # §5 L2
GATE_L2_F = 950              # §5 L2
GATE_B = 1000                # §5 L1/L2/L3/L4 — the budget law, absolute everywhere

LAYER_CAP = 5

# The in-budget cap and floor, the same declarations `inheritance/l4` makes and
# for the same reason: at four times a stream's own raw episodic footprint, a
# refusal, an eviction or a lossy answer is not a budget consequence, it is a
# regression. The floor keeps a three-event battery from being starved by an
# engine's fixed structures — and a Layer-5 engine has more of those than a
# Layer-4 one, which is exactly why the floor is declared rather than computed.
INBUDGET_MULTIPLE = 4
INBUDGET_FLOOR = 4096

# The corpus the ratified Layer-4 gate binds on (R4 clause 1). Inherited here in
# budget, where its gate's thresholds become identities.
L4_CORPUS = "l4stream"

_P0 = {"kind": "spawn", "entity": 1, "class": "node"}
_P1 = {"kind": "spawn", "entity": 2, "class": "agent"}
_P2 = {"kind": "spawn", "entity": 3, "class": "vault"}

_ANSWER_KEYS = {"status", "value", "confidence", "provenance"}


def _engine():
    return try_import(
        "adapters.l5",
        "no L5 engine yet; the Layer-5 inheritance battery engages when built "
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

def trial_layer5_inherits_the_layer1_verbs():
    """`write` / `read` / `read_range` at cap 5: exact IO, or Layer 1 is repealed.

    §5 L1 gates Retention at `F = 1000` — *"the exact return of what was written,
    read by time and by range, so any deviation is a bug, not a tolerance."* A
    prospection engine watches; it must still return.

    The `t` assertion below is the general rule's `f = 0` case: these three
    payloads are `spawn` events, nothing is pending, nothing fires, so `t` runs
    `0, 1, 2` exactly as it does at every layer beneath.
    """
    l5 = _engine()
    cap = _inbudget_cap([_P0, _P1, _P2])
    s = _fresh(l5, cap)

    s, t0 = l5.ingest(s, _P0)
    s, t1 = l5.ingest(s, _P1)
    s, t2 = l5.ingest(s, _P2)
    require_equal((t0, t1, t2), (0, 1, 2),
                  "t must begin at 0 and increase by one per successful write on "
                  "a stream that fires nothing (§1.3, STAGE-B.md §1.4) — logical "
                  "time is engine-owned at every layer")

    for t, payload in ((0, _P0), (1, _P1), (2, _P2)):
        ans = l5.query(s, {"op": "read", "t": t})
        require_equal(ans["status"], "answer",
                      "an in-budget read(t=%d) abstained at cap 5" % (t,))
        require_equal(set(ans), _ANSWER_KEYS,
                      "the Answer contract (§7.2) is not honoured at cap 5")
        require_equal(ans["value"], {"payload": payload, "t": t},
                      "read(t=%d) is not byte-exact at cap 5 — Layer 1's F=1000 "
                      "is not a tolerance" % (t,))

    e0 = {"payload": _P0, "t": 0}
    e1 = {"payload": _P1, "t": 1}
    e2 = {"payload": _P2, "t": 2}
    got = l5.query(s, {"op": "read_range", "t0": 0, "t1": 2})
    require_equal(got["status"], "answer", "read_range abstained on a full range")
    require_equal(got["value"], [e0, e1, e2], "read_range is not exact at cap 5")
    require_equal(l5.query(s, {"op": "read_range", "t0": 1, "t1": 99})["value"],
                  [e1, e2],
                  "read_range does not clamp its upper bound at cap 5")
    require_equal(l5.query(s, {"op": "read", "t": 99})["status"], "abstain",
                  "a read past the end of the log must abstain, never fabricate")
    require_equal(l5.query(s, {"op": "no_such_op"})["status"], "abstain",
                  "an unsupported query must abstain, never raise (§7.3)")


def trial_layer5_inherits_the_budget_law_and_the_snapshot_round_trip():
    """The budget law at cap 5, and §5 L1's byte-identical round trip.

    What is inherited is the **law**, not one layer's response to it (§4.1.2): a
    Layer-5 engine has Layer 3, so it may lawfully evict where a Layer-1 engine
    must refuse. What may never differ is the invariant both responses serve —
    occupancy never exceeds the cap, and a refusal is total.
    """
    l5 = _engine()

    # The cap is taken from the engine's OWN accounting of two events: a Layer-5
    # engine charges for a pending set and a fired-row shape header that no
    # `event_cost` sum knows about, and a cap computed from the payloads alone
    # would starve it and test the fixture instead of the law.
    probe = _fresh(l5, _inbudget_cap([_P0, _P1, _P2]))
    probe, _t = l5.ingest(probe, _P0)
    probe, _t = l5.ingest(probe, _P1)
    cap = probe.occupancy

    s = _fresh(l5, cap)
    s, t0 = l5.ingest(s, _P0)
    s, t1 = l5.ingest(s, _P1)
    require_equal((t0, t1), (0, 1),
                  "two events did not fit a cap set to their own measured cost")

    before = l5.snapshot(s)
    occ_before = s.occupancy
    after, t2 = l5.ingest(s, _P2)
    require(after.occupancy <= cap,
            "a write past a full budget left occupancy %d above the cap %d — the "
            "budget law is absolute at every layer (§4.1)"
            % (after.occupancy, cap))
    if t2 is None:
        require_equal(after.occupancy, occ_before,
                      "a refused write must not change occupancy")
        require_equal(l5.snapshot(after), before,
                      "a refused write must leave the state UNCHANGED — no "
                      "partial write, at any layer")
    else:
        require(l5.snapshot(after) != before,
                "the write reported a `t` but changed nothing")

    tiny = _fresh(l5, 2)
    tiny_after, t_ref = l5.ingest(tiny, _P0)
    require(t_ref is None,
            "a payload costing more than the entire cap must be refused — there "
            "is nothing eviction could free that would make room")
    require_equal(l5.snapshot(tiny_after), l5.snapshot(tiny),
                  "a refused write must leave the state unchanged")

    payloads = _l2tasks.store_payloads()
    s = _fresh(l5, _inbudget_cap(payloads))
    for p in payloads:
        s, t = l5.ingest(s, p)
        require(t is not None, "an in-budget write was refused at cap 5")
    snap = l5.snapshot(s)
    require(isinstance(snap, bytes), "snapshot must return bytes (§7.1)")
    restored = l5.restore(snap)
    require_equal(l5.snapshot(restored), snap,
                  "snapshot/restore is not byte-identical at cap 5 — §5 L1's "
                  "round-trip clause holds at every layer above it")
    for t in (0, 7, 61, len(payloads) - 1):
        require_equal(l5.query(s, {"op": "read", "t": t}),
                      l5.query(restored, {"op": "read", "t": t}),
                      "the restored state answered read(t=%d) differently" % (t,))


# ---- Layer 2: the cue battery ----------------------------------------------

def trial_layer5_inherits_the_layer2_cue_battery():
    """§5 L2's own gate, on §5 L2's own tasks, at cap 5.

    `_l2score` is the scorer the Layer-2 ascension and humility trials share, so
    this is that battery and not a friendlier copy of it.
    """
    l5 = _engine()
    payloads = _l2tasks.store_payloads()
    cap = _inbudget_cap(payloads)
    state = _l2score.ingest_store(l5, lambda: _fresh(l5, cap))
    r = _l2score.score(l5, state)

    require(r["cue_C"] >= GATE_L2_CUE_C,
            "cue-C=%d at cap 5, below the §5 L2 gate cue-C≥%d (recovered %d/%d)"
            % (r["cue_C"], GATE_L2_CUE_C, r["recovered"], r["n_answerable"]))
    require(r["F"] >= GATE_L2_F,
            "F=%d at cap 5, below the §5 L2 gate F≥%d (wrong=%d, fabricated=%d)"
            % (r["F"], GATE_L2_F, r["wrong"], r["fabricated"]))
    require(r["B"] >= GATE_B,
            "B=%d at cap 5 — the budget law broke on an in-budget store"
            % (r["B"],))
    require_equal(r["wrong"], 0, "recall returned a wrong target at cap 5")
    require_equal(r["fabricated"], 0,
                  "recall fabricated on an unanswerable cue at cap 5")


# ---- Layer 3: retention, with nothing forcing a drop ------------------------

def trial_layer5_inherits_the_layer3_retention_battery_in_budget():
    """Both frozen pressure streams, replayed with **no pressure** at cap 5."""
    l5 = _engine()
    for name in _l3tasks.STREAMS:
        bundle = _l3tasks.stream(name)
        cap = _inbudget_cap(bundle["payloads"])
        state, budget = _replay_in_budget(l5, cap, bundle["payloads"], name)
        r = _l3score.score(l5, state, name)

        require_equal(budget["refused"], 0,
                      "%s: %d writes were refused at a cap %d× the stream's own "
                      "footprint — nothing here is under pressure"
                      % (name, budget["refused"], INBUDGET_MULTIPLE))
        require(budget["B"] >= GATE_B,
                "%s: B=%d at cap 5 — peak occupancy %d exceeded the cap %d"
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

def trial_layer5_inherits_the_layer4_consolidation_battery_in_budget():
    """§5 L4's own battery on §5 L4's own binding corpus, at cap 5, in budget.

    The row this class gains at Layer 5, and the one prospection could actually
    break. A pending set, an evaluator and the engine's own emitted events all
    compete for the same cells as the interval table; the cheapest way to pay for
    them would be a lossier derived view, which `§5 L5`'s firing clauses would
    never notice.

    In budget the ratified `C ≥ 850` and reconstruction `F ≥ 900` become
    **identities**: nothing forces a fold, so every semantic query must be
    answered and every event returned. `footprint ≤ 250` is not re-applied here
    and the module docstring says why.
    """
    l5 = _engine()
    b = _l4tasks.corpus(L4_CORPUS)
    cap = _inbudget_cap(b["payloads"])
    state, budget = _replay_in_budget(l5, cap, b["payloads"], L4_CORPUS)
    r = _l4score.score(l5, state, b)

    require_equal(budget["refused"], 0,
                  "%s: %d writes were refused at a cap %d× the corpus's own "
                  "footprint" % (L4_CORPUS, budget["refused"], INBUDGET_MULTIPLE))
    require(budget["B"] >= GATE_B,
            "%s: B=%d at cap 5 — peak occupancy %d exceeded the cap %d"
            % (L4_CORPUS, budget["B"], budget["peak"], budget["cap"]))
    require_equal(r["C"], 1000,
                  "%s: C=%d in budget — Q1 %d/%d, Q2 %d/%d, Q3 %d/%d. With "
                  "nothing forcing a fold every semantic query the derived view "
                  "answers at the gate must be answered here"
                  % (L4_CORPUS, r["C"], r["q1"], r["n_q1"], r["q2"], r["n_q2"],
                     r["q3"], r["n_q3"]))
    require_equal(r["F"], 1000,
                  "%s: reconstruction F=%d in budget — %d of %d events did not "
                  "come back byte-exact. Layer 4 released episodes because their "
                  "content lived elsewhere; a Layer-5 engine that released them "
                  "for room has repealed the layer, not inherited it"
                  % (L4_CORPUS, r["F"], r["n_q4"] - r["reconstructed"], r["n_q4"]))
    require_equal(r["reconstruction_wrong"], 0,
                  "%s: reconstruction returned wrong content at cap 5 — "
                  "`wrong = 0` is structural at Layer 4 (README-l4 §1: fold only "
                  "what inverts), so a non-zero count is a repeal"
                  % (L4_CORPUS,))
    require_equal(r["coverage_wrong"], 0,
                  "%s: a semantic query was answered wrongly at cap 5" % (L4_CORPUS,))
    require_equal(r["fabricated"], 0,
                  "%s: %d unanswerable probes were answered at cap 5"
                  % (L4_CORPUS, r["fabricated"]))


# ---- the class's own wiring, engine-free ------------------------------------

def trial_the_inherited_layer4_battery_is_the_frozen_one():
    """The batteries replayed above are the older layers' own, not softer copies.

    Green today and forever, with no engine — the class's rule 4, which exists so
    that a class sitting entirely skipped cannot also be quietly pointing at a
    softer substrate. `inheritance/l4` asserts the shape of the Layer-2 and
    Layer-3 batteries; this asserts the Layer-4 one it adds, on the corpus R4
    binds that gate to.
    """
    b = _l4tasks.corpus(L4_CORPUS)
    require_equal(b["name"], L4_CORPUS,
                  "the inherited Layer-4 battery is built over a different corpus")
    require_equal(b["n_coverage"], b["n_q1"] + b["n_q2"] + b["n_q3"],
                  "the inherited coverage denominator is not Q1+Q2+Q3")
    require_equal(b["n_q4"], b["n"],
                  "the inherited reconstruction battery is no longer one query "
                  "per event — Q4 is `read(t)` asked of the whole stream")
    require(b["n"] > 0 and b["n_coverage"] > 0,
            "the inherited Layer-4 battery is empty, which would make every "
            "identity above vacuously true")

    cap = _inbudget_cap(b["payloads"])
    require(cap > b["budget_cap"],
            "the in-budget cap (%d) is not larger than the ratified Layer-4 "
            "footprint cap (%d) — this class asserts identities that only hold "
            "when nothing is under pressure, and it must be measurably not under "
            "pressure" % (cap, b["budget_cap"]))
    require_equal(cap, INBUDGET_MULTIPLE * b["raw_cells"],
                  "the in-budget cap for %s is no longer the declared multiple of "
                  "its own raw episodic footprint" % (L4_CORPUS,))

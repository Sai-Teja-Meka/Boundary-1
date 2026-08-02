"""ops/dogfood — the confidence surface (`shell/dogfood/consolidate.py`, `[L6]`).

`[L6] [DOGFOOD]`. The store's derived view now replays through
`core/layers/l6_meta_memory.py`, and the whole of that upgrade is that every
answer the shell reads back carries the engine's own `§7.2` confidence and the
report prints it. These trials hold the surface to five things:

  * the shell's set-once reading is a **narrowing** of the engine's frozen one,
    computed from it rather than typed beside it — `intend.py`'s rule for the
    condition vocabulary, applied to the second reading this shell declares;
  * the upgrade is **zero-state**: the derived state a Layer-6 replay builds is
    byte-identical to the Layer-5 replay's in every branch but the recorded
    `layer_cap`, and every answer's `status` and `value` are unchanged
    (`README-l6 §0`, on this project's own history rather than on a corpus);
  * every rendered answer carries an **integer permille** in `[0, 1000]` —
    `§7.2`'s currency, and a harness-level failure if it is anything else
    (`STAGE-B.md`'s rule for a Layer-6 battery, applied to a reader);
  * a **contradicted** set-once chain renders visibly less certain than a clean
    one, and an `as-of` before the contradiction renders certain, which is
    `README-l6 §1.4`'s horizon seen through the shell's own `asof` walk;
  * on the **committed store** the census is measured rather than assumed: no
    key of this reading is set-once, so every answer states `CERTAIN` and the
    report says why. `FIELD.md` (2026-08-02) carries the same numbers.

The committed store is only ever read. Every trial that writes uses a temporary
directory or an in-memory derived state.
"""

import io
import os

from _harness import require, require_equal, skip

from core.serialize import decode, encode
from core.layers import l2_recall as ledger
from core.layers import l5_prospection as l5
from core.layers import l6_meta_memory as l6
from shell.dogfood import cli, consolidate as co
from shell.dogfood import event as ev
from shell.dogfood import store as st


def _summary(move, line, questions=()):
    return {"project": "trial-project", "move": move,
            "decisions": ["a decision"], "files_touched": [],
            "open_questions": list(questions), "log_line": line}


STREAM = [
    _summary("FORGE", "[L1] [FORGE] retention <suite: 72/72 green> <anchors: born>"),
    _summary("ASCEND", "[L2] [ASCEND] recall <suite: 98/98 green> <anchors: l1 intact, l2 born>",
             questions=["how sure is the store of itself?"]),
]


def _records():
    return [{"payload": ev.build_payload(s), "t": i} for i, s in enumerate(STREAM)]


def _permille(value, why):
    require(isinstance(value, int) and not isinstance(value, bool),
            "%s: a confidence is an INTEGER permille (§7.2, §3.4) and a float or "
            "a bool there is a harness-level failure, not a low score" % why)
    require(0 <= value <= 1000, "%s: confidence %r is outside [0,1000]" % (why, value))


# ---- 1. the reading, narrowed and computed ----------------------------------

def trial_the_shell_declares_a_narrowing_of_the_engines_set_once_reading():
    """`SET_ONCE_KEYS` is the engine's reading intersected with this one.

    Two claims, and the second is the one with teeth. The set is a **subset** of
    `l6.SET_ONCE_KEYS`, so this shell can never call a key set-once that the
    engine does not — the confidence would then be the shell's own opinion and
    `§5 L6` asks the ENGINE for a number derived from structural evidence. And it
    is **computed**, so it cannot fall out of step with a reading that is frozen
    somewhere else: a typed copy would be a second reading, which is exactly the
    drift `ops/l4` and `ops/l6` exist to forbid one layer down.
    """
    declared = tuple(ASSERTED for ASSERTED in co.SET_ONCE_KEYS)
    for key in declared:
        require(l6.set_once(key),
                "%r is called set-once by the shell and not by the engine — the "
                "shell narrows, it never widens" % (key,))
    require_equal(
        declared,
        tuple(k for k in tuple(co.ASSERTED_KEYS) + (co.QUESTION_KEY,)
              if l6.set_once(k)),
        "the shell's set-once reading must be COMPUTED from the engine's, not "
        "typed beside it")

    # Today the intersection is empty, and the census is built to say so rather
    # than to hide it: it asks about every key the ENGINE calls set-once too.
    require_equal(co.SET_ONCE_KEYS, (),
                  "no key this reading asserts is set-once under the engine's "
                  "frozen reading (%s) — if that ever changes, the census rows "
                  "and FIELD.md's 2026-08-02 measurement change with it"
                  % ", ".join(l6.SET_ONCE_KEYS))
    for key in l6.SET_ONCE_KEYS:
        require(key in co.CENSUS_KEYS,
                "the census must ASK about %r: it is a key on which a confidence "
                "can move, and a census that only asked about what this reading "
                "writes could never see a tie" % (key,))


# ---- 2. the upgrade is zero-state -------------------------------------------

def trial_the_derived_replay_is_layer_6_and_adds_no_state():
    """`README-l6 §0` on this project's own memory: the number moved, not the state.

    The same records are folded twice — once through the frozen Layer-5 engine
    and once through the Layer-6 one — and the two states are compared through
    their canonical snapshots (§2.4). They must agree in **every branch but the
    recorded `layer_cap`**, which is the cap and not the content; and every
    answer must agree in `status` and `value`, because Layer 6 attaches a number
    and does not answer differently.
    """
    records = _records()
    six, origin, _s, entities, refused = co.derive(records)
    require(refused is None, "the default cap must admit the whole stream")
    require_equal(six.layer_cap, l6.LAYER, "the derived replay must be Layer 6")

    five = l5.make_engine(l5.LAYER, budget_cap=co.DERIVED_BUDGET)
    for record in records:
        for derived in co.derived_stream(record["payload"], entities):
            five, t = l5.write(five, derived)
            require(t is not None, "the Layer-5 control replay must not refuse")

    body6 = decode(l6.snapshot(six))["body"]
    body5 = decode(l5.snapshot(five))["body"]
    require_equal(body6["layer_cap"], 6, "the Layer-6 body records its own cap")
    require_equal(body5["layer_cap"], 5, "the Layer-5 body records its own cap")
    body6["layer_cap"] = body5["layer_cap"]
    require_equal(encode(body6), encode(body5),
                  "a Layer-6 replay of this store must hold EXACTLY what the "
                  "Layer-5 replay held — `L6State` adds no field (README-l6 §0), "
                  "so a confidence model that cost a cell here would be visible "
                  "as a divergence in these bytes")

    entity = entities["trial-project"]
    for key in co.ASSERTED_KEYS:
        a6 = l6.query(six, {"op": "current", "entity": entity, "key": key})
        a5 = l5.query(five, {"op": "current", "entity": entity, "key": key})
        require_equal(a6["status"], a5["status"], "status moved at key %r" % key)
        require_equal(encode(a6["value"]), encode(a5["value"]),
                      "the ANSWER moved at key %r — Layer 6 attaches a number, "
                      "it does not answer differently (README-l6 §1.1)" % key)
        _permille(a6["confidence"], "current(%s)" % key)
    require_equal(co.current_fact(six, entity, "layer", origin)[2], l6.CERTAIN,
                  "a key that admits updates is answered by its latest "
                  "assertion, and the engine has proved that")


# ---- 3. every rendered answer carries a permille ----------------------------

def trial_every_answer_the_surface_renders_carries_an_integer_permille():
    records = _records()
    state, origin, sessions, entities, _r = co.derive(records)
    entity = entities["trial-project"]

    for key in tuple(co.ASSERTED_KEYS) + (co.QUESTION_KEY,):
        now = co.current_fact(state, entity, key, origin)
        if now is not None:
            _permille(now[2], "current_fact(%s)" % key)
        for store_t, _value, conf in co.history(state, entity, key, origin,
                                                state.next_t - 1):
            _permille(conf, "history(%s) at store t=%s" % (key, store_t))
        for _t, _v, _n, conf in co.collapse(
                co.history(state, entity, key, origin, state.next_t - 1)):
            _permille(conf, "collapse(%s)" % key)

    rows, engine_view = co.calibration(state, entity, origin, state.next_t - 1)
    require_equal(engine_view["status"], "answer",
                  "the engine's own calibration diagnostic must answer (§7.1)")
    require_equal(len(rows), len(co.CENSUS_KEYS), "one census row per census key")
    for row in rows:
        if row["confidence"] is not None:
            _permille(row["confidence"], "census row %r" % row["key"])

    text = "\n".join(co.report(state, origin, sessions, entities, records))
    require("‰" in text, "the report must render the permille it read")
    require("calibration — what this store says about its own certainty" in text,
            "the report lost its calibration section")
    for key in co.ASSERTED_KEYS:
        require("%s " % key in text, "the census lost its %r row" % key)


def trial_the_recall_surface_states_a_confidence_even_when_it_abstains():
    """An abstention is an answer (§3.0), so it is rendered with its number.

    `§7.2` gives an abstention `confidence: 0` — it states no value, so there is
    no claim for a confidence to be about — and the CLI prints it rather than
    printing the number only when it is high, which would report the engine's
    certainty and hide its silence.
    """
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp(prefix="dogfood-calib-")
    try:
        path = os.path.join(tmp, "store.json")
        for summary in STREAM:
            out, err = io.StringIO(), io.StringIO()
            code = cli.main(["--store", path, "remember",
                             "--project", summary["project"],
                             "--move", summary["move"],
                             "--log-line", summary["log_line"]], out=out, err=err)
            require_equal(code, cli.EXIT_OK, "remember failed: %s" % err.getvalue())

        out, err = io.StringIO(), io.StringIO()
        code = cli.main(["--store", path, "recall", "nosuchtokenanywhere"],
                        out=out, err=err)
        require_equal(code, cli.EXIT_OK, "an abstention is exit 0 (§3.0)")
        text = out.getvalue()
        require("ABSTAIN  confidence=0‰" in text,
                "a recall abstention must state its own confidence: %r" % text)

        out, err = io.StringIO(), io.StringIO()
        code = cli.main(["--store", path, "recall", "retention"], out=out, err=err)
        require_equal(code, cli.EXIT_OK, "a hit is exit 0")
        require("MATCH  confidence=" in out.getvalue(),
                "a recall hit must state its own confidence")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---- 4. a contradicted key is visibly less certain --------------------------

def _tied_state():
    """A derived state carrying a set-once tie and a clean chain beside it.

    Built by hand rather than from a session summary, and that is the finding
    this fixture exists to pin: the shell's reading emits no `origin`, so a
    contradiction is not reachable from this store's own fuel (`FIELD.md`,
    2026-08-02). What IS reachable is the renderer, and the renderer must show
    the difference the moment a set-once chain has one.
    """
    state = l6.make_engine(l6.LAYER, budget_cap=1 << 20)
    stream = [{"kind": "attr", "entity": 1, "key": "layer", "val": 5},
              {"kind": "attr", "entity": 1, "key": "origin", "val": "first"},
              {"kind": "attr", "entity": 1, "key": "layer", "val": 6},
              {"kind": "attr", "entity": 1, "key": "origin", "val": "second"}]
    origin = {}
    for i, payload in enumerate(stream):
        state, t = l6.write(state, payload)
        require(t is not None, "the fixture must fit its cap")
        origin[t] = i
    return state, origin


def trial_a_contradicted_set_once_chain_is_visibly_less_certain_than_a_clean_one():
    state, origin = _tied_state()

    clean = co.current_fact(state, 1, "layer", origin)
    tied = co.current_fact(state, 1, "origin", origin)
    require_equal(clean[2], 1000,
                  "a key that admits updates is answered by its latest and the "
                  "engine has proved it")
    require_equal(tied[2], 500,
                  "a set-once chain holding two mutually exclusive claimants is "
                  "answered at permille(1/2) — the tie's own arithmetic, derived "
                  "and not typed (README-l6 §1.3)")
    require(tied[2] < clean[2],
            "the whole point of the surface: a contradicted key must render "
            "LESS CERTAIN than a clean one")

    # The horizon: `asof` prices the evidence the answer actually had, so the
    # walk shows where the chain stopped being sure of itself (README-l6 §1.4).
    walked = co.history(state, 1, "origin", origin, state.next_t - 1)
    require_equal([c for _t, _v, c in walked], [1000, 500],
                  "an as-of before the contradiction saw one claimant and was "
                  "right to say 1000; the step that introduced the second must "
                  "drop to 500")

    lines = co.calibration_lines(state, 1, origin, state.next_t - 1)
    text = "\n".join(lines)
    require("SET-ONCE" in text, "the census must mark the set-once row")
    require("500‰" in text, "the census must render the tie's own confidence")
    require("permille(1/d)" in text,
            "with a tie present the census must state the rule it applied, not "
            "the no-contradiction reason: %r" % text)
    require("ties             1 chain" in text,
            "the shell's census and the engine's own calibration diagnostic "
            "must agree on the tie count: %r" % text)


# ---- 5. the committed store (read-only) -------------------------------------

def trial_the_committed_stores_calibration_census_is_measured():
    """This project's own history, and what it says about its own uncertainty.

    The mandatory `[L6] [DOGFOOD]` measurement, asserted rather than only
    written down. Every key this reading asserts holds several values over the
    store's life — `layer` climbs, `move` changes every session, `suite` changes
    almost every session — and **not one of them is a contradiction**, because a
    chain that disagrees with itself is a contradiction only where the key admits
    exactly one value. So the store states `CERTAIN` everywhere and is right to,
    and the number is a proof rather than a default: the same renderer states 500
    on a tie (the trial above).
    """
    path = st.default_store_path()
    if not os.path.isfile(path):
        skip("no committed dogfood store yet (%s)" % st.display_path(path))
    state = st.load(path)
    records = ledger.read_range(state, 0, state.next_t - 1)
    derived, origin, _sessions, entities, refused = co.derive(records)
    require(refused is None, "the committed store must fold inside the derived cap")
    entity = entities["boundary-1-memory"]

    rows, engine_view = co.calibration(derived, entity, origin, derived.next_t - 1)
    require_equal(engine_view["value"]["ties"], 0,
                  "the engine reads no tie in this project's history")
    require_equal(engine_view["value"]["set_once_keys"], list(l6.SET_ONCE_KEYS),
                  "the diagnostic must report the engine's own reading")

    moving = 0
    for row in rows:
        if row["confidence"] is None:
            require(not row["asserts"],
                    "%r abstains but the chain walk found %d assertions"
                    % (row["key"], row["asserts"]))
            require(row["key"] in l6.SET_ONCE_KEYS,
                    "only a key the census ASKS about but this reading never "
                    "writes may be absent, and %r is not one" % (row["key"],))
            continue
        require_equal(row["confidence"], l6.CERTAIN,
                      "%r states %d‰: on this store every answer is CERTAIN, "
                      "because no key of this reading is set-once — if that has "
                      "changed, FIELD.md's 2026-08-02 census is stale and this "
                      "trial is where it says so"
                      % (row["key"], row["confidence"]))
        require(not row["set_once"],
                "%r is set-once now; the census, FIELD.md and README.md all "
                "record that none was" % (row["key"],))
        if row["claimants"] > 1:
            moving += 1
    require(moving >= 3,
            "the finding is not that nothing changed — it is that several chains "
            "disagree with themselves and none of the disagreements is a "
            "contradiction; only %d chain(s) hold more than one value" % moving)


def trial_the_kept_promises_take_back_is_rendered_by_the_surface():
    """What `read(t0)` says about a promise the store has kept, in the report.

    `trials/ops/dogfood/t_consolidate.py` asserts the take-back of the ENGINE.
    This asserts that the SURFACE says so: a kept promise's own `intend` event is
    readable, byte-exact and tagged `recall` — never `derive`, because nothing
    regenerates it once the pending entry is gone (`README-l5 §1.3`).
    """
    path = st.default_store_path()
    if not os.path.isfile(path):
        skip("no committed dogfood store yet (%s)" % st.display_path(path))
    state = st.load(path)
    records = ledger.read_range(state, 0, state.next_t - 1)
    derived, origin, _sessions, _entities, _refused = co.derive(records)
    kept = [p for p in co.promises(derived, records, origin) if p["fired"]]
    if not kept:
        skip("the store has kept no promise yet — nothing to render")

    text = "\n".join(co.prospection_lines(derived, records, origin))
    for promise in kept:
        require_equal(promise["provenance"], "recall",
                      "iid %s's own event is tagged %r" % (promise["iid"],
                                                           promise["provenance"]))
        require(promise["regenerated"],
                "iid %s's own event must come back byte-exact" % promise["iid"])
        _permille(promise["confidence"], "read(t0) of iid %s" % promise["iid"])
        for fired in promise["fired"]:
            require_equal(fired["provenance"], "derive",
                          "a fired event is regenerated by the fired ledger, so "
                          "its provenance is `derive` and not `recall`")
            _permille(fired["confidence"], "read(t_fire) of iid %s" % promise["iid"])
    require("taken back into the store" in text,
            "the surface must say that the episode was taken back: %r" % text)
    require("provenance recall" in text,
            "the surface must render the provenance kind it read")

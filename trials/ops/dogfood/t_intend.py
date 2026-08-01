"""ops/dogfood — the prospection surface (`shell/dogfood/intend.py`).

`[L5] [DOGFOOD]`. `intend` declares a promise: a condition over the sessions this
project has not written yet, and the payload to surface when one satisfies it.
The store keeps the event; `core/layers/l5_prospection.py` keeps the promise.
These trials hold the shell to five things, and every one of them is a claim
about the *seam* between the two — the engine's own gate is not re-litigated
here, `trials/ascension/l5/` owns it:

  * the declared reading **narrows** the frozen condition grammar and never
    widens it — everything it admits is `l5.readable`, and the four narrowings
    are each a fact about what `consolidate.py` emits;
  * **no payload this shell can fire satisfies any condition it can admit**,
    asserted over the whole cross product with the counters set against it, so
    cascades are impossible by construction and not by inspection
    (`corpora/l5stream/grammar.md`'s own argument, in the shell's vocabulary);
  * an intention is stored in the **engine's own form and nothing else** — a
    fourth field costs it the inversion `README-l5 §1.2` demands, and the trial
    shows the cost rather than describing it;
  * a promise **fires exactly once**, on the first session that satisfies it,
    with the `t`-accounting `BOUNDARY-RULINGS.md R6` clause 2 ratified:
    `next_t` advances by `1 + f` on the satisfying write and by 1 on every other;
  * a condition that **spans the consolidation boundary** still fires when the
    content it counts has been demoted, and the promise's own episode is then
    either taken back or **booked as a loss** — never quietly both.

Every trial that writes uses a temporary directory. The committed store is only
ever read.
"""

import io
import os
import shutil
import tempfile

from _harness import require, require_equal, skip

from core.serialize import encode
from core.layers import l2_recall as ledger
from core.layers import l5_prospection as l5
from shell.dogfood import cli, consolidate as co
from shell.dogfood import event as ev
from shell.dogfood import intend as it
from shell.dogfood import store as st


def _summary(move, line, questions=()):
    return {"project": "trial-project", "move": move,
            "decisions": ["a decision"], "files_touched": [],
            "open_questions": list(questions), "log_line": line}


def _run(argv):
    out, err = io.StringIO(), io.StringIO()
    code = cli.main(argv, out=out, err=err)
    return code, out.getvalue(), err.getvalue()


def _cond(*atoms):
    return it.condition(list(atoms))


LAYER_SIX = _cond(it.atom("kind", "attr"), it.atom("entity", 1),
                  it.atom("key", "layer"), it.atom("val_ge", 6))

FIRE = it.reminder("trials/adapters/INTERFACE.md", "the attribute gap is still open")


# ---- 1. the declared reading narrows, and never widens ----------------------

def trial_the_declared_reading_narrows_the_frozen_grammar_and_never_widens_it():
    """Everything admitted is `l5.readable`; the four narrowings each bite.

    The engine is the authority on what can be armed and the shell is the
    authority on what this store's own reading can ever assert. A condition the
    shell admits that the engine could not evaluate would be a promise that
    never arms; a condition the engine could evaluate but nothing here writes
    would be a promise that never fires. Both are silent, so both are refused at
    declare time, loudly.
    """
    it.validate_condition(LAYER_SIX)
    require(l5.readable(LAYER_SIX), "a declared condition must be engine-readable")

    good = [
        _cond(it.atom("kind", ev.KIND)),
        _cond(it.atom("entity", 1), it.atom("count_ge", 250, k="attr")),
        _cond(it.atom("key", "open_question")),
        _cond(it.atom("key", "suite"), it.atom("entity", 3)),
    ]
    for cond in good:
        it.validate_condition(cond)
        require(l5.readable(cond),
                "the shell admitted a condition the engine cannot read: %r" % (cond,))

    bad = [
        ("or", {"op": "or", "args": [it.atom("kind", "attr"), it.atom("key", "layer")]}),
        ("not", {"op": "not", "args": [it.atom("kind", "attr")]}),
        ("nested", {"op": "and", "args": [it.atom("kind", "attr"),
                                          {"op": "and", "args": [it.atom("key", "layer")]}]}),
        ("loc", _cond(it.atom("kind", "attr"), it.atom("loc", "here"))),
        ("undeclared key", _cond(it.atom("key", "no-such-key"))),
        ("undeclared kind", _cond(it.atom("kind", "note"))),
        ("count over an undeclared kind", _cond(it.atom("entity", 1),
                                                it.atom("count_ge", 3, k="note"))),
        ("no guard", _cond(it.atom("count_ge", 3, k="attr"))),
        ("no guard, val only", _cond(it.atom("val_ge", 6))),
        ("string bound", _cond(it.atom("kind", "attr"), it.atom("val_ge", "six"))),
        ("not an object", "kind=attr"),
    ]
    for label, cond in bad:
        try:
            it.validate_condition(cond)
        except ev.SchemaError:
            continue
        raise AssertionError("the declared reading admitted %s: %r" % (label, cond))

    # `loc` is the one predicate refused while being perfectly readable to the
    # engine — the refusal is about this store's reading, not about the grammar.
    require(l5.readable(_cond(it.atom("kind", "attr"), it.atom("loc", "here"))),
            "the `loc` refusal must be the SHELL's, so the engine must still read it")


def trial_no_payload_this_shell_fires_can_satisfy_a_condition_it_admits():
    """GUARDEDNESS, over the whole cross product, with the counters against it.

    `corpora/l5stream/grammar.md` makes cascades impossible by construction and
    asserts it over its own 945x945 cross product. This is the same argument in
    the shell's vocabulary: a `reminder`'s kind is outside `DECLARED_KINDS`, it
    carries no `entity` and no `src`, and it has no Layer-4 facet, so every guard
    atom is false of it — and every declared condition carries a guard.

    The counts are set to a number every `count_ge` clears, so the trial asserts
    the GUARD does the work and not an accident of arithmetic.
    """
    conditions = []
    for kind in it.DECLARED_KINDS:
        conditions.append(_cond(it.atom("kind", kind)))
        for key in it.DECLARED_KEYS:
            conditions.append(_cond(it.atom("kind", kind), it.atom("key", key)))
            for entity in (1, 2, 7):
                conditions.append(_cond(it.atom("kind", kind), it.atom("entity", entity),
                                        it.atom("key", key), it.atom("val_ge", 6)))
                conditions.append(_cond(it.atom("entity", entity), it.atom("key", key),
                                        it.atom("count_ge", 1, k=kind)))
    require(len(conditions) > 100, "the cross product must be a real one")

    fires = [FIRE,
             it.reminder("x", "y"),
             it.reminder("a path", "a much longer sentence, with punctuation: § — 6")]
    counts = {kind: 10 ** 6 for kind in it.DECLARED_KINDS}
    counts[it.REMINDER_KIND] = 10 ** 6

    for cond in conditions:
        it.validate_condition(cond)                     # only declared conditions
        for fire in fires:
            require(it.guarded(fire), "the fire payload must be a declared one")
            require(not l5.satisfies(cond, fire, counts),
                    "a fired payload satisfied a declared condition — cascades are "
                    "supposed to be impossible by construction: %r vs %r"
                    % (cond, fire))
            require(l5.arms(fire) is None,
                    "a fired payload must not itself arm an intention")
    require(it.REMINDER_KIND not in it.DECLARED_KINDS,
            "the fire kind must stay outside the kinds a condition may name — that "
            "is half the guardedness argument")


# ---- 2. the stored form is the engine's own ---------------------------------

def trial_an_intention_is_stored_in_the_engines_own_form_and_nothing_else():
    """Three fields, and a fourth costs the promise its arming.

    `README-l5 §1.2` admits an intention only when the payload rebuilds from
    `(iid, cond, fire)` as **canonical bytes**, so there is no room in the event
    for a `tok` cue surface, a project name, or a note about who declared it.
    That is the price `FIELD.md` records — a promise is `t`-addressable and not
    cue-addressable — and this asserts it rather than describing it.
    """
    payload = it.build_payload(1, LAYER_SIX, FIRE)
    require_equal(sorted(payload), ["cond", "fire", "iid", "kind"],
                  "an intention carries exactly the fields the engine inverts")
    require_equal(payload["kind"], l5.INTENTION_KIND, "the kind is the engine's own")
    require(l5.arms(payload) is not None, "the engine must arm what the shell built")
    require_equal(encode(l5.rebuild_intention(1, LAYER_SIX, FIRE)), encode(payload),
                  "the payload must be exactly its own rebuild (§2.4)")

    # The cue surface a session summary gets is exactly what an intention cannot
    # have: adding it keeps the payload canonical and stops it arming.
    with_tok = dict(payload)
    with_tok["tok"] = {"interface": 1}
    require(l5.arms(with_tok) is None,
            "a fourth field must cost the payload its arming — this is why an "
            "intention has no cue surface")

    for label, args in (("iid 0", (0, LAYER_SIX, FIRE)),
                        ("iid as bool", (True, LAYER_SIX, FIRE)),
                        ("undeclared condition", (1, {"p": "loc", "v": "x"}, FIRE)),
                        ("fire not a reminder", (1, LAYER_SIX, {"kind": "attr",
                                                                "entity": 1,
                                                                "key": "layer",
                                                                "val": 6}))):
        try:
            it.build_payload(*args)
        except ev.SchemaError:
            continue
        raise AssertionError("build_payload accepted %s" % label)


# ---- 3. exactly once, at the first satisfaction, with its own t -------------

def _store_with_a_promise(path, tail=()):
    """A temp store: three sessions, the layer-6 promise, then `tail` sessions."""
    for summary in (_summary("FORGE", "[L3] [FORGE] a <suite: 1/1 green>"),
                    _summary("ASCEND", "[L4] [ASCEND] b <suite: 2/2 green>"),
                    _summary("PULSE", "[L5] [PULSE] c <suite: 3/3 green>")):
        code, _out, err = _run(["--store", path, "remember",
                                "--project", summary["project"],
                                "--move", summary["move"],
                                "--log-line", summary["log_line"]])
        require_equal(code, cli.EXIT_OK, "remember failed: %s" % err)
    code, out, err = _run(["--store", path, "intend", "--project", "trial-project",
                           "--when-kind", "attr", "--when-key", "layer",
                           "--when-val-ge", "6",
                           "--about", "trials/adapters/INTERFACE.md",
                           "--surface", "the attribute gap is still open"])
    require_equal(code, cli.EXIT_OK, "intend failed: %s" % err)
    armed_t = int(out.strip())
    for summary in tail:
        code, _out, err = _run(["--store", path, "remember",
                                "--project", summary["project"],
                                "--move", summary["move"],
                                "--log-line", summary["log_line"]])
        require_equal(code, cli.EXIT_OK, "remember failed: %s" % err)
    state = st.load(path)
    return state, ledger.read_range(state, 0, state.next_t - 1), armed_t


def trial_a_promise_fires_exactly_once_on_the_first_session_that_satisfies_it():
    tmp = tempfile.mkdtemp(prefix="dogfood-trial-")
    try:
        path = os.path.join(tmp, "store.json")
        _state, records, armed_t = _store_with_a_promise(path, tail=[
            _summary("PULSE", "[L5] [PULSE] still five <suite: 4/4 green>"),
            _summary("ASCEND", "[L6] [ASCEND] the sixth <suite: 5/5 green>"),
            _summary("PULSE", "[L6] [PULSE] the sixth again <suite: 6/6 green>"),
            _summary("PULSE", "[L7] [PULSE] the seventh <suite: 7/7 green>")])

        derived, origin, _sessions, _entities, refused = co.derive(records)
        require(refused is None, "the default cap must admit the whole stream")

        entries = co.promises(derived, records, origin)
        require_equal(len(entries), 1, "the store declared exactly one promise")
        entry = entries[0]
        require_equal(entry["store_t"], armed_t, "the promise is the one declared")
        require_equal(len(entry["fired"]), 1,
                      "dup-fire = 0 is a gate clause: the ledger answers with a "
                      "LIST, and it must have exactly one element")

        fired = entry["fired"][0]
        require_equal(fired["store_t"], armed_t + 2,
                      "it must fire at the FIRST session asserting layer >= 6, "
                      "not the second and not the seventh")
        require_equal(encode(fired["payload"]), encode(entry["fire"]),
                      "the fired payload is the one the caller wrote into the "
                      "intention, byte for byte (§1.4)")

        # Nothing fired before the satisfying session, and nothing after it.
        before = [r for r in records if r["t"] < fired["store_t"]]
        early, early_origin, _s, _e, _r = co.derive(before)
        require_equal(co.ask(early, {"op": "fired", "iid": entry["iid"]})["status"],
                      "abstain",
                      "the promise must still be pending before its satisfaction")
        require(co.promises(early, before, early_origin)[0]["readable"],
                "a pending promise's own event stays readable (README-l5 §1.3)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def trial_a_firing_consumes_a_logical_t_of_its_own_r6_clause_2():
    """`next_t` advances by `1 + f` on the satisfying write, by 1 on every other.

    The shell is where this stops being a corpus property and becomes something a
    reader of this store has to live with: replay `t` is no longer an index into
    the caller stream, which is why `consolidate.origin` is a map and not a list.
    """
    tmp = tempfile.mkdtemp(prefix="dogfood-trial-")
    try:
        path = os.path.join(tmp, "store.json")
        _state, records, armed_t = _store_with_a_promise(path, tail=[
            _summary("ASCEND", "[L6] [ASCEND] the sixth <suite: 5/5 green>")])

        entities = co.project_entities(records)
        derived = l5.make_engine(l5.LAYER, budget_cap=co.DERIVED_BUDGET)
        callers = 0
        jumps = []
        for record in records:
            for payload in co.derived_stream(record["payload"], entities):
                before = derived.next_t
                derived, t = l5.write(derived, payload)
                require(t is not None, "the trial cap must admit every write")
                require_equal(t, before, "ingest returns the CALLER event's t")
                callers += 1
                delta = derived.next_t - before
                if delta != 1:
                    jumps.append((record["t"], payload.get("kind"), delta))

        require_equal(len(jumps), 1,
                      "exactly one caller write may advance next_t by more than "
                      "1 — the one that satisfied the condition")
        require_equal(jumps[0][2], 2, "1 + f, with f = 1 (R6 clause 2)")
        require_equal(jumps[0][1], "attr",
                      "the satisfying write is the assertion, not the episode")
        require_equal(derived.next_t - callers, 1,
                      "the engine's own clock is the auditor: next_t minus the "
                      "caller stream is the number of firings")

        # ... and the report's `origin` covers every one of those times.
        state2 = st.load(path)
        again, origin, _s, _e, _r = co.derive(
            ledger.read_range(state2, 0, state2.next_t - 1))
        require_equal(len(origin), again.next_t,
                      "origin must map EVERY logical time, firings included")
        entry = co.promises(again, ledger.read_range(state2, 0, state2.next_t - 1),
                            origin)[0]
        require_equal(entry["fired"][0]["store_t"], armed_t + 1,
                      "a firing is attributed to the store event whose write "
                      "satisfied it")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---- 4. the consolidation boundary ------------------------------------------

def trial_a_fold_over_demoted_content_still_fires_and_the_promise_is_accounted():
    """The mandatory field measurement, at trial scale.

    A `count_ge` condition is a fold over the Layer-4 per-kind counters, which
    are two cells per kind and are never decremented — so it outlives the
    episodes it counts (`README-l5 §2.3`). Under a cap that demotes them:

      * the promise still fires, exactly once;
      * the content it counted is answered by `read(t)` as `derive` or not at
        all, and never as a held episode;
      * the promise's **own** episode is either taken back (readable) or booked
        into the forgetting record (unreadable) — never gone and unbooked, which
        is the defect `BOUNDARY.log` line 26 found one layer down.
    """
    tmp = tempfile.mkdtemp(prefix="dogfood-trial-")
    try:
        path = os.path.join(tmp, "store.json")
        for i in range(6):
            code, _out, err = _run(["--store", path, "remember",
                                    "--project", "trial-project", "--move", "PULSE",
                                    "--log-line", "[L5] [PULSE] session %d "
                                                  "<suite: %d/%d green>" % (i, i, i)])
            require_equal(code, cli.EXIT_OK, "remember failed: %s" % err)
        code, out, err = _run(["--store", path, "intend", "--project", "trial-project",
                               "--when-kind", "attr",
                               "--when-count-ge", "attr:40",
                               "--about", "the consolidation boundary",
                               "--surface", "the fold outlived what it counted"])
        require_equal(code, cli.EXIT_OK, "intend failed: %s" % err)
        armed_t = int(out.strip())
        for i in range(6):
            _run(["--store", path, "remember", "--project", "trial-project",
                  "--move", "PULSE", "--log-line", "[L5] [PULSE] later %d "
                                                   "<suite: %d/%d green>" % (i, i, i)])

        state = st.load(path)
        records = ledger.read_range(state, 0, state.next_t - 1)
        roomy, roomy_origin, _s, _e, _r = co.derive(records)
        require_equal(roomy.demotions, 1,
                      "at a roomy cap the ONLY demotion is the fired intention's "
                      "own episode being taken back and given back again — "
                      "arming released it, firing consumed the derivation")

        entry = co.promises(roomy, records, roomy_origin)[0]
        require_equal(len(entry["fired"]), 1, "the fold must fire exactly once")
        counted_at = entry["fired"][0]["store_t"]

        # Now the same replay under pressure.
        tight = roomy.occupancy // 3
        squeezed, origin, _s2, _e2, refused = co.derive(records, budget_cap=tight)
        require(refused is None, "the pressured replay must still admit the stream")
        require(squeezed.demotions > 1, "a third of the budget must force demotion")

        pressed = co.promises(squeezed, records, origin)[0]
        require_equal(len(pressed["fired"]), 1,
                      "the fold must fire exactly once under pressure too — it "
                      "reads counters, not episodes")
        require_equal(pressed["fired"][0]["store_t"], counted_at,
                      "and at the same satisfaction point as at the roomy cap")

        # The content it counted: demoted or gone, never a held episode.
        held_attr = 0
        derived_attr = 0
        for t in range(squeezed.next_t):
            answer = co.ask(squeezed, {"op": "read", "t": t})
            if answer["status"] != "answer":
                continue
            if answer["value"]["payload"].get("kind") != co.ASSERTION_KIND:
                continue
            if answer["provenance"]["kind"] == "recall":
                held_attr += 1
            else:
                derived_attr += 1
        require(derived_attr > 0,
                "the assertions the fold counted must actually be demoted, or "
                "this measures nothing")

        # The promise's own episode: taken back, or booked. Never neither.
        armed_at = co._replay_t(origin, armed_t)
        seen = co.ask(squeezed, {"op": "read", "t": armed_at})
        record = co.ask(squeezed, {"op": "forgetting"})["value"]
        if seen["status"] == "answer":
            require_equal(encode(seen["value"]["payload"]),
                          encode(records[[r["t"] for r in records].index(armed_t)]["payload"]),
                          "a taken-back promise must come back byte-exact")
        else:
            require(record["count"] > 0,
                    "a promise whose episode the budget could not take back must "
                    "be IN THE RECORD — a demotion booked as a loss, never a "
                    "silence (BOUNDARY.log line 26)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---- 5. the CLI --------------------------------------------------------------

def trial_intend_declares_through_the_cli_and_never_writes_on_a_refusal():
    tmp = tempfile.mkdtemp(prefix="dogfood-trial-")
    try:
        path = os.path.join(tmp, "store.json")

        # A promise needs a store to watch: there is no entity id before there is
        # a session, and inventing one is what this shell does not do.
        code, out, err = _run(["--store", path, "intend", "--when-key", "layer",
                               "--when-val-ge", "6", "--about", "x",
                               "--surface", "y"])
        require_equal(code, cli.EXIT_USAGE, "intending against no store is a usage error")
        require(not out.strip(), "a usage error answers nothing on stdout")

        _run(["--store", path, "remember", "--project", "trial-project",
              "--move", "FORGE", "--log-line", "[L1] [FORGE] a <suite: 1/1 green>"])
        with open(path, "rb") as fh:
            before = fh.read()

        # A dry run validates and renders, and writes nothing.
        code, _out, err = _run(["--store", path, "intend", "--project", "trial-project",
                                "--when-kind", "attr", "--when-key", "layer",
                                "--when-val-ge", "6", "--about", "x",
                                "--surface", "y", "--dry-run"])
        require_equal(code, cli.EXIT_OK, "a dry run is not an error: %s" % err)
        require("INTEND" in err and "when:" in err, "a dry run must render the promise")
        with open(path, "rb") as fh:
            require_equal(fh.read(), before, "a dry run must write nothing")

        # A condition outside the declared reading is a usage error, and writes
        # nothing — the shell refuses a silent promise at declare time.
        for argv in (["--when-key", "no-such-key", "--when-val-ge", "6"],
                     ["--when-count-ge", "note:3"],
                     ["--when-count-ge", "attr"],
                     []):
            code, _out, _err = _run(["--store", path, "intend",
                                     "--project", "trial-project",
                                     "--about", "x", "--surface", "y"] + argv)
            require_equal(code, cli.EXIT_USAGE,
                          "an undeclarable condition must be a usage error: %s" % argv)
        with open(path, "rb") as fh:
            require_equal(fh.read(), before, "a refused declaration must not write")

        # The real thing.
        code, out, err = _run(["--store", path, "intend", "--project", "trial-project",
                               "--when-kind", "attr", "--when-key", "layer",
                               "--when-val-ge", "6", "--about", "x", "--surface", "y"])
        require_equal(code, cli.EXIT_OK, "intend must succeed: %s" % err)
        require_equal(out.strip(), "1", "intend prints the engine-assigned t on stdout")
        require("PENDING" in err, "the shell must ASK the engine whether it armed")

        # An iid is spent forever: §5 L5 names no re-arming.
        code, _out, err = _run(["--store", path, "intend", "--project", "trial-project",
                                "--iid", "1", "--when-kind", "attr",
                                "--when-key", "suite", "--about", "x",
                                "--surface", "y"])
        require_equal(code, cli.EXIT_USAGE, "a re-used iid must be refused loudly")
        require("re-arming" in err, "and the refusal must say why")

        # recall now carries the promises, and says nothing about them elsewhere.
        code, out, _err = _run(["--store", path, "recall", "nonexistenttoken"])
        require_equal(code, cli.EXIT_OK, "recall still exits 0")
        require("ABSTAIN" in out, "the recall answer itself is unchanged")
        require("promises" in out and "PENDING" in out,
                "a firing has to reach its owner: recall surfaces the promises")

        code, out, _err = _run(["--store", path, "consolidate"])
        require_equal(code, cli.EXIT_OK, "consolidate must still exit 0")
        require("prospection — the promises this store is keeping" in out,
                "the consolidated view gained its prospection section")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def trial_a_store_with_no_promises_says_nothing_about_prospection():
    """The surface costs nothing where it is not used — no replay, no section."""
    tmp = tempfile.mkdtemp(prefix="dogfood-trial-")
    try:
        path = os.path.join(tmp, "store.json")
        _run(["--store", path, "remember", "--project", "trial-project",
              "--move", "FORGE", "--log-line", "[L1] [FORGE] alone <suite: 1/1 green>"])
        state = st.load(path)
        require_equal(cli.promise_footer(state), [],
                      "no intention, no replay and no output")
        code, out, _err = _run(["--store", path, "recall", "alone"])
        require_equal(code, cli.EXIT_OK, "recall must exit 0")
        require("promises" not in out, "a store with no promises must not discuss them")
        code, out, _err = _run(["--store", path, "consolidate"])
        require("prospection — the promises this store is keeping" not in out,
                "and the consolidated view must not print an empty section")
        require("ARMED INTENTIONS" not in out,
                "nor a demotion breakdown for demotions that do not exist")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---- 6. the committed store (read-only) -------------------------------------

def trial_the_committed_stores_promises_are_kept():
    """This project's own promises, replayed. Read-only.

    Written so that it stays true as the store grows: every declared intention is
    either **pending** — with its own `intend` event regenerated byte-exact from
    the pending entry — or **fired exactly once**. There is no third state, and
    that is the whole of `dup-fire = 0` and `miss = 0` as this store can observe
    them.
    """
    path = st.default_store_path()
    if not os.path.isfile(path):
        skip("no committed dogfood store yet (%s)" % st.display_path(path))
    state = st.load(path)
    records = ledger.read_range(state, 0, state.next_t - 1)
    declared = it.intentions_of(records)
    if not declared:
        skip("the committed store has declared no intention yet")

    derived, origin, _sessions, _entities, refused = co.derive(records)
    require(refused is None, "the committed store must fold inside the derived cap")

    for store_t, payload in declared:
        it.validate_condition(payload["cond"])
        require(it.guarded(payload["fire"]),
                "every stored promise must surface a declared payload")
        require(l5.arms(payload) is not None,
                "every stored promise must be one the engine arms")

    entries = co.promises(derived, records, origin)
    require_equal(len(entries), len(declared), "every promise must be accounted for")
    iids = [e["iid"] for e in entries]
    require_equal(len(set(iids)), len(iids), "an iid is spent forever, so it is unique")

    for entry in entries:
        if entry["fired"]:
            require_equal(len(entry["fired"]), 1,
                          "iid %s fired more than once — dup-fire = 0" % entry["iid"])
            require(entry["fired"][0]["store_t"] is not None,
                    "a firing must be attributable to the write that caused it")
        else:
            require(entry["readable"] and entry["regenerated"],
                    "a pending promise's own intend event must come back "
                    "byte-exact from read(t) while it waits (README-l5 §1.3)")

    require_equal(derived.next_t - len(origin), 0,
                  "origin must cover every logical time the replay assigned")

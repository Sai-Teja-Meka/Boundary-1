"""ops/dogfood — the DOGFOOD shell adapter (BOUNDARY.md §9.1 DOGFOOD, §2.6).

Shell code is testable; it is only `core/` that must stay pure. These are the
fine-grained trials for the adapter that makes this engine the memory of its own
project (`shell/dogfood/`):

  * the remember event builder validates its schema and emits a canonical payload;
  * a remember/recall round trip survives a real state file on disk;
  * an abstention is always rendered explicitly — never empty silence;
  * a corrupted state file fails **loudly** and is never silently re-initialized;
  * the committed store, if present, still restores and still validates — at
    `[L5] [DOGFOOD]` against the two kinds its vocabulary now declares.

Every trial that writes uses a temporary directory. None of them touches the
committed store at `shell/dogfood/store/store.json` except read-only.
"""

import io
import os
import shutil
import tempfile

from _harness import require, require_equal, skip

from core.serialize import check_canonical
from core.layers import l2_recall as engine
from core.layers import l5_prospection as l5
from shell.dogfood import backfill, cli
from shell.dogfood import event as ev
from shell.dogfood import intend as it
from shell.dogfood import store as st

SUMMARY = {
    "project": "boundary-1-memory",
    "move": "DOGFOOD",
    "decisions": ["built the shell adapter", "chose a 2**24 budget"],
    "files_touched": ["shell/dogfood/cli.py"],
    "open_questions": ["does recall need a rarer cue surface?"],
    "log_line": "[L2] [DOGFOOD] first-run <suite: 0/0 green> <store: 0 events>",
}


def _summary(**overrides):
    out = {k: (list(v) if isinstance(v, list) else v) for k, v in SUMMARY.items()}
    out.update(overrides)
    return out


def _run(argv):
    """Run the CLI in-process; return `(exit_code, stdout, stderr)`."""
    out, err = io.StringIO(), io.StringIO()
    code = cli.main(argv, out=out, err=err)
    return code, out.getvalue(), err.getvalue()


# ---- 1. schema validation of the remember event builder --------------------

def trial_event_builder_emits_a_canonical_schema_conformant_payload():
    payload = ev.build_payload(_summary())
    require_equal(frozenset(payload.keys()), ev.PAYLOAD_KEYS, "payload key set is wrong")
    require_equal(payload["kind"], ev.KIND, "payload kind is wrong")
    check_canonical(payload)                       # raises NonCanonical if not (§2.4)

    # Atoms are ints and strings only (§1.2): the payload is built from strings,
    # arrays of strings, and the token bag's constant integer 1.
    require(all(isinstance(v, str) for v in payload["tok"].keys()),
            "token bag keys must be strings")
    require(all(v == 1 and isinstance(v, int) and not isinstance(v, bool)
                for v in payload["tok"].values()),
            "the token bag is a SET: every value must be the integer 1")

    # Everything written is searchable: every token of every text field is in the bag.
    for field in ev.TOKEN_SOURCES:
        value = payload[field]
        for text in ([value] if isinstance(value, str) else value):
            for token in ev.tokenize(text):
                require(token in payload["tok"], "token %r missing from the cue surface" % token)

    # ... and the cue side normalizes identically, so what was written is cue-able.
    cue = ev.cue_payload(["Layer-2", "DOGFOOD"])
    require_equal(cue, {"tok": {"layer": 1, "dogfood": 1}}, "cue normalization diverged")
    require("dogfood" in payload["tok"], "cue token absent from an event that used it")

    # `t` is engine-owned: the builder never puts one in the payload (§1.3).
    require("t" not in payload, "the builder must not assign t")


def trial_event_builder_rejects_malformed_summaries():
    bad = [
        ("missing field", {k: v for k, v in _summary().items() if k != "move"}),
        ("unknown field", _summary(extra="no")),
        ("non-string move", _summary(move=2)),
        ("empty log_line", _summary(log_line="   ")),
        ("list field as string", _summary(decisions="one decision")),
        ("non-string list item", _summary(files_touched=["a.py", 7])),
        ("empty list item", _summary(open_questions=[""])),
        ("not an object", ["project"]),
    ]
    for label, summary in bad:
        try:
            ev.build_payload(summary)
        except ev.SchemaError:
            continue
        raise AssertionError("schema accepted a malformed summary: %s" % label)

    # Empty arrays are legal — a backfilled event has no recoverable open questions.
    payload = ev.build_payload(_summary(decisions=[], files_touched=[], open_questions=[]))
    require_equal(payload["open_questions"], [], "empty arrays must be accepted")

    # `move` is deliberately NOT checked against the §9.1 move set: the log
    # carries FORGE-CORRECTION and THEORY, which that set does not list.
    for move in ("FORGE-CORRECTION", "THEORY"):
        ev.build_payload(_summary(move=move))


def trial_backfill_parses_the_log_without_inventing_anything():
    parsed = backfill.summaries(
        "[L0] [FORGE] a thing (x; y) — done; and another <suite: 3/3 green> <anchors: intact>\n"
        "\n"
        "[L2] [ASCEND] recall <suite: 98/98 green> <anchors: l1 intact, l2 born>\n")
    require_equal(len(parsed), 2, "blank lines must be skipped, real lines kept")
    first = parsed[0]
    require_equal(first["move"], "FORGE", "move token misparsed")
    require_equal(first["decisions"],
                  ["a thing (x; y) — done", "and another"],
                  "a `;` inside parentheses must not split a clause")
    require_equal(first["open_questions"], [],
                  "open questions are never recoverable from the log")
    require(first["log_line"].startswith("[L0] [FORGE]"), "log_line must be verbatim")
    require_equal(backfill.extract_paths("see core/a.py and B.md/C.md and 37/37 and x/y/"),
                  ["B.md", "C.md", "core/a.py", "x/y/"],
                  "path extraction must skip prose slashes and split slash-joined lists")
    for summary in parsed:
        ev.build_payload(summary)                  # every parsed line is schema-valid


# ---- 2. round trip through a temp state file -------------------------------

def trial_remember_recall_round_trip_through_a_temp_state_file():
    tmp = tempfile.mkdtemp(prefix="dogfood-trial-")
    try:
        path = os.path.join(tmp, "store.json")
        code, out, _err = _run(["--store", path, "remember", "--move", "DOGFOOD",
                                "--log-line", "[L2] [DOGFOOD] uniquetokenalpha one"])
        require_equal(code, cli.EXIT_OK, "first remember must succeed")
        require_equal(out.strip(), "0", "the first assigned t must be 0")
        require(os.path.isfile(path), "remember must create the state file")

        code, out, _err = _run(["--store", path, "remember", "--move", "PULSE",
                                "--log-line", "[L2] [PULSE] uniquetokenbeta two"])
        require_equal(code, cli.EXIT_OK, "second remember must succeed")
        require_equal(out.strip(), "1", "t must be strictly increasing from 0 (§1.3)")

        # The file is exactly the engine's snapshot bytes, and it restores.
        state = st.load(path)
        require_equal(state.next_t, 2, "restored store lost events")
        require_equal(state.budget_cap, st.DOGFOOD_BUDGET, "budget cap did not persist")
        with open(path, "rb") as fh:
            require_equal(fh.read(), engine.snapshot(state),
                          "the state file must be exactly snapshot(state) (§7.1)")

        # Recall survives the disk round trip and answers the right event.
        answer = engine.recall(state, ev.cue_payload(["uniquetokenbeta"]))
        require_equal(answer["status"], "answer", "recall must answer a unique cue")
        require_equal(answer["value"]["t"], 1, "recall answered the wrong event")
        code, out, _err = _run(["--store", path, "recall", "uniquetokenalpha"])
        require_equal(code, cli.EXIT_OK, "recall must exit 0")
        require("MATCH" in out and "t=0" in out, "CLI recall lost the match")

        # ... and status reports the store, not a guess about it.
        code, out, _err = _run(["--store", path, "status"])
        require_equal(code, cli.EXIT_OK, "status must exit 0")
        require("events       2" in out, "status lost the event count")
        require(st.state_checksum(state) in out, "status must print the state checksum")
        require("%d" % state.occupancy in out and "%d" % state.budget_cap in out,
                "status must print budget occupancy as used/total")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---- 3. abstention output shape --------------------------------------------

def trial_abstention_is_always_explicit_never_empty_silence():
    tmp = tempfile.mkdtemp(prefix="dogfood-trial-")
    try:
        path = os.path.join(tmp, "store.json")
        for move, line in (("FORGE", "[L0] [FORGE] shared alpha"),
                           ("PULSE", "[L0] [PULSE] shared beta")):
            _run(["--store", path, "remember", "--move", move, "--log-line", line])

        # (a) a cue no event carries at all
        code, out, _err = _run(["--store", path, "recall", "nonexistenttoken"])
        require_equal(code, cli.EXIT_OK, "an abstention is a correct answer (§3.0), exit 0")
        require(out.strip(), "an abstention must never be empty silence")
        require("ABSTAIN" in out, "the abstention must be labelled")
        require("MATCH" not in out, "an abstention must never render as a match")
        require("nonexistenttoken" in out, "the abstention must name the absent token")
        require("df:" in out, "the abstention must show its per-token evidence")

        # (b) a cue several events carry: ambiguity, not a coin flip
        code, out, _err = _run(["--store", path, "recall", "shared"])
        require_equal(code, cli.EXIT_OK, "an ambiguous cue still exits 0")
        require("ABSTAIN" in out and "ambiguous" in out, "ambiguity must be named as such")
        require("MATCH" not in out, "an ambiguous cue must not be answered")
        require("context, not an answer" in out,
                "candidates shown under an abstention must be labelled as context")
        require("t=0" in out and "t=1" in out, "both candidates must be shown")

        # (c) a cue that normalizes to nothing
        code, out, _err = _run(["--store", path, "recall", "a"])
        require_equal(code, cli.EXIT_OK, "an unusable cue still exits 0")
        require("ABSTAIN" in out, "an unusable cue must abstain, not crash (§7.3)")

        # The engine itself abstained in every case — the shell added no answer.
        state = st.load(path)
        for tokens in (["nonexistenttoken"], ["shared"], ["a"]):
            answer = engine.recall(state, ev.cue_payload(tokens))
            require_equal(answer["status"], "abstain", "engine should have abstained")
            require(answer["value"] is None, "an abstention carries no value (§7.2)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---- 4. corrupted state file -> loud failure -------------------------------

def trial_corrupted_state_file_fails_loudly_and_is_never_re_initialized():
    tmp = tempfile.mkdtemp(prefix="dogfood-trial-")
    try:
        path = os.path.join(tmp, "store.json")
        _run(["--store", path, "remember", "--move", "FORGE",
              "--log-line", "[L0] [FORGE] a line worth keeping"])
        with open(path, "rb") as fh:
            good = fh.read()

        def corrupt(data, label):
            with open(path, "wb") as fh:
                fh.write(data)
            try:
                st.load(path)
            except st.StoreCorrupt:
                pass
            else:
                raise AssertionError("a corrupt store loaded silently: %s" % label)

            code, out, err = _run(["--store", path, "status"])
            require_equal(code, cli.EXIT_CORRUPT, "corruption must exit 2: %s" % label)
            require("FATAL" in err, "the failure must be loud: %s" % label)
            require(path in err, "the failure must name the file: %s" % label)
            require(not out.strip(), "a corrupt store must answer nothing: %s" % label)
            with open(path, "rb") as fh:
                require_equal(fh.read(), data,
                              "the CLI must not rewrite a corrupt store: %s" % label)

        # (a) one flipped bit in the body — the L1 checksum law catches it
        middle = len(good) // 2
        corrupt(good[:middle] + bytes([good[middle] ^ 0x01]) + good[middle + 1:], "flipped bit")
        # (b) truncation
        corrupt(good[:len(good) // 2], "truncated")
        # (c) not JSON at all
        corrupt(b"hand-edited by a person who meant well", "not canonical JSON")
        # (d) a well-formed snapshot whose checksum was not recomputed
        corrupt(good.replace(b'"kind":"session_summary"', b'"kind":"session_summarz"'),
                "edited payload")

        # A refusal to proceed is not a refusal to recover: the good bytes still load.
        with open(path, "wb") as fh:
            fh.write(good)
        require_equal(st.load(path).next_t, 1, "the good store must still restore")

        # And a *missing* store is not a corrupt one: it is not an error to read.
        os.remove(path)
        code, _out, err = _run(["--store", path, "status"])
        require_equal(code, cli.EXIT_USAGE, "a missing store is a usage error, not corruption")
        require("FATAL" not in err, "a missing store must not be reported as corruption")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---- 5. the committed store (read-only) ------------------------------------

def trial_committed_store_restores_and_validates():
    """The committed store restores, and every event in it is one of the two the
    store's vocabulary declares.

    `[L5] [DOGFOOD]` widened that vocabulary: the ledger now also carries
    **intentions**, in the engine's own `intend` form (`shell/dogfood/intend.py`).
    The check is not relaxed by that — it is dispatched, and each kind is
    validated against its own schema, with the kind set itself asserted closed so
    a third kind cannot appear here unremarked.
    """
    path = st.default_store_path()
    if not os.path.isfile(path):
        skip("no committed dogfood store yet (%s)" % st.display_path(path))
    state = st.load(path)                          # raises StoreCorrupt if it ever rots
    require(state.next_t > 0, "the committed store is empty")
    require_equal(state.layer_cap, engine.LAYER, "the committed store is not a Layer-2 store")
    require(state.occupancy <= state.budget_cap, "the committed store breaches its cap (§4.1)")
    for record in engine.read_range(state, 0, state.next_t - 1):
        payload = record["payload"]
        kind = payload["kind"]
        require(kind in (ev.KIND, it.INTENTION_KIND),
                "a stored event is neither a session summary nor an intention: %r"
                % (kind,))
        if kind == ev.KIND:
            ev.validate_summary(ev.summary_of_payload(payload))
            continue
        it.validate_condition(payload["cond"])
        require(it.guarded(payload["fire"]),
                "a stored intention surfaces a payload outside the declared reading")
        require(l5.arms(payload) is not None,
                "a stored intention is one the engine would not arm — it would sit "
                "in the ledger forever as an ordinary event (README-l5 §1.2)")

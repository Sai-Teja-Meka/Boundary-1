"""ops/dogfood — the Layer-4 derived view (`shell/dogfood/consolidate.py`).

`[L4] [DOGFOOD]`. The `consolidate` surface folds the store's session summaries
through the frozen Layer-4 engine and reads the result back through the ordinary
query interface (§7.1). These trials hold it to four things:

  * the **declared reading** emits assertions the engine can invert, and asserts
    only facts the summary already carries — no invention;
  * the derived view answers `current` / `asof` / `profile` / `count` through
    `query` alone, and `asof` honours supersession rather than reading the
    present backwards;
  * under a reduced budget the two channels **separate**: a demoted episode is
    still answerable by `read(t)` and is no longer reachable by `recall`, which
    is `README-l4 §4`'s non-capability turned into a number;
  * `consolidate` is **read-only** — nothing derived is written back, and the
    store's bytes are identical before and after.

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
from core.layers import l4_consolidation as l4
from shell.dogfood import cli, consolidate as co
from shell.dogfood import event as ev
from shell.dogfood import store as st


def _summary(move, line, decisions=(), files=(), questions=()):
    return {"project": "trial-project",
            "move": move,
            "decisions": list(decisions) or ["a decision"],
            "files_touched": list(files),
            "open_questions": list(questions),
            "log_line": line}


# A three-session store whose facts genuinely supersede: the layer climbs 1 -> 2,
# and the suite count changes under it.
STREAM = [
    _summary("FORGE", "[L1] [FORGE] retention <suite: 72/72 green> <anchors: born>",
             questions=["is the cue surface wide enough?"]),
    _summary("ASCEND", "[L2] [ASCEND] recall <suite: 98/98 green> <anchors: l1 intact, l2 born>"),
    _summary("DOGFOOD", "[L2] [DOGFOOD] first-run <suite: 105/105 green>",
             questions=["does demotion cost the cue channel?", "and by how much?"]),
]


def _records():
    """`[{payload, t}]` as `read_range` would hand them to `consolidate`."""
    return [{"payload": ev.build_payload(s), "t": i} for i, s in enumerate(STREAM)]


def _run(argv):
    out, err = io.StringIO(), io.StringIO()
    code = cli.main(argv, out=out, err=err)
    return code, out.getvalue(), err.getvalue()


# ---- 1. the declared reading ------------------------------------------------

def trial_the_declared_reading_emits_assertions_the_engine_can_invert():
    """Every derived assertion round-trips through the FROZEN facet map.

    The shell declares a reading of a session; the engine declares a reading of
    its grammars. This asserts the two agree — that what the shell emits is
    exactly what `core.l4_consolidation.facet` reads and `rebuild` puts back,
    byte for byte. Without it the assertions would still fold, but the atlas
    would mark their key non-invertible and `read(t)` would abstain on every
    demoted event instead of regenerating it (`README-l4 §1`).
    """
    payload = ev.build_payload(STREAM[0])
    stream = co.session_stream(payload, 7)

    episode = stream[0]
    require_equal(episode["kind"], ev.KIND, "the first derived event is the episode")
    require_equal(episode["entity"], 7, "the episode must carry its project entity")
    require(l4.facet(episode) is None,
            "a session summary is IRREDUCIBLE to the frozen facet map — that is "
            "the premise the demotion measurement rests on")
    from core.layers.l3_forgetting import handle_atom
    require_equal(handle_atom(episode), "entity=i7",
                  "the episode must have a handle atom, or Layer-4 recall cannot reach it")

    for assertion in stream[1:]:
        require_equal(sorted(assertion), ["entity", "key", "kind", "val"],
                      "an assertion carries exactly the four fields `attr` inverts")
        fact = l4.facet(assertion)
        require(fact is not None, "the engine must read the shell's assertion as a fact")
        entity, key, value = fact
        require_equal(entity, 7, "the assertion names the wrong entity")
        require(l4.invertible(assertion, "attr", entity, key, value),
                "assertion %r does not round-trip through rebuild()" % (key,))
        require_equal(encode(l4.rebuild("attr", entity, key, value)), encode(assertion),
                      "rebuild must return the identical payload, byte for byte (§2.4)")


def trial_the_reading_asserts_only_what_the_summary_already_carries():
    """No invention: every asserted value is present in, or counted from, the summary."""
    payload = ev.build_payload(
        _summary("PULSE", "[L3] [PULSE] tidy <suite: 9/9 green> <anchors: intact>",
                 decisions=["a", "b"], files=["x.py"], questions=["why?"]))
    facts = dict(co.facts_of(payload))
    require_equal(facts["layer"], 3, "layer is read off the `[L<n>]` tag")
    require_equal(facts["move"], "PULSE", "move is the summary's own field")
    require_equal(facts["suite"], "9/9 green", "suite is the `<suite: …>` tag body")
    require_equal(facts["anchors"], "intact", "anchors is the `<anchors: …>` tag body")
    require_equal(facts["decisions"], 2, "counts are counts of what is there")
    require_equal(facts["files_touched"], 1, "counts are counts of what is there")
    require_equal(facts["open_questions"], 1, "counts are counts of what is there")

    # A line that states no layer, no suite and no anchors asserts none of them.
    bare = ev.build_payload(_summary("THEORY", "a line with no tags at all"))
    keys = [k for k, _v in co.facts_of(bare)]
    for absent in ("layer", "suite", "anchors"):
        require(absent not in keys,
                "%r must not be invented for a line that does not state it" % absent)
    require("move" in keys, "the move is always known")

    # And the store's own drift is visible rather than papered over: a truncated
    # log line simply carries fewer facts.
    require_equal(co.tagged("no tags here", "suite"), None, "a missing tag is None")
    require_equal(co.layer_of("[LX] not a layer"), None, "a malformed layer tag is None")


# ---- 2. the derived view, through query() only ------------------------------

def trial_the_derived_view_answers_the_battery_through_the_query_interface():
    records = _records()
    state, origin, sessions, entities, refused = co.derive(records)
    require(refused is None, "the default cap must admit the whole stream")
    require_equal(entities, {"trial-project": 1}, "entity ids start at 1, first seen first")
    require_equal(len(sessions), len(records), "every session must be replayed")

    entity = 1
    # Q1 — current value.
    require_equal(co.current_fact(state, entity, "layer", origin), (2, 2),
                  "current(layer) must be the last assertion, at its own store t")
    require_equal(co.current_fact(state, entity, "move", origin), ("DOGFOOD", 2),
                  "current(move) must be the last session's move")
    require(co.current_fact(state, entity, "no-such-key", origin) is None,
            "a key never asserted must ABSTAIN, never be guessed (§7.3)")

    # Q3 — the per-project fold, and the global counters.
    profile = co.ask(state, {"op": "profile", "entity": entity})
    require_equal(profile["status"], "answer", "the profile fold must be exact here")
    require_equal(profile["value"][ev.KIND], 3,
                  "the profile must count the session summaries as irreducible events")
    count = co.ask(state, {"op": "count", "kind": co.ASSERTION_KIND})
    require_equal(count["value"], profile["value"][co.ASSERTION_KIND],
                  "one project: the global counter and the fold must agree")

    # The history is the sequence of CHANGES, and it is read out of provenance.
    changes = co.collapse(co.history(state, entity, "layer", origin, state.next_t - 1))
    require_equal([(t, v) for t, v, _n in changes], [(0, 1), (1, 2)],
                  "the layer history must be 1 at store t=0, then 2 at store t=1")
    require_equal(changes[-1][2], 1,
                  "the third session restates layer 2 — a restatement is counted, not dropped")


def trial_asof_honours_supersession_rather_than_reading_the_present_backwards():
    """The Graphiti fix (`README-l4 §2.2`), on this project's own history."""
    records = _records()
    state, origin, sessions, _entities, _refused = co.derive(records)
    entity = 1

    first_end = sessions[0][2]
    last_end = sessions[-1][2]

    early = co.ask(state, {"op": "asof", "entity": entity, "key": "layer", "t": first_end})
    require_equal(early["value"], 1,
                  "as-of at the first session must return 1, not the current 2")
    late = co.ask(state, {"op": "asof", "entity": entity, "key": "layer", "t": last_end})
    require_equal(late["value"], 2, "as-of at the end must return the value in force")

    # Before the pair's first assertion there is no value in force, and the
    # engine abstains rather than reading the earliest one backwards.
    before = co.ask(state, {"op": "asof", "entity": entity, "key": "layer", "t": 0})
    require_equal(before["status"], "abstain",
                  "as-of before the first assertion must ABSTAIN (§3.0 pays 100 for it)")

    # An as-of answer cites the assertion that carries it, and that assertion is
    # the one the shell derived from that session — misattribution, checked.
    support = late["provenance"]["support"]
    require_equal(len(support), 1, "an as-of answer cites exactly one assertion")
    require_equal(origin[support[0]], 2, "the cited assertion belongs to the wrong session")


# ---- 3. the two channels separate under pressure ---------------------------

def trial_a_demoted_episode_keeps_its_content_and_loses_its_cue():
    """The mandatory measurement, at trial scale (`README-l4 §4`, in numbers).

    Under a cap the derived stream does not fit in, Layer 4 releases episodes a
    chain regenerates. This asserts what that costs and what it does not:

      * demotions actually happen, and `read(t)` still answers for every demoted
        event — the content channel is intact;
      * the engine's own provenance separates them: `kind == "recall"` for an
        episode still held, `"derive"` for one regenerated;
      * a cue that reaches an assertion while it is an episode ABSTAINS once it
        is demoted — the associative channel narrows as the budget tightens;
      * **a session summary is never demoted.** It is irreducible to the frozen
        facet map, so pressure FORGETS it. Demotion and loss are different
        ledgers and the store must not blur them.
    """
    records = _records()
    roomy, _o, sessions, _e, _r = co.derive(records)
    require_equal(roomy.demotions, 0, "the default cap must apply no pressure at all")

    probe = {"kind": co.ASSERTION_KIND, "entity": 1, "key": "suite", "val": "98/98 green"}
    found = co.ask(roomy, {"op": "recall", "cue": probe})
    require_equal(found["status"], "answer",
                  "a unique assertion must be recallable while it is an episode")
    demoted_t = found["value"]["t"]

    tight = roomy.occupancy // 3
    squeezed, _o2, sessions2, _e2, _r2 = co.derive(records, budget_cap=tight)
    require(squeezed.demotions > 0, "a third of the budget must force demotion")
    require(squeezed.occupancy <= tight, "the budget law must hold at all times (§4.1)")

    reread = co.ask(squeezed, {"op": "read", "t": demoted_t})
    require_equal(reread["status"], "answer",
                  "a demoted event must still be answerable by read(t)")
    require_equal(reread["provenance"]["kind"], "derive",
                  "a demoted event is REGENERATED, and its provenance says so")
    require_equal(encode(reread["value"]["payload"]), encode(probe),
                  "regeneration must be byte-exact, or it is not consolidation")

    gone = co.ask(squeezed, {"op": "recall", "cue": probe})
    require_equal(gone["status"], "abstain",
                  "a demoted episode has no posting, so the cue must ABSTAIN — this "
                  "is the price README-l4 §4 states in prose")

    counts = co.channels(squeezed)
    require(counts["derived"] > 0, "the channel census must see the demoted events")
    require_equal(counts["held"] + counts["derived"] + counts["gone"], squeezed.next_t,
                  "the census must close over the whole derived stream")

    summary_ts = [s[1] for s in sessions2]
    summaries = co.channels(squeezed, summary_ts)
    require_equal(summaries["derived"], 0,
                  "a session summary can NEVER be demoted: it is irreducible, so "
                  "pressure forgets it instead — measured, not assumed")
    require_equal(summaries["held"] + summaries["gone"], len(summary_ts),
                  "every session summary is either still an episode or gone")


# ---- 4. the CLI: read-only, and never silent -------------------------------

def trial_consolidate_reports_through_the_cli_and_writes_nothing():
    tmp = tempfile.mkdtemp(prefix="dogfood-trial-")
    try:
        path = os.path.join(tmp, "store.json")
        for summary in STREAM:
            code, _out, err = _run(["--store", path, "remember",
                                    "--project", summary["project"],
                                    "--move", summary["move"],
                                    "--log-line", summary["log_line"]])
            require_equal(code, cli.EXIT_OK, "remember failed: %s" % err)
        with open(path, "rb") as fh:
            before = fh.read()

        code, out, err = _run(["--store", path, "consolidate"])
        require_equal(code, cli.EXIT_OK, "consolidate must exit 0: %s" % err)
        for section in ("consolidated view", "per-project summary",
                        "decision history", "open questions", "what the budget did"):
            require(section in out, "the report lost its %r section" % section)
        require("nothing written back to the store" in out,
                "the report must say that the derivation is not persisted")

        with open(path, "rb") as fh:
            require_equal(fh.read(), before,
                          "consolidate must be READ-ONLY on the store")

        # A cue probe answers or abstains, and says which — never silence (§7.3).
        code, out, _err = _run(["--store", path, "consolidate",
                                "--cue", "nonexistenttokenhere"])
        require_equal(code, cli.EXIT_OK, "a probe that misses is still exit 0")
        require("ABSTAIN" in out, "a missing cue must be reported as an abstention")

        # A reduced budget is honoured and reported.
        code, out, _err = _run(["--store", path, "consolidate", "--budget", "400"])
        require_equal(code, cli.EXIT_OK, "a pressured replay still exits 0")
        require("demotions" in out, "the pressure section must be present")

        # A budget that is not a budget is a usage error, and writes nothing.
        code, _out, err = _run(["--store", path, "consolidate", "--budget", "0"])
        require_equal(code, cli.EXIT_USAGE, "a non-positive cap is a usage error (§4.1)")
        with open(path, "rb") as fh:
            require_equal(fh.read(), before, "a failed consolidate must not write")

        # An empty store is a usage error, not an empty report.
        empty = os.path.join(tmp, "missing.json")
        code, out, _err = _run(["--store", empty, "consolidate"])
        require_equal(code, cli.EXIT_USAGE, "a missing store cannot be consolidated")
        require(not out.strip(), "a missing store must answer nothing")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---- 5. the committed store (read-only) ------------------------------------

def trial_the_committed_store_consolidates():
    """This project's own memory folds, and the fold is exact where it claims to be."""
    path = st.default_store_path()
    if not os.path.isfile(path):
        skip("no committed dogfood store yet (%s)" % st.display_path(path))
    state = st.load(path)
    records = ledger.read_range(state, 0, state.next_t - 1)
    derived, origin, sessions, entities, refused = co.derive(records)
    require(refused is None, "the committed store must fold inside the derived cap")
    require_equal(len(sessions), len(records), "a session was dropped from the fold")
    require_equal(len(origin), derived.next_t, "the origin table must cover the stream")

    entity = entities["boundary-1-memory"]
    layer = co.current_fact(derived, entity, "layer", origin)
    require(layer is not None, "the project's claimed layer must be derivable")
    require(layer[0] >= 4, "the store's own history claims Layer 4 or later")
    require_equal(layer[1], records[-1]["t"],
                  "the layer in force must be attributed to the latest session that stated it")

    profile = co.ask(derived, {"op": "profile", "entity": entity})
    require_equal(profile["status"], "answer", "the project fold must be exact")
    require_equal(profile["value"][ev.KIND], len(records),
                  "every stored session must be counted against the project")

    census = co.channels(derived)
    require_equal(census["gone"], 0, "nothing may be lost at the unpressured cap")
    require_equal(census["derived"], 0, "nothing may be demoted at the unpressured cap")

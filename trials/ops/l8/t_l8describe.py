"""ops/l8 — `corpora/l8describe`: the artifact's own properties, machine-checked.

`BOUNDARY-HIGH.md §3` says a Layer-8 artifact is a TRIPLE — a frozen event
stream, a frozen query set with its declared class table, and a frozen derivation
procedure — and gives the triple the same three obligations the byte-match law
gives an ordinary corpus: **freeze**, **hash**, **reproduce**. This file is where
all three are checked, together with `§3`'s four constraints on the procedure and
the field-reader bench `§3`'s fourth constraint demands.

Nothing here applies a gate. No `GATE_*` or `CEILING_*` constant exists in this
directory: `R2`'s standing step puts the ruling between Stage A and any
authority, and the registry in `laws/t_rulings.py` is where a threshold acquires
one. What these trials pin is the ARTIFACT.
"""

import ast
import hashlib
import os

from _harness import PROJECT_ROOT, require, require_equal

import _l8derive as D
import _l8tasks as T
from corpora.l8describe import generator as g


# The `sha256` of the DERIVED KEY's canonical bytes over the artifact's declared
# substrate configuration — `§3`'s hash obligation. It is recomputed on every run
# and compared, which is the whole point: the key is a PROCEDURE and not a table,
# so what is recorded is the hash of what the procedure produces, not the answers.
DERIVED_KEY_SHA256 = \
    "3943c7130cd6aef6114d2ea8bef3cf906d25ff50d7b7176fe1aa98e5da4708fb"

# Measured, and pinned so a drift is red rather than disappointing. The bench
# below is a bench of NAMED single-field readers, in the `l7compose` six-labeller
# form; `FOLD_ONLY` is the remainder — the determined questions no member of it
# reaches, which is what `§3`'s fourth constraint asks the class to contain.
DETERMINED = 38
BENCH_REACHES = 9
FOLD_ONLY = 29


# --- freeze ------------------------------------------------------------------

def trial_the_stream_and_class_table_are_byte_matched_and_ship_together():
    """`§8.3` for the stream; `§3`'s freeze obligation for the whole object.

    The three members ship in ONE canonical JSON object for `corpora/l6batteryb`'s
    reason carried forward by the SPEC: the guarantees are a JOINT property, and
    three separately byte-matched files could be paired across generations while
    every individual check stayed green.
    """
    with open(g.FROZEN_PATH, "rb") as fh:
        frozen = fh.read()
    require_equal(frozen, g.frozen_bytes(),
                  "corpora/l8describe does not reproduce byte-for-byte (§8.3)")
    artifact = g.load()
    for member in ("stream", "queries", "classes", "declared", "counts"):
        require(member in artifact,
                "the artifact lost its %r member — the three members of "
                "BOUNDARY-HIGH.md §3's triple ship in one object" % (member,))
    require_equal(len(artifact["stream"]), artifact["stream_events"],
                  "declared stream length")
    require(g.SEED < 9_000_000,
            "the seed is inside §8.5's reserved holdout range and a holdout "
            "output may never be frozen into the repository")


def trial_every_query_declares_its_class_and_the_classes_are_the_declared_four():
    """`R8` clause 3: the denominator is the artifact's declared class."""
    artifact = g.load()
    declared = set(artifact["classes"])
    require_equal(declared, {"KR", "KL", "KF", "KU"}, "the declared class set")
    seen = {}
    for entry in artifact["queries"]:
        require(entry["class"] in declared,
                "query %d carries an undeclared class %r"
                % (entry["qid"], entry["class"]))
        require(isinstance(entry["answerable"], bool), "answerable is a flag")
        seen[entry["class"]] = seen.get(entry["class"], 0) + 1
    require_equal(seen, artifact["counts"]["by_class"], "per-class counts")
    require_equal([e["qid"] for e in artifact["queries"]],
                  list(range(len(artifact["queries"]))), "qids are 0..n-1")
    core = artifact["counts"]["answerable"]
    hard = seen["KF"]
    require(hard * 18 > core,
            "BOUNDARY-HIGH.md §5.4: the hard class must be a large enough share "
            "of the answerable core that the escape §3.0 offers is priced out "
            "before the gate binds — %d of %d is at or under 1/18"
            % (hard, core))


# --- reproduce ---------------------------------------------------------------

def trial_the_derivation_reproduces_its_key_byte_for_byte():
    """`§3`'s reproduce obligation, stated as `§8.3`'s ANALOGUE and never as `§8.3`.

    `§8.3` is about a generator; this is about a procedure over an engine. What
    makes it legitimate is `§2.3`: the engine's trace and final state are
    byte-reproducible from the frozen stream, so the procedure's output is still a
    deterministic function of frozen bytes.
    """
    fixture = T.stage_a()
    again = D.derive_all(fixture["artifact"], fixture["body"],
                         fixture["trace"], strict=True)
    require_equal(D.key_bytes(again), fixture["key_bytes"],
                  "the derivation does not reproduce its own key")
    require_equal(hashlib.sha256(fixture["key_bytes"]).hexdigest(),
                  DERIVED_KEY_SHA256,
                  "the derived key's recorded sha256 (BOUNDARY-HIGH.md §3's "
                  "hash obligation) — a drift in the stream, the engine or the "
                  "reading moves it, and that is what it is for")


def trial_the_derivation_is_engine_free_and_reads_no_answer():
    """Two of `§3`'s four constraints, checked against the procedure's SOURCE.

    `R8` clause 1's class-E form: a witness that may not read the answer key is
    checked against its own source, *because the generator is part of the answer
    key and not part of the substrate*. Here the same check runs on the harness's
    own derivation — it may not import the engine, and it may not read an
    `Answer`, because a key derived from what the engine says is `R8` clause 3's
    self-reported denominator with the roles swapped and every score a tautology.
    """
    path = os.path.join(PROJECT_ROOT, "trials", "_l8derive.py")
    with open(path, "r", encoding="utf-8") as fh:
        source = fh.read()
    tree = ast.parse(source)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    for name in sorted(imported):
        require(not name.startswith(("core", "adapters", "corpora.l8describe")),
                "_l8derive.py imports %r — BOUNDARY-HIGH.md §3: the procedure "
                "may not import the engine, and the artifact's generator is "
                "part of the answer key and not part of the substrate" % (name,))
    for forbidden in ('"status"', "'status'", '"provenance"', "'provenance'"):
        require(forbidden not in source,
                "_l8derive.py reads a §7.2 Answer field (%s). It reads the "
                "snapshot's canonical bytes and the frozen stream, and nothing "
                "the engine says about either" % (forbidden,))


def trial_one_reading_two_implementations_agree_event_by_event():
    """The `ops/l4`–`ops/l7` discipline: the reading is checked, not assumed.

    The derivation's reachable set is read off the snapshot's canonical bytes; the
    engine's own `read(t)` verb answers from its state. They are two
    implementations of one claim — *which events survive* — and a divergence moves
    an ANSWER and not merely an availability, which is why it is a trial.
    """
    fixture = T.stage_a()
    engine, state = fixture["engine"], fixture["state"]
    derived = D.reachable_payloads(fixture["body"], fixture["artifact"]["stream"])
    disagreements = []
    for t in range(state.next_t):
        answers = engine.read(state, t) is not None
        if answers != (t in derived):
            disagreements.append(t)
    require_equal(disagreements, [],
                  "the derivation's reachable set and the engine's own read(t) "
                  "disagree at %d logical times" % (len(disagreements),))
    # And the weight reading, copied rather than imported, is the engine's own.
    from core.layers.l3_forgetting import grammar_weight as engine_weight
    for payload in fixture["artifact"]["stream"]:
        require_equal(D.grammar_weight(payload), engine_weight(payload),
                      "the derivation's grammar_weight diverges from the "
                      "engine's for %r" % (payload,))


# --- `§3`'s fourth constraint: questions no field carries ---------------------

def trial_the_field_reader_bench_reaches_only_a_minority_of_the_class():
    """THE SIXTH SUBSTRATE KILL, MEASURED — and it lands on a sub-class.

    `BOUNDARY-HIGH.md §3` predicted it in advance: *a question forced to come from
    a fold may also be trivially answerable from a field.* Measured against a
    bench of eight NAMED single-field readers, in the shape `l7compose`'s bench of
    six labellers took: the bench reaches 9 of the 38 determined questions and 29
    are fold-only.

    **Four of the nine are the artifact's own declared controls** and the other
    five are not — and the five are the finding, because each is field-answerable
    only for a reason that is a property of the ENGINE and not of these bytes
    (`reachable(attr) == counts["attr"]` exactly because this engine at this cap
    lost no assertion; `lost_kind("note") == forgetting.count` exactly because
    every loss was a note). An artifact cannot declare that, which is
    `ATTAINABILITY.md §5`'s finding stated as a trial.
    """
    fixture = T.stage_a()
    artifact, body, key = fixture["artifact"], fixture["body"], fixture["key_strict"]
    bench = T.field_reader_bench(body)
    determined = [e for e in artifact["queries"] if key[e["qid"]][0] == "value"]
    require_equal(len(determined), DETERMINED, "determined questions")
    reached = set()
    for entry in determined:
        for reader in bench.values():
            try:
                got = reader(entry["q"])
            except Exception:
                got = None
            if got is not None and got == key[entry["qid"]][1]:
                reached.add(entry["qid"])
                break
    require_equal(len(reached), BENCH_REACHES,
                  "the field-reader bench's reach over the determined class")
    require_equal(len(determined) - len(reached), FOLD_ONLY,
                  "the fold-only remainder — what §3's fourth constraint asks "
                  "the class to contain")
    require(FOLD_ONLY * 2 > DETERMINED,
            "a class whose determined half is mostly field-answerable certifies "
            "the engine's layout and measures nothing (BOUNDARY-HIGH.md §3)")
    declared = {e["qid"] for e in artifact["queries"] if e["field_shallow"]}
    require(declared <= reached,
            "a query the artifact DECLARED field-shallow is not reached by the "
            "bench — a bench that never fires is not evidence")


def trial_the_forced_class_is_non_empty_and_so_is_the_determined_one():
    """The forcing region, exhibited: both sides of the `(count, mass)` system.

    `WEIGHTS` has three members against two equations, so *"how many of the events
    you lost carried weight w?"* has a unique non-negative composition for some
    `(count, mass)` and a set of them for others. Both must occur or the class
    measures one thing twice.
    """
    fixture = T.stage_a()
    key = fixture["key_strict"]
    artifact = fixture["artifact"]
    forced = [e["qid"] for e in artifact["queries"]
              if e["class"] == "KF" and key[e["qid"]][0] == "undetermined"]
    fixed = [e["qid"] for e in artifact["queries"]
             if e["class"] == "KF" and key[e["qid"]][0] == "value"]
    require(forced, "no KF question is underdetermined — the forced class is "
                    "empty and groundedness measures nothing")
    require(fixed, "no KF question is determined — the class is uniformly "
                   "unanswerable and an honest engine's abstention there is "
                   "§7.3's floor rather than a capability")
    require_equal(len(forced) + len(fixed), artifact["counts"]["by_class"]["KF"],
                  "every KF question is one or the other")


def trial_every_unanswerable_probe_is_unanswerable_for_every_engine():
    """`KU` is a property of the frozen bytes and never of an engine's losses.

    The artifact declines the sharper probe — *what was the content of the event
    at a lost `t`?* — precisely because WHICH `t` an engine lost is not a fact the
    artifact owns. `KF` carries the pigeonhole instead.
    """
    fixture = T.stage_a()
    artifact, key = fixture["artifact"], fixture["key_strict"]
    for entry in artifact["queries"]:
        if entry["class"] == "KU":
            require_equal(key[entry["qid"]], D.UNANSWERABLE,
                          "KU query %d is not unanswerable" % (entry["qid"],))
            require(not entry["answerable"], "KU declares itself unanswerable")
        else:
            require(entry["answerable"],
                    "query %d is outside KU and declares itself unanswerable"
                    % (entry["qid"],))


def trial_the_derivation_is_adapter_generic_on_two_engines():
    """`§3`'s adapter-generic obligation, proved on TWO engines and not argued.

    *The procedure must derive ground truth for ANY engine the generic interface
    admits.* The current `layer_cap = 7` engine and `make_engine(4)` — a capped
    one — both produce a key the procedure derives without a branch of its own,
    and the `one reading, two implementations` check holds against the capped
    engine's own `read(t)` as it does against the full one's.

    **AND THE TWO KEYS ARE IDENTICAL, which this trial's first draft asserted
    they would not be.** The fixture was wrong and the engines are right: this
    stream carries no `intend` payload and no compound, so prospection and the
    lineage ledger are inert on it and a cap-4 state and a cap-7 state over these
    bytes ARE the same state — `l5_prospection.L5State` subclasses `L4State` and
    `l7_generation` adds one ledger that stays empty. Asserting a difference
    would have been asserting a property of the ladder's plumbing and calling it
    a property of the derivation.

    What the claim actually needs is that the key is a function of the STATE and
    not of the stream, and that is asserted where it can be: at a DIFFERENT CAP
    the same engine loses different events and the key MOVES. Two engines, one
    reading; two states, two keys.
    """
    fixture = T.stage_a()
    engine, artifact = fixture["engine"], fixture["artifact"]
    state4, trace4, _report = T.replay(engine, artifact, layer_cap=4)
    body4 = D.body_of(engine.snapshot(state4))
    key4 = D.derive_all(artifact, body4, trace4, strict=True)
    require_equal(len(key4), len(fixture["key_strict"]),
                  "the capped engine's key covers the same class")
    require_equal(D.key_bytes(key4), fixture["key_bytes"],
                  "the cap-4 and cap-7 keys differ on a stream carrying no "
                  "intention and no compound — then this trial's recorded "
                  "finding about the two states being one state is stale")
    for _qid, verdict in key4.items():
        require(verdict[0] in ("value", "undetermined", "unanswerable"),
                "verdict %r outside the declared three" % (verdict,))
    reach4 = D.reachable_payloads(body4, artifact["stream"])
    disagreements = [t for t in range(state4.next_t)
                     if (engine.read(state4, t) is not None) != (t in reach4)]
    require_equal(disagreements, [],
                  "one reading, two implementations — on the capped engine too")

    # The key is a function of the STATE: a different cap, a different key.
    looser = artifact["declared"]["raw_cells"] // 2
    state2, trace2, _r2 = T.replay(engine, artifact, budget_cap=looser)
    body2 = D.body_of(engine.snapshot(state2))
    key2 = D.derive_all(artifact, body2, trace2, strict=True)
    require(D.key_bytes(key2) != fixture["key_bytes"],
            "the derivation returns the same key for two different states — it "
            "is reading the stream and calling it a self-description")
    reach2 = D.reachable_payloads(body2, artifact["stream"])
    require(len(reach2) > len(D.reachable_payloads(fixture["body"],
                                                   artifact["stream"])),
            "a looser cap did not leave more reachable — the substrate is not "
            "responding to the budget law and the forced class is an accident")


def trial_the_declared_substrate_configuration_is_what_the_engine_meets():
    """The cap is part of what the artifact freezes, and `B` holds under it."""
    fixture = T.stage_a()
    artifact, report = fixture["artifact"], fixture["report"]
    declared = artifact["declared"]
    require_equal(declared["budget_cap"],
                  declared["raw_cells"] // declared["cap_divisor"],
                  "the declared cap is the declared ratio of the raw footprint")
    require_equal(report["budget_cap"], declared["budget_cap"], "the cap met")
    require_equal(report["breaches"], 0,
                  "§4.1: occupancy exceeded the cap — B is not 1000")
    require_equal(report["refused"], 0,
                  "a refusal means the ground truth's own denominator moved; "
                  "the declared cap is chosen so none occurs")
    require(report["occupancy"] <= declared["budget_cap"], "final occupancy")
    body = fixture["body"]
    require_equal(len(body["damaged"]), 0,
                  "the engine shed a chain: at this cap the budget is declared "
                  "to cut into the IRREDUCIBLE tier and nowhere else, because a "
                  "state that lost everything says nothing about itself")

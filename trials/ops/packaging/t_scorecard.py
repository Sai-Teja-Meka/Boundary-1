"""ops/packaging — the one-command scorecard, the external adapters, and the doc.

`PACKAGE` produced three things this file is responsible for keeping true:

1. **`python3 -m trials --engine <name>`** — a layered scorecard built out of the
   suite's own shared scorers and the authority registry, never out of numbers
   typed into a report.
2. **`trials/adapters/external/`** — a reference engine written against
   `INTERFACE.md` alone, plus two stubs. The claim is that the harness grades a
   system nobody here wrote *and still discriminates*, which is only worth
   anything if the reference engine actually **fails** the layers it does not
   implement.
3. **`packaging/README-public.md`** — the public identity, whose scorecard table
   is checked here against the same measurements the command produces. A public
   number that drifts from the engine is the failure mode this project spent
   seven autopsies describing in other people's work
   (`autopsy/GAPMAP.md §2`), so it is a red trial here.

## Scale, stated rather than hidden

The full card costs about a minute (`python3 -m trials --engine ours`), and the
same card for the reference engine costs about three, most of it a naive engine
being asked 20 000 reconstruction questions. Neither belongs in every suite run.
What runs here is:

  * the **cheap tiers measured exactly** — L1 on `sessions`, the L2 cue battery,
    the whole transfer tier (25 events);
  * the **two binding gate rows re-measured live** — L3 on `l3streamb` and L4 on
    `l4stream` — because the README publishes those two numbers as *exact*, and
    the ascension trials only assert they clear a threshold. Two different
    claims, so two checks;
  * the reference engine at the **declared reduced scale**, where the
    discrimination claim is made on the measured numbers rather than on a
    verdict string, since a prefix row is `diag` by design.

`chronicle` and `murk` at Layer 1 are **not** re-measured: `ascension/l1`
already asserts `(F, C, B) == (1000, 1000, 1000)` on them exactly, in this same
suite, and re-running a 50 000-event replay to reach the identical conclusion
would buy nothing but three minutes.

The bill, measured rather than estimated: the whole `ops/packaging` class takes
the suite from **5 m 13 s to about 6 m 20 s**. That is the price of a public
document whose numbers cannot go stale without the suite going red, and it is
recorded here so that a later session weighing it has the figure.

> **Extended 2026-08-07 (`[L7] [PACKAGE]`), and the bill restated.** The README
> now publishes `L5`, `L6` and `L7` rows and a second transfer reading, so this
> file re-measures them. The **same argument** that bought the `L3` and `L4`
> re-measurements buys these: an ascension trial asserts a row *clears a
> threshold*, and the README publishes it as *exact* — two different claims, so
> two checks. An engine could drift from `AUROC 976` to 905 and stay green in
> `ascension/l6` while the public number went stale.
>
> The three new binding rows cost **~30 s** (L5 26 s over 20 000 events at the
> ratified cap, L6 and L7 under 2 s each) and the three humility rows another
> **~25 s**. Measured rather than estimated: the suite goes from **548 trials in
> 9 m 45 s** to **573 in 10 m 02 s**, and the full card from about a minute to
> **2 m 08 s**. The three upper tiers are the cheapest thing on that list, which
> is worth recording because the L4 humility ladder is still the expensive one.
> The `v1` transfer trials below are pinned to `"v1"` **explicitly** rather than
> left on a default, because `corpora/real-sessions/V2-FREEZE-STOPPED.md` records
> that a late-bound `LATEST` is exactly how a frozen measurement moves without
> anybody deciding to move it.
>
> The out-of-suite 50-event re-run the README publishes beside `v1` is **not**
> checked here and says so in the document: it is measured on the live store,
> which grows every session, so a trial asserting it would be asserting how often
> the ritual ran. What *is* checked is the property that makes the comparison
> honest — that `v1`'s frozen numbers have not moved.
"""

import ast
import os
import re

from _harness import PROJECT_ROOT, require, require_equal
import _l1score
import _l4score
import _l4tasks
import run
import scorecard
from adapters import external, l3, l4

README_PUBLIC = os.path.join(PROJECT_ROOT, "packaging", "README-public.md")
HONESTY = os.path.join(PROJECT_ROOT, "packaging", "HONESTY.md")

# The published measurements. Every one of them is either re-measured below or
# owned by a named trial in this same suite; nothing here is a number somebody
# remembered. Layer -> (column label -> value).
PUBLISHED_SYNTHETIC = {
    1: ("F 1000", "C 1000", "B 1000"),
    2: ("cue-C 1000", "F 1000", "B 1000"),
    3: ("weighted-C 917", "unweighted-C 91", "F 1000", "B 1000"),
    4: ("footprint 250", "F 968", "C 1000", "B 1000"),
    5: ("precision **1000**", "recall **1000**", "dup-fire **0**",
        "miss **0**", "F **1000**"),
    6: ("Brier **23**", "ECE **0**", "AUROC **976**", "F **955**"),
    7: ("validity **1000**", "novelty **1000**", "tagging **1000**",
        "promotion **0/0/0**", "F **1000**", "ECE **0**"),
}

# The capped (humility) measurement each row must publish, verbatim, in its own
# cell — a bare integer would match anything, including the ceiling beside it.
PUBLISHED_CAPPED = {2: "capped cue-C 0", 3: "capped weighted-C 92",
                    4: "capped F 300", 5: "capped trigger-recall 0",
                    6: "capped AUROC 500", 7: "capped conjunction 0"}

# The three binding rows added at `[L7] [PACKAGE]`, re-measured live below and
# compared against the table. Layer 5's four identities are written as identities
# on purpose: `R5` clause 1 leaves no margin to widen later.
PUBLISHED_L5 = {"precision": 1000, "recall": 1000, "dup_fire": 0, "miss": 0,
                "F": 1000, "B": 1000, "footprint": 250}
PUBLISHED_L6 = {"brier": 23, "ece": 0, "auroc": 976, "F_core": 955,
                "F_all": 958, "B": 1000, "A": 2200, "n_pos": 2100, "n_neg": 100}
PUBLISHED_L7 = {"validity": 1000, "novelty": 1000, "tagging": 1000,
                "F_core": 1000, "F_all": 1000, "ece": 0, "B": 1000,
                "A": 2000, "n_pos": 2000, "n_neg": 0, "promotion": (0, 0, 0)}
PUBLISHED_CAPPED_MEASURED = {5: 0, 6: 500, 7: 0}

# The novelty horizon, `README-l7 §2.2`, quoted in the README's own section.
PUBLISHED_NOVELTY_HORIZON = "60  ->  30  ->  0"

PUBLISHED_TRANSFER = {
    1: ("F 1000", "C 1000", "B 1000"),
    2: ("cue-C 1000", "F 1000", "B 1000"),
    4: ("footprint 151", "F 172", "C 1000", "B 1000"),
}

# The transfer finding, as numbers. Re-derived below, then checked against the
# document — this is the divergence the session was told to publish, not hide.
TRANSFER_ASSERTIONS = 0
TRANSFER_IRREDUCIBLE = 25
TRANSFER_RECONSTRUCTED = 2
TRANSFER_L3_RETAINED_AT_SAME_CAP = 2


# ---- the generic Layer-1 scorer is checked against the frozen trial ---------

def trial_the_generic_l1_scorer_agrees_with_the_frozen_ascension_trial():
    """Two instruments, one measurement — so `_l1score` cannot drift quietly.

    `ascension/l1/t_retention.py` is frozen (§9.2) and carries its own private
    `_replay_and_score`, bound to `adapters/l1`. `_l1score` is the generic
    restatement the scorecard needs. Neither replaces the other; if they ever
    disagree the frozen one is right and this trial says so loudly.
    """
    frozen = run._load_module(os.path.join(run.HERE, "ascension", "l1",
                                           "t_retention.py"))
    from corpora.sessions import generator as gen
    payloads = list(gen.generate(gen.SEED, gen.N))

    f_frozen, c_frozen, b_frozen, _state = frozen._replay_and_score(payloads)

    from adapters import l1
    state, budget, accepted = _l1score.replay(l1, l1.empty, payloads)
    r = _l1score.score(l1, state, accepted)

    require_equal((r["F"], r["C"], budget["B"]), (f_frozen, c_frozen, b_frozen),
                  "the generic Layer-1 scorer disagrees with the FROZEN Layer-1 "
                  "ascension trial on the same corpus — the frozen trial is the "
                  "one that is right, and the scorecard is measuring something "
                  "else")
    require(_l1score.snapshot_round_trips(l1, state),
            "§5 L1's snapshot/restore clause failed through the generic scorer")


# ---- the gates on the card come from the authority registry -----------------

def trial_the_scorecard_gate_table_is_the_authority_registry():
    """No gate reaches the card without a §5 clause or a ruling behind it."""
    rulings = run._load_module(os.path.join(run.HERE, "laws", "t_rulings.py"))
    registered = {}
    for rel, const, value, _auth, _note in rulings.AUTHORIZED_GATES:
        registered[(rel, const)] = value

    table = scorecard.gate_table()
    require_equal(sorted(table), [1, 2, 3, 4, 5, 6, 7],
                  "the card must cover exactly the claimed layers")

    for layer in (1, 2, 3, 4, 5, 6, 7):
        gates = table[layer]["gates"]
        require(gates, "L%d reached the card with no gate at all" % (layer,))
        for const, value in gates.items():
            key = ("ascension/l%d/%s" % (layer, _ascension_file(layer)), const)
            require(key in registered,
                    "the card prints %s for L%d, which the registry does not "
                    "authorize" % (const, layer))
            require_equal(value, registered[key],
                          "the card's %s for L%d differs from the authorized "
                          "value" % (const, layer))

    # §5.1 L1: the floor layer has no humility gate. Every layer above has one.
    require_equal(table[1]["ceilings"], {},
                  "Layer 1 is the floor (§5.1 L1) — a humility ceiling there "
                  "would be capping against a layer that does not exist")
    for layer in (2, 3, 4, 5, 6, 7):
        require(table[layer]["ceilings"],
                "L%d reached the card with no humility ceiling — the gate above "
                "it would not be shown to be load-bearing" % (layer,))


def _ascension_file(layer):
    return {1: "t_retention.py", 2: "t_recall.py", 3: "t_forgetting.py",
            4: "t_consolidation.py", 5: "t_prospection.py",
            6: "t_meta_memory.py", 7: "t_generation.py"}[layer]


# ---- the adapters -----------------------------------------------------------

def trial_every_external_adapter_exposes_the_whole_interface_surface():
    for name in external.names():
        module = external.get(name)
        for attr in external.REQUIRED_SURFACE:
            require(callable(getattr(module, attr, None)),
                    "external adapter %r does not expose %s() — INTERFACE.md's "
                    "adapter contract" % (name, attr))
        ok, reason = module.available()
        require(isinstance(ok, bool) and isinstance(reason, str) and reason,
                "%r.available() must return (bool, non-empty reason)" % (name,))
        require(module.KIND in ("reference", "stub"),
                "%r declares an unknown adapter kind %r" % (name, module.KIND))


def trial_the_stubs_are_import_safe_and_refuse_rather_than_score():
    """A stub must never produce a number for a system that was never run."""
    for name in ("mem0", "letta"):
        module = external.get(name)
        require_equal(module.KIND, "stub", "%r should be a stub" % (name,))
        ok, reason = module.available()
        require(ok is False,
                "%r reports itself runnable; no session may reach a network or "
                "a key (packaging/HONESTY.md)" % (name,))
        require("human-supervised" in reason,
                "%r's reason must name the human-supervised step that would be "
                "required" % (name,))
        calls = {"empty": (), "make_engine": (1,), "ingest": (None, {}),
                 "query": (None, {"op": "read", "t": 0}), "snapshot": (None,),
                 "last_cost": (None,)}
        require_equal(sorted(calls), sorted(external.REQUIRED_SURFACE),
                      "this trial does not exercise the whole adapter surface")
        for attr, args in sorted(calls.items()):
            try:
                getattr(module, attr)(*args)
            except module.AdapterNotRunnable:
                continue
            raise AssertionError(
                "%r.%s returned instead of refusing — a stub that answers is a "
                "measurement of a system that was never run" % (name, attr))


def trial_the_reference_engine_imports_nothing_from_core():
    """Its evidence is about the harness, which requires it to be genuinely outside."""
    path = os.path.join(run.HERE, "adapters", "external", "reference.py")
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read(), filename=path)
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    offenders = [name for name in imported
                 if name == "core" or name.startswith("core.")
                 or name in ("corpora", "_harness") or name.startswith("corpora.")]
    require(not offenders,
            "the reference EXTERNAL engine imports %s — it would then be our "
            "engine wearing a costume, and it would prove nothing about grading "
            "a foreign system" % (", ".join(sorted(set(offenders)))))


def trial_the_reference_engine_abstains_and_never_raises():
    """§7.3 — capability absence is a score, not an exception."""
    ref = external.get("reference")
    state = ref.empty(4096)
    state, t = ref.ingest(state, {"kind": "spawn", "entity": 1, "class": "node"})
    require_equal(t, 0, "the reference engine did not assign t = 0 to its first event")

    for q in ({"op": "current", "entity": 1, "key": "class"},
              {"op": "asof", "entity": 1, "key": "class", "t": 0},
              {"op": "profile", "entity": 1},
              {"op": "count", "kind": "spawn"},
              {"op": "forgetting"},
              {"op": "no_such_op"},
              {"op": "read", "t": 999},
              "not even a dict",
              {}):
        answer = ref.query(state, q)
        require(isinstance(answer, dict), "query(%r) returned a non-Answer" % (q,))
        require_equal(sorted(answer), ["confidence", "provenance", "status", "value"],
                      "query(%r) returned the wrong Answer keys (§7.2)" % (q,))
        require(answer["status"] in ("answer", "abstain"),
                "query(%r) returned an illegal status" % (q,))
        if q != {"op": "read", "t": 0}:
            require_equal(answer["status"], "abstain",
                          "query(%r) answered a question this engine cannot "
                          "answer — §7.3 wants an abstention, and §3.0 prices a "
                          "fabrication at 0" % (q,))


def trial_the_reference_engine_is_pure_and_deterministic():
    ref = external.get("reference")
    payload = {"kind": "attr", "entity": 7, "key": "status", "val": "open"}
    before = ref.empty(4096)
    after, _t = ref.ingest(before, payload)
    require_equal(before.next_t, 0, "ingest mutated the caller's state (§2.1)")
    require_equal(payload, {"kind": "attr", "entity": 7, "key": "status",
                            "val": "open"},
                  "ingest mutated the caller's payload (§2.1)")

    def replay():
        state = ref.empty(1 << 16)
        for i in range(40):
            state, _ = ref.ingest(state, {"kind": "attr", "entity": i % 5,
                                          "key": "k%d" % (i % 3), "val": i})
        return ref.snapshot(state)

    require_equal(replay(), replay(),
                  "two identical replays produced different snapshots (§2.3)")
    require_equal(ref.snapshot(ref.restore(replay())), replay(),
                  "snapshot/restore is not byte-identical (§7.1)")


# ---- the card, on both engines ---------------------------------------------

def trial_the_scorecard_grades_our_engine_and_every_gate_row_passes():
    engine, reason = scorecard.load_engine(scorecard.OURS)
    require(engine is not None, "our own engine is not gradable: %s" % (reason,))
    card = scorecard.build(engine, quick=True, with_transfer=False)
    # L4 is a declared prefix under `quick` and reports `diag` by design; every
    # other claimed tier is measured on the corpus its gate binds on.
    for layer in (1, 2, 3, 5, 6, 7):
        require(card["tiers"][layer],
                "L%d produced no row for our own engine, which claims it"
                % (layer,))
        for row in card["tiers"][layer]:
            if row.get("gated") is False:
                continue
            require_equal(row["verdict"], "PASS",
                          "L%d/%s did not pass at the declared reduced scale%s"
                          % (layer, row["corpus"],
                             (" (undefined: %s)" % (row["undefined"],))
                             if row.get("undefined") else ""))
    for layer, row in card["humility"].items():
        require_equal(row["verdict"], "HELD",
                      "the L%d humility ceiling was breached by the capped "
                      "engine — the gate above it is not load-bearing" % (layer,))
    require_equal(sorted(card["humility"]), [2, 3, 4, 5, 6, 7],
                  "every layer but the floor carries a humility row (§5.1 L1)")
    require(scorecard.render(card), "the card rendered no lines")


def trial_the_harness_grades_a_foreign_engine_and_still_discriminates():
    """The `PACKAGE` claim, as a measurement rather than a sentence.

    The reference engine implements Layers 1–2 against `INTERFACE.md` and
    nothing else. It must **clear** those two gates — otherwise the harness is
    not generic, only ours passes and the interface is a fiction — and it must
    **miss** Layers 3 and 4 by a wide margin, otherwise the ladder is not
    measuring capability.

    Layer 4 is asserted on the measured numbers, not on the verdict string: at a
    declared prefix scale the card reports `diag` for everyone, because R4 binds
    that gate to the whole stream.
    """
    engine, reason = scorecard.load_engine("reference")
    require(engine is not None, "the reference adapter did not run: %s" % (reason,))
    card = scorecard.build(engine, quick=True, with_transfer=False)
    gates = card["gates"]

    for layer in (1, 2):
        for row in card["tiers"][layer]:
            require_equal(row["verdict"], "PASS",
                          "an engine implementing L%d against INTERFACE.md alone "
                          "failed the L%d gate on %s — the interface is not "
                          "generic" % (layer, layer, row["corpus"]))

    l3row = card["tiers"][3][0]
    require_equal(l3row["verdict"], "FAIL",
                  "an engine with NO eviction cleared the Layer-3 gate — the "
                  "gate is not measuring forgetting")
    require(l3row["GATE_WEIGHTED_C"] < gates[3]["gates"]["GATE_WEIGHTED_C"],
            "reference weighted-C=%d is not below the gate"
            % (l3row["GATE_WEIGHTED_C"],))
    require(l3row["refused"] > 0,
            "the reference engine refused nothing under 10x pressure — its cap "
            "is not binding and the comparison is empty")

    l4row = card["tiers"][4][0]
    require(l4row["GATE_C"] < gates[4]["gates"]["GATE_C"],
            "an engine with NO derived schema answered the Layer-4 coverage "
            "battery (C=%d)" % (l4row["GATE_C"],))
    require(l4row["GATE_RECONSTRUCTION_F"]
            < gates[4]["gates"]["GATE_RECONSTRUCTION_F"],
            "an engine with no reconstruction cleared the Layer-4 fidelity gate")
    require_equal(l4row["fabricated"], 0,
                  "the reference engine fabricated on an unanswerable probe — a "
                  "foreign engine may be incapable, but the harness must not "
                  "reward it for guessing")

    # Above Layer 4 it claims nothing, and the card says so rather than printing
    # a zero: a tier measured against an engine that does not reach the layer
    # reports a number about the harness and not about the engine.
    for layer in (5, 6, 7):
        require_equal(card["tiers"][layer], [],
                      "L%d produced a row for an engine whose MAX_LAYER is %d"
                      % (layer, engine.max_layer))
        require(layer not in card["humility"],
                "a humility row was measured at L%d against an engine that does "
                "not reach L%d" % (layer, layer - 1))


# ---- the transfer tier and its finding --------------------------------------

def trial_the_transfer_tier_measures_real_fuel_and_reports_the_divergence():
    """The published divergence, re-derived: on real fuel Layer 4 is Layer 3.

    Not a soft observation. On `corpora/real-sessions/v1` the facet map reads
    **no** assertion and `row_shape` refuses **every** payload (a session summary
    has nested fields), so the consolidation engine builds nothing and falls back
    on the inherited Layer-3 forgetting law — and at the same cap the frozen
    Layer-3 engine retains exactly the same events. That identity is the finding.
    """
    engine, _reason = scorecard.load_engine(scorecard.OURS)
    tr = scorecard.transfer(engine, version="v1")

    require_equal((tr["rows"][1]["GATE_F"], tr["rows"][1]["GATE_C"],
                   tr["rows"][1]["GATE_B"]), (1000, 1000, 1000),
                  "Layer 1 must be exact on real fuel too — retention does not "
                  "care where an event came from")
    require_equal(tr["rows"][2]["GATE_CUE_C"], 1000,
                  "the store's own cue surface no longer recalls every uniquely "
                  "cueable session summary")
    require_equal(tr["rows"][2]["unaddressable"], 0,
                  "some session summary has no discriminating token prefix; the "
                  "transfer L2 denominator would then be measuring the corpus")

    l3note = tr["rows"][3]
    require(l3note["gateable"] is False, "the L3 transfer row must not claim a gate")
    require_equal((l3note["with_importance"], l3note["with_handle"]), (0, 0),
                  "the real corpus now carries importance or a handle field — the "
                  "recorded reason for the L3 n/a has changed and the public "
                  "README says otherwise")

    l4row = tr["rows"][4]
    require_equal(l4row["assertions"], TRANSFER_ASSERTIONS,
                  "the facet map now reads assertions in a session summary")
    require_equal(l4row["irreducible"], TRANSFER_IRREDUCIBLE,
                  "the irreducible tier on real fuel changed")
    require_equal((l4row["GATE_FOOTPRINT"], l4row["GATE_RECONSTRUCTION_F"]),
                  (151, 172),
                  "the published transfer numbers no longer describe the engine")
    require_equal(l4row["wrong"], 0,
                  "consolidation returned a WRONG reconstruction on real fuel — "
                  "coverage may collapse under pressure; correctness may not")
    require_equal(l4row["fabricated"], 0,
                  "consolidation fabricated on an unanswerable probe on real fuel")

    # The identity: Layer 4 degenerates exactly to Layer 3 on this corpus.
    from corpora import real_sessions
    payloads = real_sessions.payloads("v1")
    bundle = _l4tasks.build("real-sessions", payloads)
    state3 = l3.make_engine(3, bundle["budget_cap"])
    for payload in payloads:
        state3, _t = l3.ingest(state3, payload)
    require_equal(l3.retained(state3), TRANSFER_L3_RETAINED_AT_SAME_CAP,
                  "the Layer-3 engine retains a different number of real events "
                  "at the Layer-4 cap")
    state4, _budget = _l4score.replay(
        l4, lambda cap: l4.make_engine(4, cap), bundle)
    answered4 = sum(1 for t in range(len(payloads))
                    if l4.query(state4, {"op": "read", "t": t})["status"] == "answer")
    require_equal(answered4, TRANSFER_RECONSTRUCTED,
                  "the Layer-4 engine answers a different number of real events")
    require_equal(answered4, l3.retained(state3),
                  "the published finding is that Layer 4 has nothing to derive on "
                  "real fuel and answers exactly what Layer 3 retains; it now "
                  "answers %d against %d retained" % (answered4, l3.retained(state3)))


def trial_on_real_fuel_a_no_forgetting_engine_reconstructs_more_than_ours():
    """The uncomfortable half of the transfer finding, pinned so it cannot be lost.

    On `corpora/real-sessions/v1` at the ratified Layer-4 cap the reference
    external engine — which cannot forget at all, and simply fills then refuses
    — returns **11** of 25 events byte-exact, against our consolidation engine's
    **2**. Neither is a defect. §3.0's fidelity counts *events*, fill-then-refuse
    maximizes count by keeping the cheapest (here the earliest, shortest session
    summaries), and the inherited Layer-3 importance law spends the budget on the
    two most recent — which on this corpus are also the two largest.

    Which behaviour is *right* for a session store is a judgement the constitution
    does not make and this trial does not either. What it refuses to allow is the
    number quietly disappearing: `packaging/README-public.md` publishes both, and
    if either changes this goes red.
    """
    from corpora import real_sessions
    payloads = real_sessions.payloads("v1")
    bundle = _l4tasks.build("real-sessions", payloads)
    cap = bundle["budget_cap"]

    state, _budget = _l4score.replay(l4, lambda c: l4.make_engine(4, c), bundle)
    ours = [t for t in range(len(payloads))
            if l4.query(state, {"op": "read", "t": t})["status"] == "answer"]

    ref = external.get("reference")
    rstate = ref.make_engine(2, cap)
    for payload in payloads:
        rstate, _t = ref.ingest(rstate, payload)
    theirs = [t for t in range(len(payloads))
              if ref.query(rstate, {"op": "read", "t": t})["status"] == "answer"]

    require_equal(ours, [23, 24],
                  "our engine no longer keeps exactly the two most recent real "
                  "session summaries at the Layer-4 cap")
    require_equal(theirs, list(range(11)),
                  "the reference engine no longer keeps exactly the first eleven")
    require(len(theirs) > len(ours),
            "the published inversion is gone: a no-forgetting engine used to "
            "reconstruct more real events than ours (%d vs %d)"
            % (len(theirs), len(ours)))


# ---- the two binding gate rows, re-measured because they are published ------

def trial_the_published_binding_rows_are_measured_and_exact():
    """The README publishes L3 917/91/1000 and L4 250/968/1000 as *exact*.

    The ascension trials assert those clear a threshold, which is a different
    claim: an engine could drift from 917 to 860 and stay green there while the
    public number went stale. Half a minute of suite time buys the stronger
    statement, and the cost is recorded in this file's docstring rather than
    discovered by someone timing the suite.
    """
    import _l3score

    state, budget = _l3score.replay(
        l3, lambda cap: l3.make_engine(3, cap), scorecard.L3_BINDING)
    r3 = _l3score.score(l3, state, scorecard.L3_BINDING)
    require_equal((r3["weighted_C"], r3["unweighted_C"], r3["F"], budget["B"]),
                  (917, 91, 1000, 1000),
                  "the published Layer-3 row is stale")

    bundle = _l4tasks.corpus(scorecard.L4_BINDING)
    state, budget = _l4score.replay(l4, lambda cap: l4.make_engine(4, cap), bundle)
    r4 = _l4score.score(l4, state, bundle)
    require_equal((r4["footprint"], r4["F"], r4["C"], budget["B"]),
                  (250, 968, 1000, 1000),
                  "the published Layer-4 row is stale")


def trial_the_published_layer_5_row_is_measured_and_exact():
    """`R5` clause 1: four of these six clauses are IDENTITIES and have no margin.

    So the published row is not "clears 1000" — it *is* 1000, and a document that
    printed anything else would be printing a different claim from the one the
    gate makes. The engine's own clock audits the firing report inside
    `_l5score.score` (`assert_t_identity`), so a row that survived this check
    survived it on numbers the engine could account for.
    """
    import _l5score
    import _l5tasks
    from adapters import l5

    b = _l5tasks.corpus()
    state, budget = _l5score.replay(l5, lambda cap: l5.make_engine(5, cap), b)
    r = _l5score.score(l5, state, b)
    got = {"precision": r["precision"], "recall": r["recall"],
           "dup_fire": r["dup_fire"], "miss": r["miss"], "F": r["F"],
           "B": budget["B"], "footprint": _l5score.footprint(state, b)}
    require_equal(got, PUBLISHED_L5, "the published Layer-5 row is stale")
    require_equal((r["wrong"], r["fabricated"], budget["refused"]), (0, 0, 0),
                  "the Layer-5 row's honesty counters moved")


def trial_the_published_layer_6_row_is_measured_and_exact():
    """The row that publishes an engine which is WRONG ON PURPOSE.

    `F 955` and `n_neg 100` are the two numbers a reader is most likely to
    misread, and they are the two a drift would move first: 100 errors is
    Theorem 1's floor *and* ceiling on this artifact, so an engine measuring 99
    resolved a mirror pair and an engine measuring 101 broke something the
    theorem says it cannot.
    """
    import _l6score
    from adapters import l6

    b = _l6score.BATTERIES[scorecard.L6_BINDING]()
    state, budget = _l6score.replay(l6, lambda cap: l6.make_engine(6, cap), b,
                                    l6.DEFAULT_BUDGET)
    r = _l6score.score(_l6score.observe(l6, state, b), b)
    got = {"brier": _l6score.permille(r["brier"]),
           "ece": _l6score.permille(r["ece"]),
           "auroc": _l6score.permille(r["auroc"]),
           "F_core": _l6score.permille(r["F_core"]),
           "F_all": _l6score.permille(r["F_all"]),
           "B": budget["B"], "A": r["A"], "n_pos": r["n_pos"],
           "n_neg": r["n_neg"]}
    require_equal(got, PUBLISHED_L6, "the published Layer-6 row is stale")
    require_equal(r["wrong"], 100,
                  "the engine is wrong exactly 100 times on this artifact by "
                  "theorem — one member of each mirror pair. %d is a different "
                  "engine or a different artifact" % (r["wrong"],))
    require_equal(r["fabricated"], 0, "the Layer-6 row fabricated")


def trial_the_published_layer_7_row_is_measured_and_exact_including_the_ladder():
    """Seven clauses, and `promotion = 0` is the one no single replay can report.

    `§5 L7` states it **three deep** and `§6` names the same number a second time
    in the strain class, so the published `0/0/0` is a ladder and is measured as
    one — a rung at a time, because a ladder read only at depth 3 could not say
    where a break occurred.
    """
    import _l7score
    from adapters import l7

    b = _l7score.battery()
    state, budget = _l7score.replay(l7, lambda cap: l7.make_engine(7, cap), b,
                                    l7.DEFAULT_BUDGET)
    rows = _l7score.observe(l7, state, b)
    r = _l7score.score(rows, b)
    _after, rungs, _canon = _l7score.promotion_ladder(l7, state, b)

    got = {"validity": _l7score.permille(r["validity"]),
           "novelty": _l7score.permille(r["novelty"]),
           "tagging": _l7score.permille(r["tagging"]),
           "F_core": _l7score.permille(r["F_core"]),
           "F_all": _l7score.permille(r["F_all"]),
           "ece": _l7score.permille(r["ece"]), "B": budget["B"],
           "A": r["A"], "n_pos": r["n_pos"], "n_neg": r["n_neg"],
           "promotion": tuple(rung["promotion"] for rung in rungs)}
    require_equal(got, PUBLISHED_L7, "the published Layer-7 row is stale")
    require_equal(r["tagging_denominator"], 160,
                  "tagging's denominator is the artifact's declared G class "
                  "(R8 clause 3(b)); %d is the engine grading itself"
                  % (r["tagging_denominator"],))
    require_equal((r["wrong"], r["fabricated"]), (0, 0),
                  "the Layer-7 row's honesty counters moved")


def trial_the_published_capped_scores_for_the_three_new_tiers_are_measured():
    """Each new tier's humility row, re-measured — the gate's own load-bearing proof.

    A ceiling published without its measured capped score is a ceiling nobody has
    shown is respected. These three are the numbers `HONESTY.md §4` cites as
    evidence *for* the methodology, so they are the ones that must not drift.
    """
    engine, reason = scorecard.load_engine(scorecard.OURS)
    require(engine is not None, "our own engine is not gradable: %s" % (reason,))
    rows = scorecard.tier_humility(engine, quick=True)
    measured = {5: rows[5]["CEILING_TRIGGER_RECALL"],
                6: rows[6]["CEILING_AUROC"],
                7: rows[7]["CEILING_CONJUNCTION"]}
    require_equal(measured, PUBLISHED_CAPPED_MEASURED,
                  "a published capped score for L5/L6/L7 is stale")
    require_equal(rows[6]["confidences"], (0, 1000),
                  "the capped-5 engine no longer emits exactly {0, 1000} through "
                  "§7.2 — the Layer-6 ceiling's first prong is that the harness "
                  "supplies no convention and reads the engine's own field")
    require_equal(rows[7]["denominator"], 160,
                  "the Layer-7 conjunction's denominator is the artifact's whole "
                  "declared class (R8 clause 7), so that no engine can empty it")


# ---- the public document ----------------------------------------------------

def _tables(text):
    """Every markdown table in the document, as lists of stripped cell lists."""
    tables = []
    current = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if all(set(cell) <= set("-: ") and cell for cell in cells):
                continue                       # the header rule
            current.append(cells)
            continue
        if current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables


def _row_starting(tables, label):
    """Rows whose first cell names `label`, ignoring markdown emphasis marks."""
    for table in tables:
        for row in table:
            if row and row[0].strip().lstrip("*_ ").startswith(label):
                yield row


def trial_the_public_readme_scorecard_matches_the_measured_engine():
    """A published number that drifts from the engine is the whole failure mode.

    `autopsy/GAPMAP.md §2` convicts four engines of writing down metadata they
    never read. A README with a scorecard nothing checks is the documentation
    form of the same sin, so the table is parsed and compared to the values this
    file measures or names an owner for.
    """
    require(os.path.exists(README_PUBLIC),
            "packaging/README-public.md is missing — the PACKAGE deliverable "
            "this trial exists to keep honest")
    with open(README_PUBLIC, "r", encoding="utf-8") as fh:
        text = fh.read()
    tables = _tables(text)

    names = {1: "L1", 2: "L2", 3: "L3", 4: "L4", 5: "L5", 6: "L6", 7: "L7"}
    for layer, expected in PUBLISHED_SYNTHETIC.items():
        rows = [row for row in _row_starting(tables, names[layer])
                if len(row) >= 4 and "PASS" in " ".join(row)]
        require(rows, "no scorecard row for %s in README-public.md" % (names[layer],))
        measured_cell = " ".join(rows[0])
        for fragment in expected:
            require(fragment in measured_cell,
                    "README-public.md's %s row does not carry the measured "
                    "value %r (row: %s)" % (names[layer], fragment, measured_cell))

    for layer, capped in PUBLISHED_CAPPED.items():
        rows = [row for row in _row_starting(tables, names[layer])
                if len(row) >= 5]
        require(rows, "no scorecard row for %s" % (names[layer],))
        require(any(capped in cell for cell in rows[0][-2:]),
                "README-public.md's %s row does not carry the measured capped "
                "score %r" % (names[layer], capped))

    # The transfer tier's own table, and its two load-bearing sentences.
    flat = " ".join(text.split())
    for fragment in ("real-sessions", "26‰", "Form B",
                     "CC BY-NC", "token-F1", "MemoryAgentBench", "WRIT"):
        require(fragment in flat,
                "README-public.md no longer states %r — the limitations and the "
                "attribution are load-bearing credibility, not decoration"
                % (fragment,))
    require("footprint 151" in flat and "F 172" in flat,
            "README-public.md no longer publishes the transfer-tier divergence")
    require_equal(len(re.findall(r"\]\(\.\./LORE\.md\)", text)), 1,
                  "README-public.md must carry exactly one link to the "
                  "cultivation lore")
    lore_lines = [i for i, line in enumerate(text.split("\n")) if "LORE.md" in line]
    require_equal(len(lore_lines), 1,
                  "the cultivation framing is one link at the bottom and nothing "
                  "more (LORE.md's own containment notice); it appears on %d lines"
                  % (len(lore_lines),))
    require(lore_lines[0] >= len(text.split("\n")) - 5,
            "the one lore link is not at the bottom of the document")


def trial_the_public_readme_is_current_at_seven_of_nine():
    """The counts a stale document gets wrong first, and the ledger behind them.

    A scorecard that quietly says "four layers" while seven are claimed is the
    documentation form of `autopsy/GAPMAP.md §2`'s thesis, and it is the exact
    shape this document carried for three moves under dated notes — annotated
    debt, visible and bounded, and this is the move that owned the rewrite.
    """
    with open(README_PUBLIC, "r", encoding="utf-8") as fh:
        text = fh.read()
    flat = " ".join(text.split())

    require("Seven of the nine are built and certified" in flat,
            "README-public.md no longer states the claimed-layer count")
    require("Seven layers claimed" in flat,
            "the scorecard section no longer states how many layers it covers")
    require("`R1` through `R8`" in flat or "R1 through R8" in flat,
            "the README no longer states how many rulings bind the gates")
    require("Five candidate substrates were killed" in flat,
            "the README no longer states the substrate-kill count")
    require("Five substrate kills" in flat,
            "the README no longer carries the substrate-kill table, which is "
            "the strongest thing this project can say about whether its own "
            "corpora are tuned to its engine")
    require("2 fired / 0 pending" in flat,
            "the README no longer records the dogfood promise ledger, which is "
            "the only on-the-record demonstration of Layer 5 that is not a "
            "synthetic corpus")
    for fragment in ("no thresholds at all", "BOUNDARY-HIGH.md"):
        require(fragment in flat,
                "the README no longer records that Layers 8-9 have %r" % (fragment,))


def trial_the_public_readme_carries_the_novelty_horizon_and_its_citation_rule():
    """The one measure here whose referent MOVES, and the rule that follows.

    `README-l7 §2.2` is the source; this checks the public document quotes it and
    states the consequence. A published `novelty 1000` with no store named is the
    citation error `HONESTY.md §6` exists to forbid, and it is the only one this
    document makes easy.
    """
    with open(README_PUBLIC, "r", encoding="utf-8") as fh:
        text = fh.read()
    flat = " ".join(text.split())

    require(PUBLISHED_NOVELTY_HORIZON.replace("  ", " ") in flat,
            "README-public.md no longer publishes the novelty horizon "
            "%r" % (PUBLISHED_NOVELTY_HORIZON,))
    require("THE NOVELTY HORIZON" in text,
            "the horizon is no longer a section of its own — a citation rule "
            "buried in an appendix is a citation rule nobody follows")
    require("quoting `novelty 1000` without saying which store it was measured "
            "against" in flat.replace("**", ""),
            "the citation rule the horizon forces is gone from the README")
    require("failure of an **instrument**, not of an engine" in flat
            or "failure of an instrument, not of an engine" in flat.replace("**", ""),
            "the README no longer states the category difference; without it "
            "the horizon reads as a defect of the engine")

    source = os.path.join(PROJECT_ROOT, "core", "layers", "README-l7.md")
    with open(source, "r", encoding="utf-8") as fh:
        readme_l7 = " ".join(fh.read().split())
    require("60 -> 30 -> 0" in readme_l7,
            "core/layers/README-l7.md §2.2 no longer states the horizon the "
            "public document quotes")


def trial_the_public_readme_publishes_the_stopped_v2_freeze():
    """A `PACKAGE` deliverable that did not land is a deliverable readers must see.

    The `v2` freeze was attempted and stopped by a scrub finding. Publishing the
    stop — with what the finding is, and that it is a decision waiting rather
    than a defect — is the same discipline that publishes the transfer
    divergence: what this project will not do is publish only the parts that
    landed.
    """
    from corpora import real_sessions
    with open(README_PUBLIC, "r", encoding="utf-8") as fh:
        text = fh.read()
    flat = " ".join(text.split())

    require("the freeze was ATTEMPTED and STOPPED" in flat
            or "ATTEMPTED and STOPPED" in flat,
            "README-public.md does not record that the v2 freeze stopped")
    require("V2-FREEZE-STOPPED.md" in flat,
            "the README does not point at the decision record")
    require("A finding stops a freeze and a human decides" in flat.replace("**", ""),
            "the README no longer states the rule the freeze stopped under")
    require_equal(real_sessions.VERSIONS, ("v1",),
                  "the README says no v2 exists and corpora/real_sessions.py "
                  "says otherwise")
    require("`v1`'s numbers above are the only transfer numbers any trial "
            "re-measures" in flat.replace("**", ""),
            "the README no longer distinguishes the frozen transfer tier from "
            "the out-of-suite re-run beside it — that distinction is what makes "
            "publishing an unfrozen measurement honest rather than sloppy")
    for fragment in ("out of suite", "50 events"):
        require(fragment.lower() in flat.lower(),
                "the README no longer labels the re-run %r" % (fragment,))


def trial_the_public_readme_points_at_the_catalog_and_the_adapter_contract():
    """Two deliverables this document must POINT at rather than restate.

    The adapter contract lives in `trials/adapters/README.md` and was already
    discharged before this move; the failure catalog and the four-kind taxonomy
    live in `packaging/CATALOG.md`. A public document that restated either would
    have two copies to keep in step, which is how the numbers in one of them go
    quietly wrong.
    """
    with open(README_PUBLIC, "r", encoding="utf-8") as fh:
        text = fh.read()
    flat = " ".join(text.split())

    require("packaging/CATALOG.md" in flat or "CATALOG.md" in flat,
            "README-public.md does not point at the failure catalog")
    require(os.path.exists(os.path.join(PROJECT_ROOT, "packaging", "CATALOG.md")),
            "the catalog the README points at does not exist")
    require("trials/adapters/README.md" in flat,
            "the README does not point at the adapter contract")
    require(os.path.exists(os.path.join(PROJECT_ROOT, "trials", "adapters",
                                        "README.md")),
            "the adapter contract the README points at does not exist")
    for fragment in ("state.occupancy", "state.budget_cap", "state.next_t",
                     "restore(bytes) -> state", "integer\npermille",
                     "{observed, generated}"):
        needle = " ".join(fragment.split())
        require(needle in flat,
                "the README's summary of the adapter contract drops %r; the "
                "point of naming it here is that a foreign engine cannot be "
                "graded without it" % (needle,))


def trial_honesty_md_carries_the_four_things_it_exists_to_carry():
    """`HONESTY.md` is the claims ledger; these four sections are its whole job.

    Checked as presence of the specific commitments rather than as prose quality,
    because the failure this guards against is a section quietly disappearing
    when it becomes inconvenient — which is the only way a claims ledger ever
    fails.
    """
    require(os.path.exists(HONESTY),
            "packaging/HONESTY.md is missing — README-public.md links to it and "
            "the scorecard's credibility rests on it")
    with open(HONESTY, "r", encoding="utf-8") as fh:
        text = fh.read()
    flat = " ".join(text.split())

    # 1. What this IS — the three claims, and only these three.
    for fragment in ("executable correctness specification",
                     "deterministic reference floor", "teaching artifact"):
        require(fragment in flat,
                "HONESTY.md no longer claims to be a %r" % (fragment,))

    # 2. What this is NOT — the two disclaimers the session was told to state.
    for fragment in ("Not a production memory library",
                     "Not a neural-retrieval competitor"):
        require(fragment in flat, "HONESTY.md dropped the disclaimer %r" % (fragment,))

    # 3. The strain-2 story, with the sin named and the discipline named.
    for fragment in ("recorded but never binding", "red first",
                     "demotions 7", "forgetting-record count 0"):
        require(fragment in flat.replace("**", ""),
                "HONESTY.md's strain-2 account no longer carries %r — the story "
                "is that OUR engine committed the sin its own autopsies convict "
                "four systems of, and that it was fixed red-first" % (fragment,))

    # 4. The methodology note, and specifically the evidence that counts AGAINST.
    for fragment in ("The corpora are ours",
                     "does not transfer to our own real data",
                     "11 of 25"):
        require(fragment in flat.replace("**", ""),
                "HONESTY.md's methodology note no longer carries the "
                "counter-evidence %r; evidence both ways is the point of the "
                "section" % (fragment,))

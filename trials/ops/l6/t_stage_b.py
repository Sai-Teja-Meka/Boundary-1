"""ops/l6 — the Layer-6 Stage-B wiring, checked engine-free.

`ascension/l6/t_meta_memory.py` is entirely engine-gated by design, and
`inheritance/l6` all but one trial. That is the sanctioned trials-before-engine
split, and it has one hazard: a battery nobody can run is a battery nobody can
check. These trials are the half of Stage B that **can** be run today — the
instrument, the declared vocabulary, the denominator declaration and the document
— so the frozen battery cannot be quietly wrong about the things it does not need
an engine to be right about.

None of them applies a `§5` clause to anything. There is no gate constant in this
file, and there is nothing here for `laws/t_rulings.py` to authorize.
"""

import os
from fractions import Fraction

from _harness import require, require_equal

import _l6btasks
import _l6score
import _l6tasks

STAGE_B = os.path.join(_l6btasks.PROJECT_ROOT, "trials/ascension/l6/STAGE-B.md")

# The two query operations both artifacts speak. They are LAYER-4 verbs, and
# deliberately so: `§5 L6` asks for a confidence model, not a second reader.
DECLARED_OPS = ("asof", "current")


def _flat(path):
    with open(path, "r", encoding="utf-8") as fh:
        return " ".join(fh.read().split())


# ---- one instrument --------------------------------------------------------

def trial_the_layer6_scorer_and_the_stage_a_arithmetic_share_one_instrument():
    """An engine and a policy are measured by ONE ruler, and it is the same object.

    `_l6score` computes nothing of its own: `brier`, `ece`, `auroc` and
    `fidelity` are imported from `_l6tasks` — the functions round 1's oracle,
    round 2's exhibited witness and every named capability-free baseline are
    scored by — and `_l6btasks` imports the same four. This asserts the identity
    rather than the agreement, because two functions that agree on today's inputs
    are not one instrument.

    It is the discipline `_l4score` set and `_l5score` restated, and at Layer 6
    it is load-bearing in a new way: the humility ceiling is measured on an
    ENGINE while `t_attainability_b.py`'s `confident-always` row is measured on a
    POLICY, and `R7`'s evidence section records them as the same number. They can
    only be the same number if they are the same function.
    """
    for name in ("brier", "ece", "auroc", "fidelity", "permille"):
        require(getattr(_l6score, name) is getattr(_l6tasks, name),
                "_l6score.%s is not _l6tasks.%s — a Layer-6 engine and a Layer-6 "
                "policy would then be scored by two rulers that merely agree"
                % (name, name))
        require(getattr(_l6btasks, name) is getattr(_l6tasks, name),
                "_l6btasks.%s is not _l6tasks.%s" % (name, name))


def trial_the_ece_bins_are_the_reading_r7_clause_5_rules():
    """`bin(conf) = 9 if conf == 1000 else conf // 100` — `R7` clause 5, on the instrument.

    `§3.4`'s ten bins are `[0,100)`, `[100,200)`, …, `[900,1000]` with the last
    **closed**, which on an integer permille admits exactly one reading and
    `R7` clause 5 rules it. The clause exists because it is *"the one place a
    §3.4 quantity could be computed two defensible ways from the same numbers"*,
    and because the exhibited witness's `ECE = 0` depends on it: its 500s land in
    bin 5 and its 1000s in bin 9.

    Checked here through the instrument's own arithmetic rather than by reading
    its source: a set of answers that lands entirely in one bin has `ECE` equal
    to `|mean confidence − accuracy|` in that bin, so putting 1000 in a bin of
    its own — or splitting the closed interval — would move a number this trial
    fixes.
    """
    # A perfectly-agreeing closed last bin: 1000 at accuracy 1 contributes 0.
    require_equal(_l6score.ece([(1000, True)] * 4), 0,
                  "confidence 1000 against accuracy 1 must contribute nothing")
    # 900 is the lower, CLOSED end of the same bin and must share it: 900 and
    # 1000 together are one bin whose mean confidence is 19/20 against accuracy 1.
    require_equal(_l6score.ece([(900, True), (1000, True)]), Fraction(1, 20),
                  "the last bin is `[900, 1000]` and is closed at both ends "
                  "here: 900 and 1000 share bin 9")
    # 899 is bin 8 and must NOT share it.
    require(_l6score.ece([(899, True), (1000, True)])
            != _l6score.ece([(900, True), (1000, True)]),
            "899 and 900 landed in the same bin — `conf // 100` is the reading "
            "R7 clause 5 rules, and the boundary is where it bites")
    # The witness's own partition: 500 at accuracy 1/2, 1000 at accuracy 1.
    witness = [(500, True)] * 100 + [(500, False)] * 100 + [(1000, True)] * 2000
    require_equal(_l6score.ece(witness), 0,
                  "the exhibited witness's ECE = 0 depends on this bin index — "
                  "bin 5 carries its 500s against an accuracy of one half, which "
                  "is Theorem 1 showing up inside §3.4, and bin 9 its 1000s")


# ---- the declared vocabulary and the declared denominator ------------------

def trial_the_declared_query_vocabulary_is_the_one_the_battery_speaks():
    """`STAGE-B.md §2`: two query shapes, both of them Layer-4 verbs.

    A Layer-6 battery asks questions the layer below already answers and scores
    the **confidence** attached to them. That is `§5 L6`'s own distinction —
    *"confidence permille from structural evidence"*, not a better answer — and on
    battery-b it is load-bearing rather than stylistic: the forcing region is
    exactly the class no reader can get right, so a battery that rewarded a
    better answer there would be rewarding an engine that had read the key.

    Asserted over the frozen records of **both** artifacts, so a later artifact
    that introduced a third operation would go red here rather than reach the
    engine through a scorer that had never seen it.
    """
    for name, build in sorted(_l6score.BATTERIES.items()):
        b = build()
        ops = sorted({rec["q"]["op"] for rec in b["records"]})
        require_equal(tuple(ops), DECLARED_OPS,
                      "%s speaks query operations %r; the declared vocabulary is "
                      "%r" % (name, ops, list(DECLARED_OPS)))
        for rec in b["records"]:
            require(set(rec["q"]) <= {"op", "entity", "key", "t"},
                    "%s qid %d carries an undeclared query field: %r"
                    % (name, rec["qid"], sorted(rec["q"])))
            require(("t" in rec["q"]) == (rec["q"]["op"] == "asof"),
                    "%s qid %d: only an as-of query carries a `t`"
                    % (name, rec["qid"]))


def trial_every_query_class_declares_whether_it_scores_inside_the_denominator():
    """`R7` clause 2, as a check on the battery rather than a promise in a document.

    *"Every `ATTAINABILITY.md` and every Layer-6-or-later battery states its `A`,
    its `n_pos` and its `n_neg` explicitly beside the triple, and a battery
    declares for each query class whether it scores inside the denominator and
    why."* `_l6score.DENOMINATOR` is that declaration; `_l6score._bundle` refuses
    an artifact whose classes it does not cover; this asserts the other half —
    that the declaration is right about which classes are answerable, so *outside
    the denominator* means *unanswerable* and never *inconvenient*.

    Both artifacts are covered, including the demoted one. A demotion is a change
    of authority and not of duty: `corpora/l6battery` is still scored and still
    reported, so it still declares.
    """
    for name, build in sorted(_l6score.BATTERIES.items()):
        b = build()
        declared = _l6score.DENOMINATOR[name]
        seen = {}
        for rec in b["records"]:
            answerable = seen.setdefault(rec["class"], rec["answerable"])
            require_equal(rec["answerable"], answerable,
                          "%s: class %s mixes answerable and unanswerable "
                          "queries, so no single declaration can be true of it"
                          % (name, rec["class"]))
        for cls, (inside, why) in sorted(declared.items()):
            require_equal(inside, seen[cls],
                          "%s: class %s is declared %s §3.4's denominator but is "
                          "%sanswerable — a class is outside because an "
                          "abstention carries no confidence to calibrate, and "
                          "for no other reason"
                          % (name, cls, "inside" if inside else "outside",
                             "" if seen[cls] else "un"))
            require(why.strip() != "",
                    "%s: class %s declares no reason" % (name, cls))


def trial_the_binding_artifact_carries_a_forcing_region_and_the_diagnostic_does_not():
    """`R7` clause 3(b), stated over the two bundles the battery can reach.

    *"A gate citing `AUROC` binds only on an artifact where both classes
    non-empty is a THEOREM, and the artifact must carry the proof."* The binding
    artifact carries a forcing region; round 1's does not, and that is exactly
    why clause 1 demoted it. The bundle shapes say so, so a future session cannot
    point the gate at an artifact with no region by changing one name.
    """
    binding = _l6score.battery_b()
    diagnostic = _l6score.battery_one()
    require(binding["region_pairs"] is not None,
            "the binding artifact has lost its forcing region")
    require_equal(len(binding["region_pairs"]), _l6btasks.PAIRS,
                  "the forcing region is no longer the whole declared region")
    require(diagnostic["region_pairs"] is None,
            "round 1's artifact has acquired a forcing region — it was demoted "
            "BECAUSE it has none (R7 clause 1), and its bytes are untouched")


# ---- the document ----------------------------------------------------------

def trial_stage_b_records_the_figures_the_instrument_computes():
    """Docs are checked, not trusted (`R6` clause 3: the trial's value is enforced).

    `STAGE-B.md` records what the capped engine measures and what the artifact's
    denominator is. Those numbers are recomputed here from `_l6btasks`' own
    scoreboard — the `confident-always` row, which `ATTAINABILITY-B.md §4.2`
    establishes **is** `make_engine(layer_cap = 5)` — and required verbatim in
    the document, so prose and measurement cannot drift apart silently.
    """
    row = _l6btasks.scoreboard()["confident-always"]
    p = _l6btasks.as_permille({k: v for k, v in row.items() if k != "trace"})
    b = _l6score.battery_b()

    lines = (
        "CAPPED brier %d ece %d auroc %d F_core %d F_all %d"
        % (p["brier"], p["ece"], p["auroc"], p["F_core"], p["F_all"]),
        "DENOM A %d n_pos %d n_neg %d N %d"
        % (p["A"], p["n_pos"], p["n_neg"], b["n"]),
        "REGION pairs %d forcing_queries %d"
        % (_l6btasks.PAIRS, _l6btasks.REGION_QUERIES),
    )
    text = _flat(STAGE_B)
    for line in lines:
        require(line in text,
                "STAGE-B.md no longer records `%s` — the document and the "
                "instrument have come apart, and under R6 clause 3 the "
                "instrument is the enforced value" % (line,))


def trial_stage_b_states_what_it_deliberately_does_not_assert():
    """The restraint is part of the record, not a footnote a later session can drop.

    Layer 5's Stage B recorded one over-tightening it caught and removed —
    `wrong = 0` asserted beside `F ≥ 980` would have gated at 1000 under a 980
    clause — and `R5` clause 1 records the ratified slack as the constitution's
    own answer to `R2`'s perfection objection. Layer 6's is the tie confidence:
    the witness prices the forcing region at 500 and the battery does **not**
    require it, because `§5 L6` gates scores and not a policy's shape.

    A document may be edited; what this checks is that if the sentence goes, the
    suite goes red with it.
    """
    text = _flat(STAGE_B)
    for phrase in (
            "does not require",
            "gates a score",
            "n/a DISQUALIFIES",
            "ungated diagnostic"):
        require(phrase in text,
                "STAGE-B.md no longer states %r — the restraint and the two "
                "readings it depends on are what keep this battery from "
                "asserting more than §5 L6 does" % (phrase,))

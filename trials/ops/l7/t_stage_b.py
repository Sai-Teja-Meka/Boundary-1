"""ops/l7 — the Layer-7 Stage-B wiring, checked engine-free.

`ascension/l7/t_generation.py` is entirely engine-gated by design, and
`inheritance/l7` all but one trial. That is the sanctioned trials-before-engine
split, and it has one hazard: a battery nobody can run is a battery nobody can
check. These trials are the half of Stage B that **can** be run today — the
instrument, the declared vocabulary, the lineage reading, the denominator
declaration and the document — so the frozen battery cannot be quietly wrong
about the things it does not need an engine to be right about.

None of them applies a `§5` clause to anything. There is no gate constant in this
file, and there is nothing here for `laws/t_rulings.py` to authorize.
"""

import os
from fractions import Fraction

from _harness import require, require_equal

import _l7score
import _l7tasks

STAGE_B = os.path.join(_l7tasks.PROJECT_ROOT, "trials/ascension/l7/STAGE-B.md")

# The two query operations the artifact speaks (`STAGE-B.md §2`). One is Layer
# 7's own and one is a Layer-4 verb, and the second is not decoration: it is what
# keeps `§3.4`'s denominator from being a function of the generation class alone,
# which is the property `R8` clause 6 rests on.
DECLARED_OPS = ("current", "generate")


def _flat(path):
    with open(path, "r", encoding="utf-8") as fh:
        return " ".join(fh.read().split())


# ---- one instrument --------------------------------------------------------

def trial_the_layer7_scorer_and_the_stage_a_arithmetic_share_one_instrument():
    """An engine and a policy are measured by ONE ruler, and it is the same object.

    `_l7score` computes nothing of its own: `brier`, `ece`, `auroc`, `fidelity`
    and `permille` are imported from `_l7tasks`, which imports them from
    `_l6tasks` unchanged — the functions the exhibited witness, the oracle, both
    crimes, both hedgers and every named capability-free baseline are scored by,
    and the same functions `_l6score` scores a Layer-6 engine by. This asserts the
    **identity** rather than the agreement, because two functions that agree on
    today's inputs are not one instrument.

    It is the discipline `_l4score` set and `_l5score` and `_l6score` restated,
    and at Layer 7 it is load-bearing in a new way: `R8` clause 1's baseline table
    records `make_engine(6)` and the blanket hedger as **one measurement**, and
    the humility ceiling is measured on an engine while Stage A's row is measured
    on a policy. They can only be the same number if they are the same function.
    """
    for name in ("brier", "ece", "auroc", "fidelity", "permille"):
        require(getattr(_l7score, name) is getattr(_l7tasks, name),
                "_l7score.%s is not _l7tasks.%s — a Layer-7 engine and a Layer-7 "
                "policy would then be scored by two rulers that merely agree"
                % (name, name))
    import _l6tasks
    for name in ("brier", "ece", "auroc", "fidelity", "permille"):
        require(getattr(_l7tasks, name) is getattr(_l6tasks, name),
                "_l7tasks.%s is not _l6tasks.%s — a Layer-6 Brier and a Layer-7 "
                "Brier would then be two functions of the same shape of input, "
                "and the two layers' numbers would need a caveat about the ruler"
                % (name, name))


def trial_an_empty_denominator_is_n_a_and_never_a_perfect_score():
    """`R8` clause 3(c) on the instrument itself, before any engine reaches it.

    The whole fourth species is one line of arithmetic: a ratio whose denominator
    is 0. `_l7score._ratio` returns `None` there and never `1`, which is the
    difference between *refusing to certify* and *certifying vacuously* — the
    null-exemption `autopsy/writ` was convicted of (`evaluator.ts:545-548`, where
    a declared-absent capability leaves BOTH numerator and denominator) reduced to
    the one place it could enter this project's own gate.

    Checked here rather than only through an engine, because the engine that
    would exhibit it is the one that generates nothing, and an engine that
    generates nothing is exactly what a Layer-7 gate must not certify.
    """
    require(_l7score._ratio(0, 0) is None,
            "an empty denominator must read n/a — R8 clause 3(c) makes that a "
            "DISQUALIFICATION, and a 0/0 read as 1 would hand a perfect score to "
            "a policy with no capability at all")
    require_equal(_l7score._ratio(0, 4), Fraction(0),
                  "a zero numerator over a real denominator is 0 and not n/a — "
                  "the stricter diagnostic reads exactly this for a "
                  "retrieval-only policy, where the gated number reads n/a")
    require_equal(_l7score._ratio(3, 4), Fraction(3, 4), "an ordinary ratio")


# ---- the declared vocabulary, the lineage reading, the denominator ---------

def trial_the_declared_query_vocabulary_is_the_one_the_battery_speaks():
    """`STAGE-B.md §2`: two query shapes, one of them a Layer-4 verb.

    A Layer-7 battery asks the questions the layers below answer **and** the ones
    only composition can answer, and `R8` clause 2 makes the second a `query` op
    rather than a fourth verb, so `§7.1`'s three doors stand and
    `trials/adapters/INTERFACE.md` — copied verbatim from `§7` and used to grade
    every foreign engine — stays true.

    Asserted over the frozen records, so an artifact that introduced a third
    operation would go red here rather than reach an engine through a scorer that
    had never seen it. The `generate` cue's own shape is asserted too: it carries
    a `cue` object and nothing else, because a class readable off the query's
    **shape** is `PRE-READ.md §6.3`'s predicted fifth substrate kill, and the one
    thing an artifact must not do is hand `tagging = 1000` to a lookup.
    """
    b = _l7score.battery()
    ops = sorted({rec["q"]["op"] for rec in b["records"]})
    require_equal(tuple(ops), DECLARED_OPS,
                  "the artifact speaks query operations %r; the declared "
                  "vocabulary is %r" % (ops, list(DECLARED_OPS)))
    shapes = {}
    for rec in b["records"]:
        q = rec["q"]
        if q["op"] == "generate":
            require_equal(sorted(q), ["cue", "op"],
                          "qid %d: a generate query carries a cue and nothing "
                          "else" % (rec["qid"],))
            require_equal(sorted(q["cue"]), ["entity", "kind"],
                          "qid %d: the cue's shape" % (rec["qid"],))
        else:
            require_equal(sorted(q), ["entity", "key", "op"],
                          "qid %d: a current query's shape" % (rec["qid"],))
        shapes.setdefault(q["op"], set()).add(rec["declared"])

    require_equal(sorted(shapes["generate"]), ["G", "O", "U"],
                  "every declared class must appear behind the SAME query shape "
                  "— a generation-required class recognisable from the query "
                  "alone would hand tagging = 1000 to a lookup, which is the "
                  "fifth substrate kill PRE-READ.md §6.3 predicted and "
                  "ops/l7/t_l7compose.py's labeller bench measures at exactly "
                  "%d errors for every reader that tries" % (_l7tasks.PAIRS,))


def trial_the_lineage_vocabulary_is_r8_clause_4s_and_absence_is_lawful():
    """`R8` clause 4's item-property, and the one thing it is not.

    *"`§4.2.3`'s `kind` says how an answer reached the caller. `§5 L7`'s
    `generated` says what the item is. The two are orthogonal properties of
    different objects, so the closed vocabulary is not violated and no fifth kind
    is minted."*

    So two things must be true of the reading the battery applies, and neither is
    a `§5` clause: the lineage vocabulary is closed at two values, and the four
    `§4.2.3` kinds are **untouched** by it. And a third, which is the restraint —
    an **absent** lineage is lawful and is scored as untagged, because that is
    exactly the answer `§5 L7` prices when it says *an untagged generation is a
    fabrication*. Making absence a harness failure would convert a scored clause
    into an exception and put the capital crime outside the score.
    """
    require_equal(_l7score.LINEAGE_VOCAB, ("observed", "generated"),
                  "the lineage vocabulary is closed at R8 clause 4's two values")
    from laws.t_provenance_schema import KIND_VOCAB
    require_equal(tuple(KIND_VOCAB), ("recall", "aggregate", "derive", "absent"),
                  "§4.2.3's closed four-kind vocabulary must be untouched — R8 "
                  "clause 4 mints no fifth kind, which is the whole reason "
                  "`generated` is a property of the ITEM")
    for lineage in _l7score.LINEAGE_VOCAB:
        require(lineage not in KIND_VOCAB,
                "a lineage value collided with a §4.2.3 kind (%r): the two "
                "vocabularies describe different objects and must not be "
                "readable as each other" % (lineage,))


def trial_every_query_class_declares_whether_it_scores_inside_the_denominator():
    """`R7` clause 2, carried forward and made a check on the battery.

    *"Every battery declares for each query class whether it scores inside the
    denominator and why."* `_l7score.DENOMINATOR` is that declaration;
    `_l7score._bundle` refuses an artifact whose classes it does not cover; this
    asserts the other half — that the declaration is right about which classes
    are answerable, so *outside the denominator* means *unanswerable* and never
    *inconvenient*.

    At this layer one of the two outside classes is `KU1`, a **generation-shaped**
    unanswerable probe, which is a class no earlier artifact here has had: the
    declared rule does not determine an item, so composing anything is the
    fabrication `§3.0` prices at 0. Being outside `§3.4`'s denominator is a
    property of the honest behaviour and not an exemption from measurement.
    """
    b = _l7score.battery()
    declared = _l7score.DENOMINATOR[b["name"]]
    seen = {}
    for rec in b["records"]:
        answerable = seen.setdefault(rec["class"], rec["answerable"])
        require_equal(rec["answerable"], answerable,
                      "class %s mixes answerable and unanswerable queries, so no "
                      "single declaration can be true of it" % (rec["class"],))
    for cls, (inside, why) in sorted(declared.items()):
        require_equal(inside, seen[cls],
                      "class %s is declared %s §3.4's denominator but is "
                      "%sanswerable — a class is outside because an abstention "
                      "carries no confidence to calibrate, and for no other "
                      "reason"
                      % (cls, "inside" if inside else "outside",
                         "" if seen[cls] else "un"))
        require(why.strip() != "", "class %s declares no reason" % (cls,))


def trial_the_generation_class_is_the_artifacts_and_the_ratios_denominators_are_stated():
    """`R8` clause 3(b): which denominator is the artifact's, and which are not.

    The one artifact-bound denominator is `tagging`'s — the declared **G**
    queries — and it is what fences the other two, because an engine that
    testified to fewer generated items would fail a numerator rather than shrink
    a denominator. So the battery must read that class off the artifact and never
    off an engine, and this asserts it does: the generation class is the frozen
    record's own `declared == "G"`, its size is the artifact's, and the humility
    conjunction's denominator is the **whole** of it (clause 7).
    """
    b = _l7score.battery()
    from_records = tuple(rec["qid"] for rec in b["records"]
                         if rec["declared"] == "G")
    require_equal(b["generation_class"], from_records,
                  "the generation class the scorer uses is not the artifact's "
                  "own declared class")
    require_equal(len(from_records), 160,
                  "the declared generation-required class is 160 queries — the "
                  "denominator of tagging_all and of the humility conjunction, "
                  "and the numerator of R8 clause 8(b)'s g > 1/18 precondition")
    g = _l7tasks.generation_share()
    require(g > _l7tasks.hedger_bound(),
            "the generation-required share %s is not above R8 clause 8(b)'s "
            "1/18 precondition, so a blanket hedger would survive F ≥ 950 and "
            "the gate would bind on an artifact where the escape §3.0 offers had "
            "not been priced out" % (g,))


# ---- the document ----------------------------------------------------------

def trial_stage_b_records_the_figures_the_instrument_computes():
    """Docs are checked, not trusted (`R6` clause 3: the trial's value is enforced).

    `STAGE-B.md §6` records what the capped engine measures and what the
    artifact's classes are. The class figures are recomputed here from the frozen
    records; the capped-engine figures are owned and asserted by
    `humility/l7/t_generation.py`, which measures them on the engine, and are
    required verbatim in the document so prose and measurement cannot drift apart
    silently.
    """
    b = _l7score.battery()
    counts = {"G": 0, "O": 0, "U": 0}
    for rec in b["records"]:
        counts[rec["declared"]] += 1

    lines = (
        "CAPPED conjunction 0 F_core 883 F_all 894 ece 0",
        "DENOM A 1740 n_pos 1740 n_neg 0 abstentions 460 N %d" % (b["n"],),
        "CLASS G %d O %d U %d answerable %d"
        % (counts["G"], counts["O"], counts["U"], b["n_answerable"]),
        "LEDGER validity n/a novelty n/a tagging n/a tagging_all 0",
    )
    text = _flat(STAGE_B)
    for line in lines:
        require(line in text,
                "STAGE-B.md no longer records `%s` — the document and the "
                "instrument have come apart, and under R6 clause 3 the "
                "instrument is the enforced value" % (line,))


def trial_stage_b_states_the_restraints_and_the_divergence_it_found():
    """The restraints are part of the record, not a footnote a later session can drop.

    Layer 5's Stage B recorded one over-tightening it caught and removed; Layer
    6's declined to require the tie's own 500. This session caught **three**, and
    all three were found by running the battery against a mock rather than by
    reading it — `tagging_all` required at 1000, the promotion ladder requiring
    all 160 at every rung, and relevance checked over the whole declared class
    instead of over the answers the engine tagged. Each would have gated
    something `§5 L7` does not, and each would have killed the `k = 111` hedger
    `R8` clause 3(e)'s own arithmetic admits.

    It also records the occupancy divergence under `R6` clause 3 — the document
    says 91 233, the engine measures 91 226, the trial's value is the enforced
    one and the prose stands as written — and the ledger finding that only a mock
    could surface: `query` is pure, so a lineage ledger is written by `ingest`.

    A document may be edited; what this checks is that if those sentences go, the
    suite goes red with them.
    """
    text = _flat(STAGE_B)
    for phrase in (
            "binds nothing",
            "`n/a` DISQUALIFIES",
            "ungated diagnostic",
            "91 226",
            "written by `ingest`",
            "not exercised and not closed"):
        require(phrase in text,
                "STAGE-B.md no longer states %r — the restraints, the recorded "
                "divergence and the two readings this battery depends on are "
                "what keep it from asserting more than §5 L7 does" % (phrase,))

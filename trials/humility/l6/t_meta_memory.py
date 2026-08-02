"""humility/l6 — Layer 6 (Meta-memory) humility (BOUNDARY.md §6, §5 L6).

Runs Layer 6's **own** battery — `_l6score` over `corpora/l6batteryb`, the same
instrument and the same artifact `ascension/l6/t_meta_memory.py` will be scored
by — against the capped engine `make_engine(layer_cap = 5)`, the Prospection
engine, through the same generic interface (`§7`). The declared ceiling is
`§5 L6`'s:

```
capped AUROC ≤ 600
```

and the measurement is **500**, against a gate of 900. The structural argument is
`IMPOSSIBILITY.md`.

**GREEN this session, and that is the point of the split.** Pre-Layer-6,
`make_engine(5)` *is* the whole engine, so a capped run sitting at chance is the
very fact the gate needs Layer 6 for. The primary check runs against
`adapters/l5` (present since Layer 5 was claimed); an engine-gated confirmation
against the Layer-6 engine *built and then capped to 5* skips until Stage C and
then holds forever — the shape `humility/l4` and `humility/l5` both use.

## The artifact is BOUND, and by the same clause that binds the gate

`BOUNDARY-RULINGS.md R7` clause 1 binds **both sides** of the Layer-6 gate —
ascension **and** humility — to `corpora/l6batteryb`, in one clause, for `R6`
clause 1's reason: a ceiling measured on one artifact beside a gate cleared on
another is two facts about two worlds. `corpora/l6battery` is **demoted** to an
ungated diagnostic by the same clause and this ceiling is not measured there.

## No convention is supplied, and none is needed

`§5.1 L6` defends the ceiling by saying a capped engine *"carries no confidence
model, so the harness scores it **confident-by-default**"*, and the `[L5] [PULSE]`
pre-read flagged that sentence as the half most likely to be wrong: a convention
living in a defense sentence might make the humility side a measurement of the
harness rather than of an engine. **It is not.** The frozen Layer-5 engine emits
its confidence through `§7.2` **itself** — the distinct values it returns over all
2 400 queries are exactly `{0, 1000}` — so the harness reads the engine's own
field and supplies nothing. `README-l5 §4` wrote that down one layer early and as
a structural fact rather than a placeholder: *"every answer this engine returns
carries `confidence = 1000` … that is not a placeholder an engine could tighten;
it is what the state can support."*

## What the ceiling costs to measure, stated rather than hidden

The whole 12 000-event replay plus all 2 400 queries costs **~1.5 s** at
`DEFAULT_BUDGET`. No prefix ladder is declared and none is needed — worth
contrasting with `humility/l4`, where the capped engine was Layer 3's
`O(retained)`-per-write eviction path and the whole-stream run cost 663 s and had
to be carried by a declared doubling ladder.

## Why the measurement is 500 and not merely low

`AUROC` is a **ranking** statistic (`§3.4`, the Mann–Whitney form) and a constant
confidence ranks nothing: every correct×incorrect pair ties, ties count ½, so
`AUROC = 1/2` **exactly** whenever both classes are non-empty. The ceiling of 600
is not approached from below by a poor model; it is **sat at by arithmetic**. And
the residual `README-l5 §4` named — that `§3.4` leaves `AUROC` undefined when a
class is empty, so *"the Layer-6 humility battery needs a query class this engine
gets wrong, or its ceiling is vacuous rather than loose"* — is what the forcing
region buys: 100 errors that no reading of the frozen bytes can remove.
"""

from fractions import Fraction

from _harness import require, require_equal, try_import
from adapters import l5

import _l6btasks
import _l6score

CEILING_AUROC = 600      # §5 L6 humility ceiling (R7 clause 1 binds the artifact)
GATE_AUROC = 900         # §5 L6, the gate the ceiling must sit strictly below

CAPPED_LAYER = 5

ARTIFACT = "l6batteryb"

# What the capped engine measures on the binding artifact, recorded so a drift is
# one red. Every figure is exact; the permille rendering is §3.5's.
#
#   Brier  1/22   -> 45   a constant 1000 against a wrong share of 1/22
#   ECE    1/22   -> 45   one bin, mean confidence 1, accuracy 21/22
#   AUROC  1/2    -> 500  a constant ranks nothing: every pair ties, ties count ½
#   F_core 21/22  -> 955  it CLEARS §5 L6's fidelity clause, and that is the point
#   F_all  23/24  -> 958  the ungated diagnostic over the whole query set
RECORDED_CAPPED = {
    "brier": Fraction(1, 22),
    "ece": Fraction(1, 22),
    "auroc": Fraction(1, 2),
    "F_core": Fraction(21, 22),
    "F_all": Fraction(23, 24),
}
RECORDED_PERMILLE = {"brier": 45, "ece": 45, "auroc": 500,
                     "F_core": 955, "F_all": 958}
RECORDED_DENOMINATOR = {"A": 2200, "n_pos": 2100, "n_neg": 100}
RECORDED_OCCUPANCY = 91119

# The confidence the capped engine emits through §7.2 itself: 1000 on every
# answer, 0 on every abstention. A THIRD value would mean a confidence model had
# appeared below Layer 6.
CONFIDENT_BY_DEFAULT = (0, 1000)

_RUNS = {}


def _measure(engine, label):
    if label not in _RUNS:
        b = _l6score.BATTERIES[ARTIFACT]()
        state, budget = _l6score.replay(
            engine, lambda cap: engine.make_engine(CAPPED_LAYER, cap), b,
            engine.DEFAULT_BUDGET)
        rows = _l6score.observe(engine, state, b)
        _RUNS[label] = (state, budget, rows, _l6score.score(rows, b), b)
    return _RUNS[label]


def _assert_ceiling(engine, label):
    state, budget, rows, r, b = _measure(engine, label)

    require(r["auroc"] is not None,
            "%s: the capped engine's AUROC is n/a — §3.4 leaves it undefined "
            "when a class is empty, and a ceiling measured on an undefined "
            "statistic is vacuous rather than loose. The forcing region exists "
            "so this cannot happen: R7 clause 3(b)" % (label,))
    require(_l6score.permille(r["auroc"]) <= CEILING_AUROC,
            "%s: the capped engine reaches AUROC %d against the §5 L6 humility "
            "ceiling of %d — the Layer-6 gate would then be approachable without "
            "a confidence model at all"
            % (label, _l6score.permille(r["auroc"]), CEILING_AUROC))
    require_equal(r["auroc"], RECORDED_CAPPED["auroc"],
                  "%s: the capped engine's AUROC is no longer exactly 1/2. A "
                  "constant confidence ranks NOTHING — every correct×incorrect "
                  "pair ties and §3.4 counts a tie as ½ — so 500 is sat at by "
                  "arithmetic and not approached from below" % (label,))
    require(_l6score.permille(r["auroc"]) < GATE_AUROC,
            "%s: the capped engine cleared the §5 L6 gate's AUROC clause"
            % (label,))
    require_equal(budget["B"], 1000,
                  "%s: the capped run breached the budget law (peak %d, cap %d)"
                  % (label, budget["peak"], budget["cap"]))
    require_equal(r["fabricated"], 0,
                  "%s: the capped engine answered %d unanswerable probes. §7.3 "
                  "is the cardinal rule — capability absence surfaces as a "
                  "scored abstention" % (label, r["fabricated"]))
    return state, budget, rows, r, b


# ---- the ceiling, against the layer directly below --------------------------

def trial_the_capped_prospection_engine_cannot_reach_the_auroc_ceiling():
    """`capped AUROC ≤ 600` (§5 L6; R7 clause 1), measured **500** on `make_engine(5)`.

    `§5.1 L6` defends the ceiling: *"A capped engine below Layer 6 carries no
    confidence model, so the harness scores it confident-by-default; the
    calibration bound then fails by construction, with AUROC ≤ 600 as the
    measured ceiling."* Every word of that is measured here rather than assumed —
    including *confident-by-default*, which is read off `§7.2` and not supplied.

    The ceiling binds on `corpora/l6batteryb` by `R7` clause 1, in the **same
    clause** that binds the ascension gate there, which is what makes this a
    discrimination rather than a fact about an artifact nobody's gate is stated
    on.
    """
    _assert_ceiling(l5, "make_engine(5) via adapters/l5")


def trial_the_capped_engine_emits_a_constant_pair_through_the_answer_itself():
    """*Confident-by-default* is the ENGINE's own field, not a harness convention.

    The `[L5] [PULSE]` pre-read named this the half of its prediction most likely
    to be wrong: `§5.1 L6`'s *"the harness scores it confident-by-default"* is a
    convention living in a defense sentence, and taken literally it would hand
    the ceiling its number before anything was measured. The measurement settles
    it — the frozen Layer-5 engine emits `{0, 1000}` through `§7.2` over all
    2 400 queries, 1000 on every answer and 0 on every abstention, so the harness
    reads a field the engine already fills and invents nothing.

    That is also the whole of the impossibility, stated as data rather than as an
    argument: **a two-valued constant is not a confidence model.** The values do
    not vary with anything, least of all with how likely an answer is to be
    right, because `README-l5 §4` records that the evidence the layer below keeps
    is binary — an event is regenerated exactly or it is not — and *"every answer
    it gives is one it has proved"*.
    """
    _state, _budget, rows, r, _b = _measure(l5, "make_engine(5) via adapters/l5")
    require_equal(r["confidences"], CONFIDENT_BY_DEFAULT,
                  "the capped engine's confidence vocabulary is no longer the "
                  "constant pair {0, 1000}: a third value below Layer 6 would "
                  "mean a confidence model had appeared where §3.4 is dormant "
                  "and README-l5 §4 says the state cannot support one")

    answers = [row for row in rows if row["status"] == "answer"]
    hedges = [row for row in rows if row["status"] == "abstain"]
    require(all(row["confidence"] == 1000 for row in answers),
            "an answer carried a confidence other than 1000")
    require(all(row["confidence"] == 0 for row in hedges),
            "an abstention carried a non-zero confidence")
    require(len(answers) > 0 and len(hedges) > 0,
            "both branches must occur or the constant pair is not exhibited")


def trial_the_capped_engine_fails_the_gate_on_calibration_and_not_on_fidelity():
    """**Where** the capped engine fails is the layer, and it is measured.

    Three of `§5 L6`'s five clauses are failed and two are cleared, and the split
    is exactly the boundary Layer 6 draws:

    * `Brier 45` and `ECE 45` against 40 and 30 — **failed**, by the same
      arithmetic in both cases: one bin, one confidence, and a wrong share of
      `1/22` the constant cannot express;
    * `AUROC 500` against 900 — **failed** by 400 permille, and by arithmetic
      rather than by margin;
    * `F 955` against 950 — **cleared**, and `B 1000` — **cleared**.

    The capped engine is not bad at remembering. It answers 2 100 of 2 200
    answerable queries correctly, abstains on all 200 unanswerable ones, fabricates
    nothing and holds the budget. What it cannot do is **say how sure it is** —
    and `§3.0` cannot see the difference, because it is confidence-blind: a
    calibrated hedge and a confident lie score the same there. That is why
    `§3.4` binds from Layer 6 and why the humility ceiling is stated on `AUROC`
    and not on `F`.
    """
    _state, _budget, _rows, r, _b = _measure(l5, "make_engine(5) via adapters/l5")

    require(r["brier"] > Fraction(40, 1000),
            "the capped engine cleared Brier ≤ 40 with a constant confidence")
    require(r["ece"] > Fraction(30, 1000),
            "the capped engine cleared ECE ≤ 30 with a constant confidence")
    require(r["auroc"] < Fraction(900, 1000),
            "the capped engine cleared AUROC ≥ 900 with a constant confidence")
    require(r["F_core"] >= Fraction(950, 1000),
            "the capped engine FAILS §5 L6's fidelity clause too, which would "
            "make the ceiling a measurement of retention rather than of "
            "calibration — measured %s" % (r["F_core"],))

    for field, want in sorted(RECORDED_CAPPED.items()):
        require_equal(r[field], want,
                      "the capped engine's %s drifted from the recorded exact "
                      "figure" % (field,))
    for field, want in sorted(RECORDED_PERMILLE.items()):
        require_equal(_l6score.permille(r[field]), want,
                      "the capped engine's %s permille rendering drifted" % (field,))


def trial_the_ceiling_is_measured_on_a_denominator_the_engine_cannot_empty():
    """`R7` clauses 2 and 3(b): the ceiling's own `A`, `n_pos` and `n_neg`.

    A humility ceiling stated on `AUROC` is only a ceiling if `AUROC` is defined,
    and `README-l5 §4` said so before this battery existed: *"the Layer-6
    humility battery needs a query class this engine gets wrong, or its ceiling
    is vacuous rather than loose."* Round 1 bought that class with murk's
    contradictions and bought it **for the declared reading only**; battery-b
    buys it with a forcing region the capped engine cannot get right **for any
    reading**, which is why `R7` demoted the first artifact and bound this one.

    The capped engine's 100 errors are exactly one member of every mirror pair —
    it is a latest-wins reader, one of the six on
    `t_attainability_b.py`'s bench, and the bench measures all six at exactly
    100. It is therefore incapable in the ordinary way rather than in a way this
    artifact arranged: no reading available to it moves the number.
    """
    _state, _budget, rows, r, b = _measure(l5, "make_engine(5) via adapters/l5")

    _l6score.assert_denominator_declared(r, rows, b)
    for field, want in sorted(RECORDED_DENOMINATOR.items()):
        require_equal(r[field], want,
                      "the ceiling's %s drifted — R7 clause 2 requires it stated "
                      "beside the triple, and a ceiling measured on a moving "
                      "denominator is not a ceiling" % (field,))

    profile = _l6score.region_profile(rows, b)
    require_equal(len(profile), _l6btasks.PAIRS, "the forcing region")
    require(not _l6score.resolved_pairs(profile),
            "the capped engine resolved a mirror pair, which Theorem 2 makes "
            "impossible from the stream alone")
    region_wrong = sum(row["answered"] - row["correct"] for row in profile.values())
    require_equal(region_wrong, _l6btasks.PAIRS,
                  "the capped engine errs on exactly one member of every mirror "
                  "pair — it is the bench's `latest-wins` reader, and all six "
                  "readers on that bench measure exactly %d"
                  % (_l6btasks.PAIRS,))
    require_equal(r["n_neg"], region_wrong,
                  "all of the capped engine's error mass must be the forcing "
                  "region: the base stream is clean by construction")


def trial_the_capped_run_is_in_budget_and_the_confidence_model_cost_nothing():
    """`B = 1000` at `DEFAULT_BUDGET`, and the occupancy the ceiling is measured at.

    Recorded because `ATTAINABILITY-B.md §3.2` prices a confidence model at **18
    cells** beyond exactly this state — one set-once flag per attribute key, with
    every other declared feature reading off the interval table the engine
    already holds. The capped engine's occupancy is the baseline that price is
    stated against, so a drift in it would move a number `R7`'s evidence section
    carries.
    """
    _state, budget, _rows, r, b = _measure(l5, "make_engine(5) via adapters/l5")
    require_equal(budget["B"], 1000, "the capped run breached the budget law")
    require_equal(budget["refused"], 0,
                  "%d writes were refused at DEFAULT_BUDGET" % (budget["refused"],))
    require_equal(budget["occupancy"], RECORDED_OCCUPANCY,
                  "the capped engine's occupancy on battery-b drifted from the "
                  "figure R7's evidence section records")
    require_equal(budget["next_t"], b["n_events"],
                  "battery-b carries no intention, so one ingest is one t (R6 "
                  "clause 2's f = 0 case, of an engine)")
    require_equal(r["wrong"] + r["n_pos"], r["A"],
                  "the answered queries must partition into right and wrong")


# ---- the engine-gated confirmation (Stage C) --------------------------------

def trial_the_layer6_engine_capped_to_five_is_identically_incapable():
    """§7.4: capping is a construction-time restriction, not an imitation.

    SKIPS until `adapters/l6` exists, then holds forever. It is the check that
    `make_engine(5)` built from the *Layer-6* engine measures what
    `make_engine(5)` built from the Layer-5 engine measures — because `§7.4` says
    a capped engine *"speaks the identical interface and still surfaces missing
    capability as scores"*, and an engine that satisfied its own humility trial
    by having a slightly different capped mode would satisfy nothing at all.

    At this layer the check has a sharper edge than usual, and it is the one a
    Layer-6 engine is most likely to fail by accident: the capped mode must also
    emit the **constant pair** through `§7.2`. An engine whose confidence model
    leaked into its capped construction would report a calibrated number from a
    layer that has no evidence to calibrate on, and would be measuring its own
    Layer-6 machinery against a Layer-5 ceiling.
    """
    l6 = try_import(
        "adapters.l6",
        "no L6 engine yet; the capped-from-above confirmation engages at Stage C "
        "(the primary ceiling above runs against adapters/l5 today)")
    _s6, _b6, _rows6, r6, _bundle6 = _assert_ceiling(
        l6, "make_engine(5) via adapters/l6")
    _s5, _b5, _rows5, r5, _bundle5 = _measure(l5, "make_engine(5) via adapters/l5")

    for field in ("brier", "ece", "auroc", "F_core", "A", "n_pos", "n_neg"):
        require_equal(r6[field], r5[field],
                      "the Layer-6 engine capped to 5 measures %s = %r where the "
                      "Layer-5 engine capped to 5 measures %r — §7.4 capping is "
                      "a restriction, not a re-implementation"
                      % (field, r6[field], r5[field]))
    require_equal(r6["confidences"], CONFIDENT_BY_DEFAULT,
                  "the Layer-6 engine capped to 5 emits a confidence vocabulary "
                  "the Layer-5 engine does not: the confidence model leaked "
                  "through the cap, and the ceiling would then be measuring "
                  "Layer 6 against itself")

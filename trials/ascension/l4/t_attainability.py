"""ascension/l4 — the Layer-4 attainability arithmetic (BOUNDARY-RULINGS.md R2).

R2 obligation 3: the oracle ceiling and every named baseline are *"computed and
written into that layer's `ATTAINABILITY.md`, and machine-checked by a trial that
goes red if any recorded number drifts, **before** the gate is treated as
binding."* This is that trial. It is the ascension-side counterpart of
`humility/*/IMPOSSIBILITY.md`, and it runs today, with no engine in existence.

**BOUNDARY-RULINGS.md R4 has since ratified what this file computed**, on all
three questions Stage A put up: `footprint ≤ 250` is permille of the raw episodic
footprint (clause 2), state is priced under rule P (clause 3), and the Layer-4
ascension gate binds on `corpora/l4stream` with chronicle and murk scored as
ungated diagnostics (clause 1). The thresholds themselves are untouched, as R1
left Layer 3's. `RULING-R4-DRAFT.md` is retained as the draft of record and is
superseded by the frozen entry.

**No gate is applied to any engine here even so.** The §5 L4 thresholds appear
below because the question *this file* answers is whether a corpus admits them —
R2 obligations 1 and 2 in exact arithmetic — and it answers it with no engine in
existence. The Stage-B battery that applies them to one
(`t_consolidation.py`, `humility/l4/`) is unwritten, in the order R2's standing
step fixes: attainability arithmetic → trials → engine.

## What is asserted

1. **Discrimination on `corpora/l4stream`** — the gate lies strictly below an
   *exhibited* state's scores and strictly above every named capability-free
   baseline, and the §5 L4 humility ceiling is neither breached nor vacuous.
2. **Non-attainability on the chronicle family** — every ceiling recorded in
   `ATTAINABILITY.md §5`, and the finding that a history-free current-value table
   nearly ties chronicle's own optimum, so a gate bound there would fail R2
   obligation 2 even if it were reachable.
3. **Every recorded number** — each figure in `ATTAINABILITY.md` re-derived and
   compared, so the document cannot drift away from the corpora it describes.

The skip mechanism R1 ruled permanent — *a deferral must state the condition that
lifts it, in code* — is what
`trial_the_chronicle_family_cannot_admit_the_layer4_gate` implements from the
other side: it asserts the ceilings are **below** the gate, so if a corpus family
ever changed such that the arithmetic admitted the gate, this trial goes red and
the corpus choice is reopened by itself.
"""

from fractions import Fraction

import _l4tasks
from _harness import require, require_equal

# The ratified §5 L4 thresholds, unchanged, bound to `corpora/l4stream` by
# BOUNDARY-RULINGS.md R4. Registered in `laws/t_rulings.py` against the §5 L4
# clauses they are quoted from and against R4; see `AUTHORIZED_GATES`.
GATE_FOOTPRINT = 250
GATE_RECONSTRUCTION_F = 900
GATE_C = 850
GATE_B = 1000
CEILING_RECONSTRUCTION_F = 400

BINDING_CANDIDATE = "l4stream"
DIAGNOSTIC_CANDIDATES = ("chronicle", "murk")


# ---- the recorded arithmetic (ATTAINABILITY.md) ----------------------------
#
# corpus -> every number the document states. A drift in any one is red.

RECORDED = {
    "l4stream": {
        "n": 20000, "raw_cells": 173200, "budget_cap": 43300,
        "entities": 200, "pairs": 2951, "assertions": 18788, "irreducible": 1212,
        "n_q1": 2951, "n_q2": 15837, "n_q3": 205, "n_coverage": 18993,
        "minimal_sufficient_cells": 40737, "minimal_sufficient_permille": 235,
        "spare_cells": 2563,
        "oracle_C": 1000, "oracle_F": 984,
    },
    "chronicle": {
        "n": 50000, "raw_cells": 395632, "budget_cap": 98908,
        "entities": 9985, "pairs": 41785, "assertions": 50000, "irreducible": 0,
        "n_q1": 41785, "n_q2": 8215, "n_q3": 9990, "n_coverage": 59990,
        "minimal_sufficient_cells": 151780, "minimal_sufficient_permille": 384,
        "spare_cells": -52872,
        "oracle_C": 735, "oracle_F": 683,
    },
    "murk": {
        "n": 10000, "raw_cells": 79446, "budget_cap": 19861,
        "entities": 1798, "pairs": 7519, "assertions": 9810, "irreducible": 190,
        "n_q1": 7519, "n_q2": 2291, "n_q3": 1804, "n_coverage": 11614,
        "minimal_sufficient_cells": 28949, "minimal_sufficient_permille": 364,
        "spare_cells": -9088,
        "oracle_C": 754, "oracle_F": 711,
    },
}

# corpus -> policy -> (coverage permille, F permille), as ATTAINABILITY.md tabulates.
RECORDED_BASELINES = {
    "l4stream": {
        "verbatim-truncation-latest": (247, 325),
        "verbatim-truncation-first": (249, 327),
        "current-value-table-only": (155, 100),
        "capped-layer_cap-3": (200, 325),
    },
    "chronicle": {
        "verbatim-truncation-latest": (208, 325),
        "verbatim-truncation-first": (208, 325),
        "current-value-table-only": (697, 100),
        "capped-layer_cap-3": (226, 344),
    },
    "murk": {
        "verbatim-truncation-latest": (210, 324),
        "verbatim-truncation-first": (212, 327),
        "current-value-table-only": (647, 100),
        "capped-layer_cap-3": (225, 344),
    },
}


def _check_recorded(name):
    b = _l4tasks.corpus(name)
    o = _l4tasks.oracle(name)
    want = RECORDED[name]
    got = {
        "n": b["n"], "raw_cells": b["raw_cells"], "budget_cap": b["budget_cap"],
        "entities": len(b["entities"]), "pairs": len(b["chains"]),
        "assertions": b["assertions"], "irreducible": len(b["irreducible"]),
        "n_q1": b["n_q1"], "n_q2": b["n_q2"], "n_q3": b["n_q3"],
        "n_coverage": b["n_coverage"],
        "minimal_sufficient_cells": o["minimal_sufficient_cells"],
        "minimal_sufficient_permille": o["minimal_sufficient_permille"],
        "spare_cells": o["spare_cells"],
        "oracle_C": o["max_coverage_permille"],
        "oracle_F": o["max_reconstruction_F_permille"],
    }
    for key in sorted(want):
        require_equal(got[key], want[key],
                      "%s: %s drifted from ATTAINABILITY.md" % (name, key))


# ---- 1. the footprint reading -------------------------------------------

def trial_the_footprint_gate_is_the_budget_cap():
    """`footprint ≤ 250` read in permille of the raw episodic footprint (§1).

    The reading is defended in `ATTAINABILITY.md §1` from three ratified
    sentences and **ratified by BOUNDARY-RULINGS.md R4 clause 2**, together with
    rule P (clause 3), without which a cell count means nothing at all. What is
    asserted here is only its arithmetic consequence: the gate and the §4.1
    budget cap are the same number, so `B = 1000` and `footprint ≤ 250` are one
    constraint certified twice — once after every write, once on the final state.
    """
    for name in _l4tasks.CORPORA:
        b = _l4tasks.corpus(name)
        require_equal(b["budget_cap"], b["raw_cells"] // 4,
                      "%s: the Layer-4 budget cap is not a quarter of the raw "
                      "episodic footprint" % (name,))
        require_equal(
            _l4tasks.permille(Fraction(b["budget_cap"], b["raw_cells"])),
            GATE_FOOTPRINT,
            "%s: a state exactly filling the budget cap does not measure %d‰ — "
            "the footprint gate and the budget law have come apart"
            % (name, GATE_FOOTPRINT))


def trial_the_reconstruction_gate_is_the_literal_section_3_0_table():
    """`F ≥ 900` under the literal table ⟺ 8/9 of events reconstructed exactly.

    R3 does not reach Layer 4 (its own text says so), so no ruling was needed to
    score `F` this way and none was requested — **R4 clause 4 records that the
    concession was available, examined and declined**, because the exhibited
    witness clears the gate under the literal table (984 ≥ 900) without it. The
    equivalence is asserted rather than asserted-in-prose so that a later session
    cannot quietly adopt the friendlier reading without a ruling: under the
    corruption reading an honest abstention scores 1000 and this identity would
    fail at once.

    The identity is exact on the **Fraction**, which is where §3.1 defines `F`.
    The §5 gate is applied to the permille *calibration* of it (§3.5), and
    round-half-to-even therefore admits an exact `F` as low as **899.5‰** — half
    a permille point below the identity's threshold, which on `l4stream` is 11
    events of 20 000. That slack is asserted **in the measure** rather than in
    events, because half a permille is a property of §3.5 while events-per-
    permille is a property of a corpus's scale.
    """
    ninety = Fraction(9, 10)
    for name in _l4tasks.CORPORA:
        n = _l4tasks.corpus(name)["n"]

        def f_exact(x, n=n):
            return Fraction(x * 1000 + (n - x) * 100, n * 1000)

        threshold = -(-8 * n // 9)          # ceil(8n/9), the exact-answer floor
        require(f_exact(threshold) >= ninety,
                "%s: reconstructing ceil(8n/9)=%d events exactly does not reach "
                "F = 9/10" % (name, threshold))
        require(f_exact(threshold - 1) < ninety,
                "%s: one event short of ceil(8n/9) already reaches F = 9/10 — "
                "the 8/9 identity in ATTAINABILITY.md §2 is wrong" % (name,))

        # The rounded gate, and exactly how much the rounding rule concedes.
        least = threshold
        while least > 0 and \
                _l4tasks.permille(f_exact(least - 1)) >= GATE_RECONSTRUCTION_F:
            least -= 1
        require_equal(_l4tasks.permille(f_exact(least)), GATE_RECONSTRUCTION_F,
                      "%s: the least state clearing the rounded gate does not "
                      "calibrate to the gate itself" % (name,))
        require(f_exact(least) >= Fraction(2 * GATE_RECONSTRUCTION_F - 1, 2000),
                "%s: the permille gate admits an exact F of %s, below the "
                "899.5‰ that §3.5's round-half-to-even concedes — the gate is "
                "looser than the rounding rule allows"
                % (name, f_exact(least)))


# ---- 2. discrimination on the proposed binding corpus --------------------

def trial_l4stream_admits_the_gate_with_an_exhibited_state():
    """R2 obligation 1, by exhibition rather than by family argument.

    A concrete state — the exact interval table, the global counters, and as many
    irreducible events as the remaining cells buy — fits inside the 250‰ budget
    and scores C and F strictly above the gate. No modelling assumption about
    what a policy *could* do is needed for this half of R2.

    **R4 clause 5 makes this form the preferred practice**, forward-binding
    alongside R2: where a concrete witness state can be constructed, a Stage-A
    oracle ceiling is to be exhibited rather than merely argued, and the family
    maximization that agrees with it (`C ≤ 1000`, `F ≤ 984`) is thereby a check
    on the maximization rather than a substitute for the witness.
    """
    w = _l4tasks.witness(BINDING_CANDIDATE)
    require(w is not None,
            "no state in the family answers l4stream's battery inside its "
            "footprint — the corpus this session froze does not admit the gate "
            "it was built for")
    require_equal(w["footprint_permille"], GATE_FOOTPRINT,
                  "the witness state no longer fills the footprint exactly")
    require(w["cells"] <= _l4tasks.corpus(BINDING_CANDIDATE)["budget_cap"],
            "the witness state exceeds the budget cap (%d cells)" % (w["cells"],))
    require(w["coverage_permille"] > GATE_C,
            "l4stream witness C=%d does not lie strictly above the %d gate"
            % (w["coverage_permille"], GATE_C))
    require(w["F_permille"] > GATE_RECONSTRUCTION_F,
            "l4stream witness reconstruction-F=%d does not lie strictly above "
            "the %d gate" % (w["F_permille"], GATE_RECONSTRUCTION_F))
    require_equal(w["coverage_permille"], RECORDED["l4stream"]["oracle_C"],
                  "the witness no longer attains the recorded coverage ceiling")
    require_equal(w["F_permille"], RECORDED["l4stream"]["oracle_F"],
                  "the witness no longer attains the recorded fidelity ceiling")
    # And the loss is real: the irreducible tier is not fully affordable, so the
    # F gate measures honest lossy compression rather than a corpus with nothing
    # to lose.
    require(w["irreducible_stored"] < w["irreducible_total"],
            "every irreducible event fits — reconstruction would be lossless and "
            "the F gate would bite on nothing")


def trial_no_capability_free_baseline_clears_the_gate_on_l4stream():
    """R2 obligation 2: the gate strictly above **every named** baseline.

    Named and scored, not waved at — an unnamed baseline is an unchecked one.
    Each is a trial fixture in `_l4tasks`, never engine code, so the policies
    guarded against never exist in `core/`.
    """
    for r in _l4tasks.baselines(BINDING_CANDIDATE):
        require(r["coverage_permille"] < GATE_C,
                "baseline %s scores C=%d on l4stream, at or above the %d gate — "
                "the gate would not require consolidation"
                % (r["policy"], r["coverage_permille"], GATE_C))
        require(r["F_permille"] < GATE_RECONSTRUCTION_F,
                "baseline %s scores reconstruction-F=%d on l4stream, at or above "
                "the %d gate" % (r["policy"], r["F_permille"],
                                 GATE_RECONSTRUCTION_F))


def trial_the_capped_engine_ceiling_is_honest_on_l4stream():
    """§5 L4 humility: `capped reconstruction F ≤ 400 at footprint ≤ 250`.

    Checked from both sides. The arithmetic bound on the `layer_cap = 3` engine
    must lie **below** the ceiling — otherwise the ceiling is breached by the
    corpus alone — and must not lie so far below that the ceiling is vacuous;
    the ratified defense sentence says the capped engine *"has simply lost
    three-quarters of its episodes"*, and that is asserted as the episode share
    rather than trusted.
    """
    r = _l4tasks.baseline_capped_l3(BINDING_CANDIDATE)
    require(r["F_permille"] <= CEILING_RECONSTRUCTION_F,
            "the layer_cap=3 arithmetic bound reaches reconstruction-F=%d, above "
            "the §5 L4 humility ceiling of %d — the ceiling is breached by the "
            "corpus before any engine exists"
            % (r["F_permille"], CEILING_RECONSTRUCTION_F))
    require(r["F_permille"] > 100,
            "the capped bound sits at the abstention floor, so the ceiling "
            "distinguishes nothing")
    require_equal(r["episodes_kept_permille"], GATE_FOOTPRINT,
                  "the capped engine no longer holds a quarter of the episodes "
                  "at a quarter of the footprint — §5.1 L4's 'lost "
                  "three-quarters of its episodes' is the defense this measures")


# ---- 3. the chronicle family cannot admit the gate ----------------------

def trial_the_chronicle_family_cannot_admit_the_layer4_gate():
    """The finding this session exists to record (ATTAINABILITY.md §5).

    Stated as strict inequalities in the direction of the finding, so the
    deferral states the condition that lifts it, in code (R1 clause 5): if
    either corpus ever became redundant enough to admit the gate, this goes red
    and the Layer-4 corpus choice is reopened without any session's permission.

    **R4 clause 1 ratified this as the first of two causes**, and the second —
    the discrimination failure asserted by the trial below — is independent of
    it. A repair that made this trial go red would not by itself license a
    Layer-4 gate on the chronicle family; R4 says so in the entry rather than
    leaving it to be inferred here.
    """
    for name in DIAGNOSTIC_CANDIDATES:
        o = _l4tasks.oracle(name)
        require(not o["joint_feasible"],
                "%s: the exact interval table now fits inside 250‰ (%d ≤ %d) — "
                "the ATTAINABILITY.md §5 finding is resolved and the Layer-4 "
                "corpus binding must be revisited"
                % (name, o["minimal_sufficient_cells"], o["budget_cap"]))
        require(o["max_coverage_permille"] < GATE_C,
                "%s: the coverage ceiling reached %d, at or above the %d gate — "
                "this corpus now admits the gate" % (
                    name, o["max_coverage_permille"], GATE_C))
        require(o["max_reconstruction_F_permille"] < GATE_RECONSTRUCTION_F,
                "%s: the reconstruction ceiling reached %d, at or above the %d "
                "gate" % (name, o["max_reconstruction_F_permille"],
                          GATE_RECONSTRUCTION_F))
        require(_l4tasks.witness(name) is None,
                "%s: a state now answers the whole battery inside the footprint"
                % (name,))


def trial_chronicle_cannot_tell_consolidation_from_a_table_of_last_writes():
    """R1's second consequence, arriving one layer up (ATTAINABILITY.md §5).

    On `l3stream` a keep-latest ring buffer *tied* the optimum, so that corpus
    could not distinguish an importance ordering from an arrival ordering. On
    chronicle the current-value table — no history, no as-of, no interval, no
    pattern fold — reaches **95%** of the arithmetic optimum, and on murk
    **86%**. Even if either ceiling reached the gate, R2 obligation 2 would void
    a gate bound there.

    The contrast with `l4stream`, where the same policy reaches 155 against a
    1000 ceiling — **16%** — is asserted alongside so the finding is a
    comparison rather than an isolated number.

    **R4 clause 1 records this as the second cause, recorded verbatim beside the
    first and voiding a gate bound there on its own** — *"either cause alone
    voids a gate bound there"*. It is the cause that survives a repair of the
    footprint arithmetic, which is why it is a separate trial and not a remark
    inside the one above.
    """
    for name in DIAGNOSTIC_CANDIDATES:
        o = _l4tasks.oracle(name)
        cv = _l4tasks.baseline_current_value_table(name)
        require(Fraction(cv["coverage_permille"], o["max_coverage_permille"])
                > Fraction(4, 5),
                "%s: the history-free current-value table no longer comes within "
                "80%% of the oracle (%d vs %d) — the reason this corpus cannot "
                "carry the Layer-4 gate has changed"
                % (name, cv["coverage_permille"], o["max_coverage_permille"]))

    o4 = _l4tasks.oracle(BINDING_CANDIDATE)
    cv4 = _l4tasks.baseline_current_value_table(BINDING_CANDIDATE)
    require(Fraction(cv4["coverage_permille"], o4["max_coverage_permille"])
            < Fraction(1, 4),
            "on l4stream the history-free table now reaches a quarter of the "
            "oracle (%d vs %d) — the corpus has lost the property it was built "
            "for" % (cv4["coverage_permille"], o4["max_coverage_permille"]))


# ---- 4. every recorded number ------------------------------------------

def trial_recorded_attainability_numbers_do_not_drift():
    """R2 obligation 3, and the arithmetic BOUNDARY-RULINGS.md R4 rests on.

    R4 records two independent causes for refusing a Layer-4 gate on the
    chronicle family, and both are numbers in this table: the footprint
    arithmetic (chronicle's exact history schema at `151 780` cells = `384‰`
    against a `98 908`-cell budget, because `35 947` of `41 785` pairs are
    asserted once and identification does not compress) and the discrimination
    failure asserted by
    `trial_chronicle_cannot_tell_consolidation_from_a_table_of_last_writes`.
    A ruling is only as frozen as the figures it cites, so every one of them is
    re-derived from the frozen corpora here and a drift in any is red.
    """
    for name in _l4tasks.CORPORA:
        _check_recorded(name)


def trial_recorded_baseline_scores_do_not_drift():
    """The named-baseline half of the same obligation (R2 obligation 2, R4).

    R4 clause 1 tabulates these scores as the ground on which the gate binds to
    `corpora/l4stream` — 249/327 for the strongest verbatim truncation, 155/100
    for the history-free current-value table, 200/325 for the capped
    `layer_cap = 3` bound under the ratified 400 ceiling. Each is a trial fixture
    in `_l4tasks`, never engine code, so the policies the gate guards against
    never exist in `core/`.
    """
    for name in _l4tasks.CORPORA:
        want = RECORDED_BASELINES[name]
        got = {r["policy"]: (r["coverage_permille"], r["F_permille"])
               for r in _l4tasks.baselines(name)}
        require_equal(sorted(got), sorted(want),
                      "%s: the set of named baselines changed — R2 obligation 2 "
                      "requires every one of them named and scored" % (name,))
        for policy in sorted(want):
            require_equal(got[policy], want[policy],
                          "%s: baseline %s drifted from ATTAINABILITY.md"
                          % (name, policy))


def trial_the_oracle_dominates_every_baseline_everywhere():
    """A consistency check on the arithmetic itself, not on any corpus.

    A ceiling that some baseline exceeds is not a ceiling. This runs on all three
    corpora, so an error in the construct-family maximization shows up as a red
    trial rather than as a flattering number in a document.
    """
    for name in _l4tasks.CORPORA:
        o = _l4tasks.oracle(name)
        for r in _l4tasks.baselines(name):
            require(r["coverage_permille"] <= o["max_coverage_permille"],
                    "%s: baseline %s scores C=%d above the recorded ceiling %d — "
                    "the ceiling is not a bound"
                    % (name, r["policy"], r["coverage_permille"],
                       o["max_coverage_permille"]))
            require(r["F_permille"] <= o["max_reconstruction_F_permille"],
                    "%s: baseline %s scores F=%d above the recorded ceiling %d"
                    % (name, r["policy"], r["F_permille"],
                       o["max_reconstruction_F_permille"]))

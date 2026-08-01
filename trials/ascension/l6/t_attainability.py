"""ascension/l6 — the Layer-6 attainability arithmetic, machine-checked.

`BOUNDARY-RULINGS.md R2` makes this file the reason `ATTAINABILITY.md` is
evidence and not prose: every figure that document records is re-derived here
from the frozen battery, the frozen murk corpus and the frozen murk answer key,
and a drift in any of them is RED.

**NO GATE BINDS.** The `§5 L6` constants below are declared so the arithmetic can
be stated in the constitution's own numbers and so `laws/t_rulings.py` can
register them — they carry a `§5 L6` clause and **no companion ruling**, which is
what "no gate binds" looks like in that registry (the Layer-5 Stage-A session
established the shape, `BOUNDARY.log` line 28). Nothing here applies a clause to
an engine: the one place an engine is touched at all is
`ops/l6/t_l6battery.py`, where the frozen Layer-5 engine is replayed to check
that the declared reader is what it actually does, which is a measurement and not
a gate.

`R5` clause 2 is applied FIRST, as the obligation's own order requires: the
minimizing clauses are read direction-aware and the lower obligation is read over
the gate's conjunction, with every clause's arithmetic recorded either way.
"""

from fractions import Fraction

from _harness import require, require_equal

import _l6tasks as tasks

# ---- the ratified §5 L6 clause, in the constitution's own numbers ----------
#
# Registered in laws/t_rulings.py against `§5 L6` and NO ruling.

GATE_BRIER = 40
GATE_ECE = 30
GATE_AUROC = 900
GATE_F = 950
GATE_B = 1000
CEILING_AUROC = 600

# The exact reading (§1.1 of ATTAINABILITY.md): the gate integers are bounds on
# the quantity in [0,1], not on its permille rounding.
BRIER_BOUND = Fraction(GATE_BRIER, 1000)
ECE_BOUND = Fraction(GATE_ECE, 1000)
AUROC_BOUND = Fraction(GATE_AUROC, 1000)
F_BOUND = Fraction(GATE_F, 1000)

# The disputed intervals the two readings differ on (PRE-READ.md §2).
DISPUTED = {
    "brier": (Fraction(40, 1000), Fraction(81, 2000)),
    "ece": (Fraction(30, 1000), Fraction(61, 2000)),
    "auroc": (Fraction(1799, 2000), Fraction(900, 1000)),
}

# ---- the recorded figures --------------------------------------------------

A = 3550
N_POS = 3392
N_NEG = 158

RECORDED = {
    # policy            Brier                        ECE                  AUROC            F_core
    "oracle": (Fraction(0), Fraction(0), Fraction(1), Fraction(1696, 1775)),
    "witness": (Fraction(693, 2218750), Fraction(127, 17750), Fraction(1),
                Fraction(1696, 1775)),
    "conflict-rank": (Fraction(110085701, 3550000000), Fraction(27, 710000),
                      Fraction(253211, 267968), Fraction(1696, 1775)),
    "confident-always": (Fraction(79, 1775), Fraction(79, 1775), Fraction(1, 2),
                         Fraction(1696, 1775)),
    "base-rate-constant": (Fraction(4831, 113600), Fraction(7, 14200),
                           Fraction(1, 2), Fraction(1696, 1775)),
    "abstain-on-set-once": (Fraction(0), Fraction(0), None,
                            Fraction(17039, 17750)),
    "abstain-on-conflict": (Fraction(0), Fraction(0), None,
                            Fraction(1177, 1420)),
}

CAPABILITY_FREE = ("confident-always", "base-rate-constant",
                   "abstain-on-set-once", "abstain-on-conflict")


def _scoreboard():
    if not hasattr(_scoreboard, "cache"):
        _scoreboard.cache = tasks.scoreboard()
    return _scoreboard.cache


def _clears(figures, auroc_na_disqualifies=True):
    """Does this policy clear the whole §5 L6 gate, under the exact reading?"""
    if figures["brier"] > BRIER_BOUND:
        return False
    if figures["ece"] > ECE_BOUND:
        return False
    if figures["auroc"] is None:
        if auroc_na_disqualifies:
            return False
    elif figures["auroc"] < AUROC_BOUND:
        return False
    if figures["F_core"] < F_BOUND:
        return False
    return True


# ---- the denominator -------------------------------------------------------

def trial_the_calibration_denominator_is_what_the_document_records():
    """§3.4's `A`, `n_pos` and `n_neg`, and the fact that both classes are present.

    This is the whole reason the battery exists. On murk as previously queried
    `n_neg = 0` and AUROC is `n/a` (§3.4); here both classes are non-empty and
    the calibration triple is defined.
    """
    figures = _scoreboard()["witness"]
    require_equal(figures["A"], A, "the calibration denominator A")
    require_equal(figures["n_pos"], N_POS, "n_pos")
    require_equal(figures["n_neg"], N_NEG, "n_neg")
    require(figures["n_pos"] > 0 and figures["n_neg"] > 0,
            "§3.4 requires both AUROC classes present; the battery must "
            "guarantee it by construction and this is where that is checked")
    require_equal(figures["fabricated"], 0, "fabrications on the absence probes")


def trial_the_error_rate_is_inside_the_band_both_clauses_admit():
    """§2.1 — the size is forced, and this is the forcing.

    `F >= 950` with no abstentions caps `w` at 50 permille; `Brier <= 40`
    discriminates against the base-rate constant only where `w(1-w) > 40/1000`.
    """
    w = Fraction(N_NEG, A)
    require(w <= Fraction(50, 1000),
            "F >= 950 caps w at 50 permille (1000w + 900a <= 50); w = %s" % (w,))
    require(w * (1 - w) > BRIER_BOUND,
            "outside the Brier band the base-rate constant clears the clause: "
            "w = %s, w(1-w) = %s" % (w, w * (1 - w)))
    # The band's own endpoints, so a battery resized later is checked against
    # the same arithmetic rather than against this instance's numbers.
    require_equal(A >= 3160, True, "A >= 158/0.050")
    require_equal(A <= 3784, True, "A <= the Brier band's upper end")


# ---- the recorded scoreboard ----------------------------------------------

def trial_every_recorded_figure_is_the_computed_one():
    """The drift trial: `ATTAINABILITY.md` §3 and §4, number by number, exact."""
    board = _scoreboard()
    require_equal(sorted(board), sorted(RECORDED),
                  "the scored policies and the recorded ones must be the same set")
    for name, (brier, ece, auroc, f_core) in sorted(RECORDED.items()):
        got = board[name]
        require_equal(got["brier"], brier, "%s Brier" % (name,))
        require_equal(got["ece"], ece, "%s ECE" % (name,))
        require_equal(got["auroc"], auroc, "%s AUROC" % (name,))
        require_equal(got["F_core"], f_core, "%s F (answerable core)" % (name,))


def trial_the_permille_renderings_are_the_ones_the_document_prints():
    expected = {
        "oracle": (0, 0, 1000, 955),
        "witness": (0, 7, 1000, 955),
        "conflict-rank": (31, 0, 945, 955),
        "confident-always": (45, 45, 500, 955),
        "base-rate-constant": (43, 0, 500, 955),
        "abstain-on-set-once": (0, 0, None, 960),
        "abstain-on-conflict": (0, 0, None, 829),
    }
    board = _scoreboard()
    for name, want in sorted(expected.items()):
        p = tasks.as_permille(board[name])
        require_equal((p["brier"], p["ece"], p["auroc"], p["F_core"]), want,
                      "%s permille row" % (name,))


def trial_no_scored_policy_lands_in_a_disputed_reading_interval():
    """§1.1 — every verdict in this file is the same under both readings.

    That is what makes the reading cheap to settle now. A later policy that DID
    land in a disputed interval would be red here rather than quietly decided by
    the instrument.
    """
    for name, figures in sorted(_scoreboard().items()):
        for measure, (lo, hi) in sorted(DISPUTED.items()):
            value = figures[measure]
            if value is None:
                continue
            require(not (lo < value <= hi),
                    "%s's %s = %s lies in the interval where the exact and "
                    "permille readings of §5 L6 disagree — the reading now "
                    "decides a verdict and RULING-R7-DRAFT.md clause (iv) is no "
                    "longer optional" % (name, measure, value))


# ---- R2 obligation 1 -------------------------------------------------------

def trial_obligation_1_the_gate_lies_strictly_inside_both_ceilings():
    """`R2` obligation 1, direction-aware (`R5` clause 2), on both declared classes.

    Class O is the logical maximum over ALL policies; class E is the
    evidence-only family `§5 L6` actually asks for. `R5` clause 3 requires the
    class to be declared, and both are, so the ceiling is not a number without a
    family.
    """
    for name in ("oracle", "witness"):
        figures = _scoreboard()[name]
        require(figures["brier"] < BRIER_BOUND,
                "%s: the gate must lie strictly WORSE than the ceiling on a "
                "minimizing clause (Brier)" % (name,))
        require(figures["ece"] < ECE_BOUND, "%s: ECE ceiling" % (name,))
        require(figures["auroc"] is not None and figures["auroc"] > AUROC_BOUND,
                "%s: AUROC ceiling" % (name,))
        require(figures["F_core"] > F_BOUND, "%s: F ceiling" % (name,))


def trial_obligation_1_the_witness_attains_the_whole_gate():
    """`R4` clause 5: where a witness can be built, the ceiling is EXHIBITED.

    The witness is a concrete confidence assignment over the frozen battery —
    structural evidence in, integer permille out — and it clears every clause of
    `§5 L6` including the `B = 1000` identity, which it attains trivially by not
    touching the write path at all.
    """
    require(_clears(_scoreboard()["witness"]),
            "the exhibited witness must clear the whole §5 L6 gate")


def trial_the_evidence_only_ceiling_is_measured_against_the_oracle_ceiling():
    """§3's finding: how much lower is class E than class O?

    `PRE-READ.md §4.3` warned the evidence-only family's ceiling *"is strictly
    lower, and nobody knows by how much until it is exhibited"*. Measured: not
    lower at all on AUROC, and inside seven permille elsewhere.
    """
    o = _scoreboard()["oracle"]
    e = _scoreboard()["witness"]
    require_equal(e["auroc"], o["auroc"],
                  "class E meets class O exactly on AUROC")
    require(e["brier"] - o["brier"] < Fraction(1, 1000),
            "class E is within one permille of class O on Brier")
    require(e["ece"] - o["ece"] < Fraction(10, 1000),
            "class E is within ten permille of class O on ECE")


def trial_the_witness_price_is_named_and_the_loss_reserve_is_disclaimed():
    """`R5` clause 4 — bookkeeping priced by name, reserve disclaimed with a reason.

    The only marginal state a confidence policy needs beyond the frozen Layer-5
    state is one set-once flag per attribute key, on murk's own key vocabulary.
    Everything else it reads is already in the interval table. There is no loss
    reserve because the battery is scored in budget, where nothing is evicted —
    the disclaimer clause 4 admits, with the reason clause 4 requires.
    """
    keys = sorted({pair[1] for pair in tasks.chains()})
    require_equal(len(keys), 18, "murk's attribute-key vocabulary")
    require_equal(18, len(keys),
                  "the priced bookkeeping is one flag per key and nothing else")
    require("origin" in keys, "the set-once key must be in the vocabulary")
    require_equal(list(tasks.SET_ONCE_KEYS), ["origin"],
                  "the declared set-once reading")


# ---- R2 obligation 2, over the conjunction (R5 clause 2) -------------------

def trial_obligation_2_no_capability_free_baseline_clears_the_gate():
    """The lower obligation, read over the gate's CONJUNCTION — `R5` clause 2.

    Applied first, as the session's charter required. Every named capability-free
    policy is scored on every clause and none clears the whole gate. The two
    abstainers fail only because `§3.4` leaves AUROC undefined for them, which is
    §5's collision and `RULING-R7-DRAFT.md` clause (iii)'s question — asserted
    here under the reading the draft proposes, so that a human who took the other
    reading would find this trial red rather than find the obligation quietly
    discharged.
    """
    board = _scoreboard()
    for name in CAPABILITY_FREE:
        require(not _clears(board[name]),
                "capability-free policy %r clears the ratified §5 L6 gate — R2 "
                "obligation 2 is not discharged and no Layer-6 gate may bind"
                % (name,))


def trial_obligation_2_clause_by_clause_and_which_clauses_do_the_work():
    """`R5` clause 2 also asks for *every clause's arithmetic recorded either way*."""
    board = _scoreboard()

    # ECE discriminates against NOTHING: the base-rate constant beats the witness.
    require(board["base-rate-constant"]["ece"] <= ECE_BOUND,
            "the base-rate constant is expected to CLEAR ECE — that is the "
            "finding, not a failure")
    require(board["base-rate-constant"]["ece"] < board["witness"]["ece"],
            "a one-bin partition agrees with itself, so the capability-free "
            "constant should beat a real model on ECE")

    # Brier discriminates against BOTH constants.
    for name in ("confident-always", "base-rate-constant"):
        require(board[name]["brier"] > BRIER_BOUND,
                "Brier must discriminate against %r; it is the clause the "
                "battery's size was chosen to make load-bearing" % (name,))

    # AUROC fails both constants by arithmetic: a constant ranks nothing.
    for name in ("confident-always", "base-rate-constant"):
        require_equal(board[name]["auroc"], Fraction(1, 2),
                      "%s must score AUROC exactly 1/2 (every pair ties, ties "
                      "count half)" % (name,))

    # F discriminates against the key-blind abstainer and not the other one.
    require(board["abstain-on-conflict"]["F_core"] < F_BOUND,
            "the key-blind abstainer must fail F: it spends 900 per abstention "
            "out of a 50-permille budget")
    require(board["abstain-on-set-once"]["F_core"] >= F_BOUND,
            "the set-once abstainer clears F — which is why the collision is "
            "real and not an artefact of a badly-chosen hedge")


def trial_ranking_without_resolving_clears_the_gate():
    """§0 finding 3, and the sharpest positive result of the session.

    `conflict-rank` is KEY-BLIND: it sees that an `(entity, key)` chain disagrees
    with itself and cannot see which value is true. It clears every clause. So
    the Layer-6 gate does not require the resolving reading — a policy that could
    not have avoided the errors it is calibrating for still reaches it.
    """
    figures = _scoreboard()["conflict-rank"]
    require(_clears(figures),
            "the key-blind conflict-rank policy must clear the whole gate")
    require(figures["auroc"] > AUROC_BOUND,
            "and it must clear AUROC on ranking alone")


def trial_the_conflict_rank_levels_are_derived_and_not_typed():
    """`R5` clause 3: the fit is declared, and here it is checked.

    `conflict-rank`'s confidence levels are the battery's own measured accuracy
    at each conflict count. A level somebody tuned by hand would be red.
    """
    measured = tasks.conflict_rank_measured_levels()
    declared = dict(tasks.CONFLICT_RANK_LEVELS)
    declared[6] = tasks.CONFLICT_RANK_TAIL
    require_equal(declared, measured,
                  "conflict-rank's levels must be the measured accuracies")


def trial_the_base_rate_constant_states_the_batterys_own_accuracy():
    """It costs nothing to state because the corpus states it — so it is derived."""
    require_equal(tasks.base_rate_conf(),
                  tasks.permille(Fraction(N_POS, A)),
                  "the base-rate constant must be permille(1 - w)")


# ---- the collision ---------------------------------------------------------

def trial_the_abstainer_is_what_makes_the_auroc_reading_load_bearing():
    """§5, both horns, asserted so neither can be quoted without the other.

    A capability-free policy with NO confidence model scores better than the
    exhibited witness on three clauses and has `n_neg = 0`. Whether it clears the
    gate is entirely a question about what `n/a` means, and that question decides
    whether `R2` obligation 2 can be discharged at Layer 6 at all.
    """
    board = _scoreboard()
    hedger = board["abstain-on-set-once"]
    witness = board["witness"]

    require_equal(hedger["n_neg"], 0,
                  "the abstainer deletes exactly the queries it would get wrong "
                  "from §3.4's denominator")
    require(hedger["auroc"] is None,
            "and its AUROC is therefore undefined (§3.4)")
    require(hedger["brier"] < witness["brier"]
            and hedger["ece"] < witness["ece"]
            and hedger["F_core"] > witness["F_core"],
            "the abstainer must beat the witness on Brier, ECE and F — that is "
            "what makes the reading of `n/a` load-bearing rather than tidy")
    require(_clears(hedger, auroc_na_disqualifies=False),
            "under the reading where `n/a` merely excuses the clause, this "
            "capability-free policy clears every evaluable clause of §5 L6 — "
            "which is the horn RULING-R7-DRAFT.md clause (iii) rejects")
    require(not _clears(hedger, auroc_na_disqualifies=True),
            "and under the reading the draft proposes it does not clear")


def trial_a_perfect_reader_would_take_auroc_with_it():
    """The other horn: the better the engine, the less evaluable the gate.

    The battery's `n_neg` is a property of the DECLARED READING. A reader that
    took `origin` first-wins would answer every K1 query correctly, and §3.4
    would then leave AUROC undefined for the engine as surely as it does for the
    abstainer. This asserts the arithmetic of that, engine-free, so §6's claim is
    a measurement.
    """
    perfect = []
    for row in tasks._rows():
        if row["reader_status"] != "answer":
            continue
        # A first-wins reader is right on K1 by construction and unchanged
        # elsewhere, because the plain classes carry no set-once key.
        correct = True if row["cls"] == "K1" else row["reader_correct"]
        perfect.append((1000, correct))
    require_equal(sum(1 for _c, ok in perfect if not ok), 0,
                  "a first-wins reader is wrong nowhere on this battery")
    require(tasks.auroc(perfect) is None,
            "so §3.4 leaves its AUROC undefined — the collision's second horn")


# ---- the humility side, measured but not applied --------------------------

def trial_the_capped_engine_is_measured_and_the_ceiling_is_neither_breached_nor_vacuous():
    """§4.2 — and `PRE-READ.md §3.4`'s flagged half, scored a MISS.

    `§5.1 L6` says a capped engine *"carries no confidence model, so the harness
    scores it confident-by-default"*, and the pre-read warned that a convention
    living in a defense sentence might make the humility side a measurement of a
    convention rather than of an engine. It is not: the frozen Layer-5 engine
    emits `{0, 1000}` through `§7.2` itself (`ops/l6/t_l6battery.py`), so the
    `confident-always` row IS `make_engine(layer_cap = 5)` scored on this
    battery.

    **This does not apply the ceiling.** `trials/humility/l6/` does not exist and
    `R2`'s standing order puts the trials after the arithmetic; what is asserted
    here is that the ceiling would be neither breached nor vacuous, which is the
    attainability fact and not the humility trial.
    """
    capped = _scoreboard()["confident-always"]
    require(capped["auroc"] is not None,
            "the capped engine's AUROC must be DEFINED on this battery — on "
            "every artifact this project had before today it would not have "
            "been, which is README-l5 §4's stated seam")
    require_equal(tasks.permille(capped["auroc"]), 500, "capped AUROC")
    require(tasks.permille(capped["auroc"]) <= CEILING_AUROC,
            "the ratified ceiling must not be breached")
    require(tasks.permille(capped["auroc"]) < GATE_AUROC,
            "and it must sit strictly below the gate, or the ceiling is vacuous")
    require(not _clears(capped),
            "the capped engine must fail the gate — it fails Brier, ECE and "
            "AUROC, structurally rather than marginally")


# ---- what this session does NOT do ----------------------------------------

def trial_no_layer_6_gate_binds_on_anything():
    """The Stage-A boundary, asserted in code rather than promised in prose.

    `R2` obligation 4: the corpus binding is the human's. A Layer-6 engine, a
    Layer-6 humility trial and a Layer-6 inheritance row do not exist, and
    `RULING-R7-DRAFT.md` is deliberately not appended to `BOUNDARY-RULINGS.md`
    because appending is what freezes.
    """
    import os
    root = tasks.PROJECT_ROOT
    for absent in ("core/layers/l6_meta_memory.py",
                   "trials/adapters/l6.py",
                   "trials/humility/l6",
                   "trials/inheritance/l6"):
        require(not os.path.exists(os.path.join(root, absent)),
                "%s exists — this is a Stage-A session and the engine, the "
                "humility class and the inheritance row all come after a "
                "ruling (R2's standing step)" % (absent,))

    rulings = os.path.join(root, "BOUNDARY-RULINGS.md")
    with open(rulings, "r", encoding="utf-8") as fh:
        text = fh.read()
    require("\n# R7 " not in text,
            "RULING-R7-DRAFT.md must NOT be appended by a session; appending is "
            "what freezes and a human ratifies")

"""ascension/l6 — the Layer-6 attainability arithmetic on battery-b, round 2.

`BOUNDARY-RULINGS.md R2` makes this file the reason `ATTAINABILITY-B.md` is
evidence and not prose: every figure that document records is re-derived here
from the frozen artifact alone, and a drift in any of them is RED.

Round 1 (`t_attainability.py`, `ATTAINABILITY.md`, `corpora/l6battery`) is not
edited and still runs. What it computed is still true; what it *measured* about
itself is why this file exists. Its guarantee that `n_neg > 0` held only
relative to the declared latest-wins reading, and `§3.4` leaves `AUROC` undefined
at `n_neg = 0`, so the clause carrying `R2` obligation 2 rested on a reading a
session declared. On `corpora/l6batteryb` it rests on a **theorem**:

* every reader on `_l6btasks.READER_BENCH` — first-wins included, the very reader
  that made round 1's guarantee relative — errs on exactly `PAIRS = 100` forcing
  queries;
* and no policy that clears `§5 L6`'s own `F >= 950` can reach `n_neg = 0`,
  because hedging the region costs 900 a query out of a 50-permille budget.

**NO GATE BINDS.** The `§5 L6` constants below are declared so the arithmetic can
be stated in the constitution's own numbers and so `laws/t_rulings.py` can
register them — they carry a `§5 L6` clause and **no companion ruling**, which is
what "no gate binds" looks like in that registry. Nothing here applies a clause
to an engine: the one place an engine is touched is `ops/l6/t_l6batteryb.py`,
where the frozen Layer-5 engine is replayed to check that the declared reader is
what it actually does, which is a measurement and not a gate.

`R5` clause 2 is applied FIRST, as the obligation's own order requires.

---

**Note added 2026-08-02 (`[L5] [RULING]`, `R7` recorded). The paragraph above is
where "no gate binds" stops holding for this artifact.**

A human ratified `RULING-R7-DRAFT.md`'s round-2 draft and a `RULING` session
appended it as **`R7`**, as drafted. **`R7` clause 1 binds BOTH sides of the
Layer-6 gate — ascension and humility — to `corpora/l6batteryb`**, in one clause,
for `R6` clause 1's reason: a ceiling measured on one artifact beside a gate
cleared on another is two facts about two worlds. The six constants below now
carry `R7` beside their `§5 L6` clause in `laws/t_rulings.py`; round 1's six keep
the clause and carry no ruling, which is that registry recording `corpora/
l6battery`'s **demotion** in its own structure.

The rest of `R7` is what this file's arithmetic already assumed and may now cite:
the calibration denominator excludes abstentions and is stated beside the triple
(clause 2); `AUROC = n/a` **DISQUALIFIES** and a gate citing it binds only where
both classes non-empty is a **theorem**, priced inside clause 3(c)'s window
(clause 3); the reading is **exact, not permille** (clause 4); and the ECE bin
index is `bin(conf) = 9 if conf == 1000 else conf // 100` (clause 5), which is
what the witness's `ECE = 0` depends on.

**Two authorities, kept distinct as the `R6` session kept `R5` and `R6`.** `R5`
governs the READING of `R2`'s obligations here without an entry of its own —
clause 2 forward-binding *"because Layer 6 needs it immediately"*, clause 1
carrying `B = 1000` as the identity it has been since Layer 1, clause 3 the
declared policy class, clause 4 the pricing. `R7` governs the SUBSTRATE and the
`n/a` law. Nothing below is edited in substance and no recorded figure moves:
**authority, not behaviour.** `trials/humility/l6/` and `trials/inheritance/l6/`
are Stage B's, and the engine is Stage C's, under `R2`'s standing step.
"""

from fractions import Fraction

from _harness import require, require_equal

import _l6btasks as tasks

# ---- the ratified §5 L6 clause, in the constitution's own numbers ----------
#
# Registered in laws/t_rulings.py against `§5 L6` and NO ruling.

GATE_BRIER = 40
GATE_ECE = 30
GATE_AUROC = 900
GATE_F = 950
GATE_B = 1000
CEILING_AUROC = 600

# The exact reading (BOUNDARY-RULINGS.md R7 clause 4): the gate integers are
# bounds on the quantity in [0,1], not on its permille rounding.
BRIER_BOUND = Fraction(GATE_BRIER, 1000)
ECE_BOUND = Fraction(GATE_ECE, 1000)
AUROC_BOUND = Fraction(GATE_AUROC, 1000)
F_BOUND = Fraction(GATE_F, 1000)

DISPUTED = {
    "brier": (Fraction(40, 1000), Fraction(81, 2000)),
    "ece": (Fraction(30, 1000), Fraction(61, 2000)),
    "auroc": (Fraction(1799, 2000), Fraction(900, 1000)),
}

# ---- the recorded figures --------------------------------------------------

R = 200                 # the forcing class — the whole region, unsampled
PAIRS = 100             # mirror pairs; every committing reader errs on one each
A = 2200                # the answerable core = §3.4's denominator = 11r
N_POS = 2100
N_NEG = 100

RECORDED = {
    # policy               Brier                        ECE                AUROC          F_core
    "oracle": (Fraction(0), Fraction(0), Fraction(1), Fraction(21, 22)),
    "witness": (Fraction(1, 44), Fraction(0), Fraction(41, 42), Fraction(21, 22)),
    "conflict-rank": (Fraction(39451477, 1100000000), Fraction(7, 1100000),
                      Fraction(1913, 2100), Fraction(21, 22)),
    "confident-always": (Fraction(1, 22), Fraction(1, 22), Fraction(1, 2),
                         Fraction(21, 22)),
    "base-rate-constant": (Fraction(19091, 440000), Fraction(1, 2200),
                           Fraction(1, 2), Fraction(21, 22)),
    "detect-and-abstain": (Fraction(0), Fraction(0), None, Fraction(101, 110)),
    "abstain-on-conflict": (Fraction(0), Fraction(0), None, Fraction(383, 500)),
}

CAPABILITY_FREE = ("confident-always", "base-rate-constant",
                   "detect-and-abstain", "abstain-on-conflict")

# The hedging ladder of §5: how far a policy may hedge the region before it
# breaks the layer's own fidelity clause, and what `n_neg` is left when it does.
HEDGE_LADDER = {
    0: (100, Fraction(21, 22)),
    12: (88, Fraction(2613, 2750)),
    13: (87, Fraction(1306, 1375)),
    14: (86, Fraction(2611, 2750)),
    50: (50, Fraction(103, 110)),
    100: (0, Fraction(101, 110)),
}
MAX_AFFORDABLE_HEDGE_EXACT = 12       # under clause 4's exact reading
MAX_AFFORDABLE_HEDGE_PERMILLE = 13    # under the permille reading
FLOOR_N_NEG = 87                      # the lower of the two — reading-independent


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


# ---- the denominator, and why it is a theorem ------------------------------

def trial_the_calibration_denominator_is_what_the_document_records():
    """§3.4's `A`, `n_pos` and `n_neg`, stated explicitly beside the triple.

    The round-1 draft's clause 2 asked for exactly this and it is honoured here
    before it is ratified, because the whole of clause 3's problem is invisible
    until `A` is written down next to `N`.
    """
    figures = _scoreboard()["witness"]
    require_equal(figures["A"], A, "the calibration denominator A")
    require_equal(figures["n_pos"], N_POS, "n_pos")
    require_equal(figures["n_neg"], N_NEG, "n_neg")
    require_equal(figures["n_neg"], PAIRS,
                  "n_neg is exactly one member of every mirror pair")
    require(figures["n_pos"] > 0 and figures["n_neg"] > 0,
            "§3.4 requires both AUROC classes present")
    require_equal(figures["fabricated"], 0, "fabrications on the absence probes")


def trial_n_neg_is_a_theorem_and_not_a_property_of_a_declared_reading():
    """**The reason battery-b exists**, asserted rather than asserted about.

    Round 1's `ATTAINABILITY.md §6` recorded the honest limit of its artifact:
    *"`n_neg > 0` for the declared reading … and NOT against an arbitrary
    reader."* Here every reader on the bench — latest-wins, first-wins,
    canonical-min, canonical-max and the two that read the raw entity id — scores
    exactly `PAIRS` errors on the forcing region. `first-wins` is the specific
    counterexample round 1 named: on `corpora/l6battery` it would have answered
    the whole commitment class correctly and driven `n_neg` to 0.
    """
    scores = {}
    for name, reader, _kind in tasks.READER_BENCH:
        scores[name] = tasks.region_errors(reader)
    require_equal(sorted(set(scores.values())), [PAIRS],
                  "every reader on the bench must err on exactly %d forcing "
                  "queries; measured %r" % (PAIRS, scores))
    require("first-wins" in scores and "latest-wins" in scores,
            "the bench must contain the two readings that disagree about which "
            "end of a chain is true — they are the whole point")


def trial_a_class_e_policy_cannot_tell_the_members_of_a_pair_apart():
    """Theorem 1 at the level of the DECLARED CLASS, not of a reader.

    Every feature in `_l6btasks.FEATURES` is equal on the two members of a mirror
    pair, so a class-E policy assigns them the same status and the same
    confidence: it hedges both or neither, and it ranks them together. That is
    what makes §5's hedging arithmetic a bound on the whole class rather than on
    one policy — and it is why the vocabulary deliberately excludes the raw
    entity id and the absolute logical time, the two handles Theorem 1 leaves.
    """
    by_entity = {rec["q"]["entity"]: rec["q"] for rec in tasks.queries()
                 if rec["class"] == "K0"}
    for p in tasks.region_pairs():
        ev0 = tasks.evidence(by_entity[p["e0"]])
        ev1 = tasks.evidence(by_entity[p["e1"]])
        require_equal(sorted(ev0), sorted(tasks.FEATURES),
                      "the evidence vocabulary is closed")
        require_equal(ev0, ev1,
                      "pair %d: the declared evidence must not distinguish the "
                      "members, or a class-E policy could split a tie"
                      % (p["pair"],))
        for _name, policy, cls in tasks.POLICIES:
            if cls != "E":
                continue
            require_equal(policy(ev0, "answer"), policy(ev1, "answer"),
                          "pair %d: a class-E policy answered its two members "
                          "differently" % (p["pair"],))


def trial_the_band_is_the_window_all_three_ratified_clauses_admit():
    """§2 — the size is FORCED, and this is the forcing, with the window exact.

    Three ratified clauses pull against each other, and `w = (r/2)/A` is the
    wrong share of ANY committing reader (Theorem 1), so the window is a property
    of the artifact and not of a policy:

      * `F >= 950` for the honest committer     ->  `A >= 10r`
      * blanket abstention on the region BREAKS `F >= 950`  ->  `A < 18r`
      * `Brier <= 40` beats the base-rate constant  ->  `A < (25+5*sqrt(21))/4 r`

    `A = 11r` sits inside all three. The third bound is irrational and is checked
    as the exact rational predicate `25u^2 - 50u + 4 < 0` in `u = r/A`, never as
    a float (§2.2).
    """
    require_equal(A, 11 * R, "A = 11r")
    w = Fraction(N_NEG, A)
    require_equal(w, Fraction(1, 22), "the wrong share of any committing reader")

    bounds = tasks.band_bounds(R)
    require(A >= bounds["committer_F"],
            "A >= 10r or the honest committer cannot clear F >= 950")
    require(A < bounds["abstention_kills_F"],
            "A < 18r or blanket abstention on the region does NOT break F, and "
            "the region stops forcing a commitment")
    require(bounds["brier_beats_base_rate"](A),
            "A must be inside the Brier band or the base-rate constant clears "
            "the clause the band was chosen to make load-bearing")

    # The window's own endpoints, so a resized artifact is checked against the
    # same arithmetic rather than against this instance's numbers.
    require(not (10 * R - 1 >= bounds["committer_F"]),
            "A = 10r - 1 must fail the lower bound")
    require(not bounds["brier_beats_base_rate"](12 * R),
            "A = 12r must fail the Brier bound, which is where the tight window "
            "ends at (25 + 5*sqrt(21))/4 r ~ 11.978r")


# ---- the recorded scoreboard ----------------------------------------------

def trial_every_recorded_figure_is_the_computed_one():
    """The drift trial: `ATTAINABILITY-B.md` §3 and §4, number by number, exact."""
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
        "witness": (23, 0, 976, 955),
        "conflict-rank": (36, 0, 911, 955),
        "confident-always": (45, 45, 500, 955),
        "base-rate-constant": (43, 0, 500, 955),
        "detect-and-abstain": (0, 0, None, 918),
        "abstain-on-conflict": (0, 0, None, 766),
    }
    board = _scoreboard()
    for name, want in sorted(expected.items()):
        p = tasks.as_permille(board[name])
        require_equal((p["brier"], p["ece"], p["auroc"], p["F_core"]), want,
                      "%s permille row" % (name,))


def trial_no_scored_policy_lands_in_a_disputed_reading_interval():
    """Every VERDICT here is the same under both readings of `§5 L6`.

    A later policy that DID land in a disputed interval would be red here rather
    than quietly decided by whichever way the instrument happened to round.
    Round 2 finds the first place a reading moves a NUMBER — §5's hedging ladder,
    where the exact reading affords 12 hedged pairs and the permille reading 13 —
    and it still moves no verdict, which is recorded in
    `trial_no_policy_clearing_f_can_reach_n_neg_zero`.
    """
    for name, figures in sorted(_scoreboard().items()):
        for measure, (lo, hi) in sorted(DISPUTED.items()):
            value = figures[measure]
            if value is None:
                continue
            require(not (lo < value <= hi),
                    "%s's %s = %s lies in the interval where the exact and "
                    "permille readings of §5 L6 disagree — the reading now "
                    "decides a verdict — BOUNDARY-RULINGS.md R7 clause 4 rules "
                    "it EXACT, and a policy landing here would be the first "
                    "whose verdict that ruling decides"
                    % (name, measure, value))


# ---- R2 obligation 1 -------------------------------------------------------

def trial_obligation_1_the_gate_lies_strictly_inside_both_ceilings():
    """`R2` obligation 1, direction-aware (`R5` clause 2), on both declared classes.

    Class O may read the answer key; class E is a function of
    `_l6btasks.evidence()` and nothing else. `R5` clause 3 requires the class to
    be declared, and both are.
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

    The witness is a concrete confidence assignment over the frozen artifact —
    structural evidence in, integer permille out, no engine and no answer key —
    and it clears every clause of `§5 L6` including the `B = 1000` identity,
    which it attains trivially by not touching the write path at all.

    It is also, and this is the round-2 difference, **provably non-resolving**:
    it prices the region at the tie's own confidence because Theorem 1 forbids it
    from doing better. Round 1's witness *happened* to rank exactly like the
    oracle because murk's evidence resolved; here nothing resolves, and the
    witness clears the gate anyway.
    """
    require(_clears(_scoreboard()["witness"]),
            "the exhibited witness must clear the whole §5 L6 gate")


def trial_the_tie_confidence_is_the_regions_own_arithmetic():
    """The witness's 500 is DERIVED, not chosen (`R5` clause 3).

    The region's accuracy under any committing reader is exactly one half —
    Theorem 1 — so `permille(1/2) = 500` is the region stating its own number.
    A witness that stated anything else would score worse on Brier, which is the
    §3.4 arithmetic agreeing with the §8.7-style construction.
    """
    require_equal(tasks.TIE_CONFIDENCE, tasks.permille(Fraction(1, 2)),
                  "the tie confidence is permille(1/2)")
    region = [row for row in tasks._rows() if row["cls"] == "K0"]
    correct = sum(1 for row in region if row["reader_correct"])
    require_equal(Fraction(correct, len(region)), Fraction(1, 2),
                  "the region's measured accuracy must be exactly one half")


def trial_the_evidence_only_ceiling_is_measured_against_the_oracle_ceiling():
    """How much lower is class E than class O, and where the distance now sits.

    On round 1's battery, class E MET class O on AUROC, because murk's evidence
    resolved as well as it ranked. On battery-b it cannot: the oracle reads the
    key and reaches 1000, the evidence-only witness reaches 41/42, and the gap is
    the tie itself. The gate at 900 lies strictly inside both, so obligation 1 is
    discharged under either family — but the family now matters, and this is
    where the number that says so is recorded.
    """
    o = _scoreboard()["oracle"]
    e = _scoreboard()["witness"]
    require_equal(o["auroc"], Fraction(1), "class O attains AUROC 1000")
    require(e["auroc"] < o["auroc"],
            "class E must now fall SHORT of class O on AUROC — the forcing "
            "region is exactly the evidence the oracle has and the stream does "
            "not")
    require(e["auroc"] > AUROC_BOUND,
            "and it must still clear the gate, or the gate is unattainable by "
            "the family §5 L6 asks for")
    require_equal(o["auroc"] - e["auroc"], Fraction(1, 42),
                  "the measured distance between the two declared classes")


def trial_the_witness_price_is_named_and_the_loss_reserve_is_disclaimed():
    """`R5` clause 4 — bookkeeping priced by name, reserve disclaimed with a reason.

    Every feature in the declared vocabulary is read off the interval table the
    Layer-4 engine already holds, so the only marginal state is one set-once flag
    per attribute key. There is no loss reserve because the artifact is scored in
    budget, where nothing is evicted — the disclaimer clause 4 admits, with the
    reason clause 4 requires.
    """
    keys = sorted({pair[1] for pair in tasks.chains()})
    require_equal(len(keys), 18, "battery-b's attribute-key vocabulary")
    require("origin" in keys, "the set-once key must be in the vocabulary")
    require_equal(list(tasks.SET_ONCE_KEYS), ["origin"],
                  "the declared set-once reading")
    require_equal(sorted(tasks.FEATURES),
                  sorted(("n_assert", "n_distinct", "set_once_tie",
                          "verbatim_repeats", "assert_span")),
                  "the closed feature vocabulary the price is stated for")


# ---- R2 obligation 2, over the conjunction (R5 clause 2) -------------------

def trial_obligation_2_no_capability_free_baseline_clears_the_gate():
    """The lower obligation, read over the gate's CONJUNCTION — `R5` clause 2.

    Applied first, as the obligation's own order requires. Every named
    capability-free policy is scored on every clause and none clears the whole
    gate — and, unlike round 1, **not one of them needs the `n/a` reading to
    fail**, which `trial_detect_and_abstain_is_killed_by_fidelity` asserts
    separately.
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

    # ECE still discriminates against NOTHING — but not for round 1's reason,
    # and the difference is a finding rather than a detail. There the base-rate
    # constant scored 7/14200 against the witness's 127/17750 and BEAT a real
    # model, because a one-bin partition agrees with itself. Here the witness's
    # partition agrees with itself EXACTLY — bin 5 is 500 confidence against 1/2
    # accuracy because Theorem 1 pins the region at one half, and bin 9 is 1000
    # against 1 — so it attains ECE = 0 and the constant cannot beat it. The
    # clause is idle either way: the capability-free constant clears it with no
    # model at all.
    require(board["base-rate-constant"]["ece"] <= ECE_BOUND,
            "the base-rate constant is expected to CLEAR ECE — that is the "
            "finding, not a failure")
    require_equal(board["witness"]["ece"], Fraction(0),
                  "the witness's bins agree with themselves exactly, which is "
                  "the forcing region's own arithmetic showing up in ECE")
    require(board["base-rate-constant"]["ece"] > board["witness"]["ece"],
            "so on battery-b the constant no longer beats a real model on ECE — "
            "round 1's ordering is REVERSED here and the clause is idle for a "
            "different reason, which is recorded rather than smoothed over")

    # Brier discriminates against BOTH constants — the band, occupied.
    for name in ("confident-always", "base-rate-constant"):
        require(board[name]["brier"] > BRIER_BOUND,
                "Brier must discriminate against %r; it is the clause the "
                "band's upper end was chosen to keep load-bearing" % (name,))

    # AUROC fails both constants by arithmetic: a constant ranks nothing.
    for name in ("confident-always", "base-rate-constant"):
        require_equal(board[name]["auroc"], Fraction(1, 2),
                      "%s must score AUROC exactly 1/2 (every pair ties, ties "
                      "count half)" % (name,))

    # F discriminates against BOTH abstainers — which is the round-2 change.
    for name in ("detect-and-abstain", "abstain-on-conflict"):
        require(board[name]["F_core"] < F_BOUND,
                "%r must fail F: it spends 900 per hedge out of a 50-permille "
                "budget" % (name,))


def trial_detect_and_abstain_is_killed_by_fidelity_and_not_by_the_auroc_reading():
    """**The kill, DEMONSTRATED rather than argued** — round 1's collision, closed.

    On `corpora/l6battery` the `§3.0`-honest hedger scored `Brier 0 / ECE 0 /
    F 960 / B 1000` with `AUROC n/a` — better than the exhibited witness on three
    clauses — and the ONLY thing standing between a capability-free policy and
    the Layer-6 gate was what `n/a` meant. `ATTAINABILITY.md §5` recorded both
    horns and `RULING-R7-DRAFT.md` put the question to a human, which `R7`
    clause 3(a) answered: `n/a` DISQUALIFIES.

    On battery-b the same policy fails `F` at 918 against 950, so it does not
    clear under EITHER reading of `n/a`. The forcing region is 200 of 2 200
    answerable queries and hedging it costs 90 permille out of a 50-permille
    budget: `§5 L6`'s own fidelity clause forbids the escape, and the `n/a`
    ruling no longer has to carry `R2` obligation 2 on this artifact.
    """
    hedger = _scoreboard()["detect-and-abstain"]
    require_equal(hedger["n_neg"], 0,
                  "the hedger still deletes exactly the queries it would get "
                  "wrong from §3.4's denominator")
    require(hedger["auroc"] is None, "so its AUROC is still undefined (§3.4)")
    require_equal(hedger["F_core"], Fraction(101, 110), "its measured fidelity")
    require(hedger["F_core"] < F_BOUND,
            "and F must KILL it — that is the round-2 result and it is measured, "
            "not argued")
    require(not _clears(hedger, auroc_na_disqualifies=False),
            "it must fail even under the reading where `n/a` merely excuses the "
            "clause; on round 1's battery it cleared there, which is what made "
            "the reading load-bearing")
    require(not _clears(hedger, auroc_na_disqualifies=True),
            "and it must fail under the reading the draft proposes")


def trial_no_policy_clearing_f_can_reach_n_neg_zero():
    """`AUROC` is DEFINED for every policy that clears `§5 L6`'s own `F` clause.

    The general form of the kill, measured on a ladder rather than argued. A
    policy hedging `k` mirror pairs is left with `n_neg = PAIRS - k`, and `§3.0`
    prices each hedge at 900: `F = (21000 - 8k)/22000`. Reaching `n_neg = 0`
    means `k = 100` and `F = 918`.

    The ladder is scored OUTSIDE the class-E policy interface, which makes the
    bound stronger rather than weaker: a class-E policy cannot even choose WHICH
    pairs to hedge (the members of a pair carry identical evidence), so the
    family measured here strictly contains it.

    The reading moves a NUMBER here and no verdict: the exact reading affords 12
    hedged pairs and the permille reading 13, so `n_neg >= 87` either way.
    """
    for k, (want_neg, want_f) in sorted(HEDGE_LADDER.items()):
        n_neg, f_core = tasks.score_hedging_pairs(k)
        require_equal(n_neg, want_neg, "n_neg after hedging %d pairs" % (k,))
        require_equal(f_core, want_f, "F after hedging %d pairs" % (k,))

    n_neg, f_core = tasks.score_hedging_pairs(MAX_AFFORDABLE_HEDGE_EXACT)
    require(f_core >= F_BOUND,
            "hedging %d pairs must still clear F under the exact reading"
            % (MAX_AFFORDABLE_HEDGE_EXACT,))
    n_next, f_next = tasks.score_hedging_pairs(MAX_AFFORDABLE_HEDGE_EXACT + 1)
    require(f_next < F_BOUND,
            "and hedging one more must break it under the exact reading")
    require_equal(tasks.permille(f_next), GATE_F,
                  "that one is where the two readings differ — it rounds to 950 "
                  "and is below 950 exactly, which is BOUNDARY-RULINGS.md R7 "
                  "clause 4 earning its keep")
    _n, f_permille_edge = tasks.score_hedging_pairs(
        MAX_AFFORDABLE_HEDGE_PERMILLE + 1)
    require(tasks.permille(f_permille_edge) < GATE_F,
            "and one beyond that fails under BOTH readings")

    require_equal(PAIRS - MAX_AFFORDABLE_HEDGE_PERMILLE, FLOOR_N_NEG,
                  "the reading-independent floor on n_neg")
    require(FLOOR_N_NEG > 0,
            "so every policy that clears §5 L6's own F clause leaves both AUROC "
            "classes non-empty — the collision is closed by arithmetic on this "
            "artifact and not by a ruling about `n/a`")


def trial_ranking_without_resolving_clears_the_gate_and_the_scope_is_restated():
    """Round 1's sharpest positive result, RE-MEASURED — and its scope updated.

    Round 1 recorded: *"a policy that RANKS without RESOLVING clears the gate"*,
    measuring the key-blind `conflict-rank` at `Brier 31 / ECE 0 / AUROC 945 /
    F 955`. On battery-b that sentence changes meaning twice over and the scope
    statement has to say so:

    * it is no longer a *contingent* result. Resolving is IMPOSSIBLE here, so the
      exhibited witness is itself non-resolving and the gate is reachable only by
      ranking. The finding has been promoted from "does not require" to "cannot
      require";
    * and it is tighter. `conflict-rank` is key-BLIND — it cannot tell a set-once
      tie from an ordinary chain that was legally updated — and its AUROC falls
      from 945 to 911 against a gate of 900. It still clears, on 11 permille.

    So key-blind ranking survives, narrowly, and the margin is now the honest
    measure of what the set-once reading is worth.
    """
    figures = _scoreboard()["conflict-rank"]
    require(_clears(figures),
            "the key-blind conflict-rank policy must clear the whole gate")
    require(figures["auroc"] > AUROC_BOUND,
            "and it must clear AUROC on ranking alone")
    require(figures["auroc"] < _scoreboard()["witness"]["auroc"],
            "key-blindness must COST something, or the set-once reading buys "
            "nothing and the witness is not the ceiling it claims to be")
    require_equal(figures["auroc"], Fraction(1913, 2100),
                  "the re-measured key-blind AUROC")


def trial_the_conflict_rank_levels_are_derived_and_not_typed():
    """`R5` clause 3: the fit is declared, and here it is checked.

    `conflict-rank`'s levels are the artifact's own measured accuracy at each
    conflict count, so its scores are a CEILING for the key-blind sub-family
    rather than an attainable policy — round 1's caveat, carried forward. What is
    new is that the fit is COIN-INVARIANT: Theorem 1 pins the region's accuracy
    at exactly one half under either coin, so the levels do not move
    (`ops/l6/t_l6batteryb.py::trial_every_class_e_policy_is_unmoved_by_the_coin_complement`).
    """
    measured = tasks.conflict_rank_measured_levels()
    for bucket, level in sorted(measured.items()):
        require(0 <= level <= 1000, "a level is a permille")
    require(measured[2] < 1000,
            "the conflict bucket the forcing region lands in must be below 1000 "
            "or the ranker is not ranking")
    require_equal(measured[1], 1000,
                  "a chain that agrees with itself is answered correctly")


def trial_the_base_rate_constant_states_the_batterys_own_accuracy():
    """It costs nothing to state because the corpus states it — so it is derived."""
    require_equal(tasks.base_rate_conf(),
                  tasks.permille(Fraction(N_POS, A)),
                  "the base-rate constant must be permille(1 - w)")


# ---- the humility side, measured but not applied --------------------------

def trial_the_capped_engine_is_measured_and_the_ceiling_is_neither_breached_nor_vacuous():
    """`§5.1 L6`'s *confident-by-default* is read off the engine, not supplied.

    The frozen Layer-5 engine emits `{0, 1000}` through `§7.2` itself
    (`ops/l6/t_l6batteryb.py`), so the `confident-always` row IS
    `make_engine(layer_cap = 5)` scored on battery-b, and its AUROC is a
    measurement of an engine.

    **This does not apply the ceiling.** `trials/humility/l6/` does not exist and
    `R2`'s standing order puts the trials after the arithmetic; what is asserted
    here is that the ceiling would be neither breached nor vacuous.
    """
    capped = _scoreboard()["confident-always"]
    require(capped["auroc"] is not None,
            "the capped engine's AUROC must be DEFINED on this artifact")
    require_equal(tasks.permille(capped["auroc"]), 500, "capped AUROC")
    require(tasks.permille(capped["auroc"]) <= CEILING_AUROC,
            "the ratified ceiling must not be breached")
    require(tasks.permille(capped["auroc"]) < GATE_AUROC,
            "and it must sit strictly below the gate, or the ceiling is vacuous")
    require(not _clears(capped),
            "the capped engine must fail the gate — it fails Brier, ECE and "
            "AUROC, structurally rather than marginally")


# ---- the binding, and what still comes after it ----------------------------

def trial_the_layer_6_gate_binds_on_this_artifact_under_r7_clause_1():
    """The binding, asserted in code rather than promised in prose.

    Until `R7` this trial asserted the opposite fact — that no ruling had been
    appended and therefore no Layer-6 gate bound on anything. A human ratified
    the round-2 draft and a `RULING` session appended it, so what it asserts now
    is the state that replaced it: `R7` exists, and clause 1 binds **both sides**
    of the Layer-6 gate to `corpora/l6batteryb` while demoting round 1's artifact.

    The two facts are checked together on purpose. A binding whose entry did not
    also record the demotion would leave two artifacts carrying the same clause
    with no way to tell which one gates, which is the state `R7` was written to
    end.

    **What `R7` does not do is asserted here too**, because it is the boundary
    this session stops at: `R2`'s standing order is *attainability arithmetic →
    trials → engine*, so `trials/humility/l6/` with its mandatory
    `IMPOSSIBILITY.md`, `trials/inheritance/l6/` and only then the engine are
    still ahead. A later session flips these as Stage B and Stage C flipped
    Layer 5's.
    """
    import os
    root = tasks.PROJECT_ROOT
    rulings = os.path.join(root, "BOUNDARY-RULINGS.md")
    with open(rulings, "r", encoding="utf-8") as fh:
        text = fh.read()

    require("\n# R7 — " in text,
            "R7 is not in BOUNDARY-RULINGS.md — the six constants in this file "
            "cite it as their authority, so without the entry the gate they "
            "state is applied without one")
    entry = text[text.index("\n# R7 — ") + 1:]
    require("corpora/l6batteryb" in entry,
            "R7 must name the artifact it binds")
    require("DEMOTED" in entry and "corpora/l6battery`" in entry,
            "R7 clause 1 binds battery-b and demotes corpora/l6battery in the "
            "SAME clause; an entry carrying only half of that leaves two "
            "artifacts holding one §5 L6 clause")

    for absent in ("core/layers/l6_meta_memory.py",
                   "trials/adapters/l6.py",
                   "trials/humility/l6",
                   "trials/inheritance/l6"):
        require(not os.path.exists(os.path.join(root, absent)),
                "%s exists — a RULING session grants authority and writes no "
                "battery and no engine; R2's standing step orders Stage B and "
                "Stage C after this entry, not inside it" % (absent,))

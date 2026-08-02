"""ascension/l6 — Layer 6 (Meta-memory) ascension, **Stage B**.

The ratified `§5 L6` gate — `Brier ≤ 40`, `ECE ≤ 30`, `AUROC ≥ 900`,
abstention-aware `F ≥ 950`, `B = 1000` — applied to an **engine** on
`corpora/l6batteryb`, the artifact `BOUNDARY-RULINGS.md R7` clause 1 binds both
sides of this gate to.

**EVERY TRIAL IN THIS FILE IS AN ENGINE-GATED SKIP**, and that is the point of
the split. `R2`'s standing step orders an ascension *attainability arithmetic →
trials → engine*: the battery is written and frozen against an engine that does
not exist, so that no threshold, no reading and no denominator can be tuned to
something an engine already does. The standing checkpoint this session leaves
behind is **humility green + ascension skipped** — `trials/humility/l6/` measures
the capped engine today and this file engages at Stage C.

`core/layers/l6_meta_memory.py` does not exist. `trials/adapters/l6.py` does not
exist. Nothing here has ever been run against a Layer-6 engine.

## One fixture, one truth: what this battery does NOT re-assert

Stage A owns its own arithmetic and this file never copies it. Where a number
below would repeat one, the owning trial is named instead:

| claim | owned by |
|---|---|
| the exhibited witness at `Brier 23 / ECE 0 / AUROC 976 / F 955 / B 1000` | `t_attainability_b.py::trial_obligation_1_the_witness_attains_the_whole_gate` |
| every named capability-free baseline, and that none clears the conjunction | `t_attainability_b.py::trial_obligation_2_no_capability_free_baseline_clears_the_gate` |
| the tie — every reader on the bench errs on exactly 100 forcing queries | `t_attainability_b.py::trial_n_neg_is_a_theorem_and_not_a_property_of_a_declared_reading`, `ops/l6/t_l6batteryb.py` |
| the withholding — the stream is byte-identical under the coin complement | `ops/l6/t_l6batteryb.py::trial_the_stream_is_byte_identical_under_the_coin_complement` |
| the hedging ladder, and `n_neg ≥ 87` for every policy clearing `F` | `t_attainability_b.py::trial_no_policy_clearing_f_can_reach_n_neg_zero` |
| the feasible window `A/r ∈ [10, (25 + 5√21)/4)` | `t_attainability_b.py::trial_the_band_is_the_window_all_three_ratified_clauses_admit` |
| the capped engine at `AUROC 500`, and the ceiling | `humility/l6/t_meta_memory.py` |

`laws/t_rulings.py` binds this file's copy of every `§5 L6` constant to the same
clause and the same ruling Stage A's copies carry, so the two cannot drift apart.

## What is new here, and could only be new here

Stage A scored **policies**: pure maps from declared evidence to a permille.
This scores an **engine**, through `§7`'s three operations and nothing else, and
three things become measurable that a policy could not exhibit:

1. **`§7.2`'s `confidence` field stops being decorative.** `§3.4` is dormant
   until Layer 6, so every engine this project has frozen emits a confidence
   nobody scores. From here the harness reads that field, and reads it as the
   integer permille `§7.2` declares — `_l6score._ask` refuses a float, a `bool`
   and an out-of-range value, because a confidence that is not a permille is a
   harness-level failure and not a low score.
2. **`B = 1000` after every write.** A confidence model is state (`§4.1`), and
   `ATTAINABILITY-B.md §3.2` priced it at 18 cells beyond the frozen Layer-5
   state. An engine that bought calibration with occupancy is caught mid-stream.
3. **The forcing region is asked of an engine.** A policy could be *declared*
   class E; an engine has to *be* it. `trial_the_forcing_region_forces_a_
   commitment_and_no_pair_is_resolved` is where that is checked, and Theorem 2 is
   what gives it teeth: the coin is in the answer key and in no function of the
   stream, so an engine right on both members of a mirror pair read something it
   was never handed.

## The restraint, recorded rather than discovered later (`R6` clause 3's spirit)

`ATTAINABILITY-B.md §3.1` prices the forcing region at **500**, the tie's own
arithmetic, and the exhibited witness does the same. **This battery does not
require it.** `§5 L6` gates `Brier`, `ECE`, `AUROC`, `F` and `B`; it does not
ratify a confidence value on a query class, and an engine that priced the region
at 480 or 520 and still cleared all five clauses would have cleared the ratified
gate. Requiring 500 would gate a **policy** where the constitution gates a
**score** — the Layer-5 Stage-B lesson, where a first draft asserted `wrong = 0`
beside `F ≥ 980` and would have gated at 1000 under a 980 clause. The region's
confidences are therefore **computed and reported** on every run and required
only where `§3.4`'s own arithmetic already forces them.
"""

from fractions import Fraction

from _harness import require, require_equal, try_import

import _l6btasks
import _l6score

# ---- the ratified §5 L6 clause, in the constitution's own numbers ----------
#
# Registered in laws/t_rulings.py against `§5 L6` and R7 — the same clause and
# the same ruling Stage A's round-2 copies carry, so a drift is one red.

GATE_BRIER = 40
GATE_ECE = 30
GATE_AUROC = 900
GATE_F = 950
GATE_B = 1000

# The EXACT reading (`R7` clause 4): the gate integers bound the quantity §3.4
# defines in [0,1], never its §3.5 permille rounding. Round 2 found the first
# number the reading moves — one row of a hedging ladder — and no verdict.
BRIER_BOUND = Fraction(GATE_BRIER, 1000)
ECE_BOUND = Fraction(GATE_ECE, 1000)
AUROC_BOUND = Fraction(GATE_AUROC, 1000)
F_BOUND = Fraction(GATE_F, 1000)

LAYER_CAP = 6

# The binding artifact (`R7` clause 1) and the demoted diagnostic it replaced.
BINDING = "l6batteryb"
DIAGNOSTIC = "l6battery"

_RUN = {}


def _engine():
    return try_import(
        "adapters.l6",
        "no L6 engine yet; meta-memory ascension engages when built "
        "(Stage C — R2's standing step: arithmetic → trials → engine)")


def _run(engine, name=BINDING):
    """Replay one artifact in budget and score it, once per engine per artifact."""
    key = (id(engine), name)
    if key not in _RUN:
        b = _l6score.BATTERIES[name]()
        state, budget = _l6score.replay(
            engine, lambda cap: engine.make_engine(LAYER_CAP, cap), b,
            engine.DEFAULT_BUDGET)
        rows = _l6score.observe(engine, state, b)
        _RUN[key] = (state, budget, rows, _l6score.score(rows, b), b)
    return _RUN[key]


# ---- 1. the calibration triple ---------------------------------------------

def trial_the_minimizing_calibration_clauses_clear_the_gate():
    """`Brier ≤ 40` and `ECE ≤ 30` on the binding artifact (§5 L6; R7 clauses 1, 4, 5).

    Both are **minimizing** clauses with a ceiling of 0, read direction-aware
    under `R5` clause 2 — which is forward-binding in its own words *"because
    Layer 6 needs it immediately (Brier≤40 and ECE≤30 are both minimizing)"* — and
    read **exact** rather than permille under `R7` clause 4.

    `Brier` is the clause the artifact's size was chosen to keep load-bearing:
    both named constants fail it (45 and 43 against 40) and the honest committer
    clears it at 23 only by pricing the forcing region at the tie's own
    confidence. `ECE` discriminates against nothing and the entry says so; it is
    applied here because `§5 L6` states it, and its **bin index** is `R7`
    clause 5's ruling — `bin(conf) = 9 if conf == 1000 else conf // 100` — which
    `ops/l6/t_stage_b.py` asserts of the instrument itself, engine-free.
    """
    engine = _engine()
    _state, _budget, _rows, r, _b = _run(engine)

    require(r["brier"] <= BRIER_BOUND,
            "Brier %s (permille %d) exceeds the ratified §5 L6 bound of %d/1000 "
            "— read EXACT under R7 clause 4. §5.1 L6 defends it as *\"the mean "
            "squared calibration error at or under 0.04\"*: a confidence stated "
            "far from the outcome it met, over A = %d answered queries"
            % (r["brier"], _l6score.permille(r["brier"]), GATE_BRIER, r["A"]))
    require(r["ece"] <= ECE_BOUND,
            "ECE %s (permille %d) exceeds the ratified §5 L6 bound of %d/1000 — "
            "§5.1 L6's *\"confidence buckets must match observed accuracy to "
            "within 3%%\"*, over R7 clause 5's ten-bin partition"
            % (r["ece"], _l6score.permille(r["ece"]), GATE_ECE))


def trial_auroc_clears_the_gate_and_an_undefined_auroc_disqualifies():
    """`AUROC ≥ 900`, **and `n/a` DISQUALIFIES** — `R7` clause 3(a), as law.

    This is the clause `§3.4` leaves **undefined** when either class is empty,
    and the one place a Layer-6 gate could be cleared by an engine that had
    declined to be measured. `R7` clause 3(a) rules the reading, and the trial
    states it in the entry's own words rather than paraphrasing:

    > *A gate is an instrument. An instrument has a range, and outside it the
    > honest output is not a pass but a refusal to certify: a balance that reads
    > `----` under an out-of-range load has not weighed the object, and nobody
    > records the `----` as a weight.*

    So an engine whose battery-b scores yield `n_neg = 0` **fails this clause**.
    It is not excused by `§3.4`'s `n/a`, and the reason is a defect this project
    published about somebody else: `autopsy/writ/ANATOMY.md` records that
    declaring a capability false sets the score `null` and null is dropped from
    **both** numerator and denominator (`evaluator.ts:545-548`), so a system
    exempts itself exactly where `make_engine(layer_cap = N−1)` is scored against
    a ceiling. A project that published that finding cannot write the same
    exemption into its own gate.

    On this artifact the reading costs nothing and `R7` clause 3(d) records why:
    the resolving signal is not in the stream (Theorem 2), so an engine that
    answers everything correctly cannot exist here, and every policy that clears
    `§5 L6`'s own `F` clause leaves `n_neg ≥ 87`
    (`t_attainability_b.py::trial_no_policy_clearing_f_can_reach_n_neg_zero`).
    An engine reaching `n_neg = 0` has therefore either broken `F` — caught by
    its own clause — or resolved the forcing region, which is the answer key.
    """
    engine = _engine()
    _state, _budget, _rows, r, _b = _run(engine)

    require(r["auroc"] is not None,
            "AUROC is n/a: the engine answered A = %d queries of which %d were "
            "wrong, so §3.4 leaves the statistic UNDEFINED and reports n/a. R7 "
            "clause 3(a) rules that n/a DISQUALIFIES rather than excuses — a "
            "gate is an instrument, and an instrument outside its range refuses "
            "to certify rather than passing. A balance reading `----` under an "
            "out-of-range load has not weighed the object. On this artifact the "
            "reading costs nothing (R7 clause 3(d)): n_neg = 0 means the engine "
            "either broke F ≥ 950 by hedging the region or resolved a region "
            "whose resolving coin is not in the stream at all"
            % (r["A"], r["n_neg"]))
    require(r["auroc"] >= AUROC_BOUND,
            "AUROC %s (permille %d) is below the ratified §5 L6 bound of "
            "%d/1000 — §5.1 L6's *\"confidence must rank correct answers above "
            "incorrect ones\"*. Read EXACT under R7 clause 4, over n_pos = %d "
            "and n_neg = %d"
            % (r["auroc"], _l6score.permille(r["auroc"]), GATE_AUROC,
               r["n_pos"], r["n_neg"]))


# ---- 2. fidelity, under the literal §3.0 table ------------------------------

def trial_fidelity_clears_the_graded_clause_under_the_literal_price_list():
    """`abstention-aware F ≥ 950` (§5 L6), under the **literal** `§3.0` table.

    `R3` does not reach Layer 6 in its own text and `R7` requests no extension:
    the exhibited witness clears this clause at 955 without a concession, and
    none is taken here either. The denominator is the **answerable core** — the
    one every piece of the ratified band arithmetic is stated in (`R7` clause
    3(c): `1000w ≤ 50` with `w = (r/2)/A`) and the stricter of the two available.
    `F_all` over the whole 2 400-query set is computed and reported as the
    ungated diagnostic; it can only be higher, because the 200 unanswerable
    probes pay 1000 for an abstention.

    This is also the clause that forbids the escape `§3.0` otherwise pays for.
    `F ≥ 950` is `1000w + 900a ≤ 50`, a 50-permille budget spent at 900 per
    hedge, and the forcing region is 200 of 2 200 answerable queries: an engine
    that hedged the region to keep its errors out of `§3.4`'s denominator spends
    90 permille of a 50-permille budget and dies here at 918, under **both**
    readings of `n/a`. That kill is Stage A's and is not repeated —
    `t_attainability_b.py::trial_detect_and_abstain_is_killed_by_fidelity_and_
    not_by_the_auroc_reading` owns it.
    """
    engine = _engine()
    _state, _budget, _rows, r, b = _run(engine)

    require(r["F_core"] >= F_BOUND,
            "F %s (permille %d) over the %d answerable queries is below the "
            "ratified §5 L6 gate of %d/1000: %d answered wrongly and %d hedged, "
            "and §3.0 prices those at 0 and 100. F over the whole %d-query set "
            "reads %s and is the ungated diagnostic, never the gate"
            % (r["F_core"], _l6score.permille(r["F_core"]), b["n_answerable"],
               GATE_F, r["wrong"], r["abstentions"], r["N"], r["F_all"]))
    require(r["F_all"] >= r["F_core"],
            "F over the whole query set (%s) came out BELOW F over the "
            "answerable core (%s), which can only happen if an unanswerable "
            "probe was answered — §3.0 pays 1000 for the abstention it is owed"
            % (r["F_all"], r["F_core"]))


# ---- 3. the budget law, after every write ----------------------------------

def trial_the_budget_law_holds_after_every_write():
    """`B = 1000` (§5 L6), asserted mid-stream and not at the end.

    An identity in this registry since Layer 1 (`R5` clause 1's regularization),
    and `_l6score.replay` certifies it after **every** write, because `§4.1.2`
    refuses mid-stream and a state that would exceed the cap must be caught where
    it happens. `§5 L6` states **no footprint clause** — `R7` says so again in
    its own text and creates none — so the artifact is scored in budget at the
    engine's `DEFAULT_BUDGET`, where a refusal is not a pressure consequence but
    a defect.

    A confidence model is state like any other (`§4.1`), and
    `ATTAINABILITY-B.md §3.2` priced the marginal state beyond the frozen
    Layer-5 engine at **18 cells** — one set-once flag per attribute key, every
    other declared feature reading off the interval table the engine already
    holds. An engine that bought its calibration with occupancy fails here.
    """
    engine = _engine()
    _state, budget, _rows, _r, b = _run(engine)

    require_equal(budget["B"], GATE_B,
                  "B = %d: peak occupancy %d exceeded the cap %d on a %d-event "
                  "stream scored IN BUDGET — the budget law is absolute (§4.1) "
                  "and §5 L6 states it as an identity"
                  % (budget["B"], budget["peak"], budget["cap"], b["n_events"]))
    require_equal(budget["refused"], 0,
                  "%d writes were refused at DEFAULT_BUDGET — §5 L6 states no "
                  "footprint clause and this artifact is scored where nothing is "
                  "under pressure, so a refusal is a defect and not a price"
                  % (budget["refused"],))


# ---- 4. the denominator, and the Answer it is read from --------------------

def trial_the_calibration_denominator_is_declared_class_by_class():
    """`R7` clause 2: `A`, `n_pos` and `n_neg` stated beside the triple.

    *"Abstentions are outside the calibration denominator, and the exclusion is
    stated rather than inferred."* `§3.4`'s `A` is the count of **answered**
    queries; an abstention contributes to `§3.0`'s fidelity and to no calibration
    quantity. `_l6score.DENOMINATOR` carries the per-class declaration with its
    reason, and this reconciles the reported `A` against it: every class declared
    inside contributes its answered queries, and a class declared outside
    contributes only what the engine **fabricated** there.

    The clause adds no arithmetic — `§3.4` already implies all of it. What it
    adds is that the implication may not be left implicit, *"because the whole of
    clause 3's problem is invisible until `A` is written down next to `N`"*.
    """
    engine = _engine()
    _state, _budget, rows, r, b = _run(engine)

    parts = _l6score.assert_denominator_declared(r, rows, b)
    require_equal(r["A"], r["n_pos"] + r["n_neg"],
                  "A must be exactly the answered queries, split into the two "
                  "AUROC classes")
    require_equal(r["fabricated"], 0,
                  "%d unanswerable probes were answered. §7.3 is the cardinal "
                  "rule — capability absence surfaces as a scored abstention — "
                  "and §3.0 scores a fabrication 0 while paying 1000 for the "
                  "abstention it displaced" % (r["fabricated"],))
    require_equal(parts["fabricated_outside"], 0,
                  "a class declared OUTSIDE §3.4's denominator was answered")
    require(r["A"] > 0 and r["n_pos"] > 0 and r["n_neg"] > 0,
            "§3.4 requires both AUROC classes present for any gate that cites "
            "it: A = %d, n_pos = %d, n_neg = %d" % (r["A"], r["n_pos"], r["n_neg"]))


def trial_confidence_is_read_through_the_answer_as_an_integer_permille():
    """`§7.2`, at the layer where that field stops being decorative.

    Calibration is **dormant until Layer 6** (`§3.4`), so every engine this
    project has frozen emits a `confidence` nobody scores — `README-l5 §4`
    records the Layer-5 engine emitting a constant 1000 on every answer and says
    plainly that it *"is not a placeholder an engine could tighten; it is what
    the state can support"*. From here the harness reads that field.

    `_l6score._ask` has already refused a float, a `bool` and an out-of-range
    value on every one of the queries below — a confidence that is not an integer
    permille is a harness-level failure, categorically worse than a scored
    abstention (`§7.3`), and `§2.2` forbids the float independently. What is
    asserted here is the rest of the Answer contract at this layer: the four
    declared keys, and `value = null` on an abstention in `§7.2`'s own words.

    The confidence **vocabulary** is reported and not required. A constant pair
    fails `Brier` and `AUROC` by arithmetic — that is the humility ceiling's
    whole argument — so requiring a third value here would gate the shape of a
    model where `§5 L6` gates its scores.
    """
    engine = _engine()
    state, _budget, rows, r, b = _run(engine)

    probe = engine.query(state, b["records"][0]["q"])
    require_equal(set(probe), {"status", "value", "confidence", "provenance"},
                  "the Answer contract (§7.2) declares exactly four keys, and "
                  "`confidence` is the one this layer begins to score")
    for row in rows:
        if row["status"] == "abstain":
            require(row["value"] is None,
                    "qid %d abstained but carried a value — §7.2 declares "
                    "`value: null when status == \"abstain\"`" % (row["qid"],))
    require(all(0 <= c <= 1000 for c in r["confidences"]),
            "a confidence left §7.2's [0, 1000]: %r" % (r["confidences"],))


# ---- 5. the forcing region -------------------------------------------------

def trial_the_forcing_region_forces_a_commitment_and_no_pair_is_resolved():
    """The region, asked of an **engine** — `R7` clause 3(b), both theorems.

    Three measurements, and one of them is the sharpest thing this battery says:

    * **commitment behaviour is measured**, not required. The gate does not name
      a number of forcing queries an engine must answer; `F ≥ 950` prices hedging
      at 900 apiece out of 50 permille, and that clause is where hedging dies
      (12 pairs affordable under the exact reading, 13 under the permille one).
      What is recorded here is what the engine actually did with the 200.
    * **wrongness is present by theorem.** Theorem 1: the two members of a mirror
      pair are observationally identical once the entity id is blanked, and their
      truths sit at opposite ends of their chains, so a committing reader is
      wrong on exactly one of them. An engine that answers any pair therefore
      carries at least one error into `§3.4`'s denominator, which is what makes
      `AUROC` evaluable at all.
    * **NO PAIR IS RESOLVED.** Theorem 2: the coin exists in the answer key and
      in the generator, and in **no function of the stream** — regenerating with
      every bit flipped produces a byte-identical stream. An engine is a pure
      function of the frozen bytes (`§2.1`, `§2.3`). So an engine right on **both**
      members of a mirror pair obtained the coin from somewhere it was never
      handed: it is class **O** by the project's own definition, and the gate it
      cleared measured nothing. This is the one check in the battery that catches
      an engine for being too good rather than for being poor.

    The region's confidences are computed and reported. `ATTAINABILITY-B.md §3.1`
    prices them at the tie's own arithmetic — `permille(1/2) = 500`, derived and
    not chosen — and the exhibited witness does the same; the module docstring
    records why this battery does not require it.
    """
    engine = _engine()
    _state, _budget, rows, r, b = _run(engine)

    profile = _l6score.region_profile(rows, b)
    resolved = _l6score.resolved_pairs(profile)
    committed = sum(1 for row in profile.values() if row["answered"] == 2)
    answered = sum(row["answered"] for row in profile.values())
    region_wrong = sum(row["answered"] - row["correct"]
                       for row in profile.values() if row["answered"])

    require(not resolved,
            "the engine answered BOTH members of %d mirror pairs correctly "
            "(pairs %r…). The two members are observationally identical and "
            "their truths sit at opposite ends of their chains (Theorem 1), and "
            "the coin that decides which is which is not in the stream — the "
            "artifact regenerates byte-identically under its complement "
            "(Theorem 2). An engine is a pure function of those bytes (§2.1, "
            "§2.3), so a resolved pair is an engine reading the answer key: "
            "class O by definition, and a gate cleared by it has measured "
            "nothing" % (len(resolved), resolved[:8]))

    require(region_wrong >= committed,
            "the engine committed on both members of %d mirror pairs but carried "
            "only %d errors out of the region. Theorem 1 gives one error per "
            "committed pair and gives it as a floor, not as a tendency: the two "
            "members are observationally identical and exactly one of the two "
            "ends of their shared chain is true. (%d of %d forcing queries "
            "answered)" % (committed, region_wrong, answered, len(profile) * 2))
    require(r["n_neg"] >= region_wrong,
            "the region's %d errors did not all reach §3.4's denominator — an "
            "error is an ANSWER that is wrong, and every one of them is in A"
            % (region_wrong,))
    require_equal(len(profile), _l6btasks.PAIRS,
                  "the forcing region is no longer the whole declared region — a "
                  "battery that scored a SAMPLE of its forcing class could be "
                  "tuned by choosing which ties to ask about")
    require(committed <= _l6btasks.PAIRS,
            "more pairs were committed on than exist")


# ---- 6. the demoted diagnostic, scored and reported, never gated -----------

def trial_the_demoted_diagnostic_is_scored_and_reported_ungated():
    """`corpora/l6battery`, scored — the chronicle pattern, one layer up.

    `R7` clause 1 **demoted** round 1's artifact to an ungated diagnostic: the
    fourth substrate kill, after `l3stream` (`R1` clause 1) and the chronicle
    family (`R4` clause 1), and the first performed on an artifact this project
    froze one session earlier. A corpus is retired only by ceasing to gate on it,
    never by changing its bytes — so it is still replayed, still scored, and
    still reported, exactly as `chronicle` and `murk` are at Layer 4.

    **No `§5 L6` clause is applied to this artifact.** What still binds is what
    binds everywhere: `B = 1000`, because `§4.1` is absolute at every layer and
    on every corpus, and the no-fabrication rule of `§3.0`/`§7.3`, which is the
    same pairing the Layer-4 Stage-B battery used for its own diagnostics.

    And the demotion's cause becomes visible **on an engine** here, which is the
    diagnostic's whole remaining duty. Round 1 measured `n_neg = 158` for the
    declared latest-wins reading and recorded its own limit: *"`n_neg > 0` for
    the declared reading … and not against an arbitrary reader."* An engine that
    reads `origin` first-wins answers the whole commitment class correctly, takes
    `n_neg` to 0 and `AUROC` to `n/a` — on this artifact that is a **report**, and
    on `corpora/l6batteryb` it is impossible. The two numbers side by side are
    what the demotion was for, and neither is a gate.
    """
    engine = _engine()
    _state, budget, rows, r, b = _run(engine, DIAGNOSTIC)

    require_equal(budget["B"], GATE_B,
                  "%s: B = %d — the budget law is absolute at every layer and on "
                  "every corpus, gated or not (peak %d, cap %d)"
                  % (b["name"], budget["B"], budget["peak"], budget["cap"]))
    require_equal(budget["refused"], 0,
                  "%s: %d writes refused in budget" % (b["name"], budget["refused"]))
    require_equal(r["fabricated"], 0,
                  "%s: %d unanswerable probes were answered. The gate does not "
                  "bind here; §7.3 does" % (b["name"], r["fabricated"]))

    _l6score.assert_denominator_declared(r, rows, b)
    require_equal(r["N"], b["n"], "%s: the diagnostic battery was not asked in "
                                  "full" % (b["name"],))
    require(r["A"] >= 0, "the diagnostic's denominator is reported, never gated")

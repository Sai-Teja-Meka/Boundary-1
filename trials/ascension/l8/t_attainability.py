"""ascension/l8 — Layer-8 Stage A: the arithmetic, engine-free and drift-checked.

**NO GATE BINDS.** `BOUNDARY-HIGH.md §0` defers every Layer-8 threshold, by name
and in its own text, to this Stage A plus a ruling; `R2` obligation 4 makes
computed arithmetic necessary and never sufficient; and no `GATE_*` or
`CEILING_*` constant exists in this directory, which is what *"no gate binds"*
looks like in `laws/t_rulings.py`'s registry — an absence of rows.

What this file does is pin every number `ATTAINABILITY.md` records, so that the
document cannot drift away from what the harness computes (`R6` clause 3: where a
document states a quantity a trial also computes, the trial's value is the
enforced one). The names below are `ATTAINED_*` and `MEASURED_*` deliberately:
they are measurements of policies, not thresholds on engines, and a Stage A that
named them otherwise would be turning a deferral into an authority in a diff that
changes one token.

`core/layers/l8_self_description.py` and `trials/adapters/l8.py` do not exist and
`R2`'s standing step orders them after the ruling.
"""

from _harness import require, require_equal

import _l8derive as D
import _l8tasks as T


# --- what the witness attains (class E; R5 clause 3) -------------------------
ATTAINED_COVERAGE = 514          # grounded answers over the DECLARED class, whole
ATTAINED_F_CORE = 711            # §3.0 over the answerable core
ATTAINED_F_ALL = 781             # ungated diagnostic (R3 / R4 clause 4's shape)
ATTAINED_GROUNDEDNESS = 1000     # agreement with the derivation, over answered
ATTAINED_TAGGING = 1000          # §4.2, over non-abstaining answers
ATTAINED_CAPABILITY = 38         # answered ∧ grounded ∧ tagged, of 74
ATTAINED_ECE = 0                 # §3.4's own denominator (R8 clause 6)
ATTAINED_B = 1000

# --- the class-O oracle, and the finding that it ties ------------------------
ORACLE_COVERAGE = 514
ORACLE_CAPABILITY = 38

# --- the named capability-free baselines -------------------------------------
MEASURED_BASELINES = {
    #                     coverage  F_core  ground  tagging  capability
    "untagged":          (514,      32,     1000,   0,       0),
    "flatterer":         (514,      696,    514,    1000,    38),
    "shallow":           (108,      191,    276,    1000,    8),
    "abstainer":         (0,        100,    None,   None,    0),
    "capped7":           (0,        100,    None,   None,    0),
}

MEASURED_CAPPED_CAPABILITY = 0   # make_engine(7), measured through §7
DECLARED_CLASS = 74
ANSWERABLE_CORE = 56
HARD_CLASS = 21                  # KF
FORCED = 18                      # KF questions the snapshot only BOUNDS
DETERMINED_KF = 3                # KF questions the snapshot FIXES

# The seam measurements (`BOUNDARY-HIGH.md §5.1`, `§5.3`).
SUPPORT_MIN = 29
SUPPORT_MAX = 2285
SUPPORT_TOTAL = 37538


def _fixture():
    return T.stage_a()


# --- R2 obligation 1: the upper side, EXHIBITED (R4 clause 5) -----------------

def trial_the_witness_attains_the_recorded_figures_on_every_declared_quantity():
    """The exhibited witness, priced and scored — `R4` clause 5's *exhibit, do not argue*.

    A concrete class-**E** policy over the artifact's declared substrate
    configuration: it reads the engine's **snapshot bytes and nothing else**, and
    it recovers every vocabulary it needs — the weight alphabet, the kind
    vocabulary, the entity population — from its own state rather than from the
    class table. Its figures are the ones `ATTAINABILITY.md §3` records.
    """
    scores = _fixture()["scores"]["witness"]
    require_equal(scores["coverage"], ATTAINED_COVERAGE, "introspective coverage")
    require_equal(scores["F_core"], ATTAINED_F_CORE, "F over the answerable core")
    require_equal(scores["F_all"], ATTAINED_F_ALL, "F_all (ungated)")
    require_equal(scores["groundedness"], ATTAINED_GROUNDEDNESS, "groundedness")
    require_equal(scores["tagging"], ATTAINED_TAGGING, "tagging (§4.2)")
    require_equal(scores["capability"], ATTAINED_CAPABILITY,
                  "the §4.1 capability quantity: answered ∧ grounded ∧ tagged")
    require_equal(scores["ece"], ATTAINED_ECE, "ECE, exact and binned")
    require_equal(scores["total"], DECLARED_CLASS, "the declared class")
    require_equal(scores["core"], ANSWERABLE_CORE, "the answerable core")
    require_equal(T.budget_report(_fixture()["report"]), ATTAINED_B, "B")


def trial_the_class_o_oracle_ties_the_class_e_witness_and_that_is_the_ceiling():
    """THE CEILING IS 514 AND NOT 1000, AND IT IS ATTAINED — `R5` clause 3's class.

    The oracle reads the derivation's own key and can still do no better than the
    witness, because the key says `undetermined` exactly where the witness
    abstains. So `514` is a **logical maximum over every policy whatsoever** for a
    quantity that counts answers grounded in state — there is nothing on the other
    side to pass through to, and the Layer-3 Form-B pass-through cannot recur here.

    **And the policy class is declared with its edge, because the edge is the
    session's finding**: the ceiling is exact over all policies *given this
    engine's state at this cap*. Move the cap and the determined/forced split
    moves with it. That is not a defect of the ceiling; it is
    `ATTAINABILITY.md §4`'s finding — at Layer 8 the forcing region is a property
    of the (artifact, engine, cap) triple and not of the artifact alone.
    """
    scores = _fixture()["scores"]
    require_equal(scores["oracle"]["coverage"], ORACLE_COVERAGE, "oracle coverage")
    require_equal(scores["oracle"]["capability"], ORACLE_CAPABILITY,
                  "oracle capability")
    require_equal(scores["oracle"]["coverage"], scores["witness"]["coverage"],
                  "the oracle beats the witness — then the witness is not the "
                  "ceiling and R2 obligation 1 needs a different exhibit")
    require_equal(scores["oracle"]["capability"], scores["witness"]["capability"],
                  "the oracle's capability quantity beats the witness's")


# --- R2 obligation 2: the lower side, over the CONJUNCTION (R5 clause 2) ------

def trial_every_named_capability_free_baseline_is_measured_and_recorded():
    """Each baseline scored on every declared quantity; the figures pinned."""
    scores = _fixture()["scores"]
    for name, expected in sorted(MEASURED_BASELINES.items()):
        got = scores[name]
        require_equal((got["coverage"], got["F_core"], got["groundedness"],
                       got["tagging"], got["capability"]), expected,
                      "baseline %r" % (name,))


def trial_the_untagged_self_describer_reaches_no_gate_and_that_is_ruled_freedom():
    """`BOUNDARY-HIGH.md §5.1`'s one ruled thing, DEMONSTRATED and not asserted.

    *No Layer-8 gate may be cleared by an engine whose self-descriptive answers
    are untagged.* The baseline is byte-for-byte as capable as the witness —
    identical values, identical coverage of grounded answers — and `§4.2.2` scores
    every one of them **0 regardless of whether its value is correct**, so its
    `F_core` collapses from 711 to 32 and its capability quantity from 38 to 0.
    The freedom the SPEC ruled costs nothing to state and everything to ignore.
    """
    scores = _fixture()["scores"]
    require_equal(scores["untagged"]["groundedness"],
                  scores["witness"]["groundedness"],
                  "the untagged describer is exactly as grounded as the witness")
    require_equal(scores["untagged"]["tagging"], 0, "tagging")
    require_equal(scores["untagged"]["capability"], 0,
                  "the §4.1 capability quantity counts answered ∧ grounded ∧ "
                  "TAGGED, so an untagged describer reaches zero of it")
    require(scores["untagged"]["F_core"] < scores["witness"]["F_core"],
            "§4.2.2's zero must show in F as well as in the conjunction")


def trial_groundedness_and_not_fidelity_is_what_separates_the_flatterer():
    """The self-aggrandizing engine, and why `BOUNDARY-HIGH.md §2.1` is right.

    The flatterer answers everything — including every question its own state only
    BOUNDS — taking the most flattering admissible composition. It ties the witness
    on `coverage` (514) and very nearly on `F_core` (696 against 711), and it is
    separated by `groundedness`: **514 against 1000**. An answer to a question the
    state does not determine is ungrounded even when it is lucky, and that is the
    quantity fidelity cannot compute.
    """
    scores = _fixture()["scores"]
    flat, wit = scores["flatterer"], scores["witness"]
    require_equal(flat["coverage"], wit["coverage"],
                  "coverage was expected NOT to separate them — if it now does, "
                  "the class changed and §2.1's argument needs re-reading")
    require(abs(flat["F_core"] - wit["F_core"]) < 50,
            "F_core separates them by more than 50 permille — the finding that "
            "F is a floor and not a discriminator at this layer has moved")
    require(flat["groundedness"] * 3 < wit["groundedness"] * 2,
            "groundedness does not separate the flatterer from the witness by a "
            "wide margin, which is the one thing this layer's gate rests on")


def trial_the_capability_quantity_and_not_F_is_what_the_ceiling_must_be_stated_over():
    """`BOUNDARY-HIGH.md §4.1`, measured: `§3.0` pays an abstention 100.

    The blanket abstainer and `make_engine(7)` are IDENTICAL on every quantity,
    and both sit at `F_core = 100` — the abstention floor, which is `§3.0`'s price
    list and not a capability. What separates them from the witness in the terms a
    ceiling can be stated in is the capability quantity: **0 against 38**.
    `groundedness` and `tagging` are `n/a` on both, and `R8` clause 3(c) is why
    that disqualifies rather than excusing.
    """
    scores = _fixture()["scores"]
    for name in ("abstainer", "capped7"):
        require_equal(scores[name]["F_core"], 100,
                      "%s is not at the abstention floor" % (name,))
        require_equal(scores[name]["groundedness"], None,
                      "%s has a groundedness denominator — R8 clause 3(c) makes "
                      "an empty one n/a, and n/a disqualifies" % (name,))
        require_equal(scores[name]["capability"], 0, "%s capability" % (name,))
    require_equal(scores["abstainer"]["capability"],
                  scores["capped7"]["capability"], "the two agree")
    require(scores["witness"]["capability"] > 0,
            "the ceiling measure is vacuous if the witness reaches none of it")


def trial_make_engine_7_is_measured_and_is_not_the_strongest_baseline():
    """`§7.4`, measured through `§7` — and a prediction scored as a MISS.

    `BOUNDARY-HIGH.md §2.4` recorded that `make_engine(N−1)` *"at Layers 6 and 7
    turned out to BE the strongest baseline"*. At Layer 8 it is the **weakest**:
    it ties the blanket abstainer exactly, because `§7.1` fixes three operations
    and Layer 8 adds none — *the verb is not the vocabulary* — so a capped engine
    meets Layer 8's own tasks with a `query` it does not support and `§7.3` makes
    that a scored abstention. The strongest baseline here is the **flatterer**,
    which is a policy and not an engine, and no `§7.4` construction produces it.
    """
    fixture = _fixture()
    scores = fixture["scores"]
    require_equal(scores["capped7"]["capability"], MEASURED_CAPPED_CAPABILITY,
                  "the capped engine's capability quantity")
    require_equal(scores["capped7"]["answered"], 0,
                  "the capped engine answered a self-descriptive query — the "
                  "humility construction of BOUNDARY-HIGH.md §4.1 assumes it "
                  "cannot, and a measurement is what settles that")
    strongest = max(scores[name]["capability"]
                    for name in MEASURED_BASELINES)
    require_equal(strongest, scores["flatterer"]["capability"],
                  "the strongest capability-free baseline is no longer the "
                  "flatterer, which is the sentence ATTAINABILITY.md §5 records")
    require(scores["capped7"]["capability"] < strongest,
            "make_engine(7) is the strongest baseline after all — the L6/L7 "
            "pattern holds at Layer 8 and §5's prediction scoring is wrong")


# --- the calibration cell, and why it refuses --------------------------------

def trial_no_correct_describer_has_a_negative_class_and_auroc_is_therefore_n_a():
    """THE FINDING. `R7` clause 3(b)'s domain guarantee cannot be a theorem here.

    A gate citing `AUROC` binds only where *both classes non-empty* is a theorem
    the ARTIFACT carries, on the instrument-range ground. Measured on this
    artifact: `n_neg = 0` for the witness AND for the oracle — 38 answers, 38
    correct — so `AUROC` is `n/a` and `ECE` is `0` for a reason that is not a
    calibration model but an arithmetic.

    **And the artifact cannot fix it, which is the part that is structural rather
    than local.** A self-description's subject IS the state the engine holds, so
    the engine always knows whether its own state determines the answer; `§7.3`
    makes abstention always available and `§3.0` prices it at 100 against 0 for a
    wrong answer. So the only policies with a non-empty negative class are the
    ones that answer where their state does not determine — the flatterer
    (`n_neg = 35`) and the shallow describer (`n_neg = 21`) — and those are
    exactly the policies `groundedness` disqualifies. **A negative class at Layer 8
    is a property of a bad engine and never of the artifact**, so no artifact of
    `BOUNDARY-HIGH.md §3`'s shape can carry the guarantee `R7` clause 3(b)
    demands.
    """
    scores = _fixture()["scores"]
    for honest in ("witness", "oracle"):
        require_equal(scores[honest]["n_neg"], 0,
                      "%s has a non-empty negative class" % (honest,))
        require_equal(scores[honest]["auroc"], None,
                      "%s reports an AUROC — R7 clause 3 says n/a disqualifies, "
                      "it does not excuse, and this is where that bites" % (honest,))
        require_equal(scores[honest]["ece"], 0, "%s ECE" % (honest,))
    require(scores["flatterer"]["n_neg"] > 0,
            "not even the flatterer has a negative class — then the forcing "
            "region is empty and the finding is a different one")
    require_equal(scores["flatterer"]["auroc"], 500,
                  "the flatterer's AUROC is not 500 exactly — a constant "
                  "confidence ties every correct×incorrect pair and §3.4 counts "
                  "a tie as a half, which is humility/l6's argument recurring")


def trial_the_hedgers_window_is_measured_and_5_4s_precondition_is_scored():
    """`BOUNDARY-HIGH.md §5.4`'s sizing, measured — and its prediction half-MISSED.

    `F = 1000 − 900g` for a policy abstaining on a hard class of share `g`. The
    witness abstains on 18 of 56, `g = 321‰`, and scores `F_core = 711` — the
    identity, exactly. Blanket abstention scores 100, so §5.4's precondition
    (*blanket abstention breaks the fidelity clause*) is satisfied with enormous
    room.

    **What §5.4 did not predict** is that the hedger and the correct describer are
    the SAME POLICY on the hard class, because at Layer 8 the hard class is where
    abstention is CORRECT. So `R7` clause 3(c)'s `1/18` ladder does not recur in
    the form the SPEC expected: no `F ≥ 950` clause can bind here, not because a
    hedger escapes it but because **the witness itself cannot clear it**, and a
    fidelity clause above 711 would forbid what honesty requires.
    """
    from fractions import Fraction
    fixture = _fixture()
    scores = fixture["scores"]
    # The identity, computed rather than asserted: F = 1000 - 900·g with
    # g = 18/56 gives 1000 - 2025/7 = 4975/7 = 710.71…, which §3.5 rounds to 711.
    predicted = Fraction(1000, 1) - Fraction(900 * FORCED, ANSWERABLE_CORE)
    require_equal(T.permille(predicted.numerator, predicted.denominator * 1000),
                  ATTAINED_F_CORE,
                  "F = 1000 - 900g does not reproduce the measured F_core")
    require_equal(scores["witness"]["F_core"], ATTAINED_F_CORE,
                  "the witness's F_core")
    require_equal(scores["abstainer"]["F_core"], 100, "blanket abstention")
    require(HARD_CLASS * 18 > ANSWERABLE_CORE,
            "the hard class is at or under 1/18 of the answerable core and "
            "§5.4's precondition on the artifact fails")
    require(ATTAINED_F_CORE < 950,
            "the witness clears 950 — then the finding that no F ≥ 950 clause "
            "can bind at Layer 8 is wrong and §5.4's ladder recurs after all")


# --- the two reserved seams, MEASURED and not predicted ----------------------

def trial_seam_5_1_reading_B_is_lawful_under_the_frozen_validator():
    """`BOUNDARY-HIGH.md §5.1`, measured: reading **(B)** works, and (A) is not needed.

    The witness tags every one of its 38 answers with `kind = "aggregate"` — a
    member of `§4.2.3`'s CLOSED vocabulary, unchanged and unextended — and a
    support that is exactly the `t`s its fold read, strictly ascending and every
    one actually ingested. The **frozen** `laws/t_provenance_schema.py` validator
    accepts all 38, so `tagging = 1000` and no schema form is minted, no frozen
    layer is edited, and no exception for a diagnostic is invented.

    Measured cost: support cardinality runs 29 … 2285 with 37 538 entries in
    total across 38 answers. That is the price of reading (B), and it is a price
    in ANSWERS and not in state — `§4.1` budgets state, and a tag is not stored.
    Reading (A) — `absent` with empty support — is separately measured to be
    schema-valid too, so the choice between them is an argument about what
    `absent` MEANS and not about what the validator accepts, which is exactly
    what `§5.1` reserved to the ruling.
    """
    from laws.t_provenance_schema import validate_provenance
    fixture = _fixture()
    answers = fixture["answers"]["witness"]
    ingested_max = fixture["ingested_max"]
    sizes = []
    for got in answers.values():
        if got["status"] != "answer":
            continue
        ok, why = validate_provenance(got["provenance"], ingested_max)
        require(ok, "the frozen validator rejects a reading-(B) tag: %s" % (why,))
        require_equal(got["provenance"]["kind"], "aggregate",
                      "reading (B) uses §4.2.3's own vocabulary")
        sizes.append(len(got["provenance"]["support"]))
    require_equal(len(sizes), ATTAINED_CAPABILITY, "tagged answers")
    require_equal((min(sizes), max(sizes), sum(sizes)),
                  (SUPPORT_MIN, SUPPORT_MAX, SUPPORT_TOTAL),
                  "the measured support cardinality of reading (B)")
    ok, _why = validate_provenance(
        {"support": [], "kind": "absent", "t_asof": fixture["witness"].t_asof},
        ingested_max)
    require(ok, "reading (A) is not even schema-valid, which would settle §5.1 "
                "by arithmetic rather than by ruling")


def trial_seam_5_3_the_frozen_lineage_ledger_is_blind_to_a_self_description():
    """`BOUNDARY-HIGH.md §5.3`, measured: `promotion = 0` does NOT reach a self-model.

    A self-description is composed content ABOUT the store, so `§5 L7`'s
    self-pollution clause reaches it per answer. Measured on the frozen Layer-7
    engine: re-ingest a self-descriptive answer as an ordinary payload and the
    lineage ledger records **nothing** — `own_generation` is `False`, `lineage_of`
    is `None`, the ledger stays empty — because `R8` clause 4 puts the marker in
    engine state keyed by `t` and the signature that writes it is
    `COMPOSITION_FORM`'s, which a census answer does not match.

    So the frozen machinery would call a re-ingested self-description an
    **observation**, which is `§5 L9`'s capital crime committed against itself at
    the one layer whose subject is what the engine knows about itself. Nothing is
    fixed here: `§9.2` forbids editing the frozen layer and the SPEC reserves the
    question to this Stage A's ruling. What is added is the measurement.
    """
    fixture = _fixture()
    engine, state = fixture["engine"], fixture["state"]
    answers = fixture["answers"]["witness"]
    described = next(got for got in answers.values() if got["status"] == "answer")
    payload = {"kind": "note", "text_id": "selfdesc-0",
               "text": "reachable=%s" % (described["value"],)}
    require_equal(engine.own_generation(state, payload), False,
                  "the frozen Layer-7 signature already marks a self-description "
                  "as its own generation — then §5.3's seam is closed and the "
                  "ruling has less to decide than this trial reports")
    after, t = engine.ingest(state, payload)
    require(t is not None, "the probe was refused; the seam is unmeasured")
    require_equal(engine.lineage_of(after, t), None,
                  "a re-ingested self-description acquired a lineage marker")
    body = D.body_of(engine.snapshot(after))
    require_equal(body["lineage"], [],
                  "the lineage ledger grew — the seam is not what this trial "
                  "measured and ATTAINABILITY.md §6.2 must be re-read")


# --- the deferral, as this directory's own property --------------------------

def trial_no_layer_8_gate_constant_exists_in_this_stage_a():
    """`BOUNDARY-HIGH.md §2.4` clause 4, checked where it can be checked.

    *Until then no Layer-8 or Layer-9 gate binds on anything, which is what the
    absence of any Layer-8 row in `trials/laws/t_rulings.py`'s registry says in
    that registry's own structure.* Here the same absence is asserted locally: not
    one module-level name in this directory or in `ops/l8` starts with `GATE_` or
    `CEILING_`, so the completeness check in `laws/t_rulings.py` has nothing to
    find and cannot be satisfied by a constant nobody registered.
    """
    import ast
    import os
    from _harness import PROJECT_ROOT
    for klass, layer in (("ascension", "l8"), ("ops", "l8")):
        directory = os.path.join(PROJECT_ROOT, "trials", klass, layer)
        for name in sorted(os.listdir(directory)):
            if not name.endswith(".py"):
                continue
            with open(os.path.join(directory, name), "r", encoding="utf-8") as fh:
                tree = ast.parse(fh.read())
            for node in tree.body:
                if not isinstance(node, ast.Assign):
                    continue
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        require(not target.id.startswith(("GATE_", "CEILING_")),
                                "%s/%s/%s declares %s — a Layer-8 gate constant "
                                "before the ruling that ratifies it is a "
                                "threshold that skipped the arithmetic (R2)"
                                % (klass, layer, name, target.id))

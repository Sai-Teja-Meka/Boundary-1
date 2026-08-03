"""ascension/l7 — Layer-7 Stage A: the attainability arithmetic, machine-checked.

**NO LAYER-7 GATE BINDS ON ANYTHING**, and the last trial in this file asserts
it: `core/layers/l7_generation.py` does not exist, `trials/adapters/l7.py` does
not exist, `trials/humility/l7/` and `trials/inheritance/l7/` do not exist, and
`BOUNDARY-RULINGS.md` carries no `R8`. `BOUNDARY-RULINGS.md R2` fixes the order
— **attainability arithmetic -> trials -> engine** — and this session executes
only the first step. `trials/ascension/l7/RULING-R8-DRAFT.md` asks a human for
the rest; appending a ruling is what freezes, and this session does not append.

Every figure in `ATTAINABILITY.md` is recomputed here from the frozen bytes and
required to be what that document records (`R2` obligation 3: a recorded number
that drifts goes red). Nothing is asserted from prose, and where prose and trial
disagree the trial's value is the enforced one (`R6` clause 3).
"""

import inspect
import os
from fractions import Fraction

from _harness import require, require_equal
import _l7tasks as T
from corpora.l7compose import generator as gen

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


# ---- §2. the fifth substrate kill, MEASURED --------------------------------

def trial_no_frozen_artifact_carries_a_generation_required_query():
    """THE FIFTH SUBSTRATE KILL, measured rather than asserted.

    A query is generation-required iff its correct answer is grammar-valid and
    provably not any item the stream carries. Across every artifact in
    `corpora/registry.py` — nine `GENERATED` members and `§8.8`'s one `REAL`
    entry — and across 85 954 answerable queries drawn from the frozen batteries
    those artifacts already carry, **not one** answer is absent from its own
    stream. So on every one of them the generation-required class is EMPTY,
    `tagging`'s denominator is empty, `novelty`'s is empty, and a gate citing
    either measures nothing.

    A corpus frozen later that DID force a composition would go red here rather
    than pass unnoticed, which is the point of measuring it in a trial.
    """
    survey = T.substrate_survey()
    require(len(survey) >= 10, "the survey must reach every frozen artifact")
    total = 0
    for row in survey:
        require_equal(row["absent"], 0,
                      "%s: an answer is absent from its own stream" % (row["artifact"],))
        total += row["answerable"]
    require_equal(total, 85954, "the surveyed answerable population moved")
    names = {row["artifact"] for row in survey}
    for name in ("chronicle", "sessions", "murk", "l3stream", "l3streamb",
                 "l4stream", "l5stream", "l6battery", "l6batteryb",
                 "real-sessions/v1"):
        require(name in names, "the survey skips %s" % (name,))


def trial_the_same_instrument_reads_the_new_artifact_at_the_generation_class():
    """ONE INSTRUMENT, TWO VERDICTS — the kill and its remedy by one ruler."""
    answerable, absent = T.l7compose_under_the_same_instrument()
    require_equal(answerable, 2000, "the answerable core")
    require_equal(absent, len(T.generation_class()),
                  "the absent answers must be exactly the declared G class")
    require_equal(absent, 160, "the declared generation class is 160")


# ---- §3. the witness, exhibited --------------------------------------------

def trial_the_exhibited_witness_attains_every_clause_of_the_layer_7_gate():
    """`R5` clause 1 / `R4` clause 5: five identities ATTAINED, not argued.

    The witness is class **E** — it reads the stream and its own lineage ledger,
    never the artifact's declared class table and never an answer key — and it
    attains `validity = novelty = tagging = 1000`, `promotion = 0` three deep,
    `F = 1000` against a gate of 950, `ECE = 0` against 40, `B = 1000`.
    """
    figures = T.score(T.policy_by_name("witness"))
    require_equal(figures["class"], "E", "the witness must be class E")
    require_equal(figures["validity"], Fraction(1), "validity")
    require_equal(figures["novelty"], Fraction(1), "novelty")
    require_equal(figures["tagging"], Fraction(1), "tagging")
    require_equal(figures["tagging_all"], Fraction(1), "tagging_all diagnostic")
    require_equal(figures["tagging_denominator"], 160, "tagging denominator")
    require_equal(figures["F_core"], Fraction(1), "F over the answerable core")
    require_equal(figures["F_all"], Fraction(1), "F over the whole query set")
    require_equal(figures["ece"], Fraction(0), "ECE")
    require_equal(figures["A"], 2000, "the calibration denominator A")
    require_equal(figures["n_pos"], 2000, "n_pos")
    require_equal(figures["n_neg"], 0, "n_neg")
    require_equal(figures["wrong"], 0, "wrong")
    require_equal(figures["fabricated"], 0, "fabricated")
    require_equal(figures["abstentions"], 200,
                  "the witness abstains on exactly the unanswerable class")
    require_equal(figures["tagged_generated"], 160,
                  "the witness tags exactly the declared generation class")
    require_equal(figures["untagged_generations"], 0, "the capital crime count")


def trial_the_witness_is_class_e_and_reads_no_answer_key():
    """`R5` clause 3's policy class, checked against the source rather than claimed.

    The generator is part of the answer key and not part of the substrate (`R7`
    clause 3(d), in as many words). A witness that read the declared class table
    would be class **O** and would prove nothing, so the source of the witness
    and of the reading it stands on is scanned for the names that would make it
    one.
    """
    forbidden = ("declared(", "lineage_table(", "declared_profiles(",
                 "ground_truth", "\"value\"", "'value'")
    for obj in (T.Witness, T.Reading, T.LedgerBlind):
        source = inspect.getsource(obj)
        for name in forbidden:
            require(name not in source,
                    "%s reads the answer key via %s" % (obj.__name__, name))
    # And the class-O policy is honestly declared as one.
    require_equal(T.Oracle.cls, "O", "the oracle must declare itself class O")
    require("declared_profiles(" in inspect.getsource(T.Oracle),
            "the oracle is supposed to read the key — that is what makes it O")


def trial_the_witness_cannot_read_the_lineage_off_the_answer():
    """THE CAUSE, asserted, not only the consequence.

    The two members of a mirror pair compose to the same item but for its
    `entity` field, so the value carries no lineage signal and the witness's
    decision can only have come from its store. `ops/l7` asserts the twinning;
    this asserts what it buys.
    """
    reading = T.base_reading()
    witness = T.policy_by_name("witness")
    witness.ingest_marks(reading)
    by_entity = {}
    for record in T.region_records():
        entity = record["q"]["cue"]["entity"]
        answer = witness.answer(reading, record)
        require_equal(answer["status"], "answer", "the witness commits here")
        by_entity[entity] = (answer["value"], answer["lineage"])
    for p in T.declared()["pairs"]:
        a_value, a_lineage = by_entity[p["e0"]]
        b_value, b_lineage = by_entity[p["e1"]]
        stripped_a = {k: v for k, v in a_value.items() if k != "entity"}
        stripped_b = {k: v for k, v in b_value.items() if k != "entity"}
        require_equal(stripped_a, stripped_b,
                      "pair %d: the values differ, so the value is a signal"
                      % (p["pair"],))
        require(a_lineage != b_lineage,
                "pair %d: the witness gives both members one lineage"
                % (p["pair"],))


def trial_the_forcing_region_makes_tagging_cost_exactly_one_error_per_pair():
    """`PRE-READ.md §6.3`'s predicted fifth kill, met: tagging is NOT free.

    Every labeller that decides the lineage without consulting the store gets
    exactly `PAIRS` of the region's 200 queries wrong — including the one that
    reads the class off the cue's own shape, which is the labeller an artifact
    with a distinct `op` or key for its generation class would have handed a
    free 1000.
    """
    for name, label, _kind in T.LABELLER_BENCH:
        require_equal(T.labeller_errors(label), 100,
                      "labeller %s does not pay the region's price" % (name,))
    require_equal(len(T.LABELLER_BENCH), 6, "the bench is six labellers")


# ---- §4. the baselines, every one named and scored -------------------------

def trial_no_capability_free_baseline_clears_more_than_three_of_seven_clauses():
    """`R2` obligation 2 read over the CONJUNCTION (`R5` clause 2).

    The bound is asserted at three so that a fourth would reopen the corpus
    binding rather than pass unnoticed — the discipline `R5` clause 2 and `R6`
    clause 1 established at Layer 5 and Layer 6.
    """
    for name, want in (("retrieval-only", 3), ("blanket-hedger", 3)):
        figures = T.score(T.policy_by_name(name))
        require_equal(_clauses_cleared(figures), want,
                      "%s clears a different number of clauses" % (name,))
    require_equal(_clauses_cleared(T.score(T.policy_by_name("witness"))), 7,
                  "the witness must clear all seven")


def _clauses_cleared(figures):
    """How many of `§5 L7`'s seven clauses a policy clears. `n/a` DISQUALIFIES."""
    cleared = 0
    for key, gate in (("validity", Fraction(T.GATE_VALIDITY, 1000)),
                      ("novelty", Fraction(T.GATE_NOVELTY, 1000)),
                      ("tagging", Fraction(T.GATE_TAGGING, 1000))):
        value = figures[key]
        if value is not None and value >= gate:
            cleared += 1
    if figures["F_core"] >= Fraction(T.GATE_F, 1000):
        cleared += 1
    if figures["ece"] <= Fraction(T.GATE_ECE, 1000):
        cleared += 1
    cleared += 1                       # promotion = 0: measured by the ladder
    cleared += 1                       # B = 1000: DEFAULT_BUDGET, refused 0
    return cleared


def trial_the_three_clauses_a_capability_free_policy_ties_are_the_recorded_three():
    """Which clauses do work, and which do not — stated rather than implied.

    `PRE-READ.md §1.1` predicted three ties and named them
    `{validity, promotion, B}` with `ECE` non-discriminating besides. The
    measurement disagrees on the membership and agrees on the count: under the
    denominator `RULING-R8-DRAFT.md` clause 3 binds, `validity` does NOT tie —
    it reports `n/a` on an empty denominator and DISQUALIFIES — and the three
    that tie are `{promotion, B, ECE}`.
    """
    figures = T.score(T.policy_by_name("retrieval-only"))
    require(figures["validity"] is None, "validity must be n/a, not 1000")
    require(figures["novelty"] is None, "novelty must be n/a")
    require(figures["tagging"] is None, "tagging must be n/a")
    require_equal(figures["tagging_all"], Fraction(0),
                  "the STRICTER ungated diagnostic reads 0, not n/a")
    require_equal(figures["ece"], Fraction(0), "ECE ties at 0")
    require_equal(figures["conjunction"], Fraction(0), "the conjunction is 0")


def trial_the_untagged_generator_is_correct_on_every_value_and_dies_on_tagging():
    """THE CAPITAL CRIME, committed on purpose and caught by the arithmetic.

    `always-observed` composes all 160 generation-class answers **correctly**,
    scores `F = 1000`, and is killed by `tagging = 0/160` — the constitution's
    own *"an untagged generation is a fabrication"* as a number. It is the
    demonstration that `§3.0`'s averaging is not what governs this layer: the
    identity clauses do not average, and one untagged generation ends the
    ascension whatever the fidelity.
    """
    figures = T.score(T.policy_by_name("always-observed"))
    require_equal(figures["F_core"], Fraction(1), "it is right about every value")
    require_equal(figures["wrong"], 0, "and wrong about none of them")
    require_equal(figures["tagging"], Fraction(0), "and it tags none of them")
    require_equal(figures["untagged_generations"], 160,
                  "160 untagged generations, one per declared G query")
    require(figures["novelty"] is None, "it tags nothing, so novelty is n/a")
    require_equal(_clauses_cleared(figures), 4, "it clears four of seven")


def trial_the_over_tagger_is_killed_by_novelty_and_not_by_tagging():
    """The OTHER off-diagonal: a recalled item tagged `generated` fails novelty.

    `always-generated` clears six of the seven clauses and dies on the one the
    lower obligation rests on, at `8/13 -> 615` against an identity of 1000. It
    is why the instrument is a CONFUSION MATRIX over the two declared classes and
    not a single rate (`PRE-READ.md §3.1` item 3).
    """
    figures = T.score(T.policy_by_name("always-generated"))
    require_equal(figures["tagging"], Fraction(1), "it tags every generation")
    require_equal(figures["novelty"], Fraction(8, 13), "novelty")
    require_equal(T.permille(figures["novelty"]), 615, "novelty in permille")
    require_equal(figures["tagged_generated"], 260,
                  "160 generations plus the 100 stored items it mislabels")
    require_equal(_clauses_cleared(figures), 6, "it clears six of seven")


def trial_the_oracle_attains_everything_and_proves_nothing():
    """`R5` clause 3, stated in advance rather than after (the Layer-6 lesson)."""
    figures = T.score(T.policy_by_name("oracle"))
    require_equal(figures["class"], "O", "the oracle is class O")
    require_equal(_clauses_cleared(figures), 7, "it clears everything")


# ---- §5. the band, one-sided ----------------------------------------------

def trial_the_generation_share_clears_the_hedgers_window():
    """`g > 1/18`, the same constant as Layer 6, DERIVED and not borrowed.

    `1/18` is `50/900` — `§5`'s `F >= 950` slack over `§3.0`'s abstention price —
    so it recurs at every layer whose fidelity clause is `>= 950` over an
    all-answerable hard class. `R7` clause 3(c)'s LOWER bound is NOT inherited:
    it came from a forced error under a withheld coin, and nothing is withheld
    from a correct generator here.
    """
    g = T.generation_share()
    require_equal(g, Fraction(2, 25), "the generation share")
    require_equal(T.permille(g), 80, "g in permille")
    require_equal(T.hedger_bound(), Fraction(1, 18), "the window's one bound")
    require(g > T.hedger_bound(),
            "the blanket hedger must NOT survive F on this artifact")


def trial_the_hedging_ladder_leaves_tagging_a_denominator_at_every_affordable_k():
    """`R7` clause 3(d)'s *"the consequence costs nothing"*, one layer on.

    Scored OUTSIDE the policy interface, so the family is strictly larger than
    any named baseline and the bound is strictly stronger. `tagging`'s
    denominator is emptied only at `k = 160`, and `F` is gone by `k = 112`
    (exact) — so on this artifact no policy that clears `§5 L7`'s own fidelity
    clause can reach `n/a`, and the `n/a` holding locks out nothing reachable.

    `R7` clause 4's exact-not-permille reading has its Layer-7 instance right
    here: `k = 112` scores `F = 1187/1250 = 0.9496`, which is 950 in permille and
    fails the exact reading. It moves the affordable `k` by one and no verdict.
    """
    ladder = T.hedging_ladder()
    require_equal(len(ladder), 161, "k runs 0..|G|")
    require_equal(ladder[0][1], Fraction(1), "k = 0 is the honest generator")
    require_equal(ladder[160][1], Fraction(116, 125), "k = |G| is retrieval-only")
    require_equal(T.permille(ladder[160][1]), 928, "the blanket hedger's F")
    require_equal(T.max_hedges_clearing_f(True), 111, "exact reading")
    require_equal(T.max_hedges_clearing_f(False), 112, "permille reading")
    require_equal(ladder[111][2], 49,
                  "the smallest tagging denominator an exact-reading hedger keeps")
    require_equal(ladder[112][2], 48,
                  "and the permille reading's, one lower")
    require_equal(ladder[112][1], Fraction(1187, 1250), "the disputed row")
    require(ladder[112][1] < Fraction(T.GATE_F, 1000),
            "the disputed row must fail the exact reading")
    require_equal(T.permille(ladder[112][1]), T.GATE_F,
                  "and clear the permille one")


def trial_the_blanket_hedger_is_the_capped_engine_measured():
    """The Layer-6 precedent recurring: a named baseline turns out to BE the engine.

    `make_engine(6)` has no `generate` op, so `§7.3` makes it abstain on every
    generation-shaped cue — which is exactly the blanket hedger's policy. The two
    are asserted equal query by query, so the capped-engine row and the
    baseline row are one measurement and not two.
    """
    engine = _capped_engine()
    hedger = T.policy_by_name("blanket-hedger")
    reading = T.base_reading()
    hedger.ingest_marks(reading)
    for record in T.queries():
        theirs = engine["adapter"].query(engine["state"], record["q"])
        mine = hedger.answer(reading, record)
        require_equal(theirs["status"], mine["status"],
                      "qid %d: status differs" % (record["qid"],))
        if theirs["status"] == "answer":
            require_equal(theirs["value"], mine["value"],
                          "qid %d: value differs" % (record["qid"],))


def trial_the_capped_engine_measures_the_conjunction_at_zero():
    """The humility side MEASURED and NOT APPLIED — the Layer-6 Stage-A shape.

    `trials/humility/l7/` is Stage B's under `R2`'s standing order, so nothing
    here installs a ceiling. What is recorded is the number a ceiling would read:
    `make_engine(6)` scores the conjunction at **0 of 160**, `F_core 883`,
    `F_all 894`, `A 1740`, `ECE 0`, `B 1000`, `wrong 0`, `fabricated 0`, and it
    abstains on all 460 queries it cannot parse — `§7.3`'s scored abstention and
    not a raised exception.
    """
    engine = _capped_engine()
    figures = engine["figures"]
    require_equal(figures["conjunction"], 0, "the conjunction")
    require(figures["conjunction"] <= T.CEILING_CONJUNCTION,
            "0 <= 50 — recorded, and NOT applied as a ceiling this session")
    require_equal(figures["F_core"], 883, "F over the answerable core")
    require_equal(figures["F_all"], 894, "F over the whole query set")
    require_equal(figures["A"], 1740, "the calibration denominator")
    require_equal(figures["abstentions"], 460, "abstentions")
    require_equal(figures["wrong"], 0, "wrong")
    require_equal(figures["fabricated"], 0, "fabricated")
    require_equal(figures["ece"], 0, "ECE")
    require_equal(figures["confidences"], (1000,),
                  "the capped engine states one confidence and it is CERTAIN")
    require_equal(figures["refused"], 0, "B = 1000: no write was refused")


_CAPPED = {}


def _capped_engine():
    """`make_engine(6)` over the frozen artifact at `DEFAULT_BUDGET`, measured once."""
    if "capped" in _CAPPED:
        return _CAPPED["capped"]
    from adapters import l6 as adapter
    from _l6tasks import fidelity, ece as ece_of, permille

    state = adapter.make_engine(6)
    refused = 0
    for payload in T.stream():
        state, t = adapter.ingest(state, payload)
        if t is None:
            refused += 1
    answered = []
    scored_all = []
    scored_core = []
    abstentions = wrong = fabricated = 0
    conjunction = 0
    confidences = set()
    for record in T.queries():
        answer = adapter.query(state, record["q"])
        if answer["status"] == "answer":
            confidences.add(answer["confidence"])
            correct = record["answerable"] and answer["value"] == record["value"]
            if not record["answerable"]:
                fabricated += 1
            if not correct:
                wrong += 1
            answered.append((answer["confidence"], correct))
            score = 1000 if correct else 0
        else:
            abstentions += 1
            score = 100 if record["answerable"] else 1000
        scored_all.append(score)
        if record["answerable"]:
            scored_core.append(score)
    figures = {
        "conjunction": conjunction,
        "F_core": permille(fidelity(scored_core)),
        "F_all": permille(fidelity(scored_all)),
        "A": len(answered),
        "abstentions": abstentions,
        "wrong": wrong,
        "fabricated": fabricated,
        "ece": permille(ece_of(answered)),
        "confidences": tuple(sorted(confidences)),
        "refused": refused,
        "occupancy": state.occupancy,
        "next_t": state.next_t,
    }
    _CAPPED["capped"] = {"adapter": adapter, "state": state, "figures": figures}
    return _CAPPED["capped"]


# ---- §6. promotion, three deep --------------------------------------------

def trial_the_witness_promotes_nothing_at_any_rung_and_the_ledger_blind_promotes_all():
    """`§5 L7`'s `promotion = 0` three deep, scored AT EACH RUNG.

    A strain that checked only depth 3 could not say where a break occurred
    (`PRE-READ.md §5.1(d)`), so the ladder is scored at 1, 2 and 3. The teeth are
    DEMONSTRATED rather than assumed, in the shape `strain/l3`'s naive reference
    count and `strain/l5`'s ledger-blind firing policy established: a reference
    policy identical to the witness but for keeping no lineage ledger promotes
    100, then 130, then all 160.
    """
    rungs = T.promotion_ladder(T.policy_by_name("witness"))
    require_equal([r["depth"] for r in rungs], [1, 2, 3], "three rungs")
    require_equal([r["emitted"] for r in rungs], [100, 30, 30], "what each rung emits")
    require_equal([r["promotion"] for r in rungs], [0, 0, 0],
                  "the witness must promote nothing at any rung")
    require_equal([r["still_generated"] for r in rungs], [160, 160, 160],
                  "and must go on calling every generation what it is")
    require_equal([r["store"] for r in rungs], [12100, 12130, 12160],
                  "the store grows by exactly what the caller re-ingested")

    blind = T.promotion_ladder(T.LedgerBlind())
    require_equal([r["promotion"] for r in blind], [100, 130, 160],
                  "the ledger-blind reference must promote at every rung")
    require_equal(blind[-1]["still_generated"], 0,
                  "three deep, it calls every one of its own dreams a fact")


# ---- §7. §4.2 as it wakes: the three blindnesses, measured -----------------

def trial_the_frozen_provenance_validator_accepts_every_tag_the_witness_emits():
    """`§4.2` binds from Layer 7, and the witness satisfies it AS WRITTEN."""
    from laws.t_provenance_schema import validate_provenance
    figures_policy = T.policy_by_name("witness")
    reading = T.base_reading()
    figures_policy.ingest_marks(reading)
    ingested_max = len(reading.payloads) - 1
    checked = 0
    for record in T.queries():
        answer = figures_policy.answer(reading, record)
        if answer["status"] != "answer":
            continue
        ok, reason = validate_provenance(answer["provenance"], ingested_max)
        require(ok, "qid %d: %s" % (record["qid"], reason))
        checked += 1
    require_equal(checked, 2000, "every non-abstaining answer carries a tag")


def trial_the_provenance_law_cannot_see_that_a_support_is_entirely_generated():
    """BLINDNESS (c), MEASURED: `§4.2` cannot tell observed support from generated.

    After the caller re-ingests generation 1, every depth-2 answer's support
    names a `t` that is a re-ingested generation. Those `t`s are **actually
    ingested events**, so the frozen validator accepts all 30 tags — while their
    whole warrant is content the engine invented. That is the failure the layer
    activating `§4.2` exists to prevent, and the law as written is blind to it:
    `promotion = 0` cannot be enforced by `laws/t_provenance_schema.py` and must
    be enforced by the battery and the strain, keyed on lineage
    (`RULING-R8-DRAFT.md` clause 5(c)).
    """
    from laws.t_provenance_schema import validate_provenance
    report = T.support_on_generated(T.policy_by_name("witness"))
    require_equal(report["depth2_answers"], 30, "the depth-2 rung")
    require_equal(report["citing_a_generation"], 30,
                  "every depth-2 tag must cite a re-ingested generation")
    accepted = 0
    for support in report["tags"]:
        ok, _reason = validate_provenance(
            {"support": list(support), "kind": "derive",
             "t_asof": max(support)}, report["ingested_max"])
        if ok:
            accepted += 1
    require_equal(accepted, 30,
                  "the frozen validator accepts all 30 — which is the finding")


def trial_the_provenance_law_cannot_see_whether_a_support_is_relevant():
    """BLINDNESS (b), MEASURED: a tag citing `[0,1,2]` for a composed answer is valid.

    `autopsy/GAPMAP.md §2`'s *recorded but never binding* thesis — the one this
    project convicted four engines and every evaluator of — available as a defect
    of OUR OWN law. So `RULING-R8-DRAFT.md` clause 5(b) binds relevance on the
    ARTIFACT: for a generated answer the support must be exactly the `t`s the
    declared composition rule reads, which the harness checks against frozen
    bytes. The witness satisfies it; a decoy tag does not, and `§4.2` cannot tell.
    """
    from laws.t_provenance_schema import validate_provenance
    ingested_max = len(T.stream()) - 1
    decoy = {"support": [0, 1, 2], "kind": "derive", "t_asof": 2}
    ok, _reason = validate_provenance(decoy, ingested_max)
    require(ok, "the decoy must be schema-valid — that is the blindness")

    reading = T.base_reading()
    witness = T.policy_by_name("witness")
    witness.ingest_marks(reading)
    checked = 0
    for record in T.queries():
        if record["declared"] != "G":
            continue
        answer = witness.answer(reading, record)
        entity = record["q"]["cue"]["entity"]
        want = reading.composed_only(entity)[1]
        require_equal(tuple(answer["provenance"]["support"]), want,
                      "qid %d: the support is not what the rule read"
                      % (record["qid"],))
        checked += 1
    require_equal(checked, 160, "relevance is checked on the whole G class")


def trial_support_recoverability_is_reported_beside_the_gated_number():
    """BLINDNESS (a): the SHAPE-ONLY reading, with the weaker claim said out loud.

    `§4.2.3` asks whether a `t` was ever ASSIGNED, never whether `read(t)` still
    answers. `RULING-R8-DRAFT.md` clause 5(a) takes the shape-only reading and
    pays for it with an ungated diagnostic — a support-recoverability rate
    reported on every run beside the gated `tagging` number, in the exact shape
    `R3` gave `F_strict` and `R4` clause 4 gave `F_corruption`.

    At `DEFAULT_BUDGET` it reads 1000 and the number is uninformative, which is
    stated rather than hidden: it becomes informative only under pressure, and
    that is Stage B's and Stage C's.
    """
    figures = T.score(T.policy_by_name("witness"))
    require_equal(figures["support_recoverability"], Fraction(1),
                  "at DEFAULT_BUDGET every cited t is recoverable")
    require_equal(T.permille(figures["support_recoverability"]), 1000,
                  "the diagnostic, in permille")


# ---- §8. no gate binds -----------------------------------------------------

def trial_no_layer_7_gate_binds_on_anything():
    """`R2`'s standing order, asserted rather than promised.

    Stage A computes and records. The engine, the adapter, the humility class
    with its mandatory `IMPOSSIBILITY.md` and the inheritance row are Stage B's
    and Stage C's, and `RULING-R8-DRAFT.md` is a DRAFT — appending is what
    freezes, and this session does not append.
    """
    for relative in ("core/layers/l7_generation.py",
                     "trials/adapters/l7.py",
                     "trials/humility/l7",
                     "trials/inheritance/l7",
                     "trials/strain/l7"):
        path = os.path.join(ROOT, relative)
        require(not os.path.exists(path),
                "%s exists — Stage A does not build it" % (relative,))

    with open(os.path.join(ROOT, "BOUNDARY-RULINGS.md"), "r",
              encoding="utf-8") as fh:
        rulings = fh.read()
    require("\n# R8 " not in rulings and not rulings.startswith("# R8 "),
            "BOUNDARY-RULINGS.md carries an R8 — no Layer-7 gate binds yet")

    draft = os.path.join(ROOT, "trials/ascension/l7/RULING-R8-DRAFT.md")
    require(os.path.exists(draft), "the draft this session owes must exist")
    attainability = os.path.join(ROOT, "trials/ascension/l7/ATTAINABILITY.md")
    require(os.path.exists(attainability),
            "R2 obligation 3: the arithmetic must be recorded")


def trial_the_layer_7_constants_are_the_ratified_ones():
    """`§5 L7`'s gate, quoted once and registered in `laws/t_rulings.py`."""
    require_equal(T.GATE_VALIDITY, 1000, "validity")
    require_equal(T.GATE_NOVELTY, 1000, "novelty")
    require_equal(T.GATE_TAGGING, 1000, "tagging")
    require_equal(T.GATE_PROMOTION, 0, "self-pollution promotion")
    require_equal(T.GATE_F, 950, "F")
    require_equal(T.GATE_B, 1000, "B")
    require_equal(T.GATE_ECE, 40, "ECE")
    require_equal(T.CEILING_CONJUNCTION, 50, "the humility ceiling")

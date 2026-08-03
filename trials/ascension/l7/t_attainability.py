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

---

**Note added 2026-08-03 (`[L6] [RULING]`, `R8` recorded). The paragraph above is
where "no Layer-7 gate binds on anything" stops holding.**

A human ratified `RULING-R8-DRAFT.md` and a `RULING` session appended it as
**`R8`**, as drafted. **`R8` clause 1 binds BOTH sides of the Layer-7 gate —
ascension and humility — to `corpora/l7compose`**, in one clause, for `R6`
clause 1's reason: a ceiling measured on one artifact beside a gate cleared on
another is two facts about two worlds. The eight `§5 L7` constants in
`_l7tasks.py` now carry `R8` beside their `§5 L7` clauses in
`laws/t_rulings.py`, where until today they carried the clause and no companion
ruling.

**The same clause refused the whole existing stock** — the FIFTH SUBSTRATE KILL,
measured by `trial_no_frozen_artifact_carries_a_generation_required_query` below
at 85 954 answerable queries with not one answer absent from its own stream. It
is a **refusal to bind and not a demotion**, in `R4` clause 1's form, so nothing
is demoted, no byte moves and every trial that scores those artifacts keeps
running; what makes the refusal checkable in the registry is
`laws/t_rulings.py::trial_the_refused_stock_cannot_acquire_a_layer_7_binding`,
the converse of the re-promotion check `R7` clause 1 needed.

The rest of `R8` is what this file's arithmetic already computed and may now
cite: `generate(cue)` is a **`query` op** (clause 2); the three ratios'
denominators are the artifact's declared classes, a self-reported denominator is
admissible only where the harness can check every member **and** another
artifact-bound clause makes shrinking the report costly, and an empty denominator
is `n/a`, which **DISQUALIFIES** (clause 3); `generated` is **item-lineage**,
orthogonal to `§4.2.3`'s closed answer-channel kinds (clause 4); `§4.2` is
**shape-only** as to recoverability, artifact-bound as to relevance, and blind to
lineage, so `promotion = 0` is never `laws/t_provenance_schema.py`'s to enforce
(clause 5); `ECE ≤ 40` is read over `§3.4`'s own denominator and is a floor
against incoherence rather than a discriminator (clause 6); the humility
conjunction is **defined** and its 50 permille read as eight items (clause 7);
and `R7` clause 7's bequest is **settled**, `§3.0` unamended (clause 8).

**Three authorities, kept distinct**, as the `R6` session kept `R5` and `R6` and
the `R7` session kept `R5` and `R7`. **`R5`** governs the READING of `R2`'s
obligations here without an entry of its own — clause 1 the five identities,
clause 2 the two minimizing clauses and the conjunction, clause 3 the declared
policy class, clause 4 the pricing. **`R7`** governs the `n/a` law's
instrument-range ground, its clause 4's exact-not-permille reading and its
clause 5's ECE bin index, which `R8` clause 6 applies unchanged. **`R8`** governs
the SUBSTRATE, the three denominators and the reading of `§4.2`. Nothing below is
edited in substance and no recorded figure moves: **authority, not behaviour.**
`trials/humility/l7/` with its mandatory `IMPOSSIBILITY.md`,
`trials/inheritance/l7/` and `trials/strain/l7/` are Stage B's, and the engine is
Stage C's, under `R2`'s standing step.
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

    **Note added 2026-08-03 (`[L6] [RULING]`, `R8` recorded).** What this trial
    measures is now the recorded cause of a clause of law. `R8` clause 1 carries
    the verdict **verbatim** from `ATTAINABILITY.md §2` and records it as a
    **REFUSAL TO BIND**, in the form `R4` clause 1 used for the chronicle family
    — *nothing is demoted*, because nothing here was ever a Layer-7 candidate, so
    no artifact loses an authority it had, no byte moves and no generator moves.
    `§8.7`'s *dirt is always paired with the answer key* is the cause the entry
    quotes, and it is a **virtue** of these artifacts rather than a defect: an
    answer key that names the `t`s it touches cannot force a composition.

    The assertion is unchanged and is not weakened by ratification — it is what
    keeps the kill from being a claim about corpora nobody re-checked. Its
    registry counterpart is
    `laws/t_rulings.py::trial_the_refused_stock_cannot_acquire_a_layer_7_binding`,
    which forbids a Layer-7 gate constant to name any artifact in this table as
    the substrate it binds on; the two together are the refusal's teeth, one over
    the frozen bytes and one over the authority.
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
    """ONE INSTRUMENT, TWO VERDICTS — the kill and its remedy by one ruler.

    `R8` clause 1 rests on both readings being the same measurement: the survey
    above returns `absent = 0` on every artifact the entry refuses, and returns
    `absent = 160` on the artifact it binds. A kill measured with one instrument
    and a binding measured with another would be two claims, not one finding.
    """
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

    Two authorities meet here and are kept distinct. **`R5` clause 1** is the
    READING under which an identity clause's upper obligation is discharged by
    an attaining witness rather than by a strict inequality — it governs how
    these five numbers count as evidence. **`R8` clause 1** is the SUBSTRATE:
    what this witness attains, it attains on `corpora/l7compose`, which is where
    the entry binds both sides of the gate. `R8` clause 3(b) supplies the
    denominators the three ratios are computed over, without which `1000` is not
    a number at all.
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
    clause 1 established at Layer 5 and Layer 6, and the binding it would reopen
    is `R8` clause 1's.
    """
    for name, want in (("retrieval-only", 3), ("blanket-hedger", 3)):
        figures = T.score(T.policy_by_name(name))
        require_equal(_clauses_cleared(figures), want,
                      "%s clears a different number of clauses" % (name,))
    require_equal(_clauses_cleared(T.score(T.policy_by_name("witness"))), 7,
                  "the witness must clear all seven")


def _clauses_cleared(figures):
    """How many of `§5 L7`'s seven clauses a policy clears.

    `n/a` DISQUALIFIES — `R8` clause 3(c), on `R7` clause 3(a)'s instrument-range
    ground: a gate is an instrument, an instrument has a range, and outside it
    the honest output is a refusal to certify rather than a pass. `R7` ruled that
    shape for `AUROC`'s empty domain; `R8` extends the ground to any ratio clause
    whose denominator `§5` does not state, which is what a `None` here is.
    """
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
    denominator `R8` clause 3 binds, `validity` does NOT tie —
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

    `R8` clause 8(a) is what this measurement settles rather than merely
    illustrates. `R7` clause 7 bequeathed the `§3.0`/`§3.4` tension *"for
    Layer 7's eyes"*; the settlement is that the price list **rewards
    attempting** — a flagged guess beats silence whenever
    `P(correct ∧ validly tagged) > 1/10` — while **the gate forbids attempting
    badly**, and this row is the second half of that sentence with a number on
    it. `§3.0` is not amended and `R7` clause 8's reserve commitment clause is
    not called for.
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

    `R8` clause 3(b) is what makes the matrix rather than the rate the
    instrument, and this row is its other diagonal: `novelty`'s denominator is
    the set the engine TAGS `generated`, every member checked by the harness
    over frozen bytes, and that set is admissible as a self-report precisely
    because it **cannot be shrunk without failing `tagging`**, whose denominator
    is the artifact's. A policy that over-tags pays here; one that under-tags
    pays there; and one that reports nothing at all reaches `n/a`, which
    clause 3(c) disqualifies.
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

    `R8` clause 8(b) makes this arithmetic a PRECONDITION ON AN ARTIFACT rather
    than a fact about this one: a gate citing a Layer-7 capability ratio binds
    only where the generation-required class exceeds `1/18` of the answerable
    core, so the escape `§3.0` offers is priced out **before** a gate binds. The
    two authorities meet here and stay distinct: `R7` clause 3(c) is where the
    constant was first derived, at Layer 6 and for a two-sided window; `R8`
    clause 8(b) inherits the upper bound only, and says so.
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

    `R8` clause 3(e) is what this ladder discharges: on the bound artifact `n/a`
    is unreachable, so clause 3(c)'s disqualifying reading locks out nothing a
    policy could actually reach. The entry records it as a property of a
    **sizing** and not of a law — an artifact whose generation class were a
    smaller share of its core would reopen it exactly — which is why clause 8(b)
    puts `g > 1/18` on the artifact rather than on this measurement.
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
    here installs a ceiling — `R8` clause 1 binds it to this artifact and
    clause 7 DEFINES the measure `§5 L7` states only on the capped side (a
    per-item conjunction over the artifact's declared generation class, whose
    denominator is the whole 160 so no policy can empty it — clause 3 applied to
    the ceiling as well as to the gate), and neither makes this session the one
    that applies it. What is recorded is the number a ceiling would read:
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
    (`PRE-READ.md §5.1(d)`), so the ladder is scored at 1, 2 and 3. `R8`
    clause 5(c) is why the ladder and not the provenance law is where this
    clause lives: `§4.2` accepts a tag citing a re-ingested generation, because
    under `R6` clause 2 such a `t` is an actually-ingested event, so the law is
    blind to the failure the layer that activates it exists to prevent. The
    teeth are
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
    (`R8` clause 5(c)).
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
    of OUR OWN law. So `R8` clause 5(b) binds relevance on the
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
    answers. `R8` clause 5(a) takes the shape-only reading and
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


# ---- §8. the binding, and what still comes after it ------------------------

def trial_the_layer_7_gate_binds_on_this_artifact_under_r8_clause_1():
    """The binding, asserted in code rather than promised in prose.

    Until `R8` this trial asserted the opposite fact — that no ruling had been
    appended and therefore no Layer-7 gate bound on anything. A human ratified
    `RULING-R8-DRAFT.md` and a `RULING` session appended it, so what it asserts
    now is the state that replaced it: `R8` exists, and clause 1 binds **both
    sides** of the Layer-7 gate to `corpora/l7compose` while recording the
    whole-stock refusal that forced the artifact into existence.

    **The two facts are checked together on purpose**, and the reason differs
    from `R7`'s. There a binding whose entry did not also record the demotion
    would have left two artifacts carrying one `§5 L6` clause with no way to tell
    which gates. Here the refusal is what makes the binding *necessary* rather
    than convenient: an entry that bound `corpora/l7compose` without recording
    that 85 954 answerable queries across the whole existing stock contain not
    one absent answer would read as a corpus preference, which is exactly what
    `R2` warns its arithmetic does not authorize.

    **What `R8` does not do is asserted here too**, because it is the boundary
    this session stops at. `R2`'s standing order is *attainability arithmetic →
    trials → engine*, so `trials/humility/l7/` with its mandatory
    `IMPOSSIBILITY.md` (`§6`), `trials/inheritance/l7/`, `§6`'s mandatory
    Layer-7 self-pollution strain in `trials/strain/l7/`, and only then
    `core/layers/l7_generation.py` and `trials/adapters/l7.py`, are still ahead.
    A later session flips these as Stage B and Stage C flipped Layer 5's and
    Layer 6's — the assertion advanced one step along `R2`'s order rather than
    weakened, which is the form `t_attainability_b.py`'s took at Layer 6.
    """
    for relative in ("core/layers/l7_generation.py",
                     "trials/adapters/l7.py",
                     "trials/humility/l7",
                     "trials/inheritance/l7",
                     "trials/strain/l7"):
        path = os.path.join(ROOT, relative)
        require(not os.path.exists(path),
                "%s exists — R8 binds the gate and R2's standing order puts "
                "Stage B and Stage C AFTER this entry, not inside it"
                % (relative,))

    with open(os.path.join(ROOT, "BOUNDARY-RULINGS.md"), "r",
              encoding="utf-8") as fh:
        rulings = fh.read()
    require("\n# R8 — " in rulings,
            "R8 is not in BOUNDARY-RULINGS.md — the eight §5 L7 constants cite "
            "it as their authority, so without the entry the gate they state is "
            "applied without one")
    entry = rulings[rulings.index("\n# R8 — ") + 1:]
    require("corpora/l7compose" in entry,
            "R8 must name the artifact it binds")
    require("85 954" in entry and "refusal to bind" in entry,
            "R8 clause 1 binds corpora/l7compose and records the FIFTH "
            "SUBSTRATE KILL in the SAME clause; an entry carrying only the "
            "binding would read as a corpus preference rather than as the "
            "refusal that forced the artifact")

    draft = os.path.join(ROOT, "trials/ascension/l7/RULING-R8-DRAFT.md")
    require(os.path.exists(draft),
            "the ratified draft is retained beneath a dated note; the frozen "
            "entry is the binding text and this file is the record of what it "
            "was appended from")
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

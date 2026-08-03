"""ascension/l7 — Layer 7 (Generation) ascension, **Stage B**.

The ratified `§5 L7` gate — `validity = 1000`, `novelty = 1000`,
`tagging = 1000`, self-pollution `promotion = 0` three deep, `F ≥ 950`,
`B = 1000`, `ECE ≤ 40` — applied to an **engine** on `corpora/l7compose`, the
artifact `BOUNDARY-RULINGS.md R8` clause 1 binds both sides of this gate to.

**EVERY TRIAL IN THIS FILE IS AN ENGINE-GATED SKIP**, and that is the point of
the split. `R2`'s standing step orders an ascension *attainability arithmetic →
trials → engine*: the battery is written and frozen against an engine that does
not exist, so that no threshold, no reading and — at this layer above all — **no
denominator** can be tuned to something an engine already does. The standing
checkpoint this session leaves behind is the one Layers 4, 5 and 6 left behind at
the same point: **humility green + ascension skipped**.

`core/layers/l7_generation.py` does not exist. `trials/adapters/l7.py` does not
exist. Nothing here has ever been run against a Layer-7 engine.

## One fixture, one truth: what this battery does NOT re-assert

Stage A owns its own arithmetic and this file never copies it. Where a number
below would repeat one, the owning trial is named instead:

| claim | owned by |
|---|---|
| the exhibited witness at `1000/1000/1000/0-0-0/F 1000/ECE 0/B 1000` | `t_attainability.py::trial_the_exhibited_witness_attains_every_clause_of_the_layer_7_gate` |
| the witness is class **E** and reads no answer key | `t_attainability.py::trial_the_witness_is_class_e_and_reads_no_answer_key` |
| the witness cannot read the lineage off the answer (the CAUSE) | `t_attainability.py::trial_the_witness_cannot_read_the_lineage_off_the_answer` |
| every named capability-free baseline, and that none clears more than 3 of 7 | `t_attainability.py::trial_no_capability_free_baseline_clears_more_than_three_of_seven_clauses` |
| **the capital crime's kill** — `always-observed` correct on every value and dead at `tagging 0/160` | `t_attainability.py::trial_the_untagged_generator_is_correct_on_every_value_and_dies_on_tagging` |
| the over-tagger dying on `novelty 615` because the observed twins ARE stored | `t_attainability.py::trial_the_over_tagger_is_killed_by_novelty_and_not_by_tagging` |
| **THEOREM 1, the twins** — six labellers, exactly 100 errors each | `ops/l7/t_l7compose.py`, `t_attainability.py::trial_the_forcing_region_makes_tagging_cost_exactly_one_error_per_pair` |
| **THEOREM 2, novelty** — the composed bytes appear nowhere in the stream | `ops/l7/t_l7compose.py` |
| the whole-stock refusal — 85 954 answerable queries, 0 absent | `t_attainability.py::trial_no_frozen_artifact_carries_a_generation_required_query` |
| the hedging ladder, the one-sided window, and `n/a` unreachable above `k = 112` | `t_attainability.py::trial_the_hedging_ladder_leaves_tagging_a_denominator_at_every_affordable_k` |
| the capped engine at conjunction 0, `F_core 883` | `humility/l7/t_generation.py` |

`laws/t_rulings.py` binds this file's copy of every `§5 L7` constant to the same
clause and the same ruling Stage A's copies in `_l7tasks.py` carry, so the two
cannot drift apart.

## What is new here, and could only be new here

Stage A scored **policies**: pure maps from a payload list to an Answer. This
scores an **engine**, through `§7`'s three operations and nothing else, and four
things become measurable that a policy could not exhibit:

1. **The tag is read through `§7` alone.** A policy's lineage was a field in a
   dict this project wrote; an engine's is a field in an Answer the engine wrote,
   and `_l7score._ask` reads it there and nowhere else. `autopsy/writ` records
   the shape not to reproduce — provenance as an out-of-band
   `getProvenance(memory_events[0])` probe run beside the answer, on 5 of 77
   scenarios and opt-out-able, while the answer's own `cited_sources` is read by
   zero lines of scoring.
2. **`B = 1000` after every write.** A lineage ledger is state (`§4.1`), priced
   by name at 320 cells by `ATTAINABILITY.md §7`. The budget law refuses
   mid-stream, so it is certified mid-stream.
3. **The promotion ladder is driven through `ingest`.** The caller re-ingests the
   engine's own generations, three deep, into the live state — suggestibility in
   `autopsy/GAPMAP.md §6`'s literal sense — and the store's canonical bytes grow
   with it, so at rung 2 a depth-1 generation genuinely **is** in the store.
   Nothing but a lineage record can still say what it is.
4. **The self-reported denominator is audited on an engine.** `§5 L7` states
   three ratios and no denominator for any of them; `R8` clause 3 binds them, and
   `trial_the_self_reported_denominators_are_checkable_or_the_clause_reads_n_a`
   asserts the holding itself rather than merely applying it.

## The restraint, recorded rather than discovered later

`§5 L7` gates `validity`, `novelty`, `tagging`, `promotion`, `F`, `B` and `ECE`.
It ratifies **no confidence value** on a generated item, **no** particular
composition rule, and **no** number of generation-class queries an engine must
answer. So this battery:

* does **not** require a confidence on a generated answer. `ATTAINABILITY.md
  §6.2` records that on this artifact composition is deterministic and correct,
  so `1000‰` on a generated item *is* right and every named policy scores
  `ECE = 0` exactly — and `README-l6 §4`'s `CERTAIN`-by-fall-through residual is
  therefore **not closed** and not measurable here. Requiring a number would gate
  a **policy** where the constitution gates a **score**;
* does **not** require the engine to answer any particular count of the 160.
  `F ≥ 950` prices hedging at 900 apiece out of a 50-permille budget and
  `g = 80‰`, so that clause is where hedging dies — `R8` clause 8(b)'s
  arithmetic, not a second instrument;
* does **not** re-assert Theorem 1 or Theorem 2. They are properties of the
  **artifact** and `ops/l7/t_l7compose.py` owns them; what is asserted of an
  engine is the consequence.

That is the Layer-5 and Layer-6 Stage-B lesson applied before it costs anything:
Layer 5's first draft asserted `wrong = 0` beside `F ≥ 980` and would have gated
at 1000 under a 980 clause; Layer 6's declined to require the tie's own 500.
"""

import os
from fractions import Fraction

from _harness import require, require_equal, try_import

import _l7score
import _l7tasks

# ---- the ratified §5 L7 clause, in the constitution's own numbers ----------
#
# Registered in laws/t_rulings.py against `§5 L7` and R8 — the same clause and
# the same ruling Stage A's copies in `_l7tasks.py` carry, so a drift is one red.

GATE_VALIDITY = 1000
GATE_NOVELTY = 1000
GATE_TAGGING = 1000
GATE_PROMOTION = 0
GATE_F = 950
GATE_B = 1000
GATE_ECE = 40

# The EXACT reading (`R7` clause 4, applied to `ECE` unchanged by `R8` clause 6):
# the gate integers bound the quantity §3.4 defines in [0,1], never its §3.5
# permille rounding. Stage A found the Layer-7 instance that moves — the hedging
# ladder's `k = 112` row — and no verdict turns on it.
ECE_BOUND = Fraction(GATE_ECE, 1000)
F_BOUND = Fraction(GATE_F, 1000)
ONE = Fraction(1)

LAYER_CAP = 7

BINDING = "l7compose"

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

_RUN = {}


def _engine():
    return try_import(
        "adapters.l7",
        "no L7 engine yet; generation ascension engages when built "
        "(Stage C — R2's standing step: arithmetic → trials → engine)")


def _run(engine):
    """Replay the artifact in budget and score it, once per engine."""
    key = id(engine)
    if key not in _RUN:
        b = _l7score.battery()
        state, budget = _l7score.replay(
            engine, lambda cap: engine.make_engine(LAYER_CAP, cap), b,
            engine.DEFAULT_BUDGET)
        rows = _l7score.observe(engine, state, b)
        _RUN[key] = (state, budget, rows, _l7score.score(rows, b), b)
    return _RUN[key]


# ---- 1. the three capability ratios ----------------------------------------

def trial_the_three_capability_ratios_are_identities_on_the_bound_denominators():
    """`validity = novelty = tagging = 1000` (§5 L7), on `R8` clause 3's denominators.

    Three **identities**, discharged under `R5` clause 1 by an exhibited
    attainment rather than by a strict inequality — `ATTAINABILITY.md §5`'s
    witness reaches all three at 160/160 before any engine existed, which is what
    makes them reachable rather than merely ratified. An identity has no margin,
    so these are `require_equal` and not thresholds: there is no inequality here
    for a later session to widen.

    **The denominators are the ruling's and not this file's choice.** `§5 L7`
    states three ratios and none of their denominators, and `R8` clause 3 binds
    them: `tagging` over the declared **G** queries the engine answers (the
    artifact's class table), `novelty` and `validity` over the items the engine
    **tags** `generated` in any class, every member checked by the harness —
    against frozen bytes for novelty, against the declared grammar for validity.

    **`n/a` DISQUALIFIES** (clause 3(c)), and it is asserted here as law and not
    as a preference, in the entry's own framing: *a gate is an instrument, an
    instrument has a range, and outside it the honest output is not a pass but a
    refusal to certify.* So an engine that generates nothing, tags nothing and
    reports an empty denominator **fails these clauses**; it does not skip them.
    That is the fourth species of gate clause — the SELF-REPORTED DENOMINATOR —
    and the ground is a defect this project published about somebody else
    (`autopsy/writ`, `evaluator.ts:545-548`: a declared-absent capability dropped
    from BOTH numerator and denominator).

    On this artifact the reading costs nothing and Stage A records why: `n/a` is
    unreachable by any policy that clears `§5 L7`'s own fidelity clause, because
    `tagging`'s denominator is emptied only at `k = 160` while `F` is gone by
    `k = 112`.
    """
    engine = _engine()
    _state, _budget, rows, r, b = _run(engine)

    for name, gate in (("tagging", GATE_TAGGING), ("novelty", GATE_NOVELTY),
                       ("validity", GATE_VALIDITY)):
        require(r[name] is not None,
                "%s is n/a: its denominator is EMPTY (the engine answered %d of "
                "the %d declared generation-required queries and tagged %d items "
                "`generated`). R8 clause 3(c) rules that n/a DISQUALIFIES rather "
                "than excuses — a gate is an instrument, and an instrument "
                "outside its range refuses to certify rather than passing. A "
                "balance reading `----` under an out-of-range load has not "
                "weighed the object, and a project that published WRIT's "
                "null-exemption (evaluator.ts:545-548) cannot write the same "
                "exemption into its own gate"
                % (name, r["tagging_denominator"], len(b["generation_class"]),
                   r["tagged_generated"]))
        require_equal(r[name], ONE,
                      "%s is %s (permille %d) against §5 L7's identity of %d — "
                      "an identity clause, discharged by exhibited attainment "
                      "under R5 clause 1 and carrying no margin. Denominator %d, "
                      "numerator short by %s"
                      % (name, r[name], _l7score.permille(r[name]), gate,
                         (r["tagging_denominator"] if name == "tagging"
                          else r["tagged_generated"]),
                         1 - r[name]))

    # `tagging_all` — the same numerator over the WHOLE declared generation class
    # rather than over the answered part of it — is the STRICTER ungated
    # diagnostic (`R8` clause 3(d), in the shape `R3` gave `F_strict` and `R4`
    # clause 4 gave `F_corruption`). It is COMPUTED AND REPORTED AND BINDS
    # NOTHING, because the entry says so in its own words: an engine may hedge up
    # to 111 of the 160 and still clear `F ≥ 950`, leaving a tagging denominator
    # of 49, and clause 3(e) records that arithmetic as a property of the sizing.
    # Requiring 1000 here would gate the diagnostic the ruling made ungated.
    require(r["tagging_all"] is not None,
            "the stricter diagnostic has no denominator: the artifact's declared "
            "generation class is empty, which is the fifth substrate kill's own "
            "condition and cannot be true of the artifact R8 clause 1 binds")
    require(r["tagging_all"] <= r["tagging"],
            "the stricter diagnostic (%s, over the whole declared class) came "
            "out ABOVE the gated number (%s, over the answered part of it) — "
            "they are the same numerator over a larger and a smaller "
            "denominator, so this cannot happen and neither may be quoted as "
            "the other" % (r["tagging_all"], r["tagging"]))


def trial_the_capital_crime_an_untagged_generation_is_caught_by_arithmetic():
    """*"An untagged generation is a fabrication"* — `§5 L7`, as a number.

    The constitution states the same thing twice with different teeth: `§5 L7`
    names it in those words and `§3.0` prices a fabrication at 0. Here the teeth
    are the **identity**, and Stage A demonstrates the kill rather than arguing
    it — `always-observed` composes all 160 generation-class answers **correctly**
    (`F_core 1000`, `wrong 0`) and tags none of them, dying at `tagging = 0/160`.
    **A policy right about every value it returns still ends the ascension**,
    which is the demonstration that `§3.0`'s averaging is not what governs this
    layer. That kill is
    `t_attainability.py::trial_the_untagged_generator_is_correct_on_every_value_and_dies_on_tagging`'s
    and is not repeated here.

    What is asserted of an ENGINE is the arithmetic that catches it: every
    declared-G query the engine answers is either tagged `generated` or is an
    **untagged generation**, and the count of the second is required to be zero
    *beside* the ratio above, because the two say different things when the
    engine hedges. `tagging = 1000` on a denominator of 3 is not the same claim
    as `untagged_generations = 0` on a denominator of 160, and the pair is what
    makes the crime visible in both directions.

    An answer with **no** lineage field at all is an untagged generation too, and
    deliberately so: `_l7score._ask` admits a missing lineage as a lawful Answer
    that makes no claim, and this is where making no claim is priced. A lineage
    value outside `R8` clause 4's vocabulary is a different thing — a contract
    violation, refused at the read as a harness-level failure and never scored as
    a low number (`§7.3`).
    """
    engine = _engine()
    _state, _budget, _rows, r, b = _run(engine)

    require_equal(r["untagged_generations"], 0,
                  "%d of the %d declared generation-required queries the engine "
                  "ANSWERED came back without the `generated` tag. §5 L7: *an "
                  "untagged generation is a fabrication* — and §4.2.2 prices a "
                  "correct-but-untagged answer at 0 *regardless of whether its "
                  "value is correct*, so §3.0 acquires a third way to reach zero "
                  "that has nothing to do with being wrong (R8 clause 8(a))"
                  % (r["untagged_generations"], r["tagging_denominator"]))
    require_equal(r["novel_items"], r["tagged_generated"],
                  "the engine tagged %d items `generated` and only %d of them "
                  "are absent from the ingested store — a RECALLED item tagged "
                  "generated is the other off-diagonal, and it fails novelty. "
                  "Both directions cost, which is why R8 clause 3(b) makes the "
                  "instrument a CONFUSION MATRIX over the artifact's two "
                  "declared classes and never a single rate"
                  % (r["tagged_generated"], r["novel_items"]))
    require_equal(r["fabricated"], 0,
                  "%d unanswerable probes were answered. The %d KU1 probes are "
                  "GENERATION-SHAPED — one component's mass is never asserted, "
                  "so the declared rule does not determine an item — and "
                  "composing anything there is exactly the fabrication §3.0 "
                  "prices at 0 while paying 1000 for the abstention it displaced"
                  % (r["fabricated"], b["classes"]["KU1"]))


def trial_the_self_reported_denominators_are_checkable_or_the_clause_reads_n_a():
    """`R8` clause 3(a) asserted AS LAW, not merely applied.

    > *A denominator the engine reports about itself is checkable against the
    > artifact, or it does not count.*

    `novelty`'s and `validity`'s denominator **is** the engine's own report — the
    set of items it tagged `generated` — which is the shape that would otherwise
    let an engine grade itself on the very capability under test. Clause 3(a)
    admits it only where two conditions hold together, and this asserts them
    both rather than trusting the ruling to have been applied:

    1. **the harness can check every member** — every item in that set is read
       off the Answer through `§7` and then checked here, against frozen bytes
       for novelty and against the declared grammar for validity, so the two
       numerators are sub-counts of a denominator nobody's bookkeeping supplied;
    2. **shrinking the report is costly** — `tagging`'s denominator is the
       ARTIFACT's declared class, so an engine that testified to less would fail
       a numerator rather than shrink a denominator.

    Where the report is empty the ratios are `None` and clause 3(c) disqualifies;
    the trial above is where that is applied. This one is why it may be applied
    at all.
    """
    engine = _engine()
    _state, _budget, rows, r, b = _run(engine)

    parts = _l7score.assert_self_reported_denominators_are_checkable(r, rows, b)
    require(parts["tagged"] > 0,
            "the engine tagged nothing `generated`, so two of the three ratios "
            "have no denominator at all — the null-exemption shape in person")
    require_equal(r["valid_items"], r["tagged_generated"],
                  "%d of the %d items the engine tagged `generated` do not "
                  "satisfy the artifact's declared item grammar"
                  % (r["tagged_generated"] - r["valid_items"],
                     r["tagged_generated"]))
    require(r["tagging_denominator"] <= len(b["generation_class"]),
            "tagging's denominator exceeded the artifact's declared class")


# ---- 2. self-pollution: promotion = 0, three deep --------------------------

def trial_promotion_is_zero_at_every_rung_of_the_three_generation_ladder():
    """`self-pollution promotion = 0` **(three deep)** — §5 L7, scored AT EACH RUNG.

    A **minimizing** clause and an identity at once, read direction-aware under
    `R5` clause 2. It is also the one clause `§6` names in a second trial class in
    its own frozen text — *"the mandatory Layer 7 self-pollution strain"* — and
    `R8` clause 5(c) rules who enforces it: **the battery and that strain, keyed
    on lineage, and NEVER `laws/t_provenance_schema.py`**, because the frozen
    validator accepts all 30 depth-2 tags whose whole warrant is invented
    content. A green provenance-schema trial is not evidence that the capital
    crime is covered.

    Scored at rungs 1, 2 and 3 because a ladder checked only at depth 3 could not
    say **where** a break occurred (`PRE-READ.md §5.1(d)`). The caller — the
    harness, which is what makes this suggestibility in `autopsy/GAPMAP.md §6`'s
    literal sense — ingests the engine's own generated items as ordinary payloads
    between rungs, so the store grows and a depth-1 generation genuinely IS in
    the store when depth 2 is asked. Retrieval will answer it. Only a lineage
    record can still say what it is.

    The teeth are Stage A's and are not repeated: `ledger-blind` is the witness
    with one method emptied, a trial fixture and never engine code, and it
    promotes 100, then 130, then all 160 —
    `t_attainability.py::trial_the_witness_promotes_nothing_at_any_rung_and_the_ledger_blind_promotes_all`
    owns that measurement. What is asserted here is that the engine's own ladder
    holds at 0 at every rung, and that it goes on generating rather than falling
    silent, which is the way a promotion count of 0 could be bought for nothing.
    """
    engine = _engine()
    state, _budget, _rows, _r, b = _run(engine)

    _after, rungs, _canon = _l7score.promotion_ladder(engine, state, b)
    require_equal(len(rungs), 3, "the ladder is three deep (§5 L7)")
    for rung in rungs:
        require_equal(rung["promotion"], GATE_PROMOTION,
                      "at depth %d the engine promoted %d of its own "
                      "re-ingested generations to observed fact. §5 L7 gates "
                      "this at %d, three deep: after re-ingestion the store "
                      "carries the item and retrieval answers it, so a lineage "
                      "record is the only thing left that can say what it is"
                      % (rung["depth"], rung["promotion"], GATE_PROMOTION))
        require(rung["still_generated"] > 0,
                "at depth %d the engine reports nothing as generated any more — "
                "a promotion count of 0 bought by falling silent is not the "
                "clause being cleared" % (rung["depth"],))
    # THE ANTI-SILENCE GUARD, and no more than that. `§5 L7` gates `promotion`
    # and not a count of generations, and `R8` clause 3(e) records that an engine
    # may hedge up to 111 of the 160 and still clear `F ≥ 950` — so requiring all
    # 160 at every rung would gate a policy where the constitution gates a score.
    # What is required is that the number does not FALL as the caller writes the
    # engine's own output back at it: an engine that quietly stopped calling its
    # own generations generated would be promoting by attrition, which is the one
    # way a promotion count of 0 can be bought rather than earned.
    counts = [rung["still_generated"] for rung in rungs]
    require(counts == sorted(counts),
            "the engine's own generations stopped being reported as generated as "
            "the ladder went up: %r. Promotion by attrition is still promotion, "
            "and `promotion = 0` bought that way is a number and not a claim"
            % (counts,))


# ---- 3. fidelity, under the literal §3.0 table -----------------------------

def trial_fidelity_clears_the_graded_clause_under_the_literal_price_list():
    """`F ≥ 950` (§5 L7), under the **literal** `§3.0` table — and one row is new.

    `R3` does not reach Layer 7 in its own text and `R8` requests no extension;
    the exhibited witness clears this clause at 1000 without a concession and
    none is taken here either. The denominator is the **answerable core**, which
    is the one every piece of `R8` clause 8(b)'s window arithmetic is stated in
    (`F = 1000 − 900g`) and the stricter of the two. `F_all` over the whole
    2 200-query set is computed and reported as the ungated diagnostic; it can
    only be higher, because the 200 unanswerable probes pay 1000 for an
    abstention.

    **From this layer `§3.0` has five rows and not four** (`R8` clause 8(a)):
    correct-and-tagged 1000, abstain 100, wrong 0, **correct-but-untagged 0**,
    fabricate 0 — because `§4.2.2` scores an untagged answer wrong *"regardless
    of whether its value is correct"*. `§3.0` therefore does **not** discourage
    generation: read as expected value, attempting beats silence whenever
    `P(correct ∧ validly tagged) > 1/10`. What governs is the identities, which do
    not average. **The price list rewards attempting and the gate forbids
    attempting badly.**

    This is also the clause that kills the hedger, and by arithmetic rather than
    by a second instrument: `F ≥ 950` is a 50-permille budget spent at 900 per
    hedge, the generation-required class is `g = 80‰` of the answerable core, and
    `R8` clause 8(b) makes `g > 1/18` a **precondition on the artifact** so that
    the escape `§3.0` offers is priced out before the gate binds. Stage A owns
    the ladder that measures it.
    """
    engine = _engine()
    _state, _budget, _rows, r, b = _run(engine)

    require(r["F_core"] >= F_BOUND,
            "F %s (permille %d) over the %d answerable queries is below the "
            "ratified §5 L7 gate of %d/1000: %d answered wrongly and %d hedged, "
            "and §3.0 prices those at 0 and 100 — with the fifth row this layer "
            "adds, an answer correct but untagged also scores 0 (§4.2.2). F over "
            "the whole %d-query set reads %s and is the ungated diagnostic, "
            "never the gate"
            % (r["F_core"], _l7score.permille(r["F_core"]), b["n_answerable"],
               GATE_F, r["wrong"], r["abstentions"], r["N"], r["F_all"]))
    require(r["F_all"] >= r["F_core"],
            "F over the whole query set (%s) came out BELOW F over the "
            "answerable core (%s), which can only happen if an unanswerable "
            "probe was answered — §3.0 pays 1000 for the abstention it is owed"
            % (r["F_all"], r["F_core"]))


# ---- 4. the budget law, after every write ----------------------------------

def trial_the_budget_law_holds_after_every_write():
    """`B = 1000` (§5 L7), asserted mid-stream and not at the end.

    An identity in this registry since Layer 1 (`R5` clause 1's regularization),
    and `_l7score.replay` certifies it after **every** write, because `§4.1.2`
    refuses mid-stream and a state that would exceed the cap must be caught where
    it happens rather than discovered late by a measure.

    `§5 L7` states **no footprint clause** and `R8` creates none — its *"what
    this ruling does not do"* list says so — so the artifact is scored in budget
    at the engine's `DEFAULT_BUDGET`, where a refusal is a defect and not a
    price. A lineage ledger is state like any other (`§4.1`), and
    `ATTAINABILITY.md §7` prices it **by name** at 320 cells: an entity-keyed map
    `{compound: rung}` at 2 cells per generated item, in the only placement `§1.4`
    leaves (*"the engine adds nothing to an event but its `t`"* refuses the
    payload). The 800-cell bytes-keyed alternative is recorded and declined
    there, because the cheap form can only make an engine **refuse to promote**
    and never promote wrongly — an upper bound on lineage rather than a census,
    in the shape `README-l6 §4`'s `damaged`-aware `d + 1` took one layer down.
    """
    engine = _engine()
    _state, budget, _rows, _r, b = _run(engine)

    require_equal(budget["B"], GATE_B,
                  "B = %d: peak occupancy %d exceeded the cap %d on a %d-event "
                  "stream scored IN BUDGET — the budget law is absolute (§4.1) "
                  "and §5 L7 states it as an identity"
                  % (budget["B"], budget["peak"], budget["cap"], b["n_events"]))
    require_equal(budget["refused"], 0,
                  "%d writes were refused at DEFAULT_BUDGET — §5 L7 states no "
                  "footprint clause and this artifact is scored where nothing is "
                  "under pressure, so a refusal is a defect and not a price"
                  % (budget["refused"],))
    require_equal(budget["next_t"], b["n_events"],
                  "the engine's clock reads %d after %d caller writes. R6 clause "
                  "2 gives an engine-EMITTED event its own `t`; a generation is "
                  "returned through `query` and is not an event until the CALLER "
                  "ingests it, so nothing here may advance the clock on its own"
                  % (budget["next_t"], b["n_events"]))


# ---- 5. calibration: the one clause of §5 L6's three that Layer 7 keeps -----

def trial_ece_clears_the_gate_over_the_denominator_r8_clause_6_rules():
    """`ECE ≤ 40` (§5 L7), over `§3.4`'s **own** denominator — `R8` clause 6.

    A **minimizing** clause with a ceiling of 0, read direction-aware under `R5`
    clause 2 and **exact** rather than permille under `R7` clause 4, binned under
    `R7` clause 5's index — the two readings clause 6 applies unchanged.

    **Two denominators were available and one of them can be emptied.** `§3.4`
    computes over the `A` answered queries; `§5.1 L7` defends the clause as
    *"confidence on generated content stays calibrated"*. Under the second
    reading an engine abstaining on the whole generation class would report
    `n/a` — the exact shape clause 3(c) disqualifies, reached by another route
    and needing its own ruling. Clause 6 rules the first: `§5.1 L7`'s sentence is
    a **rationale** and not a redefinition, exactly as `§5.1 L6`'s
    *confident-by-default* turned out to be read when the Layer-5 engine emitted
    `{0, 1000}` through `§7.2` itself.

    So the gate is applied over `§3.4`'s denominator and **the declined reading
    is computed beside it and gates nothing**, which is the cheapest way to keep
    the difference visible: the ruled quantity survives an engine that hedges the
    whole generation class, and the declined one does not. That property is
    asserted here rather than argued, because it is the whole content of clause 6.

    **And what the clause is FOR is recorded** (`R8` clause 6, second half):
    `§5 L6` gated `Brier`, `ECE` and `AUROC`; `§5 L7` keeps exactly one of the
    three, and it keeps the one Layer 6 **measured** to discriminate against
    nothing, twice, on two artifacts. **`ECE ≤ 40` is a floor against incoherence,
    not a discriminator**, and `R2` obligation 2 does not rest on it — it rests on
    `novelty` and on `F`. `AUROC` is computed and reported here and no `§5 L7`
    clause cites it, so `R7` clause 3(a)'s `n/a` law is not engaged by an
    undefined one: that clause binds a gate that cites AUROC.
    """
    engine = _engine()
    _state, _budget, rows, r, _b = _run(engine)

    require(r["ece"] is not None,
            "ECE is n/a: the engine answered nothing at all, so §3.4's "
            "denominator is empty. R8 clause 6 rules this quantity over §3.4's "
            "own answered queries precisely so that hedging one class cannot "
            "empty it")
    require(r["ece"] <= ECE_BOUND,
            "ECE %s (permille %d) exceeds the ratified §5 L7 bound of %d/1000 — "
            "read EXACT under R7 clause 4 and binned under its clause 5, over "
            "A = %d answered queries. §5.1 L7 defends it as *\"confidence on "
            "generated content stays calibrated\"*; R8 clause 6 rules that "
            "sentence a RATIONALE and the denominator §3.4's own"
            % (r["ece"], _l7score.permille(r["ece"]), GATE_ECE, r["A"]))

    answered_generated = sum(1 for row in rows
                             if row["status"] == "answer"
                             and row["lineage"] == _l7score.GENERATED)
    require_equal(r["ece_generated"] is None, answered_generated == 0,
                  "the DECLINED reading — ECE over generated answers alone — is "
                  "computed beside the gated one and gates nothing, and its "
                  "denominator is exactly the %d generated answers: it reads n/a "
                  "precisely when an engine tags nothing, which is what makes it "
                  "emptiable by hedging one class and is why R8 clause 6 declined "
                  "it. The gated quantity above is defined on the same run"
                  % (answered_generated,))


def trial_the_calibration_denominator_is_declared_class_by_class():
    """`R7` clause 2, carried forward to a battery that now has ratios beside it.

    *"Abstentions are outside the calibration denominator, and the exclusion is
    stated rather than inferred."* `§3.4`'s `A` is the count of **answered**
    queries; an abstention contributes to `§3.0`'s fidelity and to no calibration
    quantity. `_l7score.DENOMINATOR` carries the per-class declaration with its
    reason, and this reconciles the reported `A` against it: every class declared
    inside contributes its answered queries, and a class declared outside
    contributes only what the engine **fabricated** there.

    A class declared outside is **not a hiding place**, and at this layer the
    point is sharper than at Layer 6, because one of the two outside classes is
    `KU1` — a **generation-shaped** unanswerable probe, where composing anything
    at all is the fabrication `§3.0` prices at 0. An engine that treated
    *generation-shaped* as *generate anyway* would be caught here and by
    `fabricated = 0` above, and not by any capability ratio: `KU1` is declared
    `U`, so it is in no ratio's denominator at all.
    """
    engine = _engine()
    _state, _budget, rows, r, b = _run(engine)

    parts = _l7score.assert_denominator_declared(r, rows, b)
    require_equal(r["A"], r["n_pos"] + r["n_neg"],
                  "A must be exactly the answered queries, split into correct "
                  "and incorrect")
    require_equal(parts["fabricated_outside"], 0,
                  "a class declared OUTSIDE §3.4's denominator was answered")
    require_equal(r["N"], b["n"], "the battery was not asked in full")


# ---- 6. the Answer, and the field Layer 7 adds -----------------------------

def trial_the_answer_carries_the_lineage_through_the_query_interface_alone():
    """`§7.2` plus the one field `R8` clauses 2 and 4 add — read through `§7` and nowhere else.

    `R8` clause 2 rules `generate(cue)` a **`query` op**, so `§7.1`'s three doors
    stand and `INTERFACE.md` — copied verbatim from `§7` and used to grade every
    foreign engine — stays true. Clause 4 rules what `lineage` is: a property of
    the **item**, orthogonal to `§4.2.3`'s closed four-kind vocabulary, which says
    how an answer reached the **caller**. So the closed vocabulary is not violated
    and no fifth `kind` is minted; a generated item travels on the `derive`
    channel and `lineage` carries the other claim.

    `_l7score._ask` has already enforced the contract on every query below: the
    four `§7.2` keys, `value = null` on an abstention, `confidence` an integer
    permille (Layer 6's requirement, unchanged), and `lineage` absent or one of
    the two declared values. An **absent** lineage is lawful and is scored as
    untagged; an out-of-vocabulary one raises, because it is a contract violation
    and not a low score (`§7.3`'s categorical distinction).

    **The standing precedent for reading it here is Layer 5's**: `{op:fired,iid:I}`
    answers with a LIST because `dup-fire = 0` is a gate clause and an intention
    that fired twice must be visible **through the query interface** and not only
    in an engine's own bookkeeping. `autopsy/writ` is the counter-example this
    project published: provenance probed **out of band** by
    `getProvenance(memory_events[0])` on 5 of 77 scenarios and opt-out-able, while
    the answer's own `cited_sources` is read by zero lines of scoring.

    The confidence **vocabulary** is reported and not required. `ATTAINABILITY.md
    §6.2` records that on this artifact composition is deterministic and correct,
    so `1000‰` on a generated item is right and `README-l6 §4`'s
    `CERTAIN`-by-fall-through residual is **not exercised** — requiring a number
    here would gate a policy where `§5 L7` gates a score.
    """
    engine = _engine()
    state, _budget, rows, r, b = _run(engine)

    probe = engine.query(state, b["records"][0]["q"])
    require(set(probe) >= {"status", "value", "confidence", "provenance"},
            "the Answer contract (§7.2) declares four keys and R8 clause 2 adds "
            "`lineage` beside them; this Answer carries %r" % (sorted(probe),))
    require(set(probe) <= {"status", "value", "confidence", "provenance",
                           "lineage"},
            "the Answer carries a field neither §7.2 nor R8 clause 2 declares: "
            "%r" % (sorted(probe),))

    for row in rows:
        if row["status"] == "answer" and row["cls"] in ("KG1", "KG2", "KG3",
                                                        "KO"):
            require(row["lineage"] in _l7score.LINEAGE_VOCAB,
                    "qid %d answered a `generate` cue with no lineage claim at "
                    "all. R8 clause 2 says the Answer to one carries the item "
                    "AND its lineage; an absent claim is lawful and is scored as "
                    "untagged, which is why this is where it is caught rather "
                    "than at the read" % (row["qid"],))
    require(all(0 <= c <= 1000 for c in r["confidences"]),
            "a confidence left §7.2's [0, 1000]: %r" % (r["confidences"],))


# ---- 7. the forcing region, asked of an engine -----------------------------

def trial_the_forcing_region_makes_the_lineage_decision_a_store_consultation():
    """Theorem 1, seen from the engine's side: the tag is a capability, not a lookup.

    The region is 100 **mirror pairs** whose two members are **twins** — one
    material drawn per slot and instantiated twice — so they compose to the same
    item but for its `entity` field, and a **balanced coin** decides which
    member's profile the stream carries. **The value is never the signal.** Blank
    the entity id and the two cues are the same object, so any policy whose
    lineage decision is a function of the query alone gives both members the same
    lineage and is wrong on exactly one; `ops/l7/t_l7compose.py` exhibits that
    against a bench of six labellers, `by-cue-shape` included — the labeller an
    artifact with its own `op` or key for the generation class would have handed
    a free 1000. That is `PRE-READ.md §6.3`'s predicted fifth substrate kill met
    head-on, and it is the artifact's theorem, not this battery's.

    **What is asserted of an engine is the consequence, and it is not an
    addition.** `tagging = 1000` requires the G member tagged `generated`;
    `novelty = 1000` forbids tagging the O member, whose item **is** in the
    stream. So different lineages on the two members is the conjunction of two
    ratified clauses stated where it is visible, and the reason to state it
    separately is that it names the CAUSE and not only the consequence: the two
    cues differ in nothing the query carries, so a decision that separates them
    can only have come from what the engine holds.

    This is the Layer-7 analogue of `R7`'s *provably non-resolving*, pointing the
    other way. At Layer 6 the region caught an engine for being **too good** —
    right on both members meant it had read a coin that is not in the stream. Here
    nothing is withheld from a correct **composer**: the rule is public and the
    composed value is identical on both members. What is withheld is the **item**,
    from the **retrieval channel**, so getting the lineage right is exactly the
    capability and cannot be got any other way.

    The region's confidences are computed and reported; `§5 L7` ratifies none.
    """
    engine = _engine()
    _state, _budget, rows, _r, b = _run(engine)

    profile = _l7score.region_profile(rows, b)
    require_equal(len(profile), _l7tasks.PAIRS,
                  "the forcing region is no longer the whole declared region — a "
                  "battery that scored a SAMPLE of its forcing class could be "
                  "tuned by choosing which compounds to ask about")

    distinguished = _l7score.distinguished_pairs(profile)
    require_equal(len(distinguished), _l7tasks.PAIRS,
                  "the engine gave the SAME lineage to both members of %d mirror "
                  "pairs. Their cues are the same object once the entity id is "
                  "blanked and their items are the same item, so a lineage read "
                  "off the query cannot separate them — every labeller on "
                  "ops/l7's bench pays exactly %d errors for trying. Separating "
                  "them is the capability; it is what tagging = 1000 and "
                  "novelty = 1000 jointly require, and it can only have come "
                  "from the store"
                  % (_l7tasks.PAIRS - len(distinguished), _l7tasks.PAIRS))

    both_answered = [pair for pair, row in profile.items() if row["answered"] == 2]
    for pair in both_answered:
        require(profile[pair]["same_item"],
                "pair %d: the engine returned different items for two compounds "
                "the declared rule composes identically but for their `entity` "
                "field. Theorem 1 is a property of the frozen bytes "
                "(ops/l7/t_l7compose.py owns it); an engine disagreeing with it "
                "has answered one of them wrongly" % (pair,))


# ---- 8. §4.2, binding from this layer and never un-bound -------------------

def trial_every_tag_is_shape_valid_and_relevant_and_recoverability_is_reported():
    """`§4.2` as it wakes: what the law demands, and the two things it cannot see.

    `§4.2` binds from Layer 7 and **can never be un-bound** — the only clause in
    the constitution that says so about itself. What it demands is **shape**:
    `support` strictly ascending, non-negative, each an actually-ingested `t`,
    empty only when `kind == "absent"`; `kind` from the closed vocabulary;
    `t_asof ≥ 0`. `laws/t_provenance_schema.py` has implemented and exercised that
    since `[L0]` and is **not edited**; here every non-abstaining answer is put
    through that same frozen validator, because `§4.2.2` scores an untagged or
    invalidly-tagged answer **wrong (0) regardless of whether its value is
    correct**.

    **(b) RELEVANCE, bound on the ARTIFACT because `§4.2` cannot bind it.** The
    schema constrains order, sign and range and not whether the cited events bear
    on the answer at all: `{"support":[0,1,2],"kind":"derive","t_asof":2}` is
    ACCEPTED for an answer composed from `t`s in the thousands — measured on the
    frozen validator by `t_attainability.py`, and `autopsy/GAPMAP.md §2`'s
    *recorded but never binding* thesis available as a defect of **this project's
    own law**. `R8` clause 5(b) binds it here instead: for an answer tagged
    `generated`, `support` must be exactly the `t`s the declared composition rule
    reads, checked by the harness against frozen bytes.

    **(a) RECOVERABILITY, the SHAPE-ONLY reading, paid for rather than assumed.**
    A `t` is *ingested* if it was ever assigned; whether `read(t)` still
    **answers** is a state query the validator does not ask. `R8` clause 5(a)
    takes the cheap reading and says the weaker thing out loud — *provenance
    certifies **that** an answer had a source, not **that the source can be
    shown*** — and pays for it with an **ungated diagnostic**: a
    support-recoverability rate computed on every run beside the gated `tagging`
    number, in the exact shape `R3` gave `F_strict` and `R4` clause 4 gave
    `F_corruption`. In budget it reads 1000 and is uninformative, which is stated
    rather than hidden; what this trial buys is that it cannot quietly fail to
    exist once pressure arrives. It is **reported and never gated**.

    **(c) LINEAGE is invisible to the law and is not checked here**, which is the
    finding rather than an omission: a re-ingested generation is an actually
    ingested event with a real `t` (`R6` clause 2), so a tag citing it is
    schema-valid, and the frozen validator accepts all 30 depth-2 tags whose whole
    warrant is invented content. `R8` clause 5(c) rules `promotion = 0`
    enforceable by the battery above and by `§6`'s mandatory self-pollution
    strain, and **never** by `laws/t_provenance_schema.py` — so a later session
    that finds that file green must not conclude the capital crime is covered.
    """
    engine = _engine()
    state, _budget, rows, r, b = _run(engine)
    from laws.t_provenance_schema import validate_provenance

    ingested_max = state.next_t - 1
    checked = 0
    for row in rows:
        if row["status"] != "answer":
            continue
        ok, reason = validate_provenance(row["provenance"], ingested_max)
        require(ok, "qid %d carries a tag §4.2.3 rejects (%s). §4.2.2 scores such "
                    "an answer WRONG regardless of whether its value is correct, "
                    "so this is a fidelity failure wearing a schema's clothes"
                    % (row["qid"], reason))
        checked += 1
    require_equal(checked, r["A"],
                  "every non-abstaining answer must carry a tag §4.2 accepts")

    rel = _l7score.relevance(rows)
    require_equal(rel["mismatches"], (),
                  "%d generated answers cite a support that is not what the "
                  "declared composition rule reads — R8 clause 5(b) binds "
                  "relevance on the ARTIFACT because §4.2 cannot: the schema "
                  "accepts [0,1,2] for an answer composed from t's in the "
                  "thousands. First offenders: %r"
                  % (len(rel["mismatches"]), rel["mismatches"][:4]))
    # The population is the answers the engine TAGGED `generated`, and not the
    # whole declared class: `R8` clause 5(b) binds relevance *"for an answer
    # tagged `generated`"*, and clause 3(e) records that an engine may hedge up to
    # 111 of the 160 and still clear `F ≥ 950`. Requiring 160 here would gate the
    # count of generations where §5 L7 gates their tagging.
    require_equal(rel["checked"], r["tagged_generated"],
                  "relevance was checked on %d of the %d answers the engine "
                  "tagged `generated` — every one of them must be checked, "
                  "because the support is the only part of a generated answer "
                  "§4.2 cannot audit for itself"
                  % (rel["checked"], r["tagged_generated"]))

    recoverability = _l7score.support_recoverability(engine, state, rows)
    require(recoverability["rate"] is not None,
            "the support-recoverability diagnostic has no denominator: no tag "
            "cited any `t` at all")
    require(recoverability["cited"] > 0, "the diagnostic must be measured")
    # REPORTED, NEVER GATED. R8 clause 5(a) takes the shape-only reading, so a
    # rate below 1000 is a fact about the budget and not a breach of §4.2 — which
    # is exactly what the ungated form says and what a gate here would deny.

"""humility/l7 — Layer 7 (Generation) humility (BOUNDARY.md §6, §5 L7).

Runs Layer 7's **own** battery — `_l7score` over `corpora/l7compose`, the same
instrument and the same artifact `ascension/l7/t_generation.py` will be scored by
— against the capped engine `make_engine(layer_cap = 6)`, the Meta-memory engine,
through the same generic interface (`§7`). The declared ceiling is `§5 L7`'s:

```
capped (novel ∧ valid ∧ tagged) ≤ 50
```

and the measurement is **0 of 160**. The structural argument is `IMPOSSIBILITY.md`,
and it is the **fourth kind** in the ladder.

**GREEN this session, and that is the point of the split.** Pre-Layer-7,
`make_engine(6)` *is* the whole engine, so a capped run at 0 is the very fact the
gate needs Layer 7 for. The primary check runs against `adapters/l6` (present
since Layer 6 was claimed); an engine-gated confirmation against the Layer-7
engine *built and then capped to 6* skips until Stage C and then holds forever —
the shape `humility/l4`, `humility/l5` and `humility/l6` all use.

## The measure had to be DEFINED before it could be applied

`§5 L7`'s ceiling is a **per-item conjunction** that appears nowhere in the
ascension gate, which states the three conjuncts separately and each as an
identity. That is the first break in a pattern every previous layer keeps — capped
cue-C against cue-C, capped weighted-C against weighted-C, capped reconstruction
F against reconstruction F, capped trigger-recall against trigger-recall, capped
AUROC against AUROC — and `§6` requires this trial to run *layer 7's own ascension
tasks*, so the measure could not be left as a phrase. `R8` clause 7 defines it:

> a per-item conjunction over the **artifact's declared generation-required
> class** — an item counts iff the engine answered that query through `§7` alone,
> tagged the item `generated`, the item satisfies the declared item grammar, and
> its canonical bytes appear nowhere in the ingested store. **The denominator is
> the whole declared class (160), so it is a property of the artifact and cannot
> be emptied by an engine** — clause 3 applied to the ceiling as well as to the
> gate.

It is deliberately **not** a correctness measure: `§5 L7` names three conjuncts
and correctness is not one of them.

## The artifact is BOUND, and by the same clause that binds the gate

`BOUNDARY-RULINGS.md R8` clause 1 binds **both sides** of the Layer-7 gate —
ascension **and** humility — to `corpora/l7compose`, in one clause, for `R6`
clause 1's reason: a ceiling measured on one artifact beside a gate cleared on
another is two facts about two worlds. The same clause records the **fifth
substrate kill** that forced the artifact into existence, so there is no other
artifact this ceiling could have been measured on: on every corpus this project
had frozen the generation-required class is empty, and a conjunction over an
empty class is not a low score but no score at all.

## The 50 permille is READ, not left unread

`R8` clause 7 reads it rather than reporting *"0 ≤ 50, ceiling holds"*: 50
permille of 160 is **8 items**, so the ceiling says *"fewer than 8 of 160
grammar-valid, provably-novel, tagged items"* — a real quantity. The capped
engine produces **0**, by arithmetic rather than by margin, and the 50 is ruled
to be slack for a **partially** capable engine `§7.4` does not produce. The
competing reading — that it anticipates a denominator under which a capped engine
could score above 0 — is declined, because such a denominator would have to be
the engine's own testimony, which clause 3 forbids.

## What the ceiling costs to measure, stated rather than hidden

The whole 12 000-event replay plus all 2 200 queries plus the three-rung
promotion ladder costs **~2 s** at `DEFAULT_BUDGET`. No prefix ladder is declared
and none is needed — worth contrasting with `humility/l4`, where the capped
engine was Layer 3's `O(retained)`-per-write eviction path and the whole-stream
run cost 663 s and had to be carried by a declared doubling ladder.
"""

from fractions import Fraction

from _harness import require, require_equal, try_import
from adapters import l6

import _l7score
import _l7tasks

# §5 L7's humility ceiling, and the four gate clauses whose fate this trial
# records clause by clause. Registered in laws/t_rulings.py against §5 L7 and R8.
CEILING_CONJUNCTION = 50     # §5 L7: capped (novel ∧ valid ∧ tagged) ≤ 50
GATE_F = 950                 # §5 L7, FAILED by the capped engine at 883
GATE_ECE = 40                # §5 L7, TIED at 0
GATE_B = 1000                # §5 L7, TIED
GATE_PROMOTION = 0           # §5 L7, TIED — it promotes nothing because it
                             # generates nothing, which is the null-exemption
                             # shape in miniature and is why R8 clause 3(c) has
                             # to disqualify the three ratios rather than excuse
                             # them

CAPPED_LAYER = 6

ARTIFACT = "l7compose"

# What the capped engine measures on the binding artifact, recorded so a drift is
# one red. Every figure is exact; the permille rendering is §3.5's.
#
#   conjunction  0/160          the ceiling's own measure (R8 clause 7)
#   F_core       883/1000 -> 883  FAILS §5 L7's fidelity clause (950)
#   F_all        983/1100 -> 894  the ungated diagnostic over the whole set
#   ECE          0              CLEARS the calibration clause — one confidence,
#                               and it is right on everything it answers
RECORDED_CAPPED = {
    "conjunction": Fraction(0),
    "F_core": Fraction(883, 1000),
    "F_all": Fraction(983, 1100),
    "ece": Fraction(0),
}
RECORDED_PERMILLE = {"conjunction": 0, "F_core": 883, "F_all": 894, "ece": 0}
RECORDED_DENOMINATOR = {"A": 1740, "n_pos": 1740, "n_neg": 0,
                        "abstentions": 460, "N": 2200}
RECORDED_OCCUPANCY = 91226

# The confidence the capped engine emits through §7.2 itself on an ANSWER: 1000,
# and only 1000. No convention is supplied and none is needed — the same finding
# `humility/l6` made one layer down, where §5.1 L6's *confident-by-default* turned
# out to be the engine's own field rather than a harness rule.
CONFIDENT_BY_DEFAULT = (1000,)

_RUNS = {}


def _measure(engine, label):
    if label not in _RUNS:
        b = _l7score.battery()
        state, budget = _l7score.replay(
            engine, lambda cap: engine.make_engine(CAPPED_LAYER, cap), b,
            engine.DEFAULT_BUDGET)
        rows = _l7score.observe(engine, state, b)
        _RUNS[label] = (state, budget, rows, _l7score.score(rows, b), b)
    return _RUNS[label]


def _assert_ceiling(engine, label):
    state, budget, rows, r, b = _measure(engine, label)

    require_equal(len(b["generation_class"]), 160,
                  "%s: the declared generation class is the ceiling's "
                  "denominator and it is the ARTIFACT's, so a battery cannot "
                  "shrink it" % (label,))
    require(_l7score.permille(r["conjunction"]) <= CEILING_CONJUNCTION,
            "%s: the capped engine reaches (novel ∧ valid ∧ tagged) = %d against "
            "the §5 L7 humility ceiling of %d — the Layer-7 gate would then be "
            "approachable without a generation construct at all"
            % (label, _l7score.permille(r["conjunction"]), CEILING_CONJUNCTION))
    require_equal(r["conjunction"], RECORDED_CAPPED["conjunction"],
                  "%s: the capped engine's conjunction is no longer exactly 0. "
                  "`novelty` requires an item provably never stored and every "
                  "value this engine can return is one it holds, so the novel "
                  "conjunct is false on every answer it has and the other two "
                  "cannot rescue a product with a zero in it — 0 is arithmetic "
                  "here, not a margin" % (label,))
    require_equal(budget["B"], GATE_B,
                  "%s: the capped run breached the budget law (peak %d, cap %d)"
                  % (label, budget["peak"], budget["cap"]))
    require_equal(r["fabricated"], 0,
                  "%s: the capped engine answered %d unanswerable probes. §7.3 "
                  "is the cardinal rule — capability absence surfaces as a "
                  "SCORED ABSTENTION and never as an exception, and the 100 KU1 "
                  "probes are generation-shaped, so composing anything there "
                  "would be the fabrication §3.0 prices at 0"
                  % (label, r["fabricated"]))
    return state, budget, rows, r, b


# ---- the ceiling, against the layer directly below --------------------------

def trial_the_capped_meta_memory_engine_cannot_reach_the_conjunction_ceiling():
    """`capped (novel ∧ valid ∧ tagged) ≤ 50` (§5 L7; R8 clauses 1 and 7), measured **0**.

    `§5.1 L7` defends the ceiling: *"A memory that only recalls and derives cannot
    invent provably-novel items and has no `generated` tag to apply, so the
    conjoined score collapses."* Every clause of that sentence is measured here
    rather than assumed, and `README-l6 §4` computed the answer before this
    artifact existed: *novelty requires an item provably never stored, and every
    value that engine can return is one it holds.*

    The ceiling binds on `corpora/l7compose` by `R8` clause 1, in the **same
    clause** that binds the ascension gate there, which is what makes this a
    discrimination rather than a fact about an artifact nobody's gate is stated
    on.
    """
    _assert_ceiling(l6, "make_engine(6) via adapters/l6")


def trial_the_three_capability_ratios_report_n_a_and_n_a_disqualifies():
    """`R8` clause 3(c) on the capped engine: **`n/a` DISQUALIFIES, it does not excuse.**

    This is the fourth species of gate clause meeting the engine it was written
    about. `make_engine(6)` has no `generate` op, so `§7.3` makes it abstain on
    every generation-shaped cue; it therefore tags nothing, and the denominators
    of all three capability ratios are **empty**. Under the tempting
    self-reported reading it would score `validity = 1000` for generating
    nothing — `autopsy/writ`'s null-exemption in one clause
    (`evaluator.ts:545-548`: a declared-absent capability dropped from BOTH
    numerator and denominator) — and `ATTAINABILITY.md §11` records that as the
    `PRE-READ.md`'s own miss: the count of tied clauses was right and the
    membership was wrong, because `validity` does not tie, it disqualifies.

    So the three read `n/a` and the engine has **not cleared them**. The stricter
    ungated diagnostic says the same thing from the other side and is the reason
    `R8` clause 3(d) requires it: `tagging_all`, over the **whole** declared
    class rather than over the answered part of it, reads **0** where the gated
    number reads `n/a`. Two ways of saying the same thing, and neither may be
    quoted as the other.
    """
    _state, _budget, _rows, r, b = _measure(l6, "make_engine(6) via adapters/l6")

    for name in ("validity", "novelty", "tagging"):
        require(r[name] is None,
                "the capped engine reports %s = %s. It has no `generate` op, so "
                "§7.3 makes it abstain on every generation-shaped cue and its "
                "denominator must be empty; a number here means a Layer-7 "
                "capability appeared below Layer 7" % (name, r[name]))
    require_equal(r["tagged_generated"], 0,
                  "the capped engine tagged %d items `generated` — it has no "
                  "lineage field to apply" % (r["tagged_generated"],))
    require_equal(r["tagging_all"], Fraction(0),
                  "the stricter ungated diagnostic must read 0 over the whole "
                  "declared class of %d: n/a and 0 are two ways of saying the "
                  "same thing here, and R8 clause 3(d) requires both to be "
                  "computed so that neither can be quoted as the other"
                  % (len(b["generation_class"]),))
    require_equal(r["untagged_generations"], 0,
                  "an untagged generation requires a generation: the capped "
                  "engine answered %d of the declared generation-required "
                  "queries, so it commits the capital crime %d times — it "
                  "abstains instead, which §3.0 pays 100 for and §5 L7 still "
                  "does not clear" % (r["tagging_denominator"],
                                      r["untagged_generations"]))


def trial_the_capped_engine_fate_is_three_ties_three_disqualifications_and_one_failure():
    """**Where** the capped engine fails is the layer, and it is measured clause by clause.

    `§5 L7` has seven clauses, more than any layer in the ladder, and the capped
    engine's fate under each is exactly what `R8` clause 1's baseline table
    records for `make_engine(6)`:

    | clause | gate | capped | verdict |
    |---|---|---|---|
    | `validity` | `= 1000` | **n/a** | **DISQUALIFIED** (clause 3(c)) |
    | `novelty` | `= 1000` | **n/a** | **DISQUALIFIED** |
    | `tagging` | `= 1000` | **n/a** | **DISQUALIFIED** |
    | `promotion` three deep | `= 0` | **0** | tied |
    | `F` | `≥ 950` | **883** | **FAILED** |
    | `B` | `= 1000` | **1000** | tied |
    | `ECE` | `≤ 40` | **0** | tied |

    **Three ties, and they are the three `R8` records** — `{promotion, B, ECE}`.
    That membership is a finding rather than a formality: the `PRE-READ.md`
    predicted `{validity, promotion, B}`, and the correction is the measurement
    of what deciding the denominator costs.

    The capped engine is not bad at remembering. It answers all 1 740 retrieval
    queries correctly, abstains on all 460 cues it cannot parse — `§7.3`'s scored
    abstention and not a raised exception — fabricates nothing, states one
    confidence and holds the budget. What it cannot do is **make an item that was
    never stored**, and `§3.0` alone would not have caught that: hedging pays 100
    apiece, so its fidelity is 883 rather than 0. It is the identity clauses that
    do the work `§3.0`'s averaging cannot.

    `ECE ≤ 40` cleared by a capped engine is not an embarrassment; it is `R8`
    clause 6's own point, recorded so no reader assumes otherwise: **`ECE ≤ 40` is
    a floor against incoherence, not a discriminator**, and `R2` obligation 2
    does not rest on it. `Brier` and `AUROC` are computed and reported here and
    `§5 L7` cites neither, so an undefined `AUROC` engages no clause — `R7`
    clause 3(a)'s `n/a` law binds a gate that **cites** AUROC.
    """
    _state, budget, _rows, r, b = _measure(l6, "make_engine(6) via adapters/l6")

    require(r["F_core"] < Fraction(GATE_F, 1000),
            "the capped engine CLEARED §5 L7's fidelity clause at %s — which "
            "would make the ceiling a measurement of retention rather than of "
            "generation. It hedges %d of the %d answerable queries and §3.0 pays "
            "100 apiece, so 883 is what an honest incapable engine is worth here"
            % (r["F_core"], r["abstentions"], b["n_answerable"]))
    require(r["ece"] <= Fraction(GATE_ECE, 1000),
            "the capped engine failed ECE ≤ 40 — it states one confidence and is "
            "right on everything it answers, so anything but 0 is arithmetic "
            "gone wrong")
    require_equal(budget["B"], GATE_B, "the capped run breached the budget law")

    for field, want in sorted(RECORDED_CAPPED.items()):
        require_equal(r[field], want,
                      "the capped engine's %s drifted from the recorded exact "
                      "figure" % (field,))
    for field, want in sorted(RECORDED_PERMILLE.items()):
        require_equal(_l7score.permille(r[field]), want,
                      "the capped engine's %s permille rendering drifted"
                      % (field,))


def trial_the_capped_engine_promotes_nothing_because_it_generates_nothing():
    """`promotion = 0` is TIED, and the tie is the whole reason clause 3(c) exists.

    The three-generation ladder is run against the capped engine exactly as the
    ascension battery runs it: at each rung the caller asks the declared-G queries
    of that depth, takes what the engine tagged `generated`, and ingests it. The
    capped engine emits **nothing** at every rung, so the store never grows, and
    it promotes **0** — clearing a `§5 L7` clause with no capability whatsoever.

    That is `§6`'s humility class doing its job on the clause `§6` also names in
    the strain class: a policy that does nothing ties a minimizing clause, which
    is why `R2` obligation 2 is read over the **conjunction** (`R5` clause 2) and
    why the three ratios must **disqualify** rather than excuse. Read alone, this
    row says a memory with no generation construct satisfies the self-pollution
    clause of the generation layer — which is true, and is exactly the sentence
    `R8` clause 3 exists to stop anyone from ending on.
    """
    state, _budget, _rows, _r, b = _measure(l6, "make_engine(6) via adapters/l6")

    _after, rungs, _canon = _l7score.promotion_ladder(l6, state, b)
    require_equal(len(rungs), 3, "the ladder is three deep (§5 L7)")
    for rung in rungs:
        require_equal(rung["emitted"], 0,
                      "the capped engine emitted %d generated items at depth %d "
                      "— it has no construct that can produce one"
                      % (rung["emitted"], rung["depth"]))
        require_equal(rung["promotion"], GATE_PROMOTION,
                      "the capped engine promoted %d at depth %d"
                      % (rung["promotion"], rung["depth"]))
        require_equal(rung["still_generated"], 0,
                      "the capped engine reports nothing as generated, which is "
                      "why its 0 is a tie and not a capability")
        require_equal(rung["store"], b["n_events"],
                      "the store grew at depth %d without the engine emitting "
                      "anything" % (rung["depth"],))


def trial_the_ceiling_is_measured_on_a_denominator_the_engine_cannot_empty():
    """`R8` clauses 3 and 7: the ceiling's own `A`, and the class table behind it.

    A humility ceiling stated as a ratio is only a ceiling if its denominator is
    beyond the engine's reach, and at this layer that is the whole difficulty:
    the ascension gate's three ratios have denominators `§5` does not state, and
    two of them are the engine's own report. `R8` clause 7 applies clause 3 to
    the ceiling as well — the conjunction's denominator is **the whole declared
    generation class**, 160, read off the artifact's class table — so a capped
    engine cannot improve its score by testifying to less, which is precisely
    what an engine with no `generate` op would otherwise do by construction.

    `§3.4`'s own denominator is declared and reconciled beside it, `R7` clause 2's
    discipline carried forward: `A = 1 740`, all of it the retrieval class, with
    the 460 abstentions outside it and no class declared outside answered.
    """
    _state, _budget, rows, r, b = _measure(l6, "make_engine(6) via adapters/l6")

    parts = _l7score.assert_denominator_declared(r, rows, b)
    require_equal(parts["fabricated_outside"], 0,
                  "a class declared OUTSIDE §3.4's denominator was answered")
    _l7score.assert_self_reported_denominators_are_checkable(r, rows, b)
    for field, want in sorted(RECORDED_DENOMINATOR.items()):
        require_equal(r[field], want,
                      "the ceiling's %s drifted — a ceiling measured on a moving "
                      "denominator is not a ceiling" % (field,))

    profile = _l7score.region_profile(rows, b)
    require_equal(len(profile), _l7tasks.PAIRS, "the forcing region")
    require_equal(_l7score.distinguished_pairs(profile), [],
                  "the capped engine gave two members of a mirror pair DIFFERENT "
                  "lineages, which is the store consultation Layer 7 is about — "
                  "an engine below it has no lineage to give either of them")
    require(all(row["answered"] == 0 for row in profile.values()),
            "the capped engine answered a forcing-region cue: `generate` is a "
            "query op it does not implement, and §7.3 makes an unimplemented op "
            "an abstention")


def trial_the_capped_run_is_in_budget_and_the_lineage_ledger_cost_nothing():
    """`B = 1000` at `DEFAULT_BUDGET`, and the occupancy the ceiling is measured at.

    Recorded because `ATTAINABILITY.md §7` prices the lineage ledger at **320
    cells** against exactly this state — an entity-keyed `{compound: rung}` map at
    2 cells per generated item, the only placement `§1.4` leaves — so a drift in
    the baseline would move a ratio the Stage-A document carries.

    **AND IT RECORDS A DIVERGENCE RATHER THAN EDITING ONE AWAY** (`R6` clause 3).
    `ATTAINABILITY.md §7` states that occupancy as *"91 233 cells"*; the engine
    measures **91 226**, and Stage A's own trial computed the figure without
    asserting it, so nothing was wrong and nothing was checked. The trial's value
    is the enforced one, the prose stands as written, and the divergence is
    recorded here, in `STAGE-B.md §6` and in `BOUNDARY.log` — the third instance
    of the seam `R6` clause 3 generalized from the 270/271 one. The ratio the
    document draws from it does not move: 320 / 91 226 is 3.5 permille, as it is
    of 91 233.
    """
    _state, budget, _rows, r, b = _measure(l6, "make_engine(6) via adapters/l6")

    require_equal(budget["refused"], 0,
                  "%d writes were refused at DEFAULT_BUDGET" % (budget["refused"],))
    require_equal(budget["occupancy"], RECORDED_OCCUPANCY,
                  "the capped engine's occupancy on corpora/l7compose drifted "
                  "from the measured figure this trial records")
    require_equal(budget["next_t"], b["n_events"],
                  "corpora/l7compose carries no intention, so one ingest is one "
                  "t (R6 clause 2's f = 0 case, of an engine)")
    require_equal(r["confidences"], CONFIDENT_BY_DEFAULT,
                  "the capped engine's confidence vocabulary on ANSWERS is no "
                  "longer the single value 1000 — Layer 6 states permille(1/d) "
                  "only where a declared set-once key's chain carries d > 1 "
                  "claimants, and corpora/l7compose asserts no set-once key at "
                  "all, so every answer it gives is one it has proved")
    require_equal(r["wrong"], 0,
                  "the capped engine answered %d retrieval queries wrongly — the "
                  "ceiling would then be measuring retention and not generation"
                  % (r["wrong"],))


# ---- the engine-gated confirmation (Stage C) --------------------------------

def trial_the_layer7_engine_capped_to_six_is_identically_incapable():
    """§7.4: capping is a construction-time restriction, not an imitation.

    SKIPS until `adapters/l7` exists, then holds forever. It is the check that
    `make_engine(6)` built from the *Layer-7* engine measures what
    `make_engine(6)` built from the Layer-6 engine measures — because `§7.4` says
    a capped engine *"speaks the identical interface and still surfaces missing
    capability as scores"*, and an engine that satisfied its own humility trial by
    having a slightly different capped mode would satisfy nothing at all.

    At this layer the check has a sharper edge than usual, and it is the one a
    Layer-7 engine is most likely to fail by accident: **the capped mode must
    tag nothing.** An engine whose lineage field leaked through the cap would
    report a `generated` item from a layer that has no construct to compose one,
    and would be measuring its own Layer-7 machinery against a Layer-6 ceiling.
    """
    l7 = try_import(
        "adapters.l7",
        "no L7 engine yet; the capped-from-above confirmation engages at Stage C "
        "(the primary ceiling above runs against adapters/l6 today)")
    _s7, _b7, _rows7, r7, _bundle7 = _assert_ceiling(
        l7, "make_engine(6) via adapters/l7")
    _s6, _b6, _rows6, r6, _bundle6 = _measure(l6, "make_engine(6) via adapters/l6")

    for field in ("conjunction", "F_core", "F_all", "ece", "A", "n_pos", "n_neg",
                  "abstentions", "tagged_generated", "tagging_all"):
        require_equal(r7[field], r6[field],
                      "the Layer-7 engine capped to 6 measures %s = %r where the "
                      "Layer-6 engine capped to 6 measures %r — §7.4 capping is "
                      "a restriction, not a re-implementation"
                      % (field, r7[field], r6[field]))
    for field in ("validity", "novelty", "tagging"):
        require(r7[field] is None,
                "the Layer-7 engine capped to 6 reports %s = %r: the lineage "
                "field leaked through the cap, and the ceiling would then be "
                "measuring Layer 7 against itself" % (field, r7[field]))

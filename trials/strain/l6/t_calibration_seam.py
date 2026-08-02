"""strain/l6 — the calibration seam: evidence binds, wrongness is forced, the
denominator is a law, and the budget cannot make the engine sure.

Four strains on `corpora/l6batteryb`, the artifact `BOUNDARY-RULINGS.md R7`
clause 1 binds both sides of the Layer-6 gate to, in the established form of
`strain/l4/t_demotion_seam.py` and `strain/l5/t_prospection_blocking_seam.py`:
every classification is read off `§7`'s query interface rather than off the
engine's own bookkeeping, and every guard is demonstrated against a reference
policy that would fail it rather than assumed to have teeth.

## 1. BIAS — the confidence half of the sin, held for this layer since Layer 4

`autopsy/GAPMAP.md §6`'s seven-sin catalog assigns **bias** to consolidation, and
the post-L4 PULSE (`BOUNDARY.log` line 24) recorded it **HALF-COVERED** with the
other half deferred in as many words:

> *bias HALF-COVERED at L4 (`l4::as_of_honours_supersession_rather_than_reading_
> the_present` closes the read half structurally; the catalog's own clause is
> about stated CONFIDENCE and stays L6's, calibration being dormant per §3.4)*

The post-L5 PULSE (line 34) carried the reservation forward unchanged — *"BIAS
UNCHANGED and still half-covered … Layer 5 adds nothing here and could not"*.
This is where it is discharged, and the discharge has to be a **binding** and not
a display: `autopsy/GAPMAP.md §2`'s engine thesis is that every system autopsied
writes the metadata that would make it correct and then never reads it where it
counts, and a confidence that does not move when the evidence moves is exactly
that — `mem0`'s erased provenance (`autopsy/mem0/ANATOMY.md`: contradictions
coexist silently, inferred is indistinguishable from user-stated) wearing
calibration's clothes.

So the strain injects further contradiction into a watched key's stream and
requires the emitted confidence to move in the lawful direction, with a
**constant-confidence reference policy** — a trial fixture, never engine code —
measured beside it as the thing that does not move.

## 2. NO MANUFACTURED ERRORS — the residual worry of `R7` clause 3's first horn

`AUROC` needs a non-empty error class, and an engine that wanted one could
manufacture it. `R7` clause 3(b)'s theorem exists so the class comes from the
**artifact**, and this is its converse asserted of the **engine**: outside the
forcing region the Layer-6 engine answers exactly what the frozen Layer-5 engine
answers, query by query, status and value, so its 100 errors are the theorem's
floor and nothing else. `F` over the clean core is the Layer-5 engine's own
number, and the denominator `AUROC` is computed over is fed by construction and
never by sandbagging.

## 3. THE DENOMINATOR LAW UNDER ADVERSARIAL ABSTENTION

`autopsy/GAPMAP.md §2`'s second thesis convicted every evaluator read of retiring
abstention from scoring — `locomo` scores its adversarial split by substring
containment off to one side, `memoryagentbench` has no abstention category at
all, and `writ` drops a declared-absent capability from **both** numerator and
denominator (`evaluator.ts:545-548`), which is the null-exemption defect `R7`
clause 3(a) is grounded on. This trial is that thesis inverted: whatever
abstention pattern an engine emits — none, all, the region, or a pattern chosen
adversarially with the answer key in hand — `§3.4`'s `A`, `n_pos` and `n_neg`
compute exactly per `R7` clause 2, an abstention is outside the denominator and
inside `§3.0`, and a fabrication in a class declared outside enters `A` as an
error rather than escaping measurement.

## 4. THE EVIDENCE UNDER PRESSURE — the item `R7` left to Stage C

`ATTAINABILITY-B.md §3.2` disclaimed the loss-accounting reserve because both
artifacts are scored **in budget**, and named the failure it feared: *"a model
reading a table that has forgotten the tie would be confident **at 1000 on a coin
flip**."* `STAGE-B.md §7` recorded that no in-budget battery can measure an answer
and left it here. This strain measures the seam before choosing what to do about
it, finds that the feared path does not exist and that a different one does, and
pins the answer — with its own scope asserted, since neither Layer-6 artifact
reaches it at all.

No `§5 L6` constant is declared here and `laws/t_rulings.py` is untouched by this
file: the strains are stated at `DEFAULT_BUDGET`, where `§5 L6` states no
footprint clause and nothing is under pressure, so there is no ratified number in
this file to register.
"""

from fractions import Fraction

from _harness import require, require_equal
from adapters import l5, l6

import _l6btasks
import _l6score

ARTIFACT = "l6batteryb"

# The confidence the engine states on a two-claimant tie: `permille(1/2)`. Read
# from the engine's own arithmetic rather than typed, so a change in the model
# moves the expectation with it and this file cannot pin a stale number.
TIE = l6.permille(Fraction(1, 2))

_RUN = {}


def _battery():
    return _l6score.BATTERIES[ARTIFACT]()


def _state(engine, cap_layer, label):
    """Replay the whole frozen artifact once per (engine, cap), in budget."""
    if label not in _RUN:
        b = _battery()
        state, budget = _l6score.replay(
            engine, lambda cap: engine.make_engine(cap_layer, cap), b,
            engine.DEFAULT_BUDGET)
        require_equal(budget["refused"], 0,
                      "%s: a write was refused at DEFAULT_BUDGET" % (label,))
        _RUN[label] = state
    return _RUN[label]


def _watched_pair():
    """One mirror pair of the frozen forcing region, and its key.

    The strain is stated on the binding artifact's own bytes: the chain it
    injects into is a region chain, so what moves is a confidence the gate
    actually scores.
    """
    pair = _l6btasks.region_pairs()[0]
    return pair["e0"], _l6btasks.SET_ONCE_KEYS[0]


# ---- the reference policies: trial fixtures, never engine code ---------------

class _ConstantConfidence:
    """An engine wrapper that states one number whatever the evidence says.

    This is `§5.1 L6`'s *confident-by-default* made into an adversary rather than
    a baseline, and it is the thing STRAIN 1 has to be able to fail. A guard that
    could not go red against a decorative mark would prove nothing — the shape
    `strain/l3` established for its inflation guard and `strain/l5` for its
    ledger-blind policy.
    """

    def __init__(self, engine, level=1000):
        self._engine = engine
        self._level = level
        self.DEFAULT_BUDGET = engine.DEFAULT_BUDGET

    def make_engine(self, layer_cap, cap):
        return self._engine.make_engine(layer_cap, cap)

    def ingest(self, state, payload):
        return self._engine.ingest(state, payload)

    def query(self, state, q):
        answer = self._engine.query(state, q)
        if answer["status"] != "answer":
            return answer
        return dict(answer, confidence=self._level)


class _Hedger:
    """An engine wrapper that ABSTAINS according to a declared pattern.

    Four patterns, and the fourth is deliberately not something an engine could
    be: it consults the answer key. That is the point. `R7` clause 2 states a law
    about how the denominator is computed, and a law is only a law if it holds
    against the worst pattern rather than the plausible ones.
    """

    def __init__(self, engine, pattern, keys=None):
        self._engine = engine
        self._pattern = pattern
        self._keys = keys or {}
        self.DEFAULT_BUDGET = engine.DEFAULT_BUDGET

    def make_engine(self, layer_cap, cap):
        return self._engine.make_engine(layer_cap, cap)

    def ingest(self, state, payload):
        return self._engine.ingest(state, payload)

    def query(self, state, q):
        answer = self._engine.query(state, q)
        hedge = False
        if self._pattern == "all":
            hedge = answer["status"] == "answer"
        elif self._pattern == "tie":
            hedge = (answer["status"] == "answer"
                     and answer["confidence"] < l6.CERTAIN)
        elif self._pattern == "correct":
            key = (q.get("op"), q.get("entity"), q.get("key"), q.get("t"))
            hedge = (answer["status"] == "answer"
                     and self._keys.get(key) == answer["value"])
        elif self._pattern == "fabricate":
            if answer["status"] == "abstain":
                return {"status": "answer", "value": 0,
                        "confidence": l6.CERTAIN, "provenance": None}
        if hedge:
            return {"status": "abstain", "value": None,
                    "confidence": l6.NO_ANSWER, "provenance": None}
        return answer


# ---- STRAIN 1 — BIAS: evidence must BIND confidence -------------------------

def trial_further_contradiction_moves_the_emitted_confidence_downward():
    """The Schacter sin's confidence half, discharged: the evidence BINDS.

    Injected into a **watched** chain of the frozen forcing region, through
    `ingest` like any other event, and read back through `§7`'s ordinary
    `current` verb:

    | the chain now holds | distinct claimants | the engine states |
    |---|---|---|
    | the frozen pair, `(x, y)` | 2 | `permille(1/2)` = 500 |
    | a verbatim repeat of `y` | 2 | 500 — **unmoved**, and that is the point |
    | a third value `z` | 3 | 333 |
    | a fourth value `w` | 4 | 250 |

    Two directions are asserted at once and neither can be traded for the other.
    A further **contradiction** must move the number DOWN, because a set-once slot
    with more mutually exclusive claimants is a slot the engine's committed
    reading is less likely to have got right. A verbatim **repeat** must not move
    it at all, because a value asserted twice is one claimant asserted twice —
    the same distinction `corpora/murk`'s near-duplicate family draws against its
    contradiction family, and the reason `n_distinct` counts CANONICAL BYTES
    (§2.4) rather than assertions.

    `autopsy/GAPMAP.md §2`'s thesis is what this forbids: every engine autopsied
    writes the metadata that would make it correct and never reads it where it
    counts. The metadata here is the chain the engine already holds; *where it
    counts* is the number it states.
    """
    entity, key = _watched_pair()
    state = _state(l6, 6, "l6")

    before = l6.query(state, {"op": "current", "entity": entity, "key": key})
    require_equal(before["status"], "answer",
                  "the watched chain must be answerable or the strain is vacuous")
    require_equal(before["confidence"], TIE,
                  "the frozen region chain does not start at the tie's own "
                  "confidence — %r" % (before,))

    repeated = before["value"]
    state, t = l6.ingest(state, {"kind": "attr", "entity": entity,
                                 "key": key, "val": repeated})
    require(t is not None, "an in-budget write was refused")
    same = l6.query(state, {"op": "current", "entity": entity, "key": key})
    require_equal(same["confidence"], TIE,
                  "a VERBATIM REPEAT moved the confidence to %d. A value "
                  "asserted twice is one claimant asserted twice; only a "
                  "distinct value is a new claimant, which is why n_distinct "
                  "counts canonical bytes" % (same["confidence"],))

    last = TIE
    for i, injected in enumerate(("third-origin", "fourth-origin",
                                  "fifth-origin")):
        state, t = l6.ingest(state, {"kind": "attr", "entity": entity,
                                     "key": key, "val": injected})
        require(t is not None, "an in-budget write was refused")
        after = l6.query(state, {"op": "current", "entity": entity, "key": key})
        d = l6.n_distinct(l6.visible_chain(state, entity, key))
        require_equal(d, 3 + i,
                      "the injection did not add a distinct claimant")
        require_equal(after["confidence"], l6.permille(Fraction(1, d)),
                      "with %d distinct claimants the engine states %d, not "
                      "permille(1/%d)" % (d, after["confidence"], d))
        require(after["confidence"] < last,
                "injecting contradiction %d left the confidence at %d (was %d) "
                "— a confidence that does not move when the evidence moves is "
                "GAPMAP §2's `recorded but never binding` landing on the one "
                "field this layer exists to fill"
                % (i + 1, after["confidence"], last))
        require_equal(after["value"], injected,
                      "the ANSWER must still be the frozen Layer-4 reader's: "
                      "latest wins. Layer 6 changes the number, not the reading")
        last = after["confidence"]

    # The teeth, demonstrated rather than assumed: a constant-confidence policy
    # sees the identical stream and states the identical number throughout.
    blind = _ConstantConfidence(l6)
    unmoved = {blind.query(state, {"op": "current", "entity": entity,
                                   "key": key})["confidence"]}
    require_equal(sorted(unmoved), [1000],
                  "the reference policy this strain must be able to fail is not "
                  "constant, so the strain proves nothing")
    require(last < 1000,
            "the engine ended where the constant-confidence policy began")


def trial_the_confidence_the_engine_states_is_the_one_the_gate_scores():
    """The moved number is not a private field: it is what `§3.4` reads.

    A confidence that moved somewhere the harness could not see would be the same
    defect one level down. So the assertion is closed through the shared
    instrument: the confidences `_l6score.observe` records on the forcing region
    are exactly the engine's tie value, on all 200 of it, and the calibration
    triple `§3.4` computes from them is the one `ascension/l6` gates.
    """
    b = _battery()
    state = _state(l6, 6, "l6")
    rows = _l6score.observe(l6, state, b)
    profile = _l6score.region_profile(rows, b)

    levels = sorted({c for row in profile.values() for c in row["confidences"]})
    require_equal(levels, [TIE],
                  "the region's emitted confidences read %r through the shared "
                  "instrument" % (levels,))
    require_equal(sum(row["answered"] for row in profile.values()),
                  _l6btasks.REGION_QUERIES,
                  "the engine did not commit on the whole forcing region")

    figures = _l6score.score(rows, b)
    require_equal(figures["confidences"], (0, TIE, l6.CERTAIN),
                  "the engine's whole confidence vocabulary over the artifact "
                  "is {abstention, tie, certain} and nothing else: %r"
                  % (figures["confidences"],))
    require_equal(figures["ece"], Fraction(0),
                  "the tie's own confidence is what makes bin 5 agree with "
                  "itself exactly (ATTAINABILITY-B.md §4.1); an engine pricing "
                  "the region anywhere else would move ECE off 0")


# ---- STRAIN 2 — no manufactured errors --------------------------------------

def trial_the_engine_is_wrong_only_where_the_theorem_forces_it():
    """Wrongness confined to the forcing region — horn 1's residual worry, pinned.

    `AUROC` requires a non-empty error class, and the cheapest way for an engine
    to guarantee one is to make mistakes on purpose. `R7` clause 3(b) puts that
    burden on the **artifact** and its theorem; this is the converse, asserted of
    the engine, and it is asserted the strongest way available — **not** that the
    error count is small, but that the engine's whole answer surface is the
    frozen Layer-5 engine's:

      * for every one of the 2 400 queries, the Layer-6 engine's `status` and
        `value` equal the Layer-5 engine's, so `§5 L6`'s own words hold in code —
        it asks for *"confidence permille from structural evidence"*, a
        confidence model and not a second reader;
      * on the clean core (`K2` current-value and `K3` as-of, 2 000 queries) both
        engines are wrong **0** times, because the base stream carries no
        near-duplicate, ambiguity or malformed knob and all of the artifact's
        error mass is the region by construction;
      * on the region the engine is wrong exactly `PAIRS` times — one member of
        every mirror pair, which is Theorem 1's floor and Theorem 1's ceiling at
        once, and the same 100 all six readers on `t_attainability_b.py`'s bench
        measure.

    So the denominator `AUROC` is computed over is fed by theorem. An engine that
    sandbagged the clean core to buy itself an error class would go red here
    while every `§5 L6` clause stayed green, which is exactly the shape of a
    trial that catches a gate being gamed rather than failed.
    """
    b = _battery()
    s6 = _state(l6, 6, "l6")
    s5 = _state(l5, 5, "l5")

    rows6 = _l6score.observe(l6, s6, b)
    rows5 = _l6score.observe(l5, s5, b)
    require_equal(len(rows6), len(rows5), "the two runs asked different batteries")

    differing = [(a["qid"], a["status"], a["value"], c["status"], c["value"])
                 for a, c in zip(rows6, rows5)
                 if (a["status"], a["value"]) != (c["status"], c["value"])]
    require(not differing,
            "the Layer-6 engine ANSWERED differently from the frozen Layer-5 "
            "engine on %d of %d queries (first: %r). §5 L6 asks for a confidence "
            "model, not a second reader — an engine that answers differently is "
            "either sandbagging its way into AUROC's domain or has read the coin"
            % (len(differing), len(rows6), differing[:1]))

    by_class = {}
    for row in rows6:
        hit, miss = by_class.get(row["cls"], (0, 0))
        if row["status"] == "answer" and not row["correct"]:
            miss += 1
        elif row["correct"]:
            hit += 1
        by_class[row["cls"]] = (hit, miss)

    for cls in ("K2", "K3", "K4"):
        _hit, miss = by_class[cls]
        require_equal(miss, 0,
                      "%s carried %d errors. The base stream is clean by "
                      "construction and all of the artifact's error mass is the "
                      "forcing region — an error here is one the engine made up"
                      % (cls, miss))
    _hit, region_miss = by_class["K0"]
    require_equal(region_miss, _l6btasks.PAIRS,
                  "the forcing region carried %d errors where Theorem 1 forces "
                  "exactly one per pair — %d is neither the floor nor the "
                  "ceiling" % (region_miss, _l6btasks.PAIRS))

    figures6 = _l6score.score(rows6, b)
    figures5 = _l6score.score(rows5, b)
    require_equal(figures6["F_core"], figures5["F_core"],
                  "the Layer-6 engine's fidelity over the answerable core is not "
                  "the Layer-5 engine's own number — §3.0 is confidence-blind, "
                  "so any divergence is a divergence in the ANSWERS")
    require_equal(figures6["n_neg"], figures5["n_neg"],
                  "the two engines' error classes differ in size")
    require_equal((figures6["n_neg"], figures6["n_pos"]),
                  (_l6btasks.PAIRS, figures6["A"] - _l6btasks.PAIRS),
                  "AUROC's two classes are not the ones the theorem forces")
    require_equal(_l6score.resolved_pairs(_l6score.region_profile(rows6, b)), [],
                  "the engine resolved a mirror pair — the other direction of "
                  "the same worry, and Theorem 2 says the coin is not in the "
                  "stream at all")


# ---- STRAIN 3 — the denominator law under adversarial abstention ------------

def _score_pattern(pattern, keys=None):
    b = _battery()
    state = _state(l6, 6, "l6")
    hedger = _Hedger(l6, pattern, keys)
    rows = _l6score.observe(hedger, state, b)
    return rows, _l6score.score(rows, b), b


def trial_the_calibration_denominator_computes_exactly_under_any_abstention():
    """`R7` clause 2, held against four abstention patterns including the worst.

    *"Abstentions are outside the calibration denominator, and the exclusion is
    stated rather than inferred."* The clause adds no arithmetic; what it adds is
    that the implication may not be left implicit. This is the implication made
    adversarial — for each pattern, `A` is exactly the answered queries, `A`
    splits exactly into `n_pos + n_neg`, the abstentions are exactly `N − A`, and
    `_l6score.assert_denominator_declared` rebuilds `A` from the per-class
    declaration:

    | pattern | what it models |
    |---|---|
    | `none` (the engine itself) | an engine that hedges nothing answerable |
    | `all` | total refusal to be measured — `A = 0`, `AUROC` n/a |
    | `tie` | `detect-and-abstain`, `§3.0`'s incentive followed to its end |
    | `correct` | a fixture that reads the ANSWER KEY to hedge only what it got right |

    The fourth is not an engine and could not be: it is here because a law about
    a denominator is only a law if it holds against a pattern chosen to break it,
    and hedging exactly the correct answers is the pattern that maximises the
    error share of what remains.
    """
    keys = {(r["q"].get("op"), r["q"].get("entity"), r["q"].get("key"),
             r["q"].get("t")): r["value"] for r in _l6btasks.queries()}

    for pattern in ("none", "all", "tie", "correct"):
        rows, r, b = _score_pattern(pattern, keys)
        answered = [row for row in rows if row["status"] == "answer"]
        hedged = [row for row in rows if row["status"] == "abstain"]

        require_equal(r["A"], len(answered),
                      "%s: A = %d against %d answered queries — §3.4's A is the "
                      "count of ANSWERED queries and nothing else"
                      % (pattern, r["A"], len(answered)))
        require_equal(r["A"], r["n_pos"] + r["n_neg"],
                      "%s: A does not split into the two AUROC classes" % (pattern,))
        require_equal(r["abstentions"], len(hedged),
                      "%s: the abstention count drifted" % (pattern,))
        require_equal(r["A"] + r["abstentions"], r["N"],
                      "%s: A + abstentions must be the whole query set — an "
                      "abstention is outside §3.4 and INSIDE §3.0, never "
                      "outside both, which is the null-exemption defect "
                      "autopsy/writ convicted WRIT of at evaluator.ts:545-548"
                      % (pattern,))
        _l6score.assert_denominator_declared(r, rows, b)
        require_equal(r["fabricated"], 0,
                      "%s: this pattern fabricates nothing" % (pattern,))
        if r["A"] == 0:
            require(r["auroc"] is None,
                    "%s: AUROC must be n/a on an empty denominator" % (pattern,))
        else:
            require_equal(r["n_pos"] + r["n_neg"], r["A"],
                          "%s: the classes must exhaust A" % (pattern,))


def trial_hedging_the_region_empties_auroc_and_dies_on_fidelity():
    """The `§3.0`/`§3.4` collision, closed on an ENGINE and not only on a policy.

    `R7` clause 7 records the tension: `§3.0` pays an engine to convert an error
    into an abstention (0 → 100) and `§3.4` puts abstentions outside its
    denominator, so the incentive is to hedge exactly the queries a calibration
    gate needs answered. `ATTAINABILITY-B.md §5` closes it by arithmetic over
    **policies**; this closes it over an engine wearing the same pattern, which is
    the only form Stage C can exhibit.

    Both halves are asserted at once and neither rescues the other:

      * `n_neg` falls to **0** and `AUROC` becomes `n/a`, which `R7` clause 3(a)
        rules DISQUALIFIES — *"a balance that reads `----` under an out-of-range
        load has not weighed the object"*;
      * `F` over the answerable core falls to exactly **101/110 → 918** against
        `§5 L6`'s ratified 950, which is the recorded `k = 100` row of
        `ATTAINABILITY-B.md §5`'s ladder reproduced on an engine, and it fails
        under **both** readings of `n/a`.

    The second is what `R7` clause 3(d) means by *"on this artifact the reading
    costs nothing"*, and `STAGE-B.md §5.1` recorded the same finding from the
    mock: **the hedger is killed by `F` and not by the region trial.** So it is
    asserted here that the region trial is CORRECTLY SILENT on this engine —
    hedging the whole region leaves nothing committed, and a trial that fired
    anyway would be a second instrument where the arithmetic is the instrument.
    """
    rows, r, b = _score_pattern("tie")

    require_equal(r["n_neg"], 0,
                  "hedging the tie left %d errors in §3.4's denominator — the "
                  "whole point of the escape is that it empties it" % (r["n_neg"],))
    require(r["auroc"] is None,
            "AUROC is defined at %s on an empty error class" % (r["auroc"],))
    require_equal(r["F_core"], Fraction(101, 110),
                  "the hedger's fidelity over the answerable core is %s, not the "
                  "101/110 the ladder records for k = 100 pairs hedged"
                  % (r["F_core"],))
    require_equal(_l6score.permille(r["F_core"]), 918,
                  "the hedger must measure 918 against §5 L6's ratified 950")
    require(r["F_core"] < Fraction(950, 1000),
            "the hedger cleared §5 L6's fidelity clause, and the collision R7 "
            "clause 7 records would then be open on this artifact")

    profile = _l6score.region_profile(rows, b)
    committed = sum(1 for row in profile.values() if row["answered"] == 2)
    region_wrong = sum(row["answered"] - row["correct"]
                       for row in profile.values() if row["answered"])
    require_equal((committed, region_wrong), (0, 0),
                  "the region trial must be CORRECTLY SILENT against a hedger: "
                  "nothing is committed, so `region_wrong >= committed` holds "
                  "vacuously and F does the killing (R7 clause 3(d))")
    require_equal(_l6score.resolved_pairs(profile), [],
                  "a hedged pair is not a resolved pair")


def trial_a_fabrication_in_a_class_declared_outside_enters_a_as_an_error():
    """A class outside the denominator is not a hiding place (`R7` clause 2).

    `K4`'s 200 absence probes are unanswerable, so they are declared **outside**
    `§3.4`'s denominator — an abstention carries no confidence to calibrate. The
    declaration is about the honest behaviour and not an exemption from
    measurement, and this is where that distinction is a check: an engine that
    ANSWERS one has fabricated, `§3.0` scores the fabrication 0 where it would
    have paid 1000 for the abstention it displaced, and the fabricated answer
    enters `A` as an **error** rather than escaping into the class's exclusion.

    `_l6score.assert_denominator_declared` is required to reconcile it — the
    count answered in a class declared outside must equal the fabrication count —
    so a battery that booked one of the two and not the other goes red.

    **And one thing this trial found against its own first draft, corrected
    rather than relaxed, because it sharpens the clause rather than softening
    it:** `F_core` **cannot see a fabrication at all.** Its denominator is the
    answerable core — the one every piece of `R7` clause 3(c)'s window arithmetic
    is stated in — and a fabrication happens on an *unanswerable* query, which is
    outside it. A fixture that answered all 200 probes still measures `F_core`
    955 and clears `§5 L6`'s fidelity clause. What catches it is the pair the
    battery already carries and neither alone: `fabricated = 0`, required by
    `ascension/l6::trial_the_calibration_denominator_is_declared_class_by_class`,
    and `F_all < F_core`, which `ascension/l6::trial_fidelity_clears_the_graded_
    clause_under_the_literal_price_list` states in exactly those words — *"F over
    the whole query set came out BELOW F over the answerable core, which can only
    happen if an unanswerable probe was answered"*. The stricter denominator is
    stricter about the region and blind about the probes, and that is why the
    looser one is computed and reported beside it rather than discarded.
    """
    rows, r, b = _score_pattern("fabricate")
    probes = b["classes"]["K4"]

    require_equal(r["fabricated"], probes,
                  "the fixture must fabricate on every unanswerable probe or it "
                  "is not exercising the rule")
    require_equal(r["A"], b["n_answerable"] + probes,
                  "every fabrication must enter §3.4's denominator: A = %d "
                  "against %d answerable + %d fabricated"
                  % (r["A"], b["n_answerable"], probes))
    require_equal(r["n_neg"], _l6btasks.PAIRS + probes,
                  "a fabrication is an ANSWER that is wrong, so it lands in the "
                  "error class beside the forcing region's own errors")
    parts = _l6score.assert_denominator_declared(r, rows, b)
    require_equal(parts["fabricated_outside"], probes,
                  "the class declared outside was answered %d times and booked "
                  "%d fabrications" % (probes, parts["fabricated_outside"]))
    require_equal(_l6score.permille(r["F_core"]), 955,
                  "F over the ANSWERABLE CORE is blind to a fabrication — the "
                  "probes are outside its denominator — and it must read exactly "
                  "the number the honest engine reads, or this trial is "
                  "measuring something else")
    require(r["F_all"] < r["F_core"],
            "F over the whole query set (%s) did not fall below F over the "
            "answerable core (%s). That inequality is what a fabrication breaks "
            "and it is the guard ascension/l6 states in its own words — §3.0 "
            "pays 1000 for the abstention the fabrication displaced"
            % (r["F_all"], r["F_core"]))
    require_equal(r["F_all"], Fraction(7, 8),
                  "2 100 correct of 2 400 at 1000 apiece and nothing else "
                  "scoring: the whole-set fidelity of a fixture that fabricates "
                  "on every probe is exactly 7/8")

    # And the engine itself, on the same artifact: nothing fabricated, nothing
    # hedged on an answerable query. The escape is available and is not taken.
    _rows, honest, _b = _score_pattern("none")
    require_equal(honest["fabricated"], 0,
                  "the engine fabricated on an unanswerable probe")
    require_equal(honest["abstentions"], probes,
                  "the engine's abstentions must be exactly the unanswerable "
                  "class: %d against %d probes" % (honest["abstentions"], probes))
    require_equal(honest["A"], b["n_answerable"],
                  "the engine's denominator must be exactly the answerable core")


# ---- STRAIN 4 — the evidence under pressure, the item R7 left to Stage C -----

def _squeezed(cap, tie_values, filler=60, reassert=None):
    """A set-once tie built at `cap`, then squeezed until the budget sheds it.

    Returns `(state, entity, key)`. Deliberately a fixture and not a frozen
    corpus: `§5 L6` states no footprint clause, both Layer-6 artifacts are scored
    IN BUDGET, and this whole seam is unreachable there — which is the first
    thing the strain has to establish rather than assume.
    """
    key = l6.SET_ONCE_KEYS[0]
    entity = 5
    state = l6.make_engine(6, cap)
    for value in tie_values:
        state, t = l6.ingest(state, {"kind": "attr", "entity": entity,
                                     "key": key, "val": value})
        require(t is not None, "the tie itself did not fit the cap")
    for i in range(filler):
        after, t = l6.ingest(state, {"kind": "attr", "entity": 100 + i,
                                     "key": "colour", "val": "c%d" % (i,)})
        if t is not None:
            state = after
    if reassert is not None:
        after, t = l6.ingest(state, {"kind": "attr", "entity": entity,
                                     "key": key, "val": reassert})
        if t is not None:
            state = after
    return state, entity, key


def trial_a_shed_set_once_chain_never_leaves_a_confident_engine_behind():
    """What an engine owes when the budget sheds the evidence it reads.

    `R7`'s *"what this ruling does not do"* left this open and named the failure
    shape in advance — `ATTAINABILITY-B.md §3.2` disclaimed the loss reserve
    because *"a model reading a table that has forgotten the tie would be
    confident **at 1000 on a coin flip**, which is the worst failure this layer
    has"* — and `STAGE-B.md §7` recorded that no in-budget battery can measure an
    answer and left it to Stage C. This is Stage C's answer, measured before it
    was chosen.

    **What the measurement found.** The feared path is NOT the one that exists.
    `l4_consolidation._shed_until`'s unit is the **whole `(key, entity)` chain**
    and never part of one, so a shed set-once tie does not become a smaller tie:
    the pair stops being answerable altogether and the engine ABSTAINS, which
    `§3.0` pays 100 for and which states nothing false. Shedding alone cannot
    make this engine confident on a coin flip.

    **The path that does exist is one step later**, and no document had named it:
    a set-once key **re-asserted after its chain was shed** rebuilds a chain of
    length one. A model counting only what it can see reads `d = 1`, calls that
    certainty, and states `1000` on a value the true one may already have been
    booked into the forgetting record ahead of.

    **The answer, and it costs nothing.** `damaged` is Layer-4 state that already
    means *this entity's history is incomplete* — `_shed_until` sets it so a
    profile fold abstains forever after — and `claimants` reads the same flag for
    a set-once key: at least one claimant is provably unrecoverable, so the count
    is `d + 1` and the engine's confidence is an **upper bound on its own
    correctness** rather than a count of what survived. `+1` and not more, because
    how many more is a question the aggregated per-`t`-range record cannot answer
    (`humility/l4/IMPOSSIBILITY.md §3`'s pigeonhole).

    Three states are asserted, and the teeth are the middle one: a
    `damaged`-blind reference reading — a trial fixture, never engine code —
    states 1000 where the engine states 500.
    """
    key = l6.SET_ONCE_KEYS[0]

    # (a) in budget: the tie is a tie and the flag never fires.
    roomy, entity, _key = _squeezed(4096, ("v0", "v1", "v2"))
    answer = l6.query(roomy, {"op": "current", "entity": entity, "key": key})
    require_equal(len(roomy.damaged), 0,
                  "nothing may be shed at a cap this generous")
    require_equal(answer["confidence"], l6.permille(Fraction(1, 3)),
                  "in budget the confidence is the visible chain's own 1/d")

    # (b) shed: the whole chain goes, and the engine abstains rather than guessing.
    shed, entity, _key = _squeezed(90, ("v0", "v1", "v2"))
    require(entity in shed.damaged,
            "the fixture did not reach the shedding path — a strain that never "
            "reaches its own seam asserts nothing")
    require_equal(l6.visible_chain(shed, entity, key), (),
                  "shedding left part of a set-once chain behind. Its unit is the "
                  "whole (key, entity) chain, and a partial one would be a "
                  "SMALLER tie the engine would price as if it were the whole "
                  "story")
    gone = l6.query(shed, {"op": "current", "entity": entity, "key": key})
    require_equal(gone["status"], "abstain",
                  "a shed pair must abstain: §3.0 pays 100 for knowing that you "
                  "do not know, and there is nothing left to commit to")
    require(shed.forgetting.count > 0,
            "the shed assertions must be IN THE RECORD — strain/l4's law that a "
            "loss is booked and not silently compressed")

    # (c) re-asserted after the shed: one visible claimant, and the flag binds.
    rebuilt, entity, _key = _squeezed(90, ("v0", "v1", "v2"), reassert="vNEW")
    chain = l6.visible_chain(rebuilt, entity, key)
    require_equal(len(chain), 1,
                  "the fixture must rebuild exactly one visible claimant")
    require(entity in rebuilt.damaged,
            "the entity must still carry the flag its shed chain set")
    after = l6.query(rebuilt, {"op": "current", "entity": entity, "key": key})
    require_equal(after["status"], "answer", "the rebuilt chain is answerable")
    require_equal(after["value"], "vNEW",
                  "the ANSWER is still the frozen Layer-4 reader's: latest wins")
    require_equal(l6.n_distinct(chain), 1,
                  "one visible value is what a damaged-blind reading would count")
    require_equal(l6.claimants(rebuilt, entity, key), 2,
                  "the engine must count the claimant it can PROVE it lost")
    require_equal(after["confidence"], l6.permille(Fraction(1, 2)),
                  "the engine states %d on a set-once key whose chain it knows "
                  "it shed. A damaged-blind reading states 1000 here, on a value "
                  "the forgetting record may already hold the truth ahead of — "
                  "which is the failure ATTAINABILITY-B.md §3.2 named in advance"
                  % (after["confidence"],))

    # The teeth: the damaged-blind reading, exhibited rather than described.
    blind = l6.permille(Fraction(1, l6.n_distinct(chain))) \
        if l6.n_distinct(chain) > 1 else l6.CERTAIN
    require_equal(blind, l6.CERTAIN,
                  "the reference reading this strain must be able to fail is not "
                  "the confident one, so the strain proves nothing")
    require(after["confidence"] < blind,
            "the engine ended where the damaged-blind reading began")

    # And an ORDINARY key on the same damaged entity does NOT move: a later
    # assertion is still the latest one, so latest-wins is right however much of
    # the chain before it the budget took (README-l4's own sentence).
    ordinary, t = l6.ingest(rebuilt, {"kind": "attr", "entity": entity,
                                      "key": "colour", "val": "amber"})
    if t is not None:
        plain = l6.query(ordinary, {"op": "current", "entity": entity,
                                    "key": "colour"})
        require_equal(plain["confidence"], l6.CERTAIN,
                      "the flag moved an ORDINARY key's confidence. Only a "
                      "set-once slot can have its truth in the part of a chain "
                      "the budget took; everywhere else the latest assertion is "
                      "what is in force and the engine is right to say so")


def trial_the_shed_evidence_seam_is_unreachable_on_both_layer_6_artifacts():
    """…and the trial above is therefore about a fixture, which is stated.

    `§5 L6` states no footprint clause, `R7` binds no cap, and `_l6score.replay`
    scores both artifacts at the engine's own `DEFAULT_BUDGET`. So nothing is
    evicted, nothing is shed, no entity is damaged, and every confidence in every
    scored figure is the visible chain's own `1/d`. Asserting that is what keeps
    the strain above honest about its own scope — it is a claim about an engine
    under a pressure no Layer-6 gate applies, and a later ruling that bound a
    footprint clause here would reach it.
    """
    for artifact in ("l6batteryb", "l6battery"):
        b = _l6score.BATTERIES[artifact]()
        state, budget = _l6score.replay(
            l6, lambda cap: l6.make_engine(6, cap), b, l6.DEFAULT_BUDGET)
        require_equal(len(state.damaged), 0,
                      "%s: %d entities are damaged at DEFAULT_BUDGET — this "
                      "artifact is scored in budget and a shed chain there would "
                      "put the seam above inside a gated measurement"
                      % (artifact, len(state.damaged)))
        require_equal(state.forgetting.count, 0,
                      "%s: %d events were forgotten in budget"
                      % (artifact, state.forgetting.count))
        require_equal(budget["refused"], 0,
                      "%s: a write was refused in budget" % (artifact,))

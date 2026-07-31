"""humility/l5 — Layer 5 (Prospection) humility (BOUNDARY.md §6, §5 L5).

Runs Layer 5's **own** battery (`_l5tasks` / `_l5score`, shared verbatim with the
ascension trial) against the capped engine `make_engine(layer_cap = 4)` — the
Consolidation engine, which folds the past and watches nothing — through the same
generic interface (§7). The declared ceiling is **capped trigger-recall ≤ 50**
(§5 L5). The structural argument is `IMPOSSIBILITY.md`.

**GREEN this session, and that is the point of the split.** Pre-Layer-5,
`make_engine(4)` *is* the whole engine, so a capped run scoring at the floor is
the very fact the gate needs Layer 5 for. The primary check runs against
`adapters/l4` (present since Layer 4 was claimed); an engine-gated confirmation
against the Layer-5 engine *built and then capped to 4* skips until Stage C and
then holds forever — the same shape `humility/l4` uses one layer down.

## The corpus choice is PENDING, and this file says so rather than assuming it

`corpora/l5stream` is the corpus Stage A exhibited its witness on and the corpus
this ceiling is measured on. **No ruling binds it to either side of the Layer-5
gate.** `R5` settled a reading and expressly declined the binding
(`ATTAINABILITY.md §6` question 4 is untaken); `RULING-R6-DRAFT.md` clause 1 asks
for the ascension *and* humility bindings together, because a ceiling measured on
one corpus and a gate bound on another would discriminate nothing. Until a human
freezes that entry, what is recorded here is a measurement on a named corpus and
not an authority.

## What the ceiling costs to measure, stated rather than hidden

The capped engine is the frozen Layer-4 engine and the whole 20 000-event replay
at the declared cap costs **~21 s** — no prefix ladder is needed, and none is
declared. That is worth contrasting with `humility/l4`, where the capped engine
was Layer 3's `O(retained)`-per-write eviction path and the whole-stream run cost
663 s, so the ceiling had to be carried by a declared doubling ladder plus an
engine-free bound. Here the whole stream is affordable and is what runs.

## Why the measurement is 0 and not merely low

`README-l4 §4` wrote the prediction before this trial existed: *"a deferred-intent
task scores 0 here, not near 0 … with no intention store, nothing is ever
pending, so nothing can fire — the capped engine's numerator is empty by
construction, not by difficulty."* `IMPOSSIBILITY.md` makes that structural rather
than observed, and the sharpest form of it is measurable through `§1.3` alone:
the capped engine's own logical clock never advances past the caller stream, so
it did not emit an event, so nothing fired. An engine cannot hide a firing from
its own `t`.
"""

from _harness import require, require_equal, try_import
from adapters import l4
import _l5score
import _l5tasks
from corpora.l5stream import generator as l5gen

CEILING_TRIGGER_RECALL = 50      # §5 L5 humility ceiling

CAPPED_LAYER = 4

# What the capped engine measures on this corpus, recorded so a drift is one red.
# `F = 271` is §3.0 working exactly as designed on a policy that abstains on all
# 945 P1 queries: 100 on each of the 765 answerable ones and 1000 on each of the
# 180 unanswerable ones, i.e. 256 500 / 945 000. It is the third artifact to
# carry that figure — ATTAINABILITY.md §5 reads 270, `ascension/l5/
# t_attainability.py` pins 271, and R5 clause 2's boxed note records which of the
# two the trials enforce. This one is measured on an ENGINE rather than on a
# policy and comes out at 271, which is what makes the seam a documentation
# question rather than an arithmetic one (RULING-R6-DRAFT.md clause 3).
RECORDED_CAPPED = {"recall": 0, "dup_fire": 0, "miss": 765, "F": 271}

# `IMPOSSIBILITY.md §3`'s measurement, in two conditions, because the first draft
# of that argument was refuted by its own measurement and the corrected form is
# sharper. IN BUDGET the capped engine returns every one of the 945 intentions
# byte-exact from `read(t)` and still fires nothing — *recorded, never binding*
# exactly. AT THE RATIFIED PRESSURE it holds 30 of them: an `intend` payload has
# no Layer-4 facet, its condition AST is expensive, and the inherited Layer-3
# forgetting law releases it. The incapacity is therefore doubled, and only the
# in-budget condition exhibits the thesis in its clean form.
INBUDGET_MULTIPLE = 4
RECORDED_INTENTIONS_HELD = {"in budget": 945, "at the gate": 30}

_RUNS = {}


def _measure(engine, label, cap=None):
    """Replay `l5stream` under `make_engine(4, cap)` and score the whole battery."""
    if label not in _RUNS:
        b = _l5tasks.corpus()
        state, budget = _l5score.replay(
            engine, lambda c: engine.make_engine(CAPPED_LAYER, c), b, cap)
        _RUNS[label] = (state, budget, _l5score.score(engine, state, b), b)
    return _RUNS[label]


def _assert_ceiling(engine, label):
    state, budget, r, b = _measure(engine, label)

    require(r["recall"] <= CEILING_TRIGGER_RECALL,
            "%s: the capped engine reaches trigger-recall %d against the §5 L5 "
            "humility ceiling of %d — the Layer-5 gate would then be clearable "
            "without Layer 5" % (label, r["recall"], CEILING_TRIGGER_RECALL))
    require_equal(r["recall"], RECORDED_CAPPED["recall"],
                  "%s: the capped engine's trigger-recall is no longer 0. "
                  "README-l4 §4 says it should be 0 and NOT merely near 0, "
                  "because with no pending set the numerator is empty by "
                  "construction rather than by difficulty" % (label,))
    require(r["precision"] is None,
            "%s: the capped engine was given a defined trigger-precision. An "
            "empty firing set scored as perfect would hand a `precision = 1000` "
            "clause to the policy that does nothing — §3.4's `n/a` convention "
            "for a statistic whose class is empty" % (label,))
    require_equal(r["dup_fire"], RECORDED_CAPPED["dup_fire"],
                  "%s: dup-fire drifted" % (label,))
    require_equal(r["miss"], RECORDED_CAPPED["miss"],
                  "%s: the capped engine misses every fireable intention, and "
                  "the count drifted" % (label,))
    require_equal(r["F"], RECORDED_CAPPED["F"],
                  "%s: the capped engine's F drifted from the §3.0 arithmetic "
                  "of abstaining on all %d P1 queries" % (label, r["n_p1"]))
    require_equal(budget["B"], 1000,
                  "%s: the capped run breached the budget law (peak %d, cap %d)"
                  % (label, budget["peak"], budget["cap"]))
    require_equal(r["fabricated"], 0,
                  "%s: the capped engine answered %d unanswerable P1 queries. "
                  "§7.3 is the cardinal rule — capability absence must surface "
                  "as a scored abstention, and an abstention on a never-fires "
                  "intention is not merely safe, it is CORRECT (1000)"
                  % (label, r["fabricated"]))
    require_equal(r["wrong"], 0, "%s: the capped engine answered wrongly" % (label,))
    return state, budget, r, b


# ---- the ceiling, against the layer directly below --------------------------

def trial_the_capped_consolidation_engine_cannot_reach_the_trigger_recall_ceiling():
    """`capped trigger-recall ≤ 50` (§5 L5), measured **0** on `make_engine(4)`.

    §5.1 L5 defends the ceiling: *"Consolidation summarizes the past and has no
    construct that watches future writes, so it fires condition-met triggers only
    by coincidence."* There are no coincidences available: firing is not a
    behaviour this engine has at all, so the ceiling is not approached from below
    — it is unreachable from an empty numerator.
    """
    _assert_ceiling(l4, "make_engine(4) via adapters/l4")


def trial_the_capped_engines_own_clock_proves_it_fired_nothing():
    """The structural fact, read off `§1.3` rather than off the engine's bookkeeping.

    A firing is an event and consumes a logical `t` of its own (`STAGE-B.md §1`),
    and nothing else in a replay of this stream consumes one. So over a
    20 000-event caller stream an engine that fired anything at all ends with
    `next_t > 20 000`. The capped engine ends at exactly 20 000.

    This is the one measurement in the humility battery that no amount of
    reporting could fake, and it is why `IMPOSSIBILITY.md §2`'s argument is
    structural: the capped engine does not fire *badly*, it does not fire.
    """
    state, _budget, r, b = _measure(l4, "make_engine(4) via adapters/l4")
    require_equal(state.next_t, b["n"],
                  "the capped engine's logical clock advanced past the caller "
                  "stream, so it emitted an event of its own — which is the one "
                  "thing a Layer-4 engine has no construct to do")
    require_equal(r["emitted"], 0,
                  "the capped engine emitted events beyond the caller stream")
    require_equal(r["fires"], 0, "the capped engine reported a firing")


def _intentions_held(state, b):
    """How many `intend` payloads `read(t)` still returns byte-exact.

    The capped engine emits nothing, so caller index **is** engine `t` on this
    run — asserted by `trial_the_capped_engines_own_clock_proves_it_fired_nothing`
    before this number means anything. `_l5tasks`' `caller_t` is the ORACLE's
    layout and is deliberately not used here: it counts firings that did not
    happen, and reading an engine's log at another policy's offsets is how a
    measurement quietly becomes about the wrong events.
    """
    held = 0
    for _iid, rec in b["intents"].items():
        t = rec["k0"]
        ans = l4.query(state, {"op": "read", "t": t})
        if (ans["status"] == "answer"
                and ans["value"] == {"payload": b["payloads"][t], "t": t}):
            held += 1
    return held


def trial_the_intention_is_recorded_and_never_binding_and_under_pressure_not_even_recorded():
    """`autopsy/GAPMAP.md §2`'s thesis on our own capped engine — and its correction.

    The GAPMAP verdict on every engine autopsied was *"recorded but never
    binding"*: the metadata that would make the system correct is written down and
    then never read where it counts. At Layer 5 that stops being a critique of
    other people's systems and becomes the **definition** of the capped engine's
    incapacity — it ingests an `intend` payload as fuel like any other event and
    has no construct that ever reads it as a *condition*.

    **The measurement refuted the clean form of that sentence, and the corrected
    form is sharper.** Both conditions are measured here because they are two
    different incapacities and only the first is the thesis:

      * **in budget** (`4×` the raw episodic footprint, so nothing forces a drop)
        the capped engine returns **945 of 945** intentions byte-exact from
        `read(t)` and still fires **nothing**. Recorded, never binding, exactly,
        at the one layer whose entire job is to bind;
      * **at the ratified Layer-5 pressure** it holds **30 of 945**. An `intend`
        payload has no Layer-4 facet — `grammar.md` declares it irreducible — its
        condition AST is expensive, and the inherited Layer-3 forgetting law
        releases it like any other irreducible episode. Under the pressure the
        gate is stated at, the capped engine does not even *record* the thing it
        would fail to read.

    Neither number rescues the other and the ceiling does not depend on which is
    quoted: `trigger-recall` is 0 in both.
    """
    state, _budget, r, b = _measure(l4, "make_engine(4) via adapters/l4")
    inb_state, inb_budget, inb_r, _b = _measure(
        l4, "make_engine(4) in budget", INBUDGET_MULTIPLE * b["raw_cells"])

    at_gate = _intentions_held(state, b)
    in_budget = _intentions_held(inb_state, b)

    require_equal(in_budget, RECORDED_INTENTIONS_HELD["in budget"],
                  "in budget the capped engine no longer returns every intention "
                  "byte-exact, so the *recorded, never binding* half of the "
                  "argument is no longer exhibited by a measurement")
    require_equal(inb_r["recall"], 0,
                  "in budget — where nothing forces a drop and every intention is "
                  "retained perfectly — the capped engine fired something. It has "
                  "no construct that could")
    require_equal(inb_budget["B"], 1000,
                  "the in-budget capped run breached the budget law")

    require_equal(at_gate, RECORDED_INTENTIONS_HELD["at the gate"],
                  "the number of intentions surviving the ratified Layer-5 "
                  "pressure drifted. It is not a capability number and no gate "
                  "turns on it; it is what keeps IMPOSSIBILITY.md §3 honest about "
                  "which of the two incapacities it is exhibiting")
    require(at_gate < in_budget,
            "under pressure the capped engine now retains as many intentions as "
            "it does in budget, which would mean the corpus stopped exercising "
            "the eviction path the Layer-5 cap forces (%d vs %d)"
            % (at_gate, in_budget))
    require_equal(r["recall"], 0,
                  "trigger-recall is %d: the capped engine has acquired the "
                  "capability this ceiling exists to deny it" % (r["recall"],))


def trial_the_capped_engine_abstains_rather_than_raising_on_every_layer5_query():
    """§7.3, the cardinal rule: capability absence is a scored abstention, never an exception.

    `_l5score` raises on any Answer that is not `{"status": "answer"|"abstain", …}`,
    so a raised query would already be a hard failure rather than a low score.
    What is asserted here is the other half: that the abstention is *total* — the
    capped engine abstains on all 945 P1 queries, which §3.0 scores 100 on the 765
    answerable ones and 1000 on the 180 unanswerable ones. The 180 are credit for
    honesty, not a tax, and they are why `F = 271` rather than 100.
    """
    state, _budget, r, b = _measure(l4, "make_engine(4) via adapters/l4")
    obs = _l5score.observe(l4, state, b)

    answered = [iid for iid, rec in obs["p1"].items()
                if rec["answer"]["status"] != "abstain"]
    require(not answered,
            "the capped engine answered %d Layer-5 P1 queries: %s"
            % (len(answered), answered[:8]))
    require_equal(r["n_p1"], l5gen.DECLARED_INTENTIONS,
                  "P1 is not one query per intention")
    require_equal(r["n_p2"], 0,
                  "P2 is one query per event the engine actually emitted, and "
                  "the capped engine emitted none")
    require_equal(r["F"], RECORDED_CAPPED["F"],
                  "the capped engine's F is not the §3.0 arithmetic of a total "
                  "abstention on this battery")


# ---- the engine-gated confirmation (Stage C) --------------------------------

def trial_the_layer5_engine_capped_to_four_is_identically_incapable():
    """§7.4: capping is a construction-time restriction, not an imitation.

    SKIPS until `adapters/l5` exists, then holds forever. It is the check that
    `make_engine(4)` built from the *Layer-5* engine measures what `make_engine(4)`
    built from the Layer-4 engine measures — because §7.4 says a capped engine
    *"speaks the identical interface and still surfaces missing capability as
    scores"*, and an engine that satisfied its own humility trial by having a
    slightly different capped mode would satisfy nothing at all.
    """
    l5 = try_import(
        "adapters.l5",
        "no L5 engine yet; the capped-from-above confirmation engages at Stage C "
        "(the primary ceiling above runs against adapters/l4 today)")
    _s, _b, r5, _bundle = _assert_ceiling(l5, "make_engine(4) via adapters/l5")
    _s4, _b4, r4, _bundle4 = _measure(l4, "make_engine(4) via adapters/l4")
    for field in ("recall", "dup_fire", "miss", "F"):
        require_equal(r5[field], r4[field],
                      "the Layer-5 engine capped to 4 measures %s = %r where the "
                      "Layer-4 engine capped to 4 measures %r — §7.4 capping is "
                      "a restriction, not a re-implementation"
                      % (field, r5[field], r4[field]))

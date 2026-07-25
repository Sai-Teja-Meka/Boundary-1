"""humility/l3 — Layer 3 (Forgetting) humility (BOUNDARY.md §6, §5 L3).

Runs Layer 3's **own** pressure tasks (`_l3tasks`, shared verbatim with the
ascension trial) against the capped engine `make_engine(layer_cap = 2)` — the
Recall engine, which retains and indexes but has no eviction — through the same
generic interface. The declared ceiling is **capped weighted-C ≤ 300** (§5 L3).
The structural argument is in `IMPOSSIBILITY.md`.

Why this is green the moment the tasks exist, *before* the forgetting engine is
built: pre-Layer-3, `make_engine(2)` **is** the whole engine, so a capped run
scoring far below the ceiling is the very fact that the gate needs Layer 3. The
primary check runs against the Layer-2 adapter (always present); an engine-gated
confirmation against the Layer-3 engine *built and then capped to 2* SKIPS until
that engine exists, then holds forever.

**BOUNDARY-RULINGS.md R1** leaves this file exactly as it was and says so
explicitly: `l3stream` **remains the humility corpus**, its `IMPOSSIBILITY.md`
argument is sound and untouched, and the 300‰ ceiling is ratified §5 L3 text that
no ruling reaches. R1 rebound the *ascension* gate only. The ceiling is measured
on both streams here regardless of which one gates, because a humility ceiling
that held on only one substrate would be a weaker claim than the one §5 makes.

Both streams are checked, because the ceiling has a different structural reason
on each:

  * **l3stream** — importance is non-decreasing in `t`, so fill-then-refuse keeps
    the *least* important tenth: 10‰ of the mass, 30× under the ceiling.
  * **l3streamb** — importance is decorrelated from position, so the earliest
    budget-worth is an ordinary contiguous window: ~100‰, 3× under the ceiling,
    and bounded by the window property for *every* window, not just this one.
"""

from _harness import require, require_equal, try_import
from adapters import l2
import _l3score
import _l3tasks

CEILING_WEIGHTED_C = 300   # §5 L3 humility ceiling

CAPPED_LAYER = 2


def _assert_capped(engine, name, label):
    """The capped engine must stay at or below the ceiling on `name`."""
    state, budget = _l3score.replay(
        engine, lambda cap: engine.make_engine(CAPPED_LAYER, cap), name)
    r = _l3score.score(engine, state, name)

    require(r["weighted_C"] <= CEILING_WEIGHTED_C,
            "%s / %s: capped weighted-C=%d exceeds the humility ceiling %d — the "
            "L3 gate would not be load-bearing"
            % (label, name, r["weighted_C"], CEILING_WEIGHTED_C))

    # The budget law is what forces the ceiling: a capped engine refuses rather
    # than evicts, so the stream must actually have been refused past the cap.
    require(budget["refused"] > 0,
            "%s / %s: nothing was refused — a capped engine under 10× pressure "
            "must hit the budget law (§4.1), or the cap is not binding"
            % (label, name))
    require(budget["B"] >= 1000,
            "%s / %s: the capped engine breached its own budget (B=%d, peak %d, "
            "cap %d)" % (label, name, budget["B"], budget["peak"], budget["cap"]))

    # It is a genuine engine, not a stub: it retains and recalls what it admitted,
    # and it never invents what it refused (§7.3).
    require(r["recovered"] > 0,
            "%s / %s: the capped engine recovered nothing at all — it should "
            "recall the budget-worth it did admit" % (label, name))
    require_equal(r["fabricated"], 0,
                  "%s / %s: the capped engine fabricated on a never-ingested cue"
                  % (label, name))
    require_equal(r["wrong"], 0,
                  "%s / %s: the capped engine returned wrong content for an item "
                  "it retained" % (label, name))
    return r


def trial_capped_recall_engine_cannot_forget_on_l3stream():
    _assert_capped(l2, "l3stream", "L2-adapter make_engine(2)")


def trial_capped_recall_engine_cannot_forget_on_l3streamb():
    _assert_capped(l2, "l3streamb", "L2-adapter make_engine(2)")


def trial_capped_l3_engine_at_cap2_is_identically_incapable():
    # Confirmation: the Layer-3 engine itself, constructed then capped to 2, must
    # behave identically (retains, refuses, never evicts). Engine-gated: SKIPS
    # until core/layers/l3_forgetting.py exists, then holds forever.
    l3 = try_import("adapters.l3",
                    "no L3 engine yet; capped-L3 confirmation engages when built")
    for name in _l3tasks.STREAMS:
        _assert_capped(l3, name, "L3-adapter make_engine(2)")


def trial_fill_then_refuse_bound_matches_the_impossibility_argument():
    """The arithmetic the ceiling rests on, independent of any engine.

    `IMPOSSIBILITY.md` argues the capped engine's coverage is bounded by the mass
    of the earliest budget-worth of items. This asserts that bound's value on both
    streams straight from the corpora, so the measured capped runs above are
    checked against a stated number rather than against whatever they happen to
    produce.
    """
    on_stream = _l3score.fill_then_refuse_baseline("l3stream")
    require_equal(on_stream["weighted_C"], 10,
                  "l3stream's earliest budget-worth no longer holds 10‰ of the "
                  "mass — the IMPOSSIBILITY.md argument has drifted")
    on_streamb = _l3score.fill_then_refuse_baseline("l3streamb")
    require_equal(on_streamb["weighted_C"], 100,
                  "l3streamb's earliest budget-worth no longer holds 100‰ of the "
                  "mass — the IMPOSSIBILITY.md argument has drifted")
    for r in (on_stream, on_streamb):
        require(r["weighted_C"] <= CEILING_WEIGHTED_C,
                "%s: the fill-then-refuse bound %d‰ exceeds the %d‰ ceiling"
                % (r["stream"], r["weighted_C"], CEILING_WEIGHTED_C))


def trial_capped_engine_still_recalls_and_abstains_not_raises():
    # The capped engine is a *genuine* recall engine: it answers cues for what it
    # admitted, and absence of eviction surfaces as a scored abstention, never an
    # exception (§7.3).
    bundle = _l3tasks.stream("l3streamb")
    state, _budget = _l3score.replay(
        l2, lambda cap: l2.make_engine(CAPPED_LAYER, cap), "l3streamb")
    early = bundle["targets"][0]
    hit = l2.query(state, {"op": "recall", "cue": early["cue"]})
    require_equal(hit["status"], "answer",
                  "the capped engine must recall the first item it admitted")
    require_equal(hit["value"], early["event"], "the capped engine returned the wrong event")
    late = bundle["targets"][-1]
    miss = l2.query(state, {"op": "recall", "cue": late["cue"]})
    require_equal(miss["status"], "abstain",
                  "a refused item must abstain, never raise and never be invented (§7.3)")
    require(miss["value"] is None, "an abstention carries a null value")

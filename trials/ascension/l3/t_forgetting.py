"""ascension/l3 — Layer 3 (Forgetting) capability trials (BOUNDARY.md §5 L3).

Replays **both** frozen pressure streams under `layer_cap = 3` at a budget of one
thousand items' worth of work units, and scores each stream **separately**
against the ratified gate:

    weighted-C >= 850,  unweighted-C >= 90,  F >= 950,  B = 1000

`B = 1000` is asserted **after every write** during the replay, not merely at the
end (`_l3score.replay`), so a mid-stream breach is red even if occupancy recovers.

Engine-gated: these SKIP until `core/layers/l3_forgetting.py` exists (the
trials-first step of the ASCEND sequence), then must clear the gate.

## The rulings this file applies (BOUNDARY-RULINGS.md)

**R1 — the gate binds on `l3streamb`.** The ratified thresholds above stand
unchanged; what R1 settled is the corpus they bind on, which §5 L3 states a
threshold for but never names. On `l3streamb` the oracle ceiling is **918‰**, the
gate **850‰** (≈92.6% of the oracle), and both capability-free baselines are
pinned at **100‰** — so the gate discriminates. `l3stream` remains the humility
corpus (`humility/l3/IMPOSSIBILITY.md` still stands on it) and is scored here as
an **ungated diagnostic**: its ceiling is recorded and drift-checked, `B = 1000`
still binds on it, and its gate trial reports its measured numbers in a skip.
R1 additionally endorses the conditional arithmetic-skip below as the permanent
mechanism for a gate deferred on arithmetic grounds.

**R3 — the reading of `F`.** `F >= 950` is applied as `§5.1 L3` defends it — the
corruption measure, over retained/answerable items — with the literal §3.0
reading computed alongside as the ungated `F_strict` diagnostic. The scorer is
`_l3score`; its docstring carries the table. R3 makes reporting `F_strict` a
condition of the reading, not a courtesy.

Neither ruling changes a number, and neither changed a score in this file. They
record the authority for what it already did.

## The anti-gaming checks run today, and forever

Two trials here need no engine and are green from this session on:

  * **keep-latest cannot clear the gate on `l3streamb`.** The cheapest
    order-based policy — a ring buffer with no importance reasoning at all — is
    simulated as a **trial fixture** (never engine code) and must score below the
    gate. On `l3stream`, by contrast, that same policy scores the *optimum*,
    which is precisely why `l3streamb` was built.
  * **the attainable ceilings are as recorded.** Per stream, the mass of the
    budget-worth of heaviest items bounds `weighted-C` over *all* retain-or-drop
    policies. On `l3streamb` that bound clears the gate; on `l3stream` it does
    not, and that finding — with its numbers and its objection — is
    `ATTAINABILITY.md`.

The `l3stream` gate trial is therefore skipped **conditionally on the
arithmetic**: it computes the ceiling and skips only while the ceiling lies below
the gate, so it engages by itself if the corpus family ever changes.
"""

from _harness import require, require_equal, skip, try_import
import _l3score
import _l3tasks

GATE_WEIGHTED_C = 850
GATE_UNWEIGHTED_C = 90
GATE_F = 950
GATE_B = 1000

LAYER_CAP = 3


def _engine():
    return try_import("adapters.l3",
                      "no L3 engine yet; forgetting ascension engages when built")


def _run_gate(name):
    """Replay one stream under layer_cap=3 and assert the ratified gate."""
    ceiling = _l3tasks.attainable_weighted_c_permille(name)
    if ceiling < GATE_WEIGHTED_C:
        skip("%s: ungated diagnostic (BOUNDARY-RULINGS.md R1) — the gate is "
             "unreachable here by ANY retain-or-drop policy: the budget-worth of "
             "heaviest items holds %d‰ of the mass against a %d‰ gate "
             "(ATTAINABILITY.md), so R1 binds the gate on l3streamb and leaves "
             "this stream scored but ungated. The skip is conditional on that "
             "arithmetic and lifts by itself if the ceiling ever reaches the gate."
             % (name, ceiling, GATE_WEIGHTED_C))

    l3 = _engine()
    bundle = _l3tasks.stream(name)
    state, budget = _l3score.replay(
        l3, lambda cap: l3.make_engine(LAYER_CAP, cap), name)
    r = _l3score.score(l3, state, name)

    require(budget["B"] >= GATE_B,
            "%s: B=%d below the L3 gate B=%d — peak occupancy %d exceeded the cap %d"
            % (name, budget["B"], GATE_B, budget["peak"], budget["cap"]))
    require(r["weighted_C"] >= GATE_WEIGHTED_C,
            "%s: weighted-C=%d below the L3 gate weighted-C>=%d (recovered mass "
            "%d/%d; the attainable ceiling on this stream is %d)"
            % (name, r["weighted_C"], GATE_WEIGHTED_C, r["recovered_mass"],
               r["total_mass"], ceiling))
    require(r["unweighted_C"] >= GATE_UNWEIGHTED_C,
            "%s: unweighted-C=%d below the L3 gate unweighted-C>=%d — only %d/%d "
            "items recovered, so less than a full budget's worth was kept"
            % (name, r["unweighted_C"], GATE_UNWEIGHTED_C, r["recovered"], r["n_targets"]))
    require(r["F"] >= GATE_F,
            "%s: F=%d below the L3 gate F>=%d (wrong=%d, fabricated=%d) — "
            "forgetting corrupted what it kept" % (name, r["F"], GATE_F,
                                                   r["wrong"], r["fabricated"]))
    # A wrong recall is worse than none (§3.0): what survives must be exact, and
    # a cue for something never ingested must never be answered.
    require_equal(r["wrong"], 0, "%s: recall returned wrong content for a retained item" % (name,))
    require_equal(r["fabricated"], 0, "%s: recall fabricated on a never-ingested cue" % (name,))
    return r


# ---- the gate, per stream (engine-gated) -----------------------------------

def trial_forgetting_meets_the_layer3_gate_on_l3streamb():
    # THE binding gate (BOUNDARY-RULINGS.md R1). The anti-recency-proxy stream:
    # importance decorrelated from position, so clearing the gate here requires
    # ranking by importance and nothing else can substitute for it.
    _run_gate("l3streamb")


def trial_forgetting_meets_the_layer3_gate_on_l3stream():
    # The monotone stream, ungated under R1. Skips while its attainable ceiling
    # (190‰) lies below the 850‰ gate — see ATTAINABILITY.md for the measurement
    # and R1 for the ruling that resolved it.
    _run_gate("l3stream")


def trial_forgetting_budget_holds_throughout_both_streams():
    # B = 1000 is the whole state — hot, cold, index, tombstones — asserted after
    # every write by `_l3score.replay`, on both streams, whatever the gate says
    # about coverage. This engages on the engine alone and does not wait on the
    # attainability ruling.
    l3 = _engine()
    for name in _l3tasks.STREAMS:
        _state, budget = _l3score.replay(
            l3, lambda cap: l3.make_engine(LAYER_CAP, cap), name)
        require(budget["B"] >= GATE_B,
                "%s: B=%d — peak occupancy %d exceeded the cap %d somewhere in "
                "the stream" % (name, budget["B"], budget["peak"], budget["cap"]))


# ---- the anti-gaming checks (no engine; green from this session on) --------

def trial_keep_latest_baseline_cannot_clear_the_gate_on_l3streamb():
    """A ring buffer must not clear the gate — checked forever, not just today.

    Implemented as a trial fixture (`_l3score.keep_latest_baseline`), never as
    engine code: the policy this guards against must not exist in `core/`.
    """
    r = _l3score.keep_latest_baseline("l3streamb")
    require(r["weighted_C"] < GATE_WEIGHTED_C,
            "keep-latest scored weighted-C=%d on l3streamb, at or above the %d‰ "
            "gate — the gate would not require importance ranking"
            % (r["weighted_C"], GATE_WEIGHTED_C))
    # And it is not merely below the gate, it is pinned near a tenth of the mass
    # by the window bound — the property that makes the guard structural.
    require(r["weighted_C"] <= 110,
            "keep-latest scored weighted-C=%d on l3streamb, above the 110‰ window "
            "bound — the stream's interleaving has drifted" % (r["weighted_C"],))
    # Its unweighted coverage is a full budget's worth: it fails on *importance*,
    # not on capacity. Without this, "it kept less" would explain the low score.
    require(r["unweighted_C"] >= GATE_UNWEIGHTED_C,
            "keep-latest kept only unweighted-C=%d — the baseline must hold a "
            "full budget's worth so its failure is about importance alone"
            % (r["unweighted_C"],))


def trial_keep_latest_is_the_optimum_on_the_monotone_stream():
    """The rationale for `l3streamb`, asserted rather than asserted-in-prose.

    On `l3stream` recency is a perfect proxy for importance: the ring buffer ties
    the arithmetic optimum. That is what a single monotone corpus cannot
    distinguish, and why the anti-recency-proxy stream exists.
    """
    r = _l3score.keep_latest_baseline("l3stream")
    ceiling = _l3tasks.attainable_weighted_c_permille("l3stream")
    require_equal(r["weighted_C"], ceiling,
                  "keep-latest no longer ties the optimum on l3stream — the "
                  "recency-as-importance-proxy rationale for l3streamb has changed")


def trial_attainable_ceilings_are_as_recorded():
    """Per stream, the ceiling on weighted-C over ALL retain-or-drop policies.

    Recorded in ATTAINABILITY.md. Machine-checked here so the finding cannot
    drift silently: `l3streamb` admits the gate, `l3stream` does not.
    """
    require_equal(_l3tasks.attainable_weighted_c_permille("l3streamb"), 918,
                  "l3streamb's attainable weighted-C drifted from ATTAINABILITY.md")
    require_equal(_l3tasks.attainable_weighted_c_permille("l3stream"), 190,
                  "l3stream's attainable weighted-C drifted from ATTAINABILITY.md")
    require(_l3tasks.attainable_weighted_c_permille("l3streamb") >= GATE_WEIGHTED_C,
            "l3streamb no longer admits the L3 gate — the ascension has no "
            "satisfiable corpus left")
    require(_l3tasks.attainable_weighted_c_permille("l3stream") < GATE_WEIGHTED_C,
            "l3stream now admits the L3 gate — the ATTAINABILITY.md objection is "
            "resolved and its ascension trial must be un-skipped")


def trial_budget_is_one_thousand_items_worth_on_both_streams():
    """The budget formula, asserted so it cannot be quietly loosened.

    `budget_cap = budget_items × event_cost(payload)` under the frozen §4.1 cost
    model — no headroom for an index, a cold tier, or a tombstone table. An
    engine pays for its own bookkeeping out of the same thousand items.
    """
    for name in _l3tasks.STREAMS:
        bundle = _l3tasks.stream(name)
        require_equal(bundle["budget_items"], 1000, "%s: item budget is not 1000" % (name,))
        require_equal(bundle["item_cost"], 11,
                      "%s: per-item retention cost drifted from the frozen cost model" % (name,))
        require_equal(bundle["budget_cap"], 11000, "%s: budget cap drifted" % (name,))
        require_equal(len(bundle["targets"]), 10 * bundle["budget_items"],
                      "%s: the stream is not 10× the budget" % (name,))

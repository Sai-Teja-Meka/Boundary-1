"""ascension/l5 — the Layer-5 attainability arithmetic, machine-checked.

`BOUNDARY-RULINGS.md R2` obligation 3 requires the oracle ceiling and every named
baseline to be *"computed and written into that layer's `ATTAINABILITY.md`, and
machine-checked by a trial that goes red if any recorded number drifts, BEFORE the
gate is treated as binding."* This is that trial.

**It applies no gate to any engine.** `core/layers/l5_prospection.py` does not
exist and `trials/humility/l5/` does not exist. The `§5 L5` constants below are
named so that this file can ask *whether the corpus admits them* (R2 obligations 1
and 2), which is the only thing Stage A is for; `trials/laws/t_rulings.py` binds
each of them to its `§5 L5` clause.

What is asserted here, and why each assertion exists:

1. **The exhibited witness attains the identity.** R4 clause 5 made an exhibited
   ceiling preferred practice wherever a witness can be built. One can be built
   here, so the ceiling is a schedule that exists rather than a bound over a
   declared family — and for the four identity clauses the ceiling is a *logical*
   maximum over every policy whatsoever, which the Layer-3 Form-B pass-through
   could not have been.
2. **The witness fits, priced under rule P**, with the operational bookkeeping and
   the loss-accounting reserve counted rather than disclaimed — the two lessons
   `BOUNDARY.log` lines 23 and 26 paid for at Layer 4.
3. **Every named baseline is scored**, and the two obligations are stated as they
   actually come out: obligation 2 holds over the conjunction and ties on the two
   minimizing clauses; obligation 1 fails a strict reading on five of six clauses
   and is discharged, if at all, by the attainment in (1). Both are asserted as
   findings so that a later session cannot quietly restate them.
4. **The engine-`t` drift** — one caller ingest advancing `next_t` by more than
   one — as a number rather than a warning.
"""

from fractions import Fraction

import _l5tasks
from _harness import require, require_equal
from corpora.l5stream import generator as l5gen

# The ratified §5 L5 gate. Named here to ask whether the corpus admits it
# (R2 obligations 1 and 2). No engine is measured against any of them.
GATE_TRIGGER_PRECISION = 1000
GATE_TRIGGER_RECALL = 1000
GATE_DUP_FIRE = 0
GATE_MISS = 0
GATE_F = 980
GATE_B = 1000
CEILING_TRIGGER_RECALL = 50      # §5 L5 humility ceiling

# The recorded numbers of ATTAINABILITY.md, in one place so a drift is one red.
RECORDED = {
    "raw_cells": 182555,
    "budget_cap": 45638,
    "battery": 1710,
    "w1_total": 4505,
    "w2_total": 41951,
    "w2_margin": 3687,
    "w2_footprint_permille": 230,
    "joint_peak_prospection": 4448,
    "bookkeeping_total": 633,
    "loss_reserve": 35,
    "engine_next_t": 20765,
    "last_fire_t": 20760,
    "f_slack_wrong": 35,
    "f_slack_abstain": 38,
}


# ---- 1. the exhibited witness attains the identity -------------------------

def trial_the_exhibited_witness_attains_the_identity():
    """The schedule of ATTAINABILITY.md §4, scored. The ceiling is a state, not a bound.

    R2 obligation 1 asks for the best score any policy the layer's capability
    permits can reach. For four of the six `§5 L5` clauses that is a logical
    maximum — precision and recall are ratios of a subset to its superset,
    `dup-fire` and `miss` are cardinalities — so no declared policy family is
    needed and none is declared. What IS needed is a policy that reaches it, and
    this is that policy: fire each intention exactly at its satisfaction point, in
    `iid` order where several fall at one caller index.
    """
    o = _l5tasks.oracle()
    b = _l5tasks.corpus()

    require_equal(o["precision"], GATE_TRIGGER_PRECISION,
                  "the exhibited witness no longer attains trigger-precision 1000")
    require_equal(o["recall"], GATE_TRIGGER_RECALL,
                  "the exhibited witness no longer attains trigger-recall 1000")
    require_equal(o["dup_fire"], GATE_DUP_FIRE,
                  "the exhibited witness fires an intention twice")
    require_equal(o["miss"], GATE_MISS,
                  "the exhibited witness misses a fireable intention")
    require_equal(o["F"], 1000,
                  "the exhibited witness no longer answers the whole P1/P2 battery")
    require(o["F"] > GATE_F,
            "the F oracle ceiling (%d) is no longer strictly above the ratified "
            "gate (%d) — F is the ONE clause of §5 L5 that discharges R2 "
            "obligation 1 by the Layer-3/Layer-4 method, and if it stops doing so "
            "the whole clause is in the identity case" % (o["F"], GATE_F))

    require_equal(o["fires"], len(b["fireable"]),
                  "the witness fires a number of times other than once per "
                  "fireable intention")
    require_equal(len(b["intents"]), l5gen.DECLARED_INTENTIONS,
                  "the intention count drifted")
    require_equal(len(b["never"]), l5gen.DECLARED_NEVER_FIRES,
                  "the never-fires tier drifted — it is what makes `abstain when "
                  "nothing satisfies it` a scored behaviour rather than an "
                  "untested claim")


def trial_the_battery_and_its_f_slack_are_as_recorded():
    """`F >= 980` on a battery of 1 710 is a threshold with a stateable margin."""
    b = _l5tasks.corpus()
    n = b["n_p1"] + b["n_p2"]
    require_equal(n, RECORDED["battery"], "the P1+P2 battery size drifted")
    require_equal(b["n_p1"], len(b["intents"]), "P1 is not one query per intention")
    require_equal(b["n_p2"], len(b["fireable"]),
                  "P2 is not one query per fired event")

    # §3.5 round-half-to-even admits an exact F as low as 979.5 permille.
    worst_wrong = max(w for w in range(n)
                      if _l5tasks.permille(Fraction(1000 * (n - w), n * 1000)) >= GATE_F)
    worst_abstain = max(a for a in range(n)
                        if _l5tasks.permille(
                            Fraction(1000 * (n - a) + 100 * a, n * 1000)) >= GATE_F)
    require_equal(worst_wrong, RECORDED["f_slack_wrong"],
                  "the number of wrong answers F>=980 admits drifted")
    require_equal(worst_abstain, RECORDED["f_slack_abstain"],
                  "the number of abstentions-on-answerable-queries F>=980 admits "
                  "drifted")


# ---- 2. the witness fits, priced under rule P ------------------------------

def trial_the_witness_fits_the_budget_priced_under_rule_p():
    b = _l5tasks.corpus()
    w1 = _l5tasks.witness_minimal()
    w2 = _l5tasks.witness_full()

    require_equal(b["raw_cells"], RECORDED["raw_cells"],
                  "l5stream's raw episodic footprint drifted — every permille "
                  "recorded in ATTAINABILITY.md is a ratio against it")
    require_equal(b["budget_cap"], RECORDED["budget_cap"],
                  "the declared budget cap drifted (raw_cells // 4, the Layer-4 "
                  "footprint ratio carried forward — §5 L5 declares no ratio of "
                  "its own)")
    require_equal(w1["total_peak"], RECORDED["w1_total"],
                  "W1, the prospection-only witness, drifted")
    require_equal(w2["total"], RECORDED["w2_total"], "W2's price drifted")
    require_equal(w2["margin"], RECORDED["w2_margin"],
                  "W2's margin drifted — this is the number a Stage-C engine "
                  "inherits, and the Layer-4 analogue was 2 563 cells of which "
                  "656 turned out to be already spent")
    require_equal(w2["footprint_permille"], RECORDED["w2_footprint_permille"],
                  "W2's footprint drifted")
    require(w2["total"] <= b["budget_cap"],
            "W2 no longer fits the declared cap: %d cells against %d — the "
            "identity would then be attainable only outside the budget law, and "
            "`B = 1000` would void the witness"
            % (w2["total"], b["budget_cap"]))
    require(w1["total_peak"] < w2["total"],
            "W1 is no longer strictly cheaper than W2 — the whole point of "
            "exhibiting both is that §5 L5's gate read literally is satisfied by "
            "a state that has forgotten the world and kept its intentions")


def trial_both_layer4_lessons_are_priced_rather_than_disclaimed():
    """The 656 unpriced cells (BOUNDARY.log line 23) and the loss reserve (line 26).

    Layer 4's Stage A declared a 2 563-cell margin and Stage C then found 656 cells
    of operational bookkeeping inside it. The same four items are carried here by
    name, priced from THIS corpus's shape; and the aggregated forgetting record is
    reserved because W2 genuinely releases content it cannot regenerate, so the
    reserve has a reachable path rather than being a ritual.
    """
    book = _l5tasks.operational_bookkeeping_cells()
    require_equal(sorted(book),
                  ["demotion_counter", "key_atlas", "per_entity_irreducible_counts"],
                  "an operational bookkeeping item disappeared from the pricing — "
                  "the Layer-4 lesson is that the items nobody prices are the "
                  "ones that eat the margin")
    require_equal(sum(book.values()), RECORDED["bookkeeping_total"],
                  "the operational bookkeeping price drifted")
    require_equal(book["per_entity_irreducible_counts"], 3 * l5gen.ENTITIES,
                  "the per-entity irreducible counts are not 3 per entity — the "
                  "part of a Layer-4 action profile no fold can reach")
    require_equal(_l5tasks.LOSS_RESERVE_CELLS, RECORDED["loss_reserve"],
                  "the loss-accounting reserve drifted from the Layer-3 "
                  "aggregated forgetting record's bound (3 + 2 × 16 buckets)")

    # The reserve is reachable, not decorative: W2 holds no episode for any note
    # and none for a fired intention, so content IS released.
    b = _l5tasks.corpus()
    released = l5gen.DECLARED_NOTES + len(b["fireable"])
    require(released > 0,
            "W2 releases nothing, so the loss-accounting reserve would be a "
            "ritual rather than a reserve and should be disclaimed with reasons "
            "instead of priced")


def trial_the_prospection_price_is_a_bound_and_the_bound_is_stated():
    """4 493 is peak-pending plus FINAL fired rows: two maxima, not one moment.

    The bound is what a budget must respect. The measurement is what actually
    happens. Recording only the first would overstate the cost; recording only the
    second would understate what a lawful engine must reserve. Both, and the gap.
    """
    w1 = _l5tasks.witness_minimal()
    bound = w1["pending_peak_cells"] + w1["fired_rows"] + w1["shapes"]
    joint = _l5tasks.joint_peak_prospection_cells()
    require_equal(joint, RECORDED["joint_peak_prospection"],
                  "the true joint high-water mark of the prospection state drifted")
    require(joint <= bound,
            "the measured joint peak (%d) exceeds the bound ATTAINABILITY.md "
            "prices (%d) — the bound is no longer a bound" % (joint, bound))
    require_equal(bound - joint, 45,
                  "the gap between the priced bound and the measured peak drifted")


# ---- 3. the two R2 obligations, as they actually come out ------------------

def trial_every_named_baseline_is_scored_and_is_far_below_the_gate():
    got = _l5tasks.baselines()
    expected = {
        "capped-4 (no trigger machinery)":
            {"precision": None, "recall": 0, "dup_fire": 0, "miss": 765, "F": 271},
        "fire-on-every-write":
            {"precision": 0, "recall": 0, "dup_fire": 9183176, "miss": 0, "F": 0},
        "fire-immediately":
            {"precision": 116, "recall": 144, "dup_fire": 0, "miss": 0, "F": 116},
        "fire-on-kind-atom-only":
            {"precision": 375, "recall": 379, "dup_fire": 0, "miss": 77, "F": 397},
    }
    require_equal(sorted(got), sorted(expected),
                  "the named baseline set drifted — R2 obligation 2 says an "
                  "unnamed baseline is an unchecked one")
    for name, want in sorted(expected.items()):
        for field, value in sorted(want.items()):
            require_equal(got[name][field], value,
                          "baseline %r drifted on %s" % (name, field))

    # The three MAXIMIZING clauses: strictly above every baseline. ✔
    for name, row in sorted(got.items()):
        require(row["recall"] < GATE_TRIGGER_RECALL,
                "baseline %r reaches trigger-recall %d against a gate of %d"
                % (name, row["recall"], GATE_TRIGGER_RECALL))
        require(row["F"] < GATE_F,
                "baseline %r reaches F %d against a gate of %d"
                % (name, row["F"], GATE_F))
        if row["precision"] is not None:
            require(row["precision"] < GATE_TRIGGER_PRECISION,
                    "baseline %r reaches trigger-precision %d against a gate of %d"
                    % (name, row["precision"], GATE_TRIGGER_PRECISION))


def trial_the_cheap_trick_is_killed_by_the_identity_and_not_by_the_corpus():
    """fire-on-every-write: perfect recall under the charitable reading, and dead.

    The ASCEND directive predicted this policy would reach recall 1000 with
    precision far below, and it does — but only once the exactly-once requirement
    is dropped, which is exactly the point. The `_any` pair is a diagnostic and
    never a gate; it exists so the arithmetic can show WHICH clause of the identity
    does the killing.
    """
    row = _l5tasks.baseline_fire_on_every_write()
    require_equal(row["recall_any"], 1000,
                  "the fire-on-every-write baseline no longer has perfect recall "
                  "under the charitable reading — it is supposed to be the policy "
                  "that cannot miss")
    require_equal(row["precision_any"], 0,
                  "the fire-on-every-write baseline's charitable precision drifted")
    require_equal(row["recall"], 0,
                  "under the ratified exactly-once reading not one of this "
                  "policy's firings may count as correct")
    require(row["dup_fire"] > 9000000,
            "the fire-on-every-write baseline's dup-fire count collapsed — the "
            "clause that kills it is `dup-fire = 0`")
    require_equal(row["fires"] - row["distinct"], row["dup_fire"],
                  "dup-fire is not fires minus distinct intentions fired")


def trial_the_analytic_cheap_trick_agrees_with_a_built_one():
    """One policy, two implementations — the discipline `_l4tasks` set at Layer 4.

    9.18 million firing records are not materialized in the suite; the baseline is
    arithmetic. A brute-force construction over a declared prefix checks that the
    arithmetic is the same policy.
    """
    m = 2000
    b = _l5tasks.corpus()
    fires = _l5tasks.brute_fire_on_every_write(m)
    built = len(fires)
    analytic = sum(m - 1 - rec["k0"] for rec in b["intents"].values()
                   if rec["k0"] < m)
    require_equal(built, analytic,
                  "the analytic form of fire-on-every-write disagrees with the "
                  "policy built by construction over the first %d caller events "
                  "(%d vs %d)" % (m, built, analytic))
    require(built > 0, "the prefix is too short to exercise the policy at all")


def trial_r2_obligation_1_is_not_dischargeable_by_a_strict_reading():
    """The collision, asserted as a finding so it cannot be quietly restated.

    Four of the six `§5 L5` clauses are identities over discrete correctness and a
    fifth (`B`) has been one since Layer 1. R2 obligation 1 demands the gate lie
    STRICTLY below the oracle ceiling. It does not, and no corpus repairs that:
    the ceiling IS the identity, by arithmetic, everywhere.

    What holds instead is the thing R2's rationale actually names — the gate is not
    void, because a policy that reaches it exists and is exhibited above. This
    trial pins both halves: the strict reading fails, and the mischief is absent.
    """
    o = _l5tasks.oracle()

    require_equal(o["precision"], GATE_TRIGGER_PRECISION,
                  "the oracle ceiling for trigger-precision is not the gate")
    require_equal(o["recall"], GATE_TRIGGER_RECALL,
                  "the oracle ceiling for trigger-recall is not the gate")
    require_equal(o["dup_fire"], GATE_DUP_FIRE,
                  "the oracle floor for dup-fire is not the gate")
    require_equal(o["miss"], GATE_MISS, "the oracle floor for miss is not the gate")
    require(not (GATE_TRIGGER_PRECISION < o["precision"]),
            "trigger-precision now lies strictly below its oracle ceiling — if "
            "that ever becomes true the Layer-5 collision has dissolved and "
            "RULING-R5-DRAFT.md clause 1 is no longer needed")
    require(GATE_F < o["F"],
            "F no longer discharges R2 obligation 1 by the ordinary method — it "
            "is the one clause of §5 L5 that does, and ATTAINABILITY.md §5 rests "
            "on the contrast")


def trial_r2_obligation_2_ties_on_the_minimizing_clauses_and_holds_on_the_conjunction():
    """The second half of the collision: `dup-fire = 0` and `miss = 0` are tied.

    R2's *"strictly above"* is written for measures where higher is better. Read
    literally against a minimizing clause it would require a baseline with a
    negative count. Read over the gate as a whole — the conjunction `§5` states —
    it is discharged with an enormous margin, and this trial asserts BOTH: that
    some baseline ties each minimizing clause, and that none clears more than
    three of the six.
    """
    got = _l5tasks.baselines()

    ties_dup = [n for n, r in got.items() if r["dup_fire"] == GATE_DUP_FIRE]
    ties_miss = [n for n, r in got.items() if r["miss"] == GATE_MISS]
    require(ties_dup,
            "no named baseline ties `dup-fire = 0` any more — the clause-wise "
            "reading of R2 obligation 2 would then be dischargeable at Layer 5 "
            "and RULING-R5-DRAFT.md clause 2 would be unnecessary")
    require(ties_miss, "no named baseline ties `miss = 0` any more")

    for name, r in sorted(got.items()):
        cleared = sum((
            r["precision"] == GATE_TRIGGER_PRECISION,
            r["recall"] == GATE_TRIGGER_RECALL,
            r["dup_fire"] == GATE_DUP_FIRE,
            r["miss"] == GATE_MISS,
            r["F"] >= GATE_F,
        ))
        require(cleared <= 3,
                "baseline %r clears %d of the 5 scored clauses — the conjunction "
                "is what discriminates at Layer 5, and if a capability-free "
                "policy ever cleared four of them the corpus binding would have "
                "to be reopened" % (name, cleared))


def trial_the_humility_ceiling_is_not_breached_and_the_reason_is_structural():
    """`capped trigger-recall <= 50`, measured 0. README-l4 §4 predicted the value.

    Stated here rather than in a humility trial because `trials/humility/l5/` does
    not exist yet: Stage A computes what the corpus admits, and the capped policy
    is a policy the corpus admits like any other.
    """
    row = _l5tasks.baseline_never_fire()
    require_equal(row["recall"], 0,
                  "the capped-4 policy's trigger-recall is no longer 0 — "
                  "README-l4 §4 says it should be 0 and not merely near 0, "
                  "because with no pending set the numerator is empty by "
                  "construction rather than by difficulty")
    require(row["recall"] <= CEILING_TRIGGER_RECALL,
            "the capped-4 policy breaches the §5 L5 humility ceiling")
    require(row["precision"] is None,
            "the capped-4 policy was given a defined trigger-precision — scoring "
            "an empty firing set as perfect would hand a `precision = 1000` "
            "clause to the policy that does nothing (§3.4's `n/a` convention for "
            "AUROC with an empty class)")
    require_equal(row["F"], 271,
                  "the capped-4 policy's F drifted — it abstains on all 945 P1 "
                  "queries, which §3.0 scores 100 on the 765 answerable ones and "
                  "1000 on the 180 unanswerable ones")


# ---- 4. the engine-`t` drift, as a number ----------------------------------

def trial_one_caller_ingest_can_advance_next_t_by_more_than_one():
    """The `[L4] [PULSE]` session's second-ranked Layer-5 risk, measured.

    A fired event is an event and `§1.3` gives it a `t` of its own, so on a stream
    carrying intentions the one-ingest-one-`t` identity that every anchor and the
    whole `inheritance/` class assume stops holding. Stage A cannot fix that — it
    is a Stage-B and Stage-C obligation — but it can stop it being a surprise.
    """
    b = _l5tasks.corpus()
    n_fires = len(b["fireable"])
    require_equal(b["n"] + n_fires, RECORDED["engine_next_t"],
                  "the engine's final `next_t` over l5stream drifted")
    require_equal(max(b["fire_t"].values()), RECORDED["last_fire_t"],
                  "the logical `t` of the last firing drifted")
    require(b["caller_t"][b["n"] - 1] > b["n"] - 1,
            "the last caller event's engine `t` is still its caller index — the "
            "drift this trial exists to record has vanished, which would mean no "
            "intention in the stream ever fires")

    # Every t is used exactly once, and firings interleave rather than trailing.
    used = sorted(list(b["caller_t"].values()) + list(b["fire_t"].values()))
    require_equal(used, list(range(b["n"] + n_fires)),
                  "the caller events and the firings do not partition the logical "
                  "times 0..next_t-1 — `t` is unique and strictly increasing in "
                  "ingestion order (§1.3), and a firing is ingested where it fires")

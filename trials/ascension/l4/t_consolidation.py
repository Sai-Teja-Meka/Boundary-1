"""ascension/l4 — Layer 4 (Consolidation) capability trials (BOUNDARY.md §5 L4).

The Stage-B battery. It applies the ratified Layer-4 gate

    footprint ≤ 250,  reconstruction F ≥ 900,  C ≥ 850,  B = 1000

to an engine, on the corpus **BOUNDARY-RULINGS.md R4 clause 1 binds it to** —
`corpora/l4stream` — with `chronicle` and `murk` scored as ungated diagnostics
on R1 clause 5's conditional arithmetic-skip. Every trial here is
**engine-gated**: they report `SKIPPED-BY-DESIGN` until
`core/layers/l4_consolidation.py` and `trials/adapters/l4.py` exist, and then
they must clear the gate. That is the standing checkpoint shape of an ASCEND
split at the trials/engine boundary — humility green, ascension skipped — and it
is R2's standing step in force: attainability arithmetic → trials → engine.

## What this file does NOT do, deliberately

Stage A already **exhibited** the oracle ceiling and scored every named
capability-free baseline, and `t_attainability.py` asserts all of it on every
run. None of that is repeated here. One fixture, one truth:

  * the exhibited witness state (43 299 cells, C = 1000, F = 984) and its
    strictly-below-the-oracle check —
    `t_attainability.py::trial_l4stream_admits_the_gate_with_an_exhibited_state`;
  * every named baseline strictly below the gate (verbatim truncation 247/325
    and 249/327, current-value-table-only 155/100, capped `layer_cap = 3`
    200/325) —
    `t_attainability.py::trial_no_capability_free_baseline_clears_the_gate_on_l4stream`
    and `::trial_recorded_baseline_scores_do_not_drift`;
  * the humility ceiling's honesty from the arithmetic side —
    `t_attainability.py::trial_the_capped_engine_ceiling_is_honest_on_l4stream`;
  * the `F ≥ 900 ⟺ 8/9 exact` identity and the half-permille §3.5 concession —
    `t_attainability.py::trial_the_reconstruction_gate_is_the_literal_section_3_0_table`.

The gate constants below are the same ratified numbers those trials name, and
`laws/t_rulings.py` binds **both** files' copies to §5 L4 and R4, so they cannot
drift apart silently — a duplicated *number* under one registry is what that
registry exists for, unlike a duplicated *fixture*, which is what this file
refuses to be.

## The measures, at Layer 4

`_l4score` carries the replay and the scoring; `_l4tasks` carries the battery
and its denominators, frozen at Stage A and cited by R4. Four things are worth
restating here because they are where a Layer-4 gate could be quietly loosened:

  * **`F` is the literal §3.0 table.** R3 excludes Layer 4 in its own text and
    **R4 clause 4 declined to extend it** — the concession was available,
    examined and refused because the exhibited witness clears the gate without
    it. So an honest abstention on an answerable reconstruction scores 100 here.
    `F_corruption` is computed and reported, never gated: R3's pairing inverted,
    the stricter number binding. **No slack exists to take.**
  * **`B = 1000` is asserted after every write**, not at the end. Under R4
    clause 2 the budget cap and the footprint gate are one number
    (`raw_cells // 4`), so a state that would exceed the footprint is refused
    mid-stream by the budget law rather than discovered late by a measure.
  * **The footprint is priced under rule P** (R4 clause 3, one cell one grammar
    atom). The half of rule P a trial can see from outside an engine — that the
    engine's own serialized state carries no more atoms than it charged itself
    for — is asserted here; the packing half is structural and is the engine's
    obligation, which is recorded rather than assumed.
  * **Nothing is answered that cannot be answered.** `wrong = 0` on
    reconstruction and `fabricated = 0` on the unanswerable probes: at Layer 4
    the temptation is to *derive* an answer where the schema has none, and §3.0
    prices that at 0, exactly as it prices a fabricated recall.
"""

from _harness import require, require_equal, skip, try_import
import _l4score
import _l4tasks

# The ratified §5 L4 thresholds, unchanged, bound to `corpora/l4stream` by
# BOUNDARY-RULINGS.md R4 clause 1. Registered in `laws/t_rulings.py` against the
# §5 L4 clauses they are quoted from and against R4; see `AUTHORIZED_GATES`.
GATE_FOOTPRINT = 250
GATE_RECONSTRUCTION_F = 900
GATE_C = 850
GATE_B = 1000

LAYER_CAP = 4

BINDING_CORPUS = "l4stream"
DIAGNOSTIC_CORPORA = ("chronicle", "murk")

_RUNS = {}


def _engine():
    return try_import(
        "adapters.l4",
        "no L4 engine yet; consolidation ascension engages when built "
        "(Stage C — R2's standing step: arithmetic → trials → engine)")


def _run(engine, name):
    """Replay and score one corpus at the Layer-4 cap, once per suite run."""
    key = (id(engine), name)
    if key not in _RUNS:
        bundle = _l4tasks.corpus(name)
        state, budget = _l4score.replay(
            engine, lambda cap: engine.make_engine(LAYER_CAP, cap), bundle)
        _RUNS[key] = (state, budget, _l4score.score(engine, state, bundle),
                      bundle)
    return _RUNS[key]


# ---- the gate (engine-gated) ------------------------------------------------

def trial_consolidation_meets_the_layer4_gate_on_l4stream():
    """THE binding gate (BOUNDARY-RULINGS.md R4 clause 1).

    `l4stream` is the corpus on which the gate discriminates on both sides: the
    upper side is exhibited (1000 / 984 against 850 / 900) and every named
    capability-free policy sits strictly below it, the history-free
    current-value table pinned at 155 against a 1000 ceiling — 16%, where on
    chronicle the same policy reaches 95% of that corpus's own optimum.
    """
    l4 = _engine()
    _state, budget, r, _b = _run(l4, BINDING_CORPUS)

    require(r["footprint"] <= GATE_FOOTPRINT,
            "footprint=%d‰ above the L4 gate ≤%d‰ (%d cells of a %d-cell raw "
            "episodic footprint) — the derived schemas did not compress 4×"
            % (r["footprint"], GATE_FOOTPRINT, r["occupancy"], r["raw_cells"]))
    require(r["C"] >= GATE_C,
            "C=%d below the L4 gate C≥%d (recovered %d/%d: Q1 %d/%d, Q2 %d/%d, "
            "Q3 %d/%d) — the derived schemas answer less than the semantic "
            "battery demands"
            % (r["C"], GATE_C, r["recovered"], r["n_coverage"],
               r["q1"], r["n_q1"], r["q2"], r["n_q2"], r["q3"], r["n_q3"]))
    require(r["F"] >= GATE_RECONSTRUCTION_F,
            "reconstruction F=%d below the L4 gate F≥%d under the LITERAL §3.0 "
            "table (%d/%d reconstructed exactly, %d abstained, %d wrong; "
            "F_corruption=%d is the ungated diagnostic and is NOT the gate — "
            "R4 clause 4 declined that concession and no slack exists to take)"
            % (r["F"], GATE_RECONSTRUCTION_F, r["reconstructed"], r["n_q4"],
               r["reconstruction_abstained"], r["reconstruction_wrong"],
               r["F_corruption"]))
    require(budget["B"] >= GATE_B,
            "B=%d below the L4 gate B=%d — peak occupancy %d exceeded the cap %d"
            % (budget["B"], GATE_B, budget["peak"], budget["cap"]))


def trial_consolidation_budget_holds_throughout_the_stream():
    """`B = 1000` after every write, which under R4 clause 2 is the footprint too.

    Separate from the gate trial so a mid-stream budget breach and a coverage
    shortfall are never confused for one another: `_l4score.replay` raises at the
    write that breaches, naming it, rather than reporting a final number that
    happens to have recovered.
    """
    l4 = _engine()
    for name in (BINDING_CORPUS,) + DIAGNOSTIC_CORPORA:
        _state, budget, _r, bundle = _run(l4, name)
        require(budget["B"] >= GATE_B,
                "%s: B=%d — peak occupancy %d exceeded the cap %d somewhere in "
                "the stream" % (name, budget["B"], budget["peak"], budget["cap"]))
        require_equal(budget["cap"], bundle["raw_cells"] // 4,
                      "%s: the Layer-4 cap is no longer a quarter of the raw "
                      "episodic footprint (R4 clause 2)" % (name,))


def trial_consolidation_state_is_priced_under_rule_p():
    """R4 clause 3, the half of pricing rule P a trial can see from outside.

    An engine's occupancy is its own accounting. This checks it against the
    engine's own **snapshot**: the atoms in the serialized state, priced by the
    frozen §4.1 model, must not exceed what the engine charged itself (plus a
    fixed allowance for the snapshot header, which is bookkeeping about the
    state rather than stored grammar).

    What it cannot see is the packing half — a composite scalar is one atom to
    `payload_cost` and several to rule P — which R4 rules **structural** and
    leaves to the engine. Recorded here rather than silently assumed, because a
    footprint measure that could be driven to 1 by encoding would make every
    number in `ATTAINABILITY.md` a wish.
    """
    l4 = _engine()
    state, _budget, r, _b = _run(l4, BINDING_CORPUS)
    atoms = _l4score.snapshot_atoms(l4, state)
    require(atoms <= r["occupancy"] + _l4score.RULE_P_HEADER_ALLOWANCE,
            "the snapshot carries %d grammar atoms but the engine charged "
            "itself %d cells — the state is under-priced against rule P (R4 "
            "clause 3), so its footprint of %d‰ is not the footprint the gate "
            "measures" % (atoms, r["occupancy"], r["footprint"]))


def trial_consolidation_never_corrupts_and_never_fabricates():
    """§3.0's two zeros, which a *deriving* engine is the first to be tempted by.

    Layer 3 could only return what it retained; Layer 4 derives, and a derived
    answer for a pair the corpus never asserted — or for an as-of before a
    pair's first assertion — is a fabrication in the exact §3.0 sense, scored 0
    however plausible it looks. Likewise a reconstruction that returns a
    different event is corruption, not lossy compression: the honest form of not
    knowing is to abstain (§7.3).
    """
    l4 = _engine()
    _state, _budget, r, _b = _run(l4, BINDING_CORPUS)
    require_equal(r["reconstruction_wrong"], 0,
                  "reconstruction returned a different event for some `t` — "
                  "consolidation may lose an episode, never rewrite one")
    require_equal(r["coverage_wrong"], 0,
                  "the derived schemas answered a semantic query wrongly; a "
                  "wrong answer scores 0 where an abstention would keep 100")
    require_equal(r["fabricated"], 0,
                  "the engine answered %d of %d unanswerable probes — pairs the "
                  "corpus never asserts, as-of before a pair's first assertion, "
                  "reconstruction past the end of the stream"
                  % (r["fabricated"], r["n_probes"]))


def trial_chronicle_and_murk_are_scored_as_ungated_diagnostics():
    """R4 clause 1, on R1 clause 5's conditional arithmetic-skip.

    Neither corpus is retired and neither's bytes change: their ceilings are
    computed, recorded and drift-checked (`t_attainability.py`), and a Layer-4
    gate trial on them skips **only while** the ceiling lies below the gate. The
    skip states the condition that lifts it, in code — if either corpus ever
    became redundant enough to admit the gate, this trial engages by itself,
    with no session's permission.

    What is *not* deferred: `B = 1000` binds on them too (the trial above), and
    so does the prohibition on fabrication. R1 settled that a diagnostic is not
    decoration.
    """
    for name in DIAGNOSTIC_CORPORA:
        o = _l4tasks.oracle(name)
        if o["max_coverage_permille"] < GATE_C or \
                o["max_reconstruction_F_permille"] < GATE_RECONSTRUCTION_F:
            skip("%s: ungated diagnostic (BOUNDARY-RULINGS.md R4 clause 1) — the "
                 "gate is unreachable here by ANY state in the declared family: "
                 "C ≤ %d against a %d gate, F ≤ %d against a %d gate, and the "
                 "exact history schema costs %d cells against a %d-cell budget. "
                 "The skip is conditional on that arithmetic and lifts by itself "
                 "if either ceiling ever reaches the gate."
                 % (name, o["max_coverage_permille"], GATE_C,
                    o["max_reconstruction_F_permille"], GATE_RECONSTRUCTION_F,
                    o["minimal_sufficient_cells"], o["budget_cap"]))

    l4 = _engine()
    for name in DIAGNOSTIC_CORPORA:
        _state, _budget, r, _b = _run(l4, name)
        require_equal(r["fabricated"], 0,
                      "%s: the engine fabricated on %d unanswerable probes"
                      % (name, r["fabricated"]))
        require(r["C"] >= GATE_C,
                "%s: C=%d below the gate this corpus now admits"
                % (name, r["C"]))
        require(r["F"] >= GATE_RECONSTRUCTION_F,
                "%s: reconstruction F=%d below the gate this corpus now admits"
                % (name, r["F"]))

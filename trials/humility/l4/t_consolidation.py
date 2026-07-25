"""humility/l4 — Layer 4 (Consolidation) humility (BOUNDARY.md §6, §5 L4).

Runs Layer 4's **own** battery (`_l4tasks` / `_l4score`, shared verbatim with the
ascension trial) at footprint 250‰ against the capped engine
`make_engine(layer_cap = 3)` — the Forgetting engine, which drops but does not
derive — through the same generic interface (§7). The declared ceiling is
**capped reconstruction F ≤ 400 at footprint ≤ 250** (§5 L4), bound to
`corpora/l4stream` by **BOUNDARY-RULINGS.md R4**. The structural argument is
`IMPOSSIBILITY.md`, which carries both halves: the behavioral one (§5.1 L4's own
defense) and the information-theoretic one (the frozen `l4-seam` pigeonhole
witness).

Why this is green the moment the battery exists, *before* the consolidation
engine is built: pre-Layer-4, `make_engine(3)` **is** the whole engine, so a
capped run scoring far below the ceiling is the very fact that the gate needs
Layer 4. The primary check runs against the Layer-3 adapter (always present); an
engine-gated confirmation against the Layer-4 engine *built and then capped to
3* SKIPS until that engine exists, then holds forever. That is the same shape
`humility/l3/t_forgetting.py` uses one layer down.

## Where the ceiling is measured, and what carries the rest — stated, not hidden

The capped engine is the **frozen** Layer-3 engine, whose eviction path is
`O(retained)` per write by design (`core/layers/README-l3.md §0.3`: the
forgetting record had to be aggregated because per-eviction records are
arithmetically unavailable). At footprint 250‰ on the whole 20 000-event
`l4stream` that is ~15 500 evictions against ~4 500 retained items, and the
replay costs **663 s** — fifteen times the entire rest of the suite. Measured
once, out of suite, it retains **4 484 of 20 000 episodes** (peak occupancy
43 299 of a 43 300 cap) and scores **C = 0, reconstruction F = 302** against the
ratified ceiling of 400. `IMPOSSIBILITY.md §4` records that run, how to
reproduce it, and why the suite does not carry it.

What the suite carries instead, and why it is not weaker:

1. **The measured capped run at declared prefix scales** (`SCALES` below). A
   prefix of a frozen corpus is that corpus's own bytes, and the footprint gate
   reads identically on it — R4 clause 2 makes `250` a *ratio* to the raw
   episodic footprint, not an absolute cell count, so the capped engine is
   squeezed to a quarter of whatever it is shown. The ceiling claim is
   scale-free for exactly that reason, and the trials assert it at every scale
   rather than at one.
2. **The whole-stream arithmetic bound**, which credits the capped engine with
   strictly *more* than it can do — cheapest-items-first, then an exact
   reconstruction for every retained `t` — and reaches **325**, under the 400
   ceiling. It is engine-free, it runs on every suite, and it is Stage A's own
   fixture (`_l4tasks.baseline_capped_l3`, tabulated by R4 clause 1). A trial
   below asserts that the instrument used at prefix scale agrees with it on the
   whole stream, so this is one measurement at several scales and not two
   instruments.
3. **The pigeonhole**, which is scale-free by construction and is what makes the
   ceiling structural rather than empirical: no measurement at any scale could
   rescue an engine whose state provably does not contain the answer.
"""

from fractions import Fraction

from _harness import require, require_equal, try_import
from adapters import l3
import _l4score
import _l4tasks

CEILING_RECONSTRUCTION_F = 400   # §5 L4 humility ceiling
GATE_FOOTPRINT = 250             # §5 L4 — the footprint the ceiling is stated AT

CAPPED_LAYER = 3
CORPUS = "l4stream"

# The declared prefix scales the capped engine is measured at (see the module
# docstring). A doubling ladder, because one scale could not show the ceiling is
# scale-free and this claim's whole strength is that it is.
SCALES = (1000, 2000, 4000)

# How far the measured `F` may spread across those scales before the
# scale-invariance this design rests on stops being true. The ceiling sits ~100‰
# above the measured value; a quarter of that headroom is the declared band, and
# the measurements cluster inside 10‰ of each other. This is not a
# constitutional threshold — it is the invariance claim, asserted rather than
# narrated, so a corpus or engine change that broke it would be red here rather
# than silently weakening `IMPOSSIBILITY.md §4`.
SCALE_INVARIANCE_BAND = 25

# `core/layers/README-l3.md §0.3`: the aggregated forgetting record costs
# `3 + 2 × len(buckets)` cells and is capped at 16 buckets forever, whatever the
# number of evictions. This is the pigeonhole's denominator.
FORGETTING_RECORD_MAX_CELLS = 35

_RUNS = {}


def _measure(engine, label, m):
    """Replay `l4stream[:m]` under `make_engine(3, cap)` and score the battery."""
    key = (label, m)
    if key not in _RUNS:
        bundle = _l4tasks.prefix(CORPUS, m)
        state, budget = _l4score.replay(
            engine, lambda cap: engine.make_engine(CAPPED_LAYER, cap), bundle)
        _RUNS[key] = (state, budget, _l4score.score(engine, state, bundle),
                      bundle)
    return _RUNS[key]


def _assert_ceiling(engine, label):
    """The ceiling, at every declared scale, with the run's own arithmetic bound."""
    for m in SCALES:
        state, budget, r, bundle = _measure(engine, label, m)
        bound = _l4score.forget_only_bound(bundle)

        require(r["footprint"] <= GATE_FOOTPRINT,
                "%s / n=%d: the capped engine sits at %d‰ of the raw episodic "
                "footprint, above the %d‰ the ceiling is stated at — it was not "
                "squeezed and the measurement means nothing"
                % (label, m, r["footprint"], GATE_FOOTPRINT))
        require(budget["B"] >= 1000,
                "%s / n=%d: the capped engine breached its own budget (B=%d, "
                "peak %d, cap %d)"
                % (label, m, budget["B"], budget["peak"], budget["cap"]))
        require(r["F"] <= CEILING_RECONSTRUCTION_F,
                "%s / n=%d: capped reconstruction F=%d exceeds the §5 L4 "
                "humility ceiling %d — the Layer-4 gate would not be "
                "load-bearing (%d/%d events reconstructed exactly)"
                % (label, m, r["F"], CEILING_RECONSTRUCTION_F,
                   r["reconstructed"], r["n_q4"]))
        require(r["F"] <= bound["F_bound"],
                "%s / n=%d: the capped engine measured F=%d above its own "
                "cheapest-items-first arithmetic bound of %d — the bound is not "
                "a bound" % (label, m, r["F"], bound["F_bound"]))

        # Not vacuous from below: it is a genuine engine that retained a real
        # quarter of the stream and reconstructs exactly what it retained, so
        # the ceiling distinguishes a capability rather than an empty state.
        require(r["F"] > 100,
                "%s / n=%d: the capped engine sits at the abstention floor — it "
                "retained nothing, so the ceiling distinguishes nothing"
                % (label, m))
        require_equal(r["reconstruction_wrong"], 0,
                      "%s / n=%d: the capped engine returned a *different* event "
                      "for some `t` — forgetting may drop, never rewrite"
                      % (label, m))


# ---- 1. the ceiling, measured -----------------------------------------------

def trial_capped_forget_only_engine_cannot_reconstruct_l4stream():
    """§5 L4: `capped reconstruction F ≤ 400 at footprint ≤ 250`.

    §5.1 L4's defense, measured: *"a forget-only engine squeezed to a quarter of
    the bytes has simply lost three-quarters of its episodes and cannot
    reconstruct what it deleted."* Dropping is not deriving.
    """
    _assert_ceiling(l3, "L3-adapter make_engine(3)")


def trial_capped_engine_lost_three_quarters_of_its_episodes():
    """The behavioral half of `IMPOSSIBILITY.md`, as an episode count.

    R4 clause 2 measured the same thing on the whole stream (5 010 of 20 000
    episodes under the cheapest-first bound; 4 484 under the real importance
    ordering, which keeps a costlier mix and therefore fewer items). Here it is
    asserted at each declared scale from the engine's own answers: the events it
    can still reconstruct are the events it still holds, and they are at most a
    quarter of what it was shown.
    """
    for m in SCALES:
        _state, _budget, r, bundle = _measure(l3, "L3-adapter make_engine(3)", m)
        bound = _l4score.forget_only_bound(bundle)
        kept = _l4tasks.permille(Fraction(r["reconstructed"], r["n"]))
        require(kept <= GATE_FOOTPRINT,
                "n=%d: the capped engine still holds %d‰ of its episodes at a "
                "quarter of the footprint — §5.1 L4's 'lost three-quarters of "
                "its episodes' is the defense this measures" % (m, kept))
        require(r["reconstructed"] <= bound["max_kept"],
                "n=%d: the capped engine retained %d items, more than the %d a "
                "cheapest-items-first policy could afford at the same cap — no "
                "importance ordering can beat cheapest-first on count"
                % (m, r["reconstructed"], bound["max_kept"]))


def trial_the_capped_ceiling_is_scale_free():
    """The claim that lets a prefix ladder carry a whole-stream ceiling.

    `footprint ≤ 250` is a **ratio** (R4 clause 2), so the capped engine is
    squeezed to a quarter of whatever it is shown and keeps a quarter of it at
    every scale. Measured, the reconstruction score moves by a few permille
    across a doubling ladder while the ceiling sits ~100‰ above it — and the
    whole-stream run recorded in `IMPOSSIBILITY.md §4` lands just past the top
    of the ladder, exactly where the ladder points.

    Asserted rather than narrated: if a corpus or engine change ever made the
    ceiling scale-dependent, the prefix measurement would stop standing in for
    the whole stream, and that must be a red trial rather than a paragraph
    nobody re-reads.
    """
    scores = []
    for m in SCALES:
        _state, _budget, r, _b = _measure(l3, "L3-adapter make_engine(3)", m)
        scores.append((m, r["F"], r["footprint"]))
    spread = max(f for _m, f, _fp in scores) - min(f for _m, f, _fp in scores)
    require(spread <= SCALE_INVARIANCE_BAND,
            "capped reconstruction F spread %d‰ across scales %s — the ceiling "
            "is no longer scale-free, so a prefix measurement no longer stands "
            "in for the whole stream"
            % (spread, [(m, f) for m, f, _fp in scores]))
    for m, _f, fp in scores:
        require(fp <= GATE_FOOTPRINT,
                "n=%d: the footprint read %d‰ — the ratio reading (R4 clause 2) "
                "is what makes the ladder legitimate" % (m, fp))


def trial_capped_engine_answers_no_consolidation_query_and_never_fabricates():
    """Capability absence surfaces as a **score**, never an exception (§7.3).

    The forget-only engine has no current-value table, no interval, no pattern
    fold; the whole Q1–Q3 coverage battery is a capability it does not have, so
    it abstains on all of it — `C = 0` against the ascension gate's 850 — and it
    invents nothing on the unanswerable probes. That gap *is* the layer.
    """
    for m in SCALES:
        _state, _budget, r, _b = _measure(l3, "L3-adapter make_engine(3)", m)
        require_equal(r["C"], 0,
                      "n=%d: the capped engine answered %d of %d semantic "
                      "queries — a forget-only engine has no derived schema to "
                      "answer them from, so either the battery has become "
                      "answerable from raw episodes or the cap is not binding"
                      % (m, r["recovered"], r["n_coverage"]))
        require_equal(r["coverage_wrong"], 0,
                      "n=%d: the capped engine answered a semantic query wrongly "
                      "rather than abstaining (§7.3)" % (m,))
        require_equal(r["fabricated"], 0,
                      "n=%d: the capped engine answered %d of %d unanswerable "
                      "probes" % (m, r["fabricated"], r["n_probes"]))


# ---- 2. the pigeonhole, measured --------------------------------------------

def trial_the_forgotten_leave_a_bounded_aggregate_and_nothing_else():
    """The information-theoretic half, in measured form (`IMPOSSIBILITY.md §3`).

    The frozen `l3` strain
    (`strain/l3/t_forgetting_strain.py::trial_two_streams_differing_only_in_what_was_forgotten_are_indistinguishable`)
    is the witness: two streams differing only in the *content* of an evicted
    item produce **byte-identical** snapshots. This is that witness's arithmetic
    consequence at Layer-4 scale, measured on the capped engine rather than
    argued: thousands of distinct evicted payloads leave behind a record of at
    most `3 + 2 × 16 = 35` integer cells, so **no injective map from the evicted
    set into Layer-3 state exists** and reconstruction over the evicted set is
    unanswerable in principle, not merely hard.

    What the engine does with that: it abstains. Every event it cannot
    reconstruct is an abstention and none is an invention — which is why the
    ceiling is 400 and not 0.
    """
    for m in SCALES:
        state, _budget, r, _b = _measure(l3, "L3-adapter make_engine(3)", m)
        evicted = r["n"] - r["reconstructed"]
        require(evicted > 0,
                "n=%d: nothing was evicted — the capped engine was not under "
                "the footprint at all" % (m,))
        require_equal(r["reconstruction_abstained"], evicted,
                      "n=%d: the events the engine cannot reconstruct are not "
                      "exactly the events it abstains on" % (m,))

        ans = l3.query(state, {"op": "forgetting"})
        require_equal(ans["status"], "answer",
                      "n=%d: the capped engine no longer reports its aggregated "
                      "forgetting record" % (m,))
        record = ans["value"]
        cells = 3 + 2 * len(record["buckets"])
        require(cells <= FORGETTING_RECORD_MAX_CELLS,
                "n=%d: the forgetting record grew to %d cells, above the %d it "
                "is bounded at forever by coarsening — the pigeonhole below "
                "assumes that bound" % (m, cells, FORGETTING_RECORD_MAX_CELLS))
        require_equal(record["count"], evicted,
                      "n=%d: the aggregated record counts %d forgotten items but "
                      "%d events cannot be reconstructed"
                      % (m, record["count"], evicted))
        require(evicted > 10 * cells,
                "n=%d: only %d items were forgotten into %d cells — the "
                "pigeonhole needs the evicted set to dwarf the record, and at "
                "this scale it no longer does" % (m, evicted, cells))


# ---- 3. the whole-stream bound, engine-free ---------------------------------

def trial_the_whole_stream_bound_is_stage_as_and_lies_under_the_ceiling():
    """The prefix instrument and Stage A's whole-stream fixture are the same one.

    `_l4score.forget_only_bound` is what prices the capped engine at prefix
    scale; `_l4tasks.baseline_capped_l3` is what R4 clause 1 tabulates on the
    whole stream (200 / 325). If they ever disagreed on the whole stream, the
    prefix measurements would be scored by a second instrument and the ceiling
    would rest on a number no ruling ever saw. They must agree, and the agreed
    number must lie under the ratified ceiling.

    No engine is needed for any of it, so this runs today and forever.
    """
    whole = _l4tasks.corpus(CORPUS)
    ours = _l4score.forget_only_bound(whole)
    stage_a = _l4tasks.baseline_capped_l3(CORPUS)

    require_equal(ours["F_bound"], stage_a["F_permille"],
                  "the prefix-scale bound and Stage A's whole-stream baseline "
                  "disagree on l4stream — the humility measurement would be "
                  "scored by an instrument no ruling has seen")
    require_equal(ours["episodes_kept_permille"],
                  stage_a["episodes_kept_permille"],
                  "the two bounds disagree on how many episodes survive at a "
                  "quarter of the footprint")
    require(ours["F_bound"] <= CEILING_RECONSTRUCTION_F,
            "the whole-stream forget-only bound reached F=%d, above the §5 L4 "
            "ceiling of %d — the ceiling is breached by the corpus before any "
            "engine exists" % (ours["F_bound"], CEILING_RECONSTRUCTION_F))
    require(ours["F_bound"] > 100,
            "the whole-stream bound sits at the abstention floor, so the "
            "ceiling distinguishes nothing")


# ---- 4. the engine-gated confirmation ---------------------------------------

def trial_capped_l4_engine_at_cap3_is_identically_incapable():
    """The Layer-4 engine, constructed and then capped to 3, must behave the same.

    Engine-gated: SKIPS until `core/layers/l4_consolidation.py` exists, then
    holds forever. §7.4 makes capping a construction-time restriction only, so a
    capped Layer-4 engine is a forget-only engine and must land under the same
    ceiling — an engine that answered the consolidation battery at
    `layer_cap = 3` would have smuggled the capability past its own cap.
    """
    l4 = try_import("adapters.l4",
                    "no L4 engine yet; the capped-L4 confirmation engages when "
                    "built")
    _assert_ceiling(l4, "L4-adapter make_engine(3)")
    for m in SCALES:
        _state, _budget, r, _b = _measure(l4, "L4-adapter make_engine(3)", m)
        require_equal(r["C"], 0,
                      "n=%d: the Layer-4 engine capped to 3 answered %d semantic "
                      "queries — capability escaped its own cap (§7.4)"
                      % (m, r["recovered"]))

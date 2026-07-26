"""strain/l4 — Layer 4 (Consolidation) under dirt, pressure and its own thesis.

Six strains, and each is a claim that could fail silently if nobody asserted it.
The taxonomy is `autopsy/GAPMAP.md §6`'s — Schacter's seven sins as strain
classes, *"each sin a strain to induce and score, not a bug to hide"* — and the
two sins consolidation is heir to are named there and taken here.

| strain | class | what would otherwise fail quietly |
|---|---|---|
| cited support | **misattribution** (right content, wrong source) | a derived answer that names a `t` which never carried it |
| as-of vs the present | **bias** (present beliefs reshape the past) | Graphiti's default read, which ignores `invalid_at` |
| the ledger closes | **absent-mindedness** (GAPMAP seed: *"what is refused under budget must be refused honestly"*) | an engine that loses episodes and calls it compression |
| Form B | the ladder's thesis | forgetting and consolidation being two mechanisms rather than one seen twice |
| flood | importance inflation | the Layer-3 guard lost in the move to a row codec |
| determinism | §2.3 | an eviction order that depends on anything but the stream |

**Misattribution and bias are Layer-4 sins by construction, not by analogy.**
Layer 3 could only return what it had retained, so a wrong source was not a
failure mode it could reach: an answer was the stored event or it was an
abstention. Layer 4 *derives*, and a derived answer has to say where it came
from and refuse to let the present rewrite the past. Those are exactly the two
defects the autopsies found in the prior art — Mem0's rewording at the door and
Graphiti's supersession-blind default read (`autopsy/GAPMAP.md §3` **S3**,
`autopsy/mem0/ANATOMY.md`) — so they are the two this layer must be strained on.

`corpora/murk` supplies the dirt. `BOUNDARY-RULINGS.md R4 clause 1` retired it as
a *ruler* and kept it as *dirt* in the same sentence: *"Its 305 recorded
contradictions are the answer key against which consolidation's supersession must
resolve-or-abstain per §3.0, and that is a strain obligation, not a gate. A
corpus can be the right dirt without being the right ruler."* This file is that
obligation discharged.
"""

import json
import os

from _harness import require, require_equal
import _l3score
import _l3tasks
import _l4score
import _l4tasks
from adapters import l3, l4
from core.state import event_cost
from corpora.murk import generator as murk_gen

BINDING = "l4stream"
DIRT = "murk"

# The ratified §5 L4 footprint, applied here to `murk` rather than to the binding
# corpus: R4 clause 1 kept murk as dirt and not as a ruler, so this strain states
# the footprint the dirt is thrown at, never a gate murk has to clear.
# Registered in `laws/t_rulings.py` against §5 L4 and R4 like every other copy.
GATE_FOOTPRINT = 250

# `core/layers/README-l3.md §0.3`: the aggregated forgetting record costs
# `3 + 2 x len(buckets)` cells and is capped at 16 buckets forever. Not a gate —
# an engine's own construction bound, inherited unchanged.
FORGETTING_RECORD_MAX_CELLS = 35

# The in-budget multiple used where a strain is about **correctness** rather than
# pressure: four times a stream's own raw episodic footprint, the same declaration
# `trials/inheritance/l4/t_inheritance.py` makes, so nothing a correctness strain
# finds can be blamed on the budget law.
INBUDGET_MULTIPLE = 4

# The flood strain's shape, mirroring `strain/l3`: heavy items placed EARLY (the
# worst case for recency) behind a flood of byte-identical copies.
DEFENDED = 30
FLOOD_SIZES = (50, 200, 800)
FLOOD_CAP_ITEMS = 60

_RUNS = {}


def _contradictions():
    """Murk's recorded contradiction defects (`ground_truth.json`, §8.7)."""
    with open(murk_gen.GROUND_TRUTH_PATH, "r", encoding="utf-8") as fh:
        truth = json.load(fh)
    return [d for d in truth["defects"] if d["type"] == "contradiction"]


def _inbudget_murk():
    """Murk replayed at cap 4, in budget: every contradiction chain survives."""
    if "murk" not in _RUNS:
        bundle = _l4tasks.corpus(DIRT)
        cap = INBUDGET_MULTIPLE * bundle["raw_cells"]
        state = l4.make_engine(4, cap)
        for payload in bundle["payloads"]:
            state, t = l4.ingest(state, payload)
            require(t is not None,
                    "an in-budget murk write was refused at cap 4")
        _RUNS["murk"] = (state, bundle)
    return _RUNS["murk"]


# ---- 1. misattribution: a derived answer names the assertion it came from ----

def trial_a_consolidated_answer_cites_the_assertion_that_carries_it():
    """**Misattribution.** Right content, wrong source, is still a defect.

    `autopsy/mem0/ANATOMY.md` found provenance ABSENT — an inferred fact and a
    user-stated one are indistinguishable at the door. `autopsy/writ/ANATOMY.md`
    found an answer's own `cited_sources` read by **zero** lines of scoring. The
    property both were missing is checkable and is checked here: every
    current-value and as-of answer carries a `support` naming a logical `t`, and
    the event **the corpus actually holds at that `t`** must assert exactly the
    value the engine returned.

    That is stronger than "the answer is right": it forbids an answer that is
    right by accident, or right about the value and wrong about where it came
    from. Provenance is dormant until Layer 7 (§4.2), which makes this a strain
    and not a gate — but the tag has to be *derivable* now or Layer 7 inherits a
    schema that cannot produce one.
    """
    state, bundle = _inbudget_murk()
    defects = _contradictions()
    require(len(defects) >= 300,
            "only %d contradictions in the answer key — the strain is thinner "
            "than R4 clause 1 records" % (len(defects),))

    checked = 0
    superseded = 0
    for defect in defects:
        pair = (defect["entity"], defect["key"])
        chain = bundle["chains"].get(pair)
        if not chain:
            continue
        checked += 1
        last_t, last_value = chain[-1]

        answer = l4.query(state, {"op": "current", "entity": pair[0],
                                  "key": pair[1]})
        require_equal(answer["status"], "answer",
                      "current(%r) abstained in budget — the chain is present"
                      % (pair,))
        require_equal(answer["value"], last_value,
                      "current(%r) did not return the value at the pair's "
                      "greatest t" % (pair,))
        support = answer["provenance"]["support"]
        require_equal(support, [last_t],
                      "current(%r) cited %r rather than the assertion at t=%d"
                      % (pair, support, last_t))
        cited = _l4tasks.facet(bundle["payloads"][support[0]])
        require(cited is not None and cited[0] == pair[0] and cited[1] == pair[1]
                and cited[2] == answer["value"],
                "current(%r) cited t=%d, where the corpus holds %r — the answer "
                "is sourced to an event that does not carry it"
                % (pair, support[0], bundle["payloads"][support[0]]))
        if chain[0][1] != last_value:
            superseded += 1

    require(checked >= 300,
            "only %d contradiction pairs were reachable" % (checked,))
    require(superseded > 0,
            "no contradiction actually changed a value, so citing the latest "
            "assertion proves nothing about supersession")


# ---- 2. bias: the present does not reshape the past -------------------------

def trial_as_of_honours_supersession_rather_than_reading_the_present():
    """**Bias.** Present beliefs must not reshape the past.

    Graphiti maintains a full bitemporal model on write and then, by default,
    **does not honour `invalid_at` at read** (`autopsy/graphiti/ANATOMY.md`,
    GAPMAP **S3**). The steal was to keep the model and fix the read: here the
    interval is integer logical-`t` arithmetic and the default read is the
    honest one. Three things are asserted for every contradicted pair:

      * as-of **at** a superseded assertion returns *that* assertion's value, not
        the current one;
      * as-of **between** two assertions returns the earlier one;
      * as-of **before** the pair's first assertion **abstains** — the case where
        a supersession-blind read invents a value that was never in force.
    """
    state, bundle = _inbudget_murk()
    checked = 0
    past_differs = 0
    for defect in _contradictions():
        pair = (defect["entity"], defect["key"])
        chain = bundle["chains"].get(pair)
        if not chain or len(chain) < 2:
            continue
        checked += 1
        current = chain[-1][1]

        for i, (stamp, value) in enumerate(chain[:-1]):
            answer = l4.query(state, {"op": "asof", "entity": pair[0],
                                      "key": pair[1], "t": stamp})
            require_equal(answer["status"], "answer",
                          "asof(%r, t=%d) abstained on a stored assertion"
                          % (pair, stamp))
            require_equal(answer["value"], value,
                          "asof(%r, t=%d) returned %r rather than the value in "
                          "force — the present overwrote the past"
                          % (pair, stamp, answer["value"]))
            if value != current:
                past_differs += 1
            gap = chain[i + 1][0] - 1
            if gap > stamp:
                between = l4.query(state, {"op": "asof", "entity": pair[0],
                                           "key": pair[1], "t": gap})
                require_equal(between["value"], value,
                              "asof(%r, t=%d) did not hold the interval open to "
                              "the next assertion" % (pair, gap))

        first = chain[0][0]
        if first > 0:
            before = l4.query(state, {"op": "asof", "entity": pair[0],
                                      "key": pair[1], "t": first - 1})
            require_equal(before["status"], "abstain",
                          "asof(%r, t=%d) answered %r before the pair's first "
                          "assertion — a supersession-blind read"
                          % (pair, first - 1, before["value"]))

    require(checked >= 200,
            "only %d contradicted pairs carried a history to test" % (checked,))
    require(past_differs > 0,
            "no past value differed from the present one, so the as-of battery "
            "could have been answered by a current-value table")


def trial_murk_under_pressure_abstains_rather_than_answering_from_a_shed_chain():
    """The same two sins, now at the Layer-4 cap where the schema does not fit.

    On `murk` the exact history schema costs 364‰ against a 250‰ budget
    (`ATTAINABILITY.md §5`), so the engine sheds chains — and a shed chain is
    precisely where a confident wrong answer would come from. Coverage falls;
    correctness does not: `wrong = 0` and `fabricated = 0` under full dirt at the
    footprint the gate is stated at.
    """
    bundle = _l4tasks.corpus(DIRT)
    state, budget = _l4score.replay(l4, lambda cap: l4.make_engine(4, cap), bundle)
    report = _l4score.score(l4, state, bundle)

    require_equal(budget["B"], 1000,
                  "murk breached its cap under pressure (peak %d, cap %d)"
                  % (budget["peak"], budget["cap"]))
    require(report["footprint"] <= GATE_FOOTPRINT,
            "murk sat at %d‰, above the footprint the strain is stated at"
            % (report["footprint"],))
    require_equal(report["coverage_wrong"], 0,
                  "the engine answered %d semantic queries wrongly under murk "
                  "pressure — a shed chain must abstain, not guess"
                  % (report["coverage_wrong"],))
    require_equal(report["reconstruction_wrong"], 0,
                  "the engine reconstructed %d events as different events"
                  % (report["reconstruction_wrong"],))
    require_equal(report["fabricated"], 0,
                  "the engine answered %d of %d unanswerable probes under murk "
                  "pressure" % (report["fabricated"], report["n_probes"]))
    require(len(state.damaged) > 0,
            "no chain was shed on murk, so this strain never reached the case it "
            "exists for")
    require(report["C"] > 0,
            "murk answered nothing at all, so `wrong = 0` is vacuous here")


# ---- 3. absent-mindedness: the ledger closes --------------------------------

def trial_every_event_is_demoted_forgotten_or_still_an_episode():
    """**Absent-mindedness**, the GAPMAP seed: what the budget cannot keep must be
    lost **honestly**.

    The layer's whole claim is that eviction has two kinds and that the engine
    knows which is which: an episode released because a chain regenerates it is a
    **demotion** and loses nothing, while an episode released with nothing behind
    it is **forgetting** and is written into the aggregated record. An engine
    that blurred the two could report a small forgetting count while having lost
    everything.

    So the ledger is asserted to close exactly, and to mean what it says:

        demotions + forgotten + episodes still held  ==  events ingested
        forgotten                                    ==  events it cannot reconstruct

    The second identity is the one with teeth. It says the record's count is not
    a number the engine chose: it is exactly the set of `t` the engine abstains
    on, so a demotion cannot be quietly booked as a loss and a loss cannot be
    quietly booked as a demotion.
    """
    bundle = _l4tasks.corpus(BINDING)
    state, budget = _l4score.replay(l4, lambda cap: l4.make_engine(4, cap), bundle)
    report = _l4score.score(l4, state, bundle)

    ledger = l4.query(state, {"op": "consolidation"})["value"]
    forgotten = state.forgetting.count
    require_equal(ledger["damaged"], 0,
                  "the binding corpus shed chains, so a shed assertion is counted "
                  "in the forgetting record as well as demoted and the ledger "
                  "below cannot close")
    require_equal(ledger["demotions"] + forgotten + ledger["episodes"],
                  bundle["n"],
                  "the ledger does not close: %d demoted + %d forgotten + %d "
                  "held against %d ingested"
                  % (ledger["demotions"], forgotten, ledger["episodes"],
                     bundle["n"]))
    require_equal(report["reconstruction_abstained"], forgotten,
                  "the engine abstains on %d events but records %d as forgotten "
                  "— the record is not the set of things it lost"
                  % (report["reconstruction_abstained"], forgotten))
    require(ledger["demotions"] > 10 * forgotten,
            "only %d demotions against %d losses — at this footprint almost every "
            "episode should be released losslessly, and if it is not, the layer "
            "is forgetting where it claims to be compressing"
            % (ledger["demotions"], forgotten))
    require_equal(report["reconstruction_wrong"], 0,
                  "an event the engine could not keep came back as a different "
                  "event — that is not honest loss")

    # The record is still the Layer-3 one: bounded forever by coarsening, so what
    # it can say about a loss is a count and a mass and never a payload.
    cells = 3 + 2 * len(state.forgetting.buckets)
    require(cells <= FORGETTING_RECORD_MAX_CELLS,
            "the forgetting record grew to %d cells, past the bound README-l3 "
            "§0.3 fixed for it" % (cells,))
    require(forgotten > 10 * cells,
            "only %d events were forgotten into %d cells — the pigeonhole that "
            "makes the loss irreversible needs the evicted set to dwarf the "
            "record" % (forgotten, cells))


# ---- 4. the Form B assertion: the ladder's thesis, as one trial -------------

def trial_the_cap4_engine_strictly_beats_the_cap3_engine_under_the_same_pressure():
    """**Form B.** Forgetting and consolidation are one mechanism seen twice.

    `core/layers/README-l3.md §0.4` chose GAPMAP **S4** form B — *"true eviction
    now, with the L4 co-design intent recorded"* — and recorded the debt:
    *"demotion-into-consolidated-form ... is deferred to Layer 4, deliberately,
    because it cannot be built before consolidation exists. A cold tier is only
    affordable if a cold entry costs materially less than an event, and the only
    thing in the ladder that makes an entry cheaper than the event it came from
    is L4 compression."*

    This is the debt coming due, measured on the corpus Layer 3 was gated on, at
    Layer 3's own pressure cap, through Layer 3's own battery and scorer. Nothing
    is re-tuned: the same 11 000 units, the same 10 000 items, the same cues. The
    only difference is that a Layer-4 episode is a **derived row** — the grammar
    priced once in a shape instead of once per event — so the same budget holds
    more of the stream, and importance-ranked eviction has more to rank.

    A note the trial states rather than hides: the Layer-3 attainability ceiling
    of 918‰ is exact over **retain-or-drop** policies, which is the family Layer
    3 could choose from. A consolidating engine is not in that family, and it
    passes through the ceiling for exactly the reason the ceiling was true. No
    Layer-3 number moves: `adapters/l3` is untouched and its gate still binds
    against 918.
    """
    stream = "l3streamb"
    cap3_state, cap3_budget = _l3score.replay(
        l3, lambda cap: l3.make_engine(3, cap), stream)
    cap3 = _l3score.score(l3, cap3_state, stream)

    cap4_state, cap4_budget = _l3score.replay(
        l4, lambda cap: l4.make_engine(4, cap), stream)
    cap4 = _l3score.score(l4, cap4_state, stream)

    require_equal(cap3_budget["cap"], cap4_budget["cap"],
                  "the two engines were not held to the same budget")
    require_equal(cap4_budget["B"], 1000,
                  "the Layer-4 engine breached Layer 3's cap (peak %d of %d)"
                  % (cap4_budget["peak"], cap4_budget["cap"]))
    require_equal(cap4["wrong"], 0,
                  "the Layer-4 engine corrupted %d retained items under Layer-3 "
                  "pressure" % (cap4["wrong"],))
    require_equal(cap4["fabricated"], 0,
                  "the Layer-4 engine fabricated on a never-ingested cue")

    require(cap4["weighted_C"] > cap3["weighted_C"],
            "the cap-4 engine scored weighted-C %d against the cap-3 engine's %d "
            "on %s — consolidation bought nothing under pressure, and the claim "
            "that forgetting and consolidation are one mechanism has no evidence "
            "here" % (cap4["weighted_C"], cap3["weighted_C"], stream))
    require(cap4["unweighted_C"] > cap3["unweighted_C"],
            "the cap-4 engine retained no more of the stream than the cap-3 "
            "engine (%d‰ against %d‰)"
            % (cap4["unweighted_C"], cap3["unweighted_C"]))
    require(l4.retained(cap4_state) > l3.retained(cap3_state),
            "the cap-4 engine held %d items against the cap-3 engine's %d at the "
            "same cap — the row codec is not compressing"
            % (l4.retained(cap4_state), l3.retained(cap3_state)))

    # ...and the mechanism is named, not merely observed: the win is per-item
    # cost, which is what §0.4 said it would have to be.
    payload = _l3tasks.stream(stream)["payloads"][0]
    shape = l4.row_shape(payload)
    require(1 + len(shape[1]) < event_cost(payload),
            "a Layer-4 episode does not cost less than the event it came from, "
            "so the advantage above came from somewhere this trial cannot name")


# ---- 5. importance inflation survives the move to a row codec ---------------

def _item(tag, weight, key="delta", val=1):
    return {"importance": weight, "key": key, "kind": "item",
            "tag": tag, "val": val}


def trial_manufactured_duplicates_still_cannot_mint_importance():
    """The Layer-3 inflation guard must survive being reimplemented over rows.

    `strain/l3` proved it for the episodic store: a cluster's `uses` count
    **distinct payloads, first occurrence only**, so a flood of byte-identical
    copies mints no mass. Layer 4 keeps its episodes as rows and reads weight and
    handle off the row's columns rather than off a rebuilt payload — a different
    implementation of the same law, and therefore a place the guard could have
    been lost without any score noticing.

    Measured the same way: heavy items placed **early** (the worst case for
    recency) survive a flood whose footprint does not grow with its size.

    One difference from the Layer-3 measurement is stated rather than smoothed
    over. There the flood held exactly 31 slots at 50, 200 and 800 copies; here
    it holds slightly **fewer** as the flood grows, because the cluster's single
    use recedes while the flood keeps arriving, so late copies are weaker than
    the copies already held and are dropped on arrival. The asserted property is
    therefore the one that matters and the one that is true — the footprint never
    grows with the flood — rather than an equality that would be asserting an
    accident of two different per-item costs.
    """
    defended = [_item("keep%03d" % i, 240) for i in range(DEFENDED)]
    probe = l4.make_engine(4, 1_000_000)
    for payload in defended:
        probe, _t = l4.ingest(probe, payload)
    cap = (probe.occupancy * FLOOD_CAP_ITEMS) // DEFENDED

    footprints = []
    for size in FLOOD_SIZES:
        state = l4.make_engine(4, cap)
        for payload in defended:
            state, _t = l4.ingest(state, payload)
        flood = _item("floodtag", 1)
        for _ in range(size):
            state, _t = l4.ingest(state, flood)
        survivors = sum(
            1 for payload in defended
            if l4.query(state, {"op": "recall", "cue": {"tag": payload["tag"]}}
                        )["status"] == "answer")
        require_equal(survivors, DEFENDED,
                      "flood %d: only %d of %d defended items survived — "
                      "repetition bought activation" % (size, survivors, DEFENDED))
        held = l4.retained(state)
        footprints.append(held - DEFENDED)
        require(state.occupancy <= cap,
                "flood %d: the cap broke (%d > %d)"
                % (size, state.occupancy, cap))

    require(footprints == sorted(footprints, reverse=True),
            "the flood's footprint grew with its size: %r at floods %r — the "
            "attack scales, so the guard is not the distinct-payload rule"
            % (footprints, list(FLOOD_SIZES)))
    require(max(footprints) < FLOOD_SIZES[0],
            "a %d-copy flood already holds %d slots; at %d copies it holds %d — "
            "the footprint is tracking the flood rather than its one use"
            % (FLOOD_SIZES[0], footprints[0], FLOOD_SIZES[-1], footprints[-1]))


# ---- 6. determinism through consolidation -----------------------------------

def trial_consolidation_is_byte_identical_across_identical_replays():
    """§2.3, through demotion, forgetting and a snapshot round trip.

    Layer 3 anchored determinism through ~9 000 evictions. Layer 4 adds two more
    ways for an ordering to leak in — the insertion order of the interval table's
    key-major nesting and of the row shapes — so the law is re-asserted over a
    replay that exercises both, at the footprint the gate is stated at.
    """
    bundle = _l4tasks.prefix(BINDING, 6000)
    cap = bundle["raw_cells"] // 4

    def replay():
        state = l4.make_engine(4, cap)
        for payload in bundle["payloads"]:
            state, _t = l4.ingest(state, payload)
        return state

    first = replay()
    second = replay()
    require_equal(l4.snapshot(first), l4.snapshot(second),
                  "two identical streams produced different Layer-4 states")
    require(first.demotions > 0 and first.forgetting.count > 0,
            "the replay neither demoted nor forgot anything, so determinism was "
            "asserted over a state no eviction ever touched")
    restored = l4.restore(l4.snapshot(first))
    require_equal(l4.snapshot(restored), l4.snapshot(first),
                  "restore did not reproduce the consolidated state byte for byte")
    for t in (0, 1, 199, 4999, bundle["n"] - 1):
        require_equal(l4.query(first, {"op": "read", "t": t}),
                      l4.query(restored, {"op": "read", "t": t}),
                      "the restored state answered read(t=%d) differently" % (t,))

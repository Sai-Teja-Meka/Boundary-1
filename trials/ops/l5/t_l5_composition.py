"""ops/l5 — the Layer-5 state composition, and the readings it rests on.

`trials/ops/l4/t_l4_composition.py` is the model, and its two structural claims
are re-made here for the capability this layer adds:

  * **one reading, two implementations.** The battery reads a condition AST
    (`trials/_l5tasks.satisfies`) and the engine reads it independently
    (`core.layers.l5_prospection.satisfies`); the battery reads an `intend`
    payload as an intention and the engine reads it independently (`arms`). If
    either pair disagreed, the engine would be answering a different question
    from the one the gate asks — and unlike a coverage miss, a divergence here
    moves a **firing**, which is what `trigger-precision` counts.
  * **arm only what inverts, and only what you can evaluate.** An armed
    intention's episode is released at the door, so the pending entry must
    rebuild the payload byte-for-byte or the release is a loss booked as
    compression — `README-l4 §1`'s rule, and `BOUNDARY.log` line 26's lesson,
    applied to promises. And a condition outside the closed vocabulary is not
    armed at all: `_l5tasks.satisfies` **raises** on one (a corpus defect must
    not become a never-fires intention nobody noticed), so an engine that armed
    it would have to answer a question the battery refuses to ask.

The composition table is the Layer-5 counterpart of `README-l4 §0.4`, and the
accounting identity — the engine's incremental `occupancy` against a full
recomputation from the state alone — is asserted after **every write** of a
replay that provably exercises arming, firing, demotion and forgetting, because
an incremental counter that drifts is exactly how a footprint measure stops
meaning anything (R4 clause 3, ruled general).

Every number below is measured. Where `core/layers/README-l5.md` states one of
them in prose, **this file is the enforced value** (`BOUNDARY-RULINGS.md R6`
clause 3).
"""

import collections

from _harness import require, require_equal
from adapters import l5
import _l5score
import _l5tasks
from core.state import event_cost, payload_cost
from core.layers.l3_forgetting import forget_cost
from corpora.l5stream import generator as l5gen

# The declared cross-section the two condition readings are compared over: every
# frozen condition against every 100th caller payload, plus each condition at its
# own satisfaction point and at the write immediately before it — the two indices
# where a disagreement would move a firing rather than merely differ.
SAMPLE_STRIDE = 100

# The composition of the engine's state at the ratified Layer-5 cap, measured.
# `README-l5.md §0.4` carries the same table in prose; this is what a drift turns
# red (R6 clause 3).
COMPOSITION = {
    "chains": 36594,          # 16 keys + 2 924 pairs + 2 × 16 827 assertions
    "atlas": 32,              # 2 × 16 keys
    "counts": 14,             # 2 × 7 grammar kinds — `fired` is the seventh
    "irreducible": 600,       # 200 entities × their `note` counts
    "demotion_counter": 1,
    "forgetting": 25,         # width 2 048, 11 buckets — bounded at 35 forever
    "pending": 2141,          # 180 never-fires entries + one shape header
    "fired": 2297,            # 765 firings + one shape header
    "rows": 2859,             # 952 surviving `note` episodes at 3 cells + shape
    "index": 1065,            # 113 handle atoms + 952 postings
    "total": 45628,
    "cap": 45638,
}

# What the working room bought, and what it did not have to buy. Stage A priced
# W2 at 41 951 cells with a **margin of 3 687** (`ATTAINABILITY.md §4`); this is
# where that margin went, item by item, and the answer is the Layer-4 answer one
# layer up: the layer's real cost is the interval table and everything else is
# the change from it.
WORKING_ROOM = {
    "stage_a_margin": 3687,
    "key_major_recovers": 184,      # against Stage A's entity-major substrate
    "prospection_below_its_bound": 55,   # 4 493 bound − 4 438 measured, final
    "loss_reserve_unused": 10,      # 35 reserved − 25 the record reached
    "fired_counter_not_priced": 2,  # the seventh grammar kind, W2 counted six
    "room": 3934,
    "spent_on_episodes": 3924,      # 2 859 rows + 1 065 index
    "left": 10,
}

_RUNS = {}


def _at_the_gate():
    if "gate" not in _RUNS:
        b = _l5tasks.corpus()
        state, budget = _l5score.replay(
            l5, lambda cap: l5.make_engine(5, cap), b)
        _RUNS["gate"] = (state, budget, b)
    return _RUNS["gate"]


# ---- one reading, two implementations ---------------------------------------

def trial_the_engine_and_the_battery_read_a_condition_the_same_way():
    """`satisfies`, twice, over a declared cross-section of the frozen stream.

    The battery's implementation is what the corpus's satisfaction points — and
    therefore the whole ground truth of `trigger-precision` and `trigger-recall`
    — are computed from. The engine's is what actually fires. They are compared
    on every condition at its own `sigma` and at `sigma − 1`, which are the two
    payloads where a divergence changes a firing, and on a strided sample across
    the whole stream, which is where a divergence would show up as a spurious one.
    """
    b = _l5tasks.corpus()
    counts_at = []
    counts = {}
    for payload in b["payloads"]:
        counts[payload.get("kind")] = counts.get(payload.get("kind"), 0) + 1
        counts_at.append(dict(counts))

    probes = list(range(0, b["n"], SAMPLE_STRIDE))
    require(len(probes) >= 200, "the declared sample is too small to be a check")

    compared = 0
    for iid, rec in b["intents"].items():
        cond = rec["cond"]
        require(l5.readable(cond),
                "intention %d's condition is not readable under the engine's "
                "closed vocabulary, so the engine would not arm it and the "
                "corpus's own satisfaction point could never be reached" % (iid,))
        indices = list(probes)
        sigma = b["sat"][iid]
        if sigma is not None:
            indices += [sigma, sigma - 1]
        for k in indices:
            if k < 0 or k >= b["n"]:
                continue
            payload = b["payloads"][k]
            mine = l5.satisfies(cond, payload, counts_at[k])
            theirs = _l5tasks.satisfies(cond, payload, counts_at[k])
            require_equal(mine, theirs,
                          "the engine and the battery disagree on whether the "
                          "payload at caller index %d satisfies intention %d — "
                          "one reading, two implementations, and a divergence "
                          "here moves a FIRING" % (k, iid))
            compared += 1
    require(compared > 180000,
            "the cross-section shrank to %d comparisons" % (compared,))


def trial_the_engine_arms_exactly_the_payloads_the_corpus_declares_intentions():
    """`arms`, over every event of the frozen stream, and its inverse.

    Two halves. The engine must arm every `intend` payload the corpus declares —
    945 of them, no more and no fewer — and it must arm **nothing else**, because
    an engine that read some other kind as an intention would be holding a
    promise the ground truth has no satisfaction point for. And every armed
    payload must rebuild from `(iid, cond, fire)` as canonical bytes, which is
    what makes releasing its episode at the door a demotion rather than a loss.
    """
    b = _l5tasks.corpus()
    armed = []
    for k, payload in enumerate(b["payloads"]):
        read = l5.arms(payload)
        if read is None:
            require(payload.get("kind") != "intend",
                    "the engine declined to arm the `intend` payload at caller "
                    "index %d, so an intention the corpus counts fireable could "
                    "never fire" % (k,))
            continue
        require_equal(payload.get("kind"), "intend",
                      "the engine armed a payload of kind %r at caller index %d"
                      % (payload.get("kind"), k))
        iid, cond, fire = read
        require_equal(l5.rebuild_intention(iid, cond, fire), payload,
                      "the armed intention at caller index %d does not rebuild "
                      "to the payload it came from — arm only what inverts" % (k,))
        require_equal((iid, cond, fire),
                      (payload["iid"], payload["cond"], payload["fire"]),
                      "the intention facet at caller index %d read different "
                      "fields from the ones the grammar declares" % (k,))
        armed.append(iid)

    require_equal(len(armed), l5gen.DECLARED_INTENTIONS,
                  "the engine armed a different number of intentions than the "
                  "corpus declares")
    require_equal(len(set(armed)), len(armed),
                  "the corpus carries a duplicate `iid`, which the engine reads "
                  "as one intention and the battery as another")


# ---- the composition --------------------------------------------------------

def trial_the_state_composition_at_the_gate_is_the_recorded_one():
    """`README-l5.md §0.4`'s table, measured rather than asserted in prose."""
    state, _budget, b = _at_the_gate()

    got = {
        "chains": l5.chain_cells(state.chains),
        "atlas": 2 * len(state.atlas),
        "counts": 2 * len(state.counts),
        "irreducible": l5.irreducible_cells(state.irreducible),
        "demotion_counter": 1,
        "forgetting": forget_cost(state.forgetting),
        "pending": l5.pending_cells(state.pending),
        "fired": l5.fired_cells(state.fired),
        "rows": l5.rows_cells(state.demotable) + l5.rows_cells(state.kept),
        "index": l5.index_cells(state.index),
        "total": state.occupancy,
        "cap": b["budget_cap"],
    }
    for name in sorted(COMPOSITION):
        require_equal(got[name], COMPOSITION[name],
                      "the Layer-5 composition drifted at `%s`" % (name,))
    require_equal(sum(got[k] for k in
                      ("chains", "atlas", "counts", "irreducible",
                       "demotion_counter", "forgetting", "pending", "fired",
                       "rows", "index")),
                  got["total"],
                  "the composition's parts do not sum to the engine's own "
                  "occupancy, so one of them is not being counted")
    require_equal(l5.accounted_occupancy(state), state.occupancy,
                  "the incremental occupancy counter and a full recomputation "
                  "from the state alone disagree at the gate")
    require_equal(len(state.verbatim), 0,
                  "an episode was stored verbatim at the gate — every `intend` "
                  "payload is armed (so no episode at all) and every other kind "
                  "has a row shape, so a verbatim tier here is a reading defect")


def trial_the_working_room_is_accounted_and_the_margin_went_where_it_is_recorded():
    """Where Stage A's 3 687 cells went — the Layer-5 analogue of `README-l4 §0.4`.

    R5 clause 4 made the point that an unpriced item is *"not a saving; it is a
    margin that has already been spent"*, and Stage A priced its bookkeeping and
    its loss reserve by name because of it. This closes the loop from the other
    end: the margin that survived those items is stated as arithmetic against the
    measured state, so the answer to *"where did the 3 687 go"* is a trial rather
    than a paragraph.
    """
    state, _budget, b = _at_the_gate()
    w = WORKING_ROOM

    require_equal(w["stage_a_margin"], _l5tasks.witness_full()["margin"],
                  "Stage A's recorded margin moved")
    room = (b["budget_cap"] - l5.chain_cells(state.chains)
            - (2 * len(state.atlas) + 2 * len(state.counts)
               + l5.irreducible_cells(state.irreducible) + 1
               + forget_cost(state.forgetting))
            - l5.pending_cells(state.pending) - l5.fired_cells(state.fired))
    require_equal(room, w["room"],
                  "the working room left after the interval table, the "
                  "bookkeeping and the prospection tiers is not the recorded one")
    spent = l5.rows_cells(state.kept) + l5.rows_cells(state.demotable) \
        + l5.index_cells(state.index)
    require_equal(spent, w["spent_on_episodes"],
                  "the episodic tier the working room bought is not the "
                  "recorded one")
    require_equal(room - spent, w["left"],
                  "the cells left over at the gate drifted from the recorded %d"
                  % (w["left"],))
    require_equal(w["room"],
                  w["stage_a_margin"] + w["key_major_recovers"]
                  + w["prospection_below_its_bound"] + w["loss_reserve_unused"]
                  - w["fired_counter_not_priced"],
                  "the recorded reconciliation of Stage A's margin to the "
                  "measured working room does not add up")


def trial_the_prospection_tiers_are_priced_as_stage_a_priced_them():
    """One price, two implementations — `_l5tasks`' pricing and the engine's.

    Stage A priced a pending entry at `iid + t0 + cond + fire` and a fired row at
    `iid + t + fire`, with the fire payload's grammar paid once under the row
    codec. The engine's own `§4.1` accounting is independent code over a
    different data structure. They must agree on the same content, or the
    41 951-cell witness was pricing a state nobody built.
    """
    state, _budget, b = _at_the_gate()

    require_equal(l5.pending_cells(state.pending),
                  _l5tasks.pending_cells(b["never"]) + 2,
                  "the engine's pending set and Stage A's price for the same 180 "
                  "never-fires intentions differ (the +2 is the one shape header "
                  "the row codec pays for `fired`'s grammar, which Stage A "
                  "carried in its own `shapes` line)")
    require_equal(l5.fired_cells(state.fired),
                  _l5tasks.fired_row_cells(len(b["fireable"])) + 2,
                  "the engine's fired ledger and Stage A's price for the same "
                  "765 firings differ")
    require_equal(l5.pending_cells(state.pending) + l5.fired_cells(state.fired),
                  _l5tasks.witness_minimal()["pending_final_cells"]
                  + _l5tasks.witness_minimal()["fired_rows"] + 4,
                  "the engine's total prospection footprint is not W1's final "
                  "state plus its two shape headers")
    require(l5.pending_cells(state.pending) + l5.fired_cells(state.fired)
            <= _l5tasks.witness_full()["prospection"],
            "the engine's prospection tiers (%d cells) exceed the BOUND Stage A "
            "priced them at (%d) — that bound is peak pending plus final fired, "
            "two maxima that do not occur together, and a state above it is a "
            "state the attainability arithmetic did not admit"
            % (l5.pending_cells(state.pending) + l5.fired_cells(state.fired),
               _l5tasks.witness_full()["prospection"]))


# ---- the accounting identity, after every write -----------------------------

def _pressured_fixture():
    """A stream that provably arms, fires, demotes and forgets, and is small."""
    payloads = []
    for i in range(80):
        payloads.append({"kind": "attr", "entity": 1 + (i % 6), "key": "level",
                         "val": i})
        if i % 8 == 0:
            payloads.append({"kind": "note", "entity": 1 + (i % 6),
                             "text_id": 5000 + i})
        if i % 10 == 3:
            payloads.append({"kind": "intend", "iid": i,
                             "cond": {"op": "and",
                                      "args": [{"p": "kind", "v": "attr"},
                                               {"p": "val_ge", "v": i + 20}]},
                             "fire": {"kind": "fired", "text_id": 9000 + i}})
    return payloads


def trial_the_occupancy_counter_never_drifts_through_arming_and_firing():
    """The engine's incremental `§4.1` counter against a full recomputation.

    Asserted after **every** write, not at the end: the write path maintains
    occupancy incrementally because recomputing per write is quadratic, and the
    two new tiers give the increment two more places to be wrong — the shape
    header a pending group pays and gives back, and the swap a firing makes
    between the two tiers. A drift of one cell here is a footprint measure that
    has stopped being a measure of anything (R4 clause 3).
    """
    payloads = _pressured_fixture()
    raw = sum(event_cost(p) for p in payloads)
    fired_any = False
    for cap in (4 * raw, raw // 3, raw // 6):
        state = l5.make_engine(5, cap)
        for i, payload in enumerate(payloads):
            state, t = l5.ingest(state, payload)
            require_equal(l5.accounted_occupancy(state), state.occupancy,
                          "occupancy drifted at write %d of a cap-%d replay: the "
                          "counter says %d and the state accounts for %d"
                          % (i, cap, state.occupancy,
                             l5.accounted_occupancy(state)))
            require(state.occupancy <= cap,
                    "occupancy %d exceeded the cap %d at write %d"
                    % (state.occupancy, cap, i))
        if l5.fired_iids(state):
            fired_any = True
        if cap == raw // 6:
            require(state.forgetting.count > 0,
                    "the tightest replay forgot nothing, so the identity was "
                    "never asserted across a recorded loss")
            require(state.demotions > 0,
                    "the tightest replay demoted nothing")
    require(fired_any,
            "no intention fired in any of the three replays, so the identity "
            "was never asserted across the pending/fired swap")


def trial_the_prospection_tiers_are_outside_every_eviction_phase():
    """`miss = 0` and `dup-fire = 0` are identities, so neither tier may be evicted.

    The engine's design decision, stated as a measurement: at a cap that takes
    **every** episode, the pending set and the fired ledger are still whole. An
    engine that could evict either could be made to break a ratified gate by
    being poor — a `miss` for a pending entry it dropped, a `dup-fire` for a
    firing it forgot it had made — and `R6` clause 2 left the budget-versus-firing
    question to Stage C precisely so that the answer would be visible here rather
    than assumed.
    """
    payloads = _pressured_fixture()
    raw = sum(event_cost(p) for p in payloads)
    state = l5.make_engine(5, raw // 8)
    refused = 0
    for payload in payloads:
        state, t = l5.ingest(state, payload)
        if t is None:
            refused += 1
    armed = [p["iid"] for p in payloads if p.get("kind") == "intend"]

    require_equal(l5.retained(state), 0,
                  "%d episodes survived a cap of an eighth of the stream's own "
                  "footprint, so this fixture does not exercise the claim"
                  % (l5.retained(state),))
    require_equal(refused, 0,
                  "%d writes were refused where episodes were still available "
                  "to evict" % (refused,))
    require_equal(sorted(l5.pending_iids(state) + l5.fired_iids(state)),
                  sorted(armed),
                  "an armed intention is neither pending nor fired after every "
                  "episode was evicted: the eviction path reached a tier that "
                  "must be outside it")
    require_equal(state.demotions + state.forgetting.count + l5.retained(state),
                  state.next_t,
                  "the ledger does not close where the episodic tier is empty")


def trial_the_declared_predicate_vocabulary_is_closed_and_matches_the_corpus():
    """The engine's vocabulary is the corpus's, and neither has grown a predicate.

    `corpora/l5stream/grammar.md` freezes six predicates and three connectives and
    calls the set closed. The engine declares its own copy — it must, since
    `core/` imports no corpus — so the two are asserted equal here, in the same
    way `ops/l4` asserts the two facet readings agree.
    """
    require_equal(sorted(l5.PREDICATES), sorted(l5gen.PREDICATES),
                  "the engine's predicate vocabulary is not the corpus's")
    require_equal(sorted(l5.CONNECTIVES), sorted(l5gen.CONNECTIVES),
                  "the engine's connective vocabulary is not the corpus's")
    require_equal(sorted(l5gen.PAYLOAD_PREDICATES),
                  sorted(p for p in l5.PREDICATES if p != "count_ge"),
                  "the corpus's PAYLOAD_PREDICATES (the GUARDEDNESS base case) "
                  "is no longer the engine's vocabulary minus the one predicate "
                  "that reads nothing of the arriving payload")
    require_equal(l5.INTENTION_KIND, "intend",
                  "the declared intention kind drifted from the grammar")
    require_equal(l5.INTENTION_FORM, ("iid", "cond", "fire"),
                  "the declared intention form drifted from the grammar")

    atoms = collections.Counter()
    for rec in _l5tasks.corpus()["intents"].values():
        for atom in _l5tasks.atoms(rec["cond"]):
            atoms[atom["p"]] += 1
    require_equal(sorted(atoms), sorted(l5.PREDICATES),
                  "the frozen stream no longer exercises every predicate the "
                  "engine declares, so part of the vocabulary is untested")
    require_equal(payload_cost({"p": "kind", "v": "note"}), 4,
                  "rule P's pricing of a bare atom moved, and every pending "
                  "entry's cost is priced against it")

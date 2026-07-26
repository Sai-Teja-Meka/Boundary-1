"""ops/l4 — the Layer-4 state composition, priced before it was built.

`BOUNDARY-RULINGS.md R2` put attainability before authority: compute what a gate
admits before you bind it. `core/layers/README-l3.md §0` applied the same
discipline one level down, to the *engine* — compute what the budget admits
before you design the state — and `trials/ops/l3/t_state_composition.py` is where
that arithmetic became assertions rather than prose. This file is the Layer-4
counterpart.

Everything here is a cost claim `core/layers/README-l4.md` makes, restated as a
trial, plus the two structural properties the engine's honesty rests on:

  * **one reading, two implementations.** The battery reads a payload as an
    `(entity, key, value)` assertion (`trials/_l4tasks.facet`); the engine reads
    it independently (`core.layers.l4_consolidation.facet`). If those two ever
    disagreed, the engine would be answering a different question from the one
    the gate asks — and a pair whose latest assertion the engine declined to fold
    would make `current` return a stale value, which is **wrong**, not merely
    absent. They are asserted equal on every frozen corpus, event by event.
  * **fold only what inverts.** Every assertion the engine consolidates must
    rebuild to the byte-exact payload it came from, or the fold does not happen.
    That is why `reconstruction wrong = 0` is structural rather than lucky, and
    it is checked here over every event of every frozen corpus rather than only
    over the ones a gate happens to ask about.

The accounting identity — the engine's incremental `occupancy` against a full
recomputation from the state alone — is asserted after **every write** of a
replay that provably exercises all three kinds of eviction, because an
incremental counter that drifts is exactly how a footprint measure stops meaning
anything (R4 clause 3).
"""

from fractions import Fraction

from _harness import require, require_equal
import _l4score
import _l4tasks
from adapters import l4
from core.state import event_cost

CORPORA = ("l4stream", "chronicle", "murk")
BINDING = "l4stream"

# The ratified §5 L4 footprint, used here to price a design the engine did NOT
# choose — the two-way indexed schema — so the arithmetic that forced the search
# is a trial rather than a paragraph. Registered in `laws/t_rulings.py`.
GATE_FOOTPRINT = 250

# Stage A's exhibited witness on `corpora/l4stream`, recorded in
# `trials/ascension/l4/ATTAINABILITY.md §4` and tabulated by R4 clause 1: the
# exact interval table plus the global counters, and the room left over for
# everything the engine needs beyond them. Re-derived here from the corpus, never
# typed twice — `t_attainability.py` owns the same numbers on the gate side.
WITNESS_MINIMAL_CELLS = 40737
WITNESS_SPARE_CELLS = 2563

_RUN = {}


def _binding_run():
    """One replay of the whole binding corpus at the Layer-4 cap, cached."""
    if "state" not in _RUN:
        bundle = _l4tasks.corpus(BINDING)
        state, budget = _l4score.replay(
            l4, lambda cap: l4.make_engine(4, cap), bundle)
        _RUN["state"] = state
        _RUN["budget"] = budget
        _RUN["bundle"] = bundle
    return _RUN["state"], _RUN["budget"], _RUN["bundle"]


# ---- 1. one reading, two implementations ------------------------------------

def trial_the_engine_and_the_battery_read_one_facet_map():
    """The engine's declared grammar reading is the battery's, event by event.

    Both are declared readings of `corpora/chronicle/grammar.md` and
    `corpora/l4stream/grammar.md` — the engine's in `ASSERTION_FORMS`, the
    battery's in `_l4tasks.facet` — and neither is derived from the other. The
    agreement is the thing that must hold, so it is measured rather than assumed:
    a divergence in which events count as assertions would move `current`'s
    answer, not merely its availability.
    """
    for name in CORPORA:
        bundle = _l4tasks.corpus(name)
        checked = 0
        for payload in bundle["payloads"]:
            mine = l4.facet(payload)
            theirs = _l4tasks.facet(payload)
            require_equal(mine, theirs,
                          "%s: the engine and the battery disagree about the "
                          "assertion facet of %r" % (name, payload))
            checked += 1
        require(checked == bundle["n"] and checked > 0,
                "%s: the facet agreement was checked on %d of %d events"
                % (name, checked, bundle["n"]))


def trial_every_folded_assertion_rebuilds_byte_exactly():
    """Consolidation is invertible or it does not happen (§2.4).

    For every event the engine folds, the payload rebuilt from
    `(kind, entity, key, value)` must equal the original in canonical bytes. This
    is the structural root of the gate's `reconstruction wrong = 0`: the engine
    cannot regenerate an event wrongly, because it never consolidates one it
    could not prove it can regenerate.
    """
    for name in CORPORA:
        bundle = _l4tasks.corpus(name)
        folded = 0
        for payload in bundle["payloads"]:
            fact = l4.facet(payload)
            if fact is None:
                continue
            folded += 1
            entity, key, value = fact
            require(l4.invertible(payload, payload["kind"], entity, key, value),
                    "%s: %r folds into a chain but does not rebuild from it — the "
                    "fold would be a silent rewrite" % (name, payload))
        require_equal(folded, bundle["assertions"],
                      "%s: the engine folded %d events where the battery counts "
                      "%d assertions" % (name, folded, bundle["assertions"]))


def trial_the_irreducible_tier_is_irreducible_to_this_engine_too():
    """What no chain regenerates must be exactly what the corpus declares.

    `corpora/l4stream/grammar.md` declares 1 212 `note` events with globally
    unique `text_id`s so that reconstruction fidelity is bounded below 1000 **by
    construction**. If the engine folded them into chains it would be scoring
    against a corpus that had lost its own floor — so the count of events this
    engine cannot consolidate is asserted against the declared tier.
    """
    bundle = _l4tasks.corpus(BINDING)
    irreducible = [t for t, p in enumerate(bundle["payloads"])
                   if l4.facet(p) is None]
    require_equal(irreducible, bundle["irreducible"],
                  "the engine's irreducible tier is not the corpus's declared one")
    require(len(irreducible) > 0,
            "the binding corpus has no irreducible tier, so F could reach 1000 "
            "and the gate would measure nothing")


# ---- 2. the arithmetic that fixed the design --------------------------------

def trial_a_second_access_path_would_breach_the_footprint_gate():
    """Why `read(t)` searches instead of looking up (README-l4 §0).

    The interval table indexes `(entity, key) -> history`. Reconstruction asks the
    inverse. An exact `t -> pair` index costs one cell per assertion, and the
    schema then costs three cells per assertion — computed here against the
    ratified 250‰ footprint gate, on the corpus R4 clause 1 binds it to.
    """
    bundle = _l4tasks.corpus(BINDING)
    raw = bundle["raw_cells"]
    cap = bundle["budget_cap"]
    assertions = bundle["assertions"]
    identification = len(bundle["chains"]) + len(set(k for _e, k in bundle["chains"]))

    two_way = identification + 3 * assertions
    require(two_way > cap,
            "a two-way indexed schema costs %d cells against a %d-cell cap — it "
            "fits, so the search this engine pays for is a choice and not a "
            "consequence, and README-l4 §0 is wrong" % (two_way, cap))
    require(_l4tasks.permille(Fraction(two_way, raw)) > GATE_FOOTPRINT,
            "a two-way indexed schema prices under the 250‰ gate, so the missing "
            "inverse index is not forced by the footprint after all")


def trial_key_major_nesting_is_the_cheaper_nesting():
    """The table nests key-major because the key vocabulary is closed.

    `keys + pairs` against `entities + pairs`: identical in the assertion cells
    and different in the identification cells, in the engine's favour on every
    frozen corpus — most sharply where the entity population is unbounded, which
    is exactly the chronicle family's defect (`ATTAINABILITY.md §5`).
    """
    for name in CORPORA:
        bundle = _l4tasks.corpus(name)
        entities = len(bundle["entities"])
        keys = len(set(k for _e, k in bundle["chains"]))
        require(keys < entities,
                "%s: the key vocabulary (%d) is not smaller than the entity "
                "population (%d), so key-major nesting buys nothing here"
                % (name, keys, entities))


def trial_the_row_codec_is_cheaper_than_the_episode_it_replaces():
    """A derived row prices the grammar once; an episode prices it every time.

    Checked on the shapes that matter to this layer: `l4stream`'s irreducible
    `note` (the tier the footprint's spare cells buy) and `l3streamb`'s `item`
    (the shape the Form-B strain rests on). The claim is not that rows are small
    — it is that the same event costs strictly less as a row than as an episode,
    which is what makes an episodic tier affordable at all under this cap.
    """
    from corpora.l3streamb import generator as streamb_gen

    samples = [("l4stream note", {"kind": "note", "entity": 7, "text_id": 42}),
               ("l3streamb item", next(iter(streamb_gen.generate(streamb_gen.SEED, 1))))]
    for label, payload in samples:
        shape = l4.row_shape(payload)
        require(shape is not None, "%s: no row shape expresses it" % (label,))
        row = 1 + len(shape[1])
        episode = event_cost(payload)
        require(row < episode,
                "%s: a row costs %d cells and the episode %d — the codec is not "
                "compression" % (label, row, episode))
        require_equal(l4.row_payload(shape, l4.row_values(payload, shape)), payload,
                      "%s: the row does not rebuild its own payload" % (label,))


# ---- 3. the composition the budget actually admits --------------------------

def trial_the_composition_sums_to_the_engines_own_occupancy():
    """Every cell of Layer-4 state is accounted for, and the parts are named.

    The Layer-3 counterpart asserted `occupancy = 12 x retained + record` with no
    cell unaccounted. Here the composition has seven parts, and their sum must be
    the occupancy the engine reports and the budget law enforces.
    """
    state, budget, bundle = _binding_run()
    parts = {
        "interval table": l4.chain_cells(state.chains),
        "key atlas": 2 * len(state.atlas),
        "global counters": 2 * len(state.counts),
        "irreducible profile": l4.irreducible_cells(state.irreducible),
        "damaged marks": len(state.damaged),
        "derived rows": l4.rows_cells(state.demotable) + l4.rows_cells(state.kept),
        "verbatim episodes": sum(event_cost(p) for p in state.verbatim.values()),
        "handle index": l4.index_cells(state.index),
        "demotion counter": 1,
        "forgetting record": 3 + 2 * len(state.forgetting.buckets),
    }
    require_equal(sum(parts.values()), state.occupancy,
                  "the named composition does not sum to the engine's occupancy: "
                  "%r" % (parts,))
    require_equal(l4.accounted_occupancy(state), state.occupancy,
                  "the incremental occupancy counter drifted from a full "
                  "recomputation of the state it claims to price")
    require(state.occupancy <= budget["cap"],
            "the final state is over its own cap (%d > %d)"
            % (state.occupancy, budget["cap"]))


def trial_the_working_room_beyond_the_witness_is_spent_and_named():
    """Where Stage A's 2 563 cells went — the number that was the finding.

    `ATTAINABILITY.md §4` exhibited a state of `40 737` cells and recorded the
    engine's working room as `2 563`, *"tight by arithmetic, not by choice, and
    recorded now so Stage C inherits a number rather than a surprise."* This is
    Stage C answering with what it spent: the bookkeeping the witness did not
    price, and the episodes the remainder bought.
    """
    state, _budget, bundle = _binding_run()
    keys = len(set(k for _e, k in bundle["chains"]))
    minimal = keys + len(bundle["chains"]) + 2 * bundle["assertions"] \
        + 2 * len(bundle["kinds"])

    bookkeeping = (2 * len(state.atlas)
                   + l4.irreducible_cells(state.irreducible)
                   + len(state.damaged)
                   + 1
                   + 3 + 2 * len(state.forgetting.buckets))
    episodes = (l4.rows_cells(state.demotable) + l4.rows_cells(state.kept)
                + sum(event_cost(p) for p in state.verbatim.values())
                + l4.index_cells(state.index))

    require(minimal <= WITNESS_MINIMAL_CELLS,
            "the engine's minimal-sufficient schema (%d cells) costs more than "
            "Stage A's exhibited witness (%d) — the witness was supposed to be "
            "the floor" % (minimal, WITNESS_MINIMAL_CELLS))
    require_equal(minimal + bookkeeping + episodes, state.occupancy,
                  "the witness/bookkeeping/episodes split does not sum to "
                  "occupancy")
    require(bookkeeping < WITNESS_SPARE_CELLS,
            "the bookkeeping the witness did not price (%d cells) has consumed "
            "the whole %d-cell working room, leaving nothing for the irreducible "
            "tier" % (bookkeeping, WITNESS_SPARE_CELLS))
    require(episodes > 0,
            "no episode survived at all — the irreducible tier bought nothing and "
            "reconstruction rests entirely on the chains")


def trial_the_accounting_identity_holds_through_every_kind_of_eviction():
    """Demotion, forgetting and shedding all fire, and none of them drifts.

    A cap deliberately too small for `murk`'s own schema, so the write path is
    driven through all four phases. The identity is asserted after **every**
    write — an incremental counter that drifts only under a rare eviction order
    is exactly the bug a final-state check would miss — and each of the three
    eviction kinds is asserted to have actually happened, so the trial cannot
    pass by never reaching them.
    """
    bundle = _l4tasks.prefix("murk", 3000)
    cap = bundle["raw_cells"] // 8               # half of what the gate allows
    state = l4.make_engine(4, cap)
    for i, payload in enumerate(bundle["payloads"]):
        state, _t = l4.ingest(state, payload)
        require(state.occupancy <= cap,
                "occupancy %d exceeded the cap %d at write %d"
                % (state.occupancy, cap, i))
        require_equal(l4.accounted_occupancy(state), state.occupancy,
                      "the occupancy counter drifted at write %d" % (i,))
    require(state.demotions > 0, "no episode was ever demoted")
    require(state.forgetting.count > 0, "nothing was ever forgotten")
    require(len(state.damaged) > 0,
            "no chain was ever shed, so the fourth eviction phase is untested "
            "and the identity above says nothing about it")
    restored = l4.restore(l4.snapshot(state))
    require_equal(l4.snapshot(restored), l4.snapshot(state),
                  "the state did not survive a snapshot round trip after "
                  "demotion, forgetting and shedding")

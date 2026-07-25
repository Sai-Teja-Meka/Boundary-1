"""ops/l3 — the Layer-3 state-composition arithmetic (README-l3 §0, RULINGS R2).

**R2 put attainability before authority: compute what a gate admits before it
binds.** This file applies the same discipline one level down, to the engine's own
state: every cost claim in `core/layers/README-l3.md §0` is asserted here, so the
arithmetic that decided the Layer-3 design is **trialed, not trusted**.

Four claims, in the order §0 makes them:

  (0) **the remainder** — the ratified `unweighted-C ≥ 90‰` clause forces ≥ 900
      retained items = 9 900 of 11 000 units, leaving 1 100 for everything else;
  (a) **Layer-2-granularity indexing is impossible** — 21 index cells per event
      means 32/item, a 343-item capacity and 34‰ against a 90‰ gate; 900 items
      would cost 2.6× the whole cap. The remainder admits **one** unit of index
      per item, and the engine's handle index costs exactly that;
  (b) **per-eviction tombstones are impossible** — one cell per eviction caps the
      retained set at 90 items (9‰), a tenfold shortfall on the layer's own gate.
      The aggregated record is bounded by a constant instead, and that bound is
      asserted against a real coarsening run;
  (c) **Letta S4 form A is vestigial at this budget** — a full-granularity hot
      tier can hold at most 8 items at the bare gate and **0** at the occupancy
      form B actually reaches. Which is why form B (true eviction) was chosen.

Then the composition itself: `12n + record ≤ 11 000` → 914 items at 91‰, and the
13-units-per-item cliff that would make it 844 items and 84‰ — a red gate. That
cliff is the reason this file exists: the layer has 14 items of margin, and any
future cell added to per-item state spends it.

The pure-arithmetic trials need no engine and are green forever. The ones that
measure the engine skip until it exists, then hold.
"""

from fractions import Fraction

from _harness import require, require_equal, try_import
from adapters import l2
import _l3fixture
import _l3tasks
from corpora.l3streamb import generator as streamb

# The two ratified clauses whose *arithmetic consequences* this file traces. They
# are §5 L3 text, quoted here as the inputs to a calculation — the gate itself is
# applied by `ascension/l3/t_forgetting.py`, which is where its authority is
# registered (`laws/t_rulings.py`).
REQUIRED_UNWEIGHTED_C_PERMILLE = 90
STREAM_ITEMS = 10000

# The composition recorded in README-l3 §0.5, on the frozen streams.
RECORDED_ITEM_UNITS = 12          # 11 event + 1 handle posting
RECORDED_RETAINED = 914
RECORDED_OCCUPANCY = 10991
RECORDED_RECORD_CELLS = 23
RECORDED_UNWEIGHTED_C_PERMILLE = 91

# The cliff: one more cell per item and the coverage gate goes red.
CLIFF_ITEM_UNITS = 13
CLIFF_RETAINED = 844
CLIFF_UNWEIGHTED_C_PERMILLE = 84


def _engine():
    return try_import("adapters.l3",
                      "no L3 engine yet; the state-composition measurements "
                      "engage when it is built")


def _budget():
    bundle = _l3tasks.stream("l3streamb")
    return bundle["budget_cap"], bundle["item_cost"]


def _items_needed():
    """The retained-item floor the coverage clause forces, from the clause alone."""
    # unweighted-C = permille(n / STREAM_ITEMS) >= 90, so n is the least integer
    # whose permille reaches the clause. Computed, not assumed.
    n = 0
    while _l3tasks.permille(Fraction(n, STREAM_ITEMS)) < REQUIRED_UNWEIGHTED_C_PERMILLE:
        n += 1
    return n


# ---- (0) the remainder -----------------------------------------------------

def trial_the_coverage_clause_leaves_one_tenth_of_the_budget_for_bookkeeping():
    cap, item = _budget()
    require_equal((cap, item), (11000, 11),
                  "the Layer-3 budget or per-item cost drifted from README-l3 §0.1")
    floor = _items_needed()
    require(floor <= 900,
            "the coverage clause needs %d items, more than the 900 §0.1 records"
            % (floor,))
    remainder = cap - 900 * item
    require_equal(remainder, 1100,
                  "the bookkeeping remainder drifted from README-l3 §0.1")
    # It is a tenth of the budget, and it must cover index + record + tiers.
    require(remainder * 10 == cap,
            "the remainder is no longer exactly a tenth of the cap (%d of %d)"
            % (remainder, cap))


# ---- (a) L2-granularity indexing is impossible -----------------------------

def trial_layer2_granularity_indexing_cannot_reach_the_coverage_clause():
    cap, item = _budget()
    payloads = _l3tasks.stream("l3streamb")["payloads"]
    l2_index_cells = len(l2._atoms(payloads[0])) + l2.MINHASH_K
    require_equal(l2_index_cells, 21,
                  "the Layer-2 index cost per l3streamb event drifted from §0.2")
    per_item = item + l2_index_cells
    require_equal(per_item, 32, "the Layer-2-granularity per-item cost drifted")

    capacity = cap // per_item
    require_equal(capacity, 343,
                  "the Layer-2-granularity capacity drifted from §0.2 (and from "
                  "the 343 items humility/l3/IMPOSSIBILITY.md measured)")
    reachable = _l3tasks.permille(Fraction(capacity, STREAM_ITEMS))
    require_equal(reachable, 34, "the Layer-2-granularity coverage drifted")
    require(reachable < REQUIRED_UNWEIGHTED_C_PERMILLE,
            "Layer-2-granularity indexing now reaches the coverage clause (%d‰ "
            "against %d‰) — §0.2's exclusion no longer holds and the design "
            "argument must be rewritten"
            % (reachable, REQUIRED_UNWEIGHTED_C_PERMILLE))

    # And the positive form: 900 items at L2 granularity overrun the whole cap.
    require(900 * per_item > 2 * cap,
            "900 items at Layer-2 granularity cost %d units against a %d cap — "
            "§0.2 records this as 2.6× and it must stay a multiple, not a squeeze"
            % (900 * per_item, cap))


def trial_the_remainder_admits_one_unit_of_index_per_item():
    cap, item = _budget()
    available = Fraction(cap - 900 * item - RECORDED_RECORD_CELLS, 900)
    require(available < 2,
            "the index budget per item is %s — §0.2's 'one whole unit' claim is "
            "no longer the binding constraint" % (available,))
    require(available >= 1,
            "the index budget per item is %s — below one unit, so not even a "
            "single posting per item would fit and Layer 3 could not recall at "
            "all" % (available,))


def trial_the_engine_handle_index_costs_exactly_one_cell_per_item():
    l3 = _engine()
    for name in _l3tasks.STREAMS:
        bundle = _l3tasks.stream(name)
        for payload in bundle["payloads"][:64]:
            require_equal(l3.index_cells(payload), 1,
                          "%s: a retained event costs more than one posting cell "
                          "— the §0.2 index budget is blown" % (name,))
            require_equal(l3.item_cost(payload), RECORDED_ITEM_UNITS,
                          "%s: per-item cost drifted from the §0.5 composition"
                          % (name,))
        # The handle is the cue handle: the probe the trials use must reach it.
        atom = l3.handle_atom(bundle["payloads"][0])
        require(atom is not None, "%s: items have no handle atom" % (name,))
        require_equal(l3.handle_atom(bundle["targets"][0]["cue"]), atom,
                      "%s: the cue's handle atom differs from the payload's — "
                      "recall could never reach it" % (name,))


# ---- (b) per-eviction tombstones are impossible -----------------------------

def trial_per_eviction_tombstones_cannot_reach_the_coverage_clause():
    cap, item = _budget()
    # A one-cell tombstone per evicted item: 12n + (STREAM_ITEMS - n) <= cap.
    n = (cap - STREAM_ITEMS) // (RECORDED_ITEM_UNITS - 1)
    require_equal(n, 90, "the one-cell-tombstone capacity drifted from §0.3")
    reachable = _l3tasks.permille(Fraction(n, STREAM_ITEMS))
    require_equal(reachable, 9, "the one-cell-tombstone coverage drifted from §0.3")
    require(reachable * 10 <= REQUIRED_UNWEIGHTED_C_PERMILLE,
            "a one-cell tombstone table now costs less than the tenfold coverage "
            "shortfall §0.3 records (%d‰ against %d‰)"
            % (reachable, REQUIRED_UNWEIGHTED_C_PERMILLE))
    # The table alone is most of the budget: the claim in its starkest form.
    require(STREAM_ITEMS - n > 8 * (cap - 900 * item),
            "9 000 tombstones no longer exceed 8× the bookkeeping remainder")


def trial_the_aggregated_record_is_bounded_by_a_constant():
    """The record's cell count is capped forever, however long the stream runs.

    Driven through a real engine at a punishing cap so the coarsening path is
    exercised (not merely reasoned about): the width doubles, buckets merge, the
    totals survive the merge exactly, and the cell count never passes
    `3 + 2 × FORGET_BUCKETS`.
    """
    l3 = _engine()
    ceiling = 3 + 2 * l3.FORGET_BUCKETS
    bundle = _l3tasks.stream("l3streamb")
    state = l3.make_engine(3, 20 * RECORDED_ITEM_UNITS + ceiling)
    widths = set()
    evicted_mass = 0
    for payload in bundle["payloads"][:3000]:
        state, _t = l3.ingest(state, payload)
        record = state.forgetting
        widths.add(record.width)
        require(l3.forget_cost(record) <= ceiling,
                "the forgetting record grew to %d cells, past the %d-cell bound "
                "— §0.3's constant-cost claim is broken"
                % (l3.forget_cost(record), ceiling))
        require(len(record.buckets) <= l3.FORGET_BUCKETS,
                "the forgetting record holds %d buckets, past the %d-bucket bound"
                % (len(record.buckets), l3.FORGET_BUCKETS))
        # Coarsening must never lose an eviction: the buckets sum to the totals.
        require_equal(sum(c for c, _m in record.buckets), record.count,
                      "coarsening lost an evicted count")
        require_equal(sum(m for _c, m in record.buckets), record.mass,
                      "coarsening lost evicted mass")
        evicted_mass = record.mass
    require(len(widths) > 1,
            "the width never doubled in 3 000 items — the coarsening path this "
            "trial exists to exercise was not reached")
    require(evicted_mass > 0, "nothing was evicted at a 20-item cap")

    # And what it answers: a t-range with evictions reads non-zero, a range past
    # the stream reads zero. This is the L6 question, at the resolution §0.3 buys.
    answer = l3.query(state, {"op": "forgetting"})
    require_equal(answer["status"], "answer", "the forgetting record must be readable")
    require_equal(answer["value"]["count"], state.forgetting.count,
                  "the reported evicted count differs from the record")
    near = l3.query(state, {"op": "forgot_at", "t": 0})
    require_equal(near["status"], "answer", "forgot_at must answer for an in-range t")
    require(near["value"]["count"] > 0,
            "the range containing the earliest evictions reports none forgotten")
    far = l3.query(state, {"op": "forgot_at", "t": 10 ** 9})
    require_equal(far["value"]["count"], 0,
                  "a range the stream never reached reports evictions")


# ---- (c) the Letta S4 form choice ------------------------------------------

def trial_letta_form_a_hot_tier_is_vestigial_at_this_budget():
    """Form A priced: `32h + 12c + record <= cap`, at the item counts that matter.

    A full-granularity hot item costs 1.67 cold ones, so the hot tier is bought
    out of the coverage margin — 8 items at the bare gate, none at the occupancy
    form B reaches. This is the arithmetic the form choice was made on (§0.4).
    """
    cap, item = _budget()
    payloads = _l3tasks.stream("l3streamb")["payloads"]
    hot_unit = item + len(l2._atoms(payloads[0])) + l2.MINHASH_K
    cold_unit = RECORDED_ITEM_UNITS

    def hot_affordable(total):
        slack = cap - RECORDED_RECORD_CELLS - cold_unit * total
        if slack < 0:
            return 0
        return slack // (hot_unit - cold_unit)

    require_equal(hot_affordable(900), 8,
                  "the affordable hot tier at the bare coverage gate drifted "
                  "from §0.4")
    require_equal(hot_affordable(RECORDED_RETAINED), 0,
                  "form A's hot tier is no longer empty at the occupancy form B "
                  "reaches — §0.4's 'vestigial' verdict must be recomputed")
    require(hot_affordable(900) * 100 < 2 * 900,
            "a hot tier of %d items is 2%% or more of the retained set — form A "
            "would stop being a decoration and the choice needs revisiting"
            % (hot_affordable(900),))
    # Each full-granularity item costs more than one and a half cold ones: the
    # exchange rate that makes the hot tier unaffordable in the first place.
    require(2 * hot_unit > 3 * cold_unit,
            "a hot item now costs less than 1.5 cold items (%d against %d) — the "
            "§0.4 exchange rate has changed" % (hot_unit, cold_unit))


# ---- the composition, and the cliff ----------------------------------------

def trial_the_recorded_composition_is_what_the_engine_reaches():
    """§0.5's table, measured on the frozen gate stream (one shared replay)."""
    l3 = _engine()
    state, budget = _l3fixture.replayed(l3, "l3streamb", 3)
    require_equal(l3.retained(state), RECORDED_RETAINED,
                  "the retained-item count drifted from the §0.5 composition")
    require_equal(state.occupancy, RECORDED_OCCUPANCY,
                  "occupancy at the end of the stream drifted from §0.5")
    require_equal(l3.forget_cost(state.forgetting), RECORDED_RECORD_CELLS,
                  "the forgetting record's cell count on the frozen stream "
                  "drifted from §0.3")
    require_equal(budget["B"], 1000, "the cap was breached during the replay")

    # The accounting identity: occupancy IS 12 per retained item plus the record,
    # with nothing unaccounted and no tier metadata (form B has none).
    require_equal(state.occupancy,
                  RECORDED_ITEM_UNITS * l3.retained(state)
                  + l3.forget_cost(state.forgetting),
                  "occupancy is not exactly 12/item + record — some cell of state "
                  "is unaccounted for, or a tier crept in")
    require(state.occupancy <= budget["cap"],
            "final occupancy %d exceeds the cap %d" % (state.occupancy, budget["cap"]))
    require_equal(_l3tasks.permille(Fraction(l3.retained(state), STREAM_ITEMS)),
                  RECORDED_UNWEIGHTED_C_PERMILLE,
                  "the retained set no longer reaches the recorded 91‰")


def trial_one_more_cell_per_item_would_make_the_coverage_gate_red():
    """The cliff §0.5 states out loud: the margin is 14 items, and that is all."""
    cap, _item = _budget()
    at_cliff = (cap - RECORDED_RECORD_CELLS) // CLIFF_ITEM_UNITS
    require_equal(at_cliff, CLIFF_RETAINED,
                  "the 13-units-per-item capacity drifted from §0.5")
    reachable = _l3tasks.permille(Fraction(at_cliff, STREAM_ITEMS))
    require_equal(reachable, CLIFF_UNWEIGHTED_C_PERMILLE,
                  "the 13-units-per-item coverage drifted from §0.5")
    require(reachable < REQUIRED_UNWEIGHTED_C_PERMILLE,
            "13 units per item now clears the coverage clause — the cliff §0.5 "
            "warns about has moved and the warning must be restated")
    at_recorded = (cap - RECORDED_RECORD_CELLS) // RECORDED_ITEM_UNITS
    require_equal(at_recorded - 900, 14,
                  "the coverage margin is no longer the 14 items §0.5 records")

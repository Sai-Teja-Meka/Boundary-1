"""trials/adapters/l7.py — the Layer-7 adapter (INTERFACE.md).

Presents `core.layers.l7_generation` as the generic interface the trial harness
speaks (`empty` / `make_engine` / `ingest` / `query` / `snapshot` / `restore` /
`last_cost`), plus the declared composition reading and the lineage ledger's own
accessors for the ops and strain trials to assert against directly. Trials import
this adapter, never the engine internals.

The layers below are untouched: `adapters/l1.py` still binds `core.engine`,
`adapters/l2.py` `core.layers.l2_recall`, `adapters/l3.py` `core.layers.
l3_forgetting`, `adapters/l4.py` `core.layers.l4_consolidation`, `adapters/l5.py`
`core.layers.l5_prospection` and `adapters/l6.py` `core.layers.l6_meta_memory`,
so `anchors/l1.json` … `anchors/l6.json` replay through their own engines and
stay byte-identical forever (§9). This adapter binds the additive Layer-7 engine,
whose `make_engine(6)` **is** the frozen Layer-6 state and verbs — the humility
counterpart to the full `layer_cap = 7` generation engine (§7.4).

The adapter carries the **implicit half** of the `§7` contract that
`trials/adapters/README.md` records — `state.occupancy`, `state.budget_cap` and
`state.next_t` read as plain attributes, `restore(bytes) -> state` beside the
three declared operations, and from Layer 6 an **integer permille** confidence on
every Answer. Layer 7 adds one requirement to that list, and it is the field
`R8` clause 2 puts on a `generate` Answer: `lineage`, absent or one of
`{observed, generated}` (`R8` clause 4). A value outside that vocabulary is a
contract violation and not a low score.
"""

from core.layers.l7_generation import (
    # generic interface (§7)
    empty, make_engine, ingest, query, snapshot, restore,
    last_cost, state_checksum, DEFAULT_BUDGET,
    # raw verbs (§5 L1 + L2/L3 recall + L4 consolidation + L5 prospection)
    write, read, read_range, recall, retained, new_state,
    current, asof, profile, covers_from,
    fired_by, pending_iids, fired_iids,
    # the declared composition reading — COMPOSITION_FORM, made mechanical
    L7State, COMPOSITION_FORM, PROFILE_FORM, PART_KIND, PROFILE_KIND,
    COMPOUND_CLASS, HUE_KEY, MASS_KEY, HUES, GRADES,
    compose, profile_form_ok, parts_of, profiles_of, is_compound, latest,
    material, profile_of, composed_only, generate,
    # the lineage ledger — the one field this layer adds
    OBSERVED, GENERATED, LINEAGE_VOCAB, LINEAGE_ENTRY_CELLS,
    own_generation, lineage_rung, lineage_of, lineage_cells,
    # the Layer-6 confidence model, carried unchanged
    SET_ONCE_KEYS, permille, confidence_for, claimants,
    visible_chain, n_distinct, set_once, ties, CERTAIN, NO_ANSWER,
    # pricing
    accounted_occupancy, pending_cells, fired_cells,
    chain_cells, irreducible_cells, rows_cells, index_cells,
    # constants & snapshot integrity
    CorruptSnapshot, MAGIC, LAYER,
)

# The Layer-6, Layer-5 and Layer-4 surfaces the inherited batteries and the older
# strain trials speak, re-exported unchanged so one adapter answers for the whole
# ladder.
from core.layers.l6_meta_memory import L6State
from core.layers.l5_prospection import (
    L5State, intention, rebuild_intention, arms, readable, satisfies,
    INTENTION_KIND, INTENTION_FORM, PREDICATES, CONNECTIVES,
)
from core.layers.l4_consolidation import (
    L4State, facet, rebuild, invertible, atlas_after,
    row_shape, row_values, row_payload, ASSERTION_FORMS,
)

__all__ = [
    "empty", "make_engine", "ingest", "query", "snapshot", "restore",
    "last_cost", "state_checksum", "DEFAULT_BUDGET",
    "write", "read", "read_range", "recall", "retained", "new_state",
    "current", "asof", "profile", "covers_from",
    "fired_by", "pending_iids", "fired_iids",
    "L7State", "COMPOSITION_FORM", "PROFILE_FORM", "PART_KIND", "PROFILE_KIND",
    "COMPOUND_CLASS", "HUE_KEY", "MASS_KEY", "HUES", "GRADES",
    "compose", "profile_form_ok", "parts_of", "profiles_of", "is_compound",
    "latest", "material", "profile_of", "composed_only", "generate",
    "OBSERVED", "GENERATED", "LINEAGE_VOCAB", "LINEAGE_ENTRY_CELLS",
    "own_generation", "lineage_rung", "lineage_of", "lineage_cells",
    "SET_ONCE_KEYS", "permille", "confidence_for", "claimants",
    "visible_chain", "n_distinct", "set_once", "ties", "CERTAIN", "NO_ANSWER",
    "accounted_occupancy", "pending_cells", "fired_cells",
    "chain_cells", "irreducible_cells", "rows_cells", "index_cells",
    "CorruptSnapshot", "MAGIC", "LAYER",
    "L6State", "L5State", "intention", "rebuild_intention", "arms", "readable",
    "satisfies", "INTENTION_KIND", "INTENTION_FORM", "PREDICATES",
    "CONNECTIVES",
    "L4State", "facet", "rebuild", "invertible", "atlas_after",
    "row_shape", "row_values", "row_payload", "ASSERTION_FORMS",
]

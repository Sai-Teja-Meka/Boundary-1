"""trials/adapters/l5.py — the Layer-5 adapter (INTERFACE.md).

Presents `core.layers.l5_prospection` as the generic interface the trial harness
speaks (`empty` / `make_engine` / `ingest` / `query` / `snapshot` / `restore` /
`last_cost`), plus the prospection internals the ops and strain trials assert
against directly. Trials import this adapter, never the engine internals.

The layers below are untouched: `adapters/l1.py` still binds `core.engine`,
`adapters/l2.py` `core.layers.l2_recall`, `adapters/l3.py` `core.layers.
l3_forgetting` and `adapters/l4.py` `core.layers.l4_consolidation`, so
`anchors/l1.json` … `anchors/l4.json` replay through their own engines and stay
byte-identical forever (§9). This adapter binds the additive Layer-5 engine,
whose `make_engine(4)` **is** the frozen Layer-4 state and verbs — the humility
counterpart to the full `layer_cap = 5` prospection engine (§7.4).
"""

from core.layers.l5_prospection import (
    # generic interface (§7)
    empty, make_engine, ingest, query, snapshot, restore,
    last_cost, state_checksum, DEFAULT_BUDGET,
    # raw verbs (§5 L1 + L2/L3 recall + L4 consolidation + L5 prospection)
    write, read, read_range, recall, retained, new_state,
    current, asof, profile, covers_from,
    fired_by, pending_iids, fired_iids,
    # the declared readings, and the state
    L5State, intention, rebuild_intention, arms, readable, satisfies,
    INTENTION_KIND, INTENTION_FORM, PREDICATES, CONNECTIVES,
    # pricing
    accounted_occupancy, pending_cells, fired_cells,
    chain_cells, irreducible_cells, rows_cells, index_cells,
    # constants & snapshot integrity
    CorruptSnapshot, MAGIC, LAYER,
)

# The Layer-4 surface the inherited batteries and the older strain trials speak,
# re-exported unchanged so one adapter answers for the whole ladder.
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
    "L5State", "intention", "rebuild_intention", "arms", "readable",
    "satisfies", "INTENTION_KIND", "INTENTION_FORM", "PREDICATES",
    "CONNECTIVES",
    "accounted_occupancy", "pending_cells", "fired_cells",
    "chain_cells", "irreducible_cells", "rows_cells", "index_cells",
    "CorruptSnapshot", "MAGIC", "LAYER",
    "L4State", "facet", "rebuild", "invertible", "atlas_after",
    "row_shape", "row_values", "row_payload", "ASSERTION_FORMS",
]

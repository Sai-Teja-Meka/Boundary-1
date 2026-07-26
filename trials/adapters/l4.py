"""trials/adapters/l4.py — the Layer-4 adapter (INTERFACE.md).

Presents `core.layers.l4_consolidation` as the generic interface the trial
harness speaks (`empty` / `make_engine` / `ingest` / `query` / `snapshot` /
`restore` / `last_cost`), plus the derived-schema internals the ops and strain
trials assert against directly. Trials import this adapter, never the engine
internals.

The layers below are untouched: `adapters/l1.py` still binds `core.engine`,
`adapters/l2.py` still binds `core.layers.l2_recall` and `adapters/l3.py` still
binds `core.layers.l3_forgetting`, so `anchors/l1.json`, `anchors/l2.json` and
`anchors/l3.json` replay through their own engines and stay byte-identical
forever (§9). This adapter binds the additive Layer-4 engine, whose
`make_engine(3)` **is** the frozen Layer-3 state and verbs — the humility
counterpart to the full `layer_cap = 4` consolidation engine (§7.4).
"""

from core.layers.l4_consolidation import (
    # generic interface (§7)
    empty, make_engine, ingest, query, snapshot, restore,
    last_cost, state_checksum, DEFAULT_BUDGET,
    # raw verbs (§5 L1 + L2/L3 recall + L4 consolidation)
    write, read, read_range, recall, retained, new_state,
    current, asof, profile, covers_from,
    # the derived schemas and their pricing
    L4State, facet, rebuild, invertible, row_shape, row_values, row_payload,
    accounted_occupancy, chain_cells, irreducible_cells, rows_cells, index_cells,
    ASSERTION_FORMS,
    # constants & snapshot integrity
    CorruptSnapshot, MAGIC, LAYER,
)

__all__ = [
    "empty", "make_engine", "ingest", "query", "snapshot", "restore",
    "last_cost", "state_checksum", "DEFAULT_BUDGET",
    "write", "read", "read_range", "recall", "retained", "new_state",
    "current", "asof", "profile", "covers_from",
    "L4State", "facet", "rebuild", "invertible", "row_shape", "row_values",
    "row_payload", "accounted_occupancy", "chain_cells", "irreducible_cells",
    "rows_cells", "index_cells", "ASSERTION_FORMS",
    "CorruptSnapshot", "MAGIC", "LAYER",
]

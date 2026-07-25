"""trials/adapters/l3.py — the Layer-3 adapter (INTERFACE.md).

Presents `core.layers.l3_forgetting` as the generic interface the trial harness
speaks (`empty` / `make_engine` / `ingest` / `query` / `snapshot` / `restore` /
`last_cost`), plus the raw verbs and the importance/eviction internals the ops and
strain trials assert against directly. Trials import this adapter, never the
engine internals.

The layers below are untouched: `adapters/l1.py` still binds `core.engine` and
`adapters/l2.py` still binds `core.layers.l2_recall`, so `anchors/l1.json` and
`anchors/l2.json` replay through their own engines and stay byte-identical
forever (§9). This adapter binds the additive Layer-3 engine, whose
`make_engine(2)` is a genuine refuse-don't-forget engine — the humility
counterpart to the full `layer_cap = 3` forgetting engine (§7.4).
"""

from core.layers.l3_forgetting import (
    # generic interface (§7)
    empty, make_engine, ingest, query, snapshot, restore,
    last_cost, state_checksum, DEFAULT_BUDGET,
    # raw verbs (§5 L1 + L2 recall + L3 forgetting)
    write, read, read_range, recall, retained, new_state,
    # the importance law and the eviction order
    importance, grammar_weight, less_important, victim_position,
    cluster_uses, handle_atom, index_cells, item_cost,
    # the aggregated forgetting record
    Forgetting, forget_empty, forget_cost, forget_bucket_at,
    FORGET_BUCKETS, FORGET_WIDTH0,
    # constants & snapshot integrity
    CorruptSnapshot, MAGIC, LAYER, HANDLE_FIELDS, GRAMMAR_WEIGHT_FIELD,
)

__all__ = [
    "empty", "make_engine", "ingest", "query", "snapshot", "restore",
    "last_cost", "state_checksum", "DEFAULT_BUDGET",
    "write", "read", "read_range", "recall", "retained", "new_state",
    "importance", "grammar_weight", "less_important", "victim_position",
    "cluster_uses", "handle_atom", "index_cells", "item_cost",
    "Forgetting", "forget_empty", "forget_cost", "forget_bucket_at",
    "FORGET_BUCKETS", "FORGET_WIDTH0",
    "CorruptSnapshot", "MAGIC", "LAYER", "HANDLE_FIELDS", "GRAMMAR_WEIGHT_FIELD",
]

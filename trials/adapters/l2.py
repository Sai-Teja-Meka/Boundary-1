"""trials/adapters/l2.py — the Layer-2 adapter (INTERFACE.md).

Presents `core.layers.l2_recall` as the generic interface the trial harness
speaks (`empty` / `make_engine` / `ingest` / `query` / `snapshot` / `restore` /
`last_cost`), plus the raw verbs (`read` / `read_range` / `recall`) for the ops
trials that assert exact IO pairs. Trials import this adapter, never the engine
internals directly.

The Layer-1 engine is untouched: its adapter (`adapters/l1.py`) still binds
`core.engine`, and the frozen L1 anchors replay through it unchanged. This
adapter binds the additive Layer-2 engine, whose `make_engine(1)` is a genuine
read-by-time Retention engine (no index, recall abstains) — the humility
counterpart to the full `layer_cap = 2` recall engine.
"""

from core.layers.l2_recall import (
    # generic interface (§7)
    empty, make_engine, ingest, query, snapshot, restore,
    last_cost, state_checksum, DEFAULT_BUDGET,
    # raw verbs (§5 L1 + L2 recall)
    write, read, read_range, recall, recall_ranking, new_state,
    # index internals used by ops/strain trials
    _atoms, _unigrams, _minhash, Index,
    # snapshot integrity
    CorruptSnapshot, MAGIC, LAYER, MINHASH_K,
)

__all__ = [
    "empty", "make_engine", "ingest", "query", "snapshot", "restore",
    "last_cost", "state_checksum", "DEFAULT_BUDGET",
    "write", "read", "read_range", "recall", "recall_ranking", "new_state",
    "_atoms", "_unigrams", "_minhash", "Index",
    "CorruptSnapshot", "MAGIC", "LAYER", "MINHASH_K",
]

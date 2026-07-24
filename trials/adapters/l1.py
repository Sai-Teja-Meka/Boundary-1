"""trials/adapters/l1.py — the Layer-1 adapter (INTERFACE.md).

Presents `core.engine` as the generic interface the trial harness speaks
(`empty` / `make_engine` / `ingest` / `query` / `snapshot` / `restore` /
`last_cost`), plus the raw Layer-1 verbs for the ops trials that assert exact
IO pairs. Trials import this adapter, never the engine internals directly.
"""

from core.engine import (
    empty, make_engine, ingest, query, snapshot, restore, last_cost,
    state_checksum, DEFAULT_BUDGET,
)
from core.layers.l1_retention import (
    write, read, read_range, new_state, CorruptSnapshot, MAGIC, LAYER,
)

__all__ = [
    # generic interface (§7)
    "empty", "make_engine", "ingest", "query", "snapshot", "restore",
    "last_cost", "state_checksum", "DEFAULT_BUDGET",
    # raw Layer-1 verbs (§5 L1)
    "write", "read", "read_range", "new_state",
    # snapshot integrity
    "CorruptSnapshot", "MAGIC", "LAYER",
]

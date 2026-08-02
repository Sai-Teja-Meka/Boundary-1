"""trials/adapters/l6.py — the Layer-6 adapter (INTERFACE.md).

Presents `core.layers.l6_meta_memory` as the generic interface the trial harness
speaks (`empty` / `make_engine` / `ingest` / `query` / `snapshot` / `restore` /
`last_cost`), plus the confidence model's own reading for the ops and strain
trials to assert against directly. Trials import this adapter, never the engine
internals.

The layers below are untouched: `adapters/l1.py` still binds `core.engine`,
`adapters/l2.py` `core.layers.l2_recall`, `adapters/l3.py` `core.layers.
l3_forgetting`, `adapters/l4.py` `core.layers.l4_consolidation` and
`adapters/l5.py` `core.layers.l5_prospection`, so `anchors/l1.json` …
`anchors/l5.json` replay through their own engines and stay byte-identical
forever (§9). This adapter binds the additive Layer-6 engine, whose
`make_engine(5)` **is** the frozen Layer-5 state and verbs — the humility
counterpart to the full `layer_cap = 6` meta-memory engine (§7.4).

The adapter also carries the **implicit half** of the §7 contract that
`trials/adapters/README.md` records: the shared scorers read `state.occupancy`,
`state.budget_cap` and `state.next_t` as plain attributes, and `restore(bytes)
-> state` sits beside the three declared operations. `_l6score` is the first
scorer written after that note; nothing here invents a fourth verb.
"""

from core.layers.l6_meta_memory import (
    # generic interface (§7)
    empty, make_engine, ingest, query, snapshot, restore,
    last_cost, state_checksum, DEFAULT_BUDGET,
    # raw verbs (§5 L1 + L2/L3 recall + L4 consolidation + L5 prospection)
    write, read, read_range, recall, retained, new_state,
    current, asof, profile, covers_from,
    fired_by, pending_iids, fired_iids,
    # the confidence model — the declared reading, the evidence, the number
    L6State, SET_ONCE_KEYS, permille, confidence_for, claimants,
    visible_chain, n_distinct, set_once, ties, CERTAIN, NO_ANSWER,
    # pricing
    accounted_occupancy, pending_cells, fired_cells,
    chain_cells, irreducible_cells, rows_cells, index_cells,
    # constants & snapshot integrity
    CorruptSnapshot, MAGIC, LAYER,
)

# The Layer-5 and Layer-4 surfaces the inherited batteries and the older strain
# trials speak, re-exported unchanged so one adapter answers for the whole ladder.
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
    "L6State", "SET_ONCE_KEYS", "permille", "confidence_for", "claimants",
    "visible_chain", "n_distinct", "set_once", "ties", "CERTAIN", "NO_ANSWER",
    "accounted_occupancy", "pending_cells", "fired_cells",
    "chain_cells", "irreducible_cells", "rows_cells", "index_cells",
    "CorruptSnapshot", "MAGIC", "LAYER",
    "L5State", "intention", "rebuild_intention", "arms", "readable",
    "satisfies", "INTENTION_KIND", "INTENTION_FORM", "PREDICATES",
    "CONNECTIVES",
    "L4State", "facet", "rebuild", "invertible", "atlas_after",
    "row_shape", "row_values", "row_payload", "ASSERTION_FORMS",
]

"""core/state.py — the immutable Layer-1 engine state and cost accounting.

Pure, integer-only (§2.2). Two structures live here:

  * `EventLog` — an immutable, block-structured append log. Plain per-append
    tuple concatenation is O(n) per write and O(n^2) over a corpus; the frozen
    corpora reach 50k events, so the log stores events in fixed-size blocks,
    giving cheap append (O(BLOCK + n/BLOCK)) and O(1) random access by `t`
    while remaining fully immutable — safe to branch (snapshot/restore
    mid-stream) because every block is a shared, frozen tuple.

  * `State` — the frozen engine state. Every op returns a new `State` and never
    mutates its inputs (§2.1). `occupancy` is a running integer counter of
    primitive state cells, accounted in explicit state — never measured from the
    OS, clock, or process memory (§4.1).

No float appears anywhere in this module (§2.2).
"""

from dataclasses import dataclass

# Block size for the event log. A power of two chosen so that both the per-block
# copy on append and the outer-block-tuple copy stay small at the Phase-0 scale
# (50k events => ~49 blocks). Purely a performance seam; it is not observable in
# any answer, snapshot, or anchor (those flatten the log in `t` order).
BLOCK = 1024


@dataclass(frozen=True)
class EventLog:
    """An immutable, block-structured append log, indexed by logical time `t`."""

    blocks: tuple   # tuple of tuples; each is length BLOCK except a partial last
    size: int       # total number of stored events


def log_empty():
    return EventLog(blocks=(), size=0)


def log_append(log, item):
    """Return a new log with `item` appended at index `log.size` (immutable)."""
    blocks = log.blocks
    if blocks and len(blocks[-1]) < BLOCK:
        last = blocks[-1] + (item,)
        new_blocks = blocks[:-1] + (last,)
    else:
        new_blocks = blocks + ((item,),)
    return EventLog(blocks=new_blocks, size=log.size + 1)


def log_get(log, i):
    """Return the event stored at index `i` (0 <= i < size). O(1)."""
    return log.blocks[i // BLOCK][i % BLOCK]


def log_iter(log):
    """Yield every event in ascending `t` order."""
    for block in log.blocks:
        for item in block:
            yield item


def log_from_list(items):
    """Build a log from a flat list of events (O(n)), preserving order."""
    items = list(items)
    blocks = []
    for i in range(0, len(items), BLOCK):
        blocks.append(tuple(items[i:i + BLOCK]))
    return EventLog(blocks=tuple(blocks), size=len(items))


@dataclass(frozen=True)
class State:
    """The frozen Layer-1 engine state (§2.1)."""

    layer_cap: int    # capability cap (§7.4): 0 = pre-retention, >=1 = retention
    budget_cap: int   # integer budget cap Bcap (§4.1)
    occupancy: int    # current cost in work units (primitive cells), a counter
    next_t: int       # next logical time to assign (§1.3) == successful writes
    last_cost: int    # work-unit cost of the most recent successful write
    events: EventLog  # the retained event records {"payload":.., "t":..}


def payload_cost(value):
    """Primitive-cell cost of a canonical value: one unit per scalar and per key.

    Integer, pure, reproducible (§4.1): identical inputs yield identical costs.
    Empty containers cost 0; an event's cost adds one cell for its assigned `t`
    (see `event_cost`), so no stored event ever costs zero.
    """
    if isinstance(value, bool):
        return 1
    if value is None or isinstance(value, (int, str)):
        return 1
    if isinstance(value, list):
        total = 0
        for v in value:
            total += payload_cost(v)
        return total
    if isinstance(value, dict):
        total = 0
        for k, v in value.items():
            total += 1                 # the key cell
            total += payload_cost(v)
        return total
    raise TypeError("payload_cost: non-canonical value")


def event_cost(payload):
    """Cost of retaining one event: its payload cells plus the assigned-`t` cell."""
    return payload_cost(payload) + 1

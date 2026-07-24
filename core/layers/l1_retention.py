"""core/layers/l1_retention.py — Layer 1: Retention (the honest floor).

The first engine code of Boundary-1: Memory. Pure, deterministic, integer-only
(§2). The five Layer-1 verbs (BOUNDARY.md §5, L1):

  write(state, payload)     -> (state', t_assigned)   # t is None on refusal
  read(state, t)            -> event | None
  read_range(state, t0, t1) -> [events]               # inclusive, t-ascending
  snapshot(state)           -> canonical bytes         # checksummed (see below)
  restore(bytes)            -> state                   # fails loudly on corruption

Retention is the **exact** return of what was written, read by time and by
range. The budget law (§4.1) binds from Layer 1: a write that would raise
occupancy above the cap is **REFUSED deterministically** — it returns
`(state, None)`, performs no partial write, and does not evict (eviction is a
Layer-3 capability, not a budget side-effect). Refusal is Layer 1's honest
answer.

The snapshot format carries a **canonical-form checksum** (SHA-256 over the
canonical encoding of the state body). It is decided here, at Layer 1, and
enters the anchors this session: it can never change. `restore` recomputes the
checksum and fails loudly (`CorruptSnapshot`) on any mismatch — a single flipped
bit in a snapshot cannot be silently restored.
"""

import hashlib
from dataclasses import replace

from core.serialize import encode, decode, check_canonical, copy_value
from core.state import (
    State, event_cost,
    log_empty, log_append, log_get, log_iter, log_from_list,
)

LAYER = 1

# The canonical snapshot envelope tag. MAGIC and the checksum discipline enter
# the anchors this session and are frozen L1 behavior forever after.
MAGIC = "boundary1-l1-snapshot"

_ENVELOPE_KEYS = frozenset({"magic", "checksum", "body"})
_BODY_KEYS = frozenset({"layer_cap", "budget_cap", "occupancy", "next_t", "events"})


class CorruptSnapshot(ValueError):
    """Raised by `restore` when a snapshot fails its integrity check (loudly)."""


# ---- construction ---------------------------------------------------------

def new_state(layer_cap, budget_cap):
    """A fresh state capped at `layer_cap` with integer budget cap `budget_cap`."""
    if not isinstance(layer_cap, int) or isinstance(layer_cap, bool):
        raise TypeError("layer_cap must be a plain int")
    if not isinstance(budget_cap, int) or isinstance(budget_cap, bool):
        raise TypeError("budget_cap must be a plain int")
    if layer_cap < 0:
        raise ValueError("layer_cap must be non-negative")
    if budget_cap <= 0:
        raise ValueError("budget_cap must be positive (§4.1)")
    return State(layer_cap=layer_cap, budget_cap=budget_cap,
                 occupancy=0, next_t=0, last_cost=0, events=log_empty())


def _retention_on(state):
    return state.layer_cap >= LAYER


# ---- verbs ----------------------------------------------------------------

def write(state, payload):
    """Append one event; assign and return its logical `t`. Refuse over budget.

    Returns `(state', t_assigned)`. On budget refusal returns `(state, None)`
    with the state **unchanged** — no partial write, no eviction (§4.1). A
    payload outside the canonical type set (§2.4) is a caller contract breach and
    raises `NonCanonical` (that is a bug in the caller, not a scored abstention).
    """
    check_canonical(payload)                       # raises on float/bytes/etc.

    if not _retention_on(state):
        # Pre-retention (layer_cap = 0, the null engine of the L1 ops baseline,
        # §5 L1): the event is seen and assigned a logical time, but nothing is
        # retained, so every later read abstains at the abstention floor.
        t = state.next_t
        return replace(state, next_t=t + 1, last_cost=0), t

    cost = event_cost(payload)
    if state.occupancy + cost > state.budget_cap:
        return state, None                         # deterministic refusal (§4.1)

    t = state.next_t
    record = {"payload": copy_value(payload), "t": t}
    new = replace(state,
                  occupancy=state.occupancy + cost,
                  next_t=t + 1,
                  last_cost=cost,
                  events=log_append(state.events, record))
    return new, t


def read(state, t):
    """Return the event record stored at logical time `t`, or None if none."""
    if not _retention_on(state):
        return None
    if not isinstance(t, int) or isinstance(t, bool):
        return None
    if t < 0 or t >= state.next_t:
        return None
    # Append-only, no eviction at Layer 1: index `t` holds exactly event `t`.
    return copy_value(log_get(state.events, t))


def read_range(state, t0, t1):
    """Return all stored events with `t` in [t0, t1] inclusive, t-ascending."""
    if not _retention_on(state):
        return []
    if not isinstance(t0, int) or isinstance(t0, bool):
        return []
    if not isinstance(t1, int) or isinstance(t1, bool):
        return []
    lo = t0 if t0 > 0 else 0
    hi = t1 if t1 < state.next_t - 1 else state.next_t - 1
    out = []
    t = lo
    while t <= hi:
        out.append(copy_value(log_get(state.events, t)))
        t += 1
    return out


# ---- snapshot / restore ---------------------------------------------------

def _body(state):
    """The canonical, deterministic dict form of the full state.

    `last_cost` is transient budget-harness bookkeeping, not observable in any
    query, so it is intentionally excluded — two independent ingest sequences
    thus yield byte-identical snapshots (determinism, §2.3).
    """
    return {
        "layer_cap": state.layer_cap,
        "budget_cap": state.budget_cap,
        "occupancy": state.occupancy,
        "next_t": state.next_t,
        "events": [copy_value(e) for e in log_iter(state.events)],
    }


def state_checksum(state):
    """The canonical-state SHA-256 hex — the checksum the snapshot embeds.

    This is the "canonical-form checksum" of §strain, frozen into the anchors
    this session. It hashes the canonical encoding of the state body (§2.4).
    """
    return hashlib.sha256(encode(_body(state))).hexdigest()


def snapshot(state):
    """Canonical, checksummed serialization of the state (§7.1, §2.4)."""
    body = _body(state)
    checksum = hashlib.sha256(encode(body)).hexdigest()
    envelope = {"magic": MAGIC, "checksum": checksum, "body": body}
    return encode(envelope)


def restore(data):
    """Rebuild a state from snapshot bytes; fail loudly on any corruption.

    A single flipped bit changes the body's canonical encoding (so the checksum
    fails), corrupts the envelope keys, or breaks the JSON/UTF-8 entirely — every
    path raises `CorruptSnapshot`. A snapshot is never silently half-restored.
    """
    try:
        envelope = decode(data)
    except Exception as exc:                        # invalid JSON / UTF-8 / float
        raise CorruptSnapshot(f"snapshot is not decodable: {exc!r}")

    if not isinstance(envelope, dict) or frozenset(envelope.keys()) != _ENVELOPE_KEYS:
        raise CorruptSnapshot("snapshot envelope keys are wrong")
    if envelope["magic"] != MAGIC:
        raise CorruptSnapshot("snapshot magic mismatch")

    body = envelope["body"]
    if not isinstance(body, dict) or frozenset(body.keys()) != _BODY_KEYS:
        raise CorruptSnapshot("snapshot body keys are wrong")

    recomputed = hashlib.sha256(encode(body)).hexdigest()
    if recomputed != envelope["checksum"]:
        raise CorruptSnapshot("snapshot checksum mismatch (corruption detected)")

    lc, bc = body["layer_cap"], body["budget_cap"]
    occ, nt, evs = body["occupancy"], body["next_t"], body["events"]
    for name, val in (("layer_cap", lc), ("budget_cap", bc),
                      ("occupancy", occ), ("next_t", nt)):
        if not isinstance(val, int) or isinstance(val, bool):
            raise CorruptSnapshot(f"snapshot {name} is not an integer")
    if not isinstance(evs, list):
        raise CorruptSnapshot("snapshot events is not an array")

    events = log_from_list(copy_value(e) for e in evs)
    return State(layer_cap=lc, budget_cap=bc, occupancy=occ,
                 next_t=nt, last_cost=0, events=events)

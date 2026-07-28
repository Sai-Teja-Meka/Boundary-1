"""trials/adapters/external/reference.py — the reference EXTERNAL engine.

This is not our engine. It is a small, complete, third-party-shaped memory
system written **against `trials/adapters/INTERFACE.md` and nothing else**, so
that the one claim `PACKAGE` has to make good on can be checked rather than
asserted:

> **the suite grades any system that implements the interface, not only ours.**

It imports **no** `core/` module. It does not know the §4.1 cost model, the
canonical encoder, the layer ladder or the trial harness; it knows three pure
functions, an Answer shape, a budget cap and a `layer_cap`. Everything it scores
is therefore evidence about the *harness*, not about our engine: if the
scorecard can put this system on the same rows as `ours`, an outside system can
be graded without touching a line of the benchmark.

## What it implements, and where it stops

| layer | what this engine does | expected verdict |
|---|---|---|
| **L1 Retention** | append-only log, read by `t`, `read_range`, snapshot/restore | clears the gate |
| **L2 Recall** | a posting-list index over flattened payload atoms; answers a cue only when exactly one stored event carries the whole probe | clears the gate |
| **L3 Forgetting** | **absent** — at the cap it refuses, which is the pre-Layer-3 lawful response (§4.1.2) and precisely not eviction | fails the gate |
| **L4 Consolidation** | **absent** — no derivation, no supersession, no reconstruction; `current` / `asof` / `profile` / `count` abstain | fails the gate |

That shape is deliberate. A reference adapter that passed everything would
prove the harness can be satisfied; one that passes the layers it implements
and fails the layers it does not is what proves the harness **discriminates**.
It is the same argument the humility class makes about `make_engine(N−1)`,
made about a system nobody here wrote.

## The interface obligations it honours

* **§7.1** — `ingest` / `query` / `snapshot` are pure: they never mutate the
  state or the payload handed in. State is a small slotted object holding plain
  dicts, copied on write and never mutated where a caller can see it.
* **§7.2** — every answer is `{status, value, confidence, provenance}`.
* **§7.3** — capability absence is an **abstention**, never an exception. Every
  op it does not implement, and every op above its `layer_cap`, abstains.
* **§7.4** — `make_engine(layer_cap)` restricts capability at construction:
  at `layer_cap = 1` the index is not consulted and `recall` abstains.
* **§4.1** — a write that would push occupancy above the cap is refused
  deterministically, with no partial write and no eviction. `ingest` returns
  `t = None` on a refusal, which is the convention `trials/_l3score.replay`
  and `_l4score.replay` already count.

## Its cost model is its own, and that is the point

§4.1 requires *an* integer, pure, reproducible cost accounting; it does not
mandate ours. This engine charges one unit per scalar and one per object key in
the payload (recursively), plus one per index posting — which happens to agree
with `core.state.payload_cost` on the corpora used here, because that is the
obvious reading of "one primitive state cell", not because it copied it. The
scorecard reports the budget measure it produces without adjustment; an
external system whose accounting were laxer would show up as a *cheaper*
footprint, and that is a difference a reader of the scorecard should see rather
than one the harness should normalize away.
"""

import hashlib
import json

NAME = "reference"
KIND = "reference"

MAGIC = "reference-external-v1"
DEFAULT_BUDGET = 1 << 20

# The layers this engine claims. Everything above it abstains (§7.3).
MAX_LAYER = 2

SYSTEM = {
    "name": "reference external engine",
    "license": "same as this repository",
    "commit_read": "n/a — written here, against INTERFACE.md alone",
    "autopsy": "n/a",
}


def available():
    """`(True, reason)` — this one runs, offline and deterministically."""
    return (True, "pure, offline, zero-dependency; runs in-process")


class CorruptSnapshot(RuntimeError):
    """A snapshot that fails its integrity check. Never recovered from."""


# ---- state -----------------------------------------------------------------
#
# A small object, copied on write. It is an object rather than a dict for one
# discovered reason, recorded in `trials/adapters/README.md`: `INTERFACE.md`
# names three functions and an Answer, and the shared scorers read the two
# §4.1 numbers — `state.occupancy` and `state.budget_cap` — as **attributes**.
# That is the implicit half of the adapter contract, and writing this engine is
# how it was found. Nothing else about the shape is borrowed from ours.

class State(object):
    """The whole state: capability cap, budget, log, index. Never mutated in place."""

    __slots__ = ("layer_cap", "budget_cap", "occupancy", "next_t",
                 "events", "index", "last_cost")

    def __init__(self, layer_cap, budget_cap, occupancy=0, next_t=0,
                 events=None, index=None, last_cost=0):
        self.layer_cap = layer_cap
        self.budget_cap = budget_cap
        self.occupancy = occupancy
        self.next_t = next_t
        self.events = {} if events is None else events
        self.index = {} if index is None else index
        self.last_cost = last_cost


def empty(budget_cap=DEFAULT_BUDGET):
    return State(MAX_LAYER, budget_cap)


def make_engine(layer_cap, budget_cap=DEFAULT_BUDGET):
    """§7.4 — construction-time capability restriction, nothing else."""
    return State(layer_cap, budget_cap)


def _copy(state):
    return State(state.layer_cap, state.budget_cap, state.occupancy,
                 state.next_t, dict(state.events),
                 {atom: tuple(ts) for atom, ts in state.index.items()},
                 state.last_cost)


# ---- the cost model (this engine's own, §4.1) ------------------------------

def payload_cost(value):
    """One unit per scalar, one per object key, recursively. Integers only."""
    if isinstance(value, dict):
        return sum(1 + payload_cost(v) for v in value.values())
    if isinstance(value, list):
        return sum(payload_cost(v) for v in value)
    return 1


def last_cost(state):
    return state.last_cost


# ---- the cue surface -------------------------------------------------------

def atoms(value, prefix=""):
    """Flatten a payload to `field=scalar` atoms; lists are index-qualified.

    The same function runs on a stored payload and on a cue probe, so a cue
    matches an event exactly when its atom set is a subset of the event's.
    """
    out = set()
    if isinstance(value, dict):
        for key in sorted(value):
            child = "%s.%s" % (prefix, key) if prefix else key
            out |= atoms(value[key], child)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            out |= atoms(item, "%s.%d" % (prefix, i))
    else:
        out.add("%s=%s" % (prefix, json.dumps(value, sort_keys=True)))
    return out


# ---- §7.1 ingest -----------------------------------------------------------

def ingest(state, payload):
    """Append one event, or refuse it. Returns `(state', t)`; `t` is None on refusal."""
    postings = atoms(payload)
    cost = payload_cost(payload) + len(postings)
    if state.occupancy + cost > state.budget_cap:
        # §4.1.2: refuse deterministically, write nothing, evict nothing.
        # This engine has no Layer-3 capability, so refusal is all it can do.
        refused = _copy(state)
        refused.last_cost = 0
        return refused, None

    new = _copy(state)
    t = new.next_t
    new.events[t] = json.loads(json.dumps(payload))        # never alias the caller's
    for atom in postings:
        new.index[atom] = new.index.get(atom, ()) + (t,)
    new.occupancy += cost
    new.next_t = t + 1
    new.last_cost = cost
    return new, t


# ---- §7.2 the Answer -------------------------------------------------------

def _answer(value, confidence, provenance):
    return {"status": "answer", "value": value, "confidence": confidence,
            "provenance": provenance}


def _abstain():
    return {"status": "abstain", "value": None, "confidence": 0,
            "provenance": {"support": [], "kind": "absent", "t_asof": 0}}


# ---- §7.1 query ------------------------------------------------------------

def read(state, t):
    if t in state.events:
        return {"payload": state.events[t], "t": t}
    return None


def recall(state, cue):
    """The unique stored event carrying the whole probe, or an abstention."""
    probe = atoms(cue)
    if not probe:
        return None
    hits = None
    for atom in sorted(probe):
        posting = set(state.index.get(atom, ()))
        hits = posting if hits is None else (hits & posting)
        if not hits:
            return None
    if len(hits) != 1:
        return None                       # ambiguous: an honest abstention
    t = hits.pop()
    return {"payload": state.events[t], "t": t}


def query(state, q):
    """Every op this engine does not implement abstains (§7.3). Never raises."""
    if not isinstance(q, dict):
        return _abstain()
    op = q.get("op")

    if op == "read":
        t = q.get("t")
        record = read(state, t) if isinstance(t, int) else None
        if record is None:
            return _abstain()
        return _answer(record, 1000,
                       {"support": [t], "kind": "recall", "t_asof": t})

    if op == "read_range":
        lo, hi = q.get("lo"), q.get("hi")
        if not isinstance(lo, int) or not isinstance(hi, int):
            return _abstain()
        found = [{"payload": state.events[t], "t": t}
                 for t in range(max(lo, 0), min(hi, state.next_t - 1) + 1)
                 if t in state.events]
        return _answer(found, 1000,
                       {"support": sorted(r["t"] for r in found),
                        "kind": "recall", "t_asof": max(hi, 0)})

    if op == "recall":
        if state.layer_cap < 2:
            return _abstain()             # §7.4: capped below Layer 2
        record = recall(state, q.get("cue"))
        if record is None:
            return _abstain()
        return _answer(record, 1000,
                       {"support": [record["t"]], "kind": "recall",
                        "t_asof": record["t"]})

    # Layer 3 and Layer 4 verbs: this engine has neither capability. It says so
    # by abstaining, which is what makes its zero a *score* rather than a crash.
    return _abstain()


# ---- §7.1 snapshot / restore ----------------------------------------------

def _body(state):
    return {"layer_cap": state.layer_cap, "budget_cap": state.budget_cap,
            "occupancy": state.occupancy, "next_t": state.next_t,
            "events": {str(t): p for t, p in sorted(state.events.items())},
            "index": {atom: list(ts) for atom, ts in sorted(state.index.items())}}


def state_checksum(state):
    return hashlib.sha256(
        json.dumps(_body(state), sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")).hexdigest()


def snapshot(state):
    doc = {"magic": MAGIC, "body": _body(state), "checksum": state_checksum(state)}
    return json.dumps(doc, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def restore(data):
    try:
        doc = json.loads(data.decode("utf-8"))
    except Exception as exc:                                  # noqa: BLE001
        raise CorruptSnapshot("undecodable snapshot: %s" % (exc,))
    if not isinstance(doc, dict) or doc.get("magic") != MAGIC:
        raise CorruptSnapshot("not a %s snapshot" % (MAGIC,))
    body = doc.get("body")
    if not isinstance(body, dict):
        raise CorruptSnapshot("snapshot has no body")
    state = State(body["layer_cap"], body["budget_cap"], body["occupancy"],
                  body["next_t"],
                  {int(t): p for t, p in body["events"].items()},
                  {atom: tuple(ts) for atom, ts in body["index"].items()})
    if state_checksum(state) != doc.get("checksum"):
        raise CorruptSnapshot("checksum mismatch — the snapshot does not verify")
    return state

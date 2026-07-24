# INTERFACE.md — The Generic Engine Interface

> This file is a **verbatim copy of BOUNDARY.md §7**. Trials speak to any engine
> only through this interface; an engine is a black box behind three pure
> functions. If this file and §7 ever disagree, §7 is authoritative and this
> copy is the defect.

Trials speak to any engine only through it; an engine is a black box behind
these three pure functions.

## 7.1 The three operations

- `ingest(state, payload) -> (state', t)`
  Pure. Appends one event, assigns and returns its logical `t` (§1.3), and
  returns the new state. Never mutates `state` or `payload`.

- `query(state, q) -> answer`
  Pure. Returns an **Answer** (below). Never mutates `state`.

- `snapshot(state) -> bytes`
  Pure. Returns the canonical JSON serialization (§2.4) of the engine's state.
  `snapshot` round-trips: a state restored from its snapshot answers queries
  identically.

## 7.2 The Answer

```json
{
  "status": "answer" | "abstain",
  "value": <allowed value | null>,     // null when status == "abstain"
  "confidence": <int 0..1000>,         // permille (§3.4)
  "provenance": <provenance-tag | null> // §4.2; may be null before Layer 7
}
```

## 7.3 The cardinal rule

**Capability absence must surface as scores, never exceptions.** If the engine
cannot handle a query — an unsupported query type, a capability it has not yet
ascended to — it MUST return `{"status":"abstain", ...}`, which the trial
harness scores by the abstention-aware table (§3.0). It MUST NOT raise. A raised
exception is a harness-level failure (red / undefined behavior), categorically
worse than a scored abstention. Missing capability is principled abstention; it
is scored, not thrown.

## 7.4 Capability-capped construction (for humility trials)

An adapter also exposes `make_engine(layer_cap) -> state`, which builds the
engine with capability restricted to `layer_cap`. The humility trial class (§6)
uses `make_engine(layer_cap = N−1)` to run layer `N`'s ascension tasks against an
engine that provably lacks layer `N`. Capping is a construction-time restriction
only: the capped engine speaks the identical `ingest` / `query` / `snapshot`
interface and still surfaces missing capability as scores (abstention), never
exceptions (§7.3).

---

## Adapter contract (for trial authors)

An **adapter** is the thin shim that presents a concrete engine as the operations
above. Adapters live under `trials/adapters/`. Until an engine exists there are no
adapters, and every engine-gated trial reports `SKIPPED-BY-DESIGN`. An adapter is
expected to expose, at minimum:

```
empty() -> state                     # a fresh empty state
make_engine(layer_cap) -> state      # a fresh state capped at layer_cap (§7.4)
ingest(state, payload) -> (state, t)
query(state, q) -> answer            # the Answer object of §7.2
snapshot(state) -> bytes             # canonical JSON (§2.4)
```

and, once the budget law binds (Layer 1, §4.1), an integer cost accessor such as
`last_cost(state) -> int` so the budget-law harness can score the budget measure
(§3.3).

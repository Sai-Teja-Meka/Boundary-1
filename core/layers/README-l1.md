# Layer 1 — Retention (the honest floor)

`[L1] [FORGE]`. The first engine code of Boundary-1: Memory. This document
states **exactly what Layer 1 can and cannot express**. Layer 2's humility trial
is written against it — the boundary drawn here is the boundary the next layer
must prove it crosses.

Code (frozen after this session, §9):
- `core/serialize.py` — core's own canonical serializer (§2.4), byte-for-byte
  equal to the `corpora/canon.py` reference (proven by the engine-serializer
  cross-check law trial).
- `core/state.py` — the immutable `State`, the block-structured event log, and
  integer cost accounting.
- `core/layers/l1_retention.py` — the five verbs and the checksummed snapshot.
- `core/engine.py` — the generic interface binding (§7): `empty` / `make_engine`
  / `ingest` / `query` / `snapshot` / `restore` / `last_cost`.

## The five verbs (§5 L1)

| verb | signature | meaning |
|------|-----------|---------|
| `write`      | `(state, payload) -> (state', t)` | append one event; assign logical `t`; `t` is `None` on budget refusal |
| `read`       | `(state, t) -> event \| None`     | the event stored at logical time `t`, or `None` |
| `read_range` | `(state, t0, t1) -> [events]`     | all stored events with `t ∈ [t0, t1]`, inclusive, t-ascending |
| `snapshot`   | `(state) -> bytes`                | canonical, checksummed serialization of the whole state |
| `restore`    | `(bytes) -> state`                | rebuild a state; fail loudly (`CorruptSnapshot`) on any corruption |

The canonical in-engine event record is exactly `{"payload": <value>, "t": <int>}`
(§1.4). `t` is engine-assigned and engine-owned, begins at `0`, is unique within a
state and strictly increasing in ingestion order (§1.3). There is no wall clock.

## What Layer 1 CAN express

- **Exact retention.** Every in-budget write is retained and read back
  **byte-exact**, by time (`read`) and by contiguous range (`read_range`).
  Fidelity is `1000` and coverage is `1000` on the full frozen corpora
  (chronicle 50k, sessions 5k, murk 10k) — the honest floor keeps everything it
  accepts, including murk's malformed-but-canonical payloads, because Retention
  judges no grammar.
- **Engine-owned logical time.** Ordering is by `t` alone; identical ingest
  sequences produce byte-identical states and answers (determinism, §2.3).
- **The budget law (§4.1), binding.** A write that would raise occupancy above
  the integer cap is **REFUSED deterministically** (`t = None`), with no partial
  write and no eviction. Occupancy is a pure integer counter of primitive state
  cells; peak occupancy never exceeds the cap, so the budget measure is `1000`.
  **Refusal is Layer 1's honest answer to pressure** — it is not forgetting.
- **Durable, verifiable state.** `snapshot` is canonical and carries a
  SHA-256 **canonical-form checksum** (frozen into the anchors this session);
  `restore` fails loudly on any single-bit corruption, truncation, or bad
  envelope. A snapshot taken mid-stream restores to a state whose continuation
  is identical to the original.
- **Principled abstention, never exceptions (§7.3).** A read outside the log, or
  any query type Layer 1 does not implement, returns an `abstain` Answer — it is
  scored, not thrown. The `layer_cap = 0` null engine retains nothing and
  abstains on every read, scoring at the abstention floor (F = 100‰).
- **A dormant provenance seam.** A read hit may carry a valid `recall`
  provenance tag (`support = [t]`), and confidence permille is emitted — but both
  are **ungated** here (§3.4, §4.2).

## What Layer 1 CANNOT express (the boundary for Layer 2+)

- **No associative recall.** There is no index from content to `t`. The only
  lookup keys are the logical time `t` and contiguous `t`-ranges. A query "which
  event mentions entity 7 / token X?" can only be answered by an external linear
  scan, not by the engine — through the interface it **abstains**. This is the
  precise gap **Layer 2 (Recall)** must cross: `recall(cue)` via a deterministic
  index. (Layer 2's humility trial runs L2's cue tasks against
  `make_engine(layer_cap = 1)` — *this* engine — and must show cue-coverage ≤ 100‰:
  a read-by-time engine cannot beat chance on associative retrieval.)
- **No forgetting / eviction.** Under pressure Layer 1 **refuses**; it never
  drops an admitted event to make room. Nothing is importance-ranked, decayed, or
  evicted. That is **Layer 3 (Forgetting)**.
- **No consolidation.** No entity summaries, attribute histories, supersession,
  or "current value among conflicts." Murk's contradictions and near-duplicates
  are retained **verbatim and side by side**; the engine neither reconciles nor
  compresses them. That is **Layer 4 (Consolidation)**.
- **No prospection.** No `intend(condition → event)`; the engine cannot watch
  future writes. That is **Layer 5**.
- **No meta-memory.** Confidence is emitted but structurally trivial
  (`1000` on a hit) and **ungated**; there is no calibrated confidence model.
  That is **Layer 6**, where calibration first binds (§3.4).
- **No generation, no binding provenance.** No `generate(cue)`, no `generated`
  lineage tag; provenance is attachable but neither required nor scored (§4.2,
  dormant until Layer 7).

## Reading list for the next session

Per `CLAUDE.md §1`, the next session reads this README before acting. The one
sentence to carry forward: **Layer 1 returns exactly what it was given, indexed
only by engine-owned time, refusing rather than forgetting — everything
content-addressed, reconciled, ranked, predicted, calibrated, or generated is
above this floor.**

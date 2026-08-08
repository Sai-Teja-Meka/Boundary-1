"""trials/_l8derive.py — THE FROZEN DERIVATION PROCEDURE (`BOUNDARY-HIGH.md §3`).

The third member of a Layer-8 artifact's triple, and the one the constitution had
no doctrine for. `§8.2`/`§8.3` freeze a *generator's output* and enforce
reproduction byte-for-byte; there is no seeded generator for an engine's
behaviour, so the byte-match law cannot reach a self-descriptive answer key. The
SPEC's answer is that **the answer key is a PROCEDURE and not a table**, and this
file is that procedure: engine-free committed source mapping

    (the frozen stream, an engine's ingestion trace, an engine's canonical
     snapshot bytes)   ->   the expected answer for each declared query

`§2.3` makes an engine's trace and final state byte-reproducible from the frozen
stream, `§7.1`'s `snapshot` is pure and returns canonical bytes (`§2.4`) that
round-trip, and `§2.1`/`§2.2` bind this module as they bind anything computed
exactly. So the key is **recomputed, not recorded**, and a drift in the stream,
the engine or this reading is red rather than disappointing.

## The four constraints `§3` places on a derivation procedure, and how each is met

* **It reads `snapshot`, never an `Answer`.** Every function below takes the
  snapshot's canonical BYTES and the frozen stream. Nothing an engine *says*
  reaches this module: a key derived from the engine's own testimony would be
  `R8` clause 3's self-reported denominator with the roles swapped, and every
  score would be a tautology. The one engine-produced input besides the snapshot
  is the **ingestion trace** — the `t` `ingest` returned for each caller payload,
  or `None` for a refusal — which is `§7.1`'s own return value and not an
  `Answer`.
* **One reading, two implementations, asserted to agree.**
  `trials/ops/l8/t_l8describe.py` asserts this module's reachable set against the
  engine's own `read(t)` verb, event by event over the whole stream, in the shape
  `ops/l4`–`ops/l7` each established. A divergence moves an ANSWER and not merely
  an availability.
* **It may not import the engine.** There is no `core.` or `adapters.` import in
  this file and `t_l8describe.py` asserts that by scanning its source, in `R8`
  clause 1's class-E form. The snapshot is parsed as canonical JSON and read as a
  document.
* **Its class must contain questions no field carries.** That is the artifact's
  burden (`corpora/l8describe/generator.py`), and the field-reader bench in the
  ops trial is where it is measured rather than asserted.

## ADAPTER-GENERIC, and what that costs

The procedure is written against the SNAPSHOT ENVELOPE the `§7`/`INTERFACE.md`
contract fixes — `{"magic", "checksum", "body"}` with a canonical body — and
against the **declared body reading** `BODY_READING` below, which names the keys
it consults and what each means. It is therefore generic over any engine whose
snapshot carries that reading, and `README.md` proves it on **two**: the
`layer_cap = 7` engine (the current one) and `make_engine(4)` (a capped one), the
second being a genuinely different state shape with no prospection tiers and no
lineage ledger.

Where a body does not carry a key the reading names, the derivation returns
`UNDETERMINED` for the questions that need it rather than guessing — the same
discipline `§7.3` gives an engine, applied to the harness. An engine whose
snapshot carries none of the reading (a Layer-1 or Layer-2 state, which has no
consolidated tier at all) makes the whole reachable fold fall back to the
event list `§5 L1` states, and that is stated in the reading rather than
special-cased in a caller.

## The three verdicts, and why there are three

Every query resolves to one of:

  `("value", v)`        the stream determines the answer and it is `v`;
  `("undetermined",)`   the stream determines it, the SNAPSHOT does not — the
                        FORCED class, where an honest engine must abstain and an
                        engine that answers is guessing about itself;
  `("unanswerable",)`   nothing determines it, because the subject is not in the
                        stream at all — `§3.0` pays a correct abstention 1000.

The middle verdict is the layer. It is what makes `groundedness` a measurement
rather than a restatement of `F`, and it is computed by asking, for each forced
query, whether the snapshot's own evidence has a **unique** extension consistent
with it. `bounds_lost_weight` below is that computation.
"""

import json


# --- the declared body reading -----------------------------------------------
#
# The keys of a canonical snapshot body this procedure consults, and what each
# one means. It is a DECLARED READING in the shape `ASSERTION_FORMS` (L4),
# `INTENTION_FORM` (L5), `SET_ONCE_KEYS` (L6) and `COMPOSITION_FORM` (L7) already
# have — with the one difference that is the whole layer: those read the caller's
# payloads and this reads the engine's snapshot.

BODY_READING = {
    "next_t": "logical times assigned; the caller stream's own clock (§1.3)",
    "counts": "per-kind ingestion counters, never decremented (§5 L4)",
    "forgetting": "the aggregated eviction record: per-t-range (count, mass), "
                  "plus totals and the current bucket width (L3/L4)",
    "chains": "the interval table, key-major: key -> entity -> [[t, value], …]",
    "kept": "row groups still held: [kind, [field, …], [[t, v, …], …]]",
    "demotable": "the same shape, for rows a chain can regenerate",
    "irreducible": "the same shape, for rows no chain regenerates",
    "verbatim": "pre-consolidation event records, where a state has any",
    "events": "the Layer-1/2/3 event list, where a state has one instead",
}

UNDETERMINED = ("undetermined",)
UNANSWERABLE = ("unanswerable",)


def value(v):
    return ("value", v)


# --- reading a snapshot ------------------------------------------------------

def body_of(snapshot_bytes):
    """The canonical body of a `§7.1` snapshot, as a plain document.

    `INTERFACE.md` fixes the envelope; a body that is not a mapping is a contract
    violation and not a low score, so it raises rather than abstaining — this is
    the harness, and `§7.3` governs an engine.
    """
    envelope = json.loads(snapshot_bytes.decode("utf-8"))
    if not isinstance(envelope, dict) or "body" not in envelope:
        raise ValueError("snapshot envelope carries no body (§7.1)")
    body = envelope["body"]
    if not isinstance(body, dict):
        raise ValueError("snapshot body is not a mapping (§2.4)")
    return body


def _row_groups(body):
    for name in ("kept", "demotable", "irreducible"):
        for group in body.get(name, ()) or ():
            if isinstance(group, list) and len(group) == 3:
                yield group


def reachable_payloads(body, stream):
    """`{t: payload}` for every logical time the state can still answer.

    Three tiers, in the order a state may carry them, and a state carrying none
    of them answers nothing:

      * **row tiers** (`kept` / `demotable` / `irreducible`) — a Layer-4 and
        later state stores an event as a derived row whose `t` is the row's first
        column; whether the row is regenerable or held verbatim is the engine's
        business and not this reading's, because `read(t)` answers from either;
      * **the interval table** (`chains`) — an assertion the engine consolidated
        is regenerable from the `(entity, key, t, value)` its chain carries;
      * **the event list** (`verbatim` / `events`) — what a pre-Layer-4 state
        carries instead.

    The payload itself is taken from the FROZEN STREAM at that `t`, not rebuilt
    from the row: this procedure asks *which* events survive, and `§5 L1`'s
    byte-exactness is a different clause with its own frozen battery. What it
    must never do is take the engine's word for WHICH ones, and it does not.
    """
    reach = {}
    for group in _row_groups(body):
        rows = group[2]
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, list) and row and isinstance(row[0], int):
                reach[row[0]] = None
    for entry in body.get("chains", ()) or ():
        if not (isinstance(entry, list) and len(entry) == 2):
            continue
        for per_entity in entry[1] or ():
            if not (isinstance(per_entity, list) and len(per_entity) == 2):
                continue
            for stamped in per_entity[1] or ():
                if isinstance(stamped, list) and stamped and \
                        isinstance(stamped[0], int):
                    reach[stamped[0]] = None
    for name in ("verbatim", "events"):
        for record in body.get(name, ()) or ():
            if isinstance(record, dict) and isinstance(record.get("t"), int):
                reach[record["t"]] = None
            elif isinstance(record, list) and record and \
                    isinstance(record[0], int):
                reach[record[0]] = None
    return {t: stream[t] for t in sorted(reach) if 0 <= t < len(stream)}


def grammar_weight(payload):
    """`l3_forgetting.grammar_weight`, restated — the reading, not the import.

    `§3` forbids this module importing the engine, and the weight is what the
    forgetting record's `mass` accumulates, so the rule is copied and the copy is
    asserted equal to the engine's own function in the ops trial. One reading,
    two implementations.
    """
    if isinstance(payload, dict):
        w = payload.get("importance")
        if isinstance(w, int) and not isinstance(w, bool) and w >= 1:
            return w
    return 1


# --- the forced class: what `(count, mass)` fixes and what it does not --------

def solutions(count, mass, weights):
    """Every non-negative composition of `count` items of total weight `mass`.

    The forgetting record keeps `(count, mass)` per `t`-range and nothing else,
    so *"how many of the events you lost carried weight w?"* is

        Σ x_i = count      Σ w_i · x_i = mass       x_i ≥ 0

    — as many unknowns as the declared alphabet has weights against exactly two
    equations. Enumerated rather than solved in closed form because the alphabet
    is declared and small, and because an enumeration is the same computation for
    an alphabet of any size, which is what an artifact-generic procedure needs.
    Integers only (`§2.2`).
    """
    weights = list(weights)
    found = []

    def walk(index, left_count, left_mass, taken):
        if index == len(weights) - 1:
            w = weights[index]
            if left_count >= 0 and w * left_count == left_mass:
                found.append(tuple(taken) + (left_count,))
            return
        w = weights[index]
        for x in range(left_count + 1):
            rest = left_mass - w * x
            if rest < 0:
                break
            walk(index + 1, left_count - x, rest, taken + [x])

    if count < 0 or mass < 0 or not weights:
        return []
    walk(0, count, mass, [])
    return found


def bounds_lost_weight(body, weights, w, bucket=None):
    """What the SNAPSHOT fixes about `lost_weight(w)`: a point, or a set.

    Returns the set of values `w`'s count could take over every composition the
    record admits. A singleton means the state DETERMINES the answer and an
    honest engine answers it; anything larger means the state only BOUNDS it and
    an honest engine abstains. That distinction is the forced class, and it is a
    property of the (artifact, engine, cap) triple rather than of the artifact
    alone — which is `ATTAINABILITY.md §4`'s finding and not a defect of this
    function.
    """
    record = body.get("forgetting")
    if not isinstance(record, dict):
        return None
    if bucket is None:
        count, mass = record.get("count"), record.get("mass")
    else:
        buckets = record.get("buckets") or []
        if not isinstance(bucket, int) or not 0 <= bucket < len(buckets):
            return None
        pair = buckets[bucket]
        if not (isinstance(pair, list) and len(pair) == 2):
            return None
        count, mass = pair
    if not isinstance(count, int) or not isinstance(mass, int):
        return None
    index = list(weights).index(w) if w in weights else None
    if index is None:
        return None
    return sorted({combo[index] for combo in solutions(count, mass, weights)})


def bucket_range(body, bucket):
    """The `[t0, t1)` a forgetting-record bucket covers, from the record's width."""
    record = body.get("forgetting")
    if not isinstance(record, dict):
        return None
    width = record.get("width")
    buckets = record.get("buckets") or []
    if not isinstance(width, int) or width <= 0:
        return None
    if not isinstance(bucket, int) or not 0 <= bucket < len(buckets):
        return None
    return (bucket * width, (bucket + 1) * width)


# --- the derivation ----------------------------------------------------------

def derive(query, artifact, body, trace, strict=True):
    """The expected answer for one declared query. One of the three verdicts.

    `artifact` supplies the DECLARED vocabulary — the weight alphabet, the kinds,
    the keys — and never an answer; `body` is the engine's canonical snapshot;
    `trace` is the `t` `ingest` returned for each caller payload. Nothing here
    consults an `Answer`.
    """
    stream = artifact["stream"]
    declared = artifact["declared"]
    weights = tuple(declared["weights"])
    kinds = tuple(declared["kinds"])
    keys = tuple(declared["keys"])

    ingested = [t for t in trace if isinstance(t, int)]
    reach = reachable_payloads(body, stream)

    q = query["q"]
    if q.get("op") != "census":
        return UNANSWERABLE
    of = q.get("of")

    if of == "reach":
        return value(len(reach))

    if of == "kind":
        kind = q.get("kind")
        if kind not in kinds:
            return UNANSWERABLE
        return value(sum(1 for p in reach.values() if p.get("kind") == kind))

    if of == "weight":
        w = q.get("w")
        if w not in weights:
            return UNANSWERABLE
        return value(sum(1 for p in reach.values() if grammar_weight(p) == w))

    if of == "key":
        key = q.get("key")
        if key not in keys:
            return UNANSWERABLE
        return value(sum(1 for p in reach.values() if p.get("key") == key))

    if of == "chain":
        minimum = q.get("min")
        lengths = _chain_lengths(reach)
        if not isinstance(minimum, int) or minimum > max(lengths.values() or [0]):
            return UNANSWERABLE
        return value(sum(1 for n in lengths.values() if n >= minimum))

    if of == "pairs":
        return value(len(_chain_lengths(reach)))

    if of == "entity_pairs":
        entity = q.get("entity")
        spawned = {p.get("entity") for p in stream if p.get("kind") == "spawn"}
        if entity not in spawned:
            return UNANSWERABLE
        lengths = _chain_lengths(reach)
        return value(sum(1 for (e, _k) in lengths if e == entity))

    if of == "lost":
        return value(len(ingested) - len(reach))

    if of == "lost_kind":
        kind = q.get("kind")
        if kind not in kinds:
            return UNANSWERABLE
        total = sum(1 for t in ingested if stream[t].get("kind") == kind)
        held = sum(1 for p in reach.values() if p.get("kind") == kind)
        return value(total - held)

    if of == "lost_at":
        span = bucket_range(body, q.get("bucket"))
        if span is None:
            return UNANSWERABLE
        t0, t1 = span
        return value(sum(1 for t in ingested
                         if t0 <= t < t1 and t not in reach))

    if of in ("lost_weight", "lost_weight_at"):
        w = q.get("w")
        if w not in weights:
            return UNANSWERABLE
        if of == "lost_weight":
            span, bucket = (0, len(stream)), None
        else:
            bucket = q.get("bucket")
            span = bucket_range(body, bucket)
            if span is None:
                return UNANSWERABLE
        t0, t1 = span
        truth = sum(1 for t in ingested
                    if t0 <= t < t1 and t not in reach
                    and grammar_weight(stream[t]) == w)
        if not strict:
            # `strict=False` is the WORLD's answer: what the frozen stream says,
            # regardless of whether the engine's state fixes it. It is what `F`
            # scores against, because `§3.0`'s `correct` is a claim about the
            # VALUE. `strict=True` is what `groundedness` scores against, because
            # `§5 L8` asks for introspection FROM STATE and an answer the state
            # does not determine is ungrounded even when it is lucky. Two
            # instruments, two readings, one procedure — and the gap between them
            # is the whole reason `BOUNDARY-HIGH.md §2.1` says groundedness and
            # not fidelity is the discriminating quantity.
            return value(truth)
        admitted = bounds_lost_weight(body, weights, w, bucket)
        if admitted is None:
            return UNDETERMINED
        if len(admitted) == 1:
            return value(truth)
        return UNDETERMINED

    return UNANSWERABLE


def _chain_lengths(reach):
    """`{(entity, key): visible assertions}` over the reachable set."""
    lengths = {}
    for payload in reach.values():
        if payload.get("kind") != "attr":
            continue
        pair = (payload.get("entity"), payload.get("key"))
        lengths[pair] = lengths.get(pair, 0) + 1
    return lengths


def derive_all(artifact, body, trace, strict=True):
    """The whole answer key: `{qid: verdict}`. Recomputed, never recorded."""
    return {entry["qid"]: derive(entry, artifact, body, trace, strict)
            for entry in artifact["queries"]}


def key_bytes(key):
    """The derived key's canonical bytes, for the `sha256` `§3`'s hash obligation pins.

    A list of `[qid, verdict, value]` triples in `qid` order — canonical by
    construction (`§2.4`), integers and strings only, no float anywhere.
    """
    rows = []
    for qid in sorted(key):
        verdict = key[qid]
        rows.append([qid, verdict[0],
                     verdict[1] if verdict[0] == "value" else None])
    return json.dumps(rows, ensure_ascii=False, separators=(",", ":"),
                      sort_keys=True).encode("utf-8")

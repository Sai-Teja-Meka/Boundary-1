"""core/layers/l3_forgetting.py — Layer 3: Forgetting (eviction under pressure).

Layer 3 adds one capability to the recall floor: **principled eviction**. Under a
stream ten times the budget, the engine keeps the important items and **drops**
the rest — deterministically, inside the cap at every instant, without corrupting
anything it keeps. It is pure, integer-only (§2), and built **entirely on top of
the frozen Layer-1 primitives** (`core/state.py`, `core/serialize.py`); it edits
neither them nor `core/layers/l2_recall.py` (§9).

The full design record — the state-composition arithmetic that fixed every cost
below, the Letta S4 form choice, the capabilities and the Layer-4 seam — is
`core/layers/README-l3.md`. This docstring states what the code does; that
document states why it is the only shape the budget admits.

## The budget decided the state, before the code (BOUNDARY-RULINGS.md R2)

At `budget_cap = 11 000` units and `11` units per retained event, the ratified
`unweighted-C ≥ 90‰` clause forces ≥ 900 retained items = 9 900 units, leaving
**1 100 units for everything else**. Two consequences, both arithmetic, both
asserted in `trials/ops/l3/t_state_composition.py`:

  * **Layer-2-granularity indexing is excluded.** At `len(atoms) + MINHASH_K = 21`
    cells per event, 900 items would cost 28 800 units — 2.6× the entire cap; the
    capacity is 343 items (34‰ against a 90‰ gate). The remainder admits **one**
    whole unit of index per item, so the index here is a **single handle posting**
    per item and discrimination moves to exact verification at query time, which
    costs state nothing.
  * **Per-eviction tombstones are excluded.** ~9 086 evictions at even one cell
    each cap the retained set at 90 items (9‰). The forgetting record is therefore
    **aggregated**: per-`t`-range `(count, mass)` accumulators whose cell count is
    bounded by a constant (16 buckets, coarsened by doubling), not by the number
    of evictions.

Composition, and it is tight: `12n + record ≤ 11 000` → **914 items, 91‰**. At 13
units per item the capacity is 843 items and the gate is red.

## Importance is structural (ACT-R base level, exact; THEORY §1, GAPMAP S7)

    importance_i(now) = grammar_weight(payload_i) × Σ_{u ∈ uses(cluster_i)} 1/(now + 1 − u)

an exact `Fraction`: **grammar weight** (the payload's declared integer
`importance`, else 1) × **reference count** (the number of summands = distinct
payloads in the item's handle cluster) × **harmonic `d = 1` recency** in logical
`t`. Only the induced **ordering** and the retention **threshold** bind; ACT-R's
float `d = 0.5` is a fit to human data and is not reproduced. The eviction hot
loop compares `(numerator, denominator)` pairs by exact integer
cross-multiplication — the same ordering, without constructing a `Fraction`.

`uses` counts **distinct payloads, first occurrence only**: a byte-identical
repetition is not a use, so it adds neither frequency nor recency. The rule holds
**at the door as well as afterwards** — an arriving repetition is credited with its
cluster's standing but not with its own arrival, so a flood of copies cannot buy
admission either. That is the whole of the importance-inflation guard —
manufactured duplicates cannot mint mass — and it is also why a near-duplicate
*cluster* shares its recency instead of each member having to earn survival alone.

## Eviction is total and pure

The victim is the least important retained item, ties broken by **`t` ascending,
then canonical payload bytes ascending** (§2.4). `now` is the `t` about to be
assigned, so `write` is a pure function of `(state, payload)`. The cap is never
exceeded by an observable state: the engine evicts *before* it inserts, and when
the arriving item is itself the least important thing in play it is the one
dropped (its `t` is spent and recorded in the forgetting record) rather than a
better item being evicted to house it.

## What Layer 1 and Layer 2 keep

The five Layer-1 verbs still answer, over the **retained** set: `read` abstains
for an evicted `t` (honest forgetting, never a fabrication), `read_range` returns
what survives in range. `recall` answers only when exactly one retained event
contains the whole probe. Snapshot is checksummed over all of state and `restore`
rederives the index from the log, rejecting any divergence.
"""

import hashlib
from dataclasses import dataclass, replace
from fractions import Fraction

from core.serialize import encode, decode, check_canonical, copy_value, NonCanonical
from core.state import event_cost

LAYER = 3

# A generous default cap, matching the Layer-1/Layer-2 defaults so cross-layer
# reasoning stays simple. Integer only (§2.2). The Layer-3 trials always pass an
# explicit, deliberately punishing cap.
DEFAULT_BUDGET = 1_000_000_000

# ---- the handle: the one index term a retained item can afford ---------------
#
# The frozen precedence of identity-bearing fields, derived from
# `corpora/*/grammar.md` exactly as Layer 2's `_ID_FIELDS` was (README-l2): the
# grammar vocabularies are fixed, so the engine knows at design time which fields
# name a thing. The FIRST field present in a payload is its handle, so a retained
# item costs exactly one posting cell — the whole index budget §0.2 leaves it.
HANDLE_FIELDS = ("tag", "id", "entity", "sid", "src", "dst")

# The payload field that declares an item's grammar weight. L3 *reads* a declared
# weight; inferring importance from content is not a Layer-3 capability.
GRAMMAR_WEIGHT_FIELD = "importance"

# ---- the aggregated forgetting record ---------------------------------------
#
# Bounded by construction: at most FORGET_BUCKETS buckets, ever. When an
# eviction's t needs a bucket beyond the last, the width DOUBLES and bucket pairs
# merge, so resolution degrades and coverage never does. Cost: 3 + 2*len(buckets)
# cells — constant in the number of evictions, which per §0.3 is the only
# affordable shape.
FORGET_BUCKETS = 16
FORGET_WIDTH0 = 64

MAGIC = "boundary1-l3-snapshot"
_ENVELOPE_KEYS = frozenset({"magic", "checksum", "body"})
_BODY_KEYS = frozenset({"layer_cap", "budget_cap", "occupancy", "next_t",
                        "events", "index", "forgetting"})


class CorruptSnapshot(ValueError):
    """Raised by `restore` when a snapshot fails its integrity check (loudly)."""


# ---- the forgetting record --------------------------------------------------

@dataclass(frozen=True)
class Forgetting:
    """The aggregated eviction record: per-`t`-range count and mass, plus totals.

    Bucket `j` covers `t in [j*width, (j+1)*width)`. Immutable: every update
    returns a new record, so a snapshot taken mid-stream never sees a later
    eviction.
    """

    width: int
    buckets: tuple      # of (count, mass) integer pairs
    count: int          # total items evicted
    mass: int           # total grammar-weight mass evicted


def forget_empty():
    return Forgetting(width=FORGET_WIDTH0, buckets=(), count=0, mass=0)


def forget_cost(record):
    """Cells the forgetting record occupies: two per bucket, three for the header."""
    return 3 + 2 * len(record.buckets)


def _forget_add(record, t, weight):
    """Record one eviction at logical time `t` with grammar weight `weight`."""
    width = record.width
    buckets = record.buckets
    j = t // width
    while j >= FORGET_BUCKETS:
        merged = []
        i = 0
        while i < len(buckets):
            count = buckets[i][0]
            mass = buckets[i][1]
            if i + 1 < len(buckets):
                count += buckets[i + 1][0]
                mass += buckets[i + 1][1]
            merged.append((count, mass))
            i += 2
        buckets = tuple(merged)
        width = width * 2
        j = t // width
    if j >= len(buckets):
        buckets = buckets + ((0, 0),) * (j + 1 - len(buckets))
    count, mass = buckets[j]
    buckets = buckets[:j] + ((count + 1, mass + weight),) + buckets[j + 1:]
    return Forgetting(width=width, buckets=buckets,
                      count=record.count + 1, mass=record.mass + weight)


def forget_bucket_at(record, t):
    """The `(count, mass)` recorded for the bucket covering logical time `t`."""
    if t < 0:
        return (0, 0)
    j = t // record.width
    if j >= len(record.buckets):
        return (0, 0)
    return record.buckets[j]


# ---- the state --------------------------------------------------------------

@dataclass(frozen=True)
class L3State:
    """The frozen Layer-3 engine state (§2.1).

    `events` holds only the **retained** records, ascending in `t` (a tuple, so
    eviction is a slice-concatenation and a snapshot taken mid-stream is safe to
    share). `index` maps each handle atom to the ascending tuple of retained `t`s
    carrying it. `forgetting` is the aggregated record of what is gone.
    """

    layer_cap: int
    budget_cap: int
    occupancy: int
    next_t: int
    last_cost: int
    events: tuple
    index: dict
    forgetting: Forgetting


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
    record = forget_empty()
    occupancy = forget_cost(record) if layer_cap >= LAYER else 0
    return L3State(layer_cap=layer_cap, budget_cap=budget_cap,
                   occupancy=occupancy, next_t=0, last_cost=0,
                   events=(), index={}, forgetting=record)


def _retention_on(state):
    return state.layer_cap >= 1


def _recall_on(state):
    return state.layer_cap >= 2


def _forgetting_on(state):
    return state.layer_cap >= LAYER


# ---- the handle atom --------------------------------------------------------

def _token(value):
    """A type-tagged token for a scalar, so `7` and `"7"` are different atoms."""
    if isinstance(value, bool):
        return "b1" if value else "b0"
    if value is None:
        return "n"
    if isinstance(value, int):
        return "i" + str(value)
    if isinstance(value, str):
        return "s" + value
    return None                                  # containers are not handles


def handle_atom(value):
    """The single index term for a payload or a cue, or None if it has no handle.

    The first field of `HANDLE_FIELDS` present in the object wins, so exactly one
    posting is created per retained item (§0.2) — and a cue naming that same field
    reaches it.
    """
    if not isinstance(value, dict):
        return None
    for field in HANDLE_FIELDS:
        if field in value:
            token = _token(value[field])
            if token is not None:
                return field + "=" + token
    return None


def index_cells(payload):
    """Index cells one retained event costs: one posting, or none if handle-free."""
    return 1 if handle_atom(payload) is not None else 0


def item_cost(payload):
    """Total work-unit cost of retaining one event: the event plus its posting."""
    return event_cost(payload) + index_cells(payload)


# ---- the importance law (§1 of README-l3) -----------------------------------

def grammar_weight(payload):
    """The payload's declared integer importance, or 1 when it declares none."""
    if isinstance(payload, dict):
        weight = payload.get(GRAMMAR_WEIGHT_FIELD)
        if isinstance(weight, int) and not isinstance(weight, bool) and weight >= 1:
            return weight
    return 1


def _find(events, t):
    """Index of the record with logical time `t`, or -1. Binary search, O(log n).

    (`bisect` is outside the import whitelist (§2.5), so the search is written
    out; `events` is always ascending in `t`.)
    """
    lo = 0
    hi = len(events) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        got = events[mid]["t"]
        if got == t:
            return mid
        if got < t:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def _lower_bound(events, t):
    """Index of the first record with `t` >= the given `t` (may be len(events))."""
    lo = 0
    hi = len(events)
    while lo < hi:
        mid = (lo + hi) // 2
        if events[mid]["t"] < t:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _payload_at(events, t):
    i = _find(events, t)
    return None if i < 0 else events[i]["payload"]


def cluster_uses(state, atom, now):
    """The `use` times of a handle cluster: first occurrence of each distinct payload.

    A byte-identical repetition is **not** a use — it adds neither frequency nor
    recency, which is the whole importance-inflation guard (README-l3 §2). `now`
    is accepted for symmetry with `importance` and is not used to select uses.
    """
    ts = state.index.get(atom)
    if ts is None:
        return ()
    seen = set()
    uses = []
    for t in ts:                                 # ascending, so first wins
        payload = _payload_at(state.events, t)
        if payload is None:
            continue
        key = encode(payload)
        if key not in seen:
            seen.add(key)
            uses.append(t)
    return tuple(uses)


def _recency_sum(uses, now):
    """Σ 1/(now + 1 − u) over the uses — the harmonic `d = 1` ACT-R surrogate."""
    total = Fraction(0, 1)
    for u in uses:
        total += Fraction(1, now + 1 - u)
    return total


def importance(state, t, now):
    """The exact `Fraction` importance of retained item `t` as of logical time `now`.

    `grammar weight × Σ_{u ∈ uses} 1/(now + 1 − u)` — weight × reference count ×
    harmonic recency (README-l3 §1). Returns None if `t` is not retained.
    """
    i = _find(state.events, t)
    if i < 0:
        return None
    payload = state.events[i]["payload"]
    atom = handle_atom(payload)
    uses = cluster_uses(state, atom, now) if atom is not None else (t,)
    if not uses:
        uses = (t,)
    return Fraction(grammar_weight(payload), 1) * _recency_sum(uses, now)


def less_important(a, b):
    """The total eviction order: is candidate `a` evicted before candidate `b`?

    A candidate is `(numerator, denominator, t, payload_bytes)` — importance as an
    exact rational, then the tie-break of §1: **`t` ascending, then canonical
    payload bytes ascending**. The comparison is integer cross-multiplication, so
    no `Fraction` is constructed in the eviction hot loop and the ordering is
    identical to the rational one.
    """
    left = a[0] * b[1]
    right = b[0] * a[1]
    if left != right:
        return left < right
    if a[2] != b[2]:
        return a[2] < b[2]
    return a[3] < b[3]


def _cluster_pairs(state, now):
    """`{t: (numerator, denominator)}` for members of multi-member handle clusters.

    Singleton clusters — the overwhelming majority, and every item on both frozen
    pressure streams — need no entry: their importance is `weight / age`, computed
    inline. Only a shared cluster needs its recency sum computed once and applied
    to each member.
    """
    pairs = {}
    for atom, ts in state.index.items():
        if len(ts) < 2:
            continue
        uses = cluster_uses(state, atom, now)
        total = _recency_sum(uses, now)
        num = total.numerator
        den = total.denominator
        for t in ts:
            payload = _payload_at(state.events, t)
            if payload is None:
                continue
            pairs[t] = (grammar_weight(payload) * num, den)
    return pairs


def _candidate(state, i, now, pairs):
    """The eviction-order candidate tuple for the retained item at position `i`."""
    record = state.events[i]
    t = record["t"]
    pair = pairs.get(t)
    if pair is None:
        num = grammar_weight(record["payload"])
        den = now + 1 - t
    else:
        num, den = pair
    return (num, den, t, None)


def victim_position(state, now, pairs=None):
    """Position in `events` of the least important retained item, or -1 if none.

    The scan is O(retained) with two integer multiplications per item; the byte
    tie-break is materialized only on an exact importance-and-`t` tie, which `t`'s
    uniqueness makes unreachable in practice and which is kept for totality.
    """
    if not state.events:
        return -1
    if pairs is None:
        pairs = _cluster_pairs(state, now)
    best_i = 0
    best = _candidate(state, 0, now, pairs)
    i = 1
    while i < len(state.events):
        cand = _candidate(state, i, now, pairs)
        left = cand[0] * best[1]
        right = best[0] * cand[1]
        if left < right or (left == right and _break_tie(state, cand, best)):
            best_i = i
            best = cand
        i += 1
    return best_i


def _break_tie(state, cand, best):
    """Resolve an exact importance tie by `t`, then by canonical payload bytes."""
    if cand[2] != best[2]:
        return cand[2] < best[2]
    a = encode(_payload_at(state.events, cand[2]))
    b = encode(_payload_at(state.events, best[2]))
    return a < b


# ---- index maintenance ------------------------------------------------------

def _index_add(index, atom, t):
    if atom is None:
        return index
    out = dict(index)
    prev = out.get(atom)
    out[atom] = (prev + (t,)) if prev is not None else (t,)
    return out


def _index_remove(index, atom, t):
    if atom is None:
        return index
    ts = index.get(atom)
    if ts is None:
        return index
    kept = tuple(x for x in ts if x != t)
    out = dict(index)
    if kept:
        out[atom] = kept
    else:
        del out[atom]
    return out


def _build_index(events, layer_cap):
    """Rederive the whole index from the retained records (used to validate restore)."""
    index = {}
    if layer_cap < 2:
        return index
    for record in events:
        atom = handle_atom(record["payload"])
        if atom is None:
            continue
        prev = index.get(atom)
        index[atom] = (prev + (record["t"],)) if prev is not None else (record["t"],)
    return index


def _accounted_occupancy(events, index, record, layer_cap):
    """Recompute occupancy from the retained state alone (restore's second guard)."""
    total = 0
    for item in events:
        total += event_cost(item["payload"])
        if layer_cap >= 2 and handle_atom(item["payload"]) is not None:
            total += 1
    if layer_cap >= LAYER:
        total += forget_cost(record)
    return total


# ---- eviction ---------------------------------------------------------------

def _evict_at(state, i, now):
    """Drop the retained item at position `i`; return the new state (pure)."""
    record = state.events[i]
    payload = record["payload"]
    atom = handle_atom(payload)
    freed = event_cost(payload) + (1 if atom is not None else 0)
    before = forget_cost(state.forgetting)
    forgetting = _forget_add(state.forgetting, record["t"], grammar_weight(payload))
    after = forget_cost(forgetting)
    return replace(state,
                   occupancy=state.occupancy - freed + (after - before),
                   events=state.events[:i] + state.events[i + 1:],
                   index=_index_remove(state.index, atom, record["t"]),
                   forgetting=forgetting)


def _drop_arriving(state, t, payload):
    """Spend `t` on an item that is itself the least important thing in play.

    It is ingested (its `t` is assigned and consumed, §1.3) and immediately
    forgotten: recorded in the aggregated record, never stored. Evicting a *more*
    important item to house it would be the policy inverted.
    """
    before = forget_cost(state.forgetting)
    forgetting = _forget_add(state.forgetting, t, grammar_weight(payload))
    after = forget_cost(forgetting)
    return replace(state,
                   occupancy=state.occupancy + (after - before),
                   next_t=t + 1,
                   last_cost=0,
                   forgetting=forgetting)


def _arriving_uses(state, payload, t):
    """The uses an arriving payload would present, at `now = t`.

    Its cluster's existing uses — so an arrival that joins a live cluster inherits
    that cluster's standing rather than starting from nothing — **plus its own
    arrival, and only if it is not a byte-identical repetition of something already
    retained.** The distinct-payload rule of §1 has to hold at the door as well as
    afterwards: if a repetition counted as a use on arrival, an attacker could buy
    admission with copies and the guard would apply only to what it displaced.
    """
    atom = handle_atom(payload)
    uses = list(cluster_uses(state, atom, t)) if atom is not None else []
    if not uses:
        return (t,)
    key = encode(payload)
    for u in uses:
        existing = _payload_at(state.events, u)
        if existing is not None and encode(existing) == key:
            return tuple(uses)                    # a repetition: not a use
    uses.append(t)
    return tuple(uses)


def _arriving_candidate(state, t, payload, pairs):
    """The eviction-order candidate the arriving item would present, at `now = t`."""
    total = _recency_sum(_arriving_uses(state, payload, t), t)
    return (grammar_weight(payload) * total.numerator, total.denominator, t, None)


# ---- verbs -----------------------------------------------------------------

def write(state, payload):
    """Append one event, evicting the least important items to make room.

    Below Layer 3 this is the frozen behaviour of the layer below: a write whose
    cost would exceed the cap is **refused** deterministically (`t = None`,
    §4.1) and nothing is dropped — which is exactly what makes
    `make_engine(layer_cap = 2)` a genuine capped engine for the humility trial
    (§7.4). At Layer 3 the engine evicts instead, and the observable occupancy
    never exceeds the cap at any point.
    """
    check_canonical(payload)

    if not _retention_on(state):
        t = state.next_t                          # null engine: sees, retains nothing
        return replace(state, next_t=t + 1, last_cost=0), t

    atom = handle_atom(payload) if _recall_on(state) else None
    cost = event_cost(payload) + (1 if atom is not None else 0)
    t = state.next_t

    if not _forgetting_on(state):
        if state.occupancy + cost > state.budget_cap:
            return state, None                    # deterministic refusal (§4.1)
        return _insert(state, t, payload, atom, cost), t

    if cost > state.budget_cap:
        # Nothing could ever hold it: a genuine budget refusal, no `t` spent.
        return state, None

    while state.occupancy + cost > state.budget_cap:
        pairs = _cluster_pairs(state, t)
        i = victim_position(state, t, pairs)
        if i < 0:
            return _drop_arriving(state, t, payload), t
        victim = _candidate(state, i, t, pairs)
        arriving = _arriving_candidate(state, t, payload, pairs)
        if not less_important(victim, arriving):
            return _drop_arriving(state, t, payload), t
        state = _evict_at(state, i, t)

    return _insert(state, t, payload, atom, cost), t


def _insert(state, t, payload, atom, cost):
    record = {"payload": copy_value(payload), "t": t}
    return replace(state,
                   occupancy=state.occupancy + cost,
                   next_t=t + 1,
                   last_cost=cost,
                   events=state.events + (record,),
                   index=_index_add(state.index, atom, t))


def read(state, t):
    """The retained event at logical time `t`, or None — evicted reads as absent."""
    if not _retention_on(state):
        return None
    if not isinstance(t, int) or isinstance(t, bool):
        return None
    i = _find(state.events, t)
    if i < 0:
        return None
    return copy_value(state.events[i])


def read_range(state, t0, t1):
    """Every retained event with `t` in [t0, t1] inclusive, `t`-ascending."""
    if not _retention_on(state):
        return []
    if not isinstance(t0, int) or isinstance(t0, bool):
        return []
    if not isinstance(t1, int) or isinstance(t1, bool):
        return []
    if t1 < t0:
        return []
    lo = _lower_bound(state.events, t0)
    out = []
    i = lo
    while i < len(state.events) and state.events[i]["t"] <= t1:
        out.append(copy_value(state.events[i]))
        i += 1
    return out


def retained(state):
    """The number of events currently retained (evictions excluded)."""
    return len(state.events)


# ---- recall (the Layer-2 capability, carried forward on the retained set) ----

def _contains(payload, cue):
    """Does `payload` satisfy the whole probe `cue`, exactly and by value?

    Exact containment: every key of the cue must be present with an equal value,
    recursively. No tokenization, no normalization, no signature — which is why
    the single-posting index of §0.2 loses no discrimination (`7` never matches
    `"7"`, and a near-duplicate is separated by the field that differs).
    """
    if not isinstance(cue, dict):
        return False
    if not isinstance(payload, dict):
        return False
    for key, want in cue.items():
        if key not in payload:
            return False
        got = payload[key]
        if isinstance(want, dict):
            if not _contains(got, want):
                return False
        elif isinstance(want, bool) or isinstance(got, bool):
            if got is not want:
                return False
        elif got != want or type(got) is not type(want):
            return False
    return True


def recall(state, cue):
    """Recover the single retained event satisfying the content probe `cue`.

    Returns an Answer (§7.2). Honest by construction: the handle atom narrows to a
    cluster, exact containment verifies the whole probe, and the engine answers
    only when **one** retained event survives both. A cue for something evicted,
    never ingested, or handle-free yields a scored **abstention** (§7.3), never a
    guess and never an exception.
    """
    if not _recall_on(state):
        return _abstain()
    if not isinstance(cue, dict):
        return _abstain()
    try:
        check_canonical(cue)
    except NonCanonical:
        return _abstain()

    atom = handle_atom(cue)
    if atom is None:
        return _abstain()                         # no handle: outside L3's index
    ts = state.index.get(atom)
    if ts is None:
        return _abstain()                         # evicted or never ingested

    hit = None
    for t in ts:
        i = _find(state.events, t)
        if i < 0:
            continue
        if _contains(state.events[i]["payload"], cue):
            if hit is not None:
                return _abstain()                 # ambiguous: two retained events fit
            hit = i
    if hit is None:
        return _abstain()

    record = copy_value(state.events[hit])
    t = record["t"]
    prov = {"support": [t], "kind": "recall", "t_asof": t}
    # The returned event is byte-exact state verified against the whole probe, so
    # the structural certainty is total. Calibration is dormant until Layer 6
    # (§3.4); Layer 6 will replace this with a model, and the aggregated
    # forgetting record is what will let it tell "evicted" from "never ingested".
    return _answer(record, 1000, prov)


# ---- the Answer (§7.2) & the generic query binding -------------------------

def _answer(value, confidence, provenance):
    return {"status": "answer", "value": value,
            "confidence": confidence, "provenance": provenance}


def _abstain(confidence=0, provenance=None):
    return {"status": "abstain", "value": None,
            "confidence": confidence, "provenance": provenance}


def _forgetting_body(record):
    return {"width": record.width,
            "buckets": [[count, mass] for count, mass in record.buckets],
            "count": record.count,
            "mass": record.mass}


def query(state, q):
    """Answer a query (§7.2). Unsupported / un-capable queries abstain, never raise."""
    if not isinstance(q, dict):
        return _abstain()
    op = q.get("op")

    if op == "read":
        event = read(state, q.get("t"))
        if event is None:
            return _abstain()
        prov = {"support": [event["t"]], "kind": "recall", "t_asof": event["t"]}
        return _answer(event, 1000, prov)

    if op == "read_range":
        if not _retention_on(state):
            return _abstain()
        events = read_range(state, q.get("t0"), q.get("t1"))
        if events:
            support = [e["t"] for e in events]
            prov = {"support": support, "kind": "aggregate", "t_asof": support[-1]}
            return _answer(events, 1000, prov)
        return _answer(events, 1000, None)        # an empty range is a valid answer

    if op == "recall":
        return recall(state, q.get("cue"))

    if op == "forgetting":
        # The aggregated record (§0.3). `kind = "absent"` with empty support is
        # the one §4.2 form that fits: this is a statement about what is *gone*,
        # so there is no retained `t` to cite.
        if not _forgetting_on(state):
            return _abstain()
        asof = state.next_t - 1 if state.next_t > 0 else 0
        return _answer(_forgetting_body(state.forgetting), 1000,
                       {"support": [], "kind": "absent", "t_asof": asof})

    if op == "forgot_at":
        if not _forgetting_on(state):
            return _abstain()
        t = q.get("t")
        if not isinstance(t, int) or isinstance(t, bool) or t < 0:
            return _abstain()
        count, mass = forget_bucket_at(state.forgetting, t)
        asof = state.next_t - 1 if state.next_t > 0 else 0
        return _answer({"count": count, "mass": mass,
                        "width": state.forgetting.width},
                       1000, {"support": [], "kind": "absent", "t_asof": asof})

    return _abstain()                             # capability absent (§7.3)


# ---- snapshot / restore ----------------------------------------------------

def _body(state):
    """The canonical, deterministic dict form of the full state (§2.4).

    `last_cost` is transient budget bookkeeping (not observable in any query), so
    it is excluded — two independent ingest sequences yield byte-identical
    snapshots (determinism, §2.3).
    """
    return {
        "layer_cap": state.layer_cap,
        "budget_cap": state.budget_cap,
        "occupancy": state.occupancy,
        "next_t": state.next_t,
        "events": [copy_value(e) for e in state.events],
        "index": {atom: list(ts) for atom, ts in state.index.items()},
        "forgetting": _forgetting_body(state.forgetting),
    }


def state_checksum(state):
    """SHA-256 hex over the canonical encoding of the full state body (§2.4)."""
    return hashlib.sha256(encode(_body(state))).hexdigest()


def snapshot(state):
    """Canonical, checksummed serialization of the state (§7.1, §2.4)."""
    body = _body(state)
    checksum = hashlib.sha256(encode(body)).hexdigest()
    return encode({"magic": MAGIC, "checksum": checksum, "body": body})


def _forgetting_from_body(body):
    if not isinstance(body, dict):
        raise CorruptSnapshot("snapshot forgetting record is not an object")
    if frozenset(body.keys()) != frozenset({"width", "buckets", "count", "mass"}):
        raise CorruptSnapshot("snapshot forgetting record keys are wrong")
    width, count, mass = body["width"], body["count"], body["mass"]
    for name, value in (("width", width), ("count", count), ("mass", mass)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise CorruptSnapshot("snapshot forgetting %s is not a non-negative int" % (name,))
    if width <= 0:
        raise CorruptSnapshot("snapshot forgetting width must be positive")
    raw = body["buckets"]
    if not isinstance(raw, list) or len(raw) > FORGET_BUCKETS:
        raise CorruptSnapshot("snapshot forgetting buckets are not a bounded array")
    buckets = []
    seen_count = 0
    seen_mass = 0
    for pair in raw:
        if (not isinstance(pair, list) or len(pair) != 2
                or not all(isinstance(x, int) and not isinstance(x, bool) and x >= 0
                           for x in pair)):
            raise CorruptSnapshot("snapshot forgetting bucket is not a (count, mass) pair")
        buckets.append((pair[0], pair[1]))
        seen_count += pair[0]
        seen_mass += pair[1]
    # The record cannot be rederived from the log — the evicted events are gone,
    # which is the honest asymmetry of this layer — so it is checked structurally:
    # the buckets must sum to the totals they claim.
    if seen_count != count or seen_mass != mass:
        raise CorruptSnapshot("snapshot forgetting buckets do not sum to their totals")
    return Forgetting(width=width, buckets=tuple(buckets), count=count, mass=mass)


def restore(data):
    """Rebuild a state from snapshot bytes; fail loudly on any corruption.

    Four independent guards, all raising `CorruptSnapshot`:
      1. the envelope/body structure and the SHA-256 checksum over the whole body;
      2. the records must be ascending and unique in `t`, and within `next_t`;
      3. the index rederived from the retained records must equal the stored one,
         so a tampered index with a recomputed checksum is still rejected;
      4. the recomputed occupancy must equal the stored occupancy, and the
         forgetting record must sum to its own declared totals.
    """
    try:
        envelope = decode(data)
    except Exception as exc:                      # invalid JSON / UTF-8 / float
        raise CorruptSnapshot("snapshot is not decodable: %r" % (exc,))

    if not isinstance(envelope, dict) or frozenset(envelope.keys()) != _ENVELOPE_KEYS:
        raise CorruptSnapshot("snapshot envelope keys are wrong")
    if envelope["magic"] != MAGIC:
        raise CorruptSnapshot("snapshot magic mismatch")

    body = envelope["body"]
    if not isinstance(body, dict) or frozenset(body.keys()) != _BODY_KEYS:
        raise CorruptSnapshot("snapshot body keys are wrong")

    if hashlib.sha256(encode(body)).hexdigest() != envelope["checksum"]:
        raise CorruptSnapshot("snapshot checksum mismatch (corruption detected)")

    layer_cap, budget_cap = body["layer_cap"], body["budget_cap"]
    occupancy, next_t = body["occupancy"], body["next_t"]
    for name, value in (("layer_cap", layer_cap), ("budget_cap", budget_cap),
                        ("occupancy", occupancy), ("next_t", next_t)):
        if not isinstance(value, int) or isinstance(value, bool):
            raise CorruptSnapshot("snapshot %s is not an integer" % (name,))
    raw_events = body["events"]
    if not isinstance(raw_events, list):
        raise CorruptSnapshot("snapshot events is not an array")

    events = []
    previous = -1
    for item in raw_events:
        if (not isinstance(item, dict)
                or frozenset(item.keys()) != frozenset({"payload", "t"})):
            raise CorruptSnapshot("snapshot event record keys are wrong")
        t = item["t"]
        if not isinstance(t, int) or isinstance(t, bool) or t <= previous:
            raise CorruptSnapshot("snapshot events are not ascending and unique in t")
        if t >= next_t:
            raise CorruptSnapshot("snapshot event t is at or beyond next_t")
        previous = t
        events.append({"payload": copy_value(item["payload"]), "t": t})
    events = tuple(events)

    raw_index = body["index"]
    if not isinstance(raw_index, dict):
        raise CorruptSnapshot("snapshot index is not an object")
    stored = {}
    for atom, ts in raw_index.items():
        if not isinstance(ts, list):
            raise CorruptSnapshot("snapshot posting list is not an array")
        stored[atom] = tuple(ts)

    record = _forgetting_from_body(body["forgetting"])

    if _build_index(events, layer_cap) != stored:
        raise CorruptSnapshot("snapshot index diverges from the retained records")

    if _accounted_occupancy(events, stored, record, layer_cap) != occupancy:
        raise CorruptSnapshot("snapshot occupancy diverges from the accounted cost")

    return L3State(layer_cap=layer_cap, budget_cap=budget_cap, occupancy=occupancy,
                   next_t=next_t, last_cost=0, events=events, index=stored,
                   forgetting=record)


# ---- the generic engine interface (§7, INTERFACE.md) -----------------------

def empty():
    """A fresh, full Layer-3 engine state (adapter contract, §7)."""
    return new_state(layer_cap=LAYER, budget_cap=DEFAULT_BUDGET)


def make_engine(layer_cap, budget_cap=DEFAULT_BUDGET):
    """A fresh state capped at `layer_cap` (§7.4). 2 = the refuse-don't-forget floor."""
    return new_state(layer_cap=layer_cap, budget_cap=budget_cap)


def ingest(state, payload):
    """Append one event; return `(state', t)`. `t` is None only on a hard refusal."""
    return write(state, payload)


def last_cost(state):
    """Integer work-unit cost of the most recent successful write (§3.3, §4.1)."""
    return state.last_cost

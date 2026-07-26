"""core/layers/l4_consolidation.py — Layer 4: Consolidation (derived schemas).

Layer 3 **dropped**: under a stream ten times the budget it kept what mattered
and forgot the rest, and what it forgot left no trace at all. Layer 4 **derives**:
every event is folded, at the door, into a schema that is cheaper than the
episode it came from, so an episode can be released *because its content already
lives somewhere else*. That is the whole layer in one sentence, and it is the
Layer-3 debt coming due (`core/layers/README-l3.md §0.4`, GAPMAP **S4** form B):
**eviction as lossy compression** rather than eviction as loss.

Pure, integer-only (§2), built entirely on the frozen Layer-1/2/3 primitives
(`core/state.py`, `core/serialize.py`, `core/layers/l3_forgetting.py`); it edits
none of them (§9). Below `layer_cap = 4` the state IS the frozen Layer-3 state
and every verb delegates to it, so `make_engine(3)` is not an imitation of the
forgetting engine — it is the forgetting engine (§7.4).

The full design record is `core/layers/README-l4.md`. This docstring states what
the code does; that document states why the 43 300-cell budget admits no other
shape.

## The budget decided the state, before the code (BOUNDARY-RULINGS.md R2)

`trials/ascension/l4/ATTAINABILITY.md §4` exhibited the witness the gate rests
on — the exact interval table plus global counters, **40 737 of 43 300 cells on
`corpora/l4stream`** — and recorded the engine's **working room as 2 563 cells,
5.9% of the budget**. Everything below is what those 2 563 cells buy, and the
arithmetic that fixed each choice is asserted in
`trials/ops/l4/t_l4_composition.py`.

Two consequences, both arithmetic, both settled before a line of this file:

  * **A second access path is unaffordable.** The interval table answers
    `(entity, key) -> history`; reconstruction asks the inverse, `t -> which
    pair`. An exact `t -> pair` index costs one cell per assertion (18 788 on
    `l4stream`), and `2 + 1 = 3` cells per assertion is **325‰** of the raw
    footprint against a 250‰ gate. So the schema carries **one** index and
    `read(t)` **searches** it. Query time pays; state does not, and only state is
    budgeted (§4.1) — the same trade `README-l3 §0.2` made one layer down, now
    forced by arithmetic rather than chosen. The table is nested **key-major**
    for the same reason: the attribute-key vocabulary is closed and small (16 on
    `l4stream`) where the entity population is not, so key-major costs
    `keys + pairs` where entity-major costs `entities + pairs` — 184 cells
    cheaper here, 9 967 on chronicle — and the search that pays for the missing
    index runs over a handful of large maps instead of thousands of tiny ones.
  * **The episode and the schema cannot both be kept.** A retained episode costs
    `event_cost + 1`; the schema costs ~2.17 cells per assertion. Holding both
    for 20 000 events is 4× the cap. So the episodic tier is **demotable**: an
    event whose content the schema regenerates exactly is released first, and
    releasing it loses nothing.

## What is stored

| component | cells | answers |
|---|---|---|
| interval table `{key: {entity: {t: value}}}` | `keys + pairs + 2 x assertions` | Q1 current-value, Q2 as-of, Q4 for every assertion |
| key atlas `{key: kind}` | `2 x keys` | which grammar form a stored assertion inverts to |
| global counters `{kind: count}` | `2 x kinds` | Q3 global counts |
| per-entity irreducible counts | `sum_e (1 + 2 x kinds_e)` | the part of Q3's profile no fold can reach |
| derived rows, by shape | `sum_s (1 + fields) + sum_rows (1 + fields)` | Q4 for events no chain regenerates |
| handle index | `atoms + postings` | `recall` (the Layer-2/3 cue channel) |
| aggregated forgetting record | `3 + 2 x buckets <= 35` | what is gone, in count and mass |

## Consolidation is invertible or it does not happen

An event is folded into an interval chain only when the payload is **exactly**
reconstructible from `(kind, entity, key, value)` — the engine rebuilds the
payload from the facet it just extracted and compares canonical bytes (§2.4). A
payload that does not round-trip is not consolidated; it is stored as a derived
row, or verbatim. So `reconstruction wrong = 0` is **structural**: the engine
never answers `read(t)` with a payload it did not prove it could rebuild.

The facet map itself is a **declared reading of the frozen chronicle-family
grammars**, exactly as `HANDLE_FIELDS` is at Layer 3 (`README-l3 §0.2`: the
grammar vocabularies are fixed, so the engine knows at design time which fields
name a thing). `trials/ops/l4/t_l4_composition.py` asserts that this reading and
the battery's own (`trials/_l4tasks.facet`) agree on every frozen corpus — one
reading, two implementations, checked rather than assumed.

## Eviction, in four phases, most-lossless first

**The demotion invariant is invertibility.** An episode may be released as a
demotion only where a chain actually rebuilds its payload — which is
`atlas_after(...) is not None` and *not* `facet(payload) is not None`. An
assertion under a key seen twice, or under a payload the rebuild cannot
reproduce, answers Q1 and Q2 exactly and regenerates **nothing**: it is kept
where the forgetting law can see it, and released into the record as a loss. Add
the case where a key's inversion dies *after* episodes under it were released
(`_reconcile_lost_key`), and the ledger of `README-l4.md §2.3` is true of the
code rather than of the corpora it was measured on:

    demotions + forgotten + episodes held  ==  events ingested
    forgotten                              ==  exactly the `t` `read` abstains on

1. **Demotion.** Release an episode whose content a chain regenerates. Nothing is
   lost; the count is reported as `demotions` and is *not* forgetting.
2. **Forgetting.** Release an irreducible episode — one no schema regenerates —
   by the **inherited Layer-3 importance law** (grammar weight x distinct-
   reference count x harmonic logical-`t` recency, exact `Fraction`s compared by
   integer cross-multiplication), least important first, ties by `t` then
   canonical bytes. Recorded in the aggregated record.
3. **Shedding.** When the derived schema *itself* does not fit, drop whole
   supersession chains, oldest-established first. The entity that owned the chain
   is marked `damaged` in the same breath: its current-value and as-of answers
   stay exact (a later assertion is still the latest one), but its action-count
   profile can no longer be folded exactly, so it **abstains** forever after
   rather than returning a confident undercount.
4. **Refusal.** Only when no eviction could make room: a payload whose schema
   delta exceeds the entire cap. `t` is not spent and the state is unchanged
   (§4.1.2), which is the one response every layer shares.

## Determinism and the Answer contract

Identical streams produce byte-identical snapshots (§2.3): every structure is a
dict in first-seen order or a tuple in `t` order, and every eviction is a total
order. Capability absence is a scored abstention, never an exception (§7.3): an
unreconstructible `t`, a pair never asserted, an as-of before a pair's first
assertion and a profile the engine can no longer fold exactly all **abstain**.
"""

import hashlib
from dataclasses import dataclass, replace
from fractions import Fraction

from core.serialize import encode, decode, check_canonical, copy_value, NonCanonical
from core.state import event_cost, payload_cost
from core.layers import l3_forgetting as l3
from core.layers.l3_forgetting import (
    Forgetting, forget_empty, forget_cost, forget_bucket_at,
    handle_atom, grammar_weight, FORGET_BUCKETS, FORGET_WIDTH0,
)

LAYER = 4

# A generous default cap, matching the Layer-1/2/3 defaults so cross-layer
# reasoning stays simple. Integer only (§2.2). The Layer-4 trials always pass an
# explicit cap — at the gate, a deliberately punishing one.
DEFAULT_BUDGET = 1_000_000_000

MAGIC = "boundary1-l4-snapshot"
_ENVELOPE_KEYS = frozenset({"magic", "checksum", "body"})
_BODY_KEYS = frozenset({"layer_cap", "budget_cap", "occupancy", "next_t",
                        "chains", "atlas", "irreducible", "counts", "damaged",
                        "demotable", "kept", "verbatim", "index", "demotions",
                        "forgetting"})


class CorruptSnapshot(ValueError):
    """Raised by `restore` when a snapshot fails its integrity check (loudly)."""


# ---- the assertion facet: a declared reading of the frozen grammars ----------
#
# Per grammar `kind`, how a payload reads as an `(entity, key, value)` assertion
# and — the half that matters — how it reads BACK. The tuple is
# `(entity_field, key_field, key_literal, value_field, value_literal)`: exactly
# one of `key_field` / `key_literal` names the attribute, and exactly one of
# `value_field` / `value_literal` carries its value.
#
# Sources: `corpora/chronicle/grammar.md`, `corpora/l4stream/grammar.md`. `link`
# is an assertion on `(src, rel)` whose value is the target — Graphiti's
# bitemporal edge (GAPMAP **S3**) with its two LLM calls replaced by integer
# interval arithmetic. `retire` asserts the closed lifecycle key `live`.
ASSERTION_FORMS = {
    "spawn":  ("entity", None,  "class", "class", None),
    "attr":   ("entity", "key", None,    "val",   None),
    "move":   ("entity", None,  "loc",   "loc",   None),
    "link":   ("src",    "rel", None,    "dst",   None),
    "retire": ("entity", None,  "live",  None,    0),
}

# The value field of these kinds names another entity, so it must be an integer;
# elsewhere a value is any scalar the grammar admits.
_INT_VALUED = frozenset({"link"})


def facet(payload):
    """Read one payload as an `(entity, key, value)` assertion, or `None`.

    `None` is the **irreducible** answer: no schema in this engine regenerates
    such an event, so it survives as a derived row or not at all.
    """
    if not isinstance(payload, dict):
        return None
    kind = payload.get("kind")
    if not isinstance(kind, str):
        return None
    form = ASSERTION_FORMS.get(kind)
    if form is None:
        return None
    entity_field, key_field, key_literal, value_field, value_literal = form

    entity = payload.get(entity_field)
    if not isinstance(entity, int) or isinstance(entity, bool):
        return None

    if key_field is None:
        key = key_literal
    else:
        key = payload.get(key_field)
        if not isinstance(key, str):
            return None

    if value_field is None:
        value = value_literal
    else:
        if value_field not in payload:
            return None
        value = payload[value_field]
        if isinstance(value, (dict, list)):
            return None
        if kind in _INT_VALUED and (not isinstance(value, int)
                                    or isinstance(value, bool)):
            return None
    return (entity, key, value)


def rebuild(kind, entity, key, value):
    """Invert the facet: the payload an `(entity, key, value)` assertion came from."""
    form = ASSERTION_FORMS.get(kind)
    if form is None:
        return None
    entity_field, key_field, _key_literal, value_field, _value_literal = form
    out = {"kind": kind, entity_field: entity}
    if key_field is not None:
        out[key_field] = key
    if value_field is not None:
        out[value_field] = value
    return out


def invertible(payload, kind, entity, key, value):
    """Does the rebuilt payload equal the original, byte for byte (§2.4)?

    Compared as canonical bytes and not as Python values, because `True == 1` in
    Python and `true != 1` in the canonical encoding. This is the whole guard
    behind `reconstruction wrong = 0`: an event that does not round-trip is
    never consolidated, so it can never be regenerated wrongly.
    """
    got = rebuild(kind, entity, key, value)
    return got is not None and encode(got) == encode(payload)


_UNSEEN = object()


def atlas_after(atlas, payload, fact):
    """The atlas entry `fact`'s key carries **after** this event is folded.

    `None` is the answer that matters: the key's inversion is not a function, so
    assertions under it answer Q1 and Q2 exactly and **regenerate nothing**.

    This is the **one** reading of the atlas transition. `_apply_schema` applies
    it and `write` demotes by it, because those two deciding by different rules
    is precisely the defect `strain/l4/t_demotion_seam.py` was written against: a
    write path that reads "this event has a facet" as "a chain regenerates it"
    releases an episode nothing can rebuild and books the loss as compression.
    **The demotion invariant is invertibility**, and this predicate is where the
    engine says so.
    """
    if fact is None:
        return None
    entity, key, value = fact
    kind = payload.get("kind") if isinstance(payload, dict) else None
    prior = atlas.get(key, _UNSEEN)
    if prior is None:
        return None                    # already ambiguous, and never recovers
    if prior is not _UNSEEN and prior != kind:
        return None                    # a second grammar form under one key
    if not invertible(payload, kind, entity, key, value):
        return None
    return kind


# ---- the derived row: the grammar factored out of the instance ---------------

def row_shape(payload):
    """`(kind, sorted field names)`, or `None` if no row can express the payload.

    A row stores an event's *values* against a shape stored once, so the field
    names and the `kind` — pure grammar, identical in every instance — are paid
    for once instead of per event. An `l3streamb` item costs `1 + 4 = 5` cells as
    a row against `11` as an episode; an `l4stream` note costs `3` against `7`.
    That is compression from **schema**, where a chain is compression from
    **supersession**; the layer needs both, because a corpus with no
    supersession (a `note`, an `item`) still has a grammar.
    """
    if not isinstance(payload, dict):
        return None
    kind = payload.get("kind")
    if not isinstance(kind, str):
        return None
    fields = []
    for name in sorted(payload):
        if name == "kind":
            continue
        if isinstance(payload[name], (dict, list)):
            return None            # a nested value is not a grammar atom
        fields.append(name)
    return (kind, tuple(fields))


def row_values(payload, shape):
    return tuple(payload[name] for name in shape[1])


def row_payload(shape, values):
    out = {"kind": shape[0]}
    for name, value in zip(shape[1], values):
        out[name] = value
    return out


# ---- the state --------------------------------------------------------------

@dataclass(frozen=True)
class L4State:
    """The frozen Layer-4 engine state (§2.1).

    `chains` is the interval table — `{key: {entity: {t: value}}}`, every inner
    map in ascending `t`, which is what makes current-value the last entry and
    as-of a walk back from it. `atlas` maps an attribute key to the grammar
    `kind` its assertions invert to, or to `None` where the engine has seen that
    key under two kinds and must therefore refuse to invert it at all.
    `demotable` holds rows a chain regenerates, `kept` rows nothing regenerates;
    `verbatim` is the fallback for payloads no shape can express.
    """

    layer_cap: int
    budget_cap: int
    occupancy: int
    next_t: int
    last_cost: int
    chains: dict          # key -> {entity: {t: value}}
    atlas: dict           # key -> kind, or None when the key is not invertible
    irreducible: dict     # entity -> {kind: count}
    counts: dict          # kind -> count (global, never decremented)
    damaged: tuple        # entities whose profile fold is no longer exact
    demotable: dict       # shape -> {t: values}   (a chain regenerates these)
    kept: dict            # shape -> {t: values}   (nothing else regenerates these)
    verbatim: dict        # t -> payload           (no shape expresses these)
    index: dict           # handle atom -> (t, ...)
    demotions: int        # episodes released losslessly into consolidated form
    forgetting: Forgetting


def new_state(layer_cap, budget_cap):
    """A fresh state capped at `layer_cap` with integer budget cap `budget_cap`.

    Below Layer 4 this returns the **frozen Layer-3 state** (§7.4): capping is a
    construction-time restriction, and the honest way to build an engine without
    consolidation is to build the engine that does not have it.
    """
    if not isinstance(layer_cap, int) or isinstance(layer_cap, bool):
        raise TypeError("layer_cap must be a plain int")
    if not isinstance(budget_cap, int) or isinstance(budget_cap, bool):
        raise TypeError("budget_cap must be a plain int")
    if layer_cap < 0:
        raise ValueError("layer_cap must be non-negative")
    if budget_cap <= 0:
        raise ValueError("budget_cap must be positive (§4.1)")
    if layer_cap < LAYER:
        return l3.new_state(layer_cap=layer_cap, budget_cap=budget_cap)
    record = forget_empty()
    return L4State(layer_cap=layer_cap, budget_cap=budget_cap,
                   occupancy=forget_cost(record) + 1, next_t=0, last_cost=0,
                   chains={}, atlas={}, irreducible={}, counts={}, damaged=(),
                   demotable={}, kept={}, verbatim={}, index={}, demotions=0,
                   forgetting=record)


# ---- cost accounting (§4.1, priced under rule P — R4 clause 3) --------------
#
# One cell, one grammar atom. Every figure below is the `payload_cost` of the
# corresponding branch of the snapshot body, so the engine's own accounting and
# the atoms a reader can count in its serialized state are the same number.

def chain_cells(chains):
    total = 0
    for per in chains.values():
        total += 1                                   # the key's own cell
        for chain in per.values():
            total += 1 + 2 * len(chain)              # its entity, then (t, value)
    return total


def irreducible_cells(irreducible):
    return sum(1 + 2 * len(per) for per in irreducible.values())


def rows_cells(rows):
    total = 0
    for shape, group in rows.items():
        width = len(shape[1])
        total += 1 + width                            # the kind, then its fields
        total += len(group) * (1 + width)             # each row: `t` + its values
    return total


def index_cells(index):
    return len(index) + sum(len(ts) for ts in index.values())


def accounted_occupancy(state):
    """Recompute occupancy from the state alone — `restore`'s independent guard.

    The write path maintains `occupancy` incrementally (it must: recomputing per
    write is quadratic). This is the check that the increments never drifted,
    and `trials/ops/l4/t_l4_composition.py` asserts the identity after every
    kind of eviction rather than only at the end.
    """
    total = chain_cells(state.chains)
    total += 2 * len(state.atlas)
    total += irreducible_cells(state.irreducible)
    total += 2 * len(state.counts)
    total += len(state.damaged)
    total += rows_cells(state.demotable)
    total += rows_cells(state.kept)
    total += sum(event_cost(p) for p in state.verbatim.values())
    total += index_cells(state.index)
    total += 1                                        # the demotion counter
    total += forget_cost(state.forgetting)
    return total


# ---- small immutable helpers ------------------------------------------------

def _dict_set(mapping, key, value):
    out = dict(mapping)
    out[key] = value
    return out


def _dict_del(mapping, key):
    out = dict(mapping)
    del out[key]
    return out


def _index_add(index, atom, t):
    if atom is None:
        return index, 0
    out = dict(index)
    prev = out.get(atom)
    if prev is None:
        out[atom] = (t,)
        return out, 2                                 # a new atom and a posting
    out[atom] = prev + (t,)
    return out, 1


def _index_remove(index, atom, t):
    if atom is None:
        return index, 0
    ts = index.get(atom)
    if ts is None:
        return index, 0
    kept = tuple(x for x in ts if x != t)
    out = dict(index)
    if kept:
        out[atom] = kept
        return out, 1
    del out[atom]
    return out, 2


def _forget(record, t, weight):
    """Record one genuine loss; return `(record', cell delta)`."""
    before = forget_cost(record)
    updated = l3._forget_add(record, t, weight)
    return updated, forget_cost(updated) - before


# ---- what one write would cost ----------------------------------------------

def _schema_delta(state, payload, fact, worst=False):
    """The cells consolidation itself needs for this event. Never optional.

    Consolidation happens at the door: the derived view is updated before the
    engine asks whether it can also afford to keep the episode. That ordering is
    the layer — an episode is a redundant copy of something already recorded,
    not the record itself.

    `worst=True` prices the event against an **empty** schema. Eviction can only
    remove entities and pairs, so a delta measured before eviction is not an
    upper bound on the delta after it; the worst case is, and it is what room is
    made for. The state is then charged the delta actually applied, so the
    slack is transient rather than permanent.
    """
    kind = payload.get("kind") if isinstance(payload, dict) else None
    cost = 0
    if kind not in state.counts:
        cost += 2                                     # a new global counter
    if fact is not None:
        entity, key, _value = fact
        if worst:
            cost += 1 + 1                             # the key, then its entity
        else:
            per = state.chains.get(key)
            if per is None:
                cost += 1                             # the key's own cell
                cost += 1                             # its first entity
            elif entity not in per:
                cost += 1
        cost += 2                                     # this assertion: (t, value)
        if key not in state.atlas:
            cost += 2                                 # the key's atlas entry
    else:
        who = _actor(payload)
        if who is not None and who not in state.damaged:
            per = None if worst else state.irreducible.get(who)
            if per is None:
                cost += 1 + 2                         # the entity, then its kind
            elif kind not in per:
                cost += 2
    return cost


def _record_delta(state, payload, demotable=True, worst=False):
    """The cells the *episode* would cost, and how it would be stored.

    The shape header is charged **per tier**: `demotable` and `kept` are separate
    stores, so one grammar shape with instances in both — murk has them, a
    well-formed `attr` beside one whose entity is a string — pays for its field
    names in each. Charging it once would understate the state by exactly the
    cells a reader can count in the snapshot, which is the drift rule P exists to
    forbid.
    """
    shape = row_shape(payload)
    if shape is None:
        cost = event_cost(payload)
        tier = "verbatim"
    else:
        width = len(shape[1])
        cost = 1 + width
        rows = state.demotable if demotable else state.kept
        if worst or shape not in rows:
            cost += 1 + width                         # the shape, stored once
        tier = "row"
    atom = handle_atom(payload)
    if atom is not None:
        cost += 2 if (worst or atom not in state.index) else 1
    return {"cost": cost, "tier": tier, "shape": shape, "atom": atom}


def _actor(payload):
    """The entity an event is *about*: its `entity`, else its `src`, else none."""
    if not isinstance(payload, dict):
        return None
    who = payload.get("entity")
    if isinstance(who, int) and not isinstance(who, bool):
        return who
    who = payload.get("src")
    if isinstance(who, int) and not isinstance(who, bool):
        return who
    return None


# ---- phase 1: demotion (lossless) -------------------------------------------

def _oldest_demotable(state):
    """The `t` of the oldest demotable row, or `None`. Rows arrive in `t` order."""
    best = None
    for group in state.demotable.values():
        if not group:
            continue
        first = next(iter(group))
        if best is None or first < best:
            best = first
    return best


def _drop_row(state, tier, t):
    """Remove one episode from the named tier; return `(state', freed, payload)`."""
    rows = state.demotable if tier == "demotable" else state.kept
    for shape, group in rows.items():
        if t not in group:
            continue
        width = len(shape[1])
        freed = 1 + width
        payload = row_payload(shape, group[t])
        smaller = _dict_del(group, t)
        if smaller:
            out = _dict_set(rows, shape, smaller)
        else:
            out = _dict_del(rows, shape)
            freed += 1 + width                        # the shape goes with it
        index, given = _index_remove(state.index, handle_atom(payload), t)
        freed += given
        field = "demotable" if tier == "demotable" else "kept"
        return replace(state, index=index, **{field: out}), freed, payload
    if tier == "kept" and t in state.verbatim:
        payload = state.verbatim[t]
        freed = event_cost(payload)
        index, given = _index_remove(state.index, handle_atom(payload), t)
        freed += given
        return (replace(state, verbatim=_dict_del(state.verbatim, t), index=index),
                freed, payload)
    return state, 0, None


def _held_stamps(state):
    """The `t` of every episode still stored, in any tier."""
    out = set()
    for rows in (state.demotable, state.kept):
        for group in rows.values():
            out.update(group)
    out.update(state.verbatim)
    return out


def _move_to_kept(state, t):
    """Move one episode from the demotable tier to the kept tier.

    Cell-neutral in the row itself and not in its shape header, which rule P
    charges **per tier** (`_record_delta`): the demotable tier may give one up and
    the kept tier may take one on. The handle index is untouched — the episode is
    still an episode and is still reachable by cue; what changed is only that
    nothing regenerates it any more, so releasing it would be a loss.
    """
    for shape, group in state.demotable.items():
        if t not in group:
            continue
        width = len(shape[1])
        delta = 0
        smaller = _dict_del(group, t)
        if smaller:
            demotable = _dict_set(state.demotable, shape, smaller)
        else:
            demotable = _dict_del(state.demotable, shape)
            delta -= 1 + width                        # the shape goes with it
        kept = state.kept
        if shape not in kept:
            delta += 1 + width                        # and is paid for here
            kept = _dict_set(kept, shape, {t: group[t]})
        else:
            kept = _dict_set(kept, shape, _dict_set(kept[shape], t, group[t]))
        return replace(state, demotable=demotable, kept=kept,
                       occupancy=state.occupancy + delta), delta
    return state, 0


def _reconcile_lost_key(state, key):
    """The key's inversion is about to die — make the ledger say so first.

    Called on the write that marks `key` ambiguous (`atlas_after` -> `None`).
    Every assertion already folded under `key` stops being regenerable in that
    same instant, and the state is holding two claims that have just become
    false:

      * an episode in the **demotable** tier is not demotable any more, because
        no chain rebuilds it — it moves to the kept tier, where releasing it is a
        recorded loss rather than a free compression;
      * an episode already **released** was booked as a demotion, and that
        booking is now a lie: `read(t)` abstains on it forever. It becomes a
        recorded loss and the demotion counter gives it back.

    The mass is `1`, the same constant `_shed_until` uses and for the same
    reason: the weight is declared inside a payload this engine can no longer
    produce, so `1` is the only honest thing left to say about it.
    """
    per = state.chains.get(key)
    if not per:
        return state
    held = _held_stamps(state)
    record = state.forgetting
    demotions = state.demotions
    given = 0
    out = state
    for stamp in sorted(t for chain in per.values() for t in chain):
        if stamp in held:
            out, _delta = _move_to_kept(out, stamp)
            continue
        record, grew = _forget(record, stamp, 1)
        given += grew
        demotions -= 1
    return replace(out, occupancy=out.occupancy + given, demotions=demotions,
                   forgetting=record)


def _demote_until(state, need):
    """Release demotable episodes, oldest first, until `need` cells are free.

    **Nothing is lost here.** A demotable row's content is exactly what its
    chain regenerates, so releasing it costs coverage nothing and fidelity
    nothing; it is counted as a `demotion` and deliberately kept out of the
    forgetting record, which is the ledger of what is *gone*.
    """
    cap = state.budget_cap
    demotions = state.demotions
    while state.occupancy + need > cap:
        t = _oldest_demotable(state)
        if t is None:
            break
        state, freed, _payload = _drop_row(state, "demotable", t)
        if freed == 0:
            break
        state = replace(state, occupancy=state.occupancy - freed)
        demotions += 1
    return replace(state, demotions=demotions)


# ---- phase 2: forgetting (the inherited Layer-3 importance law) --------------

def _episode_at(state, t):
    """The irreducible episode stored at `t`, rebuilt, or `None`."""
    for shape, group in state.kept.items():
        values = group.get(t)
        if values is not None:
            return row_payload(shape, values)
    return state.verbatim.get(t)


def _features(state):
    """`[(t, grammar weight, handle atom)]` for every irreducible episode held.

    The importance law needs three things from an episode and **not** the episode
    itself: its declared weight, its handle, and its `t`. A row already stores
    those as columns, so they are read off the row directly rather than by
    rebuilding a payload per candidate per eviction. This is why an eviction
    sweep costs a pass over the retained set and not a pass plus a payload
    reconstruction for each member of it.
    """
    out = []
    for shape, group in state.kept.items():
        fields = shape[1]
        weight_at = fields.index(l3.GRAMMAR_WEIGHT_FIELD) \
            if l3.GRAMMAR_WEIGHT_FIELD in fields else -1
        handle_at = -1
        handle_name = None
        for name in l3.HANDLE_FIELDS:
            if name in fields:
                handle_at = fields.index(name)
                handle_name = name
                break
        for t, values in group.items():
            weight = 1
            if weight_at >= 0:
                declared = values[weight_at]
                if isinstance(declared, int) and not isinstance(declared, bool) \
                        and declared >= 1:
                    weight = declared
            atom = None
            if handle_at >= 0:
                token = l3._token(values[handle_at])
                if token is not None:
                    atom = handle_name + "=" + token
            out.append((t, weight, atom))
    for t, payload in state.verbatim.items():
        out.append((t, grammar_weight(payload), handle_atom(payload)))
    return out


def _cluster_uses(state, atom):
    """The `use` times of a handle cluster: first occurrence of each distinct payload.

    The Layer-3 rule, unchanged (`README-l3 §1`): a byte-identical repetition is
    **not** a use, so a flood of copies mints no importance mass. Payloads are
    rebuilt here and only here, for the members of a cluster that actually has
    more than one member — the case where "is this a restatement?" has to be
    asked at all.
    """
    ts = state.index.get(atom)
    if ts is None:
        return ()
    seen = set()
    uses = []
    for t in ts:
        payload = _episode_at(state, t)
        if payload is None:
            continue
        fingerprint = encode(payload)
        if fingerprint not in seen:
            seen.add(fingerprint)
            uses.append(t)
    return tuple(uses)


def _recency_sum(uses, now):
    total = Fraction(0, 1)
    for u in uses:
        total += Fraction(1, now + 1 - u)
    return total


def _cluster_rates(state, now):
    """`{atom: (numerator, denominator)}` for every multi-member handle cluster.

    A singleton cluster needs no entry: its importance is `weight / age`, computed
    inline in the sweep. Only a shared cluster needs its recency sum computed once
    and applied to each member.
    """
    rates = {}
    for atom, ts in state.index.items():
        if len(ts) < 2:
            continue
        uses = _cluster_uses(state, atom)
        if not uses:
            continue
        total = _recency_sum(uses, now)
        rates[atom] = (total.numerator, total.denominator)
    return rates


def _weakest(state, now, rates):
    """The least important irreducible episode, as `(num, den, t)`, or `None`.

    Importance as an exact rational, carried as a `(numerator, denominator)` pair
    so the sweep compares by integer cross-multiplication and constructs no
    `Fraction` in the hot loop — Layer 3's arithmetic, inherited verbatim. Ties
    break by `t` ascending, then canonical payload bytes, and the byte tier is
    materialized only on an exact importance-and-`t` tie, which `t`'s uniqueness
    makes unreachable and which is kept for totality.
    """
    best = None
    for t, weight, atom in _features(state):
        rate = rates.get(atom)
        if rate is None:
            cand = (weight, now + 1 - t, t)
        else:
            cand = (weight * rate[0], rate[1], t)
        if best is None:
            best = cand
            continue
        left = cand[0] * best[1]
        right = best[0] * cand[1]
        if left < right or (left == right and _break_tie(state, cand, best)):
            best = cand
    return best


def _break_tie(state, cand, best):
    if cand[2] != best[2]:
        return cand[2] < best[2]
    return encode(_episode_at(state, cand[2])) < encode(_episode_at(state, best[2]))


def _weaker(a, b):
    """Is candidate `a` evicted before `b`? Importance, then `t` (a total order)."""
    left = a[0] * b[1]
    right = b[0] * a[1]
    if left != right:
        return left < right
    return a[2] < b[2]


def _arriving_candidate(state, payload, t, rates):
    """What the arriving irreducible episode would present, at `now = t`."""
    atom = handle_atom(payload)
    uses = list(_cluster_uses(state, atom)) if atom is not None else []
    if uses:
        fingerprint = encode(payload)
        repeat = any(encode(_episode_at(state, u)) == fingerprint for u in uses)
        if not repeat:
            uses.append(t)
    else:
        uses = [t]
    total = _recency_sum(tuple(uses), t)
    return (grammar_weight(payload) * total.numerator, total.denominator, t)


def _forget_until(state, need, now, arriving):
    """Release irreducible episodes, least important first, until `need` fits.

    Returns `(state', keep_arriving)`. `keep_arriving` is false when the arriving
    episode is itself the weakest thing in play: evicting a *more* important item
    to house it would be the policy inverted (`README-l3 §1`).
    """
    cap = state.budget_cap
    while state.occupancy + need > cap:
        rates = _cluster_rates(state, now)
        victim = _weakest(state, now, rates)
        if victim is None:
            return state, False
        if arriving is not None:
            newcomer = _arriving_candidate(state, arriving, now, rates)
            if not _weaker(victim, newcomer):
                return state, False
        state, freed, payload = _drop_row(state, "kept", victim[2])
        if freed == 0:
            return state, False
        record, given = _forget(state.forgetting, victim[2], grammar_weight(payload))
        state = replace(state, occupancy=state.occupancy - freed + given,
                        forgetting=record)
    return state, True


# ---- phase 3: shedding whole entities from the derived schema ----------------

def _shed_until(state, need, now):
    """Drop whole entities from the interval table, first-seen first.

    The unit is the **entity** and never part of one: an entity whose chains were
    partly dropped could still be asked for its action-count profile, and a fold
    over what survived would be a confident undercount — a wrong answer where
    §3.0 pays 100 for an abstention. So a shed entity is marked `damaged` and its
    profile abstains forever after, while its surviving pairs keep answering
    current-value and as-of exactly (a later assertion is still the latest one).
    """
    cap = state.budget_cap
    while state.occupancy + need > cap and state.chains:
        victim = None
        for key, per in state.chains.items():
            if not per:
                continue
            entity = next(iter(per))
            born = next(iter(per[entity]))
            if victim is None or born < victim[2]:
                victim = (key, entity, born)
        if victim is None:
            break
        key, entity, _born = victim
        per = state.chains[key]
        chain = per[entity]

        freed = 1 + 2 * len(chain)
        record = state.forgetting
        given = 0
        demotions = state.demotions
        # What a shed assertion costs the ledger depends on what the ledger has
        # already said about it, and there are exactly three cases. An episode
        # still held is not a loss at all — `read(t)` answers it from its row —
        # but nothing regenerates it now, so it leaves the demotable tier. An
        # assertion under a key whose inversion already died was recorded as lost
        # when it died, and recording it twice would inflate the very count that
        # is supposed to equal the set of `t` the engine abstains on. Everything
        # else was released as a demotion, and shedding its chain is what makes
        # that booking false: it becomes a recorded loss and the demotion counter
        # gives it back.
        held = _held_stamps(state)
        already_lost = state.atlas.get(key) is None
        for stamp in chain:
            if stamp in held:
                state, _delta = _move_to_kept(state, stamp)
                continue
            if already_lost:
                continue
            record, delta = _forget(record, stamp, 1)
            given += delta
            demotions -= 1
        per = state.chains[key]
        smaller = _dict_del(per, entity)
        if smaller:
            chains = _dict_set(state.chains, key, smaller)
        else:
            chains = _dict_del(state.chains, key)
            freed += 1                                # the key's own cell

        cost = 0
        damaged = state.damaged
        irreducible = state.irreducible
        if entity not in damaged:
            damaged = damaged + (entity,)
            cost += 1
            if entity in irreducible:
                # The entity's profile can never be exact again, so the counts
                # that only a profile would have read are dead weight now.
                freed += 1 + 2 * len(irreducible[entity])
                irreducible = _dict_del(irreducible, entity)

        state = replace(state,
                        occupancy=state.occupancy - freed + cost + given,
                        chains=chains, irreducible=irreducible,
                        damaged=damaged, demotions=demotions,
                        forgetting=record)
    return state


# ---- applying a write -------------------------------------------------------

def _apply_schema(state, payload, fact, t, kind_after):
    """Fold one event into the derived schemas; return `(state', cells spent)`.

    `kind_after` is `atlas_after(state.atlas, payload, fact)`, computed once by
    `write` and passed in rather than recomputed here — one reading, one call
    site, so the entry the atlas ends up carrying and the entry the write path
    demoted by cannot be two different answers.
    """
    spent = _schema_delta(state, payload, fact)
    kind = payload.get("kind") if isinstance(payload, dict) else None
    counts = state.counts
    if kind in counts:
        counts = _dict_set(counts, kind, counts[kind] + 1)
    else:
        counts = _dict_set(counts, kind, 1)

    chains = state.chains
    atlas = state.atlas
    irreducible = state.irreducible

    if fact is not None:
        entity, key, value = fact
        per = chains.get(key)
        chain = {} if per is None else per.get(entity, {})
        chain = _dict_set(chain, t, value)
        per = _dict_set({} if per is None else per, entity, chain)
        chains = _dict_set(chains, key, per)
        if key not in atlas or atlas[key] != kind_after:
            # `kind_after` is `None` where the key has been seen under a second
            # grammar form, or under a payload this engine cannot rebuild. Either
            # way the inversion is no longer a function, so the engine stops
            # claiming it: assertions under this key still answer Q1/Q2 exactly
            # and reconstruct not at all. Honest loss, never a wrong payload —
            # and, since this write path is what `write` demoted by, never a loss
            # booked as a demotion either.
            atlas = _dict_set(atlas, key, kind_after)
    else:
        who = _actor(payload)
        if who is not None and who not in state.damaged:
            per = irreducible.get(who)
            if per is None:
                per = {kind: 1}
            else:
                per = _dict_set(per, kind, per.get(kind, 0) + 1)
            irreducible = _dict_set(irreducible, who, per)

    return replace(state, counts=counts, chains=chains, atlas=atlas,
                   irreducible=irreducible), spent


def _apply_record(state, payload, t, demotable):
    """Store the episode itself; return `(state', cells spent)`."""
    plan = _record_delta(state, payload, demotable=demotable)
    spent = plan["cost"]
    if plan["tier"] == "verbatim":
        state = replace(state, verbatim=_dict_set(state.verbatim, t,
                                                  copy_value(payload)))
    else:
        shape = plan["shape"]
        rows = state.demotable if demotable else state.kept
        group = rows.get(shape, {})
        group = _dict_set(group, t, row_values(payload, shape))
        rows = _dict_set(rows, shape, group)
        state = replace(state, **{"demotable" if demotable else "kept": rows})
    index, _given = _index_add(state.index, plan["atom"], t)
    return replace(state, index=index), spent


def _accept(state, payload, fact, t, keep_episode, kind_after):
    """Fold, optionally retain, and charge exactly what was spent.

    Regenerability — `kind_after is not None`, and **not** `fact is not None` —
    decides both the tier an episode is stored in and which ledger a released
    episode is written to. An event with a facet whose key does not invert is
    folded like any other assertion and answers Q1 and Q2 exactly, but **no chain
    rebuilds its payload**, so it is kept where the forgetting law can see it
    and, if it is released, it is released as a loss.
    """
    regenerable = kind_after is not None
    out, spent = _apply_schema(state, payload, fact, t, kind_after)
    if keep_episode:
        out, extra = _apply_record(out, payload, t, demotable=regenerable)
        spent += extra
        return replace(out, occupancy=state.occupancy + spent,
                       next_t=t + 1, last_cost=spent), t
    if regenerable:
        # Demotion at the door: the episode is redundant the moment the chain
        # holds it, so releasing it is counted, not mourned.
        return replace(out, occupancy=state.occupancy + spent, next_t=t + 1,
                       last_cost=spent, demotions=out.demotions + 1), t
    record, given = _forget(out.forgetting, t, grammar_weight(payload))
    return replace(out, occupancy=state.occupancy + spent + given, next_t=t + 1,
                   last_cost=spent, forgetting=record), t


def write(state, payload):
    """Consolidate one event; retain its episode while the budget allows.

    Below Layer 4 this is the frozen Layer-3 write, unchanged — the capped engine
    IS the forgetting engine (§7.4). At Layer 4 the order is: fold first, keep
    second, and never exceed the cap at any observable instant.
    """
    check_canonical(payload)
    if not isinstance(state, L4State):
        return l3.write(state, payload)

    t = state.next_t
    fact = facet(payload)
    cap = state.budget_cap
    kind_after = atlas_after(state.atlas, payload, fact)
    regenerable = kind_after is not None

    # Phase 0 — the ledger before the fold. If this event is what makes its key
    # ambiguous, every assertion already folded under that key stops being
    # regenerable in the same instant, and two claims the state is holding become
    # false at once (a demotable episode that nothing demotes, and a demotion that
    # is really a loss). Reconciling here rather than later keeps the invariant
    # true at every observable instant; it runs on a local state, so a write that
    # goes on to refuse leaves the key — and the ledger — exactly as it found them.
    working = state
    if fact is not None and not regenerable \
            and state.atlas.get(fact[1]) is not None:
        working = _reconcile_lost_key(working, fact[1])

    schema_room = _schema_delta(working, payload, fact, worst=True)
    record_room = _record_delta(working, payload, demotable=regenerable,
                                worst=True)["cost"]

    def drop_room(st):
        """Room for a write whose episode is not kept.

        A dropped **regenerable** assertion is a demotion and costs nothing
        beyond the fold. Everything else — an irreducible event, or an assertion
        whose key does not invert — is a loss, and recording a loss can grow the
        aggregated record: by up to a full coarsening step the first time, and by
        nothing at all once the record is full. Reserving exactly the growth it
        has left is what stops the act of recording a loss from breaching the
        very cap it is a consequence of.
        """
        if regenerable:
            return schema_room
        return schema_room + 3 + 2 * FORGET_BUCKETS - forget_cost(st.forgetting)

    if schema_room > cap:
        return state, None            # no eviction could ever make room (§4.1.2)

    # Phase 1 — lossless demotion: release episodes a chain already regenerates.
    working = _demote_until(working, schema_room + record_room)
    if working.occupancy + schema_room + record_room <= cap:
        return _accept(working, payload, fact, t, keep_episode=True,
                       kind_after=kind_after)

    # Phase 2 — an arrival nothing can regenerate is the only witness to its own
    # content, so it competes for room against the retained irreducibles on the
    # inherited Layer-3 law, and displaces nothing weaker than itself.
    if not regenerable:
        working, keep = _forget_until(working, schema_room + record_room, t, payload)
        if keep and working.occupancy + schema_room + record_room <= cap:
            return _accept(working, payload, fact, t, keep_episode=True,
                           kind_after=kind_after)

    # Phase 3 — the episode is not kept. For a regenerable assertion that costs
    # nothing at all: the chain rebuilds it. Otherwise it is a real loss, and
    # `_accept` writes it into the forgetting record.
    if working.occupancy + drop_room(working) <= cap:
        return _accept(working, payload, fact, t, keep_episode=False,
                       kind_after=kind_after)

    working, _keep = _forget_until(working, drop_room(working), t, None)
    if working.occupancy + drop_room(working) <= cap:
        return _accept(working, payload, fact, t, keep_episode=False,
                       kind_after=kind_after)

    # Phase 4 — the derived schema itself does not fit: shed supersession chains.
    working = _shed_until(working, drop_room(working), t)
    if working.occupancy + drop_room(working) <= cap:
        return _accept(working, payload, fact, t, keep_episode=False,
                       kind_after=kind_after)

    return state, None                                # a deterministic refusal


# ---- reading ----------------------------------------------------------------

def _row_at(state, t):
    """The retained episode at `t` reconstructed from its row, or `None`."""
    for rows in (state.kept, state.demotable):
        for shape, group in rows.items():
            values = group.get(t)
            if values is not None:
                return row_payload(shape, values)
    payload = state.verbatim.get(t)
    if payload is not None:
        return copy_value(payload)
    return None


def covers_from(state):
    """The earliest logical time the interval table still covers.

    Every chain is ascending in `t`, and within one attribute key the entities
    sit in first-assertion order, so a key's first entity carries that key's
    smallest first-`t` — and the minimum over the key vocabulary is the smallest
    first-`t` in the whole table. Nothing before it can be in any chain, so a
    reconstruction below it abstains in `O(keys)` instead of sweeping every pair.

    It costs **no cells**: it is read off the table's own ordering rather than
    stored, which is the only kind of index this budget can afford (§0 of
    `README-l4.md`). Where nothing has been shed it is `0` and the shortcut never
    fires; where the schema has been squeezed it is exactly the boundary of what
    consolidation still remembers.
    """
    floor = None
    for per in state.chains.values():
        if not per:
            continue
        chain = per[next(iter(per))]
        if not chain:
            continue
        born = next(iter(chain))
        if floor is None or born < floor:
            floor = born
    return 0 if floor is None else floor


def _assertion_at(state, t):
    """`(entity, key, value)` for the assertion stored at `t`, or `None`.

    **The search the budget forces.** The interval table indexes
    `(entity, key) -> history`; an exact inverse would cost one cell per
    assertion and put the schema 30% over the footprint gate, so the inverse is
    recomputed instead of stored. Every inner map is keyed by `t`, so the scan is
    one hash lookup per pair — time, which §4.1 does not budget, in place of
    cells, which it does. Key-major nesting is what keeps it cheap in practice:
    the outer loop runs over a closed vocabulary of a dozen or so attribute keys,
    so the scan is a handful of iterator set-ups over large maps rather than
    thousands over tiny ones.
    """
    if t < covers_from(state):
        return None
    for key, per in state.chains.items():
        # The membership sweep runs over `per.values()` and not `per.items()`:
        # the sweep is the whole cost of reconstruction and pays for a tuple
        # unpack on every pair, while the owning entity is needed only on the one
        # pair that hits. Recovering it costs a second walk of a single key's
        # map — once per read, against a sweep of every pair in the table.
        for chain in per.values():
            if t in chain:
                for entity, owned in per.items():
                    if owned is chain:
                        return (entity, key, chain[t])
    return None


def read(state, t):
    """The event at `t`: retained verbatim, regenerated from the schema, or gone."""
    if not isinstance(state, L4State):
        return l3.read(state, t)
    if not isinstance(t, int) or isinstance(t, bool):
        return None
    if t < 0 or t >= state.next_t:
        return None
    payload = _row_at(state, t)
    if payload is not None:
        return {"payload": payload, "t": t}
    found = _assertion_at(state, t)
    if found is None:
        return None
    entity, key, value = found
    kind = state.atlas.get(key)
    if kind is None:
        return None                    # the key's inversion is not a function
    rebuilt = rebuild(kind, entity, key, value)
    if rebuilt is None:
        return None
    return {"payload": rebuilt, "t": t}


def read_range(state, t0, t1):
    """Every event in `[t0, t1]` the engine can still produce, `t` ascending."""
    if not isinstance(state, L4State):
        return l3.read_range(state, t0, t1)
    if not isinstance(t0, int) or isinstance(t0, bool):
        return []
    if not isinstance(t1, int) or isinstance(t1, bool):
        return []
    lo = max(0, t0)
    hi = min(t1, state.next_t - 1)
    out = []
    t = lo
    while t <= hi:
        event = read(state, t)
        if event is not None:
            out.append(event)
        t += 1
    return out


def retained(state):
    """The number of episodes still held (consolidated content is not an episode)."""
    if not isinstance(state, L4State):
        return l3.retained(state)
    total = len(state.verbatim)
    for rows in (state.kept, state.demotable):
        for group in rows.values():
            total += len(group)
    return total


def current(state, entity, key):
    """The value in force for `(entity, key)` now, or `None` — Q1."""
    per = state.chains.get(key)
    if per is None:
        return None
    chain = per.get(entity)
    if not chain:
        return None
    last = next(reversed(chain))
    return (last, chain[last])


def asof(state, entity, key, t):
    """The value in force for `(entity, key)` at logical time `t`, or `None` — Q2.

    Interval arithmetic on integer logical stamps: the assertion in force at `t`
    is the greatest `t' <= t` in the chain. Graphiti's `valid_at`/`invalid_at`
    (GAPMAP **S3**) without its two model calls, and — unlike the read path that
    steal was taken from — supersession is **honoured by default**: a `t` before
    the pair's first assertion abstains rather than returning the earliest value.
    """
    per = state.chains.get(key)
    if per is None:
        return None
    chain = per.get(entity)
    if not chain:
        return None
    for stamp in reversed(chain):
        if stamp <= t:
            return (stamp, chain[stamp])
    return None


def profile(state, entity):
    """`{kind: count}` for one entity — Q3 — or `None` when it cannot be exact.

    A fold over that entity's complete chains, plus the irreducible counts no
    fold can reach: an event whose content no schema regenerates still leaves the
    schema knowing **that** it happened, and of what kind, when the episode
    itself is long gone.
    """
    if entity in state.damaged:
        return None
    counted = {}
    for key, per in state.chains.items():
        chain = per.get(entity)
        if not chain:
            continue
        kind = state.atlas.get(key)
        if kind is None:
            return None                    # cannot attribute these to one kind
        counted[kind] = counted.get(kind, 0) + len(chain)
    extra = state.irreducible.get(entity)
    if extra is not None:
        for kind, n in extra.items():
            counted[kind] = counted.get(kind, 0) + n
    if not counted:
        return None
    return counted


# ---- recall (the Layer-2/3 cue channel, over retained episodes) --------------

def recall(state, cue):
    """Recover the single retained episode satisfying the content probe `cue`.

    The Layer-3 channel, unchanged in shape: the handle atom narrows to a
    cluster, exact containment verifies the whole probe, and the engine answers
    only when **one** retained episode survives both. What changed is what
    "retained" means — an episode released into consolidated form is no longer
    reachable by cue, which is the honest price of the compression and is stated
    as a non-capability in `README-l4.md §4`.
    """
    if not isinstance(cue, dict):
        return _abstain()
    try:
        check_canonical(cue)
    except NonCanonical:
        return _abstain()
    atom = handle_atom(cue)
    if atom is None:
        return _abstain()
    ts = state.index.get(atom)
    if ts is None:
        return _abstain()
    hit = None
    for t in ts:
        payload = _row_at(state, t)
        if payload is None:
            continue
        if l3._contains(payload, cue):
            if hit is not None:
                return _abstain()                     # ambiguous: two fit
            hit = (t, payload)
    if hit is None:
        return _abstain()
    t, payload = hit
    return _answer({"payload": payload, "t": t}, 1000,
                   {"support": [t], "kind": "recall", "t_asof": t})


# ---- the Answer (§7.2) & the generic query binding --------------------------

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
    if not isinstance(state, L4State):
        return l3.query(state, q)
    if not isinstance(q, dict):
        return _abstain()
    op = q.get("op")

    if op == "read":
        event = read(state, q.get("t"))
        if event is None:
            return _abstain()
        held = _row_at(state, event["t"]) is not None
        prov = {"support": [event["t"]],
                "kind": "recall" if held else "derive",
                "t_asof": event["t"]}
        return _answer(event, 1000, prov)

    if op == "read_range":
        events = read_range(state, q.get("t0"), q.get("t1"))
        if events:
            support = [e["t"] for e in events]
            prov = {"support": support, "kind": "aggregate", "t_asof": support[-1]}
            return _answer(events, 1000, prov)
        return _answer(events, 1000, None)

    if op == "recall":
        return recall(state, q.get("cue"))

    if op == "current":
        found = current(state, q.get("entity"), q.get("key"))
        if found is None:
            return _abstain()
        t, value = found
        return _answer(value, 1000,
                       {"support": [t], "kind": "derive", "t_asof": t})

    if op == "asof":
        t = q.get("t")
        if not isinstance(t, int) or isinstance(t, bool):
            return _abstain()
        found = asof(state, q.get("entity"), q.get("key"), t)
        if found is None:
            return _abstain()
        stamp, value = found
        return _answer(value, 1000,
                       {"support": [stamp], "kind": "derive", "t_asof": t})

    if op == "profile":
        counted = profile(state, q.get("entity"))
        if counted is None:
            return _abstain()
        # A fold over the whole stream has no bounded support to cite: the
        # episodes it counts are mostly gone. Provenance is dormant until Layer 7
        # (§4.2) and `null` is legal until then; §4.2's schema has no form for
        # "supported by everything", which is a seam Layer 7 will have to close.
        return _answer(counted, 1000, None)

    if op == "count":
        kind = q.get("kind")
        if kind not in state.counts:
            return _abstain()
        return _answer(state.counts[kind], 1000, None)

    if op == "consolidation":
        return _answer({"demotions": state.demotions,
                        "keys": len(state.chains),
                        "pairs": sum(len(per) for per in state.chains.values()),
                        "assertions": sum(len(chain)
                                          for per in state.chains.values()
                                          for chain in per.values()),
                        "episodes": retained(state),
                        "damaged": len(state.damaged)}, 1000, None)

    if op == "forgetting":
        asof_t = state.next_t - 1 if state.next_t > 0 else 0
        return _answer(_forgetting_body(state.forgetting), 1000,
                       {"support": [], "kind": "absent", "t_asof": asof_t})

    if op == "forgot_at":
        t = q.get("t")
        if not isinstance(t, int) or isinstance(t, bool) or t < 0:
            return _abstain()
        count, mass = forget_bucket_at(state.forgetting, t)
        asof_t = state.next_t - 1 if state.next_t > 0 else 0
        return _answer({"count": count, "mass": mass,
                        "width": state.forgetting.width}, 1000,
                       {"support": [], "kind": "absent", "t_asof": asof_t})

    return _abstain()                                 # capability absent (§7.3)


# ---- snapshot / restore -----------------------------------------------------
#
# Every branch below is a LIST of lists rather than an object, for two reasons
# that are the same reason: canonical JSON keys must be strings (§2.4), so an
# integer entity id would have to be stringified and un-stringified — and
# `payload_cost` charges one cell per key, so a list form makes the serialized
# atom count *equal* the engine's own accounting rather than merely close to it.
# That equality is what `trials/ascension/l4/t_consolidation.py`'s rule-P audit
# checks from outside the engine (R4 clause 3).

def _rows_body(rows):
    return [[shape[0], list(shape[1]),
             [[t] + list(values) for t, values in group.items()]]
            for shape, group in rows.items()]


def _rows_from_body(raw, what):
    out = {}
    for entry in raw:
        if not isinstance(entry, list) or len(entry) != 3:
            raise CorruptSnapshot("snapshot %s entry is malformed" % (what,))
        kind, fields, group = entry
        if not isinstance(kind, str) or not isinstance(fields, list) \
                or not isinstance(group, list):
            raise CorruptSnapshot("snapshot %s shape is malformed" % (what,))
        shape = (kind, tuple(fields))
        rows = {}
        for row in group:
            if not isinstance(row, list) or len(row) != 1 + len(fields):
                raise CorruptSnapshot("snapshot %s row width is wrong" % (what,))
            rows[row[0]] = tuple(row[1:])
        out[shape] = rows
    return out


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
        "chains": [[key, [[entity, [[t, v] for t, v in chain.items()]]
                          for entity, chain in per.items()]]
                   for key, per in state.chains.items()],
        "atlas": [[key, kind] for key, kind in state.atlas.items()],
        "irreducible": [[entity, [[kind, n] for kind, n in per.items()]]
                        for entity, per in state.irreducible.items()],
        "counts": [[kind, n] for kind, n in state.counts.items()],
        "damaged": list(state.damaged),
        "demotable": _rows_body(state.demotable),
        "kept": _rows_body(state.kept),
        "verbatim": [[t, copy_value(p)] for t, p in state.verbatim.items()],
        "index": [[atom, list(ts)] for atom, ts in state.index.items()],
        "demotions": state.demotions,
        "forgetting": _forgetting_body(state.forgetting),
    }


def state_checksum(state):
    """SHA-256 hex over the canonical encoding of the full state body (§2.4)."""
    if not isinstance(state, L4State):
        return l3.state_checksum(state)
    return hashlib.sha256(encode(_body(state))).hexdigest()


def snapshot(state):
    """Canonical, checksummed serialization of the state (§7.1, §2.4)."""
    if not isinstance(state, L4State):
        return l3.snapshot(state)
    body = _body(state)
    checksum = hashlib.sha256(encode(body)).hexdigest()
    return encode({"magic": MAGIC, "checksum": checksum, "body": body})


def restore(data):
    """Rebuild a state from snapshot bytes; fail loudly on any corruption.

    A Layer-3 snapshot restores through the frozen Layer-3 path, so a capped
    engine's state round-trips exactly as it always did. Four guards on the
    Layer-4 form: the envelope and its SHA-256; the shape of every branch; the
    handle index rederived from the retained episodes must equal the stored one;
    and the recomputed occupancy must equal the stored one, which is the check
    that the incremental accounting of the write path never drifted.
    """
    try:
        envelope = decode(data)
    except Exception as exc:                          # invalid JSON / UTF-8 / float
        raise CorruptSnapshot("snapshot is not decodable: %r" % (exc,))
    if not isinstance(envelope, dict) or frozenset(envelope.keys()) != _ENVELOPE_KEYS:
        raise CorruptSnapshot("snapshot envelope keys are wrong")
    if envelope["magic"] != MAGIC:
        return l3.restore(data)

    body = envelope["body"]
    if not isinstance(body, dict) or frozenset(body.keys()) != _BODY_KEYS:
        raise CorruptSnapshot("snapshot body keys are wrong")
    if hashlib.sha256(encode(body)).hexdigest() != envelope["checksum"]:
        raise CorruptSnapshot("snapshot checksum mismatch (corruption detected)")

    for name in ("layer_cap", "budget_cap", "occupancy", "next_t", "demotions"):
        value = body[name]
        if not isinstance(value, int) or isinstance(value, bool):
            raise CorruptSnapshot("snapshot %s is not an integer" % (name,))

    chains = {}
    for entry in body["chains"]:
        if not isinstance(entry, list) or len(entry) != 2:
            raise CorruptSnapshot("snapshot chain entry is malformed")
        key, per_raw = entry
        per = {}
        for pair in per_raw:
            if not isinstance(pair, list) or len(pair) != 2:
                raise CorruptSnapshot("snapshot chain pair is malformed")
            entity, raw = pair
            chain = {}
            previous = None
            for item in raw:
                if not isinstance(item, list) or len(item) != 2:
                    raise CorruptSnapshot("snapshot chain entry is not (t, value)")
                t = item[0]
                if not isinstance(t, int) or isinstance(t, bool) \
                        or (previous is not None and t <= previous):
                    raise CorruptSnapshot("snapshot chain is not ascending in t")
                previous = t
                chain[t] = item[1]
            per[entity] = chain
        chains[key] = per

    atlas = {}
    for entry in body["atlas"]:
        if not isinstance(entry, list) or len(entry) != 2:
            raise CorruptSnapshot("snapshot atlas entry is malformed")
        atlas[entry[0]] = entry[1]

    irreducible = {}
    for entry in body["irreducible"]:
        if not isinstance(entry, list) or len(entry) != 2:
            raise CorruptSnapshot("snapshot irreducible entry is malformed")
        irreducible[entry[0]] = {k: n for k, n in entry[1]}

    counts = {}
    for entry in body["counts"]:
        if not isinstance(entry, list) or len(entry) != 2:
            raise CorruptSnapshot("snapshot counter entry is malformed")
        counts[entry[0]] = entry[1]

    demotable = _rows_from_body(body["demotable"], "demotable")
    kept = _rows_from_body(body["kept"], "kept")

    verbatim = {}
    for entry in body["verbatim"]:
        if not isinstance(entry, list) or len(entry) != 2:
            raise CorruptSnapshot("snapshot verbatim entry is malformed")
        verbatim[entry[0]] = copy_value(entry[1])

    index = {}
    for entry in body["index"]:
        if not isinstance(entry, list) or len(entry) != 2 \
                or not isinstance(entry[1], list):
            raise CorruptSnapshot("snapshot index entry is malformed")
        index[entry[0]] = tuple(entry[1])

    record = l3._forgetting_from_body(body["forgetting"])

    state = L4State(layer_cap=body["layer_cap"], budget_cap=body["budget_cap"],
                    occupancy=body["occupancy"], next_t=body["next_t"],
                    last_cost=0, chains=chains, atlas=atlas,
                    irreducible=irreducible, counts=counts,
                    damaged=tuple(body["damaged"]), demotable=demotable,
                    kept=kept, verbatim=verbatim, index=index,
                    demotions=body["demotions"], forgetting=record)

    if _rederived_index(state) != index:
        raise CorruptSnapshot("snapshot index diverges from the retained episodes")
    if accounted_occupancy(state) != body["occupancy"]:
        raise CorruptSnapshot("snapshot occupancy diverges from the accounted cost")
    return state


def _rederived_index(state):
    """The handle index rebuilt from the retained episodes alone."""
    index = {}
    for t, payload in _all_episodes(state):
        atom = handle_atom(payload)
        if atom is None:
            continue
        prev = index.get(atom)
        index[atom] = (prev + (t,)) if prev is not None else (t,)
    return index


def _all_episodes(state):
    """`[(t, payload)]` over every retained episode, in the index's own order."""
    out = []
    for rows in (state.demotable, state.kept):
        for shape, group in rows.items():
            for t, values in group.items():
                out.append((t, row_payload(shape, values)))
    for t, payload in state.verbatim.items():
        out.append((t, payload))
    out.sort()
    return out


# ---- the generic engine interface (§7, INTERFACE.md) ------------------------

def empty():
    """A fresh, full Layer-4 engine state (adapter contract, §7)."""
    return new_state(layer_cap=LAYER, budget_cap=DEFAULT_BUDGET)


def make_engine(layer_cap, budget_cap=DEFAULT_BUDGET):
    """A fresh state capped at `layer_cap` (§7.4). 3 = the frozen forgetting engine."""
    return new_state(layer_cap=layer_cap, budget_cap=budget_cap)


def ingest(state, payload):
    """Append one event; return `(state', t)`. `t` is None only on a hard refusal."""
    return write(state, payload)


def last_cost(state):
    """Integer work-unit cost of the most recent successful write (§3.3, §4.1)."""
    return state.last_cost

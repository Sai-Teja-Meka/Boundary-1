"""core/layers/l5_prospection.py — Layer 5: Prospection (intentions that fire).

Layers 1–4 are folds over the **past**: retention returned what was written,
recall found it by content, forgetting chose what to drop, consolidation derived
what it could no longer hold. Every one of them consults the arriving payload and
the current state and nothing else. Layer 5 is the first capability that
**watches**: an intention is written now, held, and evaluated against every event
that arrives afterwards, and when one satisfies it the engine **emits an event of
its own** — once, at a logical time of its own, and never again.

Pure, integer-only (§2), built entirely on the frozen Layer-1/2/3/4 primitives;
it edits none of them (§9). Below `layer_cap = 5` the state IS the frozen
Layer-4 state and every verb delegates to it, so `make_engine(4)` is not an
imitation of the consolidation engine — it is the consolidation engine (§7.4).

The full design record is `core/layers/README-l5.md`. This docstring states what
the code does; that document states why the 45 638-cell budget admits no other
shape.

## The four ratified sentences this layer is built out of

`BOUNDARY-RULINGS.md R6` clause 2 settles what a firing does to logical time,
and the clause is the spine of this file:

> *A trigger's firing is an event (`§5 L5`: `intend(condition → event)`). Under
> `§1.4` an in-engine event record is exactly `{payload, t}`, and under `§1.3`
> `t` is unique within a state and strictly increasing in ingestion order.
> Therefore a firing consumes a logical `t` of its own, assigned in the same pure
> transition as the caller write that satisfied it, immediately after that write
> and before any later caller write, consecutively and in `iid` ascending order
> where one write satisfies several pending intentions. `ingest` returns the
> **caller** event's `t`. One caller `ingest` therefore advances `next_t` by
> `1 + f`.*

`f = 0` on a stream with nothing pending, which is why Layers 1–4 do not move
and not by exception (`STAGE-B.md §1.4`).

`ATTAINABILITY.md`'s Reading 1 settles the other half: an intention is an
**event**, not a fourth verb, because `§7.1` declares three operations and
`§1.1` says events are the only fuel. So `intend` arrives as an ingested payload
under a **declared reading** of the frozen grammar — `INTENTION_FORM` below —
exactly as `ASSERTION_FORMS` is at Layer 4 and `HANDLE_FIELDS` at Layer 3.

## What is stored, and what is not evictable

| component | cells | answers |
|---|---|---|
| everything Layer 4 stores | (`l4_consolidation`) | Q1–Q4, `recall`, the ledger |
| pending set `{shape: {iid: (t0, cond) + fire values}}` | `1 + width` per shape, `2 + cond + width` per entry | P1 for an intention that has not fired; `read(t0)` |
| fired ledger `{shape: {iid: (t,) + fire values}}` | `1 + width` per shape, `2 + width` per entry | P1, `read(t_fire)`, and **exactly-once** |

**Neither is evictable, and that is the layer rather than a convenience.**
`miss = 0` means an intention whose condition is satisfied fires, so a pending
entry an engine dropped would be an intention it silently forgot; `dup-fire = 0`
means a fired intention never fires again, so a fired entry an engine dropped
would be an intention it could fire twice. An eviction path that could reach
either would be an engine that can be made to break the gate by being poor. What
gives way under pressure is the **episodic tier**, exactly as at Layer 4, and
every loss is booked.

## Arming, and the three things that are not intentions

An arriving `intend` payload is **armed** — held in the pending set — only when
all of these hold. Otherwise it is an ordinary event and takes the frozen
Layer-4 write path, where it is irreducible and competes for room under the
inherited Layer-3 importance law:

  * its condition is **readable** under the closed predicate vocabulary
    (`readable`): an engine arms only what it can evaluate, so an unreadable
    condition never becomes an intention that silently never fires;
  * the payload is **invertible** from `(iid, cond, fire)` by canonical bytes
    (§2.4) — Layer 4's *fold only what inverts* rule, applied to the pending set,
    which is what makes releasing the episode at the door a demotion and not a
    loss;
  * its `iid` is **not already known**, pending or fired. `§5 L5` names no
    cancellation, revocation, expiry or **re-arming** (`grammar.md`, *No
    cancellation*), so the first arming of an `iid` wins and a later payload
    carrying it arms nothing. This is the one place the fired ledger is read on
    the **write** path rather than the firing path, and it is why the ledger
    cannot be decorative.

## Firing, in one pure transition

After the caller event is folded, the arriving event is evaluated against every
eligible pending intention — every one written at a **strictly earlier** logical
time — and the satisfied ones fire in `iid` ascending order, each at the next
consecutive `t`. Each firing:

  1. leaves the pending set and enters the fired ledger, which is where
     exactly-once lives; the swap **frees** `cond` cells, so a firing pays for
     itself in all but the shape header;
  2. **books the intention's own episode as lost.** The episode was released at
     arming as a demotion, because the pending entry regenerated it; the pending
     entry is now gone, `read(t0)` abstains forever, and a demotion that has
     become a loss is corrected in the same instant — `README-l4 §4`'s
     `_reconcile_lost_key` discipline, applied to promises;
  3. is itself folded like any other event (its counter, and its assertion chain
     if the fired payload has a Layer-4 facet) and its own episode released into
     the fired ledger, which regenerates it — a demotion;
  4. is then evaluated in its turn. **Cascades take the plain uniform reading**
     (an emitted event is an event, and conditions are evaluated against all
     events). `R6` clause 2 expressly leaves the question open and records that
     it is *unobservable* on `corpora/l5stream` by the GUARDEDNESS induction, so
     both readings give the identical schedule there; the uniform one is taken
     because it is the reading that needs no exception, and the work list is FIFO
     so events are always evaluated in `t` order.

Firing is **not discretionary** (`R6` clause 2). Where the budget cannot house a
firing even after eviction, the engine refuses the whole transition under
`§4.1.2` — `t` unspent, state unchanged — because an event that never happened
cannot have satisfied anything. That is the honest response and not a missed
trigger; `refused` is reported and the Layer-5 gate asserts it is 0.

## Determinism and the Answer contract

Identical streams produce byte-identical snapshots (§2.3): every structure is a
dict in first-seen order, the firing order is `iid` ascending (a declared total
order, not a scan order), and the work list is FIFO. Capability absence is a
scored abstention, never an exception (§7.3): an unknown `iid`, an intention that
has not fired, and a `t` nothing regenerates all **abstain**.

Calibration is dormant until Layer 6 (§3.4). Confidence is emitted — 1000 on a
structurally certain answer — and is **ungated**, which `README-l5.md §5` records
as the seam Layer 6 opens on this engine.
"""

import hashlib
from dataclasses import dataclass, replace

from core.serialize import encode, decode, copy_value, check_canonical
from core.state import payload_cost
from core.layers import l4_consolidation as l4
from core.layers import l3_forgetting as l3
from core.layers.l4_consolidation import (
    L4State, facet, rebuild, invertible, atlas_after,
    row_shape, row_values, row_payload,
    ASSERTION_FORMS, CorruptSnapshot,
)
from core.layers.l3_forgetting import grammar_weight, FORGET_BUCKETS

LAYER = 5

# A generous default cap, matching the Layer-1/2/3/4 defaults so cross-layer
# reasoning stays simple. Integer only (§2.2). The Layer-5 trials always pass an
# explicit cap — at the gate, `raw_cells // 4` (R6 clause 4).
DEFAULT_BUDGET = 1_000_000_000

MAGIC = "boundary1-l5-snapshot"
_ENVELOPE_KEYS = frozenset({"magic", "checksum", "body"})
_BODY_KEYS = frozenset({"layer_cap", "budget_cap", "occupancy", "next_t",
                        "chains", "atlas", "irreducible", "counts", "damaged",
                        "demotable", "kept", "verbatim", "index", "demotions",
                        "forgetting", "pending", "fired"})


# ---- the intention facet: a declared reading of the frozen grammar -----------
#
# `corpora/l5stream/grammar.md` freezes the shape
# `{"kind":"intend","iid":<int>,"cond":<AST>,"fire":<payload>}`. This is the
# Layer-5 counterpart of `ASSERTION_FORMS` — a reading of a frozen grammar, not
# a learner — and, exactly as there, it is paired with an inverse so that
# releasing the episode can be proved lossless rather than assumed to be.

INTENTION_KIND = "intend"
INTENTION_FORM = ("iid", "cond", "fire")


def intention(payload):
    """Read one payload as an `(iid, condition, fire payload)` intention, or `None`.

    `None` is the answer for everything that is not an intention this engine can
    arm. It is deliberately structural: a payload of the right `kind` whose `iid`
    is not an integer, or which carries a field the inverse cannot reproduce, is
    not an intention with a defect — it is an ordinary event.
    """
    if not isinstance(payload, dict):
        return None
    if payload.get("kind") != INTENTION_KIND:
        return None
    iid = payload.get("iid")
    if not isinstance(iid, int) or isinstance(iid, bool):
        return None
    cond = payload.get("cond")
    fire = payload.get("fire")
    if not isinstance(cond, dict) or fire is None:
        return None
    return (iid, cond, fire)


def rebuild_intention(iid, cond, fire):
    """Invert the intention facet: the payload an armed intention came from."""
    return {"kind": INTENTION_KIND, "iid": iid, "cond": cond, "fire": fire}


def arms(payload):
    """Does this payload arm an intention, and with what? `None` if it does not.

    Three conditions, all of them structural (module docstring): the condition is
    readable under the closed vocabulary, and the payload round-trips through
    `rebuild_intention` as **canonical bytes** (§2.4, not Python equality —
    `True == 1` there and `true != 1` here). The third condition, that the `iid`
    is not already known, needs the state and is checked by `write`.
    """
    read = intention(payload)
    if read is None:
        return None
    iid, cond, fire = read
    if not readable(cond):
        return None
    if encode(rebuild_intention(iid, cond, fire)) != encode(payload):
        return None
    return read


# ---- the condition grammar: the closed predicate vocabulary, evaluated -------
#
# `corpora/l5stream/grammar.md` freezes six predicates and three connectives.
# `readable` is the validator and `satisfies` the evaluator, and they are written
# as a pair on purpose: **the engine arms only what it can evaluate**, so
# `satisfies` is total on every condition `readable` admits and never raises
# inside a write. `trials/_l5tasks.satisfies` is the battery's independent
# implementation of the same reading, and
# `trials/ops/l5/t_l5_composition.py` asserts the two agree event by event over
# the whole frozen stream — one reading, two implementations, checked rather
# than assumed, exactly as `ops/l4` does for the assertion facet.

CONNECTIVES = ("and", "or", "not")
PREDICATES = ("kind", "entity", "key", "val_ge", "loc", "count_ge")

# The predicates whose `v` must be an integer, because they are compared with
# `>=`. A string there is not a false condition; it is a condition this engine
# declines to arm.
_INT_VALUED_PREDICATES = frozenset({"val_ge", "count_ge"})


def readable(cond):
    """Is `cond` an AST this engine can evaluate, under the closed vocabulary?

    An unreadable condition is **not armed** (`arms`). That is the honest
    response: an engine that stored a condition it could not evaluate would be
    holding an intention that never fires for a reason it never recorded, which
    is `autopsy/GAPMAP.md §2`'s *recorded but never binding* in its purest form.
    """
    if not isinstance(cond, dict):
        return False
    if "op" in cond:
        op = cond["op"]
        args = cond.get("args")
        if op not in CONNECTIVES or not isinstance(args, list) or not args:
            return False
        if op == "not" and len(args) != 1:
            return False
        for arg in args:
            if not readable(arg):
                return False
        return True
    p = cond.get("p")
    if p not in PREDICATES:
        return False
    if "v" not in cond:
        return False
    v = cond["v"]
    if p in _INT_VALUED_PREDICATES and (not isinstance(v, int)
                                        or isinstance(v, bool)):
        return False
    if p == "count_ge" and not isinstance(cond.get("k"), str):
        return False
    return True


def _subject(payload):
    """The entity a payload is about: `entity`, else `src` (a link's source)."""
    who = payload.get("entity")
    if not isinstance(who, int) or isinstance(who, bool):
        who = payload.get("src")
    if not isinstance(who, int) or isinstance(who, bool):
        return None
    return who


def satisfies(cond, payload, counts):
    """Does `payload` satisfy `cond`? `counts` is kind -> count INCLUDING payload.

    Pure, integer, total on every condition `readable` admits. `count_ge` is the
    one predicate that reads nothing of the arriving payload and everything of
    the past: it is a fold over the per-kind counters Layer 4 already maintains,
    which is why a condition over content **consolidation has demoted** is
    answerable at all (`grammar.md`: *"it is why this layer is built on that
    one"*).
    """
    if "op" in cond:
        op = cond["op"]
        args = cond["args"]
        if op == "and":
            for arg in args:
                if not satisfies(arg, payload, counts):
                    return False
            return True
        if op == "or":
            for arg in args:
                if satisfies(arg, payload, counts):
                    return True
            return False
        return not satisfies(args[0], payload, counts)

    p = cond["p"]
    v = cond["v"]
    if p == "kind":
        return payload.get("kind") == v
    if p == "entity":
        return _subject(payload) == v
    if p == "count_ge":
        return counts.get(cond["k"], 0) >= v
    if p == "loc":
        return payload.get("loc") == v

    found = facet(payload)
    if p == "key":
        return found is not None and found[1] == v
    # val_ge
    if found is None:
        return False
    value = found[2]
    return isinstance(value, int) and not isinstance(value, bool) and value >= v


# ---- the state --------------------------------------------------------------

@dataclass(frozen=True)
class L5State(L4State):
    """The frozen Layer-5 engine state (§2.1).

    A **subclass** of the frozen `L4State`, which is what makes Layer 4 an
    inheritance rather than a re-implementation: every Layer-4 verb, cost
    function and eviction phase operates on this state unchanged, `replace()`
    returns an `L5State`, and the single `occupancy` counter covers the
    prospection tiers too — so the Layer-4 write path evicts *around* them
    without knowing they are there.

    `pending` and `fired` are grouped by the fire payload's **row shape**, the
    Layer-4 row codec (`README-l4 §0.2`): the grammar (`kind` and field names) is
    paid for once per shape per tier, and each entry carries only its own values.
    A fire payload no shape expresses is stored under the `None` shape, verbatim.
    """

    pending: dict = None    # shape -> {iid: (t0, cond) + fire values}
    fired: dict = None      # shape -> {iid: (t,) + fire values}


def new_state(layer_cap, budget_cap):
    """A fresh state capped at `layer_cap` with integer budget cap `budget_cap`.

    Below Layer 5 this returns the **frozen Layer-4 state** (§7.4), which below
    Layer 4 is the frozen Layer-3 state, and so down. Capping is a
    construction-time restriction, and the honest way to build an engine without
    prospection is to build the engine that does not have it.
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
        return l4.new_state(layer_cap=layer_cap, budget_cap=budget_cap)
    base = l4.new_state(layer_cap=LAYER, budget_cap=budget_cap)
    return L5State(layer_cap=layer_cap, budget_cap=budget_cap,
                   occupancy=base.occupancy, next_t=0, last_cost=0,
                   chains={}, atlas={}, irreducible={}, counts={}, damaged=(),
                   demotable={}, kept={}, verbatim={}, index={}, demotions=0,
                   forgetting=base.forgetting, pending={}, fired={})


# ---- cost accounting (§4.1, priced under rule P — R4 clause 3) --------------
#
# One cell, one grammar atom. Every figure below is the `payload_cost` of the
# corresponding branch of the snapshot body, so the engine's own accounting and
# the atoms a reader can count in its serialized state are the same number.

def _shape_cells(shape):
    """The shape header: its `kind` tag and its field names, paid once per tier."""
    if shape is None:
        return 1                              # the `null` that stands for it
    return 1 + len(shape[1])


def _values_cells(shape, values):
    """The fire payload's own cells inside an entry."""
    if shape is None:
        return payload_cost(values[0])
    return len(shape[1])


def pending_cells(pending):
    """`iid`, `t0`, the condition AST, and the fire payload — per pending entry."""
    total = 0
    for shape, group in pending.items():
        total += _shape_cells(shape)
        for entry in group.values():
            total += 1 + 1 + payload_cost(entry[1])
            total += _values_cells(shape, entry[2:])
    return total


def fired_cells(fired):
    """`iid`, the firing's own `t`, and the fire payload — per fired entry."""
    total = 0
    for shape, group in fired.items():
        total += _shape_cells(shape)
        for entry in group.values():
            total += 1 + 1 + _values_cells(shape, entry[1:])
    return total


def accounted_occupancy(state):
    """Recompute occupancy from the state alone — `restore`'s independent guard.

    The write path maintains `occupancy` incrementally (it must: recomputing per
    write is quadratic). This is the check that the increments never drifted,
    and `trials/ops/l5/t_l5_composition.py` asserts the identity after arming,
    after firing and after every kind of eviction rather than only at the end.
    """
    if not isinstance(state, L5State):
        return l4.accounted_occupancy(state)
    return (l4.accounted_occupancy(state)
            + pending_cells(state.pending) + fired_cells(state.fired))


# ---- the pending set and the fired ledger -----------------------------------

def _group_of(table, iid):
    """`(shape, entry)` for `iid` in a shape-grouped tier, or `(None, None)`."""
    for shape, group in table.items():
        entry = group.get(iid)
        if entry is not None:
            return shape, entry
    return None, None


def _known(state, iid):
    """Is this `iid` already an intention — pending or fired?

    Read on the **write** path, which is what stops the fired ledger from being
    decorative: `§5 L5` names no re-arming, so an `iid` that has fired is done
    and a later payload carrying it arms nothing.
    """
    for table in (state.pending, state.fired):
        for group in table.values():
            if iid in group:
                return True
    return False


def _fire_form(fire):
    """`(shape, values)` for a fire payload under the Layer-4 row codec."""
    shape = row_shape(fire)
    if shape is None:
        return None, (copy_value(fire),)
    return shape, row_values(fire, shape)


def _fire_payload(shape, values):
    if shape is None:
        return copy_value(values[0])
    return row_payload(shape, values)


def _arm_cells(state, iid, cond, shape, values):
    """The cells arming this intention costs. Never optional: it is the layer."""
    cost = 1 + 1 + payload_cost(cond) + _values_cells(shape, values)
    if shape not in state.pending:
        cost += _shape_cells(shape)
    return cost


def _arm(state, iid, t0, cond, shape, values):
    """Add one pending entry; return `(state', cells spent)`."""
    spent = _arm_cells(state, iid, cond, shape, values)
    group = state.pending.get(shape)
    group = {} if group is None else dict(group)
    group[iid] = (t0, copy_value(cond)) + values
    pending = dict(state.pending)
    pending[shape] = group
    return replace(state, pending=pending), spent


def _unpend(state, iid):
    """Remove one pending entry; return `(state', freed, t0, cond, shape, values)`."""
    shape, entry = _group_of(state.pending, iid)
    if entry is None:
        return state, 0, None, None, None, None
    t0, cond = entry[0], entry[1]
    values = entry[2:]
    freed = 1 + 1 + payload_cost(cond) + _values_cells(shape, values)
    group = dict(state.pending[shape])
    del group[iid]
    pending = dict(state.pending)
    if group:
        pending[shape] = group
    else:
        del pending[shape]
        freed += _shape_cells(shape)
    return (replace(state, pending=pending, occupancy=state.occupancy - freed),
            freed, t0, cond, shape, values)


def _ledger_cells(state, shape, values):
    cost = 1 + 1 + _values_cells(shape, values)
    if shape not in state.fired:
        cost += _shape_cells(shape)
    return cost


def _ledger(state, iid, t, shape, values):
    """Write one firing into the fired ledger; return `(state', cells spent)`."""
    spent = _ledger_cells(state, shape, values)
    group = state.fired.get(shape)
    group = {} if group is None else dict(group)
    group[iid] = (t,) + values
    fired = dict(state.fired)
    fired[shape] = group
    return replace(state, fired=fired), spent


def _emitted_at(state, t):
    """The fired payload the engine emitted at `t`, regenerated, or `None`."""
    for shape, group in state.fired.items():
        for entry in group.values():
            if entry[0] == t:
                return _fire_payload(shape, entry[1:])
    return None


def _armed_at(state, t):
    """The `intend` payload of a still-pending intention written at `t`, or `None`.

    An armed intention's episode is released at the door, because the pending
    entry regenerates it exactly — Layer 4's demotion, one layer up. The moment
    it fires the entry is gone, this regeneration stops, and the loss is booked.
    """
    for shape, group in state.pending.items():
        for iid, entry in group.items():
            if entry[0] == t:
                return rebuild_intention(iid, copy_value(entry[1]),
                                         _fire_payload(shape, entry[2:]))
    return None


# ---- making room ------------------------------------------------------------

def _make_room(state, need, now, arriving=None):
    """Evict until `need` cells fit, most-lossless first, or give up.

    The Layer-4 eviction ladder, unchanged and inherited: demotion (lossless),
    then forgetting under the Layer-3 importance law (recorded), then shedding
    whole supersession chains (recorded, and the entity is marked damaged). What
    Layer 5 adds is only what it does **not** touch — the pending set and the
    fired ledger are outside every phase, because `miss = 0` and `dup-fire = 0`
    are identities and an engine that could evict either could be made to break
    the gate by being poor.
    """
    if state.occupancy + need <= state.budget_cap:
        return state
    state = l4._demote_until(state, need)
    if state.occupancy + need <= state.budget_cap:
        return state
    state, _keep = l4._forget_until(state, need, now, arriving)
    if state.occupancy + need <= state.budget_cap:
        return state
    return l4._shed_until(state, need, now)


def _book_loss(state, t, weight):
    """Record one genuine loss in the inherited aggregated forgetting record."""
    record, given = l4._forget(state.forgetting, t, weight)
    return replace(state, forgetting=record, occupancy=state.occupancy + given)


def _loss_reserve(state):
    """The growth the aggregated record has left, reserved on any path that loses.

    `README-l4 §2.3`'s record is bounded forever by coarsening at
    `3 + 2 * FORGET_BUCKETS` cells, so a reserve is exactly the distance from
    where it is to where it can never pass — by up to a full coarsening step the
    first time, and by nothing at all once it is full. Reserving it is what stops
    the act of *recording* a loss from breaching the very cap it is a consequence
    of, and R5 clause 4 is why it is priced here rather than assumed away.
    """
    return 3 + 2 * FORGET_BUCKETS - l4.forget_cost(state.forgetting)


# ---- arming: the Layer-5 write path -----------------------------------------

def _write_intention(state, payload, armed, t):
    """Arm one intention; release its episode as a demotion. `(state', t)` or refusal.

    The episode is **not stored**, and that is a derivation and not a saving: the
    pending entry carries `(t0, cond, fire)` and `arms` has already proved the
    payload rebuilds from them byte-for-byte, so the episode is a redundant copy
    of something the state already holds — `README-l4 §0.2`'s demotion, with the
    pending set as the derived view. `read(t0)` answers it in full for as long as
    the intention is pending.
    """
    iid, cond, fire = armed
    cap = state.budget_cap
    shape, values = _fire_form(fire)

    schema_room = l4._schema_delta(state, payload, None, worst=True)
    arm_room = _arm_cells(state, iid, cond, shape, values)
    need = schema_room + arm_room
    if need > cap:
        return state, None                # no eviction could ever make room

    working = _make_room(state, need, t)
    if working.occupancy + need > cap:
        return state, None                # a deterministic refusal (§4.1.2)

    out, spent = l4._apply_schema(working, payload, None, t, None)
    out, armed_cells = _arm(out, iid, t, cond, shape, values)
    spent += armed_cells
    return replace(out, occupancy=working.occupancy + spent, next_t=t + 1,
                   last_cost=spent, demotions=out.demotions + 1), t


# ---- firing -----------------------------------------------------------------

def _eligible(state, payload, t_event):
    """The `iid`s an arriving event satisfies, in `iid` ascending order.

    Eligibility is *written strictly earlier*: an intention is never tested
    against the event that created it (`grammar.md`: *"an intention becomes
    eligible at `k0 + 1`"*), stated over logical time so that it reads the same
    under either cascade reading. The order is `iid` ascending — a **declared**
    total order, which is what §2.3 needs so determinism does not rest on an
    engine's scan order.
    """
    ready = []
    counts = state.counts
    for group in state.pending.values():
        for iid, entry in group.items():
            if entry[0] >= t_event:
                continue
            if satisfies(entry[1], payload, counts):
                ready.append(iid)
    ready.sort()
    return ready


def _fire_one(state, iid):
    """Fire one intention at `state.next_t`. `None` if the budget cannot house it.

    Three ledgers move in one transition, and the second is the one with teeth:

      * the intention leaves the pending set and enters the fired ledger — the
        swap frees the condition's cells, so a firing is cell-negative in all but
        the shape header;
      * the intention's own episode, released at arming as a demotion because the
        pending entry regenerated it, **stops being regenerable in this instant**.
        Where the budget already has room the episode is taken back as an
        ordinary irreducible one, so nothing is lost at a generous cap; where it
        does not, the demotion has become a loss and is **booked** into the
        forgetting record while the demotion counter gives it back. That is
        `README-l4 §4`'s invariant — *the demotion invariant is invertibility* —
        carried to promises, and it is why
        `forgotten == exactly the `t` `read` abstains on` survives this layer;
      * the fired event is folded like any other event and its own episode is
        released into the fired ledger, which regenerates it — a demotion.
    """
    cap = state.budget_cap
    working, _freed, t0, cond, shape, values = _unpend(state, iid)
    if t0 is None:
        return None
    fire = _fire_payload(shape, values)
    t = working.next_t

    fact = facet(fire)
    kind_after = atlas_after(working.atlas, fire, fact)
    if fact is not None and kind_after is None \
            and working.atlas.get(fact[1]) is not None:
        working = l4._reconcile_lost_key(working, fact[1])

    schema_room = l4._schema_delta(working, fire, fact, worst=True)
    ledger_room = _ledger_cells(working, shape, values)
    need = schema_room + ledger_room + _loss_reserve(working)
    if need > cap:
        return None
    working = _make_room(working, need, t)
    if working.occupancy + need > cap:
        return None

    out, spent = l4._apply_schema(working, fire, fact, t, kind_after)
    out, ledger_cells = _ledger(out, iid, t, shape, values)
    spent += ledger_cells
    out = replace(out, occupancy=working.occupancy + spent, next_t=t + 1,
                  last_cost=spent, demotions=out.demotions + 1)

    # The promise's own episode. It was released at arming as a demotion because
    # the pending entry regenerated it; the pending entry has just gone, so that
    # booking is false from this instant. The episode is offered back to the
    # store where the budget ALREADY has room — it is content the engine once
    # released, not arriving fuel, so taking it back by evicting something else
    # would be an eviction motivated by bookkeeping rather than by the
    # importance law. Where there is no room the demotion becomes a **recorded
    # loss**, which is `README-l4 §4`'s invariant carried to promises.
    promise = rebuild_intention(iid, cond, fire)
    cost = l4._record_delta(out, promise, demotable=False)["cost"]
    if out.occupancy + cost <= cap:
        out, extra = l4._apply_record(out, promise, t0, demotable=False)
        out = replace(out, occupancy=out.occupancy + extra,
                      demotions=out.demotions - 1)
    else:
        out = _book_loss(out, t0, grammar_weight(promise))
        out = replace(out, demotions=out.demotions - 1)
    return out, fire, t


def _run_triggers(state, payload, t):
    """Evaluate, fire, and evaluate what fired — in `t` order. `None` on refusal.

    The work list is FIFO, which under the `t` semantics of `R6` clause 2 *is*
    `t` order: the firings a write causes take the next consecutive times, and a
    firing's own consequences take the times after those. Cascades are the plain
    uniform reading and are unreachable on `corpora/l5stream` by construction, so
    the loop below runs its inner pass 20 000 times and finds nothing — which is
    the point: no exception is written anywhere for the case the corpus cannot
    exhibit.

    Termination is structural rather than bounded by a limit this layer invents:
    every firing removes one intention from the pending set and nothing ever puts
    one back, so a transition emits at most `|pending|` events.
    """
    queue = [(payload, t)]
    head = 0
    while head < len(queue):
        event, when = queue[head]
        head += 1
        for iid in _eligible(state, event, when):
            fired = _fire_one(state, iid)
            if fired is None:
                return None
            state, emitted, t_fire = fired
            queue.append((emitted, t_fire))
    return state


# ---- the write --------------------------------------------------------------

def write(state, payload):
    """Ingest one event, then fire what it satisfies. `(state', caller t)`.

    Below Layer 5 this is the frozen Layer-4 write, unchanged — the capped engine
    IS the consolidation engine (§7.4). At Layer 5 the order is: the caller's
    event first and at its own `t`, then the firings it caused, each at the next
    consecutive `t`, in `iid` order, all inside one pure transition (§2.1) and
    never exceeding the cap at any observable instant (§4.1).

    `ingest` returns the **caller** event's `t` (`R6` clause 2); `next_t` advances
    by `1 + f`. A refusal is total: `t` is unspent and the state is exactly as it
    was found (§4.1.2) — including where the caller's own event fitted and a
    firing it caused did not, because an event that never happened cannot have
    satisfied anything.
    """
    check_canonical(payload)
    if not isinstance(state, L5State):
        return l4.write(state, payload)

    t = state.next_t
    armed = arms(payload)
    if armed is not None and _known(state, armed[0]):
        armed = None                  # `§5 L5` names no re-arming; the first wins
    if armed is None:
        out, got = l4.write(state, payload)
    else:
        out, got = _write_intention(state, payload, armed, t)
    if got is None:
        return state, None

    out = _run_triggers(out, payload, t)
    if out is None:
        return state, None
    return out, t


# ---- reading ----------------------------------------------------------------

def read(state, t):
    """The event at `t`: retained, emitted, still-pending, regenerated, or gone.

    Four tiers, disjoint by construction and searched cheapest-first. The two new
    ones are Layer 5's: an event the engine **emitted** is regenerated from the
    fired ledger, and an `intend` event whose intention is still **pending** is
    regenerated from the pending entry. Both are exact — the ledger and the
    pending set store the payload's own atoms under the Layer-4 row codec — so
    `reconstruction wrong = 0` stays structural at this layer too.
    """
    if not isinstance(state, L5State):
        return l4.read(state, t)
    if not isinstance(t, int) or isinstance(t, bool):
        return None
    if t < 0 or t >= state.next_t:
        return None
    payload = l4._row_at(state, t)
    if payload is None:
        payload = _emitted_at(state, t)
    if payload is None:
        payload = _armed_at(state, t)
    if payload is not None:
        return {"payload": payload, "t": t}
    return l4.read(state, t)              # the Layer-4 chain sweep, or nothing


def read_range(state, t0, t1):
    """Every event in `[t0, t1]` the engine can still produce, `t` ascending."""
    if not isinstance(state, L5State):
        return l4.read_range(state, t0, t1)
    if not isinstance(t0, int) or isinstance(t0, bool):
        return []
    if not isinstance(t1, int) or isinstance(t1, bool):
        return []
    out = []
    t = max(0, t0)
    hi = min(t1, state.next_t - 1)
    while t <= hi:
        event = read(state, t)
        if event is not None:
            out.append(event)
        t += 1
    return out


def fired_by(state, iid):
    """The event records intention `iid` fired, `t` ascending, or `None`.

    A **list**, and never a bare record: `dup-fire = 0` is a gate clause, so an
    intention that fired twice has to be visible through the query interface
    rather than only in an engine's own bookkeeping (`STAGE-B.md §2`). This engine
    cannot produce a two-element list — the ledger is keyed by `iid` and firing
    removes the intention from the pending set — and the list is what makes that
    a **measurement** rather than a promise.
    """
    if not isinstance(state, L5State):
        return None
    if not isinstance(iid, int) or isinstance(iid, bool):
        return None
    shape, entry = _group_of(state.fired, iid)
    if entry is None:
        return None
    return [{"payload": _fire_payload(shape, entry[1:]), "t": entry[0]}]


def pending_iids(state):
    """Every intention still waiting, `iid` ascending (a diagnostic, not a gate)."""
    out = []
    for group in state.pending.values():
        out.extend(group)
    out.sort()
    return out


def fired_iids(state):
    out = []
    for group in state.fired.values():
        out.extend(group)
    out.sort()
    return out


# ---- the Answer (§7.2) & the generic query binding --------------------------

def _answer(value, confidence, provenance):
    return {"status": "answer", "value": value,
            "confidence": confidence, "provenance": provenance}


def _abstain(confidence=0, provenance=None):
    return {"status": "abstain", "value": None,
            "confidence": confidence, "provenance": provenance}


def query(state, q):
    """Answer a query (§7.2). Unsupported / un-capable queries abstain, never raise."""
    if not isinstance(state, L5State):
        return l4.query(state, q)
    if not isinstance(q, dict):
        return _abstain()
    op = q.get("op")

    if op == "fired":
        records = fired_by(state, q.get("iid"))
        if records is None:
            return _abstain()
        t_fire = records[0]["t"]
        return _answer(records, 1000,
                       {"support": [t_fire], "kind": "derive",
                        "t_asof": t_fire})

    if op == "read":
        event = read(state, q.get("t"))
        if event is None:
            return _abstain()
        held = l4._row_at(state, event["t"]) is not None
        return _answer(event, 1000,
                       {"support": [event["t"]],
                        "kind": "recall" if held else "derive",
                        "t_asof": event["t"]})

    if op == "read_range":
        events = read_range(state, q.get("t0"), q.get("t1"))
        if events:
            support = [e["t"] for e in events]
            return _answer(events, 1000,
                           {"support": support, "kind": "aggregate",
                            "t_asof": support[-1]})
        return _answer(events, 1000, None)

    if op == "prospection":
        return _answer({"pending": len(pending_iids(state)),
                        "fired": len(fired_iids(state)),
                        "pending_cells": pending_cells(state.pending),
                        "fired_cells": fired_cells(state.fired)}, 1000, None)

    return l4.query(state, q)            # Layers 1–4, unchanged (§7.3 below them)


# ---- snapshot / restore -----------------------------------------------------
#
# Every branch is a LIST of lists rather than an object, for the reason
# `l4_consolidation` states: canonical JSON keys must be strings (§2.4), and
# `payload_cost` charges one cell per key, so the list form makes the serialized
# atom count *equal* the engine's own accounting rather than merely close to it.
# That equality is what the rule-P audit checks from outside the engine
# (R4 clause 3).

def _pending_body(pending):
    return [[shape[0] if shape else None,
             list(shape[1]) if shape else [],
             [[iid, entry[0], copy_value(entry[1])] + list(entry[2:])
              for iid, entry in group.items()]]
            for shape, group in pending.items()]


def _fired_body(fired):
    return [[shape[0] if shape else None,
             list(shape[1]) if shape else [],
             [[iid] + list(entry) for iid, entry in group.items()]]
            for shape, group in fired.items()]


def _body(state):
    """The canonical, deterministic dict form of the full state (§2.4)."""
    body = l4._body(state)
    body["pending"] = _pending_body(state.pending)
    body["fired"] = _fired_body(state.fired)
    return body


def state_checksum(state):
    """SHA-256 hex over the canonical encoding of the full state body (§2.4)."""
    if not isinstance(state, L5State):
        return l4.state_checksum(state)
    return hashlib.sha256(encode(_body(state))).hexdigest()


def snapshot(state):
    """Canonical, checksummed serialization of the state (§7.1, §2.4)."""
    if not isinstance(state, L5State):
        return l4.snapshot(state)
    body = _body(state)
    checksum = hashlib.sha256(encode(body)).hexdigest()
    return encode({"magic": MAGIC, "checksum": checksum, "body": body})


def _shape_from_body(kind, fields, what):
    if kind is None:
        if fields:
            raise CorruptSnapshot("snapshot %s verbatim shape carries fields"
                                  % (what,))
        return None
    if not isinstance(kind, str) or not isinstance(fields, list):
        raise CorruptSnapshot("snapshot %s shape is malformed" % (what,))
    return (kind, tuple(fields))


def _pending_from_body(raw):
    out = {}
    for entry in raw:
        if not isinstance(entry, list) or len(entry) != 3:
            raise CorruptSnapshot("snapshot pending entry is malformed")
        shape = _shape_from_body(entry[0], entry[1], "pending")
        width = 1 if shape is None else len(shape[1])
        group = {}
        for row in entry[2]:
            if not isinstance(row, list) or len(row) != 3 + width:
                raise CorruptSnapshot("snapshot pending row width is wrong")
            group[row[0]] = (row[1], row[2]) + tuple(row[3:])
        out[shape] = group
    return out


def _fired_from_body(raw):
    out = {}
    for entry in raw:
        if not isinstance(entry, list) or len(entry) != 3:
            raise CorruptSnapshot("snapshot fired entry is malformed")
        shape = _shape_from_body(entry[0], entry[1], "fired")
        width = 1 if shape is None else len(shape[1])
        group = {}
        for row in entry[2]:
            if not isinstance(row, list) or len(row) != 2 + width:
                raise CorruptSnapshot("snapshot fired row width is wrong")
            group[row[0]] = (row[1],) + tuple(row[2:])
        out[shape] = group
    return out


def restore(data):
    """Rebuild a state from snapshot bytes; fail loudly on any corruption.

    A Layer-4 (or lower) snapshot restores through the frozen path below, so a
    capped engine's state round-trips exactly as it always did. Five guards on
    the Layer-5 form: the envelope and its SHA-256; the shape of every branch;
    the handle index rederived from the retained episodes; the recomputed
    occupancy, which is the check that the incremental accounting never drifted;
    and — new here — that **no `iid` is both pending and fired**, which is the
    exactly-once invariant asserted of the bytes rather than of the write path.
    """
    try:
        envelope = decode(data)
    except Exception as exc:                       # invalid JSON / UTF-8 / float
        raise CorruptSnapshot("snapshot is not decodable: %r" % (exc,))
    if not isinstance(envelope, dict) or frozenset(envelope.keys()) != _ENVELOPE_KEYS:
        raise CorruptSnapshot("snapshot envelope keys are wrong")
    if envelope["magic"] != MAGIC:
        return l4.restore(data)

    body = envelope["body"]
    if not isinstance(body, dict) or frozenset(body.keys()) != _BODY_KEYS:
        raise CorruptSnapshot("snapshot body keys are wrong")
    if hashlib.sha256(encode(body)).hexdigest() != envelope["checksum"]:
        raise CorruptSnapshot("snapshot checksum mismatch (corruption detected)")

    pending = _pending_from_body(body["pending"])
    fired = _fired_from_body(body["fired"])

    # The Layer-4 half is rebuilt by the frozen Layer-4 reader, so there is one
    # implementation of that parse and not two. Its occupancy guard is the whole
    # state's, so the sub-snapshot carries the Layer-4 share of the count and
    # this function checks the total against `accounted_occupancy` below.
    inner = dict(body)
    del inner["pending"]
    del inner["fired"]
    inner["occupancy"] = (body["occupancy"] - pending_cells(pending)
                          - fired_cells(fired))
    base = l4.restore(encode({
        "magic": l4.MAGIC,
        "checksum": hashlib.sha256(encode(inner)).hexdigest(),
        "body": inner}))

    state = L5State(layer_cap=base.layer_cap, budget_cap=base.budget_cap,
                    occupancy=body["occupancy"], next_t=base.next_t,
                    last_cost=0, chains=base.chains, atlas=base.atlas,
                    irreducible=base.irreducible, counts=base.counts,
                    damaged=base.damaged, demotable=base.demotable,
                    kept=base.kept, verbatim=base.verbatim, index=base.index,
                    demotions=base.demotions, forgetting=base.forgetting,
                    pending=pending, fired=fired)

    both = set(pending_iids(state)) & set(fired_iids(state))
    if both:
        raise CorruptSnapshot(
            "snapshot has %d intentions both pending and fired (%s) — "
            "exactly-once is the layer, and a state that claims both could "
            "fire one twice" % (len(both), sorted(both)[:8]))
    if accounted_occupancy(state) != body["occupancy"]:
        raise CorruptSnapshot("snapshot occupancy diverges from the accounted cost")
    return state


# ---- the generic engine interface (§7, INTERFACE.md) ------------------------

def empty():
    """A fresh, full Layer-5 engine state (adapter contract, §7)."""
    return new_state(layer_cap=LAYER, budget_cap=DEFAULT_BUDGET)


def make_engine(layer_cap, budget_cap=DEFAULT_BUDGET):
    """A fresh state capped at `layer_cap` (§7.4). 4 = the frozen consolidation engine."""
    return new_state(layer_cap=layer_cap, budget_cap=budget_cap)


def ingest(state, payload):
    """Append one event and fire what it satisfies; return `(state', caller t)`."""
    return write(state, payload)


def last_cost(state):
    """Integer work-unit cost of the most recent successful write (§3.3, §4.1)."""
    return state.last_cost


# The Layer-1/2/3/4 verbs, carried forward on this module's surface so an
# adapter binds one engine rather than several. `read` and `read_range` are
# Layer 5's own (they reach the two new tiers); the rest are the frozen
# Layer-4 functions, unchanged and re-exported rather than re-implemented.
recall = l4.recall
retained = l4.retained
current = l4.current
asof = l4.asof
profile = l4.profile
covers_from = l4.covers_from
chain_cells = l4.chain_cells
irreducible_cells = l4.irreducible_cells
rows_cells = l4.rows_cells
index_cells = l4.index_cells

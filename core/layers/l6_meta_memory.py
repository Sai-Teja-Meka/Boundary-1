"""core/layers/l6_meta_memory.py — Layer 6: Meta-memory (confidence, from evidence).

Layers 1–5 answer. Layer 6 is the first capability that says **how sure it is**,
and it says it in the one currency `§7.2` declares: an integer permille, derived
from structural evidence the engine already holds, never from a float and never
from an answer key.

Pure, integer-only (§2), built entirely on the frozen Layer-1/2/3/4/5 primitives;
it edits none of them (§9). Below `layer_cap = 6` the state IS the frozen Layer-5
state and every verb delegates to it, so `make_engine(5)` is not an imitation of
the prospection engine — it is the prospection engine (§7.4).

The full design record is `core/layers/README-l6.md`. This docstring states what
the code does; that document states why the engine is wrong exactly 100 times on
the artifact `BOUNDARY-RULINGS.md R7` clause 1 binds, and why being wrong there is
the layer rather than a defect.

## The one sentence the constitution gives this layer's state

`§5.1 L6`, defending `B = 1000`:

> *Meta-memory derives confidence **from existing state** within budget.*

That is taken literally, and it decides the shape of this file. **There is no new
state at Layer 6.** `L6State` adds no field to the frozen `L5State`; `_body` is
`l5._body` unchanged, so the canonical state of a Layer-6 engine over any stream
is **byte-identical to the Layer-5 engine's over the same stream in every branch
but one — the recorded `layer_cap`, which is the cap and not the content**.
`anchors/l6.json` pins that as an identity rather than asserting it in prose.
What changed is not what the engine holds. It is what the engine says about it.

`ATTAINABILITY-B.md §3.2` priced the marginal state at **18 cells** — one
set-once flag per attribute key on battery-b's 18-key vocabulary, *"priced as
state because that is where it would live"*. It lives one step earlier than that:
the set-once reading is a **declared reading of the frozen grammars**, exactly as
`ASSERTION_FORMS` is at Layer 4 and `INTENTION_FORM` at Layer 5, and the tie
itself is read off the interval table the Layer-4 engine already carries. So the
engine spends **0**, the 18 were a ceiling and not a bill, and the divergence is
recorded rather than edited away (`R6` clause 3; `README-l6.md §0`).

## The evidence, and what it is a function of

Two features, and both are folds over `state.chains` — the interval table:

| feature | read from | what it means |
|---|---|---|
| `set_once` | `SET_ONCE_KEYS`, a declared reading | this key admits exactly ONE true value over an entity's whole history |
| `n_distinct` | the `(entity, key)` chain visible to the query | how many mutually exclusive values that chain actually asserts |
| `damaged` | Layer-4 state, unchanged | the budget shed one of this entity's chains, so its history is **incomplete** and one claimant is provably unrecoverable |

`§5 L6` asks for *"confidence permille from structural evidence"* — a
**confidence model, not a second reader** — so the answer path is the frozen
Layer-4 one, unchanged, byte for byte: `current` is still the value at a chain's
greatest `t` and `asof` still the value in force at the asked `t`. Layer 6 does
not answer differently. It answers with a number attached.

## The tie rate, derived and not chosen

Where a **set-once** key's visible chain carries `d > 1` distinct values, the
chain holds `d` mutually exclusive claimants for a slot that admits one, the
engine's reading picks one of them, and the confidence it states is

```
confidence = permille(1 / d)          exact Fraction in, integer permille out
```

At `d = 2` that is **500**, which is the tie's own arithmetic and is what
`ATTAINABILITY-B.md §3.1`'s exhibited witness prices `corpora/l6batteryb`'s
forcing region at — *derived*, `permille(1/2)`, and not typed. Everywhere else
the engine states **1000**, because everywhere else its answer is one it has
proved: `README-l5 §4` records that the evidence the layer below keeps is binary,
and that is still true — what Layer 6 adds is the one place where it is not.

**The model is provably non-resolving** (`R7` clause 3(b), Theorem 2). It reads
the chain's *shape* and never the raw entity id or an absolute `t`, so on a
mirror pair it computes the identical confidence for both members and commits to
the identical reading — which is exactly why it is wrong on one of them. An
engine that could resolve a pair would have read a coin that is not in the
stream, and `ascension/l6/t_meta_memory.py` fails it for being too good.

## What this layer does NOT do, and could not

It manufactures no errors. On every clean chain the engine answers as the Layer-5
engine answered — asserted query by query in `trials/strain/l6/` — so the
`AUROC` denominator is fed by `R7` clause 3(b)'s theorem and never by sandbagging.
It hedges nothing: `§3.0` pays 100 for an abstention and `§3.4` cannot see one, so
an engine that bought a clean denominator by declining to use it would be
following the incentive `R7` clause 7 records; `§5 L6`'s own `F ≥ 950` prices that
escape at 900 per hedge out of 50 permille, and the engine takes none of it.

Calibration binds from here and stays bound above it (§3.4). Provenance is still
dormant (§4.2) and binds at Layer 7; `README-l6.md §4` states that seam.
"""

import hashlib
from dataclasses import dataclass
from fractions import Fraction

from core.serialize import encode, decode
from core.layers import l5_prospection as l5
from core.layers import l4_consolidation as l4
from core.layers.l5_prospection import (
    L5State, CorruptSnapshot,
    intention, rebuild_intention, arms, readable, satisfies,
    INTENTION_KIND, INTENTION_FORM, PREDICATES, CONNECTIVES,
    pending_cells, fired_cells, fired_by, pending_iids, fired_iids,
)
from core.layers.l4_consolidation import (
    L4State, facet, rebuild, invertible, atlas_after,
    row_shape, row_values, row_payload, ASSERTION_FORMS,
)

LAYER = 6

# A generous default cap, matching the Layer-1..5 defaults so cross-layer
# reasoning stays simple. Integer only (§2.2). `§5 L6` states no footprint
# clause, so the Layer-6 batteries score in budget at exactly this number.
DEFAULT_BUDGET = 1_000_000_000

MAGIC = "boundary1-l6-snapshot"
_ENVELOPE_KEYS = frozenset({"magic", "checksum", "body"})


# ---- the declared set-once reading ------------------------------------------
#
# A reading of the frozen grammars and NOT a learner, in the shape this project
# has used at every layer: `HANDLE_FIELDS` (L3), `ASSERTION_FORMS` (L4),
# `INTENTION_FORM` and `PREDICATES` (L5). `origin` is `corpora/murk`'s set-once
# attribute by that generator's own frozen text — *"re-assert an entity's
# set-once attribute `origin` with a DIFFERENT value (a genuine contradiction,
# not a legal update)"* — and it is `corpora/l6batteryb`'s forcing key, asserted
# there by nothing but the region.
#
# It is a READING because it cannot be anything else, and saying so is half the
# honesty of this layer: nothing in a stream distinguishes a set-once key from an
# ordinary one that happens to have been updated. A chain that disagrees with
# itself is a contradiction only if the key admits one value, and which keys
# those are is a fact about the grammar, not about the bytes. An engine that
# guessed would be pricing legal updates as contradictions — which is exactly
# what the KEY-BLIND `conflict-rank` policy does, and what costs it 65 permille
# of AUROC margin (`ATTAINABILITY-B.md §4.3`).
#
# `trials/ops/l6/t_l6_composition.py` asserts this reading and the battery's own
# (`_l6btasks.SET_ONCE_KEYS`) agree — one reading, two implementations, checked
# rather than assumed, exactly as `ops/l4` and `ops/l5` do for their facets.

SET_ONCE_KEYS = ("origin",)


# ---- §3.5's permille, in core ------------------------------------------------

def permille(x):
    """Exact `Fraction` in [0,1] -> integer permille, round-half-to-even (§3.5).

    No float ever appears (§2.2). This is `§3.5`'s own procedure, and
    `ops/l6/t_l6_composition.py` asserts it agrees with `trials/_l6tasks.permille`
    — the instrument every score in this project is rendered by — and with
    `l2_recall`'s copy, on a declared grid that includes both half-way cases.
    """
    n = x * 1000
    q = n.numerator // n.denominator
    r = n - q
    if r < Fraction(1, 2):
        return q
    if r > Fraction(1, 2):
        return q + 1
    return q if q % 2 == 0 else q + 1


CERTAIN = 1000        # the confidence of an answer the engine has proved
NO_ANSWER = 0         # the confidence of an abstention (§7.2's `value: null` row)


# ---- the state ---------------------------------------------------------------

@dataclass(frozen=True)
class L6State(L5State):
    """The frozen Layer-6 engine state (§2.1) — Layer 5's, with no field added.

    A **subclass** of the frozen `L5State` carrying no data of its own, which is
    `§5.1 L6`'s *"derives confidence from existing state"* made structural: every
    Layer-1..5 verb, cost function and eviction phase operates on this state
    unchanged, `replace()` returns an `L6State`, and `_body` is `l5._body`, so a
    Layer-6 state and the Layer-5 state built from the same stream are **byte
    identical**.

    The subclass exists to carry the layer, not to carry a field: `query`
    dispatches on it, and `new_state(layer_cap < 6)` returns the frozen Layer-5
    state so `make_engine(5)` is the prospection engine itself (§7.4).
    """


def new_state(layer_cap, budget_cap):
    """A fresh state capped at `layer_cap` with integer budget cap `budget_cap`.

    Below Layer 6 this returns the **frozen Layer-5 state** (§7.4), which below
    Layer 5 is the frozen Layer-4 state, and so down. Capping is a
    construction-time restriction, and the honest way to build an engine with no
    confidence model is to build the engine that does not have one — which is
    what `humility/l6` measures at `AUROC = 500` exactly.
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
        return l5.new_state(layer_cap=layer_cap, budget_cap=budget_cap)
    base = l5.new_state(layer_cap=LAYER, budget_cap=budget_cap)
    return L6State(layer_cap=layer_cap, budget_cap=budget_cap,
                   occupancy=base.occupancy, next_t=0, last_cost=0,
                   chains={}, atlas={}, irreducible={}, counts={}, damaged=(),
                   demotable={}, kept={}, verbatim={}, index={}, demotions=0,
                   forgetting=base.forgetting, pending={}, fired={})


def accounted_occupancy(state):
    """Recompute occupancy from the state alone — Layer 5's, unchanged.

    There is nothing to add. That is the claim, and `ops/l6/t_l6_composition.py`
    asserts it against the engine's own snapshot rather than trusting it.
    """
    return l5.accounted_occupancy(state)


# ---- the evidence: two folds over the interval table -------------------------

def visible_chain(state, entity, key, horizon=None):
    """The `(t, value)` steps of one chain the query can see, `t` ascending.

    `horizon` is the `as-of` time, or `None` for `current`. This is the same
    prefix the battery's declared evidence extractor takes
    (`_l6btasks.evidence`), and it is taken for the same reason: evidence that a
    later assertion exists is evidence the answer at `t` does not have.
    """
    per = state.chains.get(key)
    if per is None:
        return ()
    chain = per.get(entity)
    if not chain:
        return ()
    if horizon is None:
        return tuple(chain.items())
    return tuple((stamp, value) for stamp, value in chain.items()
                 if stamp <= horizon)


def n_distinct(steps):
    """How many mutually exclusive values a chain asserts, by CANONICAL BYTES.

    §2.4 and not Python equality, for the reason `README-l4 §1` gives: `True == 1`
    in Python and `true != 1` here, so a chain asserting `1` and then `true` has
    said two different things and an engine that called them one would be
    understating a contradiction.
    """
    return len({encode(value) for _t, value in steps})


def set_once(key):
    """Does the declared reading say this key admits exactly one true value?"""
    return key in SET_ONCE_KEYS


def claimants(state, entity, key, horizon=None):
    """How many values could be the true one for a **set-once** `(entity, key)`.

    The visible chain's distinct count, plus one where the engine **knows its own
    history of that entity is incomplete**. `damaged` is Layer-4 state and already
    means exactly that: `_shed_until` drops a whole `(key, entity)` chain under
    pressure and marks the entity, *"so its action-count profile abstains forever
    after"*. Layer 6 reads the same flag for a reason Layer 4 did not need — a
    shed set-once chain can be **re-asserted afterwards**, leaving one visible
    claimant where the true one may be among those the forgetting record booked,
    and an engine that counted only what it could see would state `1000` on a
    coin flip. `README-l6 §4` records the measurement that found it.

    `+1` and not more, because that is exactly what the state supports: at least
    one claimant is provably unrecoverable, and how many more is a question the
    aggregated per-`t`-range forgetting record cannot answer (`humility/l4/
    IMPOSSIBILITY.md §3`'s pigeonhole). So the number is an **upper bound on the
    engine's own correctness**, derived from the state and never assumed.
    """
    d = n_distinct(visible_chain(state, entity, key, horizon))
    if d and entity in state.damaged:
        return d + 1
    return d


def confidence_for(state, entity, key, horizon=None):
    """The integer permille this engine states for an answer on `(entity, key)`.

    The whole confidence model, and it is short because `§5.1 L6` says the state
    is the existing one:

      * a key the declared reading calls **set-once** with `d > 1` claimants
        holds `d` mutually exclusive values for a slot that admits one; the
        engine's reading commits to one of them, so the chance that the one it
        committed to is the true one is `1/d` and the confidence it states is
        `permille(1/d)` — **500 at `d = 2`**, the tie's own arithmetic;
      * everything else is `CERTAIN`, because everything else is an answer the
        engine has proved: a chain that admits updates answers with its latest,
        and its latest is what is in force **however much of the chain before it
        the budget took** — which is why `damaged` moves a set-once key's number
        and moves nothing else.

    It reads the chain's SHAPE and never the raw entity id or an absolute `t`, so
    on two observationally identical chains it returns the identical number. That
    is not an accident of this implementation; it is `R7` clause 3(b)'s class-E
    boundary, and `strain/l6` asserts it of the frozen mirror pairs.
    """
    if not set_once(key):
        return CERTAIN
    d = claimants(state, entity, key, horizon)
    if d <= 1:
        return CERTAIN
    return permille(Fraction(1, d))


def ties(state):
    """Every `(entity, key)` chain the engine currently reads as a tie, sorted.

    A diagnostic over the engine's own state, surfaced through `§7.1`'s `query`
    by the `calibration` op below so that a trial can read the model the way a
    caller would rather than by reaching into the state.
    """
    out = []
    for key in SET_ONCE_KEYS:
        per = state.chains.get(key)
        if per is None:
            continue
        for entity, chain in per.items():
            d = n_distinct(tuple(chain.items()))
            if d > 1:
                out.append((entity, key, d))
    out.sort()
    return tuple(out)


# ---- the write path: Layer 5's, unchanged ------------------------------------

def write(state, payload):
    """Ingest one event. The frozen Layer-5 write, unchanged (§9.2).

    Layer 6 adds no state, so it adds nothing to the write path: no cell is
    spent, no eviction order moves, no promise is displaced. That is what makes
    `inheritance/l6`'s Layer-5 row pass rather than merely likely to — a
    confidence model that had to be paid for would compete with a pending set and
    a fired ledger that `README-l5 §0.1` puts outside every eviction phase on
    purpose.
    """
    return l5.write(state, payload)


read = l5.read
read_range = l5.read_range
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


# ---- the Answer (§7.2) & the generic query binding ---------------------------

def _answer(value, confidence, provenance):
    return {"status": "answer", "value": value,
            "confidence": confidence, "provenance": provenance}


def _abstain(confidence=NO_ANSWER, provenance=None):
    return {"status": "abstain", "value": None,
            "confidence": confidence, "provenance": provenance}


def query(state, q):
    """Answer a query (§7.2). Unsupported / un-capable queries abstain, never raise.

    **The answer is Layer 5's and only the confidence is Layer 6's**, which is
    `§5 L6`'s own distinction: it asks for *"confidence permille from structural
    evidence"*, not for a better reader. `current` and `asof` take the frozen
    answer path and then have this layer's number attached; every other verb
    keeps `CERTAIN`, because every other verb returns something the engine
    regenerated exactly or abstains.
    """
    if not isinstance(state, L6State):
        return l5.query(state, q)
    if not isinstance(q, dict):
        return _abstain()
    op = q.get("op")

    if op == "current" or op == "asof":
        answer = l5.query(state, q)
        if answer["status"] != "answer":
            return answer
        horizon = q.get("t") if op == "asof" else None
        conf = confidence_for(state, q.get("entity"), q.get("key"), horizon)
        return _answer(answer["value"], conf, answer["provenance"])

    if op == "calibration":
        # The model, read through §7 rather than out of the state — the shape
        # `consolidation` (L4) and `prospection` (L5) established for a layer's
        # own diagnostic. Integers only; `tie_levels` is the confidence this
        # engine would state at each distinct-value count it currently holds.
        found = ties(state)
        levels = sorted({d for _e, _k, d in found})
        return _answer({"set_once_keys": list(SET_ONCE_KEYS),
                        "ties": len(found),
                        "tie_levels": [[d, permille(Fraction(1, d))]
                                       for d in levels]}, CERTAIN, None)

    return l5.query(state, q)          # Layers 1–5, unchanged (§7.3 below them)


# ---- snapshot / restore ------------------------------------------------------
#
# The body IS Layer 5's. Only the envelope's `magic` differs, and it differs
# because a snapshot must say which engine wrote it — a Layer-6 state restored
# through the Layer-5 reader would answer every query correctly and state a
# confidence of 1000 on a tie, which is the one failure this layer exists to make
# impossible.

def _body(state):
    return l5._body(state)


def state_checksum(state):
    """SHA-256 hex over the canonical encoding of the full state body (§2.4).

    The body is `l5._body` unchanged, so this hash differs from the Layer-5
    engine's over the same stream in exactly one atom — the recorded `layer_cap`.
    `anchors/l6.json` pins that as an identity, branch by branch, rather than
    stating it: Layer 6 changed what the engine says, not what it holds.
    """
    if not isinstance(state, L6State):
        return l5.state_checksum(state)
    return hashlib.sha256(encode(_body(state))).hexdigest()


def snapshot(state):
    """Canonical, checksummed serialization of the state (§7.1, §2.4)."""
    if not isinstance(state, L6State):
        return l5.snapshot(state)
    body = _body(state)
    checksum = hashlib.sha256(encode(body)).hexdigest()
    return encode({"magic": MAGIC, "checksum": checksum, "body": body})


def restore(data):
    """Rebuild a state from snapshot bytes; fail loudly on any corruption.

    A Layer-5 (or lower) snapshot restores through the frozen path below, so a
    capped engine's state round-trips exactly as it always did. The Layer-6 form
    is re-enveloped and handed to the **frozen Layer-5 reader**, so there is one
    implementation of that parse and not two — every guard it carries (the shape
    of each branch, the rederived handle index, the recomputed occupancy, and the
    exactly-once invariant that no `iid` is both pending and fired) applies here
    unchanged and un-copied.
    """
    try:
        envelope = decode(data)
    except Exception as exc:                       # invalid JSON / UTF-8 / float
        raise CorruptSnapshot("snapshot is not decodable: %r" % (exc,))
    if not isinstance(envelope, dict) or frozenset(envelope.keys()) != _ENVELOPE_KEYS:
        raise CorruptSnapshot("snapshot envelope keys are wrong")
    if envelope["magic"] != MAGIC:
        return l5.restore(data)

    body = envelope["body"]
    if not isinstance(body, dict):
        raise CorruptSnapshot("snapshot body is not an object")
    if hashlib.sha256(encode(body)).hexdigest() != envelope["checksum"]:
        raise CorruptSnapshot("snapshot checksum mismatch (corruption detected)")

    inner = l5.restore(encode({"magic": l5.MAGIC,
                               "checksum": envelope["checksum"],
                               "body": body}))
    return L6State(layer_cap=inner.layer_cap, budget_cap=inner.budget_cap,
                   occupancy=inner.occupancy, next_t=inner.next_t,
                   last_cost=0, chains=inner.chains, atlas=inner.atlas,
                   irreducible=inner.irreducible, counts=inner.counts,
                   damaged=inner.damaged, demotable=inner.demotable,
                   kept=inner.kept, verbatim=inner.verbatim, index=inner.index,
                   demotions=inner.demotions, forgetting=inner.forgetting,
                   pending=inner.pending, fired=inner.fired)


# ---- the generic engine interface (§7, INTERFACE.md) -------------------------

def empty():
    """A fresh, full Layer-6 engine state (adapter contract, §7)."""
    return new_state(layer_cap=LAYER, budget_cap=DEFAULT_BUDGET)


def make_engine(layer_cap, budget_cap=DEFAULT_BUDGET):
    """A fresh state capped at `layer_cap` (§7.4). 5 = the frozen prospection engine."""
    return new_state(layer_cap=layer_cap, budget_cap=budget_cap)


def ingest(state, payload):
    """Append one event and fire what it satisfies; return `(state', caller t)`."""
    return write(state, payload)


def last_cost(state):
    """Integer work-unit cost of the most recent successful write (§3.3, §4.1)."""
    return state.last_cost

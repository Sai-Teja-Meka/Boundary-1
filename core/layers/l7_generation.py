"""core/layers/l7_generation.py — Layer 7: Generation (compose, tag, never promote).

Layers 1–6 answer with things the engine **has**. An event is returned byte-exact
or it is not; a fold inverts or its key is refused; an intention has fired or it
has not; a confidence is a fold over an interval table of things that were
ingested. Every one of those is a claim about content the store received.

Layer 7 is the first capability that returns an item the store **never held** —
and the first that has to say so. `§5 L7` gates `validity = 1000`,
`novelty = 1000`, `tagging = 1000`, self-pollution `promotion = 0` three deep,
`F >= 950`, `B = 1000` and `ECE <= 40`; `§4.2` wakes here and can never be
un-bound. The binding substrate is `corpora/l7compose` (`BOUNDARY-RULINGS.md R8`
clause 1), and the design record is `core/layers/README-l7.md`.

Pure, integer-only (§2), built entirely on the frozen Layer-1/2/3/4/5/6
primitives; it edits none of them (§9). Below `layer_cap = 7` the state IS the
frozen Layer-6 state and every verb delegates to it, so `make_engine(6)` is not
an imitation of the meta-memory engine — it is the meta-memory engine (§7.4).

## `generate` is a `query` op, not a fourth verb

`§7.1` declares **three** operations and `§1.1` says events are the only fuel, so
the only reading under which `§5 L7`'s `generate(cue)` and `§7.1` are both true is
that `generate` is a `query` op whose `Answer` carries the item, its confidence,
its provenance tag and its **lineage** (`R8` clause 2). That is the same argument
in the same place `ascension/l5/ATTAINABILITY.md`'s Reading 1 made for `intend`
and `R6` clause 2 ratified for `§7.1`'s *"appends one event"*.

`lineage` is a property of the **ITEM** — `observed` or `generated` — and is
orthogonal to `§4.2.3`'s closed four-kind vocabulary, which says how an answer
reached the **caller** (`R8` clause 4). No fifth `kind` is minted: a composed item
travels on the `derive` channel and `lineage` carries the other claim. **The field
is attached to `generate` answers and to nothing else**, so every Answer the
layers below produce is byte-identical to the Layer-6 engine's.

## The one field the state gains, and why it could not be zero

`README-l6 §0` recorded that Layer 6 added **no** field: `§5.1 L6` says
meta-memory derives confidence *"from existing state"*, and it did. `§5 L7` says
no such thing, and Stage B measured why it could not:

> `§7.1` makes `query` **pure**, so an engine cannot record what it **answered** —
> only what it **received**. Stage A's witness is a policy and records at answer
> time; an engine cannot, and one that tried would be reaching for a mutation
> `§2.1` forbids. (`ascension/l7/STAGE-B.md §5.1`)

So `promotion = 0` forces a **lineage ledger written by `ingest`**, and that
ledger is the single field `L7State` adds. It is priced by name — an entity-keyed
`{compound: rung}` map at 2 cells per generated item, `ATTAINABILITY.md §7`'s 320
cells for this artifact's 160 — in the only placement `§1.4` leaves, since *"the
engine adds nothing to an event but its `t`"* refuses the payload (`R8` clause 4).

## What the ledger can and cannot know, stated as an UPPER BOUND

At `ingest` the engine sees a `profile` payload arrive and must decide whether it
is one of its own, re-ingested. It cannot ask itself what it answered. What it
can read is the **shape of its own store**, and `STAGE-B.md §5.1` recorded the
two structural signatures this artifact leaves:

* **the mirror twin** — an item identical **modulo `entity`** is already held, so
  the arrival duplicates a compound the store already carries under another id.
  That is what makes a depth-1 re-ingestion recognisable, and on the frozen
  artifact it is unambiguous: the only compounds sharing a composed item modulo
  `entity` are the 100 mirror pairs, and no member's twin profile is in the stream
  when its own arrives (`ops/l7/t_l7_composition.py` asserts both).
* **the generated hop** — the arrival's composition passes through a compound
  component the store does **not** carry as an unmarked observation. That is what
  makes the ladder above depth 1 recognisable, and it never fires on the frozen
  stream, whose only stored profiles are composed from plain components.

Neither signature is a census and the design says so: a coincidence marks an
observation as generated, which can only make this engine **refuse to promote**
and never promote wrongly — an **upper bound on lineage**, exactly the shape
`README-l6 §4`'s `damaged`-aware `d + 1` took one layer down and exactly the
trade `ATTAINABILITY.md §7` records when it declines the 800-cell bytes-keyed
alternative.

## What Layer 7 does NOT change

The confidence is Layer 6's, unchanged, and a generated item is stated at
`CERTAIN`. `README-l6 §4` recorded that fall-through as *"exactly the wrong
answer and the first thing a Layer-7 engine must replace"* — and
`ATTAINABILITY.md §6.2` then measured that **this artifact cannot exercise it**:
composition here is deterministic and correct, so `1000‰` on a composed item *is*
right and every named policy scores `ECE = 0` exactly. Replacing a residual on an
artifact that cannot show the replacement is right would be building a level
nothing exercises, which is the thing `README-l6 §1.3` warns against. The
residual therefore stands **OPEN**, is not closed by this layer, and
`README-l7 §4` says so rather than letting `ECE = 0` be quoted as evidence
otherwise.

The answer path below Layer 7 is untouched: `current` and `asof` are the frozen
Layer-4 answers wearing Layer 6's number, `read`, `read_range`, `recall`,
`fired`, `profile` and `count` are unchanged, and no eviction phase learns about
the ledger. What gives way under pressure is never the ledger — a lineage entry
an engine dropped is a generation it could promote — so where the budget cannot
house one the engine refuses the whole transition under `§4.1.2`, which is the
rule `README-l5 §0.1` fixed for the prospection tiers, applied to the tier this
layer adds.
"""

import hashlib
from dataclasses import dataclass, replace
from fractions import Fraction

from core.serialize import encode, decode, check_canonical
from core.layers import l6_meta_memory as l6
from core.layers import l5_prospection as l5
from core.layers import l4_consolidation as l4
from core.layers.l6_meta_memory import (
    L6State, CorruptSnapshot,
    SET_ONCE_KEYS, permille, confidence_for, claimants,
    visible_chain, n_distinct, set_once, ties, CERTAIN, NO_ANSWER,
)
from core.layers.l5_prospection import (
    L5State, intention, rebuild_intention, arms, readable, satisfies,
    INTENTION_KIND, INTENTION_FORM, PREDICATES, CONNECTIVES,
    pending_cells, fired_cells, fired_by, pending_iids, fired_iids,
)
from core.layers.l4_consolidation import (
    L4State, facet, rebuild, invertible, atlas_after,
    row_shape, row_values, row_payload, ASSERTION_FORMS,
)

LAYER = 7

# A generous default cap, matching the Layer-1..6 defaults so cross-layer
# reasoning stays simple. Integer only (§2.2). `§5 L7` states no footprint
# clause and `R8` creates none, so the Layer-7 batteries score in budget at
# exactly this number.
DEFAULT_BUDGET = 1_000_000_000

MAGIC = "boundary1-l7-snapshot"
_ENVELOPE_KEYS = frozenset({"magic", "checksum", "body"})


# ---- the declared composition reading ----------------------------------------
#
# A reading of the frozen grammar and NOT a learner, in the shape this project
# has used at every layer: `HANDLE_FIELDS` (L3), `ASSERTION_FORMS` (L4),
# `INTENTION_FORM` and `PREDICATES` (L5), `SET_ONCE_KEYS` (L6). A session
# declares it; `trials/ops/l7/t_l7_composition.py` checks the declaration against
# `trials/_l7tasks`' own — one reading, two implementations, checked rather than
# assumed — and `trials/ops/l7/t_l7compose.py` checks that one against the frozen
# bytes.
#
# It had to be a SECOND reading, beside `ASSERTION_FORMS`, and the artifact's own
# grammar is why: `part` and `profile` are **outside** the frozen Layer-4 facet
# map, so to every engine below Layer 7 a `profile` event is an irreducible
# episode and not an assertion. The layer below can hold the event and cannot
# read it — exactly as `INTENTION_FORM` stood to Layer 4 one layer down.

PART_KIND = "part"
PROFILE_KIND = "profile"
COMPOUND_CLASS = "compound"
HUE_KEY = "hue"
MASS_KEY = "mass"

HUES = ("amber", "cobalt", "jade", "ochre", "rose", "slate", "teal", "umber")
GRADES = ("crude", "fine", "keen", "pure", "rare", "vivid")

PROFILE_FORM = ("kind", "entity", "grade", "hue", "mass")

COMPOSITION_FORM = """A compound is an entity carrying exactly two `part`
assertions with slots 0 and 1. Its `profile` item is determined by its two
components' `(hue, mass)`: the hue of slot 0, the sum of the masses, and the
grade at index `(HUES.index(h0) + HUES.index(h1)) % len(GRADES)`. A component's
`(hue, mass)` is its latest asserted pair; a compound component's is its own
profile's. A compound whose components' material is not determined has NO profile
and the only correct behaviour on it is abstention."""

# The two lineage values `R8` clause 4 rules, closed. `None` is not in the
# vocabulary and does not need to be: an answer that makes no lineage claim is
# the untagged case, which `§5 L7` prices at `tagging < 1000` rather than forbids.
OBSERVED = "observed"
GENERATED = "generated"
LINEAGE_VOCAB = (OBSERVED, GENERATED)

# Rule P (`R4` clause 3): one cell, one grammar atom. A ledger entry is an
# entity and its rung.
LINEAGE_ENTRY_CELLS = 2


def compose(h0, m0, h1, m1, entity):
    """The declared composition rule. Integer-only; no float ever appears (§2.2)."""
    grade = GRADES[(HUES.index(h0) + HUES.index(h1)) % len(GRADES)]
    return {"kind": PROFILE_KIND, "entity": entity, "grade": grade,
            "hue": h0, "mass": m0 + m1}


def profile_form_ok(item):
    """Grammar validity of a composed item — `§5 L7`'s `validity = 1000`."""
    if not isinstance(item, dict):
        return False
    if tuple(sorted(item.keys())) != tuple(sorted(PROFILE_FORM)):
        return False
    if item["kind"] != PROFILE_KIND:
        return False
    entity = item["entity"]
    if not _plain_int(entity) or entity < 0:
        return False
    if item["grade"] not in GRADES:
        return False
    if item["hue"] not in HUES:
        return False
    mass = item["mass"]
    if not _plain_int(mass) or mass < 0:
        return False
    return True


def _plain_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


# ---- the state ---------------------------------------------------------------

@dataclass(frozen=True)
class L7State(L6State):
    """The frozen Layer-7 engine state (§2.1) — Layer 6's, plus the ledger.

    A **subclass** of the frozen `L6State`, which is what makes Layers 1–6 an
    inheritance rather than a re-implementation: every verb, cost function and
    eviction phase below operates on this state unchanged, `replace()` returns an
    `L7State`, and the single `occupancy` counter covers the ledger too — so the
    Layer-4 write path evicts *around* it without knowing it is there, exactly as
    it does around Layer 5's two prospection tiers.

    `lineage` is `{entity: rung}` — the compounds whose `profile` this engine
    composed, and how deep. It is the ONE field Layer 7 adds, and `README-l7 §0`
    records the measurement that forced it: `query` is pure, so a ledger can only
    be written by `ingest`.
    """

    lineage: dict = None    # entity -> rung (1 = composed from asserted material)


def new_state(layer_cap, budget_cap):
    """A fresh state capped at `layer_cap` with integer budget cap `budget_cap`.

    Below Layer 7 this returns the **frozen Layer-6 state** (§7.4), which below
    Layer 6 is the frozen Layer-5 state, and so down. Capping is a
    construction-time restriction, and the honest way to build an engine with no
    generation construct is to build the engine that does not have one — which is
    what `humility/l7` measures at a conjunction of 0 of 160.
    """
    if not _plain_int(layer_cap):
        raise TypeError("layer_cap must be a plain int")
    if not _plain_int(budget_cap):
        raise TypeError("budget_cap must be a plain int")
    if layer_cap < 0:
        raise ValueError("layer_cap must be non-negative")
    if budget_cap <= 0:
        raise ValueError("budget_cap must be positive (§4.1)")
    if layer_cap < LAYER:
        return l6.new_state(layer_cap=layer_cap, budget_cap=budget_cap)
    base = l6.new_state(layer_cap=LAYER, budget_cap=budget_cap)
    return L7State(layer_cap=layer_cap, budget_cap=budget_cap,
                   occupancy=base.occupancy, next_t=0, last_cost=0,
                   chains={}, atlas={}, irreducible={}, counts={}, damaged=(),
                   demotable={}, kept={}, verbatim={}, index={}, demotions=0,
                   forgetting=base.forgetting, pending={}, fired={},
                   lineage={})


# ---- cost accounting (§4.1, priced under rule P — R4 clause 3) --------------

def lineage_cells(ledger):
    """`ATTAINABILITY.md §7`'s price, in code: 2 cells per generated item.

    An entity and its rung, which is exactly the two atoms the snapshot body
    carries per entry — so the engine's own accounting and the atoms a reader can
    count in its serialized state are the same number.
    """
    return LINEAGE_ENTRY_CELLS * len(ledger)


def accounted_occupancy(state):
    """Recompute occupancy from the state alone — `restore`'s independent guard."""
    if not isinstance(state, L7State):
        return l6.accounted_occupancy(state)
    return l6.accounted_occupancy(state) + lineage_cells(state.lineage)


# ---- the composition reading, over the engine's OWN state --------------------
#
# `part` and `profile` payloads have no Layer-4 facet, so the engine holds them
# as irreducible episodes in the `kept` tier under the Layer-4 row codec. Reading
# them back is therefore a scan of **two row groups** and needs no second access
# path: `ATTAINABILITY.md §7` disclaimed that path and named the two options, and
# this is the free one — *"extends the declared facet map (one more branch in a
# reading)"* rather than *"buys a second access path"* at `README-l4 §0.1`'s
# measured 343 permille.
#
# The consequence is stated rather than hidden, and it is the Layer-4 trade one
# layer up: **query time pays where state cannot** (`README-l4 §0.1`). It is also
# why composition degrades honestly under pressure — an evicted `part` episode is
# a compound whose material the reading no longer determines, and the engine
# abstains rather than composing from a hole.


def _rows_of_kind(state, kind):
    """`(t, payload)` for every retained episode of one grammar kind, `t` ascending."""
    out = []
    for tier in (state.kept, state.demotable):
        for shape, group in tier.items():
            if shape is None or shape[0] != kind:
                continue
            for t, values in group.items():
                out.append((t, row_payload(shape, values)))
    for t, payload in state.verbatim.items():
        if isinstance(payload, dict) and payload.get("kind") == kind:
            out.append((t, payload))
    out.sort(key=lambda row: row[0])
    return out


def parts_of(state):
    """`entity -> {slot: (t, of)}` for every compound the store still carries."""
    out = {}
    for t, payload in _rows_of_kind(state, PART_KIND):
        entity = payload.get("entity")
        slot = payload.get("slot")
        of = payload.get("of")
        if not (_plain_int(entity) and _plain_int(slot) and _plain_int(of)):
            continue
        out.setdefault(entity, {})[slot] = (t, of)
    return out


def profiles_of(state):
    """`entity -> (t, item)` for every `profile` episode the store still carries."""
    out = {}
    for t, payload in _rows_of_kind(state, PROFILE_KIND):
        entity = payload.get("entity")
        if not _plain_int(entity):
            continue
        out[entity] = (t, payload)        # `t` ascending, so the latest wins
    return out


def is_compound(parts, entity):
    slots = parts.get(entity)
    return slots is not None and 0 in slots and 1 in slots


def latest(state, entity, key):
    """The `(t, value)` of the last assertion on one chain, or `None`."""
    per = state.chains.get(key)
    if per is None:
        return None
    chain = per.get(entity)
    if not chain:
        return None
    stamp = next(reversed(chain))
    return (stamp, chain[stamp])


def material(state, parts, profiles, entity, seen=None):
    """`(hue, mass, support)` for one component, or `None` when undetermined.

    A plain component's material is its latest asserted `hue` and `mass`. A
    compound component's is its own profile item's — stored if the store carries
    one, composed otherwise — which is what closes the rule under composition and
    gives the self-pollution ladder its rungs.
    """
    seen = set() if seen is None else seen
    if entity in seen:
        return None                              # a cycle is not a reading
    if is_compound(parts, entity):
        built = profile_of(state, parts, profiles, entity, seen | {entity})
        if built is None:
            return None
        item, support = built
        return (item["hue"], item["mass"], support)
    hue = latest(state, entity, HUE_KEY)
    mass = latest(state, entity, MASS_KEY)
    if hue is None or mass is None:
        return None
    if not isinstance(hue[1], str) or not _plain_int(mass[1]):
        return None
    if hue[1] not in HUES:
        return None
    return (hue[1], mass[1], (hue[0], mass[0]))


def profile_of(state, parts, profiles, entity, seen=None):
    """`(item, support)` — the stored profile if there is one, else the composed one.

    `support` is the ascending tuple of every `t` the rule actually **read**,
    which is what makes `§4.2`'s `support` a RELEVANCE claim on this artifact and
    not merely a schema-valid list (`R8` clause 5(b)).
    """
    stored = profiles.get(entity)
    if stored is not None:
        return (stored[1], (stored[0],))
    if not is_compound(parts, entity):
        return None
    return _compose_from(state, parts, profiles, entity,
                         set() if seen is None else seen)


def composed_only(state, parts, profiles, entity, seen=None):
    """The composed item, IGNORING any stored profile for `entity` itself.

    What a generator computes once it has decided the stored copy is its own
    re-ingested output: the rule, applied to the material.
    """
    if not is_compound(parts, entity):
        return None
    seen = set() if seen is None else seen
    return _compose_from(state, parts, profiles, entity, seen | {entity})


def _compose_from(state, parts, profiles, entity, seen):
    slots = parts[entity]
    support = [slots[0][0], slots[1][0]]
    mat = []
    for slot in (0, 1):
        m = material(state, parts, profiles, slots[slot][1], seen)
        if m is None:
            return None
        mat.append(m)
        support.extend(m[2])
    item = compose(mat[0][0], mat[0][1], mat[1][0], mat[1][1], entity)
    return (item, tuple(sorted(set(support))))


# ---- the lineage ledger, written by `ingest` --------------------------------

def _strip_entity(item):
    return {k: v for k, v in item.items() if k != "entity"}


def own_generation(state, payload, parts=None, profiles=None):
    """Is this arriving `profile` payload one this engine composed?

    `§7.1` makes `query` pure, so this is the only moment at which the question
    can be asked at all (`STAGE-B.md §5.1`). Two structural signatures, either
    sufficient, and both read off the store as it stands **before** the write:

      (a) **the mirror twin** — an item identical modulo `entity` is already
          held, so the arrival duplicates a compound the store already carries
          under another id;
      (b) **the generated hop** — the composition passes through a compound
          component the store does not carry as an *unmarked observation*.

    (a) recognises a depth-1 re-ingestion; (b) recognises every rung above it,
    and keeps recognising it when the rung below has already been marked. An
    entity already in the ledger stays in it, which is what makes the ledger
    entity-keyed rather than bytes-keyed (`ATTAINABILITY.md §7`: the cheap form
    can only make the engine REFUSE to promote, never promote wrongly).
    """
    if not isinstance(payload, dict) or payload.get("kind") != PROFILE_KIND:
        return False
    entity = payload.get("entity")
    if not _plain_int(entity):
        return False
    if entity in state.lineage:
        return True
    parts = parts_of(state) if parts is None else parts
    profiles = profiles_of(state) if profiles is None else profiles

    slots = parts.get(entity)
    if slots is not None and 0 in slots and 1 in slots:
        for slot in (0, 1):
            child = slots[slot][1]
            if is_compound(parts, child) \
                    and (child not in profiles or child in state.lineage):
                return True

    stripped = _strip_entity(payload)
    for other, (_t, item) in profiles.items():
        if other != entity and _strip_entity(item) == stripped:
            return True
    return False


def lineage_rung(state, entity, parts=None):
    """How deep this generation is: 1, or one more than its deepest generated part."""
    parts = parts_of(state) if parts is None else parts
    slots = parts.get(entity)
    deepest = 0
    if slots is not None:
        for slot in (0, 1):
            if slot not in slots:
                continue
            child = slots[slot][1]
            deepest = max(deepest, state.lineage.get(child, 0))
    return deepest + 1


# ---- the write --------------------------------------------------------------

def write(state, payload):
    """Ingest one event, marking it in the ledger if the engine composed it.

    Below Layer 7 this is the frozen Layer-6 write, unchanged — the capped engine
    IS the meta-memory engine (§7.4). At Layer 7 the order is: read the store's
    own shape first, apply the frozen write, then record the lineage the shape
    implied, all inside one pure transition (§2.1).

    **The ledger is not evictable, and that is the layer rather than a
    convenience**: a lineage entry an engine dropped is a generation it could
    promote, so an eviction path reaching it would be an engine that can be made
    to break `§5 L7`'s `promotion = 0` by being poor. What gives way is the
    episodic tier, exactly as at Layers 4 and 5. Where the budget cannot house
    the entry even so, the engine refuses the **whole** transition under `§4.1.2`
    — `t` unspent, state unchanged — which is `README-l5 §0.1`'s rule for the
    prospection tiers applied to the tier this layer adds. On the binding
    artifact it never arises (`refused = 0`).
    """
    check_canonical(payload)
    if not isinstance(state, L7State):
        return l6.write(state, payload)

    mark = own_generation(state, payload)
    rung = lineage_rung(state, payload["entity"]) if mark else 0

    out, t = l6.write(state, payload)
    if t is None:
        return state, None
    if not mark or payload["entity"] in out.lineage:
        return out, t

    ledger = dict(out.lineage)
    ledger[payload["entity"]] = rung
    grown = replace(out, lineage=ledger,
                    occupancy=out.occupancy + LINEAGE_ENTRY_CELLS)
    if grown.occupancy > state.budget_cap:
        return state, None                       # a deterministic refusal (§4.1.2)
    return grown, t


# ---- the layers below, unchanged --------------------------------------------

read = l6.read
read_range = l6.read_range
recall = l6.recall
retained = l6.retained
current = l6.current
asof = l6.asof
profile = l6.profile
covers_from = l6.covers_from
chain_cells = l6.chain_cells
irreducible_cells = l6.irreducible_cells
rows_cells = l6.rows_cells
index_cells = l6.index_cells


# ---- generation --------------------------------------------------------------

def generate(state, entity):
    """`(item, lineage, support)` for one compound, or `None` where the rule is silent.

    The whole capability, and it is short because the reading does the work:

      * a `profile` the store **holds** and the ledger does **not** claim is an
        `observed` item, answered as a `recall` supported by its own `t`;
      * anything else the rule determines is **composed**, tagged `generated`,
        and cites exactly the `t`s the rule read;
      * a compound whose material the store does not determine has no item, and
        abstention is the only correct behaviour — the 100 generation-shaped
        `KU1` probes of `corpora/l7compose` are where composing anything at all
        would be the fabrication `§3.0` prices at 0.

    **The lineage decision is a store consultation and cannot be anything else.**
    On a mirror pair the two members' cues are the same object once the entity id
    is blanked and their items are the same item, so nothing in the query and
    nothing in the answer separates them (`R8` clause 1, Theorem 1). What
    separates them is that one is in the store and the other is not.
    """
    parts = parts_of(state)
    profiles = profiles_of(state)
    stored = profiles.get(entity)
    if stored is not None and entity not in state.lineage:
        t, item = stored
        return (item, OBSERVED, (t,))
    built = composed_only(state, parts, profiles, entity)
    if built is None:
        return None
    item, support = built
    return (item, GENERATED, support)


def lineage_of(state, entity):
    """The rung at which this engine composed `entity`'s item, or `None`."""
    if not isinstance(state, L7State):
        return None
    return state.lineage.get(entity)


# ---- the Answer (§7.2) & the generic query binding ---------------------------

def _answer(value, confidence, provenance):
    return {"status": "answer", "value": value,
            "confidence": confidence, "provenance": provenance}


def _abstain(confidence=NO_ANSWER, provenance=None):
    return {"status": "abstain", "value": None,
            "confidence": confidence, "provenance": provenance}


def _generated_answer(value, lineage, confidence, provenance):
    """`§7.2`'s four keys plus the ONE field `R8` clause 2 adds beside them."""
    out = _answer(value, confidence, provenance)
    out["lineage"] = lineage
    return out


def query(state, q):
    """Answer a query (§7.2). Unsupported / un-capable queries abstain, never raise.

    `generate` is the one op this layer adds and the one Answer that carries a
    `lineage` field. Everything else is Layer 6's Answer, byte for byte —
    including its `confidence`, which is why `inheritance/l7`'s Layer-6 row is
    green for a structural reason rather than a lucky one.
    """
    if not isinstance(state, L7State):
        return l6.query(state, q)
    if not isinstance(q, dict):
        return _abstain()
    op = q.get("op")

    if op == "generate":
        cue = q.get("cue")
        if not isinstance(cue, dict) or cue.get("kind") != PROFILE_KIND:
            return _abstain()
        entity = cue.get("entity")
        if not _plain_int(entity):
            return _abstain()
        built = generate(state, entity)
        if built is None:
            return _abstain()
        item, lineage, support = built
        kind = "recall" if lineage == OBSERVED else "derive"
        return _generated_answer(
            item, lineage, CERTAIN,
            {"support": list(support), "kind": kind, "t_asof": max(support)})

    if op == "lineage":
        # The ledger, read through `§7` rather than out of the state — the shape
        # `consolidation` (L4), `prospection` (L5) and `calibration` (L6)
        # established for a layer's own diagnostic. Integers only.
        entity = q.get("entity")
        if entity is not None:
            if not _plain_int(entity):
                return _abstain()
            rung = state.lineage.get(entity)
            if rung is None:
                return _abstain()
            return _answer({"entity": entity, "rung": rung}, CERTAIN, None)
        by_rung = {}
        for rung in state.lineage.values():
            by_rung[rung] = by_rung.get(rung, 0) + 1
        return _answer({"generated": len(state.lineage),
                        "cells": lineage_cells(state.lineage),
                        "by_rung": [[r, by_rung[r]] for r in sorted(by_rung)]},
                       CERTAIN, None)

    return l6.query(state, q)          # Layers 1–6, unchanged (§7.3 below them)


# ---- snapshot / restore ------------------------------------------------------
#
# The body is Layer 6's plus one branch, and the envelope's `magic` differs
# because a snapshot must say which engine wrote it: a Layer-7 state restored
# through the Layer-6 reader would answer every retrieval correctly and have
# forgotten **which items were its own**, which is exactly how `promotion = 0`
# breaks.

def _lineage_body(ledger):
    return [[entity, ledger[entity]] for entity in sorted(ledger)]


def _body(state):
    body = l6._body(state)
    body["lineage"] = _lineage_body(state.lineage)
    return body


def state_checksum(state):
    """SHA-256 hex over the canonical encoding of the full state body (§2.4)."""
    if not isinstance(state, L7State):
        return l6.state_checksum(state)
    return hashlib.sha256(encode(_body(state))).hexdigest()


def snapshot(state):
    """Canonical, checksummed serialization of the state (§7.1, §2.4)."""
    if not isinstance(state, L7State):
        return l6.snapshot(state)
    body = _body(state)
    checksum = hashlib.sha256(encode(body)).hexdigest()
    return encode({"magic": MAGIC, "checksum": checksum, "body": body})


def _lineage_from_body(raw):
    if not isinstance(raw, list):
        raise CorruptSnapshot("snapshot lineage branch is not an array")
    out = {}
    for row in raw:
        if not isinstance(row, list) or len(row) != 2:
            raise CorruptSnapshot("snapshot lineage entry is malformed")
        entity, rung = row
        if not _plain_int(entity) or not _plain_int(rung) or rung < 1:
            raise CorruptSnapshot("snapshot lineage entry is not (entity, rung)")
        if entity in out:
            raise CorruptSnapshot("snapshot lineage names an entity twice")
        out[entity] = rung
    return out


def restore(data):
    """Rebuild a state from snapshot bytes; fail loudly on any corruption.

    A Layer-6 (or lower) snapshot restores through the frozen path below, so a
    capped engine's state round-trips exactly as it always did. The Layer-7 form
    is re-enveloped and handed to the **frozen Layer-6 reader**, so there is one
    implementation of that parse and not two — every guard it carries applies
    here unchanged and un-copied — and the ledger is then checked on its own
    terms: an entity named twice, a rung below 1, or a total that does not
    reconcile with the recorded occupancy is a corrupt snapshot and not a quiet
    difference of opinion about what the engine made.
    """
    try:
        envelope = decode(data)
    except Exception as exc:                       # invalid JSON / UTF-8 / float
        raise CorruptSnapshot("snapshot is not decodable: %r" % (exc,))
    if not isinstance(envelope, dict) or frozenset(envelope.keys()) != _ENVELOPE_KEYS:
        raise CorruptSnapshot("snapshot envelope keys are wrong")
    if envelope["magic"] != MAGIC:
        return l6.restore(data)

    body = envelope["body"]
    if not isinstance(body, dict):
        raise CorruptSnapshot("snapshot body is not an object")
    if "lineage" not in body:
        raise CorruptSnapshot("snapshot body has no lineage branch")
    if hashlib.sha256(encode(body)).hexdigest() != envelope["checksum"]:
        raise CorruptSnapshot("snapshot checksum mismatch (corruption detected)")

    ledger = _lineage_from_body(body["lineage"])
    inner = dict(body)
    del inner["lineage"]
    inner["occupancy"] = body["occupancy"] - lineage_cells(ledger)
    base = l6.restore(encode({"magic": l6.MAGIC,
                              "checksum": hashlib.sha256(
                                  encode(inner)).hexdigest(),
                              "body": inner}))

    state = L7State(layer_cap=base.layer_cap, budget_cap=base.budget_cap,
                    occupancy=body["occupancy"], next_t=base.next_t,
                    last_cost=0, chains=base.chains, atlas=base.atlas,
                    irreducible=base.irreducible, counts=base.counts,
                    damaged=base.damaged, demotable=base.demotable,
                    kept=base.kept, verbatim=base.verbatim, index=base.index,
                    demotions=base.demotions, forgetting=base.forgetting,
                    pending=base.pending, fired=base.fired, lineage=ledger)
    if accounted_occupancy(state) != body["occupancy"]:
        raise CorruptSnapshot("snapshot occupancy diverges from the accounted cost")
    return state


# ---- the generic engine interface (§7, INTERFACE.md) -------------------------

def empty():
    """A fresh, full Layer-7 engine state (adapter contract, §7)."""
    return new_state(layer_cap=LAYER, budget_cap=DEFAULT_BUDGET)


def make_engine(layer_cap, budget_cap=DEFAULT_BUDGET):
    """A fresh state capped at `layer_cap` (§7.4). 6 = the frozen meta-memory engine."""
    return new_state(layer_cap=layer_cap, budget_cap=budget_cap)


def ingest(state, payload):
    """Append one event and fire what it satisfies; return `(state', caller t)`."""
    return write(state, payload)


def last_cost(state):
    """Integer work-unit cost of the most recent successful write (§3.3, §4.1)."""
    return state.last_cost

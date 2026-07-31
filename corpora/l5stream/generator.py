"""corpora/l5stream/generator.py — the Layer-5 PROSPECTION stream.

The `l4stream` world with one new event kind: **`intend`**, an intention carried
as an ordinary ingested payload under a declared grammar reading. Built for the
Layer-5 ascension gate (`trigger-precision = trigger-recall = 1000`,
`dup-fire = miss = 0`, `F ≥ 980`, `B = 1000`), and frozen by the Layer-5 Stage-A
attainability session before any Layer-5 trial applies a gate to any engine.

## Why an intention is an event and not a fourth verb

`BOUNDARY.md §7.1` declares **three** operations — `ingest`, `query`, `snapshot`
— and `§1.1` says events are the only fuel: *"Configuration, queries, and
side-band signals are not fuel."* `§5 L5`'s `intend(condition → event)` cannot
therefore be a fourth entry point. It arrives as an **ingested payload** whose
reading is declared by this grammar, exactly as `trials/_l4tasks.facet` is a
declared reading of the chronicle-family grammars. The engine's `intend`
*capability* is what it does with such a payload; the payload itself is fuel like
any other.

## The shape

| kind     | shape                                                            | facet |
|----------|------------------------------------------------------------------|-------|
| `spawn`  | `{"kind":"spawn","entity":<int>,"class":<str>}`                   | assertion `(entity, "class", class)` |
| `attr`   | `{"kind":"attr","entity":<int>,"key":<str>,"val":<int\\|str>}`     | assertion `(entity, key, val)` |
| `move`   | `{"kind":"move","entity":<int>,"loc":<str>}`                      | assertion `(entity, "loc", loc)` |
| `link`   | `{"kind":"link","src":<int>,"dst":<int>,"rel":<str>}`             | assertion `(src, rel, dst)` |
| `note`   | `{"kind":"note","entity":<int>,"text_id":<int>}`                  | **irreducible** |
| `intend` | `{"kind":"intend","iid":<int>,"cond":<AST>,"fire":<payload>}`     | **irreducible** |

The first five are `l4stream`'s, unchanged, with `l4stream`'s vocabularies (which
are chronicle's). `intend` is new and `corpora/l5stream/grammar.md` freezes its
condition grammar.

## The fired event, and why cascades are impossible by construction

An intention's `fire` payload is `{"kind":"fired","text_id":<int>}` — a globally
unique `text_id` drawn from the same counter as `note`, so no two events in this
world (caller-written or engine-emitted) share one.

`fired` is **not** in `KINDS`, the closed vocabulary the `kind` and `count_ge`
predicates draw from, and a `fired` payload carries **no** `entity`, `src`, `key`,
`val` or `loc` field. So no **payload atom** — `kind`, `entity`, `key`, `val_ge`,
`loc` — can hold on a fired event. That is the base case; the induction is
`GUARDEDNESS` below, and together they give: **no condition expressible in this
grammar is satisfiable by a fired event**, so a firing can never cascade into
another firing.

### GUARDEDNESS — the declared structural property

`count_ge` does not read the arriving payload at all (it is a fold over the past),
and `not` inverts, so neither is safe on its own: `not(kind = link)` holds on a
fired event precisely because a fired event is not a `link`. Every condition in
this stream is therefore **guarded** — every satisfying assignment requires at
least one payload atom to hold — by the induction

```
payload atom (kind|entity|key|val_ge|loc)   guarded
count_ge                                    NOT guarded  (ignores the payload)
not(A)                                      NOT guarded  (inverts)
and(A, B)                                   guarded iff A or B is guarded
or(A, B)                                    guarded iff A and B are both guarded
```

`count_ge` and `not` therefore only ever occur conjoined with a payload atom.
This was **not** the grammar's first draft: the first draft emitted bare
`not(kind = K)` and bare `count_ge`, and `trials/ops/l5/t_l5stream.py`'s
cross-product check went red on `iid 6` before the corpus was frozen. The corpus
was changed, not the trial.

It is what makes the corpus's central promise true: **satisfaction points are
computable exactly from the frozen stream alone**, with no engine in the loop.
Satisfaction is defined over **caller indices** — the 0-based line number of this
file — and never over the engine's logical `t`, because a fired event consumes a
`t` of its own (`§1.3`) and the engine's `t` for caller index `k` is therefore
`k` plus the number of firings that preceded it.

## No cancellation

`§5 L5` names `intend`, exactly-once firing, precision, recall, `dup-fire` and
`miss`. It does **not** name cancellation, revocation, expiry or re-arming, and
this corpus invents none of them: an intention, once written, is pending until it
fires, and forever if it never does. A `cancel` kind would be a capability the
constitution does not gate, and the Stage-A discipline (`R2`) is to compute
against the ratified gate rather than to enrich it.

## The three declared properties

1. **Never-fires intentions.** A declared share of conditions is unsatisfiable
   over the remainder of the stream, provably so from the corpus's own structure
   (`kind = spawn` after the spawn prelude; a `val_ge` above the value
   vocabulary's range; a `count_ge` above the whole stream's count of that kind).
   Without them, "abstain when nothing satisfies it" would be untested and
   `trigger-precision` could be bought by firing eagerly.

2. **Multiple satisfactions at one caller index.** Distinct pending intentions
   whose conditions are all satisfied by the *same* arriving write must all fire
   there. Firing order at one index is **`iid` ascending** — a declared total
   order, so `§2.3` determinism holds without appeal to a scan order.

3. **Conditions over demoted content.** The `count_ge` predicate is a fold over
   the past by grammar kind. At the Layer-4 footprint the base episodes cannot
   all be retained, so `count_ge` is answerable only from consolidated state — a
   condition over content the layer below has demoted, priced at two cells per
   kind, and the reason this layer is built on that one.

Randomness comes solely from corpora/prng.py; output is canonical JSONL. Same
(seed, n) -> byte-identical (BOUNDARY.md §8.3).
"""

import os
import sys

from corpora import canon
from corpora.prng import Xorshift64
from corpora.chronicle.generator import (
    CLASSES, ATTR_KEYS, ATTR_STR_VALS, RELS, LOCS,
)

SEED = 7007
N = 20000
ENTITIES = 200

# The closed kind vocabulary the `kind` and `count_ge` predicates draw from.
# `fired` is deliberately absent: see the module docstring.
KINDS = ("spawn", "attr", "move", "link", "note", "intend")

# The predicate vocabulary, closed. grammar.md freezes the semantics.
PREDICATES = ("kind", "entity", "key", "val_ge", "loc", "count_ge")
# The payload atoms — the ones that read the ARRIVING write. `count_ge` is a fold
# over the past and reads nothing of it, which is why it is not among them and why
# it may only appear guarded (see the module docstring's GUARDEDNESS induction).
PAYLOAD_PREDICATES = ("kind", "entity", "key", "val_ge", "loc")
CONNECTIVES = ("and", "or", "not")
MAX_COND_DEPTH = 3   # `and(atom, not(atom))` is the deepest shape emitted

# Integer `attr` values are drawn from [0, ATTR_INT_RANGE); a `val_ge` above it
# can never be satisfied by an integer assertion.
ATTR_INT_RANGE = 1000
VAL_GE_UNREACHABLE = 5000

# Event mix after the spawn prelude, as cumulative bands over one below(100).
BAND_ATTR = 66
BAND_MOVE = 75
BAND_LINK = 84
BAND_NOTE = 95        # [95,100) -> intend

# ---- the declared spec of the frozen instance (seed 7007, n 20000) ---------
#
# The byte-match law (§8.3) freezes the bytes; these constants freeze what the
# bytes are *for*. `trials/ops/l5/t_l5stream.py` asserts every one of them.

DECLARED_INTENTIONS = 945
DECLARED_FIREABLE = 765          # intentions some later caller write satisfies
DECLARED_NEVER_FIRES = 180       # DECLARED_INTENTIONS - DECLARED_FIREABLE
DECLARED_MULTI_SAT_INDICES = 34  # caller indices satisfying >1 pending intention
DECLARED_MAX_SAT_AT_INDEX = 3    # the largest such fan-out
DECLARED_COUNT_GE_CONDITIONS = 169  # conditions mentioning the demoted-content predicate
DECLARED_FIRE_AT_NEXT_WRITE = 110   # sigma == k0 + 1 — what a zero-knowledge guess gets
DECLARED_RAW_CELLS = 182555      # Σ event_cost over the frozen stream (§4.1 model)
DECLARED_NOTES = 2228            # the irreducible `note` tier
DECLARED_ASSERTIONS = 16827      # events in the Layer-4 assertion facet
DECLARED_PAIRS = 2924            # distinct (entity, key) pairs the facet reads
DECLARED_PEAK_PENDING = 184      # the pending set's high-water mark, in entries

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "l5stream.s7007.n20000.jsonl")


def _pick(rng, seq):
    return seq[rng.below(len(seq))]


# ---- the condition grammar -------------------------------------------------

def _atom_kind(rng):
    return {"p": "kind", "v": _pick(rng, KINDS)}


def _atom_entity(rng):
    return {"p": "entity", "v": 1 + rng.below(ENTITIES)}


def _atom_key(rng):
    return {"p": "key", "v": _pick(rng, ATTR_KEYS)}


def _atom_val_ge(rng, reachable=True):
    if reachable:
        return {"p": "val_ge", "v": _pick(rng, (100, 250, 500, 750, 900))}
    return {"p": "val_ge", "v": VAL_GE_UNREACHABLE}


def _atom_loc(rng):
    return {"p": "loc", "v": _pick(rng, LOCS)}


def _atom_count_ge(rng, reachable=True):
    kind = _pick(rng, KINDS)
    if reachable:
        return {"p": "count_ge", "k": kind, "v": _pick(rng, (50, 200, 800, 2000))}
    return {"p": "count_ge", "k": kind, "v": 10 * N}


def _condition(rng):
    """One condition AST, guarded by construction (see the module docstring).

    Depth <= MAX_COND_DEPTH. Every shape below contains at least one payload atom
    on every satisfying assignment: `count_ge` and `not` never stand alone.
    """
    band = rng.below(100)
    if band < 24:
        return _atom_kind(rng)
    if band < 36:
        return {"op": "and", "args": [_atom_entity(rng), _atom_key(rng)]}
    if band < 46:
        return {"op": "and", "args": [{"p": "kind", "v": "attr"},
                                      _atom_val_ge(rng)]}
    if band < 55:
        return {"op": "or", "args": [_atom_loc(rng), _atom_loc(rng)]}
    if band < 67:
        return {"op": "and", "args": [_atom_kind(rng), _atom_count_ge(rng)]}
    if band < 75:
        return {"op": "and", "args": [_atom_entity(rng), _atom_val_ge(rng)]}
    if band < 82:
        return {"op": "and", "args": [{"p": "kind", "v": "attr"},
                                      {"op": "not", "args": [_atom_val_ge(rng)]}]}
    if band < 88:
        return {"op": "or", "args": [_atom_key(rng), _atom_key(rng)]}
    if band < 92:
        return {"op": "and", "args": [_atom_entity(rng), _atom_count_ge(rng)]}
    # The declared never-fires band, unsatisfiable by construction:
    if band < 95:
        # every `spawn` is in the prelude, and intentions only occur after it
        return {"p": "kind", "v": "spawn"}
    if band < 98:
        return {"op": "and", "args": [{"p": "kind", "v": "attr"},
                                      _atom_val_ge(rng, reachable=False)]}
    return {"op": "and", "args": [_atom_kind(rng),
                                  _atom_count_ge(rng, reachable=False)]}


def generate(seed, n):
    """Yield `n` payloads: a spawn prelude, then assertions, notes and intentions."""
    rng = Xorshift64(seed)
    entities = min(ENTITIES, n)
    next_text_id = 1
    next_iid = 1

    for eid in range(1, entities + 1):
        yield {"kind": "spawn", "entity": eid, "class": _pick(rng, CLASSES)}

    for _ in range(n - entities):
        bucket = rng.below(100)
        if bucket < BAND_ATTR:
            eid = 1 + rng.below(entities)
            key = _pick(rng, ATTR_KEYS)
            if rng.chance(1, 2):
                val = rng.below(ATTR_INT_RANGE)
            else:
                val = _pick(rng, ATTR_STR_VALS)
            yield {"kind": "attr", "entity": eid, "key": key, "val": val}
        elif bucket < BAND_MOVE:
            eid = 1 + rng.below(entities)
            yield {"kind": "move", "entity": eid, "loc": _pick(rng, LOCS)}
        elif bucket < BAND_LINK:
            src = 1 + rng.below(entities)
            dst = 1 + rng.below(entities - 1)
            if dst >= src:
                dst += 1
            yield {"kind": "link", "src": src, "dst": dst, "rel": _pick(rng, RELS)}
        elif bucket < BAND_NOTE:
            eid = 1 + rng.below(entities)
            yield {"kind": "note", "entity": eid, "text_id": next_text_id}
            next_text_id += 1
        else:
            cond = _condition(rng)
            yield {"kind": "intend", "iid": next_iid, "cond": cond,
                   "fire": {"kind": "fired", "text_id": next_text_id}}
            next_text_id += 1
            next_iid += 1


def frozen_bytes():
    """The exact byte content of the frozen prospection stream."""
    return canon.encode_jsonl(generate(SEED, N))


def main(argv):
    if "--write" in argv:
        data = frozen_bytes()
        with open(FROZEN_PATH, "wb") as fh:
            fh.write(data)
        print(f"wrote {FROZEN_PATH} ({len(data)} bytes, {N} events, "
              f"{ENTITIES} entities)")
        return 0
    if "--check" in argv:
        ok = open(FROZEN_PATH, "rb").read() == frozen_bytes()
        print("byte-match OK" if ok else "BYTE-MATCH MISMATCH")
        return 0 if ok else 1
    print("usage: python3 -m corpora.l5stream.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

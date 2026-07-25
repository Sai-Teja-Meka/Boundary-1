"""corpora/l4stream/generator.py — the Layer-4 CONSOLIDATION stream.

A stream whose **grammar redundancy is controlled and declared**, built for the
Layer-4 ascension gate (`footprint ≤ 250‰`, ≥4× compression, at
`reconstruction-F ≥ 900` and `C ≥ 850`) after
`trials/ascension/l4/ATTAINABILITY.md` measured that the frozen chronicle family
cannot admit that gate under **any** consolidation policy.

## Why a fourth stream exists

Consolidation buys its compression from **redundancy**: an (entity, key) pair
asserted many times collapses into one interval chain, and a chain of `c`
assertions costs `2c` cells against `9c` raw. The chronicle grammar has almost
no such redundancy — 30 140 of its 35 200 (entity, key) pairs are asserted
**exactly once** and never superseded, mean chain length **1.209**, so 35% of any
exact history schema is spent on *identifying* pairs rather than on their values.
Its measured ceiling is recorded in `ATTAINABILITY.md`. `l4stream` is the stream
that supplies the redundancy the gate presupposes, and it declares how much.

## The shape

| kind    | shape                                                          | facet |
|---------|----------------------------------------------------------------|-------|
| `spawn` | `{"kind":"spawn","entity":<int>,"class":<str>}`                 | assertion `(entity, "class", class)` |
| `attr`  | `{"kind":"attr","entity":<int>,"key":<str>,"val":<int\|str>}`   | assertion `(entity, key, val)` |
| `move`  | `{"kind":"move","entity":<int>,"loc":<str>}`                    | assertion `(entity, "loc", loc)` |
| `link`  | `{"kind":"link","src":<int>,"dst":<int>,"rel":<str>}`           | assertion `(src, rel, dst)` |
| `note`  | `{"kind":"note","entity":<int>,"text_id":<int>}`                | **irreducible** |

The vocabularies are chronicle's, unchanged (`corpora/chronicle/grammar.md`), so
this is the same world with a different *shape of history* — not a different
language. Payloads use only integers and strings; there is no `importance` field
(Layer 4 weights every target `1`, §3.2's default).

## The three declared properties

1. **Bounded population.** Exactly `ENTITIES` entities, all spawned in the first
   `ENTITIES` events, and **none ever retires**. A persistent world is what makes
   supersession chains long; a churning one spends its budget on identity.

2. **Declared assertion redundancy.** Every assertion falls in the fixed key
   space `ENTITIES × (ATTR_KEYS + {loc, class} + RELS)`, so the pair count is
   `ENTITIES × KEYS_PER_ENTITY` by construction and the mean chain length is
   `assertions / pairs` — the corpus's redundancy ratio, asserted by
   `trials/ops/l4/t_l4stream.py` against `DECLARED_*` below.

3. **A declared irreducible tier.** `note` events carry a globally unique
   `text_id` that appears **exactly once** in the stream. Notes are
   grammar-redundant with nothing; no schema can regenerate one. They exist so
   that reconstruction fidelity is bounded **below 1000 by construction** and the
   `F ≥ 900` gate measures honest lossy compression rather than a corpus with
   nothing to lose.

`link` is modelled as an assertion on `(src, rel)` with the target as its value:
that is Graphiti's bitemporal edge (GAPMAP **S3**) with the two LLM calls
replaced by interval arithmetic — the current value of `(src, rel)` is the
edge's currently-valid target, and its participation set is the distinct values
of the chain.

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

SEED = 6006
N = 20000
ENTITIES = 200

# The fixed key space of the assertion facet, per entity.
LIFECYCLE_KEYS = ("class", "loc")
KEYS_PER_ENTITY = len(ATTR_KEYS) + len(LIFECYCLE_KEYS) + len(RELS)   # 8 + 2 + 6

# Event mix after the spawn prelude, as cumulative bands over one below(100).
BAND_ATTR = 74
BAND_MOVE = 84
BAND_LINK = 94        # [94,100) -> note

# ---- the declared spec of the frozen instance (seed 6006, n 20000) ---------
#
# The byte-match law (§8.3) freezes the bytes; these constants freeze what the
# bytes are *for*. `trials/ops/l4/t_l4stream.py` asserts every one of them, so a
# regeneration that stayed byte-identical while meaning something else is
# impossible, and so is a silent drift in the redundancy the gate rests on.

DECLARED_PAIR_UNIVERSE = 3200  # ENTITIES × KEYS_PER_ENTITY — the key space
DECLARED_PAIRS = 2951          # distinct (entity, key) pairs actually asserted
DECLARED_ASSERTIONS = 18788    # events in the assertion facet (all but `note`)
DECLARED_NOTES = 1212          # the irreducible tier
DECLARED_RAW_CELLS = 173200    # Σ event_cost over the frozen stream (§4.1 model)
DECLARED_MAX_CHAIN = 19        # the longest supersession chain
# The redundancy the Layer-4 gate rests on, as a permille ratio so it is exact:
# mean assertions per pair = 18788/2951 = 6.366… The chronicle family measures
# 1.197 (chronicle) and 1.305 (murk) — see trials/ascension/l4/ATTAINABILITY.md.
DECLARED_MEAN_CHAIN_PERMILLE = 6367
# The share of assertions that are a pair's LATEST — what a current-value table
# with no history at all could answer. Low here (157‰) and high on the chronicle
# family (836‰ / 766‰): that gap is what makes the as-of battery a real test.
DECLARED_TERMINAL_SHARE_PERMILLE = 157

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "l4stream.s6006.n20000.jsonl")


def _pick(rng, seq):
    return seq[rng.below(len(seq))]


def generate(seed, n):
    """Yield `n` payloads: a spawn prelude, then a redundant assertion stream."""
    rng = Xorshift64(seed)
    entities = min(ENTITIES, n)
    next_text_id = 1

    for eid in range(1, entities + 1):
        yield {"kind": "spawn", "entity": eid, "class": _pick(rng, CLASSES)}

    for _ in range(n - entities):
        bucket = rng.below(100)
        if bucket < BAND_ATTR:
            eid = 1 + rng.below(entities)
            key = _pick(rng, ATTR_KEYS)
            if rng.chance(1, 2):
                val = rng.below(1000)
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
        else:
            eid = 1 + rng.below(entities)
            yield {"kind": "note", "entity": eid, "text_id": next_text_id}
            next_text_id += 1


def frozen_bytes():
    """The exact byte content of the frozen consolidation stream."""
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
    print("usage: python3 -m corpora.l4stream.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

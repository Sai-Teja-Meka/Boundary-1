"""corpora/chronicle/generator.py — deterministic chronicle generator.

See corpora/chronicle/grammar.md for the grammar. Randomness comes solely from
corpora/prng.py. Output is canonical JSONL (corpora/canon.py). Two runs at the
same (seed, n) are byte-identical (BOUNDARY.md §8.3).

Only lists and integer indices are used in the generation path — no set
iteration — so ordering is fully deterministic across platforms.
"""

import os
import sys

from corpora import canon
from corpora.prng import Xorshift64

CLASSES = ("node", "agent", "record", "token", "vault", "relay", "ledger", "beacon")
ATTR_KEYS = ("status", "level", "owner", "tag", "size", "region", "tier", "mode")
ATTR_STR_VALS = ("alpha", "beta", "gamma", "delta", "idle", "active",
                 "sealed", "open", "north", "south", "east", "west")
RELS = ("owns", "links", "parent", "mirrors", "feeds", "guards")
LOCS = ("hall_a", "hall_b", "vault_1", "vault_2", "gate", "yard", "depths", "spire")

SEED = 1001
N = 50000

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "chronicle.s1001.n50000.jsonl")


def _pick(rng, seq):
    return seq[rng.below(len(seq))]


def _two_distinct(rng, live):
    """Two distinct indices into `live` (len(live) >= 2), uniform."""
    i = rng.below(len(live))
    j = rng.below(len(live) - 1)
    if j >= i:
        j += 1
    return live[i], live[j]


def generate(seed, n):
    """Yield `n` chronicle event payloads deterministically from `seed`."""
    rng = Xorshift64(seed)
    live = []          # live entity ids, insertion order
    next_id = 1
    produced = 0
    while produced < n:
        if not live:
            action = "spawn"
        else:
            bucket = rng.below(100)
            if bucket < 20:
                action = "spawn"
            elif bucket < 60:
                action = "attr"
            elif bucket < 75:
                action = "link" if len(live) >= 2 else "attr"
            elif bucket < 90:
                action = "move"
            else:
                action = "retire" if len(live) > 1 else "attr"

        if action == "spawn":
            eid = next_id
            next_id += 1
            live.append(eid)
            event = {"kind": "spawn", "entity": eid, "class": _pick(rng, CLASSES)}
        elif action == "attr":
            eid = _pick(rng, live)
            key = _pick(rng, ATTR_KEYS)
            if rng.chance(1, 2):
                val = rng.below(1000)
            else:
                val = _pick(rng, ATTR_STR_VALS)
            event = {"kind": "attr", "entity": eid, "key": key, "val": val}
        elif action == "link":
            src, dst = _two_distinct(rng, live)
            event = {"kind": "link", "src": src, "dst": dst, "rel": _pick(rng, RELS)}
        elif action == "move":
            eid = _pick(rng, live)
            event = {"kind": "move", "entity": eid, "loc": _pick(rng, LOCS)}
        else:  # retire
            idx = rng.below(len(live))
            eid = live[idx]
            live[idx] = live[-1]
            live.pop()
            event = {"kind": "retire", "entity": eid}

        yield event
        produced += 1


def frozen_bytes():
    """The exact byte content of the frozen chronicle corpus."""
    return canon.encode_jsonl(generate(SEED, N))


def main(argv):
    if "--write" in argv:
        data = frozen_bytes()
        with open(FROZEN_PATH, "wb") as fh:
            fh.write(data)
        print(f"wrote {FROZEN_PATH} ({len(data)} bytes, {N} events)")
        return 0
    if "--check" in argv:
        want = open(FROZEN_PATH, "rb").read()
        got = frozen_bytes()
        ok = want == got
        print("byte-match OK" if ok else "BYTE-MATCH MISMATCH")
        return 0 if ok else 1
    print("usage: python3 -m corpora.chronicle.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

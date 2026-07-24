"""corpora/murk/generator.py — the murk family (controlled dirt).

A generator LAYER over the chronicle base grammar that injects controlled
defects through explicit knobs, and records EVERY injected defect in a paired
answer key (`ground_truth.json`). Dirt is always paired with the answer key
(BOUNDARY.md §8.7): no defect is injected without being recorded, with the
event `t`'s it touches.

Four defect knobs (rates in permille, per event; at most one defect per event,
selected from a single draw over the cumulative bands):

  - contradiction : re-assert an entity's set-once attribute `origin` with a
                    DIFFERENT value (a genuine contradiction, not a legal update).
  - near_duplicate: restate an existing fact verbatim (a redundant re-assertion
                    of a prior `attr` or `link`) that dedup should collapse.
  - ambiguity     : reuse a previously-RETIRED entity id for a fresh spawn, so
                    later references to that id are ambiguous across incarnations.
  - malformed     : emit a grammar-violating payload that is still canonical-JSON
                    valid (missing field / wrong scalar type / unknown kind /
                    dangling reference).

`t` is the 0-based index of the event in the final frozen stream (the logical
time the engine will assign on ingestion).

Randomness comes solely from corpora/prng.py; output is canonical JSONL and the
answer key is canonical JSON. Same (seed, n) -> byte-identical (§8.3).
"""

import os
import sys

from corpora import canon
from corpora.prng import Xorshift64
from corpora.chronicle.generator import (
    CLASSES, ATTR_KEYS, ATTR_STR_VALS, RELS, LOCS,
)

SEED = 3003
N = 10000

# Knob rates, permille per event (cumulative bands over a single below(1000) draw).
KNOBS = {
    "contradiction": 30,
    "near_duplicate": 40,
    "ambiguity": 20,
    "malformed": 25,
}
_C = KNOBS["contradiction"]
_D = _C + KNOBS["near_duplicate"]
_A = _D + KNOBS["ambiguity"]
_M = _A + KNOBS["malformed"]

IMMUTABLE_KEY = "origin"
# Murk's own attr-key vocabulary: the chronicle keys plus the set-once `origin`
# key that the contradiction knob targets. `origin` is set at most once per
# entity by the clean base; only the contradiction knob re-asserts it.
MURK_ATTR_KEYS = ATTR_KEYS + (IMMUTABLE_KEY,)
_DANGLING_ID = 999999999

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "murk.s3003.n10000.jsonl")
GROUND_TRUTH_PATH = os.path.join(_HERE, "ground_truth.json")


def _pick(rng, seq):
    return seq[rng.below(len(seq))]


class _World:
    """Mutable base-world state shared by the normal and injected paths."""

    def __init__(self):
        self.live = []            # live entity ids (insertion order)
        self.retired = []         # retired entity ids (available for reuse)
        self.next_id = 1
        self.origin = {}          # eid -> origin value (set-once in clean base)
        self.origin_t = {}        # eid -> t at which origin was set
        self.origin_ids = []      # eids that have an origin (for contradiction)
        self.last_attr = None     # (t, event) for near-duplicate
        self.last_link = None     # (t, event) for near-duplicate


def _normal_event(rng, w, t):
    """Produce one clean chronicle-style event; mutate world; record dup anchors."""
    if not w.live:
        action = "spawn"
    else:
        bucket = rng.below(100)
        if bucket < 20:
            action = "spawn"
        elif bucket < 60:
            action = "attr"
        elif bucket < 75:
            action = "link" if len(w.live) >= 2 else "attr"
        elif bucket < 90:
            action = "move"
        else:
            action = "retire" if len(w.live) > 1 else "attr"

    if action == "spawn":
        eid = w.next_id
        w.next_id += 1
        w.live.append(eid)
        return {"kind": "spawn", "entity": eid, "class": _pick(rng, CLASSES)}

    if action == "attr":
        eid = _pick(rng, w.live)
        key = _pick(rng, MURK_ATTR_KEYS)
        if key == IMMUTABLE_KEY and eid in w.origin:
            # Preserve set-once semantics in the CLEAN base: only murk violates it.
            key = "status"
        if rng.chance(1, 2):
            val = rng.below(1000)
        else:
            val = _pick(rng, ATTR_STR_VALS)
        event = {"kind": "attr", "entity": eid, "key": key, "val": val}
        if key == IMMUTABLE_KEY:
            w.origin[eid] = val
            w.origin_t[eid] = t
            w.origin_ids.append(eid)
        w.last_attr = (t, event)
        return event

    if action == "link":
        i = rng.below(len(w.live))
        j = rng.below(len(w.live) - 1)
        if j >= i:
            j += 1
        event = {"kind": "link", "src": w.live[i], "dst": w.live[j],
                 "rel": _pick(rng, RELS)}
        w.last_link = (t, event)
        return event

    if action == "move":
        eid = _pick(rng, w.live)
        return {"kind": "move", "entity": eid, "loc": _pick(rng, LOCS)}

    # retire
    idx = rng.below(len(w.live))
    eid = w.live[idx]
    w.live[idx] = w.live[-1]
    w.live.pop()
    w.retired.append(eid)
    return {"kind": "retire", "entity": eid}


def generate_full(seed, n):
    """Return (events, ground_truth_dict) deterministically from (seed, n)."""
    rng = Xorshift64(seed)
    w = _World()
    events = []
    defects = []

    def emit(ev):
        events.append(ev)
        return len(events) - 1

    while len(events) < n:
        t = len(events)
        r = rng.below(1000)

        if r < _C and w.origin_ids:
            # contradiction: re-assert origin with a different value
            eid = _pick(rng, w.origin_ids)
            old = w.origin[eid]
            new = old
            while new == old:
                if rng.chance(1, 2):
                    new = rng.below(1000)
                else:
                    new = _pick(rng, ATTR_STR_VALS)
            ev = {"kind": "attr", "entity": eid, "key": IMMUTABLE_KEY, "val": new}
            ti = emit(ev)
            defects.append({
                "t": ti, "type": "contradiction", "entity": eid,
                "key": IMMUTABLE_KEY, "refs": sorted([w.origin_t[eid], ti]),
                "values": [old, new],
            })

        elif r < _D and (w.last_attr is not None or w.last_link is not None):
            # near_duplicate: restate a prior fact verbatim
            if w.last_attr is not None and (w.last_link is None or rng.chance(1, 2)):
                orig_t, ev0 = w.last_attr
                kind = "attr"
            else:
                orig_t, ev0 = w.last_link
                kind = "link"
            ev = dict(ev0)
            ti = emit(ev)
            defects.append({
                "t": ti, "type": "near_duplicate", "of_kind": kind,
                "refs": [orig_t, ti],
            })

        elif r < _A and w.retired:
            # ambiguity: reuse a retired id for a fresh spawn
            idx = rng.below(len(w.retired))
            rid = w.retired[idx]
            w.retired[idx] = w.retired[-1]
            w.retired.pop()
            w.live.append(rid)
            ev = {"kind": "spawn", "entity": rid, "class": _pick(rng, CLASSES)}
            ti = emit(ev)
            defects.append({
                "t": ti, "type": "ambiguity", "entity": rid,
                "reason": "reused_retired_id",
            })

        elif r < _M:
            # malformed: grammar-violating but canonical-JSON-valid payload
            sub = rng.below(4)
            eid = _pick(rng, w.live) if w.live else w.next_id
            if sub == 0:
                ev = {"kind": "attr", "entity": eid, "key": _pick(rng, ATTR_KEYS)}
                mkind = "missing_field"       # no "val"
            elif sub == 1:
                ev = {"kind": "attr", "entity": str(eid),
                      "key": _pick(rng, ATTR_KEYS), "val": rng.below(1000)}
                mkind = "wrong_type"          # entity as string
            elif sub == 2:
                ev = {"kind": "glorp", "entity": eid}
                mkind = "unknown_kind"
            else:
                ev = {"kind": "link", "src": eid, "dst": _DANGLING_ID,
                      "rel": _pick(rng, RELS)}
                mkind = "dangling_ref"
            ti = emit(ev)
            defects.append({"t": ti, "type": "malformed", "malformation": mkind})

        else:
            emit(_normal_event(rng, w, t))

    counts = {"contradiction": 0, "near_duplicate": 0, "ambiguity": 0, "malformed": 0}
    for d in defects:
        counts[d["type"]] += 1
    total = len(defects)
    ground_truth = {
        "corpus": "murk",
        "base_grammar": "chronicle",
        "seed": seed,
        "n": n,
        "knobs_permille": dict(KNOBS),
        "counts": {
            "contradiction": counts["contradiction"],
            "near_duplicate": counts["near_duplicate"],
            "ambiguity": counts["ambiguity"],
            "malformed": counts["malformed"],
            "total_defects": total,
            "clean": n - total,
        },
        "defects": defects,
    }
    return events, ground_truth


def generate(seed, n):
    events, _ = generate_full(seed, n)
    return events


def frozen_bytes():
    """The exact byte content of the frozen murk corpus."""
    events, _ = generate_full(SEED, N)
    return canon.encode_jsonl(events)


def ground_truth_bytes():
    """The exact byte content of the frozen murk answer key (trailing newline)."""
    _, gt = generate_full(SEED, N)
    return canon.canon_encode(gt) + b"\n"


def main(argv):
    if "--write" in argv:
        data = frozen_bytes()
        with open(FROZEN_PATH, "wb") as fh:
            fh.write(data)
        gt = ground_truth_bytes()
        with open(GROUND_TRUTH_PATH, "wb") as fh:
            fh.write(gt)
        print(f"wrote {FROZEN_PATH} ({len(data)} bytes, {N} events)")
        print(f"wrote {GROUND_TRUTH_PATH} ({len(gt)} bytes)")
        return 0
    if "--check" in argv:
        ok = (open(FROZEN_PATH, "rb").read() == frozen_bytes()
              and open(GROUND_TRUTH_PATH, "rb").read() == ground_truth_bytes())
        print("byte-match OK" if ok else "BYTE-MATCH MISMATCH")
        return 0 if ok else 1
    print("usage: python3 -m corpora.murk.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

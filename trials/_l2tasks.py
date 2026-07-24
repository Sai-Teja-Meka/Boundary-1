"""trials/_l2tasks.py — the shared Layer-2 cue-task builder (engine-free).

Both the L2 ascension trial and the L2 humility trial score the **same tasks**
(BOUNDARY.md §6): ascension runs them against the full recall engine
(`layer_cap = 2`), humility runs them against the capped read-by-time engine
(`layer_cap = 1`). This module builds those tasks once, deterministically, from
the **chronicle grammar** — nothing here touches an engine, so it is importable
before `core/layers/l2_recall.py` exists (the trials-first discipline of the
ASCEND sequence).

## What a cue task is

A **store** of chronicle-grammar events (spawn / attr / link / move), and a set
of **cue tasks** over it. Each answerable task is a content **probe** — a
partial attr payload `{"entity":E,"key":K,"val":V}` carrying **no `t`** — whose
ground-truth target is the single stored event that matches the whole probe.

## Grammar-controlled distractors (overlap must be *earned*)

The store is built so that, for every answerable target, lexical overlap with
its cue is **earned, not accidental**:

  * the target's `(E,K,V)` fingerprint is **unique** in the store — exactly one
    event satisfies the full probe;
  * yet the store also holds **≥2 same-entity** distractors (share `entity=E`
    and the cross-field `id#E` adjacency atom), **≥2 same-key** distractors
    (share `key=K`), and **≥2 same-val** distractors (share `val=V`).

So no single shared atom isolates the target: a recall that matched on `entity`
alone, or `key` alone, or `val` alone would land on a distractor. Only an engine
that combines the whole probe recovers the target. That is the boundary Layer 1
cannot cross (it has no content→`t` index at all) and Layer 2 must.

## The no-`t`-leak invariant

Chronicle payloads never contain `t`, so a probe built from payload fields never
encodes the target's logical time. This is asserted here and re-asserted in the
trials: README-l1 states L1's query path answers **by exact `t`**, so any cue
that leaked a `t` would let the capped read-by-time engine win by `read(t)`. No
cue may leak `t` — the capped engine must have nothing to go on but content.
"""

from corpora.prng import Xorshift64
from corpora.chronicle.generator import CLASSES, ATTR_KEYS, ATTR_STR_VALS, RELS, LOCS

# Deterministic construction parameters. A few hundred events with a small
# value space give dense, natural distractors while keeping recall scoring (a
# per-cue candidate sweep) fast at trial scale.
SEED = 20260724
N_ENTITIES = 40
N_ATTR = 560
N_LINKMOVE = 60

# Task-selection thresholds (the "earned overlap" guarantees, checked by the
# trials against the built store).
MIN_SAME_ENTITY = 2
MIN_SAME_KEY = 3
MIN_SAME_VAL = 3
N_ANSWERABLE = 150
N_UNANSWERABLE = 30

_CACHE = {}


def _pick(rng, seq):
    return seq[rng.below(len(seq))]


def _build():
    rng = Xorshift64(SEED)
    entities = list(range(1, N_ENTITIES + 1))

    payloads = []          # store, in t order
    # bookkeeping over attr events only
    fp_count = {}          # (E,K,V) -> count
    fp_t = {}              # (E,K,V) -> the (unique) t, valid only where count==1
    per_entity_attrs = {}  # E -> [t, ...]
    per_key = {}           # K -> count
    per_val = {}           # V -> count

    # 1) spawn every entity (class chosen from the grammar vocabulary).
    for eid in entities:
        payloads.append({"kind": "spawn", "entity": eid, "class": _pick(rng, CLASSES)})

    # 2) a dense field of attr events over a small (key, string-val) space, so
    #    every key and every val recur many times (distractor density) while
    #    most (E,K,V) fingerprints stay unique.
    for _ in range(N_ATTR):
        eid = _pick(rng, entities)
        key = _pick(rng, ATTR_KEYS)
        val = _pick(rng, ATTR_STR_VALS)
        t = len(payloads)
        payloads.append({"kind": "attr", "entity": eid, "key": key, "val": val})
        fp = (eid, key, val)
        fp_count[fp] = fp_count.get(fp, 0) + 1
        fp_t[fp] = t
        per_entity_attrs.setdefault(eid, []).append(t)
        per_key[key] = per_key.get(key, 0) + 1
        per_val[val] = per_val.get(val, 0) + 1

    # 3) a little link/move noise (shares id#E adjacency via src/dst, never the
    #    key/val a probe needs) to enrich the graph without adding attr matches.
    for _ in range(N_LINKMOVE):
        if rng.chance(1, 2) and len(entities) >= 2:
            i = rng.below(len(entities))
            j = rng.below(len(entities) - 1)
            if j >= i:
                j += 1
            payloads.append({"kind": "link", "src": entities[i],
                             "dst": entities[j], "rel": _pick(rng, RELS)})
        else:
            payloads.append({"kind": "move", "entity": _pick(rng, entities),
                             "loc": _pick(rng, LOCS)})

    # ---- select answerable targets (unique fingerprint + earned distractors) --
    answerable = []
    for fp in sorted(fp_t, key=lambda f: fp_t[f]):   # deterministic, t order
        eid, key, val = fp
        if fp_count[fp] != 1:
            continue
        if len(per_entity_attrs.get(eid, [])) - 1 < MIN_SAME_ENTITY:
            continue
        if per_key[key] < MIN_SAME_KEY or per_val[val] < MIN_SAME_VAL:
            continue
        t = fp_t[fp]
        answerable.append({
            "cue": {"entity": eid, "key": key, "val": val},
            "target_t": t,
            "target_event": {"payload": payloads[t], "t": t},
        })
        if len(answerable) >= N_ANSWERABLE:
            break

    # ---- select unanswerable cues (absent fingerprint, tempting partials) -----
    # (E,K,V) that never co-occur, though E exists and K, V each appear
    # elsewhere: partial matches abound, a full match does not exist, so the
    # only correct behavior is to abstain.
    unanswerable = []
    for eid in entities:
        for key in ATTR_KEYS:
            for val in ATTR_STR_VALS:
                fp = (eid, key, val)
                if fp in fp_count:
                    continue
                if per_key.get(key, 0) < MIN_SAME_KEY or per_val.get(val, 0) < MIN_SAME_VAL:
                    continue
                if len(per_entity_attrs.get(eid, [])) < 1:
                    continue
                unanswerable.append({"cue": {"entity": eid, "key": key, "val": val}})
                break
        if len(unanswerable) >= N_UNANSWERABLE:
            break

    return {
        "payloads": payloads,
        "answerable": answerable,
        "unanswerable": unanswerable,
    }


def tasks():
    """Return the deterministic task bundle (built once, cached)."""
    if "b" not in _CACHE:
        _CACHE["b"] = _build()
    return _CACHE["b"]


def store_payloads():
    return list(tasks()["payloads"])


def answerable_tasks():
    return list(tasks()["answerable"])


def unanswerable_tasks():
    return list(tasks()["unanswerable"])


def cue_has_no_t(cue):
    """A probe must never carry `t` (the no-leak invariant)."""
    return isinstance(cue, dict) and "t" not in cue


# ---- strain support: irrelevant high-atom-count decoys ---------------------

DECOY_ENTITY_BASE = 100000


def decoy_payloads(count, cue):
    """`count` high-atom-count events sharing **no atom** with `cue`.

    Entities live in a disjoint high id range, and keys/vals are novel strings,
    so no decoy touches any of the cue's atoms (`entity=`, `id#`, `key=`,
    `val=`). Each decoy also carries extra fields, making it "heavy" — a
    store-relative or length-sensitive scorer would let these perturb a fixed
    cue's ranking; a per-item scorer must not (the GA decoy-invariance strain).
    """
    ce = cue.get("entity")
    out = []
    for i in range(count):
        eid = DECOY_ENTITY_BASE + i
        if eid == ce:
            eid += 1
        out.append({
            "kind": "attr",
            "entity": eid,
            "key": "decoy_key_%d" % i,
            "val": "decoy_val_%d" % i,
            "noise_a": "decoy_noise_a_%d" % i,
            "noise_b": "decoy_noise_b_%d" % i,
            "noise_c": i,
        })
    return out

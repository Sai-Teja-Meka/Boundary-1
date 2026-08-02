"""corpora/l6batteryb/generator.py — battery-b: the forcing region.

The Layer-6 Stage-A **round 2** artifact. Round 1 froze `corpora/l6battery`, a
query set over the frozen murk corpus, and measured its own limit:

> *"On murk, evidence that ranks also resolves … So this battery's 158 errors are
> the errors of the DECLARED latest-wins reading, and its guarantee is relative
> to that reading."*  (`corpora/l6battery/README.md §4`)

That is the defect this artifact exists to remove. `§3.4` leaves `AUROC`
undefined at `n_neg = 0`, so a gate citing it can only bind on an artifact where
`n_neg > 0` is a **theorem** — true of every committing policy — and not a fact
about which reader a session happened to declare. Round 1's artifact could not
supply that, for a reason it measured rather than argued: `§8.7` injects every
murk defect by *visible construction*, so a stream-only rule recovers each family
exactly, and a reader that used the evidence to ANSWER rather than to HEDGE would
drive `n_neg` to 0 and take `AUROC` with it.

battery-b supplies it, and it supplies it by **withholding the resolving signal
at generation**.

## The forcing region

`PAIRS = 100` **mirror pairs**, 200 forcing queries. For pair `p`:

* two entities `e0 = 500000 + 2p` and `e1 = e0 + 1`, spawned at adjacent logical
  times with the **same** class;
* each receives exactly **two** `origin` assertions carrying the **same ordered
  value pair** `(x_p, y_p)`, `x_p != y_p`, emitted at adjacent logical times so
  the two members' assertions share one gap schedule;
* **nothing else ever touches either entity.** Region ids are allocated outside
  the base world, so no link, move or retire reaches them. Each member's ENTIRE
  event history is `[spawn, attr origin x, attr origin y]`;
* a **withheld coin** `b_p` decides which member's FIRST assertion is the true
  `origin` and which member's LAST one is:

  ```
  b_p = 0  ->  true(e0) = x_p (its first)   true(e1) = y_p (its last)
  b_p = 1  ->  true(e0) = y_p (its last)    true(e1) = x_p (its first)
  ```

  The coin is **balanced**: exactly `PAIRS//2` pairs each way, shuffled from the
  same PRNG *after* the stream is complete.

`origin` is asserted by NOTHING ELSE in this corpus — the clean base never emits
it — so every `origin` chain in the frozen stream is a region chain and the
region is perfectly *identifiable*. What is not recoverable is *which of the two
assertions is true*, which is the whole point: an honest engine must be able to
SEE the tie in order to price it at 500, and must be unable to BREAK it.

## The tie, and why it is a theorem

**Theorem 1 (the tie).** The two members of a pair are observationally
identical: their complete event histories are equal as sequences once the entity
id is blanked, and their logical times differ by exactly `+1` at every position.
So any reader whose answer depends on anything but the raw entity id or the
absolute `t` returns the SAME value for both — and since one member's truth is
its first assertion and the other's is its last, it is wrong on **exactly one**.
Summed over the region: **exactly `PAIRS` errors, for every such policy, under
either coin.**

**Theorem 2 (the withholding).** The frozen stream is **byte-identical** under
the coin and its complement, while the answer key differs on every one of the
200 forcing queries. `generate_full(seed, complement=True)` regenerates it and
`trials/ops/l6/t_l6batteryb.py` asserts it. So the stream carries **zero** bits
about the coin: a policy that resolves the region has read the answer key, and
the answer key is class **O** by definition. The residual freedom Theorem 1
leaves — the entity id and the absolute `t` — is closed by the BALANCE of the
coin: a rule keyed on id parity or on emission order gets both members of a pair
right on half the pairs and both wrong on the other half, which is `PAIRS`
errors again.

The consequence is the one round 1 could not reach: `n_neg >= 100 > 0` holds for
**first-wins, last-wins, and every other policy definable from the stream**, so
`AUROC` is defined by theorem rather than by a declared reading.

## The band, redone

The region size `r = 200` and the answerable core `A = 2200` are forced by three
ratified clauses pulling against each other. With `w` the wrong share and `a` the
abstained share of the answerable core, `§3.0` gives `F = 1000 - 1000w - 900a`:

| requirement | arithmetic | gives |
|---|---|---|
| the honest committer clears `F >= 950` | `w = (r/2)/A <= 50` permille | `A >= 10r` |
| blanket abstention on the region BREAKS `F >= 950` | `900(r/A) > 50` | `A < 18r` |
| `Brier <= 40` beats the base-rate constant | `w(1-w) > 40/1000` | `A < (25 + 5*sqrt(21))/4 * r ~ 11.978r` |

`A = 11r = 2200` sits inside all three with margin on both sides, so the
composition is `K0 : K2 : K3 : K4 = 1 : 7 : 3 : 1` of `r`.

## The four classes

| class | n | query | answer key | in `§3.4`'s denominator |
|---|---|---|---|---|
| **K0** forcing | 200 | `current(e, "origin")` over the whole region, unsampled | the WITHHELD-coin value | **yes** |
| **K2** current-value | 1 400 | `current(e, k)`, non-`origin`, non-region | the value at the pair's greatest `t` | **yes** |
| **K3** as-of | 600 | `asof(e, k, t)` at a NON-TERMINAL assertion | the value in force at that `t` | **yes** |
| **K4** absence probe | 200 | `current(e, k)` for a pair never asserted | **unanswerable** — abstention is the only correct behaviour | **no** |

The base stream is **clean** — no near-duplicate knob, no ambiguity knob, no
malformed knob — so every non-region query is answered correctly by the ordinary
latest-wins reading and **all of this artifact's error mass is the forcing
region, by construction**. That is what makes `n_neg` exactly `PAIRS`.

## One artifact, one byte-match

The substrate, the answer key and the query set are ONE frozen canonical JSON
object rather than three files. The reason is the theorem: the guarantee is a
JOINT property of the three, and three separately byte-matched files could be
paired across generations and lose it while every individual check stayed green.
It also needs no change to `§8.3`'s protocol (`FROZEN_PATH` + `frozen_bytes()`),
which `corpora/l6battery` already established for a non-JSONL member.

Randomness comes solely from `corpora/prng.py`; output is canonical JSON with a
trailing newline. Same `seed` -> byte-identical (§8.3).
"""

import json
import os
import sys

from corpora import canon
from corpora.prng import Xorshift64
from corpora.chronicle.generator import (
    CLASSES, ATTR_KEYS, ATTR_STR_VALS, RELS, LOCS,
)

SEED = 9009

# ---- the declared shape ----------------------------------------------------

N_STREAM = 12000                 # events in the substrate
PAIRS = 100                      # mirror pairs in the forcing region
REGION_QUERIES = 2 * PAIRS       # r — the forcing class, unsampled

K2_MULTIPLE = 7                  # of r
K3_MULTIPLE = 3
K4_MULTIPLE = 1

REGION_ID_BASE = 500000          # region ids live outside the base world
REGION_START = 1000              # first region event position
REGION_STRIDE = 100              # one pair per stride; blocks never overlap
REGION_GAP1 = (5, 25)            # spawn -> first assertion
REGION_GAP2 = (10, 60)           # first assertion -> second assertion

SET_ONCE_KEYS = ("origin",)      # asserted by the region and by nothing else

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "l6batteryb.s9009.e12000.q2400.json")


def _pick(rng, seq):
    return seq[rng.below(len(seq))]


def _value(rng):
    """One attribute value in the chronicle vocabulary: an int or a string."""
    if rng.chance(1, 2):
        return rng.below(1000)
    return _pick(rng, ATTR_STR_VALS)


# ---- the assertion reading (the Layer-4 facet map, restated engine-free) ----
#
# Identical to `trials/_l4tasks.facet` by construction; `trials/ops/l6/
# t_l6batteryb.py` asserts the two agree event by event on all 12 000 payloads,
# because a divergence here would move an ANSWER KEY and not merely a query's
# availability.

LIFECYCLE_CLASS = "class"
LIFECYCLE_LOC = "loc"
LIFECYCLE_LIVE = "live"


def facet(payload):
    """Read one payload as an `(entity, key, value)` assertion, or None."""
    kind = payload.get("kind")
    entity = payload.get("entity")
    if kind == "attr":
        if isinstance(entity, int) and not isinstance(entity, bool) \
                and isinstance(payload.get("key"), str) and "val" in payload:
            return (entity, payload["key"], payload["val"])
        return None
    if kind == "move" and isinstance(entity, int) and not isinstance(entity, bool):
        return (entity, LIFECYCLE_LOC, payload["loc"])
    if kind == "spawn" and isinstance(entity, int) and not isinstance(entity, bool):
        return (entity, LIFECYCLE_CLASS, payload["class"])
    if kind == "retire" and isinstance(entity, int) and not isinstance(entity, bool):
        return (entity, LIFECYCLE_LIVE, 0)
    if kind == "link":
        src, dst = payload.get("src"), payload.get("dst")
        if isinstance(src, int) and not isinstance(src, bool) \
                and isinstance(dst, int) and not isinstance(dst, bool) \
                and isinstance(payload.get("rel"), str):
            return (src, payload["rel"], dst)
        return None
    return None


def chains_of(payloads):
    """`(entity, key) -> [(t, value), ...]` in ingestion order."""
    chains = {}
    order = []
    for t, payload in enumerate(payloads):
        f = facet(payload)
        if f is None:
            continue
        pair = (f[0], f[1])
        if pair not in chains:
            chains[pair] = []
            order.append(pair)
        chains[pair].append((t, f[2]))
    return chains, order


# ---- the clean base --------------------------------------------------------


class _World:
    """The base world. Region ids never enter it, so the base never touches them."""

    def __init__(self):
        self.live = []
        self.next_id = 1


def _base_event(rng, w):
    """One clean chronicle-style event. NEVER asserts a set-once key."""
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
        # ATTR_KEYS is the chronicle vocabulary and carries no set-once key, so
        # this is a structural guarantee and not a filter that could be relaxed.
        return {"kind": "attr", "entity": eid, "key": _pick(rng, ATTR_KEYS),
                "val": _value(rng)}

    if action == "link":
        i = rng.below(len(w.live))
        j = rng.below(len(w.live) - 1)
        if j >= i:
            j += 1
        return {"kind": "link", "src": w.live[i], "dst": w.live[j],
                "rel": _pick(rng, RELS)}

    if action == "move":
        eid = _pick(rng, w.live)
        return {"kind": "move", "entity": eid, "loc": _pick(rng, LOCS)}

    idx = rng.below(len(w.live))
    eid = w.live[idx]
    w.live[idx] = w.live[-1]
    w.live.pop()
    return {"kind": "retire", "entity": eid}


# ---- the region layout, drawn with NO reference to the coin ----------------


def _region_layout(rng):
    """The mirror pairs, as content and positions. The coin is not drawn here."""
    region = []
    for p in range(PAIRS):
        e0 = REGION_ID_BASE + 2 * p
        cls = _pick(rng, CLASSES)
        g1 = rng.randint(*REGION_GAP1)
        g2 = rng.randint(*REGION_GAP2)
        x = _value(rng)
        y = _value(rng)
        while y == x:
            y = _value(rng)
        t_spawn = REGION_START + p * REGION_STRIDE
        region.append({
            "pair": p,
            "e0": e0,
            "e1": e0 + 1,
            "class": cls,
            "x": x,
            "y": y,
            "t_spawn": t_spawn,
            "t_first": t_spawn + g1,
            "t_second": t_spawn + g1 + g2,
        })
    return region


def _placed_events(region):
    """position -> payload, for every region event. Members are adjacent."""
    placed = {}

    def put(pos, payload):
        if pos in placed:
            raise ValueError("region blocks overlap at position %d" % (pos,))
        placed[pos] = payload

    for r in region:
        put(r["t_spawn"], {"kind": "spawn", "entity": r["e0"],
                           "class": r["class"]})
        put(r["t_spawn"] + 1, {"kind": "spawn", "entity": r["e1"],
                               "class": r["class"]})
        put(r["t_first"], {"kind": "attr", "entity": r["e0"],
                           "key": SET_ONCE_KEYS[0], "val": r["x"]})
        put(r["t_first"] + 1, {"kind": "attr", "entity": r["e1"],
                               "key": SET_ONCE_KEYS[0], "val": r["x"]})
        put(r["t_second"], {"kind": "attr", "entity": r["e0"],
                            "key": SET_ONCE_KEYS[0], "val": r["y"]})
        put(r["t_second"] + 1, {"kind": "attr", "entity": r["e1"],
                                "key": SET_ONCE_KEYS[0], "val": r["y"]})
    return placed


def _sample(rng, population, m):
    """A seeded sample of `m` distinct items, returned in the population's order.

    Partial Fisher-Yates over an index list: exactly uniform (the PRNG's `below`
    rejects the incomplete top band), integer-only.
    """
    if m > len(population):
        raise ValueError("sample larger than population (%d > %d)"
                         % (m, len(population)))
    idx = list(range(len(population)))
    taken = []
    for k in range(m):
        j = k + rng.below(len(idx) - k)
        idx[k], idx[j] = idx[j], idx[k]
        taken.append(idx[k])
    return [population[i] for i in sorted(taken)]


# ---- the whole artifact ----------------------------------------------------


def generate_full(seed, complement=False):
    """Return the battery-b artifact dict, deterministically from `seed`.

    `complement` flips every coin bit and NOTHING ELSE. The stream is built
    before the coin is drawn and never reads it, so the returned `stream` is
    byte-identical under both — which is Theorem 2, and
    `trials/ops/l6/t_l6batteryb.py` asserts it rather than trusting this
    docstring.
    """
    rng = Xorshift64(seed)

    # 1. the substrate. No coin exists yet.
    region = _region_layout(rng)
    placed = _placed_events(region)
    w = _World()
    stream = []
    for t in range(N_STREAM):
        stream.append(placed[t] if t in placed else _base_event(rng, w))

    chains, order = chains_of(stream)
    region_ids = {r["e0"] for r in region} | {r["e1"] for r in region}

    # 2. the coin — balanced, shuffled, drawn AFTER the stream is complete.
    coin = [0] * (PAIRS // 2) + [1] * (PAIRS - PAIRS // 2)
    rng.shuffle(coin)
    if complement:
        coin = [1 - b for b in coin]

    truth = {}          # entity -> the true `origin` value
    defects = []
    for r, b in zip(region, coin):
        r = dict(r)
        true0 = r["x"] if b == 0 else r["y"]
        true1 = r["y"] if b == 0 else r["x"]
        truth[r["e0"]] = true0
        truth[r["e1"]] = true1
        for eid, true_v, t_true, t_false in (
                (r["e0"], true0,
                 r["t_first"] if b == 0 else r["t_second"],
                 r["t_second"] if b == 0 else r["t_first"]),
                (r["e1"], true1,
                 r["t_second"] + 1 if b == 0 else r["t_first"] + 1,
                 r["t_first"] + 1 if b == 0 else r["t_second"] + 1)):
            defects.append({
                "t": t_false,
                "type": "forced_contradiction",
                "entity": eid,
                "key": SET_ONCE_KEYS[0],
                "pair": r["pair"],
                "refs": sorted([t_true, t_false]),
                "t_true": t_true,
                "values": [true_v, r["y"] if true_v == r["x"] else r["x"]],
            })

    # 3. the plain classes, over pairs the region does not touch.
    plain = [p for p in order
             if p[1] not in SET_ONCE_KEYS and p[0] not in region_ids]
    nonterminal = [(p, i) for p in plain for i in range(len(chains[p]) - 1)]
    k2 = _sample(rng, plain, K2_MULTIPLE * REGION_QUERIES)
    k3 = _sample(rng, nonterminal, K3_MULTIPLE * REGION_QUERIES)

    entities = sorted({p[0] for p in plain})
    keys = sorted({p[1] for p in plain})
    probes = []
    seen = set()
    while len(probes) < K4_MULTIPLE * REGION_QUERIES:
        entity = entities[rng.below(len(entities))]
        key = keys[rng.below(len(keys))]
        pair = (entity, key)
        if pair in chains or pair in seen:
            continue
        seen.add(pair)
        probes.append(pair)

    # 4. the queries.
    queries = []

    def add(cls, q, answerable, value):
        queries.append({"qid": len(queries), "class": cls, "q": q,
                        "answerable": answerable, "value": value})

    for eid in sorted(region_ids):
        add("K0", {"op": "current", "entity": eid, "key": SET_ONCE_KEYS[0]},
            True, truth[eid])
    for (entity, key) in k2:
        add("K2", {"op": "current", "entity": entity, "key": key}, True,
            chains[(entity, key)][-1][1])
    for (pair, i) in k3:
        t, value = chains[pair][i]
        add("K3", {"op": "asof", "entity": pair[0], "key": pair[1], "t": t},
            True, value)
    for (entity, key) in sorted(probes):
        add("K4", {"op": "current", "entity": entity, "key": key}, False, None)

    counts = {}
    for record in queries:
        counts[record["class"]] = counts.get(record["class"], 0) + 1
    counts["answerable"] = sum(1 for r in queries if r["answerable"])
    counts["unanswerable"] = sum(1 for r in queries if not r["answerable"])
    counts["total"] = len(queries)

    return {
        "battery": "l6batteryb",
        "seed": seed,
        "stream_events": N_STREAM,
        "set_once_keys": list(SET_ONCE_KEYS),
        "multiples": {"K2": K2_MULTIPLE, "K3": K3_MULTIPLE, "K4": K4_MULTIPLE},
        "region": {
            "pairs": PAIRS,
            "queries": REGION_QUERIES,
            "id_base": REGION_ID_BASE,
            "start": REGION_START,
            "stride": REGION_STRIDE,
        },
        "counts": counts,
        "stream": stream,
        "ground_truth": {
            "corpus": "l6batteryb",
            "base_grammar": "chronicle",
            "seed": seed,
            "n": N_STREAM,
            "counts": {"forced_contradiction": len(defects),
                       "pairs": PAIRS,
                       "clean": N_STREAM - len(defects)},
            "coin": list(coin),
            "pairs": [
                {"pair": r["pair"], "e0": r["e0"], "e1": r["e1"],
                 "class": r["class"], "values": [r["x"], r["y"]],
                 "t_spawn": r["t_spawn"], "t_first": r["t_first"],
                 "t_second": r["t_second"],
                 "first_true_member": 0 if b == 0 else 1,
                 "true": [truth[r["e0"]], truth[r["e1"]]]}
                for r, b in zip(region, coin)],
            "defects": defects,
        },
        "queries": queries,
    }


def generate(seed):
    return generate_full(seed)


def frozen_bytes():
    """The exact byte content of the frozen artifact (trailing newline)."""
    return canon.canon_encode(generate_full(SEED)) + b"\n"


def load():
    """The frozen artifact, read from disk."""
    with open(FROZEN_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv):
    if "--write" in argv:
        data = frozen_bytes()
        with open(FROZEN_PATH, "wb") as fh:
            fh.write(data)
        artifact = generate_full(SEED)
        print(f"wrote {FROZEN_PATH} ({len(data)} bytes)")
        print(f"  stream: {len(artifact['stream'])} events")
        print(f"  counts: {artifact['counts']}")
        return 0
    if "--check" in argv:
        with open(FROZEN_PATH, "rb") as fh:
            ok = fh.read() == frozen_bytes()
        print("byte-match OK" if ok else "BYTE-MATCH MISMATCH")
        return 0 if ok else 1
    print("usage: python3 -m corpora.l6batteryb.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

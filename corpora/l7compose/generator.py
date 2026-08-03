"""corpora/l7compose/generator.py — the Layer-7 generation artifact.

Layer-7 Stage A. `§5 L7` gates `validity = 1000`, `novelty = 1000`,
`tagging = 1000`, self-pollution `promotion = 0` three deep, `F >= 950`,
`B = 1000` and `ECE <= 40`. `novelty` is *"provably never-stored"*, so a gate
citing it can only bind on an artifact that carries queries **no retrieval can
answer**.

No frozen corpus does. `trials/ascension/l7/ATTAINABILITY.md §2` measures it
rather than asserting it: every frozen artifact in `corpora/registry.py` was
built so that its answer key names content the stream asserts (`§8.7`'s
*dirt is always paired with the answer key*), so on all of them the
generation-required class is **empty**, `tagging`'s denominator is empty, and by
the very holding this Stage A drafts an empty denominator is `n/a` and `n/a`
does not certify. That is the **fifth substrate kill**, and this artifact is
what it forces.

## The shape: a closed compositional grammar with a withheld item

A **compound** is `formed` from exactly two components by two `part` assertions.
A component carries a `hue` and a `mass`. The declared composition rule
(`COMPOSITION_FORM`, below, and `trials/_l7tasks.compose`) determines the
compound's `profile` item from its two components' material:

```
profile(c) = {"kind":"profile", "entity":c,
              "grade": GRADES[(HUES.index(h0) + HUES.index(h1)) % len(GRADES)],
              "hue":   h0,
              "mass":  m0 + m1}
```

where `(h_i, m_i)` is component `i`'s `(hue, mass)` — read off its assertions
when it is a plain component, and off ITS OWN profile when it is itself a
compound, which is what makes the rule closed under composition and gives the
self-pollution ladder its rungs.

For some compounds the generator **emits** that profile as an ordinary event.
For others it **withholds** it. The rule is in the grammar either way, so a
composer answers both; only a retriever answers the first.

## The forcing region: 100 MIRROR PAIRS, and what the theorem is

`PAIRS = 100` pairs of compounds `(e0, e1 = e0 + 1)`, whose two members are
**twins**: one material is drawn per slot and instantiated twice, so the two
members' event blocks are equal as sequences once the entity ids are blanked and
their positions differ by one constant offset — and they therefore compose to
the *same item but for its `entity` field*. **The value is never the signal.** A
**balanced coin** decides which member's profile is emitted (class **O**,
retrievable) and which member's is withheld (class **G**, generation-required).
Both cues are asked with the SAME op and the SAME shape:

```
{"op":"generate","cue":{"kind":"profile","entity":<e>}}
```

**Theorem 1 (the class is not readable from the query).** Blank the entity id
and the two members' queries are the *same object*. So any policy whose lineage
decision is a function of the query alone answers both identically and mislabels
**exactly one of every pair — exactly `PAIRS` lineage errors.** The two handles
that leaves — the raw entity id and the emission order, which are the same
handle here because `e1 = e0 + 1` and members are emitted in id order — are
closed by the coin's **balance**: such a rule takes both members of a pair or
neither and is right on exactly half the pairs, which is `PAIRS` errors again.
Exhibited against a bench of six labellers in `trials/ops/l7/t_l7compose.py`,
every one measuring exactly `PAIRS`.

This is the Layer-7 analogue of `corpora/l6batteryb`'s tie and it is a
**different** theorem, deliberately. Battery-b withheld the resolving signal
from the *stream*, so no reader could be right. Nothing is withheld from a
correct composer here: the composition rule is public and the composed value is
the same for both members of a pair. What is withheld is the *item*, from the
*retrieval channel* — so the value is never the signal, and the only way to get
the lineage right is to consult what one holds. That is the property
`trials/ascension/l7/PRE-READ.md §6.3` predicted a first artifact would fail:
*"a composition that is forced may also be trivially taggable."*

**Theorem 2 (novelty).** For every generation-required compound the composed
profile's canonical bytes (`§2.4`) appear **nowhere** in the frozen stream —
asserted by exhaustive comparison against all 12 000 payloads, and structurally
guaranteed besides, since a `profile` payload carries its own `entity` and no
`profile` payload for a G compound is emitted at all. This is `R7` clause 3(b)'s
pattern: the guarantee is on the **artifact**, so it holds against an arbitrary
engine rather than against the one this session had in mind.

## The self-pollution ladder, three deep

`LADDER = 30` chains. Chain `i` takes one of the region's own **G** compounds as
its depth-1 root, forms a depth-2 compound from it and a fresh component, and a
depth-3 compound from that and another fresh component. Every one of those
profiles is withheld, so:

* `lineage_depth = 1` — composable from asserted material (100 compounds);
* `lineage_depth = 2` — composable only from a depth-1 **generated** item (30);
* `lineage_depth = 3` — composable only from a depth-2 generated item (30).

`lineage_depth` is **decidable from the frozen bytes**: a compound whose profile
is in the stream is depth 0, and otherwise its depth is one more than the
greatest depth among its compound components. `trials/ops/l7/t_l7compose.py`
recomputes it from the stream alone and requires it to equal the declared table,
so `§6`'s mandatory self-pollution strain gets its rungs from the artifact and
not from an engine's own account of itself.

Re-ingestion is the caller's act and the items are ordinary payloads in the same
grammar, so the promotion failure `§5 L7` forbids is REACHABLE by construction:
append a generated profile and the stream now stores it, and a policy without a
lineage record will call it observed fact. That is measured, not argued —
`_l7tasks.promotion_ladder` scores it at each rung for the witness (0, 0, 0) and
for a ledger-blind reference policy (100, 130, 160).

## The incomposable class: generation-shaped, and unanswerable

`INCOMPOSABLE = 100` compounds one of whose components never has a `mass`
asserted. Their profiles are withheld too, and the declared rule does not
determine them, so **abstention is the only correct behaviour** — a
generation-shaped query on which composing anything at all is a fabrication
(`§3.0` scores it 0). They are outside the answerable core and outside `§3.4`'s
denominator (`R7` clause 2).

## The band, one-sided

`ATTAINABILITY.md §4` records it. With `g` the generation-required share of the
answerable core, `§3.0` and `§5 L7`'s own `F >= 950` give

```
blanket abstention on the generation class scores F = 1000 - 900g,
so it BREAKS F >= 950 iff  g > 50/900 = 1/18 = 55.5 permille.
```

This artifact sits at `g = 160/2000 = 80` permille. `R7` clause 3(c)'s LOWER
bound (`A >= 10r`) is **not** inherited and the reason is Theorem 1's difference:
that bound came from a *forced* error under a withheld coin, and nothing is
withheld from a correct generator here, so the Layer-7 window is one-sided.

## The classes

| class | n | query | answerable | declared |
|---|---|---|---|---|
| **KG1** | 100 | `generate` profile, region G member | yes | **G**, depth 1 |
| **KO**  | 100 | `generate` profile, region O member | yes | **O** |
| **KG2** | 30 | `generate` profile, ladder depth 2 | yes | **G**, depth 2 |
| **KG3** | 30 | `generate` profile, ladder depth 3 | yes | **G**, depth 3 |
| **KR**  | 1 740 | `current(entity,key)`, ordinary assertion | yes | **O** |
| **KU1** | 100 | `generate` profile, incomposable compound | **no** | U |
| **KU2** | 100 | `current(entity,key)`, never asserted | **no** | U |

`A = 2 000` answerable, `N = 2 200` total, `|G| = 160`, `|O| = 1 840`.

## One artifact, one byte-match

Substrate, declared class table and query set are ONE canonical JSON object, for
`corpora/l6batteryb`'s reason: the guarantees are a JOINT property of the three,
and three separately byte-matched files could be paired across generations and
lose it while every individual check stayed green.

Randomness comes solely from `corpora/prng.py`; output is canonical JSON with a
trailing newline. Same `seed` -> byte-identical (`§8.3`).
"""

import json
import os
import sys

from corpora import canon
from corpora.prng import Xorshift64
from corpora.chronicle.generator import (
    CLASSES, ATTR_KEYS, ATTR_STR_VALS, RELS, LOCS,
)

SEED = 10010

# ---- the declared shape ----------------------------------------------------

N_STREAM = 12000                 # events in the substrate

PAIRS = 100                      # mirror pairs — the forcing region
LADDER = 30                      # self-pollution chains, rooted in region G's
INCOMPOSABLE = 100               # generation-shaped unanswerable probes
KR_QUERIES = 1740                # ordinary retrieval class
KU2_QUERIES = 100                # ordinary absence probes

COMPOUND_CLASS = "compound"      # outside chronicle's CLASSES, deliberately
HUE_KEY = "hue"                  # outside chronicle's ATTR_KEYS, deliberately
MASS_KEY = "mass"

HUES = ("amber", "cobalt", "jade", "ochre", "rose", "slate", "teal", "umber")
GRADES = ("crude", "fine", "keen", "pure", "rare", "vivid")
MASS_RANGE = (1, 99)

REGION_ID_BASE = 700000          # compounds and their components live outside
COMPONENT_ID_BASE = 800000       # the base world entirely

REGION_START = 400               # first region event position
REGION_STRIDE = 40               # one mirror pair per stride; blocks never overlap
LADDER_START = 4600
LADDER_STRIDE = 40
INCOMP_START = 8200
INCOMP_STRIDE = 30

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "l7compose.s10010.e12000.q2200.json")


# ---- the declared readings -------------------------------------------------
#
# Two of them, in the shape `ASSERTION_FORMS` (L4), `INTENTION_FORM` (L5) and
# `SET_ONCE_KEYS` (L6) already have: a session declares them, a trial checks the
# declaration against the frozen bytes, and no engine infers them.

PROFILE_FORM = ("kind", "entity", "grade", "hue", "mass")

COMPOSITION_FORM = """A compound is an entity of class `compound` carrying
exactly two `part` assertions with slots 0 and 1. Its `profile` item is
determined by its two components' `(hue, mass)`: the hue of slot 0, the sum of
the masses, and the grade at index `(HUES.index(h0) + HUES.index(h1)) %
len(GRADES)`. A component's `(hue, mass)` is its latest asserted pair; a
compound component's is its own profile's. A compound whose components' material
is not determined has NO profile and the only correct behaviour on it is
abstention."""


def profile_form_ok(item):
    """Grammar validity of a composed item — `§5 L7`'s `validity = 1000`."""
    if not isinstance(item, dict):
        return False
    if tuple(sorted(item.keys())) != tuple(sorted(PROFILE_FORM)):
        return False
    if item["kind"] != "profile":
        return False
    entity = item["entity"]
    if not isinstance(entity, int) or isinstance(entity, bool) or entity < 0:
        return False
    if item["grade"] not in GRADES:
        return False
    if item["hue"] not in HUES:
        return False
    mass = item["mass"]
    if not isinstance(mass, int) or isinstance(mass, bool) or mass < 0:
        return False
    return True


def compose(h0, m0, h1, m1, entity):
    """The declared composition rule. Integer-only; no float ever appears."""
    grade = GRADES[(HUES.index(h0) + HUES.index(h1)) % len(GRADES)]
    return {"kind": "profile", "entity": entity, "grade": grade,
            "hue": h0, "mass": m0 + m1}


# ---- helpers ---------------------------------------------------------------

def _pick(rng, seq):
    return seq[rng.below(len(seq))]


def _value(rng):
    """One ordinary attribute value in the chronicle vocabulary."""
    if rng.chance(1, 2):
        return rng.below(1000)
    return _pick(rng, ATTR_STR_VALS)


class _World:
    """The base world. Region ids never enter it, so the base never touches them."""

    def __init__(self):
        self.live = []
        self.next_id = 1


def _base_event(rng, w):
    """One clean chronicle-style event. Never a `part`, never a `profile`."""
    if not w.live:
        action = "spawn"
    else:
        bucket = rng.below(100)
        if bucket < 20:
            action = "spawn"
        elif bucket < 62:
            action = "attr"
        elif bucket < 76:
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
        # ATTR_KEYS is the chronicle vocabulary and carries neither `hue` nor
        # `mass`, so a base event can never look like component material. That is
        # structural, not a filter that could be relaxed.
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


# ---- the composition region, drawn with NO reference to the coin -----------

class _Ids:
    def __init__(self):
        self.compound = REGION_ID_BASE
        self.component = COMPONENT_ID_BASE

    def next_compound(self):
        eid = self.compound
        self.compound += 1
        return eid

    def next_component(self):
        eid = self.component
        self.component += 1
        return eid


def _component_spec(rng, with_mass=True):
    """The MATERIAL of one component — drawn once, and shared by twins."""
    return {"hue": _pick(rng, HUES),
            "mass": rng.randint(*MASS_RANGE) if with_mass else None}


def _component(rng, ids, with_mass=True):
    spec = _component_spec(rng, with_mass)
    return {"entity": ids.next_component(), **spec}


def _instantiate(ids, spec):
    """A fresh component id carrying an existing spec — one half of a twin."""
    return {"entity": ids.next_component(), **spec}


def _component_events(comp):
    events = [{"kind": "spawn", "entity": comp["entity"], "class": "part"},
              {"kind": "attr", "entity": comp["entity"], "key": HUE_KEY,
               "val": comp["hue"]}]
    if comp["mass"] is not None:
        events.append({"kind": "attr", "entity": comp["entity"],
                       "key": MASS_KEY, "val": comp["mass"]})
    return events


def _compound_events(cid, part0, part1):
    return [{"kind": "spawn", "entity": cid, "class": COMPOUND_CLASS},
            {"kind": "part", "entity": cid, "slot": 0, "of": part0},
            {"kind": "part", "entity": cid, "slot": 1, "of": part1}]


def _layout(rng):
    """The whole composition region as content and positions, coin not drawn."""
    ids = _Ids()

    # --- the mirror pairs -------------------------------------------------
    pairs = []
    for p in range(PAIRS):
        e0 = ids.next_compound()
        e1 = ids.next_compound()
        # ONE material per slot, instantiated TWICE. The two members are
        # observationally identical once the entity ids are blanked, so they
        # compose to the SAME item but for its `entity` field — which is what
        # makes the value useless as a lineage signal, and Theorem 1 sharp.
        slot0 = _component_spec(rng)
        slot1 = _component_spec(rng)
        members = [(_instantiate(ids, slot0), _instantiate(ids, slot1)),
                   (_instantiate(ids, slot0), _instantiate(ids, slot1))]
        pairs.append({"pair": p, "e0": e0, "e1": e1,
                      "parts0": members[0], "parts1": members[1],
                      "t_block": REGION_START + p * REGION_STRIDE})

    # --- the ladder, rooted in region G members (chosen after the coin) ----
    ladder = []
    for i in range(LADDER):
        w2 = _component(rng, ids)
        w3 = _component(rng, ids)
        d2 = ids.next_compound()
        d3 = ids.next_compound()
        ladder.append({"chain": i, "d2": d2, "d3": d3, "w2": w2, "w3": w3,
                       "t_block": LADDER_START + i * LADDER_STRIDE})

    # --- the incomposable compounds ---------------------------------------
    incomposable = []
    for i in range(INCOMPOSABLE):
        a = _component(rng, ids)
        b = _component(rng, ids, with_mass=False)
        cid = ids.next_compound()
        incomposable.append({"index": i, "entity": cid, "a": a, "b": b,
                             "t_block": INCOMP_START + i * INCOMP_STRIDE})
    return pairs, ladder, incomposable


def _place(placed, pos, payload):
    if pos in placed:
        raise ValueError("region blocks overlap at position %d" % (pos,))
    placed[pos] = payload


def _attrs_of_component(comp):
    return (comp["hue"], comp["mass"])


# ---- the whole artifact ----------------------------------------------------

def generate_full(seed, complement=False):
    """Return the l7compose artifact dict, deterministically from `seed`.

    `complement` flips every coin bit and NOTHING ELSE — which member of each
    mirror pair has its profile emitted, and which has it withheld. Unlike
    `corpora/l6batteryb`, the stream is NOT byte-identical under the complement
    and is not meant to be: the coin here decides which side of the retrieval
    channel a compound sits on, and that is exactly what the engine must look at
    its own store to discover. What IS invariant is the QUERY SET's shape — the
    same 200 cues in the same order, with only their declared class swapping —
    which is Theorem 1's machine-checked half.
    """
    rng = Xorshift64(seed)

    pairs, ladder, incomposable = _layout(rng)

    # the coin — balanced, shuffled, drawn AFTER the layout is complete.
    coin = [0] * (PAIRS // 2) + [1] * (PAIRS - PAIRS // 2)
    rng.shuffle(coin)
    if complement:
        coin = [1 - b for b in coin]

    placed = {}
    profiles = {}        # entity -> the composed profile item (stored or not)
    stored = set()       # entities whose profile IS emitted into the stream
    parts_of = {}        # entity -> (part0, part1)
    material = {}        # entity -> (hue, mass) for a plain component

    # --- mirror pairs -----------------------------------------------------
    region = []
    for r, b in zip(pairs, coin):
        base = r["t_block"]
        # G member: b == 0 -> e0 is G; b == 1 -> e1 is G.
        g_member = r["e0"] if b == 0 else r["e1"]
        o_member = r["e1"] if b == 0 else r["e0"]
        cursor = base
        for idx, (cid, parts) in enumerate(
                ((r["e0"], r["parts0"]), (r["e1"], r["parts1"]))):
            u, v = parts
            for comp in (u, v):
                material[comp["entity"]] = _attrs_of_component(comp)
                for ev in _component_events(comp):
                    _place(placed, cursor, ev)
                    cursor += 1
            parts_of[cid] = (u["entity"], v["entity"])
            for ev in _compound_events(cid, u["entity"], v["entity"]):
                _place(placed, cursor, ev)
                cursor += 1
            profiles[cid] = compose(u["hue"], u["mass"], v["hue"], v["mass"], cid)
        # the withholding: exactly one member's profile is emitted.
        _place(placed, cursor, profiles[o_member])
        stored.add(o_member)
        cursor += 1
        region.append({"pair": r["pair"], "e0": r["e0"], "e1": r["e1"],
                       "generated": g_member, "observed": o_member,
                       "coin": b, "t_block": base, "t_end": cursor - 1})

    # --- the ladder, rooted in the G members of the first LADDER pairs -----
    chains = []
    for i, l in enumerate(ladder):
        root = region[i]["generated"]
        cursor = l["t_block"]
        for comp in (l["w2"], l["w3"]):
            material[comp["entity"]] = _attrs_of_component(comp)
            for ev in _component_events(comp):
                _place(placed, cursor, ev)
                cursor += 1
        parts_of[l["d2"]] = (root, l["w2"]["entity"])
        for ev in _compound_events(l["d2"], root, l["w2"]["entity"]):
            _place(placed, cursor, ev)
            cursor += 1
        rp = profiles[root]
        profiles[l["d2"]] = compose(rp["hue"], rp["mass"],
                                    l["w2"]["hue"], l["w2"]["mass"], l["d2"])
        parts_of[l["d3"]] = (l["d2"], l["w3"]["entity"])
        for ev in _compound_events(l["d3"], l["d2"], l["w3"]["entity"]):
            _place(placed, cursor, ev)
            cursor += 1
        p2 = profiles[l["d2"]]
        profiles[l["d3"]] = compose(p2["hue"], p2["mass"],
                                    l["w3"]["hue"], l["w3"]["mass"], l["d3"])
        chains.append({"chain": i, "root": root, "d2": l["d2"], "d3": l["d3"],
                       "t_block": l["t_block"], "t_end": cursor - 1})

    # --- the incomposable compounds ---------------------------------------
    incomp = []
    for c in incomposable:
        cursor = c["t_block"]
        material[c["a"]["entity"]] = _attrs_of_component(c["a"])
        material[c["b"]["entity"]] = _attrs_of_component(c["b"])
        for comp in (c["a"], c["b"]):
            for ev in _component_events(comp):
                _place(placed, cursor, ev)
                cursor += 1
        parts_of[c["entity"]] = (c["a"]["entity"], c["b"]["entity"])
        for ev in _compound_events(c["entity"], c["a"]["entity"],
                                   c["b"]["entity"]):
            _place(placed, cursor, ev)
            cursor += 1
        incomp.append({"index": c["index"], "entity": c["entity"],
                       "missing": c["b"]["entity"], "t_block": c["t_block"],
                       "t_end": cursor - 1})

    # --- the base fills every remaining position ---------------------------
    w = _World()
    stream = []
    for t in range(N_STREAM):
        stream.append(placed[t] if t in placed else _base_event(rng, w))

    # --- the declared lineage table ---------------------------------------
    lineage = {}
    for cid in sorted(profiles):
        lineage[cid] = 0 if cid in stored else 1
    for c in chains:
        lineage[c["d2"]] = 2
        lineage[c["d3"]] = 3

    # --- the ordinary retrieval class -------------------------------------
    compound_ids = set(profiles) | {c["entity"] for c in incomp}
    region_entities = compound_ids | set(material)
    base_chains, base_order = chains_of(stream, exclude=region_entities)
    plain = [p for p in base_order]
    kr = _sample(rng, plain, KR_QUERIES)

    entities = sorted({p[0] for p in plain})
    keys = sorted({p[1] for p in plain})
    probes = []
    seen = set()
    while len(probes) < KU2_QUERIES:
        entity = entities[rng.below(len(entities))]
        key = keys[rng.below(len(keys))]
        pair = (entity, key)
        if pair in base_chains or pair in seen:
            continue
        seen.add(pair)
        probes.append(pair)

    # --- the queries -------------------------------------------------------
    queries = []

    def add(cls, declared, q, answerable, value, depth=None):
        record = {"qid": len(queries), "class": cls, "declared": declared,
                  "q": q, "answerable": answerable, "value": value}
        if depth is not None:
            record["depth"] = depth
        queries.append(record)

    def profile_cue(entity):
        return {"op": "generate", "cue": {"kind": "profile", "entity": entity}}

    for r in region:
        add("KG1", "G", profile_cue(r["generated"]), True,
            profiles[r["generated"]], depth=1)
    for r in region:
        add("KO", "O", profile_cue(r["observed"]), True,
            profiles[r["observed"]], depth=0)
    for c in chains:
        add("KG2", "G", profile_cue(c["d2"]), True, profiles[c["d2"]], depth=2)
    for c in chains:
        add("KG3", "G", profile_cue(c["d3"]), True, profiles[c["d3"]], depth=3)
    for (entity, key) in kr:
        add("KR", "O", {"op": "current", "entity": entity, "key": key}, True,
            base_chains[(entity, key)][-1][1])
    for c in incomp:
        add("KU1", "U", profile_cue(c["entity"]), False, None)
    for (entity, key) in sorted(probes):
        add("KU2", "U", {"op": "current", "entity": entity, "key": key}, False,
            None)

    counts = {}
    for record in queries:
        counts[record["class"]] = counts.get(record["class"], 0) + 1
    counts["G"] = sum(1 for r in queries if r["declared"] == "G")
    counts["O"] = sum(1 for r in queries if r["declared"] == "O")
    counts["U"] = sum(1 for r in queries if r["declared"] == "U")
    counts["answerable"] = sum(1 for r in queries if r["answerable"])
    counts["unanswerable"] = sum(1 for r in queries if not r["answerable"])
    counts["total"] = len(queries)

    return {
        "battery": "l7compose",
        "seed": seed,
        "stream_events": N_STREAM,
        "grammar": {
            "compound_class": COMPOUND_CLASS,
            "hue_key": HUE_KEY,
            "mass_key": MASS_KEY,
            "hues": list(HUES),
            "grades": list(GRADES),
            "profile_form": list(PROFILE_FORM),
        },
        "region": {
            "pairs": PAIRS,
            "queries": 2 * PAIRS,
            "ladder": LADDER,
            "incomposable": INCOMPOSABLE,
            "compound_id_base": REGION_ID_BASE,
            "component_id_base": COMPONENT_ID_BASE,
        },
        "counts": counts,
        "stream": stream,
        "declared": {
            "pairs": region,
            "chains": chains,
            "incomposable": incomp,
            "lineage": {str(k): v for k, v in sorted(lineage.items())},
            "parts": {str(k): list(v) for k, v in sorted(parts_of.items())},
            "profiles": {str(k): profiles[k] for k in sorted(profiles)},
            "stored_profiles": sorted(stored),
            "coin": list(coin),
        },
        "queries": queries,
    }


# ---- the assertion reading, restated engine-free ---------------------------
#
# Identical to `trials/_l4tasks.facet`, and `trials/ops/l7/t_l7compose.py`
# asserts the agreement event by event on all 12 000 payloads, because a
# divergence here would move an ANSWER KEY and not merely a query's availability.
#
# `part` and `profile` are **outside** it, deliberately and with a consequence
# worth stating: they are Layer-7 kinds, the frozen Layer-4 facet map does not
# read them, so to every engine below Layer 7 a `part` or a `profile` event is an
# irreducible episode and not an assertion. The composition reading
# (`COMPOSITION_FORM`, implemented by `trials/_l7tasks`) is a SECOND declared
# reading over the raw payloads, in the shape `INTENTION_FORM` was at Layer 5 —
# and, exactly as there, the layer below can hold the event and cannot read it.

LIFECYCLE_CLASS = "class"
LIFECYCLE_LOC = "loc"
LIFECYCLE_LIVE = "live"


def facet(payload):
    """Read one payload as an `(entity, key, value)` assertion, or None."""
    kind = payload.get("kind")
    entity = payload.get("entity")
    plain = isinstance(entity, int) and not isinstance(entity, bool)
    if kind == "attr":
        if plain and isinstance(payload.get("key"), str) and "val" in payload:
            return (entity, payload["key"], payload["val"])
        return None
    if kind == "move" and plain:
        return (entity, LIFECYCLE_LOC, payload["loc"])
    if kind == "spawn" and plain:
        return (entity, LIFECYCLE_CLASS, payload["class"])
    if kind == "retire" and plain:
        return (entity, LIFECYCLE_LIVE, 0)
    if kind == "link":
        src, dst = payload.get("src"), payload.get("dst")
        if isinstance(src, int) and not isinstance(src, bool) \
                and isinstance(dst, int) and not isinstance(dst, bool) \
                and isinstance(payload.get("rel"), str):
            return (src, payload["rel"], dst)
        return None
    return None


def chains_of(payloads, exclude=()):
    """`(entity, key) -> [(t, value), ...]` in ingestion order."""
    built = {}
    order = []
    excluded = set(exclude)
    for t, payload in enumerate(payloads):
        f = facet(payload)
        if f is None or f[0] in excluded:
            continue
        pair = (f[0], f[1])
        if pair not in built:
            built[pair] = []
            order.append(pair)
        built[pair].append((t, f[2]))
    return built, order


def _sample(rng, population, m):
    """A seeded sample of `m` distinct items, in the population's order."""
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
    print("usage: python3 -m corpora.l7compose.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

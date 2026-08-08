"""corpora/l8describe/generator.py — the Layer-8 self-description artifact.

Layer-8 Stage A, under `BOUNDARY-HIGH.md §3` (the substrate doctrine). `§5 L8` is
*"Self-description — introspection answered FROM STATE via the ordinary query
interface"*, and the SPEC's `§3` says what an artifact for it **is**: not one
object but a **triple**, of which this module freezes the first two members and
`trials/_l8derive.py` freezes the third.

  1. a FROZEN EVENT STREAM — an ordinary `§8` corpus, seeded generator, output
     frozen, byte-match law binding unchanged;
  2. a FROZEN QUERY SET WITH ITS DECLARED CLASS TABLE — shipping in the SAME
     canonical JSON object as the stream, for `corpora/l6batteryb`'s reason
     carried forward by the SPEC: the guarantees are a JOINT property of the
     members and three separately byte-matched files could be paired across
     generations while every individual check stayed green;
  3. a FROZEN DERIVATION PROCEDURE — `trials/_l8derive.py`, engine-free committed
     source mapping *(this stream, an engine's ingestion trace, an engine's
     canonical snapshot)* to the expected answer. It is a **declared reading** in
     the shape `ASSERTION_FORMS` (L4), `INTENTION_FORM` (L5), `SET_ONCE_KEYS`
     (L6) and `COMPOSITION_FORM` (L7) already have, with the one difference that
     is the whole layer: those read the CALLER'S PAYLOADS and it reads the
     ENGINE'S SNAPSHOT.

## What this stream is FOR, and why it looks like `l4stream` under pressure

A self-description is a fact about the engine, so the stream's only job is to put
an engine into a state worth describing: chains to fold, a demotable tier, an
irreducible tier the budget must actually cut into, and a **declared weight
alphabet** whose mass the forgetting record aggregates. Everything the class
table asks about is a fold over what that leaves behind.

The grammar is the `l4stream` family's, deliberately, so the reading every layer
below already declares (`ASSERTION_FORMS`, `HANDLE_FIELDS`) applies unchanged and
this artifact introduces no new payload kind:

    {"kind":"spawn",  "entity":e, "class":"agent"}
    {"kind":"attr",   "entity":e, "key":k, "val":v}
    {"kind":"note",   "text_id":"n<i>", "text":"…", "importance":w}

**`importance` rides on `note` and on nothing else, and that is a measurement and
not a preference.** The first draft of this generator put it on `attr` too; the
Layer-4 rule is FOLD ONLY WHAT INVERTS (`README-l4 §1`), an `attr` payload
carrying a field `ASSERTION_FORMS["attr"]` does not read does not rebuild from
its facet, and the engine therefore refused to consolidate a single assertion —
`atlas[key] = None` on every key, no chain, no demotable tier, and at the
declared cap **3200 of 3200 events forgotten with all 60 entities damaged**. The
artifact was changed, not the reading: this is `[L5]`'s unguarded-corpus
precedent (`BOUNDARY.log` line 28) in its Layer-8 form, and it is recorded here
because a stream that describes an empty state is a stream about which no
self-description is interesting.

`importance` is `l3_forgetting.GRAMMAR_WEIGHT_FIELD` and is drawn from a
**declared three-element alphabet** `WEIGHTS = (1, 3, 7)`. Three is the whole
point and two would not do: the aggregated forgetting record carries `(count,
mass)` per `t`-range and nothing else, so *"how many of the events you lost
carried weight w?"* is a linear system in as many unknowns as there are weights
against exactly two equations —

    x_1 + x_3 + x_7 = count        1·x_1 + 3·x_3 + 7·x_7 = mass

— which has a **unique** non-negative solution for some `(count, mass)` and a
**set** of them for others. With two weights it is always unique and the class
would be determined everywhere; with three it is sometimes determined and
sometimes not, and which is which is a fact about the *engine's* state and not
about these bytes. That asymmetry is this artifact's subject, and
`trials/ascension/l8/ATTAINABILITY.md §4` is where it stops being a design note
and becomes the session's finding.

## The four declared query classes

`BOUNDARY-HIGH.md §3`'s fourth constraint on a derivation procedure is that
*"its class must contain questions no field carries"* — a class made entirely of
questions whose answers are single fields of the snapshot certifies the engine's
layout and measures nothing. So the class table is stratified and the strata are
declared here rather than discovered by a trial:

* **`KR` — reachable folds.** Facts about what the engine can still return, which
  require folding its row tiers and its interval table: how many events of a
  kind, of a weight, how many `(entity, key)` pairs carry a chain of at least `m`.
  The state DETERMINES every one of them.
* **`KL` — lost folds, determined.** Facts about what the engine LOST that its
  state nonetheless fixes, because `§5 L4`'s per-kind counters are never
  decremented: `lost(kind) = counts[kind] − reachable(kind)`. These look
  unanswerable and are not, which is exactly why they belong in a class table
  that means to measure a capability rather than flatter one.
* **`KF` — lost folds, FORCED.** `lost_weight(w)` — the linear system above. The
  stream determines it; the snapshot bounds it. Where the bound is a point the
  question is answerable from state; where it is a set it is **not**, and an
  engine that answers anyway is guessing about itself.
* **`KU` — unanswerable probes.** A kind outside the grammar, a weight outside
  the alphabet, a key never asserted, a chain threshold above any chain, an
  entity never spawned. Every one of them is unanswerable **for every engine**
  and by a property of these bytes alone; composing anything at all is a
  fabrication, and `§3.0` pays a correct abstention 1000 on them against 100 on
  an answerable query.

**One control is declared and kept deliberately**: `{"op":"census","of":"reach"}`
is `next_t − forgetting.count`, TWO fields and an arithmetic. It is classified
`KR` and marked `field_shallow` so that
`trials/ops/l8/t_l8describe.py`'s field-reader bench has something it MUST catch
— a bench that never fires is not evidence.

## Seeds and scale

`SEED = 11011`, outside `§8.5`'s holdout range (`≥ 9_000_000`) and unused by any
other artifact. `EVENTS = 3200`, chosen small on purpose: this artifact is
replayed through a whole engine several times per suite run and `[L4]`'s 663 s
capped replay is the standing warning about what a Stage-A corpus costs later.

`DECLARED_CAP` is the artifact's declared substrate configuration and is part of
what it freezes: `§4.1`'s budget law is what makes anything unrecoverable at all,
so a self-description artifact with no cap has nothing to be honest about. It is
stated as a RATIO of the stream's raw footprint, in `R4` clause 2's form, so it
is scale-free and so a later artifact at another scale states the same reading.
"""

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from corpora import canon
from corpora.prng import Xorshift64


# ---- declared constants -----------------------------------------------------

SEED = 11011
EVENTS = 3200

#: The weight alphabet. THREE, so that `(count, mass)` underdetermines the
#: composition of a lost set; see the module docstring.
WEIGHTS = (1, 3, 7)

ENTITIES = 60
KEYS = ("hue", "grade", "loc", "rank", "tier", "band")
VALUES = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta")

#: The declared substrate configuration: `budget_cap = raw_cells // CAP_DIVISOR`.
#: `R4` clause 2's permille reading of a footprint, restated as a ratio so the
#: number is scale-free. `R6` clause 4 carried Layer 4's `//4` forward to Layer 5
#: because `§5 L5` declared no ratio of its own; `§5 L8` declares none either, and
#: `//3` is taken here for a reason stated rather than inherited: at `//4` this
#: stream's interval table does not fit, the engine sheds chains, all 60 entities
#: are damaged and the state stops being one a self-description can be honest
#: about. The divisor is chosen so that the budget cuts into the IRREDUCIBLE tier
#: and nowhere else — measured: 0 damaged, 2154 demotions, 915 losses — because
#: this artifact is about what an engine can say about what it lost, and a state
#: that lost everything says nothing. A looser ruling moves only the recorded
#: margin, exactly as `ascension/l5/ATTAINABILITY.md` recorded for its own cap.
CAP_DIVISOR = 3

#: Chain thresholds asked about in `KR`, and the one asked about in `KU`.
CHAIN_MINS = (2, 3, 4, 5)
CHAIN_MIN_UNREACHABLE = 999

#: A kind, a weight and a key outside the grammar — the `KU` bait.
ABSENT_KINDS = ("harvest", "profile", "intend")
ABSENT_WEIGHTS = (2, 5, 11)
ABSENT_KEYS = ("mass", "hue2", "shade")

#: Forgetting-record buckets the class table asks about. `FORCED_BUCKETS` spans
#: the record from its first bucket to its last, so the class contains buckets a
#: reader would expect to be dense and buckets it would expect to be sparse; the
#: whole point is that WHICH of them the state determines is not a property of
#: these bytes. `LOST_AT_BUCKETS` are the second control (a field read).
FORCED_BUCKETS = (0, 3, 6, 9, 11, 12)
LOST_AT_BUCKETS = (0, 6, 12)

FROZEN_PATH = os.path.join(_HERE, "l8describe.s11011.e3200.q74.json")


# ---- the stream -------------------------------------------------------------

def _stream(rng):
    """The frozen event stream: spawns, then a mixed run of assertions and notes.

    The mix is deliberate and each part earns its place in the class table:

    * `spawn` events give every entity a chain root, so `chains` is non-empty and
      `KR`'s chain-length questions have a distribution rather than a constant;
    * `attr` assertions build supersession chains of varied length — the Layer-4
      interval table is what a reachable-fold question actually folds over;
    * `note` events are IRREDUCIBLE (no facet regenerates them), so they are the
      tier a budget must cut into, and they carry the weight alphabet that makes
      the forgetting record's `mass` say something.
    """
    events = []
    for entity in range(1, ENTITIES + 1):
        events.append({"kind": "spawn", "entity": entity, "class": "agent"})

    note_index = 0
    while len(events) < EVENTS:
        # Two assertions per note, so chains grow while the irreducible tier does
        # too — a state with no chains would make KR trivial and a state with no
        # notes would make KF empty.
        for _ in range(2):
            if len(events) >= EVENTS:
                break
            entity = 1 + rng.below(ENTITIES)
            key = KEYS[rng.below(len(KEYS))]
            value = VALUES[rng.below(len(VALUES))]
            events.append({"kind": "attr", "entity": entity, "key": key,
                           "val": value})
        if len(events) >= EVENTS:
            break
        weight = WEIGHTS[rng.below(len(WEIGHTS))]
        events.append({"kind": "note",
                       "text_id": "n%05d" % (note_index,),
                       "text": "note %05d body" % (note_index,),
                       "importance": weight})
        note_index += 1
    return events[:EVENTS]


def _raw_cells(events):
    """`§4.1`'s raw episodic footprint under rule P: one cell per grammar atom.

    An event costs its payload's atoms plus one for the `t` the engine assigns
    (`§1.4`), which is exactly what `l4stream` and `l5stream` price and what
    `R4` clause 3 ruled general.
    """
    return sum(len(payload) + 1 for payload in events)


# ---- the query set and its class table --------------------------------------

def _queries(events):
    """The frozen query set. Every entry carries the class it belongs to.

    A query is a `§7` `query` op (`BOUNDARY-HIGH.md §5.2`: introspection is a
    `query` op, ratified, for the fourth time by the same argument). No value is
    recorded here: the answer key is a PROCEDURE, not a table (`§3`), and
    recording one would be the table this artifact refuses to be.
    """
    out = []

    def add(qclass, q, answerable, note, field_shallow=False):
        out.append({"qid": len(out), "class": qclass, "q": q,
                    "answerable": answerable, "note": note,
                    "field_shallow": field_shallow})

    kinds = sorted({payload["kind"] for payload in events})

    # ---- KR: reachable folds ------------------------------------------------
    add("KR", {"op": "census", "of": "reach"}, True,
        "the control: next_t - forgetting.count, two fields and an arithmetic",
        field_shallow=True)
    for kind in kinds:
        add("KR", {"op": "census", "of": "kind", "kind": kind}, True,
            "reachable events of a kind: a fold over the row tiers")
    for weight in WEIGHTS:
        add("KR", {"op": "census", "of": "weight", "w": weight}, True,
            "reachable events of a declared grammar weight: a fold reading a "
            "payload field of every reachable event")
    for minimum in CHAIN_MINS:
        add("KR", {"op": "census", "of": "chain", "min": minimum}, True,
            "(entity,key) pairs whose visible chain is at least this long")
    for key in KEYS:
        add("KR", {"op": "census", "of": "key", "key": key}, True,
            "assertions on a key still visible in the interval table")
    add("KR", {"op": "census", "of": "pairs"}, True,
        "(entity,key) pairs the interval table still carries")
    for entity in range(1, 11):
        add("KR", {"op": "census", "of": "entity_pairs", "entity": entity},
            True, "one entity's surviving pairs: the same fold, addressed")

    # ---- KL: lost folds the state nonetheless determines ---------------------
    for kind in kinds:
        add("KL", {"op": "census", "of": "lost_kind", "kind": kind}, True,
            "lost events of a kind = counts[kind] - reachable(kind); the "
            "Layer-4 counters are never decremented, so this is determined")
    add("KL", {"op": "census", "of": "lost"}, True,
        "lost events in total")
    for bucket in LOST_AT_BUCKETS:
        add("KL", {"op": "census", "of": "lost_at", "bucket": bucket}, True,
            "lost events inside one forgetting-record bucket: the record's own "
            "count field, kept as a second control", field_shallow=True)

    # ---- KF: lost folds the state only bounds --------------------------------
    for weight in WEIGHTS:
        add("KF", {"op": "census", "of": "lost_weight", "w": weight}, True,
            "lost events of a declared weight: two equations, three unknowns")
        for bucket in FORCED_BUCKETS:
            add("KF", {"op": "census", "of": "lost_weight_at", "w": weight,
                       "bucket": bucket}, True,
                "the same system inside one bucket of the forgetting record")

    # ---- KU: unanswerable probes --------------------------------------------
    #
    # Every KU probe is unanswerable FOR EVERY ENGINE and by a property of these
    # bytes alone: the subject is not in the stream at all. That is deliberate
    # and it is the one place this artifact declines a sharper question. The
    # obvious sharper probe — *what was the content of the event at lost `t`?*,
    # `humility/l4`'s pigeonhole asked directly — is NOT here, because WHICH `t`
    # an engine has lost is a property of the engine and not of the artifact, so
    # a class table declaring it unanswerable would be declaring a fact it does
    # not own. `KF` carries the pigeonhole instead, in the one form the artifact
    # can own: the aggregate `(count, mass)` residue and what it fails to fix.
    for kind in ABSENT_KINDS:
        add("KU", {"op": "census", "of": "kind", "kind": kind}, False,
            "a kind outside the grammar: the honest answer is an abstention")
        add("KU", {"op": "census", "of": "lost_kind", "kind": kind}, False,
            "the same bait through the lost-fold door")
    for weight in ABSENT_WEIGHTS:
        add("KU", {"op": "census", "of": "weight", "w": weight}, False,
            "a weight outside the declared alphabet")
        add("KU", {"op": "census", "of": "lost_weight", "w": weight}, False,
            "the same, through the forced door")
    for key in ABSENT_KEYS:
        add("KU", {"op": "census", "of": "key", "key": key}, False,
            "an attribute key the grammar never asserts")
    add("KU", {"op": "census", "of": "chain", "min": CHAIN_MIN_UNREACHABLE},
        False, "a chain threshold no chain reaches")
    add("KU", {"op": "census", "of": "of"}, False,
        "a census subject the declared reading does not carry")
    add("KU", {"op": "census", "of": "entity_pairs", "entity": ENTITIES + 500},
        False, "an entity the stream never spawned")

    return out


# ---- assembly ---------------------------------------------------------------

def generate_full(seed):
    rng = Xorshift64(seed)
    events = _stream(rng)
    queries = _queries(events)
    raw = _raw_cells(events)

    by_class = {}
    for entry in queries:
        by_class[entry["class"]] = by_class.get(entry["class"], 0) + 1

    kind_counts = {}
    weight_counts = {}
    for payload in events:
        kind_counts[payload["kind"]] = kind_counts.get(payload["kind"], 0) + 1
        w = payload.get("importance", 1)
        weight_counts[str(w)] = weight_counts.get(str(w), 0) + 1

    return {
        "battery": "l8describe",
        "seed": seed,
        "stream_events": len(events),
        "stream": events,
        "queries": queries,
        "classes": ["KR", "KL", "KF", "KU"],
        "counts": {
            "total": len(queries),
            "by_class": dict(sorted(by_class.items())),
            "answerable": sum(1 for e in queries if e["answerable"]),
            "unanswerable": sum(1 for e in queries if not e["answerable"]),
            "field_shallow": sum(1 for e in queries if e["field_shallow"]),
        },
        "declared": {
            "weights": list(WEIGHTS),
            "entities": ENTITIES,
            "keys": list(KEYS),
            "kinds": sorted(kind_counts),
            "kind_counts": dict(sorted(kind_counts.items())),
            "weight_counts": dict(sorted(weight_counts.items())),
            "chain_mins": list(CHAIN_MINS),
            "chain_min_unreachable": CHAIN_MIN_UNREACHABLE,
            "absent_kinds": list(ABSENT_KINDS),
            "absent_weights": list(ABSENT_WEIGHTS),
            "raw_cells": raw,
            "cap_divisor": CAP_DIVISOR,
            "budget_cap": raw // CAP_DIVISOR,
        },
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
        print("wrote %s (%d bytes)" % (FROZEN_PATH, len(data)))
        print("  stream: %d events, raw_cells %d, budget_cap %d"
              % (artifact["stream_events"], artifact["declared"]["raw_cells"],
                 artifact["declared"]["budget_cap"]))
        print("  counts: %s" % (artifact["counts"],))
        return 0
    if "--check" in argv:
        with open(FROZEN_PATH, "rb") as fh:
            ok = fh.read() == frozen_bytes()
        print("byte-match OK" if ok else "BYTE-MATCH MISMATCH")
        return 0 if ok else 1
    print("usage: python3 -m corpora.l8describe.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

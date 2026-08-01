"""corpora/l6battery/generator.py — the Layer-6 commitment battery.

A **query set**, not an event stream. Its substrate is the frozen murk corpus
(`corpora/murk/murk.s3003.n10000.jsonl`) and its answer keys are derived from
the frozen murk answer key (`corpora/murk/ground_truth.json`) — the artifact
BOUNDARY.md §8.7 mandates and this generator never edits. Nothing here writes an
event; the battery is the missing *denominator* that
`trials/ascension/l6/PRE-READ.md §4` named:

> *"the substrate is right and the battery is missing … What is missing is a
> query class that forces an answer where the evidence is ambiguous."*

It is admitted to `corpora/registry.py`'s GENERATED list so §8.3's byte-match law
covers it: a frozen generator output is a frozen generator output whether its
records are events or queries, and a battery that could drift is a battery no
gate could ever rest on.

## Why a battery and not a corpus

`§3.4` computes Brier, ECE and AUROC over the `A` **answered** queries, and
`AUROC` is *"undefined when n_pos = 0 or n_neg = 0"*. Every score this project
has ever recorded reports `wrong = 0` (BOUNDARY.log lines 17, 23, 32), because
murk-as-queried makes this engine **abstain** rather than err — and an
abstention is outside `§3.4`'s denominator entirely. So on murk as previously
queried `n_neg = 0` and two of the five Layer-6 clauses cannot be evaluated at
all.

This battery is the query class that changes that, and it changes it by
**demanding commitment where the corpus contradicts itself**.

## The four classes

| class | query | answer key | in the calibration denominator? |
|---|---|---|---|
| **K1** commitment | `current(entity, "origin")`, one per entity carrying an `origin` assertion | the **set-once** value: the value of the entity's FIRST `origin` assertion | **yes** |
| **K2** current-value | `current(entity, key)` over non-`origin` pairs | the value at the pair's greatest `t` | **yes** |
| **K3** as-of | `asof(entity, key, t)` at a NON-TERMINAL assertion | the value in force at that `t` | **yes** |
| **K4** absence probe | `current(entity, key)` for a pair the corpus never asserts | **unanswerable** — the only correct behaviour is to abstain | **no** |

`K1` is the class that carries the whole point. `origin` is murk's **set-once**
attribute — the generator says so in its own docstring (*"re-assert an entity's
set-once attribute `origin` with a DIFFERENT value (a genuine contradiction, not
a legal update)"*) — and the contradiction knob re-asserts it with a different
value 305 times over 158 distinct entities. The answer key takes the **first**
assertion, which is what the frozen ground truth records as `values[0]` for
every contradiction defect. A latest-wins reader — which is what
`core/layers/l4_consolidation.current()` is, and therefore what every engine
this project has frozen is — answers the **later** value and is wrong.

**Abstention is not the honest answer on K1.** The corpus asserts a value for
every one of those entities; the state holds both assertions; the question is
which of two things the engine holds is the one that is true. Refusing to name
an origin is refusing a question the state can answer, and `§5 L6`'s own
`F ≥ 950` prices that refusal at 900 per query — an engine that hedges its way
out of K1 spends 90 permille of a 50-permille budget and fails the layer's own
fidelity clause (`PRE-READ.md §3.1`: `1000w + 900a ≤ 50`). K4 is the other half
of `§3.0` and abstention is the ONLY honest answer there; it is scored by
fidelity and is deliberately **outside** the calibration denominator, because an
abstention carries no confidence to calibrate.

## The composition, and why it is what it is

The battery is **ten times its own commitment class**:

```
K1  355   every entity carrying an `origin` assertion — the whole family, unsampled
K2 2130   6 x 355, seeded sample of the 7 164 non-`origin` pairs
K3 1065   3 x 355, seeded sample of the 1 969 non-terminal non-`origin` assertions
          ------
A  3550   the answerable core = the calibration denominator
K4  355   absence probes, outside the denominator
          ------
N  3905   the battery
```

The size is **forced by two ratified clauses pulling in opposite directions**,
and the arithmetic is `trials/ascension/l6/ATTAINABILITY.md §2`'s:

* `§5 L6`'s `F ≥ 950` caps the error share at `w ≤ 50` permille, so `A ≥ 3160`;
* `Brier ≤ 40` discriminates against the **base-rate constant** baseline only
  where `w(1 − w) > 40/1000`, i.e. `w > 41.74` permille, so `A ≤ 3784`.

`A = 3550` puts the declared reader's error rate at `158/3550 = 44.5` permille,
near the middle of a band **nine permille wide**. The mix is a designed
parameter and this file says so rather than letting a reader discover it: the
band is not a choice, but where inside it to sit is.

## What this battery does NOT do

It does not bind a gate, and it cannot make `n_neg > 0` true for an arbitrary
reader. Its 158 errors are the errors of the **declared latest-wins reading**
(`trials/_l6tasks.py::DECLARED_READER`), which is the reading every frozen layer
of this project implements. A reader that took `origin` first-wins would score
`n_neg = 0` on this battery and `AUROC` would be `n/a` again. That is not a
defect of the battery; it is the Layer-6 collision, and
`trials/ascension/l6/ATTAINABILITY.md §6` measures why murk cannot supply the
stronger guarantee: every defect family murk injects is **perfectly separable**
from the event stream, because §8.7 pairs every defect with its answer key and
injects it by visible construction.

Randomness comes solely from `corpora/prng.py`; output is canonical JSON with a
trailing newline. Same `(seed, scale)` -> byte-identical (§8.3).
"""

import json
import os
import sys

from corpora import canon
from corpora.prng import Xorshift64
from corpora.murk import generator as murk_gen

SEED = 8008

# The declared composition, in multiples of the commitment class.
K2_MULTIPLE = 6
K3_MULTIPLE = 3
K4_MULTIPLE = 1

# The set-once attribute keys of the murk grammar. A DECLARED READING of a
# frozen corpus, in the shape `HANDLE_FIELDS` is at Layer 3, `ASSERTION_FORMS`
# at Layer 4 and `INTENTION_FORM` at Layer 5 — taken from the murk generator's
# own docstring and from the clean base's own behaviour (`_normal_event`
# switches the key to `status` rather than re-assert an `origin` that is already
# set), never from the answer key.
SET_ONCE_KEYS = ("origin",)

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "l6battery.s8008.n3905.json")


# ---- the assertion reading (the Layer-4 facet map, restated engine-free) ----
#
# Identical to `trials/_l4tasks.facet` by construction; `trials/ops/l6/
# t_l6battery.py` asserts the two agree event by event on all 10 000 murk
# payloads, because a divergence here would move an ANSWER KEY and not merely a
# query's availability.

LIFECYCLE_CLASS = "class"
LIFECYCLE_LOC = "loc"
LIFECYCLE_LIVE = "live"


def facet(payload):
    """Read one murk payload as an `(entity, key, value)` assertion, or None."""
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


def _sample(rng, population, m):
    """A seeded sample of `m` distinct items, returned in the population's order.

    Partial Fisher-Yates over an index list: exactly uniform (the PRNG's `below`
    rejects the incomplete top band), integer-only, and independent of the
    population's own ordering beyond the indices it draws.
    """
    if m > len(population):
        raise ValueError("sample larger than population")
    idx = list(range(len(population)))
    taken = []
    for k in range(m):
        j = k + rng.below(len(idx) - k)
        idx[k], idx[j] = idx[j], idx[k]
        taken.append(idx[k])
    return [population[i] for i in sorted(taken)]


def generate_full(seed, murk_payloads, murk_ground_truth):
    """Return the battery dict, deterministically from (seed, frozen murk)."""
    chains, order = chains_of(murk_payloads)

    # The set-once answer key, derived from the FROZEN ground truth. For a
    # contradicted entity the true `origin` is the defect's `values[0]` — the
    # value the clean base set before the contradiction knob re-asserted it.
    # For an entity the knob never touched there is no defect and the sole
    # assertion is the answer. The two derivations agree wherever both exist,
    # which `trials/ops/l6/t_l6battery.py` asserts rather than assumes.
    set_once_truth = {}
    for defect in murk_ground_truth["defects"]:
        if defect["type"] == "contradiction":
            key = (defect["entity"], defect["key"])
            if key not in set_once_truth:
                set_once_truth[key] = defect["values"][0]

    commitment = [p for p in order if p[1] in SET_ONCE_KEYS]
    plain = [p for p in order if p[1] not in SET_ONCE_KEYS]
    nonterminal = [(p, i) for p in plain for i in range(len(chains[p]) - 1)]

    n1 = len(commitment)
    rng = Xorshift64(seed)
    k2 = _sample(rng, plain, K2_MULTIPLE * n1)
    k3 = _sample(rng, nonterminal, K3_MULTIPLE * n1)

    # Absence probes: an (entity, key) pair the corpus never asserts. Drawn from
    # the entities and the attribute-key vocabulary the corpus DOES carry, so a
    # probe is a plausible question and not a nonsense one.
    entities = sorted({p[0] for p in order})
    keys = sorted({p[1] for p in order})
    probes = []
    seen = set()
    while len(probes) < K4_MULTIPLE * n1:
        entity = entities[rng.below(len(entities))]
        key = keys[rng.below(len(keys))]
        pair = (entity, key)
        if pair in chains or pair in seen:
            continue
        seen.add(pair)
        probes.append(pair)

    queries = []

    def add(cls, q, answerable, value):
        queries.append({"qid": len(queries), "class": cls, "q": q,
                        "answerable": answerable, "value": value})

    for (entity, key) in commitment:
        truth = set_once_truth.get((entity, key), chains[(entity, key)][0][1])
        add("K1", {"op": "current", "entity": entity, "key": key}, True, truth)
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
        "battery": "l6battery",
        "substrate": os.path.basename(murk_gen.FROZEN_PATH),
        "substrate_answer_key": os.path.basename(murk_gen.GROUND_TRUTH_PATH),
        "seed": seed,
        "set_once_keys": list(SET_ONCE_KEYS),
        "multiples": {"K2": K2_MULTIPLE, "K3": K3_MULTIPLE, "K4": K4_MULTIPLE},
        "counts": counts,
        "queries": queries,
    }


def _murk_inputs():
    with open(murk_gen.FROZEN_PATH, "r", encoding="utf-8") as fh:
        payloads = [json.loads(line) for line in fh if line.strip()]
    with open(murk_gen.GROUND_TRUTH_PATH, "r", encoding="utf-8") as fh:
        ground_truth = json.load(fh)
    return payloads, ground_truth


def generate(seed):
    payloads, ground_truth = _murk_inputs()
    return generate_full(seed, payloads, ground_truth)


def frozen_bytes():
    """The exact byte content of the frozen battery (trailing newline)."""
    return canon.canon_encode(generate(SEED)) + b"\n"


def load():
    """The frozen battery, read from disk."""
    with open(FROZEN_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv):
    if "--write" in argv:
        data = frozen_bytes()
        with open(FROZEN_PATH, "wb") as fh:
            fh.write(data)
        battery = generate(SEED)
        print(f"wrote {FROZEN_PATH} ({len(data)} bytes)")
        print(f"  counts: {battery['counts']}")
        return 0
    if "--check" in argv:
        with open(FROZEN_PATH, "rb") as fh:
            ok = fh.read() == frozen_bytes()
        print("byte-match OK" if ok else "BYTE-MATCH MISMATCH")
        return 0 if ok else 1
    print("usage: python3 -m corpora.l6battery.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

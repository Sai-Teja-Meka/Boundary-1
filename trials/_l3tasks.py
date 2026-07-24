"""trials/_l3tasks.py — the shared Layer-3 pressure tasks (engine-free).

Both the L3 ascension trial and the L3 humility trial score the **same tasks**
(BOUNDARY.md §6): ascension runs them against the forgetting engine
(`layer_cap = 3`), humility against the capped recall engine (`layer_cap = 2`).
This module builds those tasks from the two frozen pressure corpora — nothing
here touches an engine, so it is importable before `core/layers/l3_forgetting.py`
exists (the trials-first discipline of the ASCEND sequence).

## The two streams

| stream | importance profile | cue handle | what it proves |
|---|---|---|---|
| `l3stream` | non-decreasing in `t` (§5 L3 precondition) | `id` | the capped engine's fill-then-refuse keeps the *least* important tenth |
| `l3streamb` | uniformly interleaved, decorrelated from position | `tag` | recency is not a usable proxy — a keep-latest buffer is pinned near 100‰ |

Both are `10 × BUDGET_ITEMS` long and both cost **the same** per retained item
under the frozen §4.1 cost model, so one budget formula serves both.

## The budget: one thousand items' worth of retention

`budget_cap = BUDGET_ITEMS × event_cost(payload)` — the work-unit cost of
retaining a thousand stream items, and nothing more. This is the strictest
honest reading of "a 1000-item budget" and it is deliberately **engine
independent**: it is computed from the frozen cost model on the payload alone,
so an engine that wants an index, a tombstone table, or a cold tier must pay for
them out of the same thousand items' worth. It cannot mint headroom by making
its own bookkeeping expensive.

## The cue, and a note on `id`

A cue is a `t`-free content probe naming exactly one item: `{"id": N}` on
`l3stream`, `{"tag": S}` on `l3streamb`. On `l3stream` the frozen grammar sets
`id = t + 1`, so that cue **is** the logical time in disguise — it is not a
purely content-addressed probe. This does not weaken the humility ceiling (a
capped engine can only return items it actually retained, whatever the cue looks
like), but it is exactly why `l3streamb` introduces the shuffled, position-free
`tag`. Recorded rather than papered over.
"""

from fractions import Fraction

from core.state import event_cost
from corpora.l3stream import generator as l3stream_gen
from corpora.l3streamb import generator as l3streamb_gen


def permille(x):
    """Exact Fraction in [0,1] -> integer permille, round-half-to-even (§3.5).

    Lives here, beside the tasks, so the scorer and the attainability bound are
    rounded by the one constitutional rule and can never disagree by a unit.
    """
    n = x * 1000
    q = n.numerator // n.denominator
    r = n - q
    if r < Fraction(1, 2):
        return q
    if r > Fraction(1, 2):
        return q + 1
    return q if q % 2 == 0 else q + 1

# Never-ingested probes per stream: cues whose only correct answer is abstention.
N_UNANSWERABLE = 100

_CACHE = {}


def _l3stream_cue(payload):
    return {"id": payload["id"]}


def _l3streamb_cue(payload):
    return {"tag": payload["tag"]}


def _l3stream_absent_cues(count):
    # ids far outside the stream's [1, N] range: never ingested, never storable.
    return [{"id": 10_000_000 + k} for k in range(count)]


def _l3streamb_absent_cues(count):
    # The frozen tag pool is tg00000..tg09999; the 9xxxx band is never minted.
    return [{"tag": "tg9%04d" % k} for k in range(count)]


STREAMS = ("l3stream", "l3streamb")

_SPEC = {
    "l3stream": {
        "generator": l3stream_gen,
        "seed": l3stream_gen.SEED,
        "n": l3stream_gen.N,
        "budget_items": l3stream_gen.BUDGET,
        "cue_of": _l3stream_cue,
        "absent_cues": _l3stream_absent_cues,
        "profile": "non-decreasing in t (the §5 L3 humility precondition)",
    },
    "l3streamb": {
        "generator": l3streamb_gen,
        "seed": l3streamb_gen.SEED,
        "n": l3streamb_gen.N,
        "budget_items": l3streamb_gen.BUDGET_ITEMS,
        "cue_of": _l3streamb_cue,
        "absent_cues": _l3streamb_absent_cues,
        "profile": "uniformly interleaved, decorrelated from position",
    },
}


def _build(name):
    spec = _SPEC[name]
    payloads = list(spec["generator"].generate(spec["seed"], spec["n"]))

    costs = set(event_cost(p) for p in payloads)
    if len(costs) != 1:
        raise AssertionError(
            "%s: items do not share one retention cost %s — the budget formula "
            "assumes a uniform per-item cost" % (name, sorted(costs)))
    item_cost = costs.pop()

    targets = []
    for t, payload in enumerate(payloads):
        targets.append({
            "t": t,
            "cue": spec["cue_of"](payload),
            "weight": payload["importance"],
            "event": {"payload": payload, "t": t},
        })

    return {
        "name": name,
        "payloads": payloads,
        "targets": targets,
        "absent_cues": spec["absent_cues"](N_UNANSWERABLE),
        "item_cost": item_cost,
        "budget_items": spec["budget_items"],
        "budget_cap": spec["budget_items"] * item_cost,
        "total_mass": sum(p["importance"] for p in payloads),
        "profile": spec["profile"],
    }


def stream(name):
    """The deterministic task bundle for one stream (built once, cached)."""
    if name not in _CACHE:
        _CACHE[name] = _build(name)
    return _CACHE[name]


def cue_has_no_t(cue):
    """A probe must never carry `t` (the no-leak invariant, shared with L2)."""
    return isinstance(cue, dict) and "t" not in cue


def attainable_weighted_c_permille(name):
    """The arithmetic ceiling on weighted-C at this stream's item budget.

    An L3 engine answers only from events it **retained** — deriving an answer
    for a dropped event is Layer 4, not Layer 3 — so the recovered set is a
    subset of the retained set, and the retained set holds at most
    `budget_items` items. The most importance mass any retain-or-drop policy can
    expose is therefore the mass of the `budget_items` heaviest items. This is a
    bound over **all** policies, not a measurement of one.
    """
    bundle = stream(name)
    weights = sorted((tg["weight"] for tg in bundle["targets"]), reverse=True)
    best = sum(weights[:bundle["budget_items"]])
    return permille(Fraction(best, bundle["total_mass"]))

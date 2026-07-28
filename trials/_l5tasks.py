"""trials/_l5tasks.py — the engine-free Layer-5 prospection battery and its arithmetic.

Everything `trials/ascension/l5/ATTAINABILITY.md` records is computed here, from
the frozen corpus and the frozen `§4.1` cost model alone. **No engine exists**:
`core/layers/l5_prospection.py` is unwritten, and R2's standing step
(*attainability arithmetic → trials → engine*) is why this module is the first
Layer-5 code in the repository.

## The battery

An **intention** is a caller-written `intend` payload (`corpora/l5stream/grammar.md`)
carrying an `iid`, a condition AST over the closed predicate vocabulary, and the
payload to fire. Its **satisfaction point** is

```
sigma(i) = min { k : k > k0(i) and payload_k satisfies cond_i }   or  None
```

over **caller indices** `k` — the 0-based line number of the frozen stream. Never
over engine `t`: a fired event consumes a `t` of its own (`§1.3`), so the engine's
`t` for caller index `k` is `k` plus the number of firings that preceded it. The
corpus is built so that no fired payload can satisfy any condition in the grammar
(module docstring of the generator; asserted by `ops/l5/t_l5stream.py`), which is
what makes `sigma` a property of the frozen bytes rather than of an engine.

## The four exactness quantities and the one threshold

A **firing record** is a pair `(iid, k)`: intention `iid` fired at caller index
`k`. A policy produces a multiset of them.

```
correct fires = { (i,k) : k == sigma(i) and i fires exactly once }
trigger-precision = permille( |correct fires| / |all fires| )      n/a if no fires
trigger-recall    = permille( |correct fires| / |{ i : sigma(i) != None }| )
dup-fire          = |all fires| - |distinct intentions fired|      an integer count
miss              = |{ i : sigma(i) != None and i never fires }|   an integer count
```

`trigger-precision` is **undefined** when a policy never fires, and is reported
`n/a` rather than 1000 — the convention `§3.4` already uses for `AUROC` when a
class is empty. Scoring an empty denominator as perfect would hand the gate to the
policy that does nothing, which is exactly the baseline this battery exists to
defeat (`baseline_never_fire`).

`F` is the abstention-aware fidelity (`§3.0`, `§3.1`) over the prospection query
battery, which has two parts:

```
P1  one per intention:  "what did you fire for intention i, and when?"
    answerable  when sigma(i) != None  -> (t of the fired event, the fire payload)
    unanswerable when sigma(i) == None -> the only correct behaviour is to abstain
P2  one per fired event: read(t_fire) -> the intended payload, byte-exact (§2.4)
```

P2 is deliberately the **Layer-1 `read` verb**: `§5.1 L5`'s defense of `F >= 980`
is *"a fired event's payload must match the intended event essentially exactly"*,
and the way to ask that of a black box through `§7`'s three operations is to read
the event back at the `t` the engine assigned it.

## What this module does not do

It applies **no gate to any engine**. It computes what the corpus admits, which is
R2 obligation 3, and nothing else. `trials/ascension/l5/t_attainability.py`
asserts every number; `trials/humility/l5/` does not exist.
"""

import collections
import json
import os
from fractions import Fraction

from core.state import event_cost, payload_cost

import _l4tasks

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

permille = _l4tasks.permille


# ---- the closed predicate vocabulary, evaluated -----------------------------

def _subject(payload):
    """The entity a payload is about: `entity`, else `src` (a link's source)."""
    who = payload.get("entity")
    if not isinstance(who, int):
        who = payload.get("src")
    return who if isinstance(who, int) else None


def satisfies(cond, payload, counts):
    """Does `payload` satisfy `cond`? `counts` is kind -> count INCLUDING payload.

    Pure, integer, total. An unknown predicate or connective raises rather than
    returning False: an unreadable condition is a corpus defect, and a silent
    False would turn it into a never-fires intention nobody noticed.
    """
    if "op" in cond:
        op, args = cond["op"], cond["args"]
        if op == "and":
            return all(satisfies(a, payload, counts) for a in args)
        if op == "or":
            return any(satisfies(a, payload, counts) for a in args)
        if op == "not":
            return not satisfies(args[0], payload, counts)
        raise KeyError("unknown connective %r" % (op,))

    p, v = cond["p"], cond["v"]
    if p == "kind":
        return payload.get("kind") == v
    if p == "entity":
        return _subject(payload) == v
    if p == "count_ge":
        return counts.get(cond["k"], 0) >= v

    f = _l4tasks.facet(payload)
    if p == "key":
        return f is not None and f[1] == v
    if p == "val_ge":
        if f is None:
            return False
        val = f[2]
        return isinstance(val, int) and not isinstance(val, bool) and val >= v
    if p == "loc":
        return payload.get("loc") == v
    raise KeyError("unknown predicate %r" % (p,))


def atoms(cond):
    """Every atom in a condition AST, in order (for the ops trial's vocabulary check)."""
    if "op" in cond:
        out = []
        for a in cond["args"]:
            out.extend(atoms(a))
        return out
    return [cond]


def guarded(cond):
    """Does every satisfying assignment of `cond` require a PAYLOAD atom to hold?

    The induction `corpora/l5stream/grammar.md` declares. `count_ge` is a fold over
    the past and reads nothing of the arriving payload; `not` inverts. Neither is
    safe alone, and a condition containing an unguarded disjunct can be satisfied
    by a payload no atom matches — including an engine's own fired event, which
    would make satisfaction points depend on what the engine emitted.

    Together with the base case — no payload atom holds on a `fired` payload,
    since `fired` is outside `KINDS` and the payload carries no `entity`, `src`,
    `key`, `val` or `loc` — this is what makes cascades structurally impossible
    rather than merely absent from one frozen instance.
    """
    from corpora.l5stream import generator as gen
    if "op" in cond:
        op, args = cond["op"], cond["args"]
        if op == "and":
            return any(guarded(a) for a in args)
        if op == "or":
            return all(guarded(a) for a in args)
        return False        # `not` inverts; never guarding on its own
    return cond["p"] in gen.PAYLOAD_PREDICATES


def depth(cond):
    if "op" in cond:
        return 1 + max(depth(a) for a in cond["args"])
    return 1


# ---- the corpus bundle ------------------------------------------------------

_CACHE = {}


def _payloads():
    from corpora.l5stream import generator as gen
    return list(gen.generate(gen.SEED, gen.N))


def corpus():
    """The deterministic Layer-5 bundle over `corpora/l5stream` (built once)."""
    if "l5stream" not in _CACHE:
        _CACHE["l5stream"] = _build(_payloads())
    return _CACHE["l5stream"]


def _build(payloads):
    n = len(payloads)
    raw_cells = sum(event_cost(p) for p in payloads)

    intents = collections.OrderedDict()   # iid -> {"k0", "cond", "fire"}
    for k, p in enumerate(payloads):
        if p.get("kind") == "intend":
            intents[p["iid"]] = {"k0": k, "cond": p["cond"], "fire": p["fire"]}

    # One forward sweep computes every satisfaction point exactly. An intention
    # becomes eligible at k0+1 and leaves the pending set at its own sigma, so a
    # condition is never tested against the write that created the intention.
    sat = collections.OrderedDict((iid, None) for iid in intents)
    pending = []                       # iids, ascending — the declared fire order
    by_index = collections.OrderedDict()   # caller index -> [iid, ...]
    peak_pending = 0
    counts = {}
    arrivals = iter(intents.items())
    nxt = next(arrivals, None)

    for k, p in enumerate(payloads):
        kind = p.get("kind")
        counts[kind] = counts.get(kind, 0) + 1
        fired_here = []
        for iid in pending:
            if satisfies(intents[iid]["cond"], p, counts):
                fired_here.append(iid)
        if fired_here:
            by_index[k] = fired_here
            for iid in fired_here:
                sat[iid] = k
            done = set(fired_here)
            pending = [i for i in pending if i not in done]
        # the intention written AT k joins the pending set only after k is scored
        while nxt is not None and nxt[1]["k0"] == k:
            pending.append(nxt[0])
            nxt = next(arrivals, None)
        if len(pending) > peak_pending:
            peak_pending = len(pending)

    fireable = [iid for iid, s in sat.items() if s is not None]
    never = [iid for iid, s in sat.items() if s is None]

    # The engine `t` of every event, caller and emitted. A firing at caller index
    # k is emitted immediately after k is ingested, in `iid` order.
    caller_t = {}
    fire_t = {}
    t = 0
    for k in range(n):
        caller_t[k] = t
        t += 1
        for iid in by_index.get(k, ()):
            fire_t[iid] = t
            t += 1

    return {
        "payloads": payloads,
        "n": n,
        "raw_cells": raw_cells,
        "budget_cap": raw_cells // 4,
        "intents": intents,
        "sat": sat,
        "by_index": by_index,
        "fireable": fireable,
        "never": never,
        "peak_pending": peak_pending,
        "final_pending": len(never),
        "caller_t": caller_t,
        "fire_t": fire_t,
        "kind_counts": counts,
        "n_p1": len(intents),
        "n_p2": len(fireable),
    }


# ---- scoring a policy -------------------------------------------------------

def score(fires, answers=None):
    """Score a firing multiset against the corpus's exact satisfaction points.

    `fires` is a list of `(iid, caller_index)`. `answers` optionally overrides the
    P1/P2 outcome for a policy that fires correctly but answers badly; by default
    a policy is credited with answering exactly what its own firings support.

    Two readings are returned. The **binding** one is `§5 L5`'s: a fire is correct
    only if it is the intention's *only* fire and lands on its sigma. The
    **charitable** one (`precision_any`, `recall_any`) drops the exactly-once
    requirement and asks only whether *some* fire landed on the sigma; it is a
    diagnostic, never a gate, and it exists so the table can show precisely which
    clause of the identity defeats each cheap trick.
    """
    b = corpus()
    sat = b["sat"]

    per = collections.OrderedDict()
    for iid, k in fires:
        per.setdefault(iid, []).append(k)

    n_fires = len(fires)
    distinct = len(per)
    dup_fire = n_fires - distinct
    correct = [iid for iid, ks in per.items()
               if len(ks) == 1 and sat.get(iid) is not None and ks[0] == sat[iid]]
    hit_any = [iid for iid, ks in per.items()
               if sat.get(iid) is not None and sat[iid] in ks]
    landed = sum(1 for iid, ks in per.items()
                 for k in ks if sat.get(iid) is not None and k == sat[iid])
    miss = sum(1 for iid in b["fireable"] if iid not in per)

    if answers is None:
        answers = _default_answers(per, correct)
    f_num, f_den = answers

    return _row(n_fires, distinct, len(correct), len(hit_any), landed,
                dup_fire, miss, f_num, f_den)


def _row(n_fires, distinct, correct, hit_any, landed, dup_fire, miss,
         f_num, f_den):
    """Assemble one scored row. Split out so an analytic baseline builds the same
    shape without materializing a multiset it would take millions of pairs to hold."""
    b = corpus()
    n_fireable = len(b["fireable"])
    return {
        "fires": n_fires,
        "distinct": distinct,
        "correct": correct,
        "precision": None if n_fires == 0 else permille(Fraction(correct, n_fires)),
        "recall": permille(Fraction(correct, n_fireable)),
        "precision_any": None if n_fires == 0 else permille(Fraction(landed, n_fires)),
        "recall_any": permille(Fraction(hit_any, n_fireable)),
        "dup_fire": dup_fire,
        "miss": miss,
        "F": permille(Fraction(f_num, f_den * 1000)),
    }


def _default_answers(per, correct):
    """The §3.0 numerator/denominator of the P1+P2 battery for a firing policy.

    P1: one per intention. A policy that fired intention `i` exactly at `sigma(i)`
        answers it correctly (1000). A policy that fired it elsewhere, or more than
        once, answers wrongly (0). A policy that did not fire a fireable intention
        abstains (100). A policy that did not fire a never-fires intention abstains
        on an unanswerable query, which is the correct behaviour (1000); one that
        fired it answered an unanswerable query (0).
    P2: one per fired event actually emitted. A fired event emitted at the right
        place carries the intended payload verbatim (1000); one emitted elsewhere
        is scored on the same terms as its P1 (0), since read(t) then returns a
        payload for an event that should not exist.
    """
    b = corpus()
    good = set(correct)
    total = 0
    n = 0

    for iid in b["intents"]:
        n += 1
        fired = iid in per
        if b["sat"][iid] is None:
            total += 0 if fired else 1000
        elif iid in good:
            total += 1000
        elif fired:
            total += 0
        else:
            total += 100

    for iid, ks in per.items():
        for _k in ks:
            n += 1
            total += 1000 if iid in good and len(ks) == 1 else 0

    return (total, n)


# ---- the oracle: an exhibited witness ---------------------------------------

def oracle_fires():
    """The firing schedule that attains the identity: each intention at its sigma."""
    b = corpus()
    return [(iid, k) for k, iids in b["by_index"].items() for iid in iids]


# ---- pricing, under rule P (R4 clause 3: one cell, one grammar atom) --------

# A stored row's *shape* — its kind tag and its field names — is paid once per
# distinct shape, not per row. This is the Layer-4 row codec (`README-l4 §1.3`),
# and the L4 STRAIN session's 124-cell under-report is why it is stated here
# rather than assumed.
PENDING_SHAPE_CELLS = 4        # {kind tag, k0, cond, fire_text_id} field names
FIRED_SHAPE_CELLS = 3          # {kind tag, t, text_id} field names


def cond_cells(cond):
    """Cells for one stored condition AST, priced under rule P."""
    return payload_cost(cond)


def pending_entry_cells(iid):
    """Cells for one pending-set entry: its key, its k0, its condition, its fire id."""
    b = corpus()
    rec = b["intents"][iid]
    return 1 + 1 + cond_cells(rec["cond"]) + 1


def pending_cells(iids):
    return sum(pending_entry_cells(i) for i in iids)


def fired_row_cells(count):
    """Cells for `count` fired-event rows: iid key + engine t + text_id."""
    return 3 * count


def counter_cells():
    """Two cells per grammar kind — the fold `count_ge` reads (`§5 L5` band 3)."""
    from corpora.l5stream import generator as gen
    return 2 * len(gen.KINDS)


def witness_minimal():
    """W1 — the prospection-only witness: the cheapest state that attains the identity.

    It carries the pending set, the per-kind counters `count_ge` folds over, and
    one row per fired event so P1 and P2 are answerable. It carries **nothing
    else** — no interval table, no episode, no cue index. It is exhibited to make
    the ceiling a state that exists rather than a family maximization, and to make
    the policy class honest: this is what `§5 L5`'s gate, read literally, asks for.
    """
    b = corpus()
    peak = _peak_pending_cells()
    fired = fired_row_cells(len(b["fireable"]))
    shapes = PENDING_SHAPE_CELLS + FIRED_SHAPE_CELLS
    counters = counter_cells()
    return {
        "pending_peak_cells": peak,
        "pending_final_cells": pending_cells(b["never"]),
        "fired_rows": fired,
        "counters": counters,
        "shapes": shapes,
        "total_peak": peak + fired + counters + shapes,
        "total_final": pending_cells(b["never"]) + fired + counters + shapes,
    }


def joint_peak_prospection_cells():
    """The TRUE high-water mark of (pending set + fired rows) taken together.

    `witness_minimal` and `witness_full` price the peak pending set beside the
    FINAL fired-row count, which is the sum of two maxima that do not occur at the
    same caller index and is therefore an upper bound rather than a measurement.
    This is the measurement. Both are reported: the bound is what a budget must
    respect, and the gap between them is how much of the bound is slack.
    """
    b = corpus()
    live = []
    fired = 0
    best = 0
    starts = collections.defaultdict(list)
    for iid, rec in b["intents"].items():
        starts[rec["k0"]].append(iid)
    for k in range(b["n"]):
        done = b["by_index"].get(k, ())
        if done:
            live = [i for i in live if i not in set(done)]
            fired += len(done)
        live.extend(starts.get(k, ()))
        cells = pending_cells(live) + fired_row_cells(fired)
        if cells > best:
            best = cells
    return best


def _peak_pending_cells():
    """The largest the pending set ever gets, in cells rather than in entries.

    Measured over the same forward sweep the satisfaction points come from: an
    entry joins after its own caller index is scored and leaves at its sigma, so
    this is the exact high-water mark a lawful engine must fit under the cap.
    """
    b = corpus()
    live = []
    best = 0
    by_index = b["by_index"]
    starts = collections.defaultdict(list)
    for iid, rec in b["intents"].items():
        starts[rec["k0"]].append(iid)
    for k in range(b["n"]):
        done = set(by_index.get(k, ()))
        if done:
            live = [i for i in live if i not in done]
        live.extend(starts.get(k, ()))
        cells = pending_cells(live)
        if cells > best:
            best = cells
    return best


# ---- the Layer-4 substrate this layer stands on ----------------------------

def l4_substrate_cells():
    """The consolidated Layer-4 state for `l5stream`'s base stream, priced.

    The interval table over the assertion facet (`_l4tasks`' reading, unchanged),
    plus the global counters. This is what a Layer-5 engine is *also* still
    carrying, because Layer 5 does not repeal Layer 4 — the `inheritance/` class
    exists to say so. `l5stream` is not the corpus the ratified Layer-4 gate binds
    on (R4 clause 1 binds it to `l4stream`), so nothing here applies that gate;
    this is a price, not a score.
    """
    b = _l4_bundle()
    return (len(b["entities"]) + len(b["chains"]) + 2 * b["assertions"]
            + 2 * len(b["kinds"]))


def _l4_bundle():
    if "l4view" not in _CACHE:
        _CACHE["l4view"] = _l4tasks.build("l5stream", corpus()["payloads"])
    return _CACHE["l4view"]


# The Layer-4 operational bookkeeping the L4 Stage-A witness did not price and
# Stage C then had to find 656 cells for (BOUNDARY.log line 23). Carried forward
# by name so the same omission cannot be made twice.
def operational_bookkeeping_cells():
    """Per-entity irreducible counts, the key atlas, the demotion counter."""
    b = _l4_bundle()
    keys = set(k for _e, k in b["chains"])
    return {
        "per_entity_irreducible_counts": 3 * len(b["entities"]),
        "key_atlas": 2 * len(keys),
        "demotion_counter": 1,
    }


# The Layer-3 aggregated forgetting record: (count, mass) per t-range over 16
# buckets coarsened by doubling, 3 + 2*buckets cells (BOUNDARY.log line 17).
LOSS_RESERVE_CELLS = 3 + 2 * 16


def witness_full():
    """W2 — the honest witness: a Layer-4 state that also attains the Layer-5 identity.

    W1 shows the identity is reachable. W2 shows it is reachable **without
    repealing the layer below**, at the Layer-4 footprint ratio, with the
    operational bookkeeping and the loss-accounting reserve priced rather than
    assumed away. Its margin is the number Stage C inherits.
    """
    b = corpus()
    w1 = witness_minimal()
    book = operational_bookkeeping_cells()
    substrate = l4_substrate_cells()
    book_total = sum(book.values())
    prospection = w1["pending_peak_cells"] + w1["fired_rows"] + w1["shapes"]
    total = substrate + book_total + prospection + LOSS_RESERVE_CELLS
    return {
        "budget_cap": b["budget_cap"],
        "raw_cells": b["raw_cells"],
        "l4_substrate": substrate,
        "bookkeeping": book,
        "bookkeeping_total": book_total,
        "prospection": prospection,
        "loss_reserve": LOSS_RESERVE_CELLS,
        "total": total,
        "margin": b["budget_cap"] - total,
        "footprint_permille": permille(Fraction(total, b["raw_cells"])),
    }


# ---- the capability-free baselines R2 obligation 2 demands ------------------

def baseline_never_fire():
    """The policy with no trigger machinery at all — `make_engine(layer_cap = 4)`.

    Nothing is pending, so nothing fires. `§5.1 L5`: *"Consolidation summarizes the
    past and has no construct that watches future writes."* `README-l4 §4` states
    the same thing structurally, and predicts **0, not near 0**.
    """
    return score([])


def baseline_fire_on_every_write():
    """The cheap trick the directive names: fire every intention on EVERY later write.

    It is the policy that cannot miss. Under the charitable reading it has
    **perfect recall** — every sigma is among its firings, because every index
    after `k0` is — and that is exactly what makes it the right adversary for an
    exactness gate: the identity kills it on the other three clauses at once.

    Computed **analytically** rather than by materializing the multiset: an
    intention written at caller index `k0` fires at every index in `(k0, n)`, so it
    contributes `n - 1 - k0` firings and exactly one of them (its sigma, when it
    has one) lands. The brute-force construction over a declared prefix is asserted
    against this arithmetic in `ascension/l5/t_attainability.py` — one policy, two
    implementations, checked rather than assumed.
    """
    b = corpus()
    n = b["n"]
    n_fires = sum(n - 1 - rec["k0"] for rec in b["intents"].values())
    distinct = sum(1 for rec in b["intents"].values() if rec["k0"] < n - 1)
    n_fireable = len(b["fireable"])
    # Every fireable intention fires at its sigma (charitable hit) and also
    # everywhere else, so nothing is correct under the exactly-once rule.
    return _row(n_fires, distinct, 0, n_fireable, n_fireable,
                n_fires - distinct, 0,
                *_answers_all_wrong())


def _answers_all_wrong():
    """The §3.0 battery for a policy that fires every intention, none correctly.

    Every P1 is answered and every answer is wrong (0). P2 exists once per emitted
    fired event and every one of them is spurious (0). The numerator is therefore
    0 and only the denominator is interesting.
    """
    b = corpus()
    n = b["n"]
    n_fires = sum(n - 1 - rec["k0"] for rec in b["intents"].values())
    return (0, len(b["intents"]) + n_fires)


def brute_fire_on_every_write(m):
    """The same policy, built by construction over the first `m` caller events.

    Kept small on purpose: it exists only to check the analytic form above.
    """
    b = corpus()
    fires = []
    pending = []
    starts = collections.defaultdict(list)
    for iid, rec in b["intents"].items():
        if rec["k0"] < m:
            starts[rec["k0"]].append(iid)
    for k in range(m):
        for iid in pending:
            fires.append((iid, k))
        pending.extend(starts.get(k, ()))
    return fires


def baseline_fire_immediately():
    """Fire each intention at the very next caller write, condition unread.

    The honest zero-knowledge guess, and the one whose score is a property of the
    corpus rather than of a trick: it is right exactly for the intentions whose
    satisfaction point happens to be `k0 + 1`.
    """
    b = corpus()
    fires = []
    for iid, rec in b["intents"].items():
        k = rec["k0"] + 1
        if k < b["n"]:
            fires.append((iid, k))
    return score(fires)


def baseline_fire_on_kind_only():
    """Read only the `kind` atom of a condition; treat every other predicate as true.

    A partial-capability policy rather than a capability-free one, scored because
    R2 obligation 2 asks for *every trivial policy that could pass by accident*.
    It is the strongest cheap trick available: it fires on a real reading of the
    condition grammar, just not on all of it.
    """
    b = corpus()
    fires = []
    pending = []
    starts = collections.defaultdict(list)
    for iid, rec in b["intents"].items():
        starts[rec["k0"]].append(iid)
    counts = {}
    for k, p in enumerate(b["payloads"]):
        counts[p.get("kind")] = counts.get(p.get("kind"), 0) + 1
        hit = [iid for iid in pending
               if _kind_only(b["intents"][iid]["cond"], p)]
        for iid in hit:
            fires.append((iid, k))
        done = set(hit)
        if done:
            pending = [i for i in pending if i not in done]
        pending.extend(starts.get(k, ()))
    return score(fires)


def _kind_only(cond, payload):
    if "op" in cond:
        op, args = cond["op"], cond["args"]
        if op == "and":
            return all(_kind_only(a, payload) for a in args)
        if op == "or":
            return any(_kind_only(a, payload) for a in args)
        return not _kind_only(args[0], payload)
    if cond["p"] == "kind":
        return payload.get("kind") == cond["v"]
    return True


def baselines():
    return collections.OrderedDict((
        ("capped-4 (no trigger machinery)", baseline_never_fire()),
        ("fire-on-every-write", baseline_fire_on_every_write()),
        ("fire-immediately", baseline_fire_immediately()),
        ("fire-on-kind-atom-only", baseline_fire_on_kind_only()),
    ))


def oracle():
    """The exhibited witness's score — the identity, attained."""
    return score(oracle_fires())


def count_ge_conditions():
    """Intentions whose condition mentions the demoted-content predicate."""
    b = corpus()
    return [iid for iid, rec in b["intents"].items()
            if any(a["p"] == "count_ge" for a in atoms(rec["cond"]))]


def latency_profile():
    """How far after its own write each intention's satisfaction point lies."""
    b = corpus()
    out = collections.Counter()
    for iid, s in b["sat"].items():
        if s is None:
            out["never"] += 1
        else:
            d = s - b["intents"][iid]["k0"]
            out["next write" if d == 1 else ("<=10" if d <= 10 else
                 ("<=100" if d <= 100 else ">100"))] += 1
    return dict(out)


def _report():
    b = corpus()
    print("n %d  raw_cells %d  budget_cap %d" % (b["n"], b["raw_cells"], b["budget_cap"]))
    print("intentions %d  fireable %d  never %d"
          % (len(b["intents"]), len(b["fireable"]), len(b["never"])))
    multi = [k for k, v in b["by_index"].items() if len(v) > 1]
    print("multi-sat indices %d  max fan-out %d"
          % (len(multi), max((len(v) for v in b["by_index"].values()), default=0)))
    print("peak pending entries %d  final pending %d"
          % (b["peak_pending"], b["final_pending"]))
    print("kind counts", dict(sorted(b["kind_counts"].items())))
    print("count_ge conditions %d" % (len(count_ge_conditions()),))
    print("latency", latency_profile())
    l4 = _l4_bundle()
    print("l4 view: assertions %d  pairs %d  entities %d  irreducible %d"
          % (l4["assertions"], len(l4["chains"]), len(l4["entities"]),
             len(l4["irreducible"])))
    print("P1 %d  P2 %d" % (b["n_p1"], b["n_p2"]))
    print("oracle", oracle())
    print("W1", witness_minimal())
    print("W2", witness_full())
    for name, s in baselines().items():
        print("baseline %-34s %s" % (name, s))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, PROJECT_ROOT)
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "trials"))
    _report()

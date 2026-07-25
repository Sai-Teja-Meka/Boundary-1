"""trials/_l4tasks.py — the shared Layer-4 consolidation battery (engine-free).

Nothing here touches an engine, so it is importable before
`core/layers/l4_consolidation.py` exists — the trials-first step of the ASCEND
sequence (**BOUNDARY-RULINGS.md R2**). It carries three things the Layer-4 gate
rests on, in one place so they can never disagree:

1. **the facet map** — how the chronicle-family grammar is read as
   `(entity, key, value)` assertions;
2. **the Q1–Q4 battery** — what Layer 4 is asked, per corpus;
3. **the attainability arithmetic** — the footprint pricing, the oracle
   ceilings, and every named capability-free baseline, computed from the corpus
   and the frozen §4.1 cost model alone.

`trials/ascension/l4/ATTAINABILITY.md` is the prose of what this module
computes; `trials/ascension/l4/t_attainability.py` asserts that the two agree.

## The footprint reading (§5 L4, §5.1 L4)

`BOUNDARY.md §5 L4` gates on `footprint ≤ 250 (≥4× compression)` and `§5.1 L4`
defends it as *"Derived schemas must shrink the episodic footprint to at most a
quarter of the raw bytes."* Three ratified statements — `250`, `≥4×`, `a
quarter` — are one statement iff `250` is read in **permille**, the unit §3
establishes for every measure in the constitution (`1000/250 = 4`). So:

```
raw_cells      = Σ_t event_cost(payload_t)          the episodic footprint (§4.1)
footprint‰     = permille(state_cells / raw_cells)
gate           = footprint‰ ≤ 250     ==     state_cells ≤ raw_cells // 4
```

and the Layer-4 **budget cap is that same number**: `budget_cap = raw_cells //
4`. The footprint gate and the budget law (§4.1) are then the same sentence
read twice, and `B = 1000` certifies it held *after every write* rather than
only at the end. See `ATTAINABILITY.md §1` for the erratum this reading records
against `core/layers/README-l3.md §4`'s parenthetical "≤ 250 units".

## Pricing rule P — one cell, one grammar atom

The §4.1 cost model charges one cell per scalar and one per key, and says
nothing about what a scalar may *contain*. Unconstrained, a state could pack an
entire corpus into one integer and price it at one cell. **Pricing rule P**
closes that: every stored cell holds exactly one **grammar atom** — an entity
id, a vocabulary token, an attribute value, or a logical `t`. A composite key
(`"7:status"`), a bit-packed integer, or a concatenation carrying more than one
atom is priced at the number of atoms it carries.

Rule P is what makes the oracle below a *bound* rather than a wish, and it is
the constraint the Layer-4 engine will be held to structurally (Stage C).

## The battery

| facet | one query per | answer |
|---|---|---|
| **Q1** current-value | distinct `(entity, key)` pair | the value at the pair's greatest `t` |
| **Q2** as-of | **non-terminal** assertion | the value in force at that assertion's `t` |
| **Q3** pattern | entity, plus one per grammar kind | that entity's action-count profile / the global count |
| **Q4** reconstruction | event `t` | the payload of the event at `t` |

Q1–Q3 are the **coverage** battery (§3.2, uniform weight 1 — Layer 4 declares
no importance field). Q4 is scored by **fidelity** (§3.1).

**Q2 asks only about the past.** A pair's terminal assertion is excluded,
because as-of *at the latest `t`* is the Q1 question wearing a `t`, and a
current-value table with no history at all would answer it. A pair asserted
exactly once therefore contributes no Q2 query. This is what makes Q2 a test of
attribute **history** — the Graphiti steal (GAPMAP **S3**) — rather than a
second copy of Q1.

## `F` at Layer 4 is the literal §3.0 table

**R3 does not reach Layer 4** — it says so itself: *"It does not reach layers
where eviction is not compulsory. Layers 1, 2, 4, 5, 6 and 7 score F under the
literal §3.0 table unless and until a later ruling says otherwise."* So `F` here
scores an abstention on an answerable query at **100**, not 1000, and no ruling
is requested to change that: `ATTAINABILITY.md` shows the `F ≥ 900` gate is
attainable on the binding corpus under the literal table, so the layer does not
need the friendlier reading and does not ask for it. The corruption reading is
computed alongside as the ungated diagnostic `F_corruption`, inverting R3's
pairing so that the *stricter* number is the one that binds.
"""

import collections
import json
import os
from fractions import Fraction

from core.state import event_cost

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def permille(x):
    """Exact Fraction in [0,1] -> integer permille, round-half-to-even (§3.5)."""
    n = x * 1000
    q = n.numerator // n.denominator
    r = n - q
    if r < Fraction(1, 2):
        return q
    if r > Fraction(1, 2):
        return q + 1
    return q if q % 2 == 0 else q + 1


# ---- the facet map ---------------------------------------------------------

LIFECYCLE_CLASS = "class"
LIFECYCLE_LOC = "loc"
LIFECYCLE_LIVE = "live"


def facet(payload):
    """Read one chronicle-family payload as an `(entity, key, value)` assertion.

    Returns `None` for an event the assertion grammar cannot express — murk's
    malformed payloads and `l4stream`'s `note` events. Those are the
    **irreducible** tier: nothing in a schema regenerates them, so they are the
    honest floor under reconstruction fidelity.
    """
    kind = payload.get("kind")
    entity = payload.get("entity")
    if kind == "attr":
        if isinstance(entity, int) and isinstance(payload.get("key"), str) \
                and "val" in payload:
            return (entity, payload["key"], payload["val"])
        return None
    if kind == "move" and isinstance(entity, int):
        return (entity, LIFECYCLE_LOC, payload["loc"])
    if kind == "spawn" and isinstance(entity, int):
        return (entity, LIFECYCLE_CLASS, payload["class"])
    if kind == "retire" and isinstance(entity, int):
        return (entity, LIFECYCLE_LIVE, 0)
    if kind == "link":
        src, dst = payload.get("src"), payload.get("dst")
        if isinstance(src, int) and isinstance(dst, int) \
                and isinstance(payload.get("rel"), str):
            return (src, payload["rel"], dst)
        return None
    return None


# ---- the corpora this battery is defined over ------------------------------

CORPORA = ("l4stream", "chronicle", "murk")

_CACHE = {}


def _payloads(name):
    if name == "l4stream":
        from corpora.l4stream import generator as gen
        return list(gen.generate(gen.SEED, gen.N))
    if name == "chronicle":
        from corpora.chronicle import generator as gen
    elif name == "murk":
        from corpora.murk import generator as gen
    else:
        raise KeyError(name)
    with open(gen.FROZEN_PATH, "r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def _build(name):
    payloads = _payloads(name)
    n = len(payloads)
    raw_cells = sum(event_cost(p) for p in payloads)

    chains = collections.OrderedDict()   # (entity, key) -> [(t, value), ...]
    irreducible = []                     # t of every event with no facet
    kinds = collections.OrderedDict()    # kind -> count
    profile = collections.OrderedDict()  # entity -> OrderedDict(kind -> count)

    for t, payload in enumerate(payloads):
        kind = payload.get("kind")
        kinds[kind] = kinds.get(kind, 0) + 1
        f = facet(payload)
        if f is None:
            irreducible.append(t)
        else:
            chains.setdefault((f[0], f[1]), []).append((t, f[2]))
        who = payload.get("entity")
        if not isinstance(who, int):
            who = payload.get("src")
        if isinstance(who, int):
            per = profile.setdefault(who, collections.OrderedDict())
            per[kind] = per.get(kind, 0) + 1

    entities = sorted(set(k[0] for k in chains))
    assertions = sum(len(v) for v in chains.values())

    n_q1 = len(chains)
    n_q2 = assertions - len(chains)          # non-terminal assertions only
    n_q3 = len(entities) + len(kinds)
    n_q4 = n

    return {
        "name": name,
        "n": n,
        "raw_cells": raw_cells,
        "budget_cap": raw_cells // 4,        # footprint <= 250permille (§5 L4)
        "chains": chains,
        "irreducible": irreducible,
        "kinds": kinds,
        "profile": profile,
        "entities": entities,
        "assertions": assertions,
        "n_q1": n_q1,
        "n_q2": n_q2,
        "n_q3": n_q3,
        "n_q4": n_q4,
        "n_coverage": n_q1 + n_q2 + n_q3,
    }


def corpus(name):
    """The deterministic Layer-4 bundle for one corpus (built once, cached)."""
    if name not in _CACHE:
        _CACHE[name] = _build(name)
    return _CACHE[name]


# ---- the exact minimal-sufficient state (priced under rule P) --------------

def interval_table_cells(name):
    """Cells for the exact attribute-history schema `{e: {k: [[t, v], ...]}}`.

    One cell per entity (its key in the outer table), one per `(entity, key)`
    pair (its key in the inner table), and two per assertion (`t` and the
    value). This is the **exact** Q1+Q2+Q3-sufficient state: current value is
    the chain's last entry, as-of is an interval lookup, and every pattern
    query — action counts, participation sets — is a fold over the chains.
    """
    b = corpus(name)
    return len(b["entities"]) + len(b["chains"]) + 2 * b["assertions"]


def current_value_table_cells(name):
    """Cells for the current-value-only schema `{e: {k: v}}` — Q1 and nothing else."""
    b = corpus(name)
    return len(b["entities"]) + 2 * len(b["chains"])


def global_counts_cells(name):
    """Cells for the global per-kind counters `{kind: count}` — two per kind."""
    return 2 * len(corpus(name)["kinds"])


def minimal_sufficient_cells(name):
    """The cheapest state answering **all** of Q1, Q2 and Q3 exactly."""
    return interval_table_cells(name) + global_counts_cells(name)


# ---- the oracle: the declared construct family, exactly maximized ----------
#
# **Construct family F** — declared here, so the ceiling below is a statement
# with a scope rather than an intuition. A state is a choice of:
#
#   * per entity touched : 1 cell — its key in the outer table.
#   * per pair, one of
#       CURRENT  2 cells (the pair's key cell + one value cell)
#                -> answers Q1(p). Stores no `t`, so it reconstructs nothing:
#                   `reconstruction(t)` must name the event AT `t`.
#       FULL     1 + 2c cells (the key cell + `c` × `[t, value]`)
#                -> answers Q1(p), the c−1 past-facing Q2 queries of p, and
#                   reconstructs all c of its events.
#   * per entity : Q3(e) is FREE when every pair of e is FULL (an action-count
#                  profile is a fold over complete chains); otherwise it costs
#                  `kinds(e) + 1` cells and is bought only if that is cheaper.
#   * global     : 2 cells per grammar kind -> the K global-count queries.
#   * per irreducible event : 3 cells (`[t, entity, id]`) -> its reconstruction.
#
# **Why a partial history is not in F.** For a pair with chain `c`, storing a
# suffix of depth `k` costs `1 + 2k` and answers `k` coverage queries, a ratio
# `k/(1+2k)` strictly increasing in `k`. So among the history constructs only
# `k = c` is ever on the frontier, and `CURRENT` (ratio 1/2) strictly dominates
# every one of them. That is why the greedy below — open every pair at CURRENT,
# then upgrade whole chains in descending length — is **exact within F**, not a
# heuristic.
#
# **What lies outside F.** A positional encoding (a dense array over the pair
# universe, position implying identity and so charging no key cell) is legal
# under rule P and is *cheaper* than CURRENT. It does not change any verdict
# here: on `l4stream` the family ceiling is already attained by an exhibited
# state (`witness`), and on the chronicle family the pair universe is not
# bounded by the grammar — entity ids are discovered from the data — so a dense
# array over `entities × keys` costs 9985 × 18 = 179 730 cells against a 98 908
# budget, nearly twice the whole footprint. Recorded so the family's edge is
# stated rather than assumed away.


def oracle(name):
    """Exact ceilings on C and on F at footprint ≤ 250‰, over the family F above."""
    b = corpus(name)
    budget = b["budget_cap"]
    chains = b["chains"]
    n_irr = len(b["irreducible"])
    n4 = b["n_q4"]

    # ---- max coverage -----------------------------------------------------
    room = budget - len(b["entities"])
    answered = 0
    full = set()
    if room > 0:
        opened = min(len(chains), room // 2)
        answered += opened
        room -= 2 * opened
        if opened == len(chains):
            # upgrade whole chains, longest first: +（2c−1) cells for +(c−1)
            order = sorted(chains.items(), key=lambda kv: -len(kv[1]))
            for pair, chain in order:
                c = len(chain)
                if c < 2 or room < 2 * c - 1:
                    continue
                room -= 2 * c - 1
                answered += c - 1
                full.add(pair)
            # per-entity Q3, free where every pair of the entity went FULL
            by_entity = collections.defaultdict(list)
            for pair in chains:
                by_entity[pair[0]].append(pair)
            for who, pairs in by_entity.items():
                if all(p in full for p in pairs):
                    answered += 1
                else:
                    cost = len(b["profile"].get(who, {})) + 1
                    if room >= cost:
                        room -= cost
                        answered += 1
        if room >= global_counts_cells(name):
            room -= global_counts_cells(name)
            answered += len(b["kinds"])
    max_cov = permille(Fraction(min(answered, b["n_coverage"]), b["n_coverage"]))

    # ---- max reconstruction ----------------------------------------------
    # Only FULL chains and stored irreducibles reconstruct. A chain of length c
    # costs 1 + 2c and yields c reconstructions, so short chains are the worst
    # buy: take them longest-first, then irreducibles at 3 cells each.
    room = budget - len(b["entities"])
    exact = 0
    for _pair, chain in sorted(chains.items(), key=lambda kv: -len(kv[1])):
        c = len(chain)
        if room < 1 + 2 * c:
            continue
        room -= 1 + 2 * c
        exact += c
    exact += min(n_irr, max(0, room) // 3)
    exact = min(exact, n4)
    max_f = permille(Fraction(exact * 1000 + (n4 - exact) * 100, n4 * 1000))

    minimal = minimal_sufficient_cells(name)
    return {
        "corpus": name,
        "budget_cap": budget,
        "raw_cells": b["raw_cells"],
        "max_coverage_permille": max_cov,
        "max_reconstruction_F_permille": max_f,
        "max_reconstruction_exact": exact,
        "minimal_sufficient_cells": minimal,
        "minimal_sufficient_permille": permille(Fraction(minimal, b["raw_cells"])),
        "joint_feasible": minimal <= budget,
        "spare_cells": budget - minimal,
    }


def witness(name):
    """A CONCRETE state at footprint ≤ 250‰, and exactly what it answers.

    Not an estimate and not a family argument — an exhibited state, so the
    "the gate lies strictly below the oracle" half of R2 needs no modelling
    assumption on the corpus where it matters. The state is:

        the exact interval table  +  the global per-kind counters
        +  as many irreducible events as the remaining cells buy

    It answers **every** coverage query (Q1 from each chain's last entry, Q2 by
    interval lookup, Q3 by folding complete chains) and reconstructs every
    assertion event plus the irreducibles it could afford.

    Returns `None` where the interval table does not fit — on such a corpus
    there is no state in the family answering the whole battery at all, which
    is itself the finding.
    """
    b = corpus(name)
    budget = b["budget_cap"]
    base = minimal_sufficient_cells(name)
    if base > budget:
        return None
    spare = budget - base
    irr = min(len(b["irreducible"]), spare // 3)
    exact = b["assertions"] + irr
    n4 = b["n_q4"]
    return {
        "corpus": name,
        "cells": base + 3 * irr,
        "footprint_permille": permille(Fraction(base + 3 * irr, b["raw_cells"])),
        "coverage_permille": permille(
            Fraction(b["n_coverage"], b["n_coverage"])),
        "F_permille": permille(
            Fraction(exact * 1000 + (n4 - exact) * 100, n4 * 1000)),
        "F_corruption_permille": 1000,
        "reconstructed": exact,
        "irreducible_stored": irr,
        "irreducible_total": len(b["irreducible"]),
    }


# ---- the named capability-free baselines (R2 obligation 2) ----------------

def _score_kept_events(name, kept):
    """Score a policy that holds a set of raw event `t`s and answers from them."""
    b = corpus(name)
    q1 = sum(1 for chain in b["chains"].values() if chain[-1][0] in kept)
    q2 = sum(1 for chain in b["chains"].values()
             for t, _v in chain[:-1] if t in kept)
    # Q3 is zero for every event-holding policy: an action-count profile is a
    # fold over the WHOLE stream, so a policy holding a strict subset of the
    # events cannot produce a complete count — it can only produce a wrong one.
    q3 = 0
    exact = len(kept)
    n4 = b["n_q4"]
    return {
        "coverage_permille": permille(
            Fraction(q1 + q2 + q3, b["n_coverage"])),
        "F_permille": permille(
            Fraction(exact * 1000 + (n4 - exact) * 100, n4 * 1000)),
        "q1": q1, "q2": q2, "q3": q3, "kept": len(kept),
    }


def baseline_verbatim_truncation(name, keep="latest"):
    """(i) Keep whole raw events until the 250permille footprint is spent; answer episodically.

    `keep="latest"` is the stronger variant on every corpus measured (a current
    value is more likely to be the latest assertion), so it is the one the gate
    is checked against; `keep="first"` is reported for completeness.
    """
    b = corpus(name)
    payloads = _payloads(name)
    budget = b["budget_cap"]
    order = range(b["n"] - 1, -1, -1) if keep == "latest" else range(b["n"])
    spent = 0
    kept = set()
    for t in order:
        c = event_cost(payloads[t])
        if spent + c > budget:
            break
        spent += c
        kept.add(t)
    r = _score_kept_events(name, kept)
    r.update({"policy": "verbatim-truncation-%s" % keep, "cells": spent})
    return r


def baseline_current_value_table(name):
    """(ii) The current-value table alone: no history, no patterns.

    It answers every Q1 query and nothing else. It stores no `t`, so it
    reconstructs no event — including the very assertions whose values it
    holds, since `reconstruction(t)` must name the event at `t`.
    """
    b = corpus(name)
    n4 = b["n_q4"]
    return {
        "policy": "current-value-table-only",
        "cells": current_value_table_cells(name),
        "coverage_permille": permille(Fraction(b["n_q1"], b["n_coverage"])),
        "F_permille": permille(Fraction(0 * 1000 + n4 * 100, n4 * 1000)),
        "q1": b["n_q1"], "q2": 0, "q3": 0,
    }


def baseline_capped_l3(name):
    """(iii) The `layer_cap = 3` engine at footprint 250permille — an arithmetic UPPER bound.

    The Layer-3 state costs `event_cost(payload) + 1` per retained item (§0.5 of
    `core/layers/README-l3.md`: the event plus its single handle posting). The
    bound below retains the **cheapest** items first, which no importance
    ordering can beat on count, and then credits the capped engine with every
    query those retained events could conceivably support — Q1 wherever a pair's
    terminal assertion survives, Q2 wherever a non-terminal one does, and an
    exact reconstruction for every retained `t`. It is therefore a ceiling on
    the capped engine, not a measurement of one, which is what
    `humility/l4/IMPOSSIBILITY.md` needs.
    """
    b = corpus(name)
    payloads = _payloads(name)
    budget = b["budget_cap"]
    costs = sorted((event_cost(p) + 1, t) for t, p in enumerate(payloads))
    spent = 0
    kept = set()
    for c, t in costs:
        if spent + c > budget:
            break
        spent += c
        kept.add(t)
    r = _score_kept_events(name, kept)
    r.update({"policy": "capped-layer_cap-3", "cells": spent,
              "episodes_kept_permille": permille(Fraction(len(kept), b["n"]))})
    return r


def baselines(name):
    """Every named capability-free baseline, scored on one corpus."""
    return [
        baseline_verbatim_truncation(name, "latest"),
        baseline_verbatim_truncation(name, "first"),
        baseline_current_value_table(name),
        baseline_capped_l3(name),
    ]

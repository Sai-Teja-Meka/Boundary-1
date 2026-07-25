"""trials/_l4score.py — shared Layer-4 replay and scoring (BOUNDARY.md §3, §7).

The ascension trial, the humility trial and (from Stage C) the inheritance
battery all score the **same** Q1–Q4 battery through the **same** generic
interface (§6, §7) — the only difference is the engine behind `mk`: the
consolidation engine (`layer_cap = 4`) for ascension, the forget-only engine
(`layer_cap = 3`) for humility. Keeping replay and scoring in one place
guarantees they measure identically; the gate and the ceiling live in the
trials, and their authority lives in `laws/t_rulings.py`.

The battery's *shape* — which questions are asked, of which corpus, and how many
of each — is `_l4tasks`, which is engine-free and was frozen at Stage A. This
module adds only what an engine is needed for: the replay, the queries, and the
four measures. **No number here may change a denominator `_l4tasks` fixed**, or
`ATTAINABILITY.md`'s recorded arithmetic and `BOUNDARY-RULINGS.md R4`'s table
would stop describing what the trials measure.

## The battery, as queries

| facet | query | answer |
|---|---|---|
| **Q1** current-value | `{"op":"current","entity":E,"key":K}` | the value at the pair's greatest `t` |
| **Q2** as-of | `{"op":"asof","entity":E,"key":K,"t":T}` | the value in force at `T` |
| **Q3** pattern | `{"op":"profile","entity":E}` / `{"op":"count","kind":K}` | `{kind: count}` / an integer |
| **Q4** reconstruction | `{"op":"read","t":T}` | the event record `{"payload":…, "t":T}` |

**Q4 is deliberately the Layer-1 verb.** Reconstruction is not a new question;
it is `read(t)` asked after the episodes are gone. That choice is what makes the
humility measurement meaningful rather than definitional: the capped forget-only
engine answers `read` for every event it still retains and abstains for the
rest, which is exactly the arithmetic upper bound `_l4tasks.baseline_capped_l3`
prices (`event_cost + 1` per retained item, credited with every query those
events could support). An engine that consolidated instead of retaining answers
the same verb from its schemas.

## The measures, and how each is read at Layer 4

**Coverage (§3.2)** — the target set is Q1 ∪ Q2 ∪ Q3, uniform weight 1
(`l4stream` declares no importance field). An item is recovered when the engine
answers it correctly. The denominator is `_l4tasks`' `n_coverage`, fixed by the
corpus.

**Fidelity (§3.1)** — over Q4 alone, under the **literal §3.0 table**:

  * `read(t)`, exact event record returned → 1000
  * `read(t)`, engine abstains            →  100   (honest loss, still a loss)
  * `read(t)`, anything else returned     →    0   (corruption)

**R3 does not reach Layer 4 and R4 clause 4 declined to extend it**, so an
abstention on an answerable reconstruction scores 100 here and not 1000. The
corruption reading is computed alongside as the ungated diagnostic
`F_corruption` — R3's pairing **inverted**, so the stricter number binds and the
looser one is on display. `ATTAINABILITY.md §2` records the identity this makes
the gate mean: `F ≥ 900 ⟺ at least 8/9 of all events reconstructed exactly`,
less the half permille §3.5's rounding concedes.

**Budget (§3.3)** — occupancy is checked against the cap **after every single
write**, never once at the end, and `peak` is the running maximum. Under R4
clause 2 the cap *is* the footprint gate (`raw_cells // 4`), so `B = 1000` and
`footprint ≤ 250‰` are one constraint certified twice: once throughout the
stream, once on the final state.

**Footprint (§5 L4, R4 clauses 2 and 3)** — `permille(occupancy / raw_cells)`,
the engine's own §4.1 accounting against the raw episodic footprint. The atom
audit below is the part of pricing rule P a trial can check from outside an
engine; the rest is structural and is Stage C's obligation.

## The fabrication probes are a diagnostic, never a denominator

§3.0 scores fabrication at 0, so a battery with no unanswerable query cannot
tell an honest engine from a confident one. This module therefore also builds
**unanswerable probes** — pairs the corpus never asserts, as-of questions before
a pair's first assertion, reconstructions past the end of the stream, and a
count of a kind outside the grammar. They are scored **separately** and reported
as `fabricated`, and they are deliberately **not** folded into C or F: those
denominators are `_l4tasks`' and are cited by a frozen ruling. A trial asserts
`fabricated == 0`; the measure it would otherwise perturb stays exactly the
number Stage A computed.
"""

import collections
import json
from fractions import Fraction

import _l4tasks
from _l4tasks import permille
from core.state import payload_cost

# How many unanswerable probes of each shape to build (deterministic, ordered).
N_PROBES = 100

# The snapshot's fixed header — magic, layer cap, budget cap, occupancy, next_t,
# checksum — is bookkeeping about the state rather than stored grammar, so the
# rule-P atom audit allows this many cells for it before it calls an engine
# under-priced. Generous against a 43 300-cell budget, and still far tighter
# than any packing an engine could profit from.
RULE_P_HEADER_ALLOWANCE = 64


# ---- the battery, as queries ------------------------------------------------

def _coverage_tasks(b):
    """`[(query, expected_value, facet)]` for Q1, Q2 and Q3, in a fixed order."""
    tasks = []

    for (entity, key), chain in b["chains"].items():
        tasks.append(({"op": "current", "entity": entity, "key": key},
                      chain[-1][1], "q1"))

    for (entity, key), chain in b["chains"].items():
        for t, value in chain[:-1]:          # NON-terminal assertions only (§2)
            tasks.append(({"op": "asof", "entity": entity, "key": key, "t": t},
                          value, "q2"))

    for entity in b["entities"]:
        tasks.append(({"op": "profile", "entity": entity},
                      dict(b["profile"].get(entity, {})), "q3"))
    for kind, count in b["kinds"].items():
        tasks.append(({"op": "count", "kind": kind}, count, "q3"))

    return tasks


def _reconstruction_tasks(b):
    """`[(query, expected_event)]` for Q4 — one per event `t`, in `t` order."""
    return [({"op": "read", "t": t}, {"payload": p, "t": t})
            for t, p in enumerate(b["payloads"])]


def unanswerable_probes(b):
    """Queries whose only correct behaviour is abstention (§3.0), as a diagnostic.

    Four shapes, each derived from the frozen corpus so none of them can
    accidentally be answerable:

      * a `(entity, key)` pair the corpus never asserts — the entity exists and
        the key is in the corpus's own key vocabulary, so a partial match
        abounds and a full one does not;
      * an as-of question at a `t` **before** a pair's first assertion, where no
        value is yet in force;
      * a reconstruction past the end of the stream;
      * a count of a kind outside the grammar.
    """
    keys = sorted(set(k for _e, k in b["chains"]))
    asserted = set(b["chains"])

    probes = []
    for entity in b["entities"]:
        for key in keys:
            if (entity, key) not in asserted:
                probes.append({"op": "current", "entity": entity, "key": key})
                break
        if len(probes) >= N_PROBES:
            break

    before = 0
    for (entity, key), chain in b["chains"].items():
        first = chain[0][0]
        if first > 0:
            probes.append({"op": "asof", "entity": entity, "key": key,
                           "t": first - 1})
            before += 1
        if before >= N_PROBES:
            break

    n = b["n"]
    probes.extend({"op": "read", "t": n + k} for k in range(N_PROBES))
    probes.append({"op": "count", "kind": "no_such_kind"})
    return probes


# ---- replay -----------------------------------------------------------------

def replay(engine, mk, b):
    """Ingest a whole bundle at the Layer-4 cap; assert the cap held every write.

    Returns `(state, report)`. The cap is `raw_cells // 4` — R4 clause 2's
    single number, the footprint gate and the §4.1 budget cap at once — so an
    engine that would exceed the footprint is caught *during* the stream by the
    budget law rather than at the end by the measure.
    """
    name = "%s[:%d]" % (b["name"], b["n"])
    cap = b["budget_cap"]
    payloads = b["payloads"]
    state = mk(cap)
    peak = 0
    refused = 0
    for i, payload in enumerate(payloads):
        state, t = engine.ingest(state, payload)
        if t is None:
            refused += 1
        occ = state.occupancy
        if occ > cap:
            raise AssertionError(
                "%s: occupancy %d exceeded the Layer-4 cap %d at write %d — the "
                "budget law broke mid-stream (§4.1), not merely at the end"
                % (name, occ, cap, i))
        if occ > peak:
            peak = occ
    b_permille = 1000 if peak <= cap else permille(Fraction(cap, peak))
    return state, {"peak": peak, "cap": cap, "refused": refused,
                   "B": b_permille, "corpus": b["name"], "n": b["n"]}


# ---- scoring ----------------------------------------------------------------

def _ask(engine, state, query):
    """One query through the generic interface; a raised query is a hard failure."""
    ans = engine.query(state, query)
    if not isinstance(ans, dict) or ans.get("status") not in ("answer", "abstain"):
        raise AssertionError("query %r returned a non-Answer: %r" % (query, ans))
    return ans


def score(engine, state, b):
    """Run the whole battery against `state`; return every measure and its parts."""
    recovered = 0
    cov_wrong = 0
    cov_abstained = 0
    by_facet = collections.OrderedDict((f, 0) for f in ("q1", "q2", "q3"))
    for query, expected, facet in _coverage_tasks(b):
        ans = _ask(engine, state, query)
        if ans["status"] == "answer" and ans["value"] == expected:
            recovered += 1
            by_facet[facet] += 1
        elif ans["status"] == "abstain":
            cov_abstained += 1
        else:
            cov_wrong += 1

    exact = 0
    rec_wrong = 0
    rec_abstained = 0
    for query, expected in _reconstruction_tasks(b):
        ans = _ask(engine, state, query)
        if ans["status"] == "answer" and ans["value"] == expected:
            exact += 1
        elif ans["status"] == "abstain":
            rec_abstained += 1
        else:
            rec_wrong += 1

    fabricated = 0
    probes = unanswerable_probes(b)
    for query in probes:
        if _ask(engine, state, query)["status"] != "abstain":
            fabricated += 1

    n_cov = b["n_coverage"]
    n4 = b["n_q4"]
    f_sum = exact * 1000 + rec_abstained * 100          # literal §3.0 (R4 cl. 4)
    f_corruption_sum = (exact + rec_abstained) * 1000   # R3's reading, ungated

    return {
        "corpus": b["name"],
        "n": b["n"],
        "C": permille(Fraction(recovered, n_cov)),
        "F": permille(Fraction(f_sum, n4 * 1000)),
        "F_corruption": permille(Fraction(f_corruption_sum, n4 * 1000)),
        "footprint": permille(Fraction(state.occupancy, b["raw_cells"])),
        "occupancy": state.occupancy,
        "raw_cells": b["raw_cells"],
        "budget_cap": b["budget_cap"],
        "recovered": recovered,
        "coverage_wrong": cov_wrong,
        "coverage_abstained": cov_abstained,
        "q1": by_facet["q1"], "q2": by_facet["q2"], "q3": by_facet["q3"],
        "n_q1": b["n_q1"], "n_q2": b["n_q2"], "n_q3": b["n_q3"],
        "n_coverage": n_cov,
        "reconstructed": exact,
        "reconstruction_wrong": rec_wrong,
        "reconstruction_abstained": rec_abstained,
        "n_q4": n4,
        "fabricated": fabricated,
        "n_probes": len(probes),
    }


# ---- the forget-only bound, at any scale (the humility ceiling's arithmetic) --

def forget_only_bound(b):
    """The best a forget-only engine can do on `b` at footprint 250‰.

    Identical in method to `_l4tasks.baseline_capped_l3`, which R4 clause 1
    tabulates on the whole of `l4stream` (200 / 325): price each retained item
    at `event_cost + 1` — the event plus its single handle posting
    (`core/layers/README-l3.md §0.5`) — retain the **cheapest** items first,
    which no importance ordering can beat *on count*, and credit an exact
    reconstruction for every retained `t`. What it adds is that it takes a
    **bundle**, so the same bound is available at the declared prefix scales the
    humility trial measures at; `humility/l4/t_consolidation.py` asserts that on
    the whole stream the two agree, so this is the same instrument and not a
    second one.

    It is a ceiling on the capped engine, not a measurement of one: a real
    importance ordering keeps a costlier mix and therefore fewer items.
    """
    from core.state import event_cost

    cap = b["budget_cap"]
    n4 = b["n_q4"]
    costs = sorted(event_cost(p) + 1 for p in b["payloads"])
    spent = 0
    kept = 0
    for c in costs:
        if spent + c > cap:
            break
        spent += c
        kept += 1
    return {
        "max_kept": kept,
        "episodes_kept_permille": permille(Fraction(kept, b["n"])),
        "F_bound": permille(Fraction(kept * 1000 + (n4 - kept) * 100, n4 * 1000)),
        "cells": spent,
    }


# ---- the rule-P atom audit (R4 clause 3, the part a trial can see) ----------

def snapshot_atoms(engine, state):
    """Grammar atoms in the engine's own serialized state, priced under §4.1.

    `payload_cost` charges one cell per scalar and one per key — which is
    exactly rule P's *"one cell, one grammar atom"* when each scalar carries one
    atom. So an engine whose snapshot contains materially more atoms than it
    charged itself for is under-reporting its footprint, and that is visible
    from outside the engine.

    What this cannot see is the other half of rule P: a *composite* scalar
    (`"7:status"`, a bit-packed integer) is one atom to `payload_cost` and two
    or more to rule P. R4 clause 3 rules that half structural — *"the Layer-4
    engine is to be held to it structurally when it is written"* — so it is
    Stage C's obligation and is recorded here rather than silently assumed.
    """
    return payload_cost(json.loads(engine.snapshot(state).decode("utf-8")))

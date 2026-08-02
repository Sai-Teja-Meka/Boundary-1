"""trials/_l6score.py — shared Layer-6 replay, observation and scoring (§3.4, §7).

`_l6btasks` is the round-2 Stage-A module: it reads the frozen artifact, declares
the reader, the evidence vocabulary and the policies, and computes `§3.4`'s three
quantities. `_l6tasks` is round 1's, and owns the measures themselves. This module
adds only what an **engine** is needed for — the replay, the queries, the reading
of `§7.2`'s Answer, and the assembly of the `(confidence, correct)` pairs those
measures already take.

**ONE INSTRUMENT.** `brier`, `ece`, `auroc` and `fidelity` are imported from
`_l6tasks` unchanged — the same functions round 1's oracle, round 2's exhibited
witness and every named capability-free baseline are scored by. Nothing here
re-derives a calibration quantity. An engine and a policy are therefore measured
by one ruler, which is the discipline `_l4score` set two layers down and
`_l5score` restated one layer down.

## The battery, as queries (the reading `ascension/l6/STAGE-B.md §2` declares)

Both artifacts speak the same two query shapes, and both are **Layer-4 verbs**:

| | query | answer |
|---|---|---|
| **current** | `{"op":"current","entity":E,"key":K}` | the value in force at the end of the stream |
| **asof** | `{"op":"asof","entity":E,"key":K,"t":T}` | the value in force at `T` |

That is deliberate. `§5 L6` asks for *"confidence permille from structural
evidence"* — a **confidence model, not a second reader** — so the battery asks
questions the layer below already answers and scores the *confidence* attached to
them. A Layer-6 engine that improved the answers would be answering a different
gate's question; a Layer-6 engine that changed them on the forcing region would
have read the answer key (`R7` clause 3(b), Theorem 2).

## The denominator, stated rather than inferred (`R7` clause 2)

`§3.4` computes Brier, ECE and AUROC over the `A` **answered** queries. An
abstention contributes to `§3.0`'s fidelity and to **no** calibration quantity.
So every bundle here declares, per query class, whether that class scores inside
the denominator and why — `DENOMINATOR` below — and `score` returns `A`, `n_pos`
and `n_neg` beside the triple in the same dict, never behind an accessor.

A class declared **outside** is outside because it is unanswerable and an
abstention carries no confidence to calibrate. It is not a hiding place: an
engine that *answers* one has fabricated, and a fabrication enters `A` as an
error exactly as `_l6btasks.score` scores it. Being outside the denominator is a
property of the honest behaviour, not an exemption from measurement.

## What this module does not do

It applies no gate and declares no threshold. The gates live in
`ascension/l6/t_meta_memory.py`, the ceiling in `humility/l6/t_meta_memory.py`,
and their authority in `laws/t_rulings.py`.
"""

from fractions import Fraction

import _l6btasks
import _l6tasks

# ONE INSTRUMENT — §3.4's three quantities and §3.1's fidelity, imported and not
# re-derived. `permille` is §3.5's round-half-to-even on an exact Fraction.
from _l6tasks import brier, ece, auroc, fidelity, permille  # noqa: F401

# Per query class: does this class score inside `§3.4`'s denominator? (`R7`
# clause 2 requires the declaration; the reason travels with it.)
DENOMINATOR = {
    # battery-b (`corpora/l6batteryb`) — the artifact `R7` clause 1 binds
    "l6batteryb": {
        "K0": (True, "the forcing region: answerable, and the whole of it — a "
                     "committing engine's answers land in the denominator and "
                     "exactly one member of every pair it commits on is wrong "
                     "(R7 clause 3(b), Theorem 1)"),
        "K2": (True, "current-value over ordinary chains: answerable"),
        "K3": (True, "as-of at a non-terminal assertion: answerable"),
        "K4": (False, "absence probes: unanswerable, so the only correct "
                      "behaviour is an abstention and an abstention carries no "
                      "confidence to calibrate. An ANSWER here is a fabrication "
                      "and enters A as an error"),
    },
    # round 1's `corpora/l6battery` — DEMOTED to an ungated diagnostic by `R7`
    # clause 1. Scored, never gated; the class duty is unchanged by the demotion.
    "l6battery": {
        "K1": (True, "the commitment class: answerable, and the whole of it"),
        "K2": (True, "current-value over non-`origin` chains: answerable"),
        "K3": (True, "as-of at a non-terminal assertion: answerable"),
        "K4": (False, "absence probes: unanswerable — outside for battery-b's "
                      "reason, in the artifact that first stated it"),
    },
}

_CACHE = {}


# ---- the bundles -----------------------------------------------------------

def _bundle(name, payloads, records, region_pairs=None):
    classes = {}
    for rec in records:
        classes[rec["class"]] = classes.get(rec["class"], 0) + 1
    declared = DENOMINATOR[name]
    if sorted(classes) != sorted(declared):
        raise AssertionError(
            "%s: the artifact carries query classes %r but the denominator "
            "declaration covers %r — R7 clause 2 requires a battery to declare "
            "for EVERY class whether it scores inside `§3.4`'s denominator"
            % (name, sorted(classes), sorted(declared)))
    return {
        "name": name,
        "payloads": payloads,
        "records": records,
        "n": len(records),
        "n_events": len(payloads),
        "classes": classes,
        "n_answerable": sum(1 for r in records if r["answerable"]),
        "region_pairs": region_pairs,
    }


def battery_b():
    """`corpora/l6batteryb` — the artifact both sides of the gate bind on (R7 c1)."""
    if "l6batteryb" not in _CACHE:
        _CACHE["l6batteryb"] = _bundle(
            "l6batteryb", _l6btasks.stream(), _l6btasks.queries(),
            region_pairs=_l6btasks.region_pairs())
    return _CACHE["l6batteryb"]


def battery_one():
    """`corpora/l6battery` — round 1's artifact, an UNGATED DIAGNOSTIC (R7 c1).

    Demotion is a change of authority and never of bytes: this bundle is built
    from the same frozen instance round 1 scored, through the same reader, and
    what it lost is the right to gate. The Layer-6 battery still scores it and
    still reports it, which is the duty `R1` clause 5 and `R4` clause 1 attach to
    a demoted corpus — the chronicle pattern, one layer up.
    """
    if "l6battery" not in _CACHE:
        _CACHE["l6battery"] = _bundle(
            "l6battery", _l6tasks.murk_payloads(), _l6tasks.battery()["queries"])
    return _CACHE["l6battery"]


BATTERIES = {"l6batteryb": battery_b, "l6battery": battery_one}


# ---- replay ----------------------------------------------------------------

def replay(engine, mk, b, cap):
    """Ingest the whole stream at `cap`; assert the cap held after **every** write.

    `B = 1000` is certified after every single write and never once at the end:
    the budget law refuses mid-stream (`§4.1.2`), so a state that would exceed
    the cap must be caught where it happens rather than discovered late by a
    measure.

    `§5 L6` states **no footprint clause** — `R7` says so again in its own text
    and creates none — so both artifacts are scored **in budget**, and the caller
    passes the engine's own `DEFAULT_BUDGET`. What an engine owes when the budget
    sheds the evidence a confidence model reads is expressly left open by
    `ATTAINABILITY-B.md §3.2` and by `R7`'s *"what this ruling does not do"*.
    """
    state = mk(cap)
    peak = 0
    refused = 0
    for i, payload in enumerate(b["payloads"]):
        state, t = engine.ingest(state, payload)
        if t is None:
            refused += 1
        occ = state.occupancy
        if occ > cap:
            raise AssertionError(
                "%s: occupancy %d exceeded the cap %d at write %d — the budget "
                "law broke mid-stream (§4.1), not merely at the end"
                % (b["name"], occ, cap, i))
        if occ > peak:
            peak = occ
    return state, {
        "peak": peak, "cap": cap, "refused": refused,
        "B": 1000 if peak <= cap else permille(Fraction(cap, peak)),
        "occupancy": state.occupancy,
        "next_t": state.next_t,
    }


# ---- observation -----------------------------------------------------------

def _ask(engine, state, query):
    """One query through `§7`, with `§7.2`'s Answer contract enforced.

    A raised query is a harness-level failure and categorically worse than a
    scored abstention (`§7.3`), so it is not caught here. What *is* checked is
    the shape `§5 L6` newly depends on: **`confidence` is an integer permille in
    `[0, 1000]`**. Before Layer 6 that field was emitted and ungated (`§3.4`'s
    dormancy), so nothing had ever read it; from Layer 6 it is a scored quantity,
    and a float there would break `§2.2`'s prohibition as well as `§3.4`'s
    arithmetic. A `bool` is rejected explicitly because `True == 1` in Python and
    a confidence of `True` is not a permille.
    """
    ans = engine.query(state, query)
    if not isinstance(ans, dict) or ans.get("status") not in ("answer", "abstain"):
        raise AssertionError("query %r returned a non-Answer: %r" % (query, ans))
    conf = ans.get("confidence")
    if isinstance(conf, bool) or not isinstance(conf, int):
        raise AssertionError(
            "query %r returned confidence %r — §7.2 declares an INTEGER permille "
            "in [0, 1000] and §2.2 forbids a float anywhere in core; from Layer 6 "
            "that field is scored (§3.4) and is no longer decorative"
            % (query, conf))
    if not 0 <= conf <= 1000:
        raise AssertionError(
            "query %r returned confidence %d, outside §7.2's [0, 1000]"
            % (query, conf))
    return ans


def observe(engine, state, b):
    """Ask every query and record what came back. Nothing here scores.

    Correctness is judged against the **frozen artifact's own answer key**, never
    against the engine's belief and never against the declared reader: an
    answerable query is correct when the value matches the key, an unanswerable
    one when the engine abstains (`§3.0`'s two 1000-rows).
    """
    rows = []
    for rec in b["records"]:
        ans = _ask(engine, state, rec["q"])
        status = ans["status"]
        if rec["answerable"]:
            correct = (status == "answer" and ans["value"] == rec["value"])
        else:
            correct = (status == "abstain")
        rows.append({
            "qid": rec["qid"],
            "cls": rec["class"],
            "entity": rec["q"].get("entity"),
            "answerable": rec["answerable"],
            "status": status,
            "value": ans["value"] if status == "answer" else None,
            "confidence": ans["confidence"],
            "correct": correct,
        })
    return rows


# ---- scoring ---------------------------------------------------------------

def score(rows, b):
    """`§3.4`'s triple and `§3.1`'s fidelity, with the denominator stated beside them.

    `F_core` is fidelity over the **answerable core** — the denominator every
    piece of the ratified band arithmetic is stated in (`R7` clause 3(c):
    `1000w ≤ 50` with `w = (r/2)/A`), and the stricter of the two. `F_all` is
    fidelity over the whole query set as `§3.1` writes it, and is reported as an
    ungated diagnostic: the unanswerable class scores 1000 for an abstention, so
    including it can only raise the number, and a battery that gated on the
    looser one would be spending a margin the window arithmetic never granted.
    """
    answered = []
    scored_core = []
    scored_all = []
    wrong = 0
    fabricated = 0
    abstentions = 0
    confidences = set()
    by_class = {}

    for row in rows:
        confidences.add(row["confidence"])
        hit, miss, held = by_class.get(row["cls"], (0, 0, 0))
        if row["status"] == "answer":
            answered.append((row["confidence"], row["correct"]))
            if not row["answerable"]:
                fabricated += 1
            if not row["correct"]:
                wrong += 1
            s = 1000 if row["correct"] else 0
            if row["correct"]:
                hit += 1
            else:
                miss += 1
        else:
            abstentions += 1
            s = 1000 if not row["answerable"] else 100
            held += 1
        by_class[row["cls"]] = (hit, miss, held)
        scored_all.append(s)
        if row["answerable"]:
            scored_core.append(s)

    n_pos = sum(1 for _c, ok in answered if ok)
    n_neg = len(answered) - n_pos
    return {
        "artifact": b["name"],
        "N": len(rows),
        "A": len(answered),
        "n_pos": n_pos,
        "n_neg": n_neg,
        "wrong": wrong,
        "fabricated": fabricated,
        "abstentions": abstentions,
        "confidences": tuple(sorted(confidences)),
        "by_class": by_class,
        "brier": brier(answered),
        "ece": ece(answered),
        "auroc": auroc(answered),
        "F_core": fidelity(scored_core),
        "F_all": fidelity(scored_all),
    }


def assert_denominator_declared(figures, rows, b):
    """`R7` clause 2, made a check rather than a promise.

    `A` is the count of ANSWERED queries and nothing else, and it is reconciled
    against the classes the bundle declares: every class declared inside
    contributes its answered queries, every class declared outside contributes
    only what the engine **fabricated** there. An `A` that could not be rebuilt
    from the declaration would mean the battery was reporting a denominator it
    had not declared.
    """
    inside = 0
    outside_answered = 0
    for row in rows:
        in_denominator, _why = DENOMINATOR[b["name"]][row["cls"]]
        if row["status"] != "answer":
            continue
        if in_denominator:
            inside += 1
        else:
            outside_answered += 1
    if figures["A"] != inside + outside_answered:
        raise AssertionError(
            "%s: A = %d cannot be rebuilt from the declared classes (%d inside, "
            "%d answered in a class declared outside)"
            % (b["name"], figures["A"], inside, outside_answered))
    if outside_answered != figures["fabricated"]:
        raise AssertionError(
            "%s: %d queries were answered in a class declared OUTSIDE the "
            "denominator but only %d were booked as fabrications — a class is "
            "outside because it is unanswerable, so answering one is §3.0's "
            "fabrication row and not a quiet extra"
            % (b["name"], outside_answered, figures["fabricated"]))
    return {"inside": inside, "fabricated_outside": outside_answered}


# ---- the forcing region ----------------------------------------------------

def region_profile(rows, b):
    """Per mirror pair: what the engine did with its two members.

    Returns `{pair index: {"answered": k, "correct": k, "confidences": (...)}}`
    for the artifact's forcing region, or raises where the artifact has none —
    the demoted diagnostic has no region, which is precisely why it was demoted.
    """
    if b["region_pairs"] is None:
        raise AssertionError(
            "%s carries no forcing region — R7 clause 3(b) is why a gate citing "
            "AUROC binds only on an artifact that does" % (b["name"],))
    by_entity = {row["entity"]: row for row in rows if row["cls"] == "K0"}
    profile = {}
    for p in b["region_pairs"]:
        members = [by_entity[p["e0"]], by_entity[p["e1"]]]
        answered = [m for m in members if m["status"] == "answer"]
        profile[p["pair"]] = {
            "answered": len(answered),
            "correct": sum(1 for m in members if m["correct"]),
            "confidences": tuple(m["confidence"] for m in answered),
        }
    return profile


def resolved_pairs(profile):
    """Pairs the engine got **both** members right on — the class-O tell.

    Theorem 2: the coin is not in the stream, so a policy that resolves a mirror
    pair obtained it from the answer key. An engine is a function of the frozen
    bytes (`§2.1`, `§2.3`), so a resolved pair is an engine that read something it
    was never handed.
    """
    return sorted(pair for pair, row in profile.items()
                  if row["answered"] == 2 and row["correct"] == 2)

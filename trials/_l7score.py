"""trials/_l7score.py — shared Layer-7 replay, observation and scoring (§5 L7, §7).

`_l7tasks` is the Stage-A module: it reads the frozen artifact, declares the
composition reading, the policies, the labeller bench and the measures, and
computes every figure `ATTAINABILITY.md` records with **no engine in the loop**.
This module adds only what an **engine** is needed for — the replay, the queries,
the reading of `§7.2`'s Answer plus the one field Layer 7 adds, the promotion
ladder driven through `ingest`, and the assembly of the quantities those measures
already take.

**ONE INSTRUMENT.** `brier`, `ece`, `auroc`, `fidelity` and `permille` are
imported from `_l7tasks`, which imports them from `_l6tasks` unchanged — the same
functions the exhibited witness, the oracle, both crimes, both hedgers and every
named capability-free baseline are scored by, and the same functions `_l6score`
scores a Layer-6 engine by. Nothing here re-derives a measure. An engine and a
policy are therefore measured by one ruler, which is the discipline `_l4score`
set three layers down and `_l5score` and `_l6score` restated.

## The battery, as queries (the reading `ascension/l7/STAGE-B.md §2` declares)

`corpora/l7compose` speaks **two** query shapes:

| | query | answer |
|---|---|---|
| **generate** | `{"op":"generate","cue":{"kind":"profile","entity":E}}` | the compound's `profile` item, its lineage, its confidence and its tag |
| **current** | `{"op":"current","entity":E,"key":K}` | the value in force at the end of the stream — a **Layer-4 verb**, unchanged |

`generate` is a `query` **op** and not a fourth verb (`R8` clause 2): `§7.1`
declares three operations and `§1.1` says events are the only fuel, so the only
reading under which `§5 L7`'s `generate(cue)` and `§7.1` are both true is this
one. The `current` class is carried for the same reason the Layer-6 battery
carried Layer-4 verbs: a layer's battery must still contain the questions the
layers below answer, or an engine could buy its new capability with an old one.

## The Answer, and the ONE field Layer 7 adds

`§7.2` declares four keys — `status`, `value`, `confidence`, `provenance`. `R8`
clause 2 ratifies that a `generate` Answer *"carries the item, its confidence,
its provenance tag and its lineage"*, and clause 4 rules what `lineage` is: a
property of the **item** (`observed` / `generated`), orthogonal to `§4.2.3`'s
closed four-kind vocabulary, which says how an answer reached the caller. So
`_ask` enforces:

* the four `§7.2` keys, `value = null` on an abstention;
* `confidence` an **integer permille** in `[0, 1000]` — a float, a `bool` or an
  out-of-range value is a harness-level failure and not a low score (`§7.3`'s
  categorical distinction; `§2.2` forbids the float independently);
* `lineage` **absent or `None`, or one of the two declared values**. An absent
  lineage is a lawful answer that makes no lineage claim — which is exactly the
  untagged case `§5 L7` prices at `tagging < 1000` — while a value outside the
  vocabulary is a contract violation and raises, in the shape the confidence
  check above already takes.
* an abstention carries no lineage, because an abstention returns no item to
  have one. That is `§7.2`'s own `value: null` rule applied to the field `R8`
  clause 2 adds beside it.

**The tag is read through `§7` alone.** `autopsy/writ` records the shape not to
reproduce: an out-of-band `getProvenance(memory_events[0])` probe, run beside the
answer rather than carried by it, on 5 of 77 scenarios and opt-out-able, while
the answer's own `cited_sources` is read by zero lines of scoring
(`evaluator.ts:128-135`). Every quantity below is read off the Answer.

## The denominators, stated rather than inferred (`R8` clause 3)

`§5 L7` states three ratios and **no denominator for any of them**, which is the
fourth species of gate clause this ladder has had to name — the SELF-REPORTED
DENOMINATOR, after `R5` clause 1's identity, `R5` clause 2's minimizing clause
and `R7` clause 3's empty domain. `R8` clause 3 rules them:

| ratio | denominator | checked by |
|---|---|---|
| `tagging` | the declared **G** queries the engine **answers** | the artifact's class table |
| `novelty` | the items the engine **tags** `generated`, in any class | the harness, over frozen bytes |
| `validity` | the same set | the harness, over the declared grammar |

`novelty`'s and `validity`'s denominators are the engine's own report, and they
are admissible only because **every member is checked by the harness** and the
set **cannot be shrunk without failing `tagging`**, whose denominator is the
artifact's. `assert_self_reported_denominators_are_checkable` is that pair of
conditions made a check rather than a sentence. An empty denominator is `n/a`,
and `n/a` **DISQUALIFIES** (clause 3(c)) — a gate is an instrument, and an
instrument outside its range refuses to certify rather than passing.

`§3.4`'s own denominator — the `A` **answered** queries — is declared class by
class in `DENOMINATOR` below, `R7` clause 2's discipline generalized from
calibration to a battery that now carries capability ratios beside it.

## What this module does not do

It applies no gate and declares no threshold. The gates live in
`ascension/l7/t_generation.py`, the ceiling in `humility/l7/t_generation.py`, and
their authority in `laws/t_rulings.py`.
"""

from fractions import Fraction

import _l7tasks

# ONE INSTRUMENT — §3.4's quantities and §3.1's fidelity, imported and not
# re-derived. `permille` is §3.5's round-half-to-even on an exact Fraction.
from _l7tasks import brier, ece, auroc, fidelity, permille  # noqa: F401
from _l7tasks import GENERATED, OBSERVED, canon

ARTIFACT = "l7compose"

# The lineage vocabulary `R8` clause 4 rules: a property of the ITEM, and closed.
# `None` is not in it and does not need to be — an answer that makes no lineage
# claim is the untagged case, which `§5 L7` prices rather than forbids.
LINEAGE_VOCAB = (OBSERVED, GENERATED)

# The two query operations the artifact speaks (`STAGE-B.md §2`).
DECLARED_OPS = ("current", "generate")

# Per query class: does this class score inside `§3.4`'s denominator? (`R7`
# clause 2 requires the declaration; the reason travels with it. `R8` clause 6
# rules `ECE ≤ 40` over exactly this denominator — `§3.4`'s own answered queries
# — so a class declared outside is outside for `§3.4`'s reason and no other.)
DENOMINATOR = {
    "l7compose": {
        "KG1": (True, "the forcing region's generation-required members: "
                      "answerable, and the whole region unsampled — a battery "
                      "that sampled its forcing class could be tuned by "
                      "choosing which compounds to ask about"),
        "KO": (True, "the forcing region's observed twins: answerable, and the "
                     "class that makes the instrument a CONFUSION MATRIX rather "
                     "than a single rate (R8 clause 3(b)) — a recalled item "
                     "tagged generated fails novelty here"),
        "KG2": (True, "the self-pollution ladder at depth 2: answerable"),
        "KG3": (True, "the self-pollution ladder at depth 3: answerable"),
        "KR": (True, "ordinary current-value retrieval: answerable, and the "
                     "class that keeps §3.4's denominator from being a function "
                     "of the generation class alone — which is why hedging the "
                     "whole G class cannot empty the quantity R8 clause 6 gates"),
        "KU1": (False, "generation-shaped unanswerable probes: one component's "
                       "mass is never asserted, so the declared rule does not "
                       "determine the item and abstention is the only correct "
                       "behaviour. An ANSWER here is a fabrication and enters A "
                       "as an error rather than escaping it"),
        "KU2": (False, "never-asserted current-value probes: unanswerable, for "
                       "the reason battery-b's absence probes were — an "
                       "abstention carries no confidence to calibrate"),
    },
}

_CACHE = {}


# ---- the bundle ------------------------------------------------------------

def _bundle(name, payloads, records):
    classes = {}
    for rec in records:
        classes[rec["class"]] = classes.get(rec["class"], 0) + 1
    declared = DENOMINATOR[name]
    if sorted(classes) != sorted(declared):
        raise AssertionError(
            "%s: the artifact carries query classes %r but the denominator "
            "declaration covers %r — R7 clause 2 requires a battery to declare "
            "for EVERY class whether it scores inside `§3.4`'s denominator, and "
            "R8 clause 3 requires the capability ratios' denominators stated "
            "beside it" % (name, sorted(classes), sorted(declared)))
    return {
        "name": name,
        "payloads": payloads,
        "records": records,
        "n": len(records),
        "n_events": len(payloads),
        "classes": classes,
        "n_answerable": sum(1 for r in records if r["answerable"]),
        "generation_class": _l7tasks.generation_class(),
        "region_pairs": tuple(_l7tasks.declared()["pairs"]),
        "store_canon": frozenset(canon(p) for p in payloads),
    }


def battery():
    """`corpora/l7compose` — the artifact both sides of the gate bind on (R8 c1)."""
    if ARTIFACT not in _CACHE:
        _CACHE[ARTIFACT] = _bundle(ARTIFACT, _l7tasks.stream(),
                                   _l7tasks.queries())
    return _CACHE[ARTIFACT]


BATTERIES = {ARTIFACT: battery}


# ---- replay ----------------------------------------------------------------

def replay(engine, mk, b, cap):
    """Ingest the whole stream at `cap`; assert the cap held after **every** write.

    `B = 1000` is certified after every single write and never once at the end:
    the budget law refuses mid-stream (`§4.1.2`), so a state that would exceed
    the cap must be caught where it happens rather than discovered late by a
    measure.

    `§5 L7` states **no footprint clause** and `R8` creates none — its *"what
    this ruling does not do"* list says so in its own words — so the artifact is
    scored **in budget**, at the engine's own `DEFAULT_BUDGET`, where a refusal
    is a defect and not a price. What an engine owes when the budget sheds the
    evidence a generation cites is `ATTAINABILITY.md §7` item 2's disclaimed
    reserve, named with the failure it fears and left to Stage C.
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
    """One query through `§7`, with the Answer contract enforced at the read.

    A raised query is a harness-level failure and categorically worse than a
    scored abstention (`§7.3`), so it is not caught here. What *is* checked is
    the shape `§5 L7` newly depends on — `confidence` as an integer permille
    (Layer 6's requirement, unchanged and still binding) and `lineage` as `R8`
    clause 4's closed item-property. An out-of-vocabulary lineage is a contract
    violation, not a low score; an ABSENT lineage is lawful and is precisely the
    untagged answer `§5 L7` prices.
    """
    ans = engine.query(state, query)
    if not isinstance(ans, dict) or ans.get("status") not in ("answer", "abstain"):
        raise AssertionError("query %r returned a non-Answer: %r" % (query, ans))
    for key in ("status", "value", "confidence", "provenance"):
        if key not in ans:
            raise AssertionError(
                "query %r returned an Answer missing `%s` — §7.2 declares four "
                "keys and R8 clause 2 adds `lineage` beside them, it does not "
                "replace any of them" % (query, key))
    conf = ans.get("confidence")
    if isinstance(conf, bool) or not isinstance(conf, int):
        raise AssertionError(
            "query %r returned confidence %r — §7.2 declares an INTEGER permille "
            "in [0, 1000] and §2.2 forbids a float anywhere in core; from Layer 6 "
            "that field is scored (§3.4) and R8 clause 6 keeps it scored here"
            % (query, conf))
    if not 0 <= conf <= 1000:
        raise AssertionError(
            "query %r returned confidence %d, outside §7.2's [0, 1000]"
            % (query, conf))
    lineage = ans.get("lineage")
    if lineage is not None and lineage not in LINEAGE_VOCAB:
        raise AssertionError(
            "query %r returned lineage %r — R8 clause 4 rules `generated` a "
            "property of the ITEM, and the vocabulary this battery reads is "
            "%r or absent. An absent lineage is a lawful answer that makes no "
            "claim (and is scored as untagged); a value outside the vocabulary "
            "is a contract violation and not a low score"
            % (query, lineage, list(LINEAGE_VOCAB)))
    if ans["status"] == "abstain":
        if ans["value"] is not None:
            raise AssertionError(
                "query %r abstained but carried a value — §7.2 declares "
                "`value: null when status == \"abstain\"`" % (query,))
        if lineage is not None:
            raise AssertionError(
                "query %r abstained but carried lineage %r — an abstention "
                "returns no item, so it has nothing for a property of the item "
                "to be about (§7.2's `value: null` rule, applied to the field "
                "R8 clause 2 adds beside it)" % (query, lineage))
    return ans


def observe(engine, state, b, records=None):
    """Ask every query and record what came back. Nothing here scores.

    Correctness is judged against the **frozen artifact's own answer key**, never
    against the engine's belief and never against the declared class table: an
    answerable query is correct when the value matches the key, an unanswerable
    one when the engine abstains (`§3.0`'s two 1000-rows).
    """
    rows = []
    for rec in (b["records"] if records is None else records):
        ans = _ask(engine, state, rec["q"])
        status = ans["status"]
        if rec["answerable"]:
            correct = (status == "answer" and ans["value"] == rec["value"])
        else:
            correct = (status == "abstain")
        rows.append({
            "qid": rec["qid"],
            "cls": rec["class"],
            "declared": rec["declared"],
            "depth": rec.get("depth"),
            "entity": rec["q"].get("entity", rec["q"].get("cue", {}).get("entity")),
            "answerable": rec["answerable"],
            "status": status,
            "value": ans["value"] if status == "answer" else None,
            "lineage": ans.get("lineage"),
            "confidence": ans["confidence"],
            "provenance": ans["provenance"],
            "correct": correct,
        })
    return rows


# ---- scoring ---------------------------------------------------------------

def _ratio(hit, total):
    """`R8` clause 3(c): an empty denominator is `n/a`, and `n/a` DISQUALIFIES."""
    if total == 0:
        return None
    return Fraction(hit, total)


def score(rows, b, store_canon=None):
    """`§5 L7`'s seven clauses, with every denominator stated beside them.

    `F_core` is fidelity over the **answerable core** — the denominator every
    piece of `R8` clause 8(b)'s window arithmetic is stated in (`F = 1000 − 900g`
    with `g = |G| / A`), and the stricter of the two. `F_all` is fidelity over the
    whole query set as `§3.1` writes it and is reported as an **ungated
    diagnostic**: the unanswerable class scores 1000 for an abstention, so
    including it can only raise the number.

    `ece` is `R8` clause 6's ruled quantity — `§3.4`'s own denominator, the
    answered queries, unmodified. `ece_generated` is the **declined** reading,
    computed beside it and gating nothing, because a reading that can be emptied
    by hedging one class is the shape clause 3(c) disqualifies reached by another
    route, and the cheapest way to keep that visible is to compute it.

    `auroc` is computed and reported and **no `§5 L7` clause cites it**, so `R7`
    clause 3(a)'s `n/a` law is not engaged by a `None` here: that clause binds a
    gate that cites AUROC, and Layer 7's calibration clause is `ECE` alone.
    """
    store_canon = b["store_canon"] if store_canon is None else store_canon
    declared_g = len(b["generation_class"])

    answered = []
    answered_generated = []
    scored_core = []
    scored_all = []
    wrong = fabricated = abstentions = 0
    tag_den = tag_hit = untagged_generations = 0
    gen_items = []
    confidences = set()
    by_class = {}

    for row in rows:
        hit, miss, held = by_class.get(row["cls"], (0, 0, 0))
        if row["status"] == "answer":
            confidences.add(row["confidence"])
            answered.append((row["confidence"], row["correct"]))
            if not row["answerable"]:
                fabricated += 1
            if not row["correct"]:
                wrong += 1
                miss += 1
            else:
                hit += 1
            s = 1000 if row["correct"] else 0
            if row["lineage"] == GENERATED:
                gen_items.append(row["value"])
                answered_generated.append((row["confidence"], row["correct"]))
            if row["declared"] == "G":
                tag_den += 1
                if row["lineage"] == GENERATED:
                    tag_hit += 1
                else:
                    untagged_generations += 1
        else:
            abstentions += 1
            held += 1
            s = 1000 if not row["answerable"] else 100
        by_class[row["cls"]] = (hit, miss, held)
        scored_all.append(s)
        if row["answerable"]:
            scored_core.append(s)

    novel = sum(1 for item in gen_items if canon(item) not in store_canon)
    valid = sum(1 for item in gen_items if _l7tasks.gen.profile_form_ok(item))

    n_pos = sum(1 for _c, ok in answered if ok)
    return {
        "artifact": b["name"],
        "N": len(rows),
        "A": len(answered),
        "n_pos": n_pos,
        "n_neg": len(answered) - n_pos,
        "wrong": wrong,
        "fabricated": fabricated,
        "abstentions": abstentions,
        "confidences": tuple(sorted(confidences)),
        "by_class": by_class,
        # the three capability ratios, on R8 clause 3's denominators
        "validity": _ratio(valid, len(gen_items)),
        "novelty": _ratio(novel, len(gen_items)),
        "tagging": _ratio(tag_hit, tag_den),
        "tagging_all": _ratio(tag_hit, declared_g),
        "tagging_denominator": tag_den,
        "tagged_generated": len(gen_items),
        "novel_items": novel,
        "valid_items": valid,
        "untagged_generations": untagged_generations,
        "conjunction": conjunction(rows, b, store_canon),
        # §3 measures
        "F_core": fidelity(scored_core),
        "F_all": fidelity(scored_all),
        "ece": ece(answered),
        "ece_generated": ece(answered_generated),
        "brier": brier(answered),
        "auroc": auroc(answered),
    }


def conjunction(rows, b, store_canon=None):
    """`§5 L7`'s humility measure — `(novel ∧ valid ∧ tagged)`, as `R8` clause 7 defines it.

    A **per-item conjunction over the artifact's declared generation-required
    class**: an item counts iff the engine answered that query through `§7`
    alone, tagged the item `generated`, the item satisfies the declared item
    grammar, and its canonical bytes appear nowhere in the ingested store. The
    denominator is the **whole** declared class, so it is a property of the
    artifact and cannot be emptied by an engine — clause 3 applied to the ceiling
    as well as to the gate.

    It is deliberately **not** a correctness measure: `§5 L7` names three
    conjuncts and correctness is not one of them. `F ≥ 950` is where correctness
    lives, and a policy emitting valid, novel, tagged nonsense dies there.
    """
    store_canon = b["store_canon"] if store_canon is None else store_canon
    hit = 0
    for row in rows:
        if row["declared"] != "G":
            continue
        if row["status"] != "answer" or row["lineage"] != GENERATED:
            continue
        if not _l7tasks.gen.profile_form_ok(row["value"]):
            continue
        if canon(row["value"]) in store_canon:
            continue
        hit += 1
    return Fraction(hit, len(b["generation_class"]))


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


def assert_self_reported_denominators_are_checkable(figures, rows, b):
    """`R8` clause 3(a), as law rather than as a sentence in a document.

    > *A denominator the engine reports about itself is checkable against the
    > artifact, or it does not count.*

    Admissible only where **both** of clause 3(a)'s conditions hold, and this is
    the pair made a check:

    1. **the harness can check every member.** `novelty`'s and `validity`'s
       denominator is the set of items the engine tagged `generated` — its own
       report — and every member of it is read off the Answer and then checked by
       the harness, against frozen bytes for novelty and against the declared
       grammar for validity. So the counts must reconcile exactly: the numerators
       are sub-counts of one denominator that was itself read through `§7`.
    2. **shrinking the report is costly.** `tagging`'s denominator is the
       ARTIFACT's — the declared G queries the engine answered — so an engine
       that tagged less would not shrink a denominator, it would fail a numerator.
       Asserted directly: the tagging denominator is exactly the number of
       declared-G queries answered, computed from the artifact's class table and
       never from the engine's report.

    Neither check applies a `§5` clause. What it forbids is the shape
    `autopsy/writ` convicted WRIT of at `evaluator.ts:545-548` — a declared-absent
    capability dropped from **both** numerator and denominator — arriving here
    through a denominator nobody could audit.
    """
    tagged = figures["tagged_generated"]
    if figures["novel_items"] > tagged or figures["valid_items"] > tagged:
        raise AssertionError(
            "%s: the harness verified more items than the engine reported "
            "tagging (%d novel, %d valid, %d tagged) — the numerator of a "
            "self-reported denominator must be a sub-count of it"
            % (b["name"], figures["novel_items"], figures["valid_items"], tagged))
    if tagged == 0:
        if figures["novelty"] is not None or figures["validity"] is not None:
            raise AssertionError(
                "%s: the engine tagged nothing generated, so novelty's and "
                "validity's denominators are EMPTY and both must read n/a — "
                "R8 clause 3(c) makes that a disqualification and not a pass"
                % (b["name"],))

    answered_g = sum(1 for row in rows
                     if row["declared"] == "G" and row["status"] == "answer")
    if figures["tagging_denominator"] != answered_g:
        raise AssertionError(
            "%s: tagging's denominator reads %d against %d declared-G queries "
            "answered. R8 clause 3(b) binds it to the ARTIFACT's class table, "
            "which is what fences the other two: an engine that testified less "
            "would fail this numerator rather than shrink a denominator"
            % (b["name"], figures["tagging_denominator"], answered_g))
    return {"tagged": tagged, "answered_g": answered_g}


# ---- the forcing region ----------------------------------------------------

def region_profile(rows, b):
    """Per mirror pair: what the engine did with its two observationally identical members.

    Returns `{pair index: {...}}` carrying, for each member, whether it was
    answered, whether it was correct, and the lineage it was given — plus
    `same_item`, whether the two returned values are equal once `entity` is
    stripped, which is Theorem 1's own claim seen from the engine's side.
    """
    by_entity = {row["entity"]: row for row in rows if row["cls"] in ("KG1", "KO")}
    profile = {}
    for p in b["region_pairs"]:
        g = by_entity[p["generated"]]
        o = by_entity[p["observed"]]
        item_g = _strip_entity(g["value"])
        item_o = _strip_entity(o["value"])
        profile[p["pair"]] = {
            "answered": sum(1 for m in (g, o) if m["status"] == "answer"),
            "correct": sum(1 for m in (g, o) if m["correct"]),
            "lineage_g": g["lineage"],
            "lineage_o": o["lineage"],
            "same_item": (g["status"] == "answer" and o["status"] == "answer"
                          and item_g == item_o),
            "confidences": tuple(m["confidence"] for m in (g, o)
                                 if m["status"] == "answer"),
        }
    return profile


def _strip_entity(value):
    if not isinstance(value, dict):
        return value
    return {k: v for k, v in value.items() if k != "entity"}


def distinguished_pairs(profile):
    """Pairs the engine gave DIFFERENT lineages to — the store-consulting tell.

    Theorem 1: blank the entity id and the two members' cues are the same object,
    and their items are the same item. So a policy whose lineage decision is a
    function of the query alone gives them the same lineage and is wrong on
    exactly one; a policy that gives them different lineages consulted something
    the query does not carry, and the only thing left is what it holds.
    """
    return sorted(pair for pair, row in profile.items()
                  if row["lineage_g"] != row["lineage_o"])


# ---- the promotion ladder, driven through `ingest` --------------------------

def promotion_ladder(engine, state, b, depths=(1, 2, 3)):
    """`§5 L7`'s `promotion = 0`, three deep, with the CALLER doing the re-ingesting.

    At each rung the harness asks the declared-G queries of that depth, takes the
    items the engine tagged `generated`, and **ingests them as ordinary caller
    payloads** — which is what makes this suggestibility in `autopsy/GAPMAP.md
    §6`'s literal sense rather than an engine feeding itself. It then re-asks
    **every** declared-G query and counts how many the engine now reports as
    `observed` fact.

    Scored **at each rung** because a ladder checked only at depth 3 could not say
    where a break occurred (`PRE-READ.md §5.1(d)`, `ATTAINABILITY.md §5.1`). The
    store grows as the caller writes into it, so the canonical-byte set grows with
    it — a generation re-ingested at rung 1 is genuinely in the store at rung 2,
    which is exactly the trap: `novelty` is measured against the store as it now
    is, and only a lineage record can still say what the item is.
    """
    store_canon = set(b["store_canon"])
    g_records = [rec for rec in b["records"] if rec["declared"] == "G"]
    rungs = []
    for depth in depths:
        at_depth = [rec for rec in g_records if rec.get("depth") == depth]
        emitted = []
        for row in observe(engine, state, b, at_depth):
            if row["status"] == "answer" and row["lineage"] == GENERATED:
                emitted.append(row["value"])
        for item in emitted:
            state, t = engine.ingest(state, item)
            if t is None:
                raise AssertionError(
                    "the caller's re-ingestion of a generated item was REFUSED "
                    "at depth %d — the ladder is scored in budget, where a "
                    "refusal is a defect and not a price" % (depth,))
            store_canon.add(canon(item))

        after = observe(engine, state, b, g_records)
        promoted = sum(1 for row in after
                       if row["status"] == "answer"
                       and row["lineage"] != GENERATED)
        still = sum(1 for row in after
                    if row["status"] == "answer" and row["lineage"] == GENERATED)
        rungs.append({"depth": depth, "emitted": len(emitted),
                      "promotion": promoted, "still_generated": still,
                      "store": state.next_t})
    return state, rungs, store_canon


# ---- `§4.2` as it wakes: the two checks the schema cannot make --------------

def support_recoverability(engine, state, rows):
    """BLINDNESS (a), as the ungated diagnostic `R8` clause 5(a) pays for the reading with.

    `§4.2.3` asks whether a `t` was ever **assigned**; whether `read(t)` still
    **answers** is a state query the validator does not ask and cannot be made to
    ask without becoming one. The reading taken is SHAPE-ONLY, and the price is
    this number: over every `t` the engine's own tags cite, how many the engine
    can still produce, asked through the Layer-1 `read` verb and not out of any
    bookkeeping.

    At `DEFAULT_BUDGET` it reads 1000 and is uninformative, which is **stated
    rather than hidden** (`ATTAINABILITY.md §9.1`). What it buys now is that the
    number cannot quietly fail to exist once pressure arrives.
    """
    cited = recoverable = 0
    for row in rows:
        if row["status"] != "answer" or row["provenance"] is None:
            continue
        for t in row["provenance"]["support"]:
            cited += 1
            if engine.query(state, {"op": "read", "t": t})["status"] == "answer":
                recoverable += 1
    return {"cited": cited, "recoverable": recoverable,
            "rate": _ratio(recoverable, cited)}


def relevance(rows, reading=None):
    """BLINDNESS (b), bound on the ARTIFACT because `§4.2` cannot bind it.

    The schema constrains order, sign and range and **not** whether the cited
    events bear on the answer: `{"support":[0,1,2],"kind":"derive","t_asof":2}` is
    accepted for an answer composed from `t`s in the thousands, measured on the
    frozen validator by `ascension/l7/t_attainability.py`. So `R8` clause 5(b)
    binds relevance here instead: **for an answer tagged `generated`, `support`
    must be exactly the `t`s the declared composition rule reads** — a harness
    check against frozen bytes, not a new schema clause.

    Returns `(checked, mismatches)`, where a mismatch names the qid, so a battery
    can require the count and report the offenders.
    """
    reading = _l7tasks.base_reading() if reading is None else reading
    checked = 0
    mismatches = []
    for row in rows:
        if row["status"] != "answer" or row["lineage"] != GENERATED:
            continue
        built = reading.composed_only(row["entity"])
        if built is None:
            mismatches.append((row["qid"], None, None))
            continue
        want = built[1]
        got = tuple(row["provenance"]["support"])
        checked += 1
        if got != want:
            mismatches.append((row["qid"], got, want))
    return {"checked": checked, "mismatches": tuple(mismatches)}

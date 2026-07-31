"""ascension/l5 — Layer 5 (Prospection) capability trials (BOUNDARY.md §5 L5).

The Stage-B battery. It applies the ratified Layer-5 gate

    trigger-precision = 1000,  trigger-recall = 1000,  dup-fire = 0,
    miss = 0,  F >= 980,  B = 1000

to an engine on `corpora/l5stream`. Every trial that needs an engine is
**ENGINE-GATED**: it reports `SKIPPED-BY-DESIGN` until
`core/layers/l5_prospection.py` and `trials/adapters/l5.py` exist, and then it
must clear the gate. That is the standing checkpoint shape of an `ASCEND` split
at the trials/engine boundary — humility green, ascension skipped — and it is
R2's standing step in force: *attainability arithmetic → trials → engine*.

**THE GATE BINDS ON `corpora/l5stream`, by `BOUNDARY-RULINGS.md R6` clause 1**
(ratified 2026-07-31, `[L4] [RULING]`), which binds the ascension gate and the
Layer-5 humility ceiling together in one clause — a ceiling measured on one
corpus beside a gate cleared on another would discriminate nothing. `R6` clause 4
rules the cap this battery replays at: `budget_cap = raw_cells // 4 = 45 638`,
with the events the engine **emits** competing for cells inside it rather than
enlarging it. `R5` remains what settles the *reading* of R2's obligations these
clauses are scored under, so `laws/t_rulings.py` carries both entries on every
constant below — `R5` for the reading, `R6` for the substrate — except `GATE_F`,
which carries `R6` alone, being the clause `R5` expressly excludes.

## The four identities, and the one threshold

`R5 clause 1` governs `trigger-precision`, `trigger-recall`, `dup-fire` and
`miss`: they are identities over discrete correctness, so they are asserted here
with `require_equal` — as **identities, not thresholds**. There is no `>=` to
write. `F >= 980` is the one clause of `§5 L5` that discharges R2 obligation 1 the
ordinary way (oracle 1000), is expressly **excluded** from R5 clause 1, and is
therefore the only clause below written as an inequality. R3 does not reach
Layer 5 and no extension is requested, so `F` binds under the **literal §3.0
table**: an honest abstention on an answerable P1 scores 100, not 1000.

## What this file does NOT do, deliberately

Stage A exhibited the oracle ceiling and scored every named capability-free
baseline, and `t_attainability.py` asserts all of it on every run. **One fixture,
one truth** — none of it is repeated here:

  * the exhibited witness attaining `1000 / 1000 / 0 / 0 / F 1000` at 41 951 of
    45 638 cells — `t_attainability.py::trial_the_exhibited_witness_attains_the_identity`;
  * the four named baselines and the two R2 obligations as they actually come
    out — `::trial_every_named_baseline_is_scored_and_is_far_below_the_gate`,
    `::trial_r2_obligation_1_is_not_dischargeable_by_a_strict_reading`,
    `::trial_r2_obligation_2_ties_on_the_minimizing_clauses_and_holds_on_the_conjunction`;
  * the witness's price, its bookkeeping and its loss reserve —
    `::trial_the_witness_fits_the_budget_priced_under_rule_p`,
    `::trial_both_layer4_lessons_are_priced_rather_than_disclaimed`;
  * the `F >= 980` slack (35 wrong answers, or 38 abstentions, of 1 710) —
    `::trial_the_battery_and_its_f_slack_are_as_recorded`;
  * the humility ceiling from the arithmetic side —
    `::trial_the_humility_ceiling_is_not_breached_and_the_reason_is_structural`;
  * the corpus's own declared properties — `ops/l5/t_l5stream.py`.

The gate constants below are the same ratified numbers those trials name, and
`laws/t_rulings.py` binds **both** files' copies to `§5 L5`, to `R5` and to `R6`,
so they cannot drift apart silently.

## The `t` semantics this battery measures

`STAGE-B.md §1` settles the question `R5` left open and **`R6` clause 2 ratifies
it**: a firing is an event, `§1.3` gives it a `t` of its own, and one caller
`ingest` therefore advances `next_t` by `1 + f`. That is not a footnote to this
battery — it is one of its instruments. `_l5score.assert_t_identity` audits the
engine's firing report against its own logical clock, which is why `dup-fire` is
a number an engine cannot report its way out of. Two things `R6` clause 2
expressly does **not** decide are not asserted here either: cascades (unobservable
on this corpus by the GUARDEDNESS induction, so both readings give the identical
schedule) and what an engine owes when the budget cannot house a firing — the
battery asserts the invariants and leaves the policy to Stage C, with the one
consequence the gate does fix, that a firing is not discretionary.
"""

import collections

from _harness import require, require_equal, try_import
import _l5score
import _l5tasks
from corpora.l5stream import generator as l5gen

# The ratified §5 L5 gate, unchanged. Four identities, one threshold, one budget
# law. Registered in `laws/t_rulings.py` against the §5 L5 clauses they are
# quoted from, against R6 (clause 1's corpus binding, and clause 4's cap for
# GATE_B) for every one of them, and against R5 for the five it reaches — GATE_F
# being the clause R5 expressly excludes.
GATE_TRIGGER_PRECISION = 1000
GATE_TRIGGER_RECALL = 1000
GATE_DUP_FIRE = 0
GATE_MISS = 0
GATE_F = 980
GATE_B = 1000

LAYER_CAP = 5

# The `t` layout the semantics of `STAGE-B.md §1`, ratified as R6 clause 2,
# force on this frozen stream.
# Recorded at Stage A and asserted there engine-free
# (`t_attainability.py::trial_one_caller_ingest_can_advance_next_t_by_more_than_one`);
# here it is asserted of an ENGINE, which is the half Stage A could not reach.
ENGINE_NEXT_T = 20765
LAST_FIRE_T = 20760

# The corpora every anchor and the whole `inheritance/` class replay. None of
# them carries an intention, which is why the one-ingest-one-`t` identity they
# assume is not merely still true but forced (STAGE-B.md §1.4).
INTENTION_FREE_CORPORA = ("chronicle", "sessions", "murk", "l3stream",
                          "l3streamb", "l4stream")

_RUN = {}


def _engine():
    return try_import(
        "adapters.l5",
        "no L5 engine yet; prospection ascension engages when built "
        "(Stage C — R2's standing step: arithmetic → trials → engine)")


def _run(engine):
    """Replay `l5stream` at the Layer-5 cap and score the battery, once per run."""
    key = id(engine)
    if key not in _RUN:
        b = _l5tasks.corpus()
        state, budget = _l5score.replay(
            engine, lambda cap: engine.make_engine(LAYER_CAP, cap), b)
        _RUN[key] = (state, budget, _l5score.score(engine, state, b), b)
    return _RUN[key]


# ---- 1. the gate: exactly-once, as four identities --------------------------

def trial_prospection_fires_exactly_once_and_the_four_clauses_are_identities():
    """THE binding gate's exactness half (§5 L5; R5 clause 1; R6 clause 1).

    `§5.1 L5`: *"Every intention whose condition a future write satisfies must
    fire, and nothing may fire spuriously — prospection is exact or it is
    broken."* Four clauses, four `require_equal`s. R5 clause 1 is why these are
    written as identities rather than as thresholds: the oracle ceiling **is**
    the gate for a clause of this shape, and the obligation R2 states as a strict
    inequality is discharged instead by the witness Stage A exhibited attaining
    it. An identity clause has no margin to spend, so there is no `>=` here to
    quietly widen later. `R6` clause 1 is what makes this the **binding** gate
    rather than a measurement on a named corpus: it binds all four clauses, and
    `F` and `B` with them, to `corpora/l5stream`.
    """
    l5 = _engine()
    _state, _budget, r, b = _run(l5)

    require_equal(r["precision"], GATE_TRIGGER_PRECISION,
                  "trigger-precision is an IDENTITY at §5 L5, not a threshold — "
                  "%d of %d firings landed on their own satisfaction point"
                  % (r["correct"], r["fires"]))
    require_equal(r["recall"], GATE_TRIGGER_RECALL,
                  "trigger-recall is an IDENTITY at §5 L5 — %d of %d fireable "
                  "intentions fired exactly once at their satisfaction point"
                  % (r["correct"], len(b["fireable"])))
    require_equal(r["dup_fire"], GATE_DUP_FIRE,
                  "an intention fired more than once: dup-fire %d against a gate "
                  "of 0. Exactly-once is a property of an INTENTION, and the "
                  "count is audited against the engine's own logical clock "
                  "(STAGE-B.md §1), not against its bookkeeping" % (r["dup_fire"],))
    require_equal(r["miss"], GATE_MISS,
                  "%d fireable intentions never fired: miss against a gate of 0"
                  % (r["miss"],))

    require_equal(r["fires"], len(b["fireable"]),
                  "the engine emitted %d firings for %d fireable intentions — "
                  "exactly-once means the two numbers are one number"
                  % (r["fires"], len(b["fireable"])))
    require_equal(r["malformed"], 0,
                  "an answered P1 was not a list of event records; §7.2 lets an "
                  "Answer carry any allowed value, and STAGE-B.md §2 declares "
                  "which one this query carries")


def trial_never_fires_intentions_stay_unfired_for_the_whole_stream():
    """The 180 intentions nothing satisfies, and the honesty §3.0 pays for.

    Without them `trigger-precision` could be bought by firing eagerly, and
    *"abstain when nothing satisfies it"* would be an untested claim rather than
    a scored behaviour. `corpora/l5stream/grammar.md` makes their unsatisfiability
    a property of the corpus's own structure — a `kind = spawn` after the spawn
    prelude, a `val_ge` of 5 000 against a value vocabulary bounded by 1 000, a
    `count_ge` of `10n` against a stream of `n` — so this is not a corpus that
    merely happened not to satisfy them.

    A never-fires intention's P1 is **unanswerable**: abstaining scores 1000 under
    §3.0, and answering it is a fabrication scored 0. Both halves are asserted —
    and neither is a clause added to the gate. *"No never-fires intention fires"*
    is `trigger-precision = 1000` stated directly: one spurious firing makes the
    ratio 765/766 and the identity fails. What the well-formedness half enforces
    is `§7.2`'s Answer, not a §5 threshold.
    """
    l5 = _engine()
    state, _budget, r, b = _run(l5)

    require_equal(len(b["never"]), l5gen.DECLARED_NEVER_FIRES,
                  "the never-fires tier drifted from the corpus's declaration")
    require_equal(r["fabricated"], 0,
                  "%d intentions that nothing in the stream satisfies were "
                  "answered rather than abstained on — §3.0 scores a fabrication "
                  "at 0, exactly as it scores a confident wrong answer"
                  % (r["fabricated"],))

    obs = _l5score.observe(l5, state, b)
    fired_anyway = [iid for iid in b["never"] if obs["p1"][iid]["t"]]
    require(not fired_anyway,
            "these intentions fired although no write in the whole stream "
            "satisfies their condition: %s" % (fired_anyway[:8],))
    for iid in b["never"]:
        require_equal(obs["p1"][iid]["answer"]["status"], "abstain",
                      "intention %d never fires, so its P1 is unanswerable and "
                      "the only correct behaviour is to abstain (§3.0, §7.3)"
                      % (iid,))


def trial_several_intentions_satisfied_by_one_write_all_fire_each_at_its_own_t():
    """34 caller indices satisfy more than one pending intention, fan-out up to 3.

    *"Exactly-once is a property of an intention, not of an index"*
    (`grammar.md`): a design that fired at most one intention per write would
    satisfy nothing in `§5 L5`, and would show up here as a `miss` rather than as
    a design choice. Each intention satisfied at one index fires **once**, in
    `iid` ascending order — the declared total order §2.3 needs so determinism
    does not rest on an engine's scan order — and each firing takes a `t` of its
    own, consecutively, because two events cannot share one (§1.3).
    """
    l5 = _engine()
    state, _budget, _r, b = _run(l5)
    obs = _l5score.observe(l5, state, b)

    multi = collections.OrderedDict(
        (k, v) for k, v in b["by_index"].items() if len(v) > 1)
    require_equal(len(multi), l5gen.DECLARED_MULTI_SAT_INDICES,
                  "the multi-satisfaction index count drifted from the corpus")
    require_equal(max(len(v) for v in multi.values()),
                  l5gen.DECLARED_MAX_SAT_AT_INDEX,
                  "the largest fan-out at one caller index drifted")

    for k, iids in multi.items():
        got = []
        for iid in iids:
            ts = obs["p1"][iid]["t"]
            require_equal(len(ts), 1,
                          "intention %d, one of %d satisfied by the write at "
                          "caller index %d, fired %d times"
                          % (iid, len(iids), k, len(ts)))
            got.append((iid, ts[0]))
        require_equal([i for i, _t in got], sorted(iids),
                      "the intentions satisfied at caller index %d did not fire "
                      "in `iid` ascending order — the declared total order is "
                      "what makes §2.3 determinism independent of scan order"
                      % (k,))
        ts = [t for _i, t in got]
        require_equal(ts, sorted(ts),
                      "firings at caller index %d are not in `t` order" % (k,))
        require_equal(ts, list(range(ts[0], ts[0] + len(ts))),
                      "the %d firings at caller index %d do not occupy "
                      "consecutive logical times: %s. Each firing is an event and "
                      "consumes one `t` (§1.3, STAGE-B.md §1)"
                      % (len(ts), k, ts))


def trial_a_condition_over_demoted_content_fires_from_consolidated_state():
    """The Layer-4 seam: `count_ge` is a fold, and the episodes it folds are gone.

    169 of the stream's conditions name `count_ge`, the one predicate that reads
    nothing of the arriving payload and everything of the past
    (`grammar.md`: *"a condition over exactly the content the layer below has
    demoted, priced at two cells per kind. It is why this layer is built on that
    one."*). 111 of them are fireable.

    A trigger that could only fire from **held episodes** would fail here by
    arithmetic and not by design: the raw episodic footprint is 182 555 cells
    against a 45 638-cell cap, so at most 5 412 of the 20 000 events can be held
    as episodes at all (cheapest-first, `event_cost + 1` each — the bound
    `_l5tasks` prices and the engine-free trial below asserts). The fold must
    therefore come from consolidated state.

    Two things are asserted: every fireable `count_ge` intention fires exactly at
    its satisfaction point, and at least one event a satisfied fold counted is
    answered by `read(t)` as **regenerated rather than held** — README-l4 §4's
    two provenance kinds, `derive` for an event the schema rebuilt and `recall`
    for one still stored, which is the seam made observable from outside.
    """
    l5 = _engine()
    state, _budget, _r, b = _run(l5)
    obs = _l5score.observe(l5, state, b)

    over_demoted = _l5tasks.count_ge_conditions()
    require_equal(len(over_demoted), l5gen.DECLARED_COUNT_GE_CONDITIONS,
                  "the count of conditions over demoted content drifted")

    fireable = [iid for iid in over_demoted if b["sat"][iid] is not None]
    require(fireable,
            "no condition naming `count_ge` is satisfiable in this stream, so "
            "the Layer-4 seam is not exercised at all")
    for iid in fireable:
        ts = obs["p1"][iid]["t"]
        require_equal(ts, [b["fire_t"][iid]],
                      "intention %d, whose condition folds over the past by "
                      "grammar kind, did not fire exactly once at the logical "
                      "time its satisfaction point forces (%s)"
                      % (iid, b["fire_t"][iid]))

    # The seam itself: an event the fold counted, no longer an episode.
    counted = []
    for iid in fireable:
        sigma = b["sat"][iid]
        counted.extend(b["caller_t"][k] for k in range(0, min(sigma, 400)))
        if len(counted) > 400:
            break
    kinds = collections.Counter()
    for t in counted[:400]:
        ans = l5.query(state, {"op": "read", "t": t})
        prov = ans.get("provenance") or {}
        kinds[prov.get("kind") if ans["status"] == "answer" else "abstain"] += 1
    require(kinds.get("derive", 0) > 0,
            "not one of the events these folds counted is answered as "
            "REGENERATED (`provenance.kind == \"derive\"`): %s. At this cap the "
            "episodes cannot all be held, so a fold answered only from held "
            "episodes would be answering from a tier that does not exist "
            "(README-l4 §4, the demotion seam)" % (dict(kinds),))


# ---- 2. the graded clause, the budget, the footprint -----------------------

def trial_the_fired_payload_matches_and_f_clears_the_graded_clause():
    """`F >= 980` — the ONE clause of §5 L5 that is a threshold (R5 clause 1 excludes it).

    `§5.1 L5` defends it as *"a fired event's payload must match the intended
    event essentially exactly."* Asked of a black box through `§7`'s three
    operations that is two query classes: P1, one per intention, and P2, one per
    fired event, where **P2 is the Layer-1 `read` verb** — the engine hands back
    the event it emitted at the `t` it assigned, which is what makes *"the
    payload matched"* a measurement rather than a definition.

    `F` binds under the **literal §3.0 table**: R3 excludes Layer 5 in its own
    text, and no extension is requested because the oracle reaches 1000. So an
    honest abstention on an answerable P1 scores 100 here, and the gate's honest
    margin is 35 wrong answers or 38 abstentions out of 1 710 (asserted at Stage
    A, not restated here).

    The engine adds nothing to the payload it was told to fire (§1.4). That is
    checked byte-for-byte: `read(t_fire)` must return `{"payload": <the `fire`
    payload verbatim>, "t": <t_fire>}` and nothing else, which is why the corpus
    draws `fired`'s `text_id` from the same global counter as `note`'s — so a
    firing can be attributed without the engine stamping anything into it.

    **`wrong = 0` is deliberately NOT asserted here, and the restraint is the
    point.** Given the four identities, the only way a P1 can be wrong is a
    payload that differs at the right `t` — precisely what `F` measures — and
    `F ≥ 980` on a 1 710-query battery admits **35** of them. `§5 L5` ratified
    980 and not 1000, and `R5` clause 1 records that slack as the constitution's
    own answer to R2's perfection objection (*"where the tension does arise the
    constitution already gave slack"*). Asserting `wrong = 0` beside it would
    quietly take that slack back and gate at 1000 under a 980 clause. The count
    is computed and reported in the failure message instead, which is where a
    diagnostic belongs.
    """
    l5 = _engine()
    _state, _budget, r, b = _run(l5)

    require(r["F"] >= GATE_F,
            "F %d against the §5 L5 gate of %d on a %d-query battery "
            "(P1 %d, P2 %d); wrong %d, fabricated %d — the gate admits 35 wrong "
            "answers or 38 abstentions of 1 710 and no more"
            % (r["F"], GATE_F, r["battery"], r["n_p1"], r["n_p2"],
               r["wrong"], r["fabricated"]))
    require_equal(r["n_p1"], len(b["intents"]),
                  "P1 is not one query per intention")
    require_equal(r["n_p2"], len(b["fireable"]),
                  "P2 is not one query per fired event — the denominator moves "
                  "with what the engine emitted, and an engine that emitted the "
                  "wrong number of events has already failed the identity")


def trial_the_budget_law_holds_after_every_write():
    """`B = 1000` — and the firings are inside the cap, not beside it (R6 clause 4).

    `§5.1 L5`: *"Pending intentions live within the hard budget like any other
    state."* `ATTAINABILITY.md §1` read that as covering the events the engine
    **emits** too, and `R6` clause 4 ratifies both halves: the cap is
    `budget_cap = raw_cells // 4 = 45 638`, and the emitted events are
    engine-derived and compete for cells inside it without enlarging it. No
    footprint gate is created by that clause — `§5 L5` states none — so what is
    certified here is the cap the budget law binds at, after every write. So the cap is checked after every caller write —
    `_l5score.replay` raises where it breaks, not at the end — and the pending
    set, the fired rows and the Layer-4 substrate all come out of one budget.
    """
    l5 = _engine()
    _state, budget, _r, b = _run(l5)
    require_equal(budget["B"], GATE_B,
                  "peak occupancy %d against a cap of %d — §3.3 makes any value "
                  "below 1000 a breach of the budget law and disqualifying"
                  % (budget["peak"], budget["cap"]))
    require_equal(budget["cap"], b["budget_cap"],
                  "the replay cap is not the declared Layer-5 budget")
    require_equal(budget["refused"], 0,
                  "%d caller writes were refused. A refusal is lawful (§4.1.2) "
                  "and is not lawful here: a refused write is a write the engine "
                  "never saw, so its intentions never arrive and its conditions "
                  "are never tested — the identity would be met by not being "
                  "asked" % (budget["refused"],))


def trial_the_footprint_is_priced_under_rule_p():
    """R4 clause 3, ruled general: one cell, one grammar atom.

    The half a trial can see from outside an engine is that the engine's own
    serialized state carries no materially more atoms than it charged itself for;
    the packing half — a composite scalar carrying two atoms — is structural and
    is the engine's obligation, recorded rather than silently assumed. Stage A
    priced the witness at 41 951 of 45 638 cells under this rule, and a state
    that under-reports its footprint would make that margin a wish.
    """
    l5 = _engine()
    state, _budget, _r, b = _run(l5)
    atoms = _l5score.snapshot_atoms(l5, state)
    require(atoms <= state.occupancy + _l5score.RULE_P_HEADER_ALLOWANCE,
            "the engine's snapshot carries %d grammar atoms against a charged "
            "occupancy of %d (+%d header allowance) — rule P is being "
            "under-reported, and every permille in ATTAINABILITY.md is a ratio "
            "against a number that would then not be the state's"
            % (atoms, state.occupancy, _l5score.RULE_P_HEADER_ALLOWANCE))
    require(state.occupancy <= b["budget_cap"],
            "the final state exceeds the declared cap")


# ---- 3. the `t` semantics, of an engine ------------------------------------

def trial_the_engine_t_layout_is_the_one_the_written_texts_force():
    """`R6` clause 2, asserted of an engine rather than of an arithmetic.

    A firing is an event (`§5 L5` writes `intend(condition → event)`); `§1.4`
    makes an in-engine event record exactly `{payload, t}`; `§1.3` makes `t`
    unique within a state and strictly increasing in ingestion order. Three
    ratified sentences therefore force one layout and leave no other available:
    each firing takes a `t` of its own, strictly after the write that satisfied
    it and before the next caller write, in `iid` order where several fall
    together. On `corpora/l5stream` that is 20 000 caller writes becoming 20 765
    logical times, the last firing at `t = 20 760`.

    Stage A asserted this arithmetic engine-free
    (`t_attainability.py::trial_one_caller_ingest_can_advance_next_t_by_more_than_one`).
    What is added here is the half Stage A could not reach: that the ENGINE's own
    clock agrees, and that the caller events and the firings partition
    `0 .. next_t − 1` with nothing left over and nothing counted twice.

    `R6` clause 2 ratifies the layout as `STAGE-B.md §1` derives it — including
    that `ingest` returns the **caller** event's `t` and that `§7.1`'s *"appends
    one event"* describes the caller's payload rather than capping the
    transition — so what this trial applies is a ruled semantics and not a
    session's reading.
    """
    l5 = _engine()
    state, _budget, _r, b = _run(l5)
    obs = _l5score.observe(l5, state, b)
    _l5score.assert_t_identity(obs)

    require_equal(state.next_t, ENGINE_NEXT_T,
                  "the engine's final `next_t` over l5stream is not the one the "
                  "`t` semantics force (%d caller writes + %d firings)"
                  % (b["n"], len(b["fireable"])))
    reported = sorted(t for rec in obs["p1"].values() for t in rec["t"])
    require_equal(reported, sorted(b["fire_t"].values()),
                  "the logical times the engine fired at are not the ones the "
                  "corpus's satisfaction points force under STAGE-B.md §1")
    require_equal(max(reported), LAST_FIRE_T,
                  "the logical `t` of the last firing drifted")
    require_equal(len(set(reported)), len(reported),
                  "two firings share a logical `t`, which §1.3 forbids outright")


def trial_one_caller_ingest_advances_next_t_by_exactly_one_on_an_intention_free_stream():
    """The constraint the whole decision was taken under — asserted, not promised.

    ENGINE-FREE and green today. `STAGE-B.md §1.4`, ratified as `R6` clause 2:
    the `t` semantics settled there must leave Layers 1–4 exactly where they
    were, or every anchor is wrong. They do, and not by exception: the general
    rule is *one caller event plus the firings it caused*, and on a stream that
    carries no intention the second term is zero, so *"one ingest, one `t`"* is
    the `f = 0` case of the same rule rather than a clause suspended for old
    corpora. The clause says so in its own text, and this trial is what it names
    as the assertion behind the claim.

    That is a theorem about frozen bytes, so it is asserted over the bytes: of
    every corpus in the registry, `corpora/l5stream` is the **only** one carrying
    a payload a Layer-5 reading takes as an intention. The check runs over the
    registry rather than over a list, so a corpus frozen later that did carry
    intentions would go red here and force whoever froze it to say what it means
    for the anchors — which is the point.
    """
    import json
    import os
    from corpora import registry

    carriers = []
    checked = []
    for gen in registry.GENERATED:
        name = os.path.basename(gen.FROZEN_PATH).split(".")[0]
        intents = 0
        total = 0
        for line in gen.frozen_bytes().decode("utf-8").splitlines():
            if not line.strip():
                continue
            total += 1
            payload = json.loads(line)
            if isinstance(payload, dict) and payload.get("kind") == "intend":
                intents += 1
        require(total > 0,
                "%s is empty, which would make this theorem vacuously true"
                % (name,))
        checked.append(name)
        if intents:
            carriers.append((name, intents))

    require_equal(carriers, [("l5stream", l5gen.DECLARED_INTENTIONS)],
                  "the set of frozen corpora carrying intentions changed. Every "
                  "anchor's recorded `next_t` and the whole inheritance class "
                  "assume one caller ingest advances `t` by exactly one on the "
                  "corpus they replay, and that assumption is safe only while "
                  "the corpus has nothing to fire (STAGE-B.md §1.4)")
    for name in INTENTION_FREE_CORPORA:
        require(name in checked,
                "%s is replayed by an anchor or by the inheritance class but is "
                "no longer in the registry this theorem quantifies over" % (name,))


def trial_the_declared_query_vocabulary_is_the_one_the_scorer_speaks():
    """ENGINE-FREE. `STAGE-B.md §2` declares P1's query; `_l5score` must ask it.

    Docs are checked, not trusted — the discipline `[L4] [PACKAGE]` set for
    `packaging/`. A Stage-B record that declared one query vocabulary while the
    battery asked another would leave a Stage-C engine implementing the wrong
    interface and discovering it only when the ascension trial went red for a
    reason nobody wrote down.
    """
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "STAGE-B.md"), "r", encoding="utf-8") as fh:
        record = fh.read()
    with open(os.path.join(os.path.dirname(os.path.dirname(here)),
                           "_l5score.py"), "r", encoding="utf-8") as fh:
        scorer = fh.read()

    for op in ('{"op":"fired","iid"', '{"op":"read","t"'):
        require(op in record,
                "STAGE-B.md no longer declares the query %s the battery asks"
                % (op,))
    require('"op": "fired", "iid": iid' in scorer,
            "_l5score no longer asks the P1 query STAGE-B.md declares")
    require('"op": "read", "t": t' in scorer,
            "_l5score no longer asks P2 through the Layer-1 `read` verb")

"""strain/l7 — the two seams `§4.2` opens when it wakes: the invented warrant,
and the warrant the budget takes.

`§4.2` is **dormant until Layer 7 and binding forever after** — the only clause
in the constitution that says so about itself — and `R8` clause 5 measured what
it can and cannot see before any engine existed. Two of those three blindnesses
are attacked here, on the engine, over `corpora/l7compose` (`R8` clause 1).

Neither trial declares a `§5` constant and the reason is recorded rather than
left to inference, in the form `strain/l5`'s blocking seam used: **there is no
`§5` number in this file**. `§4.2` states a *schema*, not a threshold; `R8`
clause 5(b)'s relevance check is bound to the artifact and not to a gate; and
`R8` clause 5(a)'s support-recoverability rate is **reported and never gated**,
which is the whole content of the shape-only reading. A constant here would be a
gate this file does not have the authority to apply.

## 1. THE INVERSION — what the law accepts, and what the ledger catches

`ATTAINABILITY.md §9.3` measured the blindness on a policy and `R8` clause 5(c)
ruled its consequence:

> after the caller re-ingests generation 1, **all 30** depth-2 answers' tags cite
> a `t` that is a re-ingested generation, and the frozen validator accepts **all
> 30**, while their whole warrant is content the engine invented. **The provenance
> law as written is blind to the failure the layer that activates it exists to
> prevent.**

That is `autopsy/GAPMAP.md §2`'s *recorded but never binding* thesis — the one
this project convicted four engines and every evaluator of — available as a
defect of **our own law**, and the honest response is not to pretend the law sees
it. `§4.2` is frozen (`§9.2`) and its 30 acceptances do not move. What moves is
who is asked: `R8` clause 5(c) rules `promotion = 0` enforced by the battery and
by `§6`'s self-pollution strain, **keyed on lineage**, and this measures the
inversion in one place — **30 tags accepted by the schema, 0 answers accepted as
fact** — with a ledger-blind fixture beside it turning the same 30 into 100
promotions, so the catch is demonstrated and not assumed.

## 2. THE WARRANT THE BUDGET TAKES — the question live since the kept promise

`BOUNDARY.log` line 34 filed it at the post-L5 PULSE: *must a support entry be
RECOVERABLE, or only INGESTED?* `R7` clause 7 bequeathed it and `R8` clause 5(a)
settled it **shape-only** — a support entry must be **ingested, not
recoverable** — and said the weaker claim out loud: *provenance certifies that an
answer had a source, and not that the source can be shown.* The price of taking
the cheap reading is an **ungated diagnostic**, in the exact shape `R3` gave
`F_strict` and `R4` clause 4 gave `F_corruption`.

`ATTAINABILITY.md §7` named the failure it feared: *a generation whose support
has been shed cites a `t` the forgetting record can only count*. This is that
prediction MEASURED rather than left standing, on a declared ladder of caps over
a prefix of the frozen artifact where the engine really does lose events — up to
1 934 of them, with entities damaged by shedding — and the measurement replaces
the prediction, in the shape `README-l6 §4` established one layer down when the
same kind of disclaimer was cashed out.

**THE FEARED PATH DOES NOT EXIST ON THIS ENGINE, and not because nothing is
lost.** The composition reading can only cite what it can still **read**: a
compound whose `part` episode the budget took is a compound the reading no longer
determines, so the engine loses the **answer** before it can lose the
**warrant**, and generation degrades by abstention — `§3.0` pays 100 for it —
rather than by a dangling citation. Measured across the ladder, the number of
cited `t`s the engine cannot produce is **0 at every cap**, while `forgotten` is
exactly the set of `t` it abstains on, so the two sets are disjoint by
construction rather than by luck.

**It is stated as the stronger property it is, and it is NOT gated.** `R8`
clause 5(a) demands *ingested*; this engine happens to satisfy *recoverable*, and
an engine that did not would breach no `§5 L7` clause. Saying which of the two is
the law and which is a fact about one implementation is the point of writing it
down here rather than in a gate.
"""

from fractions import Fraction

from _harness import require, require_equal
from adapters import l7
from core.state import event_cost
from laws.t_provenance_schema import validate_provenance

import _l7score
import _l7tasks
from _l7fixtures import LedgerBlind

LAYER_CAP = 7

# `ATTAINABILITY.md §9.3`'s figure, reproduced on an engine: after the caller
# re-ingests generation 1, every depth-2 answer's support names a `t` that is one
# of the engine's own re-ingested items, and the FROZEN validator accepts them
# all. Cited here as the BEFORE; the AFTER is on the line below it.
SCHEMA_ACCEPTS = 30
ACCEPTED_AS_FACT = 0

# The pressure ladder for §2, declared rather than searched: a 6 000-event prefix
# of the frozen artifact — long enough to carry whole mirror-pair blocks — and a
# ladder of absolute caps spanning the band from "nothing is lost" through
# "composition dies entirely", so the seam is looked for where it would be if it
# were anywhere.
PREFIX = 6000
CAP_LADDER = (24457, 21000, 19000, 18000, 17000, 13000)

_RUN = {}


def _fresh():
    if "run" not in _RUN:
        b = _l7score.battery()
        state, budget = _l7score.replay(
            l7, lambda cap: l7.make_engine(LAYER_CAP, cap), b, l7.DEFAULT_BUDGET)
        _RUN["run"] = (state, budget, b)
    return _RUN["run"]


def _under_pressure(cap, payloads):
    """One pressured replay per declared cap, shared by both trials below.

    The ladder is the expensive half of this file — six replays of a 6 000-event
    prefix — and both trials read the same six states, so the bill is stated and
    paid once rather than twice.
    """
    if cap in _RUN:
        return _RUN[cap]
    state = l7.make_engine(LAYER_CAP, cap)
    refused = 0
    for payload in payloads:
        state, t = l7.ingest(state, payload)
        if t is None:
            refused += 1
        require(state.occupancy <= cap,
                "occupancy %d exceeded the cap %d mid-stream (§4.1)"
                % (state.occupancy, cap))
    _RUN[cap] = (state, refused)
    return _RUN[cap]


# ---- 1. the invented warrant --------------------------------------------------

def trial_the_schema_accepts_an_invented_warrant_and_the_ledger_refuses_it():
    """`R8` clause 5(c) on an engine: 30 accepted by the law, 0 accepted as fact.

    The BEFORE is `ATTAINABILITY.md §9.3`'s and is reproduced here rather than
    cited alone, because the whole claim is a comparison and half of it measured
    on a policy would not be a comparison at all: after the caller re-ingests
    generation 1, **all 30** depth-2 answers cite a `t` that is one of the
    engine's own items, and `laws/t_provenance_schema.py` — the frozen validator,
    unedited since `[L0]` — accepts every one of them, because under `R6`
    clause 2 a re-ingested generation is an actually-ingested event with a real
    `t`.

    The AFTER is what `R8` clause 5(c) rules must catch it: **0** of those 30
    answers is reported as observed fact, and the thing that decides is the
    lineage ledger and not the tag. So the two numbers stand side by side —
    `30` and `0` — and neither may be quoted as the other. A later session that
    finds `laws/t_provenance_schema.py` green must not conclude the capital crime
    is covered; that file is exactly as green against the failure as against its
    absence.
    """
    state, _budget, b = _fresh()

    # Rung 1 only: the caller writes generation 1 back, and nothing else.
    after, _rungs, _canon = _l7score.promotion_ladder(l7, state, b, depths=(1,))
    generated_ts = set(range(b["n_events"], after.next_t))
    require_equal(len(generated_ts), 100,
                  "the caller must have written exactly generation 1 back")

    depth2 = [rec for rec in b["records"] if rec.get("depth") == 2]
    rows = _l7score.observe(l7, after, b, depth2)
    answered = [row for row in rows if row["status"] == "answer"]
    require_equal(len(answered), SCHEMA_ACCEPTS,
                  "the depth-2 rung of the artifact's own ladder")

    citing = 0
    accepted = 0
    ingested_max = after.next_t - 1
    for row in answered:
        support = row["provenance"]["support"]
        if any(t in generated_ts for t in support):
            citing += 1
        ok, _reason = validate_provenance(row["provenance"], ingested_max)
        if ok:
            accepted += 1
    require_equal(citing, SCHEMA_ACCEPTS,
                  "every depth-2 answer must now rest on a `t` the engine itself "
                  "produced — that is what the artifact's ladder is for")
    require_equal(accepted, SCHEMA_ACCEPTS,
                  "the FROZEN validator must accept all %d. If it stopped, §4.2 "
                  "would have been edited, and R8 clause 5(c)'s finding — that "
                  "the provenance law is blind to the failure the layer "
                  "activating it exists to prevent — would be being hidden "
                  "rather than answered" % (SCHEMA_ACCEPTS,))

    as_fact = sum(1 for row in answered if row["lineage"] != l7.GENERATED)
    require_equal(as_fact, ACCEPTED_AS_FACT,
                  "%d of the %d invented-warrant answers were reported as "
                  "observed fact. The schema accepts all %d and the LEDGER is "
                  "what refuses them (R8 clause 5(c)) — 30 and 0 are the two "
                  "halves of one finding" % (as_fact, len(answered),
                                             SCHEMA_ACCEPTS))

    blind_after, _r, _c = _l7score.promotion_ladder(
        LedgerBlind, state, b, depths=(1,))
    blind_rows = _l7score.observe(LedgerBlind, blind_after, b,
                                  [rec for rec in b["records"]
                                   if rec["declared"] == "G"])
    blind_as_fact = sum(1 for row in blind_rows
                        if row["status"] == "answer"
                        and row["lineage"] != l7.GENERATED)
    require_equal(blind_as_fact, 100,
                  "the ledger-blind fixture must call generation 1 fact at this "
                  "rung, or the 0 above is a property of the artifact rather "
                  "than of the ledger")


# ---- 2. the warrant the budget takes ------------------------------------------

def trial_a_generations_support_is_never_a_t_the_budget_took():
    """`R8` clause 5(a) measured under real pressure, and the prediction replaced.

    `ATTAINABILITY.md §7` disclaimed the loss-accounting reserve and named the
    failure it feared — *a generation whose support has been shed cites a `t` the
    forgetting record can only count* — and `STAGE-B.md §7` recorded that no
    in-budget battery could decide it. This decides it, on a declared ladder of
    caps over a 6 000-event prefix of the frozen artifact, and the measurement
    replaces the prediction:

    * the engine really does lose events at every rung of the ladder below the
      first — `forgotten` runs from 0 to nearly two thousand, with entities
      damaged by shedding at the bottom — so a 1000 here is not a generous
      budget;
    * **not one cited `t` is unreadable, at any cap.** The composition reading
      can only cite what it can still read, so a compound whose `part` episode
      the budget took is one the reading no longer determines and the engine
      **abstains** — `§3.0` pays 100 for that — rather than composing from a hole
      and citing it. Generation degrades from 160 answers to 0 across the ladder,
      by abstention throughout;
    * and **the forgetting record is consulted**: the set of `t` it booked is
      exactly the set `read(t)` abstains on, the closing-ledger identity Layers 4
      and 5 established, so the cited set and the lost set are disjoint by
      construction.

    **The stronger property is stated as a fact about this engine and NOT as a
    gate.** `R8` clause 5(a) demands *ingested* and not *recoverable*; an engine
    whose diagnostic read below 1000 would breach no `§5 L7` clause, and this
    trial asserts the diagnostic's value where it is measured while asserting
    nothing about what a different engine owes.
    """
    _state, _budget, b = _fresh()
    payloads = b["payloads"][:PREFIX]
    raw = sum(event_cost(p) for p in payloads)
    require(CAP_LADDER[0] <= raw,
            "the declared ladder must start at or below the prefix's own raw "
            "episodic footprint (%d), or its first rung is not a cap at all"
            % (raw,))

    generate_records = [rec for rec in b["records"] if rec["q"]["op"] == "generate"]
    profile = []
    for cap in CAP_LADDER:
        state, refused = _under_pressure(cap, payloads)
        require_equal(refused, 0,
                      "cap %d: %d writes were refused. This ladder is about "
                      "EVICTION, and a refusal means the cap was set below what a "
                      "single write costs" % (cap, refused))
        rows = _l7score.observe(l7, state, b, generate_records)
        answered = [row for row in rows if row["status"] == "answer"]
        generated = [row for row in answered if row["lineage"] == l7.GENERATED]

        dangling = 0
        cited = 0
        for row in answered:
            for t in row["provenance"]["support"]:
                cited += 1
                if l7.query(state, {"op": "read", "t": t})["status"] != "answer":
                    dangling += 1
        require_equal(dangling, 0,
                      "cap %d: %d of %d cited `t`s are ones this engine can no "
                      "longer produce. R8 clause 5(a) does not FORBID that — a "
                      "support entry must be ingested and not recoverable — so "
                      "what goes red here is the claim this file makes about "
                      "THIS engine, not a §5 L7 clause"
                      % (cap, dangling, cited))

        unreadable = sum(1 for t in range(state.next_t)
                         if l7.query(state, {"op": "read", "t": t})["status"]
                         != "answer")
        require_equal(unreadable, state.forgetting.count,
                      "cap %d: the engine abstains on %d logical times and the "
                      "forgetting record books %d. The closing ledger of Layers 4 "
                      "and 5 says those are one set: a loss booked as compression "
                      "is the defect BOUNDARY.log line 26 found, and a "
                      "compression booked as a loss is its mirror"
                      % (cap, unreadable, state.forgetting.count))
        if state.forgetting.count:
            require(state.forgetting.mass >= state.forgetting.count,
                    "cap %d: every loss carries at least its own weight" % (cap,))
        profile.append((cap, state.forgetting.count, len(state.damaged),
                        len(generated), cited))

    lost = [row[1] for row in profile]
    require(lost == sorted(lost),
            "the declared ladder must lose more as the cap falls, or it is not a "
            "pressure ladder: %r" % (profile,))
    require(lost[-1] > 0 and lost[0] == 0,
            "the ladder must span from a cap that loses nothing to one that loses "
            "a great deal, or a 1000 on the diagnostic proves nothing: %r"
            % (profile,))
    require(profile[-1][2] > 0,
            "the bottom of the ladder must reach SHEDDING — an entity marked "
            "`damaged` — because that is the path ATTAINABILITY.md §7 named when "
            "it feared *a generation whose support has been shed*: %r" % (profile,))
    answered_counts = [row[3] for row in profile]
    require(answered_counts[0] > 0 and answered_counts[-1] == 0,
            "generation must degrade from answering to abstaining across the "
            "ladder, which is the shape of the finding: %r" % (profile,))


def trial_the_support_recoverability_diagnostic_is_reported_and_never_gated():
    """`R8` clause 5(a)'s price, in budget and under pressure, and gating nothing.

    In budget the rate reads **1000** and `ATTAINABILITY.md §9.1` says so and
    calls it uninformative — *"what this clause buys is that it cannot quietly
    fail to exist once pressure arrives"*. Pressure arrives here, and it still
    reads 1000, for the reason the trial above measures.

    So the assertion is deliberately in two halves, and the second is the one that
    matters: the diagnostic **exists and is measured** at every rung where the
    engine answers anything, and **no `§5 L7` clause is applied to it**. This file
    declares no gate constant, `laws/t_rulings.py` authorizes none for it, and a
    rate below 1000 would be a fact about a budget rather than a breach of `§4.2`
    — which is exactly what the shape-only reading means and exactly what a gate
    here would deny.
    """
    state, _budget, b = _fresh()
    rows = _l7score.observe(l7, state, b)
    in_budget = _l7score.support_recoverability(l7, state, rows)
    require(in_budget["cited"] > 0, "the diagnostic must be measured")
    require_equal(in_budget["rate"], Fraction(1),
                  "in budget every cited `t` is recoverable and the diagnostic is "
                  "uninformative — stated rather than hidden")
    require_equal(_l7score.permille(in_budget["rate"]), 1000, "in permille")

    payloads = b["payloads"][:PREFIX]
    generate_records = [rec for rec in b["records"] if rec["q"]["op"] == "generate"]
    measured = 0
    for cap in CAP_LADDER:
        pressed, _refused = _under_pressure(cap, payloads)
        under = _l7score.support_recoverability(
            l7, pressed, _l7score.observe(l7, pressed, b, generate_records))
        if under["cited"] == 0:
            require(under["rate"] is None,
                    "cap %d: an empty diagnostic must read n/a and never 1 — the "
                    "same arithmetic R8 clause 3(c) turns into a disqualification "
                    "for a gated ratio, here turning into an honest absence for "
                    "an ungated one" % (cap,))
            continue
        measured += 1
        require_equal(under["rate"], Fraction(1),
                      "cap %d: the diagnostic reads %s. It is REPORTED and never "
                      "gated (R8 clause 5(a)), so this asserts what this engine "
                      "does and imposes nothing on what another owes"
                      % (cap, under["rate"]))
    require(measured >= 2,
            "the diagnostic must be measured at more than one pressured cap, or "
            "the ladder is reporting a single point as a property")

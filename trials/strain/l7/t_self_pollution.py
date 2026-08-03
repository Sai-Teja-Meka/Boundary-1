"""strain/l7 — THE MANDATORY LAYER-7 SELF-POLLUTION STRAIN (BOUNDARY.md §6).

`§6` names exactly one strain in the constitution's own frozen text, and it is
this one:

> This class includes the **mandatory Layer 7 self-pollution strain**: the engine
> re-ingests its own generations three deep, provenance/lineage chains must
> survive, and consolidation must never promote generated-lineage content to
> observed fact.

No other Schacter sin's assignment enjoys that: `autopsy/GAPMAP.md §6` **maps**
the other six, and the constitution **schedules** this one. The post-L6 PULSE
(`BOUNDARY.log` line 42) recorded the consequence — *suggestibility is
structurally L7's and not a gap*, because its literal form (misleading external
input incorporated) requires an act no layer below 7 performs: **the caller
re-ingesting the engine's own output as ordinary fuel**. Layer 5 came nearest,
being the first layer at which the engine writes events the caller did not
submit, and the guard there is that the emitted payload is byte-for-byte the
caller's own (`§1.4`), which is exactly why it is not suggestibility.

Here it is. The caller writes the engine's own compositions back at it, three
generations deep, over `corpora/l7compose`'s own ladder — 30 chains whose depth-2
compound is formed from a depth-1 **generated** item and whose depth-3 is formed
from that, with every one of those profiles withheld and the lineage depth
**decidable from the frozen bytes** (`R8` clause 1, and `ops/l7/t_l7compose.py`
recomputes it from the stream alone). So the rungs are the artifact's and not an
engine's account of itself.

## What is asserted, and what is only cited

`§5 L7` gates `promotion = 0` three deep and `R8` clause 5(c) rules **who
enforces it**: the ascension battery and this strain, keyed on **lineage**, and
never `laws/t_provenance_schema.py`, because the frozen validator accepts a tag
citing a re-ingested generation — such a `t` is an actually-ingested event under
`R6` clause 2. `ascension/l7/t_generation.py` applies the clause; this attacks
it, and the division is the standing one-fixture-one-truth discipline:

| claim | owned by |
|---|---|
| the exhibited witness's ladder, `0/0/0` with 160 still generated | `ascension/l7/t_attainability.py` |
| the ledger-blind **policy** promoting 100, 130, 160 | the same file |
| the gate clause applied to the engine | `ascension/l7/t_generation.py` |
| **the same failure reproduced on the ENGINE**, and what the ledger costs to keep | here |

## The three things this strain adds that the battery cannot

1. **The ledger is checked against the ARTIFACT's declared table, rung by rung.**
   The engine's own account of what it made is read through `§7` alone
   (`{"op":"lineage"}`) and required to agree, entity by entity, with the depth
   `corpora/l7compose` declares — so an engine that kept a ledger of the right
   *size* and the wrong *content* goes red.
2. **The teeth are demonstrated on an engine and not on a policy.** A
   **ledger-blind fixture** — this engine with one field emptied at the read, a
   trial fixture and never engine code, in the shape `strain/l3`'s naive
   reference count and `strain/l5`'s ledger-blind firing policy established —
   promotes 100, then 130, then all 160, and three deep calls every one of its
   own dreams a fact. That is `autopsy/GAPMAP.md §2`'s engine thesis (*every
   system autopsied writes the metadata that would make it correct and then never
   reads it where it counts*) turned on **our own engine**, at the one field this
   layer exists to fill.
3. **Novelty stops being the right question at depth, and the number says so.**
   `§5 L7`'s `novelty = 1000` is a canonical-byte comparison against the ingested
   store, and after the caller writes a generation back the store **contains it**.
   Measured on the grown store, the engine's still-generated items that are still
   *byte-absent* fall `60 → 30 → 0` while `tagging` holds and `promotion` stays
   0. At rung 3 a byte-comparison would call this engine a liar about every item
   it made. What keeps it honest is the ledger, which is precisely why `R8`
   clause 3 binds novelty's denominator to the items the engine **tags** rather
   than to the store, and why `promotion = 0` is a separate clause at all.
"""

from _harness import require, require_equal
from adapters import l7

import _l7score
import _l7tasks
from _l7fixtures import LedgerBlind

# §5 L7's own clause, applied at depth. Registered in `laws/t_rulings.py` against
# `§5 L7` and `R8` — the same clause and the same ruling the ascension battery's
# copy carries, so the two cannot drift apart. It is declared here because this
# file APPLIES it (at every rung, to an engine) rather than merely standing at a
# pressure, which is why `strain/l5`'s blocking seam declared none and this does.
GATE_PROMOTION = 0

LAYER_CAP = 7

# What the artifact declares and what the ladder must reproduce. Every figure is
# `corpora/l7compose`'s own: 100 depth-1 compounds in the forcing region, and 30
# chains carrying one depth-2 and one depth-3 compound each.
DECLARED_RUNGS = (1, 2, 3)
DECLARED_EMITTED = (100, 30, 30)
DECLARED_LEDGER = ({1: 100}, {1: 100, 2: 30}, {1: 100, 2: 30, 3: 30})

# The byte-novel share of what the engine still calls generated, measured against
# the store AS IT NOW IS at each rung. It falls to zero; `tagging` does not.
DECLARED_STILL_BYTE_NOVEL = (60, 30, 0)

# The ledger-blind fixture's ladder — the teeth, on an engine. It is the same
# triple `ATTAINABILITY.md §5.1` measures for the ledger-blind POLICY, which is
# what "one instrument, two implementations" looks like at the level of a failure
# mode rather than of a score.
BLIND_PROMOTION = (100, 130, 160)
BLIND_STILL_GENERATED = (60, 30, 0)

_RUN = {}


def _fresh():
    """The engine over the whole binding artifact, in budget, replayed once."""
    if "run" not in _RUN:
        b = _l7score.battery()
        state, budget = _l7score.replay(
            l7, lambda cap: l7.make_engine(LAYER_CAP, cap), b, l7.DEFAULT_BUDGET)
        _RUN["run"] = (state, budget, b)
    return _RUN["run"]


def _ledger(state):
    """The engine's own account of what it made, read through `§7` alone."""
    answer = l7.query(state, {"op": "lineage"})
    require_equal(answer["status"], "answer",
                  "the lineage diagnostic must answer through §7")
    value = answer["value"]
    return {rung: n for rung, n in value["by_rung"]}, value


# ---- 1. the ladder, three deep ----------------------------------------------

def trial_three_generations_of_re_ingestion_promote_nothing_at_any_rung():
    """`§5 L7`'s `promotion = 0` **three deep**, attacked rather than applied.

    The caller — this trial, which is what makes it suggestibility in
    `autopsy/GAPMAP.md §6`'s literal sense — takes the items the engine tagged
    `generated` at a depth and writes them back as ordinary payloads. The store
    then **carries** them: retrieval answers them, their canonical bytes are in
    it, and a depth-2 composition genuinely reads a depth-1 generation as its
    material. Nothing but a lineage record can still say what they are.

    Scored at every rung because a ladder checked only at depth 3 cannot say
    **where** a break occurred, and the anti-silence guard is asserted with it:
    an engine that stopped calling its own generations generated would be
    promoting by attrition, and a `promotion` of 0 bought that way is a number
    and not a claim.
    """
    state, _budget, b = _fresh()
    _after, rungs, _canon = _l7score.promotion_ladder(l7, state, b)

    require_equal(tuple(r["depth"] for r in rungs), DECLARED_RUNGS,
                  "the ladder is three deep (§5 L7, and §6 names it)")
    require_equal(tuple(r["emitted"] for r in rungs), DECLARED_EMITTED,
                  "the caller re-ingested a different number of the engine's own "
                  "items than the artifact declares at each depth — the rungs are "
                  "corpora/l7compose's and not an engine's account of itself")
    for rung in rungs:
        require_equal(rung["promotion"], GATE_PROMOTION,
                      "at depth %d the engine promoted %d of its own re-ingested "
                      "generations to observed fact. §5 L7 gates this at %d three "
                      "deep, and §6 puts the clause in this class as well as in "
                      "the gate" % (rung["depth"], rung["promotion"],
                                    GATE_PROMOTION))
        require_equal(rung["still_generated"], len(b["generation_class"]),
                      "at depth %d the engine reports %d of %d generation-required "
                      "answers as generated — a promotion count of 0 bought by "
                      "falling silent is promotion by attrition"
                      % (rung["depth"], rung["still_generated"],
                         len(b["generation_class"])))
    require_equal(tuple(r["store"] for r in rungs),
                  (b["n_events"] + 100, b["n_events"] + 130, b["n_events"] + 160),
                  "the store must grow by exactly what the caller wrote into it "
                  "and by nothing else — a generation is a `query` answer and not "
                  "an event until the caller ingests it (R8 clause 2)")


def trial_the_lineage_ledger_agrees_with_the_artifacts_declared_depths():
    """*"provenance/lineage chains must survive"* — §6, as an identity on the ARTIFACT.

    The engine's own account of what it made is read through `§7` alone
    (`{"op":"lineage"}`, the shape `consolidation`, `prospection` and
    `calibration` established for a layer's own diagnostic) and is required to
    agree **entity by entity** with the depth `corpora/l7compose` declares — a
    table `ops/l7/t_l7compose.py` recomputes from the frozen stream and never
    from an engine.

    So an engine keeping a ledger of the right size and the wrong content goes
    red here, and so does one whose rungs drift: the ledger is not a counter, it
    is a claim about which item came from where, and `ATTAINABILITY.md §7` prices
    it as one — 2 cells an entry, 320 for this artifact's 160.
    """
    state, _budget, b = _fresh()

    by_rung, value = _ledger(state)
    require_equal(by_rung, {},
                  "the engine's ledger is not empty after the plain replay — the "
                  "frozen stream carries no generation of its own, so an entry "
                  "here is an observation the engine has called its own work")
    require_equal(value["cells"], 0, "an empty ledger costs no cells (rule P)")

    after = state
    declared = _l7tasks.lineage_table()
    for depth, want in zip(DECLARED_RUNGS, DECLARED_LEDGER):
        after, rungs, _canon = _l7score.promotion_ladder(
            l7, after, b, depths=(depth,))
        by_rung, value = _ledger(after)
        require_equal(by_rung, want,
                      "after depth %d the engine's ledger reads %r against the "
                      "artifact's declared %r" % (depth, by_rung, want))
        require_equal(value["generated"], sum(want.values()),
                      "the ledger's own total disagrees with its rungs")
        require_equal(value["cells"],
                      l7.LINEAGE_ENTRY_CELLS * sum(want.values()),
                      "the ledger's cost is not rule P's 2 cells an entry — "
                      "ATTAINABILITY.md §7 prices it BY NAME and R5 clause 4 "
                      "forbids an unpriced item, not a cheaper one")
        wrong = sorted((entity, rung) for entity, rung in after.lineage.items()
                       if declared.get(entity) != rung)
        require_equal(wrong, [],
                      "the engine's ledger disagrees with the artifact's declared "
                      "lineage depths at %r — the depth is decidable from the "
                      "frozen bytes (R8 clause 1), so this is the engine's claim "
                      "checked against the artifact and not against itself"
                      % (wrong[:6],))
    require_equal(l7.accounted_occupancy(after), after.occupancy,
                  "the incremental accounting drifted from the state's own atoms "
                  "once the ledger was written — the ledger is state (§4.1) and "
                  "rule P prices it, so it is counted where every other branch is")


def trial_the_capital_crime_is_still_caught_three_deep():
    """The teeth, on an ENGINE: a ledger that is written and never read.

    `autopsy/GAPMAP.md §2`'s engine thesis convicted four systems of writing the
    metadata that would make them correct and then never reading it where it
    counts — `generative-agents` writing an expiration consulted by nothing,
    `mem0`'s contradictions coexisting silently, `graphiti` invalidating and then
    not honouring `invalid_at` at read, `letta`'s self-edit tools validating
    structure and never a value. The lineage ledger is the one field a Layer-7
    engine could most plausibly write and never read, so it is asserted **read**,
    by emptying it at the answer and measuring what happens.

    What happens is the whole clause: the fixture promotes 100 at depth 1, 130 at
    depth 2 and all 160 at depth 3, and three deep it calls every one of its own
    dreams a fact. `ATTAINABILITY.md §5.1` measures exactly those three numbers
    for the ledger-blind POLICY, before any engine existed; that they recur here
    on an engine is one instrument and two implementations at the level of a
    failure mode.
    """
    state, _budget, b = _fresh()
    _after, rungs, _canon = _l7score.promotion_ladder(LedgerBlind, state, b)

    require_equal(tuple(r["promotion"] for r in rungs), BLIND_PROMOTION,
                  "the ledger-blind fixture must promote at every rung, or this "
                  "strain has no teeth and `promotion = 0` is a property of the "
                  "artifact rather than of the engine")
    require_equal(tuple(r["still_generated"] for r in rungs),
                  BLIND_STILL_GENERATED,
                  "the fixture's remaining generations are exactly the items not "
                  "yet in its store, which is what makes its 0 at depth 3 a "
                  "confession and not a silence")
    require_equal(rungs[-1]["still_generated"], 0,
                  "three deep, the ledger-blind fixture calls every one of its "
                  "own dreams a fact")

    # And the fixture differs from the engine in exactly one place: it WRITES the
    # ledger and refuses to READ it. Asserted, so that a fixture which had
    # quietly become a different engine could not be mistaken for a measurement
    # of this one.
    probe, _t = l7.ingest(l7.make_engine(LAYER_CAP, l7.DEFAULT_BUDGET),
                          {"kind": "spawn", "entity": 1, "class": "node"})
    require_equal(LedgerBlind.query(probe, {"op": "read", "t": 0}),
                  l7.query(probe, {"op": "read", "t": 0}),
                  "the ledger-blind fixture must be this engine everywhere but at "
                  "a `generate` answer")


def trial_novelty_stops_being_the_right_question_at_depth_and_the_ledger_does_not():
    """The finding this ladder produces that no `§5 L7` clause states.

    `novelty = 1000` is *"provably never-stored"* — a canonical-byte comparison
    against the ingested store — and the ascension battery measures it on the
    plain replay, where it is exactly the right question. **After the caller
    writes a generation back, it is not.** The store now carries the item, so a
    byte comparison against the store as it *now is* says the engine's own
    composition is not novel — while the item's lineage has not changed at all,
    because lineage is a property of where an item came from and the store is a
    fact about where it has been since.

    Measured: the byte-novel share of what the engine still calls generated falls
    `60 → 30 → 0` across the three rungs, while `tagging` holds and `promotion`
    stays 0. **At rung 3 a byte-comparison would call this engine a liar about
    every item it made**, and the ledger is what keeps it honest.

    That is why `R8` clause 3 binds `novelty`'s denominator to the items the
    engine **tags** rather than to the store, why `promotion = 0` is a separate
    clause from `novelty = 1000` at all, and why `R8` clause 5(c) puts the
    capital crime's enforcement on lineage rather than on any comparison `§4.2`
    or `§3.0` can make.
    """
    state, _budget, b = _fresh()

    store_canon = set(b["store_canon"])
    g_records = [rec for rec in b["records"] if rec["declared"] == "G"]
    after = state
    measured = []
    for depth in DECLARED_RUNGS:
        at_depth = [rec for rec in g_records if rec.get("depth") == depth]
        emitted = [row["value"] for row in _l7score.observe(l7, after, b, at_depth)
                   if row["status"] == "answer" and row["lineage"] == "generated"]
        for item in emitted:
            after, t = l7.ingest(after, item)
            require(t is not None, "the caller's re-ingestion was refused")
            store_canon.add(_l7tasks.canon(item))
        rows = _l7score.observe(l7, after, b, g_records)
        generated = [row for row in rows if row["status"] == "answer"
                     and row["lineage"] == "generated"]
        measured.append(sum(1 for row in generated
                            if _l7tasks.canon(row["value"]) not in store_canon))
        require_equal(len(generated), len(b["generation_class"]),
                      "the engine stopped calling its generations generated at "
                      "depth %d" % (depth,))

    require_equal(tuple(measured), DECLARED_STILL_BYTE_NOVEL,
                  "the byte-novel share of the engine's own generations, measured "
                  "against the store as it now is, drifted from %r — the ladder "
                  "is what makes the number fall, and the point is that it falls "
                  "to zero while nothing about the items' lineage changes"
                  % (DECLARED_STILL_BYTE_NOVEL,))
    require_equal(measured[-1], 0,
                  "three deep, every item the engine made is in the store it was "
                  "made from. A gate that read novelty against the store here "
                  "would fail an engine for having been believed")

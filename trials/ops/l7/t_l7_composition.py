"""ops/l7 — the Layer-7 engine's composition: one reading, two implementations.

The Layer-4 analogue of this file asserted the facet map against the battery's
own reading **event by event on all 80 000 events of all three corpora**, because
a divergence there would move the ANSWER of `current()` and not merely its
availability; `ops/l5` did the same for the condition grammar and the intention
facet, and `ops/l6` for the set-once reading and the tie ladder. This is that
discipline at Layer 7, where the stakes are one step higher again: the
composition reading decides what an item *is*, so a divergence would move a
**generated value** — the one thing in this project that no stored event can be
checked against.

`COMPOSITION_FORM` is a **declared reading of the frozen grammar**, in the shape
`ASSERTION_FORMS` (L4), `INTENTION_FORM` (L5) and `SET_ONCE_KEYS` (L6) already
have. `corpora/l7compose/generator.py` declares it, `trials/_l7tasks.py`
implements it over a payload list with no engine in the loop, and
`core/layers/l7_generation.py` implements it over the engine's **own state**.
Three statements of one rule; this file is where they are checked against each
other rather than assumed to agree.

Nothing here applies a `§5` clause, and there is no gate constant in this file
for `laws/t_rulings.py` to authorize.
"""

from _harness import require, require_equal
from adapters import l6, l7
from core.layers import l6_meta_memory as l6m
from core.state import event_cost
from corpora.sessions import generator as sessions_gen

import _l7score
import _l7tasks

LAYER_CAP = 7

# `strain/l7/t_generation_seam.py`'s own middle rung, reused here so the two
# files describe one pressured state and not two: a 6 000-event prefix of the
# frozen artifact at a cap where the engine is losing events (187 of them) and
# can still compose 39 of the 100 depth-1 items.
PRESSURE_PREFIX = 6000
PRESSURE_CAP = 19000

_RUN = {}


def _replayed():
    """The engine over the whole binding artifact, in budget, replayed once."""
    if "state" not in _RUN:
        b = _l7score.battery()
        state, _budget = _l7score.replay(
            l7, lambda cap: l7.make_engine(LAYER_CAP, cap), b, l7.DEFAULT_BUDGET)
        _RUN["state"] = (state, b)
    return _RUN["state"]


# ---- one reading, two implementations ---------------------------------------

def trial_the_engines_composition_rule_is_the_declared_one():
    """The rule itself: the engine's `compose` and the artifact's are one function.

    Checked over the whole declared vocabulary rather than on a sample — 8 hues ×
    6 grades is small enough that a spot check would be a choice and an
    exhaustive one is not.
    """
    require_equal(l7.HUES, _l7tasks.HUES, "the declared hue vocabulary")
    require_equal(l7.GRADES, _l7tasks.GRADES, "the declared grade vocabulary")
    require_equal(l7.PROFILE_FORM, _l7tasks.gen.PROFILE_FORM,
                  "the declared item grammar")
    require_equal((l7.HUE_KEY, l7.MASS_KEY, l7.COMPOUND_CLASS),
                  (_l7tasks.HUE_KEY, _l7tasks.MASS_KEY, _l7tasks.COMPOUND_CLASS),
                  "the declared material keys and compound class")

    checked = 0
    for h0 in l7.HUES:
        for h1 in l7.HUES:
            for m0, m1 in ((1, 1), (7, 41), (99, 99), (0, 5)):
                mine = l7.compose(h0, m0, h1, m1, 700000)
                theirs = _l7tasks.gen.compose(h0, m0, h1, m1, 700000)
                require_equal(mine, theirs,
                              "the engine composes (%s,%d)+(%s,%d) differently "
                              "from the artifact's own rule" % (h0, m0, h1, m1))
                require(l7.profile_form_ok(mine),
                        "a composed item must satisfy the declared item grammar")
                require_equal(l7.profile_form_ok(mine),
                              _l7tasks.gen.profile_form_ok(mine),
                              "the two grammar validators disagree")
                checked += 1
    require_equal(checked, len(l7.HUES) * len(l7.HUES) * 4,
                  "the cross product must be walked in full")

    for bad in ({"kind": "profile", "entity": 1, "grade": "crude", "hue": "amber"},
                {"kind": "profile", "entity": 1, "grade": "nope", "hue": "amber",
                 "mass": 3},
                {"kind": "profile", "entity": 1, "grade": "crude", "hue": "puce",
                 "mass": 3},
                {"kind": "profile", "entity": -1, "grade": "crude", "hue": "amber",
                 "mass": 3},
                {"kind": "profile", "entity": 1, "grade": "crude", "hue": "amber",
                 "mass": True},
                "not an object"):
        require(not l7.profile_form_ok(bad),
                "the engine's item grammar accepted %r, so `validity = 1000` "
                "would be a measurement of nothing" % (bad,))


def trial_the_engine_composes_from_state_what_the_battery_composes_from_bytes():
    """The reading, entity by entity, over every compound the artifact declares.

    Two implementations of one rule reading two different things — the engine
    reads its own interval table and its own retained `part` and `profile`
    episodes, the battery reads the frozen payload list — and they must agree on
    **both halves** of the answer: the composed item, and the `support` the rule
    read to build it. The second is what `R8` clause 5(b) binds relevance on, so a
    divergence there is a provenance defect and not merely an internal one.

    The population is every compound with a `part` edge in the frozen stream —
    the 100 mirror pairs, the 30 ladder chains' two rungs each, and the 100
    incomposable probes where **both** implementations must return nothing.
    """
    state, _b = _replayed()
    reading = _l7tasks.base_reading()
    parts = l7.parts_of(state)
    profiles = l7.profiles_of(state)

    require_equal(sorted(parts), sorted(reading.parts),
                  "the engine reads a different set of compounds out of its own "
                  "state than the frozen stream carries — `part` has no Layer-4 "
                  "facet, so it is held as an irreducible episode and read back "
                  "from the row codec, and this is where that reading is checked")
    require_equal(sorted(profiles), sorted(reading.profile_at),
                  "the engine reads a different set of stored profiles than the "
                  "stream carries")

    composed = silent = 0
    for entity in sorted(parts):
        mine = l7.composed_only(state, parts, profiles, entity)
        theirs = reading.composed_only(entity)
        if theirs is None:
            require(mine is None,
                    "entity %d: the engine composed an item where the declared "
                    "rule is SILENT. That is the KU1 class — one component's "
                    "mass is never asserted — and composing anything there is "
                    "the fabrication §3.0 prices at 0" % (entity,))
            silent += 1
            continue
        require(mine is not None,
                "entity %d: the engine composed nothing where the declared rule "
                "determines an item" % (entity,))
        require_equal(mine[0], theirs[0],
                      "entity %d: the engine's composed ITEM differs from the "
                      "declared rule's" % (entity,))
        require_equal(mine[1], theirs[1],
                      "entity %d: the engine's SUPPORT differs from the `t`s the "
                      "declared rule reads — R8 clause 5(b) binds relevance on "
                      "exactly this tuple" % (entity,))
        composed += 1

        stored = l7.profile_of(state, parts, profiles, entity)
        require_equal(stored, reading.profile(entity),
                      "entity %d: the two readings disagree about whether the "
                      "store already holds this item" % (entity,))

    require_equal(silent, _l7tasks.gen.INCOMPOSABLE,
                  "the declared incomposable class")
    require_equal(composed, 2 * _l7tasks.PAIRS + 2 * _l7tasks.LADDER,
                  "every mirror-pair member and every ladder rung must compose")


# ---- the lineage signature, and the condition that makes the bound tight ------

def trial_the_ingest_time_lineage_signature_is_unambiguous_on_this_artifact():
    """What the ledger can know at `ingest`, measured in both directions.

    `§7.1` makes `query` pure, so the ledger can only be written by `ingest`
    (`STAGE-B.md §5.1`), and at `ingest` the engine has no memory of what it
    answered — only the shape of its own store. `README-l7 §1` states the rule as
    an **upper bound**: a coincidence marks an observation as generated, which
    can only make the engine refuse to promote and never promote wrongly.

    This is the measurement that makes the bound **tight on this artifact**, and
    it is the measurement a later artifact would have to repeat:

    * **no false positive.** Replaying the frozen stream, `own_generation` is
      `False` for every one of the 100 `profile` events it carries, checked
      against the state as it stood **before** each arrived. The reason is a
      property of the frozen bytes — the only compounds sharing a composed item
      modulo `entity` are the mirror twins, and a pair's other member's profile is
      never in the stream — so the signature cannot fire on an observation.
    * **no false negative.** For every one of the 100 generation-required
      compounds, the item the engine composes is recognised as its own when the
      caller writes it back, which is what makes the depth-1 rung of the ladder
      hold at all.
    """
    b = _l7score.battery()
    state = l7.make_engine(LAYER_CAP, l7.DEFAULT_BUDGET)
    arrivals = 0
    for payload in b["payloads"]:
        if isinstance(payload, dict) and payload.get("kind") == l7.PROFILE_KIND:
            arrivals += 1
            require(not l7.own_generation(state, payload),
                    "the engine claimed the stream's own `profile` event for "
                    "entity %r as its own work. The frozen stream carries no "
                    "generation of this engine's, so every arrival here is an "
                    "OBSERVATION and marking one would make the engine refuse to "
                    "promote a fact it was told" % (payload.get("entity"),))
        state, t = l7.ingest(state, payload)
        require(t is not None, "an in-budget write was refused")
    require_equal(arrivals, _l7tasks.PAIRS,
                  "the artifact stores exactly one profile per mirror pair — the "
                  "coin decides which member, and the other is withheld")
    require_equal(state.lineage, {},
                  "the ledger must be EMPTY after the frozen stream: an entry "
                  "here is an observation the engine has called its own work")

    parts = l7.parts_of(state)
    profiles = l7.profiles_of(state)
    recognised = 0
    for pair in _l7tasks.declared()["pairs"]:
        entity = pair["generated"]
        built = l7.composed_only(state, parts, profiles, entity)
        require(built is not None,
                "pair %d: the withheld member must be composable" % (pair["pair"],))
        require(l7.own_generation(state, built[0], parts, profiles),
                "pair %d: the engine would NOT recognise its own composition for "
                "entity %d if the caller wrote it back — the depth-1 rung of the "
                "self-pollution ladder rests on this, and a false negative here "
                "is a promotion" % (pair["pair"], entity))
        require_equal(l7.lineage_rung(state, entity, parts), 1,
                      "a compound composed from asserted material is rung 1")
        recognised += 1
    require_equal(recognised, _l7tasks.PAIRS, "the whole forcing region")


# ---- the state: Layer 6's, plus one branch and no more -----------------------

def trial_the_layer7_state_is_the_layer6_state_plus_the_ledger_and_nothing_else():
    """The zero-state precedent, honoured where it can be and priced where it cannot.

    `README-l6 §0` recorded that Layer 6 added **no** field, because `§5.1 L6`
    said meta-memory derives confidence *"from existing state"*. `§5 L7` says no
    such thing, and Stage B measured why it could not: `query` is pure, so a
    lineage ledger can only be written by `ingest`. **One** field is added, and
    this asserts it is one — on a stream that carries no composition at all, the
    Layer-7 body differs from the Layer-6 body in exactly two branches, and the
    second of them is empty.

    So the layer costs nothing where it does nothing, which is what
    `inheritance/l7`'s five in-budget identity rows silently stand on: a ledger
    that charged for streams with no generation in them would compete with a
    pending set and a fired ledger that `README-l5 §0.1` puts outside every
    eviction phase on purpose.
    """
    payloads = list(sessions_gen.generate(sessions_gen.SEED, 400))
    cap = 4 * sum(event_cost(p) for p in payloads)

    s7 = l7.make_engine(LAYER_CAP, cap)
    s6 = l6.make_engine(6, cap)
    for payload in payloads:
        s7, t7 = l7.ingest(s7, payload)
        s6, t6 = l6.ingest(s6, payload)
        require_equal(t7, t6, "the two engines assigned different logical times")

    require_equal(s7.lineage, {},
                  "a composition-free stream must leave the ledger empty")
    require_equal(l7.lineage_cells(s7.lineage), 0,
                  "an empty ledger costs no cells (rule P)")
    require_equal(s7.occupancy, s6.occupancy,
                  "the Layer-7 engine holds %d cells where the Layer-6 engine "
                  "holds %d on the same stream — the ledger is the only field "
                  "this layer adds, and on a stream with nothing to record it "
                  "must add nothing" % (s7.occupancy, s6.occupancy))
    require_equal(l7.accounted_occupancy(s7), s7.occupancy,
                  "the incremental accounting drifted from the state's own atoms")

    body7 = l7._body(s7) if hasattr(l7, "_body") else None
    from core.layers import l7_generation as l7m
    body7 = l7m._body(s7)
    body6 = l6m._body(s6)
    differing = sorted(set(body7) - set(body6))
    require_equal(differing, ["lineage"],
                  "the Layer-7 body carries branches the Layer-6 body does not: "
                  "%r. One field, and it is the one Stage B measured to be "
                  "forced" % (differing,))
    moved = sorted(k for k in body6 if body6[k] != body7[k])
    require_equal(moved, ["layer_cap"],
                  "the Layer-7 body differs from the Layer-6 body in %r — the "
                  "recorded cap is the cap and not the content, and everything "
                  "else Layer 7 holds it holds because Layer 6 did" % (moved,))

    for t in (0, 3, 199, len(payloads) - 1):
        require_equal(l7.query(s7, {"op": "read", "t": t}),
                      l6.query(s6, {"op": "read", "t": t}),
                      "read(t=%d) is not the Layer-6 Answer, byte for byte — "
                      "`lineage` is added to a `generate` Answer and to nothing "
                      "else (R8 clause 2)" % (t,))


def trial_the_ledger_is_priced_under_rule_p_and_is_not_evictable():
    """`ATTAINABILITY.md §7`'s 320 cells, in code, and the tier that does not give way.

    Rule P is one cell, one grammar atom, and a ledger entry is an entity and its
    rung. So the price is 2 cells an entry, the snapshot body carries exactly
    those two atoms per entry, and the two numbers are the same number.

    **The ledger is outside every eviction phase, and that is the layer rather
    than a convenience** — a lineage entry an engine dropped is a generation it
    could promote, so an eviction path reaching it would be an engine that can be
    made to break `§5 L7`'s `promotion = 0` by being poor. It is the rule
    `README-l5 §0.1` fixed for the two prospection tiers, applied to the tier
    this layer adds, and it is asserted where the episodic tier is being emptied
    around it.
    """
    state, b = _replayed()
    after, rungs, _canon = _l7score.promotion_ladder(l7, state, b)
    require_equal(len(after.lineage), 160, "the ladder's own 160 entries")
    require_equal(l7.lineage_cells(after.lineage), 320,
                  "ATTAINABILITY.md §7 prices the ledger BY NAME at 320 cells for "
                  "this artifact's 160 generated items — 2 cells an entry under "
                  "rule P, and the engine must charge itself that and no less")
    require_equal(l7.accounted_occupancy(after), after.occupancy,
                  "the ledger is counted where every other branch is")

    from core.layers import l7_generation as l7m
    body = l7m._body(after)
    atoms = sum(len(row) for row in body["lineage"])
    require_equal(atoms, l7.lineage_cells(after.lineage),
                  "the atoms a reader can count in the serialized ledger (%d) "
                  "differ from the cells the engine charged itself (%d) — that "
                  "drift is exactly what rule P exists to forbid"
                  % (atoms, l7.lineage_cells(after.lineage)))

    # Under real pressure the EPISODIC tier gives way and the ledger does not.
    # The declared cap is `strain/l7`'s own middle rung, where the engine is
    # losing events and can still compose 39 of the 100 depth-1 items.
    payloads = b["payloads"][:PRESSURE_PREFIX]
    pressed = l7.make_engine(LAYER_CAP, PRESSURE_CAP)
    for payload in payloads:
        pressed, _t = l7.ingest(pressed, payload)
    lost_before = pressed.forgetting.count
    require(lost_before > 0,
            "the pressured replay must actually be evicting, or the claim below "
            "is about a state under no pressure at all")

    depth1 = [rec for rec in b["records"] if rec.get("depth") == 1]
    items = [row["value"] for row in _l7score.observe(l7, pressed, b, depth1)
             if row["status"] == "answer" and row["lineage"] == l7.GENERATED]
    require(len(items) > 0,
            "the pressured engine must still compose something, or there is no "
            "ledger entry for the budget to be unable to take")
    for item in items:
        pressed, t = l7.ingest(pressed, item)
        require(t is not None, "the caller's write was refused under pressure")

    require_equal(len(pressed.lineage), len(items),
                  "every item the caller wrote back must be in the ledger")
    require(pressed.forgetting.count > lost_before,
            "the episodic tier did not give way to make room — the claim is that "
            "the LEDGER is what does not, so something else must")
    require(pressed.occupancy <= PRESSURE_CAP, "the budget law held (§4.1)")
    for entity in sorted(pressed.lineage):
        require_equal(l7.query(pressed, {"op": "lineage", "entity": entity})
                      ["status"], "answer",
                      "entity %d left the ledger under pressure — the tier is "
                      "outside every eviction phase, because a dropped entry is "
                      "a generation this engine could promote" % (entity,))
    require_equal(l7.accounted_occupancy(pressed), pressed.occupancy,
                  "the accounting drifted under eviction")


def trial_only_a_generate_answer_carries_a_lineage_field():
    """`R8` clause 2 adds ONE field to ONE op, and the restraint is asserted.

    `§7.2` declares four keys. `R8` clause 2 ratifies that a `generate` Answer
    carries the item, its confidence, its provenance tag **and** its lineage, and
    clause 4 rules what the lineage is. Nothing says every Answer gains a field,
    and this engine does not give one: `read`, `read_range`, `recall`, `current`,
    `asof`, `fired`, `profile` and the diagnostics return the Layer-6 Answer byte
    for byte.

    That is why `inheritance/l7`'s six rows are green for a **structural** reason:
    an engine that decorated every Answer would be handing five older scorers a
    field they were never written against, and the Layer-6 row — the one this
    layer could actually break — would be the last place anyone looked.
    """
    state, b = _replayed()
    four = {"status", "value", "confidence", "provenance"}

    gen_q = next(rec["q"] for rec in b["records"] if rec["q"]["op"] == "generate")
    answer = l7.query(state, gen_q)
    require_equal(set(answer), four | {"lineage"},
                  "a `generate` Answer carries §7.2's four keys and `lineage`, "
                  "and nothing else: %r" % (sorted(answer),))
    require(answer["lineage"] in l7.LINEAGE_VOCAB,
            "the lineage vocabulary is closed at R8 clause 4's two values")

    cur_q = next(rec["q"] for rec in b["records"] if rec["q"]["op"] == "current")
    for q in (cur_q,
              {"op": "read", "t": 0},
              {"op": "read_range", "t0": 0, "t1": 3},
              {"op": "calibration"},
              {"op": "lineage"},
              {"op": "no_such_op"},
              {"op": "generate", "cue": {"kind": "profile", "entity": -1}}):
        got = l7.query(state, q)
        require_equal(set(got), four,
                      "%r returned an Answer carrying %r — only a `generate` "
                      "answer gains a field, and an abstention gains none "
                      "because it returns no item for a property of the item to "
                      "be about" % (q, sorted(got)))
    require_equal(l7.query(state, {"op": "no_such_op"})["status"], "abstain",
                  "an unsupported query abstains, never raises (§7.3)")

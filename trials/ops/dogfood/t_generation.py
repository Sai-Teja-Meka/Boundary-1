"""ops/dogfood — the provenance surface (`shell/dogfood/consolidate.py`, `[L7]`).

`[L7] [DOGFOOD]`. The store's derived view now replays through
`core/layers/l7_generation.py`, and the upgrade is that the store **confesses its
origins**: every answer the shell renders carries its `§4.2` provenance tag, a
derived or generated answer's support is shown back to ingested ground, and the
`‰` beside it is classified by whether the engine **counted** anything to arrive
at it. `§7.1`'s three verbs are unchanged and no new one is added.

These trials hold the surface to six things:

  * the upgrade is **zero-cost on this fuel**: the lineage ledger is the one
    field `L7State` adds and this reading emits nothing it can record, so the
    derived state is the Layer-6 state to the cell and the two canonical bodies
    differ in exactly two branches (`README-l7 §0`);
  * **every rendered answer carries a tag** — one of `§4.2.3`'s closed four, or
    `UNTAGGED`, which is what `§4.2.2` prices at 0 and which the surface names
    rather than laundering into a kind;
  * a tag's **support** satisfies `§4.2.3`'s shape and is walked back to store
    `t`, with `R8` clause 5(a)'s recoverability rate reported **ungated**;
  * the **generation census** is a row at zero: no answer over this project's own
    history requires composition and none carries the `generated` tag, and that
    is a property of the READING (`DECLARED_KINDS` and `COMPOSITION_KINDS` are
    disjoint) rather than a defect of the layer;
  * the census is **not vacuous** — on fuel that does carry a compound, the same
    surface composes, tags the item `generated`, and the closing census counts it
    under `README-l6 §4`'s residual warrant;
  * the four **warrants** are a reading of the engine's own `confidence_for`,
    checked against it in both directions, and on the committed store **not one
    `‰` the surface prints is measured** — which is the residual `iid 2` was
    armed to surface.

The committed store is only ever read. Every trial that writes uses an in-memory
derived state.
"""

import os

from _harness import require, require_equal, skip

from core.serialize import decode, encode
from core.layers import l2_recall as ledger
from core.layers import l6_meta_memory as l6
from core.layers import l7_generation as l7
from shell.dogfood import consolidate as co
from shell.dogfood import event as ev
from shell.dogfood import store as st

# `§4.2.3`'s closed four, read out of the constitution's own vocabulary rather
# than typed as a preference of this trial.
ANSWER_KINDS = ("recall", "aggregate", "derive", "absent")


def _summary(move, line, questions=()):
    return {"project": "trial-project", "move": move,
            "decisions": ["a decision"], "files_touched": [],
            "open_questions": list(questions), "log_line": line}


STREAM = [
    _summary("FORGE", "[L1] [FORGE] retention <suite: 72/72 green> <anchors: born>"),
    _summary("ASCEND", "[L2] [ASCEND] recall <suite: 98/98 green> <anchors: l1 intact, l2 born>",
             questions=["where did this answer come from?"]),
    _summary("DOGFOOD", "[L2] [DOGFOOD] first-run <suite: 105/105 green>"),
]


def _records():
    return [{"payload": ev.build_payload(s), "t": i} for i, s in enumerate(STREAM)]


def _rendered():
    """`(lines, seen)` — the report, and the exact answers it rendered."""
    records = _records()
    state, origin, sessions, entities, refused = co.derive(records)
    require(refused is None, "the default cap must admit the whole stream")
    seen = []
    lines = co.report(state, origin, sessions, entities, records, seen=seen)
    return "\n".join(lines), seen, state, origin, entities


# ---- 1. the upgrade is zero-cost on this store's fuel ------------------------

def trial_the_derived_replay_is_layer_7_and_costs_this_reading_nothing():
    """`README-l7 §0`'s negative, on this project's own fuel.

    Layer 7 adds exactly one field — the lineage ledger, written by `ingest`
    because `query` is pure — and it records a `profile` payload the engine
    recognises as its own. This reading emits no `profile` at all, so the ledger
    must stay empty and the whole layer must cost **zero cells**: the derived
    state is the Layer-6 state, and the two canonical bodies differ in exactly
    two branches — the recorded `layer_cap`, which is the cap and not the
    content, and an empty `lineage`.

    A ledger that charged for a stream with no generation in it would compete for
    room with a pending set and a fired ledger `README-l5 §0.1` puts outside
    every eviction phase on purpose, which is what makes this an identity worth
    asserting rather than an observation worth recording.
    """
    records = _records()
    seven, _origin, _s, entities, refused = co.derive(records)
    require(refused is None, "the default cap must admit the whole stream")
    require_equal(seven.layer_cap, l7.LAYER, "the derived replay must be Layer 7")
    require_equal(seven.lineage, {},
                  "this reading emits no `profile`, so the ledger has nothing to "
                  "record — a non-empty ledger here would mean the engine "
                  "recognised one of its own compositions in session prose")

    six = l6.make_engine(l6.LAYER, budget_cap=co.DERIVED_BUDGET)
    for record in records:
        for derived in co.derived_stream(record["payload"], entities):
            six, t = l6.write(six, derived)
            require(t is not None, "the Layer-6 control replay must not refuse")

    require_equal(seven.occupancy, six.occupancy,
                  "the Layer-7 replay of this store must occupy exactly what the "
                  "Layer-6 replay occupied — README-l7 §0's `where there is "
                  "nothing to record it costs nothing`, and the 2 cells an entry "
                  "costs would be visible here")

    body7 = decode(l7.snapshot(seven))["body"]
    body6 = decode(l6.snapshot(six))["body"]
    require_equal(body7["lineage"], [], "the serialized ledger must be empty too")
    require_equal(body7["layer_cap"], 7, "the Layer-7 body records its own cap")
    require_equal(body6["layer_cap"], 6, "the Layer-6 body records its own cap")
    differing = sorted(k for k in set(body7) | set(body6)
                       if encode(body7.get(k)) != encode(body6.get(k)))
    require_equal(differing, ["layer_cap", "lineage"],
                  "a Layer-7 replay of this store must hold EXACTLY what the "
                  "Layer-6 replay held apart from the cap it records and an empty "
                  "ledger; these branches differ: %s" % differing)


# ---- 2. every rendered answer carries a tag ---------------------------------

def trial_every_rendered_answer_carries_a_provenance_tag_or_is_named_untagged():
    """`§4.2` is binding from Layer 7, so the surface stops treating a tag as decor.

    Two claims. Every answering row carries a `kind` drawn from `§4.2.3`'s closed
    four **and no other**, or the surface's own `UNTAGGED` — which is not one of
    the four and is deliberately not made to look like one, because `§4.2.2`
    prices an untagged non-abstaining answer at 0 *regardless of whether its value
    is correct*. And the untagged ones come from the layers' own **diagnostic**
    ops and from nowhere else, so what the report names is a bounded seam and not
    a blanket property of the engine — `forgetting` carries a valid `absent` tag
    beside them, which is why the finding is reported as a list of ops.
    """
    text, seen, _state, _origin, _entities = _rendered()
    require(seen, "the report must have rendered something")

    untagged_ops = set()
    for row in seen:
        if row["status"] != "answer":
            require_equal(row["tag"], "abstain",
                          "an abstention is rendered as one (§3.0 pays 1000 for "
                          "it and §4.2 requires no tag of it)")
            continue
        require(row["tag"] in ANSWER_KINDS or row["tag"] == co.UNTAGGED,
                "op %r rendered the tag %r, which is neither one of §4.2.3's "
                "closed four nor the surface's UNTAGGED"
                % (row["op"], row["tag"]))
        if row["tag"] == co.UNTAGGED:
            untagged_ops.add(row["op"])

    require(untagged_ops,
            "the diagnostic ops answer with `provenance: null`; if that has "
            "changed, this trial and README.md's closing paragraph are stale")
    for op in untagged_ops:
        require(op in ("consolidation", "prospection", "calibration", "lineage",
                       "profile", "count"),
                "%r answers untagged and is NOT one of the layers' own "
                "diagnostics — an ordinary verb losing its tag is a different "
                "finding and must not pass as this one" % (op,))
    require("UNTAGGED answers come from the diagnostic ops" in text,
            "the report must name the untagged answers rather than launder them")
    require("no gated number moves" in text,
            "and it must scope the finding: no §5 L7 denominator contains a "
            "diagnostic query")

    # `forgetting` is the counter-example that keeps the finding honest.
    state = co.derive(_records())[0]
    require_equal(co.tag_of(co.ask(state, {"op": "forgetting"})), "absent",
                  "`forgetting` carries a valid §4.2 tag, so the untagged set is "
                  "an uneven seam and not `the diagnostics are untagged`")


# ---- 3. support: the shape, the walk, and the ungated rate ------------------

def trial_a_rendered_tag_cites_ingested_t_and_the_recoverability_rate_is_ungated():
    """`§4.2.3`'s shape, and `R8` clause 5(a)'s diagnostic beside it.

    The schema half is the law's own: `support` is strictly ascending, every
    entry non-negative and an **actually-ingested** `t`, and empty only for an
    `absent` tag. The other half is the one `R8` clause 5(a) had to pay for in a
    diagnostic because the schema could not carry it — whether the cited `t` can
    still be **shown** — and it is reported ungated here for the same reason: an
    answer citing a `t` the budget took breaches no `§5 L7` clause.

    The structural claim underneath the rate is the one worth pinning, and it is
    `README-l7 §2.3`'s one reading over: `current` cites the assertion that
    ANSWERS it, so where a chain is shed the answer abstains and there is no
    citation left to be unrecoverable. Asserted at four caps, including caps that
    genuinely forget.
    """
    records = _records()
    for cap in (co.DERIVED_BUDGET, 4000, 1200, 400):
        state, origin, _s, entities, _r = co.derive(records, budget_cap=cap)
        entity = entities["trial-project"]
        for key in co.ASSERTED_KEYS:
            answer = co.ask(state, {"op": "current", "entity": entity, "key": key})
            if answer["status"] != "answer":
                continue
            support = co.support_of(answer)
            require_equal(list(support), sorted(set(support)),
                          "support is strictly ascending with no duplicates "
                          "(§4.2.3) — key %r at cap %d" % (key, cap))
            for t in support:
                require(isinstance(t, int) and not isinstance(t, bool) and t >= 0,
                        "a support entry is a non-negative integer t (§4.2.3)")
                require(t < state.next_t,
                        "a support entry must be an ACTUALLY-INGESTED t: %d is "
                        "not below next_t %d" % (t, state.next_t))
            require(support or co.tag_of(answer) == "absent",
                    "support may be empty ONLY when kind == 'absent' (§4.2.3)")
            shown, cited = co.recoverable(state, support)
            require_equal(shown, cited,
                          "key %r answers at cap %d while citing a t the engine "
                          "cannot produce — the reading is supposed to lose the "
                          "ANSWER before the WARRANT (README-l7 §2.3)"
                          % (key, cap))
            # And the walk the report prints is the same support, in store t.
            now = co.current_fact(state, entity, key, origin)
            require_equal(tuple(now[4]),
                          tuple(co._store_t(origin, t) for t in support),
                          "the report's cited store t must be the answer's own "
                          "support translated, not a chain the shell rebuilt")

    text, _seen, _state, _origin, _entities = _rendered()
    require("support recoverable" in text,
            "the report must state the ungated recoverability rate")
    require("R8 clause 5(a) demands INGESTED, not RECOVERABLE" in text,
            "and must say which of the two is the law and which is the diagnostic")


# ---- 4. the generation census, as a row at zero -----------------------------

def trial_the_generation_census_is_a_row_at_zero_and_the_reading_cannot_compose():
    """The mandatory `[L7] [DOGFOOD]` measurement, stated as a property of the reading.

    `COMPOSITION_FORM` determines a `profile` item from two `part` assertions.
    This shell emits `session_summary`, `attr` and `intend` and nothing else, so
    the two vocabularies are **disjoint** — the reading cannot compose, no answer
    requires composition, and no answer can carry the `generated` tag.

    The disjointness is asserted as the CAUSE, so a later session that widened
    the reading would go red here rather than quietly changing what the census
    means; and the emptiness is required to be a printed **row** rather than a
    silence, which is the shape the `[L6]` census fixed for `origin` one layer
    down.
    """
    require_equal(sorted(set(co.DECLARED_KINDS) & set(co.COMPOSITION_KINDS)), [],
                  "this reading emits %s and composition needs %s; if they now "
                  "overlap, the census below measures something else"
                  % (", ".join(co.DECLARED_KINDS),
                     ", ".join(co.COMPOSITION_KINDS)))

    text, _seen, state, _origin, entities = _rendered()
    ledger_answer, rows, probes = co.generation(state, entities)
    require_equal(ledger_answer["value"]["generated"], 0,
                  "the lineage ledger must be empty on fuel with no compound")
    require_equal(ledger_answer["value"]["cells"], 0, "and must cost no cell")
    require_equal([kind for kind, _c, _s in rows], list(co.COMPOSITION_KINDS),
                  "one row per kind the composition rule needs")
    for kind, count, _status in rows:
        require_equal(count, 0, "%r is derived %d times by a reading that does "
                                "not emit it" % (kind, count))
    require(probes, "the census must probe generate() for every project entity")
    for name, _entity, answer in probes:
        require_equal(answer["status"], "abstain",
                      "generate(%s) answered: the rule determines nothing here, "
                      "and composing anything at all would be the fabrication "
                      "§3.0 prices at 0" % (name,))

    for kind in co.COMPOSITION_KINDS:
        require("  %s " % kind in text,
                "the census must print a ROW for %r even at zero — an emptiness "
                "that is not a row is a silence" % (kind,))
    require("THE READING CANNOT COMPOSE" in text,
            "and must say so as a property of the reading")
    require("not of the layer" in text,
            "and must not let that read as a defect of Layer 7")


def trial_the_same_surface_composes_when_the_fuel_carries_a_compound():
    """The teeth: the census is measuring something, and this is what it looks like.

    A census that could only ever report zero would be indistinguishable from a
    census that was not wired up — the defect `autopsy/GAPMAP.md §2` convicts four
    engines of, one surface out. So the same renderer is handed fuel that DOES
    carry a compound, and it must compose, tag the item `generated` (`R8` clause
    4's lineage, beside `§4.2.3`'s `derive` channel and never instead of it), cite
    exactly the `t`s the rule read, and classify the number as
    `default:no-chain` — `README-l6 §4`'s residual, which `README-l7 §4` leaves
    OPEN and which this fixture is the only place in this shell that can exhibit.
    """
    state = l7.make_engine(l7.LAYER, budget_cap=1 << 20)
    stream = [{"kind": "attr", "entity": 10, "key": "hue", "val": "amber"},
              {"kind": "attr", "entity": 10, "key": "mass", "val": 3},
              {"kind": "attr", "entity": 11, "key": "hue", "val": "cobalt"},
              {"kind": "attr", "entity": 11, "key": "mass", "val": 4},
              {"kind": "part", "entity": 12, "slot": 0, "of": 10},
              {"kind": "part", "entity": 12, "slot": 1, "of": 11}]
    for payload in stream:
        state, t = l7.write(state, payload)
        require(t is not None, "the fixture must fit its cap")

    seen = []
    answer = co.ask(state, {"op": "generate",
                            "cue": {"kind": l7.PROFILE_KIND, "entity": 12}}, seen)
    require_equal(answer["status"], "answer",
                  "the rule determines an item for a compound whose components "
                  "are both asserted")
    require_equal(answer["lineage"], co.GENERATED,
                  "an item the store never held is `generated` (R8 clause 4)")
    require_equal(co.tag_text(answer), "derive+generated",
                  "the surface renders the CHANNEL and the LINEAGE side by side; "
                  "collapsing them would lose the claim R8 clause 4 keeps "
                  "orthogonal")
    require(l7.profile_form_ok(answer["value"]),
            "a composed item must be grammar-valid (§5 L7's validity clause)")
    require_equal(list(co.support_of(answer)), sorted(set(co.support_of(answer))),
                  "a generated answer's support is ascending (§4.2.3)")
    require_equal(set(co.support_of(answer)), {0, 1, 2, 3, 4, 5},
                  "and cites exactly the t's the rule read — R8 clause 5(b) binds "
                  "RELEVANCE on the artifact because the schema cannot")
    require_equal(seen[0]["warrant"], co.NO_CHAIN,
                  "a composed item has no chain, no claimant count and no "
                  "set-once status, so its ‰ is README-l6 §4's fall-through")
    require_equal(answer["confidence"], co.CERTAIN,
                  "and the fall-through states CERTAIN, which is exactly the "
                  "residual README-l7 §4 leaves OPEN")

    census = "\n".join(co.certainty_lines(seen))
    require(co.NO_CHAIN in census, "the census must carry the residual's own row")
    residual = [line for line in census.splitlines() if co.NO_CHAIN in line]
    require(any(" 1 " in line.replace("  ", " ") for line in residual),
            "and must count this composition in it: %r" % residual)
    require("NOT ONE ‰ ABOVE IS MEASURED" in census,
            "nothing here was measured either — a composed item is a "
            "fall-through and not a measurement")


# ---- 5. the warrant is a reading of the engine's own confidence function ----

def trial_the_warrant_of_a_number_is_read_off_the_engines_confidence_function():
    """`measured` means the engine COUNTED; the rest mean it did not look.

    Checked in both directions against `l6.confidence_for` rather than asserted:

      * on a **set-once** key the number is a function of the chain — a second
        claimant moves it to 500 — so `MEASURED` is the honest label;
      * on any other key the number cannot move whatever the chain does, because
        `confidence_for` returns `CERTAIN` on its first line, so the label is a
        fall-through and the surface says which one.

    The second leg is the one with teeth: it builds a chain with FIFTEEN distinct
    claimants on an ordinary key and requires the number not to budge.
    """
    state = l7.make_engine(l7.LAYER, budget_cap=1 << 20)
    stream = [{"kind": "attr", "entity": 1, "key": "origin", "val": "first"},
              {"kind": "attr", "entity": 1, "key": "origin", "val": "second"}]
    for i in range(15):
        stream.append({"kind": "attr", "entity": 1, "key": "layer", "val": i})
    for payload in stream:
        state, t = l7.write(state, payload)
        require(t is not None, "the fixture must fit its cap")

    tied = co.ask(state, {"op": "current", "entity": 1, "key": "origin"})
    ordinary = co.ask(state, {"op": "current", "entity": 1, "key": "layer"})
    require_equal(co.warrant_of("current", "origin"), co.MEASURED,
                  "a set-once key's ‰ is counted from its chain")
    require_equal(co.warrant_of("current", "layer"), co.NOT_SET_ONCE,
                  "an ordinary key's ‰ is CERTAIN before the chain is looked at")
    require_equal(tied["confidence"], 500,
                  "two claimants for a slot that admits one is permille(1/2) — "
                  "the number MOVED, which is what `measured` means")
    require_equal(ordinary["confidence"], co.CERTAIN,
                  "fifteen distinct values on an ordinary key and the number did "
                  "not move by a permille — which is what `default` means")
    require_equal(co.warrant_of("read"), co.NO_MODEL,
                  "an op with no confidence model is labelled as such")
    require_equal(co.warrant_of("generate", None, co.GENERATED), co.NO_CHAIN,
                  "a composed item is README-l6 §4's residual and is labelled as "
                  "that and not as `no-model`")
    require_equal(co.warrant_of("current", "origin", co.GENERATED), co.NO_CHAIN,
                  "lineage decides first: a composed item never reaches "
                  "confidence_for at all")


# ---- 6. the committed store (read-only) -------------------------------------

def trial_the_committed_stores_certainty_census_is_measured():
    """This project's own history, and what its every `‰` is actually worth.

    The mandatory `[L7] [DOGFOOD]` measurement, asserted rather than only written
    down, and it is a **negative twice over**: no answer over this store requires
    composition (so the `generated` case `iid 2`'s payload named is unreachable
    here), and not one number the surface prints was measured — because no key of
    this reading is set-once, so `confidence_for` returns `CERTAIN` on its first
    line every single time.

    `FIELD.md` (2026-08-03) carries the same numbers. If either becomes false —
    the reading gains a set-once key, or it learns to compose — this trial is
    where the file says so.
    """
    path = st.default_store_path()
    if not os.path.isfile(path):
        skip("no committed dogfood store yet (%s)" % st.display_path(path))
    state = st.load(path)
    records = ledger.read_range(state, 0, state.next_t - 1)
    derived, origin, sessions, entities, refused = co.derive(records)
    require(refused is None, "the committed store must fold inside the derived cap")
    require_equal(derived.lineage, {},
                  "the ledger must be empty: this store's fuel is session prose "
                  "and the engine composed none of it")

    seen = []
    text = "\n".join(co.report(derived, origin, sessions, entities, records,
                               seen=seen))
    answered = [row for row in seen if row["status"] == "answer"]
    require(len(answered) > 100, "the report must have rendered a real view")

    measured = [row for row in answered if row["warrant"] == co.MEASURED]
    composed = [row for row in answered if row["warrant"] == co.NO_CHAIN]
    require_equal(len(measured), 0,
                  "%d answers were MEASURED: some key of this reading is now "
                  "set-once, so FIELD.md's 2026-08-03 census is stale and the "
                  "report's `NOT ONE ‰ IS MEASURED` line is false"
                  % len(measured))
    require_equal(len(composed), 0,
                  "%d answers were composed: this reading has learned to compose "
                  "and the generation census now measures something else"
                  % len(composed))
    require("NOT ONE ‰ ABOVE IS MEASURED" in text,
            "and the surface must say so, because a report that printed only the "
            "number could not tell a counted 1000 from a defaulted one")
    require("THE READING CANNOT COMPOSE" in text,
            "and must state the generation census's finding as a property of the "
            "reading")

    # The take-back rule, in BOTH directions and asserted at once so neither can
    # be traded for the other (`strain/l5`'s shape, on real fuel): a FIRED
    # intention's own `intend` episode is regenerated by nothing once the pending
    # entry is gone, so where there is room it must come back into the store and
    # `recall` is the only honest tag it can carry; a PENDING one's is
    # regenerated by the pending entry and comes back `derive`.
    entries = co.promises(derived, records, origin)
    require(entries, "the committed store has declared intentions")
    fired = [p for p in entries if p["fired"]]
    require(len(fired) >= 2,
            "this store's prospective cycle has closed TWICE (iid 1 at [L6] "
            "[ASCEND], iid 2 at [L7] [ASCEND]); the ledger reports %d firings"
            % len(fired))
    for promise in entries:
        require(promise["readable"] and promise["regenerated"],
                "iid %s's own `intend` event must come back byte-exact"
                % (promise["iid"],))
        want = "recall" if promise["fired"] else "derive"
        require_equal(promise["provenance"], want,
                      "iid %s is %s and its own event is tagged %r — a fired "
                      "promise's episode is regenerated by nothing and must be "
                      "`recall`, a pending one's is regenerated by the pending "
                      "entry and must be `derive` (README-l5 §1.3)"
                      % (promise["iid"],
                         "FIRED" if promise["fired"] else "PENDING",
                         promise["provenance"]))

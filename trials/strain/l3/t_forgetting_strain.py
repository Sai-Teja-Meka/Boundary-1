"""strain/l3 — Layer 3 (Forgetting) under attack, dirt, and permutation.

The frozen ascension trial proves the engine clears the gate. This file attacks
the property that makes the gate *mean* something: that survival is bought by
structural importance and by nothing else. Three strains, the three the standing
brief specified.

## (a) Importance inflation, with the survival of the attacked set quantified

An adversary who can write can try to buy importance. The cheapest attack is
**repetition**: flood the store with copies of one item so its reference count —
and with it its activation — climbs past the items the engine is supposed to keep.

`README-l3 §1`'s rule is the whole defence: a cluster's `uses` are the **first
occurrences of its distinct payloads**, so a byte-identical repetition is *not* a
use and adds neither frequency nor recency. Here that is measured, both ways:

  * with the rule, the flood costs the attacked set **nothing** — every defended
    item survives, and the flood holds a single slot however many copies it sends;
  * the **naive** reference count (every same-handle event counted, computed here
    as a trial fixture and never as engine code) is shown to reach an activation
    that would evict the defended set outright.

The second half is what makes the first half a finding rather than a claim: the
guard is load-bearing, and the arithmetic says by how much.

## (b) Near-duplicate pressure from murk

`corpora/murk/` injects near-duplicates paired with an answer key (§8.7), and its
near-duplicate defects are **byte-identical repetitions at different `t`** — the
exact shape (a) reasons about, arriving in dirty real corpus traffic alongside
contradictions, ambiguities and malformed payloads. The frozen contract has two
halves and both are asserted:

  * **neither each pays full survival cost** — twins share one cluster, so they
    carry *equal* importance and rise and fall together; the repetition is
    excluded from the cluster's uses, so the cluster's reference count counts
    facts, not restatements;
  * **nor collide into wrongful eviction** — no cue is ever answered with the
    wrong event. Two retained twins make a cue *ambiguous* and the engine
    abstains (§7.3); a **contradiction** pair, same handle and same key but
    different value, is separated **exactly** by the field that differs — where
    Layer 2's MinHash could only abstain, exact containment resolves.

## (c) Eviction determinism, and the order-dependence that lawfully exists

Determinism is a law (§2.3): the same stream twice must give byte-identical
snapshots, evictions included. Beyond that, this strain draws the line between
permutations that are **declared safe** and permutations that lawfully change the
outcome:

  * **safe** — swapping two *adjacent* arrivals of equal grammar weight and
    distinct handles. Their `(weight, t)` multiset is unchanged, so every later
    eviction decision sees the same importance order and the **retained payload
    multiset is invariant**, as is the forgetting record's count and mass.
  * **lawfully order-dependent** — moving an item to a different position changes
    its recency, and recency is a *factor of importance*, so what survives may
    change. That is the ACT-R law working, not a determinism defect, and it is
    asserted here so the safety class above cannot be mistaken for a claim that
    order never matters.
"""

from fractions import Fraction

from _harness import require, require_equal, try_import
import _l3fixture
import _l3tasks
from corpora.l3streamb import generator as streamb
from corpora.murk import generator as murk_gen


def _engine():
    return try_import("adapters.l3",
                      "no L3 engine yet; the Layer-3 strains engage when built")


def _cap_for(l3, items, payload):
    """A budget cap that holds exactly `items` of `payload`'s shape, plus the record."""
    return items * l3.item_cost(payload) + 3 + 2 * l3.FORGET_BUCKETS


def _replay(l3, payloads, cap, layer_cap=3):
    state = l3.make_engine(layer_cap, cap)
    for payload in payloads:
        state, _t = l3.ingest(state, payload)
        require(state.occupancy <= cap,
                "occupancy %d passed the cap %d mid-stream (§4.1)"
                % (state.occupancy, cap))
    return state


def _retained_tags(l3, state):
    return set(record["payload"]["tag"] for record in state.events)


# ---- (a) importance inflation ------------------------------------------------

DEFENDED = 30          # heavy items, placed EARLY: the worst case for recency
FILLER = 300           # ordinary light traffic
FLOOD = 400            # manufactured copies, all byte-identical


def _inflation_stream(flood):
    """Defended heavy items first, then light filler, then a flood of copies."""
    out = []
    for i in range(DEFENDED):
        out.append({"kind": "item", "tag": "df%05d" % i, "key": "alpha",
                    "val": i, "importance": streamb.HEAVY_MIN})
    for i in range(FILLER):
        out.append({"kind": "item", "tag": "fl%05d" % i, "key": "beta",
                    "val": i, "importance": 1})
    copy = {"kind": "item", "tag": "atk00000", "key": "gamma", "val": 7,
            "importance": 1}
    for _ in range(flood):
        out.append(dict(copy))
    return out, copy


def trial_manufactured_duplicates_cannot_mint_importance_mass():
    l3 = _engine()
    payloads, copy = _inflation_stream(FLOOD)
    cap = _cap_for(l3, 60, payloads[0])
    state = _replay(l3, payloads, cap)

    tags = _retained_tags(l3, state)
    defended = set("df%05d" % i for i in range(DEFENDED))
    survivors = defended & tags
    require_equal(len(survivors), DEFENDED,
                  "the flood evicted %d of %d defended items — repetition bought "
                  "importance" % (DEFENDED - len(survivors), DEFENDED))

    # No mass was minted. Copies of one payload are one cluster with ONE use, so
    # however many copies are retained, the cluster's activation is exactly that of
    # a single item first seen at `t_first` — flooding does not multiply it.
    atom = l3.handle_atom(copy)
    now = state.next_t
    postings = state.index.get(atom, ())
    uses = l3.cluster_uses(state, atom, now)
    require_equal(len(uses), 1,
                  "the manufactured cluster counts %d uses from %d identical "
                  "copies — distinct-payload counting has broken"
                  % (len(uses), FLOOD))
    single = Fraction(l3.grammar_weight(copy), 1) * Fraction(1, now + 1 - uses[0])
    for t in postings:
        require_equal(l3.importance(state, t, now), single,
                      "a flooded copy at t=%d carries more than one item's worth "
                      "of activation — repetition minted mass" % (t,))

    # The residual, stated rather than hidden: the copies still *occupy slots*
    # while their cluster is recent, because Layer 3 stores what it is given and
    # reconciling redundancy is Layer 4's claim, not this layer's. What is bounded
    # is how many: the flood holds only the tail of the store's recency window, a
    # small fraction of what it sent, and never any of the defended set.
    require(len(postings) * 4 < FLOOD,
            "%d of %d manufactured copies are retained — the flood is winning "
            "more than a quarter of what it sent" % (len(postings), FLOOD))
    require(len(postings) < DEFENDED + FILLER,
            "the flood holds more slots than the legitimate stream had items")


def trial_flood_survival_does_not_grow_with_the_flood():
    """Doubling the attack must not double what it wins. Measured, not argued."""
    l3 = _engine()
    won = []
    for flood in (50, 200, 800):
        payloads, copy = _inflation_stream(flood)
        cap = _cap_for(l3, 60, payloads[0])
        state = _replay(l3, payloads, cap)
        won.append(len(state.index.get(l3.handle_atom(copy), ())))
        require_equal(len(_retained_tags(l3, state)
                          & set("df%05d" % i for i in range(DEFENDED))),
                      DEFENDED,
                      "a flood of %d evicted a defended item" % (flood,))
    require(len(set(won)) == 1,
            "the flood's retained footprint grew with its size (%s) — the attack "
            "scales, which is exactly what reference counting must prevent"
            % (won,))


def trial_the_naive_reference_count_would_have_lost_the_attacked_set():
    """The counterfactual, as a trial fixture — never as engine code.

    Counting *every* same-handle event as a use (the obvious implementation) makes
    the flooded cluster's activation grow linearly in the flood size. Priced
    against a defended heavy item's activation at the same instant, it overtakes
    it — so the attacked set would be evicted. This is the number that makes the
    distinct-payload rule load-bearing.
    """
    l3 = _engine()
    payloads, copy = _inflation_stream(FLOOD)
    cap = _cap_for(l3, 60, payloads[0])
    state = _replay(l3, payloads, cap)
    now = state.next_t

    # The weakest defended item actually retained, under the engine's real law.
    defended_ts = [record["t"] for record in state.events
                   if record["payload"]["tag"].startswith("df")]
    require(defended_ts, "no defended item survived, so there is nothing to price")
    weakest = min(l3.importance(state, t, now) for t in defended_ts)

    # The same cluster under the naive count: one use per copy, at the copy's own
    # arrival time. Computed here, from the stream, with no engine involved.
    flood_ts = [t for t, payload in enumerate(payloads) if payload == copy]
    naive = Fraction(l3.grammar_weight(copy), 1) * sum(
        Fraction(1, now + 1 - t) for t in flood_ts)
    honest = l3.importance(state, min(l3.cluster_uses(
        state, l3.handle_atom(copy), now)), now) if state.index.get(
        l3.handle_atom(copy)) else Fraction(0, 1)

    require(naive > weakest,
            "the naive reference count reaches %s against the weakest defended "
            "item's %s — it no longer overtakes the attacked set, so this "
            "counterfactual has stopped being evidence" % (naive, weakest))
    require(honest < weakest,
            "under the engine's own law the flooded cluster reaches %s, at or "
            "above the weakest defended item's %s — the guard is not holding"
            % (honest, weakest))
    # And the gap is not marginal: the naive count wins by more than an order of
    # magnitude, so the attack would not merely tie, it would sweep.
    require(naive > 10 * weakest,
            "the naive count only reaches %s against %s — recorded as a sweep, "
            "not a tie" % (naive, weakest))


# ---- (b) murk near-duplicate pressure ---------------------------------------

MURK_N = 1500
MURK_ITEMS = 90        # a punishing cap: ~1 400 evictions over dirty traffic


def _murk_bundle():
    payloads, ground_truth = murk_gen.generate_full(murk_gen.SEED, MURK_N)
    defects = {}
    for defect in ground_truth["defects"]:
        defects.setdefault(defect["type"], []).append(defect)
    return payloads, defects


def trial_murk_near_duplicates_share_survival_rather_than_each_paying_for_it():
    """Checked at the contested instant: the moment a twin arrives on a live original.

    Asserting only over the *final* state would be weak — it would pass vacuously
    on a seed where no pair happened to last. So the stream is walked, and at every
    `t` that a near-duplicate's second member arrives under pressure, one of exactly
    two lawful outcomes must hold, and the fact must survive either way:

      * **both retained** — one cluster, so they carry **equal** importance and the
        repetition is excluded from its uses: neither twin pays full survival cost;
      * **the arrival declined** — a repetition buys nothing at the door, so if its
        cluster's standing is too low it is dropped *instead of displacing its own
        original*, which must still be retained.

    What is forbidden is the third outcome: the repetition evicting the fact it
    repeats. On murk both admitted outcomes occur and the declined one need not —
    a murk twin's handle cluster is a whole entity's worth of *distinct* facts, so
    its standing carries the twin in; the repetition is excluded from the cluster's
    uses all the same, which is the property under test.
    """
    l3 = _engine()
    payloads, defects = _murk_bundle()
    cap = _cap_for(l3, MURK_ITEMS, payloads[1])
    seconds = {}
    for defect in defects["near_duplicate"]:
        first, second = defect["refs"]
        seconds[second] = first
    require(len(seconds) > 20, "murk produced too few near-duplicate pairs to strain")

    state = l3.make_engine(3, cap)
    both_retained = 0
    declined = 0
    for t, payload in enumerate(payloads):
        state, _t = l3.ingest(state, payload)
        require(state.occupancy <= cap,
                "occupancy %d passed the cap %d mid-stream" % (state.occupancy, cap))
        if t not in seconds:
            continue
        first = seconds[t]
        original = l3.read(state, first)
        twin = l3.read(state, t)
        atom = l3.handle_atom(payload)
        now = state.next_t
        if twin is not None and original is not None:
            both_retained += 1
            require_equal(l3.importance(state, first, now),
                          l3.importance(state, t, now),
                          "retained twins %d/%d carry different importance — one "
                          "is paying full survival cost alone" % (first, t))
            uses = l3.cluster_uses(state, atom, now)
            postings = state.index.get(atom, ())
            require(len(uses) < len(postings),
                    "cluster %r counts %d uses over %d retained members while "
                    "holding a byte-identical twin — a repetition was counted as "
                    "a use" % (atom, len(uses), len(postings)))
        elif twin is None:
            declined += 1
            require(original is not None,
                    "the repetition at t=%d was declined AND its original at "
                    "t=%d is gone — the fact was lost to its own restatement"
                    % (t, first))
        else:
            require(False,
                    "the repetition at t=%d evicted its own original at t=%d — a "
                    "restatement displaced the fact it restates" % (t, first))
    require(both_retained + declined == len(seconds),
            "only %d of %d near-duplicate arrivals reached a lawful outcome"
            % (both_retained + declined, len(seconds)))
    require(both_retained > 0,
            "no twin was ever admitted alongside its original, so the shared-"
            "importance half of the contract was never exercised")
    # The pressure was real: the cap bound, and most of the stream is gone.
    require(state.forgetting.count > len(payloads) // 2,
            "only %d of %d murk events were forgotten — the cap was not binding, "
            "so nothing above was tested under pressure"
            % (state.forgetting.count, len(payloads)))


def trial_murk_dirt_never_collides_into_a_wrong_answer():
    l3 = _engine()
    payloads, defects = _murk_bundle()
    cap = _cap_for(l3, MURK_ITEMS, payloads[1])
    state = _replay(l3, payloads, cap)

    # No retained event is ever answered as a different event. A twin makes the
    # cue ambiguous and the engine abstains; nothing is ever returned wrongly.
    wrong = 0
    abstained = 0
    exact = 0
    for record in state.events:
        answer = l3.query(state, {"op": "recall", "cue": record["payload"]})
        if answer["status"] == "abstain":
            abstained += 1
            continue
        if answer["value"] == record:
            exact += 1
        else:
            wrong += 1
    require_equal(wrong, 0,
                  "recall returned the wrong event for a retained cue under murk "
                  "pressure — near-duplicates collided into corruption")
    require(exact > 0, "nothing at all was recalled exactly from the murk store")

    # A contradiction pair — same handle, same key, different value — is separated
    # exactly by the field that differs. Layer 2 could only abstain here.
    resolved = 0
    for defect in defects["contradiction"]:
        first, second = defect["refs"]
        for t in (first, second):
            record = l3.read(state, t)
            if record is None:
                continue
            answer = l3.query(state, {"op": "recall", "cue": record["payload"]})
            if answer["status"] == "answer":
                require_equal(answer["value"], record,
                              "a contradiction pair resolved to the wrong member "
                              "(t=%d)" % (t,))
                resolved += 1
    require(resolved > 0,
            "no contradiction pair member survived to be resolved — the exact-"
            "containment claim was never exercised")


def trial_evicted_and_never_ingested_both_abstain_and_the_record_tells_them_apart():
    """Honest forgetting: a dropped cue abstains, and the aggregate says it was dropped.

    This is the seam Layer 6 will read. `recall` cannot distinguish *evicted* from
    *never ingested* — both are absences, and inventing a difference at the answer
    level would be fabrication. The aggregated record can, at `t`-range
    resolution, and that is exactly the resolution §0.3 could afford.
    """
    l3 = _engine()
    bundle = _l3tasks.stream("l3streamb")
    state, _budget = _l3fixture.replayed(l3, "l3streamb", 3)

    evicted = None
    for target in bundle["targets"]:
        if l3.read(state, target["t"]) is None:
            evicted = target
            break
    require(evicted is not None, "nothing was evicted from the pressure stream")

    dropped = l3.query(state, {"op": "recall", "cue": evicted["cue"]})
    require_equal(dropped["status"], "abstain",
                  "an evicted item was answered — forgetting must not fabricate")
    absent = l3.query(state, {"op": "recall", "cue": bundle["absent_cues"][0]})
    require_equal(absent["status"], "abstain", "a never-ingested cue was answered")

    here = l3.query(state, {"op": "forgot_at", "t": evicted["t"]})
    require_equal(here["status"], "answer",
                  "the forgetting record cannot be read for an evicted item's range")
    require(here["value"]["count"] > 0,
            "the range holding an evicted item reports nothing forgotten — the "
            "record cannot answer Layer 6's question")
    require(here["value"]["mass"] > 0, "the evicted range reports zero mass")
    beyond = l3.query(state, {"op": "forgot_at", "t": 10 * bundle["budget_items"] * 1000})
    require_equal(beyond["value"]["count"], 0,
                  "a range the stream never reached reports evictions")


def trial_no_heavy_tier_item_is_ever_evicted_at_ten_times_pressure():
    """The whole heavy tier survives the frozen stream — and its margin is stated.

    `weighted-C = 917‰` could in principle be reached while surrendering a few
    heavy items and compensating elsewhere. It is not: **all 800** survive, and the
    114 light items that fill the remaining slots are the most recent ones.

    The margin is stated because importance is a **rate**, not a hoard: a heavy
    item's activation decays as `1/age`, so it is not immortal — a long enough
    stream of recent light traffic must eventually outrank it. The crossover age is
    computed here from the state the engine actually reached, and asserted to lie
    well beyond this stream. That is the honest form of the claim: not "heavy items
    are safe" but "heavy items are safe *for this much pressure*, and here is where
    that stops".
    """
    l3 = _engine()
    state, _budget = _l3fixture.replayed(l3, "l3streamb", 3)
    now = state.next_t

    heavy = [r for r in state.events if r["payload"]["importance"] >= streamb.HEAVY_MIN]
    light = [r for r in state.events if r["payload"]["importance"] < streamb.HEAVY_MIN]
    require_equal(len(heavy), streamb.HEAVY_COUNT,
                  "%d of %d heavy-tier items were evicted at 10× pressure"
                  % (streamb.HEAVY_COUNT - len(heavy), streamb.HEAVY_COUNT))
    require(light, "no light item was retained, so the budget was not filled")

    # The crossover: the weakest retained light item is what a heavy item must
    # outrank, and a heavy item outranks it until its age reaches this bound.
    weakest_light = min(l3.importance(state, r["t"], now) for r in light)
    oldest_heavy_age = max(now + 1 - r["t"] for r in heavy)
    crossover = Fraction(streamb.HEAVY_MIN, 1) / weakest_light
    require(crossover > 10 * streamb.BUDGET_ITEMS,
            "the heavy tier's crossover age is %d, at or inside this stream's own "
            "length — some heavy item is already at risk, which is not what "
            "README-l3 §2 records" % (int(crossover),))
    require(oldest_heavy_age < crossover,
            "the oldest retained heavy item is at age %d, past the crossover %d — "
            "it should already have been evicted"
            % (oldest_heavy_age, int(crossover)))


# ---- (c) determinism, and the lawful order-dependence ------------------------

PERMUTE_N = 1200
PERMUTE_ITEMS = 80


def _permute_payloads():
    return list(streamb.generate(streamb.SEED, PERMUTE_N))


def trial_eviction_is_byte_identical_across_identical_replays():
    l3 = _engine()
    payloads = _permute_payloads()
    cap = _cap_for(l3, PERMUTE_ITEMS, payloads[0])
    first = _replay(l3, payloads, cap)
    second = _replay(l3, payloads, cap)
    require_equal(l3.snapshot(first), l3.snapshot(second),
                  "two identical streams produced different snapshots — eviction "
                  "is not deterministic (§2.3)")
    restored = l3.restore(l3.snapshot(first))
    require_equal(l3.snapshot(restored), l3.snapshot(first),
                  "restore(snapshot(s)) does not re-snapshot to the same bytes")
    require_equal(l3.state_checksum(restored), l3.state_checksum(first),
                  "a restored post-eviction state has a different checksum")


def _safe_swap(payloads):
    """The first adjacent pair of equal grammar weight and distinct handle."""
    for i in range(len(payloads) - 1):
        a, b = payloads[i], payloads[i + 1]
        if a["importance"] == b["importance"] and a["tag"] != b["tag"]:
            return i
    return -1


def trial_declared_safe_permutation_leaves_the_retained_set_invariant():
    l3 = _engine()
    payloads = _permute_payloads()
    cap = _cap_for(l3, PERMUTE_ITEMS, payloads[0])
    i = _safe_swap(payloads)
    require(i >= 0, "no declared-safe adjacent swap exists in the stream")

    swapped = list(payloads)
    swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]

    base = _replay(l3, payloads, cap)
    other = _replay(l3, swapped, cap)

    require_equal(_retained_tags(l3, other), _retained_tags(l3, base),
                  "a declared-safe swap (equal weight, distinct handles, adjacent) "
                  "changed which items survived — the safety class is wrong")
    require_equal(other.forgetting.count, base.forgetting.count,
                  "a declared-safe swap changed how many items were forgotten")
    require_equal(other.forgetting.mass, base.forgetting.mass,
                  "a declared-safe swap changed how much mass was forgotten")
    require_equal(l3.retained(other), l3.retained(base),
                  "a declared-safe swap changed the retained count")


def trial_two_streams_differing_only_in_what_was_forgotten_are_indistinguishable():
    """The Layer-4 seam, as a witness rather than a promise (README-l3 §4).

    Layer 4's humility ceiling will claim that a forget-only engine squeezed to a
    quarter of its bytes cannot *reconstruct* what it dropped. That claim needs a
    structural argument, and this is the sharp form of it: two streams that differ
    in the **content of an evicted item** — and in nothing else the importance law
    reads — produce **byte-identical** snapshots.

    So the dropped payload leaves no trace in state at all: not a hash, not a
    length, not a field. Reconstruction from Layer-3 state is therefore not merely
    hard, it is **impossible in principle** — there is no injective map from what
    was forgotten into 16 pairs of integers. `humility/l4/IMPOSSIBILITY.md` can be
    written against exactly this, and this trial is the witness it will cite.
    """
    l3 = _engine()
    payloads = _permute_payloads()
    cap = _cap_for(l3, PERMUTE_ITEMS, payloads[0])
    base = _replay(l3, payloads, cap)

    # An early item the base replay dropped; its grammar weight, its handle and
    # its arrival time are all held fixed, and only its *content* is changed.
    victim = None
    for i, payload in enumerate(payloads):
        if payload["tag"] not in _retained_tags(l3, base):
            victim = i
            break
    require(victim is not None, "the whole stream survived — raise the pressure")

    altered = [dict(p) for p in payloads]
    altered[victim] = dict(payloads[victim])
    altered[victim]["val"] = payloads[victim]["val"] + 1
    altered[victim]["key"] = streamb.KEYS[
        (streamb.KEYS.index(payloads[victim]["key"]) + 1) % len(streamb.KEYS)]
    require(altered[victim] != payloads[victim], "the two streams are not different")

    other = _replay(l3, altered, cap)
    require_equal(l3.snapshot(other), l3.snapshot(base),
                  "changing the content of a forgotten item changed the snapshot — "
                  "some trace of the evicted payload survives in state, and the "
                  "Layer-4 impossibility argument this witness supports is weaker "
                  "than stated")
    require_equal(other.forgetting.count, base.forgetting.count,
                  "the two streams forgot different numbers of items")


def trial_moving_an_item_in_time_lawfully_changes_what_survives():
    """The other half of the same claim: recency is a factor, so position matters.

    Without this, the safety class above could be misread as "order never
    matters", which would be false and would make the safe class vacuous. A heavy
    item moved from the head of the stream to its tail is *more* recent and
    survives where its early self did not — the ACT-R law, doing its job.
    """
    l3 = _engine()
    payloads = _permute_payloads()
    cap = _cap_for(l3, PERMUTE_ITEMS, payloads[0])
    base = _replay(l3, payloads, cap)

    # An early item that the base replay dropped; moved to the end it must survive.
    dropped = None
    for i, payload in enumerate(payloads):
        if payload["tag"] not in _retained_tags(l3, base):
            dropped = i
            break
    require(dropped is not None, "the whole stream survived — raise the pressure")

    moved = payloads[:dropped] + payloads[dropped + 1:] + [payloads[dropped]]
    after = _replay(l3, moved, cap)
    require(payloads[dropped]["tag"] in _retained_tags(l3, after),
            "an item moved from the head of the stream to its tail still did not "
            "survive — recency has stopped being a factor of importance")
    require(_retained_tags(l3, after) != _retained_tags(l3, base),
            "moving an item across the whole stream left the retained set "
            "unchanged, so the declared-safe class above is vacuous")

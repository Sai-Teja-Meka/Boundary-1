"""strain/l5 — Layer 5 (Prospection) under pressure, dirt and repetition.

Four strains. Two are named Schacter sins from `autopsy/GAPMAP.md §6`, one turns
that document's **engine thesis** on this project's own engine at the place a
Layer-5 engine could most easily earn it, and one is the determinism law
re-asserted through the two paths this layer adds.

  1. **ABSENT-MINDEDNESS — the prospective sin.** Schacter's absent-mindedness is
     the failure of *prospective* memory: the intention formed and then not acted
     on. `strain/l3` and `strain/l4` took the GAPMAP seed for this class as
     *"what is refused under budget must be refused honestly"* and made it a
     closing ledger over episodes. Here it binds on **promises**: under a budget
     that cannot hold the episodes, an armed intention is never silently
     dropped — it survives to fire, or it is still pending — and the moment it
     fires, its own `intend` episode stops being regenerable and that loss is
     **booked in the forgetting record** rather than left as a demotion that has
     quietly become a lie. That is `strain/l4`'s lesson (`BOUNDARY.log` line 26,
     the atlas-None seam) extended to the one kind of content this layer adds.

  2. **THE FIRED LEDGER BINDS** — `autopsy/GAPMAP.md §2`'s *recorded but never
     binding* thesis, inverted. The GAPMAP verdict on `generative-agents` is an
     expiration field **written and never read**; the exactly-once ledger is this
     layer's counterpart and the one field a Layer-5 engine could most plausibly
     write and never consult. It is asserted read on **both** paths — the
     satisfaction path (an intention satisfied 200 times fires once) and the
     **arming** path (`§5 L5` names no re-arming, so an `iid` that has fired is
     done) — and the teeth are demonstrated rather than assumed: a ledger-blind
     reference policy, a trial fixture and never engine code, reaches
     `dup-fire = 199` and `1 000` on the same stream where the engine reaches 0.

  3. **THE DEMOTION SEAM, FROM THE OTHER SIDE.** `strain/l4` measured what
     demotion *costs* (demoted content is `t`-addressable and not
     cue-addressable, 26‰ cue reach). This measures what it must not cost: an
     intention whose condition is satisfied by content consolidation has since
     released still fires, exactly once, at a cap where **not one episode
     survives**. `count_ge` is the predicate that reads nothing of the arriving
     payload and everything of the past, so a trigger that could only fire from
     held episodes fails here by arithmetic rather than by design.

  4. **DETERMINISM THROUGH FIRING.** Layer 5 adds two orderings a scan order
     could leak into — the pending set's and the fired ledger's insertion order,
     and the `iid` order several firings at one write take — so §2.3 is
     re-asserted over a replay that exercises both, plus the snapshot round trip
     at the gate's own cap.

**The bill, stated rather than discovered.** One whole-stream replay of
`corpora/l5stream` at the ratified cap costs ~21 s and is shared by strains 1, 3
and 4 through `_at_the_gate()`; everything else runs on small fixtures, and the
full `read(t)` partition of all 20 765 logical times costs ~2 s because three of
its four tiers answer without a sweep.
"""

import collections
import os

from _harness import require, require_equal
from adapters import l5
import _l5score
import _l5tasks
from core.state import event_cost

# The §5 L5 clauses these strains state their pressure against. Registered in
# `laws/t_rulings.py` beside their §5 L5 text and R6 clause 1: a strain does not
# apply a gate, but a §5 number cannot appear in a trial without a recorded
# authority whatever the trial does with it.
GATE_DUP_FIRE = 0
GATE_MISS = 0

LAYER_CAP = 5

# The ledger-blind reference policy's own measurement on fixture (2). It is a
# TRIAL FIXTURE and never engine code — the discipline `strain/l3`'s naive
# reference count established — and it exists so that "the ledger is read" is a
# demonstrated difference rather than an assertion about an engine that could
# have been written either way.
SATISFYING_WRITES = 200

_RUNS = {}


def _at_the_gate():
    """`corpora/l5stream` replayed at the ratified Layer-5 cap, once per run."""
    if "gate" not in _RUNS:
        b = _l5tasks.corpus()
        state, budget = _l5score.replay(
            l5, lambda cap: l5.make_engine(LAYER_CAP, cap), b)
        _RUNS["gate"] = (state, budget, b)
    return _RUNS["gate"]


def _replay(payloads, cap):
    """Ingest a fixture at `cap`, asserting the budget law after every write."""
    state = l5.make_engine(LAYER_CAP, cap)
    refused = []
    for i, payload in enumerate(payloads):
        state, t = l5.ingest(state, payload)
        if t is None:
            refused.append(i)
        require(state.occupancy <= cap,
                "occupancy %d exceeded the cap %d at write %d — the budget law "
                "broke mid-stream (§4.1)" % (state.occupancy, cap, i))
    return state, refused


def _intend(iid, cond, text_id):
    return {"kind": "intend", "iid": iid, "cond": cond,
            "fire": {"kind": "fired", "text_id": text_id}}


def _note(entity, text_id):
    return {"kind": "note", "entity": entity, "text_id": text_id}


# ---- 1. absent-mindedness: a promise is never silently dropped --------------

def trial_an_intention_survives_to_fire_or_its_loss_is_booked():
    """Schacter's PROSPECTIVE sin, on the binding corpus at the ratified cap.

    Absent-mindedness is the intention formed and then not acted on. An engine
    under budget pressure has an obvious way to commit it — drop the pending
    entry, keep the episodes, and score beautifully on everything except the one
    thing nobody measured. This trial closes that off from outside the engine,
    through `§7`'s query interface alone:

      * **every** armed intention is accounted for: 765 fired + 180 still
        pending = 945 ingested, so not one promise left the state without firing;
      * a still-pending intention's own `intend` event is returned **byte-exact**
        by `read(t0)` — the pending entry regenerates it, which is what makes
        releasing its episode at the door a demotion and not a loss;
      * a **fired** intention's `read(t0)` abstains, because the pending entry is
        gone and nothing else rebuilds a condition — and its loss is **in the
        record**: `forgot_at(t0)` carries a non-zero count for its bucket. This
        is the assertion that would go red against an engine that kept booking
        the released episode as a lossless demotion, which is exactly the defect
        `BOUNDARY.log` line 26 found one layer down and fixed there;
      * and the ledger closes over **every** logical time, emitted events
        included: `demotions + forgotten + episodes held = next_t`, with
        `forgotten` equal to the set of `t` the engine abstains on — measured by
        reading all 20 765 of them rather than by trusting a counter.
    """
    state, budget, b = _at_the_gate()

    fired = set(l5.fired_iids(state))
    pending = set(l5.pending_iids(state))
    require_equal(len(fired & pending), 0,
                  "an intention is both pending and fired — exactly-once is the "
                  "layer, and a state holding both could fire one twice")
    require_equal(sorted(fired | pending), sorted(b["intents"]),
                  "the engine ended holding neither a firing nor a pending entry "
                  "for some intention it ingested: a promise left the state "
                  "without being kept and without being refused")
    require_equal(len(fired), len(b["fireable"]),
                  "the fired ledger does not carry every fireable intention")
    require_equal(len(pending), len(b["never"]),
                  "the pending set does not carry every never-fires intention")

    # A pending promise is still readable in full; a kept one is not, and says so.
    for iid in sorted(pending):
        t0 = b["caller_t"][b["intents"][iid]["k0"]]
        ans = l5.query(state, {"op": "read", "t": t0})
        require_equal(ans["status"], "answer",
                      "intention %d is still pending, so the pending entry "
                      "regenerates its own `intend` event — read(%d) abstained"
                      % (iid, t0))
        require_equal(ans["value"], {"payload": b["payloads"][b["intents"][iid]["k0"]],
                                     "t": t0},
                      "a pending intention's own event did not come back "
                      "byte-exact from read(%d)" % (t0,))

    unbooked = []
    still_held = 0
    for iid in sorted(fired):
        t0 = b["caller_t"][b["intents"][iid]["k0"]]
        ans = l5.query(state, {"op": "read", "t": t0})
        if ans["status"] == "answer":
            # Lawful and the other half of the same rule: firing offers the
            # episode back to the store where the budget already has room, so a
            # fired intention whose event is still readable is one nothing was
            # lost of. It must be byte-exact, not approximately there.
            require_equal(ans["value"],
                          {"payload": b["payloads"][b["intents"][iid]["k0"]],
                           "t": t0},
                          "intention %d's `intend` event survived its firing but "
                          "did not come back byte-exact" % (iid,))
            still_held += 1
            continue
        booked = l5.query(state, {"op": "forgot_at", "t": t0})
        if booked["status"] != "answer" or booked["value"]["count"] < 1:
            unbooked.append(iid)
    require(not unbooked,
            "%d fired intentions left their own `intend` episode unreadable and "
            "UNBOOKED (%s): the episode was released at arming as a demotion "
            "because the pending entry regenerated it, and firing is what makes "
            "that booking false. A loss recorded as compression is `autopsy/"
            "GAPMAP.md §2`'s *recorded but never binding* landing on the one "
            "structure whose job is to say what is gone (BOUNDARY.log line 26)"
            % (len(unbooked), unbooked[:8]))
    require_equal(still_held, 0,
                  "%d fired intentions' own events are still held at the "
                  "ratified cap. That is lawful — the episode is offered back "
                  "where there is room — but at this cap the budget is pinned "
                  "and there is none, so a non-zero count here means the "
                  "measurement is no longer the one this strain describes"
                  % (still_held,))

    # The closing ledger, over every logical time the engine ever assigned.
    abstained = [t for t in range(state.next_t)
                 if l5.query(state, {"op": "read", "t": t})["status"] == "abstain"]
    require_equal(state.demotions + state.forgetting.count + l5.retained(state),
                  state.next_t,
                  "the ledger does not close: %d demotions + %d forgotten + %d "
                  "episodes held against %d events ingested (caller writes AND "
                  "the engine's own firings)"
                  % (state.demotions, state.forgetting.count,
                     l5.retained(state), state.next_t))
    require_equal(len(abstained), state.forgetting.count,
                  "the forgetting record's count is not the set of `t` the "
                  "engine abstains on: %d abstentions against %d recorded losses"
                  % (len(abstained), state.forgetting.count))
    require_equal(budget["refused"], 0,
                  "a caller write was refused at the ratified cap")


def trial_an_intention_displaces_episodes_and_the_displacement_is_recorded():
    """Under pressure the promise wins, the episode loses, and the loss is booked.

    The design decision this pins is stated in the engine's own docstring and is
    forced by the gate rather than chosen: the pending set and the fired ledger
    are **outside every eviction phase**, because `miss = 0` and `dup-fire = 0`
    are identities and an engine that could evict either could be made to break
    a ratified gate by being poor. The consequence is that an intention arriving
    at a full budget displaces an episode — and the honest half is that the
    displacement is a **recorded loss** and not a silence.

    Measured on a fixture built to make the competition unavoidable: 60 `note`
    episodes at a cap that holds only a handful, then 20 intentions that must be
    armed anyway. `count_ge` conditions are used so nothing fires until the very
    end, which keeps the pending set at its largest exactly when the budget is
    tightest.
    """
    payloads = [_note(1 + (i % 5), 1000 + i) for i in range(60)]
    payloads += [_intend(i + 1, {"p": "count_ge", "k": "note", "v": 61},
                         2000 + i) for i in range(20)]
    payloads += [_note(1, 3000)]                  # crosses the fold; all 20 fire

    generous = 4 * sum(event_cost(p) for p in payloads)
    tight = generous // 6

    state, refused = _replay(payloads, tight)
    require_equal(refused, [],
                  "a write was refused at a cap that eviction could have made "
                  "room in — the promise costs cells and episodes are what pay")

    require_equal(len(l5.fired_iids(state)), 20,
                  "not every intention fired at the fold, although all 20 "
                  "conditions were satisfied by the same arriving write")
    require_equal(len(l5.pending_iids(state)), 0,
                  "an intention was left pending after its condition was met")
    require(state.forgetting.count > 0,
            "no loss was recorded although the budget was %d against a %d-cell "
            "stream — an engine that lost nothing here did not hold what it "
            "claimed to hold" % (tight, generous // 4))
    require_equal(state.demotions + state.forgetting.count + l5.retained(state),
                  state.next_t,
                  "the ledger does not close under displacement pressure")
    abstained = sum(1 for t in range(state.next_t)
                    if l5.query(state, {"op": "read", "t": t})["status"] == "abstain")
    require_equal(abstained, state.forgetting.count,
                  "under displacement the record and the abstentions diverge: "
                  "%d abstentions against %d recorded losses"
                  % (abstained, state.forgetting.count))


# ---- 2. the fired ledger binds ---------------------------------------------

def _ledger_blind_fires(payloads):
    """A reference policy that evaluates conditions and keeps NO fired ledger.

    A **trial fixture, never engine code** (`strain/l3`'s discipline for its
    naive reference count). It reads the condition grammar exactly as the battery
    does — `_l5tasks.satisfies`, the same function the corpus's satisfaction
    points come from — and differs from a lawful engine in one respect only: it
    never records that an intention has fired, so it fires again on every later
    satisfying write. Its score is what the exactly-once clause of `§5 L5` is
    for.
    """
    live = collections.OrderedDict()
    counts = {}
    fires = []
    for k, payload in enumerate(payloads):
        kind = payload.get("kind")
        counts[kind] = counts.get(kind, 0) + 1
        for iid, cond in live.items():
            if _l5tasks.satisfies(cond, payload, counts):
                fires.append((iid, k))
        read = l5.intention(payload)
        if read is not None:
            live.setdefault(read[0], read[1])
    return fires


def trial_the_fired_ledger_is_read_on_every_later_satisfaction():
    """GAPMAP §2 inverted: the one field this layer could write and never read.

    `autopsy/generative-agents/ANATOMY.md` records an expiration written into
    every memory and consulted by nothing; `autopsy/GAPMAP.md §2` generalises it
    across four engines as *recorded but never binding*. The exactly-once ledger
    is the Layer-5 counterpart, and the failure mode is not subtle: an engine
    that marks a firing and then evaluates the intention again on the next
    satisfying write fires it 200 times and scores `dup-fire = 199`.

    The teeth are **demonstrated, not asserted**: the ledger-blind reference
    policy above is run on the same fixture and reaches exactly that, so this
    trial would be red against an engine whose mark were decorative — which is
    the property `strain/l3` established for its inflation guard and the reason
    a guard trial is worth more than a guard comment.
    """
    payloads = [_intend(1, {"p": "kind", "v": "note"}, 900)]
    payloads += [_note(1, 100 + i) for i in range(SATISFYING_WRITES)]
    cap = 4 * sum(event_cost(p) for p in payloads)

    state, refused = _replay(payloads, cap)
    require_equal(refused, [], "an in-budget write was refused")

    records = l5.fired_by(state, 1)
    require(records is not None, "the intention never fired at all")
    require_equal(len(records), 1,
                  "intention 1 fired %d times against a §5 L5 gate of "
                  "dup-fire = %d — %d later writes satisfied its condition and "
                  "every one of them had to be refused by READING the mark the "
                  "first firing left" % (len(records), GATE_DUP_FIRE,
                                         SATISFYING_WRITES - 1))
    require_equal(records[0]["t"], 2,
                  "the firing did not land on the first satisfying write (the "
                  "intention is the caller event at t=0, the first `note` at "
                  "t=1, and its firing takes the next logical time of its own)")
    require_equal(state.next_t, len(payloads) + 1,
                  "the engine's own clock says it emitted %d events for one "
                  "intention — a firing consumes exactly one `t` (§1.3), so the "
                  "clock counts firings whatever the ledger reports"
                  % (state.next_t - len(payloads),))

    ans = l5.query(state, {"op": "fired", "iid": 1})
    require_equal(ans["status"], "answer", "P1 abstained on a fired intention")
    require(isinstance(ans["value"], list) and len(ans["value"]) == 1,
            "P1 must answer with a LIST of event records, so that an intention "
            "which fired twice is visible THROUGH the query interface and not "
            "only in an engine's own bookkeeping (STAGE-B.md §2): %r"
            % (ans["value"],))

    blind = _ledger_blind_fires(payloads)
    require_equal(len(blind), SATISFYING_WRITES,
                  "the ledger-blind reference policy no longer re-fires on this "
                  "fixture, so the trial would pass against a decorative mark "
                  "and proves nothing")
    require(len(blind) - 1 > len(records) - 1,
            "the reference policy's dup-fire (%d) does not exceed the engine's "
            "(%d)" % (len(blind) - 1, len(records) - 1))


def trial_an_iid_that_has_fired_is_never_re_armed():
    """The ledger read on the WRITE path — where `§5 L5` names no re-arming.

    `corpora/l5stream/grammar.md`'s *No cancellation* section records that
    `§5 L5` *"does not name cancellation, revocation, expiry or re-arming, and
    this corpus invents none of them"*. The engine invents none either: an `iid`
    already known — pending or fired — arms nothing, so the first arming of an
    intention is the only one. A payload carrying a used `iid` is still fuel like
    any other event (§1.1) and is stored where the inherited Layer-3 law can see
    it; what it is not is a second intention.

    This is the second place the fired ledger is READ, and it is the one an
    engine could most easily leave out: no frozen corpus reaches it, because
    `l5stream`'s `iid`s are contiguous and unique
    (`ops/l5/t_l5stream.py::trial_l5stream_declared_properties_hold`). The path
    exists only under this fixture, which is precisely why it needs one.
    """
    payloads = [_intend(7, {"p": "kind", "v": "note"}, 900),
                _note(1, 101),                            # fires here
                _intend(7, {"p": "kind", "v": "note"}, 901),   # arms nothing
                _note(1, 102),
                _note(1, 103)]
    cap = 4 * sum(event_cost(p) for p in payloads)
    state, refused = _replay(payloads, cap)
    require_equal(refused, [], "an in-budget write was refused")

    records = l5.fired_by(state, 7)
    require_equal(len(records), 1,
                  "`iid` 7 fired %d times: the second `intend` payload carrying "
                  "it re-armed the intention, which is a capability `§5 L5` does "
                  "not name" % (len(records),))
    require_equal(records[0]["t"], 2,
                  "the one firing is not the one caused by the FIRST satisfying "
                  "write (the caller event at t=1 fires at t=2)")
    require_equal(state.next_t, len(payloads) + 1,
                  "the engine emitted %d events; exactly one firing is lawful "
                  "here and the clock is what says so"
                  % (state.next_t - len(payloads),))
    require_equal(l5.pending_iids(state), [],
                  "the duplicate `intend` payload left an intention pending — "
                  "the first arming wins, and a used `iid` arms nothing")

    # It is still an event: fuel is fuel (§1.1), and the engine says so.
    ans = l5.query(state, {"op": "read", "t": 3})
    require_equal(ans["status"], "answer",
                  "the duplicate `intend` payload was not retained as an "
                  "ordinary event — it arms nothing, but it was ingested")
    require_equal(ans["value"], {"payload": payloads[2], "t": 3},
                  "the duplicate `intend` event did not come back byte-exact")


def trial_an_unreadable_condition_arms_nothing_and_never_raises():
    """§7.3 on the write path: what the engine cannot evaluate, it does not promise.

    `trials/_l5tasks.satisfies` **raises** on an unknown predicate, deliberately:
    for the battery an unreadable condition is a corpus defect and a silent
    `False` would turn it into a never-fires intention nobody noticed. An engine
    has the opposite obligation — it may not raise inside a write — so it takes
    the other honest branch: a condition outside the closed vocabulary is not
    armed at all, and the payload is an ordinary irreducible event. What is
    forbidden is the third option, storing a condition the engine cannot evaluate
    and calling the result a pending intention.
    """
    bad = [
        _intend(1, {"p": "no_such_predicate", "v": 1}, 900),
        _intend(2, {"op": "xor", "args": [{"p": "kind", "v": "note"}]}, 901),
        _intend(3, {"p": "val_ge", "v": "not-an-integer"}, 902),
        _intend(4, {"p": "count_ge", "v": 1}, 903),          # no `k`
        {"kind": "intend", "iid": 5, "cond": {"p": "kind", "v": "note"},
         "fire": {"kind": "fired", "text_id": 904}, "extra": 1},   # not invertible
        {"kind": "intend", "iid": "six", "cond": {"p": "kind", "v": "note"},
         "fire": {"kind": "fired", "text_id": 905}},               # `iid` not an int
    ]
    payloads = list(bad) + [_note(1, 100 + i) for i in range(5)]
    cap = 4 * sum(event_cost(p) for p in payloads)

    state, refused = _replay(payloads, cap)
    require_equal(refused, [], "an in-budget write was refused")
    require_equal(l5.pending_iids(state), [],
                  "a condition outside the closed predicate vocabulary was armed")
    require_equal(l5.fired_iids(state), [],
                  "an intention the engine cannot evaluate fired")
    require_equal(state.next_t, len(payloads),
                  "the engine emitted an event of its own on a stream where "
                  "nothing is armed")
    for i, payload in enumerate(bad):
        ans = l5.query(state, {"op": "read", "t": i})
        require_equal(ans["status"], "answer",
                      "the unarmable payload at t=%d was not retained as an "
                      "ordinary event" % (i,))
        require_equal(ans["value"], {"payload": payload, "t": i},
                      "the unarmable payload at t=%d did not come back "
                      "byte-exact" % (i,))
    for iid in (1, 2, 3, 4, 5):
        require_equal(l5.query(state, {"op": "fired", "iid": iid})["status"],
                      "abstain",
                      "P1 answered for `iid` %d, which was never armed — §7.3 "
                      "makes capability absence a scored abstention" % (iid,))


# ---- 3. the demotion seam, from the other side ------------------------------

def trial_a_fold_over_demoted_content_still_fires_where_no_episode_survives():
    """The Layer-4 seam at its extreme: the counted episodes are all gone.

    `corpora/l5stream/grammar.md` declares `count_ge` *"a condition over exactly
    the content the layer below has demoted, priced at two cells per kind. It is
    why this layer is built on that one."* The ascension battery asserts the 111
    fireable folds fire at the ratified cap. This asserts the sharper form on a
    fixture built for it: a cap so tight that **not one episode survives**, where
    a trigger that could only fire from held episodes has nothing left to read.

    The counters `count_ge` folds over are Layer-4 state — two cells per grammar
    kind, never decremented — so the fold is exact however much of the episodic
    tier the budget has taken. Both halves are asserted: the intention fires
    exactly once at the crossing, and the events it counted are answered as
    **regenerated or gone**, never as held.
    """
    n = 40
    payloads = [{"kind": "attr", "entity": 1 + (i % 4), "key": "level",
                 "val": i} for i in range(n)]
    payloads += [_intend(1, {"p": "count_ge", "k": "attr", "v": n + 1}, 900)]
    payloads += [{"kind": "attr", "entity": 2, "key": "level", "val": 500}]

    raw = sum(event_cost(p) for p in payloads)
    state, refused = _replay(payloads, raw // 5)
    require_equal(refused, [], "a write was refused where eviction had room to make")

    # Not one of the events the fold COUNTED is still an episode. The precise
    # claim is that one and not `retained == 0`, because firing offers the
    # intention's OWN event back to the store and the swap frees enough cells to
    # take it: the survivor here is the promise, never one of the 40 `attr`
    # episodes the count was over.
    held = [t for t in range(n)
            if l5.query(state, {"op": "read", "t": t})["status"] == "answer"
            and (l5.query(state, {"op": "read", "t": t})["provenance"] or {})
            .get("kind") == "recall"]
    require_equal(held, [],
                  "%d of the events this fold counted are still held episodes — "
                  "the fold must be answered from a tier that does not exist, "
                  "and it is not being" % (len(held),))
    require(l5.retained(state) <= 1,
            "%d episodes survived a cap of a fifth of the stream's footprint; "
            "at most one can, and it is the fired intention's own event taken "
            "back by the swap that freed its condition's cells"
            % (l5.retained(state),))
    records = l5.fired_by(state, 1)
    require(records is not None,
            "the fold never fired although the %dth `attr` crossed its "
            "threshold: a trigger that reads only held episodes cannot see a "
            "count of episodes that are gone" % (n + 1,))
    require_equal(len(records), 1, "the fold fired more than once")
    require_equal(records[0]["t"], len(payloads),
                  "the fold did not fire at the write that crossed it (the "
                  "caller event at t=%d, its firing at t=%d)"
                  % (len(payloads) - 1, len(payloads)))

    kinds = collections.Counter()
    for t in range(n):
        ans = l5.query(state, {"op": "read", "t": t})
        if ans["status"] == "abstain":
            kinds["abstain"] += 1
        else:
            kinds[(ans.get("provenance") or {}).get("kind")] += 1
    require_equal(kinds.get("recall", 0), 0,
                  "an event the fold counted is still answered as a HELD episode "
                  "(`provenance.kind == \"recall\"`), so this fixture is not "
                  "measuring what it claims: %s" % (dict(kinds),))
    require(kinds.get("derive", 0) > 0,
            "not one counted event is answered as REGENERATED: %s. The seam is "
            "that the fold outlives the episodes, and a fixture where the "
            "episodes were merely gone would assert half of it" % (dict(kinds),))
    require_equal(l5.query(state, {"op": "count", "kind": "attr"})["value"],
                  n + 1,
                  "the per-kind counter the fold reads is not the count of every "
                  "`attr` event ingested — it is never decremented by eviction, "
                  "which is the whole reason a fold survives its episodes")


def trial_the_gate_run_fires_every_fold_over_content_it_has_released():
    """The same seam on the binding corpus, stated as a share rather than a case.

    At the ratified cap the engine holds 952 of 20 765 episodes, so a condition
    folding over the past is folding over content it has overwhelmingly released.
    Every fireable `count_ge` intention fires exactly once, and the arithmetic
    that makes it impossible to do otherwise is recorded here: the raw episodic
    footprint is 182 555 cells against a 45 638-cell cap.
    """
    state, _budget, b = _at_the_gate()
    folds = [iid for iid in _l5tasks.count_ge_conditions()
             if b["sat"][iid] is not None]
    require(folds, "no fold is fireable, so the seam is not exercised")
    for iid in folds:
        records = l5.fired_by(state, iid)
        require(records is not None and len(records) == 1
                and records[0]["t"] == b["fire_t"][iid],
                "intention %d folds over the past and did not fire exactly once "
                "at the logical time its satisfaction point forces (%s): %r"
                % (iid, b["fire_t"][iid], records))
    held = l5.retained(state)
    require(held * 4 < b["n"],
            "the engine holds %d episodes of %d events, which is too many for "
            "this to be a statement about released content" % (held, b["n"]))


# ---- 4. determinism through firing ------------------------------------------

def trial_determinism_holds_through_arming_firing_and_the_round_trip():
    """§2.3, re-asserted over the two orderings this layer adds.

    Layer 5 introduces two places a scan order could leak into the state — the
    insertion order of the pending set and of the fired ledger — and one place an
    engine could substitute its own for a declared one: several intentions
    satisfied by a single write must fire in **`iid` ascending order**, which
    `grammar.md` declares precisely so that determinism does not rest on however
    an engine happens to iterate.

    Asserted at two scales: byte-identity across two independent replays of a
    4 000-event prefix under real pressure (which fires, demotes and forgets),
    and the snapshot round trip at the gate's own cap on the whole stream, where
    the pending set, the fired ledger and the exactly-once invariant all have to
    survive serialization.
    """
    b = _l5tasks.corpus()
    prefix = b["payloads"][:4000]
    cap = sum(event_cost(p) for p in prefix) // 4

    first, refused_a = _replay(prefix, cap)
    second, refused_b = _replay(prefix, cap)
    require_equal(refused_a, refused_b, "two identical replays refused differently")
    require_equal(l5.snapshot(first), l5.snapshot(second),
                  "two identical replays produced different bytes — §2.3 is a "
                  "law, and firing order, pending-set order and fired-ledger "
                  "order are three new ways for a scan order to leak in")
    require(first.next_t > len(prefix),
            "the prefix fired nothing, so this replay does not exercise the "
            "orderings it exists to pin")
    require(first.forgetting.count > 0 and first.demotions > 0,
            "the prefix neither forgot nor demoted anything under a quarter of "
            "its own footprint")

    state, _budget, _b = _at_the_gate()
    snap = l5.snapshot(state)
    restored = l5.restore(snap)
    require_equal(l5.snapshot(restored), snap,
                  "snapshot/restore is not byte-identical at the ratified cap")
    require_equal(l5.state_checksum(restored), l5.state_checksum(state),
                  "the restored state's canonical checksum differs")
    require_equal(l5.pending_iids(restored), l5.pending_iids(state),
                  "the pending set did not survive the round trip")
    require_equal(l5.fired_iids(restored), l5.fired_iids(state),
                  "the fired ledger did not survive the round trip")
    for iid in (l5.fired_iids(state)[:5] + l5.pending_iids(state)[:5]):
        require_equal(l5.query(restored, {"op": "fired", "iid": iid}),
                      l5.query(state, {"op": "fired", "iid": iid}),
                      "the restored state answered P1 for `iid` %d differently"
                      % (iid,))


def trial_several_firings_at_one_write_take_iid_order_on_a_fixture():
    """The declared total order, on a fixture that makes a scan order visible.

    `l5stream`'s multi-satisfaction indices have a fan-out of 3; this fixture
    arms ten intentions in **descending** `iid` order and satisfies all of them
    with one write, so an engine that fired in insertion order would produce
    exactly the reverse of the declared one and the difference would be a `t`
    apart rather than a hash apart.
    """
    payloads = [_intend(10 - i, {"p": "kind", "v": "note"}, 900 + i)
                for i in range(10)]
    payloads += [_note(1, 500)]
    cap = 4 * sum(event_cost(p) for p in payloads)
    state, refused = _replay(payloads, cap)
    require_equal(refused, [], "an in-budget write was refused")

    order = []
    for iid in range(1, 11):
        records = l5.fired_by(state, iid)
        require(records is not None and len(records) == 1,
                "intention %d did not fire exactly once: %r" % (iid, records))
        order.append((records[0]["t"], iid))
    order.sort()
    require_equal([iid for _t, iid in order], list(range(1, 11)),
                  "ten intentions satisfied by one write did not fire in `iid` "
                  "ascending order — §2.3 needs a DECLARED total order, and the "
                  "arming order here is its exact reverse")
    times = [t for t, _iid in order]
    require_equal(times, list(range(times[0], times[0] + 10)),
                  "the ten firings do not occupy consecutive logical times: %s. "
                  "Each is an event and consumes one `t` (§1.3, R6 clause 2)"
                  % (times,))
    require_equal(state.next_t, len(payloads) + 10,
                  "the engine's clock does not account for exactly ten firings")


def trial_the_strain_file_is_registered_where_the_class_index_says_it_is():
    """Docs are checked, not trusted — the discipline `[L4] [PACKAGE]` set.

    A strain class whose README names a file that does not exist, or a file the
    README does not name, is an index that has stopped being a record.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    readme = os.path.join(os.path.dirname(here), "README.md")
    with open(readme, "r", encoding="utf-8") as fh:
        text = fh.read()
    require("l5/t_prospection_strain.py" in text,
            "trials/strain/README.md does not index this file")
    require(os.path.isfile(os.path.join(here, "t_prospection_strain.py")),
            "the indexed strain file is not where the index says it is")

"""strain/l4 — the demotion seam: what compression costs, and what it may book.

Two strains, both designed from measured field notes in `shell/dogfood/FIELD.md`
rather than from the layer's own prose, because the seam they attack is exactly
where `core/layers/README-l4.md` states a price **in words and nowhere in a
number**. Demotion is the Layer-4 move: an episode is released *because its
content already lives somewhere else* (`README-l4 §0.2`). These two trials ask
the two questions that move honestly makes reachable — what the release costs
that is not content, and whether the release was lossless at all.

| strain | class | what would otherwise fail quietly |
|---|---|---|
| the cue channel narrows as the budget tightens | **blocking** (Schacter; `autopsy/GAPMAP.md §6`) | an associative channel that quietly shrinks to a rounding error while every score still clears its gate |
| the forgetting record binds | **recorded-but-never-binding** (`autopsy/GAPMAP.md §2`, the engines' thesis) | a loss booked as compression, in our own engine |

## Strain 1 — blocking, over ASSERTIONS

`PULSE` (`BOUNDARY.log` line 24) surveyed the seven-sin catalog against
`strain/l3` and `strain/l4` and found **one genuine gap**: Layer 4 opened a new
blocking surface that no trial measures, because `README-l4 §4` records that a
demoted episode is unreachable by cue and records it in prose only.

The field note that followed is what this trial is designed from, and it
**redirected** the measurement (`FIELD.md`, 2026-07-26, *"THE DEMOTION SEAM,
measured out-of-suite"*): asked whether a demoted session summary is still
reachable by `recall`, the honest answer refutes the question — *"no session
summary is ever demoted"*, because a prose episode is irreducible to the frozen
facet map and pressure **forgets** it instead. Only **assertions** are ever
demoted. So the strain is stated over assertions, on the binding corpus, at the
footprint the layer is gated at, and it asserts three things at once:

  (a) a demoted assertion keeps its content **byte-exact** through `read(t)`,
      and the two provenance kinds separate the channels: `derive` for an event
      the schema regenerated, `recall` for one still stored as an episode;
  (b) a cue drawn from a demoted event **abstains** — and never answers wrongly.
      The abstention is the honesty (§3.0 pays it 100 and pays a confident wrong
      answer 0);
  (c) a **held** episode is still cue-reachable, so (b) measures a lost channel
      and not a broken index.

This is a **measured structural limitation**, asserted so that it cannot change
silently in either direction. `README-l4 §0.1` proved that at a 250‰ footprint
exactly one access path is affordable — an exact `t → pair` index costs a third
cell per assertion and puts the schema at 343‰ — so the associative path is the
one the budget does not buy. The trial pins the behaviour; `README-l4 §4`'s
non-capability note says why.

## Strain 2 — the forgetting record must bind

`autopsy/GAPMAP.md §2`'s first thesis is *"recorded but never binding"*: every
engine autopsied writes the metadata that would make it correct and then never
reads it where it counts — GA's `expiration` never read to evict, Graphiti's
`invalid_at` not honoured by a default read, Letta's summary wearing a user
turn's clothes. This trial is that thesis turned on **our own** engine, at the
one place a field note found it true:

> `FIELD.md`, 2026-07-26, *the atlas-None seam*: *"a payload that reads as an
> assertion but does NOT invert sets `atlas[key] = None`, and when the budget
> then releases its episode the engine books it as a **demotion** while `read(t)`
> abstains on it forever — 8 such writes at a 40-cell cap gave demotions 7,
> forgetting-record count 0, `read(0)` None, so the ledger says nothing was lost
> and the content is gone."*

That is a loss booked as compression: the forgetting record — the one structure
whose whole job is to say what is gone — was recorded and was not binding.
`README-l4 §2.3`'s closing ledger was true of the corpora it was measured on
(every frozen corpus has zero non-invertible keys) and not of the code.

**This trial was RED first**, against the engine as Layer 4 was claimed with it,
on all three of its sections. The demand it makes is truthful accounting rather
than a particular policy: a non-invertible fold is either

  * **FORGOTTEN** — the forgetting record gains its count and its mass, and
    `read(t)` abstains on it consistently; or
  * **REFUSED demotion** and held as an episode (or refused outright under
    §4.1.2, `t` unspent and the state unchanged),

and it is **never booked as demoted while unregenerable**. The engine fix that
followed is stated in one line in `core/layers/l4_consolidation.atlas_after`:
**the demotion invariant is invertibility.** Engine fixes under strain are the
established precedent — the Layer-4 ASCEND session fixed three of its own
findings rather than relaxing them (`BOUNDARY.log` line 23).

No frozen artifact moves here: no ratified number, no corpus, no anchor hash. No
frozen corpus reaches the non-invertible path (`FIELD.md`: murk 18 atlas keys,
chronicle 17, l4stream 16, all `None`-free), so `l1`–`l4` anchors come through
byte-identical and the fix is measurable only on fixtures this file builds.
"""

from fractions import Fraction

from _harness import require, require_equal
import _l4tasks
from adapters import l4
from core.serialize import encode
from core.state import event_cost

BINDING = "l4stream"

# The ratified §5 L4 footprint (BOUNDARY-RULINGS.md R4 clause 2 reads it in
# permille of the raw episodic footprint). Not a gate this file applies to an
# engine — `ascension/l4` owns that — but the pressure both strains are stated
# at, since the blocking surface exists *because* of it: at 250‰ exactly one
# access path is affordable (`README-l4 §0.1`). Registered in `laws/t_rulings.py`
# against §5 L4 and R4 like every other copy.
GATE_FOOTPRINT = 250

# Strain 2's mixed fixture. Small by design and built here rather than frozen:
# no corpus in the repo contains a non-invertible fold, and adding one would be a
# corpus decision, not a strain (§8.2 freezes generator outputs; this is a
# fixture, like `strain/l3`'s flood).
FIXTURE_ENTITIES = 12
FIXTURE_ROUNDS = 8

# The FIELD.md reproduction, verbatim: eight writes at a forty-cell cap.
FIELD_NOTE_WRITES = 8
FIELD_NOTE_CAP = 40

_RUN = {}


# ---- helpers ---------------------------------------------------------------

def _covers(payload, cue):
    """Exact containment, written here rather than borrowed from the engine.

    A trial that verified `recall` with the engine's own containment predicate
    would agree with it by construction. This is the same rule stated
    independently: every key of the cue present with an equal value, compared as
    canonical bytes so `1` never satisfies `true` (§2.4).
    """
    if not isinstance(cue, dict) or not isinstance(payload, dict):
        return encode(payload) == encode(cue)
    for name, value in cue.items():
        if name not in payload or not _covers(payload[name], value):
            return False
    return True


def _partition(state, by_t):
    """Split every assigned `t` into held / demoted / lost, by what the engine says.

    The classification is read off the ordinary query interface (§7) and nothing
    else: `read(t)` either abstains (**lost**) or answers with a provenance kind
    of `recall` (the episode is still stored: **held**) or `derive` (the schema
    regenerated it: **demoted**). Byte-exactness is checked on every answer, so
    a "demotion" that came back as a different event is caught here rather than
    being counted as a success.
    """
    held, demoted, lost, corrupted = set(), set(), set(), []
    for t in range(state.next_t):
        answer = l4.query(state, {"op": "read", "t": t})
        if answer["status"] == "abstain":
            lost.add(t)
            continue
        if encode(answer["value"]["payload"]) != encode(by_t[t]):
            corrupted.append(t)
        if answer["provenance"]["kind"] == "recall":
            held.add(t)
        else:
            demoted.add(t)
    return held, demoted, lost, corrupted


def _audit_ledger(state, by_t, label):
    """The closing ledger, asserted against what the engine actually answers.

    `README-l4 §2.3` states the identity; this checks it against the partition
    rather than against the counters' own arithmetic, which is the difference
    between a ledger that closes and a ledger that is *true*:

        demotions + forgotten + episodes held  ==  events ingested
        forgotten                              ==  the set `read(t)` abstains on
        demotions                              ==  the set `read(t)` regenerates
    """
    held, demoted, lost, corrupted = _partition(state, by_t)
    ledger = l4.query(state, {"op": "consolidation"})["value"]
    forgotten = state.forgetting.count

    require(not corrupted,
            "%s: read(t) returned a different event for t=%r — a released "
            "episode came back as something else, which is not honest loss"
            % (label, corrupted[:5]))
    require_equal(ledger["demotions"] + forgotten + ledger["episodes"],
                  state.next_t,
                  "%s: the ledger does not close — %d demoted + %d forgotten + "
                  "%d held against %d ingested"
                  % (label, ledger["demotions"], forgotten, ledger["episodes"],
                     state.next_t))
    require_equal(ledger["demotions"], len(demoted),
                  "%s: the engine books %d demotions but regenerates %d events "
                  "— a demotion it cannot reproduce is a loss wearing "
                  "compression's name" % (label, ledger["demotions"],
                                          len(demoted)))
    require_equal(forgotten, len(lost),
                  "%s: the forgetting record counts %d losses while read(t) "
                  "abstains on %d — the record is not the set of things it lost"
                  % (label, forgotten, len(lost)))
    require_equal(ledger["episodes"], len(held),
                  "%s: %d episodes held against %d answered from a stored row"
                  % (label, ledger["episodes"], len(held)))
    require(state.forgetting.mass >= forgotten,
            "%s: %d losses carry %d mass — every loss carries at least its own "
            "weight, so a record with less mass than count has lost a loss"
            % (label, forgotten, state.forgetting.mass))
    require_equal(l4.accounted_occupancy(state), state.occupancy,
                  "%s: the incremental cost accounting drifted from the state's "
                  "own atoms (rule P, R4 clause 3)" % (label,))
    require(state.occupancy <= state.budget_cap,
            "%s: the budget law broke (%d > %d)"
            % (label, state.occupancy, state.budget_cap))
    return held, demoted, lost


def _replay(payloads, cap):
    """Ingest a fixture at `cap`; return the state and the `t -> payload` map.

    A refused write spends no `t` (§4.1.2), so the map is built from what the
    engine returned and never from the caller's own enumeration.
    """
    state = l4.make_engine(4, cap)
    by_t = {}
    refused = 0
    for payload in payloads:
        state, t = l4.write(state, payload)
        if t is None:
            refused += 1
        else:
            by_t[t] = payload
    return state, by_t, refused


def _binding_at_the_gate():
    """`corpora/l4stream` replayed at the ratified footprint, built once."""
    if "gate" not in _RUN:
        bundle = _l4tasks.corpus(BINDING)
        state, by_t, refused = _replay(bundle["payloads"], bundle["budget_cap"])
        require_equal(refused, 0,
                      "%d writes were refused on the binding corpus at its own "
                      "ratified footprint" % (refused,))
        _RUN["gate"] = (state, by_t, bundle)
    return _RUN["gate"]


# ---- strain 1: blocking ------------------------------------------------------

def trial_a_demoted_assertion_keeps_its_content_and_loses_its_cue():
    """**Blocking.** The associative channel narrows as the budget tightens.

    Schacter's blocking is the memory that is present and unreachable — and that
    is exactly what a demotion produces, so this is the sin Layer 4 is heir to
    that `PULSE` found no trial measuring. `README-l4 §4` states it in prose:
    *"An episode released into consolidated form is no longer reachable by cue:
    `recall` runs over the handle index of retained episodes, and a demoted event
    has none. Its content is fully answerable by `read(t)` … but the associative
    channel narrows as the budget tightens."*

    Measured on the binding corpus at the footprint the gate is stated at,
    where 18 788 of 20 000 events are demoted and 498 survive as episodes:

      (a) **content survives, addressed by `t`.** Every demoted event comes back
          byte-exact from `read(t)`, tagged `derive`; every held one comes back
          byte-exact tagged `recall`. The two kinds partition the answers, so the
          engine is not merely right — it says which channel it was right from.
      (b) **the cue is gone, and the loss is honest.** Not one of the demoted
          events answers to a cue built from its own payload, and not one such
          cue is answered *wrongly*: `recall` abstains (§3.0 pays 100) rather
          than reaching for the nearest retained neighbour (§3.0 pays 0).
      (c) **the index still works.** All 498 held episodes are reached exactly by
          their own content, so (b) measures a channel the budget closed and not
          an index this trial broke.

    The number the prose never carried: at 250‰ the cue channel reaches **498 of
    19 286** still-answerable events — 26‰ of what `read(t)` reaches. That is the
    price of the one access path §0.1 proved affordable, and it is now asserted
    rather than described.
    """
    state, by_t, bundle = _binding_at_the_gate()
    held, demoted, lost = _audit_ledger(state, by_t, "l4stream at the gate")

    footprint = _l4tasks.permille(
        Fraction(state.occupancy, bundle["raw_cells"]))
    require(footprint <= GATE_FOOTPRINT,
            "the strain ran at %d‰, not at the footprint it is stated at"
            % (footprint,))
    require(len(demoted) > 0 and len(held) > 0,
            "the fixture demoted %d and held %d — a blocking strain needs both "
            "channels populated or it measures nothing"
            % (len(demoted), len(held)))

    # (b) a cue drawn from a demoted event: blocked, and never wrong.
    held_payloads = {t: l4.read(state, t)["payload"] for t in held}
    blocked = 0
    misdirected = []
    for t in sorted(demoted):
        cue = by_t[t]
        answer = l4.query(state, {"op": "recall", "cue": cue})
        if answer["status"] == "abstain":
            blocked += 1
            continue
        got = answer["value"]["t"]
        if got == t or got not in held or not _covers(held_payloads[got], cue):
            misdirected.append((t, got))
    require(not misdirected,
            "recall answered a demoted cue with an event that does not satisfy "
            "it: %r — the abstention is the honesty, and a confident neighbour "
            "scores 0 under §3.0" % (misdirected[:5],))
    require_equal(blocked, len(demoted),
                  "%d of %d demoted events were still reachable by their own "
                  "content — the seam this strain pins is not where "
                  "README-l4 §4 says it is" % (len(demoted) - blocked,
                                               len(demoted)))

    # (c) the held episodes are still reached exactly, so (b) is a lost channel.
    reached = 0
    unreachable = []
    for t in sorted(held):
        cue = held_payloads[t]
        answer = l4.query(state, {"op": "recall", "cue": cue})
        if answer["status"] == "answer" and answer["value"]["t"] == t:
            reached += 1
            continue
        twins = sum(1 for u in held if _covers(held_payloads[u], cue))
        if not (answer["status"] == "abstain" and twins > 1):
            unreachable.append(t)
    require(not unreachable,
            "held episodes %r are not reachable by their own content and are "
            "not ambiguous either — the cue channel is broken rather than "
            "narrowed, and strain (b) would be vacuous" % (unreachable[:5],))
    require_equal(reached, len(held),
                  "only %d of %d held episodes were recalled exactly"
                  % (reached, len(held)))

    # The price, as a number: what the surviving content costs the cue channel.
    answerable = len(held) + len(demoted)
    require(1000 * len(held) < 100 * answerable,
            "the cue channel reaches %d of %d answerable events — this fixture "
            "applies no real demotion pressure, so the blocking claim is not "
            "under test" % (len(held), answerable))


# ---- strain 2: the forgetting record binds -----------------------------------

def _fixture():
    """A stream carrying all three payload classes, plus a key that flips.

    * `status` — a well-formed `attr`: folds and **inverts**, so its episodes are
      genuinely demotable.
    * `level` — an `attr` carrying one extra field (`unit`). `facet` reads it as
      an assertion, so it answers Q1 and Q2 exactly, but `rebuild` cannot produce
      the extra field: the payload does not round-trip, the atlas marks the key
      `None`, and **nothing regenerates its events**. This is the FIELD.md
      payload class, in a stream rather than alone.
    * `note` — irreducible, the tier Layer 4 has always forgotten honestly.
    * `owns` — a `link`, an assertion on `(src, rel)`: a second invertible form,
      so the demotable tier is not one grammar kind wide.
    """
    out = []
    for r in range(FIXTURE_ROUNDS):
        for e in range(1, FIXTURE_ENTITIES + 1):
            out.append({"kind": "attr", "entity": e, "key": "status",
                        "val": "v%d" % r})
            out.append({"kind": "attr", "entity": e, "key": "level",
                        "val": r, "unit": "db"})
            out.append({"kind": "note", "entity": e,
                        "text_id": r * FIXTURE_ENTITIES + e})
            out.append({"kind": "link", "src": e, "rel": "owns",
                        "dst": (e % FIXTURE_ENTITIES) + 1})
    return out


def trial_a_non_invertible_fold_is_forgotten_and_never_booked_as_a_demotion():
    """**Recorded but never binding**, found in our own engine and closed.

    Three sections, each a state the engine can reach and could once misreport.

    **1. The field note, reproduced.** Eight writes at a forty-cell cap, of a
    payload that reads as an assertion and does not invert. The measured defect
    was `demotions 7, forgetting count 0, read(0) None`: seven events gone, the
    ledger saying nothing was lost. What is demanded is not a particular
    disposition but a truthful one — every released event is in the forgetting
    record, or it is still an episode, and `read(t)` and the record agree.

    **2. The key that flips.** An attribute key can be invertible for a hundred
    events and then meet a payload under a second grammar form, or one carrying a
    field the rebuild cannot produce. Everything already folded under it stops
    being regenerable in that instant — including episodes **already released as
    demotions**, whose booking is retroactively false. The engine reconciles the
    ledger on that write (`_reconcile_lost_key`): held episodes leave the
    demotable tier, released ones become recorded losses, and the demotion
    counter gives them back.

    **3. A mixed stream under real pressure**, at the ratified footprint and then
    below it, so demotion, forgetting and chain-shedding all run. The identities
    of `README-l4 §2.3` are asserted over the whole partition at both caps —
    including on a state with **shed chains**, where the closing ledger could not
    previously be stated at all.

    Determinism (§2.3) and the snapshot round trip are re-asserted on the flipped
    state, because a ledger correction that did not survive `restore` would be a
    correction only in memory.
    """
    # --- 1. the FIELD.md reproduction ---------------------------------------
    payloads = [{"kind": "attr", "entity": 1, "key": "k", "val": i,
                 "note": "x"} for i in range(FIELD_NOTE_WRITES)]
    state, by_t, refused = _replay(payloads, FIELD_NOTE_CAP)
    require(state.atlas.get("k") is None,
            "the reproduction's key still claims an inversion, so the field "
            "note's payload class was not reached at all")
    held, demoted, lost = _audit_ledger(state, by_t, "FIELD.md reproduction")
    require_equal(len(demoted), 0,
                  "%d of these events were booked as demotions — nothing "
                  "regenerates an assertion whose key does not invert, so a "
                  "demotion here is a loss called compression" % (len(demoted),))
    require(len(lost) > 0,
            "nothing was released at all at a %d-cell cap, so the reproduction "
            "never reached the seam" % (FIELD_NOTE_CAP,))
    require(refused + state.next_t == FIELD_NOTE_WRITES,
            "the reproduction lost a write: %d refused + %d assigned against %d "
            "submitted" % (refused, state.next_t, FIELD_NOTE_WRITES))

    # --- 2. the key that flips ----------------------------------------------
    clean = [{"kind": "attr", "entity": 1, "key": "k", "val": i}
             for i in range(10)]
    state, by_t, _refused = _replay(clean, 60)
    require(state.demotions > 0,
            "the flip fixture demoted nothing before the flip, so there is no "
            "false booking for the flip to correct")
    before = state.demotions
    _held, demoted_before, _lost = _audit_ledger(state, by_t, "before the flip")
    require_equal(len(demoted_before), before,
                  "the pre-flip state was already mis-booked")

    flipped, t = l4.write(state, {"kind": "attr", "entity": 1, "key": "k",
                                  "val": 99, "unit": "db"})
    require(t is not None, "the flipping write was refused, so nothing flipped")
    by_t[t] = {"kind": "attr", "entity": 1, "key": "k", "val": 99,
               "unit": "db"}
    require(flipped.atlas.get("k") is None,
            "the second grammar form left the key claiming an inversion")
    held, demoted, lost = _audit_ledger(flipped, by_t, "after the flip")
    require_equal(len(demoted), 0,
                  "%d events are still booked as demotions under a key that no "
                  "longer inverts — the correction did not reach the events "
                  "released before it" % (len(demoted),))
    require(len(lost) >= before,
            "only %d losses recorded against %d demotions the flip invalidated"
            % (len(lost), before))
    require_equal(l4.snapshot(l4.restore(l4.snapshot(flipped))),
                  l4.snapshot(flipped),
                  "the corrected ledger did not survive a snapshot round trip")

    # --- 3. a mixed stream, at the footprint and below it -------------------
    fixture = _fixture()
    raw = sum(event_cost(p) for p in fixture)
    seen_shedding = False
    for divisor, label in ((4, "the ratified footprint"), (6, "below it")):
        cap = raw // divisor
        state, by_t, _refused = _replay(fixture, cap)
        require(state.atlas.get("level") is None
                and state.atlas.get("status") == "attr",
                "%s: the fixture no longer carries both an invertible and a "
                "non-invertible key" % (label,))
        held, demoted, lost = _audit_ledger(state, by_t, label)
        require(len(demoted) > 0 and len(lost) > 0 and len(held) > 0,
                "%s: demoted %d, lost %d, held %d — the identity is only under "
                "test where all three dispositions occur"
                % (label, len(demoted), len(lost), len(held)))
        for t in sorted(demoted):
            require(l4.facet(by_t[t]) is not None
                    and state.atlas.get(l4.facet(by_t[t])[1]) is not None,
                    "%s: t=%d was booked as a demotion while its key does not "
                    "invert" % (label, t))
        if l4.query(state, {"op": "consolidation"})["value"]["damaged"] > 0:
            seen_shedding = True
        again, _by_t, _refused = _replay(fixture, cap)
        require_equal(l4.snapshot(again), l4.snapshot(state),
                      "%s: two identical streams produced different states "
                      "(§2.3)" % (label,))

    require(seen_shedding,
            "no chain was shed at either cap, so the ledger identity was never "
            "asserted on a state where shedding had booked losses of its own")

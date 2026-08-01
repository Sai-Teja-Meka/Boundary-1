"""anchors/ — the Layer-5 frozen anchors (BOUNDARY.md §6 anchors, §9).

Captures the exact canonical state of a fresh **prospection** engine
(`layer_cap = 5`) after replaying the frozen corpora — the pending set and the
fired ledger included, on top of everything Layer 4 already pins. The expected
hashes live in `trials/anchors/l5.json` and are **frozen**: once set (this
`ASCEND` session) an anchor's expected output never changes.

Two kinds of entry, because this layer has two things worth pinning:

  * **`corpora`** — the base corpora at `DEFAULT_BUDGET`, where nothing is
    evicted. `sessions` and `murk` carry no intention at all, so they pin that
    prospection is **inert** where there is nothing to watch: the same
    derivation Layer 4 performs, `f = 0` at every write, `next_t` equal to the
    caller count. `l5stream` pins the opposite — every one of its 945 intentions
    armed, all 765 firings emitted at their own logical times, and **nothing
    lost**: at a generous cap a fired intention's own `intend` event is taken
    back into the store, so `forgotten` is 0 and `read(t)` answers every caller
    event byte-exact.
  * **`prospection`** — `l5stream` replayed at the ratified 45 638-cell cap
    (`R6` clause 4), so the anchor covers what this layer is actually for: the
    exact state after 17 772 demotions, 2 041 recorded losses and 765 firings,
    with 180 intentions still pending. A drift in the arming rule, the firing
    order, the pending-set or fired-ledger layout, the loss reconciliation or
    the row codec moves this hash even when every score still clears the gate.
    That is the point of an anchor — scores can survive a behavioural change;
    bytes cannot.

These are NEW anchors, deliberately separate from `anchors/l1.json` …
`anchors/l4.json`. Those record replay under `make_engine(layer_cap = 1..4)`
through their own engines and stay byte-identical forever; the capped
constructor is what keeps old anchors eternal, and each new layer records its
own (§9.2).
"""

import json
import os

from _harness import require, require_equal
from adapters import l5
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen
from corpora.l5stream import generator as l5stream_gen

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANCHOR_PATH = os.path.join(_HERE, "l5.json")

_GENERATORS = {
    "sessions": sessions_gen,
    "murk": murk_gen,
    "l5stream": l5stream_gen,
}


def _load_anchors():
    with open(_ANCHOR_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


_REPLAYS = {}


def _replay_cap5(gen, seed, n, budget_cap=None):
    key = (gen.__name__, seed, n, budget_cap)
    if key not in _REPLAYS:
        state = l5.empty() if budget_cap is None else l5.make_engine(5, budget_cap)
        for payload in gen.generate(seed, n):
            state, t = l5.ingest(state, payload)
            require(t is not None,
                    "anchor replay hit a hard refusal — cap too small?")
        _REPLAYS[key] = state
    return _REPLAYS[key]


def _shape(state):
    return {
        "next_t": state.next_t,
        "episodes": l5.retained(state),
        "demotions": state.demotions,
        "forgotten": state.forgetting.count,
        "occupancy": state.occupancy,
        "keys": len(state.chains),
        "pairs": sum(len(per) for per in state.chains.values()),
        "assertions": sum(len(chain) for per in state.chains.values()
                          for chain in per.values()),
        "index_atoms": len(state.index),
        "pending": len(l5.pending_iids(state)),
        "fired": len(l5.fired_iids(state)),
    }


def trial_l5_construction_constants_match_the_anchor_assumption():
    anchors = _load_anchors()
    require_equal(l5.DEFAULT_BUDGET, anchors["default_budget"],
                  "L5 DEFAULT_BUDGET drifted from the frozen anchor assumption")
    require_equal(sorted(l5.PREDICATES), anchors["predicates"],
                  "the declared predicate vocabulary gained or lost a predicate "
                  "— every firing in every anchor depends on that reading")
    require_equal(sorted(l5.CONNECTIVES), anchors["connectives"],
                  "the declared connective vocabulary drifted")
    require_equal(list(l5.INTENTION_FORM), anchors["intention_form"],
                  "the declared intention facet drifted — an intention that no "
                  "longer inverts is one whose episode may not be released")
    require_equal(sorted(l5.ASSERTION_FORMS), anchors["assertion_kinds"],
                  "the inherited Layer-4 assertion facet gained or lost a kind")


def trial_l5_frozen_corpus_state_hashes_are_unchanged():
    anchors = _load_anchors()
    for name, spec in sorted(anchors["corpora"].items()):
        gen = _GENERATORS[name]
        require_equal(spec["seed"], gen.SEED,
                      "%s: anchor seed != generator SEED" % (name,))
        state = _replay_cap5(gen, spec["seed"], spec["n"])
        got = _shape(state)
        for field, want in sorted(got.items()):
            require_equal(want, spec[field],
                          "%s: %s drifted from the L5 anchor" % (name, field))
        require_equal(state.forgetting.count, 0,
                      "%s: an event was forgotten where the anchor records none "
                      "— at a generous cap prospection loses nothing, and a "
                      "fired intention's own event is taken back into the store"
                      % (name,))
        require_equal(l5.state_checksum(state), spec["state_sha256"],
                      "%s: canonical-state hash drifted from the frozen L5 anchor"
                      % (name,))


def trial_l5_intention_free_corpora_are_inert_under_prospection():
    """`f = 0` pinned as bytes: where nothing is armed, nothing is emitted.

    `R6` clause 2 rests on this — *"one ingest, one `t`" is that rule's `f = 0`
    case* — and `ascension/l5` asserts it over the frozen bytes of every corpus
    in the registry. What is added here is the engine's side of the same claim,
    for the two corpora this anchor replays: no pending entry, no fired entry,
    and a logical clock that ends exactly at the caller count.
    """
    anchors = _load_anchors()
    for name in ("sessions", "murk"):
        spec = anchors["corpora"][name]
        state = _replay_cap5(_GENERATORS[name], spec["seed"], spec["n"])
        require_equal(state.next_t, spec["n"],
                      "%s carries no intention, so the engine may not emit an "
                      "event of its own — its clock ended at %d over %d caller "
                      "writes" % (name, state.next_t, spec["n"]))
        require_equal((len(l5.pending_iids(state)), len(l5.fired_iids(state))),
                      (0, 0),
                      "%s armed or fired something, which no payload in it can "
                      "do" % (name,))
        require_equal(state.demotions, spec["demotions"],
                      "%s: the demotion count drifted" % (name,))


def trial_l5_prospection_state_hash_is_unchanged():
    """The anchor that pins **prospection under pressure**, not merely arming."""
    anchors = _load_anchors()
    spec = anchors["prospection"]["l5stream_at_the_gate"]
    require_equal(spec["seed"], l5stream_gen.SEED, "anchor seed != generator SEED")
    state = _replay_cap5(l5stream_gen, spec["seed"], spec["n"],
                         spec["budget_cap"])

    got = _shape(state)
    for field, want in sorted(got.items()):
        require_equal(want, spec[field],
                      "%s drifted from the L5 prospection anchor" % (field,))
    require(state.occupancy <= spec["budget_cap"],
            "the anchored state is over its own cap (%d > %d)"
            % (state.occupancy, spec["budget_cap"]))
    require_equal(len(state.damaged), spec["damaged"],
                  "the shed-chain count drifted from the anchor")
    require_equal(state.forgetting.width, spec["forget_width"],
                  "the forgetting record's coarsened width drifted")
    require_equal(len(state.forgetting.buckets), spec["forget_buckets"],
                  "the forgetting record's bucket count drifted")
    require_equal(l5.pending_cells(state.pending), spec["pending_cells"],
                  "the pending set's own cell count drifted")
    require_equal(l5.fired_cells(state.fired), spec["fired_cells"],
                  "the fired ledger's own cell count drifted")
    require_equal(l5.state_checksum(state), spec["state_sha256"],
                  "the canonical-state hash drifted from the frozen L5 anchor — "
                  "the arming rule, the firing order, the pending-set or "
                  "fired-ledger layout, the loss reconciliation or the row codec "
                  "has changed behaviour")


def trial_l5_anchor_state_snapshot_round_trips_prospection_included():
    anchors = _load_anchors()
    spec = anchors["prospection"]["l5stream_at_the_gate"]
    state = _replay_cap5(l5stream_gen, spec["seed"], spec["n"],
                         spec["budget_cap"])
    # restore validates the checksum, rebuilds the Layer-4 half through the
    # frozen Layer-4 reader, re-accounts occupancy from the state alone, and
    # refuses a state in which any `iid` is both pending and fired.
    restored = l5.restore(l5.snapshot(state))
    require_equal(l5.state_checksum(restored), spec["state_sha256"],
                  "restoring the L5 anchor state did not reproduce its frozen hash")
    require_equal(len(l5.pending_iids(restored)), spec["pending"],
                  "the pending set did not survive the snapshot round-trip")
    require_equal(len(l5.fired_iids(restored)), spec["fired"],
                  "the fired ledger did not survive the snapshot round-trip")
    require_equal(restored.forgetting.count, spec["forgotten"],
                  "the forgetting record did not survive the snapshot round-trip")


def trial_older_anchors_are_untouched_by_l5():
    # A guard, stated as a trial: the older anchor files must still exist and
    # still record replay at their own caps. We do not score them here (that is
    # `anchors/t_l1.py` … `t_l4.py`); we assert their identity is unchanged, so a
    # future edit that folded L5 into them would be caught.
    for name, layer in (("l1.json", 1), ("l2.json", 2), ("l3.json", 3),
                        ("l4.json", 4)):
        with open(os.path.join(_HERE, name), "r", encoding="utf-8") as fh:
            older = json.load(fh)
        require_equal(older["layer"], layer,
                      "anchors/%s layer changed — older anchors stay frozen"
                      % (name,))
        require("prospection" not in older,
                "anchors/%s gained a prospection entry — those engines have no "
                "construct that watches future writes, and Layer 5 does not "
                "reach back" % (name,))
    with open(os.path.join(_HERE, "l4.json"), "r", encoding="utf-8") as fh:
        l4_anchor = json.load(fh)
    require("consolidated" in l4_anchor,
            "anchors/l4.json lost its consolidated entry — Layer 4's own claim "
            "is anchored there and Layer 5 must not have displaced it")

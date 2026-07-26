"""anchors/ — the Layer-4 frozen anchors (BOUNDARY.md §6 anchors, §9).

Captures the exact canonical state of a fresh **consolidation** engine
(`layer_cap = 4`) after replaying the frozen corpora — the interval table, the
key atlas, the derived rows, the handle index and the aggregated forgetting
record included. The expected hashes live in `trials/anchors/l4.json` and are
**frozen**: once set (this ASCEND session) an anchor's expected output never
changes.

Two kinds of entry, because this layer has two things worth pinning:

  * **`corpora`** — the base corpora at `DEFAULT_BUDGET`, where nothing is
    evicted. These anchor the *derivation* itself: the facet map, the
    invertibility rule, the row codec's shapes and field order, the key-major
    nesting. A drift in any of them moves a hash even though no episode was ever
    dropped.
  * **`consolidated`** — `l4stream` replayed at the gate's own 43 300-cell cap, so
    the anchor covers what this layer is actually for: the exact state after
    18 788 demotions and 714 losses. A drift in the demotion order, the
    importance law over rows, the shedding rule or the atlas's ambiguity marking
    moves this hash even when every score still clears the gate. That is the
    point of an anchor — scores can survive a behavioural change; bytes cannot.

These are NEW anchors, deliberately separate from `anchors/l1.json`,
`anchors/l2.json` and `anchors/l3.json`. Those record replay under
`make_engine(layer_cap = 1..3)` through their own engines and stay byte-identical
forever; the capped constructor is what keeps old anchors eternal, and each new
layer records its own (§9.2).
"""

import json
import os

from _harness import require, require_equal
from adapters import l4
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen
from corpora.l4stream import generator as l4stream_gen

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANCHOR_PATH = os.path.join(_HERE, "l4.json")

_GENERATORS = {
    "sessions": sessions_gen,
    "murk": murk_gen,
    "l4stream": l4stream_gen,
}


def _load_anchors():
    with open(_ANCHOR_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


_REPLAYS = {}


def _replay_cap4(gen, seed, n, budget_cap=None):
    key = (gen.__name__, seed, n, budget_cap)
    if key not in _REPLAYS:
        state = l4.empty() if budget_cap is None else l4.make_engine(4, budget_cap)
        for payload in gen.generate(seed, n):
            state, t = l4.ingest(state, payload)
            require(t is not None,
                    "anchor replay hit a hard refusal — cap too small?")
        _REPLAYS[key] = state
    return _REPLAYS[key]


def _shape(state):
    return {
        "next_t": state.next_t,
        "episodes": l4.retained(state),
        "demotions": state.demotions,
        "forgotten": state.forgetting.count,
        "occupancy": state.occupancy,
        "keys": len(state.chains),
        "pairs": sum(len(per) for per in state.chains.values()),
        "assertions": sum(len(chain) for per in state.chains.values()
                          for chain in per.values()),
        "index_atoms": len(state.index),
    }


def trial_l4_construction_constants_match_the_anchor_assumption():
    anchors = _load_anchors()
    require_equal(l4.DEFAULT_BUDGET, anchors["default_budget"],
                  "L4 DEFAULT_BUDGET drifted from the frozen anchor assumption")
    require_equal(sorted(l4.ASSERTION_FORMS), anchors["assertion_kinds"],
                  "the declared assertion facet gained or lost a grammar kind — "
                  "every chain in every anchor depends on that reading")


def trial_l4_frozen_corpus_state_hashes_are_unchanged():
    anchors = _load_anchors()
    for name, spec in sorted(anchors["corpora"].items()):
        gen = _GENERATORS[name]
        require_equal(spec["seed"], gen.SEED,
                      "%s: anchor seed != generator SEED" % (name,))
        state = _replay_cap4(gen, spec["seed"], spec["n"])
        got = _shape(state)
        for field, want in sorted(got.items()):
            require_equal(want, spec[field],
                          "%s: %s drifted from the L4 anchor" % (name, field))
        require_equal(state.forgetting.count, 0,
                      "%s: an event was forgotten where the anchor records none "
                      "— DEFAULT_BUDGET is no longer generous" % (name,))
        require_equal(len(state.demotable) + len(state.kept), spec["shapes"],
                      "%s: the derived row-shape count drifted" % (name,))
        require_equal(l4.state_checksum(state), spec["state_sha256"],
                      "%s: canonical-state hash drifted from the frozen L4 anchor"
                      % (name,))


def trial_l4_consolidated_state_hash_is_unchanged():
    """The anchor that pins **consolidation** itself, not merely derivation."""
    anchors = _load_anchors()
    spec = anchors["consolidated"]["l4stream_at_the_gate"]
    require_equal(spec["seed"], l4stream_gen.SEED,
                  "anchor seed != generator SEED")
    state = _replay_cap4(l4stream_gen, spec["seed"], spec["n"],
                         spec["budget_cap"])

    got = _shape(state)
    for field, want in sorted(got.items()):
        require_equal(want, spec[field],
                      "%s drifted from the L4 consolidation anchor" % (field,))
    require(state.occupancy <= spec["budget_cap"],
            "the anchored state is over its own cap (%d > %d)"
            % (state.occupancy, spec["budget_cap"]))
    require_equal(len(state.damaged), spec["damaged"],
                  "the shed-chain count drifted from the anchor")
    require_equal(state.forgetting.width, spec["forget_width"],
                  "the forgetting record's coarsened width drifted")
    require_equal(len(state.forgetting.buckets), spec["forget_buckets"],
                  "the forgetting record's bucket count drifted")
    require_equal(l4.covers_from(state), spec["covers_from"],
                  "the earliest logical time the table covers drifted — nothing "
                  "is shed on this corpus, so it must still be 0")
    require_equal(l4.state_checksum(state), spec["state_sha256"],
                  "the consolidated canonical-state hash drifted from the frozen "
                  "L4 anchor — the demotion order, the importance law over rows, "
                  "the shedding rule or the atlas has changed behaviour")


def trial_l4_anchor_state_snapshot_round_trips_schemas_included():
    anchors = _load_anchors()
    spec = anchors["consolidated"]["l4stream_at_the_gate"]
    state = _replay_cap4(l4stream_gen, spec["seed"], spec["n"],
                         spec["budget_cap"])
    # restore validates the checksum, rederives the handle index from the
    # retained episodes, and re-accounts occupancy from the state alone; a clean
    # round-trip must reproduce the exact frozen hash.
    restored = l4.restore(l4.snapshot(state))
    require_equal(l4.state_checksum(restored), spec["state_sha256"],
                  "restoring the L4 anchor state did not reproduce its frozen hash")
    require_equal(restored.demotions, spec["demotions"],
                  "the demotion count did not survive the snapshot round-trip")
    require_equal(restored.forgetting.count, spec["forgotten"],
                  "the forgetting record did not survive the snapshot round-trip")


def trial_older_anchors_are_untouched_by_l4():
    # A guard, stated as a trial: the older anchor files must still exist and
    # still record replay at their own caps. We do not score them here (that is
    # `anchors/t_l1.py`, `t_l2.py` and `t_l3.py`); we assert their identity is
    # unchanged, so a future edit that folded L4 into them would be caught.
    for name, layer in (("l1.json", 1), ("l2.json", 2), ("l3.json", 3)):
        with open(os.path.join(_HERE, name), "r", encoding="utf-8") as fh:
            older = json.load(fh)
        require_equal(older["layer"], layer,
                      "anchors/%s layer changed — older anchors stay frozen"
                      % (name,))
        require("consolidated" not in older,
                "anchors/%s gained a consolidation entry — those engines do not "
                "consolidate, and Layer 4 does not reach back" % (name,))
    with open(os.path.join(_HERE, "l3.json"), "r", encoding="utf-8") as fh:
        l3_anchor = json.load(fh)
    require("pressure" in l3_anchor,
            "anchors/l3.json lost its post-eviction entry — Layer 3's own claim "
            "is anchored there and Layer 4 must not have displaced it")

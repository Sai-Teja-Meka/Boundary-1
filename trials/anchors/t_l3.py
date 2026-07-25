"""anchors/ — the Layer-3 frozen anchors (BOUNDARY.md §6 anchors, §9).

Captures the exact canonical state of a fresh **forgetting** engine
(`layer_cap = 3`) after replaying the frozen corpora — the handle index and the
aggregated forgetting record included. The expected hashes live in
`trials/anchors/l3.json` and are **frozen**: once set (this ASCEND session) an
anchor's expected output never changes.

Two kinds of entry, because this layer has two things worth pinning:

  * **`corpora`** — the base corpora at `DEFAULT_BUDGET`, where nothing is
    evicted. These anchor Layer-3 *retention* and its cheaper handle index: a
    drift in the handle precedence, the type-tagged token form, or the cost model
    moves a hash.
  * **`pressure`** — `l3streamb` replayed at the gate's own 11 000-unit cap, so
    the anchor covers what this layer is actually for: the exact post-eviction
    state after 9 086 evictions. A drift in the importance law, the eviction order,
    the tie-break, or the forgetting record's coarsening moves this hash even when
    every score still clears the gate. That is the point of an anchor — scores can
    survive a behavioural change; bytes cannot.

These are NEW anchors, deliberately separate from `anchors/l1.json` and
`anchors/l2.json`. Those record replay under `make_engine(layer_cap = 1)` and
`make_engine(layer_cap = 2)` through their own engines and stay byte-identical
forever; the capped constructor is what keeps old anchors eternal, and each new
layer records its own (§9.2).
"""

import json
import os

from _harness import require, require_equal
from adapters import l3
from corpora.chronicle import generator as chronicle_gen
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen
from corpora.l3streamb import generator as streamb_gen

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANCHOR_PATH = os.path.join(_HERE, "l3.json")

_GENERATORS = {
    "chronicle": chronicle_gen,
    "sessions": sessions_gen,
    "murk": murk_gen,
}


def _load_anchors():
    with open(_ANCHOR_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _replay_cap3(gen, seed, n, budget_cap=None):
    state = l3.empty() if budget_cap is None else l3.make_engine(3, budget_cap)
    for payload in gen.generate(seed, n):
        state, t = l3.ingest(state, payload)
        require(t is not None, "anchor replay hit a hard refusal — cap too small?")
    return state


def trial_l3_construction_constants_match_the_anchor_assumption():
    anchors = _load_anchors()
    require_equal(l3.DEFAULT_BUDGET, anchors["default_budget"],
                  "L3 DEFAULT_BUDGET drifted from the frozen anchor assumption")
    require_equal(list(l3.HANDLE_FIELDS), anchors["handle_fields"],
                  "the handle-field precedence drifted from the frozen anchor "
                  "assumption — every posting in every anchor depends on it")
    require_equal(l3.FORGET_BUCKETS, anchors["forget_buckets"],
                  "FORGET_BUCKETS drifted from the frozen anchor assumption")
    require_equal(l3.FORGET_WIDTH0, anchors["forget_width0"],
                  "FORGET_WIDTH0 drifted from the frozen anchor assumption")


def trial_l3_frozen_corpus_state_hashes_are_unchanged():
    anchors = _load_anchors()
    for name, spec in sorted(anchors["corpora"].items()):
        gen = _GENERATORS[name]
        require_equal(spec["seed"], gen.SEED, "%s: anchor seed != generator SEED" % (name,))
        state = _replay_cap3(gen, spec["seed"], spec["n"])
        require_equal(state.next_t, spec["next_t"], "%s: next_t drifted" % (name,))
        require_equal(l3.retained(state), spec["retained"],
                      "%s: retained count drifted from the L3 anchor" % (name,))
        require_equal(state.forgetting.count, spec["evicted"],
                      "%s: an eviction happened where the anchor records none — "
                      "DEFAULT_BUDGET is no longer generous" % (name,))
        require_equal(state.occupancy, spec["occupancy"],
                      "%s: occupancy (events + handle index + record) drifted"
                      % (name,))
        require_equal(len(state.index), spec["index_atoms"],
                      "%s: handle-index atom count drifted from the L3 anchor"
                      % (name,))
        require_equal(l3.state_checksum(state), spec["state_sha256"],
                      "%s: canonical-state hash drifted from the frozen L3 anchor"
                      % (name,))


def trial_l3_post_eviction_state_hash_is_unchanged():
    """The anchor that pins **forgetting** itself, not merely retention."""
    anchors = _load_anchors()
    spec = anchors["pressure"]["l3streamb_under_pressure"]
    require_equal(spec["seed"], streamb_gen.SEED, "anchor seed != generator SEED")
    state = _replay_cap3(streamb_gen, spec["seed"], spec["n"], spec["budget_cap"])

    require_equal(state.next_t, spec["next_t"], "next_t drifted from the L3 anchor")
    require_equal(l3.retained(state), spec["retained"],
                  "the retained-item count after eviction drifted from the anchor")
    require_equal(state.occupancy, spec["occupancy"], "post-eviction occupancy drifted")
    require(state.occupancy <= spec["budget_cap"],
            "the anchored state is over its own cap (%d > %d)"
            % (state.occupancy, spec["budget_cap"]))
    require_equal(len(state.index), spec["index_atoms"], "index atom count drifted")
    require_equal(state.forgetting.count, spec["evicted"],
                  "the number of evictions drifted from the anchor")
    require_equal(state.forgetting.mass, spec["evicted_mass"],
                  "the evicted mass drifted from the anchor")
    require_equal(state.forgetting.width, spec["forget_width"],
                  "the forgetting record's coarsened width drifted from the anchor")
    require_equal(len(state.forgetting.buckets), spec["forget_buckets"],
                  "the forgetting record's bucket count drifted from the anchor")
    require_equal(l3.state_checksum(state), spec["state_sha256"],
                  "the post-eviction canonical-state hash drifted from the frozen "
                  "L3 anchor — the importance law, the eviction order, the "
                  "tie-break or the record's coarsening has changed behaviour")


def trial_l3_anchor_state_snapshot_round_trips_record_included():
    anchors = _load_anchors()
    spec = anchors["pressure"]["l3streamb_under_pressure"]
    state = _replay_cap3(streamb_gen, spec["seed"], spec["n"], spec["budget_cap"])
    # restore validates the checksum, rederives the index from the retained
    # records, and re-accounts occupancy; a clean round-trip must reproduce the
    # exact frozen hash.
    restored = l3.restore(l3.snapshot(state))
    require_equal(l3.state_checksum(restored), spec["state_sha256"],
                  "restoring the L3 anchor state did not reproduce its frozen hash")
    require_equal(restored.forgetting.count, spec["evicted"],
                  "the forgetting record did not survive the snapshot round-trip")


def trial_l1_and_l2_anchors_are_untouched_by_l3():
    # A guard, stated as a trial: the older anchor files must still exist and still
    # record replay at their own caps. We do not score them here (that is
    # `anchors/t_l1.py` and `anchors/t_l2.py`); we assert their identity is
    # unchanged, so a future edit that folded L3 into them would be caught.
    with open(os.path.join(_HERE, "l1.json"), "r", encoding="utf-8") as fh:
        l1 = json.load(fh)
    require_equal(l1["layer"], 1, "anchors/l1.json layer changed — L1 anchors must stay frozen")
    require("index_atoms" not in l1["corpora"]["chronicle"],
            "anchors/l1.json gained an index field — L1 replay is index-free and frozen")
    with open(os.path.join(_HERE, "l2.json"), "r", encoding="utf-8") as fh:
        l2 = json.load(fh)
    require_equal(l2["layer"], 2, "anchors/l2.json layer changed — L2 anchors must stay frozen")
    require_equal(l2["minhash_k"], 16,
                  "anchors/l2.json MinHash width changed — L2's index is frozen, "
                  "and Layer 3 declining to build it does not reach back")
    require("pressure" not in l2,
            "anchors/l2.json gained a pressure entry — Layer 2 never evicts, and "
            "its anchors record an engine that refuses instead")

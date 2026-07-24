"""anchors/ — the Layer-2 frozen anchors (BOUNDARY.md §6 anchors, §9).

Captures the exact canonical state of a fresh **recall** engine (`layer_cap = 2`)
after replaying each frozen base corpus — the **index included**. The expected
hashes live in `trials/anchors/l2.json` and are **frozen**: once set (this ASCEND
session) an anchor's expected output never changes.

These are NEW anchors, deliberately separate from `anchors/l1.json`. Building the
associative index changes post-replay state, so L2's replay hashes differ from
L1's — but that does not touch L1's anchors, which record replay under
`make_engine(layer_cap = 1)` (a construction with no index) and stay
byte-identical forever. The capped constructor is what keeps the old anchors
eternal; the new layer records its own. A drift in the index, the atom rules, the
MinHash, the cost model, or the serializer would move an L2 hash and turn the
suite red — exactly the silent-regression guard anchors exist to be.
"""

import json
import os

from _harness import require, require_equal
from adapters import l2
from corpora.chronicle import generator as chronicle_gen
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANCHOR_PATH = os.path.join(_HERE, "l2.json")

_GENERATORS = {
    "chronicle": chronicle_gen,
    "sessions": sessions_gen,
    "murk": murk_gen,
}


def _load_anchors():
    with open(_ANCHOR_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _replay_cap2(gen, seed, n):
    state = l2.empty()   # layer_cap = 2, DEFAULT_BUDGET
    for p in gen.generate(seed, n):
        state, t = l2.ingest(state, p)
        require(t is not None, "anchor replay was refused — DEFAULT_BUDGET too small?")
    return state


def trial_l2_default_budget_and_minhash_match_anchor_assumption():
    anchors = _load_anchors()
    require_equal(l2.DEFAULT_BUDGET, anchors["default_budget"],
                  "L2 DEFAULT_BUDGET drifted from the frozen anchor assumption")
    require_equal(l2.MINHASH_K, anchors["minhash_k"],
                  "MINHASH_K drifted from the frozen anchor assumption")


def trial_l2_frozen_corpus_state_hashes_are_unchanged():
    anchors = _load_anchors()
    for name, spec in sorted(anchors["corpora"].items()):
        gen = _GENERATORS[name]
        require_equal(spec["seed"], gen.SEED, f"{name}: anchor seed != generator SEED")
        state = _replay_cap2(gen, spec["seed"], spec["n"])
        require_equal(state.next_t, spec["next_t"], f"{name}: next_t drifted from the L2 anchor")
        require_equal(state.occupancy, spec["occupancy"],
                      f"{name}: occupancy (payload + index) drifted from the L2 anchor")
        require_equal(len(state.index.postings), spec["index_atoms"],
                      f"{name}: index atom count drifted from the L2 anchor")
        require_equal(l2.state_checksum(state), spec["state_sha256"],
                      f"{name}: canonical-state hash (index included) drifted from the frozen anchor")


def trial_l2_anchor_state_snapshot_round_trips_index_included():
    anchors = _load_anchors()
    spec = anchors["corpora"]["sessions"]
    state = _replay_cap2(sessions_gen, spec["seed"], spec["n"])
    # restore validates the checksum AND rederives the index from the log; a
    # clean round-trip must reproduce the exact frozen hash.
    restored = l2.restore(l2.snapshot(state))
    require_equal(l2.state_checksum(restored), spec["state_sha256"],
                  "restoring the L2 anchor state did not reproduce its frozen hash")


def trial_l1_anchors_are_untouched_by_l2():
    # A guard, stated as a trial: the Layer-1 anchor file must still exist and
    # still record replay under layer_cap=1 (index-free). We do not import the
    # L1 adapter here to score it (that is anchors/t_l1.py's job) — we only
    # assert the frozen file's identity is unchanged in shape, so a future edit
    # that tried to fold L2 into l1.json would be caught.
    with open(os.path.join(_HERE, "l1.json"), "r", encoding="utf-8") as fh:
        l1 = json.load(fh)
    require_equal(l1["layer"], 1, "anchors/l1.json layer changed — L1 anchors must stay frozen")
    require_equal(l1["move"], "FORGE", "anchors/l1.json move changed — L1 anchors must stay frozen")
    require("index_atoms" not in l1["corpora"]["chronicle"],
            "anchors/l1.json gained an index field — L1 replay is index-free and frozen")

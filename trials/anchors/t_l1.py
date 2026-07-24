"""anchors/ — the first frozen anchors of the project (BOUNDARY.md §6 anchors).

Captures the exact canonical state of a fresh full Layer-1 engine after
replaying each frozen Phase-0 corpus. The expected hashes live in
`trials/anchors/l1.json` and are **frozen**: once set (this FORGE session) an
anchor's expected output never changes (§9). A drift in the engine, the cost
model, the serializer, or the snapshot body would move a hash and turn the
suite red — which is exactly the silent-regression guard anchors exist to be.
"""

import json
import os

from _harness import require, require_equal
from adapters import l1
from corpora.chronicle import generator as chronicle_gen
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANCHOR_PATH = os.path.join(_HERE, "l1.json")

_GENERATORS = {
    "chronicle": chronicle_gen,
    "sessions": sessions_gen,
    "murk": murk_gen,
}


def _load_anchors():
    with open(_ANCHOR_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _replay(gen, seed, n):
    state = l1.empty()
    for p in gen.generate(seed, n):
        state, t = l1.ingest(state, p)
        require(t is not None, "anchor replay was refused — DEFAULT_BUDGET too small?")
    return state


def trial_default_budget_matches_anchor_assumption():
    anchors = _load_anchors()
    require_equal(l1.DEFAULT_BUDGET, anchors["default_budget"],
                  "engine DEFAULT_BUDGET drifted from the frozen anchor assumption")


def trial_frozen_corpus_state_hashes_are_unchanged():
    anchors = _load_anchors()
    for name, spec in sorted(anchors["corpora"].items()):
        gen = _GENERATORS[name]
        require_equal(spec["seed"], gen.SEED, f"{name}: anchor seed != generator SEED")
        require_equal(spec["n"], gen.N, f"{name}: anchor n != generator N")
        state = _replay(gen, spec["seed"], spec["n"])
        require_equal(state.next_t, spec["next_t"], f"{name}: next_t drifted from the anchor")
        require_equal(state.occupancy, spec["occupancy"],
                      f"{name}: occupancy drifted from the anchor")
        require_equal(l1.state_checksum(state), spec["state_sha256"],
                      f"{name}: canonical-state hash drifted from the frozen anchor")


def trial_anchor_states_snapshot_round_trip():
    anchors = _load_anchors()
    # The smallest frozen corpus, to keep the extra replay cheap: restoring the
    # anchor state must reproduce its exact canonical hash (snapshot integrity).
    spec = anchors["corpora"]["sessions"]
    state = _replay(sessions_gen, spec["seed"], spec["n"])
    restored = l1.restore(l1.snapshot(state))
    require_equal(l1.state_checksum(restored), spec["state_sha256"],
                  "restoring the anchor state did not reproduce its frozen hash")

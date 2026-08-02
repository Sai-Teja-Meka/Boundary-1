"""anchors/ — the Layer-6 frozen anchors (BOUNDARY.md §6 anchors, §9).

Captures the exact canonical state of a fresh **meta-memory** engine
(`layer_cap = 6`) after replaying the frozen corpora, and — the entry no earlier
layer had — the exact **confidence profile** it emits over the two Layer-6
artifacts. The expected values live in `trials/anchors/l6.json` and are
**frozen**: once set (this `ASCEND` session) an anchor's expected output never
changes.

Two kinds of entry, because this layer has two things worth pinning, and they are
not the same kind of thing:

  * **`corpora`** — `sessions`, `murk` and `l5stream` at `DEFAULT_BUDGET`. What
    they pin is a **negative**: `§5.1 L6` defends `B = 1000` with *"meta-memory
    derives confidence from **existing state** within budget"*, and every shape
    figure recorded here — occupancy, episodes, demotions, forgotten, keys,
    pairs, assertions, index atoms, pending, fired — is **identical to
    `anchors/l5.json`'s own recorded figure for the same corpus**, which
    `trial_the_layer6_state_is_the_layer5_state` asserts by reading the older
    anchor file rather than by restating its numbers. Layer 6 added no cell, no
    structure and no event. Only the `state_sha256` differs, by exactly one atom:
    the recorded `layer_cap`.
  * **`calibration`** — `corpora/l6batteryb` (the artifact `R7` clause 1 binds)
    and `corpora/l6battery` (the ungated diagnostic the same clause demoted),
    each replayed at `DEFAULT_BUDGET` and asked its whole query set through `§7`.
    Recorded: `A`, `n_pos`, `n_neg`, the exact `Fraction` and permille rendering
    of every `§3.4` quantity, the engine's whole confidence vocabulary, and a
    **`trace_sha256`** over the canonical `(qid, status, confidence)` triples.
    That last one is what an anchor is for at this layer: a score can survive a
    changed model — two different confidence assignments can round to the same
    Brier — but the trace cannot. A drift in the declared set-once reading, in
    the tie arithmetic, in the horizon `as-of` prices its evidence at, or in
    which verbs carry a confidence at all moves this hash while every `§5 L6`
    clause still clears its gate.

The two artifacts are recorded side by side deliberately, because together they
are what the fourth substrate kill was **for**. On battery-b the engine measures
`AUROC 976` against a class of 100 errors no reading of the stream can remove; on
the demoted diagnostic it measures **1000**, because there evidence that ranks
also resolves and the engine's ties are exactly its errors. Neither is a gate.
The pair is the demotion's cause, visible on an engine.

These are NEW anchors, deliberately separate from `anchors/l1.json` …
`anchors/l5.json`. Those record replay under `make_engine(layer_cap = 1..5)`
through their own engines and stay byte-identical forever; the capped constructor
is what keeps old anchors eternal, and each new layer records its own (§9.2).
"""

import hashlib
import json
import os
from fractions import Fraction

from _harness import require, require_equal
from adapters import l5, l6
from core.serialize import encode
from core.layers import l5_prospection as l5m
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen
from corpora.l5stream import generator as l5stream_gen

import _l6score

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANCHOR_PATH = os.path.join(_HERE, "l6.json")
_L5_ANCHOR_PATH = os.path.join(_HERE, "l5.json")

_GENERATORS = {
    "sessions": sessions_gen,
    "murk": murk_gen,
    "l5stream": l5stream_gen,
}

# The shape fields a Layer-6 state shares with the Layer-5 state it is built on.
# Every one of them must equal `anchors/l5.json`'s own figure for that corpus:
# this layer holds nothing new, so nothing here may move.
_SHARED_SHAPE = ("next_t", "episodes", "demotions", "forgotten", "occupancy",
                 "keys", "pairs", "assertions", "index_atoms", "pending",
                 "fired")


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


_REPLAYS = {}


def _replay_cap6(name):
    if name not in _REPLAYS:
        gen = _GENERATORS[name]
        spec = _load(_ANCHOR_PATH)["corpora"][name]
        state = l6.make_engine(6, l6.DEFAULT_BUDGET)
        for payload in gen.generate(spec["seed"], spec["n"]):
            state, t = l6.ingest(state, payload)
            require(t is not None,
                    "anchor replay hit a hard refusal — cap too small?")
        _REPLAYS[name] = state
    return _REPLAYS[name]


def _shape(state):
    return {
        "next_t": state.next_t,
        "episodes": l6.retained(state),
        "demotions": state.demotions,
        "forgotten": state.forgetting.count,
        "occupancy": state.occupancy,
        "keys": len(state.chains),
        "pairs": sum(len(per) for per in state.chains.values()),
        "assertions": sum(len(chain) for per in state.chains.values()
                          for chain in per.values()),
        "index_atoms": len(state.index),
        "pending": len(l6.pending_iids(state)),
        "fired": len(l6.fired_iids(state)),
        "ties": len(l6.ties(state)),
    }


_SCORED = {}


def _score(artifact):
    if artifact not in _SCORED:
        b = _l6score.BATTERIES[artifact]()
        state, budget = _l6score.replay(
            l6, lambda cap: l6.make_engine(6, cap), b, l6.DEFAULT_BUDGET)
        rows = _l6score.observe(l6, state, b)
        _SCORED[artifact] = (state, budget, rows,
                             _l6score.score(rows, b), b)
    return _SCORED[artifact]


def _frac(pair):
    return None if pair is None else Fraction(pair[0], pair[1])


# ---- the construction constants ---------------------------------------------

def trial_l6_construction_constants_match_the_anchor_assumption():
    """Everything the anchors below are computed under, pinned before them."""
    anchors = _load(_ANCHOR_PATH)
    require_equal(anchors["layer"], 6, "the L6 anchor file's own layer")
    require_equal(l6.DEFAULT_BUDGET, anchors["default_budget"],
                  "L6 DEFAULT_BUDGET drifted from the frozen anchor assumption")
    require_equal(list(l6.SET_ONCE_KEYS), anchors["set_once_keys"],
                  "the declared set-once reading drifted — it is the half of "
                  "this layer's evidence that is a reading of a frozen grammar "
                  "and not a fold over the stream, so a drift here moves every "
                  "confidence in every trace below")
    require_equal((l6.CERTAIN, l6.NO_ANSWER),
                  (anchors["certain"], anchors["no_answer"]),
                  "the two constant confidences drifted")
    require_equal(l6.permille(Fraction(1, 2)), 500,
                  "the tie's own arithmetic is permille(1/2) = 500 (§3.5)")


# ---- the corpora, and the negative they pin ---------------------------------

def trial_l6_frozen_corpus_state_hashes_are_unchanged():
    anchors = _load(_ANCHOR_PATH)
    for name, spec in sorted(anchors["corpora"].items()):
        gen = _GENERATORS[name]
        require_equal(spec["seed"], gen.SEED,
                      "%s: anchor seed != generator SEED" % (name,))
        state = _replay_cap6(name)
        got = _shape(state)
        for field, want in sorted(got.items()):
            require_equal(want, spec[field],
                          "%s: %s drifted from the L6 anchor" % (name, field))
        require_equal(l6.state_checksum(state), spec["state_sha256"],
                      "%s: canonical-state hash drifted from the frozen L6 anchor"
                      % (name,))


def trial_the_layer6_state_is_the_layer5_state():
    """`§5.1 L6`'s *"from existing state"*, pinned against the OLDER anchor file.

    The strongest form available, and it costs nothing to state: every shared
    shape figure this anchor records must equal the figure `anchors/l5.json`
    already recorded for the same corpus at the same cap. Those numbers were
    frozen one layer ago and this session did not write them, so a Layer-6 engine
    that grew a structure would go red here against a file it cannot edit (§9.2).

    And the canonical bodies are compared branch by branch: they differ in
    exactly one, the recorded `layer_cap`, which is the cap and not the content.
    """
    anchors = _load(_ANCHOR_PATH)
    older = _load(_L5_ANCHOR_PATH)
    for name, spec in sorted(anchors["corpora"].items()):
        was = older["corpora"][name]
        for field in _SHARED_SHAPE:
            require_equal(spec[field], was[field],
                          "%s: the L6 anchor records %s = %r where the FROZEN "
                          "L5 anchor records %r — Layer 6 derives confidence "
                          "from existing state (§5.1 L6) and may not move a cell"
                          % (name, field, spec[field], was[field]))
        require(spec["state_sha256"] != was["state_sha256"],
                "%s: the L6 and L5 state hashes are equal, which cannot be — the "
                "recorded layer_cap is part of the body" % (name,))

        state6 = _replay_cap6(name)
        state5 = l5.make_engine(5, l5.DEFAULT_BUDGET)
        for payload in _GENERATORS[name].generate(spec["seed"], spec["n"]):
            state5, t = l5.ingest(state5, payload)
            require(t is not None, "the Layer-5 comparison replay was refused")
        body6 = l5m._body(state6)
        body5 = l5m._body(state5)
        differing = sorted(k for k in body6 if body6[k] != body5[k])
        require_equal(differing, ["layer_cap"],
                      "%s: the Layer-6 body differs from the Layer-5 body in %r "
                      "— Layer 6 changed what the engine SAYS, not what it holds"
                      % (name, differing))
        require_equal(l5.state_checksum(state5), was["state_sha256"],
                      "%s: the Layer-5 comparison replay did not reproduce the "
                      "frozen L5 anchor hash, so the comparison above was "
                      "against the wrong state" % (name,))


def trial_l6_anchor_state_snapshot_round_trips_the_model_included():
    """`§5 L1`'s byte-identical round trip, at cap 6, with the model inside it.

    There is no separate model to serialize — that is the layer — so what this
    asserts is that the restored state states the **same numbers**, sampled on
    the corpus that actually holds ties.
    """
    anchors = _load(_ANCHOR_PATH)
    state = _replay_cap6("murk")
    snap = l6.snapshot(state)
    restored = l6.restore(snap)
    require_equal(l6.snapshot(restored), snap,
                  "the Layer-6 snapshot is not byte-identical on round trip")
    require_equal(l6.state_checksum(restored),
                  anchors["corpora"]["murk"]["state_sha256"],
                  "restoring the L6 anchor state did not reproduce its hash")
    require_equal(l6.ties(restored), l6.ties(state),
                  "the ties the engine reads did not survive the round trip")
    key = l6.SET_ONCE_KEYS[0]
    sampled = 0
    for entity, _key, _d in l6.ties(state)[:16]:
        q = {"op": "current", "entity": entity, "key": key}
        require_equal(l6.query(restored, q), l6.query(state, q),
                      "the restored state answered or RATED entity %d "
                      "differently — the Answer carries `confidence` (§7.2) and "
                      "from Layer 6 it is scored" % (entity,))
        sampled += 1
    require(sampled > 0,
            "murk must carry ties or this trial samples nothing")


# ---- the calibration profile, which is what an anchor is for at this layer ---

def trial_l6_calibration_profiles_are_unchanged():
    """Both artifacts' `§3.4` figures and the emitted confidence TRACE.

    A score can survive a changed model; a trace cannot. Two different confidence
    assignments can round to the same Brier, so the exact `Fraction`s are pinned
    beside the permille renderings **and** a SHA-256 over the canonical
    `(qid, status, confidence)` triples is pinned beside both.
    """
    anchors = _load(_ANCHOR_PATH)
    for artifact, spec in sorted(anchors["calibration"].items()):
        _state, budget, rows, r, b = _score(artifact)

        require_equal(b["n_events"], spec["n_events"],
                      "%s: the artifact's own stream length drifted" % (artifact,))
        for field in ("N", "A", "n_pos", "n_neg", "wrong", "fabricated",
                      "abstentions"):
            require_equal(r[field], spec[field],
                          "%s: %s drifted from the L6 anchor" % (artifact, field))
        require_equal(list(r["confidences"]), spec["confidences"],
                      "%s: the engine's confidence vocabulary drifted"
                      % (artifact,))
        for field in ("brier", "ece", "auroc", "F_core", "F_all"):
            require_equal(r[field], _frac(spec[field]),
                          "%s: the exact %s drifted from the L6 anchor"
                          % (artifact, field))
            got = None if r[field] is None else _l6score.permille(r[field])
            require_equal(got, spec[field + "_permille"],
                          "%s: the permille rendering of %s drifted"
                          % (artifact, field))
        require_equal(budget["occupancy"], spec["occupancy"],
                      "%s: occupancy drifted" % (artifact,))
        require_equal(budget["next_t"], spec["next_t"],
                      "%s: the clock drifted — neither artifact carries an "
                      "intention, so one ingest is one `t` (R6 clause 2's "
                      "f = 0 case)" % (artifact,))
        require_equal(budget["refused"], 0,
                      "%s: a write was refused at DEFAULT_BUDGET" % (artifact,))

        trace = [[row["qid"], row["status"], row["confidence"]] for row in rows]
        require_equal(hashlib.sha256(encode(trace)).hexdigest(),
                      spec["trace_sha256"],
                      "%s: the emitted confidence TRACE drifted from the frozen "
                      "L6 anchor while the scores above did not — two different "
                      "models can round to one Brier, and this is the hash that "
                      "cannot" % (artifact,))


def trial_the_two_artifacts_record_the_demotions_cause_on_an_engine():
    """Why `R7` clause 1 demoted one of these and bound the other, as two numbers.

    Round 1's `corpora/l6battery` measured its own limit and recorded it: *"on
    murk, **evidence that ranks also resolves**"*, because `§8.7` injects every
    defect by visible construction. On an engine that is now a measurement rather
    than a finding about policies — the ties the engine reads there are **exactly**
    its errors, so its `AUROC` is **1000**, the ceiling, and a gate bound there
    would have been measuring an artifact's transparency rather than a model.

    On `corpora/l6batteryb` the same model measures `976`, and it cannot do
    better: the missing `1/42` is exactly the withheld coin (`ATTAINABILITY-B.md
    §3`). **Neither number is a gate here.** The pair is the demotion's cause,
    and this is where a later session finds it without re-deriving it.
    """
    anchors = _load(_ANCHOR_PATH)
    demoted = anchors["calibration"]["l6battery"]
    binding = anchors["calibration"]["l6batteryb"]

    require_equal(demoted["auroc_permille"], 1000,
                  "the demoted diagnostic no longer exhibits its own cause: on "
                  "murk the engine's ties are exactly its errors")
    require_equal(demoted["ties"], demoted["n_neg"],
                  "the tie set and the error set are the same set on murk — "
                  "%d against %d" % (demoted["ties"], demoted["n_neg"]))
    require(binding["auroc_permille"] < demoted["auroc_permille"],
            "the binding artifact must cost the model something the diagnostic "
            "does not: %d against %d"
            % (binding["auroc_permille"], demoted["auroc_permille"]))
    require_equal(binding["ties"], 2 * binding["n_neg"],
                  "on battery-b the engine reads a tie on BOTH members of every "
                  "mirror pair and is wrong on exactly one — %d ties, %d errors"
                  % (binding["ties"], binding["n_neg"]))
    require_equal(_frac(binding["auroc"]), Fraction(41, 42),
                  "the withheld coin is worth exactly 1/42 of AUROC and the "
                  "anchor is where that stops being an argument")


def trial_older_anchors_are_untouched_by_l6():
    # A guard, stated as a trial: the older anchor files must still exist and
    # still record replay at their own caps. We do not score them here (that is
    # `anchors/t_l1.py` … `t_l5.py`); we assert their identity is unchanged, so a
    # future edit that folded L6 into them would be caught.
    for name, layer in (("l1.json", 1), ("l2.json", 2), ("l3.json", 3),
                        ("l4.json", 4), ("l5.json", 5)):
        older = _load(os.path.join(_HERE, name))
        require_equal(older["layer"], layer,
                      "anchors/%s layer changed — older anchors stay frozen"
                      % (name,))
        require("calibration" not in older,
                "anchors/%s gained a calibration entry — §3.4 is DORMANT below "
                "Layer 6 and those engines emit a confidence nobody scores; "
                "Layer 6 does not reach back" % (name,))
    require("prospection" in _load(os.path.join(_HERE, "l5.json")),
            "anchors/l5.json lost its prospection entry — Layer 5's own claim is "
            "anchored there and Layer 6 must not have displaced it")
    require("consolidated" in _load(os.path.join(_HERE, "l4.json")),
            "anchors/l4.json lost its consolidated entry")

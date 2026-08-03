"""anchors/ — the Layer-7 frozen anchors (BOUNDARY.md §6 anchors, §9).

Captures the exact canonical state of a fresh **generation** engine
(`layer_cap = 7`) after replaying the frozen corpora, and — the entries no
earlier layer had — the exact **lineage and tag trace** it emits over
`corpora/l7compose`, before and after `§6`'s three-generation ladder. The
expected values live in `trials/anchors/l7.json` and are **frozen**: once set
(this `ASCEND` session) an anchor's expected output never changes.

Two kinds of entry, and the second is what an anchor is **for** at this layer.

  * **`corpora`** — `sessions`, `murk` and `l5stream` at `DEFAULT_BUDGET`. What
    they pin is a **negative**, in the shape `anchors/l6.json` established: every
    shape figure recorded here is **identical to `anchors/l6.json`'s own recorded
    figure for the same corpus**, which
    `trial_a_composition_free_stream_behaves_exactly_as_cap_6` asserts by reading
    the older anchor file rather than by restating its numbers. None of those
    three streams carries a `profile` payload, so the ledger is empty on all of
    them and costs nothing — Layer 7 adds a field, and where there is nothing to
    record it adds no cell. Only the `state_sha256` differs, in exactly two
    branches: the recorded `layer_cap`, and an **empty** `lineage`.

  * **`generation`** — `corpora/l7compose`, the artifact `R8` clause 1 binds both
    sides of the Layer-7 gate to, replayed at `DEFAULT_BUDGET` and asked its whole
    2 200-query set through `§7`. Recorded: `A` / `n_pos` / `n_neg`, the exact
    `Fraction` and permille rendering of all three capability ratios and of every
    `§3` measure, the engine's whole confidence vocabulary, the full three-rung
    ladder with the ledger it leaves — **and three hashes**:

    | hash | over | why a score cannot replace it |
    |---|---|---|
    | `trace_sha256` | `(qid, status, lineage, confidence)` | `tagging = 1000` is a ratio; **which** items were called generated is not, and two different taggings of the same count give one ratio |
    | `support_sha256` | `(qid, kind, support, t_asof)` | `R8` clause 5(b) binds relevance to *exactly* the `t`s the rule reads, and a tag that cited a different but equally-sized set would clear every §5 L7 clause |
    | `ladder.state_sha256` | the state after three generations | the ledger is the layer, and its content is not any of the numbers above |

    `anchors/l6.json` began this at Layer 6 — *"a score can survive a changed
    model and a trace cannot"* — and it applies with more force here, because
    what Layer 7 adds is not a number attached to an answer but a **claim about
    where an item came from**, and no aggregate can carry that.

These are NEW anchors, deliberately separate from `anchors/l1.json` …
`anchors/l6.json`. Those record replay under `make_engine(layer_cap = 1..6)`
through their own engines and stay byte-identical forever; the capped constructor
is what keeps old anchors eternal, and each new layer records its own (§9.2).
"""

import hashlib
import json
import os
from fractions import Fraction

from _harness import require, require_equal
from adapters import l6, l7
from core.serialize import encode
from core.layers import l6_meta_memory as l6m
from core.layers import l7_generation as l7m
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen
from corpora.l5stream import generator as l5stream_gen

import _l7score
import _l7tasks

_HERE = os.path.dirname(os.path.abspath(__file__))
_ANCHOR_PATH = os.path.join(_HERE, "l7.json")
_L6_ANCHOR_PATH = os.path.join(_HERE, "l6.json")

_GENERATORS = {
    "sessions": sessions_gen,
    "murk": murk_gen,
    "l5stream": l5stream_gen,
}

# The shape fields a Layer-7 state shares with the Layer-6 state it is built on.
# Every one must equal `anchors/l6.json`'s own figure for that corpus: none of
# these three streams carries a composition, so nothing here may move.
_SHARED_SHAPE = ("next_t", "episodes", "demotions", "forgotten", "occupancy",
                 "keys", "pairs", "assertions", "index_atoms", "pending",
                 "fired", "ties")

ARTIFACT = "l7compose"

_REPLAYS = {}
_SCORED = {}


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _frac(pair):
    return None if pair is None else Fraction(pair[0], pair[1])


def _replay_cap7(name):
    if name not in _REPLAYS:
        gen = _GENERATORS[name]
        spec = _load(_ANCHOR_PATH)["corpora"][name]
        state = l7.make_engine(7, l7.DEFAULT_BUDGET)
        for payload in gen.generate(spec["seed"], spec["n"]):
            state, t = l7.ingest(state, payload)
            require(t is not None,
                    "anchor replay hit a hard refusal — cap too small?")
        _REPLAYS[name] = state
    return _REPLAYS[name]


def _shape(state):
    return {
        "next_t": state.next_t,
        "episodes": l7.retained(state),
        "demotions": state.demotions,
        "forgotten": state.forgetting.count,
        "occupancy": state.occupancy,
        "keys": len(state.chains),
        "pairs": sum(len(per) for per in state.chains.values()),
        "assertions": sum(len(chain) for per in state.chains.values()
                          for chain in per.values()),
        "index_atoms": len(state.index),
        "pending": len(l7.pending_iids(state)),
        "fired": len(l7.fired_iids(state)),
        "ties": len(l7.ties(state)),
        "lineage": len(state.lineage),
        "lineage_cells": l7.lineage_cells(state.lineage),
    }


def _scored():
    if "run" not in _SCORED:
        b = _l7score.battery()
        state, budget = _l7score.replay(
            l7, lambda cap: l7.make_engine(7, cap), b, l7.DEFAULT_BUDGET)
        rows = _l7score.observe(l7, state, b)
        _SCORED["run"] = (state, budget, rows, _l7score.score(rows, b), b)
    return _SCORED["run"]


def _trace(rows):
    return [[row["qid"], row["status"], row["lineage"], row["confidence"]]
            for row in rows]


def _support(rows):
    out = []
    for row in rows:
        tag = row["provenance"]
        out.append([row["qid"],
                    None if tag is None else tag["kind"],
                    None if tag is None else list(tag["support"]),
                    None if tag is None else tag["t_asof"]])
    return out


# ---- the construction constants ---------------------------------------------

def trial_l7_construction_constants_match_the_anchor_assumption():
    """Everything the anchors below are computed under, pinned before them."""
    anchors = _load(_ANCHOR_PATH)
    require_equal(anchors["layer"], 7, "the L7 anchor file's own layer")
    require_equal(l7.DEFAULT_BUDGET, anchors["default_budget"],
                  "L7 DEFAULT_BUDGET drifted from the frozen anchor assumption")
    require_equal(list(l7.HUES), anchors["hues"],
                  "the declared hue vocabulary drifted — it is half of the "
                  "composition reading, and every generated item below is a "
                  "function of it")
    require_equal(list(l7.GRADES), anchors["grades"],
                  "the declared grade vocabulary drifted")
    require_equal(list(l7.PROFILE_FORM), anchors["profile_form"],
                  "the declared item grammar drifted — `validity = 1000` is "
                  "measured against it")
    require_equal(list(l7.LINEAGE_VOCAB), anchors["lineage_vocab"],
                  "R8 clause 4's closed lineage vocabulary drifted")
    require_equal(l7.LINEAGE_ENTRY_CELLS, anchors["lineage_entry_cells"],
                  "the ledger's price under rule P drifted from the figure "
                  "ATTAINABILITY.md §7 states by name")


# ---- the corpora, and the negative they pin ---------------------------------

def trial_l7_frozen_corpus_state_hashes_are_unchanged():
    anchors = _load(_ANCHOR_PATH)
    for name, spec in sorted(anchors["corpora"].items()):
        gen = _GENERATORS[name]
        require_equal(spec["seed"], gen.SEED,
                      "%s: anchor seed != generator SEED" % (name,))
        state = _replay_cap7(name)
        got = _shape(state)
        for field, want in sorted(got.items()):
            require_equal(want, spec[field],
                          "%s: %s drifted from the L7 anchor" % (name, field))
        require_equal(l7.state_checksum(state), spec["state_sha256"],
                      "%s: canonical-state hash drifted from the frozen L7 anchor"
                      % (name,))


def trial_a_composition_free_stream_behaves_exactly_as_cap_6():
    """The zero-cost half of `README-l6 §0`, carried forward and pinned.

    Layer 6 added no field at all. Layer 7 adds one, and Stage B measured why it
    had to (`§7.1` makes `query` pure, so a lineage ledger can only be written by
    `ingest`) — but on a stream that carries no composition there is nothing to
    record, so the ledger is empty and costs nothing. The strongest available
    form of that claim is the one `anchors/l6.json` used, and it costs nothing to
    state: every shared shape figure this anchor records must equal the figure the
    **frozen** `anchors/l6.json` already recorded for the same corpus at the same
    cap. Those numbers were written one layer ago and this session did not write
    them, so a Layer-7 engine that grew a structure, or charged for a ledger it
    never filled, goes red against a file it cannot edit (§9.2).

    And the canonical bodies are compared branch by branch: the Layer-7 body
    carries exactly one branch the Layer-6 body does not, and the only shared
    branch whose value differs is the recorded `layer_cap`, which is the cap and
    not the content.
    """
    anchors = _load(_ANCHOR_PATH)
    older = _load(_L6_ANCHOR_PATH)
    for name, spec in sorted(anchors["corpora"].items()):
        was = older["corpora"][name]
        for field in _SHARED_SHAPE:
            require_equal(spec[field], was[field],
                          "%s: the L7 anchor records %s = %r where the FROZEN "
                          "L6 anchor records %r — a composition-free stream must "
                          "cost a Layer-7 engine exactly what it cost a Layer-6 "
                          "one" % (name, field, spec[field], was[field]))
        require_equal(spec["lineage"], 0,
                      "%s: the ledger is not empty on a stream that carries no "
                      "`profile` payload at all — an entry here is an "
                      "observation the engine has called its own work" % (name,))
        require_equal(spec["lineage_cells"], 0,
                      "%s: an empty ledger must cost no cells (rule P)" % (name,))
        require(spec["state_sha256"] != was["state_sha256"],
                "%s: the L7 and L6 state hashes are equal, which cannot be — the "
                "recorded layer_cap and the (empty) lineage branch are both part "
                "of the body" % (name,))

        state7 = _replay_cap7(name)
        state6 = l6.make_engine(6, l6.DEFAULT_BUDGET)
        for payload in _GENERATORS[name].generate(spec["seed"], spec["n"]):
            state6, t = l6.ingest(state6, payload)
            require(t is not None, "the Layer-6 comparison replay was refused")
        body7 = l7m._body(state7)
        body6 = l6m._body(state6)
        require_equal(sorted(set(body7) - set(body6)), ["lineage"],
                      "%s: the Layer-7 body adds more than the one branch Stage "
                      "B measured to be forced" % (name,))
        require_equal(body7["lineage"], [],
                      "%s: the ledger branch is not empty" % (name,))
        differing = sorted(k for k in body6 if body6[k] != body7[k])
        require_equal(differing, ["layer_cap"],
                      "%s: the Layer-7 body differs from the Layer-6 body in %r "
                      "— everything Layer 7 holds here it holds because Layer 6 "
                      "did" % (name, differing))
        require_equal(l6.state_checksum(state6), was["state_sha256"],
                      "%s: the Layer-6 comparison replay did not reproduce the "
                      "frozen L6 anchor hash, so the comparison above was "
                      "against the wrong state" % (name,))


def trial_l7_anchor_state_snapshot_round_trips_the_ledger_included():
    """`§5 L1`'s byte-identical round trip, at cap 7, with the ledger inside it.

    Sampled on the artifact that actually holds a ledger, and after the ladder
    has filled it — a round trip over a state whose ledger is empty would be a
    round trip of the Layer-6 state wearing a Layer-7 envelope.
    """
    anchors = _load(_ANCHOR_PATH)["generation"][ARTIFACT]
    state, _budget, _rows, _r, b = _scored()
    after, _rungs, _canon = _l7score.promotion_ladder(l7, state, b)

    snap = l7.snapshot(after)
    restored = l7.restore(snap)
    require_equal(l7.snapshot(restored), snap,
                  "the Layer-7 snapshot is not byte-identical on round trip")
    require_equal(l7.state_checksum(restored), anchors["ladder"]["state_sha256"],
                  "restoring the post-ladder anchor state did not reproduce its "
                  "hash — a state that answered identically but had forgotten "
                  "WHICH items were its own would pass every §5 L7 ratio and "
                  "fail `promotion = 0` on the next rung")
    require_equal(restored.lineage, after.lineage,
                  "the lineage ledger did not survive serialization")

    sampled = 0
    for rec in b["records"]:
        if rec["declared"] != "G" or rec.get("depth") != 1:
            continue
        require_equal(l7.query(restored, rec["q"]), l7.query(after, rec["q"]),
                      "qid %d: the restored state answered or TAGGED differently"
                      % (rec["qid"],))
        sampled += 1
        if sampled >= 16:
            break
    require(sampled > 0, "the ladder must leave generation-required cues to ask")


# ---- the generation profile, which is what an anchor is for at this layer ----

def trial_l7_generation_profile_and_lineage_traces_are_unchanged():
    """`corpora/l7compose`'s figures, and the two hashes a score cannot replace.

    `tagging = 1000` says *how many* of the declared class were tagged. It does
    not say **which**, and two different taggings of the same count give one
    ratio. `R8` clause 5(b)'s relevance check says a generated answer's support
    must be exactly the `t`s the rule read — and a tag citing a different set of
    the same size clears every `§5 L7` clause. So the trace and the support are
    hashed beside the scores, in the shape `anchors/l6.json` established for the
    confidence trace one layer down.
    """
    spec = _load(_ANCHOR_PATH)["generation"][ARTIFACT]
    state, budget, rows, r, b = _scored()

    require_equal(b["n_events"], spec["n_events"],
                  "the artifact's own stream length drifted")
    for field in ("N", "A", "n_pos", "n_neg", "wrong", "fabricated",
                  "abstentions", "tagged_generated", "novel_items",
                  "valid_items", "tagging_denominator", "untagged_generations"):
        require_equal(r[field], spec[field],
                      "%s drifted from the L7 anchor" % (field,))
    for field in ("validity", "novelty", "tagging", "tagging_all",
                  "conjunction", "F_core", "F_all", "ece", "brier", "auroc"):
        require_equal(r[field], _frac(spec[field]),
                      "the exact %s drifted from the L7 anchor" % (field,))
    for field in ("validity", "novelty", "tagging", "conjunction",
                  "F_core", "F_all", "ece"):
        require_equal(_l7score.permille(r[field]), spec[field + "_permille"],
                      "the permille rendering of %s drifted" % (field,))
    require_equal(list(r["confidences"]), spec["confidences"],
                  "the engine's confidence vocabulary on ANSWERS drifted — "
                  "README-l6 §4's CERTAIN-by-fall-through residual is OPEN and "
                  "not closed, and this artifact cannot exercise it, so 1000 is "
                  "what a correct deterministic composer states and a second "
                  "value here is a change nobody measured")
    require_equal(budget["occupancy"], spec["occupancy"], "occupancy drifted")
    require_equal(budget["next_t"], spec["next_t"],
                  "the clock drifted — a generation is a `query` answer and not "
                  "an event, so nothing the engine composes may advance it "
                  "(R8 clause 2)")
    require_equal(budget["refused"], 0,
                  "a write was refused at DEFAULT_BUDGET")
    require_equal(len(state.lineage), spec["lineage"],
                  "the ledger is not empty after the plain replay: the frozen "
                  "stream carries no generation of this engine's")
    require_equal(l7.state_checksum(state), spec["state_sha256"],
                  "the canonical state hash drifted from the frozen L7 anchor")

    require_equal(hashlib.sha256(encode(_trace(rows))).hexdigest(),
                  spec["trace_sha256"],
                  "the emitted LINEAGE TRACE drifted from the frozen L7 anchor "
                  "while the ratios above did not — `tagging = 1000` is a count "
                  "and this is which items it was a count of")
    require_equal(hashlib.sha256(encode(_support(rows))).hexdigest(),
                  spec["support_sha256"],
                  "the emitted SUPPORT trace drifted while the scores did not — "
                  "R8 clause 5(b) binds relevance to exactly the `t`s the "
                  "declared rule reads, and a tag citing a different set of the "
                  "same size would clear every §5 L7 clause")


def trial_l7_self_pollution_ladder_and_its_ledger_are_unchanged():
    """`§6`'s three generations, and the ledger they leave, pinned exactly.

    The ladder is the one place where `promotion = 0` is actually at risk, and
    the ledger it leaves is the layer's whole new state. Pinning the rungs pins
    the behaviour; pinning the state hash after them pins the content, which no
    rung's number carries.
    """
    spec = _load(_ANCHOR_PATH)["generation"][ARTIFACT]["ladder"]
    state, _budget, _rows, _r, b = _scored()
    after, rungs, _canon = _l7score.promotion_ladder(l7, state, b)

    got = [[rg["depth"], rg["emitted"], rg["promotion"], rg["still_generated"],
            rg["store"]] for rg in rungs]
    require_equal(got, spec["rungs"],
                  "the three-generation ladder drifted from the frozen L7 anchor")
    by_rung = {}
    for rung in after.lineage.values():
        by_rung[rung] = by_rung.get(rung, 0) + 1
    require_equal([[rung, by_rung[rung]] for rung in sorted(by_rung)],
                  spec["ledger"],
                  "the ledger's rung profile drifted — it is the engine's own "
                  "account of what it made, and `ops/l7` checks it against the "
                  "artifact's declared depths")
    require_equal(l7.lineage_cells(after.lineage), spec["ledger_cells"],
                  "the ledger's price under rule P drifted")
    require_equal((after.next_t, after.occupancy),
                  (spec["next_t"], spec["occupancy"]),
                  "the post-ladder clock or occupancy drifted")
    require_equal(l7.state_checksum(after), spec["state_sha256"],
                  "the post-ladder state hash drifted while the rungs did not — "
                  "the ledger is the layer, and its content is not any of the "
                  "numbers above")


# ---- the older anchors ------------------------------------------------------

def trial_older_anchors_are_untouched_by_l7():
    """`§9.2`: an anchor is extended, never edited. The six below are byte-frozen.

    Layer 7 binds `§4.2` forever and adds a field to the state, which is the most
    invasive thing a layer in this ladder has done since Layer 5's two prospection
    tiers — so the assertion that the older files did not move is worth making
    where a reader will look for it.
    """
    for older in ("l1", "l2", "l3", "l4", "l5", "l6"):
        path = os.path.join(_HERE, "%s.json" % (older,))
        require(os.path.exists(path),
                "anchors/%s.json is missing — an anchor is never removed" % (older,))
        spec = _load(path)
        require_equal(spec["layer"], int(older[1:]),
                      "anchors/%s.json no longer records its own layer" % (older,))
    require_equal(_load(_L6_ANCHOR_PATH)["corpora"]["murk"]["occupancy"], 74981,
                  "the frozen L6 murk occupancy moved — the L7 corpora entries "
                  "are asserted equal to it, so an edit there would make this "
                  "layer's negative vacuous")

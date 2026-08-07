"""trials/scorecard.py — the layered scorecard behind `python3 -m trials`.

`trials/run.py` is **the one gate** and stays it: green suite or nothing commits
(§9.3). This module is not a second gate and does not fork the first one. It
reuses run.py's machinery — its `sys.path` bootstrap, its module loader, its
deterministic discovery — and adds one thing the suite does not produce: a
**layered report of one engine**, printed as a table, so that a system can be
graded and read in a single command.

    python3 -m trials --engine ours            # our engine, the full ladder
    python3 -m trials --engine reference       # an external engine, same rows
    python3 -m trials --engine mem0            # a stub: says why it cannot run
    python3 -m trials --list-engines
    python3 -m trials --suite                  # exactly run.py, the real gate

## Where every number on the card comes from

Nothing here re-implements a measure. Each tier calls the **same shared scorer
the ascension trial for that layer calls**, through the same generic interface
(§7):

| tier | replay + score | battery |
|---|---|---|
| L1 | `_l1score` | one `read(t)` per ingested event, three frozen corpora |
| L2 | `_l2score` | the frozen cue tasks (`_l2tasks`) |
| L3 | `_l3score` | both frozen pressure streams (`_l3tasks`) |
| L4 | `_l4score` | the Q1–Q4 battery (`_l4tasks`) on the binding corpus |
| L5 | `_l5score` | the P1/P2 battery (`_l5tasks`) on `corpora/l5stream` |
| L6 | `_l6score` | `corpora/l6batteryb`, with `l6battery` as the demoted diagnostic |
| L7 | `_l7score` | `corpora/l7compose`, with the three-rung promotion ladder |

`_l1score` is the one that did not exist before the first `PACKAGE`, and it is
checked against the frozen Layer-1 ascension trial's own private scorer in
`trials/ops/packaging/t_scorecard.py` rather than trusted.

> **Extended 2026-08-07 (`[L7] [PACKAGE]`).** Tiers 5, 6 and 7 were added when
> the layers they report had been claimed for one, two and three moves and the
> card still stopped at four. Nothing about tiers 1–4 changed: the same scorers,
> the same corpora, the same numbers. Two things did have to be **generalized**,
> and both are readings a ruling already fixed rather than inventions of this
> module:
>
> * **direction.** `_verdict` compared every clause with `>=` and special-cased
>   `GATE_FOOTPRINT`. Layers 5, 6 and 7 bring five more **minimizing** clauses
>   (`dup-fire`, `miss`, `Brier`, `ECE`, `promotion`), so the set is now declared
>   as `MINIMIZING` — which is `R5` clause 2's direction-aware reading applied to
>   a renderer.
> * **`n/a` disqualifies.** A clause whose measured value is *undefined* — an
>   `AUROC` with an empty error class (`R7` clause 3(a)), a Layer-7 capability
>   ratio over an empty denominator (`R8` clause 3(c)) — is **FAILED**, not
>   skipped, and the row records which clause was undefined. A card that printed
>   `n/a` and moved on would be the `AdapterCapabilities` null-exemption
>   `autopsy/writ/ANATOMY.md` convicts WRIT of (`evaluator.ts:545-548`), rebuilt
>   here by accident.
>
> The three new tiers are measured **only for an engine that reaches the layer**
> (`Engine.max_layer >= N`); for one that does not, the row says so rather than
> printing a zero, exactly as the humility rows already did.

**The gates are not typed here.** They are read out of
`laws/t_rulings.py::AUTHORIZED_GATES` — the registry that already binds every
threshold in the suite to a literal `BOUNDARY.md §5` clause or a
`BOUNDARY-RULINGS.md` entry, and whose completeness check forbids a gate
constant anywhere under `trials/` that is not in it. A gate cannot therefore
appear on this scorecard without an authority, and a gate that drifted from §5
would go red in `laws/` before it could be printed here.

## The transfer tier

Below the synthetic tiers the card prints a **transfer tier**: the same
engine, the same scorers, run on `corpora/real-sessions/` — the frozen,
checksummed snapshot of this project's own dogfood store (§8.8). It is reported
**beside** the synthetic scores and never blended into them.

Where the two diverge, the divergence is the finding. It is printed in full,
with the reason, because a benchmark that only published the corpus its engine
was designed against would be the thing this project autopsied other people for
(`autopsy/GAPMAP.md §2`).

## What a verdict means

`PASS` / `FAIL` on a tier is measured against that layer's ratified gate. It is
**not** a claim that the engine has ascended: ascension is claimed by the suite,
in `BOUNDARY.log`, under a human's eye. The scorecard reports; `run.py` gates;
the human decides.
"""

import collections
import os

import run                                   # the bootstrap and the machinery

import _l1score
import _l2score
import _l2tasks
import _l3score
import _l3tasks
import _l4score
import _l4tasks
import _l5score
import _l5tasks
import _l6score
import _l7score

OURS = "ours"

# The layers this card reports, and the corpora each tier is measured on.
LAYERS = (1, 2, 3, 4, 5, 6, 7)

L1_CORPORA = ("chronicle", "sessions", "murk")
L3_BINDING = "l3streamb"
L3_DIAGNOSTIC = "l3stream"
L4_BINDING = "l4stream"
L5_BINDING = "l5stream"
L6_BINDING = "l6batteryb"
L6_DIAGNOSTIC = "l6battery"          # DEMOTED by R7 clause 1; scored, never gated
L7_BINDING = "l7compose"

# `R5` clause 2, applied to a renderer: for a MINIMIZING clause "at or above the
# gate" reads as "at or below the number". Named as a set rather than special-
# cased one constant at a time, because Layers 5–7 brought five more of them and
# the next layer will bring its own.
MINIMIZING = frozenset((
    "GATE_FOOTPRINT",        # §5 L4
    "GATE_DUP_FIRE", "GATE_MISS",            # §5 L5
    "GATE_BRIER", "GATE_ECE",                # §5 L6 (and §5 L7's ECE)
    "GATE_PROMOTION",                        # §5 L7
))

# The declared reduced scope, for a run that must be cheap (the packaging trial
# in the suite, and `--quick` at the command line). It is a *scale*, never a
# different battery: the same scorers on a declared prefix or a smaller corpus,
# exactly as `humility/l4` measures its ceiling at declared prefix scales.
QUICK_L1_CORPORA = ("sessions",)
QUICK_L4_PREFIX = 2000


# ---- the gates, read from the authority registry ----------------------------

def _rulings():
    """`laws/t_rulings.py`, loaded through run.py's own module loader."""
    return run._load_module(os.path.join(run.HERE, "laws", "t_rulings.py"))


def gate_table():
    """`{layer: {"gates": {...}, "ceilings": {...}}}` from `AUTHORIZED_GATES`.

    The registry is keyed by trial file, and the trial files are named by layer
    (`ascension/lN/…`, `humility/lN/…`), so the layer of every authorized gate
    is read off its own path rather than restated here.
    """
    table = collections.OrderedDict(
        (n, {"gates": collections.OrderedDict(),
             "ceilings": collections.OrderedDict()}) for n in LAYERS)
    for rel, const, value, _authorities, _note in _rulings().AUTHORIZED_GATES:
        parts = rel.split("/")
        if len(parts) < 3 or not parts[1].startswith("l"):
            continue
        klass, layer_dir = parts[0], parts[1]
        try:
            layer = int(layer_dir[1:])
        except ValueError:
            continue
        if layer not in table:
            continue
        if klass == "ascension" and const.startswith("GATE_"):
            table[layer]["gates"].setdefault(const, value)
        elif klass == "humility" and const.startswith("CEILING_"):
            table[layer]["ceilings"].setdefault(const, value)
    return table


# ---- engine bindings --------------------------------------------------------

class Engine(object):
    """One engine, as the scorecard needs it: a module per layer, and a `mk`."""

    def __init__(self, name, kind, modules, max_layer, note):
        self.name = name
        self.kind = kind
        self.modules = modules          # {layer: module}
        self.max_layer = max_layer      # the highest layer it claims
        self.note = note

    def module(self, layer):
        return self.modules.get(layer)

    def mk(self, layer):
        """`mk(cap)` for a layer: a fresh state at that layer's capability."""
        module = self.module(layer)
        claim = min(layer, self.max_layer)
        return lambda cap=None: (module.make_engine(claim)
                                 if cap is None
                                 else module.make_engine(claim, cap))


def _ours():
    import importlib
    modules = {}
    for layer in LAYERS:
        modules[layer] = importlib.import_module("adapters.l%d" % layer)
    return Engine(OURS, "ours", modules, max(LAYERS),
                  "this repository's engine, one adapter per layer (§7)")


def _reaches(engine, layer):
    """Is this engine worth measuring at layer `N` at all?

    A tier measured against an engine that does not claim the layer prints a
    zero that says nothing about the engine and something misleading about the
    card. The humility rows have always guarded this way; from Layers 5–7 the
    ascension tiers do too, because their replays are the expensive ones.
    """
    return engine.max_layer >= layer and engine.module(layer) is not None


def _external(name):
    from adapters import external
    module = external.get(name)
    return Engine(name, module.KIND, {layer: module for layer in LAYERS},
                  getattr(module, "MAX_LAYER", 0),
                  module.SYSTEM.get("name", name))


def engine_names():
    from adapters import external
    return [OURS] + external.names()


def load_engine(name):
    """The engine binding for `name`, or `(None, reason)` if it cannot run."""
    if name == OURS:
        return _ours(), None
    from adapters import external
    ok, reason = external.available(name)
    if not ok:
        return None, reason
    return _external(name), None


# ---- the tiers --------------------------------------------------------------

def _verdict(measured, gates):
    """`PASS` iff every gate clause holds, read in its own direction.

    A row measured at a **reduced scale** is never given a PASS/FAIL: the
    ratified gates are bound to whole corpora by R1, R4, R6, R7 and R8, and a
    prefix is a diagnostic, not the gate. Such a row reports `diag` and prints
    its numbers, exactly as the conditionally-skipped ascension trials do.

    Two readings are applied and neither is this module's:

    * `MINIMIZING` clauses are compared `<=` (`R5` clause 2 — *"for a minimizing
      clause 'strictly above' reads as 'strictly better'"*); every other clause
      is compared `>=`, which covers the identities too, since an identity is a
      `>=` against its own maximum.
    * an **undefined** clause FAILS. `R7` clause 3(a) rules `n/a` disqualifying
      for `AUROC` on the instrument-range ground, and `R8` clause 3(c) extends
      the same holding to a capability ratio over an empty denominator. A card
      that dropped the clause instead would be reproducing the null-exemption
      this project published about somebody else.
    """
    if measured.get("gated") is False:
        return "diag"
    undefined = [const for const in gates if measured.get(const) is None]
    if undefined:
        measured.setdefault("undefined", undefined)
        return "FAIL"
    for const, gate in gates.items():
        got = measured[const]
        if const in MINIMIZING:
            if got > gate:
                return "FAIL"
        elif got < gate:
            return "FAIL"
    return "PASS"


def tier_l1(engine, corpora):
    """§5 L1 — exact retention over whole frozen corpora."""
    import importlib
    module = engine.module(1)
    rows = []
    for name in corpora:
        gen = importlib.import_module("corpora.%s.generator" % name)
        payloads = list(gen.generate(gen.SEED, gen.N))
        state, budget, accepted = _l1score.replay(module, engine.mk(1), payloads)
        r = _l1score.score(module, state, accepted)
        rows.append({
            "corpus": name, "n": len(payloads),
            "GATE_F": r["F"], "GATE_C": r["C"], "GATE_B": budget["B"],
            "refused": budget["refused"], "wrong": r["wrong"],
            "round_trip": _l1score.snapshot_round_trips(module, state),
        })
    return rows


def tier_l2(engine):
    """§5 L2 — the frozen cue battery."""
    module = engine.module(2)
    mk = engine.mk(2)
    state = _l2score.ingest_store(module, lambda: mk())
    r = _l2score.score(module, state)
    return [{
        "corpus": "l2 cue tasks", "n": len(_l2tasks.store_payloads()),
        "GATE_CUE_C": r["cue_C"], "GATE_F": r["F"], "GATE_B": r["B"],
        "wrong": r["wrong"], "fabricated": r["fabricated"],
    }]


def tier_l3(engine, streams=(L3_BINDING, L3_DIAGNOSTIC)):
    """§5 L3 — both frozen pressure streams at 10× the budget.

    Only `l3streamb` is gated. **BOUNDARY-RULINGS.md R1** binds the ratified
    Layer-3 gate to it and leaves `l3stream` scored as an ungated diagnostic,
    because on that stream the gate is unreachable by *any* retain-or-drop
    policy — its budget-worth of heaviest items holds 190‰ of the mass against
    an 850‰ gate. The card therefore reports `l3stream`'s numbers beside its own
    arithmetic ceiling and never a verdict, which is the same conditional
    treatment `ascension/l3` gives it in code.
    """
    module = engine.module(3)
    rows = []
    for name in streams:
        ceiling = _l3tasks.attainable_weighted_c_permille(name)
        gated = ceiling >= _rulings_gate("GATE_WEIGHTED_C")
        state, budget = _l3score.replay(module, engine.mk(3), name)
        r = _l3score.score(module, state, name)
        rows.append({
            "corpus": name, "n": len(_l3tasks.stream(name)["targets"]),
            "GATE_WEIGHTED_C": r["weighted_C"],
            "GATE_UNWEIGHTED_C": r["unweighted_C"],
            "GATE_F": r["F"], "GATE_B": budget["B"],
            "F_strict": r["F_strict"], "wrong": r["wrong"],
            "fabricated": r["fabricated"], "refused": budget["refused"],
            "oracle_ceiling": ceiling,
            "binding": name == L3_BINDING, "gated": gated,
        })
    return rows


def _rulings_gate(const, layer=3):
    """One authorized gate value, by name — never a literal typed here."""
    return gate_table()[layer]["gates"][const]


def tier_l4(engine, bundle=None):
    """§5 L4 — the Q1–Q4 battery at the ratified footprint."""
    module = engine.module(4)
    whole = bundle is None
    b = _l4tasks.corpus(L4_BINDING) if whole else bundle
    state, budget = _l4score.replay(module, engine.mk(4), b)
    r = _l4score.score(module, state, b)
    return [{
        "corpus": b["name"] if whole else "%s[:%d]" % (b["name"], b["n"]),
        "n": b["n"],
        "GATE_FOOTPRINT": r["footprint"], "GATE_C": r["C"],
        "GATE_RECONSTRUCTION_F": r["F"], "GATE_B": budget["B"],
        "F_corruption": r["F_corruption"], "wrong": r["reconstruction_wrong"],
        "fabricated": r["fabricated"], "occupancy": r["occupancy"],
        "raw_cells": r["raw_cells"],
        "binding": whole, "gated": whole,
    }]


def tier_l5(engine):
    """§5 L5 — the P1/P2 battery on `corpora/l5stream` at `R6` clause 4's cap.

    Four of this gate's six clauses are **identities** (`R5` clause 1), so there
    is no margin to print: the row either states the exact numbers the gate
    names or it does not clear. The engine's own clock audits the firing report
    inside `_l5score.score` (`assert_t_identity`, `R6` clause 2), so a card that
    printed a precision an engine could not account for would raise before it
    could render.
    """
    module = engine.module(5)
    b = _l5tasks.corpus()
    state, budget = _l5score.replay(module, engine.mk(5), b)
    r = _l5score.score(module, state, b)
    return [{
        "corpus": L5_BINDING, "n": len(b["payloads"]),
        "GATE_TRIGGER_PRECISION": r["precision"],
        "GATE_TRIGGER_RECALL": r["recall"],
        "GATE_DUP_FIRE": r["dup_fire"], "GATE_MISS": r["miss"],
        "GATE_F": r["F"], "GATE_B": budget["B"],
        "wrong": r["wrong"], "fabricated": r["fabricated"],
        "refused": budget["refused"],
        "footprint": _l5score.footprint(state, b),
        "next_t": r["next_t"], "emitted": r["emitted"],
        "binding": True, "gated": True,
    }]


def tier_l6(engine, artifacts=(L6_BINDING, L6_DIAGNOSTIC)):
    """§5 L6 — calibration on `corpora/l6batteryb`, with the demoted diagnostic.

    `R7` clause 1 binds both sides of the Layer-6 gate to `l6batteryb` **and
    demotes `l6battery` in the same clause**, so the card scores the second and
    never gives it a verdict — the same conditional treatment `l3stream` gets at
    Layer 3 and `chronicle`/`murk` get at Layer 4. Its row is worth printing for
    the reason the demotion happened: there the same model measures `AUROC 1000`
    because on murk the ties it reads are exactly its errors, and a gate bound
    there would have measured an artifact's transparency rather than a model.
    """
    module = engine.module(6)
    rows = []
    for name in artifacts:
        b = _l6score.BATTERIES[name]()
        state, budget = _l6score.replay(module, engine.mk(6), b,
                                        module.DEFAULT_BUDGET)
        obs = _l6score.observe(module, state, b)
        r = _l6score.score(obs, b)
        rows.append({
            "corpus": name, "n": b["n_events"],
            "GATE_BRIER": _l6score.permille(r["brier"]),
            "GATE_ECE": _l6score.permille(r["ece"]),
            "GATE_AUROC": (None if r["auroc"] is None
                           else _l6score.permille(r["auroc"])),
            "GATE_F": _l6score.permille(r["F_core"]),
            "GATE_B": budget["B"],
            "F_all": _l6score.permille(r["F_all"]),
            "A": r["A"], "n_pos": r["n_pos"], "n_neg": r["n_neg"],
            "wrong": r["wrong"], "fabricated": r["fabricated"],
            "refused": budget["refused"],
            "binding": name == L6_BINDING,
            "gated": name == L6_BINDING,
        })
    return rows


def tier_l7(engine, with_ladder=True):
    """§5 L7 — generation on `corpora/l7compose`, seven clauses and the ladder.

    `promotion = 0` is the one clause no single replay can report: `§5 L7` states
    it **three deep**, and `§6` names the same number a second time in the strain
    class. `_l7score.promotion_ladder` re-ingests the engine's own generations
    rung by rung, which is what the clause means, and the card prints the worst
    rung — a ladder read only at depth 3 could not say where a break occurred.

    The three capability ratios are computed on `R8` clause 3's **bound**
    denominators — `tagging` over the artifact's declared `G` class, `novelty`
    and `validity` over the items the engine tags, every member checked by the
    harness — so an engine that tags nothing reports `n/a` and, under clause
    3(c), FAILS.
    """
    module = engine.module(7)
    b = _l7score.battery()
    state, budget = _l7score.replay(module, engine.mk(7), b,
                                    module.DEFAULT_BUDGET)
    obs = _l7score.observe(module, state, b)
    r = _l7score.score(obs, b)

    promotion = None
    rungs = ()
    if with_ladder:
        _after, rungs, _canon = _l7score.promotion_ladder(module, state, b)
        promotion = max(rung["promotion"] for rung in rungs) if rungs else None

    def pm(key):
        return None if r[key] is None else _l7score.permille(r[key])

    return [{
        "corpus": b["name"], "n": b["n_events"],
        "GATE_VALIDITY": pm("validity"), "GATE_NOVELTY": pm("novelty"),
        "GATE_TAGGING": pm("tagging"), "GATE_PROMOTION": promotion,
        "GATE_F": pm("F_core"), "GATE_B": budget["B"], "GATE_ECE": pm("ece"),
        "F_all": pm("F_all"), "tagging_all": pm("tagging_all"),
        "tagging_denominator": r["tagging_denominator"],
        "A": r["A"], "n_pos": r["n_pos"], "n_neg": r["n_neg"],
        "wrong": r["wrong"], "fabricated": r["fabricated"],
        "refused": budget["refused"],
        "rungs": tuple(rung["promotion"] for rung in rungs),
        "still_generated": tuple(rung["still_generated"] for rung in rungs),
        "binding": True, "gated": True,
    }]


# ---- the humility tier ------------------------------------------------------

# The Layer-4 humility measurement at its declared prefix scales
# (`humility/l4/IMPOSSIBILITY.md §4`). The whole-stream run costs ~663 s — fifteen
# times the entire suite — and was measured ONCE OUT OF SUITE at F = 302; the
# ladder converges on it from below, and the card says which number it is showing.
HUMILITY_L4_PREFIX = 4000
QUICK_HUMILITY_L4_PREFIX = 1000
HUMILITY_L4_WHOLE_STREAM_F = 302        # recorded, out of suite; not measured here


def tier_humility(engine, quick=False):
    """§6 — layer N's own battery against `make_engine(N−1)`, per layer.

    Layer 1 has no humility trial (§5.1 L1: it is the floor, there is no lower
    layer to cap against), so the tier starts at Layer 2. Each row is the capped
    engine's measured score beside the ratified ceiling it must stay under —
    the number that makes the gate above it load-bearing rather than decorative.
    """
    rows = collections.OrderedDict()

    module = engine.module(2)
    if engine.max_layer >= 1:
        state = _l2score.ingest_store(module, lambda: module.make_engine(1))
        r = _l2score.score(module, state)
        rows[2] = {"CEILING_CUE_C": r["cue_C"], "capped": "make_engine(1)",
                   "corpus": "l2 cue tasks"}

    module = engine.module(3)
    if engine.max_layer >= 2:
        state, _b = _l3score.replay(
            module, lambda cap: module.make_engine(2, cap), L3_BINDING)
        r = _l3score.score(module, state, L3_BINDING)
        rows[3] = {"CEILING_WEIGHTED_C": r["weighted_C"],
                   "capped": "make_engine(2)", "corpus": L3_BINDING}

    module = engine.module(4)
    if engine.max_layer >= 3:
        m = QUICK_HUMILITY_L4_PREFIX if quick else HUMILITY_L4_PREFIX
        b = _l4tasks.prefix(L4_BINDING, m)
        state, _b = _l4score.replay(
            module, lambda cap: module.make_engine(3, cap), b)
        r = _l4score.score(module, state, b)
        rows[4] = {"CEILING_RECONSTRUCTION_F": r["F"], "C": r["C"],
                   "capped": "make_engine(3)",
                   "corpus": "%s[:%d]" % (L4_BINDING, m),
                   "whole_stream_recorded": HUMILITY_L4_WHOLE_STREAM_F}

    # L5: the numerator is empty by construction — with no pending set nothing
    # can fire, so the ceiling is loose for a structural reason and not through
    # a corpus's kindness (`humility/l5/IMPOSSIBILITY.md §1`).
    module = engine.module(5)
    if _reaches(engine, 5):
        b = _l5tasks.corpus()
        state, _b = _l5score.replay(
            module, lambda cap: module.make_engine(4, cap), b)
        r = _l5score.score(module, state, b)
        rows[5] = {"CEILING_TRIGGER_RECALL": r["recall"],
                   "capped": "make_engine(4)", "corpus": L5_BINDING,
                   "next_t": r["next_t"], "miss": r["miss"]}

    # L6: a constant confidence ranks nothing, so `AUROC = 1/2` exactly, at any
    # error rate — sat at by arithmetic (`humility/l6/IMPOSSIBILITY.md §1`).
    module = engine.module(6)
    if _reaches(engine, 6):
        b = _l6score.BATTERIES[L6_BINDING]()
        state, _b = _l6score.replay(
            module, lambda cap: module.make_engine(5, cap), b,
            module.DEFAULT_BUDGET)
        obs = _l6score.observe(module, state, b)
        r = _l6score.score(obs, b)
        rows[6] = {"CEILING_AUROC": (None if r["auroc"] is None
                                     else _l6score.permille(r["auroc"])),
                   "capped": "make_engine(5)", "corpus": b["name"],
                   "confidences": r["confidences"], "n_neg": r["n_neg"]}

    # L7: the conjunction `R8` clause 7 defines, over the artifact's own declared
    # class of 160 so that no engine can empty the denominator by testifying to
    # less (`humility/l7/IMPOSSIBILITY.md §4`).
    module = engine.module(7)
    if _reaches(engine, 7):
        b = _l7score.battery()
        state, _b = _l7score.replay(
            module, lambda cap: module.make_engine(6, cap), b,
            module.DEFAULT_BUDGET)
        obs = _l7score.observe(module, state, b)
        conj = _l7score.conjunction(obs, b)
        rows[7] = {"CEILING_CONJUNCTION": _l7score.permille(conj),
                   "capped": "make_engine(6)", "corpus": b["name"],
                   "hits": conj.numerator,
                   "denominator": len(b["generation_class"])}
    return rows


# ---- the transfer tier ------------------------------------------------------

def transfer(engine, version=None):
    """The same engine, the same scorers, on `corpora/real-sessions/` (§8.8).

    Three tiers are measurable on real fuel and reported; the fourth is not, and
    saying which is which is most of the value:

      * **L1** — exact retention, in budget. Directly comparable.
      * **L2** — the store's own cue surface. The corpus is the dogfood store,
        whose `tok` field exists precisely so a session summary is cue-
        addressable (`shell/dogfood/event.py`), so a cue battery is built here
        from the corpus rather than borrowed: for each event, the smallest
        prefix of its own tokens (rarest first, ties by token) that no other
        event carries in full. An event with no such prefix is **not uniquely
        cueable** and is reported as such rather than counted as a miss.
      * **L4** — `_l4tasks.build` over the real payloads, at the ratified
        footprint. This is where the divergence lives, and it is a property of
        the *fuel*, not of the engine: the facet map reads nothing in a session
        summary, and `row_shape` refuses a payload with a nested field, so a
        session summary is irreducible **and** un-rowable. Layer 4 has nothing
        to derive and degenerates to Layer-3 forgetting under the cap.
      * **L3** — reported as `n/a`, honestly. §5 L3's gate is stated over a
        stream that carries an `importance` field and a handle the engine can
        address (`HANDLE_FIELDS`); a session summary carries neither, so a
        Layer-3 *gate* on this corpus would be measuring the corpus, not the
        engine. What the tier does instead is report the two facts that make it
        `n/a`, which is the finding.
      * **L5, L6, L7** — added `[L7] [PACKAGE]`, and every one of them is
        `n/a` for a *different* reason, which is the whole content of the rows.
        L5 because the store's own promises are in the fuel while the facts
        that keep them are not; L6 because a corpus the engine is never wrong
        on leaves `§3.4`'s error class empty; L7 because this reading's
        vocabulary and the composition rule's are disjoint. Each row reports
        the facts that make it `n/a` rather than a zero, in the shape the L3
        row established three moves earlier.
    """
    from corpora import real_sessions
    version = version or real_sessions.LATEST
    payloads = real_sessions.payloads(version)
    manifest = real_sessions.manifest(version)

    out = {"corpus": "real-sessions/%s" % version, "n": len(payloads),
           "sha256": manifest["sha256"], "rows": collections.OrderedDict()}

    # --- L1: exact retention, in budget.
    module = engine.module(1)
    state, budget, accepted = _l1score.replay(module, engine.mk(1), payloads)
    r = _l1score.score(module, state, accepted)
    out["rows"][1] = {"GATE_F": r["F"], "GATE_C": r["C"], "GATE_B": budget["B"],
                      "refused": budget["refused"], "wrong": r["wrong"]}

    # --- L2: a cue battery built from the corpus's own cue surface.
    module = engine.module(2)
    out["rows"][2] = _transfer_l2(module, engine.mk(2), payloads)

    # --- L3: not gateable on this fuel, and why.
    out["rows"][3] = _transfer_l3_note(payloads)

    # --- L4: the full battery, at the ratified footprint.
    module = engine.module(4)
    b = _l4tasks.build("real-sessions/%s" % version, payloads)
    state, budget = _l4score.replay(module, engine.mk(4), b)
    r = _l4score.score(module, state, b)
    out["rows"][4] = {
        "GATE_FOOTPRINT": r["footprint"], "GATE_C": r["C"],
        "GATE_RECONSTRUCTION_F": r["F"], "GATE_B": budget["B"],
        "F_corruption": r["F_corruption"], "wrong": r["reconstruction_wrong"],
        "fabricated": r["fabricated"],
        "n_coverage": b["n_coverage"], "assertions": b["assertions"],
        "irreducible": len(b["irreducible"]),
        "occupancy": r["occupancy"], "raw_cells": b["raw_cells"],
    }

    # --- L5/L6/L7: three different reasons for the same `n/a`.
    if _reaches(engine, 7):
        out["rows"][5] = _transfer_l5_note(engine.module(7), engine, payloads)
        out["rows"][6] = _transfer_l6_note(engine.module(7), engine, payloads)
        out["rows"][7] = _transfer_l7_note(engine.module(7), engine, payloads)
    return out


def _real_state(module, engine, payloads):
    """The real corpus ingested in budget, once, for the three upper rows."""
    state = engine.mk(7)()
    for payload in payloads:
        state, t = module.ingest(state, payload)
        if t is None:
            raise AssertionError("the transfer corpus does not fit the default "
                                 "budget — the upper tiers cannot be measured")
    return state


def _transfer_l5_note(module, engine, payloads):
    """§5 L5 on real fuel: the promises are in the corpus and nothing fires.

    This is the first REAL corpus to carry an `intend` payload at all, so it is
    the first on which a Layer-5 measure is even attempted — and the result is a
    structural `n/a`. The store's intentions are conditioned on `attr`
    assertions, which the shell's *derived* replay produces and the store never
    holds, so no payload in the stream is a satisfaction point: the
    `trigger-recall` denominator is 0 and precision/recall are undefined rather
    than low. `dup-fire` and `miss` are 0 and tie their clauses, which is
    exactly the shape `R8` clause 3(c) rules disqualifying — a policy that does
    nothing ties the minimizing clauses of a gate it cannot clear.

    The clock is the auditor and it is reported: a firing consumes a `t` of its
    own (`R6` clause 2), so `next_t == |caller stream|` says nothing was
    emitted, without trusting a score.
    """
    state = _real_state(module, engine, payloads)
    intentions = [p for p in payloads if p.get("kind") == "intend"]
    pros = module.query(state, {"op": "prospection"})
    fired = 0
    for p in intentions:
        ans = module.query(state, {"op": "fired", "iid": p["iid"]})
        if ans["status"] == "answer":
            fired += len(ans["value"])
    pending = (pros["value"] or {}).get("pending")
    if intentions:
        carried = ("%d of %d events are `intend` payloads and every one of them "
                   "ARMS (pending %s), but no payload in this stream satisfies "
                   "any of their conditions — they watch for `attr` assertions "
                   "the shell's DERIVED replay produces and the store never "
                   "holds, so the promises are in the fuel and the facts that "
                   "would keep them are not"
                   % (len(intentions), len(payloads), pending))
    else:
        carried = ("this corpus carries no `intend` payload at all, so there is "
                   "nothing to arm and nothing to fire")
    return {
        "gateable": False,
        "intentions": len(intentions),
        "pending": pending,
        "fired": fired,
        "fireable": 0,
        "GATE_DUP_FIRE": 0, "GATE_MISS": 0,
        "next_t": state.next_t, "n": len(payloads),
        "why": "%s. The trigger-recall denominator is 0, so precision and "
               "recall are UNDEFINED rather than low; dup-fire and miss are 0 "
               "and TIE their clauses, which is the shape a policy that does "
               "nothing always has. next_t == %d == the caller stream, so the "
               "engine's own clock says it emitted nothing"
               % (carried, state.next_t),
    }


def _transfer_l6_note(module, engine, payloads):
    """§5 L6 on real fuel: nothing is wrong, so nothing can be calibrated.

    Every answer the engine gives on this corpus is a `read(t)` it regenerated
    exactly, so `n_neg = 0`, `AUROC` is undefined, and `R7` clause 3(a)'s
    holding applies to a *corpus* rather than to a policy: a gate citing `AUROC`
    binds only where both classes are guaranteed non-empty, and this one
    guarantees the opposite. `Brier` and `ECE` compute to 0 and mean nothing —
    a constant 1000 on a set of answers that are all correct is the base-rate
    constant wearing a model's clothes.

    The confidence vocabulary is the finding and is reported verbatim: it is
    `{0, 1000}`, which is the signature `humility/l6/IMPOSSIBILITY.md §1`
    measures for a **capped-5** engine. On this fuel a Layer-6 engine is
    indistinguishable from one with no confidence model, because the fuel gives
    the model nothing to price.
    """
    state = _real_state(module, engine, payloads)
    confidences = collections.Counter()
    answered = 0
    for t in range(state.next_t):
        ans = module.query(state, {"op": "read", "t": t})
        confidences[ans["confidence"]] += 1
        if ans["status"] == "answer":
            answered += 1
    return {
        "gateable": False,
        "A": answered, "n_pos": answered, "n_neg": 0,
        "GATE_AUROC": None,
        "confidences": tuple(sorted(confidences)),
        "n": len(payloads),
        "why": "%d of %d answers are correct and none is wrong, so n_neg = 0 "
               "and AUROC is UNDEFINED — R7 clause 3(a) disqualifies rather "
               "than excuses. The confidence vocabulary is %s, which is the "
               "signature of a CAPPED-5 engine: this fuel gives a confidence "
               "model nothing to price, because no key of the store's reading "
               "is set-once"
               % (answered, len(payloads), sorted(confidences)),
    }


def _transfer_l7_note(module, engine, payloads):
    """§5 L7 on real fuel: the reading cannot compose, and the ledger is empty.

    `COMPOSITION_FORM` determines a `profile` from two `part` assertions; the
    store's declared reading emits `session_summary` and `intend` and nothing
    else, so the two vocabularies are **disjoint**. `generate` abstains, the
    lineage ledger holds 0 items at 0 cells, and the three capability ratios are
    `n/a` over empty denominators — the same shape `humility/l7` measures for
    `make_engine(6)`, arrived at from the corpus side rather than the engine's.

    That is a property of the **reading**, not a defect of the layer: the same
    engine composes 160 items on `corpora/l7compose`.
    """
    state = _real_state(module, engine, payloads)
    ledger = module.query(state, {"op": "lineage"})
    entities = sorted(set(p["entity"] for p in payloads if "entity" in p))
    generated = 0
    for entity in entities or [1]:
        ans = module.query(state, {"op": "generate", "entity": entity})
        if ans["status"] == "answer":
            generated += 1
    value = ledger["value"] or {}
    return {
        "gateable": False,
        "GATE_VALIDITY": None, "GATE_NOVELTY": None, "GATE_TAGGING": None,
        "generated": generated,
        "ledger_items": value.get("generated"), "ledger_cells": value.get("cells"),
        "n": len(payloads),
        "why": "the store's declared reading emits only kinds the composition "
               "rule does not read, so `generate` abstains everywhere, the "
               "lineage ledger holds %s items at %s cells, and validity / "
               "novelty / tagging are n/a over EMPTY denominators — R8 clause "
               "3(c) disqualifies. It is a property of the reading: the same "
               "engine composes 160 items on corpora/l7compose"
               % (value.get("generated"), value.get("cells")),
    }


def transfer_cues(payloads):
    """`(tasks, unaddressable)` — the L2 transfer battery, built deterministically.

    A task is `{"cue": {"tok": {…}}, "t": t}`: the smallest prefix of event `t`'s
    own tokens, taken **rarest first and then alphabetically**, that no other
    event in the corpus carries in full. Rarest-first because a rare token is
    what makes a cue discriminating, alphabetically after that because a total
    order is what makes the battery reproducible.

    An event for which no such prefix exists — every one of its tokens is
    carried, in full, by some other event too — is returned in `unaddressable`.
    It is not scored as a miss: no engine could distinguish it from its twin, so
    counting it would measure the corpus.
    """
    bags = [set(p.get("tok", {})) for p in payloads]
    df = collections.Counter()
    for bag in bags:
        df.update(bag)

    tasks = []
    unaddressable = []
    for t, bag in enumerate(bags):
        order = sorted(bag, key=lambda tok: (df[tok], tok))
        probe = []
        found = False
        for tok in order:
            probe.append(tok)
            probe_set = set(probe)
            if not any(other != t and probe_set <= bags[other]
                       for other in range(len(bags))):
                found = True
                break
        if found:
            tasks.append({"t": t, "cue": {"tok": {tok: 1 for tok in probe}},
                          "probe": tuple(probe)})
        else:
            unaddressable.append(t)
    return tasks, unaddressable


def _transfer_l2(module, mk, payloads):
    """Score the transfer cue battery under §3.0, plus never-ingested probes."""
    tasks, unaddressable = transfer_cues(payloads)

    state = mk()
    for payload in payloads:
        state, t = module.ingest(state, payload)
        if t is None:
            raise AssertionError("the transfer corpus does not fit the default "
                                 "budget — the L2 tier cannot be measured")

    recovered = 0
    wrong = 0
    abstained = 0
    for task in tasks:
        ans = module.query(state, {"op": "recall", "cue": task["cue"]})
        want = {"payload": payloads[task["t"]], "t": task["t"]}
        if ans["status"] == "answer" and ans["value"] == want:
            recovered += 1
        elif ans["status"] == "abstain":
            abstained += 1
        else:
            wrong += 1

    # Never-ingested cues: tokens the corpus's own vocabulary does not contain.
    vocabulary = set()
    for payload in payloads:
        vocabulary |= set(payload.get("tok", {}))
    absent = [{"tok": {"zzq%04d" % k: 1}} for k in range(100)]
    absent = [cue for cue in absent
              if not (set(cue["tok"]) & vocabulary)]
    fabricated = 0
    for cue in absent:
        if module.query(state, {"op": "recall", "cue": cue})["status"] != "abstain":
            fabricated += 1

    n = len(tasks) + len(absent)
    from fractions import Fraction
    f_sum = (recovered * 1000 + abstained * 100
             + (len(absent) - fabricated) * 1000)
    return {
        "GATE_CUE_C": _l1score.permille(Fraction(recovered, len(tasks))) if tasks else 0,
        "GATE_F": _l1score.permille(Fraction(f_sum, n * 1000)) if n else 0,
        "GATE_B": 1000 if state.occupancy <= state.budget_cap else 0,
        "wrong": wrong, "fabricated": fabricated,
        "n_cueable": len(tasks), "unaddressable": len(unaddressable),
        "n_absent": len(absent),
    }


def _transfer_l3_note(payloads):
    """The two corpus facts that make a Layer-3 gate meaningless on real fuel."""
    from adapters import l3
    weighted = sum(1 for p in payloads if l3.GRAMMAR_WEIGHT_FIELD in p)
    handled = sum(1 for p in payloads
                  if any(field in p for field in l3.HANDLE_FIELDS))
    return {
        "gateable": False,
        "with_importance": weighted,
        "with_handle": handled,
        "n": len(payloads),
        "why": "§5 L3 gates weighted coverage under 10x pressure; %d of %d "
               "events carry an `%s` field and %d carry any of %s, so both the "
               "weighting and the cue address would be the harness's invention "
               "rather than the corpus's" % (weighted, len(payloads),
                                             l3.GRAMMAR_WEIGHT_FIELD, handled,
                                             "/".join(l3.HANDLE_FIELDS)),
    }


# ---- the whole card ---------------------------------------------------------

def build(engine, quick=False, with_transfer=True):
    """Measure one engine across every tier. Returns an ordered result dict."""
    gates = gate_table()
    card = collections.OrderedDict()
    card["engine"] = engine.name
    card["kind"] = engine.kind
    card["note"] = engine.note
    card["scale"] = "quick" if quick else "full"
    card["gates"] = gates
    card["tiers"] = collections.OrderedDict()

    card["tiers"][1] = tier_l1(engine, QUICK_L1_CORPORA if quick else L1_CORPORA)
    card["tiers"][2] = tier_l2(engine)
    card["tiers"][3] = tier_l3(engine, (L3_BINDING,) if quick
                               else (L3_BINDING, L3_DIAGNOSTIC))
    card["tiers"][4] = tier_l4(engine,
                               _l4tasks.prefix(L4_BINDING, QUICK_L4_PREFIX)
                               if quick else None)
    card["tiers"][5] = tier_l5(engine) if _reaches(engine, 5) else []
    card["tiers"][6] = (tier_l6(engine, (L6_BINDING,) if quick
                                else (L6_BINDING, L6_DIAGNOSTIC))
                        if _reaches(engine, 6) else [])
    card["tiers"][7] = tier_l7(engine) if _reaches(engine, 7) else []

    for layer, rows in card["tiers"].items():
        for row in rows:
            row["verdict"] = _verdict(row, gates[layer]["gates"])

    card["humility"] = tier_humility(engine, quick=quick)
    for layer, row in card["humility"].items():
        ceilings = gates[layer]["ceilings"]
        row["verdict"] = "HELD"
        for const, ceiling in ceilings.items():
            if row.get(const) is not None and row[const] > ceiling:
                row["verdict"] = "BREACHED"

    if with_transfer:
        card["transfer"] = transfer(engine)
        for layer, row in card["transfer"]["rows"].items():
            if row.get("gateable") is False:
                row["verdict"] = "n/a"
            else:
                row["verdict"] = _verdict(row, gates[layer]["gates"])
    return card


# ---- rendering --------------------------------------------------------------

LAYER_NAMES = {1: "Retention", 2: "Recall", 3: "Forgetting", 4: "Consolidation",
               5: "Prospection", 6: "Meta-memory", 7: "Generation"}


def _gate_text(gates):
    def one(const, value):
        label = const[len("GATE_"):].lower().replace("_", "-")
        if const in MINIMIZING:
            return "%s<=%d" % (label, value)
        if value == 1000 and const == "GATE_B":
            return "B=1000"
        return "%s>=%d" % (label, value)
    return " ".join(one(c, v) for c, v in gates.items())


def _measured_text(row, gates):
    out = []
    for const in gates:
        if const in row:
            label = const[len("GATE_"):].lower().replace("_", "-")
            got = row[const]
            out.append("%s %s" % (label, "n/a" if got is None else got))
    return " ".join(out)


def render(card):
    """The card as printable lines. Plain text, no colour, no dependencies."""
    lines = []
    lines.append("memtrials scorecard — engine: %s (%s)" % (card["engine"], card["kind"]))
    lines.append("  %s" % card["note"])
    lines.append("  scale: %s   gates: BOUNDARY.md §5 via laws/t_rulings.py::AUTHORIZED_GATES"
                 % card["scale"])
    lines.append("")
    lines.append("SYNTHETIC TIERS")
    for layer in LAYERS:
        gates = card["gates"][layer]["gates"]
        lines.append("  L%d %-14s gate: %s" % (layer, LAYER_NAMES[layer],
                                               _gate_text(gates)))
        if not card["tiers"][layer]:
            lines.append("      not measured: this engine does not claim "
                         "Layer %d, and a zero here would say nothing about it"
                         % (layer,))
        for row in card["tiers"][layer]:
            marker = "*" if row.get("binding") else " "
            lines.append("    %s %-22s %-46s %s"
                         % (marker, row["corpus"], _measured_text(row, gates),
                            row["verdict"]))
            if row["verdict"] == "diag" and "oracle_ceiling" in row:
                lines.append("        ungated (R1): no retain-or-drop policy "
                             "reaches the gate here — the oracle ceiling is "
                             "%d‰ against %d‰"
                             % (row["oracle_ceiling"], gates["GATE_WEIGHTED_C"]))
            elif row["verdict"] == "diag" and layer == 6:
                lines.append("        ungated (R7 clause 1): DEMOTED in the "
                             "same clause that bound its successor — on murk "
                             "the ties this model reads are exactly its "
                             "errors, so evidence that ranks also resolves")
            elif row["verdict"] == "diag":
                lines.append("        ungated: a declared reduced scale, not "
                             "the corpus the gate binds on")
            if row.get("undefined"):
                lines.append("        FAILED on an UNDEFINED clause (%s): n/a "
                             "disqualifies (R7 clause 3(a), R8 clause 3(c)) — "
                             "an instrument out of range has not weighed the "
                             "object" % (", ".join(row["undefined"]),))
            if layer == 7 and row.get("rungs"):
                lines.append("        promotion ladder, per rung: %s   still "
                             "generated: %s"
                             % (list(row["rungs"]), list(row["still_generated"])))
        ceilings = card["gates"][layer]["ceilings"]
        if ceilings:
            measured = card.get("humility", {}).get(layer)
            text = " ".join("%s<=%d" % (c[len("CEILING_"):].lower()
                                        .replace("_", "-"), v)
                            for c, v in ceilings.items())
            if measured:
                got = " ".join("%d" % measured[c] for c in ceilings
                               if c in measured)
                lines.append("      humility %s   capped %s measured %s on %s  %s"
                             % (text, measured["capped"], got,
                                measured["corpus"], measured["verdict"]))
                if layer == 4:
                    lines.append("        (whole-stream capped F is %d, measured "
                                 "once OUT OF SUITE — humility/l4/IMPOSSIBILITY.md "
                                 "§4; the prefix ladder converges on it from below)"
                                 % measured["whole_stream_recorded"])
            else:
                lines.append("      humility %s   (not measurable: this engine "
                             "does not reach the layer below)" % text)
    if "transfer" in card:
        tr = card["transfer"]
        lines.append("")
        lines.append("TRANSFER TIER — %s (%d events, sha256 %s…)"
                     % (tr["corpus"], tr["n"], tr["sha256"][:12]))
        for layer, row in tr["rows"].items():
            gates = card["gates"][layer]["gates"]
            if row.get("gateable") is False:
                lines.append("    L%d %-19s %-46s %s"
                             % (layer, "not gateable",
                                _measured_text(row, gates), "n/a"))
                lines.append("       %s" % row["why"])
                continue
            lines.append("    L%d %-19s %-46s %s"
                         % (layer, LAYER_NAMES[layer],
                            _measured_text(row, gates), row["verdict"]))
        l4 = tr["rows"][4]
        lines.append("       L4 on real fuel: %d assertions, %d irreducible of %d "
                     "events — the facet map reads nothing in a session summary "
                     "and a nested field refuses a row, so there is nothing to "
                     "derive" % (l4["assertions"], l4["irreducible"], tr["n"]))
        lines.append("       and the coverage denominator is %d (no (entity,key) "
                     "pair exists, so C here is a global count, not the semantic "
                     "battery) — read reconstruction-f, not c"
                     % (l4["n_coverage"],))
    lines.append("")
    lines.append("run.py is the gate; this card reports. `python3 -m trials --suite` "
                 "runs the real thing.")
    return lines

"""laws/ — the ruling supplement and the authority of every gate a trial applies.

`BOUNDARY-RULINGS.md` is the frozen, append-only supplement created by the
`RULING` session, under the mechanism `BOUNDARY.md §5` itself anticipates when it
defers the Layer-8 and Layer-9 thresholds to a document written at the Phase 3→4
gate: **a frozen supplement may bind.** It never amends the constitution; it
settles questions the constitution leaves open — which corpus a stated gate binds
on, which reading of a ratified defense sentence the trials implement, and what
procedure binds future gates.

This is a **laws** trial rather than an ops one because what it guards is
*legality*, not capability (§6): a gate applied without authority is an illegal
gate regardless of what any engine scores against it, and a ledger that stops
being append-only has broken the discipline every layer above it rests on.

Three things are checked.

## 1. The supplement exists and is well-formed

Entry IDs are `R1, R2, …`, contiguous from 1, in order, never reused. Every entry
declares its frozen status and its holding. The header carries the append-only
declaration, because that declaration is what check 2 enforces.

## 2. The append-only ledgers are append-only, against git history

`BOUNDARY.md §9.2` and `CLAUDE.md §5`: old `BOUNDARY.log` lines are never
rewritten, and each `BOUNDARY-RULINGS.md` entry is frozen the moment it is
committed. Both are therefore **strictly append-only files**, and that is a
property git can settle rather than a promise a session makes to itself: every
committed version of each ledger must be a **byte-exact prefix** of the file on
disk now. An edited line, a deleted entry, a re-worded ruling — each breaks the
prefix and goes red.

`BOUNDARY-RULINGS.md` has **no** committed version on the commit that creates it,
so its check is vacuous exactly once. `BOUNDARY.log` is required to have at least
one, which is what keeps the mechanism demonstrably live: the same prefix walk
runs over a file with real history on every run, so a broken walk cannot hide
behind an empty set. This mirrors `t_l3streamb.py`'s use of `l3stream` to prove
its rank statistic is not vacuously satisfied.

Skips only when git itself is unavailable (a source export rather than a clone) —
never when the answer would be inconvenient.

## 3. Every gate a trial applies is authorized

The registry below names **every** gate threshold and humility ceiling any trial
applies, with the authority for each: a literal clause of the `BOUNDARY.md §5`
table, or a `BOUNDARY-RULINGS.md` entry, or both — thresholds come from §5, and a
ruling may bind a threshold to a corpus without touching it (R1). Three things
are then checked together, and the third is what gives the first two teeth:

  * the declared authority text **actually occurs** in the document claimed;
  * the declared value **equals** the constant in the trial source, read by `ast`
    from the file rather than by importing it;
  * **no constant escapes the registry** — every module-level `GATE_*` /
    `CEILING_*` integer anywhere under `trials/` must be declared here. A future
    session cannot introduce an unauthorized gate by writing one down, because
    writing one down is exactly what this check looks for.

The scope is stated honestly: this binds module-level gate constants, which is
the form every gate in the suite takes. A threshold buried as a literal inside a
function body would not be caught, and the remedy for that is the convention this
check enforces — gates are named constants, at module level, or they are not
gates.
"""

import ast
import os
import re
import subprocess

from _harness import PROJECT_ROOT, require, require_equal, skip

TRIALS_DIR = os.path.join(PROJECT_ROOT, "trials")
RULINGS_PATH = os.path.join(PROJECT_ROOT, "BOUNDARY-RULINGS.md")
BOUNDARY_PATH = os.path.join(PROJECT_ROOT, "BOUNDARY.md")

# The two strictly append-only ledgers, and whether history is required to exist.
# BOUNDARY.log must have committed versions: it is what proves the prefix walk is
# live rather than vacuously satisfied on an empty set.
LEDGERS = (("BOUNDARY.log", True), ("BOUNDARY-RULINGS.md", False))

CONST_PREFIXES = ("GATE_", "CEILING_")

ENTRY_HEADING = re.compile(r"^# (R\d+) — (.+)$", re.MULTILINE)


# --- the gate registry ------------------------------------------------------
# (trial file, constant, value, authorities, note). An authority is
# ("BOUNDARY.md", <clause>) or ("BOUNDARY-RULINGS.md", <entry id>); the clause
# must occur verbatim in that document.

def _s5(clause):
    return ("BOUNDARY.md", clause)


def _ruling(entry):
    return ("BOUNDARY-RULINGS.md", entry)


AUTHORIZED_GATES = (
    ("ascension/l1/t_retention.py", "GATE_F", 1000, (_s5("F=1000"),),
     "§5 L1 retention fidelity"),
    ("ascension/l1/t_retention.py", "GATE_C", 995, (_s5("C≥995"),),
     "§5 L1 coverage"),
    ("ascension/l1/t_retention.py", "GATE_B", 1000, (_s5("B=1000"),),
     "§5 L1 budget; §4.1 makes it absolute"),

    ("ascension/l2/t_recall.py", "GATE_CUE_C", 900, (_s5("cue-C≥900"),),
     "§5 L2 cue coverage"),
    ("ascension/l2/t_recall.py", "GATE_F", 950, (_s5("F≥950"),),
     "§5 L2 fidelity"),
    ("ascension/l2/t_recall.py", "GATE_B", 1000, (_s5("B=1000"),),
     "§5 L2 budget"),
    ("humility/l2/t_recall.py", "CEILING_CUE_C", 100,
     (_s5("capped cue-C ≤ 100"),), "§5 L2 humility ceiling"),

    ("ascension/l3/t_forgetting.py", "GATE_WEIGHTED_C", 850,
     (_s5("weighted-C≥850"), _ruling("R1")),
     "threshold from §5 L3, unchanged; R1 binds it to corpora/l3streamb"),
    ("ascension/l3/t_forgetting.py", "GATE_UNWEIGHTED_C", 90,
     (_s5("unweighted-C≥90"), _ruling("R1")),
     "threshold from §5 L3, unchanged; R1 binds it to corpora/l3streamb"),
    ("ascension/l3/t_forgetting.py", "GATE_F", 950,
     (_s5("F≥950"), _ruling("R3")),
     "threshold from §5 L3, unchanged; R3 settles the reading of F under eviction"),
    ("ascension/l3/t_forgetting.py", "GATE_B", 1000, (_s5("B=1000"),),
     "§5 L3 budget; binds on both streams whatever R1 says about coverage"),
    ("humility/l3/t_forgetting.py", "CEILING_WEIGHTED_C", 300,
     (_s5("capped weighted-C ≤ 300"),),
     "§5 L3 humility ceiling; no ruling reaches it"),

    # Layer 4. The ratified §5 L4 thresholds, unchanged, bound to
    # corpora/l4stream by R4 — the same shape as R1's Layer-3 binding: a ruling
    # binds a threshold to a corpus without touching it. R4 also settles the two
    # readings these constants are meaningless without (the footprint's unit, and
    # pricing rule P), which is why GATE_FOOTPRINT cites it and why every one of
    # them does. `t_attainability.py` names them to ask whether a corpus admits
    # them (R2 obligations 1 and 2); the Stage-B battery that applies them to an
    # engine is not written yet.
    ("ascension/l4/t_attainability.py", "GATE_FOOTPRINT", 250,
     (_s5("footprint≤250"), _ruling("R4")),
     "threshold from §5 L4, unchanged; R4 clause 2 reads it in permille of the "
     "raw episodic footprint and clause 3 prices the cells it counts"),
    ("ascension/l4/t_attainability.py", "GATE_RECONSTRUCTION_F", 900,
     (_s5("reconstruction F≥900"), _ruling("R4")),
     "threshold from §5 L4, unchanged; R4 clause 4 keeps it on the literal §3.0 "
     "table — R3 excludes L4 and no extension was taken"),
    ("ascension/l4/t_attainability.py", "GATE_C", 850,
     (_s5("C≥850"), _ruling("R4")),
     "threshold from §5 L4, unchanged; R4 clause 1 binds it to corpora/l4stream"),
    ("ascension/l4/t_attainability.py", "GATE_B", 1000,
     (_s5("B=1000"), _ruling("R4")),
     "§5 L4 budget; under R4 clause 2 the same number as the footprint cap, "
     "certified after every write rather than on the final state"),
    ("ascension/l4/t_attainability.py", "CEILING_RECONSTRUCTION_F", 400,
     (_s5("capped reconstruction F ≤ 400 at footprint≤250"), _ruling("R4")),
     "§5 L4 humility ceiling, unchanged; R4 binds the Layer-4 humility trial to "
     "corpora/l4stream, where the capped arithmetic bound is 325"),

    # Layer 4, Stage B: the same ratified numbers, now applied to an ENGINE
    # rather than asked of a corpus. `t_consolidation.py` (ascension) is
    # engine-gated and skips until Stage C; `humility/l4` measures the capped
    # forget-only engine today. The duplication of a *value* across files is
    # what this registry is for — both copies are bound to one §5 clause and one
    # ruling here, so they cannot drift apart silently.
    ("ascension/l4/t_consolidation.py", "GATE_FOOTPRINT", 250,
     (_s5("footprint≤250"), _ruling("R4")),
     "threshold from §5 L4, unchanged; R4 clause 2 reads it in permille of the "
     "raw episodic footprint and clause 3 prices the cells it counts"),
    ("ascension/l4/t_consolidation.py", "GATE_RECONSTRUCTION_F", 900,
     (_s5("reconstruction F≥900"), _ruling("R4")),
     "threshold from §5 L4, unchanged; R4 clause 4 keeps it on the literal §3.0 "
     "table — the concession was examined and declined"),
    ("ascension/l4/t_consolidation.py", "GATE_C", 850,
     (_s5("C≥850"), _ruling("R4")),
     "threshold from §5 L4, unchanged; R4 clause 1 binds it to corpora/l4stream"),
    ("ascension/l4/t_consolidation.py", "GATE_B", 1000,
     (_s5("B=1000"), _ruling("R4")),
     "§5 L4 budget; under R4 clause 2 the same number as the footprint cap, "
     "certified after every write rather than on the final state"),
    ("humility/l4/t_consolidation.py", "CEILING_RECONSTRUCTION_F", 400,
     (_s5("capped reconstruction F ≤ 400 at footprint≤250"), _ruling("R4")),
     "§5 L4 humility ceiling, unchanged; measured against make_engine(3) at "
     "footprint 250 on corpora/l4stream per R4"),
    ("humility/l4/t_consolidation.py", "GATE_FOOTPRINT", 250,
     (_s5("footprint≤250"), _ruling("R4")),
     "the footprint the §5 L4 ceiling is stated AT — the capped engine is "
     "squeezed to it before the ceiling means anything"),

    # Layer 4, Stage C: the ratified footprint again, in the two files the
    # ENGINE brought with it. Neither applies it as a gate an engine must clear
    # on a corpus R4 binds — `ops/l4` prices a design the engine did not choose
    # against it, and `strain/l4` states the footprint murk's dirt is thrown at,
    # murk having been kept as dirt and retired as a ruler by R4 clause 1. They
    # are registered all the same, because the registry's rule is that a §5
    # number cannot appear in a trial without a recorded authority, whatever the
    # trial does with it.
    ("ops/l4/t_l4_composition.py", "GATE_FOOTPRINT", 250,
     (_s5("footprint≤250"), _ruling("R4")),
     "threshold from §5 L4, unchanged; used to price the two-way indexed schema "
     "the engine could not afford (R4 clause 2's permille reading, clause 3's "
     "pricing rule)"),
    ("strain/l4/t_consolidation_strain.py", "GATE_FOOTPRINT", 250,
     (_s5("footprint≤250"), _ruling("R4")),
     "threshold from §5 L4, unchanged; the footprint the murk strain is stated "
     "at, per R4 clause 1's keeping of murk as dirt rather than as a ruler"),
    ("strain/l4/t_demotion_seam.py", "GATE_FOOTPRINT", 250,
     (_s5("footprint≤250"), _ruling("R4")),
     "threshold from §5 L4, unchanged; the pressure the demotion-seam strains "
     "are stated at rather than a gate they apply — the blocking surface exists "
     "BECAUSE of it (README-l4 §0.1: at 250 permille exactly one access path is "
     "affordable), so the number is the strain's premise"),

    # The inheritance class (trials/inheritance/README.md). It introduces no
    # threshold of its own: every gate it applies is a ratified §5 clause of a
    # layer BELOW the one being ascended to, re-applied to the current engine at
    # cap N on an in-budget substrate. Where an inherited claim is exactness
    # rather than a threshold (nothing is under pressure, so everything must be
    # recalled), it is asserted as an identity and is deliberately not a gate.
    ("inheritance/l4/t_inheritance.py", "GATE_L2_CUE_C", 900,
     (_s5("cue-C≥900"),),
     "§5 L2 cue coverage, re-applied at layer_cap = 4"),
    ("inheritance/l4/t_inheritance.py", "GATE_L2_F", 950, (_s5("F≥950"),),
     "§5 L2 fidelity, re-applied at layer_cap = 4"),
    ("inheritance/l4/t_inheritance.py", "GATE_B", 1000, (_s5("B=1000"),),
     "the budget law, absolute at every layer (§4.1); asserted in budget, where "
     "a breach cannot be a pressure consequence"),

    # Layer 5, Stage A. The ratified §5 L5 constants, named by the attainability
    # trial ONLY so it can ask whether corpora/l5stream admits them (R2
    # obligations 1 and 2). No engine is measured against any of them — none
    # exists.
    #
    # Six of the seven carry **R5** beside their §5 L5 clause — GATE_F alone
    # carries none of it, being the clause R5 expressly EXCLUDES because it
    # discharges R2 obligation 1 the ordinary way. What that ruling authorizes is
    # stated precisely: R5 settles HOW R2's two obligations are discharged for
    # these constants — by an exhibited ATTAINMENT for a clause the constitution
    # states as an identity (clause 1), and direction-aware and over the
    # CONJUNCTION for a minimizing one (clause 2). It did **not** bind the
    # Layer-5 gate to a corpus.
    #
    # **R6 is what binds the substrate**, and every one of the seven carries it:
    # clause 1 binds the Layer-5 ascension gate AND the humility ceiling to
    # corpora/l5stream (together, because a ceiling measured on one corpus beside
    # a gate cleared on another discriminates nothing), and clause 4 rules the cap
    # the budget law binds at — `budget_cap = raw_cells // 4 = 45 638`. GATE_F
    # therefore carries R6 and not R5: the substrate is ruled for it like every
    # other clause, only the READING of R2 is not.
    #
    # Four of them are the first IDENTITIES in the registry that are not the
    # budget law: for them the oracle ceiling IS the gate, so R2's "strictly
    # below" is undischargeable by the method that discharged Layers 3 and 4.
    # That collision is the Stage-A finding recorded in
    # trials/ascension/l5/ATTAINABILITY.md §5, and R5 is what resolves it.
    ("ascension/l5/t_attainability.py", "GATE_TRIGGER_PRECISION", 1000,
     (_s5("trigger-precision=1000"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; an identity — R5 clause 1 discharges R2 obligation 1 by "
     "the witness ATTAINING it that ATTAINABILITY.md exhibits, rather than by a "
     "gate lying strictly below a ceiling; R6 clause 1 binds it to "
     "corpora/l5stream, where that witness was exhibited"),
    ("ascension/l5/t_attainability.py", "GATE_TRIGGER_RECALL", 1000,
     (_s5("trigger-recall=1000"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; an identity, discharged by exhibited attainment per R5 "
     "clause 1; bound to corpora/l5stream by R6 clause 1"),
    ("ascension/l5/t_attainability.py", "GATE_DUP_FIRE", 0,
     (_s5("dup-fire=0"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; a MINIMIZING clause — R2's 'strictly above' is written "
     "for measures where higher is better and three named baselines tie it, so "
     "R5 clause 2 reads it direction-aware and over the conjunction; R6 clause 1 "
     "binds it to corpora/l5stream"),
    ("ascension/l5/t_attainability.py", "GATE_MISS", 0,
     (_s5("miss=0"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; a MINIMIZING clause, tied by two named baselines; R5 "
     "clause 2, and R6 clause 1 for the corpus"),
    ("ascension/l5/t_attainability.py", "GATE_F", 980,
     (_s5("F≥980"), _ruling("R6")),
     "§5 L5, unchanged; the ONE clause of §5 L5 that discharges R2 obligation 1 "
     "by the ordinary method (980 < the exhibited oracle's 1000), and expressly "
     "EXCLUDED from R5 clause 1 for that reason — which is why it alone among "
     "the Layer-5 constants carries no R5. It carries R6 like every other: "
     "clause 1 binds the whole gate, this clause included, to corpora/l5stream. "
     "R3 does not reach Layer 5 and no extension is requested"),
    ("ascension/l5/t_attainability.py", "GATE_B", 1000,
     (_s5("B=1000"), _ruling("R5"), _ruling("R6")),
     "§5 L5 budget; the identity that has been in this registry since Layer 1 "
     "without ever being scored against an oracle — §3.3 makes any value below "
     "1000 disqualifying, so its ceiling is exactly 1000. R5 REGULARIZES that "
     "practice rather than correcting it: nothing earlier stated was false, and "
     "from here the clause is discharged by attainment. R6 clause 4 rules the "
     "cap it is certified against: budget_cap = raw_cells // 4 = 45 638"),
    ("ascension/l5/t_attainability.py", "CEILING_TRIGGER_RECALL", 50,
     (_s5("capped trigger-recall ≤ 50"), _ruling("R5"), _ruling("R6")),
     "§5 L5 humility ceiling, unchanged; measured 0 on the capped-4 policy, and "
     "structurally so — README-l4 §4 predicts 0 and not near 0, there being no "
     "pending set for a numerator to be drawn from. R5 clause 2 is the reading "
     "under which a baseline tying a minimizing clause does not void it; R6 "
     "clause 1 binds the ceiling to corpora/l5stream in the SAME clause as the "
     "gate, because a ceiling measured on one corpus beside a gate cleared on "
     "another discriminates nothing"),

    # Layer 5, Stage B: the same ratified numbers, now applied to an ENGINE
    # rather than asked of a corpus. `t_prospection.py` (ascension) is
    # engine-gated and skips until Stage C; `humility/l5` measures the capped
    # consolidation engine today. The duplication of a *value* across files is
    # what this registry is for — both copies are bound to one §5 clause and, for
    # the five R5 reaches, to one ruling here, so they cannot drift apart.
    #
    # THE CORPUS IS NOW BOUND, and by R6 rather than by R5. R5 settled a reading
    # and expressly declined the binding; R6 clause 1 takes it, for the ascension
    # gate and the humility ceiling TOGETHER, and R6 clause 4 rules the cap these
    # batteries replay at (raw_cells // 4 = 45 638). So each entry below carries
    # two rulings and they authorize different things: R5 the reading of R2's
    # obligations, R6 the substrate — except GATE_F, which carries R6 alone,
    # being the clause R5 expressly excludes.
    ("ascension/l5/t_prospection.py", "GATE_TRIGGER_PRECISION", 1000,
     (_s5("trigger-precision=1000"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; an IDENTITY, asserted with require_equal rather than a "
     "threshold — R5 clause 1 is why there is no inequality here to widen; R6 "
     "clause 1 binds it to corpora/l5stream"),
    ("ascension/l5/t_prospection.py", "GATE_TRIGGER_RECALL", 1000,
     (_s5("trigger-recall=1000"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; an identity, per R5 clause 1; bound to corpora/l5stream "
     "by R6 clause 1"),
    ("ascension/l5/t_prospection.py", "GATE_DUP_FIRE", 0,
     (_s5("dup-fire=0"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; a MINIMIZING clause read direction-aware and over the "
     "conjunction per R5 clause 2, bound to corpora/l5stream by R6 clause 1. The "
     "Stage-B battery observes it through the query interface and audits it "
     "against the engine's own logical clock — which is R6 clause 2's `t` "
     "semantics doing the auditing, so it is not a number an engine reports "
     "about itself"),
    ("ascension/l5/t_prospection.py", "GATE_MISS", 0,
     (_s5("miss=0"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; a MINIMIZING clause, R5 clause 2; R6 clause 1 for the "
     "corpus, and R6 clause 2 records the one consequence it fixes — a firing is "
     "NOT discretionary, since miss = 0 means an intention whose condition is "
     "satisfied fires"),
    ("ascension/l5/t_prospection.py", "GATE_F", 980,
     (_s5("F≥980"), _ruling("R6")),
     "§5 L5, unchanged; the ONE clause of §5 L5 that is a threshold, expressly "
     "EXCLUDED from R5 clause 1, which is why it alone carries no R5. It carries "
     "R6 clause 1 like every other clause of the gate — the substrate is ruled "
     "for it too. R3 does not reach Layer 5 and no extension is requested"),
    ("ascension/l5/t_prospection.py", "GATE_B", 1000,
     (_s5("B=1000"), _ruling("R5"), _ruling("R6")),
     "§5 L5 budget; asserted after EVERY write, never once at the end, because "
     "§4.1.2 refuses mid-stream. R6 clause 4 rules the cap — raw_cells // 4 = "
     "45 638 — and rules with it that the events the engine emits when triggers "
     "fire compete for cells inside that cap without enlarging it"),
    ("humility/l5/t_prospection.py", "CEILING_TRIGGER_RECALL", 50,
     (_s5("capped trigger-recall ≤ 50"), _ruling("R5"), _ruling("R6")),
     "§5 L5 humility ceiling, unchanged; measured 0 against make_engine(4) — the "
     "frozen Layer-4 engine, run over the whole stream through the generic "
     "interface, which is the half Stage A's policy-side measurement could not "
     "reach. R6 clause 1 binds this ceiling to corpora/l5stream in the SAME "
     "clause as the gate, and carries the measurement in BOTH conditions R5 "
     "clause 4 demands — 945 of 945 intentions held in budget, 30 of 945 at the "
     "ratified cap, trigger-recall 0 either way. IMPOSSIBILITY.md carries the "
     "structural argument"),

    # The inheritance class at Layer 5. As at Layer 4 it introduces no threshold
    # of its own: these are ratified §5 clauses of LOWER layers, re-applied to the
    # current engine at cap 5 on in-budget substrates. The Layer-4 row it adds is
    # asserted as an IDENTITY (C = 1000, reconstruction F = 1000) and therefore
    # declares no constant — a gate constant is what this registry governs, and
    # an in-budget identity is deliberately not one.
    ("inheritance/l5/t_inheritance.py", "GATE_L2_CUE_C", 900,
     (_s5("cue-C≥900"),),
     "§5 L2 cue coverage, re-applied at layer_cap = 5"),
    ("inheritance/l5/t_inheritance.py", "GATE_L2_F", 950, (_s5("F≥950"),),
     "§5 L2 fidelity, re-applied at layer_cap = 5"),
    ("inheritance/l5/t_inheritance.py", "GATE_B", 1000, (_s5("B=1000"),),
     "the budget law, absolute at every layer (§4.1); asserted in budget, where "
     "a breach cannot be a pressure consequence"),

    # Layer 5, Stage C: the strain class. A strain does not apply a gate — it
    # states the pressure a property is asserted UNDER — but this registry's rule
    # is that a §5 number cannot appear in a trial without a recorded authority
    # whatever the trial does with it, which is why `strain/l4`'s copies of
    # GATE_FOOTPRINT are here too.
    ("strain/l5/t_prospection_strain.py", "GATE_DUP_FIRE", 0,
     (_s5("dup-fire=0"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; the clause the fired-ledger strain exists for. It is not "
     "applied as a gate here — `ascension/l5` does that on the binding corpus — "
     "but as the number a ledger-blind reference policy is shown to miss by 199 "
     "on a fixture, which is what makes the guard load-bearing rather than "
     "assumed"),
    ("strain/l5/t_prospection_strain.py", "GATE_MISS", 0,
     (_s5("miss=0"), _ruling("R5"), _ruling("R6")),
     "§5 L5, unchanged; the clause behind the engine's design decision the "
     "absent-mindedness strain measures — the pending set and the fired ledger "
     "are outside every eviction phase, because an engine that could evict "
     "either could be made to break a ratified gate by being poor. R6 clause 2 "
     "left that question to Stage C expressly"),

    # Layer 6, Stage A — ROUND 1, AND NOW THE DEMOTED DIAGNOSTIC. The ratified §5
    # L6 numbers, declared so the attainability arithmetic can be stated in the
    # constitution's own figures — and carrying a §5 clause and NO COMPANION
    # RULING. When they were written that recorded "no gate binds anywhere"; since
    # R7 it records something sharper and permanent, which is why the six entries
    # below are unchanged rather than updated: **R7 clause 1 DEMOTED
    # corpora/l6battery to an ungated diagnostic**, so the same §5 L6 clause is
    # now authorized on one artifact (battery-b, below) and diagnostic on this
    # one, and the registry says so in its own structure by the ABSENCE of a
    # ruling here. DEMOTED_DIAGNOSTICS below makes that absence machine-checked:
    # giving these rows a ruling back — re-promoting the artifact by editing the
    # registry — is RED.
    #
    # The demotion's cause is round 1's own §6, recorded verbatim in R7: n_neg > 0
    # held here FOR THE DECLARED READING and not against an arbitrary reader,
    # because §8.7 injects every murk defect by visible construction and a
    # stream-only rule recovers each family exactly. Nothing is retired: the
    # arithmetic below still runs, still asserts every recorded figure on
    # corpora/l6battery, and is still green.
    #
    # R5 IS ALREADY IN FORCE ON THESE CLAUSES AND IS DELIBERATELY NOT CITED HERE.
    # Clause 2 is forward-binding in its own words *"because Layer 6 needs it
    # immediately (Brier<=40 and ECE<=30 are both minimizing)"*, and clause 1
    # already carries B=1000 as an identity — so R5 governs how these constants
    # are READ without any entry of its own, and the Stage-A arithmetic discharges
    # R2 obligation 2 over the conjunction under it.
    ("ascension/l6/t_attainability.py", "GATE_BRIER", 40,
     (_s5("Brier≤40"),),
     "§5 L6 calibration, unchanged; a MINIMIZING clause with ceiling 0, read "
     "direction-aware under R5 clause 2 — which is cited in ATTAINABILITY.md and "
     "not here, because R5 authorizes a reading and this entry records that no "
     "ruling authorizes a substrate. It is the clause the battery's size was "
     "chosen to make load-bearing: both named constants fail it (45 and 43)"),
    ("ascension/l6/t_attainability.py", "GATE_ECE", 30,
     (_s5("ECE≤30"),),
     "§5 L6 calibration, unchanged; MINIMIZING, ceiling 0. Measured to "
     "discriminate against NOTHING — a base-rate constant confidence puts every "
     "answer in one bin whose mean confidence is its own accuracy, so it scores "
     "0 with no model at all. Recorded rather than repaired: R5 clause 2's "
     "conjunction reading is what carries the obligation past it"),
    ("ascension/l6/t_attainability.py", "GATE_AUROC", 900,
     (_s5("AUROC≥900"),),
     "§5 L6 calibration, unchanged; the only clause both named constants fail by "
     "arithmetic rather than by margin (a constant ranks nothing, every pair "
     "ties, ties count half, AUROC = 1/2 exactly). It is also the clause §3.4 "
     "leaves UNDEFINED at n_neg = 0, which is the whole of the Layer-6 collision "
     "and RULING-R7-DRAFT.md clause 3's question"),
    ("ascension/l6/t_attainability.py", "GATE_F", 950,
     (_s5("abstention-aware F≥950"),),
     "§5 L6 fidelity, unchanged, under the LITERAL §3.0 table — R3 does not reach "
     "Layer 6 in its own text and no extension is requested, the exhibited "
     "witness clearing it at 955. It is what forbids abstaining out of the "
     "commitment class: 1000w + 900a <= 50 is a 50-permille budget spent at 900 "
     "per hedge, and the key-blind abstainer measures 829"),
    ("ascension/l6/t_attainability.py", "GATE_B", 1000,
     (_s5("B=1000"),),
     "§5 L6 budget; the identity in this registry since Layer 1, carried by R5 "
     "clause 1's regularization without needing an entry here. Attained rather "
     "than approached: the battery is scored in budget at DEFAULT_BUDGET with "
     "refused = 0, and §5 L6 states no footprint clause at all"),
    ("ascension/l6/t_attainability.py", "CEILING_AUROC", 600,
     (_s5("capped AUROC ≤ 600"),),
     "§5 L6 humility ceiling, unchanged and NOT APPLIED — trials/humility/l6/ "
     "does not exist and R2's standing order puts the trials after the "
     "arithmetic. It is declared because the attainability arithmetic measures "
     "the capped engine against it: make_engine(5) emits {0, 1000} through §7.2 "
     "itself and scores AUROC 500, so the ceiling is neither breached nor "
     "vacuous — README-l5 §4's stated seam, closed by the battery's commitment "
     "class"),

    # Layer 6, Stage A ROUND 2 — THE BINDING ARTIFACT. The SAME six ratified
    # numbers, declared a second time by the round-2 arithmetic on
    # corpora/l6batteryb, and now carrying **R7** beside their §5 L6 clause.
    #
    # R7 clause 1 binds BOTH sides of the Layer-6 gate — ascension and humility
    # together, for R6 clause 1's reason — to corpora/l6batteryb, and in the same
    # clause demotes corpora/l6battery. So two copies of one §5 clause sit in this
    # registry with different authorities, which is exactly what it is for: the
    # value check keeps them from drifting apart, and the ruling column records
    # which artifact each is authorized on.
    #
    # WHAT R7 AUTHORIZES IS THE SUBSTRATE AND THE n/a LAW, NOT THE READING, and
    # the two are kept distinct here as the R6 session kept R5 and R6. R5 governs
    # how R2's obligations are discharged at this layer without an entry of its
    # own — clause 2 forward-binding in its own words *"because Layer 6 needs it
    # immediately"*, clause 1 carrying B=1000 as the identity it has been since
    # Layer 1, clause 3 the declared policy class, clause 4 the pricing. R7 adds
    # the artifact, the calibration denominator, AUROC's domain, and the two
    # readings (exact-not-permille; the ECE bin index).
    ("ascension/l6/t_attainability_b.py", "GATE_BRIER", 40,
     (_s5("Brier≤40"), _ruling("R7")),
     "§5 L6 calibration, unchanged; MINIMIZING, read direction-aware under R5 "
     "clause 2. On battery-b it is the clause the band's UPPER end keeps "
     "load-bearing — both named constants fail it (45 and 43) and the honest "
     "committer clears it at 23 by pricing the forcing region at the tie's own "
     "confidence of 500. R7 clause 1 binds it to corpora/l6batteryb, and clause "
     "4 rules the bound EXACT (40/1000) rather than permille"),
    ("ascension/l6/t_attainability_b.py", "GATE_ECE", 30,
     (_s5("ECE≤30"), _ruling("R7")),
     "§5 L6 calibration, unchanged; MINIMIZING. Still discriminates against "
     "NOTHING, but round 1's ORDERING IS REVERSED and the reversal is recorded: "
     "the witness's bins agree with themselves exactly (bin 5 at 500 against an "
     "accuracy of one half, which is the tie's own arithmetic) so it attains 0 "
     "and the base-rate constant no longer beats a real model. R7 clause 1 binds "
     "it to corpora/l6batteryb; clause 5 rules the BIN INDEX the witness's "
     "ECE = 0 depends on — bin(conf) = 9 if conf == 1000 else conf // 100"),
    ("ascension/l6/t_attainability_b.py", "GATE_AUROC", 900,
     (_s5("AUROC≥900"), _ruling("R7")),
     "§5 L6 calibration, unchanged; the clause §3.4 leaves UNDEFINED at "
     "n_neg = 0. R7 clause 3 rules that domain: n/a DISQUALIFIES rather than "
     "excuses (a gate is an instrument and declines to certify what it cannot "
     "measure), and a gate citing AUROC binds only where both classes non-empty "
     "is a THEOREM — which battery-b's forcing region supplies, the coin being "
     "withheld and the stream byte-identical under its complement, so n_neg = "
     "100 for every committing reader definable from the stream. R7 clause 1 "
     "binds it to that artifact"),
    ("ascension/l6/t_attainability_b.py", "GATE_F", 950,
     (_s5("abstention-aware F≥950"), _ruling("R7")),
     "§5 L6 fidelity, unchanged, under the LITERAL §3.0 table — R3 does not "
     "reach Layer 6 and R7 requests no extension. On battery-b it is the clause "
     "that KILLS the detect-and-abstain hedger outright at 918, under BOTH "
     "readings of `n/a`: hedging the region costs 90 permille out of a "
     "50-permille budget, so no policy clearing F can reach n_neg = 0 (floor 87). "
     "R7 clause 1 binds it; clause 3(c) records the window that keeps a future "
     "artifact's region large enough for this clause to price hedging out"),
    ("ascension/l6/t_attainability_b.py", "GATE_B", 1000,
     (_s5("B=1000"), _ruling("R7")),
     "§5 L6 budget; the identity in this registry since Layer 1, carried by R5 "
     "clause 1's regularization. Attained rather than approached: battery-b is "
     "scored in budget at DEFAULT_BUDGET with refused = 0, and §5 L6 states no "
     "footprint clause at all — which R7 states again in its own text, creating "
     "none. R7 clause 1 binds the whole gate, this clause included"),
    ("ascension/l6/t_attainability_b.py", "CEILING_AUROC", 600,
     (_s5("capped AUROC ≤ 600"), _ruling("R7")),
     "§5 L6 humility ceiling, unchanged and NOT APPLIED HERE — "
     "trials/humility/l6/ does not exist and R2's standing order puts the trials "
     "after the arithmetic. R7 clause 1 binds this ceiling to "
     "corpora/l6batteryb in the SAME clause as the gate, because a ceiling "
     "measured on one artifact beside a gate cleared on another is two facts "
     "about two worlds: make_engine(5) emits {0, 1000} through §7.2 itself and "
     "scores AUROC 500 there, neither breached nor vacuous, bought by a query "
     "class the engine cannot get right FOR ANY READING"),
)


# --- the demoted diagnostics (R7 clause 1, in the R1 clause 5 / R4 clause 1 form)
#
# A corpus is retired only by ceasing to gate on it, never by changing its bytes.
# When a ruling demotes an artifact, the registry records it by the ABSENCE of a
# ruling beside that artifact's copies of the §5 clause — and an absence is not a
# check unless something asserts it. This is that assertion: the named file's
# constants must carry their §5 clause and NO BOUNDARY-RULINGS.md entry at all, so
# RE-PROMOTING a demoted artifact by editing this registry is red.
#
# (file, the entry that demoted it, why)

DEMOTED_DIAGNOSTICS = (
    ("ascension/l6/t_attainability.py", "R7",
     "corpora/l6battery, DEMOTED to an ungated diagnostic by R7 clause 1 — the "
     "fourth substrate kill, after l3stream (R1 clause 1) and the chronicle "
     "family (R4 clause 1). Its cause is round 1's own measurement, recorded "
     "verbatim in the entry: n_neg > 0 held there FOR THE DECLARED READING and "
     "not against an arbitrary reader. Its bytes, its generator and both trials "
     "that score it are untouched and still green; what it lost is authority"),
)


# --- helpers ----------------------------------------------------------------

def _read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def _entries():
    """The ruling IDs and titles, in file order."""
    return ENTRY_HEADING.findall(_read_text(RULINGS_PATH))


def _git(*args):
    """Run a git command at the project root; return (returncode, stdout bytes)."""
    proc = subprocess.run(("git",) + args, cwd=PROJECT_ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout


def _module_gate_constants(path):
    """Module-level `GATE_*` / `CEILING_*` integers in one file, read by `ast`.

    Parsed, never imported: this must work on a trial module whose imports would
    fail, and it must read what the file *says* rather than what a run produces.
    """
    tree = ast.parse(_read_bytes(path), filename=path)
    found = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            if not target.id.startswith(CONST_PREFIXES):
                continue
            value = node.value
            require(isinstance(value, ast.Constant) and isinstance(value.value, int)
                    and not isinstance(value.value, bool),
                    "%s: gate constant %s is not an integer literal — a gate must "
                    "be a plain integer a human can read against §5"
                    % (os.path.relpath(path, TRIALS_DIR), target.id))
            found[target.id] = value.value
    return found


def _all_trial_files():
    paths = []
    for dirpath, _dirs, files in os.walk(TRIALS_DIR):
        for fname in sorted(files):
            if fname.endswith(".py"):
                paths.append(os.path.join(dirpath, fname))
    return sorted(paths)


# --- 1. the supplement exists and is well-formed ----------------------------

def trial_boundary_rulings_exists_and_is_well_formed():
    require(os.path.exists(RULINGS_PATH),
            "BOUNDARY-RULINGS.md is missing — the rulings the trials cite have no "
            "document to live in")
    text = _read_text(RULINGS_PATH)
    # Prose wraps; the declarations are matched on whitespace-normalized text so
    # a reflowed paragraph is not mistaken for a deleted promise.
    flat = " ".join(text.split())

    require("Append-only" in flat and "frozen the moment it is committed" in flat,
            "BOUNDARY-RULINGS.md no longer declares itself append-only and its "
            "entries frozen on commit — the declaration this law enforces")
    require("does not amend it and cannot" in flat,
            "BOUNDARY-RULINGS.md no longer states its subordination to "
            "BOUNDARY.md — a supplement that may amend the constitution is not a "
            "supplement, and BOUNDARY.md has no amendment mechanism")

    entries = _entries()
    require(len(entries) >= 3,
            "BOUNDARY-RULINGS.md holds %d entries; R1-R3 are cited by the Layer-3 "
            "trials and by this registry" % (len(entries),))
    for i, (entry_id, title) in enumerate(entries, start=1):
        require_equal(entry_id, "R%d" % i,
                      "ruling IDs must run contiguously from R1 in file order "
                      "(append-only: never renumbered, never reused)")
        require(title.strip() != "", "%s has an empty title" % (entry_id,))

    # Every entry declares that it is frozen, and what it holds.
    for entry_id, _title in entries:
        body = _entry_body(text, entry_id)
        require("**Status:** FROZEN on commit." in body,
                "%s does not declare its frozen status" % (entry_id,))
        require("**Holding:**" in body,
                "%s does not state a one-line holding" % (entry_id,))


def _entry_body(text, entry_id):
    """The text of one entry: from its heading to the next entry heading or EOF."""
    starts = [(m.group(1), m.start()) for m in ENTRY_HEADING.finditer(text)]
    for i, (found, pos) in enumerate(starts):
        if found != entry_id:
            continue
        end = starts[i + 1][1] if i + 1 < len(starts) else len(text)
        return text[pos:end]
    raise AssertionError("no entry %s in BOUNDARY-RULINGS.md" % (entry_id,))


# --- 2. append-only, against git history ------------------------------------

def trial_append_only_ledgers_are_append_only_in_git_history():
    if not os.path.isdir(os.path.join(PROJECT_ROOT, ".git")):
        skip("no .git directory — history cannot be checked from a source export")
    code, _out = _git("rev-parse", "--git-dir")
    if code != 0:
        skip("git is unavailable here; the append-only history check needs a clone")

    for name, history_required in LEDGERS:
        path = os.path.join(PROJECT_ROOT, name)
        require(os.path.exists(path), "append-only ledger missing: %s" % (name,))
        current = _read_bytes(path)

        code, out = _git("log", "--format=%H", "--", name)
        require(code == 0, "git log failed for %s" % (name,))
        shas = out.decode("ascii").split()

        if history_required:
            require(len(shas) > 0,
                    "%s has no committed history — the prefix walk below would "
                    "pass vacuously, and this ledger is what proves it does not"
                    % (name,))

        for sha in shas:
            code, blob = _git("show", "%s:%s" % (sha, name))
            require(code == 0, "git show failed for %s at %s" % (name, sha[:12]))
            require(current.startswith(blob),
                    "%s is NOT append-only: the version committed at %s (%d bytes) "
                    "is not a byte-exact prefix of the current file (%d bytes) — "
                    "something already written was rewritten or removed "
                    "(BOUNDARY.md §9.2, CLAUDE.md §5)"
                    % (name, sha[:12], len(blob), len(current)))


# --- 3. every gate a trial applies is authorized ----------------------------

def trial_every_gate_binding_matches_section5_or_a_ruling():
    boundary = _read_text(BOUNDARY_PATH)
    rulings = _read_text(RULINGS_PATH)
    ruling_ids = set(entry_id for entry_id, _title in _entries())
    documents = {"BOUNDARY.md": boundary, "BOUNDARY-RULINGS.md": rulings}

    for rel, const, value, authorities, note in AUTHORIZED_GATES:
        path = os.path.join(TRIALS_DIR, rel)
        require(os.path.exists(path),
                "registry names a trial file that does not exist: %s" % (rel,))
        actual = _module_gate_constants(path).get(const)
        require(actual is not None,
                "%s no longer defines %s — the registry entry authorizing it is "
                "stale, and a gate must not lose its recorded authority silently"
                % (rel, const))
        require_equal(actual, value,
                      "%s::%s drifted from its authorized value (%s)"
                      % (rel, const, note))

        require(len(authorities) > 0,
                "%s::%s claims no authority at all" % (rel, const))
        for doc, clause in authorities:
            if doc == "BOUNDARY-RULINGS.md":
                require(clause in ruling_ids,
                        "%s::%s cites %s, which is not an entry in "
                        "BOUNDARY-RULINGS.md" % (rel, const, clause))
            require(clause in documents[doc],
                    "%s::%s claims authority %r from %s, but that text does not "
                    "occur there — the gate is applied without authority"
                    % (rel, const, clause, doc))


def trial_a_demoted_artifacts_constants_carry_no_companion_ruling():
    """The demotion, machine-checked — `R7` clause 1 in the `R4` clause 1 form.

    A demotion is a change of authority and not of bytes, so what makes it real
    is exactly this registry: the demoted artifact's copies of the §5 clause keep
    the clause and lose the ruling, while the binding artifact's copies carry it.
    An absence records nothing unless something asserts it, and this asserts it —
    a registry edit that handed those rows a ruling back would RE-PROMOTE the
    artifact silently, so it goes red here instead.
    """
    ruling_ids = set(entry_id for entry_id, _title in _entries())
    for rel, entry, why in DEMOTED_DIAGNOSTICS:
        require(entry in ruling_ids,
                "%s is recorded as demoted by %s, which is not an entry in "
                "BOUNDARY-RULINGS.md" % (rel, entry))
        rows = [row for row in AUTHORIZED_GATES if row[0] == rel]
        require(len(rows) > 0,
                "the registry names %s as a demoted diagnostic but authorizes no "
                "constant in it — the demotion has nothing to be about" % (rel,))
        for _rel, const, _value, authorities, _note in rows:
            cited = [clause for doc, clause in authorities
                     if doc == "BOUNDARY-RULINGS.md"]
            require(not cited,
                    "%s::%s cites %s, but that artifact is an UNGATED DIAGNOSTIC "
                    "(%s). A ruling beside a constant is what authorizes a gate "
                    "to bind; restoring one here re-promotes a demoted artifact "
                    "without a ruling that says so"
                    % (rel, const, ", ".join(cited), why))


def trial_no_trial_applies_an_undeclared_gate():
    """Completeness: no `GATE_*` / `CEILING_*` constant escapes the registry.

    Without this, the registry would authorize only what it already knows about
    and a new unauthorized gate could simply not be listed. With it, declaring a
    gate constant is what makes it discoverable, so the only way to add a gate is
    to give it an authority.
    """
    declared = set((rel, const) for rel, const, _v, _a, _n in AUTHORIZED_GATES)
    undeclared = []
    for path in _all_trial_files():
        rel = os.path.relpath(path, TRIALS_DIR).replace(os.sep, "/")
        for const, value in sorted(_module_gate_constants(path).items()):
            if (rel, const) not in declared:
                undeclared.append("%s::%s = %d" % (rel, const, value))
    require(not undeclared,
            "these gate constants are applied by trials but authorized by "
            "nothing — add each to AUTHORIZED_GATES with its §5 clause or its "
            "BOUNDARY-RULINGS.md entry: %s" % ", ".join(undeclared))

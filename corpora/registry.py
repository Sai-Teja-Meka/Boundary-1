"""corpora/registry.py — the catalogue the byte-match law trial iterates.

GENERATED : modules exposing FROZEN_PATH + frozen_bytes() (byte-match law, §8.3).
MURK      : the murk module, additionally exposing GROUND_TRUTH_PATH +
            ground_truth_bytes() (its answer key is frozen and byte-matched too).
REAL      : real-data corpora, exempt from byte-match, bound by SHA-256 checksum
            (the real-data rule, §8.8). Empty from Phase 0 to Layer 4; the
            byte-match trial carried the checksum branch ready the whole time,
            and the `[L4] [PACKAGE]` session filled it with the first entry —
            `corpora/real-sessions/v1`, a frozen snapshot of this project's own
            accumulated dogfood store (`corpora/real_sessions.py` is its loader
            and its scrub; the hyphenated data directory is not importable).

GENERATED currently holds eight: chronicle, sessions, murk, l3stream, l3streamb,
l4stream, l5stream, l6battery.

l6battery is the odd one and is listed deliberately. It is a **query set**, not an
event stream: its substrate is the frozen murk corpus and its answer keys are
derived from murk's frozen ground_truth.json, which is the artifact §8.7 mandates.
It is admitted here because §8.3's byte-match law is what a frozen generator
output needs whether its records are events or queries, and an attainability
arithmetic that rested on a battery which could drift would rest on nothing. It
was frozen by the Layer-6 Stage-A session and **NO Layer-6 gate binds on it**:
trials/ascension/l6/ATTAINABILITY.md computes the arithmetic and
RULING-R7-DRAFT.md awaits human ratification (BOUNDARY.log line 36).

  One consequence of that admission is recorded here rather than left to be
  rediscovered. The FROZEN Layer-5 trial ascension/l5/t_prospection.py::
  trial_one_caller_ingest_advances_next_t_by_exactly_one_on_an_intention_free_
  stream quantifies over this list and reads each member as JSONL, requiring
  l5stream to be the only corpus carrying an `intend` payload. l6battery is a
  single canonical JSON object, so it reads there as ONE line carrying no
  `intend` payload — the theorem that trial asserts stays true and is still
  correctly checked, and the frozen trial is not edited (§9.2). What the seam
  costs is that its `total > 0` guard is satisfied trivially for this member;
  what it would cost to avoid is editing a frozen trial, which is not a trade
  this project makes.

l3stream and l3streamb are both frozen and both scored — l3streamb is the Layer-3
ascension gate's binding corpus and l3stream its ungated diagnostic, per
BOUNDARY-RULINGS.md R1. l4stream is the Layer-4 consolidation corpus, frozen by
the Layer-4 Stage-A attainability session: the chronicle family's grammar
redundancy (1.197 assertions per (entity,key) pair) cannot admit the ratified
footprint gate under any policy, and l4stream supplies the redundancy the gate
presupposes — the arithmetic and the proposed binding are in
trials/ascension/l4/ATTAINABILITY.md and its R4 ruling draft. R4 has since
ratified that binding and Layer 4 is claimed.

l5stream is the Layer-5 prospection corpus, frozen by the Layer-5 Stage-A
attainability session: the `l4stream` world plus an `intend` event kind carrying a
condition AST over a closed, guarded predicate vocabulary, so that satisfaction
points are computable exactly from the frozen bytes with no engine in the loop
(corpora/l5stream/grammar.md). It is scored by trials/ascension/l5/ but **no
Layer-5 gate binds on it**: the arithmetic in that directory's ATTAINABILITY.md
found a constitutional collision between §5 L5's identity gate and R2's
strictly-below obligation, and RULING-R5-DRAFT.md awaits human ratification.

  Note added 2026-08-01 ([L5] [PULSE]). The two sentences above were true when
  written and are no longer, and this is where they stop. R5 is ratified and
  settles the READING (an identity clause discharges R2 obligation 1 by an
  exhibited attainment; a minimizing clause is read direction-aware and over the
  gate's conjunction); R6 clause 1 then binds BOTH sides of the Layer-5 gate --
  ascension and humility together -- to corpora/l5stream, and R6 clause 4 rules
  its budget_cap = raw_cells // 4 = 45638. Layer 5 is CLAIMED (BOUNDARY.log line
  32): the gate is cleared on this corpus at trigger-precision 1000, trigger-
  recall 1000, dup-fire 0, miss 0, F 1000 against 980, B 1000, at 250 permille.
  Nothing about the corpus itself moved -- same seed, same bytes, same grammar --
  and l5stream has no ungated diagnostic family in the R1-clause-5 shape, because
  no other frozen corpus carries an intend payload at all (R6 clause 1), so on
  them every Layer-5 measure is undefined rather than low.

  Note added 2026-08-01 ([L5] [ASCEND], Layer-6 Stage A ROUND 2). GENERATED now
  holds NINE: corpora/l6batteryb — battery-b — joins it, and the header's
  "currently holds eight" stops holding here rather than being rewritten.
  battery-b is
  the round-2 artifact and it exists because of a limit round 1 MEASURED on
  l6battery: §8.7 injects every murk defect by visible construction, so a
  stream-only rule recovers each family exactly and l6battery's n_neg > 0 held
  only RELATIVE TO the declared latest-wins reading (a first-wins reader would
  have answered its whole commitment class correctly and taken AUROC with it).
  battery-b removes that: its forcing region is 100 mirror pairs whose two
  members are observationally identical and whose truths sit at opposite ends of
  their chains, with the resolving coin WITHHELD at generation — the stream is
  byte-identical under the coin's complement — so n_neg = 100 is a THEOREM for
  every committing reader definable from the stream. It is one canonical JSON
  object carrying the substrate, the answer key and the query set together,
  because the guarantee is a joint property of the three and three separately
  byte-matched files could be paired across generations and lose it. The l6battery
  seam recorded above applies to it identically (one line, no `intend` payload,
  the frozen Layer-5 theorem still true and still checked).

  NO LAYER-6 GATE BINDS ON EITHER ARTIFACT. trials/ascension/l6/ATTAINABILITY-B.md
  computes the round-2 arithmetic and trials/ascension/l6/RULING-R7-DRAFT.md
  asks a human to bind battery-b and to DEMOTE l6battery to an ungated
  diagnostic; appending a ruling is what freezes, and this session does not
  append, so the demotion is proposed here and executed at ratification.

  Note added 2026-08-02 ([L5] [RULING], R7 recorded). The paragraph above was
  true when written and this is where it stops. R7 is ratified and appended, and
  it does both things that paragraph left to a human. Clause 1 binds BOTH sides
  of the Layer-6 gate -- ascension and humility together, for R6 clause 1's
  reason -- to corpora/l6batteryb, where the upper side is EXHIBITED (a
  confidence assignment reading structural evidence only, at Brier 23 / ECE 0 /
  AUROC 976 / F 955 / B 1000 against <=40 / <=30 / >=900 / >=950 / =1000) and no
  named capability-free policy clears the conjunction. AND IT DEMOTES
  corpora/l6battery TO AN UNGATED DIAGNOSTIC -- the FOURTH substrate kill, after
  l3stream (R1 clause 1) and the chronicle family (R4 clause 1), and the first
  performed on an artifact this project froze ONE SESSION EARLIER. The cause is
  round 1's own measurement, recorded verbatim in the entry: n_neg > 0 held there
  FOR THE DECLARED READING and not against an arbitrary reader, because §8.7
  injects every murk defect by visible construction and a stream-only rule
  recovers each family exactly -- on murk, evidence that ranks also resolves.
  battery-b replaces that proviso with a theorem: its forcing region is 100
  mirror pairs whose members are observationally identical, the resolving coin is
  withheld, and the stream is byte-identical under the coin's complement, so
  n_neg = 100 for EVERY committing reader definable from the stream.

  NOTHING ABOUT EITHER ARTIFACT MOVED: same seeds, same bytes, same generators,
  same trials. A demotion is a change of AUTHORITY and not of bytes (R4 clause
  1's form, which kept chronicle and murk), so trials/ops/l6/t_l6battery.py and
  trials/ascension/l6/t_attainability.py keep computing and keep running green,
  and what l6battery remains is on the record: the artifact that first gave §3.4
  a denominator at all, and the diagnostic against which battery-b's arithmetic
  is read. laws/t_rulings.py records the demotion in its own structure -- the six
  battery-b constants carry R7 beside their §5 L6 clause, the six l6battery
  copies carry the §5 clause and NO ruling -- and a registry edit that gave them
  one back turns that file red.

  Note added 2026-08-03 ([L6] [ASCEND], Layer-7 Stage A). GENERATED now holds
  TEN: corpora/l7compose joins it, and the header's "currently holds eight" and
  the "now NINE" note above both stop holding here rather than being rewritten.
  It exists because of a limit this session MEASURED across every other member
  of this list. §5 L7's novelty clause is *"provably never-stored"*, so a gate
  citing it can only bind where some query's correct answer is NOT in the
  stream; and across 85 954 answerable queries drawn from the frozen batteries
  these artifacts already carry — chronicle, sessions, murk, l3stream,
  l3streamb, l4stream, l5stream, l6battery, l6batteryb, and §8.8's
  real-sessions/v1 — NOT ONE answer is absent from its own stream. §8.7's *dirt
  is always paired with the answer key* is exactly why: an answer key that names
  the t's it touches cannot force a composition. So on every existing artifact
  the generation-required class is EMPTY, tagging's denominator is empty, and a
  gate citing it measures nothing. That is the FIFTH SUBSTRATE KILL — after
  l3stream (R1 clause 1), the chronicle family (R4 clause 1) and l6battery (R7
  clause 1) — and it is the first that falls on the WHOLE existing stock rather
  than on one artifact. NOTHING IS DEMOTED and no byte moves: nothing here was
  ever a Layer-7 candidate, so what is recorded is a refusal to bind, in the
  form R4 clause 1 used for the chronicle family.

  corpora/l7compose is what that forces: a closed compositional grammar with a
  WITHHELD ITEM. A compound is formed from two components by two `part`
  assertions, a declared rule determines its `profile` from their material, and
  for half the mirror pairs the generator emits that profile while for the other
  half it withholds it — under a BALANCED COIN, with both members asked by the
  same cue in the same shape. So the class is not readable from the query
  (Theorem 1: every labeller that does not consult the store mislabels exactly
  one member of every pair, exhibited against a bench of six), the composed item
  is provably never stored (Theorem 2: exhaustive canonical-byte comparison
  against all 12 000 payloads), and the two members compose to the SAME item but
  for its `entity` field, so the value is never the signal. It also carries the
  three-generation ladder §6's mandatory self-pollution strain will stand on,
  with lineage depth decidable from the frozen bytes.

  NO LAYER-7 GATE BINDS ON IT. trials/ascension/l7/ATTAINABILITY.md computes the
  arithmetic and trials/ascension/l7/RULING-R8-DRAFT.md asks a human to bind it;
  appending a ruling is what freezes, and that session does not append. The
  l6battery seam recorded above applies to this member identically (one line, no
  `intend` payload, the frozen Layer-5 theorem still true and still checked).

Nothing is edited; a corpus is retired only by ceasing to gate on it, never by
changing its bytes.

Each REAL entry is: {"name": str, "path": str (absolute), "sha256": hex str}.
"""

from corpora import real_sessions
from corpora.chronicle import generator as chronicle_gen
from corpora.l6battery import generator as l6battery_gen
from corpora.l6batteryb import generator as l6batteryb_gen
from corpora.l7compose import generator as l7compose_gen
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen
from corpora.l3stream import generator as l3stream_gen
from corpora.l3streamb import generator as l3streamb_gen
from corpora.l4stream import generator as l4stream_gen
from corpora.l5stream import generator as l5stream_gen

GENERATED = [chronicle_gen, sessions_gen, murk_gen, l3stream_gen, l3streamb_gen,
             l4stream_gen, l5stream_gen, l6battery_gen, l6batteryb_gen,
             l7compose_gen]

MURK = murk_gen

REAL = real_sessions.real_entries()

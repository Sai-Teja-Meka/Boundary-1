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

GENERATED currently holds seven: chronicle, sessions, murk, l3stream, l3streamb,
l4stream, l5stream.

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

Nothing is edited; a corpus is retired only by ceasing to gate on it, never by
changing its bytes.

Each REAL entry is: {"name": str, "path": str (absolute), "sha256": hex str}.
"""

from corpora import real_sessions
from corpora.chronicle import generator as chronicle_gen
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen
from corpora.l3stream import generator as l3stream_gen
from corpora.l3streamb import generator as l3streamb_gen
from corpora.l4stream import generator as l4stream_gen
from corpora.l5stream import generator as l5stream_gen

GENERATED = [chronicle_gen, sessions_gen, murk_gen, l3stream_gen, l3streamb_gen,
             l4stream_gen, l5stream_gen]

MURK = murk_gen

REAL = real_sessions.real_entries()

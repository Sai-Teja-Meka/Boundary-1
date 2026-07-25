"""corpora/registry.py — the catalogue the byte-match law trial iterates.

GENERATED : modules exposing FROZEN_PATH + frozen_bytes() (byte-match law, §8.3).
MURK      : the murk module, additionally exposing GROUND_TRUTH_PATH +
            ground_truth_bytes() (its answer key is frozen and byte-matched too).
REAL      : real-data corpora, exempt from byte-match, bound by SHA-256 checksum
            (the real-data rule, §8.8). Still empty as of L3; the byte-match trial
            already handles the checksum branch so it is ready when one arrives.

GENERATED currently holds six: chronicle, sessions, murk, l3stream, l3streamb,
l4stream.

l3stream and l3streamb are both frozen and both scored — l3streamb is the Layer-3
ascension gate's binding corpus and l3stream its ungated diagnostic, per
BOUNDARY-RULINGS.md R1. l4stream is the Layer-4 consolidation corpus, frozen by
the Layer-4 Stage-A attainability session: the chronicle family's grammar
redundancy (1.197 assertions per (entity,key) pair) cannot admit the ratified
footprint gate under any policy, and l4stream supplies the redundancy the gate
presupposes — the arithmetic and the proposed binding are in
trials/ascension/l4/ATTAINABILITY.md and its R4 ruling draft. Until a human
ratifies that binding, no Layer-4 gate binds on anything.

Nothing is edited; a corpus is retired only by ceasing to gate on it, never by
changing its bytes.

Each REAL entry is: {"name": str, "path": str (absolute), "sha256": hex str}.
"""

from corpora.chronicle import generator as chronicle_gen
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen
from corpora.l3stream import generator as l3stream_gen
from corpora.l3streamb import generator as l3streamb_gen
from corpora.l4stream import generator as l4stream_gen

GENERATED = [chronicle_gen, sessions_gen, murk_gen, l3stream_gen, l3streamb_gen,
             l4stream_gen]

MURK = murk_gen

REAL = []

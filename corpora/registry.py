"""corpora/registry.py — the catalogue the byte-match law trial iterates.

GENERATED : modules exposing FROZEN_PATH + frozen_bytes() (byte-match law, §8.3).
MURK      : the murk module, additionally exposing GROUND_TRUTH_PATH +
            ground_truth_bytes() (its answer key is frozen and byte-matched too).
REAL      : real-data corpora, exempt from byte-match, bound by SHA-256 checksum
            (the real-data rule, §8.8). Empty at Phase 0; the byte-match trial
            already handles the checksum branch so it is ready when one arrives.

Each REAL entry is: {"name": str, "path": str (absolute), "sha256": hex str}.
"""

from corpora.chronicle import generator as chronicle_gen
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen

GENERATED = [chronicle_gen, sessions_gen, murk_gen]

MURK = murk_gen

REAL = []

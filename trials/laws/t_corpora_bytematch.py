"""laws/ — corpora byte-match (BOUNDARY.md §8.3) and the real-data checksum
rule (§8.8).

Every generated corpus must regenerate byte-for-byte from its (seed, scale).
The murk answer key is frozen and byte-matched too. Real-data corpora (none at
Phase 0) are exempt from byte-match and bound instead by a SHA-256 checksum.
"""

import hashlib
import os

from _harness import require
from corpora import registry


def trial_generated_corpora_bytematch():
    for module in registry.GENERATED:
        path = module.FROZEN_PATH
        require(os.path.exists(path), f"frozen corpus missing: {path}")
        with open(path, "rb") as fh:
            frozen = fh.read()
        regenerated = module.frozen_bytes()
        require(frozen == regenerated,
                f"byte-match FAILED for {os.path.basename(path)} "
                f"(frozen {len(frozen)}B vs regenerated {len(regenerated)}B)")


def trial_murk_ground_truth_bytematch():
    m = registry.MURK
    with open(m.GROUND_TRUTH_PATH, "rb") as fh:
        frozen = fh.read()
    require(frozen == m.ground_truth_bytes(),
            "murk ground_truth.json does not match its regenerated answer key")


def trial_real_data_checksums():
    for entry in registry.REAL:
        path = entry["path"]
        require(os.path.exists(path), f"real-data corpus missing: {path}")
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        require(digest == entry["sha256"],
                f"checksum mismatch for real-data corpus {entry['name']}: "
                f"{digest} != {entry['sha256']}")

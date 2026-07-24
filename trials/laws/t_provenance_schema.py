"""laws/ — the provenance-tag schema validator (BOUNDARY.md §4.2).

The provenance law is dormant until Layer 7, but its schema and its validator are
defined and exercised now, so that when the law binds there is no ambiguity about
what a valid provenance tag is. This trial checks the validator against a battery
of known-valid and known-invalid tags.

Schema (§4.2):
  {
    "support": [<int t>, ...],   # strictly ascending, non-negative, each an
                                 # actually-ingested t; empty ONLY if kind=="absent"
    "kind": "recall"|"aggregate"|"derive"|"absent",
    "t_asof": <int >= 0>
  }
"""

from _harness import require

KIND_VOCAB = ("recall", "aggregate", "derive", "absent")
_REQUIRED_KEYS = frozenset({"support", "kind", "t_asof"})


def _is_plain_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def validate_provenance(tag, ingested_max):
    """Return (ok, reason). `ingested_max` is the largest ingested event t."""
    if not isinstance(tag, dict):
        return False, "tag is not an object"
    if frozenset(tag.keys()) != _REQUIRED_KEYS:
        return False, f"keys must be exactly {sorted(_REQUIRED_KEYS)}"
    kind = tag["kind"]
    if kind not in KIND_VOCAB:
        return False, f"kind not in vocabulary: {kind!r}"
    t_asof = tag["t_asof"]
    if not _is_plain_int(t_asof):
        return False, "t_asof must be a plain integer"
    if not (0 <= t_asof <= ingested_max):
        return False, "t_asof out of ingested range"
    support = tag["support"]
    if not isinstance(support, list):
        return False, "support must be an array"
    if len(support) == 0 and kind != "absent":
        return False, "support may be empty only when kind == 'absent'"
    prev = -1
    for t in support:
        if not _is_plain_int(t):
            return False, "support entries must be plain integers"
        if t < 0 or t > ingested_max:
            return False, "support entry out of ingested range"
        if t <= prev:
            return False, "support must be strictly ascending with no duplicates"
        prev = t
    return True, "ok"


_MAX = 100

_VALID = [
    {"support": [0, 1, 2], "kind": "recall", "t_asof": 2},
    {"support": [5], "kind": "aggregate", "t_asof": 10},
    {"support": [3, 7, 99], "kind": "derive", "t_asof": 100},
    {"support": [], "kind": "absent", "t_asof": 4},
    {"support": [12, 40], "kind": "absent", "t_asof": 40},
]

_INVALID = [
    ({"support": [0], "kind": "recall"}, "missing t_asof"),
    ({"support": [0], "kind": "recall", "t_asof": 0, "extra": 1}, "extra key"),
    ({"support": [0], "kind": "guess", "t_asof": 0}, "bad kind"),
    ({"support": [2, 1], "kind": "recall", "t_asof": 2}, "unsorted support"),
    ({"support": [1, 1], "kind": "recall", "t_asof": 2}, "duplicate support"),
    ({"support": [-1], "kind": "recall", "t_asof": 0}, "negative t"),
    ({"support": [999], "kind": "recall", "t_asof": 0}, "support out of range"),
    ({"support": [], "kind": "recall", "t_asof": 0}, "empty support, non-absent"),
    ({"support": [0], "kind": "recall", "t_asof": 1.0}, "float t_asof"),
    ({"support": [True], "kind": "recall", "t_asof": 0}, "bool in support"),
    ({"support": [0], "kind": "recall", "t_asof": 101}, "t_asof out of range"),
    ("not-an-object", "non-object tag"),
]


def trial_valid_provenance_tags_pass():
    for tag in _VALID:
        ok, reason = validate_provenance(tag, _MAX)
        require(ok, f"valid provenance tag rejected: {tag} ({reason})")


def trial_invalid_provenance_tags_fail():
    for tag, why in _INVALID:
        ok, _reason = validate_provenance(tag, _MAX)
        require(not ok, f"invalid provenance tag accepted ({why}): {tag}")

"""core/serialize.py — the engine's own canonical serializer (BOUNDARY.md §2.4).

This is core's **own** canonical JSON serializer. `core/` may not import
`corpora/` (§2.6); `corpora/canon.py` was the Phase-0 *reference* implementation.
This module re-implements the SAME spec (§2.4) under the import whitelist (§2.5:
`json` is the only import it needs), and the "engine serializer cross-check" law
trial proves the two agree **byte-for-byte** on every shared fixture.

The contract realized here (§2.4):
  - UTF-8 output bytes, no trailing newline within a single encoded value.
  - Object keys sorted ascending by Unicode code point.
  - Compact separators: item ",", key/value ":".
  - ensure_ascii = False (raw UTF-8).
  - Allowed value types ONLY: str, int, bool, None, list, dict[str -> allowed].
  - float / NaN / Infinity / bytes / set / tuple / custom object are rejected.

There is intentionally **no float path** anywhere in this module (§2.2). `bool`
is a subclass of `int`; both are allowed and render as `true`/`false` and
base-10 integers respectively — float is rejected first, so a bool is never
mistaken for a float.
"""

import json


class NonCanonical(TypeError):
    """A value is not built from the canonical type set of §2.4."""


def check_canonical(value, _path="<root>"):
    """Raise NonCanonical unless `value` is a canonical-allowed structure (§2.4)."""
    if isinstance(value, float):
        raise NonCanonical(f"float is not an allowed canonical type at {_path}")
    if isinstance(value, bytes):
        raise NonCanonical(f"bytes is not an allowed canonical type at {_path}")
    if isinstance(value, (str, bool, int, type(None))):
        return
    if isinstance(value, list):
        for i, item in enumerate(value):
            check_canonical(item, f"{_path}[{i}]")
        return
    if isinstance(value, dict):
        for k, v in value.items():
            if not isinstance(k, str):
                raise NonCanonical(f"object key must be str at {_path}: {k!r}")
            check_canonical(v, f"{_path}.{k}")
        return
    raise NonCanonical(
        f"{type(value).__name__} is not an allowed canonical type at {_path}")


def encode(value):
    """Encode an allowed value to canonical UTF-8 bytes (no trailing newline)."""
    check_canonical(value)
    text = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return text.encode("utf-8")


def _no_float(_literal):
    # json only calls parse_float for a float-shaped literal; canonical bytes
    # never contain one, so encountering it is a hard error, not a float parse.
    raise NonCanonical("float literal encountered while decoding canonical JSON")


def decode(data):
    """Decode canonical UTF-8 bytes (or str) back to a Python value."""
    if isinstance(data, (bytes, bytearray)):
        data = bytes(data).decode("utf-8")
    return json.loads(data, parse_float=_no_float)


def copy_value(value):
    """Return a fresh, structurally-identical copy of a canonical value.

    A pure value-copy: the engine never aliases a caller's mutable input and
    never hands an internal structure back to a caller (purity, §2.1). Scalars
    (str/int/bool/None) are immutable and returned as-is.
    """
    if isinstance(value, list):
        return [copy_value(v) for v in value]
    if isinstance(value, dict):
        return {k: copy_value(v) for k, v in value.items()}
    return value

"""Canonical JSON serialization — the Phase-0 reference implementation.

This implements the canonical serialization spec of BOUNDARY.md §2.4 so that
corpora can be frozen deterministically and the laws/ trials can check
round-tripping. It is *tooling*, not the engine: `core/` will grow its own
serializer later, and the canonical-round-trip law trial will cross-check that
serializer against this spec when it exists.

Rules (BOUNDARY.md §2.4), enforced here:
  - UTF-8 output bytes.
  - Object keys sorted ascending by Unicode code point.
  - Compact separators: item ",", key/value ":".
  - ensure_ascii = False (raw UTF-8).
  - Allowed value types ONLY: str, int, bool, None, list, dict[str -> allowed].
  - Floats (and NaN/Infinity), bytes, sets, tuples, and custom objects are
    rejected with a TypeError.

There is intentionally no float path anywhere in this module.
"""

import json

# Note: bool is a subclass of int in Python; both are allowed by the spec and
# json renders them as true/false and base-10 integers respectively. Float is
# rejected explicitly and first, so a bool is never mistaken for a float.

_ALLOWED_SCALARS = (str, bool, int, type(None))


def _typecheck(value, _path="<root>"):
    """Raise TypeError if `value` is not a canonical-allowed structure."""
    if isinstance(value, float):
        raise TypeError(f"float is not an allowed canonical type at {_path}")
    if isinstance(value, bytes):
        raise TypeError(f"bytes is not an allowed canonical type at {_path}")
    if isinstance(value, (str, bool, int, type(None))):
        return
    if isinstance(value, list):
        for i, item in enumerate(value):
            _typecheck(item, f"{_path}[{i}]")
        return
    if isinstance(value, dict):
        for k, v in value.items():
            if not isinstance(k, str):
                raise TypeError(f"object key must be str at {_path}: {k!r}")
            _typecheck(v, f"{_path}.{k}")
        return
    raise TypeError(f"{type(value).__name__} is not an allowed canonical type at {_path}")


def canon_encode(value):
    """Encode an allowed value to canonical UTF-8 bytes (no trailing newline)."""
    _typecheck(value)
    text = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return text.encode("utf-8")


def canon_decode(data):
    """Decode canonical UTF-8 bytes back to a Python value."""
    if isinstance(data, (bytes, bytearray)):
        data = bytes(data).decode("utf-8")
    return json.loads(data, parse_float=_no_float)


def _no_float(_literal):
    # json only calls parse_float for a float-shaped literal; canonical bytes
    # never contain one, so encountering it is a hard error.
    raise TypeError("float literal encountered while decoding canonical JSON")


def encode_jsonl(events):
    """Encode an iterable of events as canonical JSONL bytes.

    Each event is canonically encoded and followed by a single "\\n". The
    result (including the final newline) is the frozen corpus byte string.
    """
    out = bytearray()
    for event in events:
        out += canon_encode(event)
        out += b"\n"
    return bytes(out)


def decode_jsonl(data):
    """Decode canonical JSONL bytes into a list of events."""
    if isinstance(data, (bytes, bytearray)):
        data = bytes(data).decode("utf-8")
    events = []
    for line in data.split("\n"):
        if line == "":
            continue
        events.append(canon_decode(line))
    return events

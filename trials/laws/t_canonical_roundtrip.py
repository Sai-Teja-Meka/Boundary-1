"""laws/ — canonical JSON round-trip (BOUNDARY.md §2.4).

Verifies the canonical serialization contract: allowed types round-trip, keys
sort, floats are rejected. The engine's own serializer is cross-checked against
this contract once it exists.
"""

from _harness import require, require_equal, try_import
from corpora import canon

_SAMPLES = [
    0,
    -17,
    123456789012345678901234567890,
    "",
    "hello",
    "unicode-safe ascii only",
    True,
    False,
    None,
    [],
    {},
    [1, 2, 3, "a", None, True],
    {"b": 2, "a": 1, "z": [3, {"k": "v"}]},
    {"kind": "attr", "entity": 5, "key": "origin", "val": 42},
    {"nested": {"deep": {"list": [1, "two", {"three": 3}]}}},
]


def trial_roundtrip_allowed_values():
    for x in _SAMPLES:
        encoded = canon.canon_encode(x)
        decoded = canon.canon_decode(encoded)
        require_equal(decoded, x, "round-trip changed value")
        # encode is idempotent on canonical bytes
        require(canon.canon_encode(decoded) == encoded, "encode not idempotent")


def trial_sorted_keys():
    encoded = canon.canon_encode({"c": 1, "a": 2, "b": 3}).decode("utf-8")
    require_equal(encoded, '{"a":2,"b":3,"c":1}', "keys not canonically sorted")


def trial_compact_separators():
    encoded = canon.canon_encode({"a": [1, 2], "b": 3}).decode("utf-8")
    require(" " not in encoded, "canonical form contains insignificant whitespace")
    require(encoded == '{"a":[1,2],"b":3}', "unexpected canonical form")


def trial_reject_floats():
    for bad in (1.5, [1, 2.0], {"k": 0.1}, float("nan")):
        try:
            canon.canon_encode(bad)
        except TypeError:
            continue
        raise AssertionError(f"canonical encoder accepted a float: {bad!r}")


def trial_reject_non_allowed_types():
    for bad in (b"bytes", {1, 2, 3}, (1, 2)):
        try:
            canon.canon_encode(bad)
        except TypeError:
            continue
        raise AssertionError(f"canonical encoder accepted a disallowed type: {bad!r}")


def trial_jsonl_roundtrip():
    events = [{"kind": "spawn", "entity": 1, "class": "node"},
              {"kind": "attr", "entity": 1, "key": "size", "val": 7}]
    blob = canon.encode_jsonl(events)
    require(blob.endswith(b"\n"), "JSONL must end each record with a newline")
    require_equal(canon.decode_jsonl(blob), events, "JSONL round-trip changed events")


def trial_engine_serializer_crosscheck():
    # Engaged at Layer 1: core exposes its OWN canonical serializer
    # (core/serialize.py, re-implemented under the whitelist, importing neither
    # this reference nor corpora/). It must agree with this reference
    # byte-for-byte on every allowed value — both the fixed battery above and a
    # slice of every frozen base corpus.
    core_serialize = try_import(
        "core.serialize",
        "no engine serializer yet; cross-check engages at Layer 1",
    )
    for x in _SAMPLES:
        require(core_serialize.encode(x) == canon.canon_encode(x),
                f"engine serializer disagrees with the reference on {x!r}")
        # And the engine serializer must round-trip identically to the reference.
        require_equal(core_serialize.decode(core_serialize.encode(x)), x,
                      "engine serializer round-trip changed value")

    from corpora.chronicle import generator as chronicle_gen
    from corpora.sessions import generator as sessions_gen
    from corpora.murk import generator as murk_gen
    for gen, seed in ((chronicle_gen, 1001), (sessions_gen, 2002), (murk_gen, 3003)):
        for ev in gen.generate(seed, 400):
            require(core_serialize.encode(ev) == canon.canon_encode(ev),
                    f"engine serializer disagrees with the reference on a "
                    f"{gen.__name__} event: {ev!r}")

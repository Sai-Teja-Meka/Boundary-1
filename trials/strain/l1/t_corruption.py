"""strain/l1 — Layer 1 stress: corruption, duplicate flood, payload fuzzing.

Three strain families for Retention (BOUNDARY.md §6 strain):

  * **Snapshot corruption.** The canonical-form checksum (§strain, decided at
    Layer 1 and frozen into the anchors) must make a bit-flipped snapshot
    restore **loudly**: every single-bit flip is caught, never silently
    half-restored.
  * **Duplicate-event flood.** Retention does not dedup (dedup is Layer 2/4): a
    flood of identical payloads each gets a distinct, strictly-increasing `t`,
    all read back byte-exact, and the budget law still refuses deterministically
    once the cap is reached.
  * **Payload-shape fuzzing.** Murk's malformed family and a battery of grammar
    edge-case payloads (empty containers, deep nesting, big ints, unicode,
    nulls/bools) are canonical-valid, so they store and round-trip byte-exact;
    a genuinely non-canonical payload (a float) is rejected at the door.
"""

from _harness import require, require_equal
from adapters import l1
from corpora.murk import generator as murk_gen


# ---- snapshot corruption --------------------------------------------------

def _small_state():
    s = l1.empty()
    for p in murk_gen.generate(3003, 60):
        s, _t = l1.ingest(s, p)
    return s


def trial_uncorrupted_snapshot_restores_cleanly():
    s = _small_state()
    snap = l1.snapshot(s)
    restored = l1.restore(snap)                       # must not raise
    require_equal(l1.snapshot(restored), snap, "clean snapshot failed to round-trip")


def trial_single_bit_flip_is_caught_loudly():
    s = _small_state()
    snap = l1.snapshot(s)
    caught = 0
    for i in range(len(snap)):
        corrupt = bytes(snap[:i]) + bytes([snap[i] ^ 0x01]) + bytes(snap[i + 1:])
        if corrupt == snap:
            continue
        try:
            l1.restore(corrupt)
        except Exception:
            caught += 1                               # any loud failure is acceptable
        else:
            raise AssertionError(
                f"a flipped bit at byte {i} restored silently — corruption undetected")
    require(caught == len(snap),
            "every single-bit corruption of a snapshot must be caught")


def trial_truncated_and_empty_snapshots_fail_loudly():
    s = _small_state()
    snap = l1.snapshot(s)
    for bad in (b"", b"{", snap[: len(snap) // 2], snap + b"x"):
        try:
            l1.restore(bad)
        except Exception:
            continue
        raise AssertionError(f"a malformed snapshot restored silently: {bad[:16]!r}...")


# ---- duplicate-event flood ------------------------------------------------

def trial_duplicate_flood_keeps_every_copy_with_distinct_t():
    dup = {"kind": "attr", "entity": 7, "key": "status", "val": "active"}
    s = l1.empty()
    n = 5000
    for i in range(n):
        s, t = l1.ingest(s, dup)
        require_equal(t, i, "a duplicate flood must still assign strictly-increasing t")
    require_equal(s.next_t, n, "every duplicate must be retained (Retention does not dedup)")
    # A representative sample reads back byte-exact.
    for t in range(0, n, 499):
        require_equal(l1.read(s, t), {"payload": dup, "t": t}, "flooded duplicate not byte-exact")


def trial_duplicate_flood_refuses_deterministically_under_a_cap():
    dup = {"kind": "attr", "entity": 7, "key": "status", "val": "active"}

    def flood(cap):
        s = l1.make_engine(1, budget_cap=cap)
        accepted = 0
        while True:
            s2, t = l1.ingest(s, dup)
            if t is None:
                return accepted, s
            s = s2
            accepted += 1

    a1, s1 = flood(200)
    a2, _s2 = flood(200)
    require_equal(a1, a2, "the refusal point under a flood must be deterministic")
    require(a1 > 0, "at least one write should fit before the cap is reached")
    require(s1.occupancy <= s1.budget_cap, "occupancy must never exceed the cap (§4.1)")


# ---- payload-shape fuzzing ------------------------------------------------

_EDGE_PAYLOADS = [
    {},                                              # empty object
    [],                                              # empty array (as a payload)
    {"a": {}},                                       # nested empties
    {"deep": {"deep": {"deep": {"deep": [1, [2, [3, [4]]]]}}}},
    {"big": 123456789012345678901234567890},         # arbitrary-precision int
    {"neg": -999999999999},
    {"unicode": "αβγ — ✓ 深"},                        # raw UTF-8, ensure_ascii=False
    {"nulls": [None, None], "flags": [True, False]},
    {"mixed": [1, "two", None, True, {"k": [1, 2, 3]}]},
    "a bare string payload",
    42,
    True,
    None,
]


def _murk_malformed(seed, n):
    events, gt = murk_gen.generate_full(seed, n)
    return [events[d["t"]] for d in gt["defects"] if d["type"] == "malformed"]


def trial_edge_and_malformed_payloads_round_trip_byte_exact():
    fuzz = list(_EDGE_PAYLOADS) + _murk_malformed(3003, 2000)
    require(len(fuzz) > len(_EDGE_PAYLOADS), "expected some malformed murk payloads to fuzz with")
    s = l1.empty()
    ts = []
    for p in fuzz:
        s, t = l1.ingest(s, p)
        require(t is not None, f"a canonical-valid payload must not be refused: {p!r}")
        ts.append(t)
    # Read back byte-exact, both directly and after a snapshot/restore.
    s2 = l1.restore(l1.snapshot(s))
    for t, p in zip(ts, fuzz):
        require_equal(l1.read(s, t), {"payload": p, "t": t}, f"fuzz payload not byte-exact: {p!r}")
        require_equal(l1.read(s2, t), {"payload": p, "t": t},
                      f"fuzz payload not byte-exact after restore: {p!r}")


def trial_non_canonical_payload_is_rejected_at_the_door():
    s = l1.empty()
    for bad in ({"x": 1.5}, [1, 2.0], {"k": float("nan")}):
        try:
            l1.ingest(s, bad)
        except TypeError:
            continue
        raise AssertionError(f"a non-canonical (float) payload was accepted: {bad!r}")

"""ops/l1 — exact IO pairs for every Layer-1 verb (BOUNDARY.md §5 L1).

Fine-grained unit trials for `write` / `read` / `read_range` / `snapshot` /
`restore` and the generic `query` binding: t-assignment, byte-exact read-back,
range semantics, deterministic budget refusal, and the Answer contract (§7.2).
These are the correctness-of-the-pieces trials; corpus-scale replay is the
ascension class.
"""

from _harness import require, require_equal
from adapters import l1

# Fixed payloads (uniform shape => predictable, uniform cost) for deterministic
# t-assignment and budget-refusal cases.
_P0 = {"kind": "spawn", "entity": 1, "class": "node"}
_P1 = {"kind": "spawn", "entity": 2, "class": "agent"}
_P2 = {"kind": "spawn", "entity": 3, "class": "vault"}


def _fresh():
    return l1.empty()


# ---- write / t-assignment -------------------------------------------------

def trial_write_assigns_t_from_zero_strictly_increasing():
    s = _fresh()
    s, t0 = l1.write(s, _P0)
    s, t1 = l1.write(s, _P1)
    s, t2 = l1.write(s, _P2)
    require_equal((t0, t1, t2), (0, 1, 2),
                  "t must begin at 0 and increase by one per successful write (§1.3)")


def trial_write_does_not_mutate_caller_payload():
    s = _fresh()
    payload = {"kind": "attr", "entity": 1, "key": "size", "val": 7}
    before = dict(payload)
    s, _t = l1.write(s, payload)
    require_equal(payload, before, "write mutated the caller's payload (§2.1)")
    # And a later mutation of the caller's dict must not reach into stored state.
    payload["val"] = 999
    ev = l1.read(s, 0)
    require_equal(ev["payload"]["val"], 7, "stored event aliased the caller's payload")


# ---- read -----------------------------------------------------------------

def trial_read_empty_engine_is_none():
    require(l1.read(_fresh(), 0) is None, "read on an empty engine must be None")


def trial_read_returns_exact_event_record():
    s = _fresh()
    s, _ = l1.write(s, _P0)
    s, _ = l1.write(s, _P1)
    require_equal(l1.read(s, 0), {"payload": _P0, "t": 0}, "read(0) not byte-exact")
    require_equal(l1.read(s, 1), {"payload": _P1, "t": 1}, "read(1) not byte-exact")


def trial_read_out_of_range_and_bad_t_is_none():
    s = _fresh()
    s, _ = l1.write(s, _P0)
    require(l1.read(s, 1) is None, "read just past the end must be None")
    require(l1.read(s, -1) is None, "read at a negative t must be None")
    require(l1.read(s, True) is None, "read with a bool t must be None (bool != int)")
    require(l1.read(s, "0") is None, "read with a non-int t must be None")


# ---- read_range -----------------------------------------------------------

def trial_read_range_inclusive_and_clamped():
    s = _fresh()
    s, _ = l1.write(s, _P0)
    s, _ = l1.write(s, _P1)
    s, _ = l1.write(s, _P2)
    e0 = {"payload": _P0, "t": 0}
    e1 = {"payload": _P1, "t": 1}
    e2 = {"payload": _P2, "t": 2}
    require_equal(l1.read_range(s, 0, 2), [e0, e1, e2], "full range wrong")
    require_equal(l1.read_range(s, 1, 1), [e1], "singleton range wrong")
    require_equal(l1.read_range(s, 1, 99), [e1, e2], "range not clamped to the log end")
    require_equal(l1.read_range(s, -5, 0), [e0], "range not clamped at the low end")


def trial_read_range_empty_cases():
    s = _fresh()
    s, _ = l1.write(s, _P0)
    require_equal(l1.read_range(s, 5, 9), [], "range beyond the log must be empty")
    require_equal(l1.read_range(s, 1, 0), [], "inverted range (t0>t1) must be empty")
    require_equal(l1.read_range(_fresh(), 0, 10), [], "range on empty engine must be []")


# ---- budget refusal (§4.1) ------------------------------------------------

def trial_write_refuses_over_budget_deterministically():
    # Each _P* spawn costs event_cost = 6 payload cells + 1 for t = 7 work units.
    # With cap 20: writes at occupancy 0->7 (t0) and 7->14 (t1) fit; the third
    # (14->21) exceeds 20 and is refused.
    s = l1.make_engine(1, budget_cap=20)
    s, t0 = l1.write(s, _P0)
    s, t1 = l1.write(s, _P1)
    require_equal((t0, t1), (0, 1), "first two writes should fit the budget")
    occ_before = s.occupancy
    s_after, t_ref = l1.write(s, _P2)
    require(t_ref is None, "an over-budget write must return t = None (refusal)")
    require(s_after is s, "a refused write must return the state UNCHANGED (no partial write)")
    require_equal(s_after.occupancy, occ_before, "a refused write must not change occupancy")
    # The refusal decision is a pure function of the input: identical on re-run.
    _s2, t_ref2 = l1.write(s, _P2)
    require(t_ref2 is None, "refusal must be deterministic across runs")
    # Accepted events remain readable; refusal did not corrupt the log.
    require_equal(l1.read(s, 0), {"payload": _P0, "t": 0}, "accepted event lost after a refusal")


# ---- snapshot / restore ---------------------------------------------------

def trial_snapshot_is_bytes_and_restore_round_trips():
    s = _fresh()
    for p in (_P0, _P1, _P2):
        s, _ = l1.write(s, p)
    snap = l1.snapshot(s)
    require(isinstance(snap, bytes), "snapshot must return bytes (§7.1)")
    s2 = l1.restore(snap)
    # A restored state answers queries identically and re-snapshots to the same bytes.
    require_equal(l1.snapshot(s2), snap, "restore(snapshot) is not a byte-fixed-point")
    for t in (0, 1, 2, 3):
        require_equal(l1.query(s, {"op": "read", "t": t}),
                      l1.query(s2, {"op": "read", "t": t}),
                      f"restored state answered read(t={t}) differently")


# ---- the Answer contract (§7.2) -------------------------------------------

def trial_query_answer_shape_and_provenance():
    s = _fresh()
    s, _ = l1.write(s, _P0)
    hit = l1.query(s, {"op": "read", "t": 0})
    require_equal(set(hit.keys()), {"status", "value", "confidence", "provenance"},
                  "Answer keys must be exactly status/value/confidence/provenance")
    require_equal(hit["status"], "answer", "an in-range read must answer")
    require(isinstance(hit["confidence"], int) and 0 <= hit["confidence"] <= 1000,
            "confidence must be an integer permille in [0,1000] (§3.4)")
    _validate_provenance(hit["provenance"], ingested_max=s.next_t - 1)

    miss = l1.query(s, {"op": "read", "t": 9})
    require_equal(miss["status"], "abstain", "an out-of-range read must abstain, not raise")
    require(miss["value"] is None, "an abstention carries a null value")


def trial_query_unsupported_op_abstains_not_raises():
    s = _fresh()
    s, _ = l1.write(s, _P0)
    for q in ({"op": "recall", "cue": "x"}, {"op": "intend"}, {"nonsense": 1}, "not-a-dict", 42):
        ans = l1.query(s, q)
        require_equal(ans["status"], "abstain",
                      f"an unsupported query must abstain, never raise: {q!r}")


# A local copy of the §4.2 provenance-tag validation, so this trial is
# self-contained (schema mirrored from laws/t_provenance_schema.py).
_KIND_VOCAB = ("recall", "aggregate", "derive", "absent")


def _validate_provenance(tag, ingested_max):
    require(isinstance(tag, dict), "a read-hit must carry a provenance tag")
    require_equal(set(tag.keys()), {"support", "kind", "t_asof"},
                  "provenance keys must be exactly support/kind/t_asof")
    require(tag["kind"] in _KIND_VOCAB, f"provenance kind out of vocabulary: {tag['kind']!r}")
    t_asof = tag["t_asof"]
    require(isinstance(t_asof, int) and not isinstance(t_asof, bool)
            and 0 <= t_asof <= ingested_max, "t_asof must be an in-range plain int")
    support = tag["support"]
    require(isinstance(support, list), "support must be an array")
    require(len(support) > 0 or tag["kind"] == "absent",
            "support may be empty only when kind == 'absent'")
    prev = -1
    for t in support:
        require(isinstance(t, int) and not isinstance(t, bool), "support entries are plain ints")
        require(0 <= t <= ingested_max, "support entry out of ingested range")
        require(t > prev, "support must be strictly ascending with no duplicates")
        prev = t

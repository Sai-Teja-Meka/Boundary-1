"""ascension/l1 — Layer 1 (Retention) capability trials (BOUNDARY.md §5 L1).

Replays the full frozen Phase-0 corpora (chronicle 50k, sessions 5k, murk 10k)
through the generic interface and scores them against the ratified L1 gate:

    F = 1000, C >= 995, B = 1000, snapshot/restore byte-identical.

Every stored event must read back **byte-exact**, and a snapshot taken
mid-stream must restore to a state whose continuation is identical to the
un-snapshotted original. The murk corpus is included deliberately: its
"malformed" family is grammar-violating but still canonical-JSON-valid, so
Retention — which judges no grammar — must store and return it exactly like any
other payload. That is the honest floor.
"""

from fractions import Fraction

from _harness import require, require_equal
from adapters import l1
from corpora import canon
from corpora.chronicle import generator as chronicle_gen
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen

# The ratified Layer-1 ascension gate (§5).
GATE_F = 1000
GATE_C = 995
GATE_B = 1000


def _permille(x):
    n = x * 1000
    q = n.numerator // n.denominator
    r = n - q
    if r < Fraction(1, 2):
        return q
    if r > Fraction(1, 2):
        return q + 1
    return q if q % 2 == 0 else q + 1


def _replay_and_score(payloads):
    """Ingest every payload, read each back, and return (F, C, B) in permille."""
    state = l1.empty()
    for p in payloads:
        state, t = l1.ingest(state, p)
        require(t is not None, "an in-budget write must not be refused during ascension")

    n = len(payloads)
    fidelity_sum = 0
    recovered = 0
    for t, p in enumerate(payloads):
        ans = l1.query(state, {"op": "read", "t": t})
        require(ans["status"] in ("answer", "abstain"), "read must not raise (§7.3)")
        want = {"payload": p, "t": t}
        if ans["status"] == "answer" and ans["value"] == want:
            fidelity_sum += 1000
            recovered += 1
        elif ans["status"] == "abstain":
            fidelity_sum += 100
        else:
            fidelity_sum += 0

    f = _permille(Fraction(fidelity_sum, n * 1000))
    c = _permille(Fraction(recovered, n))            # uniform weights (§3.2)
    # Budget measure (§3.3): peak occupancy never exceeded the cap => B = 1000.
    b = 1000 if state.occupancy <= state.budget_cap else \
        _permille(Fraction(state.budget_cap, state.occupancy))
    return f, c, b, state


def _assert_gate(name, payloads):
    f, c, b, state = _replay_and_score(payloads)
    require(f >= GATE_F, f"{name}: F={f} below the L1 gate F={GATE_F}")
    require(c >= GATE_C, f"{name}: C={c} below the L1 gate C>={GATE_C}")
    require(b >= GATE_B, f"{name}: B={b} below the L1 gate B={GATE_B}")
    # snapshot/restore byte-identical at the ascended state.
    snap = l1.snapshot(state)
    require_equal(l1.snapshot(l1.restore(snap)), snap,
                  f"{name}: snapshot/restore is not byte-identical")
    return f, c, b


def _byte_exact_spot_check(name, payloads, step):
    """Independently confirm read-back is byte-for-byte, via the reference codec."""
    state = l1.empty()
    for p in payloads:
        state, _t = l1.ingest(state, p)
    for t in range(0, len(payloads), step):
        ev = l1.read(state, t)
        require(canon.canon_encode(ev["payload"]) == canon.canon_encode(payloads[t]),
                f"{name}: event t={t} did not read back byte-exact")


def trial_chronicle_full_replay_meets_gate():
    payloads = list(chronicle_gen.generate(chronicle_gen.SEED, chronicle_gen.N))
    f, c, b = _assert_gate("chronicle", payloads)
    require_equal((f, c, b), (1000, 1000, 1000), "chronicle must score a clean 1000/1000/1000")
    _byte_exact_spot_check("chronicle", payloads, step=337)


def trial_sessions_full_replay_meets_gate():
    payloads = list(sessions_gen.generate(sessions_gen.SEED, sessions_gen.N))
    f, c, b = _assert_gate("sessions", payloads)
    require_equal((f, c, b), (1000, 1000, 1000), "sessions must score a clean 1000/1000/1000")
    _byte_exact_spot_check("sessions", payloads, step=53)


def trial_murk_full_replay_meets_gate():
    # Includes contradictions, near-duplicates, ambiguity reuse, and the
    # malformed family — all canonical-valid payloads Retention stores verbatim.
    payloads = list(murk_gen.generate(murk_gen.SEED, murk_gen.N))
    f, c, b = _assert_gate("murk", payloads)
    require_equal((f, c, b), (1000, 1000, 1000), "murk must score a clean 1000/1000/1000")
    _byte_exact_spot_check("murk", payloads, step=101)


def trial_snapshot_restore_midstream_yields_identical_continuation():
    payloads = list(chronicle_gen.generate(chronicle_gen.SEED, 6000))
    head, tail = payloads[:3000], payloads[3000:]

    s1 = l1.empty()
    for p in head:
        s1, _t = l1.ingest(s1, p)

    # Snapshot mid-stream and restore into an independent state.
    snap = l1.snapshot(s1)
    s2 = l1.restore(snap)
    require_equal(l1.snapshot(s2), snap, "mid-stream restore is not a byte-fixed-point")

    # Continue both with the identical tail; the continuations must stay identical.
    for p in tail:
        s1, t1 = l1.ingest(s1, p)
        s2, t2 = l1.ingest(s2, p)
        require_equal(t1, t2, "restored continuation assigned a different t")

    require_equal(l1.snapshot(s1), l1.snapshot(s2),
                  "the restored state's continuation diverged from the original")
    for t in range(0, len(payloads), 211):
        require_equal(l1.query(s1, {"op": "read", "t": t}),
                      l1.query(s2, {"op": "read", "t": t}),
                      f"restored continuation answered read(t={t}) differently")

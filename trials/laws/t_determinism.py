"""laws/ — determinism (BOUNDARY.md §2.3).

Identical inputs must produce byte-identical outputs. Enforced now for the
PRNG and the corpora generators; the engine-level determinism check engages
once an engine exists.
"""

from _harness import require, try_import
from corpora.prng import Xorshift64
from corpora import canon
from corpora.chronicle import generator as chronicle_gen
from corpora.sessions import generator as sessions_gen
from corpora.murk import generator as murk_gen


def trial_prng_determinism():
    a = Xorshift64(12345)
    b = Xorshift64(12345)
    seq_a = [a.next_u64() for _ in range(256)]
    seq_b = [b.next_u64() for _ in range(256)]
    require(seq_a == seq_b, "same-seed PRNG streams diverged")
    c = Xorshift64(12346)
    seq_c = [c.next_u64() for _ in range(256)]
    require(seq_a != seq_c, "different seeds produced identical streams")


def trial_corpora_generators_determinism():
    for gen, seed in ((chronicle_gen, 777), (sessions_gen, 777), (murk_gen, 777)):
        first = canon.encode_jsonl(gen.generate(seed, 300))
        second = canon.encode_jsonl(gen.generate(seed, 300))
        require(first == second,
                f"{gen.__name__} not deterministic at fixed (seed, n)")


def trial_murk_answer_key_determinism():
    _, gt1 = murk_gen.generate_full(555, 300)
    _, gt2 = murk_gen.generate_full(555, 300)
    require(canon.canon_encode(gt1) == canon.canon_encode(gt2),
            "murk ground_truth not deterministic at fixed (seed, n)")


def trial_engine_determinism():
    # Engaged at Layer 1: identical ingest/query sequences must yield
    # byte-identical snapshots and identical answers, and a snapshot must
    # restore to a state that snapshots identically (§2.3, §7.1).
    engine = try_import(
        "core.engine",
        "no engine yet; engine determinism engages at Layer 1",
    )
    payloads = list(chronicle_gen.generate(9090, 600))

    def ingest_all():
        state = engine.empty()
        for p in payloads:
            state, _t = engine.ingest(state, p)
        return state

    s_a = ingest_all()
    s_b = ingest_all()
    snap_a = engine.snapshot(s_a)
    snap_b = engine.snapshot(s_b)
    require(snap_a == snap_b,
            "two identical ingest sequences produced different snapshots")

    # Every read answers identically across the two independent runs.
    for t in range(0, len(payloads), 37):
        require(engine.query(s_a, {"op": "read", "t": t})
                == engine.query(s_b, {"op": "read", "t": t}),
                f"engine answered read(t={t}) differently across identical runs")

    # snapshot -> restore -> snapshot is a fixed point (byte-identical).
    restored = engine.restore(snap_a)
    require(engine.snapshot(restored) == snap_a,
            "restore(snapshot(s)) does not re-snapshot to the same bytes")

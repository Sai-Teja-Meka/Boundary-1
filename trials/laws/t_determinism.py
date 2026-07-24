"""laws/ — determinism (BOUNDARY.md §2.3).

Identical inputs must produce byte-identical outputs. Enforced now for the
PRNG and the corpora generators; the engine-level determinism check engages
once an engine exists.
"""

from _harness import require, skip
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
    # Engages when an engine exists: identical ingest/query sequences must yield
    # byte-identical snapshots and answers.
    skip("no engine yet; engine determinism engages at Layer 1")

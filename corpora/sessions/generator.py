"""corpora/sessions/generator.py — deterministic sessions generator.

See corpora/sessions/grammar.md. Randomness comes solely from corpora/prng.py;
output is canonical JSONL. Same (seed, n) -> byte-identical (BOUNDARY.md §8.3).
Only lists and integer indices are used in the generation path.
"""

import os
import sys

from corpora import canon
from corpora.prng import Xorshift64

USERS = ("ada", "borg", "cleo", "dex", "echo", "fable", "gus", "hana")
ROLES = ("user", "agent")
TOOLS = ("search", "read", "write", "exec", "fetch", "plan", "spawn", "commit")

SEED = 2002
N = 5000

_HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN_PATH = os.path.join(_HERE, "sessions.s2002.n5000.jsonl")


def _pick(rng, seq):
    return seq[rng.below(len(seq))]


def generate(seed, n):
    """Yield `n` sessions event payloads deterministically from `seed`."""
    rng = Xorshift64(seed)
    open_sessions = []     # list of [sid, turns]
    next_sid = 1
    next_text_id = 1
    produced = 0
    while produced < n:
        if not open_sessions:
            action = "session_start"
        else:
            bucket = rng.below(100)
            if bucket < 15:
                action = "session_start"
            elif bucket < 70:
                action = "msg"
            elif bucket < 90:
                action = "tool"
            else:
                action = "session_end"

        if action == "session_start":
            sid = next_sid
            next_sid += 1
            open_sessions.append([sid, 0])
            event = {"kind": "session_start", "sid": sid, "user": _pick(rng, USERS)}
        elif action == "msg":
            idx = rng.below(len(open_sessions))
            sess = open_sessions[idx]
            sess[1] += 1
            text_id = next_text_id
            next_text_id += 1
            event = {"kind": "msg", "sid": sess[0], "role": _pick(rng, ROLES),
                     "text_id": text_id}
        elif action == "tool":
            idx = rng.below(len(open_sessions))
            sess = open_sessions[idx]
            event = {"kind": "tool", "sid": sess[0], "name": _pick(rng, TOOLS),
                     "code": rng.below(10)}
        else:  # session_end
            idx = rng.below(len(open_sessions))
            sess = open_sessions[idx]
            open_sessions[idx] = open_sessions[-1]
            open_sessions.pop()
            event = {"kind": "session_end", "sid": sess[0], "turns": sess[1]}

        yield event
        produced += 1


def frozen_bytes():
    """The exact byte content of the frozen sessions corpus."""
    return canon.encode_jsonl(generate(SEED, N))


def main(argv):
    if "--write" in argv:
        data = frozen_bytes()
        with open(FROZEN_PATH, "wb") as fh:
            fh.write(data)
        print(f"wrote {FROZEN_PATH} ({len(data)} bytes, {N} events)")
        return 0
    if "--check" in argv:
        want = open(FROZEN_PATH, "rb").read()
        got = frozen_bytes()
        ok = want == got
        print("byte-match OK" if ok else "BYTE-MATCH MISMATCH")
        return 0 if ok else 1
    print("usage: python3 -m corpora.sessions.generator [--write|--check]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

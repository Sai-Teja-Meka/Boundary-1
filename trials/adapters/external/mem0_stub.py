"""trials/adapters/external/mem0_stub.py — an adapter STUB for Mem0. Not runnable.

A stub is the honest half of an adapter: the mapping from `INTERFACE.md` onto a
real system's API, written down and reviewable, with the part that would make a
network call **deliberately absent**. Importing this module reaches nothing, and
running it is a separate, human-supervised session (`packaging/HONESTY.md`,
"what grading an external system would require").

Why a stub rather than a working adapter, stated once and applying to every
external system:

* **No network, no keys, ever, from a session.** Mem0's OSS core calls an LLM
  for extraction on the default `add()` path (`autopsy/mem0/ANATOMY.md`), so a
  working adapter needs a provider key and outbound egress. A session that
  fetched a key or opened a socket to produce a number would be producing a
  number nobody can reproduce, which is exactly what
  `autopsy/GAPMAP.md §2` convicts the field's evaluators of.
* **The result would not be deterministic.** `BOUNDARY.md §2.3` makes
  determinism a law for our engine, and the harness scores by exact comparison.
  An LLM-extraction pipeline returns different memories on different runs; the
  honest way to grade it is to say so in the report and to run it under a human
  who accepts that the number is a sample, not a measurement. That is a
  decision for a human, and this file does not pre-empt it.
* **The mapping is the reviewable part.** What `ingest`, `query` and `snapshot`
  would *mean* against Mem0 is a design claim that can be read and argued with
  now, on the strength of the autopsy, without running anything.

## The mapping, as designed (commit-pinned to the autopsy)

Source read: `autopsy/mem0/ANATOMY.md` — OSS core at commit `d6d89c9`.

| `INTERFACE.md` | Mem0 OSS core | note |
|---|---|---|
| `ingest(state, payload)` | `Memory.add(messages=[…], user_id=…)` | Mem0 assigns no logical `t`; §1.3 requires an engine-assigned, strictly increasing integer, so the adapter would have to **synthesize** one and record that it is the adapter's and not the system's. |
| `query(state, {"op":"recall","cue":…})` | `Memory.search(query=…, user_id=…)` | returns a ranked list with scores; the interface wants **one** answer or an abstention, so the adapter must declare a rule (top-1 above a threshold, else abstain) and that rule is the adapter's editorial choice, not Mem0's. |
| `query(state, {"op":"read","t":T})` | — | no read-by-logical-time exists. Abstains (§7.3). |
| `query(state, {"op":"current"/"asof"/"profile"})` | — | ABSENT in the OSS core: contradictions coexist, no supersession, no as-of. Abstains. |
| `snapshot(state)` | `Memory.get_all(user_id=…)` | a listing, not a state serialization; `restore` has no counterpart at all, so the §7.1 round-trip law cannot be honoured and the adapter must report that rather than fake it. |
| `make_engine(layer_cap)` | — | no capability capping exists; a humility run against Mem0 is not expressible without one, which is itself a finding worth reporting. |

## What this file guarantees

Import-safe: it imports nothing but the standard library, defines no gate, and
touches no network. `available()` returns `(False, reason)`. Every interface
function raises `AdapterNotRunnable` **when called** — and that is not a
violation of §7.3, which governs *capability absence in an engine under test*;
this module is not an engine, it is an unconfigured adapter, and the scorecard
runner checks `available()` before it would ever call one.
"""

NAME = "mem0"
KIND = "stub"

SYSTEM = {
    "name": "Mem0 (OSS core)",
    "license": "Apache-2.0 (core)",
    "commit_read": "d6d89c9",
    "autopsy": "autopsy/mem0/ANATOMY.md",
}

REQUIRES = (
    "the `mem0ai` package installed",
    "an LLM provider API key in the environment",
    "outbound network egress",
    "a human-supervised session that accepts a non-deterministic result",
)

# Layers the autopsy found present, as a claim to be *tested* rather than
# trusted — the whole point of running the adapter one day.
AUTOPSY_EXPECTATION = {
    1: "PART — vector rows, no budget refusal",
    2: "PART — BM25 + entity boost fused with semantic search",
    3: "ABSENT — decay is platform-gated; hide is not evict",
    4: "ABSENT — additive only; contradictions coexist",
}


class AdapterNotRunnable(RuntimeError):
    """This adapter is a stub: the mapping is written down, the call is not."""


def available():
    """`(False, reason)` — always, from a session. Checked before any call."""
    return (False,
            "stub: running Mem0 needs the mem0ai package, a provider key and "
            "network egress, and returns a non-deterministic result — a "
            "separate human-supervised session, never a session's own doing")


def _refuse(op):
    raise AdapterNotRunnable(
        "%s.%s is a stub. %s" % (NAME, op, available()[1]))


def empty(budget_cap=None):
    _refuse("empty")


def make_engine(layer_cap, budget_cap=None):
    _refuse("make_engine")


def ingest(state, payload):
    _refuse("ingest")


def query(state, q):
    _refuse("query")


def snapshot(state):
    _refuse("snapshot")


def last_cost(state):
    _refuse("last_cost")

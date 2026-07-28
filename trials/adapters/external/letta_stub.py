"""trials/adapters/external/letta_stub.py — an adapter STUB for Letta. Not runnable.

The companion to `mem0_stub.py`; the reasoning for stubbing rather than running
is stated there in full and applies unchanged here — no network and no keys from
a session, a non-deterministic result, and the mapping being the part that can
be reviewed now.

Letta earns a stub of its own for a specific reason rather than for symmetry:
Layer 4's demotion mechanism **is** Letta's hot/cold tiering in the
constitutional form `autopsy/GAPMAP.md` **S4 form B** chose
(`core/layers/README-l4.md`, pedigree). The system we borrowed the mechanism
from is the one it would be most informative to grade, and the two places the
autopsy says the borrowed mechanism differs are exactly what a run would test.

## The mapping, as designed (commit-pinned to the autopsy)

Source read: `autopsy/letta/ANATOMY.md` — OSS core at commit `b76da90`.

| `INTERFACE.md` | Letta OSS core | note |
|---|---|---|
| `ingest(state, payload)` | a message into the agent's recall store | Letta stamps wall-clock time; §1.3 forbids a clock and requires an engine-assigned integer `t`, so the adapter must synthesize `t` and say so. |
| `query(state, {"op":"recall","cue":…})` | `conversation_search` / archival vector search | vector search is model-dependent, so the same cue can return different things on different days; the adapter must declare its top-1-or-abstain rule. |
| `query(state, {"op":"read","t":T})` | — | no read-by-logical-time. Abstains (§7.3). |
| `query(state, {"op":"current"/"asof"})` | — | core blocks are **destructively** self-edited (`sleeptime` rethink); there is no attribute history and no as-of. Abstains. |
| the budget law (§4.1) | the in-context char limit | **advisory, not enforced** — the autopsy's finding. A budget measure over Letta would be measuring an advisory number, which the report must state rather than quietly score as `B = 1000`. |
| eviction under pressure | overflow **demotion**: evict from context, retain in recall | this is S4, and it is why the grade matters: Letta's cold tier is *unbounded*, which §4.1 forbids, so the interesting number is what happens when total occupancy is capped — the case the autopsy found nobody tests (`autopsy/GAPMAP.md §4`, the fourth axis). |
| `snapshot(state)` / `restore` | agent state export | exists in some form; whether it satisfies the §7.1 byte-identical round-trip is an open question a run would answer. |
| `make_engine(layer_cap)` | — | no capability capping; same finding as Mem0. |

## What this file guarantees

Import-safe: standard library only, no gate constant, no network. `available()`
returns `(False, reason)`; every interface function raises `AdapterNotRunnable`
when called. §7.3 is not in play — this is an unconfigured adapter, not an
engine under test, and the runner checks `available()` first.
"""

NAME = "letta"
KIND = "stub"

SYSTEM = {
    "name": "Letta (OSS core)",
    "license": "Apache-2.0 (core)",
    "commit_read": "b76da90",
    "autopsy": "autopsy/letta/ANATOMY.md",
}

REQUIRES = (
    "the `letta` package (or a running Letta server) available",
    "an LLM provider API key in the environment",
    "outbound network egress",
    "a human-supervised session that accepts a non-deterministic result",
)

AUTOPSY_EXPECTATION = {
    1: "PART — three tiers; the char limit is advisory, not enforced",
    2: "PART — conversation search + archival vector search, model-dependent",
    3: "PART — demotion, not decay: evict-from-context, retain-in-recall, "
       "cold tier unbounded",
    4: "PART — sleeptime rethink reorganizes blocks destructively, "
       "no fidelity-floor reconstruction",
}


class AdapterNotRunnable(RuntimeError):
    """This adapter is a stub: the mapping is written down, the call is not."""


def available():
    """`(False, reason)` — always, from a session. Checked before any call."""
    return (False,
            "stub: running Letta needs the letta package or a server, a "
            "provider key and network egress, and returns a non-deterministic "
            "result — a separate human-supervised session, never a session's "
            "own doing")


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

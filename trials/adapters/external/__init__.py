"""trials/adapters/external/ — engines that are not ours, behind `INTERFACE.md`.

`trials/adapters/l1.py` … `l4.py` bind **our** engine, one adapter per layer, and
the whole suite speaks to them through the generic interface (§7). This package
holds the other direction: adapters for engines nobody here wrote, so the claim
that the interface is generic can be exercised instead of asserted.

Three entries today:

| name | kind | runnable | what it is |
|---|---|---|---|
| `reference` | reference | **yes** | a complete third-party-shaped engine written against `INTERFACE.md` alone, implementing Layers 1–2 and stopping there |
| `mem0` | stub | no | the `INTERFACE.md` → Mem0 mapping, written down; the call deliberately absent |
| `letta` | stub | no | the same for Letta, whose hot/cold tiering our Layer 4 borrowed (GAPMAP **S4** form B) |

## `available()` is the gate, not an exception

Every module here exposes `available() -> (bool, reason)`. The scorecard runner
(`trials/scorecard.py`) checks it **before** it would call an interface function,
and reports the reason instead of running. That keeps two things apart which
would otherwise be confused:

* **capability absence in an engine under test** — governed by §7.3, which
  requires an *abstention* and forbids an exception. The `reference` engine
  abstains on every Layer-3 and Layer-4 verb; it never raises.
* **an unconfigured adapter** — not an engine at all. A stub raises
  `AdapterNotRunnable` if called, because there is nothing there to abstain.
  §7.3 does not reach it, and the runner never gets that far.

A stub that abstained its way through the battery would report a *score* for a
system that was never run, which is the one outcome this package exists to make
impossible.

## Running an external adapter is a human's move, not a session's

No adapter here reaches the network, reads an environment variable or wants a
key, and none ever will from inside a session: a number produced that way is
not reproducible and would contradict the discipline
`packaging/HONESTY.md` states. Grading a live external system is a separate,
deliberate, human-supervised step.
"""

from . import letta_stub, mem0_stub, reference

# name -> module. The scorecard's `--engine` takes these names, plus `ours`.
ADAPTERS = {
    reference.NAME: reference,
    mem0_stub.NAME: mem0_stub,
    letta_stub.NAME: letta_stub,
}

# The functions `INTERFACE.md`'s "Adapter contract" requires of every adapter,
# runnable or stubbed. A stub defines them and refuses when called; the check
# that all three modules carry the whole surface lives in
# `trials/ops/packaging/t_adapters.py`.
REQUIRED_SURFACE = ("empty", "make_engine", "ingest", "query", "snapshot",
                    "last_cost")


def get(name):
    """The adapter module registered under `name`, or a KeyError naming the set."""
    if name not in ADAPTERS:
        raise KeyError("no external adapter %r; known: %s"
                       % (name, ", ".join(sorted(ADAPTERS))))
    return ADAPTERS[name]


def available(name):
    """`(bool, reason)` for one adapter — the runner's precondition."""
    return get(name).available()


def names():
    return sorted(ADAPTERS)

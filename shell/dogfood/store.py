"""shell/dogfood/store.py — persistence for the dogfood store (the impure rim).

The engine is pure and has no idea a file exists (§2.2). Persistence is exactly
this module: snapshot bytes out, snapshot bytes in, with the Layer-1 checksum law
in force on the way back.

  * **Location** — `shell/dogfood/store/store.json`, inside the repo. The
    project's own memory belongs in the project's own history.
  * **Not a frozen artifact** — it grows by use and is committed with every
    session; §9.2 does not apply to it. It IS engine-owned: the bytes are exactly
    `snapshot(state)`, so hand-editing them breaks the checksum by construction.
  * **Corruption fails loudly** — `restore` raises `CorruptSnapshot` (L1 README),
    which surfaces here as `StoreCorrupt`. There is no silent re-initialization
    path anywhere in this module: a store that fails its integrity check is not
    replaced, not repaired, not ignored.

The file is written as the canonical snapshot bytes with **no trailing newline**,
so `sha256(file bytes)` is a meaningful checksum of the state itself.
"""

import hashlib
import os

from core.layers import l2_recall as engine   # shell imports core (§2.6)

STORE_DIRNAME = "store"
STORE_FILENAME = "store.json"

# The dogfood store's budget cap, in work units (§4.1). A shell-level choice of
# the engine's budget parameter — the engine's own DEFAULT_BUDGET is a trial-scale
# number, not a considered one for a store that must outlive the project.
#
#   2**24 = 16,777,216 work units.
#
# Measured over the 13 backfilled log events (payload cells + index cells):
# min 68, mean 258, max 490 work units. Budgeting a deliberately fat 4,096 units
# per event — 8x the largest real one, room for a session summary many times
# longer than any written so far — gives
#
#   16,777,216 / 4,096 = 4,096 events
#
# At one event per session and one session per day that is 4,096 days ≈ 11.2
# years; at the observed worst case (490) it is 34,239 events ≈ 93 years.
# Years of headroom either way, and the number is a power of two, exact, integer.
DOGFOOD_BUDGET = 16_777_216


class StoreMissing(RuntimeError):
    """No state file exists at the requested path."""


class StoreCorrupt(RuntimeError):
    """The state file exists but failed its integrity check. Never recovered from."""


def repo_root():
    """The repository root (== the `boundary-1-memory/` root, CLAUDE.md)."""
    here = os.path.dirname(os.path.abspath(__file__))          # shell/dogfood
    return os.path.dirname(os.path.dirname(here))              # repo root


def default_store_path():
    """The committed store: `shell/dogfood/store/store.json`."""
    return os.path.join(repo_root(), "shell", "dogfood", STORE_DIRNAME, STORE_FILENAME)


def display_path(path):
    """`path` relative to the repo root when it lives inside it, else absolute."""
    root = repo_root()
    absolute = os.path.abspath(path)
    if absolute.startswith(root + os.sep):
        return os.path.relpath(absolute, root)
    return absolute


def exists(path):
    return os.path.isfile(path)


# ---- create / load / save --------------------------------------------------

def create_state(budget_cap=DOGFOOD_BUDGET):
    """A fresh, empty Layer-2 store state at the dogfood budget cap."""
    return engine.make_engine(engine.LAYER, budget_cap=budget_cap)


def load_bytes(path):
    if not os.path.isfile(path):
        raise StoreMissing(path)
    with open(path, "rb") as fh:
        return fh.read()


def load(path):
    """Restore the state from the file at `path`.

    Raises `StoreMissing` if there is no file, `StoreCorrupt` if there is one and
    it does not verify. The second case never falls back to an empty store.
    """
    raw = load_bytes(path)
    try:
        return engine.restore(raw)
    except engine.CorruptSnapshot as exc:
        raise StoreCorrupt(str(exc))
    except Exception as exc:                     # decode/UTF-8/shape failures
        raise StoreCorrupt("%s: %s" % (type(exc).__name__, exc))


def save(path, state):
    """Write the state's snapshot bytes to `path` atomically. Returns the bytes."""
    data = engine.snapshot(state)
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)
    return data


# ---- the one write verb ----------------------------------------------------

def remember(state, payload):
    """Ingest one event; return `(state', t)`. `t` is None on budget refusal (§4.1)."""
    return engine.write(state, payload)


# ---- reporting -------------------------------------------------------------

def file_checksum(path):
    """SHA-256 over the state file's bytes (`n/a` when there is no file)."""
    if not os.path.isfile(path):
        return "n/a"
    return hashlib.sha256(load_bytes(path)).hexdigest()


def state_checksum(state):
    """SHA-256 over the canonical encoding of the full state body (engine, §2.4)."""
    return engine.state_checksum(state)


def permille(part, whole):
    """Integer permille of `part/whole`, floor — reporting only, never a float."""
    if whole <= 0:
        return 0
    return (part * 1000) // whole

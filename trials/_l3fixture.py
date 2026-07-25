"""trials/_l3fixture.py — cached Layer-3 engine replays, shared by ops and strain.

A full 10 000-item pressure replay under `layer_cap = 3` performs ~9 000 evictions
and costs a few seconds. Two trial files need the *same* post-replay state — the
state-composition ops trial (which asserts the recorded cost arithmetic of
`README-l3 §0`) and the strain trial (which asserts what survived) — so it is
replayed once here and shared, rather than twice with identical results.

Engine-gated by construction: importing this module does not touch an engine;
`replayed` does, and its callers are already `try_import`-guarded.

Nothing here decides anything. The cache is keyed by `(stream, layer_cap)` and
returns exactly what `_l3score.replay` returns, so a trial reading it is reading
the same numbers the ascension trial gates on.
"""

import _l3score

_CACHE = {}


def replayed(engine, name, layer_cap=3):
    """`(state, budget)` after replaying stream `name` under `layer_cap` (cached)."""
    key = (name, layer_cap)
    if key not in _CACHE:
        _CACHE[key] = _l3score.replay(
            engine, lambda cap: engine.make_engine(layer_cap, cap), name)
    return _CACHE[key]

"""trials/_l7fixtures.py — the Layer-7 reference fixtures. NEVER ENGINE CODE.

One fixture, and it exists so that a guard is **demonstrated** rather than
assumed — the discipline `strain/l3` set with its naive reference count (the
policy that would have swept the attacked set), `strain/l5` restated with its
ledger-blind firing policy (dup-fire 199 where the engine reaches 0) and
`strain/l6` restated with its constant-confidence policy (the thing that does not
move). A `§5` clause an engine clears is not evidence the clause has teeth; a
neighbouring policy that fails it is.

It lives here, at the trials root beside `_l7score.py` and `_l7tasks.py`, because
**two strain files use it and a fixture defined twice can drift** — which is the
one-fixture-one-truth discipline applied to a fixture rather than to a measure.
Files whose name starts with `_` are skipped by `run.py`'s discovery, so nothing
here is a trial.
"""

from dataclasses import replace

from adapters import l7


class LedgerBlind:
    """`adapters/l7` with ONE field emptied at the read.

    It is not a different engine and it is not engine code. It `ingest`s through
    `adapters/l7` unchanged, so the lineage ledger **is written** exactly as the
    engine writes it; what it refuses to do is **read** it when answering a
    `generate` cue. That is `autopsy/GAPMAP.md §2`'s engine thesis in its purest
    available form — *every system autopsied writes the metadata that would make
    it correct and then never reads it where it counts* — pointed at the one
    field `§5 L7` exists to fill.

    Measured on `corpora/l7compose`'s own three-generation ladder it promotes
    100, then 130, then all 160, and three deep it calls every one of its own
    dreams a fact: the same triple `ATTAINABILITY.md §5.1` measured for the
    ledger-blind POLICY before any engine existed.
    """

    DEFAULT_BUDGET = l7.DEFAULT_BUDGET
    make_engine = staticmethod(l7.make_engine)
    ingest = staticmethod(l7.ingest)
    snapshot = staticmethod(l7.snapshot)
    restore = staticmethod(l7.restore)

    @staticmethod
    def query(state, q):
        if isinstance(q, dict) and q.get("op") == "generate" \
                and isinstance(state, l7.L7State):
            state = replace(state, lineage={})
        return l7.query(state, q)

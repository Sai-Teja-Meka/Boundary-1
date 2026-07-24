"""humility/l2 — Layer 2 (Recall) humility (BOUNDARY.md §6, §5 L2).

Runs Layer 2's **own cue tasks** (`_l2tasks`, shared verbatim with the ascension
trial) against the capped engine `make_engine(layer_cap = 1)` — the read-by-time
Retention engine that provably lacks an associative index — through the same
generic interface. The declared ceiling is **capped cue-C ≤ 100** (§5 L2). The
structural argument for the ceiling is in `IMPOSSIBILITY.md`.

Why this is green the moment the tasks exist, *before* the recall engine is
built: pre-Layer-2, `make_engine(1)` **is** the whole engine, so a capped
recall run scoring cue-C = 0 is the very fact that recall is impossible without
the new capability. The primary check runs against the Layer-1 adapter (always
present). A second, engine-gated check confirms the Layer-2 engine *built and
then capped to 1* is identically incapable — it SKIPS until the engine exists,
then turns green, and can never drift above the ceiling.
"""

from _harness import require, try_import
from adapters import l1
import _l2score

CEILING_CUE_C = 100   # §5 L2 humility ceiling


def _assert_capped(engine, label):
    """The capped engine must abstain on cue recall: cue-C at or below ceiling."""
    state = _l2score.ingest_store(engine, lambda: engine.make_engine(1))
    r = _l2score.score(engine, state)
    require(r["cue_C"] <= CEILING_CUE_C,
            "%s: capped cue-C=%d exceeds the humility ceiling %d — the L2 gate "
            "would not be load-bearing" % (label, r["cue_C"], CEILING_CUE_C))
    # A read-by-time engine has no content index: it recovers nothing and,
    # crucially, fabricates nothing (it abstains, never guesses, §7.3).
    require(r["recovered"] == 0,
            "%s: a layer_cap=1 engine recovered %d cue targets — impossible "
            "without an associative index" % (label, r["recovered"]))
    require(r["fabricated"] == 0,
            "%s: a layer_cap=1 engine fabricated on %d unanswerable cues; "
            "missing capability must abstain, not invent (§7.3)" % (label, r["fabricated"]))
    return r


def trial_capped_read_by_time_engine_cannot_recall():
    # Primary: the layer_cap=1 Retention engine via the Layer-1 adapter. Present
    # from Layer 1, so this is the check that is green at the trials-first step.
    _assert_capped(l1, "L1-adapter make_engine(1)")


def trial_capped_l2_engine_at_cap1_is_identically_incapable():
    # Confirmation: the Layer-2 engine itself, constructed then capped to 1,
    # must behave identically (retains, abstains on recall). Engine-gated: SKIPS
    # until core/layers/l2_recall.py exists, then holds forever.
    l2 = try_import("adapters.l2",
                    "no L2 engine yet; capped-L2 confirmation engages when built")
    _assert_capped(l2, "L2-adapter make_engine(1)")


def trial_capped_engine_still_retains_and_abstains_not_raises():
    # The capped engine is a *genuine* retention engine, not a stub: read-by-time
    # works, only associative recall is absent (and absence is a scored
    # abstention, never an exception).
    state = _l2score.ingest_store(l1, lambda: l1.make_engine(1))
    hit = l1.query(state, {"op": "read", "t": 0})
    require(hit["status"] == "answer", "capped engine must still answer read-by-time")
    miss = l1.query(state, {"op": "recall", "cue": {"entity": 1, "key": "status", "val": "idle"}})
    require(miss["status"] == "abstain",
            "capped engine must abstain on recall, never raise (§7.3)")
    require(miss["value"] is None, "an abstention carries a null value")

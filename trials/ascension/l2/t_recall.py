"""ascension/l2 — Layer 2 (Recall) capability trials (BOUNDARY.md §5 L2).

Runs the shared cue tasks (`_l2tasks`) against the full recall engine
(`layer_cap = 2`) through the generic interface and scores them against the
ratified Layer-2 gate:

    cue-C >= 900,  F >= 950,  B = 1000.

The **same** tasks drive the humility trial against `make_engine(1)`, where they
must score cue-C <= 100 (`humility/l2/IMPOSSIBILITY.md`) — so this gate is proven
load-bearing on one task set. Engine-gated: SKIPS until
`core/layers/l2_recall.py` exists (the trials-first step of the ASCEND
sequence), then must clear the gate.

The cue tasks are content probes with **no `t`** and grammar-controlled
distractors (unique `(E,K,V)` target, ≥2 same-entity / same-key / same-val
distractors): recall must combine the whole probe — matching any single shared
atom lands on a distractor.
"""

from _harness import require, require_equal, try_import
import _l2score
import _l2tasks

GATE_CUE_C = 900
GATE_F = 950
GATE_B = 1000


def _engine():
    return try_import("adapters.l2",
                      "no L2 engine yet; recall ascension engages when built")


def trial_recall_meets_the_layer2_gate():
    l2 = _engine()
    state = _l2score.ingest_store(l2, l2.empty)
    r = _l2score.score(l2, state)
    require(r["cue_C"] >= GATE_CUE_C,
            "cue-C=%d below the L2 gate cue-C>=%d (recovered %d/%d)"
            % (r["cue_C"], GATE_CUE_C, r["recovered"], r["n_answerable"]))
    require(r["F"] >= GATE_F,
            "F=%d below the L2 gate F>=%d (wrong=%d, fabricated=%d)"
            % (r["F"], GATE_F, r["wrong"], r["fabricated"]))
    require(r["B"] >= GATE_B,
            "B=%d below the L2 gate B=%d — the index broke the budget"
            % (r["B"], GATE_B))
    # A wrong recall is worse than none (§3.0): the engine must never answer an
    # unanswerable cue, and never answer an answerable one incorrectly.
    require_equal(r["fabricated"], 0, "recall fabricated on an unanswerable cue")
    require_equal(r["wrong"], 0, "recall returned a wrong target on an answerable cue")


def trial_recall_answer_is_exact_with_recall_provenance():
    l2 = _engine()
    state = _l2score.ingest_store(l2, l2.empty)
    task = _l2tasks.answerable_tasks()[0]
    ans = l2.query(state, {"op": "recall", "cue": task["cue"]})
    require_equal(ans["status"], "answer", "a clean unique cue must be recalled, not abstained")
    require_equal(ans["value"], task["target_event"], "recall did not return the exact target event")
    require_equal(set(ans.keys()), {"status", "value", "confidence", "provenance"},
                  "Answer keys must be exactly status/value/confidence/provenance")
    require(isinstance(ans["confidence"], int) and 0 <= ans["confidence"] <= 1000,
            "confidence must be an integer permille in [0,1000] (§3.4)")
    prov = ans["provenance"]
    require(isinstance(prov, dict), "a recall hit must carry a provenance tag")
    require_equal(set(prov.keys()), {"support", "kind", "t_asof"}, "provenance keys wrong")
    require_equal(prov["kind"], "recall", "recall provenance kind must be 'recall'")
    require_equal(prov["support"], [task["target_t"]], "support must be exactly the target t")
    require_equal(prov["t_asof"], task["target_t"], "t_asof must be the target t")


def trial_recall_ascended_state_snapshot_restores_byte_identical():
    l2 = _engine()
    state = _l2score.ingest_store(l2, l2.empty)
    snap = l2.snapshot(state)
    restored = l2.restore(snap)
    require_equal(l2.snapshot(restored), snap,
                  "L2 snapshot/restore (index included) is not byte-identical")
    # And the restored state answers a cue identically to the original.
    cue = _l2tasks.answerable_tasks()[3]["cue"]
    require_equal(l2.query(state, {"op": "recall", "cue": cue}),
                  l2.query(restored, {"op": "recall", "cue": cue}),
                  "restored state answered a cue differently — index lost on restore")

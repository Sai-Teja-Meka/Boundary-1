"""ops/l2 — exact IO pairs for the Layer-2 index and recall (BOUNDARY.md §5 L2).

Fine-grained unit trials for the pieces recall is built from: atom derivation
(field-qualified tokens + `id#` adjacency), MinHash collision semantics,
deterministic budget refusal with the index counted, engine determinism, and the
recall Answer contract (§7.2). Corpus-scale scoring is the ascension class; these
are the correctness-of-the-pieces trials.
"""

from _harness import require, require_equal
from adapters import l2


# ---- atom derivation (token normalization; §5 L2) --------------------------

def trial_atoms_are_field_qualified_with_id_adjacency():
    unis = l2._unigrams({"kind": "attr", "entity": 7, "key": "region", "val": "north"})
    require("entity=7" in unis, "missing field-qualified entity atom")
    require("key=region" in unis, "missing field-qualified key atom")
    require("val=north" in unis, "missing field-qualified val atom")
    require("id#7" in unis, "missing cross-field entity-adjacency atom id#7")
    # A link over the same entity shares only the adjacency atom, never entity=7.
    link = l2._unigrams({"kind": "link", "src": 7, "dst": 9, "rel": "owns"})
    require("id#7" in link and "id#9" in link, "link must emit id# adjacency for src and dst")
    require("entity=7" not in link, "field-qualification must not conflate src with entity")
    require(unis & link == {"id#7"}, "attr and link about entity 7 must share exactly id#7")


def trial_qualification_prevents_cross_field_value_collision():
    # 'north' as an attr val and (hypothetically) as any other field must not
    # collide: qualified atoms differ by field.
    a = l2._atoms({"kind": "attr", "entity": 1, "key": "region", "val": "north"})
    b = l2._atoms({"kind": "move", "entity": 1, "loc": "north"})
    require("val=north" in a and "loc=north" in b, "value atoms must be field-qualified")
    require("val=north" not in b and "loc=north" not in a, "qualified value atoms leaked across fields")


# ---- MinHash collision semantics -------------------------------------------

def trial_minhash_collides_for_identical_atomsets_and_differs_otherwise():
    p = {"kind": "attr", "entity": 3, "key": "size", "val": "alpha"}
    q = {"kind": "attr", "entity": 3, "key": "size", "val": "beta"}
    sig_p1 = l2._minhash(l2._unigrams(p))
    sig_p2 = l2._minhash(l2._unigrams(dict(p)))
    require_equal(sig_p1, sig_p2, "MinHash is not deterministic for the same atom set")
    require_equal(len(sig_p1), l2.MINHASH_K, "MinHash signature has the wrong length")
    require(sig_p1 != l2._minhash(l2._unigrams(q)),
            "MinHash collided for materially different payloads")


# ---- budget refusal with the index counted (§4.1) --------------------------

def trial_write_refuses_over_budget_with_index_cost_included():
    p = {"kind": "attr", "entity": 1, "key": "status", "val": "active"}

    def fill(cap):
        s = l2.make_engine(2, budget_cap=cap)
        accepted, occ = 0, 0
        while True:
            s2, t = l2.write(s, {"kind": "attr", "entity": accepted % 5,
                                 "key": "status", "val": "active"})
            if t is None:
                return accepted, s
            s = s2
            accepted += 1
            require(s.occupancy <= cap, "occupancy exceeded the cap (§4.1)")

    a1, s1 = fill(400)
    a2, _s2 = fill(400)
    require_equal(a1, a2, "refusal point under the index-aware budget must be deterministic")
    require(a1 > 0, "at least one write should fit before the cap")
    require(s1.occupancy <= s1.budget_cap, "occupancy must never exceed the cap")
    # The index genuinely costs budget: an identical stream on a Layer-1 engine
    # (no index) fits MORE events under the same cap.
    l1s = l2.make_engine(1, budget_cap=400)
    l1_accepted = 0
    while True:
        l1s2, t = l2.write(l1s, {"kind": "attr", "entity": l1_accepted % 5,
                                 "key": "status", "val": "active"})
        if t is None:
            break
        l1s = l1s2
        l1_accepted += 1
    require(l1_accepted > a1,
            "the index must cost budget: a no-index engine should fit more events")


# ---- engine determinism (§2.3) ---------------------------------------------

def trial_two_identical_ingest_runs_snapshot_byte_identically():
    payloads = [{"kind": "attr", "entity": i % 7, "key": "tier", "val": "gamma"}
                for i in range(120)]

    def run():
        s = l2.empty()
        for p in payloads:
            s, _t = l2.ingest(s, p)
        return s

    require_equal(l2.snapshot(run()), l2.snapshot(run()),
                  "two identical ingest sequences produced different L2 snapshots")


# ---- recall Answer contract (§7.2) -----------------------------------------

def trial_recall_hit_answer_shape_and_provenance():
    s = l2.empty()
    payloads = [
        {"kind": "spawn", "entity": 1, "class": "vault"},
        {"kind": "attr", "entity": 1, "key": "region", "val": "north"},
        {"kind": "attr", "entity": 2, "key": "region", "val": "south"},
        {"kind": "attr", "entity": 1, "key": "tier", "val": "alpha"},
    ]
    ts = []
    for p in payloads:
        s, t = l2.ingest(s, p)
        ts.append(t)
    ans = l2.recall(s, {"entity": 1, "key": "region", "val": "north"})
    require_equal(ans["status"], "answer", "a unique probe must be recalled")
    require_equal(ans["value"], {"payload": payloads[1], "t": ts[1]}, "recall returned the wrong event")
    require_equal(set(ans.keys()), {"status", "value", "confidence", "provenance"}, "Answer keys wrong")
    require(isinstance(ans["confidence"], int) and 0 <= ans["confidence"] <= 1000,
            "confidence must be an integer permille in [0,1000]")
    require_equal(ans["provenance"], {"support": [ts[1]], "kind": "recall", "t_asof": ts[1]},
                  "recall provenance tag is wrong")


def trial_recall_abstains_on_absent_and_on_bad_cue_never_raises():
    s = l2.empty()
    for p in ({"kind": "attr", "entity": 1, "key": "region", "val": "north"},
              {"kind": "attr", "entity": 2, "key": "region", "val": "south"}):
        s, _t = l2.ingest(s, p)
    # absent probe (no event has this whole fingerprint) -> abstain
    miss = l2.recall(s, {"entity": 1, "key": "region", "val": "south"})
    require_equal(miss["status"], "abstain", "an absent probe must abstain, not fabricate")
    # malformed / non-canonical / non-dict cues abstain, never raise (§7.3)
    for bad in (None, 42, "cue", {"x": 1.5}, {"entity": 999}):
        ans = l2.recall(s, bad)
        require(ans["status"] in ("answer", "abstain"), "recall must never raise on a bad cue")


def trial_recall_abstains_when_capability_capped():
    s = l2.make_engine(1)   # read-by-time engine: no associative index
    for p in ({"kind": "attr", "entity": 1, "key": "region", "val": "north"},):
        s, _t = l2.ingest(s, p)
    ans = l2.query(s, {"op": "recall", "cue": {"entity": 1, "key": "region", "val": "north"}})
    require_equal(ans["status"], "abstain", "a capped engine must abstain on recall (§7.3)")
    # ...but it still retains: read-by-time works.
    require_equal(l2.query(s, {"op": "read", "t": 0})["status"], "answer",
                  "the capped engine must still answer read-by-time")

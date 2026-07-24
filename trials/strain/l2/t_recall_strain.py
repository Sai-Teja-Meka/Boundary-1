"""strain/l2 — Layer 2 (Recall) stress (BOUNDARY.md §6 strain, §5 L2).

Three strain families for the deterministic recall index:

  * **GA decoy-invariance.** Inject high-atom-count decoys that share **no atom**
    with a fixed cue; the cue's whole ranking (and its answer) must be
    **invariant**. This is the strain that indicts *store-relative / globally-
    normalized* scoring (Generative Agents' min-max recency normalization, GAPMAP
    V2): our scorer is **per-item** — `idf(a) = 1/df(a)`, a function of the atom's
    own document frequency, never of store size or a per-query min/max — so
    irrelevant decoys cannot move a fixed cue's ranking.
  * **Near-duplicate cue confusion (murk).** Over the murk corpus (`§8.7`, the
    near-duplicate family = verbatim restatements), a cue that matches a
    near-duplicated fact resolves to **two** identical events. Their MinHash
    signatures collide exactly, so the index recognizes the ambiguity and
    **abstains** — it does not fabricate one `t`. A unique fact in the same store
    is still recalled exactly (the contrast).
  * **Index-vs-log divergence.** The snapshot checksum covers **all** of state,
    index included: a single flipped bit anywhere is caught. And an index
    tampered *with its checksum recomputed* — a consistent-looking divergence —
    is still rejected, because `restore` rederives the index from the log and
    requires equality.
"""

import hashlib

from _harness import require, require_equal
from adapters import l2
from core.serialize import encode
from corpora.murk import generator as murk_gen
import _l2tasks


# ---- (a) GA decoy-invariance ----------------------------------------------

def _store_with(payloads):
    s = l2.empty()
    for p in payloads:
        s, t = l2.ingest(s, p)
        require(t is not None, "store ingest was refused unexpectedly")
    return s


def trial_decoy_injection_leaves_a_fixed_cue_ranking_invariant():
    base = _l2tasks.store_payloads()
    task = _l2tasks.answerable_tasks()[7]
    cue = task["cue"]

    s0 = _store_with(base)
    ranking0 = l2.recall_ranking(s0, cue)
    answer0 = l2.recall(s0, cue)
    require_equal(answer0["status"], "answer", "the fixed cue must resolve before decoys")
    require_equal(answer0["value"], task["target_event"], "wrong target before decoys")
    require(len(ranking0) > 1, "the cue should have several candidates (earned overlap)")

    # 300 heavy decoys sharing NO atom with the cue, appended after the store.
    decoys = _l2tasks.decoy_payloads(300, cue)
    s1 = _store_with(base + decoys)

    ranking1 = l2.recall_ranking(s1, cue)
    answer1 = l2.recall(s1, cue)

    require_equal(ranking1, ranking0,
                  "irrelevant decoys changed the cue's ranking — scoring is not per-item")
    require_equal(answer1["value"], answer0["value"],
                  "irrelevant decoys changed the recalled target")
    require_equal(answer1["confidence"], answer0["confidence"],
                  "irrelevant decoys changed the recall confidence")


def trial_decoys_are_genuinely_irrelevant_not_just_low_scoring():
    # Guard the guard: confirm the decoys really share no atom with the cue (so
    # the invariance above is meaningful, not an accident of weak overlap).
    cue = _l2tasks.answerable_tasks()[7]["cue"]
    cue_atoms = l2._atoms(cue)
    for d in _l2tasks.decoy_payloads(300, cue):
        require(l2._atoms(d).isdisjoint(cue_atoms),
                "a decoy shared an atom with the cue — decoy set is not irrelevant")


# ---- (b) near-duplicate cue confusion (murk) ------------------------------

_MURK_SEED = 3003
_MURK_N = 1200


def _murk_store():
    events, gt = murk_gen.generate_full(_MURK_SEED, _MURK_N)
    s = l2.empty()
    for p in events:
        s, t = l2.ingest(s, p)
        require(t is not None, "murk store ingest was refused unexpectedly")
    return s, events, gt


def trial_near_duplicate_cue_is_abstained_not_fabricated():
    s, events, gt = _murk_store()
    near = [d for d in gt["defects"] if d["type"] == "near_duplicate"]
    require(len(near) > 0, "expected near-duplicate defects in the murk store")

    checked = 0
    for d in near[:10]:
        orig_t, dup_t = d["refs"]
        require_equal(events[orig_t], events[dup_t],
                      "a near-duplicate defect is not a verbatim restatement")
        # MinHash collides exactly for verbatim near-duplicates.
        require_equal(s.index.sigs[orig_t], s.index.sigs[dup_t],
                      "verbatim near-duplicates did not collide under MinHash")
        # The cue is the restated payload itself: >=2 events fully match -> abstain.
        cue = events[orig_t]
        ans = l2.recall(s, cue)
        require_equal(ans["status"], "abstain",
                      "recall fabricated a single t for an ambiguous near-duplicate cue")
        require(ans["value"] is None, "an abstention carries a null value")
        checked += 1
    require(checked > 0, "no near-duplicate cue was actually exercised")


def trial_unique_fact_in_murk_store_is_recalled_exactly():
    s, events, _gt = _murk_store()
    # A payload that occurs exactly once in the store is unambiguous: recall it.
    counts = {}
    for ev in events:
        counts[encode(ev)] = counts.get(encode(ev), 0) + 1
    unique_t = None
    for t, ev in enumerate(events):
        if ev.get("kind") == "attr" and "val" in ev and counts[encode(ev)] == 1:
            unique_t = t
            break
    require(unique_t is not None, "expected at least one unique attr fact in the murk store")

    cue = events[unique_t]
    ans = l2.recall(s, cue)
    require_equal(ans["status"], "answer", "a unique fact must be recalled, not abstained")
    require_equal(ans["value"], {"payload": events[unique_t], "t": unique_t},
                  "recall returned the wrong event for a unique fact")


# ---- (c) index-vs-log divergence ------------------------------------------

def _tiny_store():
    s = l2.empty()
    for p in _l2tasks.store_payloads()[:24]:
        s, _t = l2.ingest(s, p)
    return s


def trial_uncorrupted_snapshot_restores_cleanly():
    s = _tiny_store()
    snap = l2.snapshot(s)
    restored = l2.restore(snap)
    require_equal(l2.snapshot(restored), snap, "clean L2 snapshot failed to round-trip")


def trial_single_bit_flip_anywhere_is_caught_including_index():
    s = _tiny_store()
    snap = l2.snapshot(s)
    caught = 0
    for i in range(len(snap)):
        corrupt = bytes(snap[:i]) + bytes([snap[i] ^ 0x01]) + bytes(snap[i + 1:])
        if corrupt == snap:
            continue
        try:
            l2.restore(corrupt)
        except Exception:
            caught += 1
        else:
            raise AssertionError(
                "a flipped bit at byte %d restored silently — corruption undetected" % i)
    require(caught == len(snap), "every single-bit corruption of a snapshot must be caught")


def _retampered(snap, mutate):
    """Decode a snapshot, mutate its body, RECOMPUTE the checksum, re-encode.

    Models an adversary (or a stale writer) who edits the body and fixes up the
    checksum — so only a semantic guard, not the checksum, can catch it.
    """
    from core.serialize import decode
    env = decode(snap)
    body = env["body"]
    mutate(body)
    checksum = hashlib.sha256(encode(body)).hexdigest()
    return encode({"magic": env["magic"], "checksum": checksum, "body": body})


def trial_tampered_index_with_recomputed_checksum_still_fails_loudly():
    s = _tiny_store()
    snap = l2.snapshot(s)

    def corrupt_a_posting(body):
        # Point some atom's posting at an event that does not carry it.
        for a, ts in body["index"]["postings"].items():
            body["index"]["postings"][a] = sorted(set(ts + [body["next_t"] - 1, 0]))
            break

    for mutate, label in ((corrupt_a_posting, "corrupted posting"),
                          (lambda b: b["index"]["sigs"].__setitem__(0, [0] * l2.MINHASH_K),
                           "corrupted signature")):
        bad = _retampered(snap, mutate)
        try:
            l2.restore(bad)
        except l2.CorruptSnapshot:
            continue
        raise AssertionError(
            "%s with a recomputed checksum restored silently (index-vs-log divergence "
            "undetected)" % label)


def trial_tampered_occupancy_with_recomputed_checksum_still_fails_loudly():
    s = _tiny_store()
    snap = l2.snapshot(s)
    bad = _retampered(snap, lambda body: body.__setitem__("occupancy", body["occupancy"] + 7))
    try:
        l2.restore(bad)
    except l2.CorruptSnapshot:
        return
    raise AssertionError("a tampered occupancy with a recomputed checksum restored silently")

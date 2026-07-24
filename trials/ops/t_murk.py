"""ops/ — the murk family: dirt is always paired with the answer key (§8.7).

Validates that every injected defect is recorded, that the answer key is
internally consistent, and that all four defect families are actually present
(guards the "silent zero family" failure mode).
"""

from _harness import require, require_equal
from corpora.murk import generator as murk_gen

_FAMILIES = ("contradiction", "near_duplicate", "ambiguity", "malformed")
_MALFORMATIONS = {"missing_field", "wrong_type", "unknown_kind", "dangling_ref"}


def _regen(seed, n):
    events, gt = murk_gen.generate_full(seed, n)
    return events, gt


def trial_murk_counts_are_consistent():
    events, gt = _regen(3003, 4000)
    require_equal(len(events), gt["n"], "event count != declared n")
    c = gt["counts"]
    total = sum(c[f] for f in _FAMILIES)
    require_equal(total, c["total_defects"], "family counts do not sum to total")
    require_equal(c["clean"] + c["total_defects"], gt["n"], "clean + defects != n")
    require_equal(len(gt["defects"]), c["total_defects"],
                  "defect list length != total_defects")


def trial_murk_all_families_present():
    _events, gt = _regen(3003, 4000)
    for fam in _FAMILIES:
        require(gt["counts"][fam] > 0,
                f"murk defect family '{fam}' has zero injections — dirt is missing")


def trial_murk_every_defect_maps_to_a_real_event():
    events, gt = _regen(3003, 4000)
    n = len(events)
    seen_t = set()
    for d in gt["defects"]:
        t = d["t"]
        require(0 <= t < n, f"defect t out of range: {d}")
        require(t not in seen_t, f"two defects recorded at the same t: {t}")
        seen_t.add(t)
        for r in d.get("refs", []):
            require(0 <= r < n, f"defect ref out of range: {d}")


def trial_murk_contradiction_semantics():
    events, gt = _regen(3003, 4000)
    cons = [d for d in gt["defects"] if d["type"] == "contradiction"]
    require(cons, "expected at least one contradiction")
    for d in cons:
        orig_t, cur_t = d["refs"]
        e0, e1 = events[orig_t], events[cur_t]
        require(e0["kind"] == "attr" and e1["kind"] == "attr",
                f"contradiction refs are not both attr events: {d}")
        require(e0["key"] == e1["key"] == "origin", f"contradiction not on 'origin': {d}")
        require(e0["entity"] == e1["entity"] == d["entity"],
                f"contradiction entities disagree: {d}")
        require(e0["val"] != e1["val"],
                f"contradiction values are equal (not a contradiction): {d}")
        require_equal(cur_t, d["t"], "contradiction t must be the re-assertion event")


def trial_murk_near_duplicate_semantics():
    events, gt = _regen(3003, 4000)
    dups = [d for d in gt["defects"] if d["type"] == "near_duplicate"]
    require(dups, "expected at least one near-duplicate")
    for d in dups:
        orig_t, dup_t = d["refs"]
        require_equal(events[orig_t], events[dup_t],
                      "near-duplicate must restate the prior fact verbatim")


def trial_murk_malformations_are_labelled():
    _events, gt = _regen(3003, 4000)
    mals = [d for d in gt["defects"] if d["type"] == "malformed"]
    require(mals, "expected at least one malformed payload")
    for d in mals:
        require(d["malformation"] in _MALFORMATIONS,
                f"unknown malformation label: {d}")


def trial_murk_scale_target_matches_doctrine():
    require(murk_gen.N == 10000, "murk scale target must be 10000 (§8.6)")

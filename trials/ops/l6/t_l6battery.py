"""ops/l6 — `corpora/l6battery` is what it says it is.

The generator, the composition, the answer keys and the declared reader, each
asserted rather than trusted. `trials/ascension/l6/ATTAINABILITY.md` computes the
Layer-6 arithmetic ON this battery; this file is what makes that arithmetic about
a fixed artifact instead of about whatever the generator happens to emit today.

**No gate constant is declared here and none is applied.** The battery binds
nothing: `RULING-R7-DRAFT.md` asks a human whether it should, and appending is
what freezes (`BOUNDARY.log` lines 21, 29, 31).
"""

import json
import os

from _harness import require, require_equal
from corpora import canon
from corpora.l6battery import generator as gen
from corpora.murk import generator as murk_gen

import _l4tasks
import _l6tasks


# ---- the generator ---------------------------------------------------------

def trial_the_battery_regenerates_byte_for_byte_from_its_seed():
    """§8.3, restated at the level this file owns.

    `laws/t_corpora_bytematch.py` already walks `registry.GENERATED` and would
    catch a drift; this asserts it again HERE, where the reason lives, because a
    battery whose queries could move is a battery no attainability arithmetic
    could rest on.
    """
    with open(gen.FROZEN_PATH, "rb") as fh:
        frozen = fh.read()
    require_equal(frozen, gen.frozen_bytes(),
                  "corpora/l6battery does not regenerate from (SEED, frozen murk)")


def trial_the_battery_is_canonical_json_with_one_trailing_newline():
    with open(gen.FROZEN_PATH, "rb") as fh:
        raw = fh.read()
    require(raw.endswith(b"\n"), "the frozen battery must end with one newline")
    require(not raw[:-1].endswith(b"\n"), "exactly one trailing newline")
    require_equal(canon.canon_encode(json.loads(raw.decode("utf-8"))), raw[:-1],
                  "the frozen battery is not canonical (§2.4)")


def trial_the_generator_reads_only_frozen_inputs():
    """The battery's substrate is the frozen murk corpus AND its frozen answer key.

    Both are named in the battery's own header, and both are byte-matched by the
    law trial — the answer key by its own clause, because §8.7 makes the key as
    frozen as the dirt it records.
    """
    battery = _l6tasks.battery()
    require_equal(battery["substrate"], os.path.basename(murk_gen.FROZEN_PATH),
                  "battery substrate")
    require_equal(battery["substrate_answer_key"],
                  os.path.basename(murk_gen.GROUND_TRUTH_PATH),
                  "battery answer key")
    require_equal(battery["seed"], gen.SEED, "battery seed")


# ---- the composition -------------------------------------------------------

DECLARED_COUNTS = {"K1": 355, "K2": 2130, "K3": 1065, "K4": 355,
                   "answerable": 3550, "unanswerable": 355, "total": 3905}


def trial_the_declared_composition_is_the_frozen_one():
    require_equal(dict(_l6tasks.battery()["counts"]), DECLARED_COUNTS,
                  "battery composition")


def trial_the_composition_is_ten_times_its_own_commitment_class():
    """K1 : K2 : K3 : K4 = 1 : 6 : 3 : 1, and K1 is the WHOLE family, unsampled.

    The multiples are the generator's declared constants; the unsampled half is
    the one that matters, because a battery that sampled its commitment class
    could be tuned by choosing which contradictions to ask about.
    """
    counts = _l6tasks.battery()["counts"]
    n1 = counts["K1"]
    require_equal(counts["K2"], gen.K2_MULTIPLE * n1, "K2 multiple")
    require_equal(counts["K3"], gen.K3_MULTIPLE * n1, "K3 multiple")
    require_equal(counts["K4"], gen.K4_MULTIPLE * n1, "K4 multiple")

    chains, order = gen.chains_of(_l6tasks.murk_payloads())
    whole_family = [p for p in order if p[1] in gen.SET_ONCE_KEYS]
    require_equal(n1, len(whole_family),
                  "K1 must be EVERY entity carrying a set-once assertion")
    asked = {(r["q"]["entity"], r["q"]["key"])
             for r in _l6tasks.battery()["queries"] if r["class"] == "K1"}
    require_equal(asked, set(whole_family), "K1 is the whole family, unsampled")


def trial_every_query_is_a_declared_op_over_a_declared_class():
    ops = {"K1": {"current"}, "K2": {"current"}, "K3": {"asof"},
           "K4": {"current"}}
    qids = []
    for record in _l6tasks.battery()["queries"]:
        qids.append(record["qid"])
        require(record["class"] in ops,
                "undeclared battery class: %r" % (record["class"],))
        require(record["q"]["op"] in ops[record["class"]],
                "class %s must not carry op %r"
                % (record["class"], record["q"]["op"]))
        require(isinstance(record["q"]["entity"], int)
                and not isinstance(record["q"]["entity"], bool),
                "every query names an integer entity")
        if record["q"]["op"] == "asof":
            require(isinstance(record["q"]["t"], int)
                    and not isinstance(record["q"]["t"], bool),
                    "an as-of query names an integer t")
    require_equal(qids, list(range(len(qids))), "qids are 0..N-1 in order")


# ---- the answer keys -------------------------------------------------------

def trial_the_commitment_keys_come_from_the_frozen_ground_truth():
    """K1's answer is the SET-ONCE value, and the frozen key is where it comes from.

    For a contradicted entity the true `origin` is the contradiction defect's
    `values[0]` — the value the clean base set before the knob re-asserted it.
    For an entity the knob never touched there is no defect and the entity's sole
    assertion is the answer. **The two derivations are asserted to agree wherever
    both exist**, so the key is not a preference this session expressed: it is the
    frozen ground truth and the frozen stream saying the same thing.
    """
    ground_truth = _l6tasks.murk_ground_truth()
    from_key = {}
    for defect in ground_truth["defects"]:
        if defect["type"] == "contradiction":
            from_key.setdefault((defect["entity"], defect["key"]),
                                defect["values"][0])
    require(len(from_key) > 0, "murk records no contradiction at all")

    chains, _order = gen.chains_of(_l6tasks.murk_payloads())
    checked = 0
    for record in _l6tasks.battery()["queries"]:
        if record["class"] != "K1":
            continue
        pair = (record["q"]["entity"], record["q"]["key"])
        first = chains[pair][0][1]
        require_equal(record["value"], first,
                      "K1 key must be the FIRST assertion for %r" % (pair,))
        if pair in from_key:
            require_equal(from_key[pair], first,
                          "ground truth and stream disagree on the set-once "
                          "value of %r" % (pair,))
            checked += 1
    require_equal(checked, len(from_key),
                  "every contradicted pair must carry a K1 query")


def trial_the_plain_keys_are_the_streams_own_latest_and_asof_values():
    chains, _order = gen.chains_of(_l6tasks.murk_payloads())
    for record in _l6tasks.battery()["queries"]:
        q = record["q"]
        pair = (q["entity"], q["key"])
        if record["class"] == "K2":
            require_equal(record["value"], chains[pair][-1][1],
                          "K2 key is the pair's latest value")
        elif record["class"] == "K3":
            steps = [s for s in chains[pair] if s[0] <= q["t"]]
            require_equal(record["value"], steps[-1][1],
                          "K3 key is the value in force at t")
            require(q["t"] < chains[pair][-1][0],
                    "K3 asks only about the PAST: a terminal assertion is the "
                    "K2 question wearing a t")
        elif record["class"] == "K4":
            require(pair not in chains,
                    "an absence probe must name a pair the corpus never asserts")
            require(record["answerable"] is False and record["value"] is None,
                    "an absence probe is unanswerable and carries no value")


def trial_the_facet_reading_is_the_layer_4_one_event_by_event():
    """One reading, two implementations — the ops/l4 and ops/l5 discipline.

    `corpora/l6battery.facet` and `trials/_l4tasks.facet` must agree on every one
    of murk's 10 000 payloads, because a divergence here would move an ANSWER KEY
    and not merely a query's availability.
    """
    payloads = _l6tasks.murk_payloads()
    require_equal(len(payloads), 10000, "murk scale")
    for t, payload in enumerate(payloads):
        require_equal(gen.facet(payload), _l4tasks.facet(payload),
                      "facet readings diverge at t=%d" % (t,))


# ---- the declared reader ---------------------------------------------------

def trial_the_declared_reader_is_what_the_frozen_engine_does():
    """The Stage-A arithmetic is engine-free; this is where it earns that.

    Every number in `ATTAINABILITY.md` is computed from
    `_l6tasks.declared_reader`, which is latest-wins restated engine-free. This
    replays the whole battery against the FROZEN Layer-5 engine at
    `DEFAULT_BUDGET` and requires the two to agree on all 3 905 queries, status
    and value — so the arithmetic is about the engine this project actually has
    and not about a convenient abstraction of it. It is a MEASUREMENT and not a
    gate: no §5 L6 clause is applied to the engine anywhere in this file.
    """
    from adapters import l5 as engine
    state = engine.new_state(layer_cap=5, budget_cap=engine.DEFAULT_BUDGET)
    for payload in _l6tasks.murk_payloads():
        state, _t = engine.ingest(state, payload)

    confidences = set()
    for record in _l6tasks.battery()["queries"]:
        answer = engine.query(state, record["q"])
        status, value = _l6tasks.declared_reader(record["q"])
        require_equal(answer["status"], status,
                      "engine and declared reader disagree on status at qid %d"
                      % (record["qid"],))
        if status == "answer":
            require_equal(answer["value"], value,
                          "engine and declared reader disagree on the value at "
                          "qid %d" % (record["qid"],))
        confidences.add(answer["confidence"])

    require_equal(confidences, {0, 1000},
                  "the frozen Layer-5 engine is CONFIDENT-BY-DEFAULT: every "
                  "answer carries 1000 and every abstention 0 (README-l5 §4, "
                  "§5.1 L6). A third value would mean a confidence model "
                  "appeared below Layer 6")


def trial_the_reader_errs_on_the_commitment_class_and_nowhere_else():
    """`n_neg > 0`, and exactly where the battery says it comes from.

    This is the number the whole Layer-6 arithmetic turns on
    (`PRE-READ.md §4.3` item 3): the error rate of the engine under test on the
    binding battery decides whether three of five clauses discriminate at all and
    whether AUROC is defined.
    """
    per_class = {}
    for row in _l6tasks._rows():
        hit, miss, abstained = per_class.get(row["cls"], (0, 0, 0))
        if row["reader_status"] != "answer":
            abstained += 1
        elif row["reader_correct"]:
            hit += 1
        else:
            miss += 1
        per_class[row["cls"]] = (hit, miss, abstained)

    require_equal(per_class["K1"], (197, 158, 0), "K1 (commitment)")
    require_equal(per_class["K2"], (2130, 0, 0), "K2 (current-value)")
    require_equal(per_class["K3"], (1065, 0, 0), "K3 (as-of)")
    require_equal(per_class["K4"], (0, 0, 355), "K4 (absence probes)")


def trial_the_error_rate_lies_in_the_band_both_ratified_clauses_admit():
    """The composition is FORCED, and this is the forcing, in arithmetic.

    `§5 L6`'s own `F ≥ 950` caps the error share at 50 permille with no
    abstentions (`1000w + 900a ≤ 50`); `Brier ≤ 40` discriminates against the
    base-rate constant baseline only where `w(1 − w) > 40/1000`. The battery's
    `w` must satisfy both, and does.
    """
    from fractions import Fraction
    rows = _l6tasks._rows()
    answered = [r for r in rows if r["reader_status"] == "answer"]
    wrong = sum(1 for r in answered if not r["reader_correct"])
    w = Fraction(wrong, len(answered))

    require_equal(len(answered), 3550, "the calibration denominator A")
    require_equal(wrong, 158, "n_neg under the declared reader")
    require(w <= Fraction(50, 1000),
            "F >= 950 caps w at 50 permille; this battery is at %s" % (w,))
    require(w * (1 - w) > Fraction(40, 1000),
            "Brier <= 40 does not discriminate against the base-rate constant "
            "at w = %s: w(1-w) = %s" % (w, w * (1 - w)))


# ---- the separability finding ----------------------------------------------

def trial_every_murk_defect_family_is_perfectly_separable_from_the_stream():
    """The finding that limits this battery, asserted rather than argued.

    §8.7 pairs every injected defect with its answer key AND injects it by
    visible construction, and the consequence is measurable: a stream-only rule
    recovers each family EXACTLY — symmetric difference 0 against the frozen key
    on all four. So on murk, evidence that RANKS also RESOLVES, and a reader that
    used the same evidence to answer rather than to hedge would drive `n_neg` to
    0 and take AUROC with it (§3.4). This battery therefore guarantees
    `n_neg > 0` for the DECLARED READING and not against an arbitrary reader —
    `ATTAINABILITY.md §6` and `RULING-R7-DRAFT.md` clause (iii) are where that is
    reported rather than hidden.
    """
    separability = _l6tasks.defect_separability()
    require_equal(sorted(separability),
                  ["ambiguity", "contradiction", "malformed", "near_duplicate"],
                  "all four murk families are probed")
    for family, (errors, size) in sorted(separability.items()):
        require(size > 0, "family %s is empty" % (family,))
        require_equal(errors, 0,
                      "family %s does not separate from the stream alone "
                      "(%d misclassified of %d) — if this ever becomes non-zero, "
                      "murk has acquired a class where evidence ranks without "
                      "resolving, which is exactly what the Layer-6 binding "
                      "artifact needs" % (family, errors, size))

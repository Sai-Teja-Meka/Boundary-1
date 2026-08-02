"""ops/l6 — `corpora/l6batteryb` (battery-b) is what it says it is.

Round 2 of Layer-6 Stage A. The generator, the composition, the answer key, the
declared reader — and, the reason this artifact exists at all, **the tie**.

Round 1's `corpora/l6battery` guaranteed `n_neg > 0` only *relative to the
declared latest-wins reading*, and measured why murk could not do better: `§8.7`
injects every defect by visible construction, so a stream-only rule recovers each
family exactly and a reader that used the evidence to ANSWER rather than to HEDGE
would drive `n_neg` to 0 and take `AUROC` with it. This file is where the
replacement's guarantee stops being a reading and becomes a **theorem**:

* **Theorem 1 (the tie)** — the two members of every mirror pair are
  observationally identical (identical event histories once the entity id is
  blanked, logical times differing by exactly `+1`), while one member's truth is
  its FIRST assertion and the other's is its LAST. So a reader that does not read
  the raw entity id errs on exactly one member of every pair;
* **Theorem 2 (the withholding)** — regenerating with every coin bit flipped
  produces a **byte-identical stream** and an answer key that differs on all 200
  forcing queries, so the stream carries zero bits about the coin and every
  class-E policy is unmoved by the flip.

Both are asserted here rather than argued in a README, and the second is the one
that closes the handle the first leaves.

**No gate constant is declared here and none is applied.** `RULING-R7-DRAFT.md`
asks a human whether battery-b should bind, and appending is what freezes
(`BOUNDARY.log` lines 21, 29, 31).

**Note added 2026-08-02 (`[L5] [RULING]`, `R7` recorded).** A human answered yes:
`R7` clause 1 binds **both sides** of the Layer-6 gate to `corpora/l6batteryb`,
and clause 3(b) makes a **forcing region** with a machine-checked proof the
standing precondition for any gate that cites `AUROC`. **Not one line of this
file changes for that** — the two theorems below were already trials, which is
exactly why the clause could be written as a requirement on artifacts: a region
that stopped forcing turns this file red BEFORE any gate is applied to any
engine.
"""

import json

from _harness import require, require_equal
from corpora import canon
from corpora.l6batteryb import generator as gen

import _l4tasks
import _l6btasks as tasks


# ---- the generator ---------------------------------------------------------

def trial_battery_b_regenerates_byte_for_byte_from_its_seed():
    """§8.3, restated where the reason lives.

    `laws/t_corpora_bytematch.py` walks `registry.GENERATED` and would catch a
    drift; this asserts it again HERE, because an artifact whose forcing region
    could move is an artifact no attainability arithmetic could rest on.
    """
    with open(gen.FROZEN_PATH, "rb") as fh:
        frozen = fh.read()
    require_equal(frozen, gen.frozen_bytes(),
                  "corpora/l6batteryb does not regenerate from its seed")


def trial_battery_b_is_canonical_json_with_one_trailing_newline():
    with open(gen.FROZEN_PATH, "rb") as fh:
        raw = fh.read()
    require(raw.endswith(b"\n"), "the frozen artifact must end with one newline")
    require(not raw[:-1].endswith(b"\n"), "exactly one trailing newline")
    require_equal(canon.canon_encode(json.loads(raw.decode("utf-8"))), raw[:-1],
                  "the frozen artifact is not canonical (§2.4)")


def trial_the_artifact_carries_its_substrate_its_key_and_its_queries_together():
    """One artifact, one byte-match — and the reason, asserted.

    The guarantee is a JOINT property of the stream, the key and the query set:
    a stream paired with a key from another generation would satisfy every
    per-file check and lose the theorem. So they are one canonical object, which
    is also the shape `corpora/l6battery` established for a non-JSONL member of
    `registry.GENERATED`.
    """
    artifact = tasks.artifact()
    for field in ("stream", "ground_truth", "queries"):
        require(field in artifact, "battery-b must carry %r" % (field,))
    require_equal(artifact["seed"], gen.SEED, "seed")
    require_equal(len(artifact["stream"]), gen.N_STREAM, "stream length")
    require_equal(artifact["ground_truth"]["seed"], gen.SEED,
                  "the answer key is the SAME generation as the stream")
    require_equal(artifact["ground_truth"]["n"], gen.N_STREAM,
                  "the answer key is the same generation as the stream")


# ---- the composition -------------------------------------------------------

DECLARED_COUNTS = {"K0": 200, "K2": 1400, "K3": 600, "K4": 200,
                   "answerable": 2200, "unanswerable": 200, "total": 2400}


def trial_the_declared_composition_is_the_frozen_one():
    require_equal(dict(tasks.artifact()["counts"]), DECLARED_COUNTS,
                  "battery-b composition")


def trial_the_composition_is_eleven_times_its_own_forcing_class():
    """`K0 : K2 : K3 : K4 = 1 : 7 : 3 : 1` of `r`, and K0 is the WHOLE region.

    The unsampled half is the one that matters: a battery that sampled its
    forcing class could be tuned by choosing which ties to ask about.
    """
    counts = tasks.artifact()["counts"]
    r = gen.REGION_QUERIES
    require_equal(counts["K0"], r, "the forcing class is the whole region")
    require_equal(counts["K2"], gen.K2_MULTIPLE * r, "K2 multiple")
    require_equal(counts["K3"], gen.K3_MULTIPLE * r, "K3 multiple")
    require_equal(counts["K4"], gen.K4_MULTIPLE * r, "K4 multiple")
    require_equal(counts["answerable"], 11 * r, "A = 11r")

    asked = {rec["q"]["entity"] for rec in tasks.queries()
             if rec["class"] == "K0"}
    require_equal(asked, tasks.region_ids(),
                  "K0 must ask about EVERY region entity and nothing else")


def trial_every_query_is_a_declared_op_over_a_declared_class():
    ops = {"K0": {"current"}, "K2": {"current"}, "K3": {"asof"},
           "K4": {"current"}}
    qids = []
    for record in tasks.queries():
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


def trial_the_facet_reading_is_the_layer_4_one_event_by_event():
    """One reading, two implementations — the ops/l4, ops/l5 and ops/l6 discipline.

    A divergence here would move an ANSWER KEY and not merely a query's
    availability.
    """
    payloads = tasks.stream()
    require_equal(len(payloads), gen.N_STREAM, "battery-b stream scale")
    for t, payload in enumerate(payloads):
        require_equal(gen.facet(payload), _l4tasks.facet(payload),
                      "facet readings diverge at t=%d" % (t,))


# ---- the forcing region: Theorem 1's premise -------------------------------

def trial_the_set_once_key_is_asserted_by_the_region_and_by_nothing_else():
    """`origin` is the region's key, exclusively — so the region is IDENTIFIABLE.

    That is deliberate and is not the same as being RESOLVABLE. An honest engine
    must be able to SEE a tie in order to price it at the tie's own confidence;
    what it must not be able to do is break it. The clean base draws its
    attribute keys from the chronicle vocabulary, which carries no set-once key,
    so this is structural rather than a filter that could be relaxed.
    """
    key = gen.SET_ONCE_KEYS[0]
    region_ids = tasks.region_ids()
    asserted = [t for t, p in enumerate(tasks.stream())
                if p.get("key") == key]
    require_equal(len(asserted), 2 * len(region_ids),
                  "every region entity carries exactly two set-once assertions")
    for t in asserted:
        require(tasks.stream()[t]["entity"] in region_ids,
                "a NON-region entity asserts the set-once key at t=%d — the "
                "forcing region would no longer be the whole of it" % (t,))
    for eid in sorted(region_ids):
        chain = tasks.chains()[(eid, key)]
        require_equal(len(chain), 2, "region chain length for %d" % (eid,))
        require(chain[0][1] != chain[1][1],
                "a region chain that agreed with itself would not be a tie")


def trial_the_two_members_of_every_mirror_pair_are_observationally_identical():
    """**Theorem 1's premise**, asserted at the level of the frozen bytes.

    Not a feature list — a feature list is exactly what made round 1's guarantee
    relative to a declared reading. What is required here is the whole of it: for
    every pair, the two members' COMPLETE event histories are equal as sequences
    once the entity id is blanked, and their logical times differ by exactly `+1`
    at every position. So the only thing in the entire artifact that distinguishes
    one member from the other is its raw id and a uniform one-step time shift,
    and `trial_the_stream_is_byte_identical_under_the_coin_complement` is where
    those are shown to carry no signal.
    """
    history = {}
    for t, payload in enumerate(tasks.stream()):
        for field in ("entity", "src", "dst"):
            who = payload.get(field)
            if isinstance(who, int) and not isinstance(who, bool):
                history.setdefault(who, []).append((t, payload))

    for p in tasks.region_pairs():
        h0, h1 = history[p["e0"]], history[p["e1"]]
        require_equal(len(h0), 3,
                      "a region entity's whole history is spawn + two "
                      "assertions; pair %d member 0 has %d events"
                      % (p["pair"], len(h0)))
        require_equal(len(h1), 3, "pair %d member 1" % (p["pair"],))
        for (t0, p0), (t1, p1) in zip(h0, h1):
            require_equal(t1, t0 + 1,
                          "pair %d: the members' logical times must differ by "
                          "exactly +1 at every position" % (p["pair"],))
            b0, b1 = dict(p0), dict(p1)
            b0["entity"] = b1["entity"] = "<member>"
            require_equal(b0, b1,
                          "pair %d: the members' payloads differ by more than "
                          "their entity id" % (p["pair"],))


def trial_exactly_one_member_of_every_pair_is_first_true_and_the_coin_is_balanced():
    """The other half of Theorem 1, and the closure of the id handle.

    One member's truth is its FIRST assertion and the other's is its LAST — which
    is what makes an identical answer to two identical questions wrong exactly
    once. And the coin is BALANCED, exactly `PAIRS//2` each way, which is what
    puts an id-keyed rule on the same total: such a rule takes both members of a
    pair or neither, and it is right on exactly half the pairs.
    """
    key = gen.SET_ONCE_KEYS[0]
    first_true_zero = 0
    for p in tasks.region_pairs():
        c0 = tasks.chains()[(p["e0"], key)]
        c1 = tasks.chains()[(p["e1"], key)]
        t0 = p["true"][0]
        t1 = p["true"][1]
        pos0 = 0 if t0 == c0[0][1] else 1
        pos1 = 0 if t1 == c1[0][1] else 1
        require(t0 in (c0[0][1], c0[1][1]) and t1 in (c1[0][1], c1[1][1]),
                "pair %d: a truth that is neither asserted value" % (p["pair"],))
        require_equal(pos0 + pos1, 1,
                      "pair %d: exactly one member must be first-true — this is "
                      "the whole tie" % (p["pair"],))
        require_equal(pos1, 1 - pos0, "pair %d positions" % (p["pair"],))
        if pos0 == 0:
            first_true_zero += 1
    require_equal(first_true_zero, gen.PAIRS // 2,
                  "the coin must be BALANCED, or an id-keyed or emission-order "
                  "rule would beat the region")
    require_equal(sum(tasks.ground_truth()["coin"]), gen.PAIRS // 2,
                  "the recorded coin is balanced too")


def trial_every_reader_on_the_bench_errs_on_exactly_one_member_of_every_pair():
    """**Theorem 1, EXHIBITED** — against readers built to break it.

    The tie is a claim about every reader, so it is demonstrated in the shape
    `strain/l3` established for its inflation guard and `strain/l5` for its
    ledger-blind policy: a bench of concrete readers, including the two that read
    the one handle Theorem 1 leaves. Every one of them errs on exactly `PAIRS`
    forcing queries — the blind ones by taking one member of each pair, the
    id-keyed ones by taking both members of half the pairs.

    `first-wins` is the reader that made round 1's guarantee relative: on
    `corpora/l6battery` it answered the whole commitment class correctly. Here it
    scores exactly what latest-wins scores.
    """
    for name, reader, kind in tasks.READER_BENCH:
        profile = tasks.region_error_profile(reader)
        total = sum(profile.values())
        require_equal(total, gen.PAIRS,
                      "reader %r must err on exactly one member per pair in "
                      "total (%d pairs)" % (name, gen.PAIRS))
        if kind == "blind":
            require_equal(sorted(set(profile.values())), [1],
                          "reader %r does not read the entity id, so Theorem 1 "
                          "puts it at exactly ONE error per pair" % (name,))
        else:
            require_equal(sorted(set(profile.values())), [0, 2],
                          "reader %r reads the id, so it takes both members of "
                          "a pair or neither" % (name,))
            require_equal(sum(1 for v in profile.values() if v == 2),
                          gen.PAIRS // 2,
                          "and the BALANCE is what puts it on the same total")


def trial_the_stream_is_byte_identical_under_the_coin_complement():
    """**Theorem 2** — the resolving signal is withheld, and this is the proof.

    Regenerating with every coin bit flipped produces the SAME stream, byte for
    byte, and an answer key that differs on every one of the 200 forcing
    queries. So the stream carries **zero** bits about the coin: a policy that
    resolves the region has obtained the coin from the answer key, which is class
    **O** by definition. This is the assertion that makes `n_neg > 0` a theorem
    rather than a property of a declared reading, and it is the one round 1's
    substrate could not have passed — on murk the contradiction knob always fires
    AFTER the value it corrupts, and that is a bit of the key written into the
    stream.
    """
    other_stream, other_key = tasks.complement_generation()
    require_equal(canon.canon_encode(other_stream),
                  canon.canon_encode(tasks.stream()),
                  "the stream must be byte-identical under the coin complement")

    frozen_key = {rec["qid"]: rec["value"] for rec in tasks.queries()}
    k0 = [rec["qid"] for rec in tasks.queries() if rec["class"] == "K0"]
    require_equal(len(k0), gen.REGION_QUERIES, "the forcing class")
    for qid in k0:
        require(frozen_key[qid] != other_key[qid],
                "forcing query %d has the same answer under both coins — it is "
                "not part of the withheld signal" % (qid,))
    for rec in tasks.queries():
        if rec["class"] != "K0":
            require_equal(other_key[rec["qid"]], frozen_key[rec["qid"]],
                          "the coin must move the FORCING class and nothing "
                          "else (qid %d)" % (rec["qid"],))


def trial_every_class_e_policy_is_unmoved_by_the_coin_complement():
    """Theorem 2's consequence, measured on the policies that matter.

    A class-E policy reads `evidence()`, which is a function of the stream, so
    flipping the coin must leave its answers, its confidences and every one of
    its scores exactly where they were, while the SET of queries it gets wrong on
    the region is exactly complemented. That is what "the guarantee is not
    relative to a reading" means when it is a measurement: `n_neg` does not move,
    and the 100 errors are a different 100.

    `conflict-rank`'s fitted levels are checked too, because a fit derived from
    measured accuracy would be key-derived if the accuracy moved — and it does
    not, since Theorem 1 pins the region's accuracy at exactly one half under
    either coin.
    """
    _stream, other_key = tasks.complement_generation()
    other_rows = tasks._rows_with(other_key)
    board = tasks.scoreboard()

    for name, policy, cls in tasks.POLICIES:
        if cls != "E":
            continue
        before = board[name]
        after = tasks.score(policy, rows=other_rows)
        require_equal(after["trace"], before["trace"],
                      "policy %r answers or states a different confidence under "
                      "the coin complement — it is reading the key" % (name,))
        for measure in ("A", "n_pos", "n_neg", "brier", "ece", "auroc",
                        "F_core", "F_all"):
            require_equal(after[measure], before[measure],
                          "policy %r moved on %s under the coin complement"
                          % (name, measure))

    wrong_before = {r["qid"] for r in tasks._rows()
                    if r["cls"] == "K0" and not r["reader_correct"]}
    wrong_after = {r["qid"] for r in other_rows
                   if r["cls"] == "K0" and not r["reader_correct"]}
    require_equal(len(wrong_before), gen.PAIRS, "errors before")
    require_equal(len(wrong_after), gen.PAIRS, "errors after")
    require(wrong_before.isdisjoint(wrong_after),
            "the complement must move every error to the OTHER member")
    require_equal(wrong_before | wrong_after,
                  {r["qid"] for r in tasks._rows() if r["cls"] == "K0"},
                  "and together they must be the whole forcing class")


# ---- the declared reader ---------------------------------------------------

def trial_the_declared_reader_is_what_the_frozen_engine_does():
    """The Stage-A arithmetic is engine-free; this is where it earns that.

    Every number in `ATTAINABILITY-B.md` is computed from
    `_l6btasks.declared_reader`. This replays the whole 12 000-event stream
    through the FROZEN Layer-5 engine at `DEFAULT_BUDGET` and requires the two to
    agree on all 2 400 queries, status and value. It is a MEASUREMENT and not a
    gate: no `§5 L6` clause is applied to the engine anywhere in this file.
    """
    from adapters import l5 as engine
    state = engine.new_state(layer_cap=5, budget_cap=engine.DEFAULT_BUDGET)
    for payload in tasks.stream():
        state, _t = engine.ingest(state, payload)
    require_equal(state.next_t, gen.N_STREAM,
                  "battery-b carries no intention, so one ingest is one t "
                  "(R6 clause 2's f = 0 case)")

    confidences = set()
    for record in tasks.queries():
        answer = engine.query(state, record["q"])
        status, value = tasks.declared_reader(record["q"])
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


def trial_the_reader_errs_on_the_forcing_class_and_nowhere_else():
    """All of battery-b's error mass is the region, BY CONSTRUCTION.

    The base stream is clean — no near-duplicate knob, no ambiguity knob, no
    malformed knob — so latest-wins is exactly right on every non-region query
    and `n_neg` is exactly `PAIRS`. That is what makes the band arithmetic below
    an identity rather than an estimate.
    """
    per_class = {}
    for row in tasks._rows():
        hit, miss, abstained = per_class.get(row["cls"], (0, 0, 0))
        if row["reader_status"] != "answer":
            abstained += 1
        elif row["reader_correct"]:
            hit += 1
        else:
            miss += 1
        per_class[row["cls"]] = (hit, miss, abstained)

    require_equal(per_class["K0"], (100, 100, 0), "K0 (the forcing region)")
    require_equal(per_class["K2"], (1400, 0, 0), "K2 (current-value)")
    require_equal(per_class["K3"], (600, 0, 0), "K3 (as-of)")
    require_equal(per_class["K4"], (0, 0, 200), "K4 (absence probes)")


def trial_the_error_rate_lies_in_the_band_all_three_ratified_clauses_admit():
    """The composition is FORCED, and this is the forcing, in arithmetic.

    Three ratified clauses pull against each other, and `A = 11r` sits inside all
    three. `w = (r/2)/A` is the wrong share of ANY committing reader — Theorem 1
    — so this band is a property of the artifact and not of a policy.
    """
    from fractions import Fraction
    r = gen.REGION_QUERIES
    rows = tasks._rows()
    answered = [row for row in rows if row["reader_status"] == "answer"]
    A = len(answered)
    wrong = sum(1 for row in answered if not row["reader_correct"])

    require_equal(A, 11 * r, "the calibration denominator A")
    require_equal(wrong, r // 2, "n_neg is exactly one member per pair")

    w = Fraction(wrong, A)
    bounds = tasks.band_bounds(r)
    require(A >= bounds["committer_F"],
            "F >= 950 for the honest committer needs A >= 10r; A = %d" % (A,))
    require(A < bounds["abstention_kills_F"],
            "blanket abstention on the region must BREAK F >= 950, which needs "
            "A < 18r; A = %d" % (A,))
    require(bounds["brier_beats_base_rate"](A),
            "Brier <= 40 does not discriminate against the base-rate constant "
            "at w = %s: w(1-w) = %s" % (w, w * (1 - w)))
    require(w <= Fraction(50, 1000),
            "F >= 950 caps w at 50 permille; this artifact is at %s" % (w,))

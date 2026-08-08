"""trials/_l8tasks.py — the Layer-8 Stage-A instruments: replay, policies, scorers.

`R2`'s standing step is *attainability arithmetic -> trials -> engine*, so
everything here runs with **no Layer-8 engine in existence**. What it does have is
a SUBSTRATE: the frozen Layer-7 engine, run over `corpora/l8describe`'s stream at
the artifact's declared cap, whose canonical snapshot is the state every policy
below describes and `trials/_l8derive.py` derives the key from.

## The policy classes, declared per `R5` clause 3

* **class E — the WITNESS.** `witness()` reads the engine's **snapshot bytes and
  nothing else**: not the frozen stream, not the answer key, not the declared
  class table, not `_l8derive`. It recovers the weight alphabet from the weights
  of its own reachable payloads, the kind vocabulary from its own counters and the
  entity population from its own interval table, and it abstains wherever its own
  state does not fix an answer. It is the `R8` clause 1 form: a witness that may
  not read the answer key, checked against its own **source** by
  `trials/ops/l8/t_l8describe.py`.
* **class O — the ORACLE.** `oracle()` reads the derivation's own key. It attains
  everything a Layer-8 gate could state and proves nothing, and it is here for
  exactly one purpose: to put a number on the *ceiling over all policies* so that
  the witness's shortfall can be read as a capability gap rather than assumed to
  be one.
* **the capability-free BASELINES.** `untagged()`, `flatterer()`,
  `blanket_abstainer()` — and `make_engine(7)`, which is not a policy at all but
  an engine, run through the generic interface exactly as `R8` clause 1 ran
  `make_engine(6)` and found it was the strongest baseline.

## The two instruments, and why they are two

`F` is scored against the **world** (`_l8derive.derive(..., strict=False)`): what
the frozen stream says, because `§3.0`'s *correct* is a claim about the value.
`groundedness` is scored against the **derivation** (`strict=True`): an answer to
a question the engine's own state does not determine is **ungrounded even when it
is lucky**. `BOUNDARY-HIGH.md §2.1` says in its own words why the second and not
the first is the discriminating quantity, and this module is where that stops
being a sentence and becomes two different numbers on the same policy.

Everything is integer arithmetic and `Fraction` (`§2.2`); permilles are computed
by `_permille` with `§3.5`'s round-half-to-even.
"""

from fractions import Fraction

import _l8derive as D


# --- permille ----------------------------------------------------------------

def permille(numerator, denominator):
    """`§3.5`: an exact ratio in permille, halves to the EVEN neighbour."""
    if denominator == 0:
        return None                                   # n/a — R8 clause 3(c)
    scaled = Fraction(numerator * 1000, denominator)
    floor = scaled.numerator // scaled.denominator
    rest = scaled - floor
    if rest > Fraction(1, 2):
        return floor + 1
    if rest < Fraction(1, 2):
        return floor
    return floor if floor % 2 == 0 else floor + 1


# --- the substrate replay ----------------------------------------------------

def replay(engine, artifact, layer_cap=7, budget_cap=None):
    """Run the artifact's stream through an engine; return (state, trace, body).

    The `trace` is `ingest`'s own return value per caller payload — `§7.1`'s
    contract and not an `Answer` — so `_l8derive`'s first constraint holds by
    construction. `B` is asserted after EVERY write by the caller (see
    `budget_report`), because `§4.1.2` refuses mid-stream and a self-model is
    state.
    """
    if budget_cap is None:
        budget_cap = artifact["declared"]["budget_cap"]
    state = engine.new_state(layer_cap, budget_cap)
    trace = []
    breaches = 0
    refused = 0
    for payload in artifact["stream"]:
        state, t = engine.ingest(state, payload)
        trace.append(t)
        if t is None:
            refused += 1
        if state.occupancy > state.budget_cap:
            breaches += 1
    return state, trace, {"refused": refused, "breaches": breaches,
                          "occupancy": state.occupancy,
                          "budget_cap": state.budget_cap}


def budget_report(report):
    """`§3.3`'s `B` in permille: 1000 iff occupancy never exceeded the cap."""
    return 0 if report["breaches"] else 1000


# --- the answer shape --------------------------------------------------------

def answer(value, support, kind="aggregate", t_asof=0, confidence=1000):
    return {"status": "answer", "value": value, "confidence": confidence,
            "provenance": {"support": list(support), "kind": kind,
                           "t_asof": t_asof}}


def untagged_answer(value, confidence=1000):
    return {"status": "answer", "value": value, "confidence": confidence,
            "provenance": None}


def abstain(confidence=0):
    return {"status": "abstain", "value": None, "confidence": confidence,
            "provenance": None}


# --- class E: the witness ----------------------------------------------------
#
# It reads the snapshot and nothing else. Every vocabulary it needs it recovers
# from its own state, which is what makes it a self-description rather than a
# lookup: the weight alphabet from the weights of its reachable payloads, the
# kinds from its own counters, the entities from its own interval table.

class Witness(object):
    """A concrete Layer-8 answering policy over a snapshot body. Class E."""

    def __init__(self, body, stream_for_rows):
        self.body = body
        # `stream_for_rows` is how a policy recovers a payload it still holds.
        # An ENGINE reads it out of its own rows; a Stage-A policy has no engine
        # to ask, so it takes the payload from the stream at a `t` its own state
        # says it still holds. The DECISION — which `t`s — is the snapshot's and
        # only the snapshot's, which is the property the ops trial checks by
        # blanking the stream and requiring every abstention to survive.
        self.reach = D.reachable_payloads(body, stream_for_rows)
        self.next_t = body.get("next_t", 0)
        self.t_asof = max(0, self.next_t - 1)
        self.alphabet = tuple(sorted({D.grammar_weight(p)
                                      for p in self.reach.values()}))
        self.kinds = tuple(sorted(k for k, _n in (body.get("counts") or [])))
        self.counts = dict(body.get("counts") or [])
        self.lengths = D._chain_lengths(self.reach)
        self.entities = tuple(sorted({e for (e, _k) in self.lengths}))
        self.keys = tuple(sorted({k for (_e, k) in self.lengths}))

    # -- support: reading (B) of `BOUNDARY-HIGH.md §5.1` ----------------------
    #
    # *The support is bounded after all: a self-descriptive answer cites the `t`s
    # the derivation procedure reads.* The witness cites exactly the `t`s its own
    # fold touched, `kind = "aggregate"` (`§4.2.3`'s own vocabulary, unchanged and
    # unextended), `t_asof = next_t - 1`. Nothing is minted and no frozen layer is
    # edited; `ATTAINABILITY.md §6.1` measures what it costs.

    def _fold(self, predicate):
        touched = sorted(t for t, p in self.reach.items() if predicate(p))
        return len(touched), touched

    def ask(self, q):
        of = q.get("of")
        if q.get("op") != "census":
            return abstain()

        if of == "reach":
            return answer(len(self.reach), sorted(self.reach), t_asof=self.t_asof)

        if of == "kind":
            kind = q.get("kind")
            if kind not in self.counts:
                return abstain()
            n, touched = self._fold(lambda p: p.get("kind") == kind)
            return answer(n, touched, t_asof=self.t_asof)

        if of == "weight":
            w = q.get("w")
            if w not in self.alphabet:
                return abstain()
            n, touched = self._fold(lambda p: D.grammar_weight(p) == w)
            return answer(n, touched, t_asof=self.t_asof)

        if of == "key":
            key = q.get("key")
            if key not in self.keys:
                return abstain()
            n, touched = self._fold(lambda p: p.get("key") == key)
            return answer(n, touched, t_asof=self.t_asof)

        if of == "chain":
            minimum = q.get("min")
            if not isinstance(minimum, int) or isinstance(minimum, bool):
                return abstain()
            if not self.lengths or minimum > max(self.lengths.values()):
                return abstain()
            pairs = [pair for pair, n in self.lengths.items() if n >= minimum]
            touched = sorted(t for t, p in self.reach.items()
                             if (p.get("entity"), p.get("key")) in set(pairs))
            return answer(len(pairs), touched, t_asof=self.t_asof)

        if of == "pairs":
            n, touched = self._fold(lambda p: p.get("kind") == "attr")
            return answer(len(self.lengths), touched, t_asof=self.t_asof)

        if of == "entity_pairs":
            entity = q.get("entity")
            if entity not in self.entities:
                return abstain()
            n = sum(1 for (e, _k) in self.lengths if e == entity)
            touched = sorted(t for t, p in self.reach.items()
                             if p.get("entity") == entity)
            return answer(n, touched, t_asof=self.t_asof)

        if of == "lost":
            record = self.body.get("forgetting") or {}
            return answer(record.get("count", 0), sorted(self.reach),
                          t_asof=self.t_asof)

        if of == "lost_kind":
            kind = q.get("kind")
            if kind not in self.counts:
                return abstain()
            held, touched = self._fold(lambda p: p.get("kind") == kind)
            return answer(self.counts[kind] - held, touched, t_asof=self.t_asof)

        if of == "lost_at":
            span = D.bucket_range(self.body, q.get("bucket"))
            if span is None:
                return abstain()
            buckets = (self.body.get("forgetting") or {}).get("buckets") or []
            return answer(buckets[q["bucket"]][0], sorted(self.reach),
                          t_asof=self.t_asof)

        if of in ("lost_weight", "lost_weight_at"):
            w = q.get("w")
            if w not in self.alphabet:
                return abstain()
            bucket = q.get("bucket") if of == "lost_weight_at" else None
            if of == "lost_weight_at" and \
                    D.bucket_range(self.body, bucket) is None:
                return abstain()
            admitted = D.bounds_lost_weight(self.body, self.alphabet, w, bucket)
            if admitted is None or len(admitted) != 1:
                # THE HONEST ABSTENTION, and the whole layer in one branch: the
                # record fixes `(count, mass)` and the alphabet has three weights,
                # so where the system admits more than one composition the state
                # does not determine the answer and `§7.3` says what to do about
                # it. An engine that answered here would be guessing about itself.
                return abstain()
            return answer(admitted[0], sorted(self.reach), t_asof=self.t_asof)

        return abstain()


def witness(body, stream):
    w = Witness(body, stream)
    return {entry_qid: w for entry_qid in ()} or w      # a policy object


# --- the capability-free baselines -------------------------------------------

def run_policy(policy, artifact):
    """`{qid: Answer}` for a policy exposing `.ask(q)`."""
    return {e["qid"]: policy.ask(e["q"]) for e in artifact["queries"]}


class Untagged(object):
    """THE UNTAGGED SELF-DESCRIBER — `BOUNDARY-HIGH.md §5.1`'s ruled freedom.

    Byte-for-byte the witness's values, with `provenance: null`. `§4.2.2` scores a
    non-abstaining untagged answer **0 regardless of whether its value is
    correct**, and the SPEC rules that *no Layer-8 gate may be cleared by an
    engine whose self-descriptive answers are untagged*. This baseline is that
    ruling demonstrated rather than asserted: it is exactly as capable as the
    witness and no gate is reachable.
    """

    def __init__(self, inner):
        self.inner = inner

    def ask(self, q):
        got = self.inner.ask(q)
        if got["status"] != "answer":
            return got
        return untagged_answer(got["value"], got["confidence"])


class Flatterer(object):
    """THE SELF-AGGRANDIZING ENGINE — groundedness claimed above evidence.

    It answers everything the witness answers AND everything the witness abstains
    on, taking the most flattering admissible value where its state only bounds
    the answer (the largest composition consistent with the record) and 0 where
    its state says nothing at all. Every answer is tagged and confident. It is the
    policy `F` alone cannot separate from a describer, and the one groundedness
    exists to catch.
    """

    def __init__(self, inner):
        self.inner = inner

    def ask(self, q):
        got = self.inner.ask(q)
        if got["status"] == "answer":
            return got
        w = self.inner
        of = q.get("of")
        if of in ("lost_weight", "lost_weight_at"):
            bucket = q.get("bucket") if of == "lost_weight_at" else None
            admitted = D.bounds_lost_weight(w.body, w.alphabet, q.get("w"),
                                            bucket)
            if admitted:
                return answer(max(admitted), sorted(w.reach), t_asof=w.t_asof)
        return answer(0, sorted(w.reach) or [0], t_asof=w.t_asof)


class BlanketAbstainer(object):
    """`§7.3`'s scored abstention, taken as a whole policy.

    `§3.0` pays an abstention **100**, so an engine that describes nothing is not
    at zero — it is at the abstention floor. `BOUNDARY-HIGH.md §5.4` says `F`
    therefore cannot carry `R2` obligation 2 at this layer, and `§4.1` states the
    humility ceiling over a **capability quantity** for exactly this reason. This
    baseline is where both sentences are measured.
    """

    def ask(self, q):
        return abstain()


class Oracle(object):
    """Class O. Reads the key; attains everything; proves nothing (`R5` clause 3)."""

    def __init__(self, key, t_asof, support):
        self.key = key
        self.t_asof = t_asof
        self.support = support
        self._qid = {}

    def bind(self, artifact):
        for entry in artifact["queries"]:
            self._qid[_freeze(entry["q"])] = entry["qid"]
        return self

    def ask(self, q):
        verdict = self.key.get(self._qid.get(_freeze(q)))
        if verdict is None or verdict[0] != "value":
            return abstain()
        return answer(verdict[1], self.support, t_asof=self.t_asof)


def _freeze(q):
    return tuple(sorted((k, _freeze(v) if isinstance(v, dict) else v)
                        for k, v in q.items()))


class CappedEngine(object):
    """`make_engine(7)` through the generic interface — an ENGINE, not a policy.

    `§7.4` caps at construction only: the capped engine speaks the identical
    `ingest`/`query`/`snapshot` interface and surfaces missing capability as a
    scored abstention, never an exception. `BOUNDARY-HIGH.md §4.1` is why this is
    well-defined without any harness convention — *the verb is not the
    vocabulary*: `query` is `query`, and an introspective op it does not support
    abstains under `§7.3`.
    """

    def __init__(self, engine, state):
        self.engine = engine
        self.state = state

    def ask(self, q):
        return self.engine.query(self.state, q)


# --- the scorers -------------------------------------------------------------

def _valid_tag(tag, ingested_max, validate):
    ok, _why = validate(tag, ingested_max)
    return ok


def score(answers, artifact, key_strict, key_world, ingested_max, validate):
    """Every `BOUNDARY-HIGH.md §2.1` quantity for one policy, in one pass.

    Denominators are the SPEC's, class by class (`R7` clause 2, `R8` clause 3):

      * `coverage`   — the artifact's DECLARED introspection class, WHOLE. A
                       property of the artifact, so no engine can empty it.
      * `F_core`     — the answerable core (`KR ∪ KL ∪ KF`); `F_all` over the
                       whole set, ungated (`R3` / `R4` clause 4's shape).
      * `groundedness` — the engine's ANSWERED self-descriptions inside the class.
                       The engine's own report, admissible under `R8` clause 3(a)
                       because every member is harness-checkable AND shrinking it
                       costs `coverage`. Empty ⇒ `None` ⇒ `n/a`, which
                       DISQUALIFIES (clause 3(c)).
      * `tagging`    — the non-abstaining answers inside the class.
      * `ECE`        — `§3.4`'s own denominator, the `A` answered queries
                       (`R8` clause 6), exact and binned (`R7` clauses 4–5).
      * `capability` — the ceiling measure of `BOUNDARY-HIGH.md §4.1`: a COUNT of
                       self-descriptions that are simultaneously answered,
                       grounded and tagged, over the whole declared class, never
                       `F`. An abstention contributes nothing to it.
    """
    classes = {e["qid"]: e["class"] for e in artifact["queries"]}
    answerable = {e["qid"]: e["answerable"] for e in artifact["queries"]}
    total = len(artifact["queries"])
    core = [qid for qid, ok in answerable.items() if ok]

    answered = grounded = tagged = capability = 0
    f_core_num = f_all_num = 0
    conf_pairs = []                       # (confidence, correct) for §3.4
    ungrounded_answers = []
    by_class = {}

    for qid, got in sorted(answers.items()):
        klass = classes[qid]
        slot = by_class.setdefault(klass, {"answered": 0, "grounded": 0,
                                           "tagged": 0, "abstained": 0})
        strict = key_strict[qid]
        world = key_world[qid]
        is_answer = got.get("status") == "answer"
        tag_ok = is_answer and _valid_tag(got.get("provenance"), ingested_max,
                                          validate)

        if is_answer:
            answered += 1
            slot["answered"] += 1
            value_ok = world[0] == "value" and got.get("value") == world[1]
            ground_ok = strict[0] == "value" and got.get("value") == strict[1]
            if ground_ok:
                grounded += 1
                slot["grounded"] += 1
            else:
                ungrounded_answers.append(qid)
            if tag_ok:
                tagged += 1
                slot["tagged"] += 1
            if ground_ok and tag_ok:
                capability += 1
            # §3.0: correct-and-tagged 1000; correct-but-untagged 0 (§4.2.2,
            # R8 clause 8(a)'s third zero); wrong 0; fabricate 0.
            paid = 1000 if (value_ok and tag_ok) else 0
            conf_pairs.append((got.get("confidence"), value_ok))
        else:
            slot["abstained"] += 1
            # An abstention on an ANSWERABLE query costs 900; on an unanswerable
            # one it is the correct answer and scores 1000 (the L4/L5 precedent).
            paid = 100 if answerable[qid] else 1000

        f_all_num += paid
        if answerable[qid]:
            f_core_num += paid

    ece_value, bins, n_pos, n_neg = ece(conf_pairs)

    return {
        "coverage": permille(grounded, total),
        "coverage_n": grounded,
        "F_core": permille(f_core_num, 1000 * len(core)) if core else None,
        "F_all": permille(f_all_num, 1000 * total),
        "groundedness": permille(grounded, answered),
        "tagging": permille(tagged, answered),
        "answered": answered,
        "grounded": grounded,
        "tagged": tagged,
        "capability": capability,
        "capability_pm": permille(capability, total),
        "ece": ece_value,
        "A": len(conf_pairs),
        "n_pos": n_pos,
        "n_neg": n_neg,
        "auroc": auroc(conf_pairs),
        "ungrounded": ungrounded_answers,
        "by_class": by_class,
        "total": total,
        "core": len(core),
    }


def ece(pairs):
    """`§3.4`'s ECE, exact (`R7` clause 4) at `R7` clause 5's bin index.

    `bin(conf) = 9 if conf == 1000 else conf // 100`. Returns
    `(ece_permille, bins, n_pos, n_neg)`; `None` where `A == 0`.
    """
    if not pairs:
        return None, {}, 0, 0
    bins = {}
    for conf, correct in pairs:
        index = 9 if conf == 1000 else conf // 100
        slot = bins.setdefault(index, [0, 0, 0])       # n, Σconf, Σcorrect
        slot[0] += 1
        slot[1] += conf
        slot[2] += 1 if correct else 0
    total = len(pairs)
    gap = Fraction(0)
    for index in sorted(bins):
        n, conf_sum, correct = bins[index]
        mean_conf = Fraction(conf_sum, n * 1000)
        accuracy = Fraction(correct, n)
        gap += Fraction(n, total) * abs(mean_conf - accuracy)
    n_pos = sum(1 for _c, ok in pairs if ok)
    return (permille(gap.numerator, gap.denominator), bins,
            n_pos, total - n_pos)


def auroc(pairs):
    """`§3.4`'s AUROC over (confidence, correct); `None` where a class is empty.

    `R7` clause 3: `n/a` disqualifies, it does not excuse — *a gate is an
    instrument, an instrument has a range, and outside it the honest output is
    not a pass but a refusal to certify.* Ties count a half.
    """
    pos = [c for c, ok in pairs if ok]
    neg = [c for c, ok in pairs if not ok]
    if not pos or not neg:
        return None
    u = 0
    for a in pos:
        for b in neg:
            u += 2 if a > b else (1 if a == b else 0)
    return permille(u, 2 * len(pos) * len(neg))


# --- the Stage-A fixture, computed once ---------------------------------------
#
# The replay costs ~0.3 s and every trial in `ops/l8` and `ascension/l8` wants the
# same state, so it is memoised here rather than repeated. `[L4]`'s 663 s capped
# replay is the standing reason a Stage-A module states its own bill.

_FIXTURE = {}

FIELD_READERS = ("counts[kind]", "counts[kind]-as-lost", "next_t-forgetting.count",
                 "forgetting.count", "forgetting.buckets[b][0]", "occupancy",
                 "demotions", "chain-entity-count")


def field_reader_bench(body):
    """A bench of NAMED single-field readers — the sixth-substrate-kill test.

    `BOUNDARY-HIGH.md §3`'s fourth constraint: *a class made entirely of questions
    whose answers are single fields of the snapshot certifies the engine's layout
    and measures nothing.* The `l7compose` precedent is a bench of six labellers
    each measuring exactly 100 errors; this is its Layer-8 form, and it is a bench
    of readers rather than a search for coincident integers because *"some integer
    in the snapshot happens to equal the answer"* is not a policy anyone could
    write.
    """
    counts = dict(body.get("counts") or [])
    record = body.get("forgetting") or {}
    buckets = record.get("buckets") or []

    def by_counts(q):
        return counts.get(q.get("kind")) if q.get("of") == "kind" else None

    def by_counts_lost(q):
        return counts.get(q.get("kind")) if q.get("of") == "lost_kind" else None

    def by_reach(_q):
        return body.get("next_t", 0) - record.get("count", 0)

    def by_forget(_q):
        return record.get("count")

    def by_bucket(q):
        b = q.get("bucket")
        return buckets[b][0] if isinstance(b, int) and 0 <= b < len(buckets) \
            else None

    def by_occupancy(_q):
        return body.get("occupancy")

    def by_demotions(_q):
        return body.get("demotions")

    def by_chain_entities(_q):
        return sum(len(entry[1]) for entry in body.get("chains") or ()
                   if isinstance(entry, list) and len(entry) == 2)

    return dict(zip(FIELD_READERS,
                    (by_counts, by_counts_lost, by_reach, by_forget, by_bucket,
                     by_occupancy, by_demotions, by_chain_entities)))


class ShallowDescriber(object):
    """The FIELD-READER baseline: everything the bench can reach, and nothing else.

    It is the measured form of the predicted sixth substrate kill — *a question
    forced to come from a fold may also be trivially answerable from a field* —
    turned from a worry into a scored policy, so that the fold-only remainder is a
    number rather than a claim.
    """

    def __init__(self, body, t_asof, support):
        self.bench = field_reader_bench(body)
        self.t_asof = t_asof
        self.support = support

    def ask(self, q):
        # Dispatch by the question's SHAPE to the reader shaped for it — a
        # policy someone could actually write — rather than trying every reader
        # and keeping whichever happens to be right, which would need the key.
        of = q.get("of")
        reader = {"kind": "counts[kind]",
                  "lost_kind": "counts[kind]-as-lost",
                  "reach": "next_t-forgetting.count",
                  "lost": "forgetting.count",
                  "lost_at": "forgetting.buckets[b][0]",
                  "lost_weight_at": "forgetting.buckets[b][0]"}.get(of)
        if reader is None:
            return abstain()
        try:
            got = self.bench[reader](q)
        except Exception:
            got = None
        if got is None:
            return abstain()
        return answer(got, self.support, t_asof=self.t_asof)


def stage_a():
    """The whole Stage-A measurement, memoised. Returns a plain dict."""
    if _FIXTURE:
        return _FIXTURE
    import corpora.l8describe.generator as generator
    from adapters import l7 as engine
    from laws.t_provenance_schema import validate_provenance

    artifact = generator.load()
    state, trace, report = replay(engine, artifact)
    body = D.body_of(engine.snapshot(state))
    key_strict = D.derive_all(artifact, body, trace, strict=True)
    key_world = D.derive_all(artifact, body, trace, strict=False)
    ingested_max = max(t for t in trace if t is not None)

    w = Witness(body, artifact["stream"])
    support = sorted(w.reach)
    policies = {
        "witness": w,
        "oracle": Oracle(key_strict, w.t_asof, support).bind(artifact),
        "untagged": Untagged(w),
        "flatterer": Flatterer(w),
        "abstainer": BlanketAbstainer(),
        "shallow": ShallowDescriber(body, w.t_asof, support),
        "capped7": CappedEngine(engine, state),
    }
    scores = {}
    answers = {}
    for name, policy in policies.items():
        answers[name] = run_policy(policy, artifact)
        scores[name] = score(answers[name], artifact, key_strict, key_world,
                             ingested_max, validate_provenance)

    _FIXTURE.update({
        "artifact": artifact, "engine": engine, "state": state, "trace": trace,
        "body": body, "key_strict": key_strict, "key_world": key_world,
        "ingested_max": ingested_max, "report": report, "witness": w,
        "policies": policies, "answers": answers, "scores": scores,
        "key_bytes": D.key_bytes(key_strict),
    })
    return _FIXTURE

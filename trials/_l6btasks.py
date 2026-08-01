"""trials/_l6btasks.py — the Layer-6 battery-b calibration battery (engine-free).

Round 2 of Layer-6 Stage A. Nothing here touches an engine, so it is importable
before `core/layers/l6_meta_memory.py` exists — the trials-first step of the
ASCEND sequence (**BOUNDARY-RULINGS.md R2**).

It carries five things, in one place so they can never disagree:

1. **the declared reader** — latest-wins, which is what every layer this project
   has frozen implements;
2. **the reader bench** — first-wins, latest-wins, canonical-min, canonical-max
   and two id-keyed rules, each scored on the forcing region, because the tie is
   a claim that must be *exhibited against readers that try to break it* rather
   than asserted about a family;
3. **the evidence extractor** — the closed, declared feature vocabulary a
   confidence policy may read, computed from the frozen stream **alone**;
4. **the policies** — the exhibited witness and every named capability-free
   baseline, each a pure map from evidence to an integer permille;
5. **the measures** — imported verbatim from `_l6tasks`, so round 1's numbers and
   round 2's are produced by ONE instrument and are comparable by construction.

## What round 2 changes

Round 1's `corpora/l6battery` guaranteed `n_neg > 0` *relative to the declared
latest-wins reading*: a first-wins reader would have answered its whole
commitment class correctly and taken `AUROC` with it
(`ascension/l6/ATTAINABILITY.md §6`). `corpora/l6batteryb` removes that. Its
forcing region is 100 **mirror pairs** whose two members are observationally
identical and whose truths sit at opposite ends of their chains, with the
resolving coin **withheld at generation** — so every committing reader errs on
exactly one member of every pair, `n_neg = 100` is a theorem, and `AUROC` is
defined for reasons no session declared.

`trials/ascension/l6/ATTAINABILITY-B.md` is the prose of what this module
computes; `trials/ascension/l6/t_attainability_b.py` asserts that the two agree.
"""

import json
import os
from fractions import Fraction

from corpora.l6batteryb import generator as gen

# ONE INSTRUMENT. §3.4's three quantities and §3.1's fidelity are `_l6tasks`'
# own, unchanged — a round-2 Brier and a round-1 Brier are the same function of
# the same shape of input, so the two artifacts can be compared without a
# caveat about the ruler.
from _l6tasks import permille, brier, ece, auroc, fidelity  # noqa: F401

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SET_ONCE_KEYS = gen.SET_ONCE_KEYS
PAIRS = gen.PAIRS
REGION_QUERIES = gen.REGION_QUERIES

_CACHE = {}


# ---- the frozen artifact ---------------------------------------------------

def artifact():
    if "artifact" not in _CACHE:
        _CACHE["artifact"] = gen.load()
    return _CACHE["artifact"]


def stream():
    """The substrate — everything a class-E policy is allowed to read."""
    return artifact()["stream"]


def ground_truth():
    """The answer key — class O only."""
    return artifact()["ground_truth"]


def queries():
    return artifact()["queries"]


def chains():
    if "chains" not in _CACHE:
        built, order = gen.chains_of(stream())
        _CACHE["chains"] = built
        _CACHE["order"] = order
    return _CACHE["chains"]


def region_pairs():
    return ground_truth()["pairs"]


def region_ids():
    if "region_ids" not in _CACHE:
        ids = set()
        for p in region_pairs():
            ids.add(p["e0"])
            ids.add(p["e1"])
        _CACHE["region_ids"] = ids
    return _CACHE["region_ids"]


def _canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _prefix(pair, horizon):
    chain = chains().get(pair)
    if chain is None:
        return []
    if horizon is None:
        return chain
    return [step for step in chain if step[0] <= horizon]


# ---- the readers -----------------------------------------------------------
#
# A READER answers a query from the stream. A POLICY (below) attaches a
# confidence to a reader's answer. The distinction is the one §5 L6 draws in its
# own words — it asks for "confidence permille from structural evidence", not
# for a second reader — and on battery-b it is load-bearing: the forcing region
# is exactly the class no reader can get right.

def read_latest(steps):
    return steps[-1][1]


def read_first(steps):
    return steps[0][1]


def read_canonical_min(steps):
    return min((s[1] for s in steps), key=_canon)


def read_canonical_max(steps):
    return max((s[1] for s in steps), key=_canon)


def _id_keyed(prefer_first_when_even):
    """A reader that keys on the raw entity id — the one handle Theorem 1 leaves.

    Region ids are consecutive (`e1 = e0 + 1`) and members are emitted in id
    order, so id parity, emission order and "the lower id" are the same handle.
    It carries no signal because the coin is BALANCED: such a rule takes both
    members of a pair when it is right and both when it is wrong, and it is right
    on exactly half the pairs.
    """
    def reader(steps, entity=None, **_kw):
        even = (entity % 2 == 0)
        first = even if prefer_first_when_even else (not even)
        return steps[0][1] if first else steps[-1][1]
    return reader


# `kind` says which half of the argument a reader tests.
#   "blind"   — factors through the query's observable content, so Theorem 1
#               applies directly and it errs on EXACTLY ONE member of EVERY pair;
#   "id-keyed"— reads the one handle Theorem 1 leaves (the raw entity id, which
#               here is also emission order and parity), so it takes both members
#               of a pair or neither, and lands on `PAIRS` errors only because
#               the coin is BALANCED.
READER_BENCH = (
    ("latest-wins", lambda steps, **_kw: read_latest(steps), "blind"),
    ("first-wins", lambda steps, **_kw: read_first(steps), "blind"),
    ("canonical-min", lambda steps, **_kw: read_canonical_min(steps), "blind"),
    ("canonical-max", lambda steps, **_kw: read_canonical_max(steps), "blind"),
    ("id-parity-first", _id_keyed(True), "id-keyed"),
    ("id-parity-last", _id_keyed(False), "id-keyed"),
)


def declared_reader(q):
    """Answer one battery-b query from the frozen stream, LATEST-WINS.

    This is the reading `core/layers/l4_consolidation.py` implements — an
    `(entity, key)` chain answers `current` with the value at its greatest `t`
    and `asof` with the value in force at the asked `t` — restated engine-free so
    the whole Stage-A arithmetic runs before any Layer-6 engine exists.
    `trials/ops/l6/t_l6batteryb.py` asserts the frozen Layer-5 engine returns
    exactly this on every one of the 2 400 queries.

    Returns `(status, value)` with `status` in `{"answer", "abstain"}`.
    """
    pair = (q["entity"], q["key"])
    horizon = q["t"] if q["op"] == "asof" else None
    steps = _prefix(pair, horizon)
    if not steps:
        return ("abstain", None)
    return ("answer", steps[-1][1])


def region_error_profile(reader):
    """`{pair index: how many of its two members this reader gets wrong}`.

    Theorem 1 says a reader that does not read the raw entity id errs on exactly
    ONE member of every pair, and Theorem 2 says the coin — the only thing the id
    could carry — is not in the stream, so an id-keyed reader takes both or
    neither and the BALANCE puts it on the same total. This is where both are a
    measurement instead of a paragraph.
    """
    by_entity = {}
    for record in queries():
        if record["class"] != "K0":
            continue
        q = record["q"]
        steps = _prefix((q["entity"], q["key"]), None)
        got = reader(steps, entity=q["entity"], key=q["key"])
        by_entity[q["entity"]] = (got != record["value"])
    profile = {}
    for p in region_pairs():
        profile[p["pair"]] = int(by_entity[p["e0"]]) + int(by_entity[p["e1"]])
    return profile


def region_errors(reader):
    """How many forcing queries this reader gets wrong. The tie, as one number."""
    return sum(region_error_profile(reader).values())


# ---- the evidence extractor ------------------------------------------------
#
# The closed feature vocabulary, in the shape Layer 5's six-predicate condition
# grammar is closed: a policy reads these and nothing else, and every one is a
# function of the frozen STREAM alone — never of `ground_truth`, never of a
# query's `value` field.

FEATURES = ("n_assert", "n_distinct", "set_once_tie", "verbatim_repeats",
            "assert_span")

# TWO THINGS ARE DELIBERATELY NOT IN THE VOCABULARY, and the reason is the
# theorem rather than convenience: the RAW ENTITY ID and the ABSOLUTE logical
# time are the only two handles Theorem 1 leaves, and a class-E policy that could
# read them could split a mirror pair. It would gain nothing by doing so — the
# coin is balanced, and `READER_BENCH`'s two id-keyed readers measure exactly the
# same `PAIRS` errors as the blind ones — so excluding them costs a policy no
# reachable score and buys the property that makes the class meaningful: every
# feature here is EQUAL on the two members of a pair, so a class-E policy cannot
# tell them apart, which `t_attainability_b.py` asserts rather than assumes.
#
# Every feature is also read straight off the interval table the Layer-4 engine
# already holds, which is why the price under rule P is one flag per key and
# nothing else (`R5` clause 4, ATTAINABILITY-B.md §3.2).


def evidence(q):
    """The declared structural evidence for one battery-b query.

    A dict over `FEATURES`, every value a non-negative integer, computed from the
    frozen stream and NEVER from the answer key. This is `R5` clause 3's policy
    class made mechanical: a policy that reads only what this returns is in class
    **E** (evidence-only); one that reads the key is in class **O**.

    `t_l6batteryb.py` asserts this function is INVARIANT under the coin
    complement — which is the class-E purity check, and the machine-checked half
    of Theorem 2.
    """
    pair = (q["entity"], q["key"])
    horizon = q["t"] if q["op"] == "asof" else None
    steps = _prefix(pair, horizon)
    values = [_canon(v) for _t, v in steps]
    distinct = len(set(values))
    span = (steps[-1][0] - steps[0][0]) if len(steps) > 1 else 0
    return {
        "n_assert": len(steps),
        "n_distinct": distinct,
        "set_once_tie": 1 if (q["key"] in SET_ONCE_KEYS and distinct > 1) else 0,
        "verbatim_repeats": len(values) - distinct,
        "assert_span": span,
    }


# ---- the policies ----------------------------------------------------------

TIE_CONFIDENCE = permille(Fraction(1, 2))    # 500 — the tie's own arithmetic


def policy_witness(ev, status):
    """W — the exhibited witness. Evidence-only (class E), and NON-RESOLVING.

    It prices the forcing region at the tie's own value and everything else at
    the accuracy the stream supports. It cannot do better on the region and does
    not pretend to: Theorem 1 forbids it, which is exactly why this is a
    confidence model and not a second reader.
    """
    if status != "answer":
        return (status, 0)
    if ev["set_once_tie"]:
        return ("answer", TIE_CONFIDENCE)
    return ("answer", 1000)


CONFLICT_RANK_TAIL_BUCKET = 6


def policy_conflict_rank(ev, status):
    """P_d — evidence-only, KEY-BLIND: confidence falls with the conflict count.

    The round-1 policy, re-measured on battery-b. It can see that an
    `(entity, key)` chain disagrees with itself and cannot see WHICH key admits
    only one value, so it cannot tell a forcing pair from an ordinary chain that
    was legally updated. Its levels are the battery's own measured accuracy at
    each conflict count, derived and asserted rather than typed (`R5` clause 3).
    """
    if status != "answer":
        return (status, 0)
    levels = conflict_rank_measured_levels()
    bucket = min(ev["n_distinct"], CONFLICT_RANK_TAIL_BUCKET)
    return ("answer", levels[bucket])


def conflict_rank_measured_levels():
    """The measured accuracy per conflict count, in permille — `P_d`'s levels."""
    if "conflict_levels" not in _CACHE:
        buckets = {}
        for row in _rows():
            if row["reader_status"] != "answer":
                continue
            d = min(row["evidence"]["n_distinct"], CONFLICT_RANK_TAIL_BUCKET)
            hit, n = buckets.get(d, (0, 0))
            buckets[d] = (hit + (1 if row["reader_correct"] else 0), n + 1)
        _CACHE["conflict_levels"] = {
            d: permille(Fraction(hit, n)) for d, (hit, n) in buckets.items()}
    return _CACHE["conflict_levels"]


def policy_confident_always(ev, status):
    """The capability-free baseline §5.1 L6 itself prescribes for a capped engine."""
    return (status, 1000 if status == "answer" else 0)


def policy_base_rate(ev, status):
    """The capability-free baseline that states the corpus's own accuracy, flat."""
    return (status, base_rate_conf() if status == "answer" else 0)


def policy_detect_and_abstain(ev, status):
    """The §3.0-honest hedger: abstain wherever the evidence flags the tie.

    Round 1's `abstain-on-set-once` under its true name. It is the policy that
    follows `§3.0`'s incentive to its end — turn every error into an abstention,
    and `§3.4`'s denominator loses them — and on round 1's battery it scored
    BETTER than the exhibited witness on three clauses with `AUROC` undefined,
    which is what made the reading of `n/a` load-bearing. On battery-b it is
    KILLED BY ARITHMETIC instead: the region is 200 of 2 200 answerable queries
    and `§5 L6`'s own `F >= 950` is a 50-permille budget spent at 900 per hedge.
    """
    if status == "answer" and ev["set_once_tie"]:
        return ("abstain", 0)
    return (status, 1000 if status == "answer" else 0)


def policy_abstain_on_conflict(ev, status):
    """The KEY-BLIND abstainer: hedge wherever any chain disagrees with itself."""
    if status == "answer" and ev["n_distinct"] > 1:
        return ("abstain", 0)
    return (status, 1000 if status == "answer" else 0)


def policy_oracle(ev, status, correct=None):
    """Class O — reads the answer key. The logical maximum over ALL policies."""
    if status != "answer":
        return (status, 0)
    return ("answer", 1000 if correct else 0)


def base_rate_conf():
    """The flat confidence the base-rate policy states: `permille(1 - w)`.

    DERIVED from the battery, never typed — the point of this baseline is that it
    costs nothing to state because the corpus states it.
    """
    if "base_rate" not in _CACHE:
        rows = _rows()
        answered = [r for r in rows if r["reader_status"] == "answer"]
        correct = sum(1 for r in answered if r["reader_correct"])
        _CACHE["base_rate"] = permille(Fraction(correct, len(answered)))
    return _CACHE["base_rate"]


# ---- scoring a policy over the battery -------------------------------------

def _rows_with(key_values=None):
    """Rows against an answer key. `key_values` is `{qid: value}` or the frozen one.

    Everything except `reader_correct` is a function of the STREAM. Passing a
    different key therefore changes exactly one field, which is what makes
    Theorem 2 a comparison rather than an argument.
    """
    rows = []
    for record in queries():
        status, value = declared_reader(record["q"])
        want = record["value"] if key_values is None \
            else key_values[record["qid"]]
        if record["answerable"]:
            correct = (status == "answer" and value == want)
        else:
            correct = (status == "abstain")
        rows.append({
            "qid": record["qid"],
            "cls": record["class"],
            "answerable": record["answerable"],
            "reader_status": status,
            "reader_correct": correct,
            "evidence": evidence(record["q"]),
        })
    return rows


def _rows():
    if "rows" not in _CACHE:
        _CACHE["rows"] = _rows_with(None)
    return _CACHE["rows"]


def complement_generation():
    """The artifact regenerated with EVERY coin bit flipped.

    Returns `(stream, {qid: value})`. The stream is expected to be identical to
    the frozen one — that expectation IS Theorem 2 and
    `trials/ops/l6/t_l6batteryb.py` is where it is required rather than assumed.
    """
    other = gen.generate_full(gen.SEED, complement=True)
    return other["stream"], {r["qid"]: r["value"] for r in other["queries"]}


def score(policy, use_oracle=False, rows=None):
    """Score one policy over the whole battery. Returns a dict of exact figures.

    `answered` is `§3.4`'s calibration denominator `A`: the queries the policy
    ANSWERS. An abstention contributes to `§3.0`'s fidelity and to nothing else.
    """
    answered = []
    scored_all = []
    scored_core = []
    abstentions = 0
    wrong = 0
    fabricated = 0
    trace = []
    for row in (_rows() if rows is None else rows):
        if use_oracle:
            status, conf = policy(row["evidence"], row["reader_status"],
                                  row["reader_correct"])
        else:
            status, conf = policy(row["evidence"], row["reader_status"])
        trace.append((row["qid"], status, conf))
        if status == "answer":
            correct = row["reader_correct"] if row["answerable"] else False
            if not row["answerable"]:
                fabricated += 1
            answered.append((conf, correct))
            if not correct:
                wrong += 1
            s = 1000 if correct else 0
        else:
            abstentions += 1
            s = 100 if row["answerable"] else 1000
        scored_all.append(s)
        if row["answerable"]:
            scored_core.append(s)

    n_pos = sum(1 for _c, ok in answered if ok)
    n_neg = len(answered) - n_pos
    return {
        "A": len(answered),
        "n_pos": n_pos,
        "n_neg": n_neg,
        "wrong": wrong,
        "fabricated": fabricated,
        "abstentions": abstentions,
        "brier": brier(answered),
        "ece": ece(answered),
        "auroc": auroc(answered),
        "F_all": fidelity(scored_all),
        "F_core": fidelity(scored_core),
        "trace": tuple(trace),
    }


def score_hedging_pairs(k):
    """Score a policy that HEDGES the first `k` mirror pairs and answers the rest.

    Deliberately scored OUTSIDE the policy interface, because a class-E policy
    cannot express this: the evidence of the two members of a pair is identical
    (Theorem 1), so a class-E policy hedges both members or neither and cannot
    choose WHICH pairs. Allowing the choice makes the family strictly larger than
    class E, which makes the bound it produces strictly stronger — even a policy
    that may pick its pairs cannot reach `n_neg = 0` without spending 900 per
    hedge out of `§5 L6`'s own 50-permille fidelity budget.

    Returns `(n_neg, F_core)` exactly.
    """
    hedged = {p["e0"] for p in region_pairs()[:k]} \
        | {p["e1"] for p in region_pairs()[:k]}
    scored_core = []
    n_neg = 0
    for row, record in zip(_rows(), queries()):
        if row["cls"] == "K0" and record["q"]["entity"] in hedged:
            if row["answerable"]:
                scored_core.append(100)
            continue
        if row["reader_status"] != "answer":
            if row["answerable"]:
                scored_core.append(100)
            else:
                pass
            continue
        if row["answerable"]:
            scored_core.append(1000 if row["reader_correct"] else 0)
        if not row["reader_correct"] and row["answerable"]:
            n_neg += 1
    return n_neg, fidelity(scored_core)


def as_permille(figures):
    """The same dict with each measure rounded to an integer permille, `None` kept."""
    out = {}
    for key, value in figures.items():
        if isinstance(value, Fraction):
            out[key] = permille(value)
        else:
            out[key] = value
    return out


POLICIES = (
    ("oracle", policy_oracle, "O"),
    ("witness", policy_witness, "E"),
    ("conflict-rank", policy_conflict_rank, "E"),
    ("confident-always", policy_confident_always, "E"),
    ("base-rate-constant", policy_base_rate, "E"),
    ("detect-and-abstain", policy_detect_and_abstain, "E"),
    ("abstain-on-conflict", policy_abstain_on_conflict, "E"),
)


def scoreboard():
    """Every named policy scored over battery-b, exact."""
    out = {}
    for name, policy, _cls in POLICIES:
        out[name] = score(policy, use_oracle=(name == "oracle"))
    return out


# ---- the band, as arithmetic rather than as a recorded number --------------

def band_bounds(r):
    """The feasible window for the answerable core `A`, given a region of size `r`.

    Three ratified clauses, pulling against each other, with `w = (r/2)/A` the
    wrong share of any committing reader (Theorem 1) and `a` the abstained share:

      * `F >= 950` for the honest committer   `1000w <= 50`      ->  `A >= 10r`
      * blanket abstention on the region BREAKS `F >= 950`
                                              `900(r/A) > 50`    ->  `A < 18r`
      * `Brier <= 40` beats the base-rate constant
                                              `w(1-w) > 40/1000` ->  `A < (25+5*sqrt(21))/4 * r`

    The third bound is irrational, so it is returned as the exact rational
    predicate `25u^2 - 50u + 4 < 0` in `u = r/A` rather than as a float.
    """
    return {
        "committer_F": Fraction(10) * r,                 # A >= this
        "abstention_kills_F": Fraction(18) * r,          # A <  this
        "brier_beats_base_rate": lambda A: (
            Fraction(25) * Fraction(r, A) ** 2
            - Fraction(50) * Fraction(r, A) + 4 < 0),    # A <  ~11.978r
    }

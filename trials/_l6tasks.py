"""trials/_l6tasks.py — the shared Layer-6 calibration battery (engine-free).

Nothing here touches an engine, so it is importable before
`core/layers/l6_meta_memory.py` exists — the trials-first step of the ASCEND
sequence (**BOUNDARY-RULINGS.md R2**). It carries four things the Layer-6
arithmetic rests on, in one place so they can never disagree:

1. **the declared reader** — how a query of the frozen battery is answered from
   the frozen murk stream, latest-wins, which is what every layer this project
   has frozen implements;
2. **the evidence extractor** — the closed, declared feature vocabulary a
   confidence policy may read, computed from the event stream **alone** and
   never from an answer key;
3. **the policies** — the exhibited witness and every named capability-free
   baseline, each a pure map from evidence to an integer permille;
4. **the measures** — Brier, ECE and AUROC in exact `Fraction` at §3.4's own
   bin structure, plus the §3.0 abstention-aware fidelity.

`trials/ascension/l6/ATTAINABILITY.md` is the prose of what this module
computes; `trials/ascension/l6/t_attainability.py` asserts that the two agree.

## The reading this module declares (and does not rule on)

`§3.4` defines Brier, ECE and AUROC *in `[0,1]`*; `§5 L6` states the gates as the
integers `40`, `30`, `900`; `§3.5`'s `permille` maps `[0,1]` to `[0,1000]` by
round-half-to-even. The two readings disagree on a real interval — `Brier ≤
40/1000` versus `permille(Brier) ≤ 40` differ on `(40/1000, 81/2000]`
(`PRE-READ.md §2`). This module computes **both** and this project's arithmetic
takes the **exact** one, because `§5.1 L6`'s own defense sentences state bounds
on the quantity and not on its rounding (*"at or under 0.04"*, *"to within 3%"*).
Nothing here rules; `RULING-R7-DRAFT.md` asks a human to.

## AUROC's precondition is load-bearing, not decorative

`§3.4`: *"[AUROC] is **undefined** when `n_pos = 0` or `n_neg = 0` (report
`n/a`; any gate that cites AUROC requires both classes present)."* `auroc()`
returns `None` there and every caller must handle it. That is the whole reason
this battery exists: on murk as previously queried this engine's `n_neg` is 0
and the clause carrying R2 obligation 2 evaporates.
"""

import json
import os
from fractions import Fraction

from corpora.l6battery import generator as battery_gen
from corpora.murk import generator as murk_gen

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SET_ONCE_KEYS = battery_gen.SET_ONCE_KEYS


def permille(x):
    """Exact Fraction in [0,1] -> integer permille, round-half-to-even (§3.5)."""
    n = x * 1000
    q = n.numerator // n.denominator
    r = n - q
    if r < Fraction(1, 2):
        return q
    if r > Fraction(1, 2):
        return q + 1
    return q if q % 2 == 0 else q + 1


# ---- the substrate ---------------------------------------------------------

_CACHE = {}


def murk_payloads():
    if "payloads" not in _CACHE:
        with open(murk_gen.FROZEN_PATH, "r", encoding="utf-8") as fh:
            _CACHE["payloads"] = [json.loads(line) for line in fh if line.strip()]
    return _CACHE["payloads"]


def murk_ground_truth():
    if "gt" not in _CACHE:
        with open(murk_gen.GROUND_TRUTH_PATH, "r", encoding="utf-8") as fh:
            _CACHE["gt"] = json.load(fh)
    return _CACHE["gt"]


def battery():
    if "battery" not in _CACHE:
        _CACHE["battery"] = battery_gen.load()
    return _CACHE["battery"]


def chains():
    if "chains" not in _CACHE:
        built, _order = battery_gen.chains_of(murk_payloads())
        _CACHE["chains"] = built
    return _CACHE["chains"]


# ---- the declared reader ---------------------------------------------------

def _prefix(pair, horizon):
    chain = chains().get(pair)
    if chain is None:
        return []
    if horizon is None:
        return chain
    return [step for step in chain if step[0] <= horizon]


def declared_reader(q):
    """Answer one battery query from the frozen stream, LATEST-WINS.

    This is the reading `core/layers/l4_consolidation.py` implements — an
    `(entity, key)` chain answers `current` with the value at its greatest `t`
    and `asof` with the value in force at the asked `t` — restated engine-free so
    the whole Stage-A arithmetic runs before any Layer-6 engine exists.
    `trials/ops/l6/t_l6battery.py` asserts that the frozen Layer-5 engine returns
    exactly this on every one of the 3 905 queries: one reading, two
    implementations, checked rather than assumed.

    Returns `(status, value)` with `status` in `{"answer", "abstain"}`.
    """
    pair = (q["entity"], q["key"])
    horizon = q["t"] if q["op"] == "asof" else None
    steps = _prefix(pair, horizon)
    if not steps:
        return ("abstain", None)
    return ("answer", steps[-1][1])


# ---- the evidence extractor ------------------------------------------------
#
# The closed feature vocabulary, in the shape Layer 5's six-predicate condition
# grammar is closed: a policy reads these and nothing else, and every one is a
# function of the murk event stream alone.

FEATURES = ("n_assert", "n_distinct", "set_once_conflict", "verbatim_repeats",
            "reused_entity", "unreadable_touching")


def _entity_index():
    if "entity_index" not in _CACHE:
        reused = {}
        unreadable = {}
        live_seen = set()
        retired = set()
        for t, payload in enumerate(murk_payloads()):
            entity = payload.get("entity")
            if not isinstance(entity, int) or isinstance(entity, bool):
                entity = payload.get("src")
            if battery_gen.facet(payload) is None and isinstance(entity, int) \
                    and not isinstance(entity, bool):
                unreadable.setdefault(entity, []).append(t)
            kind = payload.get("kind")
            who = payload.get("entity")
            if not isinstance(who, int) or isinstance(who, bool):
                continue
            if kind == "retire":
                retired.add(who)
            elif kind == "spawn":
                if who in retired or who in live_seen:
                    reused.setdefault(who, []).append(t)
                retired.discard(who)
                live_seen.add(who)
        _CACHE["entity_index"] = (reused, unreadable)
    return _CACHE["entity_index"]


def _canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def evidence(q):
    """The declared structural evidence for one battery query.

    A dict over `FEATURES`, every value a non-negative integer, computed from the
    frozen murk stream and NEVER from `ground_truth.json`. This is the policy
    class declaration R5 clause 3 requires, made mechanical: a policy that reads
    only what this function returns is in class **E** (evidence-only); a policy
    that reads the answer key is in class **O** (oracle).
    """
    pair = (q["entity"], q["key"])
    horizon = q["t"] if q["op"] == "asof" else None
    steps = _prefix(pair, horizon)
    values = [_canon(v) for _t, v in steps]
    distinct = len(set(values))
    repeats = len(values) - distinct
    reused, unreadable = _entity_index()
    marks = [t for t in reused.get(q["entity"], [])
             if horizon is None or t <= horizon]
    dirty = [t for t in unreadable.get(q["entity"], [])
             if horizon is None or t <= horizon]
    return {
        "n_assert": len(steps),
        "n_distinct": distinct,
        "set_once_conflict": 1 if (q["key"] in SET_ONCE_KEYS and distinct > 1)
                             else 0,
        "verbatim_repeats": repeats,
        "reused_entity": len(marks),
        "unreadable_touching": len(dirty),
    }


# ---- the policies ----------------------------------------------------------
#
# Each is `(evidence, status) -> (status, conf)`: a policy may lower confidence
# and it may ABSTAIN, but it never changes the declared reader's value. §5 L6
# asks for "confidence permille from structural evidence", not for a second
# reader — and a policy that answered differently would be a different ENGINE,
# which is Stage C's business and not Stage A's.


def policy_witness(ev, status):
    """W — the exhibited witness. Evidence-only (class E), graded, set-once-aware."""
    if status != "answer":
        return (status, 0)
    if ev["set_once_conflict"]:
        return ("answer", 20)
    if ev["n_distinct"] == 1:
        return ("answer", 1000)
    if ev["n_distinct"] <= 3:
        return ("answer", 960)
    return ("answer", 900)


CONFLICT_RANK_LEVELS = {1: 1000, 2: 828, 3: 702, 4: 500, 5: 400}
CONFLICT_RANK_TAIL = 111


def policy_conflict_rank(ev, status):
    """P_d — evidence-only, KEY-BLIND: confidence falls with the conflict count.

    The policy that **RANKS without RESOLVING**. It can see that an
    `(entity, key)` chain disagrees with itself, and it cannot see which of the
    disagreeing values is true — it does not know that `origin` is set-once and
    would not know what to do with the fact. It is the honest measure of what
    ranking alone buys.

    **Its levels are fit to this battery** and the fit is declared rather than
    hidden (`R5` clause 3): each is the battery's own measured accuracy at that
    conflict count, in permille, so `P_d` is the best a key-blind policy can do
    HERE and its scores are a ceiling for that sub-family rather than a guess.
    `t_attainability.py` re-derives every level from the battery and requires it,
    so a level somebody tuned by hand would be red.
    """
    if status != "answer":
        return (status, 0)
    return ("answer", CONFLICT_RANK_LEVELS.get(ev["n_distinct"],
                                               CONFLICT_RANK_TAIL))


def conflict_rank_measured_levels():
    """The measured accuracy per conflict count, in permille — `P_d`'s own levels."""
    if "conflict_levels" not in _CACHE:
        buckets = {}
        for row in _rows():
            if row["reader_status"] != "answer":
                continue
            d = min(row["evidence"]["n_distinct"], 6)
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


def policy_abstain_on_conflict(ev, status):
    """The §3.0-honest abstainer, KEY-BLIND: hedge wherever the chain disagrees."""
    if status == "answer" and ev["n_distinct"] > 1:
        return ("abstain", 0)
    return (status, 1000 if status == "answer" else 0)


def policy_abstain_on_set_once(ev, status):
    """The §3.0-honest abstainer with the set-once reading: hedge only where it bites."""
    if status == "answer" and ev["set_once_conflict"]:
        return ("abstain", 0)
    return (status, 1000 if status == "answer" else 0)


def policy_oracle(ev, status, correct=None):
    """Class O — reads the answer key. The logical maximum over ALL policies."""
    if status != "answer":
        return (status, 0)
    return ("answer", 1000 if correct else 0)


def base_rate_conf():
    """The flat confidence the base-rate policy states: `permille(1 − w)`.

    DERIVED from the battery, never typed — the point of this baseline is that it
    costs nothing to state because the corpus states it, and a constant somebody
    had to type would be a constant somebody could tune. `§7.2` admits only an
    integer permille, which is the one exactness caveat `PRE-READ.md §3.2`
    recorded: where the accuracy is not expressible in permille the policy rounds
    and its ECE is bounded by `1/2000` rather than being exactly 0.
    """
    if "base_rate" not in _CACHE:
        rows = _rows()
        answered = [r for r in rows if r["reader_status"] == "answer"]
        correct = sum(1 for r in answered if r["reader_correct"])
        _CACHE["base_rate"] = permille(Fraction(correct, len(answered)))
    return _CACHE["base_rate"]


# ---- the measures (§3.4, all exact) ----------------------------------------

def brier(answered):
    """`(1/A) Σ (conf/1000 − correct)²` — exact Fraction in [0,1]."""
    if not answered:
        return None
    total = Fraction(0)
    for conf, correct in answered:
        gap = Fraction(conf, 1000) - (1 if correct else 0)
        total += gap * gap
    return total / len(answered)


def ece(answered):
    """`Σ_b (n_b/A)·|mean_conf_b − acc_b|` over §3.4's ten fixed permille bins.

    Bin assignment on an integer permille is exactly `conf // 100`, with the
    single special case `conf = 1000 -> bin 9` because §3.4's last bin
    `[900,1000]` is CLOSED. Both a total order and a partition: no boundary is
    ambiguous and no value falls outside.
    """
    if not answered:
        return None
    bins = {}
    for conf, correct in answered:
        b = 9 if conf == 1000 else conf // 100
        acc, tot, n = bins.get(b, (0, 0, 0))
        bins[b] = (acc + (1 if correct else 0), tot + conf, n + 1)
    total = Fraction(0)
    for b in sorted(bins):
        acc, tot, n = bins[b]
        mean_conf = Fraction(tot, 1000 * n)
        accuracy = Fraction(acc, n)
        total += Fraction(n, len(answered)) * abs(mean_conf - accuracy)
    return total


def auroc(answered):
    """`U / (n_pos · n_neg)`, ties counting ½ — or **None** when either class is empty.

    §3.4 states the precondition in its own words: *"undefined when n_pos = 0 or
    n_neg = 0 (report n/a; any gate that cites AUROC requires both classes
    present)"*. Returning None rather than a number is what makes that clause
    visible to every caller instead of silently favourable to a perfect engine.
    """
    pos = [c for c, ok in answered if ok]
    neg = [c for c, ok in answered if not ok]
    if not pos or not neg:
        return None
    u = Fraction(0)
    neg_sorted = sorted(neg)
    import bisect
    for c in pos:
        lo = bisect.bisect_left(neg_sorted, c)
        hi = bisect.bisect_right(neg_sorted, c)
        u += lo + Fraction(hi - lo, 2)
    return u / (len(pos) * len(neg))


def fidelity(scored):
    """§3.1 over the §3.0 table. `scored` is a list of per-query scores."""
    if not scored:
        return None
    return Fraction(sum(scored), len(scored) * 1000)


# ---- scoring a policy over the battery -------------------------------------

def _rows():
    if "rows" not in _CACHE:
        rows = []
        for record in battery()["queries"]:
            status, value = declared_reader(record["q"])
            if record["answerable"]:
                correct = (status == "answer" and value == record["value"])
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
        _CACHE["rows"] = rows
    return _CACHE["rows"]


def score(policy, use_oracle=False):
    """Score one policy over the whole battery. Returns a dict of exact figures.

    `answered` is the calibration denominator `A` of §3.4: the queries the
    policy ANSWERS. An abstention contributes to §3.0's fidelity and to nothing
    else — which is the abstention-blindness `PRE-READ.md §3` named, made
    mechanical here so no caller can forget it.
    """
    answered = []
    scored_all = []
    scored_core = []
    abstentions = 0
    wrong = 0
    fabricated = 0
    for row in _rows():
        if use_oracle:
            status, conf = policy(row["evidence"], row["reader_status"],
                                  row["reader_correct"])
        else:
            status, conf = policy(row["evidence"], row["reader_status"])
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
    }


def as_permille(figures):
    """The same dict with each measure rounded to an integer permille, `None` kept."""
    out = {}
    for key, value in figures.items():
        if isinstance(value, Fraction):
            out[key] = permille(value)
        else:
            out[key] = value
    return out


# ---- the named policies, in the order ATTAINABILITY.md scores them ---------

POLICIES = (
    ("oracle", policy_oracle, "O"),
    ("witness", policy_witness, "E"),
    ("conflict-rank", policy_conflict_rank, "E"),
    ("confident-always", policy_confident_always, "E"),
    ("base-rate-constant", policy_base_rate, "E"),
    ("abstain-on-set-once", policy_abstain_on_set_once, "E"),
    ("abstain-on-conflict", policy_abstain_on_conflict, "E"),
)


def scoreboard():
    """Every named policy scored over the battery, exact."""
    out = {}
    for name, policy, _cls in POLICIES:
        out[name] = score(policy, use_oracle=(name == "oracle"))
    return out


# ---- the separability finding ----------------------------------------------

def defect_separability():
    """Can a stream-only rule recover each murk defect family exactly?

    §8.7 pairs every injected defect with its answer key and injects it by
    VISIBLE construction, and this measures the consequence: for each family, the
    number of events the declared stream-only rule misclassifies. A family that
    separates at 0 is a family whose structural evidence RESOLVES and does not
    merely RANK — which is `ATTAINABILITY.md §6`'s finding and the reason this
    battery cannot guarantee `n_neg > 0` against an arbitrary reader.
    """
    payloads = murk_payloads()
    gt = murk_ground_truth()
    marked = {}
    for defect in gt["defects"]:
        marked.setdefault(defect["type"], set()).add(defect["t"])

    out = {}

    # contradiction: a set-once key asserted with two different values.
    predicted = set()
    seen = {}
    for t, payload in enumerate(payloads):
        f = battery_gen.facet(payload)
        if f is None or f[1] not in SET_ONCE_KEYS:
            continue
        first = seen.get((f[0], f[1]))
        if first is None:
            seen[(f[0], f[1])] = _canon(f[2])
        elif first != _canon(f[2]):
            predicted.add(t)
    out["contradiction"] = (len(predicted ^ marked["contradiction"]),
                            len(marked["contradiction"]))

    # near_duplicate: an attr/link repeated verbatim within the declared window.
    window = 100
    predicted = set()
    last = {}
    for t, payload in enumerate(payloads):
        if payload.get("kind") not in ("attr", "link"):
            continue
        key = _canon(payload)
        if key in last and t - last[key] <= window:
            predicted.add(t)
        last[key] = t
    out["near_duplicate"] = (len(predicted ^ marked["near_duplicate"]),
                             len(marked["near_duplicate"]))

    # ambiguity: a spawn of an entity id that was already retired.
    predicted = set()
    retired = set()
    for t, payload in enumerate(payloads):
        kind, who = payload.get("kind"), payload.get("entity")
        if not isinstance(who, int) or isinstance(who, bool):
            continue
        if kind == "retire":
            retired.add(who)
        elif kind == "spawn" and who in retired:
            predicted.add(t)
            retired.discard(who)
    out["ambiguity"] = (len(predicted ^ marked["ambiguity"]),
                        len(marked["ambiguity"]))

    # malformed: a payload the declared grammar reading rejects.
    predicted = set()
    for t, payload in enumerate(payloads):
        kind = payload.get("kind")
        if kind not in ("attr", "link", "spawn", "move", "retire"):
            predicted.add(t)
        elif battery_gen.facet(payload) is None:
            predicted.add(t)
        elif kind == "link" and payload.get("dst") not in _known_entities(payloads, t):
            predicted.add(t)
    out["malformed"] = (len(predicted ^ marked["malformed"]),
                        len(marked["malformed"]))
    return out


def _known_entities(payloads, horizon):
    if "known" not in _CACHE:
        known = []
        live = set()
        for payload in payloads:
            who = payload.get("entity")
            if payload.get("kind") == "spawn" and isinstance(who, int) \
                    and not isinstance(who, bool):
                live.add(who)
            known.append(frozenset(live))
        _CACHE["known"] = known
    return _CACHE["known"][horizon]

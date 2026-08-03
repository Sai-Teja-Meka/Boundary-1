"""trials/_l7tasks.py — the Layer-7 generation battery (engine-free).

Layer-7 Stage A. Nothing here touches an engine, so it is importable before
`core/layers/l7_generation.py` exists — the trials-first step of the `ASCEND`
sequence (**BOUNDARY-RULINGS.md R2**).

It carries seven things, in one place so they can never disagree:

1. **the composition reading** — `COMPOSITION_FORM` made mechanical: a
   compound's material, its composed `profile` item, and the support the rule
   actually reads;
2. **the labeller bench** — six lineage labellers that decide from the QUERY
   alone (or from the two handles the query leaves, the raw entity id and the
   emission order), each scored on the forcing region, because Theorem 1 is a
   claim that must be *exhibited against labellers built to break it* rather
   than asserted about a family;
3. **the policies** — the exhibited witness, every named capability-free
   baseline, and the two deliberate crimes (`always-observed`, the untagged
   generator; `always-generated`, the over-tagger), each a pure map from a store
   to an `Answer`;
4. **the measures** — `§5 L7`'s three capability ratios with their denominators
   stated, `§3.1` fidelity, `§3.4`'s calibration triple, and the humility
   conjunction `§5` states only on the capped side;
5. **the promotion ladder** — the three-generation re-ingestion, scored at each
   rung for the witness and for a ledger-blind reference policy that is a trial
   fixture and never engine code;
6. **the band** — `g > 1/18` and the hedging ladder, as arithmetic rather than
   as a recorded number;
7. **the substrate survey** — the measurement behind the fifth substrate kill:
   what the `generated` tag costs on every artifact this project has frozen.

`trials/ascension/l7/ATTAINABILITY.md` is the prose of what this module
computes; `trials/ascension/l7/t_attainability.py` asserts that the two agree.

## The one thing this module deliberately does not have

There is no `generate` verb here and no engine. A **policy** is a function from
(store, query) to an Answer, and the store is a list of payloads — the frozen
stream, or the frozen stream with a generation appended. That is what makes
every figure below a fact about the artifact rather than a measurement of an
implementation (`R2`'s rationale: *"an oracle ceiling computed after an engine
exists is no longer a neutral fact about a corpus"*).
"""

import json
import os
from fractions import Fraction

from corpora.l7compose import generator as gen

# ONE INSTRUMENT. `§3.4`'s quantities and `§3.1`'s fidelity are `_l6tasks`' own,
# unchanged, so a Layer-6 Brier and a Layer-7 Brier are the same function of the
# same shape of input and the two layers' numbers are comparable without a
# caveat about the ruler.
from _l6tasks import permille, brier, ece, auroc, fidelity  # noqa: F401

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAIRS = gen.PAIRS
LADDER = gen.LADDER
HUES = gen.HUES
GRADES = gen.GRADES
HUE_KEY = gen.HUE_KEY
MASS_KEY = gen.MASS_KEY
COMPOUND_CLASS = gen.COMPOUND_CLASS

# `§5 L7`'s own gate, quoted here and registered in `laws/t_rulings.py`. Until
# 2026-08-03 these eight carried a `§5 L7` clause and NO COMPANION RULING, which
# is what "no Layer-7 gate binds on anything" looked like in that registry;
# `BOUNDARY-RULINGS.md R8` clause 1 binds both sides of the gate to
# `corpora/l7compose`, so every one of them now carries `R8` beside its clause.
# `R8` clause 3 supplies the three denominators `§5` states none of, and its
# clause 3(c) is why a `None` here is a FAILURE and not an excuse.
GATE_VALIDITY = 1000
GATE_NOVELTY = 1000
GATE_TAGGING = 1000
GATE_PROMOTION = 0
GATE_F = 950
GATE_B = 1000
GATE_ECE = 40
CEILING_CONJUNCTION = 50

_CACHE = {}


# ---- the frozen artifact ---------------------------------------------------

def artifact():
    if "artifact" not in _CACHE:
        _CACHE["artifact"] = gen.load()
    return _CACHE["artifact"]


def stream():
    """The substrate — everything a class-E policy is allowed to read."""
    return artifact()["stream"]


def declared():
    """The artifact's own class table. Class **O** only: a policy may not read it."""
    return artifact()["declared"]


def queries():
    return artifact()["queries"]


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def lineage_table():
    """`entity -> declared lineage depth`. 0 = stored, k = generated at rung k."""
    if "lineage" not in _CACHE:
        _CACHE["lineage"] = {int(k): v for k, v in declared()["lineage"].items()}
    return _CACHE["lineage"]


def declared_profiles():
    if "profiles" not in _CACHE:
        _CACHE["profiles"] = {int(k): v
                              for k, v in declared()["profiles"].items()}
    return _CACHE["profiles"]


def generation_class():
    """The declared **G** class: the qids whose answer no retrieval can produce."""
    return tuple(r["qid"] for r in queries() if r["declared"] == "G")


def observed_class():
    return tuple(r["qid"] for r in queries() if r["declared"] == "O")


def unanswerable_class():
    return tuple(r["qid"] for r in queries() if r["declared"] == "U")


# ---- the composition reading, mechanical -----------------------------------
#
# `COMPOSITION_FORM` is a DECLARED READING of the frozen grammar, in the shape
# `ASSERTION_FORMS` (L4), `INTENTION_FORM` (L5) and `SET_ONCE_KEYS` (L6) already
# have. It is not learned and it is not inferred: a session declares it, and
# `trials/ops/l7/t_l7compose.py` checks the declaration against the frozen bytes.

class Reading:
    """The declared readings over an ingested payload list.

    A `Reading` is what a policy is allowed to see: assertions, `part` edges,
    and whichever `profile` payloads the store actually carries. It is rebuilt
    from scratch for each store in the promotion ladder, so nothing survives a
    re-ingestion except what the store itself now says.
    """

    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.chains = {}            # (entity, key) -> [(t, value), ...]
        self.parts = {}             # entity -> {slot: (t, of)}
        self.profile_at = {}        # entity -> (t, item) for a STORED profile
        self.canon_bytes = set()
        for t, payload in enumerate(self.payloads):
            self.canon_bytes.add(canon(payload))
            f = gen.facet(payload)
            if f is not None:
                self.chains.setdefault((f[0], f[1]), []).append((t, f[2]))
            kind = payload.get("kind")
            if kind == "part":
                self.parts.setdefault(payload["entity"], {})[payload["slot"]] \
                    = (t, payload["of"])
            elif kind == "profile":
                self.profile_at[payload["entity"]] = (t, payload)

    def latest(self, entity, key):
        steps = self.chains.get((entity, key))
        return steps[-1] if steps else None

    def is_compound(self, entity):
        slots = self.parts.get(entity)
        return slots is not None and 0 in slots and 1 in slots

    def material(self, entity, seen=None):
        """`(hue, mass, support)` for one entity, or `None` when undetermined.

        A plain component's material is its latest `hue` and `mass`. A
        compound's is its own `profile` item's — stored if the store carries
        one, composed otherwise — which is what makes the rule closed under
        composition and gives the ladder its rungs.
        """
        seen = set() if seen is None else seen
        if entity in seen:
            return None                     # a cycle is not a reading
        if self.is_compound(entity):
            built = self.profile(entity, seen | {entity})
            if built is None:
                return None
            item, support = built
            return (item["hue"], item["mass"], support)
        hue = self.latest(entity, HUE_KEY)
        mass = self.latest(entity, MASS_KEY)
        if hue is None or mass is None:
            return None
        return (hue[1], mass[1], (hue[0], mass[0]))

    def profile(self, entity, seen=None):
        """`(item, support)` — the stored profile if there is one, else composed.

        `support` is the ascending tuple of every `t` the rule actually read,
        which is what makes `§4.2`'s `support` a **relevance** claim on this
        artifact and not merely a schema-valid list (`R8`
        clause 5(b)).
        """
        stored = self.profile_at.get(entity)
        if stored is not None:
            return (stored[1], (stored[0],))
        if not self.is_compound(entity):
            return None
        seen = set() if seen is None else seen
        slots = self.parts[entity]
        support = [slots[0][0], slots[1][0]]
        mat = []
        for slot in (0, 1):
            m = self.material(slots[slot][1], seen)
            if m is None:
                return None
            mat.append(m)
            support.extend(m[2])
        item = gen.compose(mat[0][0], mat[0][1], mat[1][0], mat[1][1], entity)
        return (item, tuple(sorted(set(support))))

    def composed_only(self, entity, seen=None):
        """The composed item, IGNORING any stored profile for `entity` itself.

        This is what a generator computes when it has decided the stored copy is
        its own re-ingested output: the rule, applied to the material.
        """
        if not self.is_compound(entity):
            return None
        seen = set() if seen is None else seen
        slots = self.parts[entity]
        support = [slots[0][0], slots[1][0]]
        mat = []
        for slot in (0, 1):
            m = self.material(slots[slot][1], seen | {entity})
            if m is None:
                return None
            mat.append(m)
            support.extend(m[2])
        item = gen.compose(mat[0][0], mat[0][1], mat[1][0], mat[1][1], entity)
        return (item, tuple(sorted(set(support))))

    def current(self, entity, key):
        step = self.latest(entity, key)
        if step is None:
            return None
        return step

    def recoverable(self, t):
        """Can this store still PRODUCE the event at `t`?

        THE SEAM `R8` clause 5(a) is about, named here rather
        than left implicit. `§4.2.3` asks only whether a `t` was ever ASSIGNED;
        the support-recoverability diagnostic asks whether `read(t)` still
        ANSWERS. A `Reading` is backed by a payload list with no eviction, so at
        Stage A the two coincide and the diagnostic reads 1000 — which is stated
        in `ATTAINABILITY.md §9.1` rather than hidden. The predicate lives in one
        place so that an engine-backed reading under pressure can differ here and
        nowhere else.
        """
        return 0 <= t < len(self.payloads)


def base_reading():
    if "reading" not in _CACHE:
        _CACHE["reading"] = Reading(stream())
    return _CACHE["reading"]


def recomputed_lineage(reading=None):
    """`entity -> depth`, recomputed from the STREAM alone.

    A compound whose profile is in the store is depth 0; otherwise its depth is
    one more than the greatest depth among its compound components. This is what
    *"lineage decidable from frozen bytes"* means, and `t_l7compose.py` requires
    it to equal the artifact's declared table.
    """
    reading = base_reading() if reading is None else reading
    depths = {}

    def depth(entity, seen):
        if entity in depths:
            return depths[entity]
        if entity in seen:
            return None
        if not reading.is_compound(entity):
            return 0
        if entity in reading.profile_at:
            depths[entity] = 0
            return 0
        best = 0
        for slot in (0, 1):
            child = reading.parts[entity][slot][1]
            d = depth(child, seen | {entity})
            if d is None:
                return None
            best = max(best, d)
        depths[entity] = best + 1
        return depths[entity]

    for entity in sorted(reading.parts):
        depth(entity, set())
    # A compound whose material the rule does not determine has no profile and
    # therefore no lineage: it is the U class, where abstention is the only
    # correct behaviour. Dropping it here is what makes this table exactly the
    # artifact's declared one rather than a superset of it.
    return {e: d for e, d in depths.items()
            if reading.profile(e) is not None}


# ---- the Answer ------------------------------------------------------------
#
# `§7.2`'s shape plus the ONE field Layer 7 adds, and the field is a property of
# the ITEM rather than of the answer's channel: `§4.2.3`'s four `kind`s say how
# an answer reached the caller, and `lineage` says what the item is. The two are
# orthogonal, which is why `§5 L7`'s `generated` tag does not violate `§4.2.3`'s
# *"and no other"* (`R8` clause 4).

OBSERVED = "observed"
GENERATED = "generated"
CERTAIN = 1000


def _abstain():
    return {"status": "abstain", "value": None, "lineage": None,
            "confidence": 0, "provenance": None}


def _answer(value, lineage, kind, support, t_asof, confidence=CERTAIN):
    return {"status": "answer", "value": value, "lineage": lineage,
            "confidence": confidence,
            "provenance": {"support": list(support), "kind": kind,
                           "t_asof": t_asof}}


# ---- the policies ----------------------------------------------------------

class Policy:
    """A pure map from a store to Answers, plus the lineage record it keeps.

    `cls` is `R5` clause 3's policy class: **E** reads the stream only, **O**
    may read the artifact's declared class table or its answer key.
    """

    cls = "E"
    name = "policy"

    def __init__(self):
        self.generated_entities = {}      # entity -> rung, the lineage ledger
        self.generated_ts = set()

    # -- the lineage ledger, priced in ATTAINABILITY.md §5 -------------------

    def record_generation(self, entity, rung=1):
        self.generated_entities[entity] = rung

    def ingest_marks(self, reading):
        """Mark every `t` in `reading` that carries an item this policy generated.

        This is the lawful placement `PRE-READ.md §5.2` names — *in engine state,
        keyed by `t`* — and it is why re-ingestion cannot launder a generation:
        the store says the profile is there, and the ledger says whose it is.
        """
        self.generated_ts = set()
        for entity, (t, _item) in reading.profile_at.items():
            if entity in self.generated_entities:
                self.generated_ts.add(t)

    def stored_is_observed(self, reading, entity):
        stored = reading.profile_at.get(entity)
        if stored is None:
            return False
        return stored[0] not in self.generated_ts

    # -- the answer path ----------------------------------------------------

    def answer(self, reading, record):
        raise NotImplementedError


class RetrievalOnly(Policy):
    """The capability-free baseline: answer what is stored, abstain otherwise.

    It has no composition construct at all, which is why its `validity`,
    `novelty` and `tagging` denominators are **empty** — the fourth species
    `PRE-READ.md §1.5` names, met head-on by `R8` clause 3.
    """

    name = "retrieval-only"

    def answer(self, reading, record):
        q = record["q"]
        if q["op"] == "current":
            step = reading.current(q["entity"], q["key"])
            if step is None:
                return _abstain()
            return _answer(step[1], OBSERVED, "recall", (step[0],), step[0])
        entity = q["cue"]["entity"]
        stored = reading.profile_at.get(entity)
        if stored is None:
            return _abstain()
        return _answer(stored[1], OBSERVED, "recall", (stored[0],), stored[0])


class Witness(Policy):
    """**W** — the exhibited witness. Class E, and provably STORE-CONSULTING.

    On a `generate` cue it asks its own store whether it holds the item. Where it
    does — and the copy is not one of its own re-ingested generations — the item
    is `observed` and the answer is a `recall`. Where it does not, it applies the
    declared composition rule, tags the item `generated`, cites exactly the `t`s
    the rule read, and records the generation in its ledger.

    It cannot decide the lineage from the query, and `t_attainability.py` asserts
    the cause rather than the consequence: the two members of a mirror pair carry
    the SAME composed value, so nothing in the answer distinguishes them and only
    the store does.
    """

    name = "witness"

    def answer(self, reading, record):
        q = record["q"]
        if q["op"] == "current":
            step = reading.current(q["entity"], q["key"])
            if step is None:
                return _abstain()
            return _answer(step[1], OBSERVED, "recall", (step[0],), step[0])
        entity = q["cue"]["entity"]
        if self.stored_is_observed(reading, entity):
            t, item = reading.profile_at[entity]
            return _answer(item, OBSERVED, "recall", (t,), t)
        built = reading.composed_only(entity)
        if built is None:
            return _abstain()
        item, support = built
        self.record_generation(entity)
        return _answer(item, GENERATED, "derive", support, max(support))


class AlwaysGenerated(Policy):
    """The OVER-TAGGER: compose everything, call everything `generated`.

    It never commits the capital crime and dies on `novelty` instead, because the
    items it tags on the observed half of every mirror pair **are stored**. This
    is the second off-diagonal of the confusion matrix, and it is why the
    instrument is a matrix and not a rate (`PRE-READ.md §3.1` item 3).
    """

    name = "always-generated"

    def answer(self, reading, record):
        q = record["q"]
        if q["op"] == "current":
            step = reading.current(q["entity"], q["key"])
            if step is None:
                return _abstain()
            return _answer(step[1], OBSERVED, "recall", (step[0],), step[0])
        entity = q["cue"]["entity"]
        built = reading.profile(entity)
        if built is None:
            return _abstain()
        item, support = built
        self.record_generation(entity)
        return _answer(item, GENERATED, "derive", support, max(support))


class AlwaysObserved(Policy):
    """THE CAPITAL CRIME, committed on purpose: compose, and tag nothing.

    `§5 L7` names it in the constitution's own words — *"an untagged generation
    is a fabrication"* — and `§3.0` prices a fabrication at 0. This policy is
    **correct on every value it returns**, including all 160 generations, and it
    is killed by `tagging = 0/160` alone. That is the kill demonstrated rather
    than argued, and it is the reason the identity clauses and not `§3.0`'s
    averaging are what govern this layer (`R8` clause 8).
    """

    name = "always-observed"

    def answer(self, reading, record):
        q = record["q"]
        if q["op"] == "current":
            step = reading.current(q["entity"], q["key"])
            if step is None:
                return _abstain()
            return _answer(step[1], OBSERVED, "recall", (step[0],), step[0])
        entity = q["cue"]["entity"]
        built = reading.profile(entity)
        if built is None:
            return _abstain()
        item, support = built
        return _answer(item, OBSERVED, "recall", support, max(support))


class BlanketHedger(Policy):
    """The `§3.0`-honest hedger: abstain on every generation-shaped cue.

    `R7` clause 7's escape, one layer on. It keeps 100 apiece and leaves both the
    calibration denominator and `tagging`'s denominator behind — and on this
    artifact it is killed by ARITHMETIC, because the generation class is 80
    permille of the answerable core and `§5 L7`'s own `F >= 950` is a
    50-permille budget spent at 900 per hedge.
    """

    name = "blanket-hedger"

    def answer(self, reading, record):
        q = record["q"]
        if q["op"] == "current":
            step = reading.current(q["entity"], q["key"])
            if step is None:
                return _abstain()
            return _answer(step[1], OBSERVED, "recall", (step[0],), step[0])
        return _abstain()


class Oracle(Policy):
    """Class **O** — reads the artifact's declared class table.

    It attains every clause trivially and proves nothing, which is exactly why
    `R5` clause 3 makes the class declaration mandatory: the Layer-6 lesson
    (*"a confidence oracle reading ground_truth.json attains everything and is
    useless"*) stated in advance rather than after.
    """

    cls = "O"
    name = "oracle"

    def answer(self, reading, record):
        q = record["q"]
        if q["op"] == "current":
            step = reading.current(q["entity"], q["key"])
            if step is None:
                return _abstain()
            return _answer(step[1], OBSERVED, "recall", (step[0],), step[0])
        entity = q["cue"]["entity"]
        if record["declared"] == "U":
            return _abstain()
        item = declared_profiles()[entity]
        lineage = OBSERVED if lineage_table()[entity] == 0 else GENERATED
        stored = reading.profile_at.get(entity)
        support = (stored[0],) if stored is not None else \
            reading.composed_only(entity)[1]
        if lineage == GENERATED:
            self.record_generation(entity)
        return _answer(item, lineage, "recall" if lineage == OBSERVED
                       else "derive", support, max(support))


POLICIES = (Oracle, Witness, RetrievalOnly, AlwaysGenerated, AlwaysObserved,
            BlanketHedger)


def policy_by_name(name):
    for klass in POLICIES:
        if klass.name == name:
            return klass()
    raise KeyError(name)


# ---- the labeller bench: Theorem 1, exhibited ------------------------------
#
# A LABELLER decides `observed` vs `generated` WITHOUT consulting the store. The
# three sources available to it are the query itself, the raw entity id, and the
# emission order — which here are two handles, since region members are emitted
# in id order with `e1 = e0 + 1`. Every one of them mislabels exactly `PAIRS`
# of the region's 2*PAIRS queries, and the id-keyed ones do so only because the
# coin is BALANCED.

def _label_always(value):
    return lambda entity, record: value


def _label_id_parity(generated_when_even):
    def label(entity, record):
        even = (entity % 2 == 0)
        gen_it = even if generated_when_even else (not even)
        return GENERATED if gen_it else OBSERVED
    return label


def _label_by_cue_shape(entity, record):
    """`generated` iff the cue is a profile cue — the shape-reading labeller.

    This is `PRE-READ.md §6.3`'s predicted fifth kill in person: the labeller
    that reads the class off the query's own shape. On an artifact where the
    generation class had its own op or key it would score 0 errors and
    `tagging = 1000` would measure a lookup. Here it scores `PAIRS`.
    """
    return GENERATED if record["q"]["op"] == "generate" else OBSERVED


def _label_by_pair_index(entity, record):
    """A POSITIONAL labeller: `generated` iff the compound's pair index is even.

    Constant within a pair, like the two `always-*` labellers and unlike the
    id-keyed ones, so Theorem 1's first half applies to it directly — and it is
    on the bench because it is the sharpest positional rule available and it
    still cannot beat the coin.
    """
    index = (entity - gen.REGION_ID_BASE) // 2
    return GENERATED if index % 2 == 0 else OBSERVED


LABELLER_BENCH = (
    ("always-observed", _label_always(OBSERVED), "constant"),
    ("always-generated", _label_always(GENERATED), "constant"),
    ("by-cue-shape", _label_by_cue_shape, "query-only"),
    ("by-pair-index", _label_by_pair_index, "positional"),
    ("id-parity-generated", _label_id_parity(True), "id-keyed"),
    ("id-parity-observed", _label_id_parity(False), "id-keyed"),
)


def region_records():
    """The 2*PAIRS forcing queries — the region, unsampled."""
    return tuple(r for r in queries() if r["class"] in ("KG1", "KO"))


def labeller_errors(label):
    """How many of the region's queries this labeller gets the LINEAGE wrong on."""
    wrong = 0
    for record in region_records():
        entity = record["q"]["cue"]["entity"]
        want = GENERATED if record["declared"] == "G" else OBSERVED
        if label(entity, record) != want:
            wrong += 1
    return wrong


def labeller_pair_profile(label):
    """`{pair index: how many of its two members this labeller mislabels}`."""
    by_entity = {}
    for record in region_records():
        entity = record["q"]["cue"]["entity"]
        want = GENERATED if record["declared"] == "G" else OBSERVED
        by_entity[entity] = (label(entity, record) != want)
    profile = {}
    for p in declared()["pairs"]:
        profile[p["pair"]] = int(by_entity[p["e0"]]) + int(by_entity[p["e1"]])
    return profile


# ---- the measures ----------------------------------------------------------
#
# `§5 L7` states three ratios and NO denominator for any of them. The
# denominators below are `R8` clause 3's, and they are stated
# here in one place so that no trial can quietly choose a different one.
#
#   tagging   — over the declared **G** queries the policy ANSWERS.
#               numerator: those answered with lineage `generated`.
#               (`tagging_all`, over the whole declared class, is the STRICTER
#               ungated diagnostic, in the shape `R3` gave `F_strict` and `R4`
#               clause 4 gave `F_corruption`.)
#   novelty   — over the items the policy TAGS `generated`, in any class.
#               numerator: those whose canonical bytes appear nowhere in the
#               ingested store. Checked by the harness against frozen bytes.
#   validity  — over the same set. numerator: those satisfying `PROFILE_FORM`.
#
# An empty denominator is `n/a`, and `n/a` DISQUALIFIES (clause 3(c)).

NA = None


def _ratio(hit, total):
    if total == 0:
        return NA
    return Fraction(hit, total)


def score(policy, payloads=None, records=None):
    """Score one policy over the whole battery. Exact `Fraction`s throughout."""
    reading = base_reading() if payloads is None else Reading(payloads)
    policy.ingest_marks(reading)
    records = queries() if records is None else records

    rows = []
    answered = []
    scored_all = []
    scored_core = []
    tag_den = tag_hit = 0
    gen_items = []
    wrong = fabricated = abstentions = 0
    untagged_generations = 0
    support_cited = support_recoverable = 0

    for record in records:
        ans = policy.answer(reading, record)
        status = ans["status"]
        if status == "answer":
            if record["answerable"]:
                correct = (ans["value"] == record["value"])
            else:
                correct = False
                fabricated += 1
            if not correct:
                wrong += 1
            answered.append((ans["confidence"], correct))
            tag = ans["provenance"]
            for t in tag["support"]:
                support_cited += 1
                if reading.recoverable(t):
                    support_recoverable += 1
            s = 1000 if correct else 0
            if ans["lineage"] == GENERATED:
                gen_items.append(ans["value"])
            if record["declared"] == "G":
                tag_den += 1
                if ans["lineage"] == GENERATED:
                    tag_hit += 1
                else:
                    untagged_generations += 1
        else:
            abstentions += 1
            s = 100 if record["answerable"] else 1000
        scored_all.append(s)
        if record["answerable"]:
            scored_core.append(s)
        rows.append((record["qid"], status, ans["lineage"], ans["confidence"]))

    novel = sum(1 for item in gen_items
                if canon(item) not in reading.canon_bytes)
    valid = sum(1 for item in gen_items if gen.profile_form_ok(item))
    n_declared_g = len(generation_class())

    n_pos = sum(1 for _c, ok in answered if ok)
    return {
        "policy": policy.name,
        "class": policy.cls,
        "A": len(answered),
        "n_pos": n_pos,
        "n_neg": len(answered) - n_pos,
        "wrong": wrong,
        "fabricated": fabricated,
        "abstentions": abstentions,
        "tagged_generated": len(gen_items),
        "untagged_generations": untagged_generations,
        "validity": _ratio(valid, len(gen_items)),
        "novelty": _ratio(novel, len(gen_items)),
        "tagging": _ratio(tag_hit, tag_den),
        "tagging_all": _ratio(tag_hit, n_declared_g),
        "tagging_denominator": tag_den,
        "conjunction": conjunction(policy, reading, records),
        "brier": brier(answered),
        "ece": ece(answered),
        "auroc": auroc(answered),
        "F_all": fidelity(scored_all),
        "F_core": fidelity(scored_core),
        "support_recoverability": _ratio(support_recoverable, support_cited),
        "trace": tuple(rows),
    }


def conjunction(policy, reading, records=None):
    """`§5 L7`'s humility measure — `(novel AND valid AND tagged)`, DEFINED.

    `§5` states it once and only on the capped side, so Stage A must say over
    what. It is a **per-item conjunction over the artifact's declared G class**:
    an item counts iff the policy answered that query, tagged the item
    `generated`, the item is grammar-valid, and its canonical bytes appear
    nowhere in the ingested store. The denominator is the whole declared class,
    so it is a property of the artifact and cannot be emptied by a policy.

    It is deliberately NOT a correctness measure: `§5 L7` names three conjuncts
    and correctness is not one of them. `F >= 950` is where correctness lives,
    and a policy emitting valid novel tagged nonsense dies there.
    """
    records = queries() if records is None else records
    hit = 0
    for record in records:
        if record["declared"] != "G":
            continue
        ans = policy.answer(reading, record)
        if ans["status"] != "answer" or ans["lineage"] != GENERATED:
            continue
        item = ans["value"]
        if not gen.profile_form_ok(item):
            continue
        if canon(item) in reading.canon_bytes:
            continue
        hit += 1
    return Fraction(hit, len(generation_class()))


def scoreboard():
    """Every named policy scored over the frozen artifact, exact."""
    out = {}
    for klass in POLICIES:
        out[klass.name] = score(klass())
    return out


def as_permille(figures):
    """The same dict with each `Fraction` rounded to an integer permille."""
    out = {}
    for key, value in figures.items():
        if isinstance(value, Fraction):
            out[key] = permille(value)
        else:
            out[key] = value
    return out


# ---- the promotion ladder: three generations, scored at each rung ----------

class LedgerBlind(Witness):
    """The reference policy that keeps NO lineage ledger — a trial fixture.

    It is never engine code. It exists for the reason `strain/l3`'s naive
    reference count and `strain/l5`'s ledger-blind firing policy exist: a claim
    that a record BINDS is only a claim if something that ignores the record
    measurably fails. This one composes exactly as the witness does and then
    calls its own re-ingested output observed fact — `§5 L7`'s promotion, in the
    plainest possible form.
    """

    name = "ledger-blind"

    def record_generation(self, entity, rung=1):
        pass                       # the whole difference, in one method


def promotion_ladder(policy):
    """Re-ingest the policy's own generations three deep. Returns a list of rungs.

    Each rung: the harness (the CALLER, which is what makes this suggestibility
    in `GAPMAP §6`'s literal sense) appends the items the policy generated at
    that depth as ordinary payloads, then re-asks EVERY declared-G query and
    counts how many the policy now reports as `observed` fact.

    `promotion` is that count. `§5 L7` gates it at 0, three deep.
    """
    payloads = list(stream())
    rungs = []
    produced = {}
    for depth in (1, 2, 3):
        reading = Reading(payloads)
        policy.ingest_marks(reading)
        emitted = []
        for record in queries():
            if record["declared"] != "G" or record.get("depth") != depth:
                continue
            ans = policy.answer(reading, record)
            if ans["status"] == "answer" and ans["lineage"] == GENERATED:
                emitted.append(ans["value"])
        produced[depth] = emitted
        payloads = payloads + emitted

        after = Reading(payloads)
        policy.ingest_marks(after)
        promoted = 0
        still_generated = 0
        for record in queries():
            if record["declared"] != "G":
                continue
            ans = policy.answer(after, record)
            if ans["status"] != "answer":
                continue
            if ans["lineage"] == OBSERVED:
                promoted += 1
            else:
                still_generated += 1
        rungs.append({"depth": depth, "emitted": len(emitted),
                      "promotion": promoted, "still_generated": still_generated,
                      "store": len(payloads)})
    return rungs


def support_on_generated(policy):
    """After the ladder, how many depth-2 tags cite a re-ingested GENERATION.

    `§4.2` as written cannot see it: a re-ingested generation is an actually
    ingested event with a real `t`, so a tag naming it is schema-VALID. This
    function is where `PRE-READ.md §2.2(c)` stops being an argument — the number
    it returns is the number of tags the frozen `laws/t_provenance_schema.py`
    validator accepts while their whole warrant is generated content.
    """
    payloads = list(stream())
    reading = Reading(payloads)
    policy.ingest_marks(reading)
    emitted = {}
    for record in queries():
        if record["declared"] == "G" and record.get("depth") == 1:
            ans = policy.answer(reading, record)
            if ans["status"] == "answer":
                emitted[record["qid"]] = ans["value"]
    payloads = payloads + [emitted[q] for q in sorted(emitted)]
    generated_ts = set(range(len(stream()), len(payloads)))

    after = Reading(payloads)
    policy.ingest_marks(after)
    cites = 0
    tags = []
    for record in queries():
        if record["declared"] != "G" or record.get("depth") != 2:
            continue
        ans = policy.answer(after, record)
        if ans["status"] != "answer":
            continue
        tag = ans["provenance"]
        tags.append(tag)
        if any(t in generated_ts for t in tag["support"]):
            cites += 1
    return {"depth2_answers": len(tags), "citing_a_generation": cites,
            "ingested_max": len(payloads) - 1, "tags": tuple(
                tuple(sorted(t["support"])) for t in tags)}


# ---- the band, as arithmetic rather than as a recorded number --------------

def generation_share():
    """`g` — the generation-required share of the answerable core, exact."""
    answerable = sum(1 for r in queries() if r["answerable"])
    return Fraction(len(generation_class()), answerable)


def hedger_bound():
    """The one-sided window: blanket abstention breaks `F >= 950` iff `g > 1/18`.

    `§3.0` pays 100 for an abstention on an answerable query and 1000 for a
    correct answer, so a policy that abstains on a share `g` of an all-answerable
    core and is correct elsewhere scores `F = 1000 - 900g`. Hence

        F >= 950   <=>   900g <= 50   <=>   g <= 1/18 = 55.5 permille.

    `R7` clause 3(c)'s LOWER bound (`A >= 10r`) is deliberately NOT inherited:
    it came from Theorem 1's FORCED error under a withheld coin, and nothing is
    withheld from a correct generator here, so the Layer-7 window is one-sided.
    """
    return Fraction(1, 18)


def hedging_ladder():
    """`k -> (F_core, tagging denominator)` for a policy hedging `k` G queries.

    Scored OUTSIDE the policy interface on purpose, exactly as
    `ATTAINABILITY-B.md §5`'s `k = 0..100` ladder was: a policy that may CHOOSE
    which generation-class queries to hedge is a strictly larger family than any
    named baseline, so the bound it produces is strictly stronger.

    The point of the ladder is the last column. `tagging`'s denominator is
    emptied only at `k = |G|`, and by then `F` is already gone — so on this
    artifact `n/a` is unreachable by any policy that clears `§5 L7`'s own
    fidelity clause, which is `R7` clause 3(d)'s *"the consequence costs
    nothing"* one layer on.
    """
    total_answerable = sum(1 for r in queries() if r["answerable"])
    n_g = len(generation_class())
    ladder = []
    for k in range(n_g + 1):
        f = Fraction((total_answerable - k) * 1000 + k * 100,
                     total_answerable * 1000)
        ladder.append((k, f, n_g - k))
    return ladder


def max_hedges_clearing_f(exact=True):
    """The largest `k` a hedger can afford. `exact` is `R7` clause 4's reading."""
    best = -1
    for k, f, _den in hedging_ladder():
        ok = (f >= Fraction(GATE_F, 1000)) if exact else (permille(f) >= GATE_F)
        if ok:
            best = k
    return best


# ---- the substrate survey: the fifth substrate kill, MEASURED --------------
#
# `PRE-READ.md §6.1` predicted the verdict and this is the measurement behind it.
# A query is GENERATION-REQUIRED iff its correct answer is grammar-valid and
# provably not any item the stream carries. So for every frozen artifact that
# has an answer key at all, the question is: how many of its answers are absent
# from its own stream?

def _answer_values_in_stream(payloads, answers):
    """`(n_answers, n_absent)` — how many answers the stream does NOT carry."""
    present = set()
    for payload in payloads:
        present.add(canon(payload))
        f = gen.facet(payload)
        if f is not None:
            present.add(canon(f[2]))
    absent = sum(1 for a in answers if canon(a) not in present)
    return (len(answers), absent)


def substrate_survey():
    """What the `generated` tag costs on every artifact this project has frozen.

    One row per artifact: the battery whose answers were taken, how many
    answerable queries that battery declares, and how many of their answers are
    **absent** from the artifact's own stream. An artifact whose `absent` is 0
    has an EMPTY generation-required class: no query on it can be answered only
    by composition, so on it `tagging`'s denominator is empty, `novelty`'s is
    empty, and a gate citing either measures nothing.

    Every row is computed here from the frozen bytes; none is asserted from a
    document. `trials/ascension/l7/t_attainability.py` requires the whole survey
    to read `absent = 0`, so the fifth substrate kill is a trial and not a
    paragraph — and a corpus frozen later that DID force a composition would go
    red there rather than pass unnoticed.
    """
    if "survey" in _CACHE:
        return _CACHE["survey"]
    rows = []
    for name, payloads, answers, battery, why in _substrate_rows():
        n, absent = _answer_values_in_stream(payloads, answers)
        rows.append({"artifact": name, "battery": battery, "answerable": n,
                     "absent": absent, "why": why})
    _CACHE["survey"] = tuple(rows)
    return _CACHE["survey"]


def l7compose_under_the_same_instrument():
    """The survey's own measurement, applied to the artifact this session builds.

    ONE INSTRUMENT, TWO VERDICTS: the same `_answer_values_in_stream` fold that
    reads `absent = 0` on every frozen artifact reads `absent = |G|` here. That
    is the fifth substrate kill and its remedy measured by one ruler, which is
    what keeps the kill from being a claim about corpora nobody re-checked.
    """
    answers = [r["value"] for r in queries() if r["answerable"]]
    return _answer_values_in_stream(stream(), answers)


def _jsonl(module):
    return [json.loads(line) for line in
            module.frozen_bytes().decode("utf-8").splitlines() if line]


_ASSERTION_WHY = ("every current-value answer is the value of an assertion the "
                  "stream carries: the answer key is read off the chains")
_EVENT_WHY = ("the only queries defined on it return the EVENTS themselves "
              "(read / recall / retention), so an answer is a payload the "
              "stream carries by definition")


def _substrate_rows():
    """Every frozen artifact, with the answers its own frozen battery asks for.

    The batteries are not invented here. `chronicle`, `murk`, `l4stream` and
    `l5stream` are queried for current values through the same chain reading the
    Layer-4 engine implements; `sessions`, `l3stream` and `l3streamb` are queried
    by the Layer-1/2/3 batteries, whose answers are the stored events; the two
    Layer-6 artifacts carry their query sets and answer keys inside their own
    frozen bytes; and `§8.8`'s REAL corpus carries no answer key at all.
    """
    from corpora.chronicle import generator as chronicle
    from corpora.sessions import generator as sessions
    from corpora.murk import generator as murk
    from corpora.l3stream import generator as l3s
    from corpora.l3streamb import generator as l3sb
    from corpora.l4stream import generator as l4s
    from corpora.l5stream import generator as l5s
    from corpora.l6battery import generator as l6b
    from corpora.l6batteryb import generator as l6bb
    from corpora import real_sessions
    import _l3tasks

    out = []
    for name, module in (("chronicle", chronicle), ("murk", murk),
                         ("l4stream", l4s), ("l5stream", l5s)):
        payloads = _jsonl(module)
        chains, _order = gen.chains_of(payloads)
        out.append((name, payloads, [steps[-1][1] for steps in chains.values()],
                    "current-value over its own chains", _ASSERTION_WHY))

    sess = _jsonl(sessions)
    out.append(("sessions", sess, list(sess), "the Layer-1 read battery",
                _EVENT_WHY))

    for name, module in (("l3stream", l3s), ("l3streamb", l3sb)):
        payloads = _jsonl(module)
        bundle = _l3tasks.stream(name)
        answers = [tg["event"]["payload"] for tg in bundle["targets"]]
        out.append((name, payloads, answers, "the frozen Layer-3 retention "
                    "battery (_l3tasks)", _EVENT_WHY))

    bat = l6b.load()
    out.append(("l6battery", _jsonl(murk),
                [r["value"] for r in bat["queries"] if r["answerable"]],
                "its own frozen query set",
                "its answer keys are derived from murk's frozen "
                "ground_truth.json, which names the t's each defect touches"))

    art = l6bb.load()
    out.append(("l6batteryb", art["stream"],
                [r["value"] for r in art["queries"] if r["answerable"]],
                "its own frozen query set",
                "the forcing region's two candidate values are BOTH asserted "
                "and one of them is right: it forces a commitment, not a "
                "composition"))

    if real_sessions.real_entries():
        payloads = real_sessions.payloads()
        out.append(("real-sessions/v1", payloads, list(payloads),
                    "none — there is no answer key",
                    "the REAL corpus is exempt from the byte-match law and "
                    "carries no answer key at all; 25 events cannot carry a "
                    "compositional grammar, three orders of magnitude short"))
    return out

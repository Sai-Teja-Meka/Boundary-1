"""core/layers/l2_recall.py — Layer 2: Recall (deterministic associative index).

Layer 2 adds one capability to the honest floor: **associative `recall(cue)`** —
recover a stored event from a content cue, with no logical `t` supplied. It is
pure, deterministic, integer-only (§2), and it is built **entirely on top of the
frozen Layer-1 primitives** (`core/state.py`, `core/serialize.py`,
`core/layers/l1_retention.py`); it edits none of them (§9). Layer 1's five verbs
and its byte-exact retention are unchanged and still reachable here.

## The index (rederived from Mem0's BM25 + entity-boost, GAPMAP S2)

`recall` is powered by a **deterministic index that lives in state** — token
n-grams over payload **atoms** plus per-event **MinHash** signatures. There is no
model, no embedding, no float: the index is a function of the bytes already
stored.

  * **Atoms** are field-qualified tokens derived from a payload:
    `kind=attr`, `entity=7`, `key=region`, `val=north`, and for id-bearing
    fields (`entity`/`src`/`dst`/`sid`) a cross-field adjacency atom `id#7`.
    Field-qualification is our replacement for NLTK lemmatization (whitelist,
    §2.5): the grammar vocabularies are fixed lowercase ASCII, so normalization
    is lowercase + field-qualify + id-adjacency — deterministic, no library.
  * **n-grams**: id-anchored bigrams `id#7^key=region` couple an entity to the
    facts asserted about it (the associative adjacency Mem0's entity-boost
    supplies), each a rarer, more discriminative index term.
  * **Scoring is per-item, never store-relative.** A candidate's score is
    `Σ_{a ∈ cue ∩ item} idf(a)` in exact `Fraction`, with `idf(a) = 1/df(a)` a
    function of the atom's document frequency **alone** — not of store size, not
    of any per-query min/max. Adding decoys that share none of a cue's atoms
    cannot move the ranking (the GA decoy-invariance strain). Rare atoms
    dominate; common ones (`kind=attr`) barely register — BM25's shape.
  * **MinHash** signatures (K salted SHA-256 minima, integer-only) fingerprint an
    event's atom set, so verbatim near-duplicates collide exactly — used to
    recognize the ambiguous case and abstain rather than fabricate a `t`.

## Honest recall (the deterministic floor, THEORY §2)

`recall` answers only when the cue resolves to **one** event that contains the
**whole** probe; a cue matching no event, or several equally (a near-duplicate),
yields a principled **abstention** (§7.3), never a guess. This index models the
**surface/base-level** half of spreading activation and stops there: it recovers
by lexical/structural overlap, not by learned semantic association. That
exclusion is deliberate — it is what makes recall LLM-free and byte-reproducible.

## The budget still binds (§4.1)

The index is **state**, and every atom-posting cell and signature cell **counts
against occupancy**. A write is refused deterministically when the event *plus
its index cost* would exceed the cap — an index the budget cannot afford is a
design failure, not an exemption. The snapshot's SHA-256 checksum covers **all**
of state, index included; `restore` additionally rederives the index from the
log and rejects any snapshot whose stored index diverges from it.
"""

import hashlib
from dataclasses import dataclass, field, replace
from fractions import Fraction

from core.serialize import encode, decode, check_canonical, copy_value, NonCanonical
from core.state import (
    EventLog, event_cost,
    log_empty, log_append, log_get, log_iter, log_from_list,
)

LAYER = 2

# A generous default cap: the Phase-0/L2 trial stores replay without a lawful
# refusal (budget measure B = 1000), while the refusal path (§4.1) — now
# accounting the index too — is exercised directly by small-cap ops/strain
# trials. Integer only (§2.2). Matches the Layer-1 default so cross-layer
# reasoning stays simple.
DEFAULT_BUDGET = 1_000_000_000

# MinHash: K deterministic permutations via salted SHA-256, each minimum a
# 64-bit integer. K is fixed and frozen into the L2 anchors this session.
MINHASH_K = 16
_SIG_BYTES = 8  # bytes of each SHA-256 digest taken as the 64-bit hash value

# Fields whose integer value is an entity/relation id: they emit a cross-field
# adjacency atom `id#<v>` so a cue naming an entity reaches every event about it
# regardless of which id field mentions it (Mem0 entity-boost, rederived).
_ID_FIELDS = frozenset({"entity", "src", "dst", "sid"})

MAGIC = "boundary1-l2-snapshot"
_ENVELOPE_KEYS = frozenset({"magic", "checksum", "body"})
_BODY_KEYS = frozenset({"layer_cap", "budget_cap", "occupancy", "next_t", "events", "index"})


class CorruptSnapshot(ValueError):
    """Raised by `restore` when a snapshot fails its integrity check (loudly)."""


# ---- the index -------------------------------------------------------------

@dataclass(frozen=True)
class Index:
    """The deterministic recall index (part of state; counts against budget).

    `postings` maps each atom to the ascending tuple of event `t`'s that carry
    it (the inverted index; `df(atom) = len(postings[atom])`). `sigs` is the
    per-event MinHash signature, indexed by `t` (a tuple of K integers).

    Immutable by discipline: every update returns a NEW `Index` (a shallow-copied
    `postings` dict with one tuple extended per atom), so a snapshot taken
    mid-stream never sees a later write.
    """

    postings: dict = field(default_factory=dict)
    sigs: tuple = ()

    def __eq__(self, other):
        return (isinstance(other, Index)
                and self.postings == other.postings
                and self.sigs == other.sigs)


_EMPTY_INDEX = Index(postings={}, sigs=())


# ---- the state -------------------------------------------------------------

@dataclass(frozen=True)
class L2State:
    """The frozen Layer-2 engine state: the Layer-1 fields plus the index (§2.1)."""

    layer_cap: int
    budget_cap: int
    occupancy: int
    next_t: int
    last_cost: int
    events: EventLog
    index: Index


def new_state(layer_cap, budget_cap):
    """A fresh state capped at `layer_cap` with integer budget cap `budget_cap`."""
    if not isinstance(layer_cap, int) or isinstance(layer_cap, bool):
        raise TypeError("layer_cap must be a plain int")
    if not isinstance(budget_cap, int) or isinstance(budget_cap, bool):
        raise TypeError("budget_cap must be a plain int")
    if layer_cap < 0:
        raise ValueError("layer_cap must be non-negative")
    if budget_cap <= 0:
        raise ValueError("budget_cap must be positive (§4.1)")
    return L2State(layer_cap=layer_cap, budget_cap=budget_cap, occupancy=0,
                   next_t=0, last_cost=0, events=log_empty(), index=_EMPTY_INDEX)


def _recall_on(state):
    return state.layer_cap >= LAYER


def _retention_on(state):
    return state.layer_cap >= 1


# ---- atom derivation (token normalization; grammar-vocabulary, no NLTK) ----

def _norm_scalar(v):
    """Normalize a scalar to a token string (lowercase; grammar is ASCII)."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, int):
        return str(v)
    return v.lower()


def _flatten(prefix, value, out):
    """Emit `field=token` unigram atoms for every scalar under `value`.

    Grammar payloads are flat scalar objects; the recursion keeps the index
    honest on any canonical payload (nested keys path-qualified, list items
    index-qualified) without ever assuming a shape.
    """
    if isinstance(value, dict):
        for k in value:                     # key order irrelevant: atoms form a set
            _flatten(prefix + k + ".", value[k], out)
        return
    if isinstance(value, list):
        for i, item in enumerate(value):
            _flatten(prefix + str(i) + ".", item, out)
        return
    # scalar
    key = prefix[:-1] if prefix.endswith(".") else prefix
    out.add(key + "=" + _norm_scalar(value))
    # cross-field id adjacency atom for the id-bearing fields
    leaf = key.rsplit(".", 1)[-1]
    if leaf in _ID_FIELDS and isinstance(value, int) and not isinstance(value, bool):
        out.add("id#" + str(value))


def _unigrams(payload):
    out = set()
    _flatten("", payload, out)
    return out


def _bigrams(unigrams):
    """id-anchored bigrams: couple each `id#E` to every other unigram atom.

    These are the associative adjacency terms — "entity E co-occurs with
    key=region" — rarer and more discriminative than either atom alone. Bounded
    (few id atoms per event), so the index stays affordable.
    """
    ids = sorted(a for a in unigrams if a.startswith("id#"))
    others = sorted(a for a in unigrams if not a.startswith("id#"))
    out = set()
    for a in ids:
        for b in others:
            out.add(a + "^" + b)
    return out


def _atoms(payload):
    """Every index term for a payload: unigrams + id-anchored bigrams."""
    unis = _unigrams(payload)
    return unis | _bigrams(unis)


def _minhash(unigrams):
    """K-permutation MinHash over the unigram set (integer-only, deterministic)."""
    sig = []
    for k in range(MINHASH_K):
        salt = k.to_bytes(2, "big")
        best = None
        for a in unigrams:
            h = int.from_bytes(hashlib.sha256(salt + a.encode("utf-8")).digest()[:_SIG_BYTES], "big")
            if best is None or h < best:
                best = h
        sig.append(best if best is not None else 0)
    return tuple(sig)


def _index_cost(atoms, sig):
    """Cells the index spends on one event: one per posting entry, one per sig int."""
    return len(atoms) + len(sig)


def _index_add(index, t, atoms, sig):
    """Return a new Index with event `t` added (immutable; postings stay ascending)."""
    postings = dict(index.postings)                 # shallow copy-on-write
    for a in atoms:
        prev = postings.get(a)
        postings[a] = (prev + (t,)) if prev is not None else (t,)
    return Index(postings=postings, sigs=index.sigs + (sig,))


def _build_index(events, layer_cap):
    """Rederive the full index from the event log (used to validate a restore)."""
    if layer_cap < LAYER:
        return _EMPTY_INDEX
    idx = _EMPTY_INDEX
    for ev in log_iter(events):
        unis = _unigrams(ev["payload"])
        atoms = unis | _bigrams(unis)
        idx = _index_add(idx, ev["t"], atoms, _minhash(unis))
    return idx


# ---- verbs -----------------------------------------------------------------

def write(state, payload):
    """Append one event; assign and return its logical `t`. Refuse over budget.

    The event's cost is its payload cells (§4.1) **plus** the index cells it
    creates; a write that would push occupancy over the cap is refused
    deterministically, with no partial write and no eviction (eviction is Layer
    3). Below recall (`layer_cap < 2`) no index is built — the engine is exactly
    the read-by-time floor, so `make_engine(1)` is a genuine Retention engine.
    """
    check_canonical(payload)

    if not _retention_on(state):
        t = state.next_t                            # null engine: sees, retains nothing
        return replace(state, next_t=t + 1, last_cost=0), t

    if not _recall_on(state):
        cost = event_cost(payload)
        if state.occupancy + cost > state.budget_cap:
            return state, None
        t = state.next_t
        record = {"payload": copy_value(payload), "t": t}
        return replace(state, occupancy=state.occupancy + cost, next_t=t + 1,
                       last_cost=cost, events=log_append(state.events, record)), t

    unis = _unigrams(payload)
    atoms = unis | _bigrams(unis)
    sig = _minhash(unis)
    cost = event_cost(payload) + _index_cost(atoms, sig)
    if state.occupancy + cost > state.budget_cap:
        return state, None                          # deterministic refusal (§4.1)

    t = state.next_t
    record = {"payload": copy_value(payload), "t": t}
    return replace(state,
                   occupancy=state.occupancy + cost,
                   next_t=t + 1,
                   last_cost=cost,
                   events=log_append(state.events, record),
                   index=_index_add(state.index, t, atoms, sig)), t


def read(state, t):
    """Return the event record stored at logical time `t`, or None (Layer 1 verb)."""
    if not _retention_on(state):
        return None
    if not isinstance(t, int) or isinstance(t, bool):
        return None
    if t < 0 or t >= state.next_t:
        return None
    return copy_value(log_get(state.events, t))


def read_range(state, t0, t1):
    """All stored events with `t` in [t0, t1] inclusive, t-ascending (Layer 1 verb)."""
    if not _retention_on(state):
        return []
    if not isinstance(t0, int) or isinstance(t0, bool):
        return []
    if not isinstance(t1, int) or isinstance(t1, bool):
        return []
    lo = t0 if t0 > 0 else 0
    hi = t1 if t1 < state.next_t - 1 else state.next_t - 1
    out = []
    t = lo
    while t <= hi:
        out.append(copy_value(log_get(state.events, t)))
        t += 1
    return out


# ---- recall (the Layer-2 capability) ---------------------------------------

def _permille(x):
    """Exact Fraction in [0,1] -> integer permille, round-half-to-even (§3.5)."""
    n = x * 1000
    q = n.numerator // n.denominator
    r = n - q
    if r < Fraction(1, 2):
        return q
    if r > Fraction(1, 2):
        return q + 1
    return q if q % 2 == 0 else q + 1


def recall(state, cue):
    """Recover the single stored event matching the content probe `cue`.

    Returns an Answer (§7.2). Honest by construction: answers only when exactly
    one stored event contains the **whole** probe; abstains when none does
    (unanswerable) or several do (ambiguous / verbatim near-duplicate). Never
    raises on a bad cue — capability/absence surfaces as a scored abstention
    (§7.3).
    """
    if not _recall_on(state):
        return _abstain()                           # no associative index below Layer 2
    if not isinstance(cue, dict):
        return _abstain()
    try:
        check_canonical(cue)
    except NonCanonical:
        return _abstain()

    postings = state.index.postings
    cue_unis = _unigrams(cue)
    cue_atoms = cue_unis | _bigrams(cue_unis)
    if not cue_atoms:
        return _abstain()

    # Per-item idf scores (for ranking / confidence). idf(a) = 1/df(a): a
    # function of the atom's own document frequency, never of store size or a
    # per-query min/max — so decoys sharing no cue atom cannot perturb it.
    scores = {}
    for a in cue_atoms:
        ts = postings.get(a)
        if ts is None:
            continue
        w = Fraction(1, len(ts))
        for t in ts:
            scores[t] = scores.get(t, 0) + w
    if not scores:
        return _abstain()

    # The answer must contain the WHOLE probe: intersect the postings of every
    # cue unigram. Full match(es) are exactly the events satisfying the probe.
    full = None
    for a in cue_unis:
        ts = postings.get(a)
        if ts is None:
            full = set()
            break
        full = set(ts) if full is None else (full & set(ts))
        if not full:
            break

    if not full:
        return _abstain()                           # unanswerable: nothing matches the whole probe
    if len(full) > 1:
        return _abstain()                           # ambiguous (e.g. verbatim near-duplicate)

    best_t = next(iter(full))
    best = scores[best_t]                            # a full match is the unique argmax
    others = [s for t, s in scores.items() if t != best_t]
    second = max(others) if others else 0
    conf = _permille(Fraction(best - second, best)) if best > 0 else 0

    ev = copy_value(log_get(state.events, best_t))
    prov = {"support": [best_t], "kind": "recall", "t_asof": best_t}
    return _answer(ev, conf, prov)


def recall_ranking(state, cue):
    """The per-item candidate ranking for `cue`: `[(t, score)]`, score-desc, t-asc.

    Read-only; exposes exactly the per-item idf scoring `recall` ranks by, so the
    decoy-invariance strain can assert that injecting decoys which share no cue
    atom leaves the ranking (and thus the answer) invariant — the property a
    store-relative / globally-normalized scorer would violate.
    """
    if not _recall_on(state) or not isinstance(cue, dict):
        return []
    try:
        check_canonical(cue)
    except NonCanonical:
        return []
    postings = state.index.postings
    cue_unis = _unigrams(cue)
    cue_atoms = cue_unis | _bigrams(cue_unis)
    scores = {}
    for a in cue_atoms:
        ts = postings.get(a)
        if ts is None:
            continue
        w = Fraction(1, len(ts))
        for t in ts:
            scores[t] = scores.get(t, 0) + w
    return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))


# ---- the Answer (§7.2) & the generic query binding -------------------------

def _answer(value, confidence, provenance):
    return {"status": "answer", "value": value,
            "confidence": confidence, "provenance": provenance}


def _abstain(confidence=0, provenance=None):
    return {"status": "abstain", "value": None,
            "confidence": confidence, "provenance": provenance}


def query(state, q):
    """Answer a query (§7.2). Unsupported / un-capable queries abstain, never raise."""
    if not isinstance(q, dict):
        return _abstain()
    op = q.get("op")

    if op == "read":
        ev = read(state, q.get("t"))
        if ev is None:
            return _abstain()
        prov = {"support": [ev["t"]], "kind": "recall", "t_asof": ev["t"]}
        return _answer(ev, 1000, prov)

    if op == "read_range":
        if not _retention_on(state):
            return _abstain()
        evs = read_range(state, q.get("t0"), q.get("t1"))
        if evs:
            support = [e["t"] for e in evs]
            prov = {"support": support, "kind": "aggregate", "t_asof": support[-1]}
            return _answer(evs, 1000, prov)
        return _answer(evs, 1000, None)             # an empty range is a valid answer

    if op == "recall":
        return recall(state, q.get("cue"))

    return _abstain()                               # capability absent (§7.3)


# ---- snapshot / restore (checksum covers ALL of state, index included) -----

def _index_body(index):
    """Canonical (tuple-free) dict form of the index for serialization (§2.4)."""
    return {
        "postings": {a: list(ts) for a, ts in index.postings.items()},
        "sigs": [list(s) for s in index.sigs],
    }


def _body(state):
    """The canonical, deterministic dict form of the full state (index included).

    `last_cost` is transient budget bookkeeping (not observable in any query), so
    it is excluded — two independent ingest sequences yield byte-identical
    snapshots (determinism, §2.3).
    """
    return {
        "layer_cap": state.layer_cap,
        "budget_cap": state.budget_cap,
        "occupancy": state.occupancy,
        "next_t": state.next_t,
        "events": [copy_value(e) for e in log_iter(state.events)],
        "index": _index_body(state.index),
    }


def state_checksum(state):
    """SHA-256 hex over the canonical encoding of the full state body (§2.4)."""
    return hashlib.sha256(encode(_body(state))).hexdigest()


def snapshot(state):
    """Canonical, checksummed serialization of the state (§7.1, §2.4)."""
    body = _body(state)
    checksum = hashlib.sha256(encode(body)).hexdigest()
    return encode({"magic": MAGIC, "checksum": checksum, "body": body})


def _index_from_body(index_body):
    """Rebuild an Index from its serialized body (lists back to tuples)."""
    postings = {}
    raw_postings = index_body["postings"]
    if not isinstance(raw_postings, dict):
        raise CorruptSnapshot("snapshot index postings is not an object")
    for a, ts in raw_postings.items():
        if not isinstance(ts, list):
            raise CorruptSnapshot("snapshot posting list is not an array")
        postings[a] = tuple(ts)
    raw_sigs = index_body["sigs"]
    if not isinstance(raw_sigs, list):
        raise CorruptSnapshot("snapshot index sigs is not an array")
    return Index(postings=postings, sigs=tuple(tuple(s) for s in raw_sigs))


def restore(data):
    """Rebuild a state from snapshot bytes; fail loudly on any corruption.

    Three independent guards, all raising `CorruptSnapshot`:
      1. the envelope/body structure and the SHA-256 checksum over the whole
         body (a flipped bit anywhere — payload OR index — is caught);
      2. the recomputed occupancy must equal the stored occupancy;
      3. the index rederived from the restored log must equal the stored index —
         so a snapshot whose index was tampered *and its checksum recomputed*
         (an index-vs-log divergence) is still rejected.
    """
    try:
        envelope = decode(data)
    except Exception as exc:                        # invalid JSON / UTF-8 / float
        raise CorruptSnapshot("snapshot is not decodable: %r" % (exc,))

    if not isinstance(envelope, dict) or frozenset(envelope.keys()) != _ENVELOPE_KEYS:
        raise CorruptSnapshot("snapshot envelope keys are wrong")
    if envelope["magic"] != MAGIC:
        raise CorruptSnapshot("snapshot magic mismatch")

    body = envelope["body"]
    if not isinstance(body, dict) or frozenset(body.keys()) != _BODY_KEYS:
        raise CorruptSnapshot("snapshot body keys are wrong")

    if hashlib.sha256(encode(body)).hexdigest() != envelope["checksum"]:
        raise CorruptSnapshot("snapshot checksum mismatch (corruption detected)")

    lc, bc = body["layer_cap"], body["budget_cap"]
    occ, nt, evs = body["occupancy"], body["next_t"], body["events"]
    for name, val in (("layer_cap", lc), ("budget_cap", bc), ("occupancy", occ), ("next_t", nt)):
        if not isinstance(val, int) or isinstance(val, bool):
            raise CorruptSnapshot("snapshot %s is not an integer" % (name,))
    if not isinstance(evs, list):
        raise CorruptSnapshot("snapshot events is not an array")

    events = log_from_list(copy_value(e) for e in evs)
    stored_index = _index_from_body(body["index"])

    # (3) the index must be exactly the one the log implies.
    rederived = _build_index(events, lc)
    if rederived != stored_index:
        raise CorruptSnapshot("snapshot index diverges from the event log")

    # (2) occupancy must be exactly what these events + this index cost.
    recomputed = 0
    for ev in log_iter(events):
        if lc >= LAYER:
            unis = _unigrams(ev["payload"])
            atoms = unis | _bigrams(unis)
            recomputed += event_cost(ev["payload"]) + _index_cost(atoms, _minhash(unis))
        elif lc >= 1:
            recomputed += event_cost(ev["payload"])
    if recomputed != occ:
        raise CorruptSnapshot("snapshot occupancy diverges from the accounted cost")

    return L2State(layer_cap=lc, budget_cap=bc, occupancy=occ, next_t=nt,
                   last_cost=0, events=events, index=stored_index)


# ---- the generic engine interface (§7, INTERFACE.md) -----------------------

def empty():
    """A fresh, full Layer-2 engine state (adapter contract, §7)."""
    return new_state(layer_cap=LAYER, budget_cap=DEFAULT_BUDGET)


def make_engine(layer_cap, budget_cap=DEFAULT_BUDGET):
    """A fresh state capped at `layer_cap` (§7.4). 1 = the read-by-time floor."""
    return new_state(layer_cap=layer_cap, budget_cap=budget_cap)


def ingest(state, payload):
    """Append one event; return `(state', t)`. `t` is None on budget refusal (§4.1)."""
    return write(state, payload)


def last_cost(state):
    """Integer work-unit cost of the most recent successful write (§3.3, §4.1)."""
    return state.last_cost

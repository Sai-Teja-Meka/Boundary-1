"""shell/dogfood/consolidate.py — the store's derived view, at Layer 7.

`[L4] [DOGFOOD]`, upgraded to prospection at `[L5] [DOGFOOD]`, to meta-memory at
`[L6] [DOGFOOD]` and to generation at `[L7] [DOGFOOD]`. `remember` writes
episodes and `recall` finds one of them. This module answers the third question a
memory owes its owner — *what does all of it add up to?* — by folding the store's
session summaries through `core/layers/l7_generation.py` and reading the result
back through the **ordinary query interface** (§7.1): `current`, `asof`,
`profile`, `count`, `consolidation`, `forgetting`, `recall`, `read`, `fired`,
`prospection`, `calibration`, `lineage`, `generate`. The shell computes no answer
of its own; it asks, labels, and formats.

## The shell declares a reading, exactly as the engine does

Layer 4 folds an event into a supersession chain only when its payload reads as
an `(entity, key, value)` assertion under `ASSERTION_FORMS` — *"a declared
reading of the frozen chronicle-family grammars"* (`README-l4 §1`). A session
summary is not in that grammar and never will be: it is prose, and the engine's
facet map is frozen (§9.2). So the reading of a **session** into an assertion is
declared here, in the shell, which is where a reading of a human grammar belongs
(§2.6) — the same move `tok` already makes for the cue surface.

    session summary at store `t`  ->  the summary itself, plus one `attr`
                                      assertion per fact it states about the
                                      project it belongs to

The assertions are emitted in exactly the engine's own form,
`{"kind":"attr","entity":<int>,"key":<str>,"val":<scalar>}`, and nothing else —
which is what makes them **invertible** (`README-l4 §1`), so `read(t)`
regenerates them byte-exactly after their episodes are gone and `profile`
attributes them to a grammar kind instead of abstaining.

## Nothing derived is ever written back

The derived stream is built on demand and thrown away. It is **not** ingested
into the store, and `remember` is still the store's only writer. That is a
deliberate refusal, and the autopsies are the reason: `autopsy/mem0/ANATOMY.md`
records a store in which an inferred fact and a user-stated fact are
indistinguishable once written, and §5 L7's self-pollution law exists because a
memory that promotes its own derivations to observed fact has stopped being a
record. A view recomputed from the episodes cannot drift from them; a derived
event committed beside them can. The price is that the store's own state file
stays a Layer-2 ledger, which `FIELD.md` records as this run's chafe.

## What a `t` means here

The derived stream has its own logical times — one session becomes several
events, so replay `t` and store `t` are different counters (§1.3 owns both, and
neither is the other's index). Every number this module *prints* is a **store**
`t`, translated through `origin`, so the report joins to `BOUNDARY.log` the way
`README.md` says a reader should: on the line, not on arithmetic.

`[L5]`: the replay now runs through `core/layers/l5_prospection.py`, and the
engine emits events of its own. Under `BOUNDARY-RULINGS.md R6` clause 2 a firing
consumes a logical `t` of its own, so **one caller write advances `next_t` by
`1 + f`** and replay `t` is no longer an index into the caller stream at all.
`origin` is therefore a **map** `replay t -> store t`, and a firing is attributed
to the store event whose write satisfied it — which is the honest answer to
*"where did this come from"* and the only one the caller stream can give.

## What `[L6]` changes: the number, and nothing else

The replay now runs through `core/layers/l6_meta_memory.py`, and the whole of
that upgrade is that **every answer this module reads back carries the engine's
own `§7.2` confidence, and the report prints it**. Nothing else moves, and that
is the layer rather than a convenience: `L6State` adds no field to the frozen
`L5State` (`README-l6 §0`), so the derived state this module builds is the one it
built yesterday — same occupancy, same chains, same demotions, same firings — and
what changed is what the engine says about it.

Three consequences, each stated here because each is a fact about *this store*
and not about the layer in general:

  * **the confidence is derived, never stored.** It is recomputed on every read
    of a view that is itself recomputed on every read and thrown away, so there
    is no row anywhere carrying a number somebody could edit — the `[L4]`
    refusal to write derivations back, inherited one layer on;
  * **the shell narrows, it never widens** (`intend.py`'s rule, applied to a
    second reading): `SET_ONCE_KEYS` below is *computed* from the engine's own
    frozen declaration, so this shell cannot call a key set-once that the engine
    does not, and cannot drift from it;
  * **1000 is not a default.** A key that admits updates is answered by its
    latest assertion and the engine has proved it. A set-once key whose chain
    holds `d` mutually exclusive claimants is answered at `permille(1/d)` — 500
    at `d = 2` — and `FIELD.md` records what this project's own history measures.

## What `[L7]` changes: the store confesses its origins

The replay runs through `core/layers/l7_generation.py`, and the upgrade is a
claim about *where every answer came from*, made in three places and through
`§7.1`'s three verbs unchanged:

  * **every answer is rendered with its provenance tag.** `§4.2` is dormant
    before Layer 7 and **binding, never un-bindable, from it** (`§4.2.1-2`): a
    non-abstaining answer carries a valid tag or scores **wrong (0) however
    correct its value is**. So a tag this report used to mention in two places
    is now printed beside every answer it renders — `recall` for content the
    store still holds, `derive` for content it regenerated, `generated` for an
    item it composed (`R8` clause 4's item-lineage, orthogonal to `§4.2.3`'s
    four answer-channel kinds) — and an answer that carries **no** tag is
    printed as `UNTAGGED` rather than laundered into one;
  * **lineage is displayed where it exists.** A derived or generated answer's
    `support` is the `t`s the engine says carry it, so the report translates
    them to store `t` and asks `read` whether each can still be shown. `R8`
    clause 5(a) settled the support reading **shape-only** — a support entry
    must be *ingested*, not *recoverable* — and paid for the weaker claim with
    an **ungated** recoverability rate. This is that rate, on real fuel;
  * **`CERTAIN` is split by its warrant.** `confidence_for` states
    `permille(1/d)` on a declared set-once chain and `CERTAIN` **everywhere
    else**, and `README-l6 §4` recorded the residual that leaves: *a generated
    item has no chain, no distinct-value count and no set-once status, so it
    falls through to `CERTAIN`*. A surface that printed only the number could
    not tell a `1000` the engine **counted** from a `1000` it **defaulted** to.
    So every rendered answer is classified by where its number came from
    (`warrant_of` below), and the closing census prints the tally. On this
    store the finding is total: **no key of this reading is set-once, so not one
    `‰` it prints is measured** — which is the residual `iid 2` was armed to
    surface, one tier in from the generated case it named.
"""

from core.layers import l7_generation as l7
from core.serialize import encode
from shell.dogfood import event as ev

# The dogfood store is a handful of session summaries; the derived stream is a
# few hundred assertions. A cap generous enough that nothing is evicted unless
# the operator explicitly asks for pressure (`--budget`).
DERIVED_BUDGET = 1 << 22

# The keys a session asserts about its project, in report order. Each is read
# off fields the summary already carries — the `move` flag as given, and the
# `BOUNDARY.log` line verbatim as the session itself wrote it. Nothing here is
# inferred about the world; a fact that is not in the summary is not asserted.
ASSERTED_KEYS = ("layer", "move", "suite", "anchors",
                 "decisions", "files_touched", "open_questions")

# The one key whose assertions are an append log rather than a supersession: a
# session's open questions do not overwrite the previous session's. The chain
# carries them all anyway, and `asof` walks them out — see FIELD.md.
QUESTION_KEY = "open_question"

SUMMARY_KIND = ev.KIND
ASSERTION_KIND = "attr"

# The engine's own name for the confidence of an answer it has proved. Imported
# rather than typed: `1000` appears in this module only as `l7.CERTAIN`, so the
# report cannot state a certainty the engine does not.
CERTAIN = l7.CERTAIN

# The engine's frozen kind for an intention. A stored intention is replayed
# UNCHANGED — the shell's reading of it is the identity, because the payload is
# already in the engine's own grammar and `README-l5 §1.2` admits it only if it
# rebuilds from `(iid, cond, fire)` byte-for-byte. `shell/dogfood/intend.py` is
# where that reading is declared; nothing here may add a field to it.
INTENTION_KIND = l7.INTENTION_KIND

# The three payload kinds THIS reading emits into the derived stream, and the two
# the ENGINE's composition reading needs. Both are read off the engine rather
# than typed beside it, for `SET_ONCE_KEYS`' reason: the shell narrows, it never
# widens, and a typed copy is a second reading waiting to drift.
#
# They are disjoint, and that disjointness IS the generation census's finding:
# `COMPOSITION_FORM` determines a `profile` item from two `part` assertions, and
# a store whose fuel is session prose contains neither — so under this reading no
# answer requires composition and none can carry the `generated` tag. That is a
# property of the READING and not a defect of the layer: the same engine composes
# 160 items on `corpora/l7compose` (`README-l7 §3`).
DECLARED_KINDS = (SUMMARY_KIND, ASSERTION_KIND, INTENTION_KIND)
COMPOSITION_KINDS = (l7.PART_KIND, l7.PROFILE_KIND)

# `R8` clause 4's closed lineage vocabulary — a property of the ITEM, orthogonal
# to `§4.2.3`'s four answer-channel kinds. Read off the engine, never typed.
OBSERVED = l7.OBSERVED
GENERATED = l7.GENERATED

# What the report prints for an answer that carries no `§4.2` tag at all. It is
# NOT one of `§4.2.3`'s kinds and is deliberately not made to look like one: from
# Layer 7 an untagged non-abstaining answer is what `§4.2.2` prices at 0, so the
# surface names it and does not launder it into `derive`.
UNTAGGED = "UNTAGGED"

# Where the `‰` on an answer came from. The classification is a reading of the
# ENGINE's own model (`README-l6 §1.3`, `l6.confidence_for`) and computes no
# number of its own:
#
#   MEASURED  — `confidence_for` COUNTED this answer's evidence. Reachable only
#               on a set-once key, where the number is `permille(1/d)` over the
#               chain's claimants and would have been below 1000 had the chain
#               held a rival. The number is a function of the evidence.
#   NOT_SET_ONCE — `confidence_for` returned `CERTAIN` on its FIRST line, before
#               looking at the chain, because the declared reading does not call
#               the key set-once. Defensible (`the latest assertion is what is in
#               force`) and still a fall-through: no evidence could move it.
#   NO_MODEL  — an op Layer 6 attaches `CERTAIN` to by construction (`read`,
#               `recall`, `profile`, `count`, `fired`, the diagnostics): it
#               returns content regenerated exactly, or it abstains.
#               `README-l6 §4` calls that a non-capability by construction.
#   NO_CHAIN  — a **composed** item: no chain, no distinct-value count, no
#               set-once status, so `confidence_for` is never consulted at all.
#               `README-l6 §4`'s residual proper, `README-l7 §4` states it OPEN,
#               and `iid 2` was armed to make it visible here.
MEASURED = "measured"
NOT_SET_ONCE = "default:not-set-once"
NO_MODEL = "default:no-model"
NO_CHAIN = "default:no-chain"
WARRANTS = (MEASURED, NOT_SET_ONCE, NO_MODEL, NO_CHAIN)

# The keys of this reading that the ENGINE's frozen reading calls set-once — the
# only keys on which a Layer-6 confidence can be anything but `CERTAIN`.
#
# It is COMPUTED and not typed, which is the whole of its content: `l6.set_once`
# is the authority (`SET_ONCE_KEYS = ("origin",)`, a declared reading of the
# frozen grammars, `README-l6 §1.2`), so this shell can neither call a key
# set-once that the engine does not nor fall out of step with it if the engine's
# reading is ever extended. The shell narrows; it never widens — `intend.py`'s
# rule for the condition vocabulary, applied to the second reading this shell
# declares.
#
# Today it is EMPTY, and that is a measurement rather than an oversight: the one
# key the frozen reading calls set-once is `origin`, and a session summary states
# no origin. `FIELD.md` (2026-08-02) carries the census and what follows from it.
SET_ONCE_KEYS = tuple(k for k in tuple(ASSERTED_KEYS) + (QUESTION_KEY,)
                      if l7.set_once(k))

# The keys the calibration census ASKS about: every key this reading asserts,
# plus every key the engine calls set-once whether this reading asserts it or
# not. The second half is the point — those are the only keys on which a
# confidence can be anything but `CERTAIN`, so a census that asked only about
# what this reading writes could never see a tie and would be reporting its own
# vocabulary rather than the store's certainty. Where the key is never asserted
# the row says so and the engine abstains, which is the honest empty answer.
CENSUS_KEYS = tuple(dict.fromkeys(tuple(ASSERTED_KEYS) + (QUESTION_KEY,)
                                  + tuple(l7.SET_ONCE_KEYS)))


# ---- parsing the facts a log line states ------------------------------------

def layer_of(log_line):
    """The claimed layer from a `[L<n>] …` prefix, or `None`.

    A reading of the line's own leading tag, not a judgement about the project:
    a line that does not open with `[L<digits>]` asserts no layer and none is
    invented for it.
    """
    if not log_line.startswith("[L"):
        return None
    end = log_line.find("]")
    if end < 0:
        return None
    digits = log_line[2:end]
    if not digits or not digits.isdigit():
        return None
    return int(digits)


def tagged(log_line, name):
    """The body of a `<name: …>` tag, or `None`. The first occurrence wins."""
    opener = "<%s:" % name
    start = log_line.find(opener)
    if start < 0:
        return None
    end = log_line.find(">", start)
    if end < 0:
        return None
    return log_line[start + len(opener):end].strip()


# ---- the declared reading ---------------------------------------------------

def assertion(entity, key, value):
    """One `attr` assertion in the engine's own frozen form, and nothing else."""
    return {"kind": ASSERTION_KIND, "entity": entity, "key": key, "val": value}


def facts_of(payload):
    """The `(key, value)` facts one stored session summary states. Ordered."""
    line = payload["log_line"]
    out = []
    layer = layer_of(line)
    if layer is not None:
        out.append(("layer", layer))
    out.append(("move", payload["move"]))
    for name in ("suite", "anchors"):
        body = tagged(line, name)
        if body is not None:
            out.append((name, body))
    for field in ("decisions", "files_touched", "open_questions"):
        out.append((field, len(payload[field])))
    for question in payload["open_questions"]:
        out.append((QUESTION_KEY, question))
    return out


def session_stream(payload, entity):
    """The derived events one stored session becomes: the episode, then its facts.

    The summary is replayed with an `entity` field added. That is the same kind
    of shell-derived surface `tok` already is, and it buys two things the frozen
    engine cannot be asked for: a handle atom, so the episode is reachable by
    cue at Layer 4 (`handle_atom` reads `HANDLE_FIELDS`, and prose has none of
    them), and an actor, so `profile` counts the session against its project
    instead of dropping it.
    """
    episode = dict(payload)
    episode["entity"] = entity
    out = [episode]
    for key, value in facts_of(payload):
        out.append(assertion(entity, key, value))
    return out


def derived_stream(payload, entities):
    """The derived events one **stored** event becomes, whatever kind it is.

    Two kinds, two readings, and the second one is deliberately the identity:

      * a **session summary** becomes its episode plus one assertion per fact it
        states (`session_stream`) — prose read into the engine's grammar;
      * an **intention** is already in the engine's grammar and is replayed
        unchanged. Adding an `entity` field the way `session_stream` does would
        cost it the inversion `README-l5 §1.2` demands and it would never arm.
    """
    if payload.get("kind") == INTENTION_KIND:
        return [dict(payload)]
    return session_stream(payload, entities[payload["project"]])


def project_entities(records):
    """`{project: entity id}` in first-appearance order, from 1.

    Integer ids are the engine's requirement, not a choice: `facet` refuses a
    non-integer entity and `_actor` will not attribute an episode to one. The
    order is the store's own ingestion order, so the mapping is a function of
    the store and is stable for as long as the store only grows.
    """
    out = {}
    for record in records:
        payload = record["payload"]
        if payload.get("kind") != SUMMARY_KIND:
            continue                      # an intention belongs to no project
        name = payload["project"]
        if name not in out:
            out[name] = len(out) + 1
    return out


# ---- the derived state ------------------------------------------------------

def derive(records, budget_cap=DERIVED_BUDGET):
    """Fold the store's events into a Layer-6 state.

    Returns `(state, origin, sessions, entities, refused)`:

      * `origin` — `{replay_t: store_t}`, covering **every** logical time the
        engine assigned, its own firings included (module docstring);
      * `sessions` — `[(store_t, summary_replay_t, last_replay_t)]` for the
        session summaries, in order, so a report can ask `asof` at the instant a
        session ended;
      * `entities` — the `{project: entity}` mapping the reading used;
      * `refused` — `(store_t, payload)` of the first write the budget refused,
        or `None`.

    A refusal is surfaced, never swallowed: an event the budget cannot admit
    stops the replay and is reported as such, because a view built from a
    truncated stream that says so is honest and one that does not is a lie. At
    Layer 5 a refusal is total in a second sense the engine owns — where the
    budget cannot house a firing, the whole transition is refused with `t`
    unspent (`README-l5 §1.4`), so a half-kept promise is not a state this
    replay can reach.

    `[L6]`: the engine is `l6_meta_memory` and the state it returns is the state
    `l5_prospection` returned yesterday — `L6State` adds no field (`README-l6
    §0`), so nothing above this line changes and every answer below it carries a
    confidence.

    `[L7]`: the engine is `l7_generation`, which adds exactly one field — the
    lineage ledger, written by `ingest` because `query` is pure (`README-l7 §0`).
    On this store's fuel it stays **empty**: the ledger only ever records a
    `profile` payload the engine recognises as its own, and this reading emits
    none, so the derived state is the Layer-6 state to the cell and the canonical
    body differs in exactly two branches — the recorded `layer_cap`, which is the
    cap and not the content, and an empty `lineage`. `README-l7 §0`'s *"where
    there is nothing to record it costs nothing"*, on this project's own history
    rather than on a corpus, and asserted in `t_generation.py`.
    """
    entities = project_entities(records)
    state = l7.make_engine(l7.LAYER, budget_cap=budget_cap)
    origin = {}
    sessions = []
    refused = None
    for record in records:
        payload = record["payload"]
        first = state.next_t
        for derived in derived_stream(payload, entities):
            state, t = l7.write(state, derived)
            if t is None:
                refused = (record["t"], derived)
                break
            for spent in range(t, state.next_t):
                # `t` is the caller event's; everything after it in this
                # transition is a firing the write caused (R6 clause 2).
                origin[spent] = record["t"]
        if refused is not None:
            break
        if payload.get("kind") == SUMMARY_KIND:
            sessions.append((record["t"], first, state.next_t - 1))
    return state, origin, sessions, entities, refused


# ---- reading the state back, only through query() ---------------------------

def ask(state, q, seen=None):
    """One query through the generic interface (§7.1). Never raises (§7.3).

    `seen`, when given, is the list every answer this report renders is recorded
    in as it is rendered — its `§4.2` tag, its `R8` clause 4 lineage where it has
    one, and the warrant of its `‰`. The closing census is a tally of that list
    and NOT a second pass over the state, so what it counts is exactly what the
    reader was shown. `[L7]`.
    """
    answer = l7.query(state, q)
    if seen is not None:
        seen.append(observation(q, answer))
    return answer


# ---- provenance, lineage and the warrant of a number ------------------------

def warrant_of(op, key=None, lineage=None):
    """Where the `‰` on an answer came from — counted evidence, or a fall-through.

    A reading of the engine's OWN model (`l6.confidence_for`) and not a second
    model: the shell states no number, it says which branch of the engine's
    function produced the one it was handed.

      * a **composed** item never reaches `confidence_for` at all — no chain, no
        distinct-value count, no set-once status (`README-l6 §4`);
      * `current` / `asof` on a **set-once** key COUNTS the chain's claimants, so
        the number is a function of this answer's evidence and could be below
        1000;
      * `current` / `asof` on any other key returns `CERTAIN` on the function's
        first line, before the chain is looked at;
      * every other op carries `CERTAIN` by construction.
    """
    if lineage == GENERATED:
        return NO_CHAIN
    if op in ("current", "asof"):
        return MEASURED if l7.set_once(key) else NOT_SET_ONCE
    return NO_MODEL


def tag_of(answer):
    """The `§4.2` provenance kind an answer carries, or why it carries none.

    Three outcomes and each is printed rather than smoothed: an abstention
    (`§4.2` requires no tag of one — it is the one non-answer `§3.0` pays 1000
    for), a kind from `§4.2.3`'s closed four, or `UNTAGGED` — a non-abstaining
    answer with `provenance: null`, which is exactly what `§4.2.2` prices at 0
    however correct its value is.
    """
    if answer.get("status") != "answer":
        return "abstain"
    prov = answer.get("provenance")
    if not isinstance(prov, dict) or prov.get("kind") is None:
        return UNTAGGED
    return prov["kind"]


def tag_text(answer):
    """The tag as the report prints it: the channel, and the lineage beside it.

    `R8` clause 4 keeps the two claims orthogonal — `kind` says how the answer
    reached the caller and `lineage` says what the item is — so the surface shows
    both rather than collapsing them, which is what makes `derive+generated`
    (a composed item) distinguishable from `derive` (one the engine regenerated
    from a chain it holds).
    """
    tag = tag_of(answer)
    lineage = answer.get("lineage")
    if lineage is None:
        return tag
    return "%s+%s" % (tag, lineage)


def support_of(answer):
    """The `t`s an answer's tag cites, as a tuple. Empty for an untagged answer."""
    prov = answer.get("provenance")
    if not isinstance(prov, dict):
        return ()
    support = prov.get("support")
    return tuple(support) if isinstance(support, list) else ()


def observation(q, answer):
    """One rendered answer, reduced to what the closing census counts."""
    op = q.get("op") if isinstance(q, dict) else None
    key = q.get("key") if isinstance(q, dict) else None
    lineage = answer.get("lineage")
    return {"op": op, "key": key, "status": answer.get("status"),
            "tag": tag_of(answer), "lineage": lineage,
            "confidence": answer.get("confidence"),
            "warrant": warrant_of(op, key, lineage),
            "support": support_of(answer)}


def recoverable(state, support, seen=None):
    """`(shown, cited)` — how many of a tag's cited `t`s the engine can still produce.

    `R8` clause 5(a) settled `§4.2`'s support reading **shape-only**: a support
    entry must be an **ingested** `t` and need not be a **recoverable** one, with
    the weaker claim said out loud — *provenance certifies that an answer had a
    source, and not that the source can be shown* — and paid for by an **ungated**
    recoverability rate reported beside the gated numbers. This is that rate, and
    it is ungated here too: an answer citing a `t` the budget has taken breaches
    no clause, and the surface reports it rather than gating it.
    """
    shown = 0
    for t in support:
        if ask(state, {"op": "read", "t": t}, seen)["status"] == "answer":
            shown += 1
    return (shown, len(support))


def _store_t(origin, replay_t):
    if replay_t is None:
        return None
    return origin.get(replay_t)


def _replay_t(origin, store_t):
    """The replay `t` of the caller event that came from store `t`, or `None`.

    The inverse of `origin` on its caller entries: the first replay time that
    store event occupied. A firing shares its cause's store `t`, and a firing is
    never first, so the minimum is always the caller's own.
    """
    found = None
    for replay, stored in origin.items():
        if stored == store_t and (found is None or replay < found):
            found = replay
    return found


def current_fact(state, entity, key, origin, seen=None):
    """`(value, store_t, confidence, tag, support)` for `(entity, key)` now, or `None`.

    `[L6]`: the third element is the engine's own `§7.2` confidence in integer
    permille — read off the answer, never computed here. It is `1000` on a key
    the declared reading does not call set-once, because the value in force is
    the latest assertion and that is a thing the engine has proved; it is
    `permille(1/d)` where a set-once chain holds `d` mutually exclusive
    claimants (`README-l6 §1.3`).

    `[L7]`: the fourth and fifth are the answer's own `§4.2` tag and the store
    `t`s it cites. They are appended rather than substituted so that every
    earlier reader of this tuple keeps reading what it read — the value, where it
    was decided, and how sure the engine is — and the provenance is new
    information beside them and not a rearrangement of them.
    """
    answer = ask(state, {"op": "current", "entity": entity, "key": key}, seen)
    if answer["status"] != "answer":
        return None
    support = support_of(answer)
    return (answer["value"],
            _store_t(origin, support[0] if support else None),
            answer["confidence"],
            tag_text(answer),
            tuple(_store_t(origin, t) for t in support))


def history(state, entity, key, origin, upto, seen=None):
    """The whole chain for `(entity, key)`, as `[(store_t, value, confidence)]`.

    Reconstructed by walking `asof` forward and reading each answer's own
    provenance `support` — the assertion the engine says carries the value. No
    engine internals are touched: the history is the sequence of *distinct
    supports* the ordinary as-of query reports across the stream.

    `[L6]`: each step carries the confidence the engine stated **at that
    horizon**, which is not the same number as the one it states now. `asof`
    prices the evidence the answer actually had — the chain up to the asked `t`
    (`README-l6 §1.4`) — so on a set-once key an early step can be certain and a
    later one a coin flip, and the walk shows where certainty was lost.
    """
    out = []
    stamps = set()
    for t in range(upto + 1):
        answer = ask(state, {"op": "asof", "entity": entity, "key": key, "t": t},
                     seen)
        if answer["status"] != "answer":
            continue
        support = support_of(answer)
        stamp = support[0] if support else None
        if stamp is None or stamp in stamps:
            continue
        stamps.add(stamp)
        out.append((_store_t(origin, stamp), answer["value"], answer["confidence"]))
    return out


def collapse(chain):
    """`[(store_t, value, restatements, confidence)]` — equal values folded.

    A session asserts the project's whole state every time, so most assertions
    restate the value already in force. The chain keeps them all (they are what
    `asof` walks); a *history* is the sequence of **changes**, so the display
    folds a run of equal values into the `t` it was first decided at and counts
    the restatements rather than dropping them silently.

    A fold keeps the **last** confidence of the run, which is the one that was
    still in force when the value finally changed: a restatement can only lower
    it (a further claimant on a set-once chain), never raise it, so keeping the
    first would report a certainty the later evidence had already withdrawn.
    """
    out = []
    for store_t, value, conf in chain:
        if out and out[-1][1] == value and type(out[-1][1]) is type(value):
            out[-1][2] += 1
            out[-1][3] = conf
            continue
        out.append([store_t, value, 0, conf])
    return [(t, v, n, c) for t, v, n, c in out]


def claimants_seen(chain):
    """How many mutually exclusive values a walked chain asserted, by §2.4 bytes.

    The engine's own `n_distinct` rule (`README-l6 §1.2`: canonical bytes, not
    Python equality, because `True == 1` there and `true != 1` here) applied to
    the values the *queries* returned — so this is a census of answers and not a
    reach into the state, and the shell still computes no confidence of its own.
    """
    return len({encode(value) for _t, value, _c in chain})


def calibration(state, entity, origin, upto, seen=None):
    """The per-key calibration census: what the store is certain of, and why.

    One row per key the declared reading asserts, each carrying the value in
    force, the number of distinct claimants the chain has held, whether the
    engine's frozen reading calls the key **set-once**, and the confidence the
    engine states. The engine's own `{"op":"calibration"}` diagnostic is read
    beside it (§7.1 — no new verb), so the shell's count of ties and the
    engine's cannot disagree without the report saying so.
    """
    rows = []
    for key in CENSUS_KEYS:
        now = current_fact(state, entity, key, origin, seen)
        chain = history(state, entity, key, origin, upto, seen)
        rows.append({"key": key,
                     "set_once": l7.set_once(key),
                     "asserts": len(chain),
                     "claimants": claimants_seen(chain),
                     "value": None if now is None else now[0],
                     "since": None if now is None else now[1],
                     "confidence": None if now is None else now[2],
                     "tag": None if now is None else now[3],
                     "warrant": warrant_of("current", key)})
    return rows, ask(state, {"op": "calibration"}, seen)


def channels(state, ts=None, seen=None):
    """`{held, derived, gone}` over `ts` (default: the whole derived stream).

    The discriminator is the engine's own, not the shell's: `read`'s provenance
    `kind` is `"recall"` when the episode is still held and `"derive"` when it
    was regenerated from a chain (`l4_consolidation.query`), so counting the two
    separates **still an episode** from **demoted** without touching state.

    That distinction is the whole of `README-l4 §4`'s non-capability: content
    survives demotion and association does not, because `recall` runs over the
    handle index of retained episodes and a demoted event has no posting in it.
    """
    counts = {"held": 0, "derived": 0, "gone": 0}
    span = range(state.next_t) if ts is None else ts
    for t in span:
        answer = ask(state, {"op": "read", "t": t}, seen)
        if answer["status"] != "answer":
            counts["gone"] += 1
        elif answer["provenance"]["kind"] == "recall":
            counts["held"] += 1
        else:
            counts["derived"] += 1
    return counts


def reachability(state, records, sessions, entity, origin, seen=None):
    """Per session: is its episode still readable, and still reachable by cue?

    Two channels, asked separately because Layer 4 separates them: `read(t)` is
    content and `recall(cue)` is association, and `README-l4 §4` states that a
    demoted episode keeps the first and loses the second. The cue used is the
    session's own whole token bag, which no other session's bag contains unless
    it is a strict superset — an ambiguity the answer reports rather than hides.
    """
    out = []
    summaries = [r for r in records if r["payload"].get("kind") == SUMMARY_KIND]
    for (store_t, summary_t, _last), record in zip(sessions, summaries):
        payload = record["payload"]
        read = ask(state, {"op": "read", "t": summary_t}, seen)
        cue = {"entity": entity, "tok": dict(payload["tok"])}
        found = ask(state, {"op": "recall", "cue": cue}, seen)
        hit = None
        if found["status"] == "answer":
            hit = _store_t(origin, found["value"]["t"])
        out.append({"store_t": store_t,
                    "readable": read["status"] == "answer",
                    "recallable": found["status"] == "answer",
                    "recall_t": hit,
                    "tag": tag_text(read)})
    return out


def promises(state, records, origin, seen=None):
    """What the engine did with every intention the store declared.

    Read through the **ordinary query interface** and nothing else (§7.1), which
    is what makes this a report of the engine's behaviour rather than of the
    shell's expectations:

      * `{"op":"fired","iid":I}` is the exactly-once ledger, and it answers with
        a **list** — `dup-fire = 0` is a ratified gate clause, so an intention
        that fired twice has to be visible here and not only in an engine's own
        bookkeeping (`README-l5`, `STAGE-B.md §2`). The list is reported as it
        comes back, never collapsed to its first element.
      * a **pending** intention's own `intend` event is regenerated by
        `{"op":"read","t":t0}` from the pending entry (`README-l5 §1.3`), so a
        promise still waiting can be shown in full without the episode existing.

    Each entry also carries the **provenance kind** of that read-back, because
    at Layer 5 it is the whole of the take-back rule and it points opposite ways
    for the two states a promise can be in: a *pending* intention's event is
    `derive` (the pending entry regenerates it) and a *kept* one's is `recall`
    (nothing regenerates it any more, so where there is room the episode came
    back into the store, and where there was none it is a booked loss and the
    read abstains). `README-l5 §1.3`; `BOUNDARY.log` line 32.

    Returns one entry per stored intention, in ingest order.
    """
    out = []
    for record in records:
        payload = record["payload"]
        if payload.get("kind") != INTENTION_KIND:
            continue
        iid = payload["iid"]
        entry = {"store_t": record["t"], "iid": iid,
                 "cond": payload["cond"], "fire": payload["fire"],
                 "fired": [], "readable": False, "regenerated": False,
                 "provenance": None, "confidence": None}
        answer = ask(state, {"op": "fired", "iid": iid}, seen)
        if answer["status"] == "answer":
            for rec in answer["value"]:
                read_back = ask(state, {"op": "read", "t": rec["t"]}, seen)
                entry["fired"].append({
                    "replay_t": rec["t"],
                    "store_t": _store_t(origin, rec["t"]),
                    "payload": rec["payload"],
                    "provenance": (read_back["provenance"] or {}).get("kind"),
                    "confidence": read_back["confidence"]})
        armed_at = _replay_t(origin, record["t"])
        back = ask(state, {"op": "read", "t": armed_at}, seen)
        entry["readable"] = back["status"] == "answer"
        entry["confidence"] = back["confidence"]
        entry["provenance"] = (back["provenance"] or {}).get("kind")
        if entry["readable"]:
            entry["regenerated"] = (
                encode(back["value"]["payload"]) == encode(payload))
        out.append(entry)
    return out


def describe_condition(cond):
    """One line of prose for any condition the engine can read.

    Generic over the frozen grammar rather than over the shell's narrower
    reading, so a condition this shell would no longer declare still renders as
    itself instead of as a blob — the store outlives the vocabulary that wrote
    it, and a report that could not read an old promise would be the wrong kind
    of shell.
    """
    if not isinstance(cond, dict):
        return encode(cond).decode("utf-8")
    if "op" in cond:
        args = cond.get("args") or []
        inner = [describe_condition(a) for a in args]
        if cond["op"] == "not":
            return "not(%s)" % (inner[0] if inner else "")
        joiner = " and " if cond["op"] == "and" else " or "
        return joiner.join(inner) if len(inner) > 1 else (inner[0] if inner else "")
    p = cond.get("p")
    if p == "count_ge":
        return "count(%s)>=%s" % (cond.get("k"), cond.get("v"))
    if p == "val_ge":
        return "val>=%s" % (cond.get("v"),)
    return "%s=%s" % (p, cond.get("v"))


def describe_fire(fire, width=72):
    """One line for the payload a promise surfaces."""
    if not isinstance(fire, dict):
        return encode(fire).decode("utf-8")
    text = fire.get("text")
    if not isinstance(text, str):
        return encode(fire).decode("utf-8")
    if len(text) > width:
        text = text[:width - 1] + "…"
    return "%s about %s — %s" % (fire.get("kind"), fire.get("about"), text)


def prospection_lines(state, records, origin, indent="  ", seen=None):
    """The promises section: what is pending, what fired, and what it said.

    Every number and every payload here comes back through `§7.1` (`promises`
    above); this function only labels and wraps them.
    """
    entries = promises(state, records, origin, seen)
    shape = ask(state, {"op": "prospection"}, seen)
    lines = []
    if shape["status"] == "answer":
        counts = shape["value"]
        lines.append("%sdeclared         %d intention%s — %d pending, %d fired "
                     "(%d + %d cells)"
                     % (indent, len(entries), "" if len(entries) == 1 else "s",
                        counts["pending"], counts["fired"],
                        counts["pending_cells"], counts["fired_cells"]))
    for entry in entries:
        if entry["fired"]:
            when = entry["fired"][0]
            lines.append("%siid %-3d declared at store t=%-3s  FIRED %s at store "
                         "t=%s (derived t=%s)"
                         % (indent, entry["iid"], entry["store_t"],
                            "once" if len(entry["fired"]) == 1
                            else "%d TIMES" % len(entry["fired"]),
                            when["store_t"], when["replay_t"]))
            for fired in entry["fired"]:
                text = fired["payload"].get("text") \
                    if isinstance(fired["payload"], dict) else None
                lines.append("%s    >> %s" % (indent, text if isinstance(text, str)
                                              else encode(fired["payload"]).decode("utf-8")))
                lines.append("%s       the fired event  read(t=%s) %s‰ "
                             "provenance %s (the fired ledger regenerates it)"
                             % (indent, fired["replay_t"], fired["confidence"],
                                fired["provenance"]))
        else:
            lines.append("%siid %-3d declared at store t=%-3s  PENDING%s"
                         % (indent, entry["iid"], entry["store_t"],
                            "" if entry["readable"]
                            else "  (its own event is no longer readable)"))
            lines.append("%s    surfaces  %s"
                         % (indent, describe_fire(entry["fire"])))
        lines.append("%s    when      %s"
                     % (indent, describe_condition(entry["cond"])))
        lines.append("%s    its own event  %s"
                     % (indent, _promise_episode(entry)))
    return lines


def _promise_episode(entry):
    """One line for what `read(t0)` says about a promise's own `intend` event.

    The take-back rule, read off `§7.1` (`README-l5 §1.3`): a **pending**
    intention's event is regenerated by the pending entry and comes back
    `derive`; a **kept** one's cannot be regenerated by anything, so `recall` is
    the only honest provenance it can carry and an abstention means the budget
    booked it as a loss rather than taking it back.
    """
    if not entry["readable"]:
        return ("GONE — read(t0) abstains, so the episode was booked into the "
                "forgetting record (confidence %s‰)" % entry["confidence"])
    exact = "byte-exact" if entry["regenerated"] else "NOT byte-exact"
    if entry["fired"]:
        return ("readable %s, %s‰, provenance %s — taken back into the store, "
                "which is the only honest tag once the pending entry is gone"
                % (exact, entry["confidence"], entry["provenance"]))
    return ("readable %s, %s‰, provenance %s — regenerated by the pending entry"
            % (exact, entry["confidence"], entry["provenance"]))


# ---- the report -------------------------------------------------------------

def _fmt(value, width=60):
    text = value if isinstance(value, str) else str(value)
    return text if len(text) <= width else text[:width - 1] + "…"


def calibration_lines(state, entity, origin, upto, indent="  ", seen=None):
    """The calibration census: what the store is certain of, and why it is.

    A confidence surface that only ever printed `1000‰` would be indistinguishable
    from a surface that printed a constant, which is exactly the defect
    `autopsy/GAPMAP.md §2`'s engine thesis convicts four systems of — metadata
    written and never read where it counts. So the section states the *reason*
    beside the number: how many distinct claimants each chain has held, and
    whether the key is one the engine's frozen reading calls **set-once**, which
    is the only condition under which a claimant is a rival rather than an
    update.
    """
    rows, engine_view = calibration(state, entity, origin, upto, seen)
    declared = engine_view["value"]["set_once_keys"] \
        if engine_view["status"] == "answer" else []
    ties = engine_view["value"]["ties"] if engine_view["status"] == "answer" else 0
    levels = engine_view["value"]["tie_levels"] \
        if engine_view["status"] == "answer" else []

    lines = ["", "calibration — what this store says about its own certainty"]
    lines.append("%sengine reading   set-once keys: %s  (l6.SET_ONCE_KEYS, a "
                 "declared reading of the frozen grammars)"
                 % (indent, ", ".join(declared) or "(none)"))
    lines.append("%sthis reading     %d keys asserted, of which set-once: %s  "
                 "(computed from the engine's — the shell narrows, never widens)"
                 % (indent, len(ASSERTED_KEYS) + 1,
                    ", ".join(SET_ONCE_KEYS) or "(none)"))
    lines.append("%sties             %d chain%s hold more than one claimant for "
                 "a slot that admits exactly one%s"
                 % (indent, ties, "" if ties == 1 else "s",
                    "" if not levels
                    else "  (%s)" % ", ".join("d=%d -> %d‰" % (d, c)
                                              for d, c in levels)))
    lines.append("%s%-16s %-10s %-9s %-26s %-6s %-8s %s"
                 % (indent, "key", "asserted", "claimants", "in force", "states",
                    "tag", "warrant"))
    for row in rows:
        if row["confidence"] is None:
            # An abstaining row still states its warrant, in the conditional: on
            # this store the ONE key whose ‰ could ever be measured is the one
            # this reading never asserts, and that sentence is the census's
            # sharpest row rather than an empty one.
            lines.append("%s%-16s %-10s %-9s %-26s %-6s %-8s would be %s"
                         % (indent, row["key"], "0", "0", "(never asserted)",
                            "ABSTAIN", "abstain", row["warrant"]))
            continue
        lines.append("%s%-16s %-10d %-9d %-26s %4d‰ %-8s %s%s"
                     % (indent, row["key"], row["asserts"], row["claimants"],
                        _fmt(row["value"], 26), row["confidence"], row["tag"],
                        row["warrant"],
                        "  SET-ONCE" if row["set_once"] else ""))
    contradicted = [r for r in rows if r["set_once"] and r["claimants"] > 1]
    if contradicted:
        lines.append("%sa set-once chain holding d claimants is answered at "
                     "permille(1/d): %s"
                     % (indent, ", ".join("%s d=%d -> %d‰"
                                          % (r["key"], r["claimants"],
                                             r["confidence"])
                                          for r in contradicted)))
    else:
        lines.append("%sno key of this reading is set-once, so no chain here can "
                     "be CONTRADICTED — a key that admits updates is answered by "
                     "its latest assertion, which the engine has proved, and "
                     "%d‰ is that proof and not a default"
                     % (indent, CERTAIN))
    return lines


# ---- [L7] provenance, lineage, generation, and the warrant of a number -------

def provenance_lines(state, entity, origin, indent="  ", seen=None):
    """What every answer of the decision history cites, and whether it can be shown.

    `§4.2` is dormant before Layer 7 and binding — never un-bindable — from it,
    so from this layer on a tag is not decoration: an answer without a valid one
    scores **wrong (0) regardless of whether its value is correct** (`§4.2.2`).
    This section is that law made visible on the store's own facts.

    The **recoverability** column is `R8` clause 5(a)'s ungated diagnostic, and
    it is ungated here too. That clause settled the support reading **shape-only**
    — a support entry must be an *ingested* `t`, not a *recoverable* one — said
    the weaker claim out loud (*provenance certifies that an answer had a source,
    and not that the source can be shown*) and paid for it with a rate reported
    beside the gated numbers rather than a gate of its own. On this store it
    reads all-recoverable **at every cap**, and the reason is stated rather than
    left looking like a generous budget: `README-l7 §2.3`'s finding one reading
    over, that `current` cites the assertion which ANSWERS it, so the reading
    loses the answer before it can lose the warrant.
    """
    lines = ["", "provenance — what each answer cites, and whether the citation "
                 "can still be shown"]
    lines.append("%s§4.2 binds from Layer 7 and can never be un-bound: a "
                 "non-abstaining answer carries a valid tag or scores 0 however "
                 "correct it is (§4.2.2)." % indent)
    lines.append("%s%-16s %-14s %-22s %s"
                 % (indent, "key", "tag", "cites store t", "still readable"))
    shown = cited = 0
    for key in ASSERTED_KEYS:
        answer = ask(state, {"op": "current", "entity": entity, "key": key}, seen)
        if answer["status"] != "answer":
            lines.append("%s%-16s %-14s %-22s %s"
                         % (indent, key, "abstain", "(nothing to cite)", "n/a"))
            continue
        support = support_of(answer)
        ok, total = recoverable(state, support, seen)
        shown += ok
        cited += total
        lines.append("%s%-16s %-14s %-22s %s"
                     % (indent, key, tag_text(answer),
                        " ".join(str(_store_t(origin, t)) for t in support)
                        or "(none)",
                        "%d of %d" % (ok, total)))
    lines.append("%ssupport recoverable  %d of %d cited t — UNGATED (R8 clause "
                 "5(a) demands INGESTED, not RECOVERABLE)" % (indent, shown, cited))
    if shown == cited:
        lines.append("%s  and it reads all-recoverable at every cap this store "
                     "can be replayed at, for README-l7 §2.3's reason one reading "
                     "over: `current` cites the assertion that ANSWERS it, so the "
                     "reading loses the answer before it can lose the warrant — "
                     "where a chain is shed the answer abstains and there is no "
                     "citation left to be unrecoverable." % indent)
    return lines


def generation(state, entities, seen=None):
    """The generation census: what this store composes, and what it only recalls.

    Read through `§7.1` alone — `{"op":"lineage"}` is the engine's own ledger
    diagnostic in the shape `consolidation` (L4), `prospection` (L5) and
    `calibration` (L6) established, and `{"op":"generate", ...}` is the one op
    Layer 7 adds. The shell asks; it composes nothing itself.

    Returns `(ledger_answer, kind_rows, probes)`, where `kind_rows` is one row
    per kind the ENGINE's composition reading needs — printed even at zero,
    because an emptiness that is not a row is a silence, which is the shape the
    `[L6]` census fixed for `origin` one layer down.
    """
    ledger = ask(state, {"op": "lineage"}, seen)
    rows = []
    for kind in COMPOSITION_KINDS:
        answer = ask(state, {"op": "count", "kind": kind}, seen)
        rows.append((kind, answer["value"] if answer["status"] == "answer" else 0,
                     answer["status"]))
    probes = []
    for name, entity in sorted(entities.items(), key=lambda kv: kv[1]):
        answer = ask(state, {"op": "generate",
                             "cue": {"kind": l7.PROFILE_KIND, "entity": entity}},
                     seen)
        probes.append((name, entity, answer))
    return ledger, rows, probes


def generation_lines(state, entities, indent="  ", seen=None):
    """The mandatory `[L7]` measurement, rendered as rows and not as a sentence.

    The question is `FIELD.md`'s: under this shell's declared reading, does any
    answer over this project's own history **require composition**, and does any
    carry the `generated` tag? The answer is no, twice, and the reason is a
    property of the READING rather than a defect of the layer — which is why the
    rows below are the engine's own counts of the two kinds `COMPOSITION_FORM`
    needs, and not a sentence asserting their absence.
    """
    ledger, rows, probes = generation(state, entities, seen)
    body = ledger["value"] if ledger["status"] == "answer" else {
        "generated": 0, "cells": 0, "by_rung": []}
    lines = ["", "generation — what this store composes, and what it only recalls"]
    lines.append("%sthis reading emits   %s" % (indent, ", ".join(DECLARED_KINDS)))
    lines.append("%scomposition needs    %s  (COMPOSITION_FORM: a `profile` item "
                 "determined by two `part` assertions)"
                 % (indent, ", ".join(COMPOSITION_KINDS)))
    for kind, count, status in rows:
        lines.append("%s  %-14s %6d derived%s"
                     % (indent, kind, count,
                        "  (never derived — the engine's counter abstains)"
                        if status != "answer" else ""))
    for name, entity, answer in probes:
        lines.append("%s  generate(%s)  %s%s"
                     % (indent, name, answer["status"].upper(),
                        "" if answer["status"] != "answer"
                        else "  %s  %d‰" % (tag_text(answer),
                                            answer["confidence"])))
    lines.append("%slineage ledger       %d generated item%s, %d cells%s"
                 % (indent, body["generated"], "" if body["generated"] == 1
                    else "s", body["cells"],
                    "" if not body["by_rung"]
                    else "  " + ", ".join("rung %d: %d" % (r, n)
                                          for r, n in body["by_rung"])))
    if body["generated"] == 0:
        lines.append("%sTHE READING CANNOT COMPOSE, and that is a property of the "
                     "reading and not of the layer: the two kinds the rule needs "
                     "are outside the three this shell emits, exactly as `origin` "
                     "is outside its set-once reading — the shell narrows and "
                     "never widens. The same engine composes 160 items on "
                     "corpora/l7compose (README-l7 §3)." % indent)
    return lines


def certainty_lines(seen, indent="  "):
    """Where every `‰` above came from: counted evidence, or a fall-through.

    A tally of the answers this report ACTUALLY rendered — `ask` records each one
    as it is handed over, so this is not a second pass that could disagree with
    the view above it.

    `iid 2`, armed at `[L6] [DOGFOOD]` and fired at `[L7] [ASCEND]`, asked for
    exactly this: *every permille this surface prints over generated content is a
    certainty nobody computed*, and *the 2026-08-02 census measured the blind
    spot — no key of the shell's reading is set-once, so every number the surface
    prints today is 1000 and a fall-through would be invisible in it.* It is
    invisible no longer: the generated case is unreachable under this reading
    (`generation_lines` above), and the residual it named turns out to cover the
    **whole surface** and not a corner of it, because the same `CERTAIN` is
    reached one branch earlier on every ordinary key.
    """
    total = len(seen)
    answered = [row for row in seen if row["status"] == "answer"]
    tally = {w: 0 for w in WARRANTS}
    for row in answered:
        tally[row["warrant"]] = tally.get(row["warrant"], 0) + 1
    tags = {}
    for row in answered:
        tags[row["tag"]] = tags.get(row["tag"], 0) + 1
    untagged_ops = sorted({row["op"] for row in answered
                           if row["tag"] == UNTAGGED})

    lines = ["", "certainty — where every ‰ above came from"]
    lines.append("%s%d answers read back through §7.1 while rendering this view; "
                 "%d abstained" % (indent, total, total - len(answered)))
    lines.append("%s  %-22s %6d   the engine COUNTED this answer's evidence "
                 "(a set-once chain, permille(1/d))"
                 % (indent, MEASURED, tally[MEASURED]))
    lines.append("%s  %-22s %6d   current/asof on a key this reading does not "
                 "call set-once: CERTAIN before the chain is looked at"
                 % (indent, NOT_SET_ONCE, tally[NOT_SET_ONCE]))
    lines.append("%s  %-22s %6d   an op Layer 6 attaches CERTAIN to by "
                 "construction — regenerated exactly, or abstained"
                 % (indent, NO_MODEL, tally[NO_MODEL]))
    lines.append("%s  %-22s %6d   a COMPOSED item: no chain, no claimant count, "
                 "no set-once status (README-l6 §4's residual)"
                 % (indent, NO_CHAIN, tally[NO_CHAIN]))
    if not tally[MEASURED]:
        lines.append("%sNOT ONE ‰ ABOVE IS MEASURED. Every number this surface "
                     "prints is CERTAIN by fall-through — the residual README-l6 "
                     "§4 named for a generated item, reached one branch earlier "
                     "on every ordinary key. README-l7 §4 leaves it OPEN and this "
                     "is what it looks like on real fuel." % indent)
    lines.append("%s§4.2 tags         %s"
                 % (indent, "  ".join("%s %d" % (tag, tags[tag])
                                      for tag in sorted(tags))))
    if untagged_ops:
        lines.append("%sUNTAGGED answers come from the diagnostic ops (%s). "
                     "§4.2.2 has no exception for a diagnostic, so read literally "
                     "each is an answer that scores 0 however correct it is; no "
                     "§5 L7 denominator contains a diagnostic query, so no gated "
                     "number moves. The surface names them rather than laundering "
                     "them into a kind."
                     % (indent, ", ".join(op for op in untagged_ops if op)))
    return lines


def report(state, origin, sessions, entities, records,
           refused=None, cues=(), all_questions=False, seen=None):
    """The consolidated view, as lines meant to be pasted into a preamble.

    `seen` is the collector every rendered answer is recorded in (`ask` above).
    A caller that passes its own list gets the exact rows the closing census
    tallied, which is how `t_generation.py` checks the census against the view
    rather than against a second replay.
    """
    lines = []
    seen = [] if seen is None else seen
    total = state.next_t
    summaries = [r for r in records if r["payload"].get("kind") == SUMMARY_KIND]
    declared = [r for r in records if r["payload"].get("kind") == INTENTION_KIND]
    lines.append("consolidated view — %s" % ", ".join(sorted(entities)))
    lines.append("  derived by core/layers/l7_generation.py (Layer 7) from "
                 "%d stored session summaries and %d declared intentions"
                 % (len(summaries), len(declared)))
    lines.append("  %d derived events, %d / %d work units, "
                 "nothing written back to the store"
                 % (total, state.occupancy, state.budget_cap))
    lines.append("  every ‰ below is the engine's own §7.2 confidence, derived "
                 "at read time from state it already held and never stored")
    lines.append("  every answer below carries its §4.2 provenance tag — `recall` "
                 "held, `derive` regenerated, `+generated` composed — because from "
                 "Layer 7 an untagged answer scores 0 however correct it is")
    if refused is not None:
        lines.append("  TRUNCATED — the budget refused an event of store t=%d; "
                     "everything below covers only what was admitted." % refused[0])

    shape = ask(state, {"op": "consolidation"}, seen)["value"]

    for name, entity in sorted(entities.items(), key=lambda kv: kv[1]):
        lines.append("")
        lines.append("per-project summary — %s (entity %d)" % (name, entity))
        profile = ask(state, {"op": "profile", "entity": entity}, seen)
        if profile["status"] != "answer":
            lines.append("  profile          ABSTAIN — the fold is no longer exact "
                         "(a chain of this entity was shed)")
        else:
            for kind in sorted(profile["value"]):
                count = ask(state, {"op": "count", "kind": kind}, seen)
                globally = count["value"] if count["status"] == "answer" else "n/a"
                lines.append("  %-16s %6d for this project, %s derived in all"
                             % (kind, profile["value"][kind], globally))
            lines.append("  fold             %d‰  tag %s — a fold is regenerated "
                         "exactly or abstained on, so there is nothing here for a "
                         "confidence to vary with (README-l6 §4)"
                         % (profile["confidence"], tag_text(profile)))
        lines.append("  derived schema   %d keys, %d pairs, %d assertions"
                     % (shape["keys"], shape["pairs"], shape["assertions"]))
        lines.append("  episodes held    %d of %d   demotions %d   damaged %d"
                     % (shape["episodes"], total, shape["demotions"],
                        shape["damaged"]))

        lines.append("")
        lines.append("decision history — the value in force, how sure of it, "
                     "what it is tagged, and where it changed")
        for key in ASSERTED_KEYS:
            now = current_fact(state, entity, key, origin, seen)
            if now is None:
                lines.append("  %-16s (never asserted)" % key)
                continue
            lines.append("  %-16s %-38s  %4d‰  %-8s since store t=%s"
                         % (key, _fmt(now[0], 38), now[2], now[3], now[1]))
            changes = collapse(history(state, entity, key, origin, total - 1, seen))
            if len(changes) > 1:
                # A step is annotated with its own as-of confidence only where
                # that confidence is not CERTAIN: the walk then shows exactly
                # where the chain stopped being sure of itself, and says nothing
                # everywhere else (README-l6 §1.4).
                lines.append("      %s" % "  ->  ".join(
                    "%s (t=%s%s)" % (_fmt(v, 24), st,
                                     "" if c == CERTAIN else ", %d‰" % c)
                    for st, v, _n, c in changes))

        lines.extend(calibration_lines(state, entity, origin, total - 1, seen=seen))
        lines.extend(provenance_lines(state, entity, origin, seen=seen))

        lines.append("")
        questions = history(state, entity, QUESTION_KEY, origin, total - 1, seen)
        silent = sum(1 for r in summaries if not r["payload"]["open_questions"])
        lines.append("open questions — aggregate over the whole store")
        lines.append("  recorded         %d across %d sessions  "
                     "(%d sessions recorded none)"
                     % (len(questions), len(sessions), silent))
        asked = current_fact(state, entity, "open_questions", origin, seen)
        if asked is not None:
            lines.append("  latest session   %s open at store t=%s  (%d‰, %s)"
                         % (asked[0], asked[1], asked[2], asked[3]))
        shown = questions if all_questions else [
            q for q in questions if sessions and q[0] == sessions[-1][0]]
        for store_t, text, _conf in shown:
            lines.append("    t=%-3s %s" % (store_t, _fmt(text, 88)))
        if not all_questions and len(shown) < len(questions):
            lines.append("    (%d earlier questions are in the chain — "
                         "`consolidate --questions` prints them all)"
                         % (len(questions) - len(shown)))

    if entities:
        lines.extend(generation_lines(state, entities, seen=seen))

    if declared:
        lines.append("")
        lines.append("prospection — the promises this store is keeping")
        lines.extend(prospection_lines(state, records, origin, seen=seen))

    lines.append("")
    lines.append("what the budget did")
    forgot = ask(state, {"op": "forgetting"}, seen)["value"]
    lines.append("  demotions        %d  (an episode a chain regenerates — "
                 "content kept, cue lost)" % shape["demotions"])
    if declared:
        # Both prospection tiers demote at the door, and after this store kept
        # its first promise the two are different events: an ARMED intention's
        # own `intend` event (the pending entry regenerates it) and a FIRED
        # intention's emitted event (the fired ledger does). Reporting only the
        # first would leave a demotion unattributed at a cap under no pressure
        # at all, which is how this line read before iid 1 fired.
        counts = ask(state, {"op": "prospection"}, seen)["value"]
        lines.append("    of which       ARMED INTENTIONS %d, FIRED EVENTS %d — "
                     "released at the door because the pending set and the "
                     "fired ledger regenerate them (README-l5 §1.3), not pressure"
                     % (counts["pending"], counts["fired"]))
    lines.append("  forgotten        %d events, importance mass %d  (gone)"
                 % (forgot["count"], forgot["mass"]))

    whole = channels(state, seen=seen)
    lines.append("  content channel  read(t) answers for %d of %d derived events "
                 "— %d still episodes, %d regenerated from the chains"
                 % (whole["held"] + whole["derived"], total,
                    whole["held"], whole["derived"]))
    lines.append("  cue channel      recall reaches at most the %d held episodes; "
                 "the %d regenerated events have no posting"
                 % (whole["held"], whole["derived"]))

    entity = min(entities.values()) if entities else 1
    reach = reachability(state, records, sessions, entity, origin, seen)
    summary_ts = [s[1] for s in sessions]
    summary = channels(state, summary_ts, seen)
    readable = sum(1 for r in reach if r["readable"])
    recallable = sum(1 for r in reach if r["recallable"])
    lines.append("  session summaries  %d of %d readable, %d reachable by cue, "
                 "%d demoted" % (readable, len(reach), recallable,
                                 summary["derived"]))
    lost = [r["store_t"] for r in reach if not r["recallable"]]
    if lost:
        lines.append("    unreachable by cue: store t=%s"
                     % " ".join(str(x) for x in lost))

    for raw in cues:
        tokens = raw.split()
        cue = ev.cue_payload(tokens)
        cue["entity"] = entity
        answer = ask(state, {"op": "recall", "cue": cue}, seen)
        if answer["status"] == "answer":
            hit = _store_t(origin, answer["value"]["t"])
            payload = answer["value"]["payload"]
            lines.append("  cue %-24s MATCH  %4d‰  %-8s store t=%s  %s"
                         % (raw, answer["confidence"], tag_text(answer), hit,
                            _fmt(payload.get("log_line", ""), 48)))
        else:
            lines.append("  cue %-24s ABSTAIN  %4d‰  %s"
                         % (raw, answer["confidence"], tag_text(answer)))

    lines.extend(certainty_lines(seen))
    return lines

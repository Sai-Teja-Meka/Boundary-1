"""shell/dogfood/consolidate.py — the store's derived view, at Layer 4.

`[L4] [DOGFOOD]`. `remember` writes episodes and `recall` finds one of them.
This module answers the third question a memory owes its owner — *what does all
of it add up to?* — by folding the store's session summaries through
`core/layers/l4_consolidation.py` and reading the result back through the
**ordinary query interface** (§7.1): `current`, `asof`, `profile`, `count`,
`consolidation`, `forgetting`, `recall`, `read`. The shell computes no answer of
its own; it asks, labels, and formats.

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
"""

from core.layers import l4_consolidation as l4
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


def project_entities(records):
    """`{project: entity id}` in first-appearance order, from 1.

    Integer ids are the engine's requirement, not a choice: `facet` refuses a
    non-integer entity and `_actor` will not attribute an episode to one. The
    order is the store's own ingestion order, so the mapping is a function of
    the store and is stable for as long as the store only grows.
    """
    out = {}
    for record in records:
        name = record["payload"]["project"]
        if name not in out:
            out[name] = len(out) + 1
    return out


# ---- the derived state ------------------------------------------------------

def derive(records, budget_cap=DERIVED_BUDGET):
    """Fold the store's episodes into a Layer-4 state.

    Returns `(state, origin, sessions, entities, refused)`:

      * `origin[replay_t]` — the store `t` the derived event came from;
      * `sessions` — `[(store_t, summary_replay_t, last_replay_t)]` in order, so
        a report can ask `asof` at the instant a session ended;
      * `entities` — the `{project: entity}` mapping the reading used;
      * `refused` — `(store_t, payload)` of the first write the budget refused,
        or `None`.

    A refusal is surfaced, never swallowed: an event the budget cannot admit
    stops the replay and is reported as such, because a view built from a
    truncated stream that says so is honest and one that does not is a lie.
    """
    entities = project_entities(records)
    state = l4.make_engine(l4.LAYER, budget_cap=budget_cap)
    origin = []
    sessions = []
    refused = None
    for record in records:
        payload = record["payload"]
        entity = entities[payload["project"]]
        first = state.next_t
        for derived in session_stream(payload, entity):
            state, t = l4.write(state, derived)
            if t is None:
                refused = (record["t"], derived)
                break
            origin.append(record["t"])
        if refused is not None:
            break
        sessions.append((record["t"], first, state.next_t - 1))
    return state, origin, sessions, entities, refused


# ---- reading the state back, only through query() ---------------------------

def ask(state, q):
    """One query through the generic interface (§7.1). Never raises (§7.3)."""
    return l4.query(state, q)


def _store_t(origin, replay_t):
    if replay_t is None or replay_t < 0 or replay_t >= len(origin):
        return None
    return origin[replay_t]


def current_fact(state, entity, key, origin):
    """`(value, store_t)` for `(entity, key)` now, or `None` if never asserted."""
    answer = ask(state, {"op": "current", "entity": entity, "key": key})
    if answer["status"] != "answer":
        return None
    support = answer["provenance"]["support"]
    return answer["value"], _store_t(origin, support[0] if support else None)


def history(state, entity, key, origin, upto):
    """The whole chain for `(entity, key)`, as `[(store_t, value)]`.

    Reconstructed by walking `asof` forward and reading each answer's own
    provenance `support` — the assertion the engine says carries the value. No
    engine internals are touched: the history is the sequence of *distinct
    supports* the ordinary as-of query reports across the stream.
    """
    out = []
    seen = set()
    for t in range(upto + 1):
        answer = ask(state, {"op": "asof", "entity": entity, "key": key, "t": t})
        if answer["status"] != "answer":
            continue
        support = answer["provenance"]["support"]
        stamp = support[0] if support else None
        if stamp is None or stamp in seen:
            continue
        seen.add(stamp)
        out.append((_store_t(origin, stamp), answer["value"]))
    return out


def collapse(chain):
    """`[(store_t, value, restatements)]` — consecutive equal values folded.

    A session asserts the project's whole state every time, so most assertions
    restate the value already in force. The chain keeps them all (they are what
    `asof` walks); a *history* is the sequence of **changes**, so the display
    folds a run of equal values into the `t` it was first decided at and counts
    the restatements rather than dropping them silently.
    """
    out = []
    for store_t, value in chain:
        if out and out[-1][1] == value and type(out[-1][1]) is type(value):
            out[-1][2] += 1
            continue
        out.append([store_t, value, 0])
    return [(t, v, n) for t, v, n in out]


def channels(state, ts=None):
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
        answer = ask(state, {"op": "read", "t": t})
        if answer["status"] != "answer":
            counts["gone"] += 1
        elif answer["provenance"]["kind"] == "recall":
            counts["held"] += 1
        else:
            counts["derived"] += 1
    return counts


def reachability(state, records, sessions, entity, origin):
    """Per session: is its episode still readable, and still reachable by cue?

    Two channels, asked separately because Layer 4 separates them: `read(t)` is
    content and `recall(cue)` is association, and `README-l4 §4` states that a
    demoted episode keeps the first and loses the second. The cue used is the
    session's own whole token bag, which no other session's bag contains unless
    it is a strict superset — an ambiguity the answer reports rather than hides.
    """
    out = []
    for (store_t, summary_t, _last), record in zip(sessions, records):
        payload = record["payload"]
        read = ask(state, {"op": "read", "t": summary_t})
        cue = {"entity": entity, "tok": dict(payload["tok"])}
        found = ask(state, {"op": "recall", "cue": cue})
        hit = None
        if found["status"] == "answer":
            hit = _store_t(origin, found["value"]["t"])
        out.append({"store_t": store_t,
                    "readable": read["status"] == "answer",
                    "recallable": found["status"] == "answer",
                    "recall_t": hit})
    return out


# ---- the report -------------------------------------------------------------

def _fmt(value, width=60):
    text = value if isinstance(value, str) else str(value)
    return text if len(text) <= width else text[:width - 1] + "…"


def report(state, origin, sessions, entities, records,
           refused=None, cues=(), all_questions=False):
    """The consolidated view, as lines meant to be pasted into a preamble."""
    lines = []
    total = state.next_t
    lines.append("consolidated view — %s" % ", ".join(sorted(entities)))
    lines.append("  derived by core/layers/l4_consolidation.py (Layer 4) from "
                 "%d stored session summaries" % len(records))
    lines.append("  %d derived events, %d / %d work units, "
                 "nothing written back to the store"
                 % (total, state.occupancy, state.budget_cap))
    if refused is not None:
        lines.append("  TRUNCATED — the budget refused an event of store t=%d; "
                     "everything below covers only what was admitted." % refused[0])

    shape = ask(state, {"op": "consolidation"})["value"]

    for name, entity in sorted(entities.items(), key=lambda kv: kv[1]):
        lines.append("")
        lines.append("per-project summary — %s (entity %d)" % (name, entity))
        profile = ask(state, {"op": "profile", "entity": entity})
        if profile["status"] != "answer":
            lines.append("  profile          ABSTAIN — the fold is no longer exact "
                         "(a chain of this entity was shed)")
        else:
            for kind in sorted(profile["value"]):
                count = ask(state, {"op": "count", "kind": kind})
                globally = count["value"] if count["status"] == "answer" else "n/a"
                lines.append("  %-16s %6d for this project, %s derived in all"
                             % (kind, profile["value"][kind], globally))
        lines.append("  derived schema   %d keys, %d pairs, %d assertions"
                     % (shape["keys"], shape["pairs"], shape["assertions"]))
        lines.append("  episodes held    %d of %d   demotions %d   damaged %d"
                     % (shape["episodes"], total, shape["demotions"],
                        shape["damaged"]))

        lines.append("")
        lines.append("decision history — the value in force, and where it changed")
        for key in ASSERTED_KEYS:
            now = current_fact(state, entity, key, origin)
            if now is None:
                lines.append("  %-16s (never asserted)" % key)
                continue
            value, decided = now
            lines.append("  %-16s %-38s  since store t=%s"
                         % (key, _fmt(value, 38), decided))
            changes = collapse(history(state, entity, key, origin, total - 1))
            if len(changes) > 1:
                lines.append("      %s" % "  ->  ".join(
                    "%s (t=%s)" % (_fmt(v, 24), st) for st, v, _n in changes))

        lines.append("")
        questions = history(state, entity, QUESTION_KEY, origin, total - 1)
        silent = sum(1 for r in records if not r["payload"]["open_questions"])
        lines.append("open questions — aggregate over the whole store")
        lines.append("  recorded         %d across %d sessions  "
                     "(%d sessions recorded none)"
                     % (len(questions), len(sessions), silent))
        asked = current_fact(state, entity, "open_questions", origin)
        if asked is not None:
            lines.append("  latest session   %s open at store t=%s"
                         % (asked[0], asked[1]))
        shown = questions if all_questions else [
            q for q in questions if sessions and q[0] == sessions[-1][0]]
        for store_t, text in shown:
            lines.append("    t=%-3s %s" % (store_t, _fmt(text, 88)))
        if not all_questions and len(shown) < len(questions):
            lines.append("    (%d earlier questions are in the chain — "
                         "`consolidate --questions` prints them all)"
                         % (len(questions) - len(shown)))

    lines.append("")
    lines.append("what the budget did")
    forgot = ask(state, {"op": "forgetting"})["value"]
    lines.append("  demotions        %d  (an episode a chain regenerates — "
                 "content kept, cue lost)" % shape["demotions"])
    lines.append("  forgotten        %d events, importance mass %d  (gone)"
                 % (forgot["count"], forgot["mass"]))

    whole = channels(state)
    lines.append("  content channel  read(t) answers for %d of %d derived events "
                 "— %d still episodes, %d regenerated from the chains"
                 % (whole["held"] + whole["derived"], total,
                    whole["held"], whole["derived"]))
    lines.append("  cue channel      recall reaches at most the %d held episodes; "
                 "the %d regenerated events have no posting"
                 % (whole["held"], whole["derived"]))

    entity = min(entities.values()) if entities else 1
    reach = reachability(state, records, sessions, entity, origin)
    summary_ts = [s[1] for s in sessions]
    summary = channels(state, summary_ts)
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
        answer = ask(state, {"op": "recall", "cue": cue})
        if answer["status"] == "answer":
            hit = _store_t(origin, answer["value"]["t"])
            payload = answer["value"]["payload"]
            lines.append("  cue %-24s MATCH  store t=%s  %s"
                         % (raw, hit, _fmt(payload.get("log_line", ""), 48)))
        else:
            lines.append("  cue %-24s ABSTAIN" % raw)
    return lines

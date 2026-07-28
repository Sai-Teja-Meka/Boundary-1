"""ops/l5 — the `corpora/l5stream` corpus properties the Layer-5 arithmetic rests on.

The byte-match law (§8.3) freezes this corpus's **bytes**. This file freezes what
the bytes are **for**, in the shape `ops/l4/t_l4stream.py` established: a
regeneration that stayed byte-identical while meaning something else would still
be caught here, and the figures `trials/ascension/l5/ATTAINABILITY.md` builds its
verdict on cannot drift without a red suite.

Five properties:

1. **The population is `l4stream`'s** — bounded, persistent, all spawned in the
   prelude, no dangling reference, no `retire`. The prospection stream is the
   consolidation world with one new kind, not a different world.
2. **The condition grammar is closed** — every atom draws its `p` from the six
   declared predicates, every connective from the three declared ones, every
   `kind`/`count_ge` kind from `KINDS`, and no AST is deeper than `MAX_COND_DEPTH`.
3. **Cascades are impossible by construction** — no fired payload of any
   intention in the stream satisfies any condition of any intention in it. This is
   the assertion the corpus's central promise rests on: with it, satisfaction
   points are a property of the frozen bytes; without it, they would depend on
   what an engine chose to emit.
4. **The three declared properties** — never-fires intentions, multiple
   satisfactions at one caller index, and conditions over demoted content — each
   against its `DECLARED_*` constant.
5. **The cost model** — per-kind event costs, so a change in `payload_cost` cannot
   silently move an attainability number.

Nothing here applies a gate to anything. `core/layers/l5_prospection.py` does not
exist.
"""

import collections

import _l5tasks
from _harness import require, require_equal
from core.state import event_cost
from corpora.l5stream import generator as l5gen


def _payloads():
    return list(l5gen.generate(l5gen.SEED, l5gen.N))


# ---- 1. the population is l4stream's -------------------------------------

def trial_l5stream_population_is_bounded_and_persistent():
    payloads = _payloads()
    require_equal(len(payloads), l5gen.N, "l5stream length drifted")

    spawns = [p for p in payloads if p["kind"] == "spawn"]
    require_equal(len(spawns), l5gen.ENTITIES,
                  "l5stream spawned an entity outside the prelude — the "
                  "never-fires band relies on `kind = spawn` being unsatisfiable "
                  "after the prelude, so a late spawn would silently convert a "
                  "declared never-fires intention into a firing one")
    require_equal([p["entity"] for p in spawns], list(range(1, l5gen.ENTITIES + 1)),
                  "the spawn prelude is not entities 1..ENTITIES in order")
    for i, p in enumerate(payloads[:l5gen.ENTITIES]):
        require_equal(p["kind"], "spawn",
                      "event %d is not part of the spawn prelude" % (i,))

    require(all(p["kind"] != "retire" for p in payloads),
            "l5stream contains a `retire` — the world is declared persistent")

    for p in payloads:
        for field in ("entity", "src", "dst"):
            who = p.get(field)
            if who is not None:
                require(1 <= who <= l5gen.ENTITIES,
                        "l5stream references entity %r outside [1, %d]"
                        % (who, l5gen.ENTITIES))
        if p["kind"] == "link":
            require(p["src"] != p["dst"], "a link relates an entity to itself")

    require_equal(sorted(set(p["kind"] for p in payloads)),
                  sorted(l5gen.KINDS),
                  "l5stream's kind vocabulary drifted from the closed set the "
                  "`kind` and `count_ge` predicates range over")


def trial_l5stream_ids_are_unique_across_notes_and_firings():
    payloads = _payloads()
    seen = collections.Counter()
    for p in payloads:
        if p["kind"] == "note":
            seen[p["text_id"]] += 1
        elif p["kind"] == "intend":
            seen[p["fire"]["text_id"]] += 1
    repeated = [tid for tid, c in seen.items() if c > 1]
    require(not repeated,
            "text_id %r occurs more than once across the note tier and the fired "
            "payloads — a firing is attributed to its intention BY its text_id, "
            "so a collision would make two firings indistinguishable"
            % (repeated[:3],))
    require_equal(sorted(seen), list(range(1, len(seen) + 1)),
                  "text_ids are not the contiguous global counter the grammar "
                  "declares")

    iids = [p["iid"] for p in payloads if p["kind"] == "intend"]
    require_equal(iids, list(range(1, len(iids) + 1)),
                  "iids are not the contiguous 1-based counter the grammar "
                  "declares — `iid` ascending is the declared firing order at a "
                  "caller index with several satisfactions (§2.3)")


# ---- 2. the condition grammar is closed ----------------------------------

def trial_l5stream_condition_grammar_is_closed():
    payloads = _payloads()
    conds = [p["cond"] for p in payloads if p["kind"] == "intend"]
    require_equal(len(conds), l5gen.DECLARED_INTENTIONS,
                  "l5stream's intention count drifted")

    seen_p = set()
    seen_op = set()
    for cond in conds:
        require(_l5tasks.depth(cond) <= l5gen.MAX_COND_DEPTH,
                "a condition AST is deeper than the declared bound of %d — the "
                "pending-set pricing in ATTAINABILITY.md is stated over this "
                "grammar, and an unbounded AST has no bounded cell cost"
                % (l5gen.MAX_COND_DEPTH,))
        _walk_ops(cond, seen_op)
        for atom in _l5tasks.atoms(cond):
            seen_p.add(atom["p"])
            require(atom["p"] in l5gen.PREDICATES,
                    "condition atom uses predicate %r, outside the closed "
                    "vocabulary %r" % (atom["p"], l5gen.PREDICATES))
            if atom["p"] == "count_ge":
                require(atom["k"] in l5gen.KINDS,
                        "count_ge names kind %r outside KINDS" % (atom["k"],))
            if atom["p"] == "kind":
                require(atom["v"] in l5gen.KINDS,
                        "a `kind` atom names %r outside KINDS — in particular it "
                        "must never name `fired`, which is what makes cascades "
                        "structurally impossible" % (atom["v"],))

    require_equal(sorted(seen_p), sorted(l5gen.PREDICATES),
                  "the frozen stream does not exercise every declared predicate "
                  "— a vocabulary entry no condition uses is a claim the corpus "
                  "does not support")
    require_equal(sorted(seen_op), sorted(l5gen.CONNECTIVES),
                  "the frozen stream does not exercise every declared connective")


def _walk_ops(cond, out):
    if "op" in cond:
        out.add(cond["op"])
        require(cond["op"] in l5gen.CONNECTIVES,
                "unknown connective %r" % (cond["op"],))
        require_equal(len(cond["args"]), 1 if cond["op"] == "not" else 2,
                      "connective %r has the wrong arity" % (cond["op"],))
        for a in cond["args"]:
            _walk_ops(a, out)


# ---- 3. cascades are impossible by construction ---------------------------

def trial_every_condition_is_guarded():
    """The INDUCTION half of the no-cascade argument (`grammar.md` GUARDEDNESS).

    The cross-product trial below checks the property on the 945 conditions this
    frozen instance happens to contain. This one checks the structural reason:
    every condition requires a payload atom on every satisfying assignment, so it
    is unsatisfiable by a payload no atom matches — a fired event, whatever the
    per-kind counts are and whatever a future instance of this generator emits.

    The first draft of the grammar failed exactly here: bare `not(kind = K)` and
    bare `count_ge` are both unguarded, and `iid 6` fired on a fired payload. The
    corpus was changed rather than the trial.
    """
    payloads = _payloads()
    for p in payloads:
        if p["kind"] != "intend":
            continue
        require(_l5tasks.guarded(p["cond"]),
                "intention %d's condition %r is UNGUARDED — some satisfying "
                "assignment needs no payload atom, so a payload the atoms cannot "
                "read (an engine's own fired event) can satisfy it, and the "
                "corpus could no longer state its satisfaction points"
                % (p["iid"], p["cond"]))

    # The induction is only sound if its base case holds: no payload atom is
    # satisfiable by a fired payload. Asserted over every atom in the stream.
    counts = collections.Counter(p["kind"] for p in payloads)
    fired = {"kind": "fired", "text_id": 1}
    for p in payloads:
        if p["kind"] != "intend":
            continue
        for atom in _l5tasks.atoms(p["cond"]):
            if atom["p"] not in l5gen.PAYLOAD_PREDICATES:
                continue
            require(not _l5tasks.satisfies(atom, fired, counts),
                    "payload atom %r holds on a fired payload — the base case of "
                    "the GUARDEDNESS induction fails and the whole no-cascade "
                    "argument with it" % (atom,))


def trial_no_fired_payload_can_satisfy_any_condition():
    """The corpus's central promise, asserted rather than argued.

    Satisfaction points are computable from the frozen bytes ONLY if an engine's
    own emissions cannot create new ones. The induction above says why that holds
    for any instance of this grammar; this says it holds for the instance that is
    actually frozen, over the whole cross product — 945 conditions × 945 fired
    payloads — because a structural argument and a frozen artifact are two
    different claims and this repository checks both.

    The counts passed to `count_ge` are the whole stream's, which is the most
    generous possible reading: if a fired payload cannot satisfy a condition even
    when every count is at its maximum, it cannot satisfy one at any point.
    """
    payloads = _payloads()
    intents = [p for p in payloads if p["kind"] == "intend"]
    counts = collections.Counter(p["kind"] for p in payloads)

    fired_payloads = [p["fire"] for p in intents]
    for p in fired_payloads:
        require_equal(sorted(p), ["kind", "text_id"],
                      "a fired payload has fields beyond {kind, text_id} — every "
                      "extra field is a surface an atom could match on")
        require_equal(p["kind"], "fired", "a fired payload is not of kind `fired`")
    require(l5gen.KINDS.count("fired") == 0,
            "`fired` entered KINDS — a `kind` or `count_ge` atom could then name "
            "it and a firing could cascade into another firing")

    # The cross product, with count_ge saturated.
    for intent in intents:
        for p in fired_payloads:
            require(not _l5tasks.satisfies(intent["cond"], p, counts),
                    "intention %d's condition %r is satisfied by the fired "
                    "payload %r — satisfaction points would then depend on what "
                    "an engine emitted, and this corpus could not state them"
                    % (intent["iid"], intent["cond"], p))


# ---- 4. the three declared properties -------------------------------------

def trial_l5stream_declared_properties_hold():
    b = _l5tasks.corpus()

    require_equal(len(b["intents"]), l5gen.DECLARED_INTENTIONS,
                  "l5stream's intention count drifted")
    require_equal(len(b["fireable"]), l5gen.DECLARED_FIREABLE,
                  "the fireable set drifted — it is the denominator of "
                  "trigger-recall")
    require_equal(len(b["never"]), l5gen.DECLARED_NEVER_FIRES,
                  "the never-fires tier drifted — without it, `abstain when "
                  "nothing satisfies it` is untested and trigger-precision can "
                  "be bought by firing eagerly")
    require(len(b["never"]) > 0,
            "l5stream has no never-fires intentions at all")

    multi = [k for k, v in b["by_index"].items() if len(v) > 1]
    require_equal(len(multi), l5gen.DECLARED_MULTI_SAT_INDICES,
                  "the number of caller indices satisfying more than one pending "
                  "intention drifted — exactly-once is a property of an "
                  "intention, not of an index")
    require_equal(max(len(v) for v in b["by_index"].values()),
                  l5gen.DECLARED_MAX_SAT_AT_INDEX,
                  "the largest fan-out at one caller index drifted")

    require_equal(len(_l5tasks.count_ge_conditions()),
                  l5gen.DECLARED_COUNT_GE_CONDITIONS,
                  "the number of conditions over demoted content drifted — this "
                  "is the property that makes Layer 5 stand on Layer 4 rather "
                  "than beside it")

    require_equal(_l5tasks.latency_profile()["next write"],
                  l5gen.DECLARED_FIRE_AT_NEXT_WRITE,
                  "the share of intentions whose satisfaction point is the very "
                  "next write drifted — it is exactly what a zero-knowledge "
                  "guess scores, and ATTAINABILITY.md's `fire-immediately` "
                  "baseline is that number")
    require(l5gen.DECLARED_FIRE_AT_NEXT_WRITE * 2 < l5gen.DECLARED_FIREABLE,
            "more than half the fireable intentions fire at the very next write "
            "— the corpus would then hand the gate to a policy that reads no "
            "condition at all")

    require_equal(b["peak_pending"], l5gen.DECLARED_PEAK_PENDING,
                  "the pending set's high-water mark drifted — it is what the "
                  "witness is priced at")
    require_equal(b["raw_cells"], l5gen.DECLARED_RAW_CELLS,
                  "l5stream's raw episodic footprint drifted under the §4.1 cost "
                  "model — every footprint permille in ATTAINABILITY.md is a "
                  "ratio against this number")


def trial_l5stream_layer4_view_is_as_declared():
    """The consolidation substrate this layer stands on, read by `_l4tasks`' own map.

    `l5stream` is NOT the corpus the ratified Layer-4 gate binds on (R4 clause 1
    binds that to `l4stream`) and no Layer-4 gate is applied here. What is
    asserted is only that the substrate's shape — what folds and what does not —
    is the declared one, because the witness in ATTAINABILITY.md is priced
    against it.
    """
    import _l4tasks
    b = _l4tasks.build("l5stream", _payloads())
    require_equal(b["assertions"], l5gen.DECLARED_ASSERTIONS,
                  "the assertion facet of l5stream drifted")
    require_equal(len(b["chains"]), l5gen.DECLARED_PAIRS,
                  "the (entity, key) pair count of l5stream drifted")
    require_equal(len(b["irreducible"]),
                  l5gen.DECLARED_NOTES + l5gen.DECLARED_INTENTIONS,
                  "the irreducible tier is not exactly the notes plus the "
                  "intentions — an `intend` that folded into an interval table "
                  "would be regenerable, and the pending set would be pricing "
                  "something the schema already held")
    for p in _payloads():
        if p["kind"] == "intend":
            require(_l4tasks.facet(p) is None,
                    "an `intend` payload produced a Layer-4 assertion facet")


# ---- 5. the cost model ----------------------------------------------------

def trial_l5stream_event_costs_are_the_frozen_model():
    """Per-kind costs, so a change in `payload_cost` cannot silently move a gate.

    `intend` is the one kind whose cost is not a single number: its condition AST
    varies. Its range is asserted instead, which is the honest form of the same
    check.
    """
    fixed = {"spawn": 7, "attr": 9, "move": 7, "link": 9, "note": 7}
    seen = {}
    for p in _payloads():
        seen.setdefault(p["kind"], set()).add(event_cost(p))
    for kind, want in sorted(fixed.items()):
        require_equal(sorted(seen[kind]), [want],
                      "l5stream %s events no longer cost %d cells under the "
                      "frozen §4.1 model" % (kind, want))
    require_equal(sorted(seen), sorted(l5gen.KINDS),
                  "l5stream's kind vocabulary drifted")

    require_equal(sorted(seen["intend"]), [15, 22, 24, 25],
                  "the cost spectrum of an `intend` event drifted — the "
                  "pending-set pricing in ATTAINABILITY.md is stated over this "
                  "grammar's condition ASTs, and there are exactly four distinct "
                  "AST shapes in the frozen stream")

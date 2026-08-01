"""shell/dogfood/intend.py — the promise, declared in the shell's own reading.

`[L5] [DOGFOOD]`. `remember` writes what a session did, `recall` finds one of
those events and `consolidate` says what all of them add up to. All three are
folds over the past. `intend` is the first thing this store does that faces the
other way: a **condition written now**, held, and evaluated against every session
summary written afterwards — and when one satisfies it, the engine emits the
payload the intention carried, once, at a logical time of its own
(`core/layers/README-l5.md`).

## The shell declares the reading; the engine keeps the promise

`§7.1` declares three operations and `§1.1` says events are the only fuel, so
`intend` is not a fourth verb here any more than it is in the engine: an
intention **is an ingested event**, written by the same `remember` write path
through the same budget law. What this module owns is the *reading* — and the
division of labour is exactly the one `consolidate.py` already draws:

    the shell   declares what a session summary asserts (entity, key, value),
                and therefore what a condition over future sessions may say;
    the engine  decides what arms, when it is satisfied, and fires it exactly
                once (`core/layers/l5_prospection.py`).

The stored payload is **the engine's own frozen `intend` form and nothing else**:

    {"kind":"intend","iid":<int>,"cond":<AST>,"fire":<payload>}

Not a shell schema translated later. `README-l5 §1.2` admits an intention only
when the payload rebuilds from `(iid, cond, fire)` as canonical bytes, so a
fourth field — a `tok` cue surface, a project name, a note about who declared it —
would stop it arming at all. The shell therefore adds nothing, and the price is
stated rather than hidden in `FIELD.md`: **a promise is `t`-addressable and not
cue-addressable.**

## The declared vocabulary, and why it is narrower than the engine's

The engine's condition grammar is six predicates and three connectives
(`corpora/l5stream/grammar.md`). This module admits a **strict subset**, and every
narrowing is a fact about what this store's own reading emits:

  * **`and` over atoms only** — no `or`, no `not`. `not` is what makes GUARDEDNESS
    a question in the corpus (a `not(kind=…)` is satisfied by an emitted event),
    and refusing it is how this reading makes cascades impossible **by
    construction** rather than by inspection.
  * **at least one guard atom** — `kind`, `entity` or `key`. Each is false for a
    `reminder`, so no payload this module can fire satisfies any condition it can
    admit (`guarded`, asserted by `trials/ops/dogfood/t_intend.py` over the whole
    cross product of declared conditions and declared fire payloads).
  * **`loc` is refused.** `consolidate.py`'s reading emits no `loc` field, so a
    `loc` condition is a promise that could never fire. The engine would hold it
    forever and be right to; the shell knows better and says so at declare time.
  * **`key` and `kind` and `count_ge`'s `k` are checked against the reading** —
    `ASSERTED_KEYS` + the open-question key, and the two kinds the derived stream
    contains. A condition over a key nothing writes is the same silent promise.

Everything admitted here is then handed to the engine's own `readable`, which is
the authority: the shell narrows, it never widens.
"""

from core.serialize import encode
from core.layers import l5_prospection as l5

from shell.dogfood import consolidate as co
from shell.dogfood import event as ev

# The engine's frozen kind for an intention, and the shell's kind for the payload
# it surfaces. `REMINDER_KIND` is deliberately NOT one of `DECLARED_KINDS`: that
# is half of what makes a fired event unable to satisfy a declared condition.
INTENTION_KIND = l5.INTENTION_KIND
REMINDER_KIND = "reminder"

# The kinds `consolidate.session_stream` emits into the derived stream.
DECLARED_KINDS = (ev.KIND, co.ASSERTION_KIND)

# The keys a session asserts about its project (`consolidate.ASSERTED_KEYS`),
# plus the append-log key its open questions ride.
DECLARED_KEYS = tuple(co.ASSERTED_KEYS) + (co.QUESTION_KEY,)

# The engine has six predicates; this reading admits five, and three of them can
# stand as the guard. `loc` is refused — see the module docstring.
DECLARED_PREDICATES = ("kind", "entity", "key", "val_ge", "count_ge")
GUARD_PREDICATES = ("kind", "entity", "key")

# Atoms are emitted in this order, so one declared condition has exactly one
# canonical encoding and two runs of the same flags produce the same bytes (§2.3).
_ATOM_ORDER = {p: i for i, p in enumerate(DECLARED_PREDICATES)}

FIRE_KEYS = ("kind", "about", "text")


# ---- building a condition ---------------------------------------------------

def atom(p, v, k=None):
    """One predicate atom in the frozen grammar's own shape."""
    out = {"p": p, "v": v}
    if k is not None:
        out["k"] = k
    return out


def condition(atoms):
    """`and` over the atoms, in declared order; a lone atom stays a bare atom.

    A bare atom is what `grammar.md` calls an atom condition, and the engine
    reads either. The ordering is the shell's, and it exists so that the same
    declaration always encodes to the same bytes.
    """
    ordered = sorted(atoms, key=lambda a: (_ATOM_ORDER.get(a.get("p"), 99),
                                           encode(a)))
    if len(ordered) == 1:
        return dict(ordered[0])
    return {"op": "and", "args": [dict(a) for a in ordered]}


def atoms_of(cond):
    """The atom list of a **declared** condition. Raises on anything else."""
    if not isinstance(cond, dict):
        raise ev.SchemaError("a condition must be an object, got %s"
                             % type(cond).__name__)
    if "op" in cond:
        if cond["op"] != "and":
            raise ev.SchemaError(
                "this reading admits `and` only, not %r: `or` and `not` are "
                "refused so that no fired payload can satisfy a declared "
                "condition (see the module docstring)" % (cond["op"],))
        args = cond.get("args")
        if not isinstance(args, list) or not args:
            raise ev.SchemaError("`and` must carry a non-empty `args` array")
        for arg in args:
            if not isinstance(arg, dict):
                raise ev.SchemaError("every conjunct must be an object")
            if "op" in arg:
                raise ev.SchemaError(
                    "this reading is a conjunction of ATOMS: a nested "
                    "connective is refused")
        return list(args)
    return [cond]


def validate_condition(cond):
    """Raise `ev.SchemaError` unless `cond` is a condition this reading declares.

    The shell narrows and the engine is the authority: every check below is about
    what `consolidate.py` actually emits, and the last one hands the result to
    `l5.readable`, which is the frozen definition of what can be armed at all.
    """
    atoms = atoms_of(cond)
    guards = 0
    for a in atoms:
        p = a.get("p")
        if p not in DECLARED_PREDICATES:
            raise ev.SchemaError(
                "predicate %r is not in this reading's vocabulary (%s); the "
                "engine's `loc` is refused because a session summary has no "
                "`loc` field, so such a promise could never fire"
                % (p, ", ".join(DECLARED_PREDICATES)))
        if "v" not in a:
            raise ev.SchemaError("atom %r carries no value" % (p,))
        v = a["v"]
        if p in GUARD_PREDICATES:
            guards += 1
        if p == "kind" and v not in DECLARED_KINDS:
            raise ev.SchemaError(
                "kind %r is not emitted by the declared reading (%s)"
                % (v, ", ".join(DECLARED_KINDS)))
        if p == "key" and v not in DECLARED_KEYS:
            raise ev.SchemaError(
                "key %r is not asserted by the declared reading (%s)"
                % (v, ", ".join(DECLARED_KEYS)))
        if p == "entity" and (not isinstance(v, int) or isinstance(v, bool)):
            raise ev.SchemaError("entity must be an integer (the project id)")
        if p in ("val_ge", "count_ge"):
            if not isinstance(v, int) or isinstance(v, bool):
                raise ev.SchemaError("%s must compare against an integer" % (p,))
        if p == "count_ge":
            k = a.get("k")
            if k not in DECLARED_KINDS:
                raise ev.SchemaError(
                    "count_ge counts a kind the reading emits (%s), not %r"
                    % (", ".join(DECLARED_KINDS), k))
    if not guards:
        raise ev.SchemaError(
            "a declared condition needs at least one guard atom (%s): without "
            "one, `count_ge` and `val_ge` say nothing about the arriving event "
            "and the promise is not guarded against what it fires"
            % ", ".join(GUARD_PREDICATES))
    if not l5.readable(cond):
        raise ev.SchemaError(
            "the engine cannot evaluate this condition, so it would not arm it "
            "(README-l5 §1.2: an engine arms only what it can evaluate)")
    return cond


# ---- the payload a promise surfaces ------------------------------------------

def reminder(about, text):
    """The fire payload: what this store surfaces when the condition is met."""
    if not isinstance(about, str) or not about.strip():
        raise ev.SchemaError("--about must be a non-empty string (what it is about)")
    if not isinstance(text, str) or not text.strip():
        raise ev.SchemaError("--surface must be a non-empty string (what to say)")
    return {"kind": REMINDER_KIND, "about": about, "text": text}


def guarded(fire):
    """Can this payload satisfy any condition this reading admits? (False = safe.)

    Structural, in the shape `grammar.md`'s *Cascades are impossible by
    construction* argument takes: a `reminder`'s kind is outside `DECLARED_KINDS`
    so no `kind` or `count_ge` atom reaches it; it carries no `entity` and no
    `src`, so `entity` is false; it has no Layer-4 facet, so `key` and `val_ge`
    are false; `loc` is not in the vocabulary. Every declared condition carries at
    least one guard atom, so every declared condition is false of it.
    """
    if not isinstance(fire, dict):
        return False
    if fire.get("kind") != REMINDER_KIND or REMINDER_KIND in DECLARED_KINDS:
        return False
    if sorted(fire) != sorted(FIRE_KEYS):
        return False
    return True


# ---- the event ---------------------------------------------------------------

def build_payload(iid, cond, fire):
    """Validate and return the stored intention payload — the engine's own form.

    The last check is the one that matters and it is the engine's, not the
    shell's: `l5.arms` returns `None` unless the condition is readable AND the
    payload rebuilds from `(iid, cond, fire)` as canonical bytes. A payload this
    function returns is one the engine will arm.
    """
    if not isinstance(iid, int) or isinstance(iid, bool) or iid < 1:
        raise ev.SchemaError("iid must be a positive integer")
    validate_condition(cond)
    if not guarded(fire):
        raise ev.SchemaError(
            "the fire payload must be a %r of exactly %s — a payload outside the "
            "declared reading could satisfy a declared condition"
            % (REMINDER_KIND, ", ".join(FIRE_KEYS)))
    payload = l5.rebuild_intention(iid, cond, fire)
    if l5.arms(payload) is None:
        raise ev.SchemaError(
            "the engine would not arm this payload (README-l5 §1.2: readable, "
            "invertible, and an `iid` it does not already know)")
    return payload


# ---- reading the store's own promises ----------------------------------------

def is_intention(payload):
    return isinstance(payload, dict) and payload.get("kind") == INTENTION_KIND


def intentions_of(records):
    """`[(store_t, payload)]` for every intention in the store, in ingest order."""
    return [(r["t"], r["payload"]) for r in records if is_intention(r["payload"])]


def next_iid(records):
    """The next free `iid`. §5 L5 names no re-arming, so an `iid` is spent forever."""
    used = [p["iid"] for _t, p in intentions_of(records)]
    return (max(used) + 1) if used else 1


def known_iids(records):
    return sorted(p["iid"] for _t, p in intentions_of(records))


# ---- rendering ---------------------------------------------------------------

# One describer, in `consolidate.py`, because a report of an old promise must not
# depend on the vocabulary that is current when it is read (`describe_condition`
# is generic over the frozen grammar; this reading is narrower than that).
describe_condition = co.describe_condition
describe_fire = co.describe_fire

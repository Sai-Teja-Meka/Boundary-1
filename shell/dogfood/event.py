"""shell/dogfood/event.py — the session-summary event schema (DOGFOOD).

One remembered event is one **session summary**. The schema follows the
`corpora/sessions` grammar's shape — a `kind`-tagged flat object whose atoms are
integers and strings only (§1.2, §2.4) — with the session-summary fields:

    {"kind": "session_summary",
     "project":        <str>,          # which project the session belonged to
     "move":           <str>,          # the single move executed (§9.1)
     "decisions":      [<str>, ...],   # what was decided
     "files_touched":  [<str>, ...],   # what it wrote
     "open_questions": [<str>, ...],   # what it left open
     "log_line":       <str>,          # the BOUNDARY.log line, verbatim
     "tok":            {<str>: 1, ...}}# the derived cue surface (below)

`t` is **not** in the payload: it is engine-assigned and engine-owned (§1.3).

## The cue surface (`tok`)

The Layer-2 index derives its atoms from payload fields (`core/layers/l2_recall.py`),
and `recall` answers only when one stored event contains the **whole** cue probe.
A free-token cue like `graphiti bitemporal` is therefore not expressible against
the prose fields directly — nothing in the payload is keyed by a bare word. So
the shell derives one: `tok` is the set of normalized tokens drawn from every
text field, stored as an **object with the constant value 1**.

Two consequences worth stating, because they shaped the schema:

  * It must be an object, not a list. The engine's flattener index-qualifies list
    items (`tok.0=graphiti`), which would make a cue position-dependent; an
    object gives the position-free atom `tok.graphiti=1`.
  * The value must be a constant, not a count. A cue carries `1`; if the event
    carried `3` the atoms would differ and the cue would miss. `tok` is a set.

A cue `{"tok": {"graphiti": 1, "bitemporal": 1}}` then means exactly what the
engine already implements: the conjunction of both atoms, answered only when one
event carries both. No engine change, no scoring in the shell.

Normalization is deterministic and library-free (no `re`, no stemmer): lowercase,
split on every character outside `[a-z0-9]`, keep runs of at least
`MIN_TOKEN_LEN`. It is the same function on both sides — ingest and cue — so
whatever a summary is searchable by is exactly what it was written with.
"""

KIND = "session_summary"

STR_FIELDS = ("project", "move", "log_line")
LIST_FIELDS = ("decisions", "files_touched", "open_questions")
SUMMARY_KEYS = frozenset(STR_FIELDS + LIST_FIELDS)
PAYLOAD_KEYS = frozenset(SUMMARY_KEYS | {"kind", "tok"})

# Text fields tokenized into the cue surface: everything a human wrote.
TOKEN_SOURCES = STR_FIELDS + LIST_FIELDS

# One-character tokens ("a", "3" out of "(a)" or "L3") carry no cue value and
# would only inflate the index; two is the shortest real token ("l1", "ga").
MIN_TOKEN_LEN = 2


class SchemaError(ValueError):
    """A session summary does not satisfy the schema above."""


# ---- token normalization (identical on ingest and on cue) ------------------

def tokenize(text):
    """Normalized tokens of one string: lowercase `[a-z0-9]+` runs, len >= 2.

    Deterministic and dependency-free. Every non-ASCII-alphanumeric character
    (punctuation, whitespace, `—`, `×`, `≥`) is a separator, so prose, paths and
    identifiers all tokenize by the same rule.
    """
    out = []
    cur = []
    for ch in text.lower():
        if ("a" <= ch <= "z") or ("0" <= ch <= "9"):
            cur.append(ch)
            continue
        if len(cur) >= MIN_TOKEN_LEN:
            out.append("".join(cur))
        cur = []
    if len(cur) >= MIN_TOKEN_LEN:
        out.append("".join(cur))
    return out


def token_bag(summary):
    """The `tok` object for a summary: `{token: 1}` over every text field."""
    bag = {}
    for field in TOKEN_SOURCES:
        value = summary[field]
        texts = [value] if isinstance(value, str) else value
        for text in texts:
            for tok in tokenize(text):
                bag[tok] = 1
    return bag


def cue_payload(tokens):
    """The engine cue for a list of raw cue tokens: `{"tok": {tok: 1, ...}}`.

    Normalized by the same `tokenize` used at ingest, so a cue token that
    normalizes away (a single character) simply does not appear in the probe.
    """
    bag = {}
    for raw in tokens:
        for tok in tokenize(raw):
            bag[tok] = 1
    return {"tok": bag}


# ---- schema ----------------------------------------------------------------

def validate_summary(summary):
    """Raise `SchemaError` unless `summary` is a well-formed session summary.

    Note what is deliberately NOT checked: `move` is validated as a non-empty
    string, not against the §9.1 move set. `BOUNDARY.log` already carries
    `FORGE-CORRECTION` and `THEORY`, which the move set does not list; a store
    that refused its own project's history would be the wrong kind of strict.
    """
    if not isinstance(summary, dict):
        raise SchemaError("summary must be an object, got %s" % type(summary).__name__)
    keys = frozenset(summary.keys())
    missing = sorted(SUMMARY_KEYS - keys)
    unknown = sorted(keys - SUMMARY_KEYS)
    if missing:
        raise SchemaError("summary is missing required fields: %s" % ", ".join(missing))
    if unknown:
        raise SchemaError("summary has unknown fields: %s" % ", ".join(unknown))

    for field in STR_FIELDS:
        value = summary[field]
        if not isinstance(value, str) or isinstance(value, bool):
            raise SchemaError("%s must be a string, got %s" % (field, type(value).__name__))
        if not value.strip():
            raise SchemaError("%s must not be empty" % (field,))

    for field in LIST_FIELDS:
        value = summary[field]
        if not isinstance(value, list):
            raise SchemaError("%s must be an array, got %s" % (field, type(value).__name__))
        for i, item in enumerate(value):
            if not isinstance(item, str) or isinstance(item, bool):
                raise SchemaError("%s[%d] must be a string, got %s"
                                  % (field, i, type(item).__name__))
            if not item.strip():
                raise SchemaError("%s[%d] must not be empty" % (field, i))
    return summary


def build_payload(summary):
    """Validate a session summary and return the canonical event payload.

    Pure: the caller's `summary` is never mutated and never aliased into the
    result (the engine copies again on write, but the shell does not rely on it).
    """
    validate_summary(summary)
    payload = {"kind": KIND}
    for field in STR_FIELDS:
        payload[field] = summary[field]
    for field in LIST_FIELDS:
        payload[field] = list(summary[field])
    payload["tok"] = token_bag(summary)
    return payload


def summary_of_payload(payload):
    """The session summary carried by a stored payload (the `tok` surface dropped)."""
    return {field: payload[field] for field in sorted(SUMMARY_KEYS)}

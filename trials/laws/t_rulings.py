"""laws/ — the ruling supplement and the authority of every gate a trial applies.

`BOUNDARY-RULINGS.md` is the frozen, append-only supplement created by the
`RULING` session, under the mechanism `BOUNDARY.md §5` itself anticipates when it
defers the Layer-8 and Layer-9 thresholds to a document written at the Phase 3→4
gate: **a frozen supplement may bind.** It never amends the constitution; it
settles questions the constitution leaves open — which corpus a stated gate binds
on, which reading of a ratified defense sentence the trials implement, and what
procedure binds future gates.

This is a **laws** trial rather than an ops one because what it guards is
*legality*, not capability (§6): a gate applied without authority is an illegal
gate regardless of what any engine scores against it, and a ledger that stops
being append-only has broken the discipline every layer above it rests on.

Three things are checked.

## 1. The supplement exists and is well-formed

Entry IDs are `R1, R2, …`, contiguous from 1, in order, never reused. Every entry
declares its frozen status and its holding. The header carries the append-only
declaration, because that declaration is what check 2 enforces.

## 2. The append-only ledgers are append-only, against git history

`BOUNDARY.md §9.2` and `CLAUDE.md §5`: old `BOUNDARY.log` lines are never
rewritten, and each `BOUNDARY-RULINGS.md` entry is frozen the moment it is
committed. Both are therefore **strictly append-only files**, and that is a
property git can settle rather than a promise a session makes to itself: every
committed version of each ledger must be a **byte-exact prefix** of the file on
disk now. An edited line, a deleted entry, a re-worded ruling — each breaks the
prefix and goes red.

`BOUNDARY-RULINGS.md` has **no** committed version on the commit that creates it,
so its check is vacuous exactly once. `BOUNDARY.log` is required to have at least
one, which is what keeps the mechanism demonstrably live: the same prefix walk
runs over a file with real history on every run, so a broken walk cannot hide
behind an empty set. This mirrors `t_l3streamb.py`'s use of `l3stream` to prove
its rank statistic is not vacuously satisfied.

Skips only when git itself is unavailable (a source export rather than a clone) —
never when the answer would be inconvenient.

## 3. Every gate a trial applies is authorized

The registry below names **every** gate threshold and humility ceiling any trial
applies, with the authority for each: a literal clause of the `BOUNDARY.md §5`
table, or a `BOUNDARY-RULINGS.md` entry, or both — thresholds come from §5, and a
ruling may bind a threshold to a corpus without touching it (R1). Three things
are then checked together, and the third is what gives the first two teeth:

  * the declared authority text **actually occurs** in the document claimed;
  * the declared value **equals** the constant in the trial source, read by `ast`
    from the file rather than by importing it;
  * **no constant escapes the registry** — every module-level `GATE_*` /
    `CEILING_*` integer anywhere under `trials/` must be declared here. A future
    session cannot introduce an unauthorized gate by writing one down, because
    writing one down is exactly what this check looks for.

The scope is stated honestly: this binds module-level gate constants, which is
the form every gate in the suite takes. A threshold buried as a literal inside a
function body would not be caught, and the remedy for that is the convention this
check enforces — gates are named constants, at module level, or they are not
gates.
"""

import ast
import os
import re
import subprocess

from _harness import PROJECT_ROOT, require, require_equal, skip

TRIALS_DIR = os.path.join(PROJECT_ROOT, "trials")
RULINGS_PATH = os.path.join(PROJECT_ROOT, "BOUNDARY-RULINGS.md")
BOUNDARY_PATH = os.path.join(PROJECT_ROOT, "BOUNDARY.md")

# The two strictly append-only ledgers, and whether history is required to exist.
# BOUNDARY.log must have committed versions: it is what proves the prefix walk is
# live rather than vacuously satisfied on an empty set.
LEDGERS = (("BOUNDARY.log", True), ("BOUNDARY-RULINGS.md", False))

CONST_PREFIXES = ("GATE_", "CEILING_")

ENTRY_HEADING = re.compile(r"^# (R\d+) — (.+)$", re.MULTILINE)


# --- the gate registry ------------------------------------------------------
# (trial file, constant, value, authorities, note). An authority is
# ("BOUNDARY.md", <clause>) or ("BOUNDARY-RULINGS.md", <entry id>); the clause
# must occur verbatim in that document.

def _s5(clause):
    return ("BOUNDARY.md", clause)


def _ruling(entry):
    return ("BOUNDARY-RULINGS.md", entry)


AUTHORIZED_GATES = (
    ("ascension/l1/t_retention.py", "GATE_F", 1000, (_s5("F=1000"),),
     "§5 L1 retention fidelity"),
    ("ascension/l1/t_retention.py", "GATE_C", 995, (_s5("C≥995"),),
     "§5 L1 coverage"),
    ("ascension/l1/t_retention.py", "GATE_B", 1000, (_s5("B=1000"),),
     "§5 L1 budget; §4.1 makes it absolute"),

    ("ascension/l2/t_recall.py", "GATE_CUE_C", 900, (_s5("cue-C≥900"),),
     "§5 L2 cue coverage"),
    ("ascension/l2/t_recall.py", "GATE_F", 950, (_s5("F≥950"),),
     "§5 L2 fidelity"),
    ("ascension/l2/t_recall.py", "GATE_B", 1000, (_s5("B=1000"),),
     "§5 L2 budget"),
    ("humility/l2/t_recall.py", "CEILING_CUE_C", 100,
     (_s5("capped cue-C ≤ 100"),), "§5 L2 humility ceiling"),

    ("ascension/l3/t_forgetting.py", "GATE_WEIGHTED_C", 850,
     (_s5("weighted-C≥850"), _ruling("R1")),
     "threshold from §5 L3, unchanged; R1 binds it to corpora/l3streamb"),
    ("ascension/l3/t_forgetting.py", "GATE_UNWEIGHTED_C", 90,
     (_s5("unweighted-C≥90"), _ruling("R1")),
     "threshold from §5 L3, unchanged; R1 binds it to corpora/l3streamb"),
    ("ascension/l3/t_forgetting.py", "GATE_F", 950,
     (_s5("F≥950"), _ruling("R3")),
     "threshold from §5 L3, unchanged; R3 settles the reading of F under eviction"),
    ("ascension/l3/t_forgetting.py", "GATE_B", 1000, (_s5("B=1000"),),
     "§5 L3 budget; binds on both streams whatever R1 says about coverage"),
    ("humility/l3/t_forgetting.py", "CEILING_WEIGHTED_C", 300,
     (_s5("capped weighted-C ≤ 300"),),
     "§5 L3 humility ceiling; no ruling reaches it"),

    # Layer 4. The ratified §5 L4 thresholds, unchanged, bound to
    # corpora/l4stream by R4 — the same shape as R1's Layer-3 binding: a ruling
    # binds a threshold to a corpus without touching it. R4 also settles the two
    # readings these constants are meaningless without (the footprint's unit, and
    # pricing rule P), which is why GATE_FOOTPRINT cites it and why every one of
    # them does. `t_attainability.py` names them to ask whether a corpus admits
    # them (R2 obligations 1 and 2); the Stage-B battery that applies them to an
    # engine is not written yet.
    ("ascension/l4/t_attainability.py", "GATE_FOOTPRINT", 250,
     (_s5("footprint≤250"), _ruling("R4")),
     "threshold from §5 L4, unchanged; R4 clause 2 reads it in permille of the "
     "raw episodic footprint and clause 3 prices the cells it counts"),
    ("ascension/l4/t_attainability.py", "GATE_RECONSTRUCTION_F", 900,
     (_s5("reconstruction F≥900"), _ruling("R4")),
     "threshold from §5 L4, unchanged; R4 clause 4 keeps it on the literal §3.0 "
     "table — R3 excludes L4 and no extension was taken"),
    ("ascension/l4/t_attainability.py", "GATE_C", 850,
     (_s5("C≥850"), _ruling("R4")),
     "threshold from §5 L4, unchanged; R4 clause 1 binds it to corpora/l4stream"),
    ("ascension/l4/t_attainability.py", "GATE_B", 1000,
     (_s5("B=1000"), _ruling("R4")),
     "§5 L4 budget; under R4 clause 2 the same number as the footprint cap, "
     "certified after every write rather than on the final state"),
    ("ascension/l4/t_attainability.py", "CEILING_RECONSTRUCTION_F", 400,
     (_s5("capped reconstruction F ≤ 400 at footprint≤250"), _ruling("R4")),
     "§5 L4 humility ceiling, unchanged; R4 binds the Layer-4 humility trial to "
     "corpora/l4stream, where the capped arithmetic bound is 325"),
)


# --- helpers ----------------------------------------------------------------

def _read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def _entries():
    """The ruling IDs and titles, in file order."""
    return ENTRY_HEADING.findall(_read_text(RULINGS_PATH))


def _git(*args):
    """Run a git command at the project root; return (returncode, stdout bytes)."""
    proc = subprocess.run(("git",) + args, cwd=PROJECT_ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout


def _module_gate_constants(path):
    """Module-level `GATE_*` / `CEILING_*` integers in one file, read by `ast`.

    Parsed, never imported: this must work on a trial module whose imports would
    fail, and it must read what the file *says* rather than what a run produces.
    """
    tree = ast.parse(_read_bytes(path), filename=path)
    found = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            if not target.id.startswith(CONST_PREFIXES):
                continue
            value = node.value
            require(isinstance(value, ast.Constant) and isinstance(value.value, int)
                    and not isinstance(value.value, bool),
                    "%s: gate constant %s is not an integer literal — a gate must "
                    "be a plain integer a human can read against §5"
                    % (os.path.relpath(path, TRIALS_DIR), target.id))
            found[target.id] = value.value
    return found


def _all_trial_files():
    paths = []
    for dirpath, _dirs, files in os.walk(TRIALS_DIR):
        for fname in sorted(files):
            if fname.endswith(".py"):
                paths.append(os.path.join(dirpath, fname))
    return sorted(paths)


# --- 1. the supplement exists and is well-formed ----------------------------

def trial_boundary_rulings_exists_and_is_well_formed():
    require(os.path.exists(RULINGS_PATH),
            "BOUNDARY-RULINGS.md is missing — the rulings the trials cite have no "
            "document to live in")
    text = _read_text(RULINGS_PATH)
    # Prose wraps; the declarations are matched on whitespace-normalized text so
    # a reflowed paragraph is not mistaken for a deleted promise.
    flat = " ".join(text.split())

    require("Append-only" in flat and "frozen the moment it is committed" in flat,
            "BOUNDARY-RULINGS.md no longer declares itself append-only and its "
            "entries frozen on commit — the declaration this law enforces")
    require("does not amend it and cannot" in flat,
            "BOUNDARY-RULINGS.md no longer states its subordination to "
            "BOUNDARY.md — a supplement that may amend the constitution is not a "
            "supplement, and BOUNDARY.md has no amendment mechanism")

    entries = _entries()
    require(len(entries) >= 3,
            "BOUNDARY-RULINGS.md holds %d entries; R1-R3 are cited by the Layer-3 "
            "trials and by this registry" % (len(entries),))
    for i, (entry_id, title) in enumerate(entries, start=1):
        require_equal(entry_id, "R%d" % i,
                      "ruling IDs must run contiguously from R1 in file order "
                      "(append-only: never renumbered, never reused)")
        require(title.strip() != "", "%s has an empty title" % (entry_id,))

    # Every entry declares that it is frozen, and what it holds.
    for entry_id, _title in entries:
        body = _entry_body(text, entry_id)
        require("**Status:** FROZEN on commit." in body,
                "%s does not declare its frozen status" % (entry_id,))
        require("**Holding:**" in body,
                "%s does not state a one-line holding" % (entry_id,))


def _entry_body(text, entry_id):
    """The text of one entry: from its heading to the next entry heading or EOF."""
    starts = [(m.group(1), m.start()) for m in ENTRY_HEADING.finditer(text)]
    for i, (found, pos) in enumerate(starts):
        if found != entry_id:
            continue
        end = starts[i + 1][1] if i + 1 < len(starts) else len(text)
        return text[pos:end]
    raise AssertionError("no entry %s in BOUNDARY-RULINGS.md" % (entry_id,))


# --- 2. append-only, against git history ------------------------------------

def trial_append_only_ledgers_are_append_only_in_git_history():
    if not os.path.isdir(os.path.join(PROJECT_ROOT, ".git")):
        skip("no .git directory — history cannot be checked from a source export")
    code, _out = _git("rev-parse", "--git-dir")
    if code != 0:
        skip("git is unavailable here; the append-only history check needs a clone")

    for name, history_required in LEDGERS:
        path = os.path.join(PROJECT_ROOT, name)
        require(os.path.exists(path), "append-only ledger missing: %s" % (name,))
        current = _read_bytes(path)

        code, out = _git("log", "--format=%H", "--", name)
        require(code == 0, "git log failed for %s" % (name,))
        shas = out.decode("ascii").split()

        if history_required:
            require(len(shas) > 0,
                    "%s has no committed history — the prefix walk below would "
                    "pass vacuously, and this ledger is what proves it does not"
                    % (name,))

        for sha in shas:
            code, blob = _git("show", "%s:%s" % (sha, name))
            require(code == 0, "git show failed for %s at %s" % (name, sha[:12]))
            require(current.startswith(blob),
                    "%s is NOT append-only: the version committed at %s (%d bytes) "
                    "is not a byte-exact prefix of the current file (%d bytes) — "
                    "something already written was rewritten or removed "
                    "(BOUNDARY.md §9.2, CLAUDE.md §5)"
                    % (name, sha[:12], len(blob), len(current)))


# --- 3. every gate a trial applies is authorized ----------------------------

def trial_every_gate_binding_matches_section5_or_a_ruling():
    boundary = _read_text(BOUNDARY_PATH)
    rulings = _read_text(RULINGS_PATH)
    ruling_ids = set(entry_id for entry_id, _title in _entries())
    documents = {"BOUNDARY.md": boundary, "BOUNDARY-RULINGS.md": rulings}

    for rel, const, value, authorities, note in AUTHORIZED_GATES:
        path = os.path.join(TRIALS_DIR, rel)
        require(os.path.exists(path),
                "registry names a trial file that does not exist: %s" % (rel,))
        actual = _module_gate_constants(path).get(const)
        require(actual is not None,
                "%s no longer defines %s — the registry entry authorizing it is "
                "stale, and a gate must not lose its recorded authority silently"
                % (rel, const))
        require_equal(actual, value,
                      "%s::%s drifted from its authorized value (%s)"
                      % (rel, const, note))

        require(len(authorities) > 0,
                "%s::%s claims no authority at all" % (rel, const))
        for doc, clause in authorities:
            if doc == "BOUNDARY-RULINGS.md":
                require(clause in ruling_ids,
                        "%s::%s cites %s, which is not an entry in "
                        "BOUNDARY-RULINGS.md" % (rel, const, clause))
            require(clause in documents[doc],
                    "%s::%s claims authority %r from %s, but that text does not "
                    "occur there — the gate is applied without authority"
                    % (rel, const, clause, doc))


def trial_no_trial_applies_an_undeclared_gate():
    """Completeness: no `GATE_*` / `CEILING_*` constant escapes the registry.

    Without this, the registry would authorize only what it already knows about
    and a new unauthorized gate could simply not be listed. With it, declaring a
    gate constant is what makes it discoverable, so the only way to add a gate is
    to give it an authority.
    """
    declared = set((rel, const) for rel, const, _v, _a, _n in AUTHORIZED_GATES)
    undeclared = []
    for path in _all_trial_files():
        rel = os.path.relpath(path, TRIALS_DIR).replace(os.sep, "/")
        for const, value in sorted(_module_gate_constants(path).items()):
            if (rel, const) not in declared:
                undeclared.append("%s::%s = %d" % (rel, const, value))
    require(not undeclared,
            "these gate constants are applied by trials but authorized by "
            "nothing — add each to AUTHORIZED_GATES with its §5 clause or its "
            "BOUNDARY-RULINGS.md entry: %s" % ", ".join(undeclared))

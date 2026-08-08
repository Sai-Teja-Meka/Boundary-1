"""laws/ — `BOUNDARY-HIGH.md`: the structural law for Layers 8 and 9, and its
NO-NUMBER property, enforced mechanically.

`BOUNDARY.md §5` defers the Layer-8 and Layer-9 thresholds to a document written
at the Phase 3→4 gate, and `BOUNDARY-RULINGS.md`'s preamble names it — *"call it
`BOUNDARY-HIGH.md`"*. `[L7] [ASCEND-SPEC]` wrote it. It settles the measures,
the substrate doctrine, the humility construction, two law seams and the
schedule, and **declares no threshold at all**: `R2` binds it in its own text
(*"at every layer, including `BOUNDARY-HIGH.md` when it is written"*) and
requires a gate's discrimination arithmetic recorded **before** the gate binds,
so a number written there — with no artifact, no measure and no baseline behind
it — would be the discrimination failure `R2` exists to forbid, committed in the
act of scheduling the gate.

This is a **laws** trial and not an `ops` one for the reason `t_rulings.py` gives
for itself (§6): what it guards is *legality*, not capability. A threshold
applied without authority is an illegal threshold whatever an engine scores
against it, and a canon-grade document that stopped being append-only would break
the discipline every layer above it will rest on.

Four things are checked.

## 1. The document exists and is well-formed

Its status block, its subordination to `BOUNDARY.md` (a supplement that could
amend the constitution is not a supplement, and `BOUNDARY.md` has no amendment
mechanism), its append-only declaration — which is what check 3 enforces — and
the sections its own schedule refers to.

## 2. The committed hash is pinned

`SPEC_SHA256` is the file's hash at the commit that froze it. A change to the
document is **red unless the same commit changes the pin**, which is exactly the
point: `§6.2` there says an amendment is a later ruling's job, and a pin that can
only move in a commit carrying that ruling is what makes an amendment visible
rather than quiet.

## 3. Append-only, against git history

The same walk `t_rulings.py` runs over `BOUNDARY.log` and `BOUNDARY-RULINGS.md`:
every committed version of the file must be a **byte-exact prefix** of the file
on disk now. It is vacuous exactly once — on the commit that creates the file —
exactly as `BOUNDARY-RULINGS.md`'s was, and the two checks together give the
document its discipline: **appends only, and each append re-pins the hash under a
ruling.**

Skips only when git itself is unavailable (a source export rather than a clone) —
never when the answer would be inconvenient.

## 4. The NO-NUMBER property

`BOUNDARY-HIGH.md §0` states it as a property that can be checked rather than
trusted, and this is the check. Two halves:

  * **in the document** — every cell of every `threshold` column reads exactly
    `DEFERRED — Stage A + ruling` and carries **no digit**. The document is free
    to *cite* ratified numbers in its prose (`§5 L7`'s `F ≥ 950`, `R7` clause
    3(c)'s window) because citing is not declaring; what it may not do is put a
    number where a gate constant would live, and the threshold column is exactly
    that place;
  * **in the repository** — no Layer-8 or Layer-9 trial directory, engine file or
    adapter exists (`R2`'s standing step orders them after Stage A's arithmetic),
    and no gate constant cites this document or `§5`'s deferral cell as its
    authority. `t_rulings.py`'s registry is where a gate acquires an authority;
    a Layer-8 row appearing there before a ruling exists is a threshold that
    skipped the arithmetic.

The second half is the one with the mutation behind it: a session that wrote a
number into a threshold cell, or a `GATE_*` constant into a Layer-8 trial, would
turn a deferral into an authority in a diff that changes one token.

**One operational note, recorded because it cost this session a false red.**
Re-pinning replaces a 64-character hex with another, so a mutated copy of this
file has **exactly the same size** as the restored one; `run.py` loads trial
modules by path, and CPython will serve a cached `__pycache__/*.pyc` when size
and mtime-seconds both match. A mutation run that re-pins and restores inside one
second can therefore leave a stale bytecode cache that reports the mutated
constant against the restored file. It is a property of the loader and not of
this check — clear `__pycache__` after a mutation run, and read the red as *"the
pin the interpreter loaded"* rather than *"the pin in the file"*.

**This trial is written to be ADVANCED and not weakened.** When Layer 8's Stage A
runs, `trials/ascension/l8/` will exist and its absence assertion moves to a
presence assertion under a dated note, in the form `l6/t_attainability_b.py` and
`l7/t_attainability.py` each took three times — an inventory of where `R2`'s
order has got to, never a claim that is quietly dropped.
"""

import hashlib
import os
import subprocess

from _harness import PROJECT_ROOT, require, require_equal, skip

SPEC_NAME = "BOUNDARY-HIGH.md"
SPEC_PATH = os.path.join(PROJECT_ROOT, SPEC_NAME)
RULINGS_REGISTRY = os.path.join(PROJECT_ROOT, "trials", "laws", "t_rulings.py")

# The hash of the document at the commit that froze it. It moves only in a commit
# that also carries the ruling authorizing the change (BOUNDARY-HIGH.md §6.2).
SPEC_SHA256 = "013f85eae2dfe5f19ddfabbc9aa5bae250e7171f796679465489bf2b88f8e5b3"

# The one string a threshold cell may carry. No digit, by construction.
DEFERRAL_TOKEN = "DEFERRED — Stage A + ruling"

# The measure tables of §2: Layer 8's rows and Layer 9's rows. A document that
# lost its tables would satisfy "no cell carries a digit" vacuously, so the count
# is asserted too — not as a gate on the document's shape, but so the check
# cannot pass by having nothing left to check.
MIN_DEFERRED_CLAUSES = 12

# Sections the document's own schedule refers to. Named here so a section that
# disappeared would be caught by the document's own index rather than by a reader.
REQUIRED_SECTIONS = (
    "## §0. The ordering collision, and the resolution",
    "## §1. What binds at Layers 8 and 9 regardless of any threshold",
    "## §2. The measures, before the thresholds",
    "## §3. The substrate doctrine — what a Layer-8 artifact IS",
    "## §4. The humility axes",
    "## §5. The law seams",
    "## §6. The schedule",
    "## §7. What this document does not do",
    "## §8. Where this document is checked",
)

# The rulings that bind this document sight-unseen (BOUNDARY.log line 48): six
# holdings across these five entries — R2, R4 clause 5, R5 clauses 1-4, R7
# clause 3, R7 clauses 4-5, R8 clause 3. It acknowledges each by name; a document
# that dropped one would be applying a discipline it no longer says it is under.
BINDING_RULINGS = ("R2", "R4", "R5", "R7", "R8")

# R2's standing step orders every one of these after Stage A's arithmetic, and
# Stage A has not run. Each is an inventory line, advanced when the order does.
LAYER_8_9_ABSENT = (
    "trials/ascension/l8", "trials/ascension/l9",
    "trials/humility/l8", "trials/humility/l9",
    "trials/inheritance/l8", "trials/inheritance/l9",
    "trials/strain/l8", "trials/strain/l9",
    "trials/ops/l8", "trials/ops/l9",
    "trials/adapters/l8.py", "trials/adapters/l9.py",
)


# --- helpers ----------------------------------------------------------------

def _read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def _spec_text():
    return _read_bytes(SPEC_PATH).decode("utf-8")


def _git(*args):
    proc = subprocess.run(("git",) + args, cwd=PROJECT_ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout


def _table_rows(text):
    """Yield (line_number, cells) for every markdown table row in the document."""
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        yield number, cells


def _is_separator(cells):
    return all(set(cell) <= set("-: ") and cell for cell in cells)


def _threshold_cells(text):
    """Every cell under a column headed `threshold`, with its line number.

    The header row fixes the column index; the rows that follow are read at that
    index until a line that is not a table row. Separator rows are skipped.
    """
    found = []
    column = None
    for number, cells in _table_rows(text):
        lowered = [cell.lower() for cell in cells]
        if "threshold" in lowered:
            column = lowered.index("threshold")
            continue
        if column is None or _is_separator(cells):
            continue
        if len(cells) <= column:
            # A row narrower than its header: the table ended, or is malformed.
            column = None
            continue
        found.append((number, cells[column]))
    return found


# --- 1. the document exists and is well-formed ------------------------------

def trial_boundary_high_exists_and_is_well_formed():
    require(os.path.exists(SPEC_PATH),
            "%s is missing — `BOUNDARY.md §5` defers the Layer-8 and Layer-9 "
            "thresholds to it and `BOUNDARY-RULINGS.md`'s preamble names it"
            % (SPEC_NAME,))
    text = _spec_text()
    # Prose wraps; declarations are matched on whitespace-normalized text so a
    # reflowed paragraph is not mistaken for a deleted promise (the form
    # `t_rulings.py` established for the same job).
    flat = " ".join(text.split())

    require("**Status:** FROZEN on commit." in flat,
            "%s does not declare its frozen status" % (SPEC_NAME,))
    require("**Holding:**" in flat,
            "%s does not state a one-line holding" % (SPEC_NAME,))
    require("Append-only" in flat and "frozen the moment it is committed" in flat,
            "%s no longer declares itself append-only and frozen on commit — the "
            "declaration check 3 enforces" % (SPEC_NAME,))
    require("does not amend it and cannot" in flat,
            "%s no longer states its subordination to BOUNDARY.md — a supplement "
            "that may amend the constitution is not a supplement, and "
            "BOUNDARY.md has no amendment mechanism" % (SPEC_NAME,))
    require("every threshold is deferred" in flat,
            "%s no longer states that every threshold is deferred, which is the "
            "holding this trial exists to keep true" % (SPEC_NAME,))

    for section in REQUIRED_SECTIONS:
        require(" ".join(section.split()) in flat,
                "%s no longer carries the section %r that its own schedule "
                "refers to" % (SPEC_NAME, section))

    for entry in BINDING_RULINGS:
        require("`%s`" % (entry,) in text,
                "%s does not acknowledge %s, which binds it sight-unseen "
                "(BOUNDARY.log line 48) — a document under a discipline it does "
                "not name is a document that will be read as though it were not"
                % (SPEC_NAME, entry))


# --- 2. the committed hash is pinned ----------------------------------------

def trial_the_committed_hash_of_the_spec_is_pinned():
    """The pin moves only in a commit that also carries the ruling.

    `BOUNDARY-HIGH.md §6.2`: the document is append-only from its commit and a
    later ruling supersedes a section **by saying so**. The pin is what makes
    that visible — an edit is red until the pin moves, and moving the pin is an
    edit to this file, in the same diff, where a reviewer sees it.
    """
    require(os.path.exists(SPEC_PATH), "%s is missing" % (SPEC_NAME,))
    actual = hashlib.sha256(_read_bytes(SPEC_PATH)).hexdigest()
    require_equal(actual, SPEC_SHA256,
                  "%s has changed since it was frozen. If that change is "
                  "authorized by a BOUNDARY-RULINGS.md entry, move the pin in "
                  "the same commit; if it is not, the document is a frozen "
                  "artifact under BOUNDARY.md §9.2 and the edit is not lawful"
                  % (SPEC_NAME,))


# --- 3. append-only, against git history ------------------------------------

def trial_the_spec_is_append_only_in_git_history():
    if not os.path.isdir(os.path.join(PROJECT_ROOT, ".git")):
        skip("no .git directory — history cannot be checked from a source export")
    code, _out = _git("rev-parse", "--git-dir")
    if code != 0:
        skip("git is unavailable here; the append-only history check needs a clone")

    current = _read_bytes(SPEC_PATH)
    code, out = _git("log", "--format=%H", "--", SPEC_NAME)
    require(code == 0, "git log failed for %s" % (SPEC_NAME,))
    for sha in out.decode("ascii").split():
        code, blob = _git("show", "%s:%s" % (sha, SPEC_NAME))
        require(code == 0, "git show failed for %s at %s" % (SPEC_NAME, sha[:12]))
        require(current.startswith(blob),
                "%s is NOT append-only: the version committed at %s (%d bytes) "
                "is not a byte-exact prefix of the current file (%d bytes) — "
                "something already written was rewritten or removed "
                "(BOUNDARY.md §9.2, CLAUDE.md §5)"
                % (SPEC_NAME, sha[:12], len(blob), len(current)))


# --- 4. the no-number property ----------------------------------------------

def trial_no_threshold_is_declared_in_the_spec():
    """Every `threshold` cell is the deferral token, and carries no digit.

    The document may **cite** ratified numbers in its prose — `§5 L7`'s
    `F ≥ 950`, `R7` clause 3(c)'s window, the measured `650` of the no-model
    class — because citing is not declaring. What it may not do is put a number
    where a gate constant would live, and a `threshold` column is exactly that
    place: it is the cell `BOUNDARY.md §5`'s own table fills for Layers 1–7 and
    leaves as *specified at Phase 3→4 gate* for these two.
    """
    text = _spec_text()
    cells = _threshold_cells(text)
    require(len(cells) >= MIN_DEFERRED_CLAUSES,
            "%s declares %d threshold cells; §2 states the measures for %d "
            "clauses-to-be, and a document that lost its tables would satisfy "
            "the no-digit check by having nothing left to check"
            % (SPEC_NAME, len(cells), MIN_DEFERRED_CLAUSES))
    for number, cell in cells:
        require(not any(ch.isdigit() for ch in cell),
                "%s line %d: a threshold cell carries a digit (%r). No number is "
                "declared in this document: R2 binds it in its own text and "
                "requires the discrimination arithmetic recorded BEFORE a gate "
                "binds, so a threshold written here — with no artifact, no "
                "measure and no baseline behind it — is a number in a table and "
                "not a test (R2 obligation 4)" % (SPEC_NAME, number, cell))
        require_equal(cell, DEFERRAL_TOKEN,
                      "%s line %d: a threshold cell does not read the deferral "
                      "token. Every one defers, in the same words, so that a "
                      "clause cannot lose its deferral by being phrased "
                      "differently" % (SPEC_NAME, number))


def trial_no_layer_8_or_9_gate_exists_anywhere():
    """`R2`'s order, as an inventory — advanced when the order advances.

    Stage A has not run, so no Layer-8 or Layer-9 trial directory, adapter or
    engine file exists; and no gate constant cites this document, or `§5`'s
    deferral cell, as its authority. `t_rulings.py`'s registry is where a gate
    acquires an authority, and a Layer-8 row appearing there before a ruling
    exists would be a threshold that skipped the arithmetic.

    When Stage A runs, the absences below move to presences under a dated note,
    in the form `l6/t_attainability_b.py` and `l7/t_attainability.py` each took —
    advanced one step, never weakened.
    """
    for rel in LAYER_8_9_ABSENT:
        path = os.path.join(PROJECT_ROOT, *rel.split("/"))
        require(not os.path.exists(path),
                "%s exists. R2's standing step orders trials and engine AFTER "
                "the attainability arithmetic, and no Layer-8 or Layer-9 Stage A "
                "has run — so this trial is where that inventory is kept and it "
                "is advanced by a session that takes the next step, under a "
                "dated note, rather than by one that quietly finds it stale"
                % (rel,))
    layers_dir = os.path.join(PROJECT_ROOT, "core", "layers")
    for fname in sorted(os.listdir(layers_dir)):
        require(not (fname.startswith("l8_") or fname.startswith("l9_")),
                "core/layers/%s exists — a Layer-8 or Layer-9 engine before its "
                "gate has an attainability arithmetic, which is the ordering R2 "
                "exists to forbid" % (fname,))

    registry = _read_bytes(RULINGS_REGISTRY).decode("utf-8")
    require(SPEC_NAME not in registry,
            "trials/laws/t_rulings.py cites %s. Thresholds do not live in that "
            "document and never will: BOUNDARY-HIGH.md §6.2 lands every deferred "
            "number in a BOUNDARY-RULINGS.md entry, where every other gate "
            "constant in this project carries its authority" % (SPEC_NAME,))
    require("specified at Phase 3→4 gate" not in registry,
            "trials/laws/t_rulings.py cites §5's Layer-8/Layer-9 deferral cell as "
            "the authority for a gate constant. That cell is the absence of a "
            "threshold, not one — a gate authorized by it is a gate authorized "
            "by nothing")

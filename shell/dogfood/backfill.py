"""shell/dogfood/backfill.py — turn `BOUNDARY.log` into session summaries.

The project's history becomes its memory's first contents. Every line of
`BOUNDARY.log` is one committed move, which is exactly one session, which is
exactly one remembered event — so the backfill is a parse, not an invention.

    python3 -m shell.dogfood.backfill            # print one JSON summary per line
    python3 -m shell.dogfood.backfill --count    # just how many lines parsed

It writes nothing: `remember` stays the only writer. The operator pipes each
line into it, so a backfilled event travels the same schema validation, the same
tokenizer, and the same budget law as a live one.

## What is derived, and how honestly

  * `log_line` — the log line **verbatim**. Nothing is derived from nothing.
  * `move` — the second bracketed token. Not checked against the §9.1 move set:
    the log itself carries `FORGE-CORRECTION` and `THEORY`, which that set does
    not list (see `event.validate_summary`).
  * `decisions` — the line body (its trailing `<suite: …> <anchors: …>` metadata
    removed) split on `;` at parenthesis depth 0. A log line is prose; this is a
    mechanical reading of it, and it is the weakest derivation here.
  * `files_touched` — the path-like tokens of the line: anything containing `/`
    or ending in a known extension, with `:LINENO` suffixes and surrounding
    punctuation stripped.
  * `open_questions` — **empty, always**. The log records what a session decided,
    never what it left open; inventing them retroactively would be fabrication.
    Only live sessions can fill this field.
"""

import json
import os
import sys

from shell.dogfood import store as st

PROJECT = "boundary-1-memory"
LOG_FILENAME = "BOUNDARY.log"

_EXTENSIONS = (".md", ".py", ".json", ".jsonl", ".log", ".txt")
_EDGE_PUNCTUATION = "`'\"(),;:<>[]{}|.*"


def log_path():
    return os.path.join(st.repo_root(), LOG_FILENAME)


# ---- parsing ---------------------------------------------------------------

def split_prefix(line):
    """`[L2] [ASCEND] rest` -> `("L2", "ASCEND", "rest")`; None if unparseable."""
    if not line.startswith("["):
        return None
    first = line.find("]")
    if first < 0:
        return None
    layer = line[1:first]
    remainder = line[first + 1:].lstrip()
    if not remainder.startswith("["):
        return None
    second = remainder.find("]")
    if second < 0:
        return None
    return layer, remainder[1:second], remainder[second + 1:].strip()


def strip_metadata(body):
    """Drop the trailing `<…>` groups (`<suite: …>`, `<anchors: …>`) from a body."""
    text = body.rstrip()
    while text.endswith(">"):
        opener = text.rfind("<")
        if opener < 0:
            break
        text = text[:opener].rstrip()
    return text


def split_clauses(body):
    """Split on `;` at parenthesis depth 0, so a `;` inside `(…)` stays put."""
    clauses = []
    depth = 0
    current = []
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = depth - 1 if depth > 0 else 0
        if ch == ";" and depth == 0:
            clauses.append("".join(current).strip())
            current = []
            continue
        current.append(ch)
    clauses.append("".join(current).strip())
    return [c for c in clauses if c]


def _looks_like_path(token):
    """A path is a token with a known extension, or a directory ending in `/`.

    Deliberately conservative: a bare slash is not enough, because the log writes
    prose lists with slashes too (`fidelity/coverage/budget/calibration`,
    `<suite: 37/37 green>`). This under-collects rather than inventing files.
    """
    return token.endswith(_EXTENSIONS) or token.endswith("/")


def extract_paths(line):
    """The path-like tokens of a log line, deduplicated and sorted."""
    found = set()
    for raw in line.split():
        token = raw.strip(_EDGE_PUNCTUATION)
        # a `file.py:217` source reference
        if ":" in token:
            head, _, tail = token.rpartition(":")
            if head and tail.isdigit():
                token = head
        token = token.strip(_EDGE_PUNCTUATION)
        if not token or not _looks_like_path(token):
            continue
        segments = token.split("/")
        if len(segments) > 1 and all(s.endswith(_EXTENSIONS) for s in segments):
            found.update(segments)          # `A.md/B.md/C.md` is a list, not a path
        else:
            found.add(token)
    return sorted(found)


def summary_of_line(line):
    """One `BOUNDARY.log` line -> one session summary (the `event.py` schema)."""
    parsed = split_prefix(line.strip())
    if parsed is None:
        return None
    _layer, move, body = parsed
    prose = strip_metadata(body)            # the line minus its <suite:…> metadata
    return {
        "project": PROJECT,
        "move": move,
        "decisions": split_clauses(prose),
        "files_touched": extract_paths(prose),
        "open_questions": [],               # never recoverable from the log
        "log_line": line.strip(),
    }


def summaries(text):
    """Every parseable line of a log's text, in order (t will follow line order)."""
    out = []
    for line in text.splitlines():
        if not line.strip():
            continue
        summary = summary_of_line(line)
        if summary is None:
            raise ValueError("unparseable BOUNDARY.log line: %r" % (line[:60],))
        out.append(summary)
    return out


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    with open(log_path(), "r", encoding="utf-8") as fh:
        parsed = summaries(fh.read())
    if "--count" in argv:
        print(len(parsed))
        return 0
    for summary in parsed:
        print(json.dumps(summary, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

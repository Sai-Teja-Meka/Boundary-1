"""shell/dogfood/cli.py — `python3 -m shell.dogfood`: remember / recall / status.

    remember   ingest one session summary; print the engine-assigned `t`
    recall     associative recall over the store from free cue tokens
    status     event count, budget occupancy, checksum, the last three events

Exit codes:

    0  success — including an **abstention**, which is a correct answer (§3.0)
    1  usage or schema error (nothing written)
    2  the state file failed its integrity check (nothing written, no re-init)
    3  the write was refused by the budget law (§4.1; nothing written)

Everything printed on stdout is the answer; everything on stderr is bookkeeping,
so `t=$(... remember ...)` is a legal thing to write.
"""

import argparse
import json
import sys

from core.layers import l2_recall as engine
from shell.dogfood import event as ev
from shell.dogfood import store as st

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_CORRUPT = 2
EXIT_REFUSED = 3

NEAREST_SHOWN = 5
LINE_WIDTH = 96


# ---- shared plumbing -------------------------------------------------------

def _fatal_corrupt(path, reason, err):
    """The corruption message. Loud, exact, and offering no re-initialization."""
    print("FATAL: the dogfood state file failed its integrity check.", file=err)
    print("  path:   %s" % st.display_path(path), file=err)
    print("  reason: %s" % reason, file=err)
    print("The Layer-1 checksum law fails loudly (README-l1): a store that does not",
          file=err)
    print("verify is never silently re-initialized, repaired, or ignored. Restore it",
          file=err)
    print("from git history (git checkout -- %s) or delete it deliberately."
          % st.display_path(path), file=err)
    return EXIT_CORRUPT


def _load(path, err, allow_create=False, out=None):
    """Load the store. Returns `(state, exit_code)`; state is None on failure."""
    try:
        return st.load(path), EXIT_OK
    except st.StoreMissing:
        if allow_create:
            print("no store at %s — initializing a new one (budget cap %d)"
                  % (st.display_path(path), st.DOGFOOD_BUDGET), file=err)
            return st.create_state(), EXIT_OK
        print("no store at %s — nothing has been remembered yet."
              % st.display_path(path), file=err)
        return None, EXIT_USAGE
    except st.StoreCorrupt as exc:
        return None, _fatal_corrupt(path, str(exc), err)


def _truncate(text, width=LINE_WIDTH):
    return text if len(text) <= width else text[:width - 1] + "…"


# ---- rendering -------------------------------------------------------------

def render_event(record, indent="  "):
    """One stored event, rendered to be pasted into a session preamble."""
    payload = record["payload"]
    lines = ["%st=%d  %s  (%s)" % (indent, record["t"], payload["move"], payload["project"])]
    lines.append("%s  log: %s" % (indent, payload["log_line"]))
    for field, label in (("decisions", "decisions"),
                         ("files_touched", "files"),
                         ("open_questions", "open questions")):
        items = payload[field]
        if not items:
            lines.append("%s  %s: (none recorded)" % (indent, label))
            continue
        lines.append("%s  %s:" % (indent, label))
        for item in items:
            lines.append("%s    - %s" % (indent, item))
    return lines


def render_recall(state, tokens, cue, answer):
    """The full `recall` output: a match, or an explicit, diagnosed abstention.

    Never empty silence. An abstention says which of the two honest Layer-2
    boundaries it hit — nothing carries the whole cue, or several things do — and
    shows the evidence for it, labelled as context rather than as an answer.
    """
    bag = cue["tok"]
    probe = sorted(bag)
    lines = ["memory-recall  cue: %s  (store: %d events)"
             % (" ".join(tokens), state.next_t)]
    if not probe:
        lines.append("ABSTAIN — the cue has no usable tokens (a token is an "
                     "[a-z0-9] run of length >= %d)." % ev.MIN_TOKEN_LEN)
        return lines
    lines.append("probe: %s" % " ".join(probe))

    if answer["status"] == "answer":
        record = answer["value"]
        prov = answer["provenance"]
        lines.append("MATCH  confidence=%d‰  provenance=%s support=%s"
                     % (answer["confidence"], prov["kind"], prov["support"]))
        lines.extend(render_event(record))
        return lines

    # Abstention. Diagnose it from the engine's own ranking: a single-token cue's
    # ranking IS that token's posting list, so the per-token document frequencies
    # and the full-match set are engine-derived, not re-implemented here.
    postings = {}
    for tok in probe:
        ranking = engine.recall_ranking(state, {"tok": {tok: 1}})
        postings[tok] = set(t for t, _score in ranking)

    absent = [tok for tok in probe if not postings[tok]]
    full = None
    for tok in probe:
        full = set(postings[tok]) if full is None else (full & postings[tok])
    full = sorted(full or ())

    if absent:
        lines.append("ABSTAIN — no stored event carries: %s" % " ".join(absent))
    elif not full:
        lines.append("ABSTAIN — every cue token is stored, but no single event "
                     "carries all %d together." % len(probe))
    else:
        lines.append("ABSTAIN — ambiguous: %d stored events carry the whole cue, "
                     "and Layer 2 answers only when exactly one does (README-l2)."
                     % len(full))

    lines.append("  df: %s" % "  ".join("%s=%d" % (tok, len(postings[tok])) for tok in probe))

    if full:
        lines.append("  the %d events carrying the whole cue (context, not an answer):"
                     % len(full))
        for t in full:
            lines.extend(render_event(engine.read(state, t), indent="    "))
    else:
        ranking = engine.recall_ranking(state, cue)[:NEAREST_SHOWN]
        if ranking:
            lines.append("  nearest by cue overlap (context, not an answer):")
            for t, _score in ranking:
                payload = engine.read(state, t)["payload"]
                hit = sorted(tok for tok in probe if tok in payload["tok"])
                lines.append("    t=%d  %s  [%s]"
                             % (t, _truncate(payload["log_line"], 64), " ".join(hit)))
        else:
            lines.append("  no stored event shares any atom with this cue.")
    return lines


def render_status(state, path):
    occ, cap = state.occupancy, state.budget_cap
    lines = [
        "store        %s" % st.display_path(path),
        "events       %d" % state.next_t,
        "budget       %d / %d work units used (%d‰ of cap)"
              % (occ, cap, st.permille(occ, cap)),
        "checksum     %s" % st.state_checksum(state),
        "file-sha256  %s" % st.file_checksum(path),
        "layer_cap    %d" % state.layer_cap,
    ]
    last = engine.read_range(state, state.next_t - 3, state.next_t - 1)
    if not last:
        lines.append("last three   (none — the store is empty)")
        return lines
    lines.append("last three")
    for record in last:
        payload = record["payload"]
        lines.append("  %s" % _truncate("t=%-3d %-16s %s"
                                        % (record["t"], payload["move"], payload["log_line"])))
    return lines


# ---- commands --------------------------------------------------------------

def _summary_from_args(args, err):
    """Build a session summary from `--json` (stdin or a file) or from flags."""
    source = args.json
    if source is None and not sys.stdin.isatty() and args.log_line is None:
        source = "-"                     # piped input with no flags: read it
    if source is not None:
        raw = sys.stdin.read() if source == "-" else open(source, "r", encoding="utf-8").read()
        try:
            return json.loads(raw)
        except ValueError as exc:
            print("usage: --json input is not valid JSON: %s" % exc, file=err)
            return None
    return {
        "project": args.project,
        "move": args.move if args.move is not None else "",
        "decisions": list(args.decision),
        "files_touched": list(args.file),
        "open_questions": list(args.question),
        "log_line": args.log_line if args.log_line is not None else "",
    }


def cmd_remember(args, out, err):
    summary = _summary_from_args(args, err)
    if summary is None:
        return EXIT_USAGE
    try:
        payload = ev.build_payload(summary)
    except ev.SchemaError as exc:
        print("usage: %s" % exc, file=err)
        return EXIT_USAGE

    state, code = _load(args.store, err, allow_create=True)
    if state is None:
        return code

    state, t = st.remember(state, payload)
    if t is None:
        print("REFUSED: this write would raise occupancy above the budget cap "
              "(%d used of %d) — the budget law refuses, it does not evict (§4.1)."
              % (state.occupancy, state.budget_cap), file=err)
        return EXIT_REFUSED

    st.save(args.store, state)
    print(t, file=out)
    print("remembered t=%d  (%s / %s)  store: %d events, %d/%d work units"
          % (t, payload["move"], payload["project"], state.next_t,
             state.occupancy, state.budget_cap), file=err)
    return EXIT_OK


def cmd_recall(args, out, err):
    state, code = _load(args.store, err)
    if state is None:
        return code
    cue = ev.cue_payload(args.tokens)
    answer = engine.recall(state, cue)
    for line in render_recall(state, args.tokens, cue, answer):
        print(line, file=out)
    return EXIT_OK


def cmd_status(args, out, err):
    state, code = _load(args.store, err)
    if state is None:
        return code
    for line in render_status(state, args.store):
        print(line, file=out)
    return EXIT_OK


# ---- entry point -----------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="python3 -m shell.dogfood",
        description="The dogfood memory of this project: remember / recall / status.")
    parser.add_argument("--store", default=st.default_store_path(),
                        help="state file (default: shell/dogfood/store/store.json)")
    subs = parser.add_subparsers(dest="command")

    remember = subs.add_parser("remember", help="ingest one session summary")
    remember.add_argument("--json", metavar="PATH",
                          help="read the summary as JSON from PATH ('-' for stdin)")
    remember.add_argument("--project", default="boundary-1-memory")
    remember.add_argument("--move")
    remember.add_argument("--decision", action="append", default=[])
    remember.add_argument("--file", action="append", default=[])
    remember.add_argument("--question", action="append", default=[])
    remember.add_argument("--log-line", dest="log_line")

    recall = subs.add_parser("recall", help="associative recall from cue tokens")
    recall.add_argument("tokens", nargs="+", metavar="TOKEN")

    subs.add_parser("status", help="event count, budget, checksum, last three")
    return parser


def main(argv=None, out=None, err=None):
    out = out if out is not None else sys.stdout
    err = err if err is not None else sys.stderr
    parser = build_parser()
    args = parser.parse_args(list(sys.argv[1:] if argv is None else argv))
    if args.command == "remember":
        return cmd_remember(args, out, err)
    if args.command == "recall":
        return cmd_recall(args, out, err)
    if args.command == "status":
        return cmd_status(args, out, err)
    parser.print_help(err)
    return EXIT_USAGE

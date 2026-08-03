"""shell/dogfood/cli.py — `python3 -m shell.dogfood`: remember / recall / intend / consolidate / status.

    remember     ingest one session summary; print the engine-assigned `t`
    recall       associative recall over the store from free cue tokens
    intend       declare a promise: a condition over future sessions, and what
                 to surface when one satisfies it
    consolidate  the store's Layer-7 derived view, for a session preamble
    status       event count, budget occupancy, checksum, the last three events

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
from shell.dogfood import consolidate as co
from shell.dogfood import event as ev
from shell.dogfood import intend as it
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

def render_intention(record, indent="  "):
    """One stored intention: what it watches, and what it will surface.

    An intention carries exactly the three fields the engine can invert
    (`README-l5 §1.2`), so there is no prose to render and nothing to truncate —
    the condition and the fire payload are the whole event.
    """
    payload = record["payload"]
    return ["%st=%d  INTEND iid=%s" % (indent, record["t"], payload.get("iid")),
            "%s  when:     %s" % (indent, co.describe_condition(payload.get("cond"))),
            "%s  surfaces: %s" % (indent, co.describe_fire(payload.get("fire")))]


def render_event(record, indent="  "):
    """One stored event, rendered to be pasted into a session preamble."""
    payload = record["payload"]
    if it.is_intention(payload):
        return render_intention(record, indent=indent)
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
        lines.append("ABSTAIN  confidence=%d‰ — the cue has no usable tokens (a "
                     "token is an [a-z0-9] run of length >= %d)."
                     % (answer["confidence"], ev.MIN_TOKEN_LEN))
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

    # The confidence of an abstention is the engine's own and it is 0 (§7.2's
    # `value: null` row): an abstention states no value, so there is no claim for
    # a confidence to be about. It is printed rather than omitted because a
    # surface that showed the number only when it was high would be reporting the
    # engine's certainty and hiding its silence.
    conf = answer["confidence"]
    if absent:
        lines.append("ABSTAIN  confidence=%d‰ — no stored event carries: %s"
                     % (conf, " ".join(absent)))
    elif not full:
        lines.append("ABSTAIN  confidence=%d‰ — every cue token is stored, but no "
                     "single event carries all %d together." % (conf, len(probe)))
    else:
        lines.append("ABSTAIN  confidence=%d‰ — ambiguous: %d stored events carry "
                     "the whole cue, and Layer 2 answers only when exactly one "
                     "does (README-l2)." % (conf, len(full)))

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
        if it.is_intention(payload):
            lines.append("  %s" % _truncate(
                "t=%-3d %-16s iid=%s  when %s"
                % (record["t"], "INTEND", payload.get("iid"),
                   co.describe_condition(payload.get("cond")))))
            continue
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


def promise_footer(state, indent="  "):
    """The promises the store is keeping, replayed on demand. `[]` when there are none.

    A firing has to reach its owner somewhere, and this repository does not get
    to invent a channel for it: `§7.1` returns it and the shell prints it. So
    `recall` and `consolidate` both end here, and nothing else in the shell
    produces prospection output.

    The replay is skipped entirely when no intention has been declared, so a
    store that has made no promises pays nothing for the surface existing.
    """
    records = engine.read_range(state, 0, state.next_t - 1)
    if not it.intentions_of(records):
        return []
    derived, origin, _sessions, _entities, refused = co.derive(records)
    lines = co.prospection_lines(derived, records, origin, indent=indent)
    if refused is not None:
        lines.append("%sthe derived replay was TRUNCATED at store t=%d"
                     % (indent, refused[0]))
    return lines


def cmd_recall(args, out, err):
    state, code = _load(args.store, err)
    if state is None:
        return code
    cue = ev.cue_payload(args.tokens)
    answer = engine.recall(state, cue)
    for line in render_recall(state, args.tokens, cue, answer):
        print(line, file=out)
    promises = promise_footer(state)
    if promises:
        print("promises (replayed through Layer 7; `consolidate` for the whole view)",
              file=out)
        for line in promises:
            print(line, file=out)
    return EXIT_OK


def _condition_from_args(args, entity, err):
    """The declared condition these flags name, or `None` with a usage message.

    The shell builds the AST; `intend.validate_condition` decides whether this
    reading admits it and `l5.readable` whether the engine could evaluate it at
    all. The `entity` atom is always present: it is the guard, and it is what
    makes the promise a promise about *this project* rather than about whatever
    the store fills up with later.
    """
    atoms = [it.atom("entity", entity)]
    if args.when_kind is not None:
        atoms.append(it.atom("kind", args.when_kind))
    if args.when_key is not None:
        atoms.append(it.atom("key", args.when_key))
    if args.when_val_ge is not None:
        atoms.append(it.atom("val_ge", args.when_val_ge))
    if args.when_count_ge is not None:
        raw = args.when_count_ge
        kind, sep, number = raw.partition(":")
        if not sep or not number.lstrip("-").isdigit():
            print("usage: --when-count-ge takes KIND:N (e.g. attr:250)", file=err)
            return None
        atoms.append(it.atom("count_ge", int(number), k=kind))
    if len(atoms) == 1:
        print("usage: an intention needs something to watch — give at least one "
              "of --when-kind / --when-key / --when-val-ge / --when-count-ge",
              file=err)
        return None
    return it.condition(atoms)


def cmd_intend(args, out, err):
    """Declare a promise: write the intention as an event, then check it armed.

    The write path is `remember`'s — one store, one writer, one budget law. What
    is different is the last step: the shell replays the store through Layer 5
    and asks `§7.1` whether the intention is pending, because *the engine decides
    what arms* (`README-l5 §1.2`) and a shell that reported success without
    asking would be reporting its own intentions rather than the store's.
    """
    state, code = _load(args.store, err)
    if state is None:
        return code
    records = engine.read_range(state, 0, state.next_t - 1)

    entities = co.project_entities(records)
    if args.project not in entities:
        print("usage: no session of project %r is in the store, so the declared "
              "reading has no entity id for it; `remember` one first."
              % args.project, file=err)
        return EXIT_USAGE
    entity = entities[args.project]

    cond = _condition_from_args(args, entity, err)
    if cond is None:
        return EXIT_USAGE

    known = it.known_iids(records)
    iid = args.iid if args.iid is not None else it.next_iid(records)
    if iid in known:
        print("usage: iid %d is already declared (%s) — §5 L5 names no re-arming, "
              "so an iid is spent forever and the engine would arm nothing."
              % (iid, " ".join(str(i) for i in known)), file=err)
        return EXIT_USAGE

    try:
        payload = it.build_payload(iid, cond, it.reminder(args.about, args.surface))
    except ev.SchemaError as exc:
        print("usage: %s" % exc, file=err)
        return EXIT_USAGE

    preview = {"payload": payload, "t": state.next_t}
    if args.dry_run:
        for line in render_intention(preview):
            print(line, file=err)
        print("dry run — nothing written", file=err)
        return EXIT_OK

    state, t = st.remember(state, payload)
    if t is None:
        print("REFUSED: this write would raise occupancy above the budget cap "
              "(%d used of %d) — the budget law refuses, it does not evict (§4.1)."
              % (state.occupancy, state.budget_cap), file=err)
        return EXIT_REFUSED

    st.save(args.store, state)
    print(t, file=out)
    print("declared t=%d  iid=%d  store: %d events, %d/%d work units"
          % (t, iid, state.next_t, state.occupancy, state.budget_cap), file=err)
    for line in render_intention({"payload": payload, "t": t}):
        print(line, file=err)

    # The engine decides what arms; ask it rather than assume it (§7.1).
    for line in promise_footer(state):
        print(line, file=err)
    return EXIT_OK


def cmd_consolidate(args, out, err):
    """The derived view: fold the store through Layer 7, ask, and format.

    The fold is recomputed from the episodes every time and never written back
    (`consolidate.py`'s module docstring says why), so this command is read-only
    on the store — it opens the file, and nothing it derives can outlive the
    process. `--budget` replays the same episodes under a smaller cap, which is
    the only way to observe demotion on a store that is nowhere near its own.
    """
    state, code = _load(args.store, err)
    if state is None:
        return code
    records = engine.read_range(state, 0, state.next_t - 1)
    if not records:
        print("the store holds no session summaries yet — nothing to consolidate.",
              file=err)
        return EXIT_USAGE
    budget = args.budget if args.budget is not None else co.DERIVED_BUDGET
    if budget <= 0:
        print("usage: --budget must be a positive integer (§4.1)", file=err)
        return EXIT_USAGE
    derived, origin, sessions, entities, refused = co.derive(records, budget_cap=budget)
    for line in co.report(derived, origin, sessions, entities, records,
                          refused=refused, cues=args.cue,
                          all_questions=args.questions):
        print(line, file=out)
    print("derived %d events from %d stored events at a %d-unit cap"
          % (derived.next_t, len(records), budget), file=err)
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
        description="The dogfood memory of this project: "
                    "remember / recall / intend / consolidate / status.")
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

    intend = subs.add_parser(
        "intend", help="declare a promise over future sessions of this project")
    intend.add_argument("--project", default="boundary-1-memory",
                        help="the project the condition is about (its entity id "
                             "is read out of the store's own reading)")
    intend.add_argument("--when-kind", dest="when_kind", metavar="KIND",
                        help="the derived kind to watch (%s)"
                             % "/".join(it.DECLARED_KINDS))
    intend.add_argument("--when-key", dest="when_key", metavar="KEY",
                        help="the asserted key to watch (%s)"
                             % "/".join(it.DECLARED_KEYS))
    intend.add_argument("--when-val-ge", dest="when_val_ge", type=int,
                        metavar="N", help="fire when that key's value reaches N")
    intend.add_argument("--when-count-ge", dest="when_count_ge", metavar="KIND:N",
                        help="fire when N events of KIND have been derived — a "
                             "fold that outlives the episodes it counts")
    intend.add_argument("--surface", required=True, metavar="TEXT",
                        help="what to say when it fires")
    intend.add_argument("--about", required=True, metavar="WHAT",
                        help="what the reminder is about (a path, a document)")
    intend.add_argument("--iid", type=int,
                        help="the intention id (default: the next free one)")
    intend.add_argument("--dry-run", dest="dry_run", action="store_true",
                        help="validate and render it; write nothing")

    consolidate = subs.add_parser(
        "consolidate", help="the store's Layer-7 derived view of this project")
    consolidate.add_argument("--budget", type=int, metavar="UNITS",
                             help="replay the fold under a reduced cap "
                                  "(default %d) to observe demotion"
                                  % co.DERIVED_BUDGET)
    consolidate.add_argument("--cue", action="append", default=[], metavar="TOKENS",
                             help="probe the derived state with a cue "
                                  "(repeatable; quote multi-token cues)")
    consolidate.add_argument("--questions", action="store_true",
                             help="print every open question in the chain, not "
                                  "only the latest session's")

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
    if args.command == "intend":
        return cmd_intend(args, out, err)
    if args.command == "consolidate":
        return cmd_consolidate(args, out, err)
    if args.command == "status":
        return cmd_status(args, out, err)
    parser.print_help(err)
    return EXIT_USAGE

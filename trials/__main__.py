"""`python3 -m trials` — one command, one engine, the layered scorecard.

    python3 -m trials                          # our engine, the full ladder
    python3 -m trials --engine reference       # an external engine, same rows
    python3 -m trials --engine mem0            # a stub: prints why it cannot run
    python3 -m trials --engine ours --quick    # the declared reduced scale
    python3 -m trials --list-engines
    python3 -m trials --suite                  # exactly `python3 trials/run.py`

**`run.py` is still the one gate.** `--suite` does not re-implement it, wrap it
in a judgement, or add a threshold: it calls `run.main()` and returns its exit
code unchanged, so "green suite or nothing commits" (§9.3, `CLAUDE.md §3`) means
the same thing whichever way it is invoked. Everything else this entry point
does is *reporting* — the scorecard is a view of one engine, not a gate on it.

The four lines below are the only thing duplicated from `run.py`: the `sys.path`
bootstrap, which has to happen before `import run` can work at all. After that,
`run`'s loader, its discovery and its exit convention are used as they are.

Exit codes:

    0  the scorecard was produced (whatever it says), or the suite was green
    1  the suite was red, or the named engine cannot run here
    2  usage
"""

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))            # .../trials
_ROOT = os.path.dirname(_HERE)                                # repo root
for _p in (_HERE, _ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import run                                                     # noqa: E402
import scorecard                                               # noqa: E402


def build_parser():
    parser = argparse.ArgumentParser(
        prog="python3 -m trials",
        description="The memtrials layered scorecard. `run.py` is the gate; "
                    "this reports.")
    parser.add_argument("--engine", default=scorecard.OURS, metavar="NAME",
                        help="which engine to grade (default: ours). "
                             "`--list-engines` shows the set.")
    parser.add_argument("--quick", action="store_true",
                        help="the declared reduced scale (same batteries, "
                             "smaller corpora) — for a fast read, never for a "
                             "published number")
    parser.add_argument("--no-transfer", action="store_true",
                        help="omit the real-sessions transfer tier")
    parser.add_argument("--list-engines", action="store_true",
                        help="print the engines this command can grade")
    parser.add_argument("--suite", action="store_true",
                        help="run the full trial suite (exactly run.py) and "
                             "return its exit code")
    return parser


def main(argv=None, out=None, err=None):
    out = out if out is not None else sys.stdout
    err = err if err is not None else sys.stderr
    args = build_parser().parse_args(list(sys.argv[1:] if argv is None else argv))

    if args.suite:
        return run.main()

    if args.list_engines:
        from adapters import external
        print("engines:", file=out)
        print("  %-12s %-10s %s" % ("ours", "ours",
                                    "this repository's engine, one adapter per layer"),
              file=out)
        for name in external.names():
            module = external.get(name)
            ok, reason = module.available()
            print("  %-12s %-10s %s" % (name, module.KIND,
                                        "runnable" if ok else "NOT RUNNABLE"),
                  file=out)
            if not ok:
                print("  %-24s%s" % ("", reason), file=out)
        return 0

    if args.engine not in scorecard.engine_names():
        print("usage: no engine %r; known: %s"
              % (args.engine, ", ".join(scorecard.engine_names())), file=err)
        return 2

    engine, reason = scorecard.load_engine(args.engine)
    if engine is None:
        print("%s cannot be graded here: %s" % (args.engine, reason), file=err)
        print("Running an external system is a separate, human-supervised step "
              "(packaging/HONESTY.md). This session-safe command will not fetch "
              "a key or open a socket.", file=err)
        return 1

    card = scorecard.build(engine, quick=args.quick,
                           with_transfer=not args.no_transfer)
    for line in scorecard.render(card):
        print(line, file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

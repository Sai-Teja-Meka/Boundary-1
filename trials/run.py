#!/usr/bin/env python3
"""trials/run.py — the one gate. Runs every trial class; exit 0 iff all green.

Green suite (exit 0) or nothing commits (BOUNDARY.md §9.3, CLAUDE.md §3).

Discovery: for each trial class directory, import every `*.py` file that does
not start with `_`, find every top-level `trial_*` callable (sorted by name),
and run it. Outcomes: GREEN / SKIPPED-BY-DESIGN / RED (see _harness.py).

Exit code: 0 iff there are no RED trials. Skips are legal.
"""

import importlib.util
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))       # .../trials
ROOT = os.path.dirname(HERE)                            # repo root

# Both on sys.path so trials can import `_harness` and `corpora.*`.
for p in (HERE, ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

from _harness import SkipTrial  # noqa: E402

TRIAL_CLASSES = ("laws", "ops", "ascension", "humility", "strain", "anchors")

GREEN = "GREEN"
SKIP = "SKIPPED-BY-DESIGN"
RED = "RED"


def _load_module(path):
    name = "trial_" + os.path.relpath(path, ROOT).replace(os.sep, "_")[:-3]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _discover(klass_dir):
    """Yield (file_path, func_name, func) for every trial in a class dir."""
    if not os.path.isdir(klass_dir):
        return
    for fname in sorted(os.listdir(klass_dir)):
        if not fname.endswith(".py") or fname.startswith("_"):
            continue
        path = os.path.join(klass_dir, fname)
        module = _load_module(path)
        for attr in sorted(vars(module)):
            if attr.startswith("trial_"):
                fn = getattr(module, attr)
                if callable(fn):
                    yield path, attr, fn


def main():
    results = {GREEN: 0, SKIP: 0, RED: 0}
    red_details = []

    for klass in TRIAL_CLASSES:
        klass_dir = os.path.join(HERE, klass)
        printed_header = False
        for path, name, fn in _discover(klass_dir):
            if not printed_header:
                print(f"\n== {klass}/ ==")
                printed_header = True
            rel = os.path.relpath(path, HERE)
            label = f"{rel}::{name}"
            try:
                fn()
            except SkipTrial as e:
                results[SKIP] += 1
                print(f"  [SKIPPED-BY-DESIGN] {label}  ({e.reason})")
            except Exception as e:  # noqa: BLE001 — any failure is RED
                results[RED] += 1
                tb = traceback.format_exc()
                red_details.append((label, e, tb))
                print(f"  [RED]  {label}  ({type(e).__name__}: {e})")
            else:
                results[GREEN] += 1
                print(f"  [GREEN] {label}")

    total = results[GREEN] + results[SKIP] + results[RED]
    print("\n" + "=" * 60)
    print(f"trials: {total}   "
          f"green: {results[GREEN]}   "
          f"skipped-by-design: {results[SKIP]}   "
          f"red: {results[RED]}")

    if red_details:
        print("\n--- RED detail ---")
        for label, _e, tb in red_details:
            print(f"\n{label}:\n{tb}")
        print("SUITE RED")
        return 1

    print("SUITE GREEN")
    return 0


if __name__ == "__main__":
    sys.exit(main())

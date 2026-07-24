"""trials/_harness.py — shared helpers for every trial.

A trial is any top-level function named `trial_*` in a `*.py` file inside a
trial-class directory (laws/ ops/ ascension/ humility/ strain/ anchors/). It is
called with no arguments. Its outcome:

  - returns normally            -> GREEN
  - raises SkipTrial(reason)    -> SKIPPED-BY-DESIGN  (e.g. no engine yet)
  - raises anything else        -> RED

`run.py` puts both the project root and the trials/ directory on sys.path, so a
trial may `from _harness import ...` and `from corpora... import ...`.
"""

import os

HARNESS_DIR = os.path.dirname(os.path.abspath(__file__))   # .../trials
PROJECT_ROOT = os.path.dirname(HARNESS_DIR)                 # repo root
CORE_DIR = os.path.join(PROJECT_ROOT, "core")


class SkipTrial(Exception):
    """Raise to report SKIPPED-BY-DESIGN (a capability that does not exist yet)."""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def skip(reason):
    raise SkipTrial(reason)


def require(condition, message):
    """Assert a condition; a failure is a RED trial with `message`."""
    if not condition:
        raise AssertionError(message)


def require_equal(got, want, message="values differ"):
    if got != want:
        raise AssertionError(f"{message}: got {got!r}, want {want!r}")


def try_import(module_name, skip_reason):
    """Import a module or raise SkipTrial — for parametric, engine-gated trials."""
    try:
        __import__(module_name)
    except ImportError:
        raise SkipTrial(skip_reason)
    import importlib
    return importlib.import_module(module_name)

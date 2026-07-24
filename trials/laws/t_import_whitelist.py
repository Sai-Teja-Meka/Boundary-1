"""laws/ — the import-whitelist parser (BOUNDARY.md §2.5).

Two guarantees:
  1. core/WHITELIST agrees VERBATIM with the frozen list in BOUNDARY.md §2.5.
  2. Every import in every core/**/*.py resolves to a whitelisted top-level
     module (or to `core` itself / a relative import).

core/ has no engine yet, so (2) passes vacuously, but the parser runs now so the
first line of engine code is already governed.
"""

import ast
import os

from _harness import CORE_DIR, require, require_equal

# The frozen list, verbatim from BOUNDARY.md §2.5. This constant is the second
# witness; core/WHITELIST is the first. They must agree.
CONSTITUTION_WHITELIST = [
    "json", "fractions", "itertools", "functools",
    "collections", "hashlib", "math", "typing", "dataclasses",
]

WHITELIST_PATH = os.path.join(CORE_DIR, "WHITELIST")


def _parse_whitelist(path):
    mods = []
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.split("#", 1)[0].strip()
            if line:
                mods.append(line)
    return mods


def _iter_core_py():
    for dirpath, _dirs, files in os.walk(CORE_DIR):
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(dirpath, f)


def _top(module_name):
    return module_name.split(".", 1)[0]


def trial_whitelist_matches_constitution():
    listed = _parse_whitelist(WHITELIST_PATH)
    require_equal(listed, CONSTITUTION_WHITELIST,
                  "core/WHITELIST does not match BOUNDARY.md §2.5 verbatim")


def trial_core_imports_are_whitelisted():
    allowed = set(CONSTITUTION_WHITELIST) | {"core"}
    violations = []
    for path in _iter_core_py():
        with open(path, "r", encoding="utf-8") as fh:
            tree = ast.parse(fh.read(), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if _top(alias.name) not in allowed:
                        violations.append((path, alias.name))
            elif isinstance(node, ast.ImportFrom):
                if node.level and node.level > 0:
                    continue  # relative import within core
                if node.module is not None and _top(node.module) not in allowed:
                    violations.append((path, node.module))
    require(not violations,
            f"core/ imports outside the whitelist: {violations}")

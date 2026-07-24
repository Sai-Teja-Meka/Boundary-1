"""laws/ — the float-literal scanner for core/ (BOUNDARY.md §2.2).

Scans every core/**/*.py and flags any float use:
  * a float literal constant (e.g. 1.0, .5, 1e3);
  * a call to the builtin `float(...)`;
  * an attribute access on a `math` float-returning function name (sqrt, log,
    sin, cos, tan, exp, pow with float, etc.) — belt-and-suspenders on the
    "math is integer-use-only" rule.

core/ has no engine yet, so this passes vacuously, but the scanner is armed for
the first line of engine code.
"""

import ast
import os

from _harness import CORE_DIR, require

_MATH_FLOAT_FUNCS = {
    "sqrt", "log", "log2", "log10", "log1p", "exp", "expm1",
    "sin", "cos", "tan", "asin", "acos", "atan", "atan2",
    "sinh", "cosh", "tanh", "pow", "hypot", "dist", "fmod",
    "remainder", "ldexp", "nextafter", "cbrt", "erf", "erfc", "gamma", "lgamma",
}


def _iter_core_py():
    for dirpath, _dirs, files in os.walk(CORE_DIR):
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(dirpath, f)


def _scan(path):
    with open(path, "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=path)
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            hits.append((getattr(node, "lineno", "?"), f"float literal {node.value!r}"))
        elif isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id == "float":
                hits.append((getattr(node, "lineno", "?"), "float(...) call"))
            elif (isinstance(fn, ast.Attribute)
                  and isinstance(fn.value, ast.Name)
                  and fn.value.id == "math"
                  and fn.attr in _MATH_FLOAT_FUNCS):
                hits.append((getattr(node, "lineno", "?"),
                             f"math.{fn.attr}(...) returns float"))
    return hits


def trial_no_floats_in_core():
    violations = []
    for path in _iter_core_py():
        for lineno, what in _scan(path):
            violations.append(f"{path}:{lineno}: {what}")
    require(not violations, "float usage found in core/:\n" + "\n".join(violations))

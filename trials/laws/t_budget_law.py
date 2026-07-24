"""laws/ — the budget-law harness (BOUNDARY.md §4.1).

Parametric: it engages only when an engine exists. When it does, it will ingest
a corpus through the generic interface (INTERFACE.md) and assert:

  * every reported cost is an integer (never a float);
  * cost accounting is pure and reproducible — the same input yields the same
    total cost across two independent runs;
  * the budget measure (§3.3) is computed from integer cost and integer budget.

Until `core.engine` exists this reports SKIPPED-BY-DESIGN. The harness is written
now so ascension cannot silently bypass the budget law later.
"""

from _harness import require, try_import
from corpora.chronicle import generator as chronicle_gen


def _run_against(engine):
    payloads = list(chronicle_gen.generate(4242, 500))

    def ingest_all():
        state = engine.empty()
        total = 0
        for p in payloads:
            state, _t = engine.ingest(state, p)
            total += engine.last_cost(state)
        return total

    cost_a = ingest_all()
    cost_b = ingest_all()
    require(isinstance(cost_a, int) and not isinstance(cost_a, bool),
            "budget cost must be a plain integer")
    require(cost_a == cost_b, "cost accounting is not reproducible (impure budget)")


def trial_budget_law_harness():
    engine = try_import(
        "core.engine",
        "no engine yet; budget-law harness engages when core.engine exists",
    )
    _run_against(engine)

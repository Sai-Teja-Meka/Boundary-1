"""ops/l3 — the anti-recency-proxy pressure stream (§5 L3, §8).

Certifies the declared spec of `corpora/l3streamb/`:

  (a) **total mass matches spec** — and the tier structure that produces it;
  (b) **importance is decorrelated from position** — by an exact integer
      Spearman rank statistic with midranks, asserted as `rho^2` against a
      squared tolerance so no square root (and therefore no float) is needed;
  (c) **every contiguous budget-sized window holds ~10% of the mass** — checked
      over all 9001 windows, not sampled.

Plus the two consequences that make the corpus load-bearing: both order-based
baselines (fill-then-refuse, keep-latest) are pinned near 100‰, far below the
850‰ ascension gate, while the arithmetic optimum clears it.

The same rank statistic is computed on `l3stream` and required to be ~1, so the
statistic is demonstrably **live**: a broken implementation that returned zero
for everything would fail that check.

Integer-only arithmetic throughout (§2.2): permille bounds are compared as
cross-multiplied integers, and the correlation is compared squared.
"""

from _harness import require, require_equal
from corpora.l3stream import generator as l3
from corpora.l3streamb import generator as b


# ---- the exact rank statistic ---------------------------------------------

def _double_midranks(ws):
    """Midranks of `ws`, each multiplied by 2 so every value stays an integer.

    Ties take the average of the positions they span (the standard midrank), and
    doubling makes that average integral: a tie block spanning 0-based ranks
    `[i, j]` has 1-based midrank `(i + j + 2) / 2`, so twice it is `i + j + 2`.
    Scaling every rank by the same constant leaves a correlation unchanged.
    """
    order = sorted(range(len(ws)), key=lambda i: ws[i])
    out = [0] * len(ws)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and ws[order[j + 1]] == ws[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = i + j + 2
        i = j + 1
    return out


def spearman_terms(ws):
    """Return `(cov, var_pos, var_rank)`, all integers, for Spearman's rho.

    `rho = cov / sqrt(var_pos * var_rank)`, so `rho^2 = cov^2 / (var_pos *
    var_rank)` — an exact rational a caller can bound without a square root.
    Every term is scaled by `n` (and the ranks by 2), which cancels in `rho`.
    Position is the x variable and is tie-free, so its own ranks are `0..n-1`.
    """
    n = len(ws)
    xs = list(range(n))
    rs = _double_midranks(ws)
    sx, sr = sum(xs), sum(rs)
    cov = n * sum(x * r for x, r in zip(xs, rs)) - sx * sr
    var_x = n * sum(x * x for x in xs) - sx * sx
    var_r = n * sum(r * r for r in rs) - sr * sr
    return cov, var_x, var_r


def _weights(gen, seed, n):
    return [it["importance"] for it in gen.generate(seed, n)]


# ---- (a) the declared spec -------------------------------------------------

def trial_l3streamb_determinism():
    a = list(b.generate(b.SEED, 500))
    c = list(b.generate(b.SEED, 500))
    require(a == c, "l3streamb not deterministic at fixed (seed, n)")


def trial_l3streamb_scale_and_shape():
    items = list(b.generate(b.SEED, b.N))
    require_equal(len(items), 10 * b.BUDGET_ITEMS, "stream length must be 10× the item budget")
    tags = set()
    for it in items:
        require_equal(sorted(it.keys()), ["importance", "key", "kind", "tag", "val"],
                      "l3streamb item shape drifted")
        require(it["kind"] == "item", f"bad kind: {it}")
        require(isinstance(it["importance"], int) and not isinstance(it["importance"], bool)
                and it["importance"] >= 1, f"importance must be a positive int: {it}")
        require(it["key"] in b.KEYS, f"key outside the grammar vocabulary: {it}")
        require(isinstance(it["val"], int) and 0 <= it["val"] <= 999, f"val out of range: {it}")
        tags.add(it["tag"])
    require_equal(len(tags), len(items),
                  "tags must be unique — a tag is the item's identity and cue handle")


def trial_l3streamb_total_mass_matches_spec():
    ws = _weights(b, b.SEED, b.N)
    require_equal(sum(ws), b.TOTAL_MASS, "total importance mass drifted from the declared spec")
    heavy = [w for w in ws if w >= b.HEAVY_MIN]
    light = [w for w in ws if w < b.HEAVY_MIN]
    require_equal(len(heavy), b.HEAVY_COUNT, "heavy-tier item count drifted from spec")
    require_equal(sum(heavy), b.HEAVY_MASS, "heavy-tier mass drifted from spec")
    for w in heavy:
        require(b.HEAVY_MIN <= w <= b.HEAVY_MAX, f"heavy weight {w} outside [{b.HEAVY_MIN},{b.HEAVY_MAX}]")
    for w in light:
        require(b.LIGHT_MIN <= w <= b.LIGHT_MAX, f"light weight {w} outside [{b.LIGHT_MIN},{b.LIGHT_MAX}]")
    require(b.HEAVY_COUNT < b.BUDGET_ITEMS,
            "the heavy tier must fit inside the item budget with room to spare")


def trial_l3streamb_heavy_items_are_one_per_stratum():
    # The placement guarantee, checked directly: the strata tile the stream, and
    # exactly one heavy item falls in each. This is what makes the even spread a
    # construction rather than a lucky seed.
    ws = _weights(b, b.SEED, b.N)
    bounds = b.strata_bounds(b.N, b.HEAVY_COUNT)
    require_equal(bounds[0][0], 0, "strata must start at 0")
    require_equal(bounds[-1][1], b.N, "strata must tile the whole stream")
    for j in range(1, len(bounds)):
        require_equal(bounds[j][0], bounds[j - 1][1], f"stratum {j} does not abut its predecessor")
    for j, (lo, hi) in enumerate(bounds):
        n_heavy = sum(1 for i in range(lo, hi) if ws[i] >= b.HEAVY_MIN)
        require_equal(n_heavy, 1, f"stratum {j} [{lo},{hi}) holds {n_heavy} heavy items, want exactly 1")


# ---- (b) the rank statistic ------------------------------------------------

def trial_l3streamb_importance_is_decorrelated_from_position():
    ws = _weights(b, b.SEED, b.N)
    cov, var_x, var_r = spearman_terms(ws)
    require(var_x > 0 and var_r > 0, "degenerate rank variance — the statistic would be undefined")
    tol = b.RANK_CORRELATION_TOLERANCE_PERMILLE
    # rho^2 <= (tol/1000)^2   <=>   cov^2 * 1000^2 <= tol^2 * var_x * var_r
    require(cov * cov * 1000 * 1000 <= tol * tol * var_x * var_r,
            "importance/position rank correlation exceeds the declared %d‰ tolerance "
            "— the stream is not decorrelated (cov=%d, var_x=%d, var_r=%d)"
            % (tol, cov, var_x, var_r))


def trial_rank_statistic_is_live_on_the_monotone_stream():
    # The same statistic on l3stream, whose weights are non-decreasing in t,
    # must come out ~1. Without this, a statistic that always returned 0 would
    # satisfy the decorrelation check vacuously.
    ws = _weights(l3, l3.SEED, l3.N)
    cov, var_x, var_r = spearman_terms(ws)
    floor_permille = 950
    require(cov * cov * 1000 * 1000 >= floor_permille * floor_permille * var_x * var_r,
            "the rank statistic does not detect l3stream's monotone importance "
            "profile — the decorrelation check on l3streamb would be vacuous")


# ---- (c) the window bound --------------------------------------------------

def _prefix(ws):
    out = [0]
    for w in ws:
        out.append(out[-1] + w)
    return out


def trial_l3streamb_every_budget_window_holds_a_tenth_of_the_mass():
    ws = _weights(b, b.SEED, b.N)
    total = sum(ws)
    pre = _prefix(ws)
    width = b.BUDGET_ITEMS
    lo_permille = b.WINDOW_TARGET_PERMILLE - b.WINDOW_TOLERANCE_PERMILLE
    hi_permille = b.WINDOW_TARGET_PERMILLE + b.WINDOW_TOLERANCE_PERMILLE
    n_windows = len(ws) - width + 1
    require_equal(n_windows, 9001, "expected 9001 contiguous budget-sized windows")
    for s in range(n_windows):
        mass = pre[s + width] - pre[s]
        require(mass * 1000 >= lo_permille * total,
                "window [%d,%d) holds %d/%d of the mass, below the declared %d‰ floor"
                % (s, s + width, mass, total, lo_permille))
        require(mass * 1000 <= hi_permille * total,
                "window [%d,%d) holds %d/%d of the mass, above the declared %d‰ ceiling"
                % (s, s + width, mass, total, hi_permille))


def trial_l3streamb_order_based_baselines_are_bounded_below_the_gate():
    """Both order-based policies keep a contiguous window, so both are pinned.

    fill-then-refuse keeps the first budget-worth; keep-latest keeps the last.
    The window bound above makes both ≤ 110‰ — a *structural* bound over every
    window, not a measurement at one seed — against an 850‰ ascension gate and a
    300‰ humility ceiling.
    """
    ws = _weights(b, b.SEED, b.N)
    total = sum(ws)
    pre = _prefix(ws)
    width = b.BUDGET_ITEMS
    gate, ceiling = 850, 300
    for label, mass in (("fill-then-refuse (first budget-worth)", pre[width] - pre[0]),
                        ("keep-latest (last budget-worth)", pre[len(ws)] - pre[len(ws) - width])):
        require(mass * 1000 < gate * total,
                "%s reaches %d/%d of the mass — at or above the %d‰ gate, so the "
                "gate would not require importance ranking" % (label, mass, total, gate))
        require(mass * 1000 <= ceiling * total,
                "%s reaches %d/%d of the mass — above the %d‰ humility ceiling"
                % (label, mass, total, ceiling))


def trial_l3streamb_optimum_clears_the_gate_with_margin():
    """The corpus is *fit for* the ratified gate: the optimum exceeds 850‰.

    A corpus on which no policy could reach the gate would make the Layer-3
    ascension unsatisfiable by construction (which is exactly the recorded
    finding about `l3stream` — see `trials/ascension/l3/ATTAINABILITY.md`). This
    asserts l3streamb does not have that defect.
    """
    ws = sorted(_weights(b, b.SEED, b.N), reverse=True)
    total = sum(ws)
    best = sum(ws[:b.BUDGET_ITEMS])
    permille = best * 1000 // total
    require_equal(permille, b.ATTAINABLE_WEIGHTED_C_PERMILLE,
                  "the attainable weighted-C ceiling drifted from the declared spec")
    require(best * 1000 >= 850 * total,
            "the 1000 heaviest items hold only %d‰ — below the 850‰ gate, so no "
            "engine could clear Layer 3 on this stream" % (permille,))
    # And the heavy tier alone — 800 items, comfortably inside the budget —
    # already clears it, so the gate does not depend on capacity brinkmanship.
    heavy_only = sum(ws[:b.HEAVY_COUNT])
    require(heavy_only * 1000 >= 850 * total,
            "retaining the whole heavy tier reaches only %d‰ — the gate would "
            "depend on filling the budget exactly" % (heavy_only * 1000 // total,))

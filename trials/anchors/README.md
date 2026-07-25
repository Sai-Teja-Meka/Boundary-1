# trials/anchors/

Frozen regression trials that capture exact past behavior. Once an anchor is
set, its expected output never changes — anchors guarantee no silent regression
across sessions.

**Extending** anchors (adding new ones) is allowed; **editing** an existing
anchor is forbidden (§9). The `BOUNDARY.log` line for a move records whether
anchors were left `intact` or `extended`.

Present — one anchor file and one replay trial per claimed layer:

- `l1.json` / `t_l1.py` — replay under `make_engine(layer_cap = 1)`, which is
  index-free and therefore byte-identical forever.
- `l2.json` / `t_l2.py` — replay under `layer_cap = 2`, index included. Layer 2's
  index legitimately changes post-replay state, so L2 records **new** anchors
  rather than folding itself into `l1.json`; `t_l2.py` guards that separation.
- `l3.json` / `t_l3.py` — replay under `layer_cap = 3`, carrying a
  **post-eviction** entry as well as retention entries, so a drift in the
  importance law, the eviction order, the tie-break or the forgetting record's
  coarsening turns the suite red **even when every score still clears the gate**.

The capped constructor is what makes an older layer's anchors eternal: each layer
replays through its own `layer_cap`, so a new layer never perturbs the ones below.

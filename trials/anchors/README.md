# trials/anchors/

Frozen regression trials that capture exact past behavior. Once an anchor is
set, its expected output never changes — anchors guarantee no silent regression
across sessions.

**Extending** anchors (adding new ones) is allowed; **editing** an existing
anchor is forbidden (§9). The `BOUNDARY.log` line for a move records whether
anchors were left `intact` or `extended`.

Present — one anchor file and one replay trial per claimed layer:

- `l1.json` / `t_l1.py` — replay through the L1 adapter, whose `empty()` is the
  `layer_cap = 1` construction: index-free, and therefore byte-identical forever.
- `l2.json` / `t_l2.py` — replay at `layer_cap = 2`, index included. Layer 2's
  index legitimately changes post-replay state, so L2 records **new** anchors
  rather than folding itself into `l1.json`; `t_l2.py` guards that separation.
- `l3.json` / `t_l3.py` — replay at `layer_cap = 3`, carrying a **post-eviction**
  entry as well as retention entries, so a drift in the importance law, the
  eviction order, the tie-break or the forgetting record's coarsening turns the
  suite red **even when every score still clears the gate**.
- `l4.json` / `t_l4.py` — replay at `layer_cap = 4`, carrying a **consolidated**
  entry (`l4stream` at the gate's own 43 300-cell cap, after 18 788 demotions and
  714 losses) as well as derivation entries at `DEFAULT_BUDGET`, so a drift in
  the facet map, the invertibility rule, the row codec's field order, the
  key-major nesting, the demotion order or the shedding rule turns the suite red
  **even when every score still clears the gate**.
- `l5.json` / `t_l5.py` — replay at `layer_cap = 5`, carrying a **prospection**
  entry (`l5stream` at the ratified 45 638-cell cap, after 17 772 demotions,
  2 041 losses and 765 firings with 180 intentions still pending) as well as
  entries at `DEFAULT_BUDGET`. The generous-cap entries pin both directions:
  `sessions` and `murk` carry no intention, so prospection is **inert** on them
  and their clocks end exactly at the caller count, while `l5stream` at
  `DEFAULT_BUDGET` pins that nothing is lost where there is room — every caller
  event byte-exact, `forgotten = 0`. A drift in the arming rule, the firing
  order, the pending-set or fired-ledger layout, the loss reconciliation or the
  row codec turns the suite red **even when every score still clears the gate**.

The capped constructor (§7.4) is what makes an older layer's anchors eternal: each
layer replays at its own `layer_cap`, so a new layer never perturbs the ones below.

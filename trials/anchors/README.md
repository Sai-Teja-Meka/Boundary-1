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

- `l6.json` / `t_l6.py` — replay at `layer_cap = 6`, and the first anchor file
  that pins a **model** rather than only a state. Its `corpora` entries pin a
  **negative**: every shared shape figure equals `anchors/l5.json`'s own frozen
  figure for the same corpus, asserted by reading that file, because `§5.1 L6`
  defends `B = 1000` with *"meta-memory derives confidence from existing state"*
  and this engine adds no field — the canonical bodies differ in exactly one
  branch, the recorded `layer_cap`. Its `calibration` entries carry both Layer-6
  artifacts at `DEFAULT_BUDGET` — `A`, `n_pos`, `n_neg`, every `§3.4` quantity as
  an exact `Fraction` **and** its permille rendering, the engine's whole
  confidence vocabulary, and a `trace_sha256` over the canonical
  `(qid, status, confidence)` triples. The trace is the point: a score can
  survive a changed model, since two different confidence assignments can round
  to one Brier, and the trace cannot. The two artifacts sit side by side because
  together they are what the fourth substrate kill was for — `AUROC 976` on the
  binding artifact against **1000** on the demoted diagnostic, where the ties the
  engine reads are exactly its errors.

- `l7.json` / `t_l7.py` — replay at `layer_cap = 7`, and the first anchor file
  that pins **what an engine made** rather than only what it holds or how sure it
  is. Its `corpora` entries pin the same **negative** `l6.json` pins, one layer
  on: `sessions`, `murk` and `l5stream` carry no `profile` payload, so the ledger
  is empty and costs nothing, every shared shape figure equals `anchors/l6.json`'s
  own frozen figure for the same corpus, and the canonical bodies differ in
  exactly two branches — the recorded `layer_cap`, and an **empty** `lineage`.
  Its `generation` entry carries `corpora/l7compose` at `DEFAULT_BUDGET`: all
  three capability ratios and every `§3` measure as an exact `Fraction` **and** a
  permille rendering, the confidence vocabulary, the whole three-rung ladder with
  the ledger it leaves (`{1: 100, 2: 30, 3: 30}`, 320 cells) — and **three
  hashes**, because at this layer a score cannot stand in for any of them:
  `trace_sha256` over `(qid, status, lineage, confidence)`, since `tagging = 1000`
  says how many and not **which**; `support_sha256` over
  `(qid, kind, support, t_asof)`, since `R8` clause 5(b) binds relevance to
  *exactly* the `t`s the rule reads and a tag citing a different set of the same
  size clears every `§5 L7` clause; and a state hash **after** the three
  generations, since the ledger is the layer and its content is not any rung's
  number.

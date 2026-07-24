# core/

The **pure engine**. Empty at Phase 0 except `WHITELIST` (the machine-readable
stdlib import allowlist, §2.5).

Non-negotiable, enforced by the `laws/` trials:

- **Purity** — every op is `op(state, input) -> (state', output)`; no hidden
  state, no input mutation, no globals.
- **No I/O, no wall clock, no randomness, no floats** (§2.2).
- **Import whitelist** — only the modules in `WHITELIST`, and `math` for integer
  use only (§2.5).
- **Layering** — `shell/` may import `core/`; **`core/` may NEVER import
  `shell/`** (§2.6). `core/` imports neither corpora nor trials.

`core/layers/` holds the per-layer engine code, added one layer at a time by
`ASCEND` moves. Old layers are frozen and never edited (§9).

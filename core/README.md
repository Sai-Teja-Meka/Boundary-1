# core/

The **pure engine**.

- `WHITELIST` — the machine-readable stdlib import allowlist (§2.5).
- `serialize.py` — core's own canonical encoder (§2.4), byte-for-byte equal to the
  `corpora/canon` reference and proven so by the serializer cross-check law.
- `state.py` — the immutable block-structured event log and integer cost accounting.
- `engine.py` — the generic interface (§7): `empty` / `make_engine` / `ingest` /
  `query` / `snapshot` / `restore` / `last_cost`.
- `layers/` — the per-layer engine code (below).

Non-negotiable, enforced by the `laws/` trials:

- **Purity** — every op is `op(state, input) -> (state', output)`; no hidden
  state, no input mutation, no globals.
- **No I/O, no wall clock, no randomness, no floats** (§2.2).
- **Import whitelist** — only the modules in `WHITELIST`, and `math` for integer
  use only (§2.5).
- **Layering** — `shell/` may import `core/`; **`core/` may NEVER import
  `shell/`** (§2.6). `core/` imports neither corpora nor trials.

`core/layers/` holds the per-layer engine code, added one layer at a time by
`ASCEND` moves. Old layers are frozen and never edited (§9). Three layers are
claimed — **L1 Retention**, **L2 Recall**, **L3 Forgetting** — each with its own
`README-lN.md`; see `core/layers/README.md` for the index.

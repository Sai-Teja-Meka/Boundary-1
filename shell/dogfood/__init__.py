"""shell/dogfood/ — the DOGFOOD adapter: this engine as its own project memory.

A CLI (`python3 -m shell.dogfood`) with three commands — `remember`, `recall`,
`status` — over a persistent Layer-2 store held in `shell/dogfood/store/`.
The shell does the I/O; the engine stays pure (§2.2, §2.6).

See `README.md` (decisions) and `FIELD.md` (what chafed, in use).
"""

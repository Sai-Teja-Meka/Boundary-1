# shell/

The **impure rim**: CLI, persistence, and adapters. `shell/` **may** import
`core/`; `core/` may **never** import `shell/` (§2.6).

Everything the constitution forbids in `core/` — file and network I/O, argument
parsing, reading the environment — lives here, on the far side of the purity
boundary. The engine stays pure; the shell does the touching of the world.

Empty at Phase 0 — filled during `ASCEND`/`DOGFOOD` moves once there is an engine
to wrap.

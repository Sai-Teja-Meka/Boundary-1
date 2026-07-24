# trials/anchors/

Frozen regression trials that capture exact past behavior. Once an anchor is
set, its expected output never changes — anchors guarantee no silent regression
across sessions.

**Extending** anchors (adding new ones) is allowed; **editing** an existing
anchor is forbidden (§9). The `BOUNDARY.log` line for a move records whether
anchors were left `intact` or `extended`.

Empty at Phase 0 — the first anchors are set when the first engine behavior
exists to freeze.

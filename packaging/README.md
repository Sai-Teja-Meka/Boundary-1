# `packaging/`

Distribution scaffolding for the public identity **memtrials**. Filled by the
`PACKAGE` move (`BOUNDARY.md §9.1`).

**No longer empty.** The first `PACKAGE` ran at Layer 4 (`BOUNDARY.log`,
`[L4] [PACKAGE]`): the benchmark learned to travel, and nothing was published.

| file | what it is |
|---|---|
| `README-public.md` | the sober public identity — the problem, the ground-truth audit, the positioning against MemoryAgentBench and WRIT, the L1–L4 scorecard with its humility ceilings, the limitations, and the transfer tier |
| `HONESTY.md` | the claims discipline: what this is, what it is not, the strain-2 story told straight, and the methodology evidence **both ways** |

Both are checked rather than trusted. `trials/ops/packaging/t_scorecard.py`
parses `README-public.md`'s scorecard and compares every published number
against the engine — measured live where that is cheap, and named to its owning
trial where it is not. A public number that drifts from the engine is a **red
suite**, which is the only form of documentation discipline this project trusts.

## What else the first PACKAGE produced, elsewhere in the tree

Packaging is not a directory; it is a property of the whole repository. The
other four deliverables landed where they belong:

* `trials/adapters/external/` — a **reference external engine** written against
  `INTERFACE.md` and importing nothing from `core/`, plus adapter stubs for Mem0
  and Letta. It clears Layers 1–2 and fails Layers 3–4, which is how the harness
  demonstrates that it grades any system *and* still discriminates.
  `trials/adapters/README.md` carries the contract, including the half
  `INTERFACE.md` leaves implicit.
* `trials/__main__.py` + `trials/scorecard.py` — the one-command entry,
  `python3 -m trials --engine <ours|reference|…>`, built on `run.py`'s own
  machinery and the shared per-layer scorers. **`run.py` is still the one gate**;
  `--suite` calls it and returns its exit code unchanged.
* `corpora/real-sessions/v1/` — the frozen, checksummed, scrubbed **transfer
  corpus** (§8.8), a snapshot of this project's own dogfood store.
  `corpora/real_sessions.py` is its loader and its scrub.
* `trials/ops/packaging/` — the trials that keep all of the above honest.

## The standing constraints

Whatever lands here still obeys the whole constitution: zero third-party
dependencies, deterministic, and `python3 trials/run.py` green before any commit
— documentation included (§9.3).

And one more, recorded by the session that filled this directory: **preparing to
publish is not publishing.** Repository visibility, write-ups and the grading of
live external systems are human decisions, taken one deliberate step at a time.
No adapter here reaches a network or wants a key.

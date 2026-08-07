# `packaging/`

Distribution scaffolding for the public identity **memtrials**. Filled by the
`PACKAGE` move (`BOUNDARY.md §9.1`).

**No longer empty.** The first `PACKAGE` ran at Layer 4 (`BOUNDARY.log`,
`[L4] [PACKAGE]`): the benchmark learned to travel, and nothing was published.
The second ran at Layer 7 (`[L7] [PACKAGE]`), when three claimed layers were
missing from the scorecard and the Phase 3→4 gate was the next move: **Phase 3
now travels standalone**, and still nothing is published.

| file | what it is |
|---|---|
| `README-public.md` | the sober public identity — the problem, the ground-truth audit, the positioning against MemoryAgentBench and WRIT, the five substrate kills, the **L1–L7** scorecard with its humility ceilings, the novelty horizon, the limitations, and the transfer tier |
| `CATALOG.md` | the failure catalog: Schacter's seven sins in their complete Phase-3 form with a trial against every row, the three **catalog extensions** the ladder minted (the denominator law, the novelty horizon, the lateness theorem), and — adjacent, because it is a different kind of claim — the **four-kind impossibility taxonomy**, final below `BOUNDARY-HIGH.md` |
| `HONESTY.md` | the claims discipline: what this is, what it is not, the strain-2 story told straight, and the methodology evidence **both ways** |

All three are checked rather than trusted. `trials/ops/packaging/t_scorecard.py`
parses `README-public.md`'s scorecard and compares every published number against
the engine; `t_catalog.py` compares every quotation in `CATALOG.md` against the
document it is quoted from and requires every trial it names to exist under the
class it names it in. A public number or a quotation that drifts is a **red
suite**, which is the only form of documentation discipline this project trusts.

## What the two `PACKAGE` moves produced elsewhere in the tree

Packaging is not a directory; it is a property of the whole repository.

* `trials/adapters/external/` — a **reference external engine** written against
  `INTERFACE.md` and importing nothing from `core/`, plus adapter stubs for Mem0
  and Letta. It clears Layers 1–2, fails Layers 3–4 and is not measured above
  that, which is how the harness demonstrates that it grades any system *and*
  still discriminates. `trials/adapters/README.md` carries the **adapter
  contract**, including the half `INTERFACE.md` leaves implicit — and it now runs
  through Layer 7's `lineage` field.
* `trials/__main__.py` + `trials/scorecard.py` — the one-command entry,
  `python3 -m trials --engine <ours|reference|…>`, built on `run.py`'s own
  machinery and the shared per-layer scorers, now covering **all seven claimed
  tiers** and their humility rows. **`run.py` is still the one gate**; `--suite`
  calls it and returns its exit code unchanged.
* `corpora/real-sessions/v1/` — the frozen, checksummed, scrubbed **transfer
  corpus** (§8.8), a snapshot of this project's own dogfood store.
  `corpora/real_sessions.py` is its loader and its scrub.
* `corpora/real-sessions/V2-FREEZE-STOPPED.md` — the record of a `v2` freeze that
  was **attempted and stopped by its own scrub**, with everything a human needs
  to decide it. A deliverable that did not land is still a deliverable, and the
  refusal is kept true by `trials/ops/packaging/t_real_sessions_v2.py`.
* `trials/ops/packaging/` — the trials that keep all of the above honest.

## The standing constraints

Whatever lands here still obeys the whole constitution: zero third-party
dependencies, deterministic, and `python3 trials/run.py` green before any commit
— documentation included (§9.3).

Two more, one recorded by each session that filled this directory.

**Preparing to publish is not publishing.** Repository visibility, write-ups and
the grading of live external systems are human decisions, taken one deliberate
step at a time. No adapter here reaches a network or wants a key.

**Packaging describes; it never redefines.** Every number in this directory is
read from the repository, and where a description and the repository disagree the
repository is right and the sentence changes. No file here has ever moved a
ratified threshold, a ceiling, a corpus binding or a score, and none may.

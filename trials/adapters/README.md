# `trials/adapters/` — the only thing a trial is allowed to talk to

`BOUNDARY.md §7` defines a **generic engine interface**: three pure functions and
an Answer. `INTERFACE.md` in this directory is a verbatim copy of it (§7 is
authoritative; the copy is the defect if they disagree). Every trial in the suite
speaks to an engine only through an adapter here — never to `core/` directly —
which is what makes the sentence below checkable rather than aspirational:

> **the suite grades any system that implements the interface, not only ours.**

## The catalogue

| adapter | binds | claims |
|---|---|---|
| `l1.py` | `core.engine` | Layer 1 |
| `l2.py` | `core.layers.l2_recall` | Layers 1–2 |
| `l3.py` | `core.layers.l3_forgetting` | Layers 1–3 |
| `l4.py` | `core.layers.l4_consolidation` | Layers 1–4 |
| `l5.py` | `core.layers.l5_prospection` | Layers 1–5 |
| `external/reference.py` | nothing in `core/` | Layers 1–2, and stops |
| `external/mem0_stub.py` | — | a written-down mapping; not runnable |
| `external/letta_stub.py` | — | a written-down mapping; not runnable |

One adapter per layer on our side, because the older engines stay frozen (§9.2):
`anchors/l1.json` replays through `adapters/l1` forever, whatever Layer 4 does.

## The contract, including the half `INTERFACE.md` leaves implicit

`INTERFACE.md`'s "Adapter contract" names six functions:

```
empty() -> state
make_engine(layer_cap) -> state
ingest(state, payload) -> (state, t)      # t is None on a budget refusal (§4.1.2)
query(state, q) -> answer                 # the §7.2 Answer, never an exception
snapshot(state) -> bytes
last_cost(state) -> int
```

Writing `external/reference.py` — an engine with no knowledge of this repository
— surfaced one more requirement that the interface document does not state, and
it is recorded here rather than left to be rediscovered:

> **The two §4.1 numbers are read as attributes.** The shared scorers read
> `state.occupancy` and `state.budget_cap` directly, because §3.3's budget
> measure and §5 L4's footprint are defined over them and §7 gives no accessor
> for either. `_l3score` and `_l4score` are frozen and take the attribute form
> only; `_l1score`, written this session, also accepts a mapping — so the
> portable answer is **attributes**, on whatever object an adapter calls a state.
> `restore(bytes) -> state` is the same kind of implicit requirement, needed by
> §5 L1's round-trip clause.

This is a finding about our own interface document, not a complaint about it:
§7 is frozen, so the gap is *recorded* here and in `INTERFACE.md`'s neighbours
rather than patched into the constitution.

## `external/` — engines that are not ours

The three modules under `external/` exist to keep the generic claim honest. Two
rules govern them, and the second one is the load-bearing one:

1. **`available()` before anything else.** Every module exposes
   `available() -> (bool, reason)`. The scorecard runner checks it before it
   would call an interface function.
2. **A stub never produces a score.** A stub *raises* when called
   (`AdapterNotRunnable`) instead of abstaining, which looks like a violation of
   §7.3 and is not: §7.3 governs **capability absence in an engine under test**,
   where an abstention is the honest answer and gets scored by the §3.0 table. A
   stub is not an engine — there is nothing behind it to abstain. If a stub
   abstained its way through a battery it would report a *measurement of a system
   that was never run*, which is the single worst thing this directory could
   produce.

No adapter here opens a socket, reads an environment variable, or wants a key,
and none will from inside a session: a number obtained that way is not
reproducible, and `packaging/HONESTY.md` records why grading a live external
system is a separate, human-supervised step.

## Adding an adapter for a real system

1. Read `INTERFACE.md` and the implicit half above.
2. Write the mapping down first, as `mem0_stub.py` and `letta_stub.py` do:
   which call serves each op, what has no counterpart, and what the adapter has
   to *invent* (a logical `t`, a top-1-or-abstain rule). Every invention is the
   adapter's editorial choice and belongs in the report beside the score.
3. Register it in `external/__init__.py::ADAPTERS`.
4. Grade it with `python3 -m trials --engine <name>`, under a human, with the
   non-determinism stated.

The scorecard will place it on the same rows as ours, against the same ratified
gates, measured by the same scorers. That is the whole design: the benchmark
does not know whose engine it is holding.

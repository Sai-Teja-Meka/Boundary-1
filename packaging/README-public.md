# memtrials

**An executable correctness specification for memory systems.** Nine ordered
capability layers, each with a ratified threshold, each with a proof that the
layer below it cannot pass, all graded by deterministic code with no model in
the loop. Four layers are built and certified; five are specified and unclaimed.

---

## The problem

Memory systems race to **recall** and never prove they can do anything else.
There is no accepted way to show that a system forgets under a hard budget, that
it consolidates without lying about what it consolidated, that its confidence
tracks its accuracy, or that it can tell a thing it remembered from a thing it
made up. And the ground truth the field measures recall against is not reliable
enough to settle even the question it does ask.

That last sentence is not rhetoric. We audited it.

### The ground-truth audit, and what may be repeated from it

`autopsy/locomo/ANATOMY.md` (LoCoMo, commit `3eb6f2c`) sampled 60 of the 1 986
QA items with their resolved evidence and found mis-keyed answers
(`conv9:qa70`, `conv9:qa42`, `conv2:qa41`), gold drawn from outside the
conversation (`conv4:qa66`), malformed gold (`conv3:qa39`, `conv3:qa66`,
`conv8:qa19`), category mislabels (`conv0:qa3`, `conv7:qa79`, `conv4:qa46`), and
temporal keys stated as relative phrases. A published audit's 6.4% figure is
agreed as a **floor**; the sample suggests two to three times that in the
temporal and open-domain categories, with single-hop clean.

**Only numbers and techniques travel from that audit.** The LoCoMo corpus is
**CC BY-NC 4.0**, so no text of it is reproduced here, and no corpus in this
repository is derived from it. What we took is method: adversarial construction
(mis-attribution, false presupposition) rebuilt from *our own* grammars as an
abstention family (`autopsy/GAPMAP.md` **S6**), and three corpus rules —
grounding, canonical keys, closed-world honest labelling.

**The judge attribution is kept exact, because it is routinely blurred.** The
in-repo, official LoCoMo judge is **token-F1 overlap** (`evaluation.py:209–214`),
with open-domain scored on only the first `;`-clause and adversarial scored by
substring containment. The lenient `gpt-4o-mini` judge — the one measured to
accept 62.81% of wrong-but-adjacent answers — is a **downstream, third-party
addition**, not part of the LoCoMo repository. Criticising the second is not
criticising the first.

---

## Positioning

Seven systems were read from source before a line of this engine was written —
four memory engines, two evaluators, one further evaluator read later — and the
positioning below is what survived that reading. Every claim is pinned to the
commit it was traced at, exactly as the autopsies are. The full argument is
`autopsy/GAPMAP.md §4`; this is its summary.

**Against MemoryAgentBench** (commit `455306d`, MIT code; dataset licensed
separately). It is a flat, parallel-track leaderboard: four independent dataset
configs scored as `accuracy(method, task)`, dispatched per-baseline
(`agent.py:64+`), with no capability cap on the system under test and no
upper-bound assertion anywhere. It therefore **cannot express an impossibility
gate** — "a system frozen at capability N−1 must score at or below a ceiling on
task N" has no analogue in its architecture. It also has no abstention category:
a system that knows it does not know earns nothing for saying so.

**Against WRIT** (commit `3c0900a`, v0.2.0; MIT declared in `package.json:23`,
no `LICENSE` file; the independent project of Mark Hendrickson, posted as a
complementary benchmark in the comments of Penfield Labs' proposal — the two are
separate work). WRIT is the second independent evaluator to lack
impossibility-gating (flat 16-way union, `types.ts:16–32`; grouping never
ordering, `runner.ts:77–112`), and the first found to contain a mechanism
pointing the *other* way: `AdapterCapabilities` lets a system declare a
capability `false`, which sets that score `null`, and `null` is filtered out of
**both** numerator and denominator (`evaluator.ts:545–548`, stated outright at
`docs/metrics.md:204`). A system exempts itself by declaring itself incapable.
Here the capped engine is run through the identical interface on the new layer's
own tasks, must abstain rather than raise, and has its abstentions **scored**
against a declared ceiling. Provenance in WRIT is likewise a property of the
*store*, probed out-of-band on 5 of 77 scenarios and opt-out-able, while the
answer's own `cited_sources` is read by **zero** lines of scoring; from Layer 7
here an untagged answer scores 0 however correct.

**The fourth axis, and the one nobody occupies.** What the field calls
"selective forgetting" is **supersession reasoning** — answer with the newest
value (`templates.py:80`). Generative Agents writes an `expiration` field and
never reads it to evict (`associative_memory.py:79–82`, commit `fe05a71`); Mem0
gates decay to its platform and hides rather than deletes (commit `d6d89c9`);
Graphiti invalidates and never evicts (commit `3bb2d0b`); Letta demotes into an
**unbounded** cold tier (commit `b76da90`). **Removal under a hard budget is
untested by every system and every evaluator we read.** Layer 3 gates it.

One thesis ties the four engines together, and it is the reason this project
exists: **recorded but never binding.** Each writes the metadata that would make
it correct — the expiry, the source flag, the `invalid_at`, the
derived-vs-original marker — and then never reads it where it would count.

---

## The scorecard

Four layers claimed. Gates are `BOUNDARY.md §5`, unchanged; the corpus each gate
binds on is settled by `BOUNDARY-RULINGS.md` R1 (Layer 3) and R4 (Layer 4).
Reproduce the whole table with:

```
python3 -m trials --engine ours          # ~1 minute
python3 trials/run.py                    # the actual gate: 217 trials, ~5 minutes
```

| layer | ratified gate | measured | verdict | humility ceiling | capped engine, measured |
|---|---|---|---|---|---|
| **L1** Retention | F=1000, C≥995, B=1000, snapshot byte-identical | F 1000 · C 1000 · B 1000 (chronicle 50k, sessions 5k, murk 10k) | PASS | — (floor: no lower layer to cap against) | — |
| **L2** Recall | cue-C≥900, F≥950, B=1000 | cue-C 1000 · F 1000 · B 1000 | PASS | capped cue-C ≤ 100 | **capped cue-C 0** (`make_engine(1)`) |
| **L3** Forgetting | weighted-C≥850, unweighted-C≥90, F≥950, B=1000 | weighted-C 917 · unweighted-C 91 · F 1000 · B 1000 (`l3streamb`, 10× budget) | PASS | capped weighted-C ≤ 300 | **capped weighted-C 92** (`make_engine(2)`; 34 for the frozen L2 engine capped the same way) |
| **L4** Consolidation | footprint≤250, reconstruction F≥900, C≥850, B=1000 | footprint 250 · F 968 · C 1000 · B 1000 (`l4stream`, 20k) | PASS | capped reconstruction F ≤ 400 | **capped F 300** at `l4stream[:4000]`; 302 whole-stream, measured once out of suite |
| L5 Prospection | trigger-precision = trigger-recall = 1000, dup-fire = miss = 0 | — | unclaimed | capped trigger-recall ≤ 50 | — |
| L6 Meta-memory | Brier≤40, ECE≤30, AUROC≥900 | — | unclaimed | capped AUROC ≤ 600 | — |
| L7 Generation | validity = novelty = tagging = 1000, self-pollution promotion = 0 | — | unclaimed | capped (novel∧valid∧tagged) ≤ 50 | — |
| L8 Self-description · L9 Birth | *thresholds specified at the Phase 3→4 gate* | — | unspecified | — | — |

Every gate printed by `python3 -m trials` is read out of
`trials/laws/t_rulings.py::AUTHORIZED_GATES`, the registry that binds each
threshold to a literal §5 clause or a ruling and forbids any gate constant under
`trials/` that is not in it. A number on this table that drifted from the engine
is a red trial (`trials/ops/packaging/t_scorecard.py`).

### Two entries in that table that need a sentence each

**Layer 3's `l3stream` diagnostic.** The Layer-3 gate binds on `l3streamb`, not
on `l3stream`, and the reason is arithmetic rather than convenience: on
`l3stream` the budget-worth of heaviest items holds **190‰** of the total mass,
so an 850‰ gate is unreachable there by *any* retain-or-drop policy, including a
perfect one. The session that discovered this **stopped and withheld the
engine**; a human ruling moved the binding, never the threshold
(`BOUNDARY-RULINGS.md` R1). `l3stream` is still replayed and still scored, as an
ungated diagnostic, at 174‰ against its own 190‰ ceiling.

**Form B — the Layer-4 engine passing *through* a Layer-3 ceiling.** At Layer 3's
own pressure cap, on Layer 3's own binding corpus, through Layer 3's own battery
with nothing re-tuned, the Layer-4 engine reaches **weighted-C 924** where the
frozen Layer-3 engine reaches 917 — and Layer 3's recorded oracle ceiling is
918. **That ceiling is exact over the policy class Layer 3 could choose from:
retain-or-drop, where the only question is which whole episodes to keep. A
consolidating engine is not in that class, and it passes through the ceiling for
precisely the reason the ceiling was true.** No Layer-3 number moves: the L3
adapter is untouched, its gate still binds at 850 against 918, and its own
measurement is still 917. The mechanism is named rather than observed —
`l3streamb` contains no supersession at all, so the entire gain is the row codec
at 6 cells per retained item against 12.

### The limitations, which are load-bearing

**The cue channel reaches 26‰ of what the engine can answer.** At the ratified
Layer-4 footprint on the binding corpus, 18 788 of 20 000 events are demoted:
their content is fully returned by `read(t)`, and **not one of them answers a cue
built from its own payload**. The associative channel reaches the 498 still-held
episodes — **26‰** of the 19 286 events the engine can still return. Every
blocked cue abstains; none is answered wrongly. This is a **non-capability by
arithmetic, not by omission**: at a quarter of the raw footprint exactly one
access path is affordable, the schema carries the `(entity, key) → history` one,
and the associative path is the one the budget does not buy. Demoted content is
`t`-addressable, not cue-addressable.

**Reconstruction is a sweep, not a lookup.** The inverse index that would make
`read(t)` a lookup costs a third cell per assertion — 343‰ against a 250‰ gate —
so query time pays what state cannot. The suite is about five minutes, most of
it that trade.

**714 events on the binding corpus are gone and cannot be recovered.** They left
behind a count and a mass in 23 integer cells. No injective map exists from
thousands of payloads into 23 cells, so those events are unanswerable in
principle and the engine abstains on every one. It can, however, tell *forgotten*
from *demoted* from *never ingested*.

**Four layers are unbuilt, and Layer 5 already has a known problem.** §5 L5's
gate is an **identity** (`trigger-precision = trigger-recall = 1000`), while the
standing rule R2 requires every future gate to lie strictly *below* the oracle
ceiling on its binding corpus — and for an exactness gate the oracle ceiling is
1000. That obligation cannot be discharged at Layer 5 by the method that
discharged it at Layers 3 and 4, and it is recorded as the next open question
rather than quietly resolved.

**Calibration is dormant.** No confidence number here is gated until Layer 6.
The engine emits structural certainty; do not read it as calibrated.

---

## The transfer tier — and where it diverges

Synthetic corpora are built by the same people who built the engine. So the
scorecard carries a **transfer tier**: the same engine, the same scorers, run on
`corpora/real-sessions/v1` — a frozen, checksummed snapshot of this project's own
accumulated session store, 25 real events written by humans and agents about this
repository, bound by SHA-256 under `BOUNDARY.md §8.8` and scrubbed at the freeze
(7 families scanned, 0 findings, 0 removals, 0 events modified).

| layer | measured on `real-sessions/v1` | verdict |
|---|---|---|
| L1 Retention | F 1000 · C 1000 · B 1000 | PASS |
| L2 Recall | cue-C 1000 · F 1000 · B 1000 (25 of 25 uniquely cueable) | PASS |
| L3 Forgetting | **not gateable**: 0 of 25 events carry an importance field, 0 carry any handle field | n/a |
| L4 Consolidation | footprint 151 · F 172 · C 1000 · B 1000 | **FAIL** |

**Layers 1 and 2 transfer cleanly.** Exact retention does not care where an event
came from, and the store's own cue surface recalls every summary.

**Layer 3 is reported `n/a` rather than scored.** Its gate is stated over a
stream carrying an `importance` field and a handle the engine can address; a real
session summary carries neither. A weighting invented by the harness would be
measuring the harness.

**Layer 4 fails, and the failure is a property of the fuel.** The facet map reads
**0** assertions in a session summary and `row_shape` refuses every one of them
(a nested field is not a grammar atom), so the engine builds no chain, no row and
no derived view: **0 assertions, 0 rows, 0 demotions, 25 of 25 irreducible.**
Consolidation degenerates exactly to Layer-3 forgetting, and the identity is
exact — at the same cap the frozen Layer-3 engine retains the same 2 events the
Layer-4 engine can answer. `C 1000` on that row should be read as nothing at all:
with no `(entity, key)` pair in the corpus the coverage denominator is **1**, a
single global count. Read `F 172`.

**And the uncomfortable part, published rather than buried.** On this corpus the
reference *external* engine — which cannot forget, and simply fills then refuses
— returns **11** of 25 events byte-exact against our **2**. Neither is a defect
and neither is a fluke: §3.0's fidelity counts events, fill-then-refuse maximizes
count by keeping the cheapest (here the earliest, shortest summaries), and our
inherited importance law spends the budget on the two most recent — which on this
corpus are also the two largest. Whether "the latest two sessions in full" or
"the first eleven" is the better memory of a project is a judgement the
constitution does not make, and neither does this table. What we will not do is
publish only the corpus our engine was designed against.

---

## What it grades, and how

Everything speaks one interface (`BOUNDARY.md §7`): `ingest`, `query`,
`snapshot`, plus `make_engine(layer_cap)` for the capped runs. Trials never touch
an engine directly. A reference external engine, written against that interface
and importing nothing from this repository's core, is graded on the same rows:
it clears Layers 1 and 2 and fails Layers 3 and 4, which is how the harness shows
it is generic *and* discriminating.

```
python3 -m trials --list-engines
python3 -m trials --engine reference      # a foreign engine, same gates
python3 -m trials --engine mem0           # a stub: prints why it will not run here
```

Adapter stubs for **Mem0** and **Letta** carry the interface mapping in full and
deliberately stop short of the call. Running a live external system needs a
provider key, network egress and a tolerance for non-deterministic results; that
is a human-supervised step, not something a session does to itself.

## Properties

Zero third-party dependencies. Pure Python standard library, from a frozen
nine-module whitelist. No floats, no wall clock, no randomness outside one
xorshift PRNG that the engine never imports. Byte-identical results on every
platform and every run — determinism is a law here, enforced by a trial class,
not an aspiration. Nothing ships unless `python3 trials/run.py` exits 0, and that
includes documentation.

## Honesty

What this is, what it is not, and what its own engine was caught doing:
[`packaging/HONESTY.md`](HONESTY.md). Read it before citing anything above.

## Reading order

`BOUNDARY.md` (the frozen constitution) → `BOUNDARY-RULINGS.md` (the frozen
supplement) → `autopsy/GAPMAP.md` (what the prior art does and does not do) →
`core/layers/README-l4.md` (the newest layer) → `BOUNDARY.log` (every session
ever run, append-only).

---

*This project keeps a cultivation metaphor, quarantined in exactly one file:*
[`LORE.md`](../LORE.md).

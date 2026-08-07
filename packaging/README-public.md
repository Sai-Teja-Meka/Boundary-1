# memtrials

**An executable correctness specification for memory systems.** Nine ordered
capability layers, each with a ratified threshold, each with a proof that the
layer below it cannot pass, all graded by deterministic code with no model in
the loop. **Seven of the nine are built and certified**; the last two —
self-description and birth — receive laws but **no thresholds at all** until
`BOUNDARY-HIGH.md` is written at the Phase 3→4 gate.

Retention, recall, forgetting, consolidation, prospection, meta-memory,
generation. Each gate binds on a corpus a human bound **by ruling** — eight of
them, `R1` through `R8`, in a frozen append-only supplement — after the
arithmetic showing it is attainable was computed and machine-checked with **no
engine in existence**. Five candidate substrates were killed by that arithmetic
along the way, one of them an artifact this project had frozen a single session
earlier.

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

### Five substrate kills, and what they cost us

The claim a benchmark is least able to make about itself is that its corpora are
not tuned to its engine. What this one can put on the record instead is the list
of its own artifacts that were **disqualified by arithmetic**, each with its
cause recorded verbatim in a frozen ruling and each still running in the suite as
an ungated diagnostic:

| # | artifact | why it cannot carry a gate |
|---|---|---|
| 1 | `l3stream` (`R1`) | its budget-worth of heaviest items holds **190‰** of the mass, so an 850‰ gate is unreachable by *any* retain-or-drop policy, including a perfect one |
| 2–3 | `chronicle` + `murk` at Layer 4 (`R4`) | the exact history schema costs **384‰** against a 250‰ gate, short by 52 872 cells, *because identification does not compress* — **and** a current-value table with no history whatsoever reaches **95%** of the oracle, so the corpus cannot tell consolidation from a table of last-writes |
| 4 | `l6battery` (`R7`) | on `murk`, **evidence that ranks also resolves** — `§8.7` injects every defect by visible construction, so a stream-only rule recovers each family exactly. Demoted **one session after this project froze it**, by a limit that same session measured and published about itself |
| 5 | the **whole existing stock** at Layer 7 (`R8`) | across 85 954 answerable queries drawn from every frozen artifact's own battery, **not one** answer is absent from its own stream, so the generation-required class is empty everywhere and a gate citing novelty or tagging measures nothing. Recorded as a **refusal to bind** rather than a demotion — nothing was demoted, no byte moved, and the survey is a **trial**, so a corpus frozen later that *did* force a composition goes red rather than passing unnoticed |

Two of the five were found by sessions that **stopped and withheld the engine**
at the sanctioned boundary rather than shipping around the finding. All five were
resolved by a human ruling, none by a session's convenience, and no threshold in
`BOUNDARY.md §5` has ever moved.

---

## The scorecard

Seven layers claimed. Gates are `BOUNDARY.md §5`, unchanged; the corpus each gate
binds on is settled by `BOUNDARY-RULINGS.md` R1 (Layer 3), R4 (Layer 4), R6
(Layer 5), R7 (Layer 6) and R8 (Layer 7). Reproduce the whole table with:

```
python3 -m trials --engine ours          # 2m08, all seven tiers plus the transfer tier
python3 trials/run.py                    # the actual gate: 573 trials, 10m02
```

| layer | ratified gate | measured | verdict | humility ceiling | capped engine, measured |
|---|---|---|---|---|---|
| **L1** Retention | F=1000, C≥995, B=1000, snapshot byte-identical | F 1000 · C 1000 · B 1000 (chronicle 50k, sessions 5k, murk 10k) | PASS | — (floor: no lower layer to cap against) | — |
| **L2** Recall | cue-C≥900, F≥950, B=1000 | cue-C 1000 · F 1000 · B 1000 | PASS | capped cue-C ≤ 100 | **capped cue-C 0** (`make_engine(1)`) |
| **L3** Forgetting | weighted-C≥850, unweighted-C≥90, F≥950, B=1000 | weighted-C 917 · unweighted-C 91 · F 1000 · B 1000 (`l3streamb`, 10× budget) | PASS | capped weighted-C ≤ 300 | **capped weighted-C 92** (`make_engine(2)`; 34 for the frozen L2 engine capped the same way) |
| **L4** Consolidation | footprint≤250, reconstruction F≥900, C≥850, B=1000 | footprint 250 · F 968 · C 1000 · B 1000 (`l4stream`, 20k) | PASS | capped reconstruction F ≤ 400 | **capped F 300** at `l4stream[:4000]`; 302 whole-stream, measured once out of suite |
| **L5** Prospection | trigger-precision = trigger-recall = 1000, dup-fire = miss = 0, F≥980, B=1000 | precision **1000** · recall **1000** · dup-fire **0** · miss **0** · F **1000** · B 1000 (`l5stream`, 20k) | PASS | capped trigger-recall ≤ 50 | **capped trigger-recall 0** (`make_engine(4)`) |
| **L6** Meta-memory | Brier≤40, ECE≤30, AUROC≥900, F≥950, B=1000 | Brier **23** · ECE **0** · AUROC **976** · F **955** · B 1000 (`l6batteryb`, 12k) | PASS | capped AUROC ≤ 600 | **capped AUROC 500** (`make_engine(5)`) |
| **L7** Generation | validity = novelty = tagging = 1000, promotion = 0 three deep, F≥950, B=1000, ECE≤40 | validity **1000** · novelty **1000** · tagging **1000** · promotion **0/0/0** · F **1000** · B 1000 · ECE **0** (`l7compose`, 12k) | PASS | capped (novel∧valid∧tagged) ≤ 50 | **capped conjunction 0** of 160 (`make_engine(6)`) |
| L8 Self-description · L9 Birth | *thresholds specified at the Phase 3→4 gate* | — | unspecified | *specified at the Phase 3→4 gate* | — |

Every gate printed by `python3 -m trials` is read out of
`trials/laws/t_rulings.py::AUTHORIZED_GATES`, the registry that binds each
threshold to a literal §5 clause or a ruling and forbids any gate constant under
`trials/` that is not in it. A number on this table that drifted from the engine
is a red trial (`trials/ops/packaging/t_scorecard.py`).

### The three upper tiers, and what a competing system would have to show

The rows above are numbers. These are the claims they are evidence for, each
stated so somebody else's system can settle it.

**L5 Prospection — a gate that is an IDENTITY, and two promises kept on the
record.** Four of the six clauses admit no margin (`precision = recall = 1000`,
`dup-fire = miss = 0`), so `R5` clause 1 rules that the upper obligation is
discharged by **exhibiting a witness that attains** it — a stronger evidentiary
burden than a strict inequality, not a weaker one. The engine's own clock is the
auditor: a firing consumes a logical `t` of its own, so 20 000 caller writes
become **20 765** logical times and `next_t − |caller stream|` is checked against
the firings the query interface reports. **Dup-fire is therefore not a number an
engine can report its way out of.**

The demonstration nobody can stage is on this repository's own history. Two
intentions were armed in the project's dogfood store and kept:
`iid 1` armed at `[L5] [DOGFOOD]` fired **eleven moves later** at `[L6] [ASCEND]`,
exactly once; `iid 2` armed at `[L6] [DOGFOOD]` fired at `[L7] [ASCEND]`. The
ledger reads **2 fired / 0 pending**. Both are visible through `§7.1` alone as a
**one-element list** — because `dup-fire = 0` is a gate clause and an intention
that fired twice has to be visible in the *query interface*, not only in an
engine's bookkeeping.

*A competing system would have to show*: a stored condition, an evaluator on the
write path, and an emission with a place in logical time — scored exactly-once
against a corpus that declares its own satisfaction points. `autopsy/GAPMAP.md`
finds prospection **absent** in all four engines read, with Letta certified
absent on the precise distinction (schedule- and turn-count-triggered
maintenance is not condition-triggered).

**L6 Meta-memory — an engine that is wrong on purpose, and says so first.**
`corpora/l6batteryb` carries 100 **mirror pairs** whose members are
observationally identical once the entity id is blanked, with a **withheld,
balanced coin** deciding which member's first assertion is true. Regenerate the
artifact with every coin bit flipped and the stream is **byte-identical** while
the answer key changes on all 200 forcing queries — so the coin is in no function
of the stream, and every reader is wrong on exactly one member of every pair. Six
readers built to break it all measure exactly 100.

So `F 955` and **not** the `F 1000` the layers below reach, by theorem and not by
defect; the engine states `500` on each of those queries before it commits, which
is `permille(1/d)` derived and not typed; and `ECE = 0` **exactly**, because bin 5
carries 200 answers at confidence one-half against an accuracy of one-half. The
model adds **no field** to the state below it.

*A competing system would have to show*: a confidence that **ranks** — `AUROC`,
not a score — on an artifact where both classes are guaranteed non-empty.
Calibration is **absent** in all four engines and both evaluators read; a
retrieval score is not a calibrated confidence.

**L7 Generation — self-tagged recall-versus-generation, with the denominator on
the artifact.** `corpora/l7compose`'s 100 mirror pairs are **twins**: they compose
to the same item but for its `entity` field, so **the value is never the signal**,
and a balanced coin decides which member's item the stream carries. Any policy
whose lineage decision is a function of the query alone mislabels exactly one
member of every pair. This engine returns the **same value** for both members and
a **different lineage** on all 100 — so nothing in the question and nothing in the
answer could have carried the decision, and `tagging = 1000` is a capability
rather than a lookup.

Both provenance crimes are committed on purpose and both are caught by the
arithmetic. `always-observed` composes all 160 generation-class answers
**correctly**, at `F 1000` with `wrong 0`, and dies at `tagging 0/160` — a policy
right about every value it returns still ends the ascension, which is the
identity clauses doing work `§3.0`'s averaging cannot. `always-generated` clears
**six of seven** and dies at `novelty 615`, because the 100 items it tags on the
observed half of every pair **are stored**. The instrument is therefore a
**confusion matrix over two declared classes** and never a single rate.

And the ladder: `§6` names the Layer-7 self-pollution strain in the
constitution's own frozen text, so the caller re-ingests the engine's own output
three generations deep and `promotion` is scored **at every rung** — `0 / 0 / 0`,
against a ledger-blind fixture that promotes **100, then 130, then all 160** and
three deep calls every one of its own dreams a fact.

*A competing system would have to show*: that it distinguishes the two channels
at all, with both classes non-empty, with the distinction **not free** (a class
readable off the query measures a lookup), read through the ordinary query
interface, and with the **artifact** supplying the denominator — self-tagging is
not self-grading. Against `autopsy/writ` at `3c0900a` the contrast is sharper
than positioning claimed: there the answer's own `cited_sources` is read by
**zero** lines of scoring, and `checkHallucination` scores a tagged generation as
a **defect**.

### THE NOVELTY HORIZON — read this before quoting `novelty 1000`

`novelty = 1000` is *"provably never-stored"*: a canonical-byte comparison
against the ingested store. After the caller writes a generation back, **the
store contains it.** Measured over the same three-rung ladder, the byte-novel
share of what the engine still calls generated falls

```
60  ->  30  ->  0
```

while `tagging` holds at **1000** and `promotion` stays **0**. At rung 3 a byte
comparison would call this engine **a liar about every item it made**, and
nothing about those items' lineage has changed — what changed is where they have
been since.

That is a failure of an **instrument**, not of an engine, and it is why
`novelty`'s denominator is bound to the items the engine **tags** rather than to
the store (`R8` clause 3(b)), why `promotion = 0` is a separate clause from
`novelty = 1000` at all, and why the capital crime's enforcement rides
**lineage** and not any comparison `§4.2` or `§3.0` can make (`R8` clause 5(c)).
`laws/t_provenance_schema.py` is exactly as green against the failure as against
its absence.

**So: quoting `novelty 1000` without saying which store it was measured against
is the citation error `HONESTY.md §6` exists to forbid.** It is the one number
here that makes that error easy. Measured by
`strain/l7::trial_novelty_stops_being_the_right_question_at_depth_and_the_ledger_does_not`;
the full note is `packaging/CATALOG.md §2.2`.

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

**The Layer-5 promise ledger has a non-capability the layer below did not.**
Neither prospection tier is reachable by **cue**: all 180 pending intentions and
all 765 firings return byte-exact from `read(t)` and **not one of the 945**
answers a cue built from its own payload. The cue channel reaches **51‰** of what
`read(t)` still answers, against 26‰ one layer down — and here the budget closes
nothing. A payload is **cue-addressable or an intention, never both**, because
the invertibility rule that *opens* the capability is the rule that closes the
channel.

**Layer 6 ships an engine that is wrong on purpose, and Layer 7 ships one that
returns items no event ever carried.** Both are stated at the tiers above and
both change how a number may be cited: `F 955` at Layer 6 is a theorem's floor
and not a defect, and `novelty 1000` at Layer 7 is a comparison against a store
that moves. Neither may be quoted beside the layers below without its reading.

**Calibration is dormant below Layer 6 — and above it, it is dormant on our own
real data.** `§3.4` binds from Layer 6 and stays bound; but on
`corpora/real-sessions` every answer the engine gives is correct, so `n_neg = 0`,
`AUROC` is **undefined**, and the confidence vocabulary the engine emits is
`{0, 1000}` — which is the signature `humility/l6/IMPOSSIBILITY.md` measures for
a **capped-5** engine. On this fuel a Layer-6 engine is indistinguishable from
one with no confidence model, because the fuel gives the model nothing to price.

**Six of the engine's own diagnostic ops answer without a provenance tag.**
`consolidation`, `count`, `profile`, `prospection`, `calibration` and `lineage`
return `provenance: null` while `forgetting` carries a valid `absent` tag beside
them, so the seam is **uneven** and not a property of `query`. `§4.2.2` has no
exception for a diagnostic, so read literally each of those scores 0 however
correct it is. **No `§5 L7` denominator contains a diagnostic query, so no gated
number moves** — and the cause is structural: `§4.2.3` admits an empty `support`
only when `kind == "absent"`, so the schema offers exactly one bearer for *"no
bounded support"*. It is recorded and deliberately **not fixed**, because fixing
it means either editing a frozen layer or minting a schema form the frozen
`§4.2.3` does not have. It is Layer 8's, squarely: at Layer 8 the untagged class
and the layer's own subject are the same class.

**Two layers are unbuilt and have NO thresholds at all.** Self-description and
birth receive laws — `§4.1`'s budget law, `§4.2`'s provenance law which binds
from Layer 7 and can never be un-bound, `§3.4`'s calibration bounds, `§2`'s
physics, `§7`'s three doors — and their gate cells read *specified at the Phase
3→4 gate*, where every other row states a number. `BOUNDARY-HIGH.md` has not
been written. Six rulings already bind it sight-unseen.

**Ordering is a design commitment, not a finding.** That memory capability is
ladder-shaped is asserted by this constitution and is established by nothing
here. An architecture reaching Layer 5 without Layer 3 would not be caught by
this benchmark; it would score 0 on Layer 3 and be right to.


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
| L5 Prospection | **not gateable**: this corpus carries no `intend` payload at all, so nothing arms and nothing fires; `dup-fire 0` and `miss 0` **tie** their clauses, which is the shape a policy that does nothing always has | n/a |
| L6 Meta-memory | **not gateable**: 25 of 25 answers correct, so `n_neg = 0` and `AUROC` is **undefined**; `R7` clause 3(a) disqualifies rather than excuses. Confidence vocabulary `{1000}` | n/a |
| L7 Generation | **not gateable**: `generate` abstains everywhere, the lineage ledger holds 0 items at 0 cells, and validity / novelty / tagging are `n/a` over **empty** denominators; `R8` clause 3(c) disqualifies | n/a |

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

**The three upper rows are `n/a` for three different reasons, and that is their
whole content.** Layer 5 because the corpus predates the store's first promise;
Layer 6 because a corpus the engine is never wrong on leaves `§3.4`'s error class
empty; Layer 7 because the store's declared reading and the composition rule's
vocabulary are **disjoint** — `count(part)` and `count(profile)` both abstain,
and the same engine composes 160 items on `corpora/l7compose`. None of the three
is a defect of a layer; all three are properties of the fuel, which is exactly
what a transfer tier is for.

### `real-sessions/v2` — the freeze was ATTEMPTED and STOPPED

The store has grown from 25 events to 50 across five more claimed layers — counted
at the freeze attempt, before this session's own ritual `remember`, which is the
same cut point `v1` used — so this `PACKAGE` move repeated `v1`'s freeze procedure
at current scale. **The procedure stopped where `v1`'s own README says a freeze
stops.** No `v2` exists; `v1`'s bytes, manifest and checksum are untouched; the
decision record is
[`corpora/real-sessions/V2-FREEZE-STOPPED.md`](../corpora/real-sessions/V2-FREEZE-STOPPED.md).

The scrub found **one** thing in 601 257 bytes: a 64-character hex run of the
`long_hex` family, sitting in the `[L4] [PACKAGE]` session summary that recorded
the freeze of `v1`. The match is **`v1`'s own corpus checksum** — this
repository's own published number, printed in that corpus's manifest, in its
README and in `BOUNDARY.log`. It is a **true positive of the pattern and a false
positive of the purpose**, and the sharpest detail is that the same decision names
three checksums and *shortens two of them*: the corpus does not carry a habit, it
carries one line where a habit lapsed, written by the session that wrote the
scrub.

Three shortcuts existed and all three are refused in the record: freeze anyway (a
frozen corpus is immutable forever, §9.2 — the one irreversible move on the
list); drop or redact the event (*"the scrub reports; it never edits"*, and a
corpus that dropped an event would stop being the snapshot the transfer tier's
honesty rests on); or narrow `long_hex` so it does not match (relaxing the
instrument to admit the finding, which is the one thing this repository never
does). **A finding stops a freeze and a human decides.** It is a decision waiting,
not a defect.

It is also the store's own oldest theme arriving at the freeze procedure: *the
store is exactly as wide as its source.* A project whose sessions write about
freezing its own artifacts writes those artifacts' checksums into its own memory,
and nothing in a 64-character hex run says which kind of hex it is.

### What the re-run found anyway — measured OUT OF SUITE, on 50 unfrozen events

The transfer re-run did not need the freeze, so it was run on the store as it
stood and is labelled for what it is: **not frozen, not in the suite, and it will
move with the next session's `remember`.** `v1`'s numbers above are the only
transfer numbers any trial re-measures, because they are the only ones bound to
bytes that cannot move.

| layer | `v1` (25 events, frozen) | the store at 50 events (out of suite) |
|---|---|---|
| L1 Retention | F 1000 · C 1000 · B 1000 | F 1000 · C 1000 · B 1000 — unchanged |
| L2 Recall | cue-C 1000, **25 of 25** uniquely cueable | cue-C 1000, **46 of 50** — and **4 are not uniquely cueable at all** |
| L3 Forgetting | n/a — 0 importance, 0 handle | n/a — still 0 and 0 |
| L4 Consolidation | footprint 151 · F **172** · 25 irreducible | footprint 198 · F **226** · 50 irreducible; the Layer-3 identity **still exact** — 7 answered, 7 retained |
| L5 Prospection | n/a — no `intend` payload exists | n/a — **3 intentions arm, none fires** |
| L6 Meta-memory | n/a — `n_neg = 0` | n/a — `n_neg = 0`, confidence vocabulary still `{0, 1000}` |
| L7 Generation | n/a — empty denominators | n/a — ledger 0 items / 0 cells |
| the inversion | reference **11** of 25 against our **2** | reference **22** of 50 against our **7** |

**Five more layers of session history did not make the store a better corpus for
the upper layers. It made the reasons they are ungradable sharper, and it cost
the store its first two unreachable memories.** Four findings, in the order they
matter.

* **The store lost its first memory to blocking, by growth alone.** At 25 events
  every summary was uniquely cueable. At 50, four are not — and one of them is a
  *session summary*: store `t=12`, the `[L2] [ASCEND] recall` line, whose every
  token is now carried in full by some other event. `FIELD.md`'s 2026-07-24 note
  said *"the store's thinnest entries are its most important ones"*; the session
  that **built recall** is now the one the store cannot find by cue. Nothing
  broke. The corpus grew.
* **The other three are the promises, and they are uncueable by construction.**
  An `intend` payload carries no `tok` field, because a fourth field would leave
  the payload canonical and stop it arming — the rule that opens the capability
  is the rule that closes the channel. `strain/l5` measures that on the binding
  corpus; here it is a property of a **real corpus**, and this is the first REAL
  corpus in the project to carry an intention at all.
* **The promises are in the fuel and the facts that would keep them are not.**
  All three arm; none fires; `next_t == 50 ==` the caller stream, so the engine's
  own clock says it emitted nothing. Their conditions watch for `attr`
  assertions, which the shell's **derived** replay produces and the store never
  holds. That is the shell/engine division of labour seen from the corpus side —
  and it is why `dup-fire 0` and `miss 0` **tie** while precision and recall are
  undefined rather than low.
* **Layer 4 still degenerates exactly to Layer 3, and the inversion held while
  doubling.** At the same cap the Layer-4 engine answers the 7 events the
  Layer-3 engine retains — the identity `v1` published, re-derived at twice the
  scale. And the reference engine that cannot forget still reconstructs more:
  **22 against 7**, where it was 11 against 2. Both engines keep doing exactly
  what they were designed to do, and on this fuel ours still keeps fewer.

---

## What it grades, and how

Everything speaks one interface (`BOUNDARY.md §7`): `ingest`, `query`,
`snapshot`, plus `make_engine(layer_cap)` for the capped runs. Trials never touch
an engine directly. A reference external engine, written against that interface
and importing nothing from this repository's core, is graded on the same rows:
it clears Layers 1 and 2, fails Layers 3 and 4, and is not measured above that —
because a zero on a layer an engine does not claim says nothing about the engine
and something misleading about the card. That is how the harness shows it is
generic *and* discriminating.

**The adapter contract is written down, including the half `§7` leaves
implicit**, and it is not restated here: `trials/adapters/README.md` carries it.
`§7` is frozen, so what a foreign adapter must supply beyond the three pure
functions was *recorded* rather than patched into the constitution —
`state.occupancy`, `state.budget_cap` and `state.next_t` read as **attributes**,
`restore(bytes) -> state` beside them, `§7.2`'s `confidence` as an **integer
permille** from Layer 6 (refused at the read, because a confidence that is not a
permille is a harness-level failure and not a low score), and from Layer 7 a
`lineage` field on a `generate` Answer that is **absent or one of
`{observed, generated}`**. That list is itself a kept promise: it was armed as an
intention in this project's own store at `[L5] [DOGFOOD]` and surfaced eleven
moves later at `[L6] [ASCEND]`, one stage after the scorer that had already
assumed it — the lateness is recorded in the document rather than tidied away.

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
supplement, eight entries) → `autopsy/GAPMAP.md` (what the prior art does and
does not do) → [`packaging/CATALOG.md`](CATALOG.md) (the failure catalog and the
four-kind impossibility taxonomy) → `core/layers/README-l7.md` (the newest layer)
→ `BOUNDARY.log` (every session ever run, append-only).

---

## Appendix — the superseded paragraphs, kept rather than edited

`BOUNDARY-RULINGS.md R6` clause 3: *"where a document states a quantity a trial
also computes, the trial's value is the enforced one, the prose stands as
written, the divergence is recorded rather than edited away."* Three dated notes
above the paragraph below superseded it, once per claimed layer, and each said in
its own text that a later `PACKAGE` move owned the rewrite. This is that move.

The paragraph and its notes are **moved, not edited**: every byte below is as it
was written, and the limitations section above now states what is currently true.
They are kept because a reading that supersedes another should have to show the
one it replaced — and because the "known problem" recorded here is the clearest
short account of a collision that took two rulings to settle.

> **Note added 2026-08-01 (`[L5] [ASCEND]`).** **Layer 5 is now claimed**, so
> the paragraph below is superseded on both of its counts and is left as written
> rather than edited (`BOUNDARY-RULINGS.md R6` clause 3's discipline: a reading
> that supersedes another should have to show the one it replaced). Three layers
> are unbuilt, not four. And the "known problem" is settled: `R5` clause 1 rules
> that an **identity** gate discharges R2's upper obligation by an exhibited
> witness *attaining* it — a stronger evidentiary burden than a strict
> inequality, not a weaker one — `R5` clause 2 reads a **minimizing** clause
> direction-aware and over the gate's conjunction, and `R6` clause 1 binds both
> sides of the Layer-5 gate to `corpora/l5stream`, where no named
> capability-free policy clears more than two of the five scored clauses. The
> engine then cleared it: trigger-precision 1000, trigger-recall 1000, dup-fire
> 0, miss 0, `F` 1000 against a gate of 980, `B` 1000 at 250‰ of the raw
> episodic footprint. **Nothing in the L1–L4 scorecard above moves**; this
> document's own counts of built and unbuilt layers do, and a later `PACKAGE`
> move owns the rewrite.

> **Note added 2026-08-02 (`[L6] [ASCEND]`, Layer 6 claimed).** **Three** layers
> are unbuilt now — generation, self-description and birth — and the paragraph
> below is superseded twice over rather than edited (`R6` clause 3). Layer 6's
> gate was cleared on `corpora/l6batteryb` per `R7` clause 1 at `Brier 23`,
> `ECE 0`, `AUROC 976`, `F 955`, `B 1000`, and the **next** open question is not
> a constitutional collision but a bequest: `R7` clause 7 records that `§3.0`
> pays an engine to convert an error into an abstention while `§3.4` cannot see
> one, closed on this artifact by arithmetic and reopening at Layer 7 where
> `§4.2` gives the price list a third way to reach 0. **Nothing in the L1–L4
> scorecard above moves.**

**Four layers are unbuilt, and Layer 5 already has a known problem.** §5 L5's
gate is an **identity** (`trigger-precision = trigger-recall = 1000`), while the
standing rule R2 requires every future gate to lie strictly *below* the oracle
ceiling on its binding corpus — and for an exactness gate the oracle ceiling is
1000. That obligation cannot be discharged at Layer 5 by the method that
discharged it at Layers 3 and 4, and it is recorded as the next open question
rather than quietly resolved.

---

> **Note added 2026-08-03 (`[L7] [ASCEND]`, Layer 7 claimed).** Two layers are
> unbuilt now — self-description and birth — and both still receive laws but
> **no thresholds** until `BOUNDARY-HIGH.md` is written at the Phase 3→4 gate.
> The `L1`–`L4` scorecard table above does not move; the `L5`, `L6` and `L7`
> tiers remain deliberately deferred to a later `PACKAGE` move, and this note
> adds no row rather than publishing one a docs-are-checked trial has not been
> written against.
>
> What a later `PACKAGE` move should carry from this layer, recorded so it is not
> re-derived: the flagship claim `autopsy/GAPMAP.md §4` axis (b) was written for
> — **self-tagged recall-versus-generation, with the denominator on the artifact
> and not on the engine's own testimony** — is now measured rather than
> positioned. `R8` clause 3 names the **fourth species** of gate clause (the
> self-reported denominator, after the identity, the minimizing clause and the
> empty domain) and rules that a denominator the engine reports about itself is
> checkable against the artifact or it does not count; the instrument is a
> **confusion matrix** over two declared classes and never a single rate, because
> both directions cost; and the contrast with `autopsy/writ` at `3c0900a` is
> sharper than the positioning claimed, since there `cited_sources` is read by
> **zero** lines of scoring and `checkHallucination` scores a tagged generation as
> a **defect**. Cite it with the commit, the artifact and the store the novelty
> was measured against, as this document's citation discipline already requires.

> **Discharged 2026-08-07 (`[L7] [PACKAGE]`).** The note above is the last of the
> four in this appendix and it is answered rather than rewritten. The `L5`, `L6`
> and `L7` tiers are published above and every number in them is re-measured live
> by `trials/ops/packaging/t_scorecard.py`, which is the condition that note set
> for adding a row. What it asked to be carried from Layer 7 is carried in three
> places: the fourth species and the confusion matrix in the Layer-7 tier, the
> `autopsy/writ` contrast beside it, and the store-the-novelty-was-measured-
> against rule promoted out of a note into a section of its own (**the novelty
> horizon**), because a citation rule buried in an appendix is a citation rule
> nobody follows.

---

*This project keeps a cultivation metaphor, quarantined in exactly one file:*
[`LORE.md`](../LORE.md).

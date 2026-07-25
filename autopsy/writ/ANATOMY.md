# ANATOMY — WRIT (Write Integrity Test)

Subject of `[L3] [AUTOPSY]`, **short format** — the seventh autopsy and the
second of an *evaluator* rather than an engine. Traced from source (schema,
evaluator, adapter interface, the whole 77-scenario corpus) in a read-only clone
outside this repo. This session discharges the one pre-publication dependency
`GAPMAP §4 (b)` recorded against itself: *"the required action before publication
is to fetch/verify WRIT, not to reword."* WRIT is now fetched and read.

**Attribution correction (this is the record; GAPMAP is not edited this
session).** WRIT is the **independent project of Mark Hendrickson**, published at
`markmhendrickson/writ` under his own name and credited to his own blog post
(`README.md:9`) — all 10 commits in the repository are authored by him. It was
posted in the comments of Penfield Labs' benchmark proposal as a **complementary**
benchmark, and WRIT's own framing agrees (`README.md:251–265`,
*"Complementary, Not Competing"*). Earlier project docs shorthand it as
**"WRIT/Penfield"**; that is a **misattribution**. The cross-reference into
`GAPMAP §4 (b)` lands in the next PULSE.

Nothing here changes the frozen constitution; a **Constitutional note** at the
end records that no law-change objection arose.

## License + commit hash examined

- **License: MIT**, declared in `package.json:23` (`"license": "MIT"`) and
  `README.md:319–321`. **There is no `LICENSE` file at the repository root** —
  the grant exists only as those two declarations. Recorded as a fact, not an
  objection; nothing is vendored from WRIT into this repo.
- **Commit `3c0900a84203fa7203fbab86952460053506a567`** (2026-06-22,
  *"feat(neotoma-adapter): memory_events-driven write path + history-preserving
  probe"*). Version **0.2.0** (`package.json:3`, `src/runner.ts:12`).
- Every line/section citation below is at that commit.

---

## Structure

TypeScript, zero runtime dependencies (`package.json:24–29` — `tsx`,
`typescript`, `vitest`, `@types/node` are all devDependencies).

| part | file | what it is |
|---|---|---|
| schema | `src/types.ts` | the whole vocabulary: categories, capabilities, failure modes, scores |
| corpus | `scenarios/*.json` | **77** hand-authored scenarios, 16 categories |
| loader | `src/loader.ts` | read + structural validation |
| grader | `src/evaluator.ts` | per-scenario scoring, failure detection, layer attribution |
| judge | `src/judge.ts` | optional LLM judge (gpt-4o-mini default), in-process cache, substring fallback |
| driver | `src/runner.ts`, `src/cli.ts` | scenario × mode loop, aggregate, optional CI thresholds |
| adapters | `src/adapter.ts`, `src/adapters/{baseline,neotoma}.ts` | the system-under-test interface and two reference implementations |

**Corpus shape.** 77 scenarios, 173 `memory_events` total (**mean 2.25 per
scenario**), 3–11 sessions each (mean 5.9). Categories: `abstention` 5,
`certification` 5, `closure` 2, `constraint` 5, `drift` 5, `entity` 5,
`extraction_drift` 5, `failure_injection` 5, `forgetting` 5, `lifecycle` 5,
`multi_hop` 5, `provenance` 5, `temporal` 5, `trust_hierarchy` 5, `update` 5,
`work_state` 5.

**Grading mechanism, measured over the corpus.** `eval_rubric.method` admits only
three values in the type (`EvalMethod`, `types.ts:74`) and `scoreResult`
dispatches on exactly two of them (`evaluator.ts:62–76`). The corpus declares
**fourteen**: `structured` 33, `exact` 18, `semantic` 6, `abstention` 5,
`constraint` 4, `multi_criterion` 3, `contains` 2, and seven singletons. Every
method the dispatcher does not recognise — 44 of 77 scenarios, including all 18
labelled `exact` — falls through to `checkRecall`, which is **case-insensitive
substring containment** (`evaluator.ts:246–267`). The remaining 33 use
`checkStructuredRecall`: the fraction of `required_elements` present as
substrings, correct at `≥ 0.8` (`evaluator.ts:269–283`). **No scenario in the
shipped corpus invokes `llm_judge`** — the judge is built but currently unreached
by the data. So WRIT as shipped is, in practice, a **substring grader**, and
`loader.ts:35–73` validates none of this: not the category, not the capability
names, not the failure-mode names, not the rubric method.

---

## Verdict 1 — Structure: flat, and *anti*-gated. Our axis (a) **CONFIRMED and sharpened.**

`ScenarioCategory` is a **flat union of 16 strings** (`types.ts:16–32`), and
`RequiredCapability` a flat union of 15 (`types.ts:34–49`). Results are grouped
by category and by mode for reporting (`runner.ts:77–112`) — **grouping, never
ordering**. There is no prerequisite relation, no capability cap, no
upper-bound assertion, no notion of a system frozen below a capability: a grep for
`gate|tier|ceiling|capped|prerequisite|depends on` across `src/`, `docs/` and
`README.md` returns only incidental matches on `AggregateScores`.

Three things come closest, and each falls short in a way worth recording:

1. **A corpus-composition convention, not an ordering.**
   `tests/scenarios/validate_all.test.ts:5–30` splits `ORIGINAL_CATEGORIES` (10)
   from `EXTENDED_CATEGORIES` (6) and requires **≥5** scenarios of the first and
   **≥2** of the second (`:126–148`). That is a coverage floor on the dataset. It
   says nothing about whether a system may attempt one category before another.
2. **Thresholds exist, but they are floors on the whole run.**
   `cli.ts:96–127` implements `--fail-below-recall`, `--fail-below-update` and
   `--fail-above-hallucination`, exiting 1 on breach. They are **caller-supplied**,
   apply to the **aggregate over all scenarios**, and are not per-capability.
   Nothing in WRIT can express *"a system frozen at capability N−1 must score **at
   or below** X on capability N."* The one threshold with a ceiling's shape
   (`--fail-above-hallucination`) bounds a **defect rate**, not a capability.
3. **The one place a system declares what it cannot do makes the gap wider, not
   narrower.** `AdapterCapabilities` (`adapter.ts:69–78`) is eight self-declared
   booleans. When one is `false`, the corresponding score is set to `null`
   (`evaluator.ts:84, 100, 123, 160–170, 172–181`), and `aggregateScores` filters
   `null` out of **both numerator and denominator** (`evaluator.ts:545–548`).
   `docs/metrics.md:204` states the policy outright: *"Metrics that return `null`
   … are excluded from aggregation — they do not penalize or inflate scores."*

Point 3 is the sharpening, and it is the inverse of our humility class rather
than a weak version of it. In WRIT, **a system exempts itself from a capability
by declaring it unsupported** — `BaselineAdapter` declares all eight `false`
(`baseline.ts:79–90`) and is therefore *not scored* on history, temporal replay
or provenance, rather than scored 0 on them. Under `BOUNDARY.md §6/§7.4` the
opposite holds: `make_engine(layer_cap = N−1)` is run through the **identical**
interface on layer N's **own** ascension tasks, must **abstain rather than raise**
(§7.3), and its abstentions are **scored** by the §3.0 table against a declared
ceiling. Our L3 measured the capped `layer_cap = 2` engine at **34‰** against its
300 ceiling; WRIT's equivalent system reports `null` and vanishes from the
denominator.

GAPMAP §4 (a) claimed impossibility-gating as novel against MemoryAgentBench's
flat leaderboard. WRIT is the second independent evaluator to lack the construct,
and the first to contain a mechanism actively pointing the other way. **Axis (a)
holds, strengthened.**

---

## Verdict 2 — Provenance: audited from outside, opt-out-able, and novelty absent. Our axis (b) **CONFIRMED, with corrections.**

**Externally probed, out-of-band — confirmed exactly.** `provenance_complete` is
computed by calling the adapter's **side-channel** method, not by inspecting the
answer:

```ts
const prov = await adapter.getProvenance(scenario.memory_events[0]!.id);   // evaluator.ts:128
provenance_complete =
  prov.source_session === gt.provenance.source_session &&                  // evaluator.ts:132–135
  prov.source_message_index === gt.provenance.source_message_index;
```

Integer equality against the scenario's authored ground truth
(`docs/metrics.md:67–78`). It is graded **only** when the probe declares
`provenance_tracing` (`evaluator.ts:125–127`) — **5 of 77 scenarios** — and always
against `memory_events[0]`, the first event, regardless of which fact the probe
actually asked about.

**Never at answer time — confirmed, and stronger than expected.** `ProbeResult`
does carry a per-answer provenance field, `cited_sources: string[]`
(`types.ts:183`), and the Neotoma adapter populates it (`neotoma.ts:273, 306`).
**No scoring path anywhere reads it** — `cited_sources` appears in the adapters,
the type, the docs and the tests, and in **zero** lines of `evaluator.ts` or
`report.ts`. An answer's own claim about where it came from is collected and
discarded. Provenance in WRIT is a property of **the store**, audited by a side
channel; it is never a property of **the answer**.

**And it is optional.** `if (!capabilities.supports_provenance)
provenance_complete = null` (`evaluator.ts:123–124`) → excluded from aggregation
(`evaluator.ts:545–548`, `docs/metrics.md:204`). A system that tracks no
provenance is not scored 0 on provenance; it is **not scored on provenance**.
Contrast `BOUNDARY.md §4.2.2`: from Layer 7, every non-abstaining answer must
carry a valid tag, and *"an answer without a valid provenance tag scores as
**wrong (0)**, regardless of whether its value is correct."* Un-optable, per
answer, forever after.

**Novelty as a sanctioned capability: ABSENT, and the sign is inverted.** A grep
for `novelty` over the entire repository returns **zero hits**. There is no
`generated` tag, no generation capability, no tagging metric, no
`RequiredCapability` or `AggregateScores` field for either. The only construct
touching invented content is the failure mode `memory_hallucination`
(`types.ts:55`), and its check is:

```ts
const containsKnownValue = [...allValues].some((v) => answer.includes(v));
return !containsKnownValue && answer.length > 0;                          // evaluator.ts:347–350
```

— where `allValues` is every value in the scenario's ground truth and memory
events (`evaluator.ts:335–345`). **Any non-empty answer that does not restate a
stored value is, by construction, a defect.** Under our L7 the same output — a
grammar-valid, provably-never-stored, tagged item — is the capability
(`novelty = 1000`, `tagging = 1000`, §5 L7). Note also that `README.md:38–44`
declares WRIT *"tests both, and requires systems to distinguish between"*
model-level hallucination and infrastructure-level memory corruption; the
implemented check is a single substring test over known values and **cannot make
that distinction** — it flags both alike, and flags a correct paraphrase alike.

**The sharpened form from the directive, confirmed and extended by one clause:**

> WRIT audits provenance **from outside** — an out-of-band `getProvenance()` probe
> against authored ground truth, opt-out-able by declaring
> `supports_provenance: false`, and never a property of the answer, whose own
> `cited_sources` field is collected and never read. Ours is a **law the system
> enforces on itself at answer time**, where an untagged answer scores 0 however
> correct its value. And ours is the only suite where **tagged generation is a
> scored capability** — in WRIT it is not merely unscored but **scored as a
> defect**, since ungrounded output is what `memory_hallucination` detects.

Axis (b) does **not** weaken to "we operationalize WRIT's proposal." WRIT
specifies no self-tagging obligation, gated or otherwise; the phase-gate condition
GAPMAP §4 (b) named for a re-scope is not met. **The flag is discharged; the axis
stands as written, in its sharpened form.**

---

## Verdict 3 — "Selective Forgetting": policy compliance, **and the metric that would measure it is unimplemented.** The directive's expected form is **corrected.**

The directive expected *"policy forgetting (`should_persist=false` items must not
persist; **Over-retention Rate**) vs budget-pressure eviction."* The first half is
right. The second half is not: **Over-retention Rate does not exist in the code.**

- `README.md:161` lists it among the diagnostic metrics: *"Over-retention Rate |
  Fraction of non-memory items that persist."*
- There is **no such field** in `ScenarioScores` (`types.ts:225–241`) or
  `AggregateScores` (`types.ts:254–270`). `over_retention` survives only as a
  `FailureMode` string (`types.ts:58`) and a name in `docs/authoring.md:166`.
- `docs/metrics.md` — the file that defines every *implemented* metric, section by
  section — has **no Over-retention section at all**.
- `detectFailures` (`evaluator.ts:407–472`) never pushes `over_retention`.
- `selective_forgetting` exists only as a `RequiredCapability` string
  (`types.ts:42`). **No branch of `scoreResult` keys on it.** The five forgetting
  scenarios are scored by `recall_correct` (plus `abstention_correct` and the
  hallucination check) exactly like every other scenario.

**Worse: over-retention is unpenalized per-scenario, not merely unaggregated.**
The one field that would catch it is `eval_rubric.forbidden_elements`, present in
exactly 5 scenarios (forgetting-001/002/003/005 and update-005). It is **not in
the `EvalRubric` type** (`types.ts:76–81`), and `checkStructuredRecall` reads
**only** `required_elements` (`evaluator.ts:269–283`). It is inert data.
Concretely, `forgetting-001-ephemeral-instructions` requires `["Alex Chen",
"architect"]` and forbids `["bullet points", "bullet point"]`; a system answering
*"Alex Chen, architect, and you asked me to respond in bullet points"* scores
`recall_correct = true`, `recall_score = 1.0`, and **no failure is detected**.
`forgetting-004` uses method `exact` and declares no forbidden elements at all.

**And the reference adapter is handed the answer.** The optional `setScenario`
hook (`adapter.ts:15–28`, `neotoma.ts:87–90`) gives the adapter the full scenario
including the typed `memory_events` — the structured truth. The Neotoma adapter's
native probe then filters with the ground-truth flag itself:

```ts
if (ev.retracted_in !== null || ev.should_persist === false) continue;    // neotoma.ts:240
```

The system under test is **told which items to forget by the key it is graded
against**, and its native probe never reads the probe prompt at all — it recites
every tracked entity's value chain (`neotoma.ts:202–276`). Combined with substring
grading, that is a structurally weak instrument for this capability.

**The precise differences from our L3, as verified — the three named in the
directive all hold, plus two more:**

1. **No budget.** A grep for `budget|capacity|evict|limit` across `src/` returns
   **zero** hits. Nothing in WRIT's schema, adapter interface, scores or metrics
   carries an occupancy or a cap. `BOUNDARY.md §4.1` binds a budget law from
   Layer 1; our L3 asserts occupancy against the cap after **every one of 10 000
   writes** and evicts *before* it inserts.
2. **No pressure.** Mean 2.25 memory events per scenario across 3–11 sessions.
   Nothing is ever dropped because something else needed the room. Our L3 runs a
   10 000-item stream against a 1 000-item budget — **10×** — and retains 914.
3. **No importance-preservation requirement.** `MemoryEvent` (`types.ts:112–122`)
   has no importance, weight or priority field, and no metric in
   `AggregateScores` is importance-weighted; every scenario contributes 1 to a
   mean. Our `weighted-C` (§3.2) is importance-weighted mass recovery, gated at
   **850‰**, reached at **917‰** against a **918‰** arithmetic oracle ceiling.
4. **(added) Forgetting by declared policy, not by decision.** `should_persist` is
   an **authored boolean on the item**. The system is asked to obey a label; it is
   never asked to *choose* among items it would rather keep. Our L3 has no such
   label: importance is derived structurally (grammar weight × distinct-reference
   count × harmonic logical-`t` recency, `README-l3 §1`), so the engine must rank
   items nobody labelled, and the victim is a computed consequence.
5. **(added) The failure points the other way.** WRIT's forgetting failure is
   retaining **too much** (`over_retention`). It has no failure mode for having
   dropped something it should have kept under pressure, because it never creates
   the pressure that would cause one. Our L3 is scored on **what survives**
   (`weighted-C`, `unweighted-C`) *and* on not corrupting it (`F = 1000`, `wrong =
   0`, `fabricated = 0`).

**Net.** WRIT's "Selective Forgetting" is **retraction / scope compliance** — obey
a *don't-remember* directive — and as shipped it is graded only by whether the
**durable** facts came back. It is the nearest neighbour to our L3 in the
literature and it is not adjacent: no budget, no pressure, no importance, no
choice. **GAPMAP's fourth axis — "removal-under-pressure is untested anywhere" —
survives contact with WRIT unchanged. WRIT is the seventh subject examined and the
seventh not to test it.**

---

## Prospective memory (axis c): **ABSENT.**

No `intend`, no trigger registry, no condition→event construct, no future-firing
anything: a grep for `intend|intention|trigger|prospect|deferred` over `src/`,
`docs/` and `README.md` returns one match — the word "Trigger" as a table heading
in `docs/metrics.md:192`. The string `prospective` appears **nowhere** in the
corpus. The many scenario prompts beginning *"Remind me …"* are **retrospective
probe phrasing** ("Remind me what you know about my relationship history"), not
intentions. Every scenario's `probe` fires **once**, at an authored session index
(`types.ts:129–135`). **`GAPMAP §4 (c)` stands: no subject implements it, and now
no evaluator scores it.**

---

## Steals (PACKAGE-bound; both survive contact with the code)

**W1 — the three-mode attribution design.** `EvaluationMode = "no_memory" |
"native_memory" | "oracle_memory"` (`types.ts:70`), implemented in
`evaluateScenario` (`:20–32`) with `buildOracleState` handing the adapter the
ground-truth state of every `should_persist` event (`:507–515`), and read by the
comparison rules at `README.md:173–176`: *Native < Oracle = memory-system failure;
Native < No-Memory = the memory system actively harms; Oracle < perfect = model
failure.* Attribution to state / retrieval / agent-policy layers follows
(`evaluator.ts:474–505`).

*Why it survives:* we already own both endpoints separately — the null-engine
(`layer_cap = 0`) baseline lives in `ops/` as an L1 sanity check (`§5 L1`), and
`RULING R2` already mandates the **oracle ceiling** be computed in an
`ATTAINABILITY.md` *before* a gate binds (L3's 918‰). WRIT's contribution is to
**report the reference points as one row on the same tasks**. The steal is
therefore a **reporting discipline**: every ascension ships
`{no-memory floor, capability-free baselines, capped-engine measurement, engine,
oracle ceiling}` together, which is what L3 already did in prose (100‰ / 100‰ /
34‰ / 917‰ / 918‰) and what PACKAGE should render as a standing table.
*Constraints:* our oracle is the **arithmetic optimum over all policies**, not a
hand-built perfect state — WRIT's oracle is the authored answer key, which is why
its Oracle mode measures the model and ours measures the ladder. And no floats:
WRIT's confidences are `number | null` in `[0,1]` (adapters emit 0.8 / 0.9 / 1.0)
and `pre_delivery_flagged` compares `result.confidence < 1.0`
(`evaluator.ts:221`); ours are integer permille (`§3.4`).

**W2 — the failure-mode vocabulary, for our strain docstrings.** 17 typed modes
(`types.ts:51–68`). The ones worth cross-referencing by name where our strains
already assert the behaviour: **`silent_drift`** (value changed with no record of
the change — our L3 aggregated forgetting record and the L4 seam),
**`false_confidence`** (high confidence on wrong or stale data — our L6 Brier /
ECE / AUROC), **`provenance_loss`** (§4.2), **`over_retention`** (the inverse of
our L3 — worth citing precisely *because* WRIT leaves it unimplemented),
**`stale_memory`** / **`retrieval_miss`** / **`incorrect_generalization`**
(L2/L4), **`authority_violation`** (derived-vs-original, our S1/S4 seam),
**`flush_corruption`** (durability under interrupted writes — a name we have no
trial for yet).

*Constraint, taken from WRIT's own drift:* steal the **vocabulary, never the
enforcement.** The shipped corpus uses roughly **60 failure-mode strings and 16
required-capability strings that are outside the TypeScript enums** (e.g.
`sensitive_data_leak`, `privacy`, `wrong_neighborhood`), and `validateScenario`
(`loader.ts:35–73`) checks neither, so the schema and the data have silently
diverged. If we adopt any of these names they get a **closed registry checked by a
`laws/` trial**, exactly as `trials/laws/t_rulings.py` already does for every
`GATE_*` / `CEILING_*` constant.

---

## Maturity evidence

| | |
|---|---|
| commit examined | `3c0900a` — 2026-06-22 |
| history | **10 commits**, 2026-04-09 → 2026-06-22, **all by Mark Hendrickson** |
| version | 0.2.0 (`package.json:3`); one archived release note (`docs/releases/completed/v0.2.0/`) |
| stars / forks / open issues | **9 / 0 / 0** (github.com repository page, read 2026-07-25 — the GitHub API is blocked by this environment's egress policy, so this is a page read, not an API read) |
| corpus | 77 scenarios, 16 categories, 173 memory events, hand-authored |
| tests | 6 files (`tests/unit/*`, `tests/integration/*`, `tests/scenarios/validate_all.test.ts`) |
| CI | `.github/workflows/benchmark.yml` — `tsc --noEmit` + `vitest run`, then a baseline benchmark run uploaded as an artifact |
| dependencies | **zero runtime deps** (devDependencies only) |
| license | MIT declared in `package.json:23` and `README.md:321`; **no `LICENSE` file** |

**Assessment.** A single-author, three-month-old, pre-1.0 benchmark with a working
harness, real CI, and a real hand-authored corpus. GAPMAP §4 (b) described it as
*"proposal-stage"* on the supplied characterization: that is **half right and now
correctable**. It is more built than "proposal" implies — the harness runs, the
scenarios load, the metrics compute. It is less settled than a maintained
benchmark: the README's schema documents 6 categories where the code has 16
(`README.md:62` vs `types.ts:16–32`), the README advertises a metric the code does
not implement (Over-retention Rate), the corpus declares fourteen rubric methods
where the grader dispatches on two, and the LLM judge is unreached by any shipped
scenario. The *design* is ahead of the *instrument*.

**One honest credit, recorded because it is a third-party corroboration.** WRIT's
own landscape survey (`README.md:229–265`, covering LoCoMo, LongMemEval, BEAM and
AMB) reaches independently the conclusion GAPMAP reached from four engine traces:
*"Every widely used AI memory benchmark tests retrieval… None test write
integrity"* (`README.md:231`). That is our **"recorded but never binding"** thesis
arrived at from the evaluator side by someone who never read our notes. The
diagnosis agrees. The remedy is where we differ, and the difference is the whole
of axis (b): **WRIT proposes to audit the store from outside; we make the answer
carry its own tag or score zero.**

---

## Constitutional note

No objection to the frozen `BOUNDARY.md` or to `BOUNDARY-RULINGS.md` arose from
this autopsy. Nothing frozen was read as wrong. The one documentation item found
— the `"WRIT/Penfield"` misattribution in earlier project docs, and GAPMAP §4 (b)'s
now-dischargeable unverified flag — is an **erratum in non-frozen documentation**,
recorded here and to be reconciled at the next **PULSE**; `autopsy/GAPMAP.md` is
**not edited this session** (one move per session, `§9.1`). WRIT itself was cloned
read-only into the scratchpad and nothing from it was vendored, copied, or
committed into this repository.

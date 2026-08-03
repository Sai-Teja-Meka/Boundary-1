# STAGE-B.md — the Layer-7 Stage-B record: the batteries, the denominators, the restraints

`[L6] [ASCEND]` generation, **Stage B**. `BOUNDARY-RULINGS.md R2`'s standing step
orders an ascension *attainability arithmetic → trials → engine*, and this is the
middle step: the ascension battery, the humility battery and the inheritance
battery are written and run against an engine that **does not exist**, so that no
threshold, no reading and — at this layer above all — **no denominator** can be
tuned to something an engine already does.

`core/layers/l7_generation.py` does not exist. `trials/adapters/l7.py` does not
exist. `trials/strain/l7/` does not exist. The standing checkpoint this session
leaves behind is the one Layers 4, 5 and 6 left behind at the same point:
**humility green + ascension skipped**.

**Nothing here asks a human for anything.** `R8` is ratified and settles the
substrate, the three denominators, the `generate` reading, `§4.2`'s three
blindnesses, `ECE`'s denominator, the humility conjunction and `R7` clause 7's
bequest; §7 records explicitly that this session found no binding gap `R8` does
not cover, and drafted no `R9`.

**`§6`'s mandatory Layer-7 self-pollution strain is not written here.** It is
Stage D's by the constitution's own schedule — `§6` names it in the strain class,
and the strain class is where an ASCEND writes it, after the engine exists. The
artifact already carries what it will need (30 ladder chains, three generations
deep, with lineage decidable from the frozen bytes), and `R8` clause 5(c) already
rules that `promotion = 0` is enforced by the battery **and** by that strain and
never by `laws/t_provenance_schema.py`. The ascension battery applies the clause;
the strain will attack it.

---

## §1. What Stage A left, and what only Stage B can add

Stage A scored **policies**: pure maps from a payload list to an `Answer`,
computed from the frozen artifact with no engine in the loop. `R8` clause 1 then
bound both sides of the Layer-7 gate to `corpora/l7compose` and recorded the
fifth substrate kill. What a policy cannot exhibit, and what these batteries are
for:

1. **The tag is read through `§7` alone.** A policy's `lineage` was a field in a
   dict this project wrote; an engine's is a field in an `Answer` the engine
   wrote, and `_l7score._ask` reads it there and nowhere else. `autopsy/writ`
   records the shape not to reproduce — provenance probed **out of band** by
   `getProvenance(memory_events[0])` on 5 of 77 scenarios and opt-out-able, while
   the answer's own `cited_sources` is read by zero lines of scoring
   (`evaluator.ts:128-135`). The standing precedent for reading it in the Answer
   is Layer 5's `{op:fired,iid:I}`, which answers with a **list** because
   `dup-fire = 0` is a gate clause.
2. **`B = 1000` after every write.** A lineage ledger is state (`§4.1`), priced
   by name at 320 cells by `ATTAINABILITY.md §7`. The budget law refuses
   mid-stream, so it is certified mid-stream.
3. **The promotion ladder is driven through `ingest`.** The caller re-ingests the
   engine's own generations, three deep, into the live state — suggestibility in
   `autopsy/GAPMAP.md §6`'s literal sense — and the store's canonical bytes grow
   with it, so at rung 2 a depth-1 generation genuinely **is** in the store.
4. **The layers below are re-asked at cap 7** (`trials/inheritance/l7/`),
   including — new at this layer — `§5 L6`'s calibration battery.

## §2. The declared query vocabulary

`corpora/l7compose` speaks **two** query shapes:

| | query | answer |
|---|---|---|
| **generate** | `{"op":"generate","cue":{"kind":"profile","entity":E}}` | the compound's `profile` item, its lineage, its confidence and its tag |
| **current** | `{"op":"current","entity":E,"key":K}` | the value in force at the end of the stream — a Layer-4 verb, unchanged |

`generate` is a **`query` op** and not a fourth verb (`R8` clause 2): `§7.1`
declares three operations and `§1.1` says events are the only fuel. The `current`
class is 1 740 of the 2 200 queries and is carried for the reason the Layer-6
battery carried Layer-4 verbs — a layer's battery must still contain the
questions the layers below answer, or an engine could buy its new capability with
an old one. It is also what keeps `§3.4`'s denominator from being a function of
the generation class alone, which is the property `R8` clause 6 rests on.

`ops/l7/t_stage_b.py::trial_the_declared_query_vocabulary_is_the_one_the_battery_speaks`
asserts the vocabulary over the frozen records, engine-free.

## §2.1 The Answer, and the one field Layer 7 adds

`§7.2` declares four keys; `R8` clause 2 ratifies that a `generate` Answer
*"carries the item, its confidence, its provenance tag and its lineage"*, and
clause 4 rules `generated` a property of the **item**, orthogonal to `§4.2.3`'s
closed four-kind vocabulary, which says how an answer reached the **caller**. So
the closed vocabulary is not violated and no fifth `kind` is minted.

`_l7score._ask` enforces the contract at the read:

| | rule | why it is a harness-level failure and not a low score |
|---|---|---|
| the four `§7.2` keys | present on every Answer | `R8` clause 2 **adds** `lineage`; it replaces nothing |
| `confidence` | integer permille in `[0, 1000]` | Layer 6's requirement, unchanged; `§2.2` forbids the float independently |
| `lineage` | **absent, or one of `{observed, generated}`** | an absent claim is lawful and is scored as untagged; a value outside the vocabulary is a contract violation (`§7.3`'s categorical distinction) |
| an abstention | carries no lineage | `§7.2`'s own `value: null` rule, applied to the field beside it |

## §3. The three denominators, applied (`R8` clause 3)

`§5 L7` states three ratios and **no denominator for any of them** — the fourth
species of gate clause this ladder has had to name, after `R5` clause 1's
identity, `R5` clause 2's minimizing clause and `R7` clause 3's empty domain.

| ratio | denominator | numerator | checked by |
|---|---|---|---|
| `tagging` | the declared **G** queries the engine **answers** | those answered with lineage `generated` | the artifact's class table |
| `novelty` | the items the engine **tags** `generated`, in any class | those whose canonical bytes appear nowhere in the ingested store | the harness, over frozen bytes |
| `validity` | the same set | those satisfying the declared item grammar | the harness, over that grammar |

**And the holding itself is asserted as law, not merely applied.**
`assert_self_reported_denominators_are_checkable` is clause 3(a)'s two conditions
made a check: every member of the self-reported set is read off the `Answer` and
then checked by the harness, and the set cannot be shrunk without failing
`tagging`, whose denominator is the artifact's. **An empty denominator is `n/a`,
and `n/a` DISQUALIFIES** — stated as law in
`trial_the_three_capability_ratios_are_identities_on_the_bound_denominators`, in
the entry's own words rather than as a paraphrase:

> A gate is an instrument. An instrument has a range, and outside it the honest
> output is not a pass but a refusal to certify: a balance that reads `----`
> under an out-of-range load has not weighed the object.

`§3.4`'s own denominator is declared class by class in `_l7score.DENOMINATOR` and
reconciled on every scored run (`R7` clause 2, carried forward to a battery that
now has capability ratios beside its calibration):

| class | n | in `§3.4`'s denominator | why |
|---|---:|---|---|
| **KG1** | 100 | yes | the forcing region's generation-required members, the whole region unsampled |
| **KO** | 100 | yes | the observed twins — the class that makes the instrument a confusion matrix |
| **KG2 / KG3** | 30 / 30 | yes | the self-pollution ladder |
| **KR** | 1 740 | yes | ordinary retrieval; what keeps `§3.4`'s `A` from being a function of the G class |
| **KU1** | 100 | **no** | generation-shaped unanswerable probes: composing anything is a fabrication |
| **KU2** | 100 | **no** | never-asserted current-value probes |

A class declared outside is **not a hiding place**, and at this layer the point is
sharper than at Layer 6 because `KU1` is generation-shaped: an engine that read
*generation-shaped* as *generate anyway* is caught by `fabricated = 0` and by the
reconciliation, and by no capability ratio at all.

`F`'s denominator is the **answerable core**, the stricter of the two and the one
every piece of `R8` clause 8(b)'s window arithmetic is stated in
(`F = 1000 − 900g`). `F_all` over the whole 2 200-query set is computed and
reported as the ungated diagnostic.

## §4. The restraints, recorded now rather than discovered later

Layer 5's Stage B recorded one over-tightening it caught and removed — `wrong = 0`
asserted beside `F ≥ 980` would have gated at 1000 under a 980 clause — and Layer
6's declined to require the tie's own 500. **This session caught three, and all
three were found by running the battery against a mock rather than by reading
it.** Each is a place where a battery would have gated something `§5 L7` does not.

1. **`tagging_all` was required at 1000 and is now REPORTED.** `R8` clause 3(d)
   makes the stricter number an **ungated** diagnostic in the shape `R3` gave
   `F_strict` and `R4` clause 4 gave `F_corruption` — *"it binds nothing"* — and
   clause 3(e) computes exactly what that buys: an engine may hedge up to **111**
   of the 160 and still clear `F ≥ 950`, leaving a tagging denominator of 49.
   Requiring the diagnostic at 1000 would have gated the number the ruling made
   ungated, and would have killed a policy the entry's own arithmetic admits.
2. **The promotion ladder required all 160 still generated at every rung and now
   requires only that the count does not FALL.** The anti-silence guard is real —
   a promotion count of 0 bought by ceasing to call one's own generations
   generated is promotion by attrition — but requiring 160 gated the *count of
   generations* where `§5 L7` gates their promotion.
3. **Relevance was checked over the whole declared class and is now checked over
   the answers the engine TAGGED.** `R8` clause 5(b) binds it *"for an answer
   tagged `generated`"*; the population is the tagged set, and requiring 160 was
   the same over-tightening as (1) wearing a provenance clause's clothes.

Two more things in the battery **look** like additions and are not:

* **different lineages on the two members of a mirror pair.** `tagging = 1000`
  requires the G member tagged; `novelty = 1000` forbids tagging the O member,
  whose item **is** in the stream. So it is the conjunction of two ratified
  clauses stated where it is visible, and it is stated separately because it
  names the **cause**: the two cues differ in nothing the query carries.
* **`fabricated = 0`.** `§7.3` is the cardinal rule and `§3.0` prices a
  fabrication at 0 while paying 1000 for the abstention it displaced. The battery
  states it; the price list already did.

And one thing the battery deliberately does **not** measure: **a confidence on a
generated item.** `ATTAINABILITY.md §6.2` records that composition here is
deterministic and correct, so `1000‰` on a generated item *is* right and every
named policy scores `ECE = 0` exactly — so `README-l6 §4`'s
`CERTAIN`-by-fall-through residual is **not exercised and not closed**, and no
later session may quote this battery's `ECE = 0` as evidence otherwise.

## §5. `ECE` under both readings, and what the clause is FOR

`R8` clause 6 rules `ECE ≤ 40` over `§3.4`'s **own** denominator — the answered
queries — because the alternative available reading (`§5.1 L7`'s *"confidence on
generated content stays calibrated"*) has a denominator an engine can **empty**
by hedging one class, which is the exact shape clause 3(c) disqualifies reached by
another route. The battery therefore gates the ruled quantity and **computes the
declined one beside it**, gating nothing: `ece_generated` reads `n/a` precisely
when an engine tags nothing, which is the property that makes it emptiable and is
the whole content of the clause. Keeping it visible costs one line and is the
cheapest way to stop a later session from re-litigating a reading by forgetting
which one was taken.

**And what the clause is for is recorded**: `§5 L6` gated `Brier`, `ECE` and
`AUROC`; `§5 L7` keeps exactly one of the three, and it keeps the one Layer 6
**measured** to discriminate against nothing, twice, on two artifacts. `ECE ≤ 40`
is **a floor against incoherence, not a discriminator**, and `R2` obligation 2
does not rest on it — it rests on `novelty` and on `F`. `Brier` and `AUROC` are
computed and reported and `§5 L7` cites neither, so an undefined `AUROC` engages
no clause: `R7` clause 3(a)'s `n/a` law binds a gate that **cites** AUROC.

Worth recording because it was measured rather than predicted: the floor **does**
bite. A mock that fabricated on the 100 generation-shaped `KU1` probes took `ECE`
to `1/21 → 48` and failed the clause — confident, wrong, and incoherent in
exactly the way a floor is for. Four other clauses caught it too; none of them is
`ECE`, and that is the difference between a floor and a discriminator.

## §5.1 The battery was validated against a MOCK `§7` engine before it was frozen

A fully engine-gated battery is a battery nobody has run, and a gate never shown
attainable is exactly what `R2` exists to prevent. So the Layer-5 and Layer-6
Stage-B discipline was repeated: a mock `§7` engine — the frozen Layer-6 engine
wearing the exhibited witness's composition — was bound as `adapters.l7` **in the
scratchpad, never committed**, and the whole of Stage B was run against it.

* **Clean mock: every ascension trial GREEN**, every inheritance trial GREEN at
  cap 7, and `humility/l7`'s `§7.4` confirmation GREEN. That is the check that
  matters — a battery the exhibited witness could not clear would be measuring
  something `ATTAINABILITY.md` never showed reachable.
* **The lawful-hedger boundary, checked in both directions.** A policy hedging
  `k = 111` of the 160 — the last row `R8` clause 3(e) says clears `F` under the
  exact reading — clears the **whole battery**, which is what the three restraints
  above were removed to make true. At `k = 112` exactly one trial goes red, and it
  is `F`, at `1187/1250 = 950` in permille and a failure exact: `R7` clause 4's
  first Layer-7 instance, met on an engine.
* **Eight deliberate breaks, each RED on the right trial:**

| break | what goes red |
|---|---|
| **ledger-blind** — the ledger stops being read | the promotion ladder, at depth 1, promoting **100** |
| **always-observed** — compose everything, tag nothing (the capital crime) | `tagging = 0/160`, the untagged-generation count, the ratios, the region trial, the denominator check — five ways, while `F_core` stays **1000** |
| **always-generated** — tag the observed twins too | `novelty = 8/13 → 615`, the confusion matrix's other off-diagonal, plus relevance and the region trial |
| **blanket hedger** | `F` at 883 **and** the three ratios at `n/a`, which disqualifies — both horns, unlike Layer 6 where the region trial was correctly silent |
| **fabricator on `KU1`** | `fabricated`, the declared-outside reconciliation, `F_all < F_core`, and `ECE` at 48 |
| **float confidence** | every trial, at the `§7.2` read |
| **irrelevant support** (`[0,1,2]`, schema-valid) | relevance alone — `§4.2` accepts it, and the artifact-bound check is the only thing that does not |
| **lineage outside the vocabulary** | every trial, at the read — a contract violation and not a low score |

**And the mock found the one thing Stage B could not have read off a document:
`promotion = 0` forces the lineage ledger to be written by `ingest`.** `§7.1`
makes `query` pure, so an engine cannot record what it **answered** — only what it
**received**. Stage A's witness is a policy and records at answer time; an engine
cannot, and a Layer-7 engine that tried would be reaching for a mutation `§2.1`
forbids. What is decidable at ingest on this artifact is recorded here for Stage
C rather than left to be rediscovered: an arriving `profile` payload is one of the
engine's own iff an identical item **modulo `entity`** is already held (the
mirror twin, which is what makes a depth-1 re-ingestion recognisable) or its
composition hops through a compound component the store does not carry as an
unmarked observation (which is what makes the ladder above it recognisable). That
is an **engine design** question and not a reading, so no ruling is drafted for
it; what Stage B owes is the measurement that the clause is reachable at all, and
it is.

## §6. The recorded figures

Measured this session on `adapters/l6` — `make_engine(layer_cap = 6)`, the capped
engine — through `§7` alone, and identical to `ATTAINABILITY.md §6.1`'s
`make_engine(6)` row, because `t_attainability.py::trial_the_blanket_hedger_is_the_capped_engine_measured`
establishes that that row **is** the capped engine rather than a model of it.
Recomputed and required verbatim by
`ops/l7/t_stage_b.py::trial_stage_b_records_the_figures_the_instrument_computes`;
under `R6` clause 3 the instrument is the enforced value.

```
CAPPED conjunction 0 F_core 883 F_all 894 ece 0
DENOM A 1740 n_pos 1740 n_neg 0 abstentions 460 N 2200
CLASS G 160 O 1840 U 200 answerable 2000
LEDGER validity n/a novelty n/a tagging n/a tagging_all 0
```

The capped engine's occupancy at `DEFAULT_BUDGET` is **91 226** with
`refused = 0`, and its confidence vocabulary on an answer is exactly `{1000}`.
The ceiling is `capped (novel ∧ valid ∧ tagged) ≤ 50`: **neither breached nor
vacuous**, sat at 0 by arithmetic, and read by `R8` clause 7 as eight items of
slack for a partially capable engine `§7.4` does not produce.
`humility/l7/IMPOSSIBILITY.md` is the structural argument `§6` requires for it,
and it is the **fourth kind** in the ladder — absent bits (L4), absent machinery
(L5), absent order (L6), **absent generativity** (L7).

**ONE DIVERGENCE RECORDED RATHER THAN EDITED AWAY** (`R6` clause 3, whose rule is
that where a document states a quantity a trial also computes, the trial's value
is the enforced one and the prose stands as written): `ATTAINABILITY.md §7`
states the capped engine's occupancy over the same 12 000 events as **91 233
cells**; the engine measures **91 226**. Stage A's own trial computed the figure
without asserting it, so nothing was wrong and nothing was checked; it is asserted
now, in `humility/l7/t_generation.py::trial_the_capped_run_is_in_budget_and_the_lineage_ledger_cost_nothing`.
No claim moves with it: the ratio `ATTAINABILITY.md §7` draws — the 320-cell
lineage ledger as a share of that occupancy — is 3.5 permille of either figure.
This is the third instance of the seam `R6` clause 3 generalized from the 270/271
one, after `corpora/l5stream/grammar.md`'s closing block.

The inheritance identities and thresholds were verified attainable before being
frozen, by running the whole cap-7 class against the mock: the Layer-1 verbs,
`§5 L2`'s cue gate, `§5 L3`'s retention battery on both frozen pressure streams,
`§5 L4`'s consolidation battery on `corpora/l4stream`, `§5 L5`'s prospection
battery on `corpora/l5stream` and — new at this layer — `§5 L6`'s calibration
battery on `corpora/l6batteryb`, all green.

## §6.1 The Layer-6 inheritance row is the first that is not an identity in budget

Every other inherited row becomes an identity when nothing is under pressure —
everything recalled, everything reconstructed, every intention fired exactly once
— because those capabilities are exact and pressure is the only thing that can
cost them anything. `§5 L6`'s are not: on `corpora/l6batteryb` the engine is wrong
**exactly 100 times by theorem** (`R7` clause 3(b)), whatever the budget. So the
row re-applies `§5 L6`'s ratified numbers unchanged — `Brier ≤ 40`, `ECE ≤ 30`,
`AUROC ≥ 900`, `F ≥ 950`, `B = 1000` — which is the class's rule 3 read in the
direction it is less often read: *the old gates, not new ones*, and where the
inherited claim is a threshold, the threshold is what is inherited.

It is also the row generation could actually break, and the mechanism is named
rather than assumed: `README-l6 §4` records that a generated item has no chain,
no distinct-value count and no set-once status, so a Layer-6 `confidence_for`
falls through to `CERTAIN` on it — *"exactly the wrong answer and the first thing
a Layer-7 engine must replace."* An engine that replaced it by widening the tie
reading, or by routing the whole answer surface through a new model, would move
confidences on chains that have nothing to do with generation, and `AUROC ≥ 900`
is where that lands. `ascension/l7` scores `ECE` and nothing else of `§3.4`'s
triple, so **this row is the only place the ranking is still asked for**.

## §6.2 The class now carries six layers of history per replay

The Layer-3 rows run above an aggregated forgetting record; the Layer-4 rows above
an interval table and a demotion counter; the Layer-5 rows above a **two-tier
prospection ledger** — a pending set and a fired ledger, both outside every
eviction phase on purpose — and the Layer-6 rows above a **zero-state confidence
view**, a model that adds no field to the state it reads. A Layer-7 engine
inherits all of it at once, and a lineage ledger is new state beside all of it.

## §7. No `R9` is drafted, and the absence is reported rather than left unstated

The directive's fourth item is conditional: *only if a genuine binding gap
surfaces that `R8` does not cover*. **None surfaced.** Every question this session
had to answer was already answered, and by whom is worth recording, because the
whole point of `R2`'s ordering is that Stage B should not be discovering law:

| what Stage B needed | where it was already settled |
|---|---|
| which artifact both sides bind on | `R8` clause 1 |
| what happens to the artifacts the fifth kill refused | `R8` clause 1 — a refusal to bind, nothing demoted |
| whether `generate` is a fourth verb | `R8` clause 2 |
| the denominators of the three ratios, and what `n/a` means | `R8` clause 3 |
| where the `generated` marker may live, and whether it mints a fifth `kind` | `R8` clause 4 |
| what `§4.2` demands, and what it cannot see | `R8` clause 5, all three blindnesses |
| which denominator `ECE ≤ 40` is computed over | `R8` clause 6 |
| what the humility conjunction measures, and how to read the 50 | `R8` clause 7 |
| whether `§3.0` discourages generation | `R8` clause 8 — it does not; the identities govern |
| how `R2`'s two obligations are read at this layer | `R5` clauses 1–4, forward-binding in their own text |
| exact or permille, and the ECE bin index | `R7` clauses 4 and 5, applied unchanged by `R8` clause 6 |
| what a firing does to `next_t` on the inherited Layer-5 row | `R6` clause 2 |
| whether `F` takes a concession under eviction | `R3` does not reach Layer 7, and none is requested |

Three items are **open and deliberately not taken**, and none is a gap in `R8`:

* **how a Layer-7 engine keeps its lineage ledger.** `§5.1` above records what
  Stage B measured — `query` is pure, so the ledger is written by `ingest` — and
  stops there, because it is an **engine design** question and not a reading. `R8`
  clause 4 rules the lawful *placement* and leaves the rule to Stage C.
* **the composition access path.** `ATTAINABILITY.md §7` disclaims it with its
  reason: `part` and `profile` have no Layer-4 facet, and whether a Layer-7 engine
  extends the declared facet map or buys `README-l4 §0.1`'s second index at 343
  permille is a Stage-C question **no in-budget battery can decide**, `§5 L7`
  stating no footprint clause.
* **the loss-accounting reserve**, disclaimed with the failure it fears named —
  *a generation whose support has been shed cites a `t` the forgetting record can
  only count*, which is `§4.2` blindness (a) meeting eviction. The
  support-recoverability diagnostic exists so that the number cannot quietly fail
  to exist when pressure arrives; in budget it reads 1000 and is uninformative,
  which is stated rather than hidden.

## §8. Where Stage B lives

| file | what it carries |
|---|---|
| `trials/_l7score.py` | the shared instrument: replay, `§7.2`-and-`lineage`-enforcing observation, the three capability ratios on `R8` clause 3's denominators, `§3.1` fidelity, `§3.4`'s quantities, the per-class denominator declaration, the promotion ladder, the region profile, and the two `§4.2` checks the schema cannot make. Imports its measures from `_l7tasks` unchanged — one ruler for an engine and a policy |
| `ascension/l7/t_generation.py` | the gate on `corpora/l7compose`, **all engine-gated skips** |
| `humility/l7/t_generation.py` + `IMPOSSIBILITY.md` | the ceiling on `make_engine(6)`, **green this session**, and the fourth kind of impossibility |
| `inheritance/l7/t_inheritance.py` | Layers 1–6 re-asked at cap 7, in budget — engine-gated, plus the class's engine-free wiring check |
| `ops/l7/t_stage_b.py` | the half of Stage B that can be run without an engine: one instrument, the vocabulary, the lineage reading, the denominator declaration, this document |

# Layer 4 — Consolidation (episodic → semantic derived schemas)

`[L4] [ASCEND]`. The fourth capability of Boundary-1: Memory. Layer 1 retained
and refused; Layer 2 recalled by content and still refused; Layer 3 **dropped**,
and what it dropped left no trace at all. Layer 4 **derives** — it folds every
event, at the door, into a schema cheaper than the episode it came from, so an
episode can be released *because its content already lives somewhere else*, and
the answer to a question about it can be **reconstructed** rather than recalled.

This document states **exactly what Layer 4 can and cannot express**. Layer 5's
humility trial is written against the boundary drawn in §5.

Intellectual pedigree: Soar's episodic→semantic split and episodic reconstruction
(Nuxoll & Laird 2007, 2012) and semantic abstraction (Tulving 1972) —
`autopsy/theory-actr-soar/BRIEF.md §4`, `autopsy/GAPMAP.md §6`. The supersession
mechanism is Graphiti's bitemporal edge model (GAPMAP **S3**) with its two LLM
calls replaced by integer interval arithmetic. The demotion mechanism is Letta's
hot/cold tiering in the constitutional form `README-l3 §0.4` chose and deferred:
GAPMAP **S4** form B, *demotion-into-consolidated-form*. Soar chunking
(procedural learning) is out of scope and stays out.

Code (frozen after this session, §9):
- `core/layers/l4_consolidation.py` — the `L4State` (interval table, key atlas,
  global counters, per-entity irreducible counts, derived rows, handle index,
  demotion counter, the inherited forgetting record), the facet map and its
  inverse, the four-phase eviction path, the Layer-1/2/3 verbs, and the
  checksummed snapshot/restore.
- `trials/adapters/l4.py` — the Layer-4 adapter. `core/engine.py`,
  `core/layers/l1_retention.py`, `l2_recall.py` and `l3_forgetting.py` are
  **untouched**; `anchors/l1.json`, `l2.json` and `l3.json` replay through their
  own adapters unchanged.

---

## §0. The budget decided the state, before the code (BOUNDARY-RULINGS.md R2)

Stage A did for the *gate* what `README-l3 §0` did for the *engine*: it computed
what the budget admits before anything bound. `trials/ascension/l4/
ATTAINABILITY.md §4` **exhibited** the witness — the exact interval table plus
the global counters, `40 737` of `43 300` cells on `corpora/l4stream` — and
recorded the consequence for this session in one number:

> *"The engine's working room is **2 563 cells — 5.9% of the budget**. Everything
> the Stage-C engine needs beyond the bare interval table (any index, any
> derived-vs-episodic marking, any bookkeeping the Form-B eviction path requires)
> comes out of that, and the irreducible tier competes for the same cells. This is
> the Layer-4 analogue of Layer 3's 14-item margin: tight by arithmetic, not by
> choice."*

Every design decision below is that number spending itself. The arithmetic is
asserted in `trials/ops/l4/t_l4_composition.py`, not trusted.

### 0.1 Consequence (a) — a second access path is unaffordable. CONFIRMED.

The interval table indexes `(entity, key) → history`, which is what Q1
(current-value) and Q2 (as-of) ask. Q4 (reconstruction) asks the **inverse**:
given `t`, which pair asserted it? An exact `t → pair` index costs **one cell per
assertion**, and the schema then costs three cells per assertion rather than two:

| schema | cells on `l4stream` | footprint |
|---|---|---|
| identification + `2 × assertions` (one access path) | 40 543 | 234‰ |
| identification + `3 × assertions` (both) | **59 331** | **343‰** |
| the ratified gate | ≤ 43 300 | ≤ 250‰ |

A two-way index overruns the entire Layer-4 budget by 37% **before a single
irreducible event is stored**. It is not merely expensive; it is *excluded*, in
exactly the sense §0.2 of `README-l3` excluded the Layer-2 index one layer down.

So the schema carries **one** index and `read(t)` **searches** it:

> **Reconstruction is a sweep, not a lookup.** Every chain is a map keyed by `t`,
> so testing one pair is a single hash probe, and `read(t)` probes the pairs until
> one answers. Query time pays; **state does not**, and only state is budgeted
> (§4.1) — `README-l3 §0.2` made the same trade for its handle index, but there it
> was a choice and here it is a consequence.
>
> Two things keep the sweep from being ruinous, and both are free:
> * **key-major nesting.** The table is `{key: {entity: {t: value}}}`, not
>   `{entity: {key: …}}`. The attribute-key vocabulary is closed and small (16 on
>   `l4stream`, 17–18 on the chronicle family) where the entity population is not
>   (200 here, **9 985** on chronicle), so identification costs `keys + pairs`
>   instead of `entities + pairs` — **184 cells cheaper here, 9 967 on
>   chronicle** — and the sweep runs over a dozen large maps instead of thousands
>   of tiny ones.
> * **the covered floor.** Within a key, entities sit in first-assertion order, so
>   a key's first entity carries that key's smallest first-`t`, and the minimum
>   over the key vocabulary is the earliest `t` the whole table still covers
>   (`covers_from`). A reconstruction below it abstains in `O(keys)`. It costs
>   **no cells** — it is read off the table's own ordering rather than stored,
>   which is the only kind of index this budget can afford.

The bill is stated rather than hidden: **the suite pays for the missing inverse
index in wall time**, most of it on `chronicle`, where 50 000 reconstruction
queries sweep ~29 000 surviving pairs. That is §0.1's trade seen from the other
side, and it is the honest price of a 250‰ footprint.

### 0.2 Consequence (b) — the episode and the schema cannot both be kept

A retained episode costs `event_cost + 1`; the schema costs ~2.17 cells per
assertion. Holding both for 20 000 events is roughly **4× the cap**. So the
episodic tier is **demotable**, and this is where `README-l3 §0.4`'s recorded debt
comes due:

> **L3→L4 co-design intent** (`README-l3 §0.4`, quoted): *"S4's other
> constitutional form — demotion-into-consolidated-form, where eviction compresses
> an item into a derived schema so cold growth is bounded by compression rather
> than by a second budget — is deferred to Layer 4, deliberately, because it
> cannot be built before consolidation exists. … a cold tier is only affordable if
> a cold entry costs materially less than an event, and the only thing in the
> ladder that makes an entry cheaper than the event it came from is L4
> compression."*

Layer 4 pays it in two currencies at once:

* **supersession compression** — a pair asserted `c` times costs `1 + 2c` cells
  against `9c` raw. This is what the gate measures and what `l4stream` was frozen
  to supply.
* **schema compression** — an event no chain can absorb is still stored as a
  **derived row**: its shape (`kind` + field names) is paid for **once**, and the
  event itself costs `1 + fields` cells. An `l4stream` `note` costs 3 cells
  against 7 as an episode; an `l3streamb` `item` costs 5 against 11. The grammar
  is priced once instead of once per event.

The second currency is what makes the Form-B claim measurable on a **Layer-3**
corpus, where there is no supersession at all (§2.4).

### 0.3 Consequence (c) — the shedding unit is the chain, and the entity is marked

When the derived schema *itself* does not fit — `chronicle` needs 384‰ of its raw
footprint to hold its own history, `murk` 364‰ (`ATTAINABILITY.md §5`) — something
in the schema has to go. The unit is a whole supersession chain, oldest-
established first, and the entity that owned it is marked `damaged` in the same
breath:

* current-value and as-of stay **exact** for a damaged entity, because shedding
  only ever removes a *prefix* of a pair's history: the latest assertion ≤ `T` is
  either still there and correct, or absent and abstained. It is never a
  different assertion.
* the action-count **profile** can no longer be folded exactly, so it
  **abstains** forever after. A fold over what survived would be a confident
  undercount — 0 under §3.0 where an abstention keeps 100.

That asymmetry is the whole reason the mark exists, and it is why the unit is the
chain and not the pair-half.

### 0.4 The composition, and what it reaches

Measured on `corpora/l4stream` at the ratified cap of 43 300 cells:

| component | cells |
|---|---|
| interval table (16 keys, 2 951 pairs, 18 788 assertions) | 40 543 |
| global per-kind counters | 10 |
| **the schema the battery strictly needs** | **40 553** |
| key atlas (`key → kind`, 16 entries) | 32 |
| per-entity irreducible counts (200 entities × `note`) | 600 |
| shed-chain marks | 0 |
| demotion counter | 1 |
| aggregated forgetting record (width 2 048, 10 buckets) | 23 |
| **bookkeeping the witness did not price** | **656** |
| derived rows — 498 surviving `note` episodes at 3 cells | 1 497 |
| handle index (91 atoms + 498 postings) | 589 |
| **the irreducible tier the remainder bought** | **2 086** |
| **total** | **43 295 ≤ 43 300** |

Key-major nesting recovers **184** cells against Stage A's entity-major witness,
so the working room is **2 747** rather than 2 563. It is spent 656 on bookkeeping
and 2 086 on episodes, leaving **5 cells**. That is where the 2 563 ran out, and
the answer is not dramatic: the layer's real cost is the interval table, and
everything else is the change from it.

---

## §1. The derivation law (structural, exact, invertible)

Consolidation is **not** summarization and **not** a judgement. For each event the
engine asks one question with a declared answer:

```
facet(payload) = (entity, key, value)   or   None
```

read off `ASSERTION_FORMS`, a frozen table of five grammar kinds — a declared
reading of `corpora/chronicle/grammar.md` and `corpora/l4stream/grammar.md`,
exactly as `HANDLE_FIELDS` is at Layer 3 (`README-l3 §0.2`: *"the grammar
vocabularies are fixed, so the engine knows at design time which fields name a
thing"*). `link` reads as an assertion on `(src, rel)` whose value is the target —
Graphiti's bitemporal edge with its LLM date-interpretation cost never incurred,
because `t` is engine-assigned at ingest (§1.3).

Two rules make the derivation safe rather than merely cheap:

* **Fold only what inverts.** The engine rebuilds the payload from the facet it
  just extracted and compares **canonical bytes** (§2.4, not Python equality —
  `True == 1` there and `true ≠ 1` here). A payload that does not round-trip is
  not consolidated at all: it becomes a derived row, or is stored verbatim. So
  `reconstruction wrong = 0` is **structural**, not lucky — the engine never
  regenerates an event it did not first prove it could regenerate.
* **An ambiguous key stops claiming an inversion.** The atlas maps an attribute
  key to the grammar kind its assertions invert to. A key seen under two kinds,
  or under a payload that did not round-trip, is marked `None`: its assertions go
  on answering Q1 and Q2 exactly and **reconstruct nothing**. Honest loss, never
  a wrong payload.

**Q3's counts are two folds, and one of them cannot be a fold.** An entity's
action profile is a fold over its complete chains — free, because the chains are
there. Its *irreducible* events are not in any chain, so the schema keeps a
per-entity `{kind: count}`: an event whose content no schema regenerates still
leaves the schema knowing **that** it happened, and of what kind, long after the
episode is gone. That is the cheapest honest thing consolidation can say about
what it could not consolidate, and it costs 600 of the 2 747 spare cells.

**Eviction is four phases, most-lossless first**, and every one of them is a total
order (§2.3):

1. **Demotion** — release an episode a chain regenerates. Oldest first. Nothing is
   lost; it is counted as a `demotion` and deliberately kept **out** of the
   forgetting record, which is the ledger of what is *gone*.
2. **Forgetting** — release an irreducible episode by the **inherited Layer-3
   importance law**: `grammar weight × distinct-reference count × harmonic
   logical-`t` recency`, exact `Fraction`s compared by integer cross-
   multiplication, ties by `t` then canonical bytes, and the arriving item
   competes like any other and displaces nothing weaker than itself. Recorded.
3. **Shedding** — drop a whole supersession chain (§0.3). Recorded, per assertion,
   at each assertion's own `t`.
4. **Refusal** — only when no eviction could make room. `t` is not spent and the
   state is unchanged (§4.1.2) — the one response every layer shares.

---

## §2. What the strains found (`trials/strain/l4/`)

### 2.1 Misattribution: a derived answer names the assertion that carries it

The two sins consolidation is heir to are **misattribution** and **bias**
(`autopsy/GAPMAP.md §6`, Schacter). Layer 3 could not commit either: an answer was
the stored event or it was an abstention. Layer 4 derives, so both become
reachable — and both are exactly what the autopsies found in the prior art
(`autopsy/mem0/ANATOMY.md`: provenance ABSENT, inferred and user-stated
indistinguishable; `autopsy/writ/ANATOMY.md`: an answer's own `cited_sources` read
by **zero** lines of scoring).

Measured on murk's **305 recorded contradictions**, in budget: every
current-value answer carries a `support` naming one logical `t`, and **the event
the corpus holds at that `t` asserts exactly the value returned**. Not "the answer
is right" — the answer is right *and* correctly sourced, checked against the
frozen corpus rather than against the engine's own belief. Provenance is dormant
until Layer 7 (§4.2), which is why this is a strain and not a gate; the point is
that the tag is **derivable now**, so Layer 7 does not inherit a schema that
cannot produce one.

### 2.2 Bias: the present does not reshape the past

Graphiti maintains the full bitemporal model on write and then, **by default, does
not honour `invalid_at` at read**. The steal was to keep the model and fix the
read. For every contradicted pair:

* as-of **at** a superseded assertion returns *that* value, not the current one;
* as-of **between** two assertions holds the interval open to the next one;
* as-of **before** the pair's first assertion **abstains** — the case where a
  supersession-blind read invents a value that was never in force.

Under murk's full dirt at the footprint the gate is stated at, where 490 entities
have had chains shed: `wrong = 0`, `fabricated = 0`, coverage 695‰. Coverage
falls under pressure; correctness does not.

### 2.3 Absent-mindedness: the ledger closes

The GAPMAP seed for this class is *"what is refused under budget must be refused
honestly"*. At Layer 4 the honest question is sharper, because eviction now has
two kinds and an engine that blurred them could report a tiny forgetting count
while having lost everything. Two identities are asserted on the binding corpus:

```
demotions + forgotten + episodes held  =  18 788 + 714 + 498  =  20 000  =  events ingested
forgotten                              =  events the engine cannot reconstruct  =  714
```

The second is the one with teeth. The forgetting record's count is not a number
the engine chose: it is **exactly** the set of `t` the engine abstains on, so a
demotion cannot be booked as a loss and a loss cannot be booked as a demotion. And
the record is still the Layer-3 one — `3 + 2 × buckets ≤ 35` cells, bounded
forever by coarsening — so 714 distinct payloads left behind 23 integer cells, and
the pigeonhole that makes the loss irreversible holds here exactly as
`humility/l4/IMPOSSIBILITY.md §3` argues it does one layer down.

### 2.4 Form B: the ladder's thesis, measured

`README-l3 §0.4` deferred *demotion-into-consolidated-form* to this layer and said
why. This is the debt coming due, on **Layer 3's own binding corpus, at Layer 3's
own pressure cap, through Layer 3's own battery and scorer** — the same 11 000
units, the same 10 000 items, the same cues, nothing re-tuned:

| engine | items retained | weighted-C | unweighted-C | F | wrong | fabricated |
|---|---|---|---|---|---|---|
| `make_engine(3)` — the frozen forgetting engine | 914 | **917** | 91 | 1000 | 0 | 0 |
| `make_engine(4)` — consolidation | **1 566** | **924** | **157** | 1000 | 0 | 0 |

The mechanism is named rather than merely observed: `l3streamb` has **no
supersession at all** (its `tag`s are unique), so not one chain is built. The
entire gain is the row codec — 6 cells per retained item against 12 — which is
`§0.2`'s second currency, and it is asserted in the trial that a Layer-4 episode
costs strictly less than the event it came from.

**A number that must not be misread, stated here rather than discovered later.**
`trials/ascension/l3/ATTAINABILITY.md` records an oracle ceiling of **918‰** on
this stream, and the cap-4 engine reaches **924**. That ceiling is exact over
**retain-or-drop** policies — the family Layer 3 could choose from, where the only
question is *which* whole episodes to keep. A consolidating engine is not in that
family, and it passes through the ceiling for precisely the reason the ceiling was
true. **No Layer-3 number moves**: `adapters/l3` is untouched, its gate still binds
at 850 against 918, and its own measurement is still 917.

### 2.5 The inflation guard survives the move to a row codec

Layer 3 proved that a flood of byte-identical copies mints no importance mass,
because a cluster's `uses` count **distinct payloads, first occurrence only**.
Layer 4 keeps episodes as rows and reads weight and handle off the row's columns
rather than off a rebuilt payload — a different implementation of the same law,
and therefore a place the guard could have been lost with no score noticing. At
floods of 50 / 200 / 800 copies against 30 heavy items placed **early** (the worst
case for recency): **30/30 survive** every time, and the flood's slot count is
35 / 34 / 31 — it does not grow with the flood. It drifts *down*, because the
cluster's single use recedes while copies keep arriving, so late copies are weaker
than the ones already held and are dropped on arrival.

### 2.6 Determinism through consolidation

Identical streams give byte-identical snapshots through demotion and forgetting,
and `restore(snapshot(s))` re-snapshots to the same bytes. Layer 4 adds two new
ways for an ordering to leak in — the insertion order of the key-major nesting and
of the row shapes — so the law is re-asserted over a replay that exercises both,
at the footprint the gate is stated at. The consolidated state is anchored in
`anchors/l4.json`, so a change in the demotion order, the importance law over
rows, the shedding rule or the atlas turns the suite red even when every score
still clears the gate.

---

## §3. What Layer 4 CAN express

- **Consolidation at the ratified gate.** On the binding corpus
  (`corpora/l4stream`, BOUNDARY-RULINGS.md R4 clause 1): **footprint 250‰,
  C = 1000‰, reconstruction F = 968‰, B = 1000** against a gate of
  `footprint ≤ 250, C ≥ 850, F ≥ 900, B = 1000`. Stage A's exhibited witness —
  the best any state in the declared family can do — scores 1000 / 984, so the
  engine lands **16‰ off an arithmetic optimum** it does not have the working room
  to reach exactly, while every named capability-free baseline sits far below
  (verbatim truncation 247/325, current-value-table-only 155/100, capped
  `layer_cap = 3` 200/325). `F_corruption = 1000` is the ungated diagnostic
  (R4 clause 3's pairing inverted, so the stricter number binds).
- **The whole semantic battery, exactly.** Q1 current-value 2 951/2 951, Q2 as-of
  15 837/15 837, Q3 profiles and global counts 205/205 — every one answered
  through the ordinary query interface (§7), `wrong = 0`, `fabricated = 0` on
  every unanswerable probe.
- **Reconstruction of episodes that no longer exist.** 19 286 of 20 000 events
  returned byte-exact by `read(t)` — the Layer-1 verb — with only 498 of them
  still stored as episodes. **18 788 events were demoted and are still answerable
  in full.** That gap is the layer.
- **Supersession honoured by default.** As-of is integer interval arithmetic on
  engine-assigned `t`; a query before a pair's first assertion abstains rather
  than reading the present backwards.
- **Provenance derivable at the door.** Every current-value and as-of answer
  cites the assertion that carries it, verified against the frozen corpus.
- **Layers 1, 2 and 3, carried forward.** `read`, `read_range`, `recall`,
  `forgetting` and `forgot_at` all still answer; the inheritance class replays
  §5 L1's exact IO, §5 L2's cue gate (`cue-C ≥ 900`, `F ≥ 950`) and §5 L3's
  retention battery on both frozen pressure streams **in budget**, where the
  scores are asserted as identities rather than thresholds.
- **Strictly more than Layer 3 under Layer 3's own pressure** (§2.4).

## §4. What Layer 4 CANNOT express (the boundary for Layer 5+)

- **No prospection — the Layer-5 humility seam.** This is the precise statement,
  and it is structural rather than a promise: Layer 4 has **no construct that
  watches future writes**. There is no `intend`, no condition, no trigger, no
  pending set; `write` is a fold plus an eviction and consults nothing but the
  arriving payload and the current state. Every schema this layer maintains is a
  fold over the **past** — an interval closed at a `t` already assigned, a count
  of things already seen. §5.1 L5 puts it exactly: *"Consolidation summarizes the
  past and has no construct that watches future writes, so it fires condition-met
  triggers only by coincidence."*

  Stated for the layer above: **a deferred-intent task scores 0 here, not near
  0.** `trigger-recall` is the fraction of intentions whose condition a later
  write satisfies and which fired; with no intention store, nothing is ever
  pending, so nothing can fire — the capped engine's numerator is empty by
  construction, not by difficulty, and `capped trigger-recall ≤ 50` (§5 L5) is a
  ceiling this engine sits at **zero** against. The `intend(condition → event)`
  verb is not implemented and `query` abstains on it (§7.3), which is what makes
  the measurement a score rather than an exception. `humility/l5/IMPOSSIBILITY.md`
  should be written against that absence: not "the schemas are too lossy to
  notice the trigger" but "there is nothing to notice with", and the honest
  residual is that a Layer-5 engine will have to add state the budget must then
  price, exactly as this layer had to price its atlas and its counters.

- **No recall of a demoted episode.** An episode released into consolidated form
  is no longer reachable **by cue**: `recall` runs over the handle index of
  retained episodes, and a demoted event has none. Its content is fully
  answerable by `read(t)`, `current` and `asof` — the schema regenerates it — but
  the associative channel narrows as the budget tightens. That is the honest price
  of the compression, and it is the seam where a Layer-6 confidence model will
  have something to say: the engine can already tell *demoted* (content survives,
  cue does not) from *forgotten* (content gone, counted) from *never ingested*.

- **No inference beyond the declared grammar.** The facet map is a **declared
  reading** of frozen grammars, not a learner. An event outside it is irreducible
  to this engine however regular it looks, and an attribute key seen under two
  kinds stops being invertible rather than being guessed at. What Layer 4 claims
  is *derivation from a declared schema*, not *schema discovery*.

- **No summarization, and no judgement about content.** A chain is the exact
  history, not a précis; a profile is a count, not a description. Nothing in this
  layer produces text, chooses what is interesting, or decides that two differently
  spelled facts are the same fact. Layer 7 generates; Layer 4 only folds.

- **No reconstruction of what was shed or forgotten.** Shedding drops a chain
  prefix and forgetting drops an irreducible episode; both are recorded as a count
  and a mass per `t`-range and **never as a payload**. The pigeonhole of
  `humility/l4/IMPOSSIBILITY.md §3` applies to this engine too: 714 distinct
  payloads into 23 integer cells admits no injective map, so those events are
  unanswerable in principle and the engine abstains on all of them.

- **No calibrated confidence, no generation, no binding provenance.** Confidence
  is emitted as structural certainty (1000 on a verified or regenerated answer)
  but **ungated** until Layer 6 (§3.4). Provenance tags are attached and are
  derivable, but neither required nor scored until Layer 7 (§4.2) — and one seam
  is already visible: a Q3 fold over the whole stream has **no bounded support to
  cite**, and §4.2's schema has no form for "supported by everything". Layer 7
  will have to close that.

## Reading list for the next session

Per `CLAUDE.md §1`, the next session reads this README before acting. The one
sentence to carry forward: **Layer 4 folds every event, at the door, into a
derived schema it has proved it can invert — an interval chain when the event
supersedes something, a typed row against a learned shape when it does not — and
then releases the episode itself, so that at a quarter of the raw episodic
footprint it answers the whole semantic battery exactly and still returns 19 286
of 20 000 events byte-exact while holding 498, paying for the one access path it
cannot afford in query time rather than in cells, and recording what it genuinely
lost as a count and a mass it can never turn back into a payload.**

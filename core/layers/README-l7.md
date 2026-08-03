# Layer 7 — Generation (`generate(cue)`: compose, tag, never promote)

`[L7] [ASCEND]`. The seventh capability of Boundary-1: Memory. Layer 1
**retained**, Layer 2 **recalled**, Layer 3 **dropped**, Layer 4 **derived**,
Layer 5 **watched**, Layer 6 **doubted**. Every one of those is a claim about
content the store *received*: an event comes back byte-exact or it does not, a
fold inverts or its key is refused, an intention has fired or it has not, a
confidence is a fold over an interval table of things that were ingested.

Layer 7 is the first capability that returns an item **the store never held**,
and the first that has to say so about itself. `README-l6 §4` wrote down the seam
it opens on:

> *"nothing this engine returns is tagged `generated` because nothing this engine
> returns is generated … a capped-6 engine should fail `§5 L7` structurally
> rather than marginally."*

It does — at a conjunction of 0 of 160, by arithmetic and not by margin. This
document states **exactly what Layer 7 can and cannot express**. Layer 8's
humility trial will be written against the boundary drawn in §4, and §5 says what
that seam is allowed to assume today, which is: no number at all.

Intellectual pedigree: there is none to steal. `autopsy/GAPMAP.md §1` finds
generation **absent** in all four engines autopsied, and `autopsy/writ`'s firsthand
read at `3c0900a` finds the sign **inverted** — `checkHallucination`
(`evaluator.ts:347-350`) flags any non-empty answer restating no stored value, so
a tagged generation is scored there as a **defect**. What is inherited is `§4.2`,
which wakes here and can never be un-bound, and the four layers of discipline
beneath it.

Code (frozen after this session, §9):
- `core/layers/l7_generation.py` — the `L7State` (a **subclass** of the frozen
  `L6State` adding exactly one field, the lineage ledger), the declared
  composition reading, the `generate` query op, and the ledger written by
  `ingest`.
- `trials/adapters/l7.py` — the Layer-7 adapter. `core/engine.py`,
  `l1_retention.py`, `l2_recall.py`, `l3_forgetting.py`, `l4_consolidation.py`,
  `l5_prospection.py` and `l6_meta_memory.py` are **untouched**; `anchors/l1.json`
  … `anchors/l6.json` replay through their own adapters unchanged.

---

## §0. The one field, and the measurement that forced it

Every `ASCEND` since Layer 3 has opened with a state-composition arithmetic and
reported where its margin ran out — 14 items, 5 cells, 10 cells. Layer 6 opened
instead with a **negative**: `§5.1 L6` says meta-memory derives confidence *"from
existing state"*, so `L6State` added no field and `README-l6 §0` recorded that as
the finding.

`§5 L7` says no such thing, and this layer does not get to choose. Stage B
measured why, against a mock engine, and the finding is the one no document could
have been read for (`ascension/l7/STAGE-B.md §5.1`):

> `§7.1` makes `query` **pure**, so an engine cannot record what it **answered** —
> only what it **received**. Stage A's witness is a policy and records at answer
> time; an engine cannot, and one that tried would be reaching for a mutation
> `§2.1` forbids.

So `promotion = 0` — the clause `§5 L7` gates and `§6` names a second time in the
strain class — **forces a lineage ledger written by `ingest`**, and that ledger is
the single field `L7State` adds beside the frozen `L6State`. It is priced by name
before it was written and the price is the one it cost:

| item | priced (`ATTAINABILITY.md §7`) | spent | where |
|---|---|---|---|
| the lineage ledger `{compound: rung}` | **320 cells** (2 an entry, 160 items) | **320** | engine state keyed by `t`, the only placement `§1.4` leaves |
| the bytes-keyed alternative | 800 cells | **0** | recorded and **declined**: the cheap form can only make the engine *refuse to promote*, never promote wrongly |
| the composition access path | disclaimed, with its reason | **0** | see §1.1 — it is a reading, not an index |
| the loss-accounting reserve | disclaimed, with the failure it fears named | **0** | see §2.3, where the feared failure is measured and does not exist |

Rule P is one cell, one grammar atom, and a ledger entry is an entity and its
rung: the atoms a reader can count in the serialized branch and the cells the
engine charged itself are the same number, asserted rather than assumed
(`ops/l7/t_l7_composition.py`).

**And where there is nothing to record it costs nothing.** On `sessions`, `murk`
and `l5stream` — none of which carries a `profile` payload — the ledger is empty,
the occupancy is the Layer-6 engine's to the cell, and `anchors/l7.json` pins that
against `anchors/l6.json`'s own frozen figures, a file this session could not
edit. That is what `inheritance/l7`'s six in-budget rows silently stand on: a
ledger that charged for streams with no generation in them would compete for room
with a pending set and a fired ledger `README-l5 §0.1` puts outside every eviction
phase **on purpose**.

---

## §1. The capability, in four lines

### 1.1 `generate` is a `query` op, and composition is a reading

`§7.1` declares **three** operations and `§1.1` says events are the only fuel, so
the only reading under which `§5 L7`'s `generate(cue)` and `§7.1` are both true is
that **`generate` is a `query` op** whose `Answer` carries the item, its
confidence, its provenance tag and its lineage (`R8` clause 2). That is the same
argument in the same place `ascension/l5/ATTAINABILITY.md`'s Reading 1 made for
`intend` and `R6` clause 2 ratified for `§7.1`'s *"appends one event"* — three
precedents now, and `trials/adapters/INTERFACE.md` (copied verbatim from `§7` and
used to grade every foreign engine) stays true.

`COMPOSITION_FORM` is a **declared reading of the frozen grammar**, in the shape
`ASSERTION_FORMS` (L4), `INTENTION_FORM` (L5) and `SET_ONCE_KEYS` (L6) already
have. It had to be a *second* reading and the artifact's own grammar is why:
`part` and `profile` are **outside** the frozen Layer-4 facet map, so to every
engine below Layer 7 a `profile` event is an irreducible episode and not an
assertion — the layer below can hold the event and cannot read it, exactly as
`INTENTION_FORM` stood to Layer 4 one layer down.

**The access path is the free one, and the bill is stated.** `ATTAINABILITY.md
§7` named two options and disclaimed the choice: extend the reading, or buy a
second access path at `README-l4 §0.1`'s measured 343 permille. The reading is
taken. `part` and `profile` episodes live in the Layer-4 `kept` tier under the row
codec, so reading them back is a scan of **two row groups** and costs no cell —
and **query time pays where state cannot**, which is `README-l4 §0.1`'s trade one
layer up. It is also why composition degrades honestly under pressure: a compound
whose `part` episode the budget took is one the reading no longer determines, and
the engine abstains rather than composing from a hole (§2.3).

### 1.2 The answer: hold, compose, or abstain

```
generate(entity):
    the store HOLDS a profile for it, and the ledger does not claim it
        -> that item, lineage `observed`, kind `recall`, support (its own t)
    the rule DETERMINES an item
        -> that item, lineage `generated`, kind `derive`,
           support = exactly the t's the rule read
    otherwise
        -> abstain
```

Three lines, and the third is the one a naive composer gets wrong: the 100
generation-shaped `KU1` probes of `corpora/l7compose` have one component whose
`mass` is never asserted, the declared rule does not determine an item, and
composing anything there is the fabrication `§3.0` prices at 0 while paying 1000
for the abstention it displaced.

`lineage` is a property of the **ITEM** and is orthogonal to `§4.2.3`'s closed
four-kind vocabulary, which says how an answer reached the **caller** (`R8`
clause 4). No fifth `kind` is minted: a composed item travels on the `derive`
channel and `lineage` carries the other claim. **The field is on a `generate`
Answer and on nothing else** — `read`, `read_range`, `recall`, `current`, `asof`,
`fired`, `profile` and the diagnostics return the Layer-6 Answer byte for byte,
which is asserted (`ops/l7`) and is why five older scorers never see a field they
were not written against.

### 1.3 The lineage decision is a store consultation, and cannot be anything else

`corpora/l7compose`'s forcing region is 100 **mirror pairs** whose two members are
**twins**: one material drawn per slot and instantiated twice, so they compose to
the *same item but for its `entity` field*, and a balanced coin decides which
member's profile the stream carries. **The value is never the signal.** Blank the
entity id and the two cues are the same object, so any policy whose lineage
decision is a function of the query alone mislabels exactly one member of every
pair — 100 errors, exhibited against a bench of six labellers (`R8` clause 1,
Theorem 1).

This engine gives the two members **different** lineages on all 100 pairs and the
**same** value on all 100. Nothing in the query and nothing in the answer could
have carried that decision; the only thing left is what the engine holds. That is
the Layer-7 analogue of `R7`'s *provably non-resolving*, pointing the other way:
at Layer 6 the region caught an engine for being **too good**, and here nothing is
withheld from a correct composer — what is withheld is the **item**, from the
**retrieval channel**.

### 1.4 The ledger, and why it is an UPPER BOUND

At `ingest` the engine sees a `profile` payload arrive and cannot ask itself what
it answered. What it can read is the shape of its own store, and `STAGE-B.md
§5.1` recorded the two structural signatures this artifact leaves:

| signature | what it recognises |
|---|---|
| **the mirror twin** — an item identical **modulo `entity`** is already held | a depth-1 re-ingestion |
| **the generated hop** — the composition passes through a compound component the store does not carry as an *unmarked observation* | every rung above it |

Neither is a census, and the design says so. A coincidence marks an *observation*
as generated, which can only make this engine **refuse to promote** and never
promote wrongly — an **upper bound on lineage**, exactly the shape `README-l6 §4`'s
`damaged`-aware `d + 1` took one layer down and exactly the trade
`ATTAINABILITY.md §7` records when it declines the bytes-keyed alternative.

**On this artifact the bound is tight, and that is measured rather than assumed**
(`ops/l7/t_l7_composition.py`): replaying the frozen stream, the signature is
`False` for every one of the 100 `profile` events it carries — the only compounds
sharing a composed item modulo `entity` are the mirror twins, and a pair's other
member's profile is never in the stream — and it is `True` for every one of the
100 withheld items when the caller writes them back. No false positive, no false
negative. A later artifact would have to repeat that measurement; the rule does
not carry itself.

The rung an entry records is `1 + ` the deepest rung among its compound
components, so the ledger's own profile after `§6`'s ladder is `{1: 100, 2: 30,
3: 30}` — and `strain/l7` requires it to agree **entity by entity** with the depth
`corpora/l7compose` declares and `ops/l7/t_l7compose.py` recomputes from the
frozen bytes. The ledger is not a counter; it is a claim about which item came
from where, checked against the artifact and never against itself.

### 1.5 The ledger is not evictable

`promotion = 0` means a lineage entry an engine dropped is a generation it could
promote, so an eviction path reaching the ledger would be an engine that can be
made to break a ratified gate **by being poor**. What gives way is the episodic
tier, exactly as at Layers 4 and 5; where the budget cannot house the entry even
so, the engine refuses the **whole** transition under `§4.1.2` — `t` unspent,
state unchanged. That is `README-l5 §0.1`'s rule for the two prospection tiers
applied to the tier this layer adds. On the binding artifact it never arises
(`refused = 0`), and under real pressure `ops/l7` measures the episodic tier
giving way around a ledger that does not.

---

## §2. What the strains found (`trials/strain/l7/`)

### 2.1 SUGGESTIBILITY — the one strain the constitution schedules

`§6` names it in its own frozen text — *"the mandatory Layer 7 self-pollution
strain"* — and no other Schacter sin's assignment enjoys that: `autopsy/GAPMAP.md
§6` **maps** the other six and the constitution **schedules** this one. The
post-L6 PULSE (`BOUNDARY.log` line 42) recorded why it could not have been
discharged earlier: its literal form requires an act no layer below 7 performs,
**the caller re-ingesting the engine's own output as ordinary fuel**. Layer 5 came
nearest and the guard there is that the emitted payload is byte-for-byte the
caller's own (`§1.4`), which is exactly why it is not suggestibility.

Measured over the artifact's own three-generation ladder, at every rung:

| rung | emitted | store | **promotion** | still generated | ledger |
|---:|---:|---:|---:|---:|---|
| 1 | 100 | 12 100 | **0** | 160 | `{1: 100}` |
| 2 | 30 | 12 130 | **0** | 160 | `{1: 100, 2: 30}` |
| 3 | 30 | 12 160 | **0** | 160 | `{1: 100, 2: 30, 3: 30}` |

**And the teeth are demonstrated on an engine, not on a policy.** A ledger-blind
fixture — this engine with one field emptied at the read, a trial fixture and
never engine code, in the shape `strain/l3`'s naive reference count and
`strain/l5`'s ledger-blind firing policy established — promotes **100, then 130,
then all 160**, and three deep calls every one of its own dreams a fact. Those are
the same three numbers `ATTAINABILITY.md §5.1` measured for the ledger-blind
*policy* before any engine existed: one instrument and two implementations, at the
level of a failure mode rather than of a score. It is `autopsy/GAPMAP.md §2`'s
engine thesis — *every system autopsied writes the metadata that would make it
correct and then never reads it where it counts* — pointed at the one field this
layer exists to fill.

### 2.2 The finding no `§5 L7` clause states: novelty stops being the right question

`novelty = 1000` is *"provably never-stored"*, a canonical-byte comparison against
the ingested store. After the caller writes a generation back, **the store
contains it**. Measured on the store as it now is, the byte-novel share of what
the engine still calls generated falls

```
60  ->  30  ->  0
```

across the three rungs, while `tagging` holds at 1000 and `promotion` stays 0.
**At rung 3 a byte-comparison would call this engine a liar about every item it
made.** Nothing about those items' lineage changed; what changed is where they
have been since.

That is why `R8` clause 3 binds `novelty`'s denominator to the items the engine
**tags** rather than to the store, why `promotion = 0` is a separate clause from
`novelty = 1000` at all, and why `R8` clause 5(c) puts the capital crime's
enforcement on **lineage** rather than on any comparison `§4.2` or `§3.0` can
make. It is recorded here because no clause of `§5 L7` says it and a later session
reading the gate alone would not find it.

### 2.3 `§4.2` as it wakes: the invented warrant, and the warrant the budget takes

**THE INVERSION.** `ATTAINABILITY.md §9.3` measured the blindness on a policy;
`strain/l7` reproduces it on the engine. After the caller re-ingests generation 1,
**all 30** depth-2 answers cite a `t` that is one of the engine's own items, and
the frozen `laws/t_provenance_schema.py` — unedited since `[L0]` — accepts **all
30**, because under `R6` clause 2 a re-ingested generation is an actually-ingested
event with a real `t`. **The provenance law as written is blind to the failure the
layer that activates it exists to prevent.** What catches it is the ledger: **0**
of those 30 is reported as observed fact, where the ledger-blind fixture reports
100 at the same rung. `30` and `0` are the two halves of one finding, and neither
may be quoted as the other. A later session that finds `t_provenance_schema.py`
green must not conclude the capital crime is covered; that file is exactly as
green against the failure as against its absence.

**THE WARRANT THE BUDGET TAKES — the question live since the kept promise.**
`BOUNDARY.log` line 34 filed it at the post-L5 PULSE (*must a support entry be
RECOVERABLE, or only INGESTED?*), `R7` clause 7 bequeathed it, and `R8` clause
5(a) settled it **shape-only**: a support entry must be **ingested, not
recoverable**, with the weaker claim said out loud — *provenance certifies that an
answer had a source, and not that the source can be shown* — and paid for by an
**ungated** support-recoverability rate. `ATTAINABILITY.md §7` named the failure it
feared: *a generation whose support has been shed cites a `t` the forgetting record
can only count.*

Measured on a declared ladder of six caps over a 6 000-event prefix, where the
engine loses from 0 to 1 934 events and sheds chains at the bottom:

> **The feared path does not exist on this engine, and not because nothing is
> lost.** The composition reading can only cite what it can still **read**, so the
> engine loses the **answer** before it can lose the **warrant**: generation
> degrades from 160 answers to 0 across the ladder, by **abstention** throughout
> (`§3.0` pays 100 for it), and the number of cited `t`s the engine cannot produce
> is **0 at every cap**. The forgetting record is consulted and closes the ledger
> the way Layers 4 and 5 close theirs — `forgotten` is exactly the set of `t` the
> engine abstains on — so the cited set and the lost set are disjoint by
> construction rather than by luck.

**It is stated as the stronger property it is, and it is NOT gated.** `R8` clause
5(a) demands *ingested*; this engine happens to satisfy *recoverable*, and an
engine that did not would breach no `§5 L7` clause. Saying which of the two is the
law and which is a fact about one implementation is why it is written here and not
in a gate.

---

## §3. What Layer 7 CAN express

- **Generation at the ratified gate.** On the binding artifact
  (`corpora/l7compose`, `BOUNDARY-RULINGS.md R8` clause 1), with `ECE` read
  **exact** under `R7` clause 4 and binned under clause 5:

  ```
  validity 1000   novelty 1000   tagging 1000   promotion 0 / 0 / 0 (three deep)
  F_core 1000 (F_all 1000, the ungated diagnostic)    ECE 0 exactly
  B 1000, refused 0    A 2000   n_pos 2000   n_neg 0   wrong 0   fabricated 0
  abstentions 200 — exactly the unanswerable class
  ```

  against a gate of `= 1000 / = 1000 / = 1000 / = 0 / ≥ 950 / = 1000 / ≤ 40`. The
  figures are the exhibited witness's, clause for clause — which is `R2`
  obligation 1 discharged and not a coincidence: `ATTAINABILITY.md §5` exhibited
  them before any engine existed, and Stage C's burden was to compute them **from
  the engine's own state** rather than from the battery's declared evidence.

- **Telling the two channels apart when nothing in the question does.** 100
  mirror pairs, the same value returned for both members and a different lineage
  on every one. `tagging = 1000` here is a **capability** and not a lookup, which
  is what `PRE-READ.md §6.3` predicted a first artifact would fail to force and
  what `R8` clause 1's Theorem 1 makes structural.

- **Committing where hedging would pay.** `§3.0` offers 100 an abstention against
  a flagged guess's 0, and `R8` clause 8 records that the price list therefore
  *rewards* attempting. The engine takes none of the escape: its 200 abstentions
  are exactly the 200 unanswerable probes, including all 100 generation-shaped
  ones where a naive composer fabricates.

- **Surviving its own output, three deep.** §2.1's table, and a ledger whose rung
  profile agrees entity by entity with a depth decidable from frozen bytes.

- **Layers 1–6, carried forward.** `inheritance/l7` replays `§5 L1`'s exact IO and
  byte-identical round trip, `§5 L2`'s cue gate, `§5 L3`'s retention battery on
  both frozen pressure streams, `§5 L4`'s consolidation battery on
  `corpora/l4stream`, `§5 L5`'s prospection battery on `corpora/l5stream` — all as
  in-budget identities — and `§5 L6`'s **own ratified gate** on
  `corpora/l6batteryb`, the first inherited row whose clauses stay thresholds
  because the forcing region makes the engine wrong exactly 100 times by theorem
  whatever the budget. That row is the only place the **ranking** is still asked
  for, and it is green for a structural reason: this layer replaced no confidence.

---

## §4. What Layer 7 CANNOT express (the boundary for Layer 8+)

- **THE `ECE` RESIDUAL IS OPEN, AND THIS LAYER DID NOT CLOSE IT.** `README-l6 §4`
  recorded it in advance: *a generated item has no chain, no distinct-value count
  and no set-once status, so `confidence_for` returns `CERTAIN` on it by falling
  through — which is exactly the wrong answer and is the first thing a Layer-7
  engine must replace.* It is **not replaced**, and the reason is measured rather
  than convenient (`ATTAINABILITY.md §6.2`, `STAGE-B.md §4`): on this artifact
  composition is **deterministic and correct**, so `1000‰` on a composed item *is*
  right and every named policy scores `ECE = 0` exactly. Building a confidence
  model for generated items here would be building a level nothing exercises,
  which is the thing `README-l6 §1.3` warns against — *a level nothing exercises
  is a level that could be wrong*.

  So the engine states `CERTAIN` on a generated item, `ECE = 0` is not evidence
  the residual is closed, and no later session may quote it as such. **What would
  close it is an artifact on which composition can be wrong** — a compositional
  grammar whose rule is underdetermined by the material in a measurable share of
  cases, so that a calibrated composer beats a confident one. `§5 L7` does not
  require it and `R8` clause 6 records that `ECE ≤ 40` is *a floor against
  incoherence, not a discriminator*; the residual is therefore an open design
  question and not a defect, and it is stated here so that it is inherited rather
  than rediscovered.

- **No lineage for an item the engine did not compose.** The ledger records what
  *this* engine made. A generation composed by a **different** engine and ingested
  by this one is an ordinary observation, and this engine will call it one. `R8`
  clause 4 puts the marker in engine state keyed by `t` precisely because `§1.4`
  forbids the payload, and the consequence is that lineage does not travel between
  states except through `snapshot`/`restore`. Two engines cannot compare notes.

- **No lineage beyond an upper bound.** §1.4: the signature is structural, a
  coincidence over-marks, and over-marking can only make the engine refuse to
  promote. On `corpora/l7compose` the bound is tight and measured; on an artifact
  where two distinct compounds composed to one item, it would not be, and the
  honest consequence is that the engine would decline to call a real observation a
  fact. That is a **non-capability by design**, chosen against an 800-cell census
  that would have been exact about forgeries and no better about anything else.

- **No composition the reading does not determine, and none under pressure that
  costs it its material.** Generation is a fold over held state, so it degrades
  from 160 answers to 0 as the budget tightens (§2.3), and every step of that
  degradation is an abstention. There is no partial composition, no best guess and
  no confidence low enough to license one.

- **No confidence on a reconstruction, still.** `read`, `read_range`, `recall`,
  `fired`, `profile` and `count` all return `1000`, unchanged from Layers 5 and 6,
  because they return content the engine regenerated exactly or they abstain.
  `README-l6 §4` called that a non-capability by construction and it is unchanged
  here.

### 4.1 The four-kind impossibility taxonomy, in its final form

`§6` requires every humility trial to ship an `IMPOSSIBILITY.md` giving a
**structural** argument. Four exist, and with Layer 7 the taxonomy has all four
kinds it will have below `BOUNDARY-HIGH.md`. Naming them is the point: an
`IMPOSSIBILITY.md` that could be any of the four is a template, and one that says
which it is has done the work.

| layer | the kind | the argument, in one line |
|---|---|---|
| **L4** | **absent bits** | *information-theoretic.* Thousands of distinct evicted payloads map into an aggregated forgetting record of at most 35 integer cells, so no injective map exists and the answers are unreachable **in principle** — the pigeonhole witness |
| **L5** | **absent machinery** | *no operation on the write path consults a stored condition.* In budget the capped engine holds every intention **byte-exact** and still fires nothing: nothing is missing from the state, and what is missing is a verb |
| **L6** | **absent order** | *no ranking.* The capped engine holds **both halves of every tie** and answers all 200 forcing queries; a constant assigns one confidence, every correct×incorrect pair ties, `§3.4` counts a tie as ½, so `AUROC = 1/2` **exactly** |
| **L7** | **absent generativity** | *an engine that can only find cannot make.* The capped engine's information is complete, its verbs sufficient and its answers ordered; what it cannot do is produce an item the store never contained, and **no reading of held state produces one** |

The fourth kind is the first whose failure is not about held state at all, and it
is distinguished rather than restated: it **survives a perfect state** (nothing
evicted, nothing damaged, nothing refused — the number does not move) and it is
**closed under adding readings** and not only under adding budget, a reading being
a function of the payloads whose range is bounded by them.

---

## §5. The Layer-8 seam, stated honestly and with no number in it

`§5`'s own table gives Layers 8 and 9 laws but **not thresholds**: both rows read
*specified at the Phase 3→4 gate*, where every other row states a gate.
`BOUNDARY-RULINGS.md`'s preamble derives its own authority from exactly that
concession, and names the deferred document without naming its filename — *call it
`BOUNDARY-HIGH.md`*. **It has not been written.** So this section states what
Layer 8 will demand **structurally**, and defers every number, because a layer
README that guessed a threshold would be doing what `R2` exists to forbid: fixing
a gate before its attainability is arithmetic.

**What `§5 L8` says in its own words:** *Self-description — introspection answered
FROM STATE via the ordinary query interface.* Three things follow from ratified
text alone, and none of them is a number.

1. **`§7.1`'s three doors stand, again.** Introspection is a `query` op, for the
   fourth time by the same argument: `intend` (L5, `R6` clause 2), `generate`
   (L7, `R8` clause 2), and `§7.1` declares three operations. Whatever L8 asks,
   it asks it through `query`, and an engine that grew a fourth verb would make
   `trials/adapters/INTERFACE.md` false.
2. **"FROM STATE" is the whole clause, and this ladder has spent seven layers
   making it hard.** A Layer-8 engine must answer questions about *itself* out of
   cells it has already paid for. The candidates are on the record and every one
   is already priced: the interval table and the demotion counter (L4), the
   aggregated forgetting record (L3/L4), the two prospection tiers (L5), the
   declared readings (L4/L5/L6/L7), and this layer's ledger. Whether a
   self-description that is honest about all of them is affordable is an
   **arithmetic**, and `R2` requires it computed and recorded before any gate
   binds.
3. **`§4.2` binds there too, and cannot be un-bound.** A self-descriptive answer
   is a non-abstaining answer, so it carries a valid tag or scores 0 *regardless
   of whether its value is correct*. What an answer *about the engine* cites is
   not obvious — `R8` clause 5(b) had to bind relevance on an artifact because the
   schema could not, and a Layer-8 artifact will have to do the same for a class
   of answer whose support may be a fact about state rather than about events.

**Three seams this layer hands upward, named and unpriced:**

* **the ledger is a self-description already.** `{"op":"lineage"}` answers a
  question about the engine's own history out of engine state through `§7` alone,
  which is `§5 L8`'s sentence in miniature. It is a diagnostic and gates nothing
  today; whether a Layer-8 gate would find it sufficient, insufficient or
  disqualifying is not this document's to say.
* **the four `IMPOSSIBILITY.md` arguments are claims the engine cannot make about
  itself.** Every one of them is a fact about what the engine cannot do, written
  by a human in prose and checked by a trial. An engine that could state them
  *from state* would be doing something categorically new — and an engine that
  merely stored them would be failing `§5 L8`'s *from state* the way a stored
  confidence would have failed `§5.1 L6`'s.
* **the humility ceiling has nowhere obvious to stand.** `§6` caps at `N − 1` and
  a capped-7 engine has every verb Layer 8 will use — `query` is `query`. Layer 7
  is the first layer at which the *ascension* gate needed a denominator `§5` did
  not state (`R8` clause 3, the fourth species); Layer 8 may be the first at which
  the *humility* side needs one, and the honest prediction is that whoever writes
  `BOUNDARY-HIGH.md` will find that question before they find a threshold.

Every number in this section is absent on purpose. `§5` defers them, `R2` orders
them after an arithmetic nobody has computed, and no session may bind a gate that
the constitution has reserved for a document that does not exist.

---

## Reading list for the next session

Per `CLAUDE.md §1`, the next session reads this README before acting. The one
sentence to carry forward: **Layer 7 answers exactly what Layer 6 answered and
adds one op and one field — `generate(cue)`, which returns a stored item as
`observed` or a composed one as `generated` with exactly the `t`s the declared
rule read, and a lineage ledger of 2 cells an entry written by `ingest` because
`query` is pure — telling the two channels apart on 100 mirror pairs where
nothing in the question can, promoting none of its own output three generations
deep, abstaining rather than composing from a hole, and stating `CERTAIN` on what
it makes because on this artifact composition cannot be wrong, which is a residual
this layer names and does not close.**

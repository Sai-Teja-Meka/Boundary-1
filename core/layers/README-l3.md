# Layer 3 — Forgetting (principled eviction under pressure)

> **Erratum — 2026-07-25 (`[L3] [RULING]`, directed by `BOUNDARY-RULINGS.md
> R4 clause 2`).** **§4** below reads the Layer-4 footprint gate as an
> **absolute** quantity — *"the Layer-4 gate's own footprint (`≤ 250` units, ≥4×
> compression) this engine holds `250 // 12 = 20` items"*. That reading is
> **superseded**: `footprint ≤ 250` is **250 permille of the raw episodic
> footprint**, the only reading under which §5 L4's own `(≥4× compression)`,
> §5.1's *"at most a quarter of the raw bytes"*, and §5.1's humility defense
> *"lost three-quarters of its episodes"* say one thing rather than three.
>
> This document is **frozen** (§9.2) and **nothing beneath this note is
> rewritten** — the erratum stands above the historical text, in the form the
> `[L3] [PULSE]` session established for the `autopsy/*/ANATOMY.md` errata.
>
> **What the erratum does not reach.** The **seam** §4 draws is untouched and is
> in fact sharper under the ratified reading: a forget-only engine at 250‰ of
> `corpora/l4stream` retains **5 010 of 20 000** episodes rather than twenty, and
> still cannot reconstruct the other **14 990**, because what it dropped left no
> trace in state at all (the byte-identical-snapshot witness §4 cites). The
> `20`-item figure was the *illustration*; the impossibility was never resting on
> it. Everything else in this README — §0's state-composition arithmetic, §1's
> importance law, §2's strain findings, §3 — concerns the **Layer-3** budget of
> 11 000 work units, is unaffected by a Layer-4 unit question, and is correct as
> written. Arithmetic on the record: `trials/ascension/l4/ATTAINABILITY.md §1`.

`[L3] [ASCEND]`. The third capability of Boundary-1: Memory. Layer 1 retained and
refused; Layer 2 recalled by content and still refused. Layer 3 **drops** — under
a stream ten times the budget it keeps what matters and forgets the rest, on a
structural importance law, deterministically, with the budget cap never breached
and nothing it keeps corrupted.

This document states **exactly what Layer 3 can and cannot express**. Layer 4's
humility trial is written against the boundary drawn here.

Intellectual pedigree: ACT-R base-level activation (Anderson & Lebiere 1998;
Anderson & Schooler 1991), rederived in exact integers as the **optimized
frequency×recency form** — see `autopsy/theory-actr-soar/BRIEF.md §1` and the
importance law below. The hot/cold demotion idea is Letta's (GAPMAP **S4**); §0.4
records why this layer **declines** it and what it does instead.

Code (frozen after this session, §9):
- `core/layers/l3_forgetting.py` — the `L3State` (retained records + handle index
  + aggregated forgetting record), the importance law, the eviction path, the
  Layer-1/2 verbs, and the checksummed snapshot/restore.
- `trials/adapters/l3.py` — the Layer-3 adapter. `core/engine.py`,
  `core/layers/l1_retention.py` and `core/layers/l2_recall.py` are **untouched**;
  `anchors/l1.json` and `anchors/l2.json` replay through their own adapters
  unchanged.

---

## §0. The state-composition arithmetic (BOUNDARY-RULINGS.md R2, applied to the budget)

**R2 put attainability before authority: compute what a gate admits before you
bind it.** The same discipline applies one level down, to the *engine*: compute
what the budget admits before you design the state. This section was written
**before a line of `l3_forgetting.py` existed**, and every cost claim in it is an
assertion in `trials/ops/l3/t_state_composition.py` — the arithmetic is trialed,
not trusted.

### 0.1 The budget, and what the gate already spends of it

The Layer-3 budget is fixed by `trials/_l3tasks.py`, engine-independently:

```
budget_cap = budget_items × event_cost(payload) = 1000 × 11 = 11 000 work units
```

Two ratified gate clauses (§5 L3) then constrain the *composition* of state
before any design choice is made:

| clause | consequence |
|---|---|
| `unweighted-C ≥ 90‰` | ≥ 900 of the 10 000 stream items must be **recoverable**, so ≥ 900 must be **retained** |
| `weighted-C ≥ 850‰` | the retained set must include ~741 of the 800 heavy items (`ATTAINABILITY.md`) |

The retained set therefore costs **at least `900 × 11 = 9 900` units**, leaving a
remainder of **1 100 units — 10% of the budget** — to cover *everything else the
engine needs*: its index, its forgetting record, and any tier metadata.

Every claim below is an arithmetic fact about that 1 100-unit remainder.

### 0.2 Consequence (a) — L2-granularity indexing is impossible. CONFIRMED.

The Layer-2 index costs, per event, `len(atoms) + MINHASH_K` cells (README-l2,
`_index_cost`). On an `l3streamb` item that is `5 + 16 = 21` cells, so a retained
item at Layer-2 granularity costs `11 + 21 = 32`:

| | value |
|---|---|
| capacity at 32 units/item | **343 items** |
| its unweighted-C | **34‰** — against a 90‰ gate |
| cost of 900 items at L2 granularity | **28 800 units = 2.62 × the whole cap** |
| index budget actually available per item (900 items, 23-cell record) | **359/300 ≈ 1.20 units** |

So the L2 index is not merely expensive here, it is **excluded**: it overruns the
entire budget by 2.6× before the first index-free item is stored. 343 items is
also exactly the figure `humility/l3/IMPOSSIBILITY.md` measured for the capped
`layer_cap = 2` engine — the same wall, seen from the ascension side.

The remainder admits **at most one whole unit of index per retained item.** The
design that achieves it:

> **A single-posting handle index.** Each retained item contributes **exactly one
> posting entry** — its *handle atom*, the field-qualified, type-tagged token of
> the first field of the payload present in a frozen precedence list
> (`tag`, `id`, `entity`, `sid`, `src`, `dst`). Cost: **1 cell per retained
> item**, on the same accounting convention the frozen L2 index uses (one cell per
> posting entry; the atom string itself is not separately charged).
>
> What replaces the other 20 cells:
> * **the MinHash signature (16 cells) is deleted.** L2 needed it to *recognize*
>   near-duplicates approximately. L3 does not approximate: a cue's candidates
>   are verified by **exact containment against the stored payload**, which is
>   strictly sharper than a signature collision and costs nothing in state.
> * **the 4 remaining unigram/bigram atoms are deleted.** Discrimination moves
>   from the index to the verification step: the handle narrows to a cluster, and
>   exact containment picks out the one member that satisfies the whole probe.
>   Query time pays; **state does not**, and only state is budgeted (§4.1).

Per-item cost is therefore **12 units** (11 event + 1 posting).

### 0.3 Consequence (b) — per-eviction tombstones are impossible. CONFIRMED.

At 10× pressure the engine evicts ~9 086 of 10 000 items. A tombstone costing
even **one** cell per eviction gives `12n + (10 000 − n) ≤ 11 000`, i.e.

```
n ≤ 90 items   →   unweighted-C = 9‰   against a 90‰ gate
```

A one-cell tombstone table costs the layer **a tenfold shortfall on its own
coverage gate**. Nine thousand tombstones are 83% of the entire cap and 8× the
1 100-unit remainder. Per-eviction records are not expensive here; they are
**arithmetically unavailable**, exactly as `l3stream`'s gate was.

So the forgetting record must be **aggregated**, and its cost must be bounded by
a constant rather than by the number of evictions:

> **The aggregated forgetting record.** Per **logical-`t` range**, two integer
> accumulators — `evicted_count` and `evicted_mass` (summed grammar weight) —
> plus the stream totals:
>
> ```
> {"width": <int>, "buckets": [[count, mass], …], "count": <int>, "mass": <int>}
> ```
>
> Bucket `j` covers `t ∈ [j·width, (j+1)·width)`. `width` starts at
> `FORGET_WIDTH0 = 64` and **doubles**, merging bucket pairs, whenever an
> eviction's `t` would need a bucket index ≥ `FORGET_BUCKETS = 16`. The bucket
> count is therefore capped at 16 forever, and resolution — never coverage —
> degrades as the stream grows.
>
> **Stated total cost: `3 + 2 × len(buckets)` cells, at most `3 + 32 = 35`, and
> `23` on the frozen 10 000-item streams** (width settles at 1 024, ten buckets
> in use). Constant in the number of evictions, which is the whole point.

**What it answers for Layer 6, precisely.** "Did I forget something relevant
here?" — where *here* is a logical-time range — is answerable **yes/no with a
count and a mass**: `{"op":"forgot_at","t":T}` returns the bucket covering `T`,
and `{"op":"forgetting"}` returns the whole record. What it **cannot** answer is
*which* item, or its cue, or its payload: that is the per-eviction tombstone
§0.3 just proved unaffordable. So Layer 6 can distinguish *"I evicted 412 items
worth 1 038 of mass in the range containing your query"* from *"I have never
evicted anything near your query"* — a calibration signal — but it can never
reconstruct a dropped item. Reconstruction is Layer 4's claim, not ours (§4).

### 0.4 Consequence (c) — the Letta form choice: **B**, with intent recorded

GAPMAP **S4** (Letta `b76da90` `summarizer.py:244–342`) offers two constitutional
forms of hot/cold demotion, and instructs ASCEND to choose:

**Form A — two budgets: a full-granularity hot tier plus a reduced-granularity
cold tier, both refuse-on-exceed.** Priced against the same 11 000 units, with
`h` hot items at 32/item, `c` cold at 12/item and a 23-cell record:

```
32h + 12c + 23 ≤ 11 000 ,  h + c = the item count the coverage gate needs
```

| total items retained | its unweighted-C | affordable **hot** tier |
|---|---|---|
| 900 (the bare gate) | 90‰ — zero margin | **8 items** |
| 905 | 91‰ | 5 items |
| 910 | 91‰ | 2 items |
| 914 (what form B reaches) | 91‰ | **0 items** |

Each full-granularity hot item costs **1.67 cold items**, so form A buys an
8-item hot tier by spending the layer's entire coverage margin — and at the
occupancy form B actually reaches, the hot tier is **empty**. A two-budget design
whose hot tier holds 8 of 10 000 items is not a tier; it is a decoration with a
name. **Form A is arithmetically vestigial at this budget.**

**Form B — true eviction now, with the L4 co-design intent recorded.** Chosen.
An evicted item is **gone**: no cold copy, no demoted stub, no tier metadata
(0 cells — part of why B fits). What survives it is the aggregated record of
§0.3, which reports *that* and *how much* was forgotten, never *what*.

The recorded intent, so Layer 4 inherits a design and not a surprise:

> **L3→L4 co-design intent.** S4's other constitutional form —
> *demotion-into-consolidated-form*, where eviction compresses an item into a
> derived schema so cold growth is bounded by compression rather than by a second
> budget — is **deferred to Layer 4, deliberately, because it cannot be built
> before consolidation exists.** The arithmetic above is why: a cold tier is only
> affordable if a cold entry costs *materially less than an event*, and the only
> thing in the ladder that makes an entry cheaper than the event it came from is
> L4 compression (`footprint ≤ 250`, ≥4× — §5 L4). Layer 4 should therefore read
> this layer's eviction path as its **input**, not its rival: the item L3 drops is
> the item L4 must have abstracted *first*, and the aggregated record's
> `(t-range, count, mass)` is the ledger against which L4's schemas can be checked
> for having covered what eviction removed.

### 0.5 The composition, and what it reaches

| component | cost | on the frozen 10 000-item streams |
|---|---|---|
| retained events | `11 × n` | 10 054 at n = 914 |
| handle index | `1 × n` (one posting per item) | 914 |
| aggregated forgetting record | `3 + 2 × len(buckets)` ≤ 35 | 23 |
| tier metadata (form B has none) | **0** | 0 |
| **total** | `12n + record` | **10 991 ≤ 11 000** |

```
capacity = (11 000 − record) // 12 = 914 items   →   unweighted-C = 91‰  (gate 90‰)
```

The margin is 14 items, and it is *the whole margin*: at 13 units/item the
capacity falls to 844 items and **84‰ — a red gate**. That is how tight Layer 3's
state budget is, and it is why §0.2 and §0.3 had to be settled before the engine
was written rather than after.

---

## §1. The importance law (structural, exact, ordering-only)

Importance is **not** a policy knob and **not** a float. For a retained item `i`
at logical time `now`:

```
importance_i(now) = grammar_weight(payload_i) × Σ_{u ∈ uses(cluster_i)} 1/(now + 1 − u)
```

an exact `fractions.Fraction`, with three structural factors and nothing else:

* **grammar weight** — the payload's declared integer `importance` field, or `1`
  when the grammar declares none. L3 **reads** a declared weight; it does not
  *infer* importance from content (§3, non-capabilities).
* **reference count** — `|uses|`, the number of summands: the count of
  **distinct** payloads in the item's handle cluster. This is the frequency term
  of ACT-R's optimized base-level form, and it is where inflation resistance
  lives (§2).
* **logical-`t` recency** — the harmonic `d = 1` term `1/(now + 1 − u)` per use,
  the exact-rational surrogate for ACT-R's `t^{−d}` (THEORY §1: the float
  `d = 0.5` is a fit to human data and is deliberately **not** reproduced). The
  only clock is the engine-assigned logical `t` (§1.3).

**Only the ordering and the threshold bind** (THEORY §1, GAPMAP S7). The engine
never compares an activation to a constant: it compares two items, by exact
integer cross-multiplication of their `(numerator, denominator)` pairs — no float,
no `Fraction` object in the eviction hot loop, the same ordering to the last bit.

**Eviction is deterministic and totally ordered.** The victim is the least
important retained item, ties broken by **`t` ascending, then canonical payload
bytes ascending** (§2.4) — a total order, since `t` is unique within a state and
the byte tier settles any hypothetical remainder. `now` is the `t` about to be
assigned, so eviction is a pure function of `(state, payload)`.

**`uses` counts distinct payloads, first occurrence only.** A cluster's uses are
the `t`s at which each *distinct* payload in it first appeared. A byte-identical
repetition is therefore **not a use**: it adds neither frequency nor recency.
That single rule is what §2 rests on.

---

## §2. What the strains found (`trials/strain/l3/`)

### 2.1 Importance inflation: the attacked set survives whole

An adversary floods the store with byte-identical copies of one item, trying to
buy activation with repetition. Measured against 30 defended heavy items placed
**early** (the worst case for recency) at a 60-item cap:

| flood size | defended items surviving | slots the flood holds | cluster uses |
|---|---|---|---|
| 50 | **30 / 30** | 31 | **1** |
| 200 | **30 / 30** | 31 | **1** |
| 800 | **30 / 30** | 31 | **1** |

Two facts, and the second is the load-bearing one:

* **No mass is minted.** However many copies are retained, the cluster has
  **one** use, so its activation is exactly that of a single item first seen at
  `t_first` — asserted per copy, not in aggregate. The flood's footprint is
  identical at 50, 200 and 800 copies: **the attack does not scale.**
* **The naive count would have lost the set.** Counting every same-handle event
  as a use — the obvious implementation — reaches an activation **17× the weakest
  defended item's**, which would evict the attacked set outright. That
  counterfactual is computed as a trial fixture, never as engine code, so the
  guard is demonstrably load-bearing rather than merely present.

**The residual, stated rather than hidden.** Copies still *occupy slots* while
their cluster is recent (31 of 400, bounded by the store's recency window and
independent of the flood size). Layer 3 stores what it is given; reconciling
redundancy into one representative is **Layer 4's** claim. And an adversary who
can mint genuinely *distinct* payloads under one handle does raise that cluster's
reference count — that is **real overlap**, which the law is supposed to reward;
detecting "these are the same fact restated" is again consolidation, not
forgetting.

### 2.2 Near-duplicate pressure from murk

1 500 dirty events (52 near-duplicate pairs, 36 contradictions, ambiguities and
malformed payloads) at a 90-item cap — 1 399 forgotten, 101 retained. Checked at
the contested instant, the moment a twin arrives on a live original:

* **Neither pays full survival cost.** Twins share one handle cluster, so they
  carry **equal** importance and rise and fall together; the repetition is
  excluded from the cluster's uses, so `len(uses) < len(postings)` wherever a twin
  is retained — the cluster counts **facts, not restatements**.
* **No wrongful eviction, and no wrongful answer.** A repetition never evicts the
  fact it repeats (asserted as a forbidden outcome, not hoped for), and **no
  retained event is ever answered as a different event** — `wrong = 0` under full
  murk pressure. Two retained twins make a cue *ambiguous* and the engine abstains
  (§7.3); a **contradiction** pair — same handle, same key, different value — is
  separated **exactly** by the field that differs. This is where the traded MinHash
  is repaid: Layer 2 could only abstain on a signature collision, while exact
  containment resolves.

### 2.3 The heavy tier survives — and the crossover is stated

At 10× pressure on `l3streamb`, **all 800** heavy items survive; the remaining 114
slots hold the most recent light items, for `weighted-C = 917‰` against a 918‰
oracle ceiling. But importance is a **rate**, not a hoard: a heavy item's
activation decays as `1/age`, so it is not immortal. From the state the engine
actually reached, the weakest retained light item scores `3/191` and a heavy item
outranks it until age

```
240 / (3/191) = 15 280      against this stream's length of 10 000
```

so a stream about **1.5× longer** would begin surrendering the earliest heavy
items to dense recent traffic. That is the ACT-R law working as designed, and it
is asserted as a bound rather than left as a surprise for Layer 4.

### 2.4 Determinism, and the order-dependence that lawfully exists

* **Determinism (§2.3).** The same stream twice gives byte-identical snapshots,
  evictions included, and `restore(snapshot(s))` re-snapshots to the same bytes
  after 9 086 evictions.
* **Declared-safe permutation.** Swapping two *adjacent* arrivals of equal grammar
  weight and distinct handles leaves the `(weight, t)` multiset unchanged, so every
  later eviction decision sees the same order: the **retained payload multiset is
  invariant**, as are the forgetting record's count and mass.
* **Lawful order-dependence, asserted so the safe class is not vacuous.** Moving an
  item to a different position changes its recency, and recency is a *factor of
  importance* — an item the stream dropped from its head **survives** when moved to
  its tail. Order matters, in exactly the way the law says it should.

---

## §3. What Layer 3 CAN express

- **Principled eviction under 10× pressure.** On the binding corpus
  (`corpora/l3streamb`, BOUNDARY-RULINGS.md R1): **weighted-C = 917‰,
  unweighted-C = 91‰, F = 1000, B = 1000** against a gate of
  `weighted-C ≥ 850, unweighted-C ≥ 90, F ≥ 950, B = 1000`. The oracle ceiling —
  the best any retain-or-drop policy could reach — is **918‰**, so the engine lands
  **1‰ off the arithmetic optimum**, while both capability-free baselines
  (fill-then-refuse, keep-latest) are pinned at 100‰ and the capped `layer_cap = 2`
  engine measures 34‰.
- **Forgetting that never corrupts.** `F = 1000`: every retained item is returned
  byte-exact for its cue, `wrong = 0`, `fabricated = 0`. An evicted cue and a
  never-ingested cue both **abstain** (§7.3) — honest forgetting, never invention.
- **The budget law, absolutely, at every instant.** Occupancy is asserted against
  the cap **after every one of 10 000 writes**, and the engine evicts *before* it
  inserts, so no observable state ever exceeds the cap. `B = 1000` on **both**
  streams. The accounting identity holds exactly: `occupancy = 12 × retained +
  record`, with no cell of state unaccounted for.
- **An aggregated account of what is gone.** `{"op":"forgetting"}` and
  `{"op":"forgot_at","t":T}` answer *how many* items and *how much mass* were
  forgotten in a logical-`t` range, in `3 + 2 × buckets ≤ 35` cells, bounded
  forever by coarsening.
- **Determinism through eviction.** Byte-identical snapshots across identical
  streams; the post-eviction state is anchored in `anchors/l3.json`, so a change in
  the importance law, the eviction order, the tie-break or the record's coarsening
  turns the suite red even when every score still clears the gate.
- **Layers 1 and 2, carried forward on the retained set.** `read`, `read_range` and
  `recall` all still answer, over what survives.

## §4. What Layer 3 CANNOT express (the boundary for Layer 4+)

- **No reconstruction of what it dropped — the Layer-4 humility seam.** This is
  the precise statement, and it is a **witness**, not a promise: two streams that
  differ in the *content* of an evicted item — same grammar weight, same handle,
  same arrival time — produce **byte-identical snapshots**
  (`strain/l3::trial_two_streams_differing_only_in_what_was_forgotten_are_indistinguishable`).
  So a forgotten payload leaves **no trace at all** in state: not a hash, not a
  length, not a field. The forgetting record is 16 pairs of integers however many
  distinct items were dropped, so **no injective map from the evicted set into
  Layer-3 state exists**, and reconstruction from it is impossible in principle
  rather than merely hard.

  Stated for the layer above: **eviction drops what consolidation would have
  abstracted.** At the Layer-4 gate's own footprint (`≤ 250` units, ≥4×
  compression) this engine holds `250 // 12 = 20` items — twenty of ten thousand —
  and must abstain on all the rest, because dropping is not deriving. That is the
  gap `footprint ≤ 250` at `reconstruction F ≥ 900` measures, and
  `humility/l4/IMPOSSIBILITY.md` should be written against the witness above:
  the capped `layer_cap = 3` engine cannot exceed its `F ≤ 400` ceiling because
  the information it would need is provably absent from its state, not merely
  inconvenient to recover. The `(t-range, count, mass)` ledger is what Layer 4
  inherits: the account against which its schemas can be checked for having
  covered what eviction removed (§0.4, the recorded S4 co-design intent).
- **No reconciliation of redundancy or contradiction.** Byte-identical twins are
  both stored when the budget allows and both compete for space; a cue matching two
  retained events **abstains** rather than picking one. Deriving "the current value
  among conflicts", or one representative from a near-duplicate cluster, is
  **Layer 4**. §2.1's residual — copies occupying slots while their cluster is
  recent — is this same boundary seen from the budget side.
- **No inference of importance from content.** L3 **reads** the grammar's declared
  integer weight (`importance`, else 1) and combines it with structural reference
  count and logical-`t` recency. It does not judge that an undeclared item matters;
  a corpus that declares nothing is ranked by reference count and recency alone.
  What Layer 3 claims is *eviction ranked by importance*, not *importance
  estimation*.
- **A narrower recall channel than Layer 2, by budget arithmetic and on the
  record.** §0.2 priced the Layer-2 index out at this cap, so recall here needs the
  cue to name the item's **handle** field: a cue naming only non-handle fields
  abstains, and so does one naming `dst` where `src` was the handle. Within a
  handle, verification is *exact* and therefore sharper than Layer 2 (no
  normalization conflating `7` with `"7"`, no MinHash collision); across handles it
  is blind where Layer 2 could still associate. Both engines exist and neither is
  edited: `adapters/l2` remains the full-granularity recall channel at a budget
  that can afford it. Layer 3's is what 1 100 leftover units buy.
- **No prospection, meta-memory, generation, or binding provenance.** Confidence is
  emitted as structural certainty (1000 on a verified answer) but **ungated** until
  Layer 6 (§3.4) — and the aggregated record is what will let Layer 6 tell
  *evicted* from *never ingested*, which `recall` deliberately cannot. Provenance
  tags are attached but neither required nor scored until Layer 7 (§4.2). No
  `intend`, no calibrated confidence model, no `generate` — Layers 5, 6, 7.

## Reading list for the next session

Per `CLAUDE.md §1`, the next session reads this README before acting. The one
sentence to carry forward: **Layer 3 keeps what an exact ACT-R base-level
ordering says matters — grammar weight × distinct-reference count × harmonic
logical-`t` recency — evicting the least important item deterministically before
every write that would breach the cap, retaining 914 of 10 000 items for 917‰ of
the importance mass against a 918‰ ceiling, corrupting nothing it keeps, and
leaving of everything it drops only a bounded per-`t`-range count and mass, so
what it forgot is gone in a way no Layer-3 state could reconstruct.**


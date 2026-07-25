# ATTAINABILITY.md — what the Layer-4 gate can and cannot reach, per corpus

**BOUNDARY-RULINGS.md R2** put attainability before authority: *"a gate must lie
strictly below the oracle ceiling and strictly above every capability-free
baseline on its binding corpus, and that arithmetic must be computed and recorded
in an `ATTAINABILITY.md` BEFORE the gate binds."* This is that document for
Layer 4, written **before a line of `core/layers/l4_consolidation.py` exists** and
before any Layer-4 trial applies a gate to an engine.

Everything numeric here is computed by `trials/_l4tasks.py` from the frozen
corpora and the frozen §4.1 cost model alone, and asserted by
`trials/ascension/l4/t_attainability.py`, so no number below can drift silently.

**The verdict, first.** The ratified Layer-4 gate is **unattainable on the frozen
chronicle family by any policy whatsoever** — the same category of defect R1
found at Layer 3, arriving one layer up for a different reason. A new corpus,
`corpora/l4stream`, is frozen this session on the same append-only path
`l3streamb` took; on it the gate discriminates with margin on both sides. The
binding is **not** made by this session: it is proposed in
`RULING-R4-DRAFT.md` for human ratification, and **until that ruling exists no
Layer-4 gate binds on anything.** Per the ASCEND directive's own instruction,
Stage A is delivered as its own committed session and stops here.

---

## §1. What `footprint ≤ 250` means, and an erratum

`BOUNDARY.md §5 L4` gates on

```
footprint≤250 (≥4× compression) at reconstruction F≥900, C≥850, B=1000
```

and `§5.1 L4` defends the first clause as *"Derived schemas must shrink the
episodic footprint to at most a quarter of the raw bytes."*

Three ratified statements — `250`, `≥4×`, *a quarter* — are **one** statement iff
`250` is read in **permille**, the unit §3 establishes for every measure in the
constitution: `1000/250 = 4`, and a quarter is 250‰. Under any absolute reading
of `250` the parenthetical `≥4×` and the defense sentence's *a quarter* would both
have to be coincidences of one particular corpus size. So:

```
raw_cells   = Σ_t event_cost(payload_t)        the episodic footprint (§4.1)
footprint‰  = permille(state_cells / raw_cells)
the gate    = footprint‰ ≤ 250   ==   state_cells ≤ raw_cells // 4
budget_cap  = raw_cells // 4                   (§4.1, the same number)
```

The footprint gate and the budget law are then the same sentence read twice, and
the ratified `B = 1000` is not redundant beside it: `B` certifies the cap held
**after every write** (`§3.3`, `§4.1.2`), while `footprint` is what the final
state costs.

A third ratified sentence confirms the reading independently. `§5.1 L4`'s humility
defense reads: *"a forget-only engine squeezed to a quarter of the bytes has
simply lost three-quarters of its episodes."* Measured, the `layer_cap = 3` engine
at footprint 250‰ retains **250‰ of the episodes of `l4stream`** (5 010 of 20 000)
and 272‰ of chronicle's — three-quarters lost, exactly as defended. Under an
absolute reading of `250` **units** the same engine would hold `250 // 12 = 20`
items of 20 000, having lost 99.9% of its episodes, and the defense sentence would
be describing something else entirely.

> **Erratum, recorded and not acted on.** `core/layers/README-l3.md §4` reads the
> Layer-4 footprint as *"`≤ 250` units"* and computes `250 // 12 = 20` items from
> it. That README is **frozen** (§9.2) and is **not edited**; the reading it used
> is superseded here on the strength of the three ratified sentences above, and
> the disagreement is put on the record rather than quietly resolved. Nothing
> else in that section depends on it: the seam it draws — that a forget-only
> engine cannot reconstruct what it dropped — holds under either reading, and
> holds more sharply under this one, since 5 010 retained episodes still leave
> 14 990 unreconstructible.

### Pricing rule P — one cell, one grammar atom

The §4.1 cost model charges one cell per scalar and one per key, and says nothing
about what a scalar may *contain*. Unconstrained, a state could pack a whole
corpus into a single integer and price it at one cell, and every number in this
document would be meaningless. **Rule P** closes that:

> Every stored cell holds exactly one **grammar atom** — an entity id, a
> vocabulary token, an attribute value, or a logical `t`. A composite key
> (`"7:status"`), a bit-packed integer, or any concatenation carrying more than
> one atom is priced at the number of atoms it carries, not at one cell.

Rule P is the premise under which every ceiling below is a bound rather than a
wish, and it is the constraint the Stage-C engine is to be held to structurally.

---

## §2. The battery: what Layer 4 is asked

Layer 4 answers four question classes. The reconciliation the GAPMAP steals
imply — that supersession lives **here** and not at Layer 6 — is what Q1 and Q2
are.

| facet | one query per | answer | measure |
|---|---|---|---|
| **Q1** current-value | distinct `(entity, key)` pair | the value at the pair's greatest `t` | C |
| **Q2** as-of | **non-terminal** assertion | the value in force at that assertion's `t` | C |
| **Q3** pattern | entity, plus one per grammar kind | that entity's action-count profile / the global count | C |
| **Q4** reconstruction | event `t` | the payload of the event at `t` | F |

**Q2 asks only about the past.** A pair's terminal assertion is excluded from the
Q2 battery, because *as-of at the latest `t`* is the Q1 question wearing a `t`,
and a current-value table with no history whatsoever would answer it. A pair
asserted exactly once therefore contributes no Q2 query at all. This is what
makes Q2 a test of attribute **history** — the Graphiti steal (GAPMAP **S3**),
cured of model-dependence: `valid_from`/`invalid_from` are integer logical stamps
and the two LLM calls Graphiti pays for become interval arithmetic.

### `F` at Layer 4 is the **literal** §3.0 table, and no ruling is requested

**R3 does not reach Layer 4**, and says so in its own text: *"It does not reach
layers where eviction is not compulsory. Layers 1, 2, 4, 5, 6 and 7 score F under
the literal §3.0 table unless and until a later ruling says otherwise."* So at
Layer 4 an abstention on an answerable query scores **100**, not 1000, and

```
F ≥ 9/10   ⟺   at least 8/9 of all events reconstructed EXACTLY
```

since `(1000x + 100(n−x)) / 1000n ≥ 9/10` reduces to `x ≥ 8n/9`. That identity is
exact on the `Fraction`, which is where §3.1 defines `F`. The §5 gate is applied
to the **permille calibration** of it, and §3.5's round-half-to-even therefore
admits an exact `F` as low as `899.5‰` — half a permille point, which on
`l4stream` is 11 events of 20 000. Stated rather than rounded past: the honest
form of the gate is *8/9 of the stream, less half a permille of rounding*, and
`t_attainability.py` asserts the concession in the measure rather than in
events, because half a permille is a property of §3.5 while events-per-permille
is a property of a corpus's scale.

**No extension of R3 to Layer 4 is requested.** §4 below shows the `F ≥ 900` gate
is attainable on the proposed binding corpus under the literal table, so the layer
does not need the friendlier reading and declines to ask for it. The corruption
reading is computed alongside as the ungated diagnostic `F_corruption` —
R3's pairing **inverted**, so that the stricter number is the one that binds and
the looser one is the one on display.

---

## §3. The oracle, and the family it is exact over

**Construct family F**, declared so that the ceiling below is a statement with a
scope rather than an intuition. A state is a choice of:

| construct | cells | answers |
|---|---|---|
| entity, touched | 1 | (prerequisite for its pairs) |
| pair at **CURRENT** | 2 (its key cell + one value cell) | `Q1(p)`. Stores no `t`, so it **reconstructs nothing** — `reconstruction(t)` must name the event *at* `t` |
| pair at **FULL** (chain `c`) | `1 + 2c` (key cell + `c` × `[t, value]`) | `Q1(p)`, the `c−1` past-facing `Q2(p, ·)`, and all `c` of its reconstructions |
| entity profile | free where every pair of that entity is FULL, else `kinds(e) + 1` | `Q3(e)` |
| global counters | `2` per grammar kind | the `K` global-count queries |
| irreducible event | 3 (`[t, entity, id]`) | its reconstruction only |

**Why a partial history is not in F.** For a pair with chain `c`, storing a suffix
of depth `k` costs `1 + 2k` and answers `k` coverage queries, a ratio
`k/(1+2k)` **strictly increasing** in `k`. So among history constructs only
`k = c` is ever on the frontier, and `CURRENT` (ratio `1/2`) strictly dominates
every one of them. That is why the maximization is a greedy — open every pair at
CURRENT, then upgrade whole chains longest-first — and why the greedy is **exact
within F**, not a heuristic.

**Where F's edge is.** A positional encoding — a dense array over the pair
universe, position implying identity and charging no key cell — is legal under
rule P and is *cheaper* than CURRENT. It changes no verdict here, for two
different reasons on the two sides:

- on `l4stream` the ceiling is not argued from F at all: §4 **exhibits a concrete
  state** that attains it, so the "strictly below the oracle" half of R2 needs no
  family assumption on the corpus where it matters;
- on the chronicle family the pair universe is **not bounded by the grammar** —
  entity ids are discovered from the data — so a dense array over
  `entities × keys` costs `9 985 × 18 = 179 730` cells against a `98 908` budget,
  nearly twice the entire footprint. The cheaper encoding is unavailable exactly
  where it would be needed.

This is stated rather than assumed away: the negative verdict of §5 is *exact
within F*, and F is declared above.

---

## §4. `corpora/l4stream` — the gate is a real test

Frozen this session at seed `6006`, `n = 20 000`, on the same append-only path
`l3streamb` took at Layer 3: the existing corpora are untouched, a new one is
added, and the arithmetic is recorded before anything binds.

```
n = 20 000 events     raw_cells = 173 200     budget_cap = 43 300  (= 250‰)
entities 200   pairs 2 951   assertions 18 788   irreducible (`note`) 1 212
mean supersession chain 6.367     longest chain 19
battery:  Q1 2 951 + Q2 15 837 + Q3 205 = 18 993 coverage targets;  Q4 20 000
```

### The witness — exhibited, not argued

The **exact minimal-sufficient state** for the whole coverage battery is the
interval table plus the global counters:

```
interval table   = entities + pairs + 2 × assertions
                 =    200   + 2 951 +  37 576        = 40 727 cells
global counters  = 2 × 5 kinds                       =     10 cells
                                                       ------
minimal sufficient                                     40 737 cells  = 235‰
```

It **fits**, with `43 300 − 40 737 = 2 563` cells (15‰ of the raw footprint) to
spare, and those spare cells buy `854` of the 1 212 irreducible `note` events at
3 cells each. That single concrete state scores:

| | value | gate |
|---|---|---|
| footprint | **250‰** (43 299 of 43 300 cells) | ≤ 250 |
| C (Q1 + Q2 + Q3, all answered) | **1000‰** | ≥ 850 |
| reconstruction F, **literal §3.0** (19 642 of 20 000 exact) | **984‰** | ≥ 900 |
| `F_corruption` (the R3 reading, ungated diagnostic) | 1000‰ | — |

Q3 is free here rather than cheap: an action-count profile is a fold over
complete chains, and every chain is complete. The family maximization agrees —
`C ≤ 1000`, `F ≤ 984` — which is the check that the witness is not merely good but
optimal.

### The discrimination check (R2, both obligations)

| policy | C | F |
|---|---|---|
| **oracle ceiling** (exhibited above) | **1000** | **984** |
| the ratified gate | **850** | **900** |
| (i) verbatim-truncation at 250‰, keep-latest | 247 | 325 |
| (i) verbatim-truncation at 250‰, keep-first | 249 | 327 |
| (ii) current-value-table-only (6 102 cells, 35‰) | 155 | 100 |
| (iii) `make_engine(layer_cap = 3)` at 250‰ — arithmetic **upper bound** | 200 | **325** |

- **Strictly below the oracle**: `850 < 1000` and `900 < 984`. ✔
- **Strictly above every named baseline**: `850 > 249` and `900 > 327`. ✔
- **The humility ceiling is honest and not vacuous**: §5 L4 allows the capped
  engine `reconstruction F ≤ 400`; its arithmetic ceiling here is **325**, so the
  ceiling binds without being unreachable. ✔

Each baseline earns its place rather than decorating the table:

- **(i) verbatim truncation** is what "just keep a quarter of the raw events" buys.
  It is scored in its *strongest* variant (keep-latest, because a current value is
  more likely to be a recent assertion) and still reaches 247: consolidation is not
  a synonym for truncation.
- **(ii) the current-value table** is the policy that answers *today* and has no
  history at all. It costs 35‰ and reaches 155 — and reconstructs **nothing**,
  scoring F at the abstention floor of 100, because it stores no `t` and
  `reconstruction(t)` must name the event at `t`. It is in the table because on
  the chronicle family (§5) this same policy nearly ties the optimum.
- **(iii) the capped `layer_cap = 3` engine** is priced at `event_cost + 1` per
  retained item — the event plus its single handle posting (`README-l3 §0.5`) —
  retaining the **cheapest** items first, which no importance ordering can beat on
  count, and then credited with every query those retained events could
  conceivably support. It is a ceiling on the capped engine, not a measurement of
  one, which is what `humility/l4/IMPOSSIBILITY.md` will need.

### What the margin is, honestly

The engine's working room is **2 563 cells — 5.9% of the budget**. Everything the
Stage-C engine needs beyond the bare interval table (any index, any derived-vs-
episodic marking, any bookkeeping the Form-B eviction path requires) comes out of
that, and the irreducible tier competes for the same cells. This is the Layer-4
analogue of Layer 3's 14-item margin: tight by arithmetic, not by choice, and
recorded now so Stage C inherits a number rather than a surprise.

---

## §5. The chronicle family — the gate is unattainable

### chronicle (`s1001`, `n = 50 000`)

```
raw_cells 395 632   budget_cap 98 908 (= 250‰)
entities 9 985   pairs 41 785   assertions 50 000   irreducible 0
mean supersession chain 1.197     terminal share 836‰
battery:  Q1 41 785 + Q2 8 215 + Q3 9 990 = 59 990 coverage targets;  Q4 50 000
```

**The exact minimal-sufficient state does not fit, and not narrowly:**

```
interval table + counters = 9 985 + 41 785 + 100 000 + 10 = 151 780 cells = 384‰
against a budget of                                          98 908 cells = 250‰
                                                    short by 52 872 cells
```

Chronicle needs **1.53× the entire Layer-4 footprint** to hold its own history
exactly. And the family maximization at 250‰ reaches only

| | C | F |
|---|---|---|
| **oracle ceiling** | **735** | **683** |
| the ratified gate | 850 | 900 |
| verdict | **short by 115‰** | **short by 217‰** |

**Why, in one sentence:** consolidation buys compression from redundancy, and
**chronicle has 1.197× where the gate demands 4×**. 35 947 of its 41 785 pairs are
asserted exactly once and never superseded; `836‰` of its assertions are their
pair's latest. It is a *write-once world*, so 35% of any exact history schema goes
on **identifying** pairs rather than on their values — `9 985 + 41 785 = 51 770`
cells of identification against `100 000` of content — and identification is
precisely what does not compress.

**And the second consequence, which is R1's finding arriving one layer up.** On
chronicle the **current-value table with no history whatsoever scores 697** —
**95% of the 735 arithmetic optimum** (on murk, 647 against 754, 86%), at 236‰ of
the footprint. A policy
containing no consolidation at all, no as-of, no interval, no pattern fold, comes
within 38‰ of the best any state in the family can do. Chronicle cannot, by
itself, distinguish a consolidating engine from a table of last-writes, exactly as
`l3stream` could not distinguish an importance ordering from a ring buffer. Even
if its ceiling reached the gate, R2 obligation 2 would void a gate bound there.

### murk (`s3003`, `n = 10 000`)

```
raw_cells 79 446   budget_cap 19 861 (= 250‰)
entities 1 798   pairs 7 519   assertions 9 810   irreducible 190 (malformed)
mean supersession chain 1.305     terminal share 766‰
minimal sufficient 28 949 cells = 364‰   —   short by 9 088 cells
oracle ceiling:  C ≤ 754,  F ≤ 711     current-value-table-only:  C = 647, F = 100
```

Murk inherits chronicle's grammar and therefore chronicle's write-once shape. Its
oracle is **754** against an 850 gate and **711** against a 900 gate; its
current-value baseline reaches 647. The same verdict, for the same reason.

This does **not** retire murk from Layer 4. Its **305 recorded contradictions**
(`corpora/murk/ground_truth.json`, 158 entities, longest chain 9) are the answer
key against which consolidation's supersession must resolve-or-abstain per §3.0,
and that is a **strain** obligation (Stage D (c)), not a gate. A corpus can be the
right dirt without being the right ruler.

---

## §6. The verdict, and what is *not* being done here

**The discrimination check fails on the chronicle family and passes on
`l4stream`.** Per the ASCEND directive — *"do not proceed past a failed
discrimination check; deliver Stage A as its own committed session (corpus +
ATTAINABILITY + any ruling draft for human ratification) and stop"* — this session
stops at the end of Stage A. No Layer-4 ascension battery, no humility battery, no
inheritance battery, and no engine.

**No gate binds yet.** R2 obligation 4 is explicit: *"A gate that has not had this
arithmetic computed has no authority yet."* The arithmetic is now computed and on
the record, which is a necessary condition and not a sufficient one — the
**corpus binding** is a question the constitution leaves open in exactly the way
R1 answered it for Layer 3, and it is a human's to settle. `RULING-R4-DRAFT.md`
states the proposed holding; it is a **draft** and is deliberately **not** appended
to `BOUNDARY-RULINGS.md`, because appending is what freezes an entry and this
session has no authority to freeze a ruling for itself.

**No frozen artifact was edited.** `BOUNDARY.md`, `BOUNDARY-RULINGS.md`, every
frozen corpus, every frozen layer, `core/layers/README-l3.md` and every existing
trial's behaviour are untouched. What this session adds is: one new corpus, one
engine-free task module, one ops trial, one attainability trial, this document,
and a ruling draft. `trials/laws/t_rulings.py`'s gate registry receives the four
Layer-4 constants — the additive extension that file exists to hold, and the
mechanism by which a new gate constant cannot exist without a recorded authority.

**What a human is being asked to decide.** Three things, in order of how much they
bind:

1. **The footprint reading** (§1) — `250` as permille of the raw episodic
   footprint. Determinate from three ratified sentences in my reading, and
   contradicted by one frozen README's parenthetical, which is why it is put up
   for ratification rather than assumed.
2. **The corpus binding** (§4, §5) — the Layer-4 ascension gate on
   `corpora/l4stream`, with chronicle and murk scored as ungated diagnostics on
   the conditional-arithmetic-skip mechanism R1 endorsed as permanent.
3. **Pricing rule P** (§1) — one cell, one grammar atom, without which no
   footprint number means anything.

Until then, `trials/ascension/l4/t_attainability.py` asserts every number above
and applies no gate to any engine, and `trials/humility/l4/` does not exist.

# RULING-R4-DRAFT.md — proposed, **not** ratified, **not** in force

> **This is a draft.** It is deliberately **not** appended to
> `BOUNDARY-RULINGS.md`, because appending is what freezes an entry
> (`BOUNDARY-RULINGS.md` header; `laws/t_rulings.py` check 2), and a session has
> no authority to freeze a ruling for its own benefit. It lives here, under the
> ascension trial that computed the arithmetic, until a human ratifies it in a
> `RULING` session — or rejects it, or replaces it with something else.
>
> **Nothing in this file binds anything today.** No Layer-4 gate is applied to
> any engine, and none will be until an entry with this content — or different
> content — exists in the frozen supplement. `trials/ascension/l4/` currently
> contains attainability arithmetic and no ascension battery.

**Proposed ID:** `R4` (the next free entry; IDs are assigned in order and never
reused).
**Would bind:** the Layer-4 ascension trials (`trials/ascension/l4/`) and the
Layer-4 humility trial (`trials/humility/l4/`), when either exists.
**Authority invoked:** `BOUNDARY.md §5 L4`, `§5.1 L4`, `§3` (the permille unit),
`§4.1` (the budget law and its cost model), `§8` (the corpora doctrine);
`BOUNDARY-RULINGS.md R1` (the precedent for binding a stated threshold to a
corpus), `R2` (which requires the arithmetic below to exist before any of this
binds), `R3` (whose scope this ruling deliberately does **not** extend).
**Proposed holding:** the ratified Layer-4 thresholds stand **unchanged**;
`footprint ≤ 250` is read in **permille of the raw episodic footprint**; the
Layer-4 ascension gate binds on **`corpora/l4stream`**; `corpora/chronicle` and
`corpora/murk` are scored as **ungated diagnostics**; state is priced under
**rule P**, one cell per grammar atom.

---

## The three questions

`BOUNDARY.md §5 L4` states the Layer-4 gate as

```
footprint≤250 (≥4× compression) at reconstruction F≥900, C≥850, B=1000
```

and leaves three things open, each of the kind `BOUNDARY-RULINGS.md`'s own
preamble names as legitimately rulable — *"which reading of a ratified defense
sentence the trials implement"*, *"which corpus a stated gate binds on"*, and
*"what procedure binds future gates"*.

1. **In what unit is `250`?** The constitution gives a bare number.
2. **On which corpus?** §5 L4 names none, exactly as §5 L3 named none.
3. **How is a state priced?** §4.1 charges one cell per scalar and per key, and
   says nothing about what a scalar may contain — so an unconstrained state could
   pack a whole corpus into one integer and price it at one cell.

The full arithmetic is in `ATTAINABILITY.md`, computed and machine-checked before
this draft was written and before any engine exists.

---

## Proposed clause 1 — `footprint ≤ 250` is 250 permille of the raw episodic footprint

```
raw_cells   = Σ_t event_cost(payload_t)          the episodic footprint (§4.1)
footprint‰  = permille(state_cells / raw_cells)
the gate    = footprint‰ ≤ 250   ==   state_cells ≤ raw_cells // 4
budget_cap  = raw_cells // 4                     the §4.1 cap, the same number
```

**Why this reading and no other.** Three ratified sentences say the same thing
under it and three different things under any absolute reading:

- §5 L4's own parenthetical, `(≥4× compression)`: `1000 / 250 = 4`.
- §5.1 L4's defense: *"shrink the episodic footprint to at most a quarter of the
  raw bytes"* — a quarter is 250‰.
- §5.1 L4's humility defense: *"a forget-only engine squeezed to a quarter of the
  bytes has simply lost three-quarters of its episodes."* Measured, the
  `layer_cap = 3` engine at this cap holds **250‰ of `l4stream`'s episodes** —
  three-quarters lost, as defended. Under an absolute reading of 250 *units* the
  same engine holds 20 episodes of 20 000 and has lost 99.9% of them, and the
  defense sentence describes nothing that happens.

§3 is also the constitution's own answer to *"in what unit"*: every measure it
defines is calibrated to an integer **in permille**, and `permille` is the one
rounding rule §3.5 provides.

**What this clause costs.** `core/layers/README-l3.md §4` — frozen, and **not
edited** — reads the same clause as *"≤ 250 units"* and derives `250 // 12 = 20`
items from it. Ratifying this clause supersedes that parenthetical. It leaves the
seam that section actually draws untouched and in fact sharper: a forget-only
engine at 250‰ retains 5 010 of `l4stream`'s 20 000 episodes and still cannot
reconstruct the other 14 990.

---

## Proposed clause 2 — the gate binds on `corpora/l4stream`

**The ratified thresholds stand, unchanged.** `footprint ≤ 250`,
`reconstruction F ≥ 900`, `C ≥ 850`, `B = 1000` and the humility ceiling
`capped reconstruction F ≤ 400` are ratified text and are not touched, softened,
rescaled, or read as a fraction of anything.

**On the frozen chronicle family the gate is unattainable by any policy.**

| | `chronicle` | `murk` | `l4stream` |
|---|---|---|---|
| mean supersession chain | 1.197 | 1.305 | **6.367** |
| terminal-assertion share | 836‰ | 766‰ | **157‰** |
| exact history schema | 384‰ | 364‰ | **235‰** |
| oracle ceiling, C | 735 | 754 | **1000** |
| oracle ceiling, reconstruction-F | 683 | 711 | **984** |
| the ratified gate | 850 / 900 | 850 / 900 | 850 / 900 |
| **verdict** | short by 115 / 217 | short by 96 / 189 | **clears by 150 / 84** |

Consolidation buys compression from **redundancy**, and the chronicle grammar has
1.197× where the gate demands 4×: 35 947 of its 41 785 `(entity, key)` pairs are
asserted exactly once and never superseded. It is a write-once world, so 51 770 of
the 151 780 cells its exact history costs go on **identifying** pairs rather than
on their values — and identification is precisely what does not compress.

**And chronicle could not carry the gate even if it reached it.** There the
current-value table — no history, no as-of, no interval, no pattern fold — scores
**697 against a 735 optimum**: 95% of the best any state can do, with none of the
capability. That is R1's `l3stream` finding arriving one layer up, and R2
obligation 2 voids a gate a capability-free policy sits at.

**On `l4stream` the gate discriminates on both sides**, and the upper side is
**exhibited rather than argued** — a concrete state (the exact interval table, the
global counters, and 854 of the 1 212 irreducible events) fits the footprint
exactly and scores `C = 1000`, `F = 984`:

| policy | C | F |
|---|---|---|
| exhibited oracle state | **1000** | **984** |
| gate | 850 | 900 |
| verbatim-truncation at 250‰ (keep-latest / keep-first) | 247 / 249 | 325 / 327 |
| current-value-table-only | 155 | 100 |
| `make_engine(layer_cap = 3)` at 250‰ (arithmetic upper bound) | 200 | **325** |

The §5 L4 humility ceiling of 400 is neither breached (325 < 400) nor vacuous
(325 > the 100 abstention floor).

**`corpora/chronicle` and `corpora/murk` remain, and are scored as ungated
diagnostics**, on the conditional-arithmetic-skip mechanism R1 clause 5 endorsed
as permanent: their ceilings are computed, recorded and drift-checked; a Layer-4
ascension trial on them skips **only while** the ceiling lies below the gate, and
engages by itself if that ever changes. Neither corpus is retired, neither's bytes
change, and murk keeps its Layer-4 obligation in full — its **305 recorded
contradictions** are the answer key against which consolidation must resolve or
abstain per §3.0, which is a **strain** obligation and not a gate.

**What this clause does not license.** Not "score it on an easier corpus". R1
already refused that reading of itself, and the same refusal is repeated here: the
§5 corpus preconditions bind first, the arithmetic is a check applied to a corpus
already admissible, and `l4stream` is *harder* in the sense that matters —
chronicle cannot distinguish consolidation from a table of last-writes, and
`l4stream` pins that same policy at 155.

---

## Proposed clause 3 — pricing rule P: one cell, one grammar atom

> Every stored cell holds exactly one **grammar atom** — an entity id, a
> vocabulary token, an attribute value, or a logical `t`. A composite key
> (`"7:status"`), a bit-packed integer, or any concatenation carrying more than
> one atom is priced at the number of atoms it carries, not at one cell.

Without rule P no footprint number means anything: §4.1's cost model charges per
scalar and per key without constraining what a scalar contains, so a state could
serialize a corpus into a single integer and claim a footprint of one cell. Rule P
is the smallest constraint that closes the hole while changing no ratified
sentence — it does not alter `payload_cost`, it states what a *lawful* state may
put in a cell, and it is checkable structurally rather than by inspection.

Rule P is stated as a **general** pricing rule, not a Layer-4 one: it makes every
footprint and occupancy figure in the project mean what it has always been read to
mean. Layers 1–3 already satisfy it (they store grammar values verbatim), so
ratifying it changes no existing score.

---

## Proposed clause 4 — Layer 4 scores `F` under the literal §3.0 table

R3 excludes itself from Layer 4 in its own text: *"Layers 1, 2, 4, 5, 6 and 7
score F under the literal §3.0 table unless and until a later ruling says
otherwise."* **This draft is not that ruling and does not ask to be.** At Layer 4
an honest abstention on an answerable reconstruction scores **100**, so

```
F ≥ 9/10   ⟺   at least 8/9 of all events reconstructed EXACTLY
```

exactly on the `Fraction` (§3.5's permille calibration concedes half a permille
point on top — 11 events of 20 000 on `l4stream`, recorded in
`ATTAINABILITY.md §2` rather than rounded past). `ATTAINABILITY.md §4` shows that gate is attainable on `l4stream` under the
literal table (`F = 984`), so the layer does not need the friendlier reading. The
corruption reading is computed alongside as the ungated diagnostic
`F_corruption` — R3's pairing inverted, so the **stricter** number binds and the
looser one is merely on display.

Recorded here because declining an available concession is a decision, and a
later session should be able to see that it was made deliberately rather than
overlooked.

---

## What this draft would not do

- It would **not** amend `BOUNDARY.md`. No ratified sentence is edited or reread.
- It would **not** change any threshold, in either direction, on any layer.
- It would **not** retire `corpora/chronicle` or `corpora/murk`, weaken their ops
  trials, or touch their frozen bytes.
- It would **not** edit `core/layers/README-l3.md`. Clause 1 supersedes one
  parenthetical in a frozen document by stating the better reading on the record;
  the frozen text stays as it is, wrong on that point, forever.
- It would **not** extend R3 to Layer 4, or to anything.

## Where it would be enforced, if ratified

- `trials/ascension/l4/t_attainability.py` — already written and already green:
  the recorded arithmetic, the discrimination check, and the chronicle-family
  finding stated as the condition that lifts its own deferral.
- `trials/ops/l4/t_l4stream.py` — the corpus properties the discrimination rests
  on: bounded population, declared redundancy, the irreducible tier, and the
  contrast with the chronicle family.
- `trials/laws/t_rulings.py` — the gate registry, which already carries the four
  Layer-4 constants against their §5 L4 clauses and would gain this entry's ID
  beside them.
- `trials/ascension/l4/t_consolidation.py` and `trials/humility/l4/` — Stage B,
  which does not exist yet and is not written until this question is settled.

# RULING-R6-DRAFT.md — proposed entry `R6`

> **DRAFT. Not appended to `BOUNDARY-RULINGS.md`, deliberately.** Appending is
> what freezes an entry, and no session has the authority to freeze a ruling for
> itself. This document states a proposed holding for a human to accept, amend or
> refuse. **Nothing in it binds anything today**, and the Stage-B trials it would
> authorize are written and running as skips (`ascension/l5`), as green
> measurements against a *named* corpus (`humility/l5`), and as skips
> (`inheritance/l5`) — none of them claiming an authority this draft does not yet
> have.

---

# R6 — The Layer 5 ascension gate binds on `corpora/l5stream`; a firing's logical time

**Status:** DRAFT — frozen on commit **if** a human appends it.
**Binds:** the Layer-5 ascension trials (`trials/ascension/l5/`) and the Layer-5
humility trial (`trials/humility/l5/`); clause 2 binds **every layer from here
on**, including `BOUNDARY-HIGH.md` when it is written, and clause 3 binds the
ATTAINABILITY/ruling practice at every layer.
**Authority:** `BOUNDARY.md §1.1`, `§1.3`, `§1.4`, `§2.1`, `§2.2`, `§2.3`,
`§4.1`, `§5 L5`, `§5.1 L5`, `§7.1`, `§7.2`, `§7.3`, `§8`;
`BOUNDARY-RULINGS.md R1` and `R4` (the precedent for binding a stated threshold
to a corpus), `R2` (whose obligations this rests on), `R3` (whose scope this
does **not** extend), `R4` clauses 3 and 5, `R5` (whose four clauses govern how
R2's obligations are discharged here, and which expressly left the `t` question
to Stage B). Resolves question 4 of `trials/ascension/l5/ATTAINABILITY.md §6`,
the question `R5` recorded as open, and question 3 of the same section.
**Holding:** the ratified `§5 L5` thresholds stand **unchanged**; the Layer-5
ascension gate **and** the Layer-5 humility ceiling both bind on
`corpora/l5stream`; a **firing is an event and occupies a logical `t` of its
own**, so one caller `ingest` advances `next_t` by `1 + f`; where a prose figure
and a machine-checked one diverge, **the machine-checked one is the enforced
one** and the divergence is recorded rather than edited away; and
`budget_cap = raw_cells // 4` is the Layer-5 budget reading.

## The question

`§5 L5` states the Layer-5 ascension gate as

```
trigger-precision=1000, trigger-recall=1000, dup-fire=0, miss=0, F≥980, B=1000
```

with a humility ceiling of `capped trigger-recall ≤ 50`, and — exactly as `§5 L3`
and `§5 L4` did — names **no corpus**, no budget ratio, and no rule for what
happens to logical time when a trigger fires.

`R5` settled the two *methodological* questions Stage A put (how R2's obligations
are discharged for an identity clause and for a minimizing one) and deliberately
took neither of the two *substantive* ones: it does not bind the gate to a
corpus, and it does not settle the engine-`t` question. Stage B has now written
the ascension, humility and inheritance batteries, engine-free, which is the
point in R2's standing step at which both may be decided. This is that ruling.

## The ruling

### 1. The thresholds stand, and both sides of the Layer-5 gate bind on `corpora/l5stream`

**The ratified thresholds stand, unchanged.** `trigger-precision = 1000`,
`trigger-recall = 1000`, `dup-fire = 0`, `miss = 0`, `F ≥ 980`, `B = 1000` and
the humility ceiling `capped trigger-recall ≤ 50` are ratified text and are not
touched, softened, rescaled, or read as a fraction of anything.

**The Layer-5 ascension gate binds on `corpora/l5stream`** (seed `7007`,
`n = 20 000`, `raw_cells = 182 555`), and **so does the Layer-5 humility
ceiling.** The two are bound together in one clause because binding them apart
would discriminate nothing: a ceiling measured on one corpus beside a gate
cleared on another is two facts about two worlds.

**The upper side is EXHIBITED, per R5 clause 1** — the discharge that clause
makes available to an identity gate, and the stronger evidentiary burden it
imposes rather than the weaker one:

| policy | precision | recall | dup-fire | miss | F | clauses cleared |
|---|---|---|---|---|---|---|
| **exhibited witness** (fire each intention at its own satisfaction point, `iid` order), 41 951 of 45 638 cells = 230‰ | **1000** | **1000** | **0** | **0** | **1000** | 5 of 5 |
| **the ratified gate** | 1000 | 1000 | 0 | 0 | 980 | — |
| `make_engine(layer_cap = 4)` — no trigger machinery | *n/a* | 0 | **0** | 765 | 271 | 1 of 5 |
| fire-on-every-write | 0 | 0 | 9 183 176 | **0** | 0 | 1 of 5 |
| fire-immediately (condition unread) | 116 | 144 | **0** | **0** | 116 | 2 of 5 |
| fire-on-`kind`-atom-only | 375 | 379 | **0** | 77 | 397 | 1 of 5 |

**The lower side holds over the conjunction, per R5 clause 2**: no named
capability-free policy clears more than **two of the five** scored clauses, and
the strongest of them is 621‰ short on precision and 621‰ short on recall. The
two clauses baselines do tie — `dup-fire = 0` and `miss = 0` — are minimizing,
and a policy that fires once per intention gets the first for free while one that
fires everywhere gets the second. Neither is a capability. What is a capability is
holding both **at the same time as** precision and recall. `t_attainability.py`
asserts the conjunction bound at **three**, so a policy clearing four would reopen
this binding rather than pass unnoticed.

**The humility side is measured on an engine, not only on a policy — which is
what Stage B adds to the record.** Stage A scored `capped-4` as a *policy* that
never fires. Stage B runs `make_engine(layer_cap = 4)` — the frozen Layer-4
engine — over the whole 20 000-event stream through the generic interface (§7)
and measures **trigger-recall 0** against the ratified ceiling of 50, with
precision `n/a` (§3.4's convention for an empty class), dup-fire 0, miss 765,
`F` 271, `wrong = 0`, `fabricated = 0`, `B = 1000`. The ceiling is not breached,
is not vacuous, and is **loose for a structural reason**: firing is not a
behaviour that engine has, so the numerator is empty by construction.

**Why there is no alternative substrate, and why that is not a corpus search.**
R2 warns that its arithmetic *"does not authorize choosing a corpus because it
makes a gate reachable"*. That mischief cannot arise here. `§5 L5` states no
corpus precondition; an intention is an ingested payload under a declared grammar
reading (`ATTAINABILITY.md`'s Reading 1, forced by `§7.1` and `§1.1`); and **no
other frozen corpus contains an `intend` payload at all** — chronicle, sessions,
murk, l3stream, l3streamb and l4stream have no intentions, so on them the
`trigger-recall` denominator is 0 and every Layer-5 measure is undefined rather
than low. `l5stream` was frozen at Stage A, before any Layer-5 trial and before
any engine, on the append-only path `l3streamb` and `l4stream` took.

**There is consequently no diagnostic corpus family at Layer 5**, and this entry
does not invent one. R1 clause 5's conditional arithmetic-skip kept `l3stream`
and later `chronicle`/`murk` as *ungated diagnostics* because those corpora could
still be **scored** — their ceilings were low, not undefined. A corpus with no
intentions cannot be scored for prospection at any value; reporting `n/a` from
six corpora would be six ways of saying the same nothing. What replaces the
diagnostic here is `ops/l5/t_l5stream.py`'s declared corpus properties and the
four named policies, all of which run every suite.

### 2. A firing is an event and occupies a logical `t` of its own

**Ruled, and forward-binding at every layer that emits an event of its own:**

> **A trigger's firing is an event (`§5 L5`: `intend(condition → event)`). Under
> `§1.4` an in-engine event record is exactly `{payload, t}`, and under `§1.3`
> `t` is unique within a state and strictly increasing in ingestion order.
> Therefore a firing consumes a logical `t` of its own, assigned in the same pure
> transition as the caller write that satisfied it, immediately after that write
> and before any later caller write, consecutively and in `iid` ascending order
> where one write satisfies several pending intentions. `ingest` returns the
> **caller** event's `t`. One caller `ingest` therefore advances `next_t` by
> `1 + f`, where `f` is the number of firings that write caused.**

**`§7.1`'s "appends one event" is read as describing the caller's payload** — one
payload, one event, one returned `t` — and **not** as a cardinality limit on the
transition. That is the only reading under which `§5 L5` and `§7.1` are both
true: under the other, a fired event could never be appended at all, `§7.1`
declares only three operations, and prospection would be unreachable by any
lawful engine. It is the same argument, in the same place, that
`ATTAINABILITY.md`'s Reading 1 already made when it held that an intention cannot
be a fourth verb — and it is a **reading of ratified text, not an amendment of
it**.

**Layers 1–4 do not move, and not by exception.** The rule is *one caller event
plus the firings it caused*; on a stream with nothing pending, `f = 0`, and
*"one ingest, one `t`"* is that rule's `f = 0` case. No anchor's recorded
`next_t` changes, no frozen trial's `t = 0, 1, 2` changes, and the
`inheritance/` class replays unchanged — because **no corpus any of them replays
carries an intention**, which is asserted over the bytes of every corpus in the
registry
(`ascension/l5/t_prospection.py::trial_one_caller_ingest_advances_next_t_by_exactly_one_on_an_intention_free_stream`)
rather than assumed. A corpus frozen later that carried intentions turns that
trial red and forces the question to be answered again, in the open.

**Two things are expressly NOT decided by this clause**, and a later session may
not cite it as having decided them:

- **Cascades.** Whether an engine-emitted event is itself a "write" that pending
  conditions are tested against is not forced by any ratified text, and is
  **unobservable** on `corpora/l5stream` by construction: the GUARDEDNESS
  induction makes it impossible for any condition in the grammar to be satisfied
  by a `fired` payload, asserted as an induction and over the whole 945 × 945
  cross product. Both readings produce the identical schedule here. The `t` rule
  above holds under either.
- **What an engine owes when the budget cannot house a firing.** The gate fixes
  the invariants — `B = 1000` after every write, the `t` partition, exactly-once
  — and one consequence: a firing is not discretionary, since `miss = 0` means an
  intention whose condition is satisfied fires. Whether an engine makes room by
  the inherited Layer-3/Layer-4 eviction path or refuses the whole transition
  under `§4.1.2` is a Stage-C design question this entry leaves open.

The full derivation, the alternatives and the contradiction check against every
text that could object are `trials/ascension/l5/STAGE-B.md §1`, which this clause
ratifies rather than summarizes.

### 3. Where a prose figure and a machine-checked one diverge, the machine-checked one binds

**Forward-binding at every layer:**

> **Where a document states a quantity that a trial also computes, the trial's
> value is the enforced one. A prose figure that differs is NOT edited into
> agreement: the historical text stands as written, the divergence is recorded —
> in the ruling that freezes the entry where one exists, and otherwise by a dated
> erratum note above the text naming the machine-checked source of record — and
> the session that finds it says so in `BOUNDARY.log`. An unrecorded divergence
> is the failure; a recorded one is a document doing its job.**

`R5` performed exactly this once, as a boxed note, for the `capped-4` baseline's
`F`: `ATTAINABILITY.md §5` reads **270**, `t_attainability.py` pins **271**, and
R5 recorded which the trials enforce *"so the discrepancy is on the record rather
than in a diff nobody runs."* Two things since make the one-off worth
generalizing:

- **A third artifact now reports it.** `humility/l5/t_prospection.py` measures the
  capped **engine** — not a policy — through the generic interface and gets
  **271**: 945 P1 abstentions, 100 on each of the 765 answerable and 1000 on each
  of the 180 unanswerable, `256 500 / 945 000`. The figure is arithmetic and the
  seam is documentation. No holding turns on it under either number.
- **A second, larger instance was found this session.**
  `corpora/l5stream/grammar.md`'s closing block claims *"Every number below is a
  `DECLARED_*` constant in `generator.py` and is asserted by
  `trials/ops/l5/t_l5stream.py`"* — and **not one of them is**: it reads 956 / 775
  / 181 intentions, 26 multi-satisfaction indices at fan-out 6, 164 `count_ge`
  conditions and 181 043 raw cells against the frozen instance's 945 / 765 / 180,
  34 indices at fan-out 3, 169 conditions and 182 555 raw cells. The cause is on
  the record: Stage A's first corpus draft was not guarded, its ops trial went red,
  and *"the CORPUS was changed, not the trial"* (`BOUNDARY.log` line 28) — the
  prose was re-derived and that block was not. Handled under this clause: a dated
  erratum note above it, no historical line rewritten, no corpus byte touched, and
  `generator.py`'s `DECLARED_*` constants named as the record.

The clause is deliberately **not** a licence to edit. It settles which number is
in force and requires the other to remain visible, which is the same discipline
`R3` applied to `F_strict` and `R4` clause 4 to `F_corruption`: *a reading that
supersedes another should have to show the one it replaced.*

### 4. The Layer-5 budget reading: `budget_cap = raw_cells // 4`

`§5 L5` cites `B = 1000` and declares **no pressure ratio of its own**, unlike
`§5 L3` (*"stream = 10× budget"*) and `§5 L4` (`footprint ≤ 250`); `§5.1 L5` says
only that *"Pending intentions live within the hard budget like any other
state."* A budget must nonetheless be named before an oracle ceiling means
anything, because R2 obligation 1 derives the ceiling from *"the corpus, the
budget law, and nothing else"*.

**Ruled:** the Layer-4 footprint ratio carries forward —
`budget_cap = raw_cells // 4 = 45 638` on `corpora/l5stream` — and the events the
engine **emits** compete for cells inside that cap without enlarging it, which is
what `§5.1 L5`'s *"like any other state"* means here.

This ratifies the strictest defensible reading, which Stage A chose deliberately
and for a reason that survives ratification: a layer above consolidation should
not be handed a looser budget than consolidation, and a witness that fits at 250‰
fits at every looser reading *a fortiori*. A looser ruling would move the recorded
margin (3 687 cells, 8.1%) and nothing else. It is ruled rather than left open
because three batteries now replay at that number rather than merely computing
against it.

**No footprint gate is created.** `§5 L5` states none, and this clause states
none; what is ruled is the cap the budget law binds at, certified the way `§3.3`
and `§4.1.2` certify every cap — after every write.

## Rationale

**The repair belongs at the binding, not at the number** — R1's rule and R4's,
applied a third time. No `§5 L5` threshold moves in either direction. What is
decided is what the ratified numbers attach to, which is the one thing this
document's own preamble says a ruling is for.

**No engine's inability motivated this.** `core/layers/l5_prospection.py` does not
exist and `trials/adapters/l5.py` does not exist. Stage A stopped at the
attainability boundary, `R5` was decided against arithmetic, and Stage B has
written every battery — ascension, humility, inheritance — before any engine, so
that the corpus binding and the `t` semantics are fixed before anything can be
tuned to them. As in R1, R4 and R5: had an engine existed, this ruling should have
been harder to obtain.

**Clause 2 is the one clause here that could not have been written earlier, and
R5 said so.** Settling logical time in a ruling written before the trials existed
would have been exactly the ordering R2 forbids — the semantics would have been a
guess that the trials were then built to satisfy. Written in this order, the
decision is derived from six ratified sentences, checked against every frozen
trial that could contradict it, and *already asserted* by a Stage-A trial that
was written before anyone proposed a clause: `t_attainability.py::trial_one_caller_ingest_can_advance_next_t_by_more_than_one`
requires that the caller events and the firings **partition** `0 .. next_t − 1`
and that *"a firing is ingested where it fires"*. The ruling states what the
suite was already enforcing, which is the weakest possible way for a clause of
this reach to be introduced, and deliberately so.

**Clause 2 also refuses the two easy generalizations.** Cascades and
budget-refused firings are adjacent, tempting, and under-determined by the
ratified text — and one of them is unobservable on the binding corpus by
construction. Deciding an unobservable question would set a precedent no
measurement could ever have corrected. `grammar.md`'s own `No cancellation`
section made the same refusal at Stage A (*"R2's Stage-A discipline is to compute
against the ratified gate rather than to enrich it"*), and this is that discipline
at Stage B.

## What this ruling does not do

- It does **not** amend `BOUNDARY.md`. No ratified sentence is edited or reread.
  Clause 2 reads `§7.1`; it does not rewrite it, and the sentence it reads keeps
  its literal force for the caller's payload.
- It does **not** change any threshold, in either direction, on any layer. In
  particular it does not lower `trigger-precision`, `trigger-recall`, `dup-fire`,
  `miss`, `F` or the `≤ 50` ceiling.
- It does **not** weaken `R2`. Obligations 3 and 4 are untouched — the arithmetic
  is computed, recorded and machine-checked before the gate binds — and `R5`'s
  four clauses continue to govern *how* obligations 1 and 2 are discharged here.
- It does **not** create a Layer-5 footprint gate, extend `R3` to Layer 5, or
  request the corruption reading of `F`. The oracle reaches 1000, so the layer
  does not need the friendlier reading and declines to ask for it — R4 clause 4's
  discipline, third instance.
- It does **not** settle cascades, or what an engine owes when the budget cannot
  house a firing (clause 2's two express non-decisions).
- It does **not** authorize a `cancel`, `revoke`, `expire` or `re-arm`
  construct. `§5 L5` names none and the corpus invents none.
- It does **not** licence editing a frozen or historical document. Clause 3
  settles which number is enforced and requires the other to stay visible.
- It does **not** claim Layer 5, grant a Layer-5 capability, or license an engine.
  Stage C — `core/layers/l5_prospection.py`, `trials/adapters/l5.py`,
  `core/layers/README-l5.md`, the strain class, the anchor — is unwritten, and
  R2's standing step still orders it.

## Enforcement

- `trials/ascension/l5/ATTAINABILITY.md` and `t_attainability.py` — the Stage-A
  arithmetic clause 1 rests on: the exhibited witness, the four named baselines,
  the conjunction bound asserted at three, and the `t` layout asserted
  engine-free.
- `trials/ascension/l5/STAGE-B.md` — clause 2's derivation, its contradiction
  check, and clause 3's second instance.
- `trials/ascension/l5/t_prospection.py` — the gate applied to an engine
  (engine-gated), the `t` layout asserted of an engine, and the intention-free
  theorem over every corpus in the registry (engine-free).
- `trials/humility/l5/t_prospection.py` and `IMPOSSIBILITY.md` — the ceiling
  measured on `make_engine(4)` through the generic interface, and the structural
  argument for it.
- `trials/inheritance/l5/t_inheritance.py` — Layers 1–4 re-asked at cap 5, so the
  new capability cannot be bought with an old one.
- `trials/ops/l5/t_l5stream.py` — the corpus properties clause 1 rests on,
  including the GUARDEDNESS induction clause 2's first non-decision turns on.
- `trials/laws/t_rulings.py` — the gate registry, where the Layer-5 constants
  would carry this entry beside their `§5 L5` clauses, and the completeness check
  that forbids an unregistered gate constant anywhere under `trials/`.

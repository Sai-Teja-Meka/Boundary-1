# ATTAINABILITY.md — what the Layer-5 gate can and cannot reach on `corpora/l5stream`

> **RATIFIED IN PART — 2026-07-31, `BOUNDARY-RULINGS.md R5`.** This document was
> written at Stage A, before any ruling existed, and asked a human to decide four
> things (§6). **Two are now decided, and the decisions are frozen in `R5`, not
> here:**
>
> * **how R2 obligation 1 is discharged for an identity gate** (§5, question 1) —
>   by an **exhibited witness ATTAINING** it, a named policy priced against the
>   budget, scored, and asserted in the drift trial: **R5 clause 1**, which
>   expressly excludes `F ≥ 980` because it discharges the obligation by the
>   ordinary Layer-3/Layer-4 method;
> * **how R2 obligation 2 reads for a minimizing clause** (§5, question 2) —
>   direction-aware (*strictly better*) and over the gate's **conjunction**, with
>   every clause's arithmetic recorded either way: **R5 clause 2**.
>
> Two clauses of R5 bind this document's method forward rather than answering a
> question it asked: §3's declaration of the **policy class** a ceiling is exact
> over is made a standing obligation at every layer (**clause 3**), and §4's
> pricing of **operational bookkeeping** and a **loss-accounting reserve** is
> made one too (**clause 4**) — both alongside R2 and R4 clause 5.
>
> **Two questions are NOT decided and stay open.** The budget reading of §1
> (`budget_cap = raw_cells // 4`) is not ruled on: R5 records this document's
> arithmetic under it as evidence, and — as §1 says of itself — a looser reading
> would move only the recorded margin. **The corpus binding (question 4) is not
> taken**, so no Layer-5 gate binds on `corpora/l5stream` or on anything else,
> and the constants in `trials/laws/t_rulings.py` carry R5 for a *reading* and
> not for a substrate.
>
> The text below is **unedited** and stands as the Stage-A record — including its
> forward-looking sentences (*"no gate binds"*, *"a human's to settle"*), which
> were true when written and are answered by R5 rather than rewritten. No
> threshold it tests against moved, and no number it records was corrected: R5
> **regularizes** the practice §5 found unexamined and declares nothing earlier
> false. One figure is stated exactly in R5 because that entry freezes it — §5's
> table records the `capped-4` baseline's `F` as **270** and
> `t_attainability.py`, which is what a drift turns red, pins it at **271**; the
> difference is one permille of a policy that clears one clause of five either
> way, and this document is left as written.

**BOUNDARY-RULINGS.md R2** put attainability before authority: *"a gate must lie
strictly below the oracle ceiling and strictly above every capability-free
baseline on its binding corpus, and that arithmetic must be computed and recorded
in an `ATTAINABILITY.md` BEFORE the gate binds."* This is that document for
Layer 5, written **before a line of `core/layers/l5_prospection.py` exists** and
before any Layer-5 trial applies a gate to any engine.

Everything numeric here is computed by `trials/_l5tasks.py` from the frozen corpus
and the frozen §4.1 cost model alone, and asserted by
`trials/ascension/l5/t_attainability.py`, so no number below can drift silently.

---

## §0. The verdict, first

Three findings, in the order of how much they bind.

**1. The gate is attainable, and the ceiling is EXHIBITED.** A concrete witness —
a firing schedule over `corpora/l5stream` and the state that produces it, priced
under rule P and fitting inside the budget with 3 687 cells to spare — attains

```
trigger-precision 1000    trigger-recall 1000    dup-fire 0    miss 0    F 1000
```

which is the ratified `§5 L5` gate **exactly**, `F` excepted (gate 980, oracle
1000).

**2. R2 obligation 1 cannot be discharged at Layer 5 by the method that
discharged it at Layers 3 and 4.** Four of the six gate clauses are **identities
over discrete correctness**, so the oracle ceiling *is* the gate: `1000 < 1000` is
false, and `dup-fire < 0` is not a thing that exists. The obligation's own words
demand a **strict** inequality on both sides. What this session can offer instead
is the exhibited attainment above — the gate is not void, because a policy
reaching it exists and is named — and whether that discharges R2 is **a human's
to settle**. `RULING-R5-DRAFT.md` states the proposed holding.

**3. R2 obligation 2, read clause by clause, is also undischargeable here — and
it survives read over the conjunction.** `dup-fire = 0` is tied by three of the
four named baselines, and `miss = 0` is tied by two of them, because both are
**minimizing** clauses and R2's *"strictly above"* is written for measures where
higher is better. No capability-free policy comes near the gate as a whole:
the best of them reaches `precision 375 / recall 379 / F 397` against
`1000 / 1000 / 980`. The conjunction discriminates by a wide margin; no single
clause does.

**This session claims nothing and binds nothing.** Per the ASCEND directive's own
instruction, Stage A is delivered as its own committed session — corpus,
`ATTAINABILITY.md`, ruling draft — and stops. `trials/ascension/l5/t_attainability.py`
applies no gate to any engine, `trials/humility/l5/` does not exist, and
`core/layers/l5_prospection.py` does not exist.

---

## §1. What `§5 L5` asks, and the two readings this document declares

`BOUNDARY.md §5 L5` gates on

```
trigger-precision=1000, trigger-recall=1000, dup-fire=0, miss=0, F≥980, B=1000
```

and `§5.1 L5` defends the first four in one sentence: *"Every intention whose
condition a future write satisfies must fire, and nothing may fire spuriously —
**prospection is exact or it is broken**."*

### Reading 1 — an intention is an EVENT, not a fourth verb

`§7.1` declares **three** operations and `§1.1` says events are the only fuel:
*"Configuration, queries, and side-band signals are not fuel."* `intend(condition
→ event)` therefore cannot be a fourth entry point into the engine. It arrives as
an **ingested payload** whose reading is declared by
`corpora/l5stream/grammar.md`, exactly as `_l4tasks.facet` is a declared reading
of the chronicle-family grammars and `HANDLE_FIELDS` is at Layer 3. The engine's
`intend` *capability* is what it does with such a payload.

This is a reading of ratified text, not an amendment of it, and it is the only
reading under which `§5 L5` and `§7.1` are both true.

### Reading 2 — the budget `B = 1000` is certified at the Layer-4 footprint ratio

`§5 L5` cites `B = 1000` and declares **no pressure ratio of its own** — unlike
`§5 L3` (*"stream = 10× budget"*) and `§5 L4` (`footprint ≤ 250`). `§5.1 L5` says
only: *"Pending intentions live within the hard budget like any other state."* A
budget must nonetheless be named before an oracle ceiling means anything, because
R2 obligation 1 derives the ceiling from *"the corpus, the budget law, and nothing
else"*.

This document declares:

```
raw_cells   = Σ_t event_cost(payload_t)  over the frozen caller stream = 182 555
budget_cap  = raw_cells // 4 = 45 638            (the Layer-4 footprint ratio)
```

**The strictest defensible reading, chosen deliberately.** A layer above
consolidation should not be handed a looser budget than consolidation, and a
witness that fits at 250‰ fits at every looser reading *a fortiori* — so the
finding is robust to a human ruling the other way, and the only thing at risk is
the size of the recorded margin. Note that `raw_cells` counts the **caller**
stream only: the events the engine emits when triggers fire are engine-derived and
compete for cells inside the same cap without enlarging it, which is what
`§5.1 L5`'s *"like any other state"* means here.

### Pricing rule P applies unchanged

R4 clause 3 ruled rule P — one cell, one grammar atom — **general and not
Layer-4-only**. Every cell counted below is one atom: a condition AST is priced at
`payload_cost` over its own JSON, an `iid` at one cell, a logical `t` at one cell.
A row's *shape* (its kind tag and field names) is paid **once per distinct shape**,
which is the Layer-4 row codec; the `[L4] [ASCEND]` session's 124-cell shape-header
under-report is why that is stated here rather than assumed.

---

## §2. The battery: what Layer 5 is asked, and what the four quantities are

An **intention** is a caller-written `intend` payload carrying an `iid`, a
condition AST over the closed predicate vocabulary, and the payload to fire. Its
**satisfaction point** is

```
sigma(i) = min { k : k > k0(i) and payload_k satisfies cond_i }     or  none
```

over **caller indices** `k` — the 0-based line number of the frozen stream, never
the engine's logical `t`. The corpus makes this a property of the frozen bytes:
`fired` is outside the predicate vocabulary's kind set and a fired payload carries
no field any payload atom reads, and every condition is **guarded**, so no firing
can ever satisfy another condition (`corpora/l5stream/grammar.md`, GUARDEDNESS;
asserted twice in `trials/ops/l5/t_l5stream.py`, once as the induction and once
over the whole 945 × 945 cross product).

### The four exactness quantities

A **firing record** is a pair `(iid, k)`. A policy produces a multiset of them.

```
correct fires     = { (i,k) : k == sigma(i) and i fires exactly once }
trigger-precision = permille( |correct fires| / |all fires| )     n/a if no fires
trigger-recall    = permille( |correct fires| / |{ i : sigma(i) != none }| )
dup-fire          = |all fires| − |distinct intentions fired|     an integer count
miss              = |{ i : sigma(i) != none and i never fires }|  an integer count
```

**`trigger-precision` is undefined when a policy never fires, and is reported
`n/a`, not 1000.** This is the convention `§3.4` already establishes for `AUROC`
when a class is empty (*"It is undefined when `n_pos = 0` or `n_neg = 0` (report
`n/a`)"*), and it matters: an empty denominator scored as perfect would hand a
`precision = 1000` clause to the policy that does nothing, which is precisely the
`capped-4` baseline this battery exists to defeat.

### The `F` battery — one threshold among four identities

`§5.1 L5` defends `F ≥ 980` as *"a fired event's payload must match the intended
event essentially exactly."* Asked of a black box through `§7`'s three operations,
that is two query classes:

| | one query per | answerable when | answer |
|---|---|---|---|
| **P1** | intention (945) | `sigma(i) != none` | the `t` of the fired event, and its payload |
| | | `sigma(i) == none` | **unanswerable** — the only correct behaviour is to abstain |
| **P2** | fired event (765) | always | `read(t_fire)` returns the intended payload, byte-exact (§2.4) |

`N = 1 710` queries. P2 is deliberately the **Layer-1 `read` verb**: it asks the
engine to hand back the event it emitted at the `t` it assigned, which is what
makes "the payload matched" a measurement rather than a definition.

`F` binds under the **literal §3.0 table**. R3 excludes Layer 5 in its own text
(*"Layers 1, 2, 4, 5, 6 and 7 score F under the literal §3.0 table unless and
until a later ruling says otherwise"*), and **no extension is requested**: §4 shows
the oracle reaches 1000, so the layer does not need the friendlier reading and
declines to ask for it — the same refusal R4 clause 4 recorded for Layer 4, made
for the same reason.

The honest form of the gate, on this battery: `F ≥ 980` admits **at most 35 wrong
answers**, or **at most 38 abstentions on answerable queries**, out of 1 710 —
§3.5's round-half-to-even admitting an exact `F` as low as 979.5‰. A never-fires
intention correctly abstained on scores **1000**, not 100, because its query is
unanswerable; the 180 of them are credit for honesty, not a tax.

---

## §3. The policy class, and why the Form-B pass-through cannot recur here

R4 clause 5 made an exhibited ceiling preferred practice, and the `[L4] [ASCEND]`
session recorded the reason a ceiling needs its class stated at all: the Layer-4
engine, run at Layer 3's own cap on Layer 3's own corpus through Layer 3's own
scorer, reached **weighted-C 924 — straight through Layer 3's 918‰ oracle
ceiling** — because that ceiling was exact over *retain-or-drop* policies, the
family Layer 3 could choose from, and a consolidating engine is not in it. An
argued ceiling is only as good as its declared family.

**This document therefore declares two classes, because it makes two different
kinds of claim.**

**(a) The identity ceiling is class-independent.** `trigger-precision ≤ 1000`,
`trigger-recall ≤ 1000`, `dup-fire ≥ 0` and `miss ≥ 0` are **logical maxima over
every policy whatsoever** — not maximizations over a declared family. Precision is
a ratio of a subset to its superset; recall likewise; `dup-fire` and `miss` are
cardinalities of sets. No future capability, at Layer 6 or Layer 9 or in
`BOUNDARY-HIGH.md`, can pass through them, because there is nothing on the other
side to pass through to. The Layer-3 pass-through **cannot** recur on these four
numbers, and that is a property of the measures, not a promise about engines.

**(b) The budget claim is class-dependent, and its class is declared.** §4's
witness costs 41 951 of 45 638 cells. That is a **price for one design**, not a
minimum over all designs. The class it is exact over is:

> states that answer the P1/P2 battery of §2 and maintain the Layer-4 assertion
> facet of `corpora/l5stream` exactly, under rule P, with the fired events' own
> storage counted inside the cap.

A state outside that class may be cheaper — §4's `W1` is, by a factor of nine —
and a state that must *also* clear the ratified Layer-4 gate on this corpus is not
priced here at all, because `R4 clause 1` binds that gate to `corpora/l4stream`
and `l5stream` is not it. **The margin recorded in §4 is a margin for that class
and no other**, and a Stage-C engine that leaves it inherits the number, not the
reassurance.

---

## §4. The witness — exhibited, not argued

### The schedule

Fire each intention exactly at its own satisfaction point; where several are
satisfied by one arriving write, fire them in `iid` ascending order. That is the
whole policy. Its firing trace, first six firings of 765:

| `iid` | written at `k0` | `sigma` | engine `t` of the firing | condition |
|---|---|---|---|---|
| 1 | 202 | 219 | 220 | `and(kind=attr, val_ge 900)` |
| 3 | 258 | 262 | 264 | `and(kind=attr, val_ge 500)` |
| 4 | 265 | 288 | 291 | `kind = intend` |
| 6 | 302 | 303 | 307 | `and(kind=attr, not(val_ge 500))` |
| 7 | 339 | 340 | 345 | `kind = attr` |
| 9 | 381 | 383 | 389 | `kind = attr` |

**The drift in the last two columns is the finding the `[L4] [PULSE]` session
ranked second and named for this one.** A fired event is an event and `§1.3` gives
it a `t` of its own, so **one caller `ingest` can advance `next_t` by more than
one**: caller index 219 is engine `t` 219 and its firing is `t` 220; by caller
index 383 the offset is 5; over the whole stream 20 000 caller writes produce
20 765 logical times, the last firing landing at `t = 20 760`. Every anchor and
the whole `inheritance/` class assume one ingest advances `t` by one, and on a
stream carrying intentions that identity stops holding. It is a Stage-B and
Stage-C obligation, recorded here because Stage A is where it becomes a number.

### The score

| | value | gate |
|---|---|---|
| trigger-precision | **1000** (765 of 765 firings correct) | = 1000 |
| trigger-recall | **1000** (765 of 765 fireable) | = 1000 |
| dup-fire | **0** | = 0 |
| miss | **0** | = 0 |
| `F`, literal §3.0 (1 710 of 1 710 exact) | **1000** | ≥ 980 |
| footprint | **230‰** (41 951 of 45 638 cells) | (B = 1000 ⟺ occupancy ≤ cap) |

### The price — W1, the prospection-only state

The cheapest state that attains the identity carries **nothing but** the pending
set, the per-kind counters `count_ge` folds over, and one row per fired event so
that P1 and P2 are answerable:

```
peak pending set (184 entries at their own AST cost)        2 191 cells
fired-event rows (765 × [iid, t, text_id])                  2 295
per-kind counters (2 × 6 kinds)                                12
row-shape headers (pending 4, fired 3), paid once               7
                                                            -----
W1                                                          4 505 cells  = 25‰
```

W1 is exhibited for one reason, and it is not flattery: **it is what `§5 L5`'s
gate, read literally, asks for.** A state that has forgotten the entire world and
kept only its intentions scores `1000 / 1000 / 0 / 0` and 1000 on `F`. That is a
true fact about the ratified gate and it is recorded rather than smoothed over.
It is also why §3(b) declares a class, and why the honest witness is W2.

### The price — W2, the witness that does not repeal the layer below

```
Layer-4 assertion facet of l5stream (interval table + counters)   36 790 cells
operational bookkeeping                                              633
    per-entity irreducible counts   600   (3 × 200 entities)
    key atlas                        32   (2 × 16 keys)
    demotion counter                  1
prospection state (peak pending 2 191 + fired rows 2 295 + shapes 7) 4 493
loss-accounting reserve (3 + 2 × 16 buckets)                          35
                                                                  ------
W2                                                                41 951 cells
budget_cap                                                        45 638
margin                                                             3 687  (8.1%)
footprint                                                            230‰
```

**Both L4 lessons are priced, not disclaimed.**

- **Operational bookkeeping.** `[L4] [ASCEND]` (BOUNDARY.log line 23) found 656
  cells of it *after* Stage A had declared a 2 563-cell margin — per-entity
  irreducible counts, the key atlas, the forgetting record, the demotion counter.
  The same four items are carried here **by name and by construction**, priced
  from this corpus's own shape (200 entities, 16 keys) rather than copied.
- **The loss-accounting reserve.** `[L4] [STRAIN]` (line 26) turned GAPMAP §2's
  *"recorded but never binding"* thesis on this project's own engine: a
  non-invertible fold was booked as a lossless demotion while `read(t)` abstained
  on it forever. The 35-cell aggregated forgetting record is reserved here
  **because W2 genuinely loses things** — 2 228 `note` episodes and every fired
  intention's episode are released, and a release that is not regenerable is a
  loss that must be booked. It is a reserve with a reachable path, not a ritual.

**One honesty note on the prospection line.** 4 493 is the **peak** pending set
plus the **final** fired-row count: two maxima that do not occur at the same caller
index, so it is an upper bound rather than a measurement. The true joint
high-water mark is **4 448 cells**, 45 lower. The bound is what a budget must
respect; the gap is how much of it is slack, and both are recorded so neither can
be quoted as the other.

---

## §5. The discrimination check (R2, both obligations)

| policy | precision | recall | dup-fire | miss | F |
|---|---|---|---|---|---|
| **oracle ceiling** (exhibited, §4) | **1000** | **1000** | **0** | **0** | **1000** |
| **the ratified gate** | **1000** | **1000** | **0** | **0** | **980** |
| (i) `make_engine(layer_cap = 4)` — no trigger machinery | *n/a* | **0** | 0 | 765 | 270 |
| (ii) fire-on-every-write | 0 | 0 | **9 183 176** | 0 | 0 |
| (iii) fire-immediately (condition unread) | 116 | 144 | 0 | 0 | 116 |
| (iv) fire-on-`kind`-atom-only | 375 | 379 | 0 | 77 | 397 |

Each baseline earns its place.

- **(i) capped-4** is the humility seam, and `README-l4 §4` predicted its value
  exactly: *"a deferred-intent task scores 0 here, not near 0 … with no intention
  store, nothing is ever pending, so nothing can fire — the capped engine's
  numerator is empty by construction, not by difficulty."* Measured: recall **0**
  against a `§5 L5` ceiling of **50**. The ceiling is not breached and is not
  vacuous in the way that matters — it is *loose*, and the reason is structural
  rather than a corpus's kindness. Its `F` of 270 is `§3.0` working as designed:
  it abstains on all 945 P1 queries, which is **wrong** on the 765 answerable ones
  (100 each) and **exactly right** on the 180 unanswerable ones (1000 each).
- **(ii) fire-on-every-write** is the cheap trick the ASCEND directive named, and
  it behaves exactly as predicted — *under the charitable reading*. Dropping the
  exactly-once requirement and asking only whether *some* firing landed on the
  satisfaction point, it scores **recall 1000** (it cannot miss: it fires
  everywhere) at **precision 0** (765 landings among 9 184 121 firings — 0.08‰,
  which rounds to 0 in permille). **The identity kills it, and here is exactly
  how:** under the ratified exactly-once reading not one of its firings is
  correct, so precision and recall are both 0, and `dup-fire` is **9 183 176**
  against a gate of **0**. Computed analytically — an intention written at `k0`
  fires `n − 1 − k0` times — with a brute-force construction over a declared
  prefix asserted against the arithmetic, one policy and two implementations.
- **(iii) fire-immediately** is the honest zero-knowledge guess: fire at the very
  next write, condition unread. Its score is a property of the corpus rather than
  of a trick — it is right exactly for the 110 intentions whose satisfaction point
  happens to be `k0 + 1`. That the corpus yields it only 144‰ is the reason
  `corpora/l5stream/grammar.md` declares the latency profile: 110 fire at the next
  write, 270 within ten, 188 within a hundred, 197 beyond a hundred, 180 never. A
  corpus where most intentions fired immediately would have handed the gate to
  this policy.
- **(iv) fire-on-`kind`-atom-only** is the strongest cheap trick available: it
  reads the condition grammar for real, just not all of it — every `kind` atom is
  evaluated and every other predicate is treated as true. At **375 / 379** it is
  the closest any capability-free or partial-capability policy comes, and it is
  still 621‰ short on precision and 621‰ short on recall.

### Obligation 1 — below the oracle: **NOT DISCHARGEABLE by the L3/L4 method**

| clause | gate | oracle ceiling | strictly below? |
|---|---|---|---|
| trigger-precision | 1000 | 1000 | **no — equal** |
| trigger-recall | 1000 | 1000 | **no — equal** |
| dup-fire | 0 | 0 | **no — equal, and the direction is inverted** |
| miss | 0 | 0 | **no — equal, and the direction is inverted** |
| `F` | 980 | 1000 | **yes** ✔ |
| `B` | 1000 | 1000 | **no — equal** |

Five of six fail a strict reading. This is not a defect of the corpus and no other
corpus repairs it: for a gate stated as an identity over discrete correctness, the
oracle ceiling **is** the identity, on every corpus, by arithmetic. R2's own
rationale states the mischief it is guarding against — *"A gate at or above the
oracle ceiling is **void**: it forbids what it purports to test"* — and that
mischief is **absent here**, because §4 exhibits a policy that reaches it.

`F ≥ 980` is the one clause that discharges normally, and it is worth noticing
that it does: one §5 clause contains both kinds of sub-gate at once, so no ruling
can dispose of Layer 5 by treating the whole clause as exceptional.

**And the precedent is older than Layer 5.** `B = 1000` has been an identity gate
at **every layer since Layer 1** — `§3.3` makes any value below 1000 *"a breach of
the budget law and … disqualifying"*, so its ceiling is exactly 1000 — and neither
`trials/ascension/l3/ATTAINABILITY.md` nor
`trials/ascension/l4/ATTAINABILITY.md` scored it against an oracle in their
discrimination checks. Layer 4's `footprint ≤ 250` is likewise a **minimizing**
clause, and R4's discrimination table scores its baselines on `C` and `F` only.
The identity problem did not arrive at Layer 5; Layer 5 is where it stops being
possible to leave unexamined, because four of the layer's own characteristic
measures are identities rather than one incidental budget law.

### Obligation 2 — above every capability-free baseline: **holds over the conjunction**

| clause | gate | best baseline | strictly better? |
|---|---|---|---|
| trigger-precision | 1000 | 375 (iv) | **yes** ✔ |
| trigger-recall | 1000 | 379 (iv) | **yes** ✔ |
| `F` | 980 | 397 (iv) | **yes** ✔ |
| dup-fire | 0 | 0 (i), (iii), (iv) | **no — tied** |
| miss | 0 | 0 (ii), (iii) | **no — tied** |

`dup-fire` and `miss` are minimizing clauses and R2's *"strictly above"* is
written for measures where higher is better; read literally it would require a
baseline with a negative count, which does not exist. Read over the **gate as a
whole** — the conjunction of its six clauses, which is how `§5` states it and how
any trial would apply it — obligation 2 is discharged with an enormous margin:
**no named baseline clears more than three of the six clauses**, and the two it
does clear it clears by doing nothing (firing never, or firing once each
regardless of condition). A policy that fires exactly once per intention gets
`dup-fire = 0` for free; what it cannot get for free is `dup-fire = 0` **and**
`precision = 1000` **and** `recall = 1000` at once.

### The humility ceiling

`§5 L5` allows the capped engine `trigger-recall ≤ 50`. Measured: **0**. Not
breached, and structurally so — `README-l4 §4` states the reason in advance and
`humility/l5/IMPOSSIBILITY.md` is to be written against it: *"not 'the schemas are
too lossy to notice the trigger' but 'there is nothing to notice with'."*

---

## §6. What is *not* being done here, and what a human is asked to decide

**No gate binds.** R2 obligation 4 is explicit: *"A gate that has not had this
arithmetic computed has no authority yet."* The arithmetic is now computed and on
the record, which is necessary and not sufficient. `t_attainability.py` applies no
gate to any engine, `trials/humility/l5/` does not exist, and no Layer-5 engine
exists.

**No frozen artifact was edited.** `BOUNDARY.md`, `BOUNDARY-RULINGS.md`, every
frozen corpus, every frozen layer, every frozen trial and every anchor are exactly
as they were. What this session adds is: one new corpus, one engine-free task
module, one ops trial, one attainability trial, this document, and a ruling draft.
`trials/laws/t_rulings.py`'s gate registry receives the Layer-5 constants — the
additive extension that file exists to hold, and the mechanism by which a new gate
constant cannot exist without a recorded authority.

**What a human is being asked to decide**, in order of how much it binds:

1. **How R2 obligation 1 is discharged for an identity gate** (§5). The proposal:
   by an **exhibited witness attaining** the identity, since the mischief R2 names
   — a gate that forbids what it purports to test — is exactly what an attaining
   witness rules out. The counter-argument is in R2's own rationale and is recorded
   here rather than answered away: *"A gate equal to its oracle ceiling demands
   perfection from an engine that must also be honest under §3.0."* `§5.1 L5`
   answers it in the constitution's own words — *"prospection is exact or it is
   broken"* — and the §3.0 tension does not arise for these four clauses, which
   count firings rather than score answers, and where abstention is not one of the
   available behaviours. It does arise for `F`, which is why `F` was ratified at
   980 and not at 1000.
2. **How R2 obligation 2 reads for a minimizing clause** (§5). The proposal:
   direction-aware (*strictly better*, not *strictly above*), and discharged over
   the **conjunction** of a gate's clauses rather than clause by clause — with the
   arithmetic for every clause recorded either way, as it is above.
3. **The budget reading** (§1). `budget_cap = raw_cells // 4`, the Layer-4
   footprint ratio carried forward, `§5 L5` declaring no ratio of its own. Chosen
   as the strictest defensible reading; a looser ruling changes only the recorded
   margin, never the verdict.
4. **The corpus binding** (§4, §5) — the Layer-5 ascension gate on
   `corpora/l5stream`, in the shape R1 and R4 established.

`RULING-R5-DRAFT.md` states the proposed holding on (1), (2) and one methodology
clause. It is a **draft** and is deliberately **not** appended to
`BOUNDARY-RULINGS.md`, because appending is what freezes an entry and this session
has no authority to freeze a ruling for itself.

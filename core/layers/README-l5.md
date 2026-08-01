# Layer 5 — Prospection (`intend(condition → event)`, fired exactly once)

`[L5] [ASCEND]`. The fifth capability of Boundary-1: Memory. Layer 1 **retained**
and refused; Layer 2 **recalled** by content; Layer 3 **dropped**, and what it
dropped left no trace; Layer 4 **derived**, so an episode could be released
because its content already lived somewhere else. Every one of those is a fold
over the past: the write path consults the arriving payload and the current state
and nothing else. Layer 5 **watches** — a condition is written now, held, and
evaluated against every event that arrives afterwards, and when one satisfies it
the engine **emits an event of its own**: once, at a logical time of its own, and
never again.

This document states **exactly what Layer 5 can and cannot express**. Layer 6's
humility trial is written against the boundary drawn in §5.

Intellectual pedigree: the prospective-memory literature by way of
`autopsy/GAPMAP.md §6`, where **absent-mindedness** — the intention formed and
then not acted on — is the Schacter sin this layer is heir to. It is also the
capability **every one of the seven autopsies found absent**: `generative-agents`,
`mem0`, `graphiti`, `letta`, `memoryagentbench`, `locomo` and `writ` have no
`intend`, no condition and no trigger between them (`autopsy/GAPMAP.md §1`), and
WRIT's *"Remind me"* prompts are retrospective. There is no prior art to steal
from here; what is inherited is Layer 4's discipline, not another system's design.

Code (frozen after this session, §9):
- `core/layers/l5_prospection.py` — the `L5State` (a **subclass** of the frozen
  `L4State`, plus the pending set and the fired ledger), the declared intention
  facet and its inverse, the closed condition vocabulary with its validator and
  its evaluator, arming, firing, and the checksummed snapshot/restore.
- `trials/adapters/l5.py` — the Layer-5 adapter. `core/engine.py`,
  `l1_retention.py`, `l2_recall.py`, `l3_forgetting.py` and `l4_consolidation.py`
  are **untouched**; `anchors/l1.json` … `l4.json` replay through their own
  adapters unchanged.

---

## §0. The budget decided the state, before the code (BOUNDARY-RULINGS.md R2)

Stage A did for the *gate* what `README-l4 §0` did for the Layer-4 engine.
`trials/ascension/l5/ATTAINABILITY.md §4` **exhibited** the witness the gate rests
on — `W2`, a Layer-4 state that also attains the Layer-5 identity, at **41 951 of
45 638 cells** — and recorded the consequence for this session in one number:

> *"`W2` 41 951 / `budget_cap` 45 638 / **margin 3 687 (8.1%)**. … The margin
> recorded in §4 is a margin for that class and no other, and a Stage-C engine
> that leaves it inherits the number, not the reassurance."*

Everything below is that number spending itself. The arithmetic is asserted in
`trials/ops/l5/t_l5_composition.py`, not trusted — and under `R6` clause 3, where
this document states a figure that file also computes, **that file is the enforced
value**.

### 0.1 The state is Layer 4's, plus two tiers that cannot be evicted

`L5State` is a **subclass** of the frozen `L4State`. That is not a convenience: it
is what makes Layer 4 an *inheritance* rather than a re-implementation. Every
Layer-4 cost function, verb and eviction phase operates on this state unchanged,
`replace()` returns an `L5State`, and the single `occupancy` counter covers the
two new tiers — so the Layer-4 write path evicts **around** prospection without
knowing it is there.

| tier | shape | cells |
|---|---|---|
| pending set | `{shape: {iid: (t0, cond) + fire values}}` | `1 + width` per shape, `2 + cond + width` per entry |
| fired ledger | `{shape: {iid: (t,) + fire values}}` | `1 + width` per shape, `2 + width` per entry |

Both are grouped by the fire payload's **row shape** — the Layer-4 row codec
(`README-l4 §0.2`), so the grammar is paid for once per shape per tier and each
entry carries only its own values. The prices come out **identical to Stage A's**:
a pending entry at `iid + t0 + cond + fire` and a fired row at `iid + t + fire`,
asserted against `_l5tasks`' independent pricing of the same content.

> **Neither tier is evictable, and that is the layer rather than a convenience.**
> `miss = 0` means an intention whose condition is satisfied fires, so a pending
> entry an engine dropped would be an intention it silently forgot. `dup-fire = 0`
> means a fired intention never fires again, so a fired entry an engine dropped
> would be an intention it could fire twice. An eviction path that could reach
> either would be an engine that can be made to **break a ratified gate by being
> poor**. What gives way under pressure is the episodic tier, exactly as at Layer
> 4, and every loss is booked. `R6` clause 2 expressly left *"what an engine owes
> when the budget cannot house a firing"* to Stage C; this is the answer, and
> `ops/l5/t_l5_composition.py::trial_the_prospection_tiers_are_outside_every_eviction_phase`
> is where it is a measurement rather than a paragraph.

### 0.2 A firing pays for itself

The swap a firing makes — one pending entry out, one fired entry in — **frees**
exactly the condition's cells, because the two entries are otherwise the same
shape. On `corpora/l5stream` a condition costs 4 to 14 cells, so the 765 firings
are collectively cell-negative and the only thing a firing can cost is the fired
tier's one shape header and a coarsening step of the forgetting record. That is
why the ratified `refused = 0` is comfortable rather than lucky: the transition
that *has* to succeed is the cheap one.

### 0.3 The composition, and where the 3 687 went

Measured on `corpora/l5stream` at the ratified cap of 45 638 cells (`R6` clause 4):

| component | cells |
|---|---|
| interval table (16 keys, 2 924 pairs, 16 827 assertions) | 36 594 |
| key atlas (16 keys) | 32 |
| global per-kind counters (7 kinds — `fired` is the seventh) | 14 |
| per-entity irreducible counts (200 entities × `note`) | 600 |
| demotion counter | 1 |
| aggregated forgetting record (width 2 048, 11 buckets) | 25 |
| **bookkeeping** | **672** |
| pending set — 180 never-fires intentions + one shape header | 2 141 |
| fired ledger — 765 firings + one shape header | 2 297 |
| **prospection** | **4 438** |
| derived rows — 952 surviving `note` episodes at 3 cells + shape | 2 859 |
| handle index (113 atoms + 952 postings) | 1 065 |
| **the episodic tier the remainder bought** | **3 924** |
| **total** | **45 628 ≤ 45 638** |

The margin reconciles item by item, and the items are the ones R5 clause 4 was
written about:

| | cells |
|---|---|
| Stage A's recorded margin | 3 687 |
| key-major nesting, against Stage A's entity-major substrate | **+184** |
| prospection below its own bound (4 493 bound, 4 438 final) | **+55** |
| loss reserve unused (35 reserved, 25 the record reached) | **+10** |
| the `fired` counter — a seventh grammar kind `W2` counted six of | **−2** |
| **working room** | **3 934** |
| spent on the episodic tier (2 859 rows + 1 065 index) | −3 924 |
| **left** | **10** |

That is where the 3 687 ran out, and — as at Layer 4, where the same accounting
left five cells — the answer is undramatic and worth recording as such: **the
layer's real cost is still the interval table**, prospection is a tenth of the
budget, and everything else is the change from it.

Stage A's two disciplines held on contact. The **operational bookkeeping** it
carried by name (600 + 32 + 1) was exactly right; the **loss reserve** it took
because *"`W2` genuinely loses things"* was needed and was not fully spent. The
one item Stage A did not price is two cells wide.

---

## §1. The derivation law, one layer up (structural, exact, invertible)

### 1.1 An intention is an event, and reading one is a declared reading

`ATTAINABILITY.md`'s Reading 1 — forced by `§7.1`'s three operations and `§1.1`'s
*"events are the only fuel"* — is that `intend` cannot be a fourth verb. It
arrives as an ingested payload, and the engine reads it through

```
INTENTION_FORM = ("iid", "cond", "fire")     # {"kind":"intend", …}
```

a **declared reading of the frozen grammar**, exactly as `ASSERTION_FORMS` is at
Layer 4 and `HANDLE_FIELDS` at Layer 3. `ops/l5/t_l5_composition.py` asserts that
this reading and the battery's own agree on **every event of the frozen stream** —
one reading, two implementations, checked rather than assumed, because unlike a
coverage miss a divergence here moves a *firing*.

### 1.2 Three rules decide whether a payload arms anything

An `intend` payload becomes a pending intention only when all three hold.
Otherwise it is an **ordinary event** and takes the frozen Layer-4 write path,
where it is irreducible and competes for room under the inherited Layer-3
importance law. The engine never raises and never half-arms.

* **The condition is readable.** Six predicates, three connectives, and nothing
  else (`readable`). `trials/_l5tasks.satisfies` *raises* on an unknown predicate,
  deliberately — for the battery an unreadable condition is a corpus defect and a
  silent `False` would turn it into a never-fires intention nobody noticed. An
  engine has the opposite obligation, so it takes the other honest branch:
  **arm only what you can evaluate.** The forbidden third option is storing a
  condition the engine cannot evaluate and calling the result a pending intention.
* **The payload inverts.** The engine rebuilds it from `(iid, cond, fire)` and
  compares **canonical bytes** (§2.4, not Python equality — `True == 1` there and
  `true ≠ 1` here). This is `README-l4 §1`'s *fold only what inverts*, applied to
  the pending set, and it is what makes releasing the episode at the door a
  demotion rather than a loss booked as compression.
* **The `iid` is not already known.** `§5 L5` names no cancellation, revocation,
  expiry or **re-arming**, and `corpora/l5stream/grammar.md`'s *No cancellation*
  section records that the corpus invents none. The engine invents none either:
  the first arming of an `iid` wins, and a later payload carrying it arms nothing.

### 1.3 Arming releases the episode; firing takes it back, or books the loss

An armed intention's episode is **not stored**. The pending entry carries
`(t0, cond, fire)` and `arms` has already proved the payload rebuilds from them
byte-for-byte, so the episode is a redundant copy of something the state already
holds — Layer 4's demotion, with the pending set as the derived view. `read(t0)`
answers it in full for as long as the intention is pending.

**Firing consumes that derivation**, and this is the sharpest thing this layer has
to say about itself:

> The pending entry is gone, so nothing rebuilds a condition any more. The
> episode is **offered back to the store where the budget already has room** — it
> is content the engine once released, not arriving fuel, so taking it back by
> evicting something else would be an eviction motivated by bookkeeping rather
> than by the importance law. Where there is no room, the demotion has become a
> **loss** and is booked into the forgetting record while the demotion counter
> gives it back.

At a generous cap that means nothing is lost: on `l5stream` at `DEFAULT_BUDGET`
all 20 000 caller events come back byte-exact, `forgotten = 0`, and 945 demotions
stand for the 945 intentions whose episodes the pending set holds in derived form.
At the ratified cap the budget is pinned and there is never room, so all 765
firings book their promise as a loss — and `read(t0)` abstains on exactly those.
It is `README-l4 §4`'s invariant — **the demotion invariant is invertibility** —
carried to promises, and it is why the closing ledger survives this layer:

```
demotions + forgotten + episodes held  =  17 772 + 2 041 + 952  =  20 765  =  next_t
forgotten                              =  exactly the t read() abstains on  =  2 041
```

The second identity is the one with teeth, and at Layer 5 it is asserted over
**every** logical time the engine ever assigned, its own firings included.

### 1.4 Firing, in one pure transition

After the caller event is folded at its own `t`, the arriving event is evaluated
against every **eligible** pending intention — every one written at a strictly
earlier logical time, which is `grammar.md`'s *"eligible at `k0 + 1`"* stated over
logical time so that it reads the same under either cascade reading — and the
satisfied ones fire in **`iid` ascending order**, each at the next consecutive
`t`. `ingest` returns the caller event's `t`; `next_t` advances by `1 + f`
(`R6` clause 2).

**Cascades take the plain uniform reading**: an emitted event is an event, and
conditions are evaluated against all events. `R6` clause 2 expressly leaves the
question open and records that it is *unobservable* on `corpora/l5stream` by the
GUARDEDNESS induction, so both readings give the identical schedule there. The
uniform one is taken because it is the reading that needs no exception written
anywhere, and the work list is FIFO — which, under the `t` semantics, **is** `t`
order. Termination is structural and not a limit this layer invents: every firing
removes one intention from the pending set and nothing ever puts one back, so a
transition emits at most `|pending|` events.

**A firing is not discretionary.** Where the budget cannot house one even after
eviction, the engine refuses the **whole transition** under `§4.1.2` — `t`
unspent, state unchanged — because an event that never happened cannot have
satisfied anything. That is the honest response and not a missed trigger; on the
binding corpus it never arises, and `refused = 0` is asserted.

---

## §2. What the strains found (`trials/strain/l5/`)

### 2.1 Absent-mindedness: a promise is never silently dropped

The Schacter sin this layer is heir to is the **prospective** one — the intention
formed and then not acted on — and an engine under pressure has an obvious way to
commit it: drop the pending entry, keep the episodes, and score beautifully on
everything except the thing nobody measured. Measured on the binding corpus at the
ratified cap, through `§7`'s query interface alone:

* **765 fired + 180 pending = 945 ingested.** Not one promise left the state
  without firing or still waiting.
* A **pending** intention's own `intend` event comes back **byte-exact** from
  `read(t0)`; a **fired** one's abstains, and its loss is **in the record** —
  `forgot_at(t0)` carries it. That last assertion is the one that would go red
  against an engine still booking the released episode as a lossless demotion,
  which is precisely the defect `BOUNDARY.log` line 26 found one layer down.
* The closing ledger of §1.3, over all 20 765 logical times.

And the price of the design decision in §0.1, stated as a measurement rather than
implied: at a cap that takes **every** episode, an intention arriving still gets
armed — the promise wins, the episode loses, and **the displacement is a recorded
loss and not a silence**.

### 2.2 The fired ledger binds — GAPMAP §2, inverted

`autopsy/generative-agents/ANATOMY.md` records an expiration written into every
memory and consulted by nothing; `autopsy/GAPMAP.md §2` generalises it across four
engines as *recorded but never binding*. The exactly-once ledger is the Layer-5
counterpart and the one field an engine could most plausibly write and never
consult. It is asserted read on **both** paths:

* **the satisfaction path** — an intention satisfied 200 times fires **once**;
* **the arming path** — an `iid` that has fired arms nothing, so a second `intend`
  payload carrying it does not re-arm (§1.2). No frozen corpus reaches this path,
  because `l5stream`'s `iid`s are contiguous and unique, which is exactly why it
  needs a fixture.

The teeth are **demonstrated rather than assumed**, in the shape `strain/l3`
established for its inflation guard: a **ledger-blind reference policy** — a trial
fixture, never engine code — reaches `dup-fire = 199` on the same stream where the
engine reaches 0. A guard trial that could not go red against a decorative mark
would prove nothing.

### 2.3 The demotion seam, from the other side

`strain/l4` measured what demotion *costs* (demoted content is `t`-addressable and
not cue-addressable — 26‰ cue reach). This measures what it must not cost: a
`count_ge` fold fires exactly once at a cap where **not one episode survives**, and
no counted event is answered as held (`provenance.kind` is `derive` or the read
abstains; `recall` never appears). The counters the fold reads are Layer-4 state,
two cells per grammar kind and never decremented, so the fold outlives the
episodes it counts — which is `grammar.md`'s own sentence about why this layer is
built on that one, made a measurement.

### 2.4 Determinism through arming and firing

Layer 5 adds two orderings a scan order could leak into — the pending set's and
the fired ledger's insertion order — and one place an engine could substitute its
own for a declared one. Asserted at two scales: byte-identity across two
independent replays of a 4 000-event prefix under real pressure (which fires,
demotes and forgets), and the snapshot round trip at the gate's own cap, where the
pending set, the fired ledger and the exactly-once invariant all have to survive
serialization. Plus a fixture that arms ten intentions in **descending** `iid`
order and satisfies all ten with one write, so an engine firing in insertion order
would produce the exact reverse of the declared one — and be a `t` apart rather
than a hash apart.

---

## §3. What Layer 5 CAN express

- **Prospection at the ratified gate.** On the binding corpus
  (`corpora/l5stream`, BOUNDARY-RULINGS.md R6 clause 1): **trigger-precision
  1000, trigger-recall 1000, dup-fire 0, miss 0, F 1000, B 1000** against a gate
  of `= 1000, = 1000, = 0, = 0, ≥ 980, = 1000`, at **250‰** of the raw episodic
  footprint with `refused = 0`, `wrong = 0` and `fabricated = 0`. The four
  identities are attained and not approached; `F` clears its one threshold with
  its whole slack unspent (the gate admits 35 wrong answers of 1 710 and the
  engine returns none), and every named capability-free baseline sits far below —
  the strongest, `fire-on-kind-atom-only`, is 621‰ short on both precision and
  recall (`ATTAINABILITY.md §5`).
- **Exactly-once, audited by the constitution's own clock.** 765 firings at 765
  logical times of their own; 20 000 caller writes become **20 765** logical
  times, the last firing at `t = 20 760`. `_l5score.assert_t_identity` checks the
  engine's firing report against `next_t − |caller stream|`, so an engine that
  fired twice and reported once fails on `§1.3` rather than on a score.
- **The 180 intentions nothing satisfies stay dormant to stream end**, and their
  P1 is **unanswerable**: abstaining scores 1000 under §3.0, and answering one is
  a fabrication scored 0. `fabricated = 0`.
- **Several intentions satisfied by one write all fire**, each once, in `iid`
  ascending order, at consecutive logical times — 34 caller indices with a fan-out
  of 3 on the binding corpus, ten in reverse arming order on a fixture.
- **Conditions over content the layer below has released.** 111 fireable
  `count_ge` folds fire exactly at their satisfaction points while the engine
  holds 952 episodes of 20 765 events. A trigger that could only fire from held
  episodes would fail by arithmetic: 182 555 raw cells against a 45 638-cell cap.
- **A pending intention is readable.** `read(t0)` returns the `intend` event
  byte-exact while the intention waits, regenerated from the pending entry.
- **Layers 1, 2, 3 and 4, carried forward.** The inheritance class replays §5 L1's
  exact IO and byte-identical round trip, §5 L2's cue gate (`cue-C ≥ 900`,
  `F ≥ 950`), §5 L3's retention battery on both frozen pressure streams, and — new
  at this layer — §5 L4's consolidation battery on `corpora/l4stream` **in budget,
  as identities** (`C = 1000`, reconstruction `F = 1000`). The Layer-4 row is the
  one prospection could actually break, and it does not.

## §4. What Layer 5 CANNOT express (the boundary for Layer 6+)

- **No calibrated confidence — the Layer-6 humility seam.** This is the precise
  statement, and it is structural rather than a promise. Every answer this engine
  returns carries `confidence = 1000`, and it is **ungated** (§3.4: calibration is
  dormant until Layer 6). That is not a placeholder an engine could tighten; it is
  what the state can support. Confidence here would have to be **derived from
  structural evidence**, and the evidence this layer keeps is binary: an event is
  regenerated exactly or it is not; an intention has fired or it has not; a fold is
  exact or its entity is damaged. There is no quantity in this state that varies
  with how likely an answer is to be right, because every answer it gives is one
  it has proved.

  Stated for the layer above: **a capped-5 engine is confident-by-default, and
  should fail `§5 L6` structurally rather than marginally.** `§5 L6` gates on
  `Brier ≤ 40`, `ECE ≤ 30` and `AUROC ≥ 900` with a humility ceiling of
  `capped AUROC ≤ 600`, and `§5.1 L6` already names the mechanism: *"A capped
  engine below Layer 6 carries no confidence model, so the harness scores it
  confident-by-default; the calibration bound then fails by construction."* Make
  that exact against this engine: **AUROC is a ranking statistic** (`§3.4`, the
  Mann–Whitney form), and a constant confidence ranks nothing — every
  correct×incorrect pair ties, ties count ½, so `AUROC = 500` exactly, not
  approximately, whenever both classes are non-empty. The ceiling of 600 is not
  approached from below by a poor model; it is sat at by arithmetic, and the
  honest residual is that `§3.4` makes AUROC **undefined when either class is
  empty** — so `humility/l6/IMPOSSIBILITY.md` will have to say what a battery does
  with an engine whose answers are all correct, which on this corpus's P1/P2
  battery is exactly what happens. That is the seam, and it is worth naming now:
  **the Layer-6 humility battery needs a query class this engine gets wrong**, or
  its ceiling is vacuous rather than loose.

- **No cancellation, revocation, expiry or re-arming.** `§5 L5` names none, the
  corpus invents none, and neither does the engine. An intention, once armed, is
  pending until it fires and forever if it never does; an `iid` that has fired is
  done. These are not omissions to be filled in later without a ruling — they are
  capabilities the constitution does not gate, and adding one would be adding a
  measure `§5` has no threshold for.

- **No recall of a pending intention or of an emitted event.** Both are
  regenerated by `read(t)` and neither is reachable **by cue**: `recall` runs over
  the handle index of retained *episodes*, and neither tier is one. This is the
  same seam `README-l4 §4` measured for demoted content, one tier wider — and it
  is a non-capability by arithmetic, not by omission, for the same reason: at
  250‰ exactly one access path is affordable.

  > **Note added 2026-08-01 (`[L5] [STRAIN]`, the prospection blocking seam).**
  > The paragraph above states this price in prose and nowhere in a number, which
  > `PULSE` (`BOUNDARY.log` line 34) recorded as the one genuine gap in the
  > seven-sin strain audit: **blocking**, the sin of a memory that is present and
  > unreachable, is now committed by two tiers no earlier layer had. It is
  > measured on the binding corpus at the ratified cap by
  > `trials/strain/l5/t_prospection_blocking_seam.py`. Nothing above is
  > corrected; the numbers the prose never carried are these, and they bind from
  > here:
  >
  > **Both prospection tiers are `t`-addressable and not cue-addressable.** At
  > `budget_cap` 45 638 on `corpora/l5stream`: all **180** pending intentions
  > return their own `intend` event byte-exact from `read(t0)` and all **765**
  > firings return their emitted payload byte-exact from `read(t_fire)`, every one
  > of them tagged `derive` and never `recall` — and **not one** of those **945**
  > prospection-tier events answers a cue built from its own payload. Every
  > blocked cue **abstains**; none is answered wrongly, so the missing channel
  > costs 100 per query under §3.0 and never 0. The cue channel reaches the
  > **952** held episodes and nothing else, **952 of 18 724** events still
  > answerable by `t` — **51‰**, against `README-l4 §4`'s 26‰ one layer down, and
  > all 952 are still recalled exactly, so what is asserted is a channel that
  > does not exist and not an index the trial broke.
  >
  > **The reason above is the right reason for Layer 4 and for neither tier
  > here**, which is what the measurement found and what this note exists to
  > record (`R6` clause 3: the historical sentence stands as written, the
  > divergence is recorded rather than edited away). The budget closes nothing
  > here:
  >
  > * **the armed tier** — a payload is **cue-addressable or an intention, never
  >   both**. `recall` addresses an episode by a `HANDLE_FIELDS` atom
  >   (`README-l3 §0.2`), the frozen `intend` grammar carries none of them, and
  >   §1.2 arms only a payload that rebuilds from `(iid, cond, fire)` as canonical
  >   bytes — so a would-be intention carrying `entity` is retained as an ordinary
  >   episode and reached exactly, and arms nothing. **The rule that opens the
  >   capability is the rule that closes the channel**, which is the engine-side
  >   form of the field note that found the shell half (`FIELD.md`, 2026-08-01:
  >   adding `tok` leaves the payload perfectly canonical and stops it arming).
  > * **the fired tier** — the closure is the **tier**, not the grammar. A firing
  >   is folded and its episode released into the fired ledger, which regenerates
  >   it, so it is never an episode and never earns a posting: a fire payload that
  >   *does* carry a handle field is still unreachable while an ordinary event
  >   carrying the same atom is reached exactly by it.
  >
  > The same rule prices the loss, too: an `intend` payload declaring
  > `importance` carries a fourth field and stops arming, so **a promise always
  > weighs exactly 1 in the forgetting record and can never outbid the episodes it
  > displaces**. The trial pins all of it so it cannot change silently in either
  > direction; this note says why it is what it is.

- **No inference beyond the declared condition grammar.** Six predicates, three
  connectives, and a condition outside them arms nothing. The vocabulary is a
  **declared reading** of a frozen grammar, not a learner; an engine that guessed
  at an unknown predicate would be firing on a condition it could not evaluate.

- **No cascade the corpus can exhibit.** The engine takes the uniform reading and
  evaluates conditions against emitted events, but `corpora/l5stream`'s
  GUARDEDNESS makes that unobservable by construction, so **the reading is
  untested by any gate**. It is stated here rather than claimed: what is measured
  is that the two readings coincide on this corpus, and `R6` clause 2's first
  express non-decision stands.

- **No reconstruction of what was shed or forgotten.** Inherited unchanged from
  Layer 4, and it now reaches promises: a fired intention whose episode the budget
  could not take back is recorded as a count and a mass per `t`-range and **never
  as a payload**. `humility/l4/IMPOSSIBILITY.md §3`'s pigeonhole applies to this
  engine too — 2 041 distinct payloads into 25 integer cells admits no injective
  map — so those events are unanswerable in principle and the engine abstains on
  all of them.

- **No generation and no binding provenance.** Provenance tags are attached and
  are derivable (a firing cites its own `t` with `kind: "derive"`), but neither
  required nor scored until Layer 7 (§4.2). Nothing in this layer produces
  content: a fired payload is the payload the caller wrote into the intention,
  byte-for-byte, and `§1.4`'s *"the engine adds nothing to an event but its `t`"*
  is asserted on every one of the 765.

## Reading list for the next session

Per `CLAUDE.md §1`, the next session reads this README before acting. The one
sentence to carry forward: **Layer 5 holds a condition it has proved it can
evaluate and a payload it has proved it can rebuild, releases the intention's own
episode because the pending entry regenerates it, and then — on the first later
event that satisfies the condition — emits the intended payload at a logical time
of its own, exactly once, moving the intention from the pending set into a fired
ledger that is read on every later satisfaction *and* on every later arming, in a
transition that pays for itself in cells and books the promise's own episode as a
loss the moment firing makes it unregenerable.**

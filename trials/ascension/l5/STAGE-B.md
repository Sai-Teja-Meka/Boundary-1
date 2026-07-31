# STAGE-B.md — the Layer-5 Stage-B record: the `t` semantics, and the battery

`[L4] [ASCEND]` prospection, **Stage B**. R2's standing step orders an ascension
*attainability arithmetic → trials → engine*, and this is the middle step: the
ascension battery, the humility battery and the inheritance battery are written
and run against an engine that **does not exist**, so that no threshold, no
reading and no corpus choice can be tuned to something an engine already does.

`core/layers/l5_prospection.py` does not exist. `trials/adapters/l5.py` does not
exist. **No Layer-5 gate binds on anything**: `R5` settled a reading of R2's
obligations and expressly declined the corpus binding, and this session does not
take it either — `RULING-R6-DRAFT.md` asks a human for it.

What this session adds:

| | |
|---|---|
| `trials/ascension/l5/t_prospection.py` | the gate battery — **engine-gated skips**, plus two engine-free trials |
| `trials/humility/l5/` | the capped-4 battery — **green today** — and its `IMPOSSIBILITY.md` |
| `trials/inheritance/l5/t_inheritance.py` | Layers 1–4 re-asked at cap 5 — engine-gated skips, plus one engine-free trial |
| `trials/_l5score.py` | the engine-facing replay/observe/score, feeding Stage A's frozen scorer |
| this document | the record, and **§1** the `t` decision |
| `RULING-R6-DRAFT.md` | the draft: the corpus binding, the `t` clause, the 271 note |

---

## §1. T-SEMANTICS — what a firing does to logical time

### 1.0 The question, and its standing

`R5` closes with it, in its own *"what this ruling does not do"*:

> *"It does **not** settle the engine-`t` question. `§1.3` gives every event its
> own logical `t` and a fired event is an event, so over `corpora/l5stream` the
> exhibited witness turns 20 000 caller writes into 20 765 logical times, the last
> firing landing at `t = 20 760` — **one caller `ingest` advancing `next_t` by
> more than one**, which every anchor and the whole `inheritance/` class currently
> assume it cannot. That is measured and asserted at Stage A … and deliberately
> left open: it is a Stage-B and Stage-C design question, and settling it in a
> ruling written before those trials exist would be exactly the ordering R2
> forbids."*

Stage B is where R2's ordering says it may be settled. It is settled **from the
written texts**, not from convenience, and the derivation is below so that the
clause `RULING-R6-DRAFT.md` proposes can be checked against it rather than
believed.

### 1.1 The texts

| | |
|---|---|
| **§1.3** | *"Upon ingestion the engine assigns the event a **logical time `t`**: a non-negative integer that is **unique within a state**, **strictly increasing in ingestion order**, and begins at `0`. `t` is engine-assigned and engine-owned. … `t` is the sole ordering authority in the system. There is no wall-clock time."* |
| **§1.4** | *"The canonical in-engine event record is exactly `{"payload": <value>, "t": <int>}` … The engine adds nothing to an event but its `t`."* |
| **§2.2** | *"**Wall clock** — no `time`, no `datetime`, no calendar. **The only clock is the engine-assigned logical `t` (§1.3)**."* |
| **§2.3** | Identical `(state, input)` sequences produce **byte-identical** results. |
| **§5 L5** | *"Prospection — `intend(condition → **event**)`; triggers fire exactly-once **on future writes**."* |
| **§5.1 L5** | *"Every intention whose condition a future write satisfies must fire … A **fired event's payload** must match the intended event essentially exactly."* |
| **§7.1** | *"`ingest(state, payload) -> (state', t)`. Pure. **Appends one event**, assigns and returns its logical `t` (§1.3), and returns the new state."* |

### 1.2 The derivation, in five forced steps

**(a) A firing produces an EVENT.** `§5 L5` writes the capability as
`intend(condition → event)` and `§5.1 L5` speaks of *"a fired event's payload"*.
The object a trigger produces is an event of the system, not a callback, a
side-band signal or a query result — and `§1.1` forbids the alternatives from
being anything the engine deals in at all (*"Configuration, queries, and
side-band signals are not fuel"*).

**(b) It therefore carries a `t`.** `§1.4` says an in-engine event record is
**exactly** `{payload, t}`. There is no event record without a `t`, so a fired
event has one. `§2.2` forecloses every other kind of stamp: there is no clock but
`t`.

**(c) That `t` is its own, and this is forced rather than chosen.** `§1.3` makes
`t` **unique within a state**. The arriving caller write is one event and the
firing it causes is a different event, so they cannot share a `t`. No other
candidate exists: `t` is an integer (§1.3, and §2.2 forbids floats, so there is
no "between"), a caller may not supply one, and there is no wall clock. **A
firing consumes a logical `t` of its own.**

**(d) It sits immediately after the write that satisfied it.** `§1.3` makes `t`
**strictly increasing in ingestion order**, and `§5 L5` has triggers fire *"on
future writes"* — a firing is caused by an arriving event, so it cannot precede
it and its `t` is strictly greater. It cannot be deferred past the next caller
write either: `§2.1` makes a write one pure transition, so the state that
transition returns must already contain the firings that transition caused, and
*"exactly-once on future writes"* would otherwise be ambiguous about which write
a trigger fired on. Where one write satisfies several pending intentions, `§2.3`
requires a **declared total order** rather than a scan order, and the corpus
declares it: `iid` ascending (`corpora/l5stream/grammar.md`). So a write is

```
one caller event at t = next_t,  then its firings at the next consecutive t,
                                 in iid ascending order
```

**(e) `ingest` returns the caller event's `t`, and `next_t` advances by `1 + f`.**
`§7.1` says `ingest` *"appends one event, assigns and returns its logical `t`"*.
The one event the caller submitted is appended and its `t` returned; the firings
are appended by the same transition but are not what the caller handed over.
After the call, `next_t` is higher by `1 + f` where `f` is the number of firings
that write caused.

**On `§7.1`'s "appends one event", stated plainly because it is the one place a
reader will stop.** Two readings are available:

* **(i)** a cardinality constraint on the transition — *at most one event may be
  added per `ingest`*. Under (i) prospection is impossible, because a fired event
  is an event (step (a)) and would need appending, and `§7.1` declares only three
  operations, so there is no other door. `§5 L5` and `§7.1` would contradict each
  other, and both are ratified.
* **(ii)** a description of what the **caller's payload** does — one payload, one
  event, one returned `t` — silent about events the engine derives from that
  write. Under (ii) both sentences are true.

**Reading (ii) is taken, for the reason Stage A took its Reading 1:** it is the
only reading under which `§5 L5` and `§7.1` are both true. This is the same
argument in the same place — `ATTAINABILITY.md`'s Reading 1 already held that an
intention cannot be a fourth verb and must arrive as an ingested payload, on
exactly this ground — and it is a **reading of ratified text, not an amendment
of it**. `RULING-R6-DRAFT.md` clause 2 asks a human to ratify it rather than
leaving it as a session's assumption.

**And the alternatives fail on written text, not on taste:**

| candidate | what it contradicts |
|---|---|
| the firing shares the triggering write's `t` | `§1.3` — `t` is *unique within a state* |
| the firing gets no `t` at all | `§1.4` — an in-engine event record is *exactly* `{payload, t}`; and `§5.1 L5`'s `F` clause becomes unmeasurable through `§7`'s three operations, since Stage A's frozen P2 battery is `read(t_fire)` |
| the firing gets a fractional or derived time | `§2.2` — no floats, and no clock but `t` |
| firings are batched and flushed at the next caller write | `§2.1` — the transition that caused them must return the state containing them; and `§5 L5`'s *"on future writes"* stops naming a write |

### 1.3 The decision

> **A firing is an event and occupies a logical `t` of its own, assigned in the
> same pure transition as the caller write that satisfied it, immediately after
> it, consecutively and in `iid` ascending order where several fall together.
> `ingest` returns the caller event's `t`. One caller `ingest` therefore advances
> `next_t` by `1 + f`, where `f` is the number of firings that write caused.**

On `corpora/l5stream` that is 20 000 caller writes becoming **20 765** logical
times, the last firing at `t = 20 760` — the numbers Stage A measured and
`t_attainability.py::trial_one_caller_ingest_can_advance_next_t_by_more_than_one`
has asserted engine-free since. `t_prospection.py::trial_the_engine_t_layout_is_the_one_the_written_texts_force`
asserts them of an engine, which is the half Stage A could not reach.

### 1.4 The constraint: Layers 1–4 do not move, and not by exception

The constraint this decision was taken under is that on **intention-free streams
the engine must advance `t` exactly as L1–L4 did, or every anchor is wrong.**

It holds, and it holds for the strongest available reason: `f = 0`. The general
rule is *one caller event plus the firings it caused*; a stream with nothing
pending causes no firings; *"one ingest, one `t`"* is the `f = 0` case of the
same rule rather than a clause suspended for old corpora. Nothing is
grandfathered and no special case is written anywhere.

**How the anchors actually construct the assumption** — because a decision about
them should be checked against what they do, not against what they are said to
do. `anchors/t_l1.py`, `t_l2.py`, `t_l3.py` and `t_l4.py` each replay a **frozen
corpus** through a **frozen adapter** and compare `state.next_t` against a number
recorded in `anchors/l*.json`, beside a state hash. They do not assert a *law*
about `ingest`; they assert *this corpus, replayed, ends at this `next_t`*. The
same is true of `ops/l1/t_verbs.py::trial_write_assigns_t_from_zero_strictly_increasing`
and of `inheritance/l4`'s verb battery, which use fixed `spawn` payloads.

So the assumption is safe exactly while the streams they replay carry nothing
that can fire — and that is a theorem about frozen bytes, so it is asserted over
the bytes:
`t_prospection.py::trial_one_caller_ingest_advances_next_t_by_exactly_one_on_an_intention_free_stream`
walks **every corpus in `corpora/registry.py`** and requires that `l5stream` is
the only one carrying an `intend` payload. A corpus frozen later that did carry
intentions goes red there and forces whoever freezes it to say what it means for
the anchors, rather than discovering it as a drifted hash.

### 1.5 The contradiction check — every written text that could object

The ASCEND directive for this session is explicit: *if ANY written law, ruling or
frozen trial contradicts the chosen semantics **as written**, stop and report for
a human ruling.* The check was run, and it is recorded here in full so that its
completeness can be argued with:

| text | bears on | verdict |
|---|---|---|
| `§1.3` uniqueness / strict increase / engine-owned | the whole decision | **requires** it; the firing's own `t` is forced |
| `§1.4` *"the engine adds nothing to an event but its `t`"* | the fired payload | **consistent**, and asserted: `read(t_fire)` must return the intention's `fire` payload verbatim. The corpus draws `fired`'s `text_id` from `note`'s global counter precisely so attribution needs no stamp |
| `§2.1` purity, `§2.3` determinism | firing order | **consistent**; `iid` ascending is a declared total order |
| `§2.2` the `t` clause | any other clock | **forecloses** every alternative |
| `§3.3` / `§4.1` budget | firings' cells | **consistent**; emitted events compete inside the same cap (`ATTAINABILITY.md §1`) |
| `§5 L5`, `§5.1 L5` | firing semantics | **requires** a fired *event* with a readable payload |
| `§7.1` *"appends one event"* | the transition's cardinality | **admits two readings**; reading (ii) is the only one under which `§5 L5` and `§7.1` are both true, and is put to a human as `R6` clause 2 rather than assumed |
| `§7.2` the Answer, `§7.3` the cardinal rule | the battery's queries | **consistent**; an engine without the capability abstains |
| `R1`–`R4` | — | none reaches `t` |
| `R5` | — | expressly **leaves it open** for this stage |
| `anchors/t_l1..t_l4` + `anchors/l*.json` | recorded `next_t` | **unaffected**: no anchor corpus carries an intention (§1.4, asserted) |
| `ops/l1/t_verbs.py::trial_write_assigns_t_from_zero_strictly_increasing` | `t = 0,1,2` | **unaffected**: `spawn` fixtures, `f = 0` |
| `inheritance/l4/t_inheritance.py` verb battery | *"increase by one per successful write"* | **unaffected**: same fixtures, `f = 0`. The sentence is true of what it runs |
| `ascension/l5/t_attainability.py::trial_one_caller_ingest_can_advance_next_t_by_more_than_one` | the layout | **already asserts this semantics** — `next_t = n + firings`, and *"the caller events and the firings partition the logical times `0..next_t-1`"*, *"a firing is ingested where it fires"* |
| `core/state.py` — `next_t: "next logical time to assign (§1.3) == successful writes"` | the counter's meaning | **consistent**: a firing *is* a successful write of an event; the identity is with writes, not with caller ingests |
| `core/layers/l3_forgetting.py::_drop_arriving` — *"It is ingested (its `t` is assigned and consumed, §1.3) and immediately forgotten"* | whether a `t` survives its payload | **supporting precedent**: a `t` is spent by ingestion, not by retention — already true one layer down |

**Nothing contradicts it.** The decision is put to a human as a ruling clause
because it is a *reading* that binds future layers, not because this session found
an objection it could not answer.

### 1.6 What is deliberately NOT decided

**(a) Whether a fired event is itself a "write" that pending intentions are tested
against** — cascades. No ratified text forces an answer: `§5 L5` says triggers
fire *"on future writes"* and does not say whether an engine-emitted event is one.
It is also **unobservable on this corpus**, by construction rather than by luck:
`corpora/l5stream/grammar.md`'s GUARDEDNESS induction makes it impossible for any
condition in the grammar to be satisfied by a `fired` payload, and
`ops/l5/t_l5stream.py` asserts that twice — once as the induction and once over
the whole 945 × 945 cross product. Both readings therefore produce the identical
firing schedule here, and the gate is invariant to the choice.

It is recorded rather than settled because settling an under-determined question
on a corpus that cannot exhibit the difference is exactly how a convenience
becomes a precedent. **The `t` decision does not depend on it**: under either
reading each firing takes its own `t`, in order, in the same transition.
`RULING-R6-DRAFT.md` clause 2 states the non-decision so a later session cannot
cite the ruling as having made it.

**(b) What an engine must do when the budget cannot house a firing.** The battery
asserts the invariants and not a policy: `B = 1000` after every write, the `t`
partition, and exactly-once. Whether an engine makes room by the inherited
Layer-3/Layer-4 eviction path or refuses the whole transition under `§4.1.2`
(`t` unspent, state unchanged, no partial write) is the engine's business at
Stage C — with one thing already fixed by the gate rather than by preference: a
firing is **not** discretionary. `miss = 0` means an intention whose condition is
satisfied fires, so an engine may release a firing's *episode* the way Layer 4
releases any other, but it may not decline to fire.

---

## §2. The query vocabulary this battery declares

`§7.1` gives three operations and no query vocabulary; each layer declares the
queries its battery asks, as `_l4score` did for Q1–Q4. Layer 5 asks two, and
`ascension/l5/t_prospection.py::trial_the_declared_query_vocabulary_is_the_one_the_scorer_speaks`
asserts that this section and `_l5score` have not drifted apart.

| | query | answer |
|---|---|---|
| **P1** | `{"op":"fired","iid":I}` | the **list** of event records intention `I` fired, `t` ascending; **abstain** iff it never fired |
| **P2** | `{"op":"read","t":T}` | the event record `{"payload":…,"t":T}` — the Layer-1 verb |

**Why P1 answers with a list.** `dup-fire = 0` is a gate clause, so an intention
that fired twice has to be visible **through the query interface** rather than
only in an engine's own bookkeeping. A correct answer is a one-element list; a
two-element list is a wrong answer *and* a `dup-fire`, and both are scored. An
answered P1 that is not a non-empty list of event records is scored wrong and
counted as malformed, so the shape cannot degrade quietly.

**Why P2 is `read`.** Stage A chose it and the reason survives: `§5.1 L5` asks
that *"a fired event's payload match the intended event essentially exactly"*,
and the way to ask that of a black box through `§7`'s three operations is to read
the event back at the `t` the engine assigned it. That makes *"the payload
matched"* a measurement rather than a definition — and it is also what makes §1's
`t` decision load-bearing rather than bookkeeping: without a `t` of its own, a
firing has no address to be read back at.

**The audit that makes the self-report honest.** `_l5score.assert_t_identity`
requires

```
next_t  −  |caller stream|   ==   the number of firings P1 reports
```

because a firing consumes exactly one `t` and nothing else in this replay
consumes one (§1). An engine that fired twice and reported once fails it, and so
does one that emitted an event nobody asked for. The engine's own clock audits
its own report.

---

## §3. The battery, and what it deliberately does not repeat

**One fixture, one truth.** Stage A exhibited the oracle ceiling, scored the four
named capability-free baselines, priced both witnesses with their bookkeeping and
their loss reserve, and stated the two R2 obligations as findings —
`t_attainability.py` asserts every one of those on every run. **None of it is
restated in the Stage-B battery**, which names the owning trial instead. The gate
*constants* are duplicated across the two files, and that duplication is what
`laws/t_rulings.py` exists to police: both copies are bound to one `§5 L5` clause
and, for the six R5 reaches, to that entry.

| trial | what it binds |
|---|---|
| `trial_prospection_fires_exactly_once_and_the_four_clauses_are_identities` | precision = recall = 1000, dup-fire = miss = 0, **as identities** (R5 clause 1) |
| `trial_never_fires_intentions_stay_unfired_for_the_whole_stream` | the 180 never-fires: unfired, P1 abstains, `fabricated = 0` |
| `trial_several_intentions_satisfied_by_one_write_all_fire_each_at_its_own_t` | 34 indices, fan-out 3: each fires once, `iid` order, consecutive `t` |
| `trial_a_condition_over_demoted_content_fires_from_consolidated_state` | the L4 seam: 111 fireable `count_ge` folds fire, and a counted event comes back `derive` and not `recall` |
| `trial_the_fired_payload_matches_and_f_clears_the_graded_clause` | `F ≥ 980`, literal §3.0, `wrong = 0` |
| `trial_the_budget_law_holds_after_every_write` | `B = 1000`, and `refused = 0` — a refused caller write is one the engine never saw |
| `trial_the_footprint_is_priced_under_rule_p` | R4 clause 3's atom audit, the half a trial can see |
| `trial_the_engine_t_layout_is_the_one_the_written_texts_force` | §1, of an engine |
| `trial_one_caller_ingest_advances_next_t_by_exactly_one_on_an_intention_free_stream` | §1.4, over every frozen corpus — **engine-free, green today** |
| `trial_the_declared_query_vocabulary_is_the_one_the_scorer_speaks` | §2 against `_l5score` — **engine-free, green today** |

Three clauses are worth stating in their own right because they are where a
Layer-5 gate could be quietly loosened:

* **The four identities are `require_equal`, not `>=`.** R5 clause 1 is why:
  there is no margin to spend on a clause whose ceiling *is* the gate, so there is
  no inequality to widen later.
* **`F` binds under the literal `§3.0` table.** R3 excludes Layer 5 in its own
  text and **no extension is requested** — the oracle reaches 1000, so the layer
  does not need the friendlier reading and declines to ask for it, which is R4
  clause 4's discipline applied again. An honest abstention on an answerable P1
  scores 100 here.
* **`refused = 0` is asserted.** A refusal is lawful under `§4.1.2` and is not
  lawful *here*: a refused write is a write the engine never saw, so its
  intentions never arrive and its conditions are never tested. The identity would
  be met by not being asked.

**And one clause the battery deliberately does NOT assert.** The first draft
required `wrong = 0` beside `F ≥ 980`, and that was over-tightening, caught by
running the scorer against a mock engine that fires everything correctly and
returns one wrong payload: it scores `F = 999`, clears the ratified gate, and
would have been failed by an assertion `§5 L5` does not make. Given the four
identities the only possible wrong answer *is* a payload that differs at the right
`t`, which is exactly what `F` measures — and `F ≥ 980` admits **35** of them out
of 1 710. `§5 L5` ratified 980 and not 1000, and `R5` clause 1 records that slack
as the constitution's own answer to R2's perfection objection. Asserting
`wrong = 0` beside it would gate at 1000 under a 980 clause. It is computed and
reported, never required. This is the one place a Stage-B battery could have
silently tightened a ratified gate, and it is recorded rather than merely avoided.

Three assertions that look like additions and are not, stated so the distinction
is checkable: *no never-fires intention fires* is `trigger-precision = 1000` said
directly (one spurious firing makes the ratio 765/766); the Answer's **shape**
(`malformed = 0`) enforces `§7.2` and `§7.3`, where a non-conforming Answer is a
harness-level failure *"categorically worse than a scored abstention"*, not a
§5 threshold; and `refused = 0` is a precondition for the corpus's ground truth
applying at all, not a measure.

**The battery was validated against a mock engine before being frozen** — a
scratchpad `§7` stub, never committed, implementing the exhibited witness's
schedule. The oracle scores `1000 / 1000 / 0 / 0 / F 1000` through `_l5score`,
which is the check that matters: a battery the exhibited witness could not clear
would be a gate Stage A never showed to be attainable. A duplicate firing is
caught at `dup-fire 1 / precision 997`, a missed one at `miss 1 / recall 999`, and
an engine that emits an event it does not report is caught by the `t` identity
rather than by any score.

---

## §4. The humility side, and one refuted premise

`trials/humility/l5/` is **green this session**: `make_engine(layer_cap = 4)` is
the frozen Layer-4 engine, so the ceiling can be measured today, on the whole
20 000-event stream (~21 s — no prefix ladder is needed, unlike `humility/l4`,
where the capped engine's `O(retained)` eviction path cost 663 s).

Measured: **trigger-recall 0** against the ratified ceiling of 50, precision
`n/a` (§3.4's convention for an empty class — scoring an empty firing set as
perfect would hand a `precision = 1000` clause to the policy that does nothing),
dup-fire 0, miss 765, `F` **271**, `wrong = 0`, `fabricated = 0`, `B = 1000`.

**`IMPOSSIBILITY.md`'s first draft was refuted by its own mandatory measurement,
and the corrected form is sharper.** The intended argument was GAPMAP §2's
thesis — *recorded but never binding*: the capped engine stores the intention as
an event and never reads it as a condition. In budget that is exactly what
happens (**945 of 945** intentions returned byte-exact by `read(t)`, and nothing
fires). **At the ratified Layer-5 cap it holds 30 of 945**: an `intend` payload
has no Layer-4 facet, its condition AST is expensive, and the inherited Layer-3
forgetting law releases it. Under the pressure the gate is stated at, the capped
engine does not even *record* the thing it would fail to read. Both are measured
and both are in the document, because quoting only the flattering one is the
omission `R5 clause 4` was written about.

**The corpus choice is PENDING and both documents say so.** No ruling binds
`corpora/l5stream` to the humility side any more than to the ascension side.
`RULING-R6-DRAFT.md` clause 1 asks for **both bindings together**: a ceiling
measured on one corpus beside a gate bound on another would discriminate nothing.

---

## §5. The inheritance side

`trials/inheritance/l5/` extends the standing class at cap 5 on in-budget
substrates: the Layer-1 verbs, the Layer-2 cue battery at `§5 L2`'s own gate, the
Layer-3 retention battery on both frozen pressure streams as identities, and —
**new at this layer** — the Layer-4 consolidation battery on `corpora/l4stream`,
also as identities (`C = 1000`, reconstruction `F = 1000`, `wrong = 0`,
`fabricated = 0`).

The Layer-4 row is the one prospection could actually break, and it is not a
formality: a pending set, an evaluator on the write path and the engine's own
emitted events all compete for the same cells as the interval table, and the
cheapest way to buy room for them is a lossier derived view — which `§5 L5`'s
four firing clauses would never notice. `footprint ≤ 250` is deliberately **not**
re-applied, because it is a claim about compression under pressure and this class
is defined by there being none.

---

## §6. One corpus-documentation defect, found and handled

`corpora/l5stream/grammar.md`'s closing section, *"The declared properties of the
frozen instance"*, states *"Every number below is a `DECLARED_*` constant in
`generator.py` and is asserted by `trials/ops/l5/t_l5stream.py`"* — and **not one
of its numbers is**. It reads 956 intentions / 775 fireable / 181 never-fires,
26 multi-satisfaction indices with a fan-out of 6, 164 `count_ge` conditions,
181 043 raw cells; the frozen instance is 945 / 765 / 180, 34 indices with a
fan-out of 3, 169 conditions, 182 555 raw cells, and `generator.py`'s
`DECLARED_*` constants say so.

The cause is on the record in `BOUNDARY.log` line 28: Stage A's first corpus draft
was **not guarded**, its own ops trial went red on `iid 6`, and *"the CORPUS was
changed, not the trial"*. The prose was re-derived; that closing block was not.
Everything else in the document — the kinds table, the condition grammar, the
GUARDEDNESS argument, the satisfaction rule, the no-cancellation clause — describes
the frozen bytes correctly and is unaffected.

**Handled the way this repository handles a stale frozen document**: a **dated
erratum note above the block**, no historical line rewritten, naming
`generator.py`'s `DECLARED_*` constants and `ops/l5/t_l5stream.py` as the record
— the form R4 clause 2 used for `README-l3 §4` and the `PULSE` session used for
the `ANATOMY.md` errata. No frozen corpus byte is touched and no number moves: the
corpus was always the one the constants describe, and it is the document that was
describing something else.

---

## §7. What a human is asked to decide

`RULING-R6-DRAFT.md`, in order of how much it binds:

1. **The corpus binding** — `corpora/l5stream` for the Layer-5 ascension gate
   **and** for the humility ceiling, in the shape R1 and R4 established.
2. **The `t` semantics** — §1's decision as a ruling clause, including `§7.1`'s
   reading (ii) and the two things §1.6 deliberately leaves undecided.
3. **The `270` / `271` seam** — whether the standing rule R5's boxed note applied
   once needs to become a general one, now that a third artifact reports it.
4. **The budget reading** — `budget_cap = raw_cells // 4`, still unruled from
   Stage A (`ATTAINABILITY.md §6` question 3), and now the cap three batteries
   actually replay at.

The draft is a **draft**. It is not appended to `BOUNDARY-RULINGS.md`, because
appending is what freezes an entry and no session has authority to freeze a
ruling for itself.

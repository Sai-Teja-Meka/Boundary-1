# ATTAINABILITY.md — Layer 8, Stage A

> **NO GATE BINDS.** `BOUNDARY-HIGH.md §0` defers every Layer-8 threshold, by
> name and in its own text, to *this Stage A plus a ruling*. `R2` obligation 4
> makes computed arithmetic **necessary and never sufficient**: the numbers below
> are measurements of policies, not thresholds on engines, and they acquire
> authority only in the entry a human appends to `BOUNDARY-RULINGS.md`.
> `RULING-R9-DRAFT.md` is deliberately **not appended**, because appending is
> what freezes.
>
> Every figure here is computed by `trials/_l8tasks.py` from frozen bytes and a
> deterministic replay, and asserted by `trials/ascension/l8/t_attainability.py`
> and `trials/ops/l8/t_l8describe.py`, both of which run every suite. Where this
> document and a trial state the same quantity, **the trial's value is the
> enforced one** (`R6` clause 3).

---

## §1. What this session was asked for, and what it found

The SPEC scheduled this Stage A to fill twelve deferred threshold cells. **Seven
of them are Layer 8's and this session fills those.** The other five are Layer
9's, and `BOUNDARY-HIGH.md §2.4` clause 2 puts each number *"at that layer's
Stage A"* while `§6.1` says in as many words that *"Layer 9 repeats the same arc
from its own Stage A with its own ruling"* and *"a Layer-8 ruling does not reach
them"*. Layer 9's `successor conformance` and `emission groundedness` are
quantities over an emitter that would have to be built on a Layer-8 engine that
does not exist, so measuring them here is not merely out of scope — it is
arithmetic with no subject. **The SPEC's text wins and the five stay deferred**;
this is recorded as a scope finding rather than executed quietly.

Of Layer 8's seven, **six are measured and one refuses.** The refusal is
`calibration`, and it is the session's central finding:

> **No artifact of `BOUNDARY-HIGH.md §3`'s shape can force a self-descriptive
> error.** A self-description's subject *is* the state the engine holds, so the
> engine always knows whether its own state determines an answer; `§7.3` makes
> abstention always available and `§3.0` prices it at **100** against **0** for a
> wrong answer. Every policy with a non-empty negative class is therefore a
> policy that answered where its state did not determine — exactly what
> `groundedness` disqualifies. So `n_neg > 0` is **a property of a bad engine and
> never of the artifact**, and `R7` clause 3(b)'s *"both classes non-empty is a
> theorem the artifact carries"* cannot be discharged at Layer 8 by any artifact
> of this shape. `AUROC` is `n/a` on the witness and on the oracle alike, and
> `R7` clause 3(a) says `n/a` **disqualifies, it does not excuse**.

That is a **constitutional** finding in the species of `BOUNDARY.log` line 28,
not a corpus one, and the SPEC's `§3` predicted the general worry in advance
(*"the engine holds the state the question is about, so the resolving signal
cannot simply be withheld from it the way `corpora/l6batteryb` withholds a
coin"*). It predicted the mechanism and named the wrong failure: `§3` expected a
**sixth substrate kill** shaped as *"a question forced to come from a fold may
also be trivially answerable from a field"*. That kill lands too, and it lands
**partially and engine-relatively** — §5 scores both predictions, misses
included.

---

## §2. THE ARTIFACT — `corpora/l8describe`, the triple

`BOUNDARY-HIGH.md §3` says a Layer-8 artifact is not one object but a triple, and
this is the first one built.

| member | where it lives | what freezes it |
|---|---|---|
| the **frozen event stream** | `corpora/l8describe/generator.py` at `SEED = 11011`, `EVENTS = 3200`, output frozen to `l8describe.s11011.e3200.q74.json` | `§8.2`/`§8.3` unchanged, byte-match law binding, seed outside `§8.5`'s holdout range |
| the **frozen query set with its class table** | the same canonical JSON object — 74 queries, four declared classes | `corpora/l6batteryb`'s joint-property reason, carried forward by the SPEC |
| the **frozen derivation procedure** | `trials/_l8derive.py`, committed source in a file of its own | `§9.2`: superseded by a later artifact, never edited in place |

**The answer key is a PROCEDURE and not a table.** It is recomputed on every run
from *(the frozen stream, the engine's ingestion trace, the engine's canonical
snapshot)* and its canonical bytes carry a recorded `sha256`:

```
derived key sha256 = 3943c7130cd6aef6114d2ea8bef3cf906d25ff50d7b7176fe1aa98e5da4708fb
```

**One half of `§3`'s hash obligation is discharged here and the other is
deferred, stated rather than glossed.** `§3` asks for the recorded `sha256` *and*
an `anchors/` entry pinning it. The `sha256` is recorded and re-derived every run
(`ops/l8::trial_the_derivation_reproduces_its_key_byte_for_byte`); the `anchors/`
entry is **not** written, because an anchors entry pins an ENGINE's recorded
state and no Layer-8 engine exists — `R2`'s standing step puts it after the
ruling. The tamper-evidence `§3` asks for is live today; the class entry lands at
Stage E with the engine whose behaviour it would pin.

### 2.1 The four declared classes, and the denominators they fix

`R8` clause 3: the denominator is the artifact's declared class unless clause
3(a)'s two conditions both hold.

| class | n | what it asks | verdict of the derivation |
|---|---:|---|---|
| **KR** | 28 | reachable folds — events of a kind, of a grammar weight, on a key; `(entity, key)` pairs with a chain of at least `m` | the state DETERMINES every one |
| **KL** | 7 | lost folds the state nonetheless fixes, because `§5 L4`'s per-kind counters are never decremented: `lost(kind) = counts[kind] − reachable(kind)` | DETERMINED |
| **KF** | 21 | lost folds the state only BOUNDS — `lost_weight(w)` against the forgetting record's `(count, mass)` | **3 determined, 18 forced** |
| **KU** | 18 | probes whose subject is not in the stream at all | UNANSWERABLE, for every engine |

Answerable core = `KR ∪ KL ∪ KF` = **56**. Declared class = **74**.

### 2.2 The forcing region, and why the weight alphabet has three members

The aggregated forgetting record keeps `(count, mass)` per `t`-range and nothing
else, so *"how many of the events you lost carried weight `w`?"* is

```
x₁ + x₃ + x₇ = count            1·x₁ + 3·x₃ + 7·x₇ = mass
```

— three unknowns against two equations. With **two** weights the system is always
uniquely solvable and the class would be determined everywhere; with **three** it
is uniquely solvable for some `(count, mass)` and not for others. Measured on
this artifact at its declared cap: the record carries **13 buckets at width
256**, of which **one** admits a unique composition and **twelve** do not, and
globally the system admits **259** compositions. That is `humility/l4`'s
pigeonhole — *thousands of distinct evicted payloads map into an aggregate record
of at most 35 integer cells* — turned from an impossibility argument into a
**scored class**.

### 2.3 The declared substrate configuration

`budget_cap = raw_cells // 3 = 15 940 // 3 = 5 313`. `§5 L8` declares no pressure
ratio of its own, exactly as `§5 L5` did not, and `R6` clause 4's reason applies:
a reading is taken and stated rather than left open, because several batteries
now replay at that number.

`//3` and not `//4` **for a measured reason and not a preference**: at `//4` this
stream's interval table does not fit, the engine sheds chains, all 60 entities
are damaged, and the state stops being one a self-description can be honest
about. At `//3` the budget cuts into the **irreducible tier and nowhere else** —
measured: 0 damaged, 2 154 demotions, **915 losses**, `refused = 0`, occupancy
5 310 of 5 313, `B = 1000` asserted after every write.

**An engine-breaking finding of this session's own, fixed rather than relaxed**
(`corpora/l8describe/generator.py`'s docstring carries it): the first draft put
`importance` on `attr` payloads too. The Layer-4 rule is FOLD ONLY WHAT INVERTS,
an `attr` carrying a field `ASSERTION_FORMS["attr"]` does not read does not
rebuild from its facet, and the engine consolidated **nothing** — `atlas[key] =
None` on every key, and at the declared cap **3 200 of 3 200 events forgotten
with all 60 entities damaged**. The artifact was changed, not the reading:
`[L5]`'s unguarded-corpus precedent (`BOUNDARY.log` line 28) in its Layer-8 form.

---

## §3. THE ARITHMETIC — Layer 8's seven cells

Policy classes are declared per `R5` clause 3. **Class E** is the witness: it
reads the engine's **snapshot bytes and nothing else** — not the frozen stream's
lost events, not the answer key, not the class table, not `_l8derive` — and
recovers the weight alphabet, the kind vocabulary and the entity population from
its own state. **Class O** is the oracle, which reads the key.

| `BOUNDARY-HIGH.md §2.1` cell | denominator (SPEC's) | surface | witness attains | proposed |
|---|---|---|---:|---|
| **introspective coverage** | the declared class, WHOLE (74) | `query` | **514** | see `RULING-R9-DRAFT.md` |
| **self-description `F`** | the answerable core (56); `F_all` ungated | `query` | **711** (`F_all` **781**) | ” |
| **groundedness** | the engine's ANSWERED self-descriptions (38) | `query`, checked against `snapshot` | **1000** | ” |
| **tagging** (`§4.2`) | the non-abstaining answers (38) | `query`'s `provenance` | **1000** | ” |
| **calibration** (`§3.4`) | the `A` answered queries | `query`'s `confidence` | `ECE` **0**; `AUROC` **n/a** | **REFUSED — §4** |
| **budget `B`** | the state's own cap | `snapshot` + the refusal path | **1000** | ” |
| **humility ceiling** | §4's capability quantity over the declared class | `query` | capped-7 measures **0** against the witness's **38** | ” |

### 3.1 Groundedness is a different instrument from `F`, and the difference is measured

`F` is scored against the **world** — what the frozen stream says — because
`§3.0`'s *correct* is a claim about the value. `groundedness` is scored against
the **derivation**: an answer to a question the engine's own state does not
determine is **ungrounded even when it is lucky**. The two numbers come apart on
exactly one policy and that policy is the flatterer (§4.2), which is what
`BOUNDARY-HIGH.md §2.1`'s *"why groundedness is the discriminating quantity, and
why it is not fidelity"* asserts and this session measures.

### 3.2 `R8` clause 3(a) is claimed for `groundedness`, and the two conditions are stated

`groundedness`'s denominator is the engine's own report — the answers it chose to
give. It is admissible under clause 3(a) because **both** conditions hold and the
`ATTAINABILITY.md` is required to say which: (1) every member is harness-checkable
against the derivation over frozen bytes; and (2) shrinking the report costs
`introspective coverage`, whose denominator is the artifact's declared class,
whole, so **an engine cannot improve a score by testifying less**. The measured
proof of (2) is the blanket abstainer: `groundedness` `n/a`, `coverage` 0.

### 3.3 Pricing, per `R5` clause 4 — and what is DISCLAIMED, with reasons

`R5` clause 4: *an unpriced item is not a saving; it is a margin that has already
been spent.* Stage A prices what it can and disclaims the rest **by name**.

* **Priced.** The artifact's own state costs: 5 310 of 5 313 cells at the
  declared cap, a margin of **3 cells**, with the interval table the dominant
  term exactly as at Layers 4 and 5.
* **Disclaimed — operational bookkeeping for a Layer-8 engine.** No cells are
  reserved here for a self-model, because `BOUNDARY-HIGH.md §5.2` rules that
  **`query` is pure, so a self-description cannot record that it was asked**, and
  every quantity the class asks about is a fold over state the engine already
  pays for. If a Stage C finds it must WRITE something to describe itself, that
  is a cost this document did not price, and the failure it would cause is named:
  the L4 shape, where 656 cells the witness never priced were found by Stage C
  inside a declared 2 563-cell margin and left five.
* **Disclaimed — a loss reserve.** None is taken, because nothing in the
  Layer-8 answer path releases content: a `query` is pure. The failure that
  disclaimer fears is `BOUNDARY.log` line 26's, and it cannot arise on a path
  that never evicts.
* **Priced in ANSWERS and not in state — the tag.** Reading (B)'s support runs
  **29 … 2 285** entries with **37 538** in total across 38 answers. `§4.1`
  budgets state and a tag is not stored, so this is a cost in bytes returned and
  not in cells held; it is recorded because a later session should not discover
  it as a surprise.

---

## §4. THE REFUSAL — calibration, and why it is constitutional

### 4.1 The measurement

| policy | answered `A` | `n_pos` | `n_neg` | `ECE` | `AUROC` |
|---|---:|---:|---:|---:|---:|
| witness (class E) | 38 | 38 | **0** | 0 | **n/a** |
| oracle (class O) | 38 | 38 | **0** | 0 | **n/a** |
| flatterer | 74 | 39 | 35 | 473 | **500** |
| shallow describer | 29 | 8 | 21 | 724 | **500** |
| blanket abstainer | 0 | 0 | 0 | n/a | n/a |
| `make_engine(7)` | 0 | 0 | 0 | n/a | n/a |

The flatterer's `AUROC` is **500 exactly**, and the reason is `humility/l6`'s own
argument recurring one layer up: a constant confidence ties every
correct×incorrect pair and `§3.4` counts a tie as a half.

### 4.2 Why the artifact cannot fix it

`R7` clause 3(b) requires the domain guarantee to be a **theorem the artifact
carries**, holding *against an arbitrary engine*. Here it holds only against a
**bad** engine, and the argument is three sentences of ratified law:

1. `§5 L8`'s subject is the engine's own state, so for every declared question
   the engine can compute whether its state determines the answer — it is the
   same fold either way.
2. `§7.3` guarantees that an unanswerable-from-state query may be abstained on,
   and the abstention is scored rather than thrown.
3. `§3.0` pays that abstention **100** against **0** for a wrong answer.

So a correct describer never answers where it would be wrong, `n_neg = 0`, and
the negative class exists only for a policy `groundedness` already
disqualifies. **This is not a shortage of forcing; it is a surplus of
self-knowledge**, and it is why `corpora/l6batteryb`'s withheld coin has no
Layer-8 analogue: the coin can be withheld from a reader, and a self-description
has nothing to read but itself.

### 4.3 What this does NOT say

* It does not say `ECE` is unmeasurable. `ECE` over `§3.4`'s own denominator
  (`R8` clause 6) is **0** on the witness, exactly and by arithmetic, and 473 on
  the flatterer. It measures something; what it does not do is **discriminate**,
  which is precisely what `R8` clause 6 already recorded of `ECE ≤ 40` at Layer 7
  — *a floor against incoherence, not a discriminator* — and `R2` obligation 2
  does not rest on it here either.
* It does not close `README-l7 §4`'s `ECE` residual. That section says what would
  close it — *an artifact on which the composed answer can be **wrong*** — and
  this session's finding is that at Layer 8 the corresponding artifact **cannot
  exist**, which is a stronger statement about Layer 8 and no statement at all
  about Layer 7. `BOUNDARY-HIGH.md §2.2` inherits the residual as raw material
  and closes nothing, and neither does this.
* It does not propose amending `§3.4`, `§3.0` or `§7.3`. `CLAUDE.md §5` is the
  procedure for a rule that seems wrong, and none of these does.

---

## §5. THE PREDICTIONS, SCORED — misses included

`BOUNDARY-HIGH.md §6.1` asks a later session to score its two named stop points
*"the way the Layer-5, Layer-6 and Layer-7 Stage-A sessions scored theirs, misses
included."*

**Prediction 1 — the sixth substrate kill: `§3`.** *A question forced to come
from a fold may also be trivially answerable from a field.* **PARTIAL HIT, and it
lands in a place the prediction did not name.** Measured against a bench of eight
**named** single-field readers, in the shape `l7compose`'s bench of six labellers
took: the bench reaches **9 of the 38** determined questions and **29 are
fold-only**. Four of the nine are the artifact's own declared controls. The other
five are the finding — and each is field-answerable for a reason that is a
property of the **engine** and not of the bytes: `reachable(attr) ==
counts["attr"]` exactly because this engine at this cap lost no assertion;
`lost_kind("note") == forgetting.count` exactly because every loss was a note. **An
artifact cannot declare that**, so `§3`'s fourth constraint — *its class must
contain questions no field carries* — **cannot be discharged by an artifact
alone**. It is discharged only as measured against a declared substrate, which is
the same structure as §4's refusal reached by a second route.

Scored as a policy rather than a note: the **shallow describer**, which dispatches
each question to the field reader shaped for it, attains `coverage` **108** and
capability **8** against the witness's **514** and **38**. The class survives, and
it survives by a margin that is now a number.

**Prediction 2 — the sizing constraint: `§5.4`.** *A Layer-8 gate binds only on
an artifact whose hard class is a large enough share of its answerable core that
blanket abstention breaks the fidelity clause.* **SATISFIED, and the prediction's
reasoning is a MISS.** The hard class is 21 of 56 = 375‰, far above `1/18`, and
blanket abstention scores `F_core` **100** against the witness's **711**. But
`§5.4` expected the `1/18` ladder to recur: it does not, because **the hedger and
the correct describer are the same policy on the hard class**. The witness
abstains on 18 of 56 and `F = 1000 − 900·(18/56) = 710.71…`, which `§3.5` rounds
to the measured **711**. So no `F ≥ 950` clause can bind at Layer 8 — not because
a hedger escapes it, but because **the witness itself cannot clear it**, and a
fidelity clause above 711 would forbid what honesty requires.

**Prediction 3 — `§2.4` clause 2's aside.** *`make_engine(N−1)` measured, which
at Layers 6 and 7 turned out to BE the strongest baseline.* **MISS.** At Layer 8
`make_engine(7)` is the **weakest** — it ties the blanket abstainer on every
quantity — because `§7.1` fixes three operations and Layer 8 adds none, so
*the verb is not the vocabulary* and a capped engine meets Layer 8's own tasks
with a `query` it does not support. The strongest capability-free baseline is the
**flatterer**, which is a policy and not an engine, and no `§7.4` construction
produces it. `BOUNDARY-HIGH.md §4.1`'s humility construction is thereby confirmed
in its own terms and its ceiling is **loose**, in exactly the sense `R8` clause 7
ruled Layer 7's 50 to be: the capped engine measures 0 **by arithmetic** (no
`census` op, so `§7.3` abstains, so the conjunction has a zero in it), and any
ceiling above 0 is slack for a partially capable engine `§7.4` does not produce.

---

## §6. THE RESERVED SEAMS, MEASURED

`BOUNDARY-HIGH.md §5` reserved two seams *"to a ruling this document schedules
rather than to a session's discretion."* Neither is settled here. Both are
measured, and the measurements are shaped for the ruling that settles them.

### 6.1 `§5.1` — `§4.2` for support that is a fact about state

The SPEC states three candidate readings exhaustively *"so that a session cannot
choose one by implementing it"*. This session implements **(B)** for the witness
**as a measurement of what (B) costs**, and reports that (A) is equally
schema-valid, so the choice remains the ruling's.

* **(B) is lawful and complete.** The witness tags all 38 answers with
  `kind = "aggregate"` — a member of `§4.2.3`'s **closed** vocabulary, unchanged
  and unextended — and a `support` that is exactly the `t`s its fold read,
  strictly ascending, every one actually ingested (`R8` clause 5(a): ingested, not
  recoverable). The **frozen** `laws/t_provenance_schema.py` validator accepts all
  38. `tagging = 1000`. **No schema form is minted and no frozen layer is
  edited**, which is what `README-l7 §5` called *an amendment wearing a fix's
  clothes* and what the SPEC forbids.
* **Its price is measured**: support cardinality 29 … 2 285, 37 538 entries over
  38 answers. A price in answers, not in cells.
* **(A) is schema-valid too** — `{"support": [], "kind": "absent", "t_asof": …}`
  passes the same frozen validator. So the choice between (A) and (B) is **an
  argument about what `absent` MEANS** and not about what the law accepts, which
  is exactly the shape `§5.1` reserved.
* **(C) is priced without being taken**: a describer that abstained on the whole
  class rather than tag it is the blanket abstainer — `coverage` 0, capability 0.
  The SPEC's *"narrower is a finding"* would, here, be a narrowing to nothing.

**What the ruling still owns**: which of (A), (B), (C) binds. This session's
measurement is that (B) is available at no cost in law and a stated cost in
answer size, which is a fact the ruling did not have.

### 6.2 `§5.3` — `promotion = 0` reaching an engine's own self-description

**Measured on the frozen Layer-7 engine, not predicted.** A self-descriptive
answer re-ingested as an ordinary payload acquires **no lineage marker**:
`own_generation` is `False`, `lineage_of(t)` is `None`, and the ledger stays
empty. The cause is in ratified law rather than in an oversight — `R8` clause 4
puts the marker in engine state keyed by `t`, and the signature that writes it is
`COMPOSITION_FORM`'s, which a census answer does not match.

So **the frozen machinery would call a re-ingested self-description an
observation.** That is `§5 L9`'s capital crime committed against itself at the
one layer whose subject is what the engine knows about itself, and it is exactly
the seam the SPEC named. Nothing is fixed here: `§9.2` forbids editing the frozen
layer, and the question — *is a self-description `generated` for promotion
purposes?* — is reserved to this Stage A's ruling. What is added is that the
answer is not free: whichever way the ruling goes, a Layer-8 engine must extend
the marking, and `BOUNDARY-HIGH.md §5.3`'s constraint on clause shape holds — **a
Layer-8 clause may not cite novelty in `§5 L7`'s byte-comparison-against-the-store
form**, because a correct self-description that restated a stored payload would be
scored un-novel for being right.

---

## §7. WHAT THIS DOCUMENT DOES NOT DO

- It does **not** bind a gate, declare a gate constant, or add a row to
  `trials/laws/t_rulings.py`'s registry. Not one module-level `GATE_*` /
  `CEILING_*` name exists under `trials/ascension/l8/` or `trials/ops/l8/`, and a
  trial in this directory asserts that.
- It does **not** append its own ruling. `RULING-R9-DRAFT.md` waits.
- It does **not** write a Layer-8 engine, adapter, humility trial, inheritance
  trial or strain. `R2`'s standing step orders all of them after the ruling, and
  `BOUNDARY-HIGH.md §6.1` puts them at Stages B–D.
- It does **not** settle either reserved seam, does **not** mint a fifth
  impossibility kind (`§4.2` there reserves that to Stage B, *from measurement*),
  and does **not** touch `real-sessions/v2`, whose freeze stays STOPPED.
- It does **not** move any score, threshold, ceiling or corpus binding at Layers
  1 through 7.

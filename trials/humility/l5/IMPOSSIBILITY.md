# IMPOSSIBILITY.md — why `make_engine(layer_cap = 4)` cannot reach the Layer-5 ceiling

> **THE CORPUS IS NOW BOUND — 2026-07-31, `BOUNDARY-RULINGS.md R6` clause 1
> (`[L4] [RULING]`).** The boxed note below says the corpus is *pending*; it was
> true when written and is answered here rather than rewritten. `R6` clause 1
> binds `corpora/l5stream` to the Layer-5 **humility ceiling and the ascension
> gate together, in one clause**, for the reason that note gives — a ceiling
> measured on one corpus beside a gate cleared on another would discriminate
> nothing. Nothing else in this document changes: no number moved, the argument
> below never depended on which corpus it was, and both measured conditions of §3
> (945 of 945 intentions held in budget, 30 of 945 at the ratified cap,
> `trigger-recall` **0** either way) are carried verbatim into R6's Stage-B
> evidence, because R5 clause 4 is why quoting only the flattering one would have
> been an omission.

`BOUNDARY.md §6` requires every humility trial to ship a **structural** argument —
not an empirical observation — for why the capped engine cannot exceed its
declared ceiling. The ceiling is `§5 L5`'s:

```
capped trigger-recall ≤ 50
```

and the measurement, on `corpora/l5stream` at the declared Layer-5 cap, is **0**.

> **The corpus is PENDING.** No ruling binds `corpora/l5stream` to either side of
> the Layer-5 gate. `R5` settled a *reading* of R2's obligations and expressly
> declined the binding (`ATTAINABILITY.md §6` question 4 is untaken).
> `trials/ascension/l5/RULING-R6-DRAFT.md` clause 1 asks a human for the
> **ascension and humility bindings together**, because a ceiling measured on one
> corpus and a gate bound on another would discriminate nothing. Until that entry
> is frozen, what stands here is a measurement on a named corpus — and an argument
> that does not depend on which corpus it is.

---

## §1. The ceiling is not approached from below. The numerator is empty.

`trigger-recall` is

```
|{ i : i fired exactly once, at its own satisfaction point }|  /  |{ i : sigma(i) ≠ none }|
```

The denominator is a property of the frozen stream: 765 fireable intentions,
computed with no engine in the loop (`_l5tasks`, `ops/l5/t_l5stream.py`). The
numerator counts **firings**, and firing is not a behaviour `make_engine(4)`
has at all.

`README-l4 §4` stated this before any Layer-5 trial existed, and stated it as a
value rather than as a tendency:

> *"a deferred-intent task scores **0** here, **not near 0** … `trigger-recall` is
> the fraction of intentions whose condition a later write satisfies and which
> fired; with no intention store, nothing is ever pending, so nothing can fire —
> the capped engine's numerator is empty by construction, not by difficulty."*

A ceiling of 50 is therefore **loose**, and it is loose for a structural reason
rather than through a corpus's kindness. Nothing is being asked to be difficult
here: there is no mechanism whose failure rate the 50 bounds.

## §2. What prospection requires, and which piece the capped engine lacks

Prospection is the first capability in the ladder that is not a fold over the
past. Stated minimally, it needs three things:

1. **a stored condition** — an intention, held in state after the write that
   created it, still there when a later write arrives;
2. **an evaluator** — machinery that takes an *arriving* event and a *stored*
   condition and decides satisfaction, on the write path, before the state
   transition completes;
3. **an emission with a place in logical time** — a fired event that consumes a
   `t` of its own (`§1.3`; `trials/ascension/l5/STAGE-B.md §1`), so that what
   fired can be read back and scored.

The capped engine has (1) and lacks (2) entirely, which makes (3) unreachable.
This is not a lossiness claim. `§5.1 L5` puts the boundary in the constitution's
own words — *"Consolidation summarizes the past and has no construct that watches
future writes"* — and `README-l4 §4` gives it in the engine's own terms:

> *"Layer 4 has **no construct that watches future writes**. There is no `intend`,
> no condition, no trigger, no pending set; `write` is a fold plus an eviction and
> consults nothing but the arriving payload and the current state. Every schema
> this layer maintains is a fold over the **past** — an interval closed at a `t`
> already assigned, a count of things already seen."*

Every branch of the Layer-4 write path is a function of the arriving payload and
the derived view. There is no branch that reads a *previously stored payload* and
asks a question of the arriving one. Adding one is not a tuning of Layer 4; it is
Layer 5.

**The `t` argument makes this checkable rather than merely arguable.** A firing is
an event and consumes exactly one logical `t`, and nothing else in a replay of
this stream consumes one. So over a 20 000-event caller stream, an engine that
fired anything at all ends with `next_t > 20 000`. The capped engine ends at
exactly 20 000 —
`t_prospection.py::trial_the_capped_engines_own_clock_proves_it_fired_nothing`.
An engine cannot hide a firing from its own clock, so *"it did not fire"* is a
fact read off `§1.3` and not a score anyone had to trust.

## §3. Recorded, never binding — and, under pressure, not even recorded

`autopsy/GAPMAP.md §2`'s engine thesis is that every system autopsied *"writes
the metadata that would make it correct and then never reads it where it counts"*.
At Layer 5 that stops being a critique of other people's systems and becomes the
**definition** of the capped engine's incapacity: an `intend` payload is fuel like
any other (`§1.1`; `ATTAINABILITY.md`'s Reading 1), so the capped engine ingests
it, stores it, and answers `read(t)` with it — and never once reads it as a
*condition*.

**The first draft of this section said exactly that, and its own mandatory
measurement refuted it.** The corrected form is sharper, and both halves are
measured (`t_prospection.py::trial_the_intention_is_recorded_and_never_binding_and_under_pressure_not_even_recorded`):

| condition | intentions returned byte-exact by `read(t)` | `trigger-recall` |
|---|---|---|
| **in budget** (4× the raw episodic footprint — nothing forces a drop) | **945 of 945** | **0** |
| **at the ratified Layer-5 cap** (`raw_cells // 4`) | **30 of 945** | **0** |

* In budget the thesis holds in its clean form: every intention is retained
  perfectly, and not one is ever binding.
* At the pressure the gate is stated at, the capped engine does not even
  **record** the thing it would fail to read. An `intend` payload has **no
  Layer-4 facet** — `corpora/l5stream/grammar.md` declares it irreducible, beside
  `note` — its condition AST is expensive, and the inherited Layer-3 forgetting
  law releases it like any other irreducible episode.

The two incapacities are independent and neither rescues the other. A Layer-4
engine handed a larger budget records every intention and still fires nothing; a
Layer-4 engine at the Layer-5 cap loses most of them as well. `trigger-recall` is
0 either way, which is why the ceiling does not depend on which condition is
quoted — and why quoting only the flattering one would have been the kind of
omission `R5 clause 4` was written about.

## §4. The pigeonhole does not apply here, and saying so is the honest part

`humility/l4/IMPOSSIBILITY.md §3` argues an information-theoretic impossibility:
thousands of distinct evicted payloads map into an aggregated forgetting record of
at most 35 integer cells, so no injective map exists and the answers are
unreachable **in principle**.

**That argument is not available at Layer 5 and is not borrowed.** The capped
engine's failure is not that the information is gone — in budget it holds every
intention byte-exact and still scores 0. The failure is that it has no *operation*
that consults a stored condition on the write path. It is an absence of
machinery, not an absence of information, and those are different arguments with
different strengths. Stating which one applies is what keeps the §6 obligation
from degenerating into a template.

The two are related in exactly one place, and it is recorded rather than
smuggled: §3's second row shows the Layer-3 forgetting law removing most of the
intentions under pressure, so at the gate's own cap the information *is* also
partly gone. That is a second, weaker reason for the same 0 — weaker because a
larger budget would remove it and the first reason would still stand alone.

## §5. What would falsify this argument

Stated so the argument is refutable rather than decorative. The ceiling claim
fails if any of these becomes true:

* a `make_engine(4)` run ends with `next_t > |caller stream|` on an
  intention-free-of-firings replay — the capped engine emitted an event, so it
  has an emission path;
* `trigger-recall > 0` for the capped engine on any corpus — one firing is one
  more than a construct-free engine can produce;
* the corpus's fireable set becomes empty, which would make the denominator 0 and
  the measurement vacuous rather than structural (`ops/l5/t_l5stream.py` asserts
  765 fireable, and `ATTAINABILITY.md §5` records what each named policy reaches).

## §6. Where this is enforced

* `trials/humility/l5/t_prospection.py` — the ceiling against `make_engine(4)` on
  the whole 20 000-event stream, the clock argument, the two-condition
  measurement of §3, the §7.3 total-abstention check, and the Stage-C
  confirmation against the Layer-5 engine *capped to 4* (§7.4), which skips until
  that engine exists.
* `trials/ascension/l5/t_attainability.py::trial_the_humility_ceiling_is_not_breached_and_the_reason_is_structural`
  — the same 0, from the arithmetic side, engine-free, since Stage A.
* `trials/laws/t_rulings.py` — `CEILING_TRIGGER_RECALL = 50` bound to its `§5 L5`
  clause and to `R5`.

  > **Note added 2026-07-31 (`[L4] [RULING]`).** It now carries `R6` beside them:
  > `R5` for the reading under which a baseline tying a minimizing clause does not
  > void a gate, `R6` clause 1 for the substrate this ceiling is measured on.

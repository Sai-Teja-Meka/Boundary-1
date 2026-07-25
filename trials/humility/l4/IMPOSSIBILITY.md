# IMPOSSIBILITY.md — Layer 4 (Consolidation) humility

**Written at Stage B**, before `core/layers/l4_consolidation.py` exists, in the
order `BOUNDARY-RULINGS.md R2` fixes: attainability arithmetic → trials →
engine. `BOUNDARY.md §6` requires every humility trial to ship a **structural**
argument — *"not an empirical observation"* — for why the capped engine cannot
exceed the ceiling. This layer's argument has two halves, and the second is what
makes it structural.

## The claim

On Layer 4's own battery (`_l4tasks` Q1–Q4, shared verbatim with the ascension
trial) at **footprint ≤ 250‰** of the raw episodic footprint, the capped engine
`make_engine(layer_cap = 3)` — Forgetting, which drops but does not derive —
scores **reconstruction F ≤ 400** (§5 L4, bound to `corpora/l4stream` by
`BOUNDARY-RULINGS.md R4`). Genuine Layer-4 consolidation must clear **F ≥ 900**
at **C ≥ 850**; the gap is the capability.

Measured, the capped engine reaches **F = 302 and C = 0**. The ceiling is
respected with 98‰ to spare on the measure that binds, and the coverage battery
— the whole semantic half of the layer — is not answered at all.

---

## §1. The behavioral argument — §5.1 L4's own defense

`§5.1 L4` defends the ceiling in one sentence:

> *"Dropping is not deriving — a forget-only engine squeezed to a quarter of the
> bytes has simply lost three-quarters of its episodes and cannot reconstruct
> what it deleted."*

That is an arithmetic claim, and it is exact:

1. **The budget law forces the squeeze.** R4 clause 2 rules `footprint ≤ 250`
   to be 250‰ of the raw episodic footprint, so the Layer-4 cap is
   `raw_cells // 4` — **43 300 cells** on `l4stream`'s 173 200. From Layer 1 the
   budget law (§4.1) binds absolutely, and at `layer_cap = 3` the only lawful
   response to a full budget is **eviction**: the engine drops, because deriving
   is the capability it does not have.

2. **A retained item costs `event_cost + 1`.** The event plus its single handle
   posting (`core/layers/README-l3.md §0.5`) — 8 cells for a `spawn`, `move` or
   `note`, 10 for an `attr` or `link`. Retaining the **cheapest** items first
   maximizes the *count*, and no importance ordering can beat cheapest-first on
   count. That bound holds **5 010 of 20 000** episodes — 250‰, three-quarters
   lost, exactly as defended — and credits an exact reconstruction for every one
   of them, for `F ≤ 325`.

3. **A real ordering does worse, because it keeps a costlier mix.** The measured
   engine ranks by importance, not by price, so it retains **4 484** episodes
   (224‰) and scores **F = 302**.

4. **Only derivation closes the gap.** `F ≥ 900` is `8/9` of *all* events
   reconstructed exactly (`ATTAINABILITY.md §2`, and R4 clause 4 keeps it on the
   literal §3.0 table). At a quarter of the footprint no retain-or-drop policy
   can hold 8/9 of the episodes — 17 778 events would cost at least 142 224
   cells against a 43 300 cap, **3.3× the whole budget**. The only way to answer
   for an event you do not hold is to have **derived a schema that regenerates
   it**, which is Layer 4. ∎

This half is sound, and it is the half `§5.1` states. On its own it would still
be an argument about *cost*: it says a forget-only engine cannot **afford** the
episodes. The next section says something stronger and different — that even
with the affordability question set aside, the information is **not there**.

---

## §2. The coverage half — C = 0, and why that is structural too

The Q1–Q3 battery asks for current values, as-of values, action-count profiles
and global counts. A forget-only engine has no current-value table, no interval,
no fold: every one of those queries is a capability it does not have, so it
**abstains** on all 18 993 of them (§7.3 — capability absence surfaces as a
score, never an exception) and scores `C = 0` against the ascension gate's 850.

This is not a measurement artifact of asking an old engine new questions. It is
the point of the battery: Q3's counts are folds over the **whole stream**,
including its evicted three-quarters, and Q2 asks what was in force at a `t` the
engine no longer holds. An engine that answered them from a quarter of the
episodes would be answering from evidence it does not have — which is
fabrication, priced at 0 by §3.0 exactly as a wrong recall is. The capped engine
does not do that: `fabricated = 0` at every scale, on every probe.

---

## §3. The information-theoretic argument — the pigeonhole, in its formal debut

The behavioral argument bounds what the capped engine can **afford**. This one
bounds what its state can **contain**, and it is why the ceiling is structural
rather than empirical: no cleverer forget-only engine, at any budget arithmetic,
can do better.

### The witness

`trials/strain/l3/t_forgetting_strain.py::trial_two_streams_differing_only_in_what_was_forgotten_are_indistinguishable`
— **frozen at Layer 3**, and cited here rather than re-run — exhibits two
streams that differ *only* in the content of an evicted item (same grammar
weight, same handle, same arrival time) and produce **byte-identical
snapshots**. Not a hash, not a length, not a field of the dropped payload
survives anywhere in Layer-3 state.

### The counting

What Layer-3 state records about eviction is the **aggregated forgetting
record** (`README-l3 §0.3`): per logical-`t` range, a count and a summed mass,
in at most `3 + 2 × 16 = 35` integer cells, coarsened by doubling **forever**.
Measured on `l4stream` at footprint 250‰, the capped engine drops thousands of
distinct payloads into **27–35 cells** — 15 516 of them on the whole stream.

So consider the map from *evicted content* to *state*. Its domain is the set of
distinct payload sequences the corpus grammar admits over the evicted
positions — astronomically larger than 35 integers can index — and the witness
shows two members of that domain landing on the **same** state. By the
pigeonhole principle there is **no injective map from the evicted set into
Layer-3 state**, and therefore:

* **Q4 over evicted events is structurally unanswerable.** Two streams with
  byte-identical states must return byte-identical answers (§2.3, determinism is
  a law). They disagree about what was at `t`. So for at least one of them any
  answer is wrong, and the only behaviour that is correct on both is
  abstention — which scores 100, not 1000. No engine capped below Layer 4 can
  reconstruct an evicted event, however it is built.
* **Q1 and Q2 over evicted assertions are unwitnessable.** The current value of
  a pair whose latest assertion was evicted, and the value in force at an
  evicted `t`, are functions of content that left no trace. The same two streams
  disagree about them and the same state must answer both.
* **Q3 is worse, not better.** A profile or a global count is a fold over the
  whole stream. The aggregated record carries a count and a mass **per `t`
  range**, never per kind and never per entity, so it cannot even contribute a
  partial fold. It says *how much* was forgotten and never *what*.

**What the record does buy, stated so the argument is not overclaimed.** The
capped engine can distinguish *"I evicted 412 items worth 1 038 of mass in the
range containing your query"* from *"I have never evicted anything near your
query"* — a Layer-6 calibration signal, and the reason it abstains **honestly**
rather than inventing. That is exactly why the ceiling is 400 and not 0: an
engine that reconstructs a quarter of the stream and abstains on the rest is
doing the best a forget-only engine can do, and §3.0 pays 100 for each honest
abstention. ∎

### Why the seam was laid one layer down

`core/layers/README-l3.md §4` wrote this seam as the boundary of Layer 3 —
*"eviction drops what consolidation would have abstracted"* — and directed that
this document be written against that witness. It is. The one thing that
changed since is the unit: R4 clause 2's erratum replaced §4's `250 // 12 = 20`
items with 250‰ of the footprint, and the seam is **sharper** under the ratified
reading, not weaker — 4 484 retained episodes still leave 15 516 that no
Layer-3 state can reconstruct.

---

## §4. What was measured, where, and what it cost

Everything below is measured by `t_consolidation.py` in this directory, from the
capped engine's own answers through the generic interface (§7). **Measured,
never typed:** the ceiling assertion in the trial is the ratified `≤ 400` and
nothing else — the numbers here are what the run produces, and if they drift the
document is wrong and the suite still says so, because every one of them is
re-derived on every run.

### In suite: the declared prefix ladder

`l4stream[:n]` at `budget_cap = raw_cells(n) // 4`, i.e. footprint 250‰ at every
scale:

| n | cap (cells) | retained | retained‰ | C | **F** | F_corruption | footprint | cheapest-first bound |
|---|---|---|---|---|---|---|---|---|
| 1 000 | 2 082 | 213 | 213 | **0** | **292** | 1000 | 249‰ | 334 |
| 2 000 | 4 245 | 437 | 219 | **0** | **297** | 1000 | 250‰ | 337 |
| 4 000 | 8 580 | 891 | 223 | **0** | **300** | 1000 | 250‰ | 331 |

`B = 1000` at every scale (the cap held after every write), `wrong = 0`,
`fabricated = 0`.

### Out of suite, once: the whole stream

| n | cap | retained | retained‰ | C | **F** | footprint | wall time |
|---|---|---|---|---|---|---|---|
| 20 000 | 43 300 | 4 484 | 224 | **0** | **302** | 250‰ (43 299 cells) | **663 s** |

Reproduce with:

```
python3 -c "
import sys; sys.path.insert(0,'trials'); sys.path.insert(0,'.')
import _l4tasks, _l4score
from adapters import l3
b = _l4tasks.corpus('l4stream')
st, rep = _l4score.replay(l3, lambda cap: l3.make_engine(3, cap), b)
print(_l4score.score(l3, st, b), rep)"
```

### Why the suite carries the ladder and not the whole stream

The capped engine is the **frozen** Layer-3 engine, whose eviction path is
`O(retained)` per write — a consequence of `README-l3 §0.3`, where per-eviction
records were shown to be arithmetically unavailable and the forgetting record
had to be aggregated instead. At footprint 250‰ on 20 000 events that is ~15 500
evictions against ~4 500 retained items, and the replay costs **663 s** against
a **48 s** whole suite. Carrying it would multiply the cost of every future
session's suite by roughly fifteen, to move a measurement from 300 to 302 under
a ceiling of 400.

The ladder is not a weaker substitute, for three reasons, and the first is
asserted as a trial rather than claimed here:

1. **The ceiling is scale-free** (`trial_the_capped_ceiling_is_scale_free`).
   R4 clause 2 makes `250` a **ratio**, so the capped engine is squeezed to a
   quarter of whatever it is shown at every scale. The measurements cluster
   inside 10‰ across a doubling ladder — 292, 297, 300 — and the whole-stream
   run lands at 302, just past the top of the ladder, exactly where the ladder
   points. A prefix of a frozen corpus is that corpus's own bytes: no new
   corpus, no byte-match question, nothing generated.
2. **The whole-stream bound runs on every suite anyway, engine-free.** The
   cheapest-items-first ceiling on the *whole* stream is
   `_l4tasks.baseline_capped_l3` — the fixture R4 clause 1 tabulates at
   **200 / 325** — and `trial_the_whole_stream_bound_is_stage_as_and_lies_under_the_ceiling`
   asserts both that it lies under the ratified 400 and that the instrument used
   at prefix scale agrees with it on the whole stream. So the whole-stream claim
   is machine-checked every run; what the ladder adds is that a *real engine*
   lands well under a bound that already holds.
3. **The pigeonhole is scale-free by construction.** §3 quantifies over
   content, not over stream length. No measurement at any scale could rescue an
   engine whose state provably does not contain the answer — which is precisely
   what §6 means by asking for a structural argument rather than an empirical
   one.

---

## §5. Enforcement

- `trials/humility/l4/t_consolidation.py` — the capped runs at every declared
  scale (ceiling, footprint, `B`, `C = 0`, no fabrication, no corruption), the
  scale-invariance claim, the measured pigeonhole (evicted count against the
  record's ≤ 35 cells), and the engine-gated confirmation against the Layer-4
  engine capped to 3, which must be identically incapable (§7.4).
- `trials/strain/l3/t_forgetting_strain.py` — the byte-identical-snapshot
  witness §3 rests on. **Frozen at Layer 3 and cited, never duplicated.**
- `trials/ascension/l4/t_attainability.py::trial_the_capped_engine_ceiling_is_honest_on_l4stream`
  — the same ceiling from the arithmetic side, asserting it is neither breached
  by the corpus (325 ≤ 400) nor vacuous (325 > the 100 abstention floor).
- `trials/laws/t_rulings.py` — `CEILING_RECONSTRUCTION_F = 400` and
  `GATE_FOOTPRINT = 250` in this directory carry their §5 L4 clauses and R4 in
  the gate registry; neither can exist here without a recorded authority.
- The byte-match law (§8.3) freezes `corpora/l4stream`, so every scale on the
  ladder is a prefix of bytes that cannot drift.

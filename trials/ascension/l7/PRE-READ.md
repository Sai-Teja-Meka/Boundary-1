# PRE-READ.md — Layer 7 (Generation), read before Stage A exists

`[L6] [PULSE]`, 2026-08-02. **This is not an `ATTAINABILITY.md`.** It binds
nothing, rules nothing, names no corpus, and applies no gate to any engine.
`core/layers/l7_generation.py` does not exist, no Layer-7 constant appears in any
trial, and `laws/t_rulings.py` is untouched by this document — a gate constant is
what that registry governs, and this file declares none. The directory it sits in
holds no `t_*.py`, so `run.py` walks it and finds nothing to run.

`BOUNDARY-RULINGS.md R2` fixes the standing order of an `ASCEND`: **attainability
arithmetic → trials → engine**, with the arithmetic recorded and machine-checked
*before* the gate is treated as binding. A `PULSE` cannot discharge R2 and does
not try to. What it can do is what the `[L4] [PULSE]` (`BOUNDARY.log` line 24)
did for Layer 5 and the `[L5] [PULSE]` (line 34, `../l6/PRE-READ.md`) did for
Layer 6 — read the ratified clauses one layer ahead, say which of R2's
obligations the existing rulings already discharge and which they do not, and
**predict the shape of the collision** so the Stage-A session meets it with its
arithmetic ready instead of discovering it.

Both prior pre-reads were scored by the sessions that met them, and both records
are worth as much for their misses as for their hits: Layer 5's collision was
confirmed with one half unpredicted (line 28), and Layer 6's was confirmed with
**three** halves wrong — obligation 2 did *not* rest entirely on AUROC, the
flagged humility worry was the wrong worry, and the corpus candidacy verdict
("murk plus a battery, no new corpus obviously required") was overturned twice,
first by a new artifact and then by that artifact's own demotion (lines 36–38).
This document is written expecting to be scored the same way.

Every figure below is exact `Fraction` arithmetic over `§3`'s own definitions.
Where a later `ATTAINABILITY.md` computes one of these quantities, **that file is
the enforced value** and this one is prose (`R6` clause 3).

---

## §1. The clause structure of `§5 L7`, read against R2, R5 and R7

`§5 L7`'s gate is **`validity = 1000`, `novelty = 1000`, `tagging = 1000`,
`self-pollution promotion = 0` (three deep), `F ≥ 950`, `B = 1000`, `ECE ≤ 40`**,
with a humility ceiling of **capped `(novel ∧ valid ∧ tagged) ≤ 50`**.

Seven clauses — more than any layer in the ladder — and sorting them into `R5`'s
kinds is the first thing Stage A owes:

| clause | kind | direction | ceiling | R2 obligation 1 discharged by |
|---|---|---|---|---|
| `validity = 1000` | **identity** | maximizing | 1000 | exhibited attainment (`R5` clause 1) |
| `novelty = 1000` | **identity** | maximizing | 1000 | exhibited attainment (`R5` clause 1) |
| `tagging = 1000` | **identity** | maximizing | 1000 | exhibited attainment (`R5` clause 1) |
| `promotion = 0` three deep | **identity** | **minimizing** | 0 | exhibited attainment (`R5` clauses 1 **and** 2) |
| `F ≥ 950` | graded | maximizing | 1000 | the ordinary method |
| `B = 1000` | **identity** | — | 1000 | exhibited attainment (`R5` clause 1, as since Layer 1) |
| `ECE ≤ 40` | graded | **minimizing** | 0 | the ordinary method, direction-aware (`R5` clause 2) |
| capped `(novel ∧ valid ∧ tagged) ≤ 50` | ceiling | minimizing | — | measured, §1.3 |

**Layer 7 needs no `R5`-shaped ruling of its own, and neither did Layer 6.** `R5`
clause 1 governs identities and clause 2 governs minimizing clauses, both
forward-binding in their own text; clause 3 (declare the ceiling's policy class)
and clause 4 (price bookkeeping and loss reserves, or disclaim them with reasons)
apply unchanged. Five of the seven clauses are identities, which is the highest
count in the ladder — Layer 5 had four of six — so `R5` clause 1's *exhibited
attainment* is the dominant instrument at this layer and an argued ceiling will
almost never be the right form (`R4` clause 5).

**That is not where Layer 7 gets hard**, and saying so is the same half-value the
Layer-6 pre-read got from saying it about clause shape. Layer 7 gets hard at the
**denominators**, and §1.2 is where that starts.

### 1.1 Where the discrimination obligations land

`R2` obligation 1 (a gate strictly below its oracle ceiling, or — per `R5`
clause 1 — an identity attained by an exhibited witness) is discharged clause by
clause the ordinary way, provided a witness can be built. Nothing structural
blocks it: unlike Layer 5's identities, which forced `R5` into existence, Layer 7
arrives with the reading already ratified.

`R2` obligation 2 — strictly better than **every named capability-free baseline**
— is where the layer's whole weight lands, and the arithmetic is unusually
lopsided. Take the obvious capability-free policy, a **retrieval-only engine**
(which *is* `make_engine(6)`, so it is measured and not merely named — the L6
precedent, where confident-always turned out to be the capped engine itself):

| clause | retrieval-only policy | does the clause discriminate? |
|---|---|---|
| `validity = 1000` | **1000** — every stored item is grammar-valid by construction | **no** — tied at the gate |
| `promotion = 0` | **0** — it generates nothing, so it promotes nothing | **no** — tied at the gate |
| `B = 1000` | **1000** — lawful | **no** — tied, as at every layer since Layer 1 |
| `ECE ≤ 40` | base-rate constant confidence scores `ECE = 0` **exactly, at every error rate** | **no** — measured at Layer 6, see §1.2 |
| `tagging = 1000` | **denominator-dependent**: `n/a` or `0` | **the whole question** — §3 |
| `F ≥ 950` | depends on the artifact's mix | partly — §4 |
| `novelty = 1000` | **0** — every value it can return is one it holds | **yes, by arithmetic** |

So: **three of the seven clauses are attained perfectly by a policy with no
capability at all**, a fourth (`ECE`) is the one clause Layer 6 *measured* to be
non-discriminating, a fifth (`tagging`) evaporates or does not depending on a
decision nobody has taken, and `R5` clause 2's conjunction reading therefore
carries the entire lower obligation — resting, when the dust settles, on
**`novelty`** and on `F`.

This is Layer 6's shape one layer on, and the parallel is exact enough to be
useful: there, obligation 2 rested on `AUROC`, failed both constants **by
arithmetic rather than by margin** (400 permille, at every error rate), and was
the one clause `§3.4` could let evaporate. Here it rests on `novelty`, fails a
retrieval-only policy by arithmetic rather than by margin (**1000** permille, the
maximum possible), and is the one clause a **self-reported denominator** could
let evaporate. The difference is the good news of this document: `AUROC`'s domain
was a property of the *engine's own accuracy*, which no artifact can fully
control; `novelty`'s denominator is a property of the *artifact*, which a Stage A
can fix by construction. **Layer 7's lower obligation is safer than Layer 6's,
conditional on one decision, and §3 is that decision.**

### 1.2 `ECE ≤ 40` is the weakest of Layer 6's three calibration clauses, alone

`§5 L6` gated `Brier ≤ 40`, `ECE ≤ 30` and `AUROC ≥ 900`. `§5 L7` keeps exactly
one of the three, and it keeps the one that was measured to discriminate against
nothing.

`ATTAINABILITY-B.md §4` and `R7`'s evidence section both record it: a **base-rate
constant** — one flat confidence equal to the corpus's own accuracy — puts every
answer in **one** ECE bin whose mean confidence *is* its accuracy, so `ECE = 0`
at every error rate, with no confidence model of any kind. At round 1 that
capability-free policy *beat* the exhibited witness on ECE; at round 2 the
witness's own bins agreed with themselves exactly and tied it at 0. Either way
the clause separated nothing, twice, on two artifacts.

Layer 7 therefore inherits, as its sole calibration clause, the clause Layer 6
proved inert — and drops both clauses that did work. A Stage A should state that
in its own text rather than let a reader assume `ECE ≤ 40` is doing what
`AUROC ≥ 900` did. It is a **floor against incoherence**, not a discriminator,
and `R2` obligation 2 must not be reported as resting on it.

One reading it *does* need, and §4.3 is where it bites: `§5.1 L7` defends the
clause with *"confidence on **generated content** stays calibrated"*, while
`§3.4` computes ECE over **the `A` answered queries**. Those are two different
denominators, and one of them can be emptied.

### 1.3 The humility ceiling is stated in a measure the ascension gate never states

Every humility ceiling in the ladder so far is stated in a quantity the same
layer's ascension gate also states: capped `cue-C` against `cue-C ≥ 900`, capped
`weighted-C` against `weighted-C ≥ 850`, capped `reconstruction F` against
`reconstruction F ≥ 900`, capped `trigger-recall` against `trigger-recall = 1000`,
capped `AUROC` against `AUROC ≥ 900`. `§6` requires exactly this: the humility
trial runs **layer `N`'s own ascension tasks** and asserts the capped engine
scores at or below the ceiling.

Layer 7 breaks the pattern. Its ceiling is stated over
**`(novel ∧ valid ∧ tagged)`** — a per-item conjunction that appears **nowhere in
the ascension gate**, which states the three conjuncts separately and each as an
identity. On the ascension side the conjunction is implied and trivial (all three
at 1000 forces the conjunction to 1000); on the humility side the conjunction is
the *only* thing measured. So Stage A must **define a measure `§5` states only
once and only on the capped side**: over which item set, with which denominator,
and answered through `§7` alone.

`core/layers/README-l6.md §4` already computed what the ceiling will read against
the engine that exists, and computed it as arithmetic rather than as a margin:

> the conjunction is **0**, not near 0 … `novelty` requires an item *provably
> never stored*, and every value this engine can return is one it holds, so the
> novel conjunct is false on every answer it has and the other two conjuncts
> cannot rescue a product with a zero in it. The ceiling of 50 is not approached
> from below by a poor generator; there is no generator.

That is a **structurally 0** ceiling, and the honest question Stage A owes is
whether it is therefore *vacuous*. The Layer-6 form of this question was settled
by exhibiting the query class that makes the ceiling bite (`K0`, the forcing
region — the capped engine measured 500 against 600, *neither breached nor
vacuous*, and `README-l5 §4`'s stated seam closed). The Layer-7 form is
different and easier to get wrong: a ceiling of 50 against a measured 0 leaves
**50 permille of unexplained headroom** and the ladder has no precedent for
reading it. Two readings are available and Stage A should take one explicitly —
that the 50 is slack for a *partially* capable engine that `§7.4` does not
produce (in which case the ceiling is loose but the measurement is real), or that
it anticipates a denominator under which a capped engine could score above 0 (in
which case the denominator is the thing to name). What it must not do is report
"0 ≤ 50, ceiling holds" and move on: that sentence is true of a ceiling that
measures nothing.

### 1.4 One clause is both a gate clause and a mandatory strain — say which owns it

`self-pollution promotion = 0` is stated twice in the constitution: in `§5 L7`'s
gate row, and in `§6`'s description of the `strain/` class, which names *"the
**mandatory Layer 7 self-pollution strain**"* as a member of that class in its own
text. No other clause in the ladder is named in two trial classes at once.

This is the ONE FIXTURE, ONE TRUTH discipline (`BOUNDARY.log` lines 22, 30, 39)
arriving as a constitutional requirement rather than as a session's good manners:
Stage A must say which instrument **owns** the number, and the other must name
the owning trial rather than re-assert it. The precedent is settled — the
ascension battery scores the gate, the strain class states the property under
conditions the gate does not reach — and §5 below is where the strain's own
demands are set out.

### 1.5 The fourth-species collision watch — the shape, and it exists

Three species of gate clause have now been named and ruled on:

1. **The identity** (`R5` clause 1) — the oracle ceiling *is* the gate, so R2's
   strict inequality is not merely unavailable but unreachable, and the obligation
   is discharged by an exhibited **attainment**.
2. **The minimizing clause** (`R5` clause 2) — "strictly above" is written for
   measures where higher is better, so it is read direction-aware and over the
   gate's **conjunction**.
3. **The clause with an empty domain** (`R7` clause 3) — `AUROC` at `n_neg = 0`,
   ruled to **disqualify** rather than excuse, on the instrument-range framing
   (*a balance reading `----` under an out-of-range load has not weighed the
   object*), grounded on the null-exemption defect `autopsy/writ` convicted WRIT
   of at `evaluator.ts:545-548`.

**A fourth species arrives at Layer 7, and it has a name: the SELF-REPORTED
DENOMINATOR.**

`validity`, `novelty` and `tagging` are ratios, and `§5` states none of their
denominators. Every prior layer's capability-specific quantity carried its
denominator with it or inherited one from `§3`: `footprint` is cells over raw
cells; `trigger-precision` and `trigger-recall` are firings over firings and over
satisfactions, both computable from frozen bytes with no engine in the loop;
`dup-fire` and `miss` are cardinalities. At Layer 7 the obvious denominator for
all three is **the set of items the engine says it generated** — and that set is
the engine's own testimony about the very thing being tested.

Follow it to its end and the failure is exact:

> An engine that generates nothing, tags nothing, and declares its generation set
> empty scores `validity = n/a`, `novelty = n/a`, `tagging = n/a` on an empty
> denominator, `promotion = 0` (nothing to promote), `B = 1000` and `ECE ≤ 40`
> (base-rate constant). If `n/a` excuses those clauses, a retrieval-only engine
> clears every evaluable clause of `§5 L7` with no capability whatsoever, and no
> Layer-7 gate can bind on any artifact.

That is round 1's `detect-and-abstain` (`BOUNDARY.log` line 36) reappearing one
layer up with a different escape hatch, and it is **WRIT's null-exemption in a
new costume**: WRIT drops a declared-absent capability from *both* numerator and
denominator (`evaluator.ts:545-548`); a self-reporting Layer-7 engine drops the
entire generation class from both. `R7` clause 3(a) rules that shape
disqualifies, and its rationale is stated in instrument-range terms that read
naturally here — but **clause 3 is stated about `AUROC`**, and a Stage A may not
quietly extend a ruling's holding past the clause it names. So the fourth species
is a genuine gap in the ruling stock, and the shape of the fix is already
visible in `R7` clause 3(b): put the burden on the **artifact**. The denominators
must be **the artifact's declared classes**, not the engine's self-report — which
is §3's arithmetic and the single most consequential decision at this layer.

---

## §2. `§4.2` as it wakes: the provenance law binds from Layer 7, forever

`§4.2` has been dormant for six layers. At Layer 7 it becomes **binding, and once
bound it can never be un-bound** — the only clause in the constitution that says
so about itself. Stage A is the last session that can decide anything about it
cheaply.

### 2.1 What the law as written demands

`§4.2.2`: every **non-abstaining** answer MUST carry a valid provenance tag; an
answer without one scores **wrong (0)**, *"regardless of whether its value is
correct."* `§4.2.3` fixes the schema, and `trials/laws/t_provenance_schema.py`
has implemented and exercised it since `[L0]`, dormant law and live validator:

* `support` — a list of integers, **strictly ascending, no duplicates,
  non-negative, each an actually-ingested event `t`**; empty **only** when
  `kind == "absent"`.
* `kind` — one of exactly **`"recall"`, `"aggregate"`, `"derive"`, `"absent"`**,
  *"and no other."*
* `t_asof` — a non-negative integer.

All four kinds are already emitted by the engine that exists (`core/engine.py`,
`l2_recall.py`, `l3_forgetting.py` and up), so the vocabulary is exercised rather
than theoretical — which matters for §2.3.

### 2.2 What the law cannot see

Three things, and each is a decision waiting for Stage A.

**(a) Recoverability.** `§4.2.3` validates a tag's **shape**. `t` is *ingested*
if it was ever assigned, which is a fact about `next_t` and nothing else. Whether
`read(t)` still **answers** — whether the event is held, regenerable, or in the
forgetting record — is a different question the validator does not ask and cannot
be made to ask without becoming a state query. This is the `[L5] [PULSE]` finding
(`BOUNDARY.log` line 34), filed at that PULSE and **measured again** at the
`[L6] [ASCEND]` and `[L6] [DOGFOOD]` sessions when the fired promise's own warrant
became forgettable: a fired intention's `intend` event at `t0` is taken back where
there is room and **booked into the forgetting record where there is not**, so a
support entry naming `t0` is schema-valid and names content the engine cannot
produce. `strain/l5::trial_a_kept_promise_is_booked_and_an_unkept_one_still_regenerates`
pins both directions today; `shell/dogfood/FIELD.md` (2026-08-02) records the
same asymmetry on this project's own store, where `iid 1`'s `intend` event comes
back tagged `recall` because there was room and `iid 2`'s comes back `derive`
because a pending entry regenerates it.

**(b) Relevance.** The schema constrains order, sign and range. It does not
constrain **whether the cited events bear on the answer at all**. A tag citing
`[0, 1, 2]` for an answer derived from `[91, 92]` is valid. Nothing in `§4.2`
scores support for being *the* support, so an engine can be perfectly compliant
and perfectly uninformative. This is worth naming because it is precisely
`autopsy/GAPMAP.md §2`'s **recorded but never binding** thesis — the one this
project convicted four engines and every evaluator of — available as a defect of
*our own* law, and a Stage A that does not name it will have shipped it.

**(c) Lineage.** `§4.2.3`'s vocabulary has **no `"generated"` kind**, and says
*"and no other."* `§5 L7` requires *"100% of generated items must carry the
`generated` lineage tag."* Both are ratified. They are consistent only if the
`generated` tag is **not** a provenance kind — see §5.2, where the machinery
question is settled.

Worse, and this is the sharp end of (c): under `R6` clause 2 a firing is an
event, ingested, with a `t` of its own. At Layer 7 the mandatory self-pollution
strain re-ingests the engine's own generations, which makes them **actually
ingested events with real `t`s**. A tag citing them is schema-valid.
**`§4.2` cannot distinguish support-on-observed from support-on-generated** — and
promoting generated-lineage content to observed fact is exactly what `§5 L7`'s
own `promotion = 0` clause forbids. The provenance law, as written, is blind to
the failure the layer that activates it exists to prevent.

### 2.3 What a Stage A must therefore decide or draft

Four items, in descending order of how much they bind:

1. **Recoverable or merely ingested** — the question `R7` clause 7 bequeathed in
   as many words and the `[L6] [DOGFOOD]` session deliberately **refused to arm an
   intention about**, on the ground that it must be settled at Stage A, before the
   claim a layer-condition can see (`FIELD.md`, 2026-08-02: *"this reading can
   watch for a fact and not for the moment before it"*). The refusal was correct
   and it is why this section exists here rather than in a reminder that would
   have arrived after the decision.

   **The collision is softer than line 34 feared, and Stage A should say so.** For
   the fired event specifically, the natural support has a **recoverable member**:
   the fired event lives at its own `t_fire`, which the fired ledger regenerates,
   so an engine that cites `t_fire` and not `t0` satisfies the strict reading
   without Layer 5 changing anything. The constraint lands on **which `t` the
   Layer-7 engine chooses to cite**, not on a shape Layer 5 lawfully produces. And
   there is currently **no `why did this fire` query** in `§7`'s vocabulary, so
   the case is not live today.

   **It becomes live at Layer 7 for a different reason**, and this is the part
   line 34 could not see: `generate(cue)`'s natural support is *the material it
   composed from*, which under Layer 4 can be **regenerable-but-not-stored** and
   under Layer 3 can be **gone-but-counted**. A generation composed from a
   demoted assertion cites a `t` that `read(t)` answers by `derive`; one composed
   from a shed chain cites a `t` the forgetting record can only count. So the
   question stops being about promises and becomes about generation's own
   warrant.

2. **If shape-only is the reading, say the weaker thing out loud, and measure
   it.** Provenance would then certify *that* an answer had a source and not
   *that the source can be shown*. `[L5] [PULSE]` already wrote the obligation
   that follows: *"the project should say so in its own documents before it says
   it about anyone else's."* The instrument to draft is not a new gate but a
   **reported, ungated diagnostic** — a support-recoverability rate beside the
   gated `tagging` number — in the exact shape `R3` gave `F_strict` and `R4`
   clause 4 gave `F_corruption`: the stricter number computed on every run,
   binding nothing, impossible to lose quietly.

3. **The lineage/kind reading.** Declare that `generated` is a property of the
   **item** and the four `§4.2.3` kinds are properties of the **answer's
   channel**, that the two are orthogonal, and that the closed vocabulary is
   therefore not violated by `§5 L7`'s tag. This is a reading of ratified text in
   the shape `R4` clause 2 took for `footprint ≤ 250` and `R6` clause 2 took for
   `§7.1`'s *"appends one event"* — cheap now, expensive after a battery has
   assumed one.

4. **Where the promotion check lives.** Since `§4.2`'s validator is shape-only and
   blind to lineage (§2.2(c)), `promotion = 0` cannot be enforced by the
   provenance law trial. It must be enforced by the battery and the strain,
   keyed on lineage. Say so, so that a later session does not find a green
   `laws/t_provenance_schema.py` and conclude the capital crime is covered.

---

## §3. The capital crime as gate arithmetic

`§5 L7`: *"`tagging = 1000`: 100% of generated items must carry the `generated`
lineage tag; **an untagged generation is a fabrication**."* `§3.0` prices a
fabrication at **0**. The constitution names its own capital crime, in its own
words, and this section is about what trial shape can actually enforce it.

### 3.1 The trial shape, and the one way it fails

The naive shape is a rate: *tagged generations over generations*. It fails, and
it fails in the way §1.5 names — if the denominator is the engine's own generation
set, the engine grades itself, and the engine that generates nothing scores
perfectly on an empty denominator.

The shape that works has three parts, and each is forced:

1. **The denominator is the artifact's declared class, not the engine's
   testimony.** A binding artifact declares, per query, whether its answer is
   reachable by retrieval or **only by composition**. `tagging` is then scored
   over the declared generation class, and an engine that answers a
   generation-class query without the tag has fabricated — scored 0 under `§3.0`
   *and* fatal to a `= 1000` identity, which is the constitution stating the same
   thing twice with different teeth.
2. **`novelty` is checked against the ingested set, by the harness, over frozen
   bytes.** *"Provably never-stored"* is exactly checkable: the returned item's
   canonical bytes (`§2.4`) are compared against every payload the stream carries.
   This is a fold the harness can compute with no engine in the loop, which is
   what makes `novelty = 1000` a measurement rather than a definition — the same
   discipline that made `P2` the Layer-1 `read` verb at Layer 5 and `Q4` the
   Layer-1 `read` verb at Layer 4.
3. **Both directions cost.** A generated item tagged as recall is the capital
   crime. A *recalled* item tagged as generated fails `novelty` — it was stored.
   So the instrument is a **confusion matrix over the two declared classes**, not
   a single rate, and both off-diagonals must be non-empty-able: the artifact must
   admit an engine that could get either wrong.

### 3.2 What the flagship claim requires the gate to score

`autopsy/GAPMAP.md §4` axis (b) is this project's sharpest positioning claim, and
`autopsy/writ/ANATOMY.md` confirmed it firsthand at commit `3c0900a`: WRIT
collects the answer's own `cited_sources` and **reads it with zero lines of
scoring**, probes provenance out-of-band on **5 of 77** scenarios, makes that
probe **opt-out-able** via `supports_provenance`, and — the sign **inverted** —
`checkHallucination` flags any non-empty answer restating no stored value, so a
*tagged generation is scored as a defect*. Against that, our claim is
**self-tagged recall-vs-generation provenance that is scored**: an untagged
answer scores 0 however correct.

For that claim to be *earned* rather than asserted, the Layer-7 gate must score
four things, and a Stage A that scores fewer has published the claim without the
measurement behind it:

* **That the engine distinguishes the two channels at all** — both classes
  non-empty on the ascension run **and** on the humility run (`R6` clause 1's
  one-artifact rule, and `R7` clause 3's instrument-range lesson applied to a
  different clause).
* **That the distinction is not free.** If a query's class is readable off the
  *query*, the engine can tag correctly without consulting its own store, and
  `tagging = 1000` measures nothing. The artifact must make the engine look at
  what it holds. **This is the most likely place a first Layer-7 artifact dies**
  — §6.3.
* **That the tag is read through `§7` alone.** The `generated` marker must reach
  the harness in the `Answer`, never out of engine bookkeeping — the standing
  precedent being `{"op":"fired","iid":I}` answering with a **list** because
  `dup-fire = 0` is a gate clause and an intention that fired twice must be
  visible through the query interface. WRIT's out-of-band `getProvenance` probe
  is precisely the thing not to reproduce.
* **That self-tagging is not self-grading.** §1.5, restated as a scoring rule:
  the engine supplies the tag, the **artifact** supplies the denominator.

---

## §4. `R7` clause 7's bequest: the price list, before any gate is drafted

`R7` clause 7 records the `§3.0`/`§3.4` tension *"for Layer 7's eyes"* and states
in its own text that **Layer 7 is where it bites next and it will bite harder**,
because `§4.2` gives the price list *"a third way to reach 0 that has nothing to
do with being wrong."* This section is that bequest examined — and it is examined
here, at a PULSE, **because an intention about it was correctly refused**
(`FIELD.md`, 2026-08-02; `BOUNDARY.log` line 41): a reminder that fires on
`layer ≥ 7` arrives after the Stage A it exists to inform, so the question had to
be carried by a document rather than by a promise.

### 4.1 The five ways an answer can score, at Layer 7

`§3.0` is confidence-blind: *a calibrated hedge and a confident lie are the same
number*. From Layer 7 it acquires a third zero:

| the engine's behaviour on an answerable query | `§3.0` |
|---|---|
| correct, validly tagged | **1000** |
| **abstains** | **100** |
| wrong | **0** |
| **correct but untagged or invalidly tagged** (`§4.2.2`) | **0** |
| fabricates on an unanswerable query | **0** |

**A generated answer with cited support IS a flagged guess**, and the price list
pays a flagged guess **0** and silence **100** whenever the guess misses. Read
naively as expected value, attempting generation beats silence whenever
`P(correct ∧ validly tagged) > 1/10` — a low bar, so `§3.0` alone does *not*
strongly discourage generation, which is the opposite of the Layer-6 situation
and worth stating because it is easy to assume otherwise.

**The identities are what actually govern.** `validity`, `novelty` and `tagging`
are `= 1000` clauses: they do not average. One untagged generation ends the
ascension whatever the engine's fidelity. So at Layer 7 the identity clauses do
the work `§3.0`'s averaging cannot, and the honest summary is that **the price
list rewards attempting and the gate forbids attempting badly** — which is a
coherent incentive and should be recorded as one rather than as a collision.

### 4.2 The hedger, and the `1/18` window — the same constant as Layer 6

The escape `R7` clause 7 names is the one Layer 6 measured: abstain on the hard
class, keep 100 apiece, and leave the calibration denominator behind. Price it
from the ratified numbers alone.

Let the **generation-required class** be a share `g` of an all-answerable core.
A policy that abstains on all of it and is correct elsewhere scores, under
`§3.0`,

```
F = 1000 − 900·g        so   F ≥ 950   ⟺   g ≤ 50/900 = 1/18 = 55.5‰
```

So a blanket hedger survives the fidelity clause **iff the generation class is at
most one eighteenth of the answerable core**, and dies otherwise.

**`1/18` is exactly `R7` clause 3(c)'s upper window bound** (`A < 18r`,
i.e. `r/A > 1/18`), and the recurrence is not a coincidence: the constant is
`50/900` — `§5`'s `F ≥ 950` slack over `§3.0`'s abstention price — so it recurs
at *every* layer whose fidelity clause is `≥ 950` and whose hard class is
all-answerable. Layer 6 is the precedent and `corpora/l6batteryb` sits at
`r/A = 1/11`, comfortably above it. A Layer-7 artifact must clear the same bar,
and Stage A gets the arithmetic for free from a ruling already on the books.

**What Layer 7 does *not* inherit is the lower bound.** `R7` clause 3(c)'s
`A ≥ 10r` came from Theorem 1's *forced* error — a withheld coin made every
committing reader wrong on exactly half the region, so the honest committer's own
error rate needed room under `F ≥ 950`. Layer 7 has no such theorem: a correct
generator can be right on the entire generation class, because nothing is
withheld from it. So the Layer-7 window is **one-sided** — `g > 1/18`, with no
floor — and a Stage A that copies `[10, 11.978…)` across will have imported an
arithmetic whose premise does not hold. Say why it does not, and the window is
simpler here rather than harder.

### 4.3 `ECE`'s denominator can be emptied, and the ruling stock does not reach it

`R7` clause 2 states the calibration denominator explicitly: **abstentions are
outside it**. `§5.1 L7` defends `ECE ≤ 40` as *"confidence on generated content
stays calibrated."* Put those together:

> If `ECE ≤ 40` is read over **generated answers**, then an engine that abstains
> on the whole generation class has an **empty ECE denominator**, and the clause
> reports `n/a` — the exact shape `R7` clause 3 ruled disqualifying for `AUROC`.
> But clause 3 is stated **about `AUROC`**, so at Layer 7 that reading needs a
> ruling of its own.
>
> If `ECE ≤ 40` is read over **all answered queries** (`§3.4`'s own definition,
> unmodified), the denominator is the whole answered core, cannot be emptied by
> hedging one class, and no new ruling is needed at all.

The second reading costs nothing and is what `§3.4` literally says; `§5.1 L7`'s
sentence is then a **rationale** for the clause rather than a redefinition of its
denominator — which is exactly how `§5.1 L6`'s *"the harness scores it
confident-by-default"* turned out to be read (`BOUNDARY.log` line 39: the engine
emits `{0, 1000}` through `§7.2` itself, so no convention was supplied and none
was needed). **Recommended: take the `§3.4` reading, state it, and note that the
alternative would have required an `R7`-clause-3-shaped ruling the project does
not otherwise need.** This is `R4` clause 2's lesson about `footprint ≤ 250` —
cheap to settle before a measurement, expensive after.

---

## §5. The self-pollution strain, playbook-mandated

`§6` makes it mandatory in the strain class's own text; `§5 L7` gates it at
`promotion = 0` **three deep**; `LORE.md` calls it *drinking one's own dreams
three cups deep*. It is the only trial the constitution specifies by procedure
rather than by measure, and that is what makes it awkward.

### 5.1 What it demands of corpus or battery design

**(a) Its substrate is engine output, and that is a first.** Every strain in the
suite runs over frozen corpora or over fixtures a trial builds. Three generations
of re-ingested generations are a **function of the engine under test**, so
`§8.2`/`§8.3`'s byte-match law cannot reach them: there is no seeded generator to
re-run. What *does* reach them is `§2.3` — determinism makes the three
generations byte-reproducible — and the `anchors/` class, which is the project's
existing instrument for pinning exact behaviour that has no generator.
Recommended shape: the strain computes the three generations, and an anchor pins
their canonical bytes, so the procedure is reproducible and non-drifting without
inventing a corpus doctrine `§8` does not have.

**(b) Re-ingestion is the caller's act, which is what makes it suggestibility.**
The harness submits the engine's own generation back through `ingest` as an
ordinary payload. That is `autopsy/GAPMAP.md §6`'s **suggestibility** in its
literal form — *implanted / externally-seeded memories* — and §6 of the survey
this document belongs to finds it structurally Layer 7's rather than an open gap.

**(c) Lineage must survive two existing paths, and both are load-bearing.** An
ingested generation is an ordinary event, so Layer 4 will fold it into the
interval table like any other and Layer 5 may fire on it. **An assertion derived
from a generated event must not become an observed fact**, and a firing triggered
by a generated event must not launder it. `promotion = 0` is therefore a claim
about the `l4_consolidation` derive path and the `l5_prospection` arming path as
much as about anything Layer 7 adds — which means the Layer-7 engine cannot
implement lineage as a wrapper around a new verb.

**(d) Three deep is a ladder and must be scored at each rung**, not only at the
end. Generation 1's lineage surviving into generation 3 is the claim; a strain
that only checks depth 3 cannot say where a break occurred. `ATTAINABILITY-B.md`'s
hedging ladder (`k = 0…100`, scored outside the policy interface) is the shape.

### 5.2 Does the existing `derive`/`recall` machinery carry, or must `generate` be minted?

**It carries the channel and not the lineage, and the `generate` tag must be
minted.** The distinction is worth being exact about, because both halves are
already implemented and it would be easy to assume the job is done.

| question | answered by | status today |
|---|---|---|
| *How did this answer reach me?* | `§4.2.3` `kind` ∈ `{recall, aggregate, derive, absent}` | **implemented and exercised**, all four kinds emitted |
| *What is this item?* | `§5 L7`'s `generated` lineage tag | **does not exist** |

`recall` versus `derive` already distinguishes *stored verbatim* from
*regenerated from a schema* — `strain/l4::trial_a_demoted_assertion_keeps_its_content_and_loses_its_cue`
and `strain/l5`'s two tiers assert exactly that partition today, and
`shell/dogfood`'s report prints it. But a **generated item is neither**: never
stored, and not regenerated from stored content — composed. `derive` is the
closest of the four and it is not the same claim.

So the lineage marker is orthogonal to the kind, and three placements are
available. Stage A must choose one and price it:

* **In the payload** — refused by `§1.4`: *"The engine adds nothing to an event
  but its `t`."* The engine may not stamp a field onto a payload it ingests. (The
  harness may, when it re-ingests a generation — but then the marker is the
  *harness's* testimony, which is §1.5's defect with the roles swapped.)
* **In engine state, keyed by `t`** — lawful, and the only placement that is the
  engine's own claim about its own history. It is **priceable under rule P**
  (`R4` clause 3) and it is the first Layer-7 budget item, so `R5` clause 4
  applies in full: priced by name, or disclaimed with reasons. The Layer-3
  precedent says the affordable form of a per-`t` record is an **aggregate**, and
  the Layer-4 precedent (`damaged`) says a single flag can carry *"this entity's
  history is incomplete"* honestly.
* **Derived from the provenance chain** — an item is generated-lineage iff its
  support reaches a generated root. Free, and it still needs the roots marked, so
  it reduces to the second placement rather than replacing it.

**And Layer 6 already recorded the residual this will land on**
(`README-l6.md §4`, written so *"the Layer-7 session finds it rather than
discovers it"*): a generated item has **no chain, no distinct-value count and no
set-once status**, so `confidence_for` falls through to `CERTAIN` on it —
`1000‰` on a thing the engine invented. That is *"exactly the wrong answer and is
the first thing a Layer-7 engine must replace"*, and it is what `ECE ≤ 40` will
measure first.

### 5.3 One reading Stage A owes before anything else: `generate(cue)` is a query

`§5 L7` writes `generate(cue)`, which reads like a fourth verb. `§7.1` declares
**three** operations and `§1.1` says events are the only fuel. The only reading
under which both are true is that **`generate` is a `query` op** —
`{"op": "generate", "cue": …}` — whose `Answer` carries the generated item, its
confidence and its tag.

This is the same argument in the same place that `ATTAINABILITY.md`'s Reading 1
made for `intend` at Layer 5 (*"an intention is an EVENT, not a fourth verb"*)
and that `R6` clause 2 ratified for `§7.1`'s *"appends one event"*. It is a
reading of ratified text and not an amendment, it has two precedents, and it
should be stated in Stage A's first paragraph rather than assumed by its
battery — because the alternative reading (a fourth door) would make `§7.1` false
and `INTERFACE.md` wrong, and `§7`'s *"an engine is a black box behind these
three pure functions"* is copied verbatim into the adapter contract every foreign
engine is graded through.

---

## §6. Corpus candidacy — what substrate forces generation

**Verdict: no frozen corpus can carry it, and the artifact must be built.** This
is a stronger verdict than the Layer-6 pre-read's (*"the substrate is right and
the battery is missing"*), and it is stronger because the Layer-6 answer was
overturned twice and the reason it was overturned applies here in advance.

### 6.1 What the substrate must force

A query is **generation-required** iff its correct answer is grammar-valid and
**provably not any item the stream carries**. Every frozen corpus in
`corpora/registry.py` was built so that its answer key names content the stream
asserts — `§8.7` is explicit that *dirt is always paired with the answer key*, and
`chronicle`, `sessions`, `murk`, `l3stream`, `l3streamb`, `l4stream` and
`l5stream` are all built to be *answerable from what was written*. A corpus whose
answers are in it cannot force composition. `l6batteryb`'s forcing region comes
closest in spirit — it forces a *commitment* — but its answers are two values the
stream carries, one of which is right.

The shape that works is a **closed compositional grammar with a withheld cell**:
the grammar determines an item from asserted material (a composition rule that is
a **declared reading** in the shape `ASSERTION_FORMS`, `INTENTION_FORM` and
`SET_ONCE_KEYS` already have), and the generator **withholds the composed item
from the stream**. Retrieval cannot answer it, because it is not there;
composition can, because the rule is in the grammar.

### 6.2 What the discrimination check demands of it

Six items, and each has a precedent to copy rather than invent:

1. **A novelty theorem, machine-checked over the frozen bytes** — the composed
   item's canonical bytes appear nowhere in the stream, asserted by exhaustive
   comparison, in the shape `ops/l6/t_l6batteryb.py` asserts its tie. `R7` clause
   3(b)'s pattern: put the guarantee on the **artifact**, not on a declared
   reading, so it holds against an arbitrary engine rather than against the one
   the session had in mind. Round 1's demotion is the cost of getting this wrong.
2. **Both classes present, and non-trivially so** — a recall class whose answers
   *are* stored, and a generation class whose answers provably are not, with the
   generation share `g > 1/18` of the answerable core (§4.2) so the blanket
   hedger dies on `F`.
3. **An exhibited class-E witness** (`R4` clause 5, `R5` clause 3) that attains
   `validity = novelty = tagging = 1000` and `promotion = 0` **without reading the
   answer key**, with its policy class declared. A class-O witness that reads the
   withheld cell attains everything trivially and proves nothing — the Layer-6
   lesson stated in advance rather than after.
4. **Every capability-free baseline scored**, including the three that *tie*
   (§1.1) — a Stage A that names only the retrieval-only policy's `novelty = 0`
   will report a discrimination broader than the one it measured.
5. **The denominators declared per class** (§1.5, §3.1), which is `R7` clause 2's
   discipline generalised from calibration to capability quantities.
6. **The humility side on the same artifact** (`R6` clause 1) with the
   conjunction measure defined (§1.3), and its `IMPOSSIBILITY.md` giving a
   **structural** argument — which at this layer is the fourth kind in the ladder
   and should say so: not `humility/l4`'s information-theoretic pigeonhole, not
   `humility/l5`'s absence of machinery, not `humility/l6`'s absence of a
   *ranking*, but the absence of a **construct that can produce a never-stored
   item at all**, with the conjunction at 0 by arithmetic because a product with
   a zero in it cannot be rescued.

### 6.3 The predicted fifth substrate kill

`R7` clause 1 killed `corpora/l6battery` because on murk *evidence that ranks
also resolves* — `§8.7` injects every defect by **visible construction**, so a
stream-only rule recovers each family exactly and the artifact measured its own
transparency rather than a model. The Layer-7 analogue is:

> **A composition that is forced may also be trivially taggable.** If the
> generation class is recognisable **from the query alone** — a distinct `op`, a
> distinct key, a shape no recall query has — then the engine tags correctly
> without ever consulting what it holds, and `tagging = 1000` measures a
> lookup rather than a capability. The artifact would be certifying its own
> legibility, exactly as `l6battery` certified murk's.

**This is the most likely place a first Layer-7 artifact is killed**, and it is
the finding this document most expects to be scored on. The fix has a shape:
queries whose class the query does not reveal — the same cue answered by
retrieval for one entity and only by composition for another, so the engine must
look at its own store to know which it did. Whether that is constructible while
keeping the novelty theorem machine-checkable is the arithmetic Stage A owes, and
it is not obvious that it is.

---

## §7. The predicted shape

Stated the way the two prior pre-reads stated theirs, so the session that meets it
can score it right or wrong:

> **Layer 7's Stage A will find `R2` obligation 1 discharged the ordinary way on
> every clause — five identities by exhibited attainment under `R5` clause 1, `F`
> and `ECE` by the ordinary method, no `R5`-shaped reading problem anywhere — and
> `R2` obligation 2 discharged only over the **conjunction**, resting on
> **`novelty`** and `F`, with `validity`, `promotion` and `B` **tied at the gate**
> by a retrieval-only policy and `ECE` discriminating nothing (Layer 6's measured
> finding, carried forward). The session will stop at **the denominators**: the
> fourth species named in §1.5, where `validity`/`novelty`/`tagging` have no
> denominator in `§5` and the tempting one is the engine's own testimony. The
> second stop, and the more expensive one, is at **an artifact where tagging is
> not free** (§6.3) — the Layer-7 form of the defect that killed `l6battery` one
> session after it was frozen. The predicted ruling is **`R4`-shaped plus a
> bequest discharged**: a reading (`generate` as a `query` op; `generated` as
> item-lineage orthogonal to `§4.2.3`'s closed kinds; `ECE` over `§3.4`'s own
> denominator; the three capability denominators bound to the artifact's declared
> classes) **and** a substrate, **and** a clause settling `R7` clause 7's
> recoverable-or-ingested question, which `[L6] [DOGFOOD]` deliberately declined to
> arm a reminder for precisely so that it would be decided here.**

**The half most likely to be wrong, named in advance so the miss is on the
record.** §6.3 says a first artifact probably dies on free tagging, and §6.2 item 1
says the novelty theorem must hold against an arbitrary engine. Those two pull
against each other: making the class *unrecognisable from the query* is what
makes tagging non-free, and making the withheld item *provably absent* is what
makes novelty machine-checkable — and the sharpest way to hide a class from the
query is to make its answers look like the others', which is exactly the property
that makes an exhaustive byte-comparison harder to state cleanly. If Stage A
finds those two requirements jointly satisfiable with a short argument, this
document overestimated the difficulty and the miss belongs here.

---

## §8. What this document does not do

No gate binds. No corpus is named as a substrate. No threshold moves, in either
direction, on any layer. No ruling is drafted and none is proposed for appending
— appending is what freezes, and a `PULSE` has no business near it. `R2`'s
standing step is untouched: a Layer-7 `ASCEND` still owes its own
`ATTAINABILITY.md` with the arithmetic computed, recorded and machine-checked
before any Layer-7 gate acquires authority, and every number in this file is
prose that such a file would supersede.

# IMPOSSIBILITY.md — why `make_engine(layer_cap = 6)` cannot reach the Layer-7 ceiling

`BOUNDARY.md §6` requires every humility trial to ship a **structural** argument —
not an empirical observation — for why the capped engine cannot exceed its
declared ceiling. The ceiling is `§5 L7`'s:

```
capped (novel ∧ valid ∧ tagged) ≤ 50
```

and the measurement, on `corpora/l7compose` at `DEFAULT_BUDGET`, is **0 of 160**,
against an ascension gate of three separate identities at 1000.

**The artifact is bound, both sides, by one clause.** `BOUNDARY-RULINGS.md R8`
clause 1 binds the Layer-7 ascension gate **and** this ceiling to
`corpora/l7compose`, for `R6` clause 1's reason: a ceiling measured on one
artifact beside a gate cleared on another is two facts about two worlds. The same
clause records the **fifth substrate kill** — 85 954 answerable queries across
every artifact this project had frozen, not one answer absent from its own stream
— so there is no other artifact this ceiling could have been measured on. On all
of them the generation-required class is empty, and a conjunction over an empty
class is not a low score; it is no score at all.

**And the measure had to be defined before it could be applied.** `§5 L7` states
the conjunction **once**, and only on the capped side; the ascension gate names
the three conjuncts separately and each as an identity. That is the first break
in a pattern every previous layer keeps, so `R8` clause 7 defines it — a per-item
conjunction over the artifact's **declared** generation-required class, with the
whole 160 as the denominator so that no engine can empty it. Everything below is
stated in that measure.

---

## §1. The two prongs, both measured

`R5` clause 4 is the reason both are here rather than the flattering one alone:
*"an unpriced item is not a saving; it is a margin that has already been spent"*,
and the Layer-5 document's first draft was refuted by its own mandatory
measurement. Both of these are asserted by `t_generation.py`, on the engine,
through `§7`.

### Prong 1 — the capped engine ANSWERS nothing in the generation channel

`make_engine(6)` has no `generate` op. `§7.3` is the cardinal rule — *capability
absence must surface as scores, never exceptions* — so every one of the 360
`generate` cues comes back as a **scored abstention**:

```
460 abstentions      = 260 answerable generation cues
                     + 100 KU1 generation-shaped unanswerable probes
                     + 100 KU2 never-asserted current-value probes
A = 1 740            every one of them a `current` query, every one correct
wrong 0   fabricated 0   B 1000   refused 0
```

It is not incapable in a way this artifact arranged. It answers **all** 1 740
retrieval queries correctly, holds the budget, states one confidence and invents
nothing. What it never does is return an item.

### Prong 2 — the three capability ratios have EMPTY DENOMINATORS, and `n/a` DISQUALIFIES

Because it tags nothing, the denominators of `validity`, `novelty` and `tagging`
are empty and all three read **`n/a`**. `R8` clause 3(c) rules what that means,
and it is the fourth species of gate clause this ladder has had to name — the
SELF-REPORTED DENOMINATOR, after `R5` clause 1's identity, `R5` clause 2's
minimizing clause and `R7` clause 3's empty domain:

> A gate is an instrument. An instrument has a range, and outside it the honest
> output is not a pass but a refusal to certify: a balance that reads `----`
> under an out-of-range load has not weighed the object.

The ground is a defect this project published about somebody else.
`autopsy/writ/ANATOMY.md` records that declaring a capability false sets the score
`null`, and null is dropped from **both** numerator and denominator
(`evaluator.ts:545-548`, `docs/metrics.md:204`). Under that reading this engine
would score `validity = 1000` for generating nothing. **A project that published
that finding cannot write the same exemption into its own gate**, so the three
clauses are failed and not skipped — and the stricter ungated diagnostic says the
same thing from the other side, `tagging_all = 0` over the whole declared class of
160 (`R8` clause 3(d)).

### The fate of all seven clauses, because three of them are TIED

| clause | gate | capped | verdict |
|---|---|---|---|
| `validity` | `= 1000` | **n/a** | **DISQUALIFIED** |
| `novelty` | `= 1000` | **n/a** | **DISQUALIFIED** |
| `tagging` | `= 1000` | **n/a** | **DISQUALIFIED** |
| `promotion` three deep | `= 0` | **0** | tied |
| `F` | `≥ 950` | **883** | **FAILED** |
| `B` | `= 1000` | **1000** | tied |
| `ECE` | `≤ 40` | **0** | tied |

The three ties are the three `R8` clause 1's baseline table records, and the
membership is a **finding**: `PRE-READ.md §1.1` predicted `{validity, promotion,
B}`, and the correction — that `validity` does not tie but disqualifies — is the
measurement of what deciding the denominator costs. `ECE ≤ 40` cleared by an
engine with no generation construct is not an embarrassment either; it is `R8`
clause 6's own point, recorded rather than left for a reader to assume: **`ECE ≤
40` is a floor against incoherence, not a discriminator**, and `R2` obligation 2
does not rest on it.

`promotion = 0` tied by an engine that promotes nothing because it **generates**
nothing is the sharpest of the three, and it is why clause 3(c) has to
disqualify rather than excuse. Read alone, that row says a memory with no
generation construct satisfies the self-pollution clause of the generation layer.
It does. That is the sentence `R8` clause 3 exists to stop anyone from ending on.

---

## §2. The structural argument: an engine that can only find cannot make

A generated item must be, by `§5 L7`'s own words, **grammar-valid**, **provably
never-stored**, and carried by a `generated` lineage tag. Take the middle
conjunct alone and the argument closes in three lines.

1. Every value a Layer-6 engine can return is a value it **holds**. Its whole
   answer surface is retrieval and derivation: `read` and `read_range` return the
   event; `recall` returns a stored episode; `current` and `asof` return an
   asserted value out of the interval table; `profile` and `count` are folds over
   what was ingested; `fired` returns a payload the caller itself wrote. Every one
   of those is the identity or a projection on content the store received.
2. `novelty = 1000` demands an item whose canonical bytes appear **nowhere** in
   the ingested store. No projection of stored content can produce one, because
   the projection's output is drawn from its input.
3. So the novel conjunct is **false on every answer the engine has**, and the
   product `(novel ∧ valid ∧ tagged)` has a zero in it that the other two cannot
   rescue.

`README-l6 §4` wrote that down before `corpora/l7compose` existed, which is why
this document can cite it rather than derive it: *"novelty requires an item
provably never stored, and every value this engine can return is one it holds, so
the novel conjunct is false on every answer it has and the other two conjuncts
cannot rescue a product with a zero in it. The ceiling of 50 is not approached
from below by a poor generator; there is no generator."*

**And the artifact does not weaken the argument by supplying the item.** The
composition rule `COMPOSITION_FORM` is public — it is a declared reading of the
frozen grammar, exactly as `ASSERTION_FORMS`, `INTENTION_FORM` and `SET_ONCE_KEYS`
are — so nothing is withheld from a correct **composer**. What is withheld is the
**item**, from the **retrieval channel**: for every generation-required compound
the composed `profile`'s canonical bytes appear nowhere in the frozen stream
(Theorem 2, exhaustively checked against all 12 000 payloads by
`trials/ops/l7/t_l7compose.py`). A retrieving engine asked for it can do exactly
two things — return something it holds, which is wrong, or abstain, which is
honest. It abstains. **No reading of held state produces an item the store never
contained.**

The second conjunct closes independently and needs no arithmetic at all: there is
no `generated` lineage field anywhere below Layer 7 to apply. `§4.2.3`'s closed
vocabulary is about the **answer's channel** and `R8` clause 4 rules `generated`
a property of the **item** — a claim the Layer-6 Answer has no place to carry and
the Layer-6 state has no ledger to support. Even an engine that somehow returned
a novel item would return it **untagged**, which `§5 L7` names in the
constitution's own words: *an untagged generation is a fabrication*.

---

## §3. THE FOURTH KIND OF IMPOSSIBILITY, and the taxonomy now needs the word

Stating **which** kind applies is what keeps the `§6` obligation from degenerating
into a template, and this is the fourth distinct kind in the ladder. Its members,
in order:

| layer | the capped engine lacks | the argument |
|---|---|---|
| **L4** | **absent bits** | *information-theoretic.* Thousands of distinct evicted payloads map into an aggregated forgetting record of at most 35 integer cells, so no injective map exists and the answers are unreachable **in principle** (`humility/l4/IMPOSSIBILITY.md §3`, the pigeonhole witness) |
| **L5** | **absent machinery** | *no operation on the write path consults a stored condition.* In budget the capped engine holds every intention **byte-exact** and still fires nothing: nothing is missing from the state, and what is missing is a verb (`humility/l5/IMPOSSIBILITY.md §4`) |
| **L6** | **absent order** | *no ranking.* The capped engine holds **both halves of every tie** and answers all 200 forcing queries; a constant assigns one confidence, every correct×incorrect pair ties, `§3.4` counts a tie as ½, so `AUROC = 1/2` exactly. Confidence emitted is not confidence calibrated (`humility/l6/IMPOSSIBILITY.md §4`) |
| **L7** | **absent generativity** | *the subject of this document, below* |

> ### The fourth kind: an engine that can only find cannot make.
>
> Layers 4, 5 and 6 each fail on something the capped engine lacks **about what
> it holds** — the bits are gone, no verb reaches them, or nothing orders them.
> Layer 7 is the first whose failure is not about held state at all. The capped
> engine's information is complete, its verbs are sufficient for every question
> it can answer, and its answers are ordered by a confidence model that works.
> What it cannot do is **produce an item the store never contained** — and that
> is not a shortage of anything it has, because **no reading of held state
> produces an item the store never contained.** Every operation it owns maps
> stored content to stored content; novelty demands a value outside that image;
> the demand is unsatisfiable by composition of the operations, not by a margin
> and not by a budget.
>
> The three earlier kinds ask *what is missing from the state?* This one asks
> *what is missing from the closure of the operations?* — and the answer is the
> capability itself. An engine that can only **find** cannot **make**.

Two properties of the fourth kind are worth naming, because they are what
distinguish it from the three above rather than restate them:

* **It survives a perfect state.** Give the capped engine the whole stream at
  `DEFAULT_BUDGET` with nothing evicted, nothing damaged and nothing refused —
  which is exactly how this ceiling is measured — and the number does not move.
  L4's pigeonhole needed pressure; L5's needed only a verb; L6's needed a tie in
  the artifact. This one needs nothing from the artifact except a query whose
  answer is not in the store, which is what the fifth substrate kill established
  no frozen corpus had.
* **It is closed under adding readings, not only under adding budget.** A
  Layer-6 engine may declare a new reading of the frozen grammar — that is
  precisely what `SET_ONCE_KEYS`, `INTENTION_FORM` and `ASSERTION_FORMS` are —
  and no reading helps, because a reading is a function of the payloads and its
  range is bounded by them. The composition rule is a reading **plus** an
  operation that emits a value the reading did not read, and it is the second
  half that Layer 6 does not have.

The taxonomy is a `PACKAGE` deliverable and the post-L6 `PULSE` recorded that it
becomes a four-kind taxonomy the moment this document exists (`BOUNDARY.log` line
41, recommending that `PACKAGE` follow Layer 7 for exactly this reason). The four
words are **absent bits (L4)**, **absent machinery (L5)**, **absent order (L6)**,
**absent generativity (L7)**.

---

## §4. Why the ceiling is not vacuous, and why the 50 permille is read

A ceiling is only a ceiling where its measure is defined and its denominator is
beyond the engine's reach. Both are `R8` clause 7's doing and neither is
incidental.

**Defined.** The conjunction appears nowhere in the ascension gate, so `§6`'s
requirement that the humility trial run *layer 7's own ascension tasks* would
otherwise have had no measure to run. Clause 7 supplies one, and it is not a
correctness measure: `§5 L7` names three conjuncts and correctness is not one of
them. `F ≥ 950` is where correctness lives, and a policy emitting valid, novel,
tagged nonsense dies there rather than here.

**Beyond reach.** The denominator is the **whole** declared generation-required
class — 160 — read off the artifact's own class table, so an engine cannot
improve its score by testifying to less. That is clause 3 applied to the ceiling
as well as to the gate, and at this layer it is load-bearing rather than tidy: an
engine with no `generate` op empties every self-reported denominator by
construction, and a ceiling stated over one of those would have been a ratio with
nothing underneath it.

**The 50 permille is read rather than reported.** `PRE-READ.md §1.3` required a
session to take one of the two available readings explicitly instead of writing
*"0 ≤ 50, ceiling holds"*, which is a sentence that is true of a ceiling
measuring nothing. `R8` clause 7 takes the first: **50 permille of 160 is eight
items**, so the ceiling reads *"fewer than 8 of 160 grammar-valid,
provably-novel, tagged items"* — a real quantity — and the 50 is slack for a
**partially** capable engine that `§7.4` does not produce. The competing reading,
that it anticipates a denominator under which a capped engine could score above
0, is declined with its reason: under the artifact-bound denominator no capped
engine can, so such a denominator would have to be the engine's own testimony,
which clause 3 forbids. The ceiling is therefore **loose by eight items and the
measurement is real**.

---

## §5. What would falsify this argument

Stated so the argument is refutable rather than decorative. The ceiling claim
fails if any of these becomes true:

* `make_engine(6)` returns a value on any `generate` cue on any corpus — a
  generation construct would then exist below Layer 7, where `§5 L7` says the
  capability is;
* the capped engine's conjunction is anything other than exactly **0** while it
  tags nothing — that would be an arithmetic error in `R8` clause 7's measure and
  not an engine improvement;
* any of the three capability ratios reports a **number** rather than `n/a` on
  the capped run: its denominator is its own report, so a number there means it
  tagged something, and `trial_the_three_capability_ratios_report_n_a_and_n_a_disqualifies`
  is where that is caught;
* the capped engine **clears** `F ≥ 950`, which would make this ceiling a
  measurement of retention rather than of generation. It measures 883, and the
  262 permille it is short by is `§3.0`'s abstention price on the class it cannot
  answer;
* an item the capped engine returns is absent from the store — Theorem 2 says
  the generation-required items are, and every answer this engine gives is
  content it received, so such an item would mean it composed one.

---

## §6. Where this is enforced

* `trials/humility/l7/t_generation.py` — the ceiling against `make_engine(6)` on
  the whole 12 000-event artifact through the generic interface (conjunction
  `0 ≤ 50`); the three ratios reading `n/a` with `n/a` disqualifying and
  `tagging_all = 0` beside them; the seven-clause fate as three ties, three
  disqualifications and one failure; the promotion ladder tied at 0 with nothing
  emitted at any rung; the declared denominator (`A 1 740`, 460 abstentions) and
  the forcing region with no pair distinguished; the budget law, the recorded
  occupancy and the single confidence value; and the engine-gated `§7.4`
  confirmation against the Layer-7 engine *capped to 6*, which skips until Stage C.
* `trials/ascension/l7/t_attainability.py::trial_the_capped_engine_measures_the_conjunction_at_zero`
  — the same 0, from the arithmetic side, since Stage A: the `make_engine(6)` row
  of that scoreboard is measured and not modelled, and
  `trial_the_blanket_hedger_is_the_capped_engine_measured` asserts query by query
  that the capped engine **is** the blanket hedger — the Layer-6 precedent
  recurring, where `confident-always` turned out to be `make_engine(5)` itself.
* `trials/ops/l7/t_l7compose.py` — Theorem 1's twins, the balanced coin, the
  six-labeller bench, Theorem 2's exhaustive canonical-byte comparison, the
  lineage ladder and the re-ingestibility that makes promotion reachable at all.
* `trials/laws/t_rulings.py` — `CEILING_CONJUNCTION = 50` bound to its `§5 L7`
  clause and to `R8`, whose clause 1 binds this ceiling and the ascension gate to
  `corpora/l7compose` together and whose clause 7 defines the measure.

# BOUNDARY.md — The Constitution of Boundary-1: Memory

> This document is **frozen**. It is never edited. There is no amendment
> mechanism. Everything the engine may become is bounded by what is written
> here. If a rule below seems wrong, the procedure is: log the objection in
> `BOUNDARY.log` and stop. The human decides. Code does not.

Public identity: **memtrials**. Internal name: **Boundary-1: Memory**.
This is a deterministic, zero-dependency memory engine, ascended through nine
capability layers, certified at each layer by a layered trial suite. Nothing
ships unless `trials/run.py` exits `0`.

All cultivation / realm framing lives in `LORE.md` and **only** there. This
document and all code use plain, sober terms.

---

## §1. The Fuel — Events

1. The engine consumes exactly one kind of input: **events**. Nothing else is
   fuel. Configuration, queries, and side-band signals are not fuel.

2. A caller submits a **payload**. A payload is a value drawn from the canonical
   type set defined in §2: it is built solely from **integers, strings,
   booleans, null, arrays, and string-keyed objects**. A payload never contains
   a floating-point number, bytes, a set, a tuple distinct from a list, or any
   custom object.

3. Upon ingestion the engine assigns the event a **logical time `t`**: a
   non-negative integer that is unique within a state, strictly increasing in
   ingestion order, and begins at `0`. `t` is **engine-assigned and
   engine-owned**. A caller may neither supply nor override it. `t` is the sole
   ordering authority in the system. There is no wall-clock time.

4. The canonical in-engine event record is exactly:

   ```json
   {"payload": <value>, "t": <int>}
   ```

   Any further structure a caller needs lives *inside* `payload`. The engine
   adds nothing to an event but its `t`.

---

## §2. The Physics

### 2.1 Purity

Every core operation is a **pure function** of explicit state:
`op(state, input) -> (state', output)`. There is no hidden state, no mutation
of the caller's inputs, no global variables, no ambient context.

### 2.2 The four prohibitions in `core/`

Within `core/` the following are forbidden, without exception:

- **I/O** — no file access, no sockets, no stdin/stdout/stderr, no environment
  reads, no subprocess.
- **Wall clock** — no `time`, no `datetime`, no calendar. The only clock is the
  engine-assigned logical `t` (§1.3).
- **Randomness** — no `random`, no `os.urandom`, no entropy of any kind. The
  only randomness anywhere in the project is `corpora/prng.py` (§8), which
  `core/` never imports.
- **Floats** — no float literals, no `float(...)`, no float arithmetic, no
  float-returning function. All numbers in core are exact integers or
  `fractions.Fraction`.

### 2.3 Determinism

Identical `(state, input)` sequences produce **byte-identical**
`(state', output)` sequences on every platform and every run. Determinism is
not a goal; it is a law, enforced by the `laws/` trial class.

### 2.4 Canonical JSON serialization

All serialization passes through a single canonical encoder governed by these
rules:

- Output is **UTF-8** bytes.
- Object keys are strings, sorted ascending by Unicode code point.
- No insignificant whitespace: item separator is `","`, key/value separator is
  `":"` (equivalently, Python `json.dumps(..., separators=(",", ":"))`).
- `ensure_ascii = false`: raw UTF-8 is emitted, never `\uXXXX` for printable
  non-ASCII.
- Integers render in base-10 with no leading zeros and no `+` sign.
- Booleans render as `true` / `false`; null renders as `null`.
- There is no trailing newline within a single encoded value. (Line-oriented
  corpora join encoded values with a single `"\n"` each — see §8.)

**Allowed value types**, and only these:

| type    | JSON form           |
|---------|---------------------|
| string  | `"..."`             |
| integer | `-?[0-9]+`          |
| boolean | `true` / `false`    |
| null    | `null`              |
| array   | `[...]` of allowed  |
| object  | `{...}`, string keys → allowed |

**Explicitly disallowed**: float, `NaN`, `Infinity`, bytes, set, custom object.

**Round-trip law**: for every allowed value `x`,
`decode(encode(x)) == x`; and for every canonical byte string `b`,
`encode(decode(b)) == b`.

### 2.5 The stdlib import whitelist for `core/`

`core/` may import from the standard library **only** the following modules:

```
json  fractions  itertools  functools  collections  hashlib  math  typing  dataclasses
```

- `math` is whitelisted **for integer use only** (e.g. `math.gcd`,
  `math.isqrt`, `math.comb`, `math.factorial`, `math.perm`). Any `math`
  function that returns a float (`sqrt`, `log`, `sin`, float `pow`, …) is
  forbidden by the float prohibition (§2.2), whitelist notwithstanding.
- No other stdlib module may be imported by `core/` — not `os`, `sys`, `time`,
  `random`, `re`, `decimal`, `statistics`, `datetime`, nothing.
- No third-party package may be imported by `core/`, ever.

The whitelist is **frozen**. There is no constitutional amendment mechanism;
the whitelist cannot be extended. The machine-readable copy lives at
`core/WHITELIST` and MUST agree with this list verbatim (enforced by the
import-whitelist law trial).

### 2.6 The layering rule

`shell/` may import `core/`. **`core/` may NEVER import `shell/`.** `core/` is
the pure engine; `shell/` holds the CLI, persistence, and adapters. Corpora and
trials are tooling; `core/` imports neither.

---

## §3. The Four Measures

Four measures, and only four: **fidelity, coverage, budget, calibration**. Every
capability claim is scored by them. All measure arithmetic is done in exact
`fractions.Fraction`; the final calibration to an integer is in **permille**
(parts per thousand, `0..1000`) via the `permille` function of §3.5.

### 3.0 The abstention-aware per-query score

Each query has a ground truth that is either **answerable** (a correct value
exists) or **unanswerable** (the only correct behavior is to abstain). The
engine either **answers** (with a value) or **abstains**. The per-query score
`s` is:

| situation                                   | score `s` |
|---------------------------------------------|-----------|
| answerable → engine answers **correctly**   | **1000**  |
| unanswerable → engine **abstains**          | **1000**  |
| answerable → engine **abstains**            | **100**   |
| answerable → engine answers **wrongly**     | **0**     |
| unanswerable → engine **answers** (fabricates) | **0**  |

Knowing that you do not know is worth exactly as much as knowing the answer
(1000). A hedge on an answerable query keeps a little credit (100). Confident
error and fabrication earn nothing (0).

### 3.1 Fidelity (F)

Mean per-query score over the query set:

```
F = (Σ_i s_i) / (N · 1000)          as a Fraction in [0, 1]
F‰ = permille(F)                     integer in [0, 1000]
```

where `N` is the number of queries and `s_i` the per-query score (§3.0).

### 3.2 Coverage (C)

Importance-weighted recovery of the target set. Each target item `i` carries an
integer importance weight `w_i ≥ 1` (default `1`); an item is **recovered** when
the engine answers it correctly (score 1000 under §3.0):

```
C = ( Σ_{i recovered} w_i ) / ( Σ_i w_i )      a Fraction in [0, 1]
C‰ = permille(C)
```

With uniform weights this is the fraction of answerable targets correctly
answered. The weighted form is what Layer 3 requires: importance-weighted
coverage that must survive eviction under 10× pressure.

### 3.3 Budget (B)

Adherence to the integer budget cap. The budget law (§4.1) refuses any write that
would exceed the cap, so a lawful engine's peak occupancy never exceeds it. With
integer budget cap `Bcap > 0` and integer **peak occupancy** `peak`:

```
B = 1                if peak ≤ Bcap
B = Bcap / peak      if peak > Bcap       (a Fraction in (0,1))
B‰ = permille(B)
```

A lawful engine scores `B‰ = 1000`; any value below 1000 is a breach of the
budget law and is disqualifying. Budget is the measure that certifies the cap
held under a trial. Cost accounting is pure and integer (§4.1).

### 3.4 Calibration (K) — Brier, ECE, AUROC, all exact

The engine attaches to every answer an integer **confidence in permille**
(`conf_i ∈ [0, 1000]`) derived from structural evidence, never a float. Over the
`A` answered queries with `correct_i ∈ {0, 1}`, three quantities are computed in
exact `Fraction`:

```
Brier = (1/A) · Σ_i (conf_i/1000 − correct_i)^2            in [0,1], lower better
ECE   = Σ_b (n_b/A) · | mean_conf_b − acc_b |              in [0,1], lower better
AUROC = U / (n_pos · n_neg)                                in [0,1], higher better
```

- **Brier** is the mean squared gap between stated confidence and outcome.
- **ECE** bins the answered queries into the ten fixed permille bins `[0,100)`,
  `[100,200)`, …, `[900,1000]` (last bin closed); `mean_conf_b` and `acc_b` are
  the mean confidence and mean correctness within bin `b`, `n_b` its count, and
  empty bins contribute 0.
- **AUROC** is the Mann–Whitney statistic: `U` counts, over all
  correct×incorrect answer pairs, those whose correct answer carried the higher
  confidence (ties count ½); `n_pos` / `n_neg` are the counts of correct /
  incorrect answers. It is **undefined** when `n_pos = 0` or `n_neg = 0` (report
  `n/a`; any gate that cites AUROC requires both classes present).

Calibration is this triple. A convenience scalar `K‰ = permille(1 − Brier)` is
defined for reporting, but §5 gates cite Brier/ECE/AUROC directly where they bite
(most sharply at Layer 6).

### 3.5 The `permille` calibration function

`permille(x)` maps an exact `Fraction x ∈ [0,1]` to an integer in `[0,1000]`
using **round-half-to-even** (banker's rounding) on the exact rational, so the
result is platform-independent:

```
let n = 1000 · x            (a Fraction)
let q = n.numerator // n.denominator     (floor)
let r = n − q                            (Fraction in [0,1))
if r <  1/2:  return q
if r >  1/2:  return q + 1
if r == 1/2:  return q if q is even else q + 1
```

No float ever appears in this computation.

---

## §4. The Budget Law and the Provenance Law

### 4.1 The Budget Law — binding from Layer 1

1. Each engine state carries an integer **budget cap `Bcap`** and an integer
   **occupancy** (current resource cost, in *work units* — one unit is one
   primitive state cell). Occupancy and all cost accounting are pure, integer,
   and reproducible: identical inputs yield identical costs, and no float ever
   enters the budget. Cost is accounted in explicit state (a counter), never by
   measuring the OS, the clock, or process memory.

2. From **Layer 1 onward the law binds**: a write that would raise occupancy
   above `Bcap` is **REFUSED, deterministically** — the engine returns a
   refusal, performs no partial write, and does **not** evict (eviction is a
   Layer 3 capability, not a budget side-effect). The accept/refuse decision is a
   pure function of the input, identical on every run.

3. The **budget measure** (§3.3) certifies the cap held: a lawful engine never
   exceeds `Bcap` and scores `B‰ = 1000`. Below Layer 1 the budget is measured
   and reported but does not gate.

### 4.2 The Provenance Law — dormant until Layer 7, binding forever after

1. Before Layer 7 this law is **dormant**: provenance may be attached but is
   neither required nor scored.

2. From **Layer 7 onward** it is **binding, and once bound it can never be
   un-bound**. Every non-abstaining answer MUST carry a valid **provenance
   tag**. An answer without a valid provenance tag scores as **wrong (0)**,
   regardless of whether its value is correct.

3. The provenance-tag schema (validated by the provenance-tag schema validator
   law trial):

   ```json
   {
     "support": [<int t>, ...],   // sorted, ascending, non-negative, each an
                                  // actually-ingested event t; may be empty
                                  // ONLY when kind == "absent"
     "kind": "<string>",          // one of: "recall","aggregate","derive","absent"
     "t_asof": <int>              // non-negative logical time the answer holds as-of
   }
   ```

   All numbers are integers. `support` is strictly ascending with no duplicates.
   `kind` is drawn from the fixed vocabulary and no other. `t_asof ≥ 0`. An
   `"absent"` tag (justified negative / abstention-as-answer) is the only case
   in which `support` may be empty.

---

## §5. The Nine-Layer Ladder

Each layer is a capability claimed only by passing its **ascension** trials at or
above the ascension gate. Each gate is stated in the metric that layer is about —
the four measures of §3, plus the capability-specific quantities named in §5.1.
Every layer also declares a **humility failure ceiling**: the maximum score an
engine capped one layer below — `make_engine(layer_cap = N−1)` — may reach on
layer `N`'s own ascension tasks, run through the same generic interface (§7). The
humility trial class (§6) asserts the capped engine scores **at or below** that
ceiling, proving the gate cannot be cleared without the new capability; each
layer ships an `IMPOSSIBILITY.md` structural argument for its ceiling.

Layers 8–9 receive laws but **not thresholds** yet — thresholds are
**specified at the Phase 3→4 gate**.

Legend (all permille unless noted): **F** fidelity, **C** coverage, **B** budget,
**K** calibration (Brier / ECE / AUROC). "capped" = the `layer_cap = N−1` engine.

| L | Capability | Ascension gate | Humility ceiling (capped scores ≤) |
|---|------------|----------------|-------------------------------------|
| 1 | **Retention** — write / read-by-time / read_range / snapshot / restore; budget law binding | F=1000, C≥995, B=1000, Brier≤10, snapshot/restore byte-identical | capped F ≤ 150 |
| 2 | **Recall** — associative `recall(cue)` via deterministic index (token n-grams, MinHash) | cue-C≥900, F≥950, AUROC≥800, B=1000, Brier≤50 | capped cue-C ≤ 100 |
| 3 | **Forgetting** — principled eviction under pressure (stream = 10× budget) | weighted-C≥850, unweighted-C≥90, F≥950, B=1000, ECE≤80 | capped weighted-C ≤ 300 |
| 4 | **Consolidation** — episodic→semantic derived schemas with reconstruction | footprint≤250 (≥4× compression) at reconstruction F≥900, C≥850, B=1000, Brier≤60 | capped reconstruction F ≤ 400 at footprint≤250 |
| 5 | **Prospection** — `intend(condition → event)`; triggers fire exactly-once on future writes | trigger-precision=1000, trigger-recall=1000, dup-fire=0, miss=0, F≥980, B=1000, Brier≤30 | capped trigger-recall ≤ 50 |
| 6 | **Meta-memory** — confidence permille from structural evidence | Brier≤40, ECE≤30, AUROC≥900, abstention-aware F≥950, B=1000 | capped AUROC ≤ 600 |
| 7 | **Generation** — `generate(cue)`: grammar-valid, provably never-stored, 100% tagged `generated` | validity=1000, novelty=1000, tagging=1000, self-pollution promotion=0 (three deep), F≥950, B=1000, ECE≤40 | capped (novel∧valid∧tagged) ≤ 50 |
| 8 | **Self-description** — introspection answered FROM STATE via the ordinary query interface | *specified at Phase 3→4 gate* | *specified at Phase 3→4 gate* |
| 9 | **Birth** — emit a functioning L1 successor from the self-model alone; successor passes the entire frozen L1 suite | *specified at Phase 3→4 gate* | *specified at Phase 3→4 gate* |

### 5.1 Threshold defenses (one sentence each)

**Layer 1 — Retention** (capped = the null `layer_cap = 0` engine)
- `F=1000`: Retention is the exact return of what was written, read by time and by range, so any deviation is a bug, not a tolerance.
- `C≥995`: Every in-budget write must be retrievable; only boundary as-of queries at the very edges of the log may legitimately abstain.
- `B=1000`: The budget law is absolute — an over-budget write is refused deterministically, so peak occupancy never exceeds the cap.
- `Brier≤10`: Retention answers straight from stored ground truth, so stated confidence must almost perfectly match the near-certain correctness.
- `snapshot/restore byte-identical`: A state restored from its snapshot must answer identically, so the round-trip is byte-for-byte or it is broken.
- Humility `capped F ≤ 150`: An engine with no retention can only abstain on answerable reads (score 100 each), so it cannot rise above the abstention floor.

**Layer 2 — Recall** (capped = the `layer_cap = 1` Retention engine)
- `cue-C≥900`: Associative recall must return the intended target from a cue against grammar-controlled distractors at least 90% of the time.
- `F≥950`: A wrong recall is worse than none, so the abstention-aware score of returned items must stay very high.
- `AUROC≥800`: Match confidence must separate true targets from lookalike distractors well above chance.
- `B=1000`: The deterministic index is built within the same hard budget; the cap still holds absolutely.
- `Brier≤50`: Recall confidence must track whether the retrieved item is actually the cue's target.
- Humility `capped cue-C ≤ 100`: A read-by-time engine has no associative index, so cue-based retrieval against distractors cannot beat chance (~1 in the candidate pool).

**Layer 3 — Forgetting** (capped = the `layer_cap = 2` Recall engine)
- `weighted-C≥850`: Under a stream of 10× the budget, importance-weighted eviction must keep at least 85% of the total importance mass recoverable.
- `unweighted-C≥90`: Retained content is ~1/10 of the stream, so plain recovery near 10% confirms a full budget's worth was kept, not less.
- `F≥950`: Forgetting may drop items but must never corrupt the ones it keeps, so surviving recalls stay exact.
- `B=1000`: Eviction holds peak occupancy inside the cap at all times, even under 10× pressure — the budget law never breaks.
- `ECE≤80`: The engine must know what it forgot, so confidence on evicted items is low and well-calibrated (abstain, not fabricate).
- Humility `capped weighted-C ≤ 300`: Without principled eviction, a recall-only engine fills to budget then refuses the rest, keeping the earliest items rather than the important ones, so it cannot preserve the important mass.

**Layer 4 — Consolidation** (capped = the `layer_cap = 3` Forgetting engine)
- `footprint≤250` (≥4× compression): Derived schemas must shrink the episodic footprint to at most a quarter of the raw bytes.
- `reconstruction F≥900`: At that footprint the engine must still reconstruct query answers at ≥90% fidelity, proving the schemas are lossy-but-honest.
- `C≥850`: The derived schemas (entity summaries, attribute histories, action patterns) must answer at least 85% of the semantic queries raw episodes could.
- `B=1000`: Consolidation and its derived schemas run within the hard budget like any other state.
- `Brier≤60`: Reconstructed answers must carry honest confidence reflecting the lossy consolidation.
- Humility `capped reconstruction F ≤ 400 at footprint≤250`: Dropping is not deriving — a forget-only engine squeezed to a quarter of the bytes has simply lost three-quarters of its episodes and cannot reconstruct what it deleted.

**Layer 5 — Prospection** (capped = the `layer_cap = 4` Consolidation engine)
- `trigger-precision=1000 ∧ trigger-recall=1000`: Every intention whose condition a future write satisfies must fire, and nothing may fire spuriously — prospection is exact or it is broken.
- `dup-fire=0 ∧ miss=0`: Exactly-once means no trigger fires twice and none is missed.
- `F≥980`: A fired event's payload must match the intended event essentially exactly.
- `B=1000`: Pending intentions live within the hard budget like any other state.
- `Brier≤30`: A fired trigger asserts a deterministic match, so its confidence must reflect that near-certainty.
- Humility `capped trigger-recall ≤ 50`: Consolidation summarizes the past and has no construct that watches future writes, so it fires condition-met triggers only by coincidence.

**Layer 6 — Meta-memory** (capped = the `layer_cap = 5` Prospection engine)
- `Brier≤40`: Structurally-derived confidence must be sharp and accurate, keeping the mean squared calibration error at or under 0.04.
- `ECE≤30`: Confidence buckets must match observed accuracy to within 3% expected calibration error.
- `AUROC≥900`: Confidence must rank correct answers above incorrect ones with area under ROC at least 0.90.
- `abstention-aware F≥950`: Under the 1000/1000/100/0 table, knowing-that-you-don't-know earns full credit and fabrication must be near-absent.
- `B=1000`: Meta-memory derives confidence from existing state within budget.
- Humility `capped AUROC ≤ 600`: An engine that emits fixed or heuristic confidence with no structural-evidence model produces uninformative confidences that barely separate right from wrong.

**Layer 7 — Generation** (capped = the `layer_cap = 6` Meta-memory engine)
- `validity=1000`: Every generated item must be grammar-valid; an invalid generation is a hard failure.
- `novelty=1000`: Every generated item must be provably never-stored; reproducing a stored item is not generation.
- `tagging=1000`: 100% of generated items must carry the `generated` lineage tag; an untagged generation is a fabrication.
- `self-pollution promotion=0` (three deep): After re-ingesting its own generations three deep, the engine must never promote generated-lineage content to observed fact, and provenance chains must survive.
- `F≥950, B=1000, ECE≤40`: Provenance chains stay intact within budget, and confidence on generated content stays calibrated.
- Humility `capped (novel∧valid∧tagged) ≤ 50`: A memory that only recalls and derives cannot invent provably-novel items and has no `generated` tag to apply, so the conjoined score collapses.

---

## §6. The Trial Classes

A trial is **green**, **red**, or **skipped-by-design**. `trials/run.py` exits
`0` iff no trial is red. Skips are legal (a law that needs an engine reports
`SKIPPED-BY-DESIGN` until the engine exists).

- **`laws/`** — Universal invariants of *legality*, not capability. They must
  hold at every layer regardless of what the engine can do: determinism,
  canonical round-trip, budget-accounting purity, the import whitelist, the
  no-float rule in `core/`, corpora byte-match, and the provenance-tag schema.
  A red law means an **illegal** engine; no ascension is possible.

- **`ops/`** — Fine-grained unit and property trials for individual operations
  and building blocks (the PRNG, the generators, primitives). Correctness of the
  pieces.

- **`ascension/`** — Capability trials. Passing a layer's ascension trials at or
  above its §5 gate entitles the engine to claim that layer. Scored by the four
  measures (§3).

- **`humility/`** — For each layer `N`, the humility trial takes **layer `N`'s
  own ascension tasks** and runs them, through the same generic interface (§7),
  against **`make_engine(layer_cap = N−1)`** — the engine built with capability
  capped one layer below. It asserts the capped engine's scores are **at or
  below** the layer's declared **humility failure ceiling** (§5), proving the
  ascension gate is load-bearing and cannot be cleared by the previous layer's
  capability alone. **Every humility trial ships an `IMPOSSIBILITY.md`** giving a
  **structural** argument (not an empirical observation) for why the capped
  engine cannot exceed the ceiling. (The per-layer fabrication ceiling of earlier
  drafts is *not* a constitutional measure; it survives only as a component of
  the abstention-aware scoring that Layer 6+ calibration relies on.)

- **`strain/`** — Scale and stress trials over large corpora and dirty
  (**murk**) input; they check that the measures and the budget hold up under
  volume and injected defects. Strain trials usually draw on murk (§8). This
  class includes the **mandatory Layer 7 self-pollution strain**: the engine
  re-ingests its own generations three deep, provenance/lineage chains must
  survive, and consolidation must never promote generated-lineage content to
  observed fact.

- **`anchors/`** — Frozen regression trials that capture exact past behavior.
  Once an anchor is set, its expected output never changes. Anchors guarantee no
  silent regression across sessions. **Extending** anchors (adding new ones) is
  allowed; **editing** an existing anchor is forbidden (§9).

---

## §7. The Generic Engine Interface

This spec is copied verbatim to `trials/adapters/INTERFACE.md`. Trials speak to
any engine only through it; an engine is a black box behind these three pure
functions.

### 7.1 The three operations

- `ingest(state, payload) -> (state', t)`
  Pure. Appends one event, assigns and returns its logical `t` (§1.3), and
  returns the new state. Never mutates `state` or `payload`.

- `query(state, q) -> answer`
  Pure. Returns an **Answer** (below). Never mutates `state`.

- `snapshot(state) -> bytes`
  Pure. Returns the canonical JSON serialization (§2.4) of the engine's state.
  `snapshot` round-trips: a state restored from its snapshot answers queries
  identically.

### 7.2 The Answer

```json
{
  "status": "answer" | "abstain",
  "value": <allowed value | null>,     // null when status == "abstain"
  "confidence": <int 0..1000>,         // permille (§3.4)
  "provenance": <provenance-tag | null> // §4.2; may be null before Layer 7
}
```

### 7.3 The cardinal rule

**Capability absence must surface as scores, never exceptions.** If the engine
cannot handle a query — an unsupported query type, a capability it has not yet
ascended to — it MUST return `{"status":"abstain", ...}`, which the trial
harness scores by the abstention-aware table (§3.0). It MUST NOT raise. A raised
exception is a harness-level failure (red / undefined behavior), categorically
worse than a scored abstention. Missing capability is principled abstention; it
is scored, not thrown.

### 7.4 Capability-capped construction (for humility trials)

An adapter also exposes `make_engine(layer_cap) -> state`, which builds the
engine with capability restricted to `layer_cap`. The humility trial class (§6)
uses `make_engine(layer_cap = N−1)` to run layer `N`'s ascension tasks against an
engine that provably lacks layer `N`. Capping is a construction-time restriction
only: the capped engine speaks the identical `ingest` / `query` / `snapshot`
interface and still surfaces missing capability as scores (abstention), never
exceptions (§7.3).

---

## §8. The Corpora Doctrine

1. **Seeded generators.** Every synthetic corpus is produced by a deterministic
   generator seeded by an explicit integer seed, drawing randomness solely from
   `corpora/prng.py` (§8.5). 

2. **Frozen outputs.** A generator's output at a named `(seed, scale)` is
   frozen to a committed file. That file is the canonical corpus.

3. **The byte-match law.** Re-running a generator at the same `(seed, scale)`
   MUST reproduce the frozen file **byte-for-byte** (enforced by the corpora
   byte-match law trial). Any drift is a red suite. Frozen outputs are never
   edited (§9).

4. **Banned stdlib random.** `import random`, `os.urandom`, and every other
   entropy source are forbidden throughout the project. The xorshift PRNG is the
   only randomness that exists.

5. **The hidden-holdout-seed note.** A reserved seed range (seeds `≥ 9_000_000`)
   is held out as **hidden holdouts**: these seeds are used to evaluate
   generalization on inputs the engine has never been frozen against, and their
   outputs are **never committed** as frozen files. The doctrine forbids
   freezing any holdout-seed output into the repo.

6. **Scale targets** (Phase 0; scale grows in later phases via strain):
   chronicle **~50k** events, sessions **~5k** events, murk **~10k** events.

7. **The murk family.** `corpora/murk/` is a generator *layer* over the base
   grammars that injects controlled defects through explicit **knobs**:
   contradiction rate, near-duplicate rate, ambiguity rate, and
   malformed-payload rate. Every frozen murk output ships a
   **`ground_truth.json`** answer key listing **every** injected defect with the
   event `t`'s it touches. **Dirt is always paired with the answer key**: no
   defect is ever injected without being recorded. Trials at every layer may
   draw on murk; strain trials usually should.

8. **The real-data rule.** A frozen, checksummed snapshot of real data is a
   **legal corpus**. It has no generator, so it is **exempt from the byte-match
   law**; instead it is bound by its recorded **SHA-256 checksum** (a
   checksum-match law replaces byte-match for real-data corpora). A real-data
   corpus ships a checksum manifest and is never edited.

---

## §9. The Session Doctrine

1. **One move per session.** Each session executes **exactly one** move, drawn
   from:

   `{ FORGE, AUTOPSY, GAPMAP, ASCEND, STRAIN, DOGFOOD, PULSE, PACKAGE }`

   - **FORGE** — lay down foundational scaffolding: constitution, corpora, and
     trial infrastructure.
   - **AUTOPSY** — dissect a prior design, engine, or failure; deposit a report
     in `autopsy/`.
   - **GAPMAP** — survey what is missing before an ascension; produce a gap map.
   - **ASCEND** — implement and attempt a layer's capability and its ascension
     trials to claim the next layer.
   - **STRAIN** — push scale and dirt; add or run strain trials.
   - **DOGFOOD** — drive the engine over real data end-to-end through `shell/`.
   - **PULSE** — health check: re-run the suite, record status, small
     maintenance.
   - **PACKAGE** — the packaging move (later phase); fills `packaging/`.

2. **Frozen artifacts are never edited.** Old layers, frozen trials, frozen
   corpora, anchors, and `BOUNDARY.md` itself are immutable. New work adds new
   files; it does not mutate frozen ones. Old `BOUNDARY.log` lines are never
   rewritten.

3. **Green or nothing.** No commit is made while `trials/run.py` exits nonzero.
   A green suite is the precondition for every commit — including a
   documentation-only change. A red suite ends the session with a log line
   explaining the failure and no commit.

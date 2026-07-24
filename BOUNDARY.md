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

Every capability claim is scored by four measures. All measure arithmetic is
done in exact `fractions.Fraction`; the final calibration to an integer is in
**permille** (parts per thousand, `0..1000`).

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

Fraction of queries the engine chose to answer (did not abstain):

```
C = A / N                            A = count of answered queries
C‰ = permille(C)
```

### 3.3 Calibration (K)

The engine attaches to every answer an integer **confidence in permille**
(`conf_i ∈ [0, 1000]`). Over the `A` answered queries, with
`correct_i ∈ {0, 1}`:

```
G = ( Σ_i |conf_i − 1000·correct_i| ) / A     mean L1 reliability gap, in permille
K‰ = permille( 1 − G/1000 ) = 1000 − permille(G/1000)
```

`K‰ = 1000` means stated confidence matched outcome exactly on every answered
query; lower means confidence and correctness diverged. If `A = 0`, `K` is
defined as `1000` (a fully abstaining engine is vacuously calibrated) but note
that Coverage will be `0`.

### 3.4 Economy (E)

Budget adherence (see §4). With integer total cost `cost` and integer budget
`B > 0`:

```
E = 1                if cost ≤ B
E = B / cost         if cost > B          (a Fraction in (0,1))
E‰ = permille(E)
```

Meeting or beating budget is full marks; overrun is penalized in exact
proportion.

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

1. Every `ingest` and every `query` consumes a declared, **integer** cost, in
   abstract *work units*. One work unit is one primitive state access (the read
   or write of one logical cell). The engine defines its unit consistently and
   accounts for it in explicit state (a counter), never by measuring the OS,
   the clock, or process memory.

2. Cost accounting is **pure and reproducible**: identical inputs yield
   identical costs. Costs are integers; no float ever enters the budget.

3. A trial grants the engine an integer **budget `B`** per episode. From
   **Layer 1 onward**, the Economy measure (§3.4) gates ascension, and the
   per-layer humility ceilings bound worst-case behavior under budget. Below
   Layer 1 the budget is measured and reported but does not gate.

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

Each layer is a capability the engine may claim only by passing its **ascension**
trials at or above the ascension gate, while never breaching its **humility
failure ceiling**. Measures are in permille (§3). `H` is the humility ceiling:
the maximum permille of humility-trial queries the engine may answer *wrongly*
(a wrong value, or any non-abstaining answer to an unanswerable query).

Layers 8–9 receive laws but **not thresholds** yet — thresholds are
**specified at the Phase 3→4 gate**.

| L | Capability | Ascension gate (min ‰) | Humility ceiling `H` (max ‰) |
|---|------------|------------------------|------------------------------|
| 1 | **Recall** — exact store / point fetch | F≥950, C≥900, K≥800, E≥700 | 50 |
| 2 | **Recency & Range** — ordered / as-of / range reads | F≥950, C≥900, K≥820, E≥720 | 45 |
| 3 | **Aggregation** — exact integer aggregates | F≥940, C≥880, K≥840, E≥740 | 40 |
| 4 | **Association** — links / joins / adjacency | F≥930, C≥860, K≥850, E≥760 | 35 |
| 5 | **Summarization** — bounded honest compression | F≥920, C≥820, K≥870, E≥820 | 30 |
| 6 | **Contradiction & Dedup** — detect / resolve / abstain | F≥930, C≥800, K≥890, E≥780 | 25 |
| 7 | **Provenance** — every answer cites its support | F≥940, C≥800, K≥900, E≥780 | 20 |
| 8 | **Revision & Forgetting** — bounded retention, reported forgetting | *specified at Phase 3→4 gate* | *specified at Phase 3→4 gate* |
| 9 | **Self-Audit & Adversarial Robustness** — audits own provenance under adversarial murk | *specified at Phase 3→4 gate* | *specified at Phase 3→4 gate* |

### 5.1 Threshold defenses (one sentence each)

**Layer 1 — Recall**
- `F≥950`: Exact key-value recall is the simplest capability, so near-perfection is the minimum bar to claim it works at all.
- `C≥900`: Every stored key is answerable here, so the engine should answer at least 90% rather than hide behind abstention.
- `K≥800`: Confidence need only roughly track correctness this early, so an 800‰ reliability (≤200‰ mean gap) is a lenient but non-trivial floor.
- `E≥700`: A naive exact store may be wasteful, so we require only 70% budget efficiency while the engine is young.
- `H≤50`: Even the first layer must almost never fabricate — at most 5% of impossible questions may be answered wrongly.

**Layer 2 — Recency & Range**
- `F≥950`: Ordered and as-of reads are still deterministic lookups, so the fidelity bar holds at 95%.
- `C≥900`: Range and recency queries remain fully answerable from stored events, so 90% coverage is still expected.
- `K≥820`: Temporal ordering gives the engine more signal to calibrate on, so we tighten calibration slightly.
- `E≥720`: Ordered access should be nearly as cheap as point access, so efficiency rises modestly.
- `H≤45`: As-of queries invite off-by-one fabrication, so the hallucination ceiling tightens to 4.5%.

**Layer 3 — Aggregation**
- `F≥940`: Integer aggregates are exact but compose more steps, so we allow a hair more slack at 94%.
- `C≥880`: Some aggregates over empty or unknown ranges are legitimately unanswerable, so coverage eases to 88%.
- `K≥840`: Aggregation error is easy to self-detect, so calibration should improve to 84%.
- `E≥740`: Aggregates can be maintained incrementally, so we expect better efficiency at 74%.
- `H≤40`: Aggregates over missing data are a classic fabrication trap, so the ceiling tightens to 4%.

**Layer 4 — Association**
- `F≥930`: Joins multiply the chance of a single wrong link, so 93% acknowledges the compounded difficulty.
- `C≥860`: Many association queries have no matching link and must be abstained on, so coverage eases to 86%.
- `K≥850`: Link confidence is directly checkable against adjacency, so calibration rises to 85%.
- `E≥760`: Indexed adjacency should keep join cost bounded, so efficiency climbs to 76%.
- `H≤35`: Inventing a nonexistent relationship is the worst failure here, so the ceiling drops to 3.5%.

**Layer 5 — Summarization**
- `F≥920`: Lossy summaries trade some fidelity for size, so 92% is the honest floor for a compressing memory.
- `C≥820`: A bounded summary cannot answer everything and must abstain more, lowering coverage to 82%.
- `K≥870`: A summarizer that knows what it discarded should be well-calibrated, so we demand 87%.
- `E≥820`: Compression exists to save budget, so efficiency must jump to 82% to justify the layer.
- `H≤30`: Summaries tempt confident guessing about discarded detail, so the ceiling tightens to 3%.

**Layer 6 — Contradiction & Dedup**
- `F≥930`: Resolving contradictions restores correctness, so fidelity recovers to 93% despite dirtier input.
- `C≥800`: Genuinely unresolved contradictions must be abstained on, so coverage floors at 80%.
- `K≥890`: Detecting a contradiction is itself a calibration signal, so we require 89%.
- `E≥780`: Dedup shrinks state and should pay for its detection cost, so efficiency holds at 78%.
- `H≤25`: Silently choosing a side of a true contradiction is fabrication, so the ceiling drops to 2.5%.

**Layer 7 — Provenance**
- `F≥940`: With provenance forcing justified answers, unjustifiable guesses vanish and fidelity should rise to 94%.
- `C≥800`: Requiring citable support makes the engine abstain whenever it cannot cite, holding coverage at 80%.
- `K≥900`: Provenance ties confidence to concrete support, so calibration must reach 90%.
- `E≥780`: Carrying provenance adds bookkeeping, so we hold efficiency at 78% rather than raising it.
- `H≤20`: An answer without valid provenance now scores zero, so tolerated fabrication falls to its strictest 2%.

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

- **`humility/`** — Adversarial trials whose queries are **unanswerable by
  construction**; the only correct behavior is calibrated abstention. Scored by
  the abstention-aware table (§3.0) and bounded by the layer's §5 humility
  ceiling.

  **The humility fairness rule.** A humility trial must pose the **same task**
  through the **same generic interface** (§7) as its paired ascension trial —
  identical `ingest` / `query` / `snapshot`, no capability hints, no
  special-casing. It differs only in that its queries have no correct
  non-abstaining answer. **Every humility trial ships an `IMPOSSIBILITY.md`**
  giving a *structural* argument (not an empirical observation) for why no
  correct non-abstaining answer can exist. Without that argument the ceiling
  would be arbitrary; with it the ceiling is principled.

- **`strain/`** — Scale and stress trials over large corpora and dirty
  (**murk**) input; they check that the measures and the budget hold up under
  volume and injected defects. Strain trials usually draw on murk (§8).

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
  "confidence": <int 0..1000>,         // permille (§3.3)
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

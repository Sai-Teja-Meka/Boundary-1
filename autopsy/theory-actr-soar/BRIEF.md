# BRIEF — ACT-R declarative memory & Soar episodic memory / chunking

`[L0] [THEORY]` — a documented one-off, lighter than an AUTOPSY: no repository,
no call paths. This reads the published **equations and documentation** of two
cognitive architectures and maps them onto our ladder. Sources are cited by name
and year; where I am unsure of a specific source I describe the idea without
attributing it. A **Constitutional note** at the end records that no law-change
objection arose.

---

## 1. ACT-R base-level activation → Layer 3 (Forgetting / importance)

**In words.** In ACT-R (Anderson & Lebiere, 1998; Anderson et al., 2004) a
declarative chunk `i` has a *base-level activation* that rises each time the chunk
is used and decays as time passes since each use. A chunk used often and recently
is highly active; a chunk used once, long ago, is nearly gone. Base-level is the
recency-and-frequency part of a chunk's total activation.

**In math.** The base-level learning equation:

```
B_i = ln( Σ_{j=1}^{n} t_j^{-d} )
```

where `n` is the number of past uses of chunk `i`, `t_j` is the elapsed time since
the `j`-th use, and `d` is the decay rate (conventionally `d ≈ 0.5`). A common
"optimized" approximation separates frequency from recency,
`B_i ≈ ln(n) − d·ln(L) (+ const)`, with `L` the chunk's lifetime (e.g. Petrov,
2006, on efficient approximation of this equation).

**What it predicts.**
- *Power-law forgetting.* For a single use, `B_i = −d·ln(t)`: activation falls
  logarithmically, and the retrieval function derived from it (§3) falls as a
  **power law of time** — the empirical form of forgetting (Wixted & Ebbesen,
  1991), and, per the rational analysis, a mirror of how *need probability* decays
  in the environment (Anderson & Schooler, 1991).
- *Rehearsal / practice boost.* Each additional use adds a `t_j^{-d}` term, so
  more (and more recent) uses raise `B_i`; the summation over separated uses is
  what produces spacing effects, and the frequency term echoes the power law of
  practice (Newell & Rosenbloom, 1981).

**How our L3 importance model re-derives it in our physics.** The original is
float-valued (`t_j^{-d}` with `d = 0.5` is irrational). We do not — and need not —
reproduce it numerically, because **only the *ordering* it induces over items and
the *retention threshold* bind our L3 gate** (importance-weighted coverage ≥ 850‰
at 10× budget: what matters is *which* items survive eviction, i.e. the top-budget
by importance, not the numeric activation). So we define an **activation-order-
preserving** importance in exact arithmetic over our integer logical time `t`.
With current time `T` and use-times `{t_1 < … < t_n}`, take the decay-1 (harmonic)
surrogate

```
w_i = Σ_{j=1}^{n} 1 / (T − t_j + 1)          (an exact fractions.Fraction)
```

which is strictly monotone in both **recency** (a recent use makes a denominator
small, dominating the sum) and **frequency** (more uses add more terms) — the two
things ACT-R's base-level predicts — while remaining float-free and byte-
reproducible. A general rational decay `d = p/q` is available by exact pairwise
comparison of the sums, but `d = 1` already preserves the recency×frequency shape
and yields power-law-shaped decay; ties are broken deterministically by
`(n, t_n, id)`. **We take ACT-R's *shape*, not its numbers**: the frozen float
constant `d = 0.5` is a fit to human data, and our gates read ordering and
thresholds, not activation magnitudes.

---

## 2. Spreading activation → Layer 2 (Recall), and the deterministic floor

Beyond base level, an ACT-R chunk's activation gets a **spreading** term from cues
currently in context: `A_i = B_i + Σ_j W_j·S_ji`, where the sources `j` are
elements in the buffers, `W_j` is their attentional weight, and `S_ji` is the
learned strength of association from `j` to `i` (often `S_ji = S − ln(fan_j)`, the
fan effect — Anderson, 1974). This grounds **cue-driven associative recall**: a
cue in context raises the activation of items associated with it, so retrieval is
what the cue *spreads to* — the theoretical ancestor of our L2 `recall(cue)`.

**Deterministic-floor note (liftable into `README-l2`).** Our L2 index deliberately
models only the *base-level and surface* half of this picture, **not semantic
spread.** ACT-R's `S_ji` are learned, real-valued associative strengths — graded
semantic relatedness accumulated from experience. Our deterministic index (token
n-grams, MinHash set-similarity) recovers a cue's target by **lexical / surface
overlap**, and it stops there: it does not estimate learned semantic association,
does not spread activation through a graded network, and assigns no float
strengths. This is intentional. Semantic spread is exactly the component that makes
recall model-dependent and non-reproducible (the failure our engine autopsies
found again and again — retrieval quality riding on an embedding model's whims);
excluding it is what makes L2 a **deterministic floor** — an LLM-free, exactly-
reproducible recall channel that a later layer may *augment* but must never
*depend on* for correctness.

---

## 3. Activation → retrieval probability / latency → Layer 6 (Meta-memory)

ACT-R maps activation to observable behavior through two equations:

```
P(retrieve i) = 1 / ( 1 + exp( −(A_i − τ) / s ) )      (retrieval probability)
     RT_i     = F · exp( −A_i )                        (retrieval latency)
```

A chunk is retrieved if its activation clears threshold `τ` (with logistic noise
`s`), and it comes back faster the more active it is (`F` scales latency). The key
point for us: **`A_i` is computed from the *structure* of memory** — how recently
and often the chunk was used, how strongly the current cues point at it — and that
structural quantity is mapped to a *probability of correct retrieval*. That is the
**ancestor of our L6 thesis**: confidence should be a function of *structural
evidence* (support count, recency, corroboration, cue strength), not a free-floating
guess. We record ACT-R's activation→probability map as **pedigree** for L6.

**Caveat (must be stated).** ACT-R's mapping is **fit to human data**: `d, s, τ, F,
S` are estimated to reproduce human latencies and error rates — it is a descriptive
model of people. **Our confidence is calibrated against trial ground truth**: we
score Brier / ECE / AUROC (§3.4) of our stated confidence versus *known-correct*
answers, not versus human reaction-time distributions. So we inherit the *form*
(confidence = f(structural evidence)) and reject the *objective* (fit-to-human);
our L6 gate is "well-calibrated to truth," which is a different and, for our
purposes, stricter target.

---

## 4. Soar: episodic snapshots and chunking → Layer 4 (and what stays out)

**Episodic memory → L4 (consolidation).** Soar (Laird, Newell & Rosenbloom, 1987;
Laird, 2012) records, automatically and without editing, **temporally-indexed
snapshots of working memory** — an episode per decision cycle (Nuxoll & Laird,
2007; 2012). Retrieval builds a partial cue and returns the best-matching episode
(feature-overlap plus a recency bias), then **reconstructs the full snapshot** from
that cue. Two things map cleanly onto us. First, Soar's deliberate architectural
split between an **episodic** store (raw, temporally-ordered snapshots — our
events) and a separate **semantic** store (de-contextualized facts) is precisely
the *episodic→semantic* direction our **L4 Consolidation** formalizes: deriving
schemas (entity summaries, attribute histories, action patterns) from the episodic
stream. Second, Soar's "reconstruct the whole episode from a partial cue" is the
same shape as our **L4 reconstruction-under-a-fidelity-floor** gate — recover the
answer from a compressed representation, and be honest about what cannot be
recovered.

**Chunking → deliberately out of scope.** Soar's learning mechanism, *chunking*
(Laird, Rosenbloom & Newell, 1986), fires when the agent hits an **impasse**,
solves it by subgoaling, and then compiles the successful problem-solving into a
new **production rule** that skips the impasse next time — it caches *procedure*,
learning how to *act* faster (and is known to risk over-general or "masking"
chunks, a cautionary parallel to our "generated-lineage must never be promoted to
observed fact"). **This is procedural learning, and it is out of scope by one
sentence:** our engine is a *memory*, not an agent that acts, so we consolidate and
revise *declarative* structure (what is remembered) and never compile new operators
(how to behave). We keep Soar's episodic/semantic architecture and leave its skill-
acquisition mechanism to systems that have a body to move.

---

## 5. The ladder ↔ cognitive-theory mapping (liftable into GAPMAP / README)

A half-page crosswalk from the memory-science canon to our nine layers and trial
classes. Use it to justify layer boundaries in GAPMAP and to head each layer's
README with its intellectual pedigree.

| Our construct | Cognitive-theory ancestor | What we take / what we drop |
|---|---|---|
| **L1 Retention** | Episodic vs. semantic memory (Tulving, 1972; 1983) — the raw, time-stamped record | Take: exact time-indexed storage. Drop: reconstructive distortion (ours is lossless at L1). |
| **L2 Recall** | Encoding-specificity / cue-dependent retrieval (Tulving & Thomson, 1973); spreading activation & fan (Anderson, 1974) | Take: cue→target retrieval. Drop: learned *semantic* spread (deterministic floor, §2). |
| **L3 Forgetting** | Base-level activation & power-law forgetting (Anderson & Schooler, 1991; Wixted & Ebbesen, 1991); power law of practice (Newell & Rosenbloom, 1981) | Take: recency×frequency *ordering* under pressure. Drop: the float `d`; only ordering + threshold bind (§1). |
| **L4 Consolidation** | Episodic→semantic split & episodic reconstruction in Soar (Nuxoll & Laird, 2007; 2012); semantic abstraction (Tulving, 1972) | Take: derive schemas from episodes; reconstruct under a fidelity floor. Drop: Soar chunking / procedural learning (§4). |
| **L5 Prospection** | Prospective memory — event- vs time-based; multiprocess framework (Einstein & McDaniel, 1990; McDaniel & Einstein, 2000); constructive simulation of the future (Schacter & Addis, 2007; Tulving, 1985, autonoetic "mental time travel") | Take: `intend(condition→event)`, event-cued triggers firing on future writes. Drop: subjective "autonoesis"; ours is exactly-once code. |
| **L6 Meta-memory** | Activation→retrieval-probability mapping (ACT-R; Anderson & Lebiere, 1998); metamemory / feeling-of-knowing | Take: confidence = f(structural evidence). Drop: fit-to-human parameters — we calibrate to trial truth (§3). |
| **L7 Generation** | Constructive memory / imagination reuses episodic machinery (Schacter & Addis, 2007) | Take: generation is a first-class, *tagged* act. Drop: blurring generated and remembered — provenance forbids it. |
| **Strain classes** | **Schacter's Seven Sins of Memory** (Schacter, 1999; 2001) | Each "sin" is a strain to induce and *score*, not a bug to hide (below). |

**Schacter's Seven Sins → strain classes** (the strain doctrine's pedigree):
- **Transience** (fading over time) → L3 strain: importance-weighted coverage must
  survive 10× pressure.
- **Absent-mindedness** (encoding/attention lapse) → ingestion / budget strain:
  what is refused under budget must be refused *honestly*.
- **Blocking** (retrieval failure, tip-of-the-tongue) → L2 recall strain: a valid
  cue that fails to retrieve is a scored failure, not a shrug.
- **Misattribution** (right content, wrong source) → **L7 provenance strain** — the
  exact failure our engine autopsies kept finding (source recorded, never bound).
- **Suggestibility** (implanted / externally-seeded memories) → **L7 self-pollution
  strain**: re-ingested generated content must never be promoted to observed fact.
- **Bias** (present beliefs reshape the past) → L6 calibration: stated confidence
  must track truth, not the engine's current summary.
- **Persistence** (intrusive memories that will not leave) → L8 Revision &
  Forgetting: the inverse failure — commanded, honest forgetting.

**One-line takeaways for GAPMAP §4.** (a) L3's importance model is ACT-R base-level
with the float replaced by exact recency×frequency ordering. (b) L2 is deliberately
the *base-level/surface* half of activation, never semantic spread. (c) L6 inherits
activation→probability but calibrates to truth, not to humans. (d) L4 is Soar's
episodic→semantic split; chunking (procedural) is out of scope. (e) L5 is
event/time-based prospective memory made exactly-once. (f) Schacter's seven sins
are a ready-made taxonomy for the strain class — one strain family per sin.

---

## Constitutional note (no law-change objection)

No objection to the frozen `BOUNDARY.md`. The cognitive canon *supports* the ladder
as written: it independently motivates L3's recency×frequency importance, L2's
cue-dependent recall, L6's structure-derived confidence, L4's episodic→semantic
consolidation, and L5's event/time-triggered prospection, and it hands us
Schacter's seven sins as a principled strain taxonomy — while confirming the two
places our physics must *diverge* from the human models (no floats: ordering over
magnitude; calibrate to truth, not to human data). Nothing here asks the sky to
change; it explains why the sky is shaped the way it is.

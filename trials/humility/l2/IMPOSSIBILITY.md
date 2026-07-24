# IMPOSSIBILITY.md — Layer 2 (Recall) humility

The structural argument for the Layer-2 humility ceiling, written against
`core/layers/README-l1.md`'s stated **non-capabilities**. The trial
(`t_recall.py`) enforces it; this file says *why* it must hold, structurally,
before any run.

## The claim

On Layer 2's own ascension tasks — recover a stored target from a content
**cue** against grammar-controlled distractors — the capped engine
`make_engine(layer_cap = 1)` (Retention, read-by-time only) scores **cue-C ≤
100‰**. Genuine Layer-2 recall must clear **cue-C ≥ 900‰**; the gap is the
capability.

## The structural argument

1. **Layer 1 has no content→`t` index — by its own README.** README-l1, *"What
   Layer 1 CANNOT express"*: *"There is no index from content to `t`. The only
   lookup keys are the logical time `t` and contiguous `t`-ranges. A query
   'which event mentions entity 7 / token X?' can only be answered by an
   external linear scan, not by the engine — through the interface it
   **abstains**."* The capped engine's entire query surface is `read(t)` and
   `read_range(t0, t1)`; **both are keyed by `t`, never by content.**

2. **The cue carries no `t`, so it addresses nothing the capped engine can
   use.** A cue is a partial payload probe — `{"entity":E,"key":K,"val":V}`.
   Chronicle payloads never contain `t` (grammar.md), and the task builder
   asserts every cue is `t`-free (`_l2tasks.cue_has_no_t`, re-checked in the
   scorer). README-l1 is explicit that L1's query path answers **by exact `t`**;
   therefore **any cue that leaked a `t` would be a leak** — the capped engine
   would simply `read(t)` and win. The tasks close that leak by construction, so
   the capped engine is handed a pure content descriptor and a query surface
   that accepts only `t`. It can do nothing but **abstain**.

3. **Distractors deny recovery by luck.** Each answerable target has a **unique**
   `(E,K,V)` fingerprint, but the store also holds ≥2 same-entity, ≥2 same-key,
   and ≥2 same-val distractors (enforced in `_l2tasks`). Even if the capped
   engine were permitted a single blind guess per cue — e.g. always return the
   most recent event, or a fixed `t` — the target is one specific event among
   many equally-plausible-by-any-single-atom distractors, so the expected hit
   rate is at the noise floor, far below 900‰. And it is not even permitted that
   guess through the interface: with no content key, the honest response is
   abstention, which recovers nothing (cue-C contribution 0) while keeping
   fidelity off the fabrication floor.

4. **Abstention scores nothing for coverage.** Under §3.0 an answerable query the
   engine abstains on scores 100 for **fidelity**, but coverage counts only
   **recovered** targets (correct answers, score 1000). A never-recovering engine
   therefore has **cue-C = 0‰ ≤ 100‰**, with no seed, store, or tie-break able to
   lift it — the ceiling holds by construction, not by measurement.

5. **Only an associative index closes the gap.** To reach cue-C ≥ 900‰ the engine
   must map a content cue to the `t` of the matching event **without being told
   the `t`** — i.e. maintain the content→`t` index README-l1 says Layer 1 does
   not have. That is precisely the Layer-2 capability the capped engine lacks.
   Hence the ceiling cannot be cleared without Layer 2. ∎

## Enforcement

- `_l2tasks` builds the cue tasks with `t`-free cues and the earned-overlap
  distractor guarantees; the scorer re-asserts no cue carries `t`.
- `trials/humility/l2/t_recall.py` runs the tasks against `make_engine(1)` and
  asserts cue-C ≤ 100, `recovered == 0`, and `fabricated == 0` — the capped
  engine recovers nothing and invents nothing.
- The same tasks drive `trials/ascension/l2/t_recall.py` against the full
  `layer_cap = 2` engine, where the identical construction must clear cue-C ≥
  900 — so the gate is shown to be load-bearing on one shared task set.

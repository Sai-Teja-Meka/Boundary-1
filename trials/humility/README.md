# trials/humility/

Humility is a **trial class**, not an abstention gimmick. For each layer `N`, the
humility trial takes **layer `N`'s own ascension tasks** and runs them, through
the same generic interface (`trials/adapters/INTERFACE.md`), against
**`make_engine(layer_cap = N−1)`** — the engine built with capability capped one
layer below.

It asserts the capped engine's scores are **at or below** the layer's declared
**humility failure ceiling** (`BOUNDARY.md §5`). This proves the ascension gate is
**load-bearing**: it cannot be cleared by the previous layer's capability alone.
If a `layer_cap = N−1` engine could pass layer `N`'s tasks, the gate would be
measuring nothing.

**Every humility trial ships an `IMPOSSIBILITY.md`** giving a *structural*
argument (not an empirical observation) for why the capped engine cannot exceed
the ceiling.

The per-layer fabrication ceiling of earlier drafts is **not** a constitutional
measure; it survives only as a component of the abstention-aware scoring
(`§3.0`) that Layer 6+ calibration relies on.

Populated alongside ascension trials, one layer at a time. Present:

- `l2/t_recall.py` + `l2/IMPOSSIBILITY.md` — the capped `layer_cap = 1` engine
  against Layer 2's cue tasks (ceiling: cue-C ≤ 100).
- `l3/t_forgetting.py` + `l3/IMPOSSIBILITY.md` — the capped `layer_cap = 2` engine
  against Layer 3's pressure tasks (ceiling: weighted-C ≤ 300).
- `l4/t_consolidation.py` + `l4/IMPOSSIBILITY.md` — the capped `layer_cap = 3`
  engine against Layer 4's Q1–Q4 battery at footprint 250‰ (ceiling:
  reconstruction F ≤ 400). Measured **0 / 302** where the ceiling allows 400 and
  the gate demands `C ≥ 850`, `F ≥ 900`. Its `IMPOSSIBILITY.md` is the first to
  carry an **information-theoretic** argument beside the behavioral one: the
  frozen Layer-3 `l4-seam` strain witnesses two streams differing only in
  evicted content producing byte-identical states, so thousands of evicted
  payloads map into a ≤ 35-cell aggregate record and reconstruction over the
  evicted set is unanswerable by pigeonhole — not merely unaffordable. §4 of
  that document records where each number was measured, including the one
  whole-stream run the suite does not carry and why.

- `l5/t_prospection.py` + `l5/IMPOSSIBILITY.md` — the capped `layer_cap = 4`
  engine against Layer 5's own P1/P2 battery (ceiling: `trigger-recall ≤ 50`).
  Measured **0**, on the whole 20 000-event stream through the generic interface
  — no prefix ladder is declared or needed, the capped engine here being the
  frozen Layer-4 one rather than Layer 3's `O(retained)` eviction path. Its
  `IMPOSSIBILITY.md` argues an **absence of machinery** rather than an absence of
  information, and says so: the `l4` pigeonhole is *not* borrowed, because in
  budget the capped engine holds all 945 intentions byte-exact and still scores
  0. The sharpest form is read off `§1.3` alone — a firing consumes a logical
  `t`, so an engine that fired anything ends past the caller stream, and this one
  ends exactly on it. **The corpus (`corpora/l5stream`) is PENDING**: no ruling
  binds it to the humility side any more than to the ascension side, and
  `ascension/l5/RULING-R6-DRAFT.md` clause 1 asks for both bindings together.

**Layer 1 has no humility trial** and never will: it is the floor, so there is no
lower layer to cap against. Its null-engine (`layer_cap = 0`) baseline lives in
`trials/ops/l1/t_capped0_baseline.py` as a sanity check (§5 L1, §6).

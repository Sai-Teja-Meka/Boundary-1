# core/layers/

Per-layer engine code, one module per claimed layer (`l1_retention.py`, …), each
with its own `README-lN.md`. A layer is laid down by the `FORGE` that first
builds it and claimed by the `ASCEND` that clears its gate.

Claimed layers:
- **Layer 1 — Retention** — `l1_retention.py` (`README-l1.md`). The honest floor:
  write / read-by-time / read_range / snapshot / restore, budget law binding.
- **Layer 2 — Recall** — `l2_recall.py` (`README-l2.md`). Associative
  `recall(cue)` via a deterministic index (field-qualified atoms, id-anchored
  n-grams, MinHash) that lives in state and counts against budget. Built on the
  frozen Layer-1 primitives; edits none of them.
- **Layer 3 — Forgetting** — `l3_forgetting.py` (`README-l3.md`). Principled
  eviction under 10× pressure: an exact ACT-R base-level importance ordering
  (grammar weight × distinct-reference count × harmonic logical-`t` recency), a
  total tie-break, a single-posting handle index, and an aggregated per-`t`-range
  forgetting record — all inside a budget the state-composition arithmetic of
  `README-l3.md §0` fixed before the code was written. Built on the frozen
  Layer-1 primitives; edits none of them, and does not edit Layer 2.
- **Layer 4 — Consolidation** — `l4_consolidation.py` (`README-l4.md`).
  Episodic→semantic derived schemas with reconstruction: every event is folded at
  the door into an interval chain (when it supersedes something) or a typed row
  against a learned shape (when it does not), and only if the fold **inverts** to
  the byte-exact payload; the episode is then released — *demotion*, GAPMAP S4
  form B, the debt `README-l3 §0.4` recorded — so at a quarter of the raw
  episodic footprint the whole semantic battery is answered exactly and
  reconstruction still returns 19 286 of 20 000 events. Built on the frozen
  Layer-1 primitives and the frozen Layer-3 eviction law; edits neither, and
  `make_engine(3)` **is** the Layer-3 engine (§7.4).

Once a layer is claimed its code is **frozen**: it is never edited (§9). A newer
layer builds on the frozen layers beneath it.

Per `CLAUDE.md §1`, every session reads the most recent layer's README
(currently `README-l4.md`) before acting.

# trials/strain/

Scale and stress trials over large corpora and dirty (**murk**) input. They
check that the four measures and the budget hold up under volume and injected
defects. Strain trials usually draw on murk (`corpora/murk/`, §8.7).

Includes the **mandatory Layer 7 self-pollution strain**: the engine re-ingests
its own generations three deep; provenance/lineage chains must survive, and
consolidation must never promote generated-lineage content to observed fact
(§6, §5 L7).

Present — laid down by the `ASCEND` that first needed them, and grown by `STRAIN`
moves as scale targets rise beyond the Phase-0 corpora (chronicle ~50k,
sessions ~5k, murk ~10k, l3stream / l3streamb ~10k each):

- `l1/t_corruption.py` — single-bit snapshot corruption, truncation, empty
  snapshots; every one caught loudly.
- `l2/t_recall_strain.py` — decoy-invariance (300 heavy decoys sharing no atom
  with the cue leave a fixed cue's ranking untouched), murk near-duplicate cues
  abstaining rather than fabricating, and index-vs-log divergence caught even when
  the checksum is recomputed.
- `l3/t_forgetting_strain.py` — importance-inflation flooding, murk near-duplicate
  pressure, determinism through ~9 000 evictions, the declared-safe permutation and
  the lawful order-dependence, and the Layer-4 seam **witness**: two streams
  differing only in the content of an evicted item snapshot byte-identically.

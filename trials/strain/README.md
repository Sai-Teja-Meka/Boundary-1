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
- `l4/t_consolidation_strain.py` — the two Schacter sins consolidation is heir to
  (**misattribution**: a derived answer must cite the assertion that carries it;
  **bias**: as-of must honour supersession rather than reading the present
  backwards), both on murk's 305 recorded contradictions and again under murk's
  full dirt at the footprint the gate is stated at; the **absent-mindedness**
  seed from `autopsy/GAPMAP.md §6` as a closing ledger (`demotions + forgotten +
  episodes held = events ingested`, and `forgotten` = exactly the events the
  engine cannot reconstruct); the **Form B** assertion, the ladder's thesis as a
  single trial — the cap-4 engine strictly beats the frozen cap-3 engine on
  `l3streamb` at Layer 3's own pressure cap; the inflation guard re-proved over
  the row codec; and determinism through demotion and forgetting.
- `l4/t_demotion_seam.py` — the demotion seam, two strains designed from measured
  field notes (`shell/dogfood/FIELD.md`) rather than from the layer's own prose.
  **Blocking** (the gap `PULSE`, `BOUNDARY.log` line 24, found in the seven-sin
  audit): at the ratified footprint on the binding corpus, demoted content is
  `t`-addressable and **not** cue-addressable — all 18 788 demoted events return
  byte-exact from `read(t)` while the cue channel reaches only the 498 held
  episodes, every blocked cue **abstains** and none is answered wrongly, and the
  held episodes are still recalled exactly so the loss is a channel and not a
  broken index. **Recorded-but-never-binding** (`autopsy/GAPMAP.md §2`'s engine
  thesis, turned on our own engine): a fold that does not invert regenerates
  nothing, so releasing its episode is a **loss** and never a demotion — the
  field note's reproduction, a key whose inversion dies after episodes under it
  were already released, and a mixed stream at and below the footprint where
  demotion, forgetting and chain-shedding all run. Red first, on all three
  sections; the engine fix that followed is `atlas_after`.
- `l5/t_prospection_strain.py` — prospection under pressure, repetition and dirt.
  **Absent-mindedness**, the *prospective* Schacter sin (`autopsy/GAPMAP.md §6`):
  under a budget that cannot hold the episodes an armed intention is never
  silently dropped — 765 fired + 180 pending = 945 ingested — a pending
  intention's own `intend` event comes back byte-exact from `read(t0)` while a
  fired one's abstains, and **that loss is booked**, so `forgot_at(t0)` carries
  it rather than the demotion counter keeping a booking that firing made false;
  plus the closing ledger over every logical time the engine ever assigned, the
  engine's own firings included, measured by reading all 20 765 of them. **The
  fired ledger binds** (`autopsy/GAPMAP.md §2`'s *recorded but never binding*,
  inverted — GA's expiration is written and read by nothing): the exactly-once
  mark is read on the satisfaction path *and* on the arming path, where an `iid`
  that has fired arms nothing because `§5 L5` names no re-arming, with a
  **ledger-blind reference policy** (a trial fixture, never engine code) reaching
  `dup-fire = 199` on the same stream to show the guard is load-bearing; and an
  unreadable condition arms nothing and never raises (§7.3 on the write path).
  **The demotion seam from the other side**: a `count_ge` fold fires exactly once
  at a cap where **not one episode survives**, and no counted event is answered
  as held. **Determinism** through arming, firing and the round trip, plus the
  declared `iid` order on a fixture that arms ten intentions in its exact
  reverse.

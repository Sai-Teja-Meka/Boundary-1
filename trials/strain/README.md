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
- `l5/t_prospection_blocking_seam.py` — the prospection blocking seam, the gap
  `PULSE` (`BOUNDARY.log` line 34) found in the Layer-5 seven-sin audit, closed in
  the form `l4/t_demotion_seam.py` established one layer down. **Blocking over the
  armed tier**: at the ratified cap on the binding corpus all 180 pending
  intentions return their own `intend` event byte-exact from `read(t0)` tagged
  `derive`, not one answers a cue built from its own payload, none is answered
  wrongly, and the 952 held episodes are still recalled exactly — so the cue
  channel reaches 952 of 18 724 answerable events, **51‰** against `strain/l4`'s
  26‰. **Blocking over the fired tier**: all 765 firings are regenerated by
  `read(t_fire)` and live in no index. The two causes are isolated rather than
  asserted, and they are **not** the budget: a payload is *cue-addressable or an
  intention, never both* (a handle field stops it arming), while a fired event
  carrying a handle field is still unreachable although an ordinary event
  carrying the same atom is reached exactly — the grammar closes one channel and
  the tier closes the other. **The kept-promise asymmetry**, `FIELD.md`'s
  2026-08-01 finding made behaviour in both directions: under pressure every
  fired intention's own episode is booked through the forgetting record with its
  count and its mass while the armed neighbour beside it regenerates byte-exact,
  and at a generous cap on the same frozen bytes it is **taken back** as a stored
  episode and nothing is forgotten — the two halves being the two defects the
  project has already committed (`BOUNDARY.log` line 26 and line 32). Plus the
  measured figures asserted against the `README-l5 §4` note that reports them
  (`R6` clause 3).

- `l6/t_calibration_seam.py` — **the calibration seam**, four strains on
  `corpora/l6batteryb` at `DEFAULT_BUDGET` (`§5 L6` states no footprint clause).
  **Bias**, the confidence half of the Schacter sin the post-L4 strain audit
  deferred to this layer in as many words (`BOUNDARY.log` line 24): injected
  contradiction into a **watched chain of the frozen forcing region** must move
  the emitted confidence *down* (500 → 333 → 250 → 200 as claimants accumulate)
  while a **verbatim repeat** must not move it at all, with a
  constant-confidence reference policy — a trial fixture, never engine code —
  measured beside it as the thing that does not move. **No manufactured
  errors**: the Layer-6 engine's `status` and `value` equal the frozen Layer-5
  engine's on all 2 400 queries, so the clean core carries 0 errors and the
  region carries exactly 100 — `AUROC`'s domain is fed by `R7` clause 3(b)'s
  theorem and never by sandbagging. **The denominator law under adversarial
  abstention**, `autopsy/GAPMAP.md §2`'s evaluator thesis inverted: four
  abstention patterns including one that consults the ANSWER KEY, and for every
  one of them `A` is exactly the answered queries, `A = n_pos + n_neg`,
  `A + abstentions = N`, and the per-class declaration rebuilds `A`; the hedger
  dies at `F 918` and not at the region trial, and a fabrication in a class
  declared outside enters `A` as an error. **The evidence under pressure**, the
  item `R7` left to Stage C: shedding drops a whole chain so a shed tie abstains
  rather than shrinking, but a set-once key **re-asserted after its chain was
  shed** would leave a confident engine behind — the `damaged` flag Layer 4
  already carries is what stops it, and the strain asserts its own scope, since
  neither Layer-6 artifact reaches the seam at all.

- `l7/t_self_pollution.py` — **`§6`'S MANDATORY LAYER-7 SELF-POLLUTION STRAIN**,
  the one trial the constitution names by procedure in its own frozen text
  (*"the engine re-ingests its own generations three deep, provenance/lineage
  chains must survive, and consolidation must never promote generated-lineage
  content to observed fact"*). **Suggestibility**, the seventh Schacter sin and
  the last uncovered one — structurally L7's, because its literal form requires
  an act no layer below 7 performs: the **caller** re-ingesting the engine's own
  output as ordinary fuel (`BOUNDARY.log` line 42). Run over
  `corpora/l7compose`'s own three-generation ladder, scored **at each rung**
  because a ladder checked only at depth 3 cannot say where a break occurred:
  `promotion = 0` at 1, 2 and 3, with 160 of 160 still reported generated and the
  store growing by exactly what the caller wrote (12 100 / 12 130 / 12 160). The
  engine's ledger is read through `§7` alone (`{"op":"lineage"}`) and required to
  agree **entity by entity** with the depth the artifact declares — `{1: 100}`,
  `{1: 100, 2: 30}`, `{1: 100, 2: 30, 3: 30}` at 200 / 260 / 320 cells under rule
  P — so an engine keeping a ledger of the right size and the wrong content goes
  red. The teeth are demonstrated on an **engine**: a ledger-blind fixture
  (`trials/_l7fixtures.py`, never engine code) that writes the ledger and refuses
  to read it promotes **100, then 130, then all 160**, the same triple
  `ATTAINABILITY.md §5.1` measured for the ledger-blind *policy*. And the finding
  no `§5 L7` clause states: measured against the store as it now is, the
  **byte-novel** share of the engine's own generations falls `60 -> 30 -> 0`
  while `tagging` holds and `promotion` stays 0 — at rung 3 a byte comparison
  would call this engine a liar about every item it made, which is why `R8`
  clause 3 binds novelty's denominator to what the engine **tags** and clause
  5(c) puts the capital crime on lineage.

- `l7/t_generation_seam.py` — the two seams `§4.2` opens when it wakes, on
  `corpora/l7compose`. **The inversion**: after the caller re-ingests generation
  1, all **30** depth-2 answers cite a `t` that is one of the engine's own items
  and the FROZEN `laws/t_provenance_schema.py` accepts all 30 — `R6` clause 2
  makes such a `t` an actually-ingested event — while **0** of them is reported
  as observed fact, the ledger-blind fixture reporting 100 at the same rung.
  `30` and `0` are the two halves of one finding (`R8` clause 5(c)), and a later
  session finding that validator green must not conclude the capital crime is
  covered. **The warrant the budget takes**, the question live since the kept
  promise (`BOUNDARY.log` line 34, `R7` clause 7, settled shape-only by `R8`
  clause 5(a)): on a declared ladder of six caps over a 6 000-event prefix where
  the engine loses up to 1 934 events and sheds chains, **not one cited `t` is
  unreadable at any cap** — the composition reading can only cite what it can
  still read, so the engine loses the *answer* before the *warrant* and
  generation degrades from 160 answers to 0 **by abstention**, with `forgotten`
  exactly the set of `t` it abstains on. The stronger property is stated as a
  fact about this engine and **not gated**: `R8` clause 5(a) demands *ingested*,
  and the support-recoverability rate is reported and binds nothing, so this file
  declares no `§5` constant and says why.

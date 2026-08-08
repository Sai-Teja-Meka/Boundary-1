# corpora/l8describe — the Layer-8 self-description artifact

The first **triple** in the sense of `BOUNDARY-HIGH.md §3`, frozen by the Layer-8
Stage-A session (`BOUNDARY.log` line 51). **No Layer-8 gate binds on it**: the
arithmetic is in `trials/ascension/l8/ATTAINABILITY.md` and
`RULING-R9-DRAFT.md` awaits human ratification.

| member | file | frozen by |
|---|---|---|
| the event stream | `l8describe.s11011.e3200.q74.json` (`stream`) | `§8.2` / `§8.3`, byte-match law unchanged |
| the query set + class table | the same object (`queries`, `classes`, `declared`) | the same object, for `corpora/l6batteryb`'s joint-property reason |
| the derivation procedure | `trials/_l8derive.py` | committed source in a file of its own (`§9.2`) |

`SEED = 11011` (outside `§8.5`'s holdout range), 3 200 events, 15 940 raw cells,
74 queries. Declared substrate configuration: `budget_cap = raw_cells // 3 =
5 313`.

## Why the answer key is a procedure

A self-description's correct answers are a function of **the engine under test**,
not of frozen bytes, so `§8.3` cannot reach them for want of a seeded generator
for an engine's behaviour. `_l8derive.py` maps *(this stream, an engine's
ingestion trace, an engine's canonical snapshot)* to the expected answer and is
**recomputed, not recorded**; its output's canonical bytes carry a recorded
`sha256` and `trials/ops/l8/t_l8describe.py` re-derives and compares it every
run. `§2.3`'s determinism is what makes that legitimate.

## The four classes

| class | n | what it asks |
|---|---:|---|
| `KR` | 28 | reachable folds — the state DETERMINES them |
| `KL` | 7 | lost folds the state nonetheless fixes (`§5 L4`'s counters are never decremented) |
| `KF` | 21 | lost folds the state only BOUNDS — the forcing region |
| `KU` | 18 | probes whose subject is not in the stream at all, for every engine |

**The forcing region** is the aggregated forgetting record's `(count, mass)`
against a **three**-member weight alphabet `(1, 3, 7)`: three unknowns, two
equations, uniquely solvable for some buckets and not for others. Measured at the
declared cap: 13 buckets at width 256, **one** determined and **twelve** not, 259
global compositions. It is `humility/l4`'s pigeonhole turned into a scored class.

## What this artifact CANNOT declare, and says so

Two properties a reader would expect the artifact to own turn out to belong to
the **(artifact, engine, cap) triple** instead, and both are `ATTAINABILITY.md`'s
findings rather than defects here:

* **which `KF` questions are forced.** Determinacy is a fact about the engine's
  record, so `R7` clause 3(b)'s *"a theorem the artifact carries"* cannot be met
  by these bytes alone.
* **which questions no field carries.** A bench of eight named single-field
  readers reaches 9 of the 38 determined questions; four are this artifact's own
  declared controls and five are field-answerable only because *this* engine at
  *this* cap lost only notes.

The sharper `KU` probe — *what was the content of the event at a lost `t`?* — is
deliberately **absent** for the same reason: which `t` an engine lost is not a
fact this artifact owns, and a class table declaring it unanswerable would be
declaring something it cannot.

## One engine-breaking finding, fixed rather than relaxed

The first draft put `importance` on `attr` payloads. Layer 4's rule is FOLD ONLY
WHAT INVERTS, an `attr` carrying a field `ASSERTION_FORMS["attr"]` does not read
does not rebuild from its facet, and the engine consolidated **nothing** —
`atlas[key] = None` on every key, and at the declared cap **3 200 of 3 200 events
forgotten with all 60 entities damaged**. The artifact was changed, not the
reading: `[L5]`'s unguarded-corpus precedent (`BOUNDARY.log` line 28) in its
Layer-8 form.

## Regenerating

```
python3 -m corpora.l8describe.generator --check    # byte-match
python3 -m corpora.l8describe.generator --write    # re-freeze (never routine)
```

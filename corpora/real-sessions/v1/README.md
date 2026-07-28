# `corpora/real-sessions/v1` — the transfer corpus

`[L4] [PACKAGE]`, 2026-07-26. The first **real-data** corpus in this project, and
the first fuel here that no generator produced.

```
real-sessions.v1.n25.jsonl   25 events, 158 828 bytes, canonical JSONL (§2.4)
MANIFEST.json                the checksum manifest §8.8 requires
```

`sha256 = ee9529c5cba539747e9254b2fc25c0c2cd5c17c31dc4def3ceedde2594cfd109`

## What it is

A frozen snapshot of this project's own accumulated **dogfood store**
(`shell/dogfood/store/store.json`) — the session summaries the project has
written about itself, one per remembered session, from `[L0] [FORGE]` to
`[L4] [STRAIN]`.

It is **already in fuel format by construction**, not by conversion. Every event
in the store was built by `shell/dogfood/event.build_payload` from a validated
session summary, so freezing it is a copy. The freeze asserted exactly that,
event by event, before writing a byte:

```
build_payload(summary_of_payload(p)) == p    for all 25 payloads
```

and `trials/ops/packaging/t_real_sessions.py` re-asserts it on the frozen bytes
on every suite run. A corpus that claimed to be fuel and was not would be the
quietest possible way to fake a transfer result.

## Why it is a legal corpus (`BOUNDARY.md §8.8`)

§8 binds every synthetic corpus to the **byte-match law**: re-run the generator
at the same `(seed, scale)` and the bytes must be identical. This corpus has no
generator, so §8.8 exempts it and binds it instead to its recorded **SHA-256
checksum**:

> *"A frozen, checksummed snapshot of real data is a legal corpus. It has no
> generator, so it is exempt from the byte-match law; instead it is bound by its
> recorded SHA-256 checksum … A real-data corpus ships a checksum manifest and is
> never edited."*

`corpora/registry.py::REAL` carries the entry, and
`laws/t_corpora_bytematch.py::trial_real_data_checksums` — which has stood ready
with nothing to check since Layer 3 — now hashes the file and compares it to the
manifest on every run. The manifest's number is the authority; the file is the
thing checked. Reading the checksum out of the file it is supposed to bind would
make the law vacuous, so `real_sessions.real_entries()` takes it from the
manifest and never from a fresh hash.

## The scrub

The freeze ran a scrub pass and **recorded it whether or not it found anything**.
It found nothing: **0 findings, 0 removals, 25 of 25 events frozen unmodified**.

Seven families were scanned, declared as data in
`corpora/real_sessions.py::SCRUB_PATTERNS` so the whole scrub is auditable
without reading code: `email`, `url`, `absolute_path`, `windows_path`,
`credential`, `long_hex`, `ipv4`.

Three things about that result are worth stating plainly rather than leaving as
a clean line in a manifest:

* **It is not luck.** A session summary is written into a validated schema whose
  text fields are prose about this repository's own files. There was never a
  mechanism by which a key or a home directory would enter one. The scrub is
  cheap insurance on a corpus that is about to travel, not a rescue.
* **It is a trial, not a claim.** `trials/ops/packaging/t_real_sessions.py`
  re-runs `scrub_report` over the frozen bytes every suite run. A later version
  frozen with a finding in it goes red; a scrub someone forgot to run is not a
  state this repository can reach.
* **The scrub reports; it never edits.** A finding stops a freeze and a human
  decides — the same discipline §9 applies to a frozen artifact anywhere else.
  Had it found something, this file would say what was removed and the event
  count would not be 25.

One near-match is recorded so a future reader does not rediscover it as a
surprise: the corpus contains the string `Recall@5` (a metric name quoted from
`autopsy/memoryagentbench/ANATOMY.md`). It contains an `@`; it is not an
address, and the `email` pattern correctly does not match it.

## Why `v1`, and what a later PACKAGE does

The store grows every session, so **any** snapshot of it is a snapshot as of a
moment. This one was cut at:

| | |
|---|---|
| store file sha256 | `be595ec15a83d393b9f08d2cbfb7231a645f06dba05b754fac3760b6f5151409` |
| store state checksum | `3e8d81fb5d95cae617facc2e44f44b21624f4c13001a42f3b2957c027242cb6b` |
| store `next_t` | 25 |
| repository commit | `595851edacb8e96cbd74462ccd59111d2c573532` |

§9.2 forbids editing a frozen artifact, so a later, larger snapshot is a **new
version directory** (`v2/`) with its own manifest and its own checksum. `v1`
keeps these bytes and this checksum forever. **Refinements re-freeze; they never
re-write** — which is also why the two remembers this very session adds to the
store are *not* in this corpus, and should not be: the corpus is what the store
was when it was frozen, and the log line that records the freeze is written
after it.

## What it is good for, and what it is not

It is the **transfer tier** of the scorecard: the same engine, the same scorers,
run on real fuel beside the synthetic corpora
(`python3 -m trials --engine ours`). Where the two diverge, the divergence is
published rather than hidden — and on this corpus they diverge sharply at
Layer 4, for reasons that are a property of the fuel and not of the engine.
`packaging/README-public.md` carries the numbers and the reading.

It is **not** a gate corpus, and no ratified threshold binds on it. It is 25
events written by one project about itself: too small to gate anything, and
about a subject the engine's designers were not neutral about. It is evidence
about *transfer*, which is exactly the thing synthetic corpora cannot supply.

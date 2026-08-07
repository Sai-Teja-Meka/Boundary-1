# `real-sessions/v2` — the freeze was ATTEMPTED and STOPPED

`[L7] [PACKAGE]`, 2026-08-07. **No `v2/` directory exists, and this file is why.**
`corpora/real_sessions.py::VERSIONS` still reads `("v1",)`; `corpora/registry.py::REAL`
still carries one entry; `v1`'s bytes, its manifest and its checksum are untouched.

The `PACKAGE` move was to repeat `v1`'s freeze procedure at current scale. The
procedure was repeated **exactly**, and it stopped where `v1`'s own README says a
freeze stops:

> *"The scrub **reports**; it never edits. A finding stops a freeze and a human
> decides — the same discipline §9 applies to a frozen artifact anywhere else.
> Had it found something, this file would say what was removed and the event
> count would not be 25."*
> — `corpora/real-sessions/v1/README.md`

The scrub found something. So this file says what it found, and the event count
is nothing, because nothing was frozen.

---

## §1. What `v2` would have been

Measured from `shell/dogfood/store/store.json` as it stood **before this
session's own ritual `remember`** — the same cut point `v1` used, and the same
reason (*"the corpus is what the store was when it was frozen, and the log line
that records the freeze is written after it"*).

| | |
|---|---|
| events | **50** — 47 `session_summary` + **3 `intend`** |
| canonical JSONL bytes | 601 257 |
| raw episodic footprint (`event_cost`, rule P) | 38 426 cells |
| would-be corpus `sha256` | `d1d964c5f074aa36c0b435a2614fa36b4aba919eacd39f238fae507d82769e59` |
| store file `sha256` | `1111d469e95376b2edd2c4c7b0cc5964c717cc9eb2a964893977e6273ab9d6ea` |
| store state checksum | `1c0f850289ee809502eb12c930c7f83233a0178e6fc6e135db58dc29781a45e6` |
| store `next_t` | 50 |

**It is fuel by construction, and that was checked before anything else**, per
kind, because the store now carries **two** declared kinds where `v1` carried
one:

* `session_summary` — `event.build_payload(event.summary_of_payload(p)) == p`,
  47 of 47;
* `intend` — `l5.rebuild_intention(p["iid"], p["cond"], p["fire"]) == p` and
  `l5.arms(p) is not None`, 3 of 3.

So the corpus is a copy and not a conversion, exactly as `v1` is. What it is not
is frozen.

---

## §2. THE STOP — one scrub finding, and what it is

```
family   long_hex
match    ee9529c5cba539747e9254b2fc25c0c2cd5c17c31dc4def3ceedde2594cfd109
why      "a 32+ hex run is a checksum, a key or a full commit sha; none of the
          three belongs in prose a corpus carries"
where    store t = 25 — the `[L4] [PACKAGE]` session summary, in the decision
          that records the freeze of v1
```

The decision reads, in full:

> *"corpora/real-sessions/v1 frozen under §8.8: 25 events, 158828 bytes, sha256
> ee9529c5…cfd109, cut from store sha256 be595ec1 at commit 595851e; the
> byte-match law's checksum branch, ready since Layer 3, is now live"*

**The match is `v1`'s own corpus checksum.** It is not a credential, not a host,
not a path, not a person: it is this repository's own published number, printed
in `v1/MANIFEST.json`, in `v1/README.md`, in `packaging/README-public.md` and in
`BOUNDARY.log`. It is a **true positive of the pattern and a false positive of
the purpose**, and it is exactly one of them in 601 257 bytes.

Three things about it are worth stating rather than leaving in a diff.

* **The sharpest detail is the inconsistency, not the string.** That one
  decision names three checksums and **shortens two of them** — `be595ec1` (8
  chars) and `595851e` (7) — and writes the third in full. So the corpus does
  not carry a habit; it carries one line where a habit lapsed. And the session
  that wrote that line is the session that wrote the scrub.
* **It is the store's own theme arriving at the freeze procedure.**
  `shell/dogfood/FIELD.md`'s standing first note is *"the store is exactly as
  wide as its source"*. A project whose sessions write about freezing its own
  artifacts writes those artifacts' checksums into its own memory — and the
  scrub cannot tell that hex from a key, because nothing in a 64-character hex
  run says which it is.
* **`v1`'s README anticipated a finding and anticipated the wrong shape of
  one.** It says *"this file would say what was removed"*. Removal is not
  available here: the string is not a secret, and dropping the event that
  carries it would make the corpus stop being a snapshot of the store — which is
  the one property `trial_the_corpus_is_fuel_by_construction_not_by_conversion`
  exists to hold. So the procedure has a case it did not have a branch for.

**No session may resolve it**, and the three ways a session could have are each
refused here with the reason:

| what a session could do | why it is not a session's to do |
|---|---|
| freeze anyway | a frozen corpus is immutable forever (§9.2). Freezing over a live scrub finding is the one irreversible move on this list |
| drop or redact the event | *"the scrub reports; it never edits"*, and a corpus that dropped an event would not be the snapshot the whole transfer tier's honesty rests on |
| narrow `long_hex` so it does not match | relaxing the instrument to admit the finding. This repository's whole discipline is the other way round: **fix or withdraw, never relax** — `BOUNDARY.log` counts twenty-two engine-breaking findings under that rule |

---

## §3. THE SECOND COST, found while preparing the freeze

This one is not a blocker on its own, and it is recorded because it is the part
a human deciding §2 needs and could not otherwise know: **freezing a `v2` moves
a number a FROZEN Layer-7 trial asserts.**

`trials/_l7tasks.py::_substrate_rows` — Stage-A code, frozen at `[L6] [RULING]`
— reads the REAL corpus through a **late-bound default**:

```python
if real_sessions.real_entries():
    payloads = real_sessions.payloads()          # -> LATEST
    out.append(("real-sessions/v1", payloads, list(payloads), ...))
```

When it was written there was one version, so `payloads()` *was* `payloads("v1")`.
Add a `v2` and `LATEST` moves, and two things happen at once:

* the row keeps the label `real-sessions/v1` while carrying `v2`'s payloads;
* `trial_no_frozen_artifact_carries_a_generation_required_query` asserts
  `require_equal(total, 85954)` on the surveyed answerable population, and the
  total becomes `85954 − 25 + |v2|`. At the 50 events measured above that is
  **85 979**, and the suite goes red.

**The finding it would go red on is not the finding it is measuring.** The same
instrument reads `absent = 0` on the live 50-event store — measured, not assumed
— so `v2` falls squarely inside `R8` clause 1's refused class and forces no
composition. What would move is the *population*, not the *property*: the fifth
substrate kill is unshaken and the trial that guards it would fail for a reason
its own docstring does not name (*"a corpus frozen later that DID force a
composition would go red here"* — this one would not).

That is a real seam and it has exactly one clean resolution, which is again not a
session's to take: whoever authorizes the freeze should also say whether the
Stage-A fixture is **pinned** to `v1` (a one-token change that preserves the
frozen measurement precisely, leaving `85954` describing the same 25 events it
always described) or whether the survey is meant to grow with the stock and the
frozen assertion is meant to be superseded by a ruling. `[L7] [PACKAGE]`
deliberately did **neither**, because both are decisions about a frozen artifact.

`trials/ops/packaging/t_real_sessions_v2.py` asserts the arithmetic of this seam
on every suite run, so the figure a decision would be taken against cannot go
stale between now and then.

---

## §4. What was delivered instead

The transfer re-run the freeze was for did not need the freeze, so it was run and
published — **out of suite**, on the store as it stood at 50 events, and labelled
as such wherever it appears. `packaging/README-public.md` carries the table and
the reading; `v1`'s frozen numbers stand beside it unedited and are still the
only transfer numbers any trial re-measures, because they are the only ones bound
to bytes that cannot move.

The finding, in one line: **five more layers of session history did not make the
store a better corpus for the upper layers — it made the reasons they are
ungradable on it sharper, and it cost the store its first two unreachable
memories.**

---

## §5. Where this is enforced

* `trials/ops/packaging/t_real_sessions_v2.py` — that the scrub over the
  committed store still finds **exactly one** thing, of family `long_hex`, whose
  match is `v1`'s own recorded manifest checksum and whose event is the
  `[L4] [PACKAGE]` summary; that `VERSIONS` is still `("v1",)` and `REAL` still
  holds one entry, so no `v2` was frozen quietly; that this document exists and
  names the family and the store `t`; and §3's arithmetic, against
  `_l7tasks.substrate_survey()` itself.
* `trials/ops/packaging/t_real_sessions.py` — `v1`, unchanged, including its own
  scrub which still finds nothing in the frozen bytes.
* Nothing here gates a score. No ratified number, ceiling or corpus binding
  moves, and `corpora/registry.py::REAL` is exactly what it was.

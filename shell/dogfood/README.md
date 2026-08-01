# shell/dogfood — the engine as its own memory

`[L2] [DOGFOOD]`, first run. This is the adapter that makes Boundary-1 the memory
of the project that is building it. One session is one event; the whole store is
this project's history, held by the engine the history is about.

The shell does the I/O and the engine stays pure (§2.2, §2.6): `shell/` imports
`core/`, `core/` never imports `shell/`. Persistence lives here, as a state file.
No engine code was changed to make this work.

```
python3 -m shell.dogfood remember --move DOGFOOD --log-line "[L2] [DOGFOOD] …"
python3 -m shell.dogfood remember --json -        # a summary as JSON on stdin
python3 -m shell.dogfood recall graphiti bitemporal
python3 -m shell.dogfood intend --when-kind attr --when-key layer --when-val-ge 6 \
    --about trials/adapters/INTERFACE.md --surface "…"   # a promise
python3 -m shell.dogfood consolidate              # the Layer-5 derived view
python3 -m shell.dogfood consolidate --budget 8000 --cue "graphiti bitemporal"
python3 -m shell.dogfood status
```

Exit codes: `0` success — **including an abstention**, which is a correct answer
(§3.0); `1` usage/schema error; `2` the state file failed its integrity check;
`3` the write was refused by the budget law (§4.1). `remember` prints the
engine-assigned `t` on stdout and its bookkeeping on stderr, so
`t=$(… remember …)` is legal.

## The event

The schema follows the `corpora/sessions` grammar's shape — a `kind`-tagged
object of integers and strings — with the session-summary fields:

```json
{"kind":"session_summary","project":"…","move":"…","decisions":["…"],
 "files_touched":["…"],"open_questions":["…"],"log_line":"…","tok":{"…":1}}
```

`t` is never in the payload: it is engine-assigned and engine-owned (§1.3).

`tok` is the **cue surface**, and it is the one piece of shaping the shell does.
Layer 2 answers only when one stored event contains the whole cue probe, and a
probe is a partial payload — so a free-token cue like `graphiti bitemporal` is not
expressible against prose fields, because nothing in the payload is keyed by a
bare word. `tok` gives it one: the set of normalized tokens of every text field.
Two details are forced by the engine, not chosen:

* **an object, not a list** — the index flattener index-qualifies list items
  (`tok.0=graphiti`), which would make a cue position-dependent; an object yields
  the position-free atom `tok.graphiti=1`;
* **a constant `1`, not a count** — a cue carries `1`, so an event carrying `3`
  would be a different atom and would miss. `tok` is a set, and says so.

A cue is then exactly what the engine already implements — the conjunction of its
atoms — and the shell computes no scores of its own.

Normalization is deterministic and library-free (no `re`, no stemmer): lowercase,
split on every character outside `[a-z0-9]`, keep runs of ≥ 2 characters. The
same function runs on both sides, so what a summary was written with is exactly
what it can be found by.

`move` is validated as a non-empty string, **not** against the §9.1 move set:
`BOUNDARY.log` carries `FORGE-CORRECTION` and `THEORY`, which that set does not
list. A store that refused its own project's history would be the wrong kind of
strict.

## Decision 1 — the budget

`DOGFOOD_BUDGET = 2**24 = 16,777,216` work units, chosen once at store creation
and thereafter part of the state (`shell/dogfood/store.py`). The engine's own
`DEFAULT_BUDGET` is a trial-scale number; a store meant to outlive the project
deserves a considered one.

The arithmetic. Measured over the 13 backfilled log events — payload cells plus
index cells, the accounting of §4.1 — one event costs **min 68, mean 258, max 490**
work units. Budget a deliberately fat **4,096 units per event**, eight times the
largest real one, room for a session summary many times longer than any written
so far:

```
16,777,216 / 4,096 = 4,096 events   ≈ 11.2 years at one session per day
16,777,216 /   490 = 34,239 events  ≈ 93 years at the observed worst case
16,777,216 /   258 = 65,027 events  ≈ 178 years at the observed mean
```

At the actual cadence of this project — a few sessions a week — the fat estimate
alone is a lifetime of headroom. The cap is a power of two, exact, integer, and
never a float.

When it does bind, it binds honestly: the budget law **refuses** the write and
evicts nothing (§4.1). The CLI exits `3` and says so. Layer 3 will be the layer
that can do something better than refuse; until then, refusal is the honest
answer, and a store that fills is a signal to ascend, not to quietly drop the
oldest session.

## Decision 2 — where the state file lives, and what it is

`shell/dogfood/store/store.json`, inside the repository. The project's own memory
belongs in the project's own history: it is reviewable in a diff, it travels with
a clone, and a session that reads it needs nothing but the checkout.

**It is not a frozen artifact.** §9.2 freezes old layers, frozen trials, frozen
corpora, anchors, and `BOUNDARY.md`. The store is none of those. It **grows by
use** and is committed with each session, and its bytes change every time.

**It is engine-owned.** The file is exactly `snapshot(state)` — canonical JSON,
sorted keys, no trailing newline — so `sha256(file)` is a checksum of the state
itself. It is written only by `remember`, only through the engine, and it is
**never hand-edited**. There is no need for that rule to be enforced socially: a
hand edit changes the body without changing the envelope checksum, and the next
command refuses to run (below). Nor is it a corpus — §8's byte-match and
real-data doctrines govern corpora, and the store is neither generated from a
seed nor a frozen snapshot of anything.

> **2026-07-26 note (`[L4] [PULSE]`) — the alignment below has lapsed, exactly as
> the paragraph said it could. It is recorded, not repaired.**
>
> `BOUNDARY.log` line 20 — `[L3] [ASCEND] layer-4 consolidation, STAGE A` — was
> committed without a `remember`, so the store has no event for it. Measured this
> session: 23 log lines, 22 stored events. `t = line − 1` holds for `t ≤ 18`
> (log lines 1–19); from `t = 19` onward the offset is **2** (`t=19` ↔ line 21,
> `t=21` ↔ line 23).
>
> **The resolution is documentation, and the paragraph below already contains
> it:** `t` counts **remembered sessions**, and only ever did. The equality with
> the log line index was a *ritual convenience* — true while the ritual held,
> never enforced, never an invariant, and never depended upon by any trial or by
> `recall`. Nothing is wrong with the store and nothing is wrong with the log:
> the store is a complete, correct record of what it was told, and the log is a
> complete, correct record of what was done. They are simply two ledgers with two
> different counts, and no code has ever assumed otherwise.
>
> **What is NOT done, deliberately.** The gap is not backfilled. Writing a
> Stage-A event now would give it a `t` above the sessions that followed it,
> making the store's one real ordering guarantee — ingestion order — a lie in
> order to rescue a convenience that was never load-bearing. §1.3 owns `t`, and a
> late insert is not something the engine can express. The lapse stays visible.
>
> **What a reader should do instead:** join on the `log_line` field, which
> carries the line's own text, not on arithmetic between two counters. The bolded
> equality below should be read as history — true from `t=0` to `t=18` — and not
> as a property of the store.

One property worth keeping: because the backfill walked `BOUNDARY.log` in order
and every session from now on remembers its own line before committing, **event
`t` equals the log line index**. The store does not enforce that — the ritual
does. If a session ever commits without remembering, the alignment is gone and
the store is still correct; it is a convenience, not an invariant.

## Decision 3 — corruption fails loudly

`restore` raises `CorruptSnapshot` on any corruption — a flipped bit, a
truncation, a tampered payload, an index that diverges from the log (README-l1,
README-l2). The shell surfaces that as `StoreCorrupt` and the CLI stops:

```
FATAL: the dogfood state file failed its integrity check.
  path:   shell/dogfood/store/store.json
  reason: snapshot checksum mismatch (corruption detected)
The Layer-1 checksum law fails loudly (README-l1): a store that does not verify
is never silently re-initialized, repaired, or ignored. Restore it from git
history (git checkout -- shell/dogfood/store/store.json) or delete it deliberately.
```

Exit code `2`, nothing written, nothing answered. **There is no silent re-init
path in the code** — not a fallback, not a `--force`, not a repair mode. A
memory that quietly starts over when it cannot read itself is worse than one that
stops, because it looks identical to one that never had anything to say.

A **missing** store is not a corrupt store: `remember` initializes a new one and
announces it on stderr; `recall` and `status` say there is nothing yet and exit
`1`. Only a file that exists and does not verify is fatal.

## recall, and why it abstains so often

`recall` asks the engine and prints what it says. A hit prints the match with its
`t`, its confidence in permille, its provenance tag, and the summary formatted to
paste into a session preamble. Everything else prints an **explicit abstention**
— never empty silence (§7.3) — diagnosed into the two honest Layer-2 boundaries:

* *no stored event carries `<token>`* — the cue misses;
* *N stored events carry the whole cue, and Layer 2 answers only when exactly one
  does* — the cue is ambiguous, and all N are listed.

Both cases also print the per-token document frequencies, and the miss case
prints the nearest events by cue overlap. Those listings are labelled **"context,
not an answer"**, and they are not the engine's answer: the engine abstained, and
the shell does not launder that into a guess. The diagnosis itself is
engine-derived — a single-token cue's `recall_ranking` *is* that token's posting
list — so the shell re-implements no index logic.

Abstention is not failure here. Under §3.0, knowing that you do not know is worth
exactly as much as knowing; the CLI exits `0`.

## consolidate — the Layer-4 derived view (`[L4] [DOGFOOD]`)

`remember` writes episodes and `recall` finds one of them. `consolidate` answers
the third question a memory owes its owner — *what does all of it add up to?* —
by folding the store's session summaries through
`core/layers/l4_consolidation.py` and reading the result back through the
**ordinary query interface** (§7.1): `current`, `asof`, `profile`, `count`,
`consolidation`, `forgetting`, `read`, `recall`. The shell computes no answer of
its own; it asks, labels, and formats for pasting into a session preamble.

Three sections, and each is a §5 L4 capability rather than a rendering choice:

* **per-project summary** — `profile(entity)` and `count(kind)`: how many
  sessions the project has, and how many facts they asserted. The profile is the
  fold Layer 4 calls Q3, and it **abstains** rather than undercounting if a chain
  of that entity was ever shed (`README-l4 §0.3`).
* **decision history** — `current(entity, key)` for the value in force, and
  `asof(entity, key, t)` walked forward for where it changed. The chain is read
  out of each answer's own **provenance `support`**, so the history is the
  sequence of assertions the engine says carry it, not a sequence the shell
  reconstructed. Consecutive equal values are folded into the `t` they were first
  decided at, with the restatements counted rather than dropped.
* **open-question aggregate** — the same `asof` walk over the `open_question`
  chain, which is every question every session left open, in order.

### The shell declares a reading, exactly as the engine does

Layer 4 folds an event into a supersession chain only when its payload reads as
an `(entity, key, value)` assertion under the frozen `ASSERTION_FORMS` — *"a
declared reading of the frozen chronicle-family grammars"* (`README-l4 §1`). A
session summary is not in that grammar and never will be: it is prose, and the
facet map is frozen (§9.2). So the reading of a **session** into assertions is
declared in `consolidate.py`, in the shell, which is where a reading of a human
grammar belongs (§2.6) — the same move `tok` already makes for the cue surface.

One session becomes its own episode plus one `attr` assertion per fact it states
about its project: `layer` (from the `[L<n>]` tag), `move`, `suite` and `anchors`
(from the `<…: …>` tags), the three field counts, and one `open_question` per
question. Each is emitted in exactly the engine's own form —
`{"kind":"attr","entity":<int>,"key":<str>,"val":<scalar>}` and nothing else —
which is what makes it **invertible**, so `read(t)` regenerates it byte-exactly
after its episode is gone and `profile` attributes it to a grammar kind instead
of abstaining. A fact the summary does not carry is not asserted: a log line with
no `<suite: …>` tag states no suite, and none is invented for it.

### Nothing derived is ever written back

The derived stream is built on demand and thrown away. It is **not** ingested
into the store, and `remember` is still the store's only writer. That is a
deliberate refusal, and the autopsies are the reason: `autopsy/mem0/ANATOMY.md`
records a store in which an inferred fact and a user-stated fact are
indistinguishable once written, and §5 L7's self-pollution law exists because a
memory that promotes its own derivations to observed fact has stopped being a
record. A view recomputed from the episodes cannot drift from them; a derived
event committed beside them can.

The price is stated rather than hidden: **the store's own state file stays a
Layer-2 ledger** (`status` still prints `layer_cap 2`), so consolidation is
something the project's memory *can be asked for* and not something it *is*.
`FIELD.md` records that as this run's chafe.

### `--budget`: the only way to see demotion here

The store is 23 events against a 2²⁴-unit cap, so nothing is ever evicted and the
derived view at the default cap shows `demotions 0`. `--budget UNITS` replays the
same episodes under a smaller cap, which is how the demotion seam is measured
out-of-suite (the command and the numbers are in `FIELD.md`):

```
python3 -m shell.dogfood consolidate --budget 8000
```

The report then separates the two channels using the engine's own provenance —
`kind == "recall"` when an episode is still held, `"derive"` when it was
regenerated from a chain — which is `README-l4 §4`'s non-capability turned into a
number.

## intend — the promise (`[L5] [DOGFOOD]`)

`remember` writes what a session did, `recall` finds one of those events and
`consolidate` says what all of them add up to. All three are folds over the past.
`intend` is the first thing this store does that faces the other way: **a
condition written now, evaluated against every session summary written
afterwards, and a payload surfaced when one satisfies it — once.**

```
python3 -m shell.dogfood intend \
    --when-kind attr --when-key layer --when-val-ge 6 \
    --about  trials/adapters/INTERFACE.md \
    --surface "…what to say when it fires…"
```

The division of labour is the one `consolidate` already draws, and it is the
whole design: **the shell declares the reading, the engine keeps the promise.**

### An intention is an event, in the engine's own form

`§7.1` declares three operations and `§1.1` says events are the only fuel, so
`intend` is no more a fourth verb here than it is in the engine
(`core/layers/README-l5.md §1.1`). The stored payload is the frozen `intend`
shape and **nothing else**:

```json
{"kind":"intend","iid":<int>,"cond":<AST>,"fire":<payload>}
```

Not a shell schema translated later. `README-l5 §1.2` arms an intention only when
the payload rebuilds from `(iid, cond, fire)` as canonical bytes, so a fourth
field — a `tok` cue surface, the project's name, a note about who declared it —
would stop it arming at all. The consequence is a real one and is stated rather
than hidden: **a promise is `t`-addressable and not cue-addressable.** `recall`
cannot find it; `FIELD.md` carries the note.

The write path is `remember`'s: one store, one writer, one budget law, and the
same exit codes (`3` on a refusal). What is different is the last step —
after writing, the shell **replays the store and asks `§7.1` whether the
intention is pending**, because the engine decides what arms and a shell that
reported success without asking would be reporting its own intentions.

### The declared reading, narrower than the grammar on purpose

The engine's condition vocabulary is six predicates and three connectives. This
shell admits a strict subset, and every narrowing is a fact about what
`consolidate.py` emits (`shell/dogfood/intend.py` states each one):

| narrowing | why |
|---|---|
| `and` over atoms only — no `or`, no `not` | `not` is what makes GUARDEDNESS a question; refusing it makes a cascade impossible **by construction** |
| at least one guard atom (`kind` / `entity` / `key`) | each is false of a `reminder`, so no payload this shell fires satisfies any condition it admits |
| `loc` refused | a session summary has no `loc`, so such a promise could never fire |
| `key` / `kind` / `count_ge`'s `k` checked against the reading | a condition over a key nothing writes is the same silent promise |

Everything admitted is then handed to the engine's own `readable`, which is the
authority: **the shell narrows, it never widens.** A condition outside the
reading is a usage error at declare time (exit `1`, nothing written) rather than
an intention that waits forever for a fact no one will ever assert.

`--when-count-ge KIND:N` is the one that spans the consolidation boundary: a fold
over the Layer-4 per-kind counters, two cells per kind and never decremented, so
it **outlives the episodes it counts**. `FIELD.md` records that measured.

### Where a firing surfaces

Nowhere new. `§7.1` returns it and the shell prints it, so both `consolidate` and
`recall` end with the promises section and nothing else in the shell produces
prospection output:

```
prospection — the promises this store is keeping
  declared         1 intention — 1 pending, 0 fired (26 + 0 cells)
  iid 1   declared at store t=31   PENDING
      surfaces  reminder about trials/adapters/INTERFACE.md — …
      when      kind=attr and entity=1 and key=layer and val>=6
```

`{"op":"fired","iid":I}` is the exactly-once ledger and it answers with a **list**
— `dup-fire = 0` is a ratified gate clause, so an intention that fired twice has
to be visible through the query interface and not only in an engine's own
bookkeeping. The shell prints what comes back and never collapses it to its first
element. A store that has declared no intention skips the replay entirely and
prints nothing.

### The store is a ledger of promises; the view is what keeps them

The state file is still a **Layer-2 ledger** (`status` still prints `layer_cap
2`), and it still holds only what it was told. An intention sitting in it is
inert: the arming, the watching and the firing all happen in the **derived
replay**, which is recomputed on demand and thrown away — for the reason
`consolidate` gives, that committing a derived event beside a remembered one is
the mem0 defect the autopsy names and the §5 L7 self-pollution law forbids. A
firing is therefore a *fact about the store*, re-derived identically on every
read, and never a row somebody could edit. `FIELD.md` records the chafe that
comes with it.

### The seed

The first promise this store keeps is one the project actually made: `iid 1`,
declared at store `t=31`, fires when a session summary first asserts `layer = 6`
and surfaces the **`INTERFACE.md` attribute gap** — the adapter contract's
unstated requirement that `state.occupancy` and `state.budget_cap` are read as
plain attributes, found at `[L4] [PACKAGE]` by writing
`trials/adapters/external/reference.py` against that document alone and recorded
in `trials/adapters/README.md` because §7 is frozen. Layer 6 is where the next
shared scorer is written, which is exactly when someone needs to be told.

## Backfill

`python3 -m shell.dogfood.backfill` parses `BOUNDARY.log` into one summary per
line and prints them as JSON; the operator pipes each into `remember`, so
`remember` stays the only writer and a backfilled event travels the same schema
validation, the same tokenizer, and the same budget law as a live one. What is
derived and how honestly is documented in that module's docstring; the short
version is that `log_line` is verbatim, `decisions` is a mechanical `;`-split of
the prose, `files_touched` is a conservative path extraction, and
`open_questions` is **always empty**, because the log never recorded them and
inventing them would be fabrication.

## The ritual gains a step

From the next session onward, the closing step of every session is:

```
python3 -m shell.dogfood remember --move <MOVE> --log-line "<the BOUNDARY.log line>" \
    [--decision …] [--file …] [--question …]
```

before the commit, so the store and the log stay in step and the next session can
recall what this one decided. `git add shell/dogfood/store/store.json` — the
store is committed with the move it records.

## Files

| file | what it is |
|------|------------|
| `event.py`    | the session-summary schema, the tokenizer, the cue surface |
| `store.py`    | the budget, the state-file location, load/save, corruption |
| `consolidate.py` | the declared reading of a session into `attr` assertions, the Layer-5 replay, the derived-view report |
| `intend.py`   | the declared condition vocabulary, the promise's schema, guardedness |
| `cli.py`      | `remember` / `recall` / `intend` / `consolidate` / `status`, and all rendering |
| `backfill.py` | `BOUNDARY.log` → session summaries (writes nothing) |
| `store/store.json` | the state file: engine-owned, committed, never hand-edited |
| `FIELD.md`    | what chafed, in use |

Trials: `trials/ops/dogfood/` — `t_intend.py` covers the declared reading's
narrowings, GUARDEDNESS over the whole cross product of declared conditions and
declared fire payloads, the stored form (and what a fourth field costs it),
exactly-once firing at the first satisfying session, the `1 + f` `t`-accounting of
`R6` clause 2, a `count_ge` fold surviving the demotion of everything it counts,
and the committed store's own promises; `t_dogfood.py` covers schema validation, a round
trip through a real temp state file, abstention output shape, corruption → loud
failure, and a read-only check that the committed store still restores;
`t_consolidate.py` covers the declared reading's invertibility against the frozen
facet map, the derived battery through `query` alone, as-of under supersession,
the demotion measurement (content kept, cue lost, session summaries never
demoted), and that `consolidate` is read-only on the store. Shell code is
testable; it is only `core/` that must stay pure.

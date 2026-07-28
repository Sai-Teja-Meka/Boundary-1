# HONESTY.md — the claims discipline

`[L4] [PACKAGE]`, 2026-07-26. Read this before citing anything in
[`README-public.md`](README-public.md).

Every autopsy in this repository convicted a system of the same thing: writing
down the metadata that would have made it correct, and then never reading it
where it counted (`autopsy/GAPMAP.md §2`). A benchmark's version of that sin is a
claim nothing checks. This file is the claim ledger, and the rule it runs on is
simple: **anything stated here that could be a trial, is one.**

---

## 1. What this is

**An executable correctness specification for memory.** Nine capability layers in
a fixed order, each with a ratified threshold, each with a structural argument
that the layer below it cannot pass — and all of it as running code, not prose.
The specification is the trial suite. If the spec and a document disagree, the
suite is right.

**A deterministic reference floor.** Every measurement is exact-integer or exact
rational arithmetic, byte-identical on every platform and every run, with no
model anywhere in the loop and no third-party dependency at all. Where the
literature grades by token overlap or by an uncached call to a hosted model, this
grades by code you can read, on corpora that regenerate byte-for-byte from a
seed. That is a *floor*, deliberately: it says what any system must at least be
able to do, exactly, before fuzzier grading is worth arguing about.

**A teaching artifact.** The layer READMEs state what each layer *cannot* express
as carefully as what it can, every gate carries its arithmetic before it carries
an engine, and two failed ascensions are in the log with their numbers. The
mistakes are the pedagogy; they are not cleaned up.

## 2. What this is not

**Not a production memory library.** There is no server, no persistence layer
beyond one JSON snapshot, no concurrency, no eviction tuned for a workload, no
API stability promise. The engine holds a few thousand events under a hard cell
budget and is measured on corpora of tens of thousands. Do not put it behind a
product.

**Not a neural-retrieval competitor.** There are no embeddings, no learned
ranking, no semantic similarity, and there will not be: the import whitelist is
frozen at nine standard-library modules and floats are prohibited in the core.
Layer 2 is deliberately the *surface* half of activation — cue-dependent
retrieval over a deterministic index — and never semantic spread. A system with
embeddings will beat it on any task where paraphrase matters. That is not the
claim.

**Not a ranking of other people's systems.** Seven systems were read from source
and their designs are documented in `autopsy/`, pinned to commits. **None of them
has been run or scored here.** The adapter stubs for Mem0 and Letta stop short of
the call on purpose. Any table putting a number beside another project's name
would be a number this repository did not measure.

**Not a general-purpose corpus.** `corpora/real-sessions/v1` is 25 events written
by one project about itself. It is evidence about *transfer*; it is far too small
and far too partial to gate anything, and no ratified threshold binds on it.

**Not published.** Repository visibility, write-ups and the grading of external
systems are human decisions, taken one deliberate step at a time. This session
prepared the artifact; it did not ship it.

## 3. The strain-2 story, told straight

The `[L4] [STRAIN]` session pointed the engines' own thesis at our engine, and it
held.

A field note from routine dogfooding found a seam: an attribute key that reads as
an assertion but does **not** invert — a payload the schema cannot rebuild —
leaves the atlas marked `None`. When the budget then released that episode, the
engine booked it as a **demotion**, the lossless kind, and `read(t)` abstained on
it forever afterwards. Eight such writes at a 40-cell cap produced *demotions 7,
forgetting-record count 0, `read(0)` → nothing*. The one structure whose entire
job is to say what is gone said nothing was.

That is **exactly** the sin four autopsies convicted four systems of —
*recorded but never binding*, the thesis of `autopsy/GAPMAP.md §2` — and the one
structure whose entire job is to say what is gone is where it landed. Ours was
not a special case. It was an instance.

It was fixed **red first**. The strain trial was written before the fix and its
recorded failure message is the engine's own accusation — *"the engine books 7
demotions but regenerates 0 events."* The trial demands truthful **accounting**,
not a particular policy: a non-invertible fold is either forgotten (the record
gains its count and its mass, `read(t)` abstains consistently), or refused
demotion and held as an episode, or refused outright with `t` unspent — and it is
**never** booked as demoted while unregenerable. Every identity is asserted
against the partition read off the ordinary query interface, never against the
counters' own arithmetic, which is the difference between a ledger that closes
and a ledger that is true.

The fix made invertibility the demotion invariant, and corrected bookings made
before a key's inversion died, atomically, on the write that kills it. Measured
after: 0 false demotions, 6 recorded losses with their mass, 1 held episode, one
deterministic refusal, `read(t)` abstaining on exactly the 6.

Three things about that episode are the reason it is in this file rather than
only in the log:

* **No frozen corpus reaches the path.** `murk` has 18 atlas keys, `chronicle`
  17, `l4stream` 16, all `None`-free. The whole pre-existing suite ran
  outcome-identical before and after the fix and every anchor came through
  byte-identical. **A bug invisible to every gate we had is exactly the kind a
  benchmark is most likely to ship.** It was found by using the thing, not by
  measuring it.
* **The trial that catches it is now permanent**, on fixtures written for it.
* **The engine's own scores did not move**, which means nothing here was fixed
  *because* it improved a number.

Two other engine-breaking findings from the same layer are in the log with the
same treatment: a shedding loop that broke on its first coarsening step and on
`chronicle` turned 15 137 writes into refusals and **4 924 wrong current-value
answers** — the one way this design can be made to lie — and a 124-cell
under-report of the footprint under pricing rule P. Both were fixed rather than
relaxed. Three of that session's own trials went red against its first draft.

## 4. The methodology note — the evidence both ways

**Determinism is real, and it is the strongest thing here.** Identical inputs
give byte-identical states and answers, enforced by a laws trial class, on every
platform. Every corpus regenerates byte-for-byte from its seed. There is no
model, no clock, no float, no entropy. Nothing in the published numbers depends
on a service being up or a temperature being 0.

**The gates are load-bearing, and that is measured rather than argued.** For each
claimed layer, the engine capped one layer below is run through the identical
interface on the new layer's own tasks and must score at or below a declared
ceiling: measured **cue-C 0** against 100 at Layer 2, **weighted-C 92** against
300 at Layer 3 (34 for the frozen Layer-2 engine capped the same way), and
**reconstruction F 300–302** against 400 at Layer 4. Each ships an
`IMPOSSIBILITY.md` giving a *structural* reason, not an empirical one; the
Layer-4 argument reaches a pigeonhole — thousands of distinct evicted payloads
into at most 35 integer cells admits no injective map.

**Attainability precedes authority.** Since Layer 3, no gate may bind until the
arithmetic showing it lies strictly below the oracle ceiling and strictly above
every named capability-free baseline has been computed and recorded. That rule
exists because a gate was found unsatisfiable *after* it was ratified, and it has
since stopped a second one: the Layer-4 attainability session computed that the
`chronicle` family could not admit the ratified footprint under any policy,
**withheld the engine, and stopped**. A human ruling moved the binding corpus;
no threshold was touched, and both failures are in the log with their numbers.

Now the other side of the ledger.

**The corpora are ours.** All seven synthetic corpora were written by the
same project that wrote the engine, and two of them (`l3streamb`, `l4stream`)
were frozen *specifically* because an earlier corpus could not discriminate. That
is defensible — a corpus that cannot tell a capability from its absence is
useless for gating, and the reasoning is recorded in a frozen ruling rather than
in a commit message — but it is exactly the shape of a benchmark tuned to its
engine, and a reader is entitled to weigh it as such. The single mitigation is
the transfer tier, and the transfer tier is 25 events.

**Layer 4 does not transfer to our own real data.** On
`corpora/real-sessions/v1` the facet map reads 0 assertions and every payload is
un-rowable, so consolidation builds nothing and degenerates exactly to Layer-3
forgetting. Worse for us: the reference *external* engine, which cannot forget at
all, reconstructs **11 of 25** real events against our **2**. That is not a bug —
fidelity counts events, fill-then-refuse maximizes count, our importance law
spends the budget on the two most recent — but it is a real result and it is in
the public scorecard, not in a footnote.

**The facet map is a declared reading, not a learner.** Layer 4 derives from a
frozen table of five grammar kinds. An event outside it is irreducible however
regular it looks. What is claimed is derivation from a *declared* schema; schema
discovery is not claimed, and the real-sessions result is what that limit looks
like from outside.

**One measured number is not measured in the suite.** The Layer-4 humility
whole-stream run costs ~663 seconds — fifteen times the entire suite — so it was
measured **once, out of suite**, at reconstruction F = 302, with its reproduction
command recorded. What runs every time is a declared prefix ladder converging on
it from below (292 → 297 → 300) plus a scale-invariance assertion. The distinction
is stated wherever the number appears.

**The 26‰ cue-reach is a real cost, not a footnote.** Layer 4 buys its
compression by closing the associative channel on demoted content. We chose to
measure and publish that rather than describe it, but it is a capability the
engine had at Layer 3 and does not have at Layer 4 for anything it demoted.

**Five layers are unbuilt.** Prospection, meta-memory, generation,
self-description and birth are specified and unclaimed, and two of them have no
thresholds yet. Any claim about what this benchmark proves is a claim about four
layers.

**Ordering is a design commitment, not a finding.** That memory capability is
ladder-shaped — that consolidation presupposes forgetting, which presupposes
recall — is asserted by this constitution and is not established by anything here.
An architecture that reached Layer 5 without Layer 3 would not be caught by this
benchmark; it would simply score 0 on Layer 3 and be right to.

## 5. What grading an external system would require

Every adapter stub in `trials/adapters/external/` stops short of the call, and
the reason is not squeamishness:

* **A key and a socket produce an unreproducible number.** No session in this
  project fetches credentials or opens a network connection. A score obtained
  that way could not be reproduced by a reader, which is the criticism this
  project levelled at an uncached, single-call `gpt-4o` judge in someone else's
  harness.
* **The result would not be deterministic.** An LLM-extraction pipeline returns
  different memories on different runs. The harness compares exactly. The honest
  way to grade such a system is to say plainly that the number is a *sample*, and
  that is a call for a human to make.
* **The adapter must invent things, and every invention must be declared.** None
  of the systems read assigns an engine-owned logical `t`; none exposes
  capability capping, so a humility run is not expressible against them at all;
  a ranked search result must be turned into one answer or an abstention by a
  rule the adapter chooses. Each of those is the adapter's editorial decision and
  belongs in the report beside the score, not behind it.

The mappings are written down now precisely so they can be argued with before any
number exists.

## 6. How to cite the numbers here

* Give the **commit**. Every measurement in `README-public.md` is reproducible
  from a checkout with `python3 -m trials --engine ours` and `python3
  trials/run.py`, and both are cheap. A number without a commit is not a claim
  about this repository.
* Say **which corpus**. `weighted-C 917` is Layer 3 on `l3streamb`. The same
  engine scores 174 on `l3stream`, and both numbers are true.
* Do not quote a **capped** score as an engine's score. Capped runs are the
  humility measurement; a capped engine is deliberately handicapped.
* Do not turn a **transfer** number into a general one, in either direction. 25
  events is 25 events.
* Do not attribute the lenient LLM judge to **LoCoMo**. The in-repo judge is
  token-F1; the model judge is a downstream addition.
* Nothing here has been **peer-reviewed, replicated externally, or run against
  another live system**. Four layers of a nine-layer specification are built and
  certified against corpora this project wrote. That is the whole of it.

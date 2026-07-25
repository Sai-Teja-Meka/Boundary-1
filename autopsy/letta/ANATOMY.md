# ANATOMY — Letta (formerly MemGPT)

> **Erratum — 2026-07-25 (`[L3] [PULSE]`).** The text below uses **pre-ratification
> layer names**. It is left exactly as written; this note maps it, and nothing
> beneath it is rewritten.
>
> | as written below | ratified ladder (`BOUNDARY.md §5`) |
> |---|---|
> | "Layer 6 (Contradiction & Dedup)" (`:193`), "targets Layer 6 + Layer 7" (`:198`), "the observed record (Layer 6)" (`:217`), "our **Layer 6/7**" (`:225`) | **there is no standalone Contradiction layer.** Supersession, contradiction and "the current value among conflicts" are facets of **L4 Consolidation** (attribute histories: newest entry = current value, conflicting entries = the contradiction, as-of query = L4 reconstruction) |
> | "Layer 7 (Provenance)" (`:194`), "citable support (Layer 7)" (`:218`) | ratified **L7 is Generation**. The *provenance law* (§4.2) is dormant until Layer 7 and binding forever after, so the layer **number** is right and only the **name** is pre-ratification |
> | ratified **L6** | **Meta-memory** |
>
> **What was already correct, so the erratum does not over-reach:** every **Layer
> 3** reference (`:181`, `:185`, `:224` — the hard budget, the recoverability
> invariant, what L3 should adopt) is right on both number and name. Ratified L3
> **is** Forgetting under a binding budget, and `core/layers/README-l3.md §0.4`
> shows the adoption actually happened.
>
> Letta's hot/cold demotion is carried into the steal list as **GAPMAP S4**, which
> ruled it unconstitutional as-is and left the choice of form to `ASCEND`.
> `core/layers/README-l3.md §0.4` records the disposition: the **two-budget** form
> is priced out as arithmetically vestigial at this budget (a hot tier of 8 items
> at the bare gate, 0 at the occupancy actually reached), Layer 3 takes **true
> eviction** with the L4 co-design intent recorded, and
> **demotion-into-consolidated-form** is deliberately deferred to **Layer 4**
> because a cold entry can only cost less than an event once consolidation exists.
>
> Reconciled in `autopsy/GAPMAP.md` ("Naming reconciliation", read before the
> matrix), which flagged this as an erratum in non-frozen documentation to be
> fixed at the next doc pass. This is that pass.

Subject of `[L0] [AUTOPSY]`. Traced from source (call paths, not READMEs) in a
read-only clone outside this repo, scoped to the **core agent-memory machinery**
(tiers, self-editing tools, overflow, sleeptime) — not server/API plumbing beyond
what those paths touch. A **Constitutional note** at the end records that no
law-change objection arose. (The "continual learning in token space" thesis is
context, not evidence; only code is cited.)

## License + commit hash examined (+ open-core boundary)

- **License:** Apache License 2.0 (`LICENSE`, lines 1–3) for the `letta/` package.
- **Repo:** `github.com/letta-ai/letta`
- **Commit examined:** `b76da9092518cbaa2d09042e52fdcbde69243e18` (default branch, shallow clone).
- **Open-core boundary observed:** like Graphiti and unlike Mem0, the memory
  machinery is **not feature-gated in code** — no "not supported in OSS" guards in
  the tools, summarizer, or sleeptime paths. The full agent runtime (core/recall/
  archival tiers, self-editing tools, summarizer, sleeptime agents, the `server/`
  REST API) is in the Apache-2.0 package. The proprietary layer is **Letta Cloud**
  (hosted agent infra + the Agent Development Environment) built on top —
  organizational, external to the traced code.

## Core data model (file:line citations)

Three memory tiers (the "LLM-as-OS" abstraction):

- **Core memory = `Block`s, always in-context** (`schemas/block.py`): `value: str`
  (`:19`), `limit: int = CORE_MEMORY_BLOCK_CHAR_LIMIT` (`:20`), `read_only: bool`
  (`:36`), `label`, `description`, plus actor attribution `created_by_id` /
  `last_updated_by_id` (`:73–74`). Blocks are rendered into the system prompt with
  a live `chars_current=… chars_limit=…` header (`schemas/memory.py:154, 191–192`).
- **Recall memory = the full message store** (`services/message_manager.py`),
  the durable conversation history; queried by `conversation_search`
  (`services/tool_executor/core_tool_executor.py:81`).
- **Archival memory = `Passage`s in a vector store** (`schemas/passage.py`);
  written by `archival_memory_insert`, read by `archival_memory_search`
  (`core_tool_executor.py:307, 278`).

What crosses between tiers, and when: crossing is **agent-driven** (the LLM calls
memory tools to promote recall/archival content into core, or insert into
archival) **except context overflow**, which is automatic (below). Core is bounded
(char limit); recall and archival are unbounded.

## Write path (ingestion → storage) — as traced

Every step's messages are persisted to the **recall** store automatically. Beyond
that, writes are the agent's own tool calls, plus two background processes.

**Self-editing tools** (`core_tool_executor.py`):
- `core_memory_append` (`:319–326`): `read_only` check (`:320–321`), then
  `value + "\n" + content` and persist. No other check.
- `core_memory_replace` (`:328–344`): `read_only` check (`:336–337`); require
  `old_content in current_value` (`:339–340`); then a **verbatim
  `current_value.replace(old, new)`** (`:341`) and persist.
- `memory_replace` (`:346`+): a patch-style editor that rejects a missing
  (`:498`) or non-unique (`:503`) hunk context and a line-number banner (`:423`).
- `archival_memory_insert` (`:307`): embed + store a passage.

**Focus #2 verdict — what validates an edit? Only *structure*, never *truth*.**
The guards are: block is not `read_only`; the `old_content`/patch context exists
and is unique; and the char `limit` — which is **advisory only**: it is rendered
to the model (`schemas/memory.py:154, 191`) but `grep` finds **no hard raise** on
exceeding it in `core_tool_executor.py` or `block_manager.py`. So if the agent
replaces a true fact with a false one, the edit applies silently as long as the
old string exists and the block is writable. **Nothing catches a wrong self-edit**
(failures #3397, #3388).

**Overflow (automatic) — `services/summarizer/summarizer.py`:** a `Summarizer`
(`:36`) with `message_buffer_limit=10`, `message_buffer_min=3`,
`partial_evict_summarizer_percentage=0.30` (`:47–64`). When the in-context buffer
exceeds the limit, `_static_buffer_summarization` (`:244`) computes a trim index
snapped to a user-message boundary (`:290–293`), **evicts everything between the
system message and the trim index** (`:306`), keeps the `message_buffer_min` most
recent (`:283`), and — if a summarizer agent is configured — **background-
summarizes the evicted messages** (`:314–340`). The summary is injected as a
**`role=MessageRole.user` message** (`:216–242`, `:220`).

**Focus #3 verdict — is anything lost, and recorded?** Eviction removes messages
from the **in-context** working set but **does not delete them** — they persist in
the recall store and remain searchable via `conversation_search`. So durable loss
is nil; the loss is of *working context*, recorded as (a) the injected summary and
(b) the retained recall rows. The weak point is fidelity of the summary, not
durability (failure #2512: the last user question can be summarized away).

## Read path (query → answer) — as traced

- **Core memory:** no retrieval — Blocks are always rendered into the system
  prompt (`schemas/memory.py`), passively present every turn.
- **Recall:** `conversation_search` (`core_tool_executor.py:81–276`) — a filtered
  search over the message store (role/date filters, paged).
- **Archival:** `archival_memory_search` (`:278–305`) — vector search over
  passages.

Reads of recall/archival are **agent-initiated tool calls** — the model decides to
search; there is no automatic retrieval into context. There is no "answer" object;
results are returned to the LLM as tool output. No confidence score accompanies
memory reads.

## Sleep-time / background memory agents

Present and central. `groups/sleeptime_multi_agent_v3.py` (`run_sleeptime_agents`,
`:127`) issues background tasks; the sleeptime agent's charter
(`prompts/system_prompts/sleeptime_v2.py`) is to keep core memory blocks
"comprehensive, readable, and up to date" and free of "redundant and outdated
information" (`:16, 20`). It edits blocks with the same precise tools **and a
`rethink` tool that "reorganize[s] the entire memory block at a single time"**
(`:15, 21`).

**Focus #4 verdict:** the reorganization is **destructive** — `rethink` overwrites
a block's whole `value` in place and precise edits delete "outdated" text. It is
*re-derivable in principle* (the source messages survive in recall), but it is a
**one-shot in-place rewrite, not a versioned/idempotent derivation**: the prior
block state is replaced, tracked only by `last_updated_by_id` (who), not a
reconstructable lineage. Sleeptime triggers on a schedule/turn-count, not on
content.

## Forgetting / decay — overflow-demotion only; no decay

Search performed: `grep -niE '\bttl\b|expire|decay|evict|forget|prune'` over
`services/passage_manager.py` and `services/message_manager.py` → **nothing**.

- **No TTL, decay, or capacity eviction** on recall messages or archival passages;
  both grow without bound.
- The only "forgetting" is (a) **context eviction on overflow** — demotion from
  the working set, fully recoverable from recall — and (b) **sleeptime block
  rewrites** — destructive to the block, recoverable from recall. Neither is
  age/importance/budget-driven auto-eviction; the durable stores never shrink.

## Calibration / provenance

- **Calibration — ABSENT.** No confidence on memory edits or on
  conversation/archival search results; no abstention.
- **Provenance — largely ABSENT at the semantic level.** Blocks carry
  `created_by_id` / `last_updated_by_id` (`schemas/block.py:73–74`) — coarse
  *actor* attribution (who last wrote), but **no flag distinguishing an
  agent-authored self-edit from a human-set value**, and **no link from a
  statement in a block back to the recall message(s) that justify it**. Derived
  summaries are worse than unmarked: the overflow summary is injected **as a
  `role=user` message** (`summarizer.py:220`), so a lossy machine-generated
  artifact is structurally indistinguishable from a genuine user turn. Archival
  passages carry no source-episode link. You cannot, from the store, tell derived
  from original or grounded from invented.

## Prospective memory — **ABSENT** (partial answer certified)

The subject most likely to have a partial answer does not. There is no
`intend(condition → event)` and nothing that fires on a *future* write matching a
condition. The nearest constructs are **schedule/turn-count-triggered** sleeptime
agents (`run_sleeptime_agents`) — background maintenance, not content-conditioned
triggers — and there is no reminder/timer/`request_heartbeat` content-trigger in
the memory tools (`grep` over `functions/function_sets/base.py`,
`schemas/memory.py`, the sleeptime group → nothing). Where a real prospective
memory would live: a condition-indexed intention store consulted on each new
message in the agent step loop. Absent.

## Three failure modes (tracker)

1. **No duplicate-label guard → stale core memory silently persists in the
   compiled prompt.** A wrong/duplicate block is not caught; outdated content
   keeps being rendered into context. The self-edit path has no integrity check
   beyond structure.
   https://github.com/letta-ai/letta/issues/3397
2. **Summarizer drops the live user question.** On overflow the summarizer
   ignores the intended keep-last-N retention, so the most recent user
   message/question is summarized away and the agent can no longer answer it —
   lossy compaction losing exactly the information it was meant to preserve.
   https://github.com/letta-ai/letta/issues/2512
3. **Cross-session core-memory poisoning persists (sandbox isolation failure).**
   An unvalidated write to core memory persists and leaks across sessions — with
   no semantic validation on self-edits, a bad/adversarial edit becomes durable,
   first-class memory.
   https://github.com/letta-ai/letta/issues/3388

## ONE technique worth stealing

**The bounded working-tier + unbounded recoverable backing-tier split, where
eviction is *demotion, not deletion*.** Letta binds the size of exactly one tier —
in-context core memory — and when it overflows, messages are evicted from the
working set but **retained in the recall store** and summarized, so nothing leaves
durable storage (`summarizer.py:244–342`; recall persists). This is the honest way
to run a memory under a hard budget, and it lands squarely in our **Layer 3
(Forgetting)**: apply the **budget law (§4.1) to the hot working tier only**, and
make eviction a *demotion to a searchable cold tier* rather than a destructive
drop. It also sharpens our budget measure — "budget" is occupancy of the bounded
tier, not of total memory — and gives Layer 3 a clean recoverability invariant:
evicted ≠ forgotten, evicted = demoted-and-still-recallable.

## ONE mistake worth codifying (as a strain-trial idea)

**Mistake: a self-authored memory write is trusted with zero semantic validation —
the agent can overwrite a true fact with a false one, or invent an unobserved
fact, and it becomes first-class memory indistinguishable from grounded truth**
(structural guards only; #3397, #3388). This is a **Layer 6 (Contradiction &
Dedup) + Layer 7 (Provenance)** failure: a derived/self-authored edit that
contradicts the observed record, or that has no observational support, must not be
silently promotable to an answered fact.

**Strain-trial idea (targets Layer 6 + Layer 7; extends `corpora/murk`):**
- *Corpus:* a stream of **observed** ground-truth facts (real ingested events),
  followed by a batch of **self-edit operations** submitted through the engine's
  memory-write interface. Tag each self-edit in `ground_truth.json` as
  **grounded** (supported by a prior observed event), **contradicting** (asserts a
  value that conflicts with an observed event, e.g. observed "meeting at 15:00",
  self-edit "meeting at 17:00"), or **invented** (asserts an unobserved fact).
- *Manipulation that exposes it:* make the contradicting/invented self-edits
  syntactically clean (the "old string" they replace really exists; within any
  advisory limit) so a Letta-style structural guard passes them all.
- *Assertions:* (a) a **contradicting** self-edit is rejected or flagged, never
  silently applied over the observed record; (b) an **invented** self-edit cannot
  be returned as an answered fact without provenance whose support bottoms out in
  an observed event — otherwise the engine must **abstain** (§3.0); (c) a query
  after the edits returns the **observed** value or abstains, never the fabricated
  self-edit as first-class truth; (d) provenance distinguishes agent-authored from
  observed at read.
- *Why it bites:* a MemGPT-style engine applies all three edit classes verbatim
  and the fabricated value becomes unmarked core memory. Our engine must gate
  self-writes against the observed record (Layer 6) and refuse to promote
  ungrounded writes to fact without citable support (Layer 7).

## Constitutional note (no law-change objection)

No objection to the frozen `BOUNDARY.md`. Letta contributes the best *architecture*
of the four subjects (bounded working tier + recoverable backing store) — which our
budget law and **Layer 3** should adopt — but it also shows, more starkly than the
others, the failure our **Layer 6/7** exist to prevent: a memory that lets its own
agent write unvalidated, unprovenanced facts over the record, then renders derived
summaries as if they were user turns. The recurring pattern across all four
autopsies holds here too — *actor/limit metadata is recorded but never made binding
at write or read time.* No change is warranted.

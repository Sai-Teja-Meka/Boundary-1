# ANATOMY — MemoryAgentBench

**Official harness used** (not the LongMemEval fallback): `HUST-AI-HYZ/MemoryAgentBench`,
the ICLR 2026 benchmark (arXiv 2507.05257). One caveat recorded up front: the
**dataset is HuggingFace-hosted and HuggingFace egress is blocked by this
environment's org policy (403 CONNECT)**, so I could not sample raw rows from
`ai-hyz/MemoryAgentBench`; I sampled the **ground-truth loader, templates, and code
judges in the repo instead** (arguably more revealing for answer-key defects) and
say so in the sampling section. This is a benchmark autopsy — the judge is the
subject, not the memory. A **Constitutional note** at the end records that no
law-change objection arose.

## Licenses + commit hash examined

- **Repo (code) license:** **MIT** (`LICENSE`, © 2026 Yuanzhe Hu).
- **Dataset license:** **separate and not retrievable here** (HF blocked). The
  dataset is *reformulated from prior benchmarks* — RULER, InfBench, HELMET,
  LongMemEval, detectiveQA, and ICL classification sets (`README.md:191`,
  `configs/data_conf/*`), plus two newly-built subsets (EventQA, FactConsolidation).
  The MIT **code** license does **not** relicense the **data**: the effective data
  terms are the *union of the upstream source licenses*, which differ (RULER/HELMET
  are permissive; several ICL/QA sources carry CC or research-only terms). Anyone
  reusing the data inherits that patchwork, not MIT. **Record separately; do not
  assume the repo license covers the corpus.**
- **Commit examined:** `455306dcabc3842526eb83cd4e225e5d486c5c5d` (default branch).
- Note: the harness **vendors three baselines in-tree** (`cognee/`, `letta/`,
  `mem0/`) plus method files (`methods/{zep,raptor,self_rag,graph_rag,hipporag,
  memorag,embedding_retriever}`) — relevant to task-posing below.

## Task-posing model

- **Interface:** `AgentWrapper.send_message(message, memorizing, query_id,
  context_id)` (`agent.py:18, 258`). Ingestion vs query is a **boolean flag**:
  `memorizing=True` feeds a chunk into the system under test; `memorizing=False`
  asks a question. That is the whole contract — effectively a 1-method interface
  (`ingest`/`query` collapsed onto one call), with **no `snapshot`** and no
  capability-absence-as-score (an unsupported task just yields a wrong answer).
- **Delivery = incremental chunk replay ("inject once, query many times").** A
  long context is split into fixed-size chunks (`agent_chunk_size`) and streamed in
  via repeated `send_message(chunk, memorizing=True)`; then one context is queried
  by *many* QA pairs (`conversation_creator.py:94, 155–159`; one item →
  `len(query_and_answers)` questions). Efficient: expensive ingestion amortized
  over many cheap assertions.
- **But the harness is welded to specific baselines, not a clean adapter.**
  Dispatch is per-baseline: `_initialize_{long_context,letta,mem0,cognee,zep,rag}_
  agent` and `_handle_{letta,cognee}_agent` / `_process_letta_message`
  (`agent.py:64, 137, 217, 227, 236, 249, 412, 500, 450`), with bespoke wiring
  (`letta_mode == 'insert'` → `passage_manager.insert_passage`, `:457`;
  `cognee.cognify(...)`, `:513`). A foreign memory system *can* be plugged in if it
  implements `send_message`, but every baseline needed hand-written integration —
  compare our `trials/adapters/INTERFACE.md` (a fixed `ingest`/`query`/`snapshot`
  contract with capability-absence surfaced as scores). MemoryAgentBench's contract
  is thinner and its integrations are bespoke.

## Judging map (per task type: mechanism, reproducibility)

The four headline competencies are **code-judged and reproducible**; an LLM judge
is confined to two auxiliary subsets (`README.md:175–187`, `utils/eval_other_utils.py`).

| Competency / subset | Datasets | Mechanism | Reproducible? |
|---|---|---|---|
| **Accurate Retrieval** | event_qa, ruler_qa1/2 | `substring_exact_match` (code) | Yes (deterministic) |
| **Conflict Resolution** | fact_mh, fact_sh | `substring_exact_match` (code) | Yes |
| **Long-Range Understanding** | detectiveQA | `exact_match` (code, strict) | Yes |
| **Test-Time Learning** | ICL_{banking,clinic,nlu,trec_*} | `exact_match` (code, strict) | Yes |
| Recsys | recsys | Recall@5 (code) | Yes |
| **LongMemEval** | longmemeval | **LLM-as-judge** | **No** (see below) |
| InfBench (summarization) | infbench | **F1 via LLM-as-judge** (HELMET-style) | **No** |

- `substring_exact_match_score` = gold answer (lowercased) is a **substring** of the
  prediction, max over valid answers (`eval_other_utils.py:105, 424, 534`).
- `exact_match` = `normalize_answer(pred) == normalize_answer(gold)` (`:102`) —
  **strict**; the README itself warns `"label: 43"` ≠ `"43"` counts wrong.
- **The LLM-judge sites (the LoCoMo-audit question, answered):**
  `llm_based_eval/longmem_qa_evaluate.py` — **model `gpt-4o`** (`:96`),
  `temperature=0` (`:163`), per-task yes/no rubric prompts (`get_anscheck_prompt`,
  `:20–39`, including a knowledge-update variant and an abstention variant). But:
  **no caching, no seed persistence, a single call (no majority vote, no
  disagreement handling)**, and the verdict is parsed as **`label = 'yes' in
  eval_response.lower()`** (`:168`) — a bare substring test that false-positives on
  `"yesterday"` or `"yes and no"`. Reproducibility rests entirely on `gpt-4o`
  @ temp 0 being stable across API revisions, which it is not (tracker #15).

## Ground-truth provenance + sampling findings

- **Provenance:** two newly-built synthetic subsets (**EventQA**,
  **FactConsolidation**) generated by the authors (synthesis lives in gitignored
  `process_data/`), plus **reformulations of RULER / InfBench / HELMET /
  LongMemEval / detectiveQA / ICL** (`README.md:24, 191`). So ground truth is
  *synthetic-templated* for the two new sets and *inherited* for the rest.
- **Sampling — method and honesty:** I could **not** sample the 30 HF rows (HF
  egress 403-blocked; `curl` and WebFetch both refused). I instead sampled the
  answer-key *machinery*: the loader (`conversation_creator.py` — one context →
  many QA pairs, `context > 2000` chars asserted, `:130`), the query **templates**
  (`utils/templates.py`), and the code judges (`utils/eval_other_utils.py`). What
  that surface reveals:
  1. **Contamination is real and reported:** the model can answer some items *with
     no context at all* from parametric knowledge (tracker **#10**). FactConsolidation
     defends against this with a **deliberately counterfactual** framing (its
     worked example answers "current president of Russia" → "Donald Trump", and
     instructs "answer **only** from the knowledge pool … rather than the real facts
     in real world", `templates.py:80`) — a good anti-contamination device the
     other subsets lack.
  2. **`substring_exact_match` is spoofable:** a verbose answer that contains the
     gold string *anywhere* is scored correct even if it also asserts a wrong
     value, and short/numeric gold answers can match incidentally. This is the
     judge for the *two* "accuracy" competencies (AR and Conflict Resolution).
  3. **`exact_match` is format-brittle** (README's own admission): a correct answer
     with a prefix/formatting scores wrong — biasing toward terse systems and
     penalizing ones that explain.

## Selective Forgetting analysis (the competency, examined)

The competency the prompt calls "Selective Forgetting" is built in the repo as
**`Conflict_Resolution`**, dataset **FactConsolidation** (`sh`=single-hop,
`mh`=multi-hop; 6k–262k context; `configs/data_conf/Conflict_Resolution/*.yaml`),
judged by `substring_exact_match`.

**What it actually tests:** the query template (`templates.py:80`) says every fact
carries a serial number, *newer facts have larger serials*, and the task is to
"**solve the conflicts … by finding the newest fact with larger serial number**."
So it is **supersession-by-recency-reasoning over retained facts** — a
*max-over-serial* retrieval-and-reasoning task. It is **not** commanded deletion,
**not** decay, and **not** forgetting.

**What a system that CANNOT forget scores:** it is **not punished — if anything it
is advantaged.** To pick the max-serial fact you must *retain every conflicting
fact and its serial*; a system that evicted old facts would lose the very ordering
the task needs. And because the judge is substring match, a system that dumps
*all* facts (old + newest) still scores correct as long as the newest value
appears. **Forgetting is neither rewarded nor required here.** The
forgetting-named competency measures conflict-resolution reasoning, not the
ability to forget — a genuine name/semantics gap (and it is hard regardless:
typed multi-hop CR reportedly ~12%, tracker #18).

## The impossibility-gate answer (feeds GAPMAP §4)

**The four competencies are independent parallel tracks** — separate dataset
configs run by separate scripts (`configs/data_conf/{Accurate_Retrieval,
Conflict_Resolution,Long_Range_Understanding,Test_Time_Learning}`,
`bash_files/`), scored independently. There is **no ordering, no dependency, no
capability-tier notion, and no capped-system construction**. The harness computes
`accuracy(method, task)` — a flat leaderboard.

**Therefore an impossibility gate cannot be expressed in this architecture.** Our
humility construct — *a system frozen at capability N−1 must provably score ≤ a
ceiling on task N* — has **no analog**: MemoryAgentBench never runs a deliberately
lesser system to prove a task requires a capability; it only measures absolute
accuracy and ranks. Expressing a gate would require (a) a capability-cap on the
system under test and (b) an *upper-bound* assertion — neither exists here. **Our
gated ladder is strictly more expressive than the field's leading benchmark; this
is a capability to claim, not borrow, in GAPMAP §4.**

## Three linkable defects / limitations

1. **Contamination — the benchmark can score "memory" the model never needed.**
   The LLM answers some items correctly with no context, from parametric
   knowledge, so the metric partly measures pretraining, not memory.
   https://github.com/HUST-AI-HYZ/MemoryAgentBench/issues/10
2. **LLM-judge / pipeline results are not reproducible.** Users cannot reproduce
   the Mem0 + LongMemEval(S*) numbers — the `gpt-4o` judge is uncached, single-call,
   `'yes'`-substring-parsed, and the pipeline is nondeterministic.
   https://github.com/HUST-AI-HYZ/MemoryAgentBench/issues/15
3. **Welded-baseline fragility.** The bespoke per-baseline integrations break in
   ways that silently zero out memory — e.g. "Empty memory in Mem0" (the harness's
   Mem0 wiring stored nothing), so a baseline can score near-zero for an
   integration bug, not a memory failure.
   https://github.com/HUST-AI-HYZ/MemoryAgentBench/issues/11

## ONE technique worth stealing (for our corpora)

**Serial-numbered supersession facts with a deterministic, code-checkable
max-serial answer key.** FactConsolidation tags each conflicting fact with a
monotonically increasing serial and defines the correct answer as *the value of
the largest-serial fact* (`templates.py:80`) — a conflict-resolution corpus whose
ground truth is computed by pure integer comparison, **no LLM judge**. This is
exactly what our future **Layer-6 (Contradiction & Dedup)** corpus needs and what
every engine-subject autopsy lacked: the serial *is* our integer logical `t`, so a
supersession corpus can carry `(fact, t)` pairs with `ground_truth = value at
max t`, checked by exact code — deterministic, float-free, byte-matchable, and
paired with a murk-style answer key. Steal the serial-key construction into
`corpora/` (a Conflict corpus) and keep the correctness check in code, never a
model. (Steal the harness's "inject once, query many times" shape too: ingest a
frozen corpus once per trial, then run a battery of scored queries against the one
ingested state.)

## ONE mistake our harness must never make (a rule for `trials/run.py`)

**Rule: `run.py` decides correctness only by exact, exclusive, deterministic code
comparison — never by substring/containment, and never by an LLM judge. A response
is correct only if its extracted answer *equals* the expected value under our
canonical normalization AND does not also assert a contradicting value; a response
that contains the correct answer *alongside* a wrong one is WRONG (§3.0: a wrong
answer scores 0 and cannot be laundered by also emitting the gold string).**

MemoryAgentBench scores its two "accuracy" competencies by `gold in prediction`
(`eval_other_utils.py:534`) and its QA/summarization subsets by a `gpt-4o`
`'yes'`-substring judge (`longmem_qa_evaluate.py:168`). Both let a wrong-but-verbose
answer pass and are unreproducible or gameable. Our suite's whole premise is that
green is earned by a deterministic assertion; importing substring-tolerance or an
LLM judge would silently repeal that. `run.py` must treat "answer contains the gold
substring" and "an LLM said yes" as **inadmissible** correctness signals.

## Constitutional note (no law-change objection)

No objection to the frozen `BOUNDARY.md`. MemoryAgentBench *validates* three of our
choices by contrast: it keeps its headline competencies on **deterministic code
judges** (as our determinism law demands) yet still leaks into an **unreproducible
LLM judge** on two subsets (which our runner-rule above forbids outright); its
**forgetting-named competency doesn't test forgetting**, vindicating our decision
to specify Layer 3 (eviction under pressure) and Layer 6 (contradiction) as
*separate, precisely-defined* gates rather than one fuzzy "forgetting" score; and
its **flat-leaderboard architecture cannot express an impossibility gate**,
confirming that our humility trial class is a genuine capability of our design, not
a reinvention. No change is warranted.

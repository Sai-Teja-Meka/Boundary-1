# ANATOMY — Zep / Graphiti

> **Erratum — 2026-07-25 (`[L3] [PULSE]`).** The text below uses **pre-ratification
> layer names**. It is left exactly as written; this note maps it, and nothing
> beneath it is rewritten.
>
> | as written below | ratified ladder (`BOUNDARY.md §5`) |
> |---|---|
> | "Layer 6 (Contradiction & Dedup)" (`:192`), "targets Layer 6" (`:208`), "the property Layer 6 certifies" (`:225`), "what **Layer 6** should institutionalize" (`:231`) | **there is no standalone Contradiction layer.** Supersession, contradiction and "the current value among conflicts" are facets of **L4 Consolidation** (attribute histories: newest entry = current value, conflicting entries = the contradiction, as-of query = L4 reconstruction) |
> | "Layer 8 (Revision & Forgetting)" (`:193`) | **there is no standalone Revision layer.** Commanded, principled forgetting is **L3 Forgetting** (eviction under pressure), with as-of audit supplied by **L4**. Ratified **L8 is Self-description** |
> | ratified **L6** | **Meta-memory** |
>
> **What was already correct, so the erratum does not over-reach:** *"what **Layer
> 7** demands"* (`:232`, provenance) has the right **number** — §4.2 is dormant
> until Layer 7 and binding forever after — though ratified **L7 is Generation**,
> not "Provenance".
>
> Graphiti's bitemporal *invalidate-not-delete* is carried into the steal list as
> **GAPMAP S3 → L4**, informing L3 — the same remapping, recorded there against the
> frozen names.
>
> Reconciled in `autopsy/GAPMAP.md` ("Naming reconciliation", read before the
> matrix), which flagged this as an erratum in non-frozen documentation to be
> fixed at the next doc pass. This is that pass.

Subject of `[L0] [AUTOPSY]`. Traced from source (call paths, not READMEs) in a
read-only clone outside this repo, scoped to the **core graph memory library**
(`graphiti_core/`) — not `server/`, `mcp_server/`, drivers, or embedder/LLM
plumbing beyond what the core paths touch. A **Constitutional note** at the end
records that no law-change objection arose.

## License + commit hash examined (+ open-core boundary)

- **License:** Apache License 2.0 (`LICENSE`, lines 1–3) for `graphiti_core/`.
- **Repo:** `github.com/getzep/graphiti`
- **Commit examined:** `3bb2d0bba56f8e22311574c045452c420a012f49` (default branch, shallow clone).
- **Open-core boundary observed:** unlike Mem0, the OSS core is **not
  feature-gated in code** — there are no "not supported in OSS" guards; the
  library is fully functional standalone against a graph DB (Neo4j / FalkorDB /
  Kuzu). The proprietary layer is the **separate hosted Zep product** (Zep Cloud
  memory API / dashboards) built on top; the in-repo `server/` and `mcp_server/`
  are thin wrappers. The open-core signal is organizational, not technical: a
  contributor license agreement (`Zep-CLA.md`) assigns contributions to Zep.

## Core data model (file:line citations)

A **bitemporal, episode-sourced knowledge graph**. Two node kinds and typed
edges; the fact lives on the **edge**.

- **`EntityEdge`** (`edges.py:263`) — the fact carrier: `fact` (str, `:265`),
  `fact_embedding` (`:266`), and a full **bitemporal quartet**:
  - `created_at` (`:54`, base `Edge`) — **transaction time**: when the edge
    entered the graph.
  - `expired_at` (`:271`) — **transaction time**: when the edge was *invalidated*
    in the graph (null while live).
  - `valid_at` (`:274`) — **valid time**: "when the fact became true."
  - `invalid_at` (`:277`) — **valid time**: "when the fact stopped being true."
  - `episodes` (`:267`) — list of **source episode UUIDs** (provenance → sources).
  - `reference_time` (`:280`) — an extra timestamp (see failure #1661: write-only).
- **`EpisodicNode`** (`nodes.py:318`) — a raw source unit: `source`
  (`message`/`text`/`json`, `:319`), `content`, `source_description`, `valid_at`
  (`:322`, the episode's event/reference time), `created_at` (`:98`, ingestion),
  and `entity_edges` (`:325`) — UUIDs of the edges derived from it (**forward
  provenance**).
- **`EntityNode`** (`nodes.py:499`) carries a `summary` (`:501`);
  **`CommunityNode`** (`nodes.py:687`) carries a `summary` (`:689`).
- **Structural edges:** `EpisodicEdge`/`HasEpisodeEdge` (episode → entity
  "MENTIONS"), `NextEpisodeEdge` (episode chain), `CommunityEdge`
  (`edges.py:143, 575, 689, 822`).

Provenance is **bidirectional and first-class**: `EntityEdge.episodes ↔
EpisodicNode.entity_edges`, plus MENTIONS edges.

## Write path (ingestion → storage) — as traced

`Graphiti.add_episode(...)` → the episode processing pipeline (`graphiti.py`):

1. **Extract entities** — `extract_nodes` (`:617`) → `resolve_extracted_nodes`
   (`:621`, dedup against existing nodes).
2. **Extract edges** — `extract_edges` (`:656`), an LLM call that also proposes
   `valid_at`/`invalid_at` from the text (`prompts/extract_edges.py:172, 256`).
3. **Resolve edges** — `resolve_extracted_edges` (`:669` →
   `utils/maintenance/edge_operations.py:325`), per edge
   `resolve_extracted_edge` (`:623`):
   - **Deterministic fast path** (`:684–695`): if an existing edge has the same
     endpoints and byte-normalized `fact`, reuse it and just append the episode
     UUID to its `episodes` (dedup, no new edge).
   - Otherwise an **LLM dedup/contradiction judge** — `dedupe_edges.resolve_edge`
     at **`ModelSize.small`** (`:726–731`) — returns `duplicate_facts` and
     `contradicted_facts` (`prompts/dedupe_edges.py:29–31, 80–83`).
   - **LLM timestamp extraction** — `_extract_edge_timestamps` (`:576`), a second
     small-model call, sets `valid_at`/`invalid_at` from the fact + the episode's
     `valid_at`.
4. **Apply supersession — `resolve_edge_contradictions` (`:538`), deterministic
   given the dates:** for each contradicted edge, if the intervals overlap such
   that the old fact started before the new one
   (`edge_valid_at < resolved_edge_valid_at`, `:564–567`), set
   `edge.invalid_at = resolved_edge.valid_at` and
   `edge.expired_at = utc_now()` (`:569–570`). **The old edge is invalidated, not
   deleted.**
5. **Persist** — `build_episodic_edges` (`:720`) + `add_nodes_and_edges_bulk`
   (`:726`); optional `update_community`.

**Focus #2 verdict (supersession sturdiness):** the mechanism is the best of the
three subjects — a real bitemporal invalidate-not-delete audit trail. But it is a
**hybrid whose hard decisions are model-dependent**: *which* facts contradict
(`dedupe_edges.resolve_edge`, small model) and *when* facts became/ceased valid
(`extract_timestamps`, small model) are both LLM calls; only the interval
arithmetic (`:538–573`) is deterministic. So supersession is **not reproducible
across runs/models** — it collapses on weaker models (failure #1666). It is
sturdy against data loss, fragile against determinism.

## Read path (query → answer) — as traced

`search(...)` (`search/search.py:98`) is a **no-generative-LLM hybrid**. Per
entity type it runs, in parallel: **BM25 full-text** (`edge_fulltext_search`),
**cosine** on embeddings, and **BFS graph traversal** (`edge_bfs_search`), then
fuses/reranks with **RRF** (reciprocal rank fusion), **MMR**, a
**`node_distance_reranker`** (graph distance from a center node), or
`episode_mentions_reranker` (`search.py:50–65`). A **cross-encoder reranker** is
*optional* (`:114, 176`) — if configured it adds a model call at read, but the
default recipes are pure lexical+vector+graph. Results are thresholded by
`reranker_min_score`.

**Focus #3 verdict (does read honor `invalid_at`?): NO, not by default.** The
search Cypher *returns* `valid_at`/`invalid_at`/`expired_at`
(`search_utils.py:253–255, …`) but applies **no temporal WHERE** unless the
caller supplies one: `SearchFilters.valid_at / invalid_at / expired_at` all
default `None` (`search_filters.py:62–65`) and the filter constructors add
clauses only when set (`:120–129`). A `grep` for a hardcoded
`invalid_at IS NULL` in the search queries returns nothing. **So a plain search
surfaces invalidated (superseded) edges ranked alongside live ones** — honoring
the bitemporal model at read is opt-in. The model is maintained on write and not
enforced on read (the recurring pattern: GA's `filling`, Mem0's source, Graphiti's
`invalid_at`).

## Consolidation-adjacent machinery (community detection)

`utils/maintenance/community_operations.py`: `get_community_clusters` →
**`label_propagation`** (`:80, 93`) derives communities from the entity graph
(higher-order structure, algorithmic — not an LLM). `build_community` (`:174`)
creates a `CommunityNode` whose **summary is LLM-generated** by iteratively
`summarize_pair`-ing member summaries (`:141, 187`). Two maintenance modes:

- **Full rebuild** — `build_communities` (`:216`): recluster everything (failure
  #1657: `build_communities(group_ids=...)` first wipes *all* communities).
- **Incremental** — `update_community` (`:325`): on a new entity, attach it to a
  community and merge its summary via one `summarize_pair` (`:336`).

**Nuance:** incremental mode never re-runs label propagation, so community
*membership* drifts stale (new entities glued to the nearest existing cluster)
until a full, destructive rebuild. Higher-order structure exists but is not
cheaply kept current.

## Forgetting / decay — INVALIDATE, never auto-evict

Search performed across `graphiti.py` and `graph_data_operations.py`:
`grep -niE '\bttl\b|evict|decay|forget|prune|remove_episode'`.

- **No TTL, decay, or automatic eviction.** Supersession only sets
  `expired_at`/`invalid_at` (`edge_operations.py:569–570`); the edge row persists
  forever as a bitemporal record. The graph therefore **grows monotonically**,
  accumulating ever more invalidated edges (which, per Focus #3, still surface in
  default search).
- The **only deletion** is manual: `remove_episode` (`graphiti.py:1765`), and it
  deletes only edges *uniquely* sourced from that episode
  (`Edge.delete_by_uuids`, `:1790`). There is no size, age, or budget bound.

## Calibration / provenance

- **Calibration — ABSENT.** Reads carry RRF/MMR/cosine/BM25 fusion scores and a
  `reranker_min_score` cutoff — *retrieval relevance*, never a calibrated
  probability that a fact is true. No confidence, no abstention.
- **Provenance — PRESENT and first-class (the strongest of the three subjects).**
  Every `EntityEdge` cites its source episodes (`edges.py:267`) and every
  `EpisodicNode` lists the edges derived from it (`nodes.py:325`), backed by
  MENTIONS/HAS_EPISODE edges. You can trace any fact to the raw episodes that
  produced it. *Caveat:* provenance is **carried but not enforced** — search
  neither requires nor surfaces it as a gate, and `reference_time` is written on
  every edge yet never returned by any read path (failure #1661).

## Prospective memory — **ABSENT**

No `intend(condition → event)` and nothing that fires on a future write.
`valid_at`/`invalid_at` are *past/observed* event times, not future triggers.
Where a real prospective memory would live: a condition-indexed intention store
consulted inside `add_episode` on each new episode. No such store exists.

## Three failure modes (tracker)

1. **Contradiction/supersession collapses on weak models.** The dedup/
   contradiction judge (`dedupe_edges.resolve_edge`, run at `ModelSize.small`)
   silently stops detecting contradictions on non-reasoning small models; a
   reasoning-first schema is needed to restore it. Confirms supersession is
   model-dependent, not deterministic.
   https://github.com/getzep/graphiti/issues/1666
2. **`EntityEdge.reference_time` is write-only** — persisted on every edge, never
   returned by any read path. A temporal field maintained on write and ignored on
   read: the same shape as the default-search-ignores-`invalid_at` gap.
   https://github.com/getzep/graphiti/issues/1661
3. **`build_communities(group_ids=...)` wipes ALL communities, then rebuilds only
   the selected groups** — a destructive full-rebuild consolidation that can
   erase higher-order structure outside the requested scope.
   https://github.com/getzep/graphiti/issues/1657

## ONE technique worth stealing

**The bitemporal invalidate-not-delete edge.** A fact carries two independent
time axes — *valid time* (`valid_at`/`invalid_at`: when the fact was true in the
world) and *transaction time* (`created_at`/`expired_at`: when the graph believed
it) — and supersession **marks the old edge invalid rather than destroying it**
(`edge_operations.py:569–570`), so "what is true now," "what was true as-of T,"
and "what did we believe as-of T" are all answerable from one immutable trail.
This is the best existing answer to *facts change*, and it lands squarely in our
**Layer 6 (Contradiction & Dedup)** — supersede by invalidation, never overwrite
— and directly informs **Layer 8 (Revision & Forgetting)**. It fits our physics
better than Graphiti's does: our logical `t` is already an integer, so the four
marks become integer `t` stamps set by **deterministic** comparison (no wall
clock, no floats), curing the model-dependence that makes Graphiti's version
fragile.

## ONE mistake worth codifying (as a strain-trial idea)

**Mistake: the bitemporal truth is maintained but not the default at read — a
superseded fact keeps surfacing because plain search ignores `invalid_at`.** The
"current truth" query is opt-in, not the default (`search_filters.py:62–65`; no
default temporal WHERE). This is a Layer-6 / answer-contract failure: the default
answer must be *what is true now*, with superseded facts reachable only by an
explicit as-of override.

**Strain-trial idea (targets Layer 6 + our answer contract; extends
`corpora/l3stream`/`murk`):**
- *Corpus:* supersession chains per `(entity, key)` — fact `F` with
  `valid_at=t0`, then a superseding fact `F'` at `t1 > t0` that invalidates `F`
  (`F.invalid_at=t1`). Record in `ground_truth.json`, for each query time `τ`,
  the single fact valid at `τ`.
- *Manipulation that exposes it:* phrase the **stale** fact `F` so it is *more*
  lexically/semantically similar to the query cue than the current `F'` (e.g.
  `F` echoes the query's wording; `F'` is paraphrased). A retriever that ranks by
  similarity and ignores `invalid_at` will float the invalidated `F` to the top.
- *Assertions:* (a) a **default** "what is X?" query at "now" returns **only**
  `F'`, never the invalidated `F`, even though `F` scores higher on similarity;
  (b) an **as-of `τ0` (t0 ≤ τ0 < t1)** query returns `F` (bitemporal
  correctness); (c) store growth is bounded by live slots for querying purposes —
  invalidated facts are retained for audit but never returned as current.
- *Why it bites:* a Graphiti-style default search fails (a); our engine must make
  valid-as-of-now the default and require an explicit temporal override to reveal
  superseded facts — the property Layer 6 certifies.

## Constitutional note (no law-change objection)

No objection to the frozen `BOUNDARY.md`. Graphiti is the closest prior art to
our laws and mostly affirms them: its bitemporal invalidate-not-delete is what
**Layer 6** should institutionalize, and its first-class edge→episode provenance
is what **Layer 7** demands — but it also shows the two failure shapes our laws
exist to prevent: hard decisions left **model-dependent** (contradiction detection
that collapses on weak models, #1666 — our determinism law forbids this), and a
temporal/provenance model **maintained on write but not honored on read** (default
search ignores `invalid_at`; `reference_time` write-only, #1661 — our Layer-6
answer contract forbids this). No change is warranted; if anything Graphiti is the
proof that these laws are worth enforcing rather than leaving to a prompt.

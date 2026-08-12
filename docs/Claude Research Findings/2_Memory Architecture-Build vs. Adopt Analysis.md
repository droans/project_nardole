# Memory Architecture for a Local-First Personal AI Assistant

## TL;DR
- **Do not adopt Letta as your runtime, and do not build a full Letta-style core/recall/archival tier system.** Build a **custom memory layer on Meilisearch hybrid search plus a lightweight SQLite/Postgres relational store** for provenance, importance scores, permission scoping, and staleness. Meilisearch's hybrid retrieval + a small "working context" already covers most of what tiered memory buys a single-user assistant; the parts it doesn't cover (self-editing consolidation, contradiction handling, importance scoring) are cheaper to add as your own thin layer than to inherit an entire agent runtime that would duplicate your orchestration and permission layers.
- **Borrow specific mechanisms, not whole frameworks:** Generative Agents' recency×importance×relevance retrieval score (Park et al., UIST 2023), Zep/Graphiti's bi-temporal fact invalidation for contradiction/staleness, MemGPT's memory-pressure eviction concept, and Onyx's permission-mirroring (`allowed_principals` metadata filtered at retrieval, never at the LLM layer).
- **Your genuine differentiator — an inspectable "why did the assistant think this was important" signal — has no incumbent.** Treat every memory item as a provenance-bearing evidence object with a salience score, an evidence chain (source doc IDs + inference reasoning + confidence), and a bi-temporal validity window, all stored in the relational sidecar and surfaced in your raw-data-browsing UI.

## Key Findings

1. **Tiered memory is largely over-engineering for a single-user Meilisearch-backed assistant.** MemGPT's tiering solves a problem you mostly don't have: paging a fixed context window when history exceeds it. Meilisearch already does the "external context" retrieval job. What you should keep from the tiered model is not the three tiers but two orthogonal ideas: (a) a small always-in-prompt "core/working context" block, and (b) agentic self-editing/consolidation of durable facts.

2. **Custom-on-Meilisearch wins on integration fit; Mem0 is the fallback; Letta is the wrong shape.** Letta is a full agent runtime that would compete with your orchestration, permission, and tool layers. Mem0 is a clean, framework-agnostic, Apache-2.0 memory layer that composes with your OpenAI-compatible endpoint — but it introduces a second vector store (pgvector/Qdrant + optional Neo4j) that duplicates Meilisearch and hides its scoring/decay logic from your inspectable-UI goal.

3. **Importance scoring is a solved-enough research area you can adapt directly.** The canonical formula is Park et al.'s `score = α_recency·recency + α_importance·importance + α_relevance·relevance`. Gmail's Priority Inbox provides the production analog: a per-user model predicting the probability the user acts on an item.

4. **Proactivity without a heartbeat = an external scheduler/event bus that wakes a normal agent turn, gated by a confidence threshold.** Letta removed heartbeats because modern models self-terminate; it now recommends "custom prompting" for repeated triggering and offers "sleep-time agents" for background memory work. For a home server, use a hybrid: event-driven triggers (new email webhook/push, calendar-approaching) for freshness plus a low-frequency cron sweep for salience re-evaluation, each feeding a proactivity scorer that suppresses low-confidence items.

5. **Permission-scope memory by tagging each item with source account/integration and filtering at the retrieval layer**, exactly like Onyx mirrors source ACLs. Meilisearch's `filterableAttributes` enforce this deterministically before content reaches the model.

6. **Handle contradiction/staleness with bi-temporal validity windows and explicit supersession**, per the Zep/Graphiti design: never hard-delete, close the old fact's validity window and record the new one, so the assistant reasons over current state while history stays queryable and auditable.

## Comparison Table: Mem0 vs. Letta vs. Custom-on-Meilisearch

| Dimension | **Mem0** (memory layer) | **Letta** (agent runtime) | **Custom on Meilisearch + SQLite/Postgres** |
|---|---|---|---|
| **What it is** | Framework-agnostic memory layer you "bolt on"; passive fact extraction with ADD/UPDATE/DELETE/NOOP routing | Full stateful-agent runtime; "agents run inside Letta" — manages loop, tools, state, memory | Your own thin layer: Meilisearch as searchable index + relational sidecar for scores/provenance/scoping |
| **Integration complexity (Python home server)** | Low–moderate: 3 Docker containers (FastAPI API, Postgres+pgvector, Neo4j). `pip install mem0ai`, `Memory().add()/search()` | High: "a platform migration rather than a drop-in memory dependency"; overlaps your orchestration | Moderate: no new datastore beyond what you run; you write consolidation/decay/supersession yourself |
| **Maturity / stability** | 62,468 GitHub stars (Aug 4, 2026); v1.0.0 shipped Oct 16, 2025; 186M API calls Q3 2025 | Grew from MemGPT (13K+ stars); $10M seed at $70M post (Sept 2024); ships very rapidly | Depends on you; algorithms are well-documented and small |
| **Licensing** | Apache-2.0 (open-core risk: single vendor, $24M raised, no foundation) | Apache-2.0 core; cloud/ADE proprietary | Meilisearch CE = MIT; your code = yours |
| **Composes with OpenAI-compatible endpoint** | Yes — "works across OpenAI, Anthropic, and custom LLM endpoints" | Yes — BYOK OpenAI-compatible gateways, reasoning_effort passthrough | Yes — you call the endpoint directly |
| **Duplicates Meilisearch?** | Yes — introduces pgvector/Qdrant (+Neo4j) as a second vector store | Yes — Postgres+pgvector, its own hybrid+RRF search | No — single source of truth |
| **Fits inspectable "why important" UI?** | Poorly — importance/extraction logic is internal; only a SQLite op-audit trail | Poorly — self-editing memory is opaque, "harder to debug than a fixed pipeline" | **Yes — you design the provenance/score schema the UI reads** |
| **Conflicts with your permission/orchestration layer?** | Minimal — clean API boundary | **Yes — its agent loop, tool rules, identities duplicate yours** | None — you own it |
| **Used for personal (non-enterprise) assistants?** | Yes — OpenMemory MCP, local-mem0-mcp (fully offline w/ Ollama) | Mostly agent/coding-agent framing; "better suited to single-user deployments" per third parties | N/A (bespoke) |
| **Write-path cost** | One routing LLM call per batch of extracted candidates at every write | Every memory op costs inference tokens (agent reasons about what to store) | You choose — heuristic-only or optional LLM |

**Verdict:** Build custom. Fall back to Mem0 only if you find yourself reimplementing a large fraction of its extraction/consolidation pipeline — and even then, use it on the write path while keeping Meilisearch as the read index. Reject Letta as a runtime.

## Details

### 1. Tiered memory: necessary or over-engineering?

**What MemGPT/Letta tiering actually solves.** The original MemGPT paper (Packer et al., arXiv:2310.08560, Oct 2023, rev. Feb 2024) frames the problem as the fixed context window being a scarce resource: "we treat context windows as a constrained memory resource, and design a memory hierarchy for LLMs analogous to memory tiers used in traditional OSes." The abstract's framing: LLMs are "constrained by limited context windows," and MemGPT proposes "virtual context management ... drawing inspiration from hierarchical memory systems in traditional operating systems which provide the illusion of an extended virtual memory via paging between physical memory and disk." Its concrete failure cases and numbers:

- **Multi-session consistency (Deep Memory Retrieval / DMR task):** DMR tests "the consistency of a conversational agent" — asking a question that "explicitly refers back to a prior conversation." Fixed-context baselines saw only "a lossy summarization of the past five conversations to mimic an extended recursive summarization procedure," while MemGPT "has access to the full conversation history but must access it via paginated search queries." Accuracy (Table 2): GPT-4 **32.1% → 92.5%** with MemGPT; GPT-4 Turbo **35.3% → 93.4%**; GPT-3.5 Turbo **38.7% → 66.9%**. This is the "contradiction / forgetting old facts" failure quantified.
- **Document QA (retriever-reader on NaturalQuestions-Open):** "MemGPT's performance is unaffected by increased context length," whereas truncation-based fixed-context models degrade "as the necessary compression grows." Fixed-context baselines are "capped roughly at the performance of the retriever" — if the retriever misses the gold doc, they "never see" it, while MemGPT "can make multiple calls to the retriever by querying archival storage."
- **Nested key-value retrieval (multi-hop):** GPT-3.5 "hits 0 percent accuracy at 1 nesting level"; GPT-4 and GPT-4 Turbo "hit 0 percent accuracy by 3 nesting levels"; "MemGPT with GPT-4 ... is unaffected with the number of nesting levels."

**Why this maps weakly onto your system.** Three reasons the tiering payoff shrinks for you:

- **Meilisearch is your "external context."** MemGPT's central trick — page the full history in and out of a fixed window via search — is exactly what Meilisearch hybrid search gives you natively (keyword + vector, RRF-fused/scored, sub-50ms, native embedder support). The DMR baseline was crippled specifically because it only saw lossy summaries; you retrieve against the full corpus.
- **The Zep authors' critique of DMR applies to you:** DMR conversations contain only ~60 messages, "easily fitting within current LLM context windows" (Zep, arXiv:2501.13956, Jan 2025). Modern long-context models plus retrieval blunt the exact edge MemGPT measured.
- **Letta itself walked back the most "agentic" part.** In Letta V1 (Oct 14, 2025) heartbeats and `send_message` are deprecated because "understanding of the agentic control loop is baked into the underlying models."

**What you should still keep.** Two things tiering gets right that flat retrieval alone does not:
- **A small always-in-context "working memory" block** (Letta's "core memory," always visible "like RAM"; Generative Agents' equivalent) — persistent user facts (name, key preferences, household members) injected into every prompt without a retrieval call. Cheap and high-value.
- **Agentic self-editing / consolidation** — writing a durable, de-duplicated fact ("user's dentist is Dr. Lee, moved offices May 2026") rather than re-deriving it from raw email every time. Mem0 formalizes this as an LLM routing each candidate fact to ADD / UPDATE / DELETE / NOOP.

**When the difference starts to matter (volume/usage thresholds).** For a single user or small household, flat hybrid retrieval + working context is sufficient until: (a) you accumulate enough contradicting/superseding facts that recency-vs-relevance conflicts surface (a changed phone number retrieved alongside the old one); (b) durable preferences get buried under high-volume low-value data (the "flat memory" failure — a timezone preference outranked by a one-off weather comment); or (c) you want reflections/summaries over long spans. These are consolidation and scoring problems, not context-paging problems — which is why you can solve them with a thin layer, not a runtime.

### 2. Mem0 vs. Letta vs. custom — for this specific stack

**Mem0** (Apache-2.0; 62,468 GitHub stars as of Aug 4, 2026; v1.0.0 shipped Oct 16, 2025; the org reports growing "from 35 million [API calls] in Q1 to 186 million in Q3 2025"): a framework-agnostic memory *layer*, not a runtime. "You bolt it onto whatever agent framework you're already using." Composes cleanly with any OpenAI-compatible endpoint ("Works across OpenAI, Anthropic, and custom LLM endpoints"). Self-hosted stack is three Docker containers (FastAPI API, Postgres+pgvector, Neo4j for graph). It writes a SQLite audit trail of every memory operation. Used successfully for *personal* assistants (OpenMemory MCP runs Mem0 locally for Claude Desktop/Cursor; local-mem0-mcp runs fully offline with Ollama + phi3:mini). **Downside for you:** it introduces a *second* vector store (pgvector/Qdrant) that duplicates Meilisearch, and its importance/extraction logic is internal — working against your inspectable-UI differentiator. Write cost is one LLM routing call per batch of extracted facts, so cost scales with ingested volume regardless of novelty.

**Letta** (Apache-2.0; grew from MemGPT, which has 13K+ GitHub stars; raised a $10M seed led by Felicis at a $70M post-money valuation, announced Sept 26, 2024, with angels including Jeff Dean, Clem Delangue, and Cristóbal Valenzuela): a full stateful-agent *runtime*. "Agents don't just use Letta for memory; they run inside Letta. The framework manages the agent loop, tool execution, state persistence, and memory." Backed by Postgres + pgvector, hybrid search fused with RRF. Model-agnostic, supports OpenAI-compatible BYOK gateways. **Downside for you:** adopting it "is a platform migration rather than a drop-in memory dependency." Its agent loop, tool rules, tool execution, and multi-user "identities" directly overlap and would compete with your own orchestration and per-(task×integration×account) permission system. Using it purely for archival memory is technically possible — the arXiv study 2606.15903 hit Letta's archival REST endpoints (`POST/GET/DELETE /v1/agents/{aid}/archival-memory`) directly, "keeping the LLM out of the recall hot path" — but at that point you're running a heavy agent server as a glorified vector store, which pgvector or Meilisearch does more simply.

**Custom on Meilisearch + SQLite/Postgres sidecar:** you already run Meilisearch as primary store. Add a relational sidecar for memory-item metadata: importance score, provenance chain, permission tags, validity windows, access counters. Retrieval = Meilisearch hybrid query (permission-filtered) → re-rank by composite recency/importance/relevance score computed from sidecar fields. **Upside:** no duplicate vector store, full control over the scoring/provenance the UI needs to expose, minimal new infra, no runtime lock-in. **Downside:** you build (and maintain) consolidation, decay, and supersession logic yourself — though the algorithms are well-documented and small.

**Licensing note:** Meilisearch Community Edition is MIT; an Enterprise Edition under BUSL was introduced (2025) for large-scale security/observability features irrelevant to a single-user deployment. Both Mem0 and Letta are Apache-2.0. Note the open-core risk flagged by observers: Mem0 is a single VC-backed vendor with **$24M raised** (a Kindred Ventures–led seed plus a $20M Series A led by Basis Set Ventures announced Oct 28, 2025, with Peak XV, GitHub Fund, and Y Combinator) and no independent foundation, so a future relicensing to a restrictive source-available license is a structural (not current) risk.

### 3. Representing and storing "inferred importance"

**No surveyed system exposes an inspectable importance signal — this is your differentiator, and recent research validates the shape it should take.** The survey "From Agent Traces to Trust" (arXiv:2606.04990) argues memory items should be treated as "provenance-bearing evidence objects whose origins, updates, retrievals, validity, and downstream influence should remain inspectable," with typed relations (Support, Depend-on, Contradict, Update, Invalidate). A commercial system, Hakuya, already ships "provenance on every belief" where "each memory carries its source, evidence type, and confidence."

**The scoring literature you can adapt directly:**
- **Generative Agents (Park et al., Stanford, UIST 2023):** `retrieval_score = α_recency·recency + α_importance·importance + α_relevance·relevance`. Recency is an exponential decay — verbatim: "we treat recency as an exponential decay function over the number of sandbox game hours since the memory was last retrieved. Our decay factor is 0.995"; relevance = cosine similarity; importance = an LLM rating 1–10 assigned at write time. The reference implementation (retrieve.py) used weights — verbatim: "The composite score is recency×0.5 + relevance×3 + importance×2, with all dimensions normalized to [0, 1]. The top 30 nodes by composite score enter the planning context." This is "the de facto standard for agent memory retrieval ... Adopted by virtually every subsequent system (MemGPT, Mem0, LangGraph)."
- **Gmail Priority Inbox (Aberdeen, Pacovsky, Slater, NIPS 2010 workshop):** "ranks mail by the probability that the user will perform an action on that mail" via "a per-user statistical model of importance, updated as frequently as possible," inferring importance "without explicit user labelling" and using thresholds the user can tune. This is the production template for personal-stream salience: learn from implicit signals (opens, replies, stars, deletes).
- **Newer critique to design around:** Park's importance term is "static — assigned once at write time and never updated by outcomes" (arXiv:2604.12007). Design your score to be updatable by access frequency and downstream use, not frozen at write.

**Recommended importance model for you (hybrid, cheap):** a base heuristic score (sender is a known contact, contains action verbs/dates/amounts, thread activity) + an optional LLM rating for ambiguous items + implicit-feedback updates (did the user open/act on the surfaced item?). Store the components, not just the final number, so the UI can explain "scored high because: from a frequent contact, contains a deadline, you replied to this thread twice."

**Decay/update over time.** The dominant pattern is a recency-weighted composite that multiplies relevance by an exponential decay of time-since-last-access, so unreferenced items fade. Concrete parameterizations in the literature: Ebbinghaus-style `I(t) = I₀·e^(−λt)` with λ≈0.001/hour (half-life ≈29 days) in one human-inspired architecture (arXiv:2605.08538); a dual-layer scheme (fast-fading short-term vs. slow-fading long-term) in FadeMem, reported at "45% less storage." Best practice: **passive decay for noise (TTL/LRU on low-value items), active supersession for facts (never silently decay a stated fact — invalidate it explicitly when contradicted).** Note the GDPR angle: an append-only memory that "remembers everything forever" is a deletion-request liability (GDPR Article 17), so a decay/eviction log doubles as a compliance record.

### 4. Triggering background/proactive reasoning without a heartbeat

**Why the heartbeat went away and what replaced it.** Letta V1 (Oct 2025): "Agents no longer understand the concept of heartbeats (unless implemented manually). For repeatedly triggering agents to run independently (e.g., processing time or sleep-time compute), you'll need custom prompting to explain this environment to the agent." Letta's structured answer is **sleep-time agents**: background agents that "run in the background between conversations to consolidate fragmented memories ... reorganize and deduplicate ... archive and prune outdated" items, triggered "after a configured number of user messages or when the context window is compacted." Note this is background *memory maintenance*, not inference-driven *proactivity* — it does not decide to surface something to the user. (Letta's own guidance: run the sleep-time agent on a stronger, less latency-constrained model while the foreground uses a fast one.)

**Trigger mechanism tradeoffs for a home server:**
- **Polling/cron:** simplest; robust to missed webhooks. But wastes compute checking for changes that haven't happened, and can blow through upstream API rate limits (a cited example: 100 endpoints polled every 30s = 12,000 GitHub req/hr against a 5,000/hr cap). Mitigate with conditional GET (ETags/If-Modified-Since). Best for: low-frequency salience re-evaluation sweeps.
- **Event-driven (webhook/push):** near-real-time and efficient (one widely-repeated third-party claim attributes a "70–90%" latency reduction to Confluent, but that exact figure does not appear in Confluent's own material — treat as unverified vendor attribution). Key caveat: "a webhook tells me something changed. It does not tell me the truth about what changed, or in what order" — you need idempotent handlers keyed on a stable event ID to avoid duplicate/stale reasoning. Best for: freshness-critical triggers (new email, calendar event approaching).
- **Periodic salience re-evaluation:** re-score existing memory as context changes (a deadline that was low-priority last month becomes urgent). Cheapest as a nightly batch; risk is staleness between runs.

**Recommended hybrid:** event-driven for the handful of high-value freshness triggers + a low-frequency cron sweep for salience re-scoring + a Generative-Agents-style **reflection trigger** (fire background synthesis when *cumulative importance of recent observations crosses a threshold*, rather than on a fixed schedule).

**Confidence gating before surfacing (the trust problem).** Prior research found even "notify"/"suggest" proactivity must be high-precision or it erodes trust. The pattern from a proactive-enterprise-agents paper (arXiv:2607.07721) is a dedicated **Proactivity Scorer** ranking candidate insights across "urgency, relevance, persona-fit, and confidence," reporting Precision@5 = 0.83 and a false-positive rate of 0.11 in their case studies (vendor-authored; treat as illustrative). General confidence-threshold practice from adjacent fields (SOC alerting, customer-support notifications): (a) tune the threshold on the precision/recall curve deliberately, biasing toward precision for proactive pushes; (b) use **tiered surfacing** — high confidence → notify; medium → hold in a "for review" queue in the raw-data UI rather than interrupting; low → log only; (c) **calibrate** confidence against actual accuracy before trusting thresholds (a model reporting 0.9 may be right only ~70% of the time); (d) require corroboration from more than one independent signal before a proactive push. Log every trigger's reasoning for transparency and learning — which dovetails with your provenance model.

### 5. Multi-account / multi-integration memory scoping

**Scope memory items with the same granularity as your permission system and enforce at the retrieval layer.** The Onyx/Danswer pattern is the direct model: connectors set to "Auto Sync Permissions" "maintain an access control list from the source and restrict users to only see data they have access to" — "Access mirrors the source system," mirroring source ACLs at sync time (Onyx syncs from Confluence, Jira, GitHub, Google Drive, Gmail, Slack, Salesforce, SharePoint).

**The enterprise multi-tenant RAG consensus, applied to your single-user/multi-account case:**
- **Tag at ingestion, filter at query.** "At ingestion time, attach an `allowed_principals` metadata field to each chunk listing the user and group IDs from the source system who can read the underlying record. At query time, add a filter that intersects the calling user's groups with `allowed_principals`."
- **Never filter at the LLM layer.** "LLMs are probabilistic and susceptible to prompt injection. Instructing the model to only use Tenant A's documents will fail under adversarial conditions. Enterprise security requires deterministic guarantees, meaning filtering must happen at the database retrieval layer before context reaches the model."
- **Meilisearch supports this natively:** add your scoping fields (`integration`, `account_instance`, `task_type`, `allowed_principals`) to `filterableAttributes`; every memory query is issued with a filter derived from the active permission context. Filterable attributes must be declared before use and changing them triggers reindexing — so design your scoping schema up front. Meilisearch's own docs note filters' use-case explicitly: "restricting the results a specific user has access to." Add Meilisearch tenant tokens / scoped API keys as a defense-in-depth second layer.

For your model, each memory item's scope should be the tuple **(task_type × integration × account_instance)** that produced it, so a query issued in one permission context can never surface a memory derived from data the current context shouldn't see. Where a memory is synthesized from multiple sources spanning contexts, it inherits the *intersection* (most restrictive) of their scopes, or is split.

### 6. Conflicting / stale information handling

**The state-of-the-art pattern is bi-temporal fact validity with explicit supersession, from Zep/Graphiti** (Rasmussen et al., "Zep: A Temporal Knowledge Graph Architecture for Agent Memory," arXiv:2501.13956, Jan 2025). Two independent time axes per fact: **event time T** (when the fact was true in the world) and **ingestion/transaction time T′** (when the system learned it). "When the system identifies temporally overlapping contradictions, it invalidates the affected edges by setting their `t_invalid` to the `t_valid` of the invalidating edge" — the old fact is "invalidated but preserved," never deleted. This lets the assistant "reason over the current state while the history stays queryable," and answer "what did we know as of date X." An LLM compares each new fact against semantically related existing facts to detect contradictions, constrained to the same entity pair to bound cost. (Zep reports 18.5% accuracy improvement on LongMemEval and 90% lower latency vs. a MemGPT baseline — vendor-reported.)

**The risk of acting on stale data is the core trust hazard for a personal assistant** — texting an old phone number, showing up at a rescheduled meeting's old time, honoring a superseded preference. Mitigations, layered:
- **Timestamps + recency weighting** so newer facts win ties in retrieval (the "customer migrated Postgres→MySQL" case where equal-weight memory picks whichever the retriever scored higher).
- **Explicit supersession** (Zep pattern above) so contradictions are resolved at write time, not left for the retriever to arbitrate. Mem0 formalizes this as its UPDATE/DELETE routing; a "reasonable production policy" is "active supersession on every write so contradictions never accumulate."
- **Source-of-truth hierarchies:** for structured facts (calendar time, contact phone), treat the integration as authoritative over free-text mentions — a calendar API's event time supersedes an email saying "let's meet at 3." Encode source authority as a field so conflict resolution is deterministic where possible and LLM-mediated only where not.
- **Surface conflicts in the UI** rather than silently resolving, given your raw-data-browsing surface: show "phone number changed May 2026 (superseded: old number)" with both the current value and the invalidated one.

## Proposed Data Model Sketch (implementation-ready)

Two stores working together: **Meilisearch** (the searchable index; one document per memory item, embeddings auto-generated) and a **relational sidecar** (SQLite for single-user; Postgres if the household grows) holding the structured metadata, scores, provenance graph, and validity windows. The sidecar is the source of truth for scoring/provenance/permissions; Meilisearch mirrors the fields needed for filtering and first-pass ranking.

### `memory_item` (relational sidecar + mirrored to Meilisearch)
```
id                    UUID (pk)
content               TEXT            -- the durable fact/summary, human-readable
content_type          ENUM            -- fact | preference | event | reflection | observation
embedding             (managed by Meilisearch embedder; not stored here)

-- Importance / salience (components stored, not just final score)
importance_base       REAL            -- heuristic score at write time [0,1]
importance_llm        REAL NULL       -- optional LLM 1–10 rating, normalized [0,1]
importance_current    REAL            -- live composite, updated by feedback/decay
salience_components   JSON            -- {from_known_contact:true, has_deadline:true, thread_replies:2, ...}
confidence            REAL            -- system confidence in the item's correctness [0,1]

-- Recency / decay
created_at            TIMESTAMP
last_accessed_at      TIMESTAMP       -- updated on retrieval; feeds recency decay
access_count          INTEGER
decay_lambda          REAL            -- per-item decay rate (fast for noise, slow for facts)
ttl_expires_at        TIMESTAMP NULL  -- passive eviction for low-value items

-- Bi-temporal validity (contradiction/staleness)
valid_from            TIMESTAMP       -- event time: when true in the world
valid_until           TIMESTAMP NULL  -- NULL = currently valid; set on supersession
ingested_at           TIMESTAMP       -- transaction time
superseded_by         UUID NULL       -- fk -> memory_item.id (the newer fact)
status                ENUM            -- active | superseded | expired | user_deleted

-- Permission scoping (mirrored to Meilisearch filterableAttributes)
integration           TEXT            -- e.g. gmail, gcal, whatsapp
account_instance      TEXT            -- which connected account produced it
task_type             TEXT            -- the permission task-type bucket
allowed_principals    JSON/ARRAY      -- principal/group IDs allowed to see it (Onyx-style)
source_authority      INTEGER         -- for source-of-truth hierarchy tie-breaks

-- Housekeeping
updated_at            TIMESTAMP
```

### `provenance_edge` (the inspectable evidence chain)
```
id                    UUID (pk)
memory_id             UUID  fk -> memory_item.id
relation              ENUM  -- derived_from | supports | contradicts | updates | invalidates
source_kind           ENUM  -- raw_document | tool_output | user_statement | other_memory | inference
source_ref            TEXT  -- Meilisearch doc id / message id / tool-call id
reasoning             TEXT  -- natural-language "why this mattered" (the UI-surfaced explanation)
confidence            REAL
created_at            TIMESTAMP
```
This table is what powers the "why did the assistant think this was important" UI: for any memory item, walk its `provenance_edge` rows to show the source documents, the inference reasoning, and the confidence — plus any `contradicts`/`invalidates` edges to show supersession history. The typed relations map directly to the "From Agent Traces to Trust" schema (Support / Depend-on / Contradict / Update / Invalidate).

### `feedback_event` (updates importance from implicit/explicit signals)
```
id            UUID
memory_id     UUID
signal        ENUM   -- surfaced | user_opened | user_acted | user_dismissed | user_pinned | user_corrected
weight        REAL
created_at    TIMESTAMP
```

### Retrieval flow
1. Derive permission filter from active context: `integration IN (...) AND account_instance IN (...) AND task_type = ... AND allowed_principals INTERSECTS caller_groups AND status = 'active' AND (valid_until IS NULL OR valid_until > now())`.
2. Issue Meilisearch hybrid query with that filter (deterministic pre-LLM gate).
3. Re-rank candidates by composite `score = w_r·recency(last_accessed_at, decay_lambda) + w_i·importance_current + w_rel·semantic_similarity`, optionally minus a staleness penalty.
4. Inject top-N into working context; update `last_accessed_at`/`access_count`.
5. On write of a new fact, run supersession check against same-entity items; set `valid_until`/`superseded_by`/`status` on the old, add `provenance_edge` (relation=`invalidates`).

## Recommendations

**Stage 1 — Ship flat + working context + provenance (weeks, not months).** Build the custom layer: memory items in Meilisearch with the sidecar schema above. Implement (a) a small always-in-prompt working-context block of durable user facts, (b) the permission filter at the Meilisearch query layer with `allowed_principals`, (c) the `provenance_edge` table and the UI view that renders it. Skip LLM importance ratings initially — use the heuristic `importance_base` only. **Benchmark to advance:** if users report the assistant surfacing buried/irrelevant memories, or retrieving contradicting facts, proceed to Stage 2.

**Stage 2 — Add scoring, decay, and supersession.** Turn on the composite recency×importance×relevance re-rank, per-item decay (fast λ for observations, slow for facts), and the bi-temporal supersession check on write. Add `feedback_event` capture so importance updates from what the user actually opens/acts on (the Gmail Priority Inbox lesson). **Benchmark to advance to proactivity:** only once retrieval quality and contradiction handling are trusted — proactivity on a shaky memory base amplifies errors.

**Stage 3 — Proactivity, gated hard on confidence.** Add event-driven triggers for high-value freshness events + a nightly salience-re-scoring sweep + reflection-on-importance-threshold. Route candidates through a proactivity scorer; **start with a deliberately high confidence threshold biased toward precision**, use tiered surfacing (notify / hold-for-review / log-only), and calibrate confidence against observed accuracy before loosening. **Threshold to loosen:** only after measuring a low false-positive rate on the hold-for-review queue over a sustained period.

**Reassess the build-vs-adopt decision if:** (a) the household grows to many users with complex cross-user sharing (then Mem0's multi-user primitives or Letta's identities become more attractive); (b) you find yourself reimplementing a large fraction of Mem0's extraction/consolidation pipeline (then adopt Mem0 as the write-path layer while keeping Meilisearch as the read index); or (c) Meilisearch relicenses its core away from MIT (monitor this).

**Do not** adopt Letta as a runtime — it duplicates your orchestration and permission layers and is "a platform migration rather than a drop-in." **Do not** rely on the LLM to self-filter by permission — enforce deterministically at retrieval. **Do not** hard-delete superseded facts — invalidate and preserve.

## Caveats

- **Benchmark framing is contested and often vendor-authored.** MemGPT's DMR numbers (35.3%→93.4%) are real and from the primary paper, but the DMR task itself is criticized (by a competitor, Zep) as too easy for modern long-context models. The proactivity Precision@5=0.83 figure, Zep's "18.5%/90%" improvements, and the "70–90% latency reduction" for event-driven architectures are from vendor/vendor-adjacent sources (the last is an unverified third-party attribution to Confluent) and should be treated as illustrative, not guarantees.
- **Importance scoring is inherently personal and noisy.** Gmail's own research notes importance must be inferred "without explicit user labelling" from "non-stationary and noisy training data," and that users still need to "tune their threshold." Expect a cold-start period and design for user correction.
- **Time-sensitivity of library claims:** Letta V1's heartbeat removal is dated Oct 14, 2025; Mem0 v1.0.0 is dated Oct 16, 2025 (62,468 stars as of Aug 4, 2026); Meilisearch's Enterprise/BUSL split and hybrid-search features are current as of mid-2026. Verify versions at implementation time, as all three projects ship rapidly.
- **The single biggest unquantified risk is the LLM cost/latency of write-time consolidation and contradiction-checking** at your data volumes (email/calendar/messages can be high-throughput). Mem0's design incurs "one routing LLM call per batch of extracted candidates at every write step"; budget for this and consider using a smaller/cheaper local model for the write path (the sleep-time pattern: fast model foreground, cheaper model for background maintenance).

## Open Questions (feed into permissions-system and infrastructure research prompts)

1. **Permissions:** When a memory is synthesized from sources spanning multiple (task×integration×account) scopes, what is the exact resolution rule — intersection (most-restrictive), split-into-per-scope-copies, or a new "derived" scope class? This needs a formal policy in the permissions research.
2. **Permissions:** How are `allowed_principals` kept in sync when source-system permissions change *after* ingestion (Onyx re-syncs ACLs on a schedule)? Does memory need a re-scoping sweep, and what's the staleness tolerance?
3. **Infrastructure:** What is the write-path LLM budget (calls/day, latency, local vs. hosted model) for consolidation, importance rating, and contradiction-checking at realistic personal-data volumes? This determines whether the sleep-time (background, cheaper-model) pattern is mandatory.
4. **Infrastructure:** Does the reflection/salience-re-scoring sweep run as a separate scheduled process, and how does it coordinate with Meilisearch reindexing (which is triggered by `filterableAttributes` and embedder changes)?
5. **Infrastructure:** Event-driven triggers require durable, idempotent event handling (stable event IDs, dedup). What message-queue/scheduler primitive fits a single home-server deployment without heavy infra?
6. **Both:** Should the provenance/audit log be tamper-evident (Hakuya-style hash-chaining) for a personal assistant, or is that over-engineering outside regulated contexts? This trades UI trust/GDPR-defensibility against complexity.

# Project Nardole

A local-first, home-server-hosted personal AI assistant written in Python — modeled on the capable, proactive AI assistants seen in film/TV rather than a narrow productivity tool.

This file exists because Claude Code sessions don't have access to the research and decisions made in the corresponding claude.ai Project. Keep it updated as architecture decisions get finalized.

## Core Defining Traits

- **Ingestion & retrieval**: Personal data (email, calendar, messages, files) ingested into **Meilisearch** for hybrid keyword + vector search
- **Proactivity**: Ability to work proactively with user approval
- **Agentic execution**: Can take real actions (send email, create calendar events, etc.)
- **Permission system**: Granular, fail-secure, scoped per `task_type × integration × account_instance`. Three states: Always Allow / Always Ask / Always Deny. Full audit logging. No silent failures.
- **Interfaces**: Chat, raw ingested-data browser (first-class surface, not an afterthought), MCP server, REST API
- **Model-agnostic**: OpenAI-compatible endpoint; local model support via Ollama or similar
- **LLM-only-when-necessary**: Deterministic-first design — don't reach for the LLM when plain code will do
- **Scope of responsibility**: Legal/compliance scoping is the end user's job; integrations self-report failures rather than failing silently

## Design Philosophy

- **Research before code.** Architecture decisions are made only after sequenced research, not assumed upfront.
- **Concrete over aspirational.** Goals must be falsifiable — the standard is "could point to this and say yes or no." Buzzwords and unmeasurable language are rejected.
- **Lean-first with documented graduation triggers.** Prefer the simplest implementation that works, with explicit, defined conditions for when to add complexity — don't pre-build for scale that isn't needed yet.

## Status: Research Completed So Far

### 1. Prior art & market research
Surveyed: Khoj, Leon, Letta/MemGPT, Home Assistant Assist, AnythingLLM, Onyx/Danswer, Rasa, Microsoft Copilot/Recall, Apple Intelligence.

**Finding:** No existing open-source project combines all four defining traits. Three genuine differentiation opportunities:
1. Inferred-importance proactivity (not schedule-based)
2. Granular per-instance permission system
3. Raw data browser as a first-class surface (no incumbent treats this as first-class)

### 2. Memory architecture research
**Recommendation:** Custom memory layer on Meilisearch + a SQLite/Postgres relational sidecar.

**Alternative on the table:** Lean-first — everything in Meilisearch initially, graduate to a sidecar only when triggered. Three specific triggers identified where Meilisearch alone breaks down:
- High-frequency mutable state
- Graph-shaped provenance requiring multi-hop traversal
- Atomic transactions during fact supersession

**Open question, not yet resolved:** whether to formally adopt lean-first-with-graduation-triggers as the recommendation, or commit to the sidecar from day one.

## Key Research Findings to Carry Into Design

- **Proactivity trust (Meurisch et al., ACM IMWUT 2020):** fully autonomous AI action is the *least* preferred mode; suggest-and-confirm is most preferred.
- **Proactivity trust (Kraus et al., IEEE Access 2021):** "Intervention"-level proactivity shows no trust growth over time.
  - **Implication for Nardole:** "Always Allow" should be deliberately hard to reach by design, not a default users fall into casually.
- **Permission system validation:** Onyx's permission-mirroring pattern + the OWASP agentic security framework (v2.01, June 2026) both support scoped-permission + audit-log as the primary defense. Prompt injection may be structural rather than something you can patch away — design permissions assuming injection will happen.
- **Silent failures kill trust:** Google's Gemini transition documented silent action failures on high-frequency tasks as a "confidence killer." This directly validates the no-silent-failures requirement.
- **"Local = private" is not a security argument on its own:** Microsoft Recall's repeated failures are the cautionary example — local storage still needs real access controls.
- **Recurring utility must precede monetization theory:** Amazon Alexa's trajectory (~$25B in losses, reduced to "smart timer" in practice) — don't build for a business model before the core utility loop actually works.

## Tools & Stack

- **Meilisearch** — primary search/retrieval store
- **Python** — implementation language
- **Ollama** (or similar) — local model serving
- **OpenAI-compatible REST endpoint** — model abstraction layer
- **MCP (Model Context Protocol)** — third-party client interface

## On the Horizon

- Verification pass on the goals/features section against the "yes or no" falsifiability standard
- Likely future research: permissions design, infrastructure/build recommendations, proactivity engine design
- Pending architecture decisions: final call on memory model (lean vs. sidecar-from-day-one), permission system implementation details

---
*This file is maintained manually — the claude.ai Project and Claude Code do not sync automatically. Update it when research or architecture decisions land in the Project.*

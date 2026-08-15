---
id: ADR-012
version: 1.0.0
authority: normative
owner: Platform Architecture
date: '2026-08-10'
title: Render-First Platform and PostgreSQL Consolidation
status: superseded
related_specs:
- SPEC-002A
- SPEC-016
- SPEC-019
- SPEC-020
- SPEC-021
- SPEC-022
- SPEC-023
- SPEC-024
- SPEC-025
---

# ADR-012: Render-First Platform and PostgreSQL Consolidation

| Status | Superseded by [ADR-013](ADR-013-cloudflare-workers-public-host.md) |
| --- | --- |
| Date | 2026-08-10 |
| Related specs | SPEC-002A, SPEC-016, SPEC-019, SPEC-020–025 |

## Context

The platform already separates **logical capabilities** from **physical deployment** ([SPEC-002A](../specs/SPEC-002A-architectural-principles.md), [ADR-010](ADR-010-future-services.md)). Early product work and pilot hosting notes accumulated heterogeneous stack assumptions (static GitHub Pages + separate backend, optional Supabase, multi-vendor host recipes, and implementation-repo mentions of Vercel Edge patterns). That spread increased inference cost for engineers and coding agents without improving financial correctness or auditability.

Goals for the preferred implementation path:

- fewer infrastructure surfaces
- production viability without premature distribution
- financial and audit correctness on relational transactions
- clear environment, webhook, and migration contracts
- agentic extensibility without AI becoming financial authority
- reproducible deployment via Infrastructure-as-Code

## Decision

1. **Render** is the preferred application and runtime platform for AGI product implementations that follow the platform’s recommended physical architecture.
2. **Render PostgreSQL** is the preferred canonical application datastore.
3. **Next.js (TypeScript)** begins as a **modular monolith** web service on Render (UI, route handlers, server actions, domain modules, webhooks).
4. **Drizzle ORM** is the preferred schema/migration layer for PostgreSQL (migrations remain explicit and reviewable; the live database is authoritative).
5. Specialized external providers remain in the preferred path:
   - **Clerk** — authentication and sessions
   - **Stripe** — payment processing
   - **Resend** — transactional email
   - **OpenAI** — primary AI provider (optional specialized providers behind abstractions)
6. **Escalation layers only with evidence:** Render Background Workers, Cron Jobs, Private Services, Key Value, and Workflows are optional. The MVP baseline is GitHub → Render (web + PostgreSQL) + the external providers above.
7. Logical capability boundaries, lifecycle, and contracts remain deployment-independent for **conformance**. Alternate topologies may still conform ([SPEC-013](../specs/SPEC-013-repository-conformance.md)); this ADR defines the **preferred** path that implementation teams should default to.

## Rationale

- Operational simplicity: one host family for web + database + optional workers/cron.
- Relational and transactional semantics for donations, allocations, ledger, and webhooks.
- Auditability: append-oriented financial history in PostgreSQL with reconstructable state.
- Lower vendor count for baseline infra vs multi-host + multi-backend combinations.
- Clean scale path: add workers/cron/cache/replicas only when workload evidence requires them.
- Infrastructure as code: `render.yaml` / Render Blueprints for reproducible deploys.

## Consequences

- Convex-style or BaaS-as-primary-persistence patterns are **not** the preferred path; any residual mentions are historical or pilot-specific.
- Vercel-as-primary-host and Vercel-specific serverless boundaries are **not** the preferred path; residual mentions in pilot notes are historical.
- Relational schema design and migrations become first-class implementation work.
- Real-time multiplayer features (if required) need explicit design (e.g. polling, SSE, or later optional infrastructure)—not assumed via a realtime BaaS.
- Database lifecycle (backups, migrations, restore, access control) is an engineering responsibility on Render PostgreSQL.
- Preferred stack documentation lives in [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)–[SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md) and [implementation guidance](../docs/implementation-guidance.md).

## Alternatives considered

| Alternative | Why not preferred |
| --- | --- |
| Vercel + Convex | Extra BaaS semantics; weaker fit for financial ledger transactions and audit reconstruction as primary store |
| Vercel + managed Postgres | Viable app hosting, but preferred path consolidates web + Postgres operational surface on Render |
| Render + Convex | Unneeded dual persistence model for MVP |
| Supabase as primary platform | Acceptable as historical pilot auth/data surface; not preferred canonical stack going forward |
| Bespoke multi-cloud stack | Higher ops cost without proven workload need |

## Status

**Superseded** (2026-08-13) by [ADR-013](ADR-013-cloudflare-workers-public-host.md) (Cloudflare + Supabase hosted platform). Keep this file for history. Render is no longer the preferred application host; allocation middleware, webhooks, and PostgreSQL-backed services belong on Workers talking to Supabase. Logical modular-monolith principle is unchanged.

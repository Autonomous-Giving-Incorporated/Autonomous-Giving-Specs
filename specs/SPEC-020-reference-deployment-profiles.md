---
id: SPEC-020
title: Reference Deployment Profiles
version: 2.0.0
status: accepted
authority: informative
owner: Platform Architecture
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-011
- SPEC-013
- SPEC-021
- SPEC-022
- SPEC-025
related_adrs:
- ADR-001
- ADR-010
- ADR-012
related_contracts: []
---

# SPEC-020: Reference Deployment Profiles
| Version | 2.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-006, SPEC-021 | Related ADRs | ADR-001, ADR-010, ADR-012 | Related contracts | None |

## Purpose

Publish **informative** reference deployment profiles so implementers share a clear MVP path without reading premature distribution into the platform canon. Version 2 aligns the recommended physical profile with the **Render-first** preferred stack ([ADR-012](../adr/ADR-012-render-first-platform.md), [SPEC-021](SPEC-021-preferred-application-stack.md)).

## Scope

Physical deployment examples only. Logical capabilities remain defined by [SPEC-006](SPEC-006-capability-boundaries.md). These profiles are **examples, not requirements** for conformance.

## Authority

This specification is **informative**. Conformance is not conditioned on selecting a profile ([SPEC-013](SPEC-013-repository-conformance.md)). Implementations MAY invent other topologies that preserve capabilities, contracts, and lifecycle.

## Architectural rule

**Do not create distributed infrastructure before workload evidence requires it.**

## Profile A — Demo

| Element | Choice |
| --- | --- |
| Frontend | Static host or local Next.js |
| Data | Static fixtures ([Community AI Lab](../demo/community-ai-lab/)) |
| Backend | None required |
| Secrets | None |
| Infrastructure | None |

Use for narrative demos and deterministic replay without operational systems.

## Profile B — MVP (**recommended**)

```text
GitHub
  ↓
Render
├── Next.js web service  (modular monolith)
│     UI + route handlers + server actions
│     domain modules (Fund Intel | Autonomous Giving | Impact Relay)
│     webhooks, authz, AI entrypoints
└── PostgreSQL
      (canonical application datastore)

External (preferred):
├── Clerk   (authentication)
├── Stripe  (payments)
├── Resend  (transactional email)
└── OpenAI  (primary AI; provider abstraction)
```

| Characteristic | Value |
| --- | --- |
| Executables | Single Next.js web service |
| Deployments | Single operational unit on Render |
| Database | One primary Render PostgreSQL |
| ORM / migrations | Drizzle; explicit reviewable migrations |
| Auth | Clerk (identity); AGI owns authorization |
| Payments | Stripe |
| Email | Resend |
| AI | OpenAI primary |
| Worker / cron / KV | **Not** required for baseline |
| Orchestration / broker / mesh | Not required |

Capabilities remain separate **in code**. Deployment remains **unified**.

### Preferred stack (MVP)

| Concern | Recommendation |
| --- | --- |
| Platform | Render |
| Application | Next.js + TypeScript |
| Database | Render PostgreSQL |
| Migrations | Drizzle explicit migrations |
| Authentication | Clerk |
| Authorization | Application-owned policies |
| Payments | Stripe |
| Email | Resend |
| AI | OpenAI via `AIProvider` abstraction |
| IaC | `render.yaml` / Blueprints |
| VCS | GitHub |

Full stack detail: [SPEC-021](SPEC-021-preferred-application-stack.md). Persistence: [SPEC-022](SPEC-022-postgresql-persistence.md). Ops: [SPEC-025](SPEC-025-operations-deploy-and-scale.md).

## Profile C — Production scale-out

Same modular application, optional:

- horizontal web instances
- Render Background Worker (async job consumers)
- Render Cron Jobs (reconciliation/reporting)
- tighter observability and backup tiers

Still one logical system; **not** a microservices mandate.

## Profile D — Enterprise

Optional extraction of capabilities, optional private services, optional streaming, optional multi-region, optional specialized vector DB. Adopt only with operational justification ([SPEC-002A](SPEC-002A-architectural-principles.md), [SPEC-025](SPEC-025-operations-deploy-and-scale.md) scale triggers).

## Evolution path

```text
Phase 0  Spec consolidation (this repository)
Phase 1  Platform foundation (Next.js + Postgres + Drizzle + Clerk + Render)
Phase 2  Financial core (Stripe + ledger + webhooks + receipts)
Phase 3  Allocation system (funds, programs, disbursements)
Phase 4  Operations (reconciliation, reporting, audit surfaces)
Phase 5  AI assistance (matching, analysis, recommendations + provenance)
Phase 6  Async/scale extraction (workers/cron/KV/private only with evidence)
```

## Historical note (superseded preferred diagrams)

Earlier v1 diagrams showed **GitHub Pages + generic single backend + optional object storage** as the illustrative MVP. That logical modular-monolith idea remains valid; the **preferred physical stack** is now Render + Next.js + PostgreSQL + Clerk/Stripe/Resend/OpenAI. Pilot notes mentioning Supabase, multi-host recipes, or Vercel Edge patterns are **historical or product-local**, not the platform preferred path.

## Non-goals

This document does not force Profile D, require Kubernetes, or condition conformance on Render. It replaces any implication that distributed infrastructure or multi-vendor BaaS is the reference MVP shape.

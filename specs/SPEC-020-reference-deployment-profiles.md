---
id: SPEC-020
title: Reference Deployment Profiles
version: 2.1.0
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
- ADR-013
related_contracts: []
---

# SPEC-020: Reference Deployment Profiles
| Version | 2.1.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-006, SPEC-021 | Related ADRs | ADR-001, ADR-010, ADR-012, ADR-013 | Related contracts | None |

## Purpose

Publish **informative** reference deployment profiles so implementers share a clear MVP path without reading premature distribution into the platform canon. The preferred hosted platform is **Cloudflare + Supabase** ([ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)). [ADR-012](../adr/ADR-012-render-first-platform.md) (Render-first) is superseded. Do not treat Render, Vercel, or GitHub Pages as the implementation path.

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
Cloudflare
├── Workers / Pages / static assets   (modular monolith)
│     UI + Worker / route handlers
│     domain modules (Fund Intel | Autonomous Giving | Impact Relay)
│     webhooks, authz, AI entrypoints
├── Durable Objects                   (only if live coordination is needed)
└── Queues / Cron Triggers            (deferred, webhook, retry work)
        ↓
Supabase
├── Auth                              (preferred identity)
├── PostgreSQL                        (canonical application datastore)
└── Storage                           (evidence / large artifacts)

External if still required:
├── Stripe   (payments)
├── Resend   (transactional email)
├── OpenAI   (primary AI; provider abstraction)
└── Clerk    (only if a product still requires it)
```

| Characteristic | Value |
| --- | --- |
| Executables | Next.js static/Workers surface + Worker APIs as one modular unit |
| Deployments | Single operational unit on Cloudflare |
| Database | One primary Supabase PostgreSQL |
| Object files | Supabase Storage when binaries are needed |
| ORM / migrations | Explicit reviewable SQL migrations (Drizzle acceptable) |
| Auth | Supabase Auth (identity); AGI owns authorization |
| Payments | Stripe, if still required |
| Email | Resend, if still required |
| AI | OpenAI primary, if still required |
| Durable Objects | **Not** required for baseline |
| Queues / Cron Triggers | Use when deferred, webhook, or retry work exists |
| Orchestration / broker / mesh | Not required |
| D1 / KV | Not baseline; do not migrate canonical Postgres to D1 |

Capabilities remain separate **in code**. Deployment remains **unified**.

### Preferred stack (MVP)

| Concern | Recommendation |
| --- | --- |
| Platform | Cloudflare (Workers, static assets / Pages) |
| Application | Next.js + TypeScript (static export and/or Workers) |
| Database | Supabase PostgreSQL |
| Object storage | Supabase Storage |
| Migrations | Explicit SQL migrations (Drizzle acceptable) |
| Authentication | Supabase Auth |
| Authorization | Application-owned policies |
| Payments | Stripe, if still required |
| Email | Resend, if still required |
| AI | OpenAI via `AIProvider` abstraction, if still required |
| IaC | Product-repo Wrangler/Pages + Supabase project (none in this specs repo) |
| VCS | GitHub |

Full stack detail: [SPEC-021](SPEC-021-preferred-application-stack.md). Persistence: [SPEC-022](SPEC-022-postgresql-persistence.md). Ops: [SPEC-025](SPEC-025-operations-deploy-and-scale.md).

## Profile C — Production scale-out

Same modular application, optional:

- additional Worker isolates / static-asset scale
- Cloudflare Queues (async job consumers, webhook/retry)
- Cron Triggers (reconciliation/reporting)
- Durable Objects (live coordination)
- tighter observability and backup tiers

Still one logical system; **not** a microservices mandate. Do **not** add a second application PaaS (Render, Vercel) as the scale-out path.

## Profile D — Enterprise

Optional extraction of capabilities, optional private services, optional streaming, optional multi-region, optional specialized vector DB. Adopt only with operational justification ([SPEC-002A](SPEC-002A-architectural-principles.md), [SPEC-025](SPEC-025-operations-deploy-and-scale.md) scale triggers).

## Evolution path

```text
Phase 0  Spec consolidation (this repository)
Phase 1  Platform foundation (Next.js + Workers + Supabase Auth/Postgres/Storage)
Phase 2  Financial core (Stripe + ledger + Worker/Queue webhooks + receipts)
Phase 3  Allocation system (funds, programs, disbursements)
Phase 4  Operations (reconciliation, reporting, audit surfaces)
Phase 5  AI assistance (matching, analysis, recommendations + provenance)
Phase 6  Async/scale extraction (Durable Objects / additional Queues/Cron only with evidence)
```

## Historical (superseded) — Render Profile B

The following Version 2 Profile B diagram is **historical**. Do not implement it for new work. [ADR-012](../adr/ADR-012-render-first-platform.md) is superseded by [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md). The residual Blueprint is [`docs/historical/render.yaml.example`](../docs/historical/render.yaml.example).

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

External (historical preferred):
├── Clerk   (authentication)
├── Stripe  (payments)
├── Resend  (transactional email)
└── OpenAI  (primary AI; provider abstraction)
```

Earlier v1 diagrams showed **GitHub Pages + generic single backend**. Both v1 and Render v2 diagrams are **historical**. Residual Render, Vercel, and multi-host notes are not the implementation path.

## Non-goals

This document does not force Profile D, require Kubernetes, or condition conformance on Cloudflare or Supabase. Render, Vercel, and GitHub Pages are not the recommended MVP. It replaces any implication that distributed infrastructure or a second application PaaS is the reference MVP shape.

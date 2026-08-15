---
id: SPEC-021
title: Preferred Application Stack
version: 1.2.0
status: accepted
authority: informative
owner: Platform Architecture
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-019
- SPEC-020
- SPEC-022
- SPEC-023
- SPEC-024
- SPEC-025
- SPEC-026
related_adrs:
- ADR-010
- ADR-012
- ADR-013
- ADR-015
related_contracts: []
---

# SPEC-021: Preferred Application Stack
| Version | 1.2.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-006, SPEC-020 | Related ADRs | ADR-010, ADR-012, ADR-013 | Related contracts | None |

## Purpose

Define the **preferred** AGI application stack so implementers and coding agents can deploy without inventing hosting topology, execution boundaries, or integration defaults. This specification is **informative** for conformance: alternate stacks may still conform when capabilities, contracts, and lifecycle invariants hold.

## Scope

Physical application platform, runtime shape, preferred source layout, and optional async extraction. Logical capabilities remain [SPEC-006](SPEC-006-capability-boundaries.md). Financial ownership is [SPEC-023](SPEC-023-financial-ledger-invariants.md). Integrations are [SPEC-024](SPEC-024-integration-boundaries.md). Operations are [SPEC-025](SPEC-025-operations-deploy-and-scale.md).

## Authority

**Informative preferred architecture** is [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) (Cloudflare + Supabase). [ADR-012](../adr/ADR-012-render-first-platform.md) is superseded. Do not treat Render, Vercel, or GitHub Pages as the implementation path. Do not treat any vendor as a conformance mandate.

## Architectural rule

**Do not create distributed infrastructure before workload evidence requires it.**

## Baseline topology (MVP)

```text
[ Client browser ]
        |
        v
[ Cloudflare ]
   Workers / Pages / static assets
   Next.js (TypeScript) UI
   Worker / route handlers / API
   Domain modules (capability boundaries)
   Authorization enforcement
   every.org webhook endpoints (P0 donation-source)
   Stripe billing webhooks (tenant SaaS only, if charged)
   AI orchestration entrypoints
   PostgreSQL access (explicit migrations; Drizzle acceptable)
        |
        +-- Durable Objects          (only if live coordination is needed)
        +-- Queues / Cron Triggers   (deferred, webhook, retry)
        v
[ Supabase ]
   Auth          (preferred identity)
   PostgreSQL    (canonical application datastore)
   Storage       (evidence / large artifacts)

External if still required:
  every.org | Stripe (tenant billing only) | Resend | OpenAI | Clerk

Source control: GitHub
IaC: product-repo Wrangler/Pages + Supabase project
     (this specs repository has neither)
```

| Element | Preferred choice |
| --- | --- |
| Application platform | Cloudflare Workers, static assets / Pages |
| Application | Next.js + TypeScript |
| Database | Supabase PostgreSQL |
| Object storage | Supabase Storage |
| ORM / migrations | Explicit SQL migrations (Drizzle ORM acceptable) |
| Auth (identity) | Supabase Auth |
| Payments | Stripe for tenant/SaaS billing only, if tenants are charged |
| Email | Resend, if still required |
| AI primary | OpenAI (provider abstraction required), if still required |
| Async (MVP) | In-process job contract; Queues when deferred/webhook/retry work exists |
| Scheduled (MVP) | Cron Triggers only when an operational reason is documented |
| Live coordination | Durable Objects only if needed |
| Cache / D1 / KV | None until demonstrated requirement; D1 is not the canonical store |
| IaC | Product-repo Wrangler/Pages + Supabase project |
| VCS | GitHub |

## Modular monolith boundary

The Cloudflare Worker / static surface **may** contain:

- Next.js UI (static export and/or Workers)
- Route handlers and API endpoints
- Domain services for Fund Intel, Autonomous Giving, and Impact Relay **modules**
- Authorization enforcement (application-owned)
- every.org (or adapter) webhook endpoints
- Stripe billing webhook endpoints (when tenants are charged)
- Identity webhook endpoints (Supabase Auth; Clerk only if still required)
- Resend integration (when email is used)
- AI orchestration entrypoints
- PostgreSQL access

Use **clear internal module boundaries** even though deployment is one operational unit. Do **not** force microservices.

Allocation middleware, webhooks, and PostgreSQL-backed services run as **Workers (or Worker + Queue)** talking to Supabase. They are not a Render web service.

### Preferred source layout

```text
src/
  app/                 # Next.js App Router (UI + route handlers)
  components/
  domain/
    donations/
    allocations/
    disbursements/
    organizations/
    reporting/
    evidence/          # Impact Relay concerns when co-located
    intelligence/      # Fund Intel concerns when co-located
  services/
    database/          # DB client, transactions
    auth/              # Supabase Auth session → AGI principal mapping
    payments/          # Stripe tenant-billing client + webhooks (if used)
    email/             # Resend (if used)
    ai/                # AIProvider abstraction
  jobs/                # Job handlers (same contract whether in-process or Queue)
  lib/
  types/
drizzle/               # schema + migrations (or equivalent paths documented in repo)
```

Capability modules map to glossary **Capability** / **Module** terms; package names may vary if boundaries stay enforceable. Wrangler/Pages files belong in the **product** repository, not this specs repo.

## Optional escalation services

| Service | Purpose | Introduce when |
| --- | --- | --- |
| Cloudflare Queues | Long-running or retryable work outside request latency budget | Synchronous tasks regularly exceed acceptable latency; durable retries or webhook deferral needed |
| Cron Triggers | Periodic reconciliation, reporting, cleanup | Documented operational schedule with owner and failure visibility |
| Durable Objects | Live coordination / strongly consistent session state | Live multi-actor coordination is required |
| Additional Worker isolates | Independently scaled internal component | Distinct lifecycle, security boundary, or scaling justified |

**MVP must not prescribe these without evidence**, except that Queues/Cron Triggers are the directed home for deferred, webhook, and retry work when that work exists. Document the same **job contract** ([SPEC-025](SPEC-025-operations-deploy-and-scale.md)) so later extraction is mechanical.

Do **not** escalate to Render Background Worker, Render Cron, Render Private Service, Render Key Value, or Render Workflows.

## Object storage

Evidence binaries and large artifacts SHOULD use **Supabase Storage** when following [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md). S3-compatible object storage remains allowed. Metadata and financial truth remain in PostgreSQL. Object storage is not required for a donation-ledger MVP that stores only structured records.

## Historical (superseded) — Render baseline

The following ADR-012 topology is **historical**. Do not implement it for new work. Residual Blueprint: [`docs/historical/render.yaml.example`](../docs/historical/render.yaml.example).

```text
[ Client browser ]
        |
        v
[ Render Web Service ]
   Next.js (TypeScript)
   UI / route handlers / server actions
   Domain modules / authz / every.org / Stripe billing / Clerk webhooks
        |
        v
[ Render PostgreSQL ]

IaC: render.yaml / Render Blueprints
Escalation (historical): Render Background Worker / Cron / Private Service / KV / Workflows
```

## Non-goals

- Mandating Cloudflare, Supabase, or Render for conformance
- Prescribing microservices
- Requiring D1, KV, or Kubernetes at MVP
- Adding Wrangler, Pages projects, or other deployables to this specifications repository
- Replacing logical capability ownership with vendor product names

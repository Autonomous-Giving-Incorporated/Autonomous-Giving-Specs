---
id: SPEC-021
title: Preferred Application Stack
version: 1.0.0
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
related_adrs:
- ADR-010
- ADR-012
- ADR-013
related_contracts: []
---

# SPEC-021: Preferred Application Stack
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-006, SPEC-020 | Related ADRs | ADR-010, ADR-012, ADR-013 | Related contracts | None |

## Purpose

Define the **preferred** AGI application stack so implementers and coding agents can deploy without inventing hosting topology, execution boundaries, or integration defaults. This specification is **informative** for conformance: alternate stacks may still conform when capabilities, contracts, and lifecycle invariants hold.

## Scope

Physical application platform, runtime shape, preferred source layout, and optional async extraction. Logical capabilities remain [SPEC-006](SPEC-006-capability-boundaries.md). Financial ownership is [SPEC-023](SPEC-023-financial-ledger-invariants.md). Integrations are [SPEC-024](SPEC-024-integration-boundaries.md). Operations are [SPEC-025](SPEC-025-operations-deploy-and-scale.md).

## Authority

**Informative preferred architecture** is [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) (Cloudflare + Supabase). [ADR-012](../adr/ADR-012-render-first-platform.md) is superseded. Render topology in the sections below is **historical** — do not treat it as the implementation path. Do not treat any vendor as a conformance mandate.

## Architectural rule

**Do not create distributed infrastructure before workload evidence requires it.**

## Baseline topology (MVP)

```text
[ Client browser ]
        |
        v
[ Render Web Service ]
   Next.js (TypeScript)
   UI
   Route handlers / API
   Server actions
   Domain modules (capability boundaries)
   Authorization enforcement
   Stripe / Clerk webhook endpoints
   AI orchestration entrypoints
   PostgreSQL access (Drizzle)
        |
        v
[ Render PostgreSQL ]

External (preferred):
  Clerk | Stripe | Resend | OpenAI

Source control: GitHub
IaC: render.yaml / Render Blueprints
```

| Element | Preferred choice |
| --- | --- |
| Application platform | Render |
| Application | Next.js + TypeScript |
| Database | Render PostgreSQL |
| ORM / migrations | Drizzle ORM (explicit SQL migrations) |
| Auth (identity) | Clerk |
| Payments | Stripe |
| Email | Resend |
| AI primary | OpenAI (provider abstraction required) |
| Async (MVP) | In-process job contract; extract worker only when needed |
| Scheduled (MVP) | None until operational reason documented |
| Cache / queue | None until demonstrated requirement |
| IaC | `render.yaml` Blueprint |
| VCS | GitHub |

## Modular monolith boundary

The Render web service **may** contain:

- Next.js UI
- Route handlers and API endpoints
- Server actions
- Domain services for Fund Intel, Autonomous Giving, and Impact Relay **modules**
- Authorization enforcement (application-owned)
- Stripe webhook endpoints
- Clerk webhook endpoints (when identity sync is required)
- Resend integration
- AI orchestration entrypoints
- PostgreSQL access

Use **clear internal module boundaries** even though deployment is one service. Do **not** force microservices.

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
    database/          # Drizzle client, transactions
    auth/              # Clerk session → AGI principal mapping
    payments/          # Stripe client + webhook handlers
    email/             # Resend
    ai/                # AIProvider abstraction
  jobs/                # Job handlers (same contract whether in-process or worker)
  lib/
  types/
drizzle/               # schema + migrations (or equivalent paths documented in repo)
```

Capability modules map to glossary **Capability** / **Module** terms; package names may vary if boundaries stay enforceable.

## Optional escalation services

| Service | Purpose | Introduce when |
| --- | --- | --- |
| Render Background Worker | Long-running or retryable work outside request latency budget | Synchronous tasks regularly exceed acceptable latency; durable retries needed |
| Render Cron Job | Periodic reconciliation, reporting, cleanup | Documented operational schedule with owner and failure visibility |
| Render Private Service | Internal-only independently scaled component | Distinct lifecycle, security boundary, or scaling justified |
| Render Key Value | Cache, coordination, or lightweight queue | Measurable benefit for shared cache/coordination |
| Render Workflows | Complex durable multi-step orchestration | Multi-step async orchestration exceeds simple job/retry model |

**MVP must not prescribe these without evidence.** Document the same **job contract** ([SPEC-025](SPEC-025-operations-deploy-and-scale.md)) so later extraction is mechanical.

## Object storage

Evidence binaries and large artifacts SHOULD use **Supabase Storage** when following [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md). S3-compatible object storage remains allowed. Metadata and financial truth remain in PostgreSQL. Object storage is not required for a donation-ledger MVP that stores only structured records.

## Non-goals

- Mandating Cloudflare, Supabase, or Render for conformance
- Prescribing microservices
- Requiring D1, KV, or Kubernetes at MVP
- Replacing logical capability ownership with vendor product names

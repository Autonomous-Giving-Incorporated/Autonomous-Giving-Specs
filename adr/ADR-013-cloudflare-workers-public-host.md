---
id: ADR-013
version: 1.0.0
authority: normative
owner: Platform Architecture
date: '2026-08-13'
title: Cloudflare Workers Public Host for the AGI Suite
status: accepted
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-013
- SPEC-020
- SPEC-021
- SPEC-022
- SPEC-024
---

# ADR-013: Cloudflare Workers Public Host for the AGI Suite

| Status | Accepted |
| --- | --- |
| Date | 2026-08-13 |
| Related specs | SPEC-002A, SPEC-006, SPEC-013, SPEC-020, SPEC-021, SPEC-022, SPEC-024 |

## Context

[ADR-012](ADR-012-render-first-platform.md) established a **Render-first modular monolith** with Render PostgreSQL as the preferred physical architecture for AGI product implementations. That decision remains the right default for **durable application** work: allocation middleware, webhooks, ledger writes, and a PostgreSQL-backed modular monolith.

Operator direction on 2026-08-13 is to finish migrating the **public AGI suite** to Cloudflare Workers-based infrastructure. The public surfaces in scope are:

- Autonomous Giving workbench (public)
- Portfolio Signals public
- Impact Relay public

Observed product facts that constrain this decision:

- The public AGI site is already a **static Next.js export** with no application backend in that deployable.
- Portfolio Signals retains a workspace plus an existing Supabase project (`utdioxwiskzatwoejgiu`). That store may remain an **external**; this ADR does not move Postgres into Cloudflare D1.
- This specifications repository contains **no application code** and must not gain Wrangler config, Pages projects, or other deployables ([ADR-001](ADR-001-repository-strategy.md), [ADR-004](ADR-004-repository-ownership.md)).
- Logical capabilities and physical hosts remain independent ([SPEC-002A](../specs/SPEC-002A-architectural-principles.md), [ADR-010](ADR-010-future-services.md)). Fund Intel, Autonomous Giving, and Impact Relay are capabilities—not mandatory separate deployables.

Leaving ADR-012 as the only preferred-host record would keep engineers and coding agents inferring Render (or residual Vercel notes) as the public-site host. Repealing ADR-012 would incorrectly drop the durable application path.

## Decision

1. **Cloudflare Workers with static assets, and/or Cloudflare Pages**, is the preferred hosted path for public AGI suite surfaces (workbench, Portfolio Signals public, Impact Relay public).
2. **[ADR-012](ADR-012-render-first-platform.md) is not superseded.** Render (or a similar durable application host) remains the optional preferred host for PostgreSQL-backed product services, allocation middleware, webhooks, and other server-side application runtime. This ADR specializes **public static and edge surfaces** only.
3. Specialized providers remain **externals**, not platform hosts:
   - **Clerk** — authentication and sessions
   - **Stripe** — payment processing
   - **Resend** — transactional email
   - **OpenAI** — primary AI provider (optional specialized providers behind abstractions)
   - **Supabase** — existing Portfolio Signals workspace datastore (`utdioxwiskzatwoejgiu`) and any similar product-local Postgres; not a mandate to adopt Supabase for new greenfield canonical stores ([SPEC-022](../specs/SPEC-022-postgresql-persistence.md))
4. **Do not** introduce Kubernetes, a service mesh, or an event broker as the public-suite host.
5. **Do not** migrate canonical application Postgres into Cloudflare D1 in this decision. D1, KV, R2, Durable Objects, Queues, and Workflows are escalation options only when workload evidence requires them.
6. Implementation repositories own Wrangler/Pages configuration and deploy pipelines. This specs repository stays free of application code and deployables.
7. Logical capability boundaries, lifecycle, and contracts remain deployment-independent for **conformance** ([SPEC-013](../specs/SPEC-013-repository-conformance.md)). Alternate public hosts may still conform; this ADR defines the **preferred** public-suite path.

## Rationale

- The public suite is already a static Next.js export: Cloudflare Workers static assets and Pages match that shape without inventing a backend.
- One preferred public host reduces inference cost versus residual Vercel, GitHub Pages, or Render-as-static-host notes.
- Keeping ADR-012 in force preserves transactional PostgreSQL semantics for donations, allocations, ledger, and webhooks.
- Leaving the existing Supabase project as an external avoids an unforced D1/Hyperdrive migration.
- Specs remain implementation-neutral: authorizing a host is not shipping that host here.

## Consequences

- README and onboarding must distinguish **public static/edge** (Cloudflare, this ADR) from **durable application** (Render or similar, ADR-012).
- Vercel-as-primary public host, GitHub Pages as the sole public host, and Render-as-the-only-public-host are **not** the preferred path for the suite surfaces listed above; residual mentions are historical or product-local.
- Product repos may use Workers static assets, Pages, or the Workers-compatible static export pipeline; this canon does not require a specific Wrangler file layout.
- Relational schema, migrations, and financial reconstructability stay on PostgreSQL where an application datastore is required—not on D1 by default.
- Preferred-stack documentation for the durable application path remains [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)–[SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md) and [implementation guidance](../docs/implementation-guidance.md), with this ADR as the public-host overlay.

## Alternatives considered

| Alternative | Why not preferred |
| --- | --- |
| Render-only, including public static suite | Conflicts with 2026-08-13 operator direction; public site has no backend that needs Render |
| Vercel as public host | Residual/historical; not the directed public path |
| GitHub Pages as sole public host | Weaker edge/Workers path; superseded as preferred public host by this ADR |
| Move application Postgres into D1 | No evidence that SQLite-at-the-edge fits ledger, webhooks, or the existing Supabase workspace; keep Postgres external |
| Kubernetes / multi-service mesh for the public suite | Premature distribution; the public suite is static/edge |
| Repeal ADR-012 | Would drop the durable application and PostgreSQL preference without cause |

## Status

**Accepted** (2026-08-13). Specializes public static and edge hosting. Does **not** supersede [ADR-012](ADR-012-render-first-platform.md) for durable application, allocation middleware, or PostgreSQL-backed services. Logical modular-monolith and capability-independence principles are unchanged.

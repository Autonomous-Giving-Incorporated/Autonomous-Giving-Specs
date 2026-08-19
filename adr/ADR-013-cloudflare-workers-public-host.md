---
id: ADR-013
version: 1.1.0
authority: normative
owner: Platform Architecture
date: '2026-08-13'
title: Cloudflare and Supabase Hosted Platform
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

# ADR-013: Cloudflare and Supabase Hosted Platform

| Status | Accepted |
| --- | --- |
| Date | 2026-08-13 |
| Related specs | SPEC-002A, SPEC-006, SPEC-013, SPEC-020, SPEC-021, SPEC-022, SPEC-024 |

## Context

[ADR-012](ADR-012-render-first-platform.md) established a **Render-first modular monolith** with Render PostgreSQL as the preferred physical architecture. An earlier draft of this ADR treated Cloudflare as a public-static overlay and left Render as the optional durable application host.

Operator correction on 2026-08-13: the **designed hosted stack is Cloudflare + Supabase**. Render is no longer needed. Allocation middleware, webhooks, and PostgreSQL-backed services are not a Render app.

Observed product facts:

- The public AGI suite (workbench, Portfolio Signals public, Impact Relay public) includes a **static Next.js export** for the public AGI site.
- Portfolio Signals already uses Supabase project `utdioxwiskzatwoejgiu` (PostgreSQL workspace). That project is in-path as the canonical datastore, not a leftover external to be replaced by Render Postgres.
- This specifications repository contains **no application code** and must not gain Wrangler config, Pages projects, or other deployables ([ADR-001](ADR-001-repository-strategy.md), [ADR-004](ADR-004-repository-ownership.md)).
- Logical capabilities and physical hosts remain independent ([SPEC-002A](../specs/SPEC-002A-architectural-principles.md), [ADR-010](ADR-010-future-services.md)). Fund Intel, Autonomous Giving, and Impact Relay are capabilities—not mandatory separate deployables.

Keeping Render as a second application host would contradict the designed stack and keep engineers inferring a host that is no longer required.

## Decision

1. **This ADR supersedes [ADR-012](ADR-012-render-first-platform.md) for hosted platform.** Render is not the preferred durable application host. Do not start new Render services for AGI suite work.
2. The **canonical physical stack** is:
   - **Cloudflare:** Workers; static assets and/or Pages for public suite surfaces; **Durable Objects** when live coordination is needed; **Queues** and **Cron Triggers** for deferred, webhook, and retry work.
   - **Supabase:** Auth; **PostgreSQL** as the canonical application datastore; Storage.
3. **Allocation middleware, webhooks, and PostgreSQL-backed services** run as **Workers (or Worker + Queue)** talking to Supabase. They are not a Render web service.
4. Remaining **externals** (already in the prior preferred path; do not invent new vendors):
   - **Stripe** — tenant/SaaS billing only (never donation capture). AGI does not process gifts; gift tracking is third-party connectors in Portfolio Signals ([ADR-015](ADR-015-donation-tracking-money-boundary.md))
   - **Resend** — transactional email, if the product still requires it
   - **OpenAI** — primary AI provider, if the product still requires it (optional specialized providers behind abstractions)
   - **Clerk** — only if a product still requires it; **Supabase Auth** is the preferred identity for this hosted stack
5. **Do not** introduce Kubernetes, a service mesh, or an event broker as the hosted platform.
6. **Do not** migrate canonical application Postgres into Cloudflare D1. D1 and KV remain non-baseline.
7. Implementation repositories own Wrangler/Pages configuration and the Supabase project. This specs repository stays free of application code and deployables.
8. Logical capability boundaries, lifecycle, and contracts remain deployment-independent for **conformance** ([SPEC-013](../specs/SPEC-013-repository-conformance.md)). Alternate topologies may still conform; this ADR defines the **preferred** hosted path.

## Rationale

- One compute family (Cloudflare) plus one data family (Supabase) matches the operator-designed stack and the existing Supabase workspace.
- Public static export and Worker/Queue backends share a host family without a second application PaaS.
- PostgreSQL remains the canonical datastore ([SPEC-022](../specs/SPEC-022-postgresql-persistence.md), [SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md)); Supabase Postgres preserves relational and audit semantics without D1.
- Queues and Cron Triggers cover webhook verification, retries, and deferred work without Render Background Workers.
- Specs remain implementation-neutral: authorizing a host is not shipping that host here.

## Consequences

- [ADR-012](ADR-012-render-first-platform.md) is **superseded**. Keep the file for history. Residual Render, `render.yaml`, and Render PostgreSQL mentions in SPECs, onboarding, and pilot notes are **historical** unless a product documents a still-required exception.
- README, onboarding, and implementation guidance point at Cloudflare + Supabase, not Render.
- Vercel, GitHub Pages as sole public host, and Render-as-application-host are **not** the preferred path.
- Identity defaults to Supabase Auth. Clerk is not the default for new hosted-platform work.
- Product repos may use Workers static assets, Pages, Durable Objects, Queues, and Cron Triggers as this ADR allows; this canon does not require a specific Wrangler file layout.
- Preferred-stack documentation in [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)–[SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md) that still diagrams Render is historical; follow this ADR for new work.

## Alternatives considered

| Alternative | Why not preferred |
| --- | --- |
| Keep Render for durable application / allocation middleware | Operator correction: Render is no longer needed; those workloads belong on Workers talking to Supabase |
| Vercel as public or application host | Residual/historical; not the directed path |
| GitHub Pages as sole public host | Weaker Workers path; not the directed public host |
| Move application Postgres into D1 | No evidence that SQLite-at-the-edge fits ledger or the existing Supabase workspace |
| Kubernetes / multi-service mesh | Premature distribution |
| Invent additional vendors (new auth, email, or AI providers) | Not required; keep Stripe as tenant billing only, plus Resend/OpenAI/Clerk only if a product still needs them |

## Status

**Accepted** (2026-08-13). **Supersedes [ADR-012](ADR-012-render-first-platform.md)** for hosted platform. Logical modular-monolith and capability-independence principles are unchanged.

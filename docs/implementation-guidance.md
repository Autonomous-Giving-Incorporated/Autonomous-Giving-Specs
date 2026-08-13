# Implementation guidance

Practical guidance for product teams implementing the Autonomous Giving Platform. Normative rules remain in SPECs; this document is informative unless it restates a normative requirement.

## Preferred implementation shape

**Canonical hosted stack** ([ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)): **Cloudflare + Supabase**. [ADR-012](../adr/ADR-012-render-first-platform.md) (Render-first) is **superseded**. Do not point new work at Render.

```text
GitHub → Cloudflare (Workers / Pages / static assets
           + Durable Objects if live coordination is needed
           + Queues / Cron Triggers for deferred, webhook, retry work)
       → Supabase (Auth + PostgreSQL + Storage)
Externals if still required: Stripe · Resend · OpenAI · Clerk
```

Public suite (workbench, Portfolio Signals public, Impact Relay public) and allocation middleware / webhooks / PostgreSQL-backed services share this path: **Workers (or Worker + Queue) talking to Supabase**, not a Render app.

| Layer | Preference |
| --- | --- |
| Compute / public host | Cloudflare Workers, static assets / Pages |
| Live coordination | Durable Objects, only if needed |
| Deferred / webhook / retry | Cloudflare Queues and Cron Triggers |
| Auth | Supabase Auth (Clerk only if a product still requires it) |
| Database | Supabase PostgreSQL (canonical; not D1) |
| Object files | Supabase Storage |
| Application modules | Next.js + TypeScript (static export and/or Workers) |
| ORM / migrations | Explicit SQL migrations against Supabase Postgres (Drizzle acceptable) |
| Authorization | Application-owned roles and policies |
| Payments | Stripe, if still required |
| Email | Resend, if still required |
| AI | OpenAI via provider abstraction, if still required |
| IaC | Product repos: Wrangler/Pages + Supabase project. This specs repo has neither. Residual `render.yaml.example` is historical (ADR-012). |

**Not required for MVP:** Kubernetes, event broker, service mesh, Render, D1, multiple databases, per-capability containers, separate vector DB.

## Capability modules

Implement Fund Intel, Autonomous Giving, and Impact Relay as **modules** with:

- clear package/module boundaries
- owned contracts at the edge
- no silent writes across capability private state

Co-location does not merge responsibilities.

## Contracts and events without brokers

- Call module APIs in-process for MVP.
- Persist events to PostgreSQL for audit and replay.
- Optionally enqueue background jobs for email/webhooks/AI (same job contract whether in-process or worker).
- Introduce a broker only when operational criteria justify it.

Events describe **what happened**, not **which product hosts the queue**.

## Financial core

Follow [SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md):

- append-oriented financial history
- Stripe webhook verification + idempotency
- payment ≠ ledger ≠ allocation ≠ disbursement
- AI recommendations advisory until authorized

## Persistence

Follow [SPEC-022](../specs/SPEC-022-postgresql-persistence.md):

- PostgreSQL is AGI canonical application store (Supabase Postgres per [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md))
- Supabase Auth is preferred identity; Stripe remains processor truth if payments are used
- Prefer relational columns for money fields; JSONB for payloads/metadata
- Optional pgvector before external vector DBs

## Environment and deploy

- Env catalog: [SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md), [`.env.example`](../.env.example)
- Host: [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) (Wrangler/Pages in the product repo; Supabase project). [`render.yaml.example`](../render.yaml.example) is historical.
- Onboarding: [onboarding.md](onboarding.md)
- Recovery: [recovery-runbook.md](recovery-runbook.md)

## Optional evolution

| Phase | When | What changes |
| --- | --- | --- |
| 0 Spec consolidation | Now | Canon points at Cloudflare + Supabase (ADR-013); ADR-012 superseded |
| 1 Platform foundation | Default | Next.js + Workers + Supabase Auth/Postgres/Storage |
| 2 Financial core | Product need | Stripe (if required) + ledger + Worker/Queue webhooks + receipts |
| 3 Allocation system | Product need | Funds, programs, disbursements on Workers → Supabase |
| 4 Operations | Product need | Reconciliation, reporting, audit surfaces |
| 5 AI assistance | Product need | Matching/analysis with provenance |
| 6 Async/scale extraction | Metrics justify | Durable Objects, additional Queues/Cron, extraction |

## Decision matrix: when to extract a service

Extract a capability into a separately deployable **service** only when one or more hold:

| Criterion | Example signal |
| --- | --- |
| Independent scaling | One capability saturates compute while others idle |
| Independent deployment | Different release cadence with real cost to coupling |
| Separate teams | Distinct on-call and ownership that needs hard isolation |
| Operational isolation | Different data residency or compliance plane |
| Fault isolation | Failure domain must not take down the whole MVP |

**If none apply → remain a modular monolith.**

## When NOT to extract

- “Microservices are modern”
- Premature optimization without load evidence
- To match a three-box diagram
- Before contracts and lifecycle tests are green
- Before a single-database MVP has proven the product loop

## Superseded preferred assumptions

| Old preferred implication | Current preferred path |
| --- | --- |
| GitHub Pages + separate generic backend as sole MVP diagram | Cloudflare Workers / Pages + Supabase (ADR-013) |
| Render-first modular monolith (ADR-012) | Superseded: Workers (or Worker + Queue) talking to Supabase |
| Clerk as default identity for new hosted-platform work | Supabase Auth; Clerk only if a product still requires it |
| Multi-host recipe soup (Railway/Fly/Vercel/Render) as platform default | Cloudflare + Supabase; other hosts remain historical unless re-justified |
| Convex / BaaS-as-primary-persistence | Not preferred; Supabase PostgreSQL is canonical application store |
| D1 as canonical datastore | Not preferred; keep Postgres on Supabase |
| Workers/cron mandatory as a second PaaS | Queues/Cron Triggers on Cloudflare when deferred/webhook/retry work exists |

Historical pilot plans under `docs/superpowers/` may still describe prior product choices; they do not redefine the preferred platform stack.

## Next recommended steps

After pinning a specs release that includes ADR-013:

1. Scaffold Next.js static/Workers deploy to Cloudflare and connect the Supabase project (Auth + Postgres + Storage).
2. Supabase Auth → application principal + org membership tables in Postgres.
3. Stripe test webhooks (if still required) via Worker or Worker + Queue with idempotent ledger writes ([SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md)).
4. Receipts + Resend (if still required; non-blocking for settlement).
5. Allocations / disbursements with Approval gates on Workers talking to Supabase.
6. Observability correlation + reconciliation job contract (Queue/Cron as needed).
7. AI provider abstraction with advisory-only financial outputs.
8. Add Durable Objects only when live coordination is needed.

Full ordered table and exit criteria: [roadmap — Next recommended steps](../roadmap/specification-roadmap.md#next-recommended-steps-implementation). Day-one setup: [onboarding](onboarding.md).

## Related docs

- [implementation-consumption.md](implementation-consumption.md) — pin and replace duplicates
- [SPEC-013](../specs/SPEC-013-repository-conformance.md) — conformance (topology-agnostic)
- [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)–[SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)
- [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) — Cloudflare + Supabase hosted platform
- [ADR-012](../adr/ADR-012-render-first-platform.md) — superseded (Render-first, historical)
- [Roadmap next steps](../roadmap/specification-roadmap.md#next-recommended-steps-implementation)

# Implementation guidance

Practical guidance for product teams implementing the Autonomous Giving Platform. Normative rules remain in SPECs; this document is informative unless it restates a normative requirement.

## Preferred implementation shape

**Public AGI suite** (workbench, Portfolio Signals public, Impact Relay public): Cloudflare Workers with static assets and/or Pages ([ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)). The public AGI site is a static Next.js export; Cloudflare is the preferred public host. Render is **not** the only public host.

**Durable application** (allocation middleware, webhooks, PostgreSQL-backed services): **Render-first modular monolith** ([ADR-012](../adr/ADR-012-render-first-platform.md), [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md) Profile B, [SPEC-021](../specs/SPEC-021-preferred-application-stack.md)). ADR-012 is not repealed.

```text
Public suite:  GitHub → Cloudflare Workers / Pages (static Next.js / edge)
Durable app:   GitHub → Render (Next.js web + PostgreSQL)  [optional]
Externals:     Clerk + Stripe + Resend + OpenAI + existing Supabase
```

| Layer | Preference |
| --- | --- |
| Public host | Cloudflare Workers / Pages |
| Durable application platform | Render (or similar); optional |
| Application | Next.js + TypeScript (static export for public suite; one web service when a durable app exists) |
| Database | Existing Supabase workspace as an external, or Render PostgreSQL for new canonical app stores; not D1 by default |
| ORM / migrations | Drizzle (explicit SQL migrations) |
| Authentication | Clerk |
| Authorization | Application-owned roles and policies |
| Payments | Stripe |
| Email | Resend |
| AI | OpenAI via provider abstraction |
| Worker / cron / KV / D1 | Only when workload evidence requires |
| IaC | Product repos: Wrangler/Pages for public suite; `render.yaml` / Blueprints for optional durable app. This specs repo has neither. |

**Not required for MVP:** Kubernetes, event broker, service mesh, multiple databases, per-capability containers, Background Workers, Key Value, D1, Workflows, separate vector DB.

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

- PostgreSQL is AGI canonical application store
- Clerk/Stripe remain sources of identity/processor truth
- Prefer relational columns for money fields; JSONB for payloads/metadata
- Optional pgvector before external vector DBs

## Environment and deploy

- Env catalog: [SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md), [`.env.example`](../.env.example)
- Blueprint: [`render.yaml.example`](../render.yaml.example)
- Onboarding: [onboarding.md](onboarding.md)
- Recovery: [recovery-runbook.md](recovery-runbook.md)

## Optional evolution

| Phase | When | What changes |
| --- | --- | --- |
| 0 Spec consolidation | Now | Canon points at Render-first path |
| 1 Platform foundation | Default | Next.js + Postgres + Drizzle + Clerk + Render |
| 2 Financial core | Product need | Stripe + ledger + webhooks + receipts |
| 3 Allocation system | Product need | Funds, programs, disbursements |
| 4 Operations | Product need | Reconciliation, reporting, audit surfaces |
| 5 AI assistance | Product need | Matching/analysis with provenance |
| 6 Async/scale extraction | Metrics justify | Workers, cron, KV, private services |

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
| GitHub Pages + separate generic backend as sole MVP diagram | Public suite on Cloudflare (ADR-013); durable app Next.js modular monolith on Render (ADR-012) |
| Supabase as default durable store/auth for new platform work | Render PostgreSQL + Clerk |
| Multi-host recipe soup (Railway/Fly/Vercel) as platform default | Cloudflare for public suite (ADR-013); Render for optional durable app (ADR-012); Vercel/Railway/Fly remain historical unless re-justified |
| Convex / BaaS-as-primary-persistence | Not preferred; PostgreSQL is canonical application store |
| Workers/cron mandatory for MVP | Escalation only with evidence |

Historical pilot plans under `docs/superpowers/` may still describe prior product choices; they do not redefine the preferred platform stack.

## Next recommended steps

After pinning a specs release that includes ADR-012, ADR-013, and SPEC-020–025:

1. Scaffold Next.js + Drizzle + Render Blueprint (web + Postgres only).
2. Clerk → application principal + org membership tables.
3. Stripe test webhooks with idempotent ledger writes ([SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md)).
4. Receipts + Resend (non-blocking for settlement).
5. Allocations / disbursements with Approval gates.
6. Observability correlation + reconciliation job contract.
7. AI provider abstraction with advisory-only financial outputs.
8. Extract workers/cron/KV only with metrics.

Full ordered table and exit criteria: [roadmap — Next recommended steps](../roadmap/specification-roadmap.md#next-recommended-steps-implementation). Day-one setup: [onboarding](onboarding.md).

## Related docs

- [implementation-consumption.md](implementation-consumption.md) — pin and replace duplicates
- [SPEC-013](../specs/SPEC-013-repository-conformance.md) — conformance (topology-agnostic)
- [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)–[SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)
- [ADR-012](../adr/ADR-012-render-first-platform.md) — durable application / PostgreSQL
- [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) — public suite Cloudflare host
- [Roadmap next steps](../roadmap/specification-roadmap.md#next-recommended-steps-implementation)

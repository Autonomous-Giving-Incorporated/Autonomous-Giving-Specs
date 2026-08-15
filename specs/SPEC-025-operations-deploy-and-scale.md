---
id: SPEC-025
title: Operations Deploy Observability and Scale
version: 1.1.0
status: accepted
authority: informative
owner: Platform Architecture
related_specs:
- SPEC-016
- SPEC-020
- SPEC-021
- SPEC-022
- SPEC-023
- SPEC-024
related_adrs:
- ADR-012
- ADR-013
related_contracts: []
---

# SPEC-025: Operations, Deploy, Observability, and Scale
| Version | 1.1.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-020, SPEC-021, SPEC-023 | Related ADRs | ADR-012, ADR-013 | Related contracts | None |

## Purpose

Define preferred environment variables, Cloudflare + Supabase deployment contract, environments, observability, backups/recovery, async jobs, cron, and scale triggers so deployment and operations are not inferred ad hoc.

## Authority

**Informative** preferred operations contract under [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md). [ADR-012](../adr/ADR-012-render-first-platform.md) (Render-first) is superseded. Financial idempotency remains normative via [SPEC-023](SPEC-023-financial-ledger-invariants.md).

---

## 1. Environment variables

Never commit real secrets. Maintain a product-repo `.env.example` aligned to this catalog.

### DATABASE

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `DATABASE_URL` | PostgreSQL connection string | Yes | all | Supabase Postgres / local | Rotate credentials on leak; update Worker/Supabase secrets |

### AUTH (Supabase — preferred)

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `SUPABASE_URL` | Project URL | No | all | Supabase | Rotate via project settings if leaked with keys |
| `SUPABASE_ANON_KEY` | Public/anon key | No | all | Supabase | Rotate on leak |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-only service role | Yes | server/Worker only | Supabase | Rotate immediately on leak; never expose to browser |

### AUTH (Clerk — only if a product still requires it)

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Client Clerk key | No | if Clerk used | Clerk | Rotate via Clerk dashboard |
| `CLERK_SECRET_KEY` | Server Clerk API | Yes | if Clerk used | Clerk | Rotate immediately on leak |
| `CLERK_WEBHOOK_SECRET` | Verify Clerk webhooks | Yes | staging/prod when used | Clerk | Rotate with webhook endpoint |

### STRIPE (if the product still requires Stripe)

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `STRIPE_SECRET_KEY` | Server Stripe API | Yes | all | Stripe | Separate test/live; rotate on leak |
| `STRIPE_WEBHOOK_SECRET` | Verify Stripe webhooks | Yes | all with webhooks | Stripe | Per endpoint |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Client Stripe key | No | all | Stripe | Test vs live keys |

### RESEND (if the product still requires email)

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `RESEND_API_KEY` | Send email | Yes | all that send mail | Resend | Rotate on leak |
| `EMAIL_FROM` | Default From address | No | all that send mail | Operator | Domain verification |

### OPENAI / AI (if the product still requires AI)

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `OPENAI_API_KEY` | Primary AI provider | Yes | envs with AI | OpenAI | Rotate on leak |
| `AI_PROVIDER` | Optional provider selector | No | optional | App | N/A |

### APPLICATION

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `APP_URL` | Canonical public base URL | No | all | Operator | Update on domain change |
| `NODE_ENV` | runtime mode | No | all | App | N/A |

Do not invent unused vendor env vars. Do not add Render-injected `RENDER` / Blueprint `fromDatabase` variables as the preferred path.

Canonical example file: [`.env.example`](../.env.example). Historical Render Blueprint (do not use): [`docs/historical/render.yaml.example`](../docs/historical/render.yaml.example).

---

## 2. Environments

| | LOCAL | STAGING | PRODUCTION |
| --- | --- | --- | --- |
| Database | Local Postgres or local Supabase | Isolated Supabase project/branch | Production Supabase PostgreSQL |
| Auth | Local Supabase Auth (or Clerk only if still required) | Staging Supabase Auth | Production Supabase Auth |
| Stripe | Test mode keys | Test mode keys | Live mode keys |
| Resend | Test/dev domain or log-only | Staging sender domain | Production sender domain |
| AI | Dev keys; spend limits | Staging keys; limits | Production keys; limits |
| Migrations | Dev applies freely | Apply on deploy | Controlled apply on deploy |
| Deploy trigger | Developer machine | Push to staging branch / manual | Push to main or approved promote |
| Production data | **Never required** | Anonymized or synthetic preferred | Real data |

---

## 3. Cloudflare + Supabase deploy (MVP)

MVP models **only**:

1. Cloudflare **Workers** and/or **Pages / static assets** (Next.js)
2. One **Supabase** project: Auth, PostgreSQL, Storage

Do **not** automatically add Durable Objects, extra Queues, or Cron Triggers without product evidence—except that deferred, webhook, and retry work belongs on Queues / Cron Triggers when that work exists.

Wrangler/Pages configuration lives in the **product** repository. This specs repository has **no** `wrangler.toml`, Pages project, or other deployable ([ADR-001](../adr/ADR-001-repository-strategy.md), [ADR-004](../adr/ADR-004-repository-ownership.md), [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)).

### Documented contract

| Topic | Preference |
| --- | --- |
| Repository | GitHub connected to Cloudflare (Workers / Pages) |
| Branch | `main` → production; `staging` or preview as configured |
| Build / deploy | Product-repo Wrangler/Pages pipeline (e.g. `npm ci &&` documented build) |
| Health check | HTTP path e.g. `/api/health` |
| Env / secrets | Cloudflare Worker/Pages secrets + Supabase dashboard; never commit secrets |
| Database | Supabase PostgreSQL → `DATABASE_URL` |
| Auth / storage | Same Supabase project |
| Auto deploy | On push to configured branch |
| Migrations | Explicit release step: `npm run db:migrate` (or equivalent) in build/pre-deploy—not silent ORM sync |
| Staging vs prod | Separate Cloudflare envs and Supabase projects (or documented branches) and secret sets |

Do **not** start new Render services. Do **not** copy the historical Blueprint into a new product as the preferred path.

### Historical (superseded) — Render Blueprint

ADR-012 modeled one Render web service + one Render PostgreSQL via `render.yaml`. That path is **superseded**. The leftover file is [`docs/historical/render.yaml.example`](../docs/historical/render.yaml.example) and is labeled do-not-use.

---

## 4. Async execution (job contract)

### When work leaves the synchronous request path

Candidates: large AI jobs, email batches, report generation, reconciliation, enrichment, import processing, receipt generation, expensive matching, external API retries.

### Job record requirements

| Field | Required |
| --- | --- |
| Deterministic job ID | Yes |
| Idempotency key | Yes |
| Status | Yes |
| `created_at` | Yes |
| `started_at` | When running |
| `completed_at` | When terminal |
| Retry count | Yes |
| Last error | On failure |
| Provenance | Yes (why/how created) |
| Initiating actor/system | Yes |

### Lifecycle

```text
queued → running → succeeded | failed | cancelled
```

If a Queue consumer is not yet required, implement the **same contract** in-process or via deferred tasks so extraction later is mechanical. When work is deferred, prefer **Cloudflare Queues** (Worker + Queue) talking to Supabase—not a Render Background Worker.

---

## 5. Cron / periodic jobs

Do not schedule without a documented operational reason. Each cron job specification MUST include:

- purpose
- schedule
- idempotency requirements
- retry behavior
- failure visibility
- database impact
- external APIs touched

### Likely candidates (not mandatory MVP)

| Job | Typical purpose |
| --- | --- |
| Payment reconciliation | Compare Stripe vs internal payment/ledger |
| Settlement checks | Detect stuck pending payments |
| Reporting | Aggregate operational reports |
| Stale job cleanup | Fail or requeue abandoned jobs |
| Anomaly detection | Flag unusual donation patterns |
| Scheduled donor communications | Consent-respecting campaigns |
| Data quality checks | Orphaned rows, invariant scans |

Prefer **Cloudflare Cron Triggers** when schedule is required; until then, operator-run scripts may suffice. Do not add Render Cron Jobs as the preferred path.

---

## 6. Observability

### Minimum visibility

Structured logs with:

- request IDs
- job IDs
- payment IDs
- donation IDs
- correlation IDs
- webhook event IDs
- error classification
- actor identity (where available)
- timestamps

### Do not log

- passwords
- API keys / secrets
- complete payment credentials
- unnecessary sensitive donor PII

### Failed donation/payment trace

Developers MUST be able to locate a failed flow across:

```text
request → Stripe → Worker/Queue webhook → Supabase PostgreSQL → email
```

using correlation of request id, Stripe event id, `webhook_events` row, donation/payment ids, and `notification_events` status.

---

## 7. Backups and recovery

| Topic | Preference |
| --- | --- |
| Backups | Rely on Supabase PostgreSQL automated backups; confirm plan features for the chosen tier |
| PITR | Use point-in-time recovery when available on the plan; document RPO/RTO targets operationally |
| Recovery objectives | Define product RPO/RTO (example targets: RPO ≤ 24h for MVP tier; tighten with evidence) |
| Restore procedure | Restore to new instance → verify → cut over; see [recovery runbook](../docs/recovery-runbook.md) |
| Migration recovery | Prefer forward fixes; restore from backup only for catastrophic schema/data loss |
| Accidental deletion | Compensating entries for financial; restore for bulk destruction |
| Webhook replay | Re-fetch from Stripe / replay stored `webhook_events` with idempotent handlers |
| Post-recovery reconciliation | Run payment reconciliation job; compare processor vs ledger |

---

## 8. Scaling policy

| Stage | Topology |
| --- | --- |
| **BASELINE** | Workers / Pages / static assets + Supabase Postgres |
| **ADD QUEUE WHEN** | Sync tasks regularly exceed latency budget; durable retries or webhook deferral needed |
| **ADD CRON WHEN** | Documented operational schedule with owner and failure visibility |
| **ADD DURABLE OBJECT WHEN** | Live coordination is required |
| **ADD READ REPLICA WHEN** | Read workload demonstrates DB pressure |
| **ADD SPECIALIZED VECTOR DB WHEN** | pgvector no longer meets measured workload |
| **ADD MICROSERVICE WHEN** | Ownership, scaling, security, or failure isolation provides measurable value |

**No speculative infrastructure.** Do not add Render workers, D1 as canonical store, Kubernetes, or a service mesh as the scale path.

---

## 9. Security operations (preferred path)

Aligned with [SPEC-016](SPEC-016-security-and-trust-boundaries.md):

- least privilege DB users and Cloudflare / Supabase access
- secrets only in Cloudflare secrets / Supabase dashboard (never in this repo)
- webhook verification mandatory for Stripe
- parameterized queries via ORM/SQL (no string-concat SQL)
- application authorization after Supabase Auth (or Clerk if still required)
- admin access audited
- rate limiting at edge/app for auth and webhooks as practical
- dependency scanning in CI
- production DB access restricted and logged

---

## Non-goals

- Mandating a specific APM vendor
- Requiring multi-region active-active for MVP
- Defining every product’s exact RPO/RTO numbers as platform law
- Shipping Wrangler or Pages config from this specifications repository

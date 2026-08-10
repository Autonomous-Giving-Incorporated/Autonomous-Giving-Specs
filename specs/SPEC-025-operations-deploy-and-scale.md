---
id: SPEC-025
title: Operations Deploy Observability and Scale
version: 1.0.0
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
related_contracts: []
---

# SPEC-025: Operations, Deploy, Observability, and Scale
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-020, SPEC-021, SPEC-023 | Related ADRs | ADR-012 | Related contracts | None |

## Purpose

Define preferred environment variables, Render deployment contract, environments, observability, backups/recovery, async jobs, cron, and scale triggers so deployment and operations are not inferred ad hoc.

## Authority

**Informative** preferred operations contract under [ADR-012](../adr/ADR-012-render-first-platform.md). Financial idempotency remains normative via [SPEC-023](SPEC-023-financial-ledger-invariants.md).

---

## 1. Environment variables

Never commit real secrets. Maintain a product-repo `.env.example` aligned to this catalog.

### DATABASE

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `DATABASE_URL` | PostgreSQL connection string | Yes | all | Render Postgres / local | Rotate credentials on leak; update Render env |

### AUTH (Clerk)

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Client Clerk key | No | all | Clerk | Rotate via Clerk dashboard |
| `CLERK_SECRET_KEY` | Server Clerk API | Yes | all | Clerk | Rotate immediately on leak |
| `CLERK_WEBHOOK_SECRET` | Verify Clerk webhooks | Yes | staging/prod when used | Clerk | Rotate with webhook endpoint |

### STRIPE

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `STRIPE_SECRET_KEY` | Server Stripe API | Yes | all | Stripe | Separate test/live; rotate on leak |
| `STRIPE_WEBHOOK_SECRET` | Verify Stripe webhooks | Yes | all with webhooks | Stripe | Per endpoint |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Client Stripe key | No | all | Stripe | Test vs live keys |

### RESEND

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `RESEND_API_KEY` | Send email | Yes | all that send mail | Resend | Rotate on leak |
| `EMAIL_FROM` | Default From address | No | all that send mail | Operator | Domain verification |

### OPENAI / AI

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `OPENAI_API_KEY` | Primary AI provider | Yes | envs with AI | OpenAI | Rotate on leak |
| `AI_PROVIDER` | Optional provider selector | No | optional | App | N/A |

### APPLICATION

| Name | Purpose | Secret | Envs | Owner | Rotation |
| --- | --- | --- | --- | --- | --- |
| `APP_URL` | Canonical public base URL | No | all | Operator | Update on domain change |
| `NODE_ENV` | runtime mode | No | all | App | N/A |

### RENDER-SPECIFIC

Document only variables actually required by the service. Common patterns:

| Name | Purpose | Secret |
| --- | --- | --- |
| Render-provided `RENDER` / service metadata | Platform introspection | No |
| Linked `DATABASE_URL` from Blueprint | Injected by Render when DB linked | Yes |

Do not invent unused vendor env vars.

Canonical example files: [`.env.example`](../.env.example), illustrative Blueprint: [`render.yaml.example`](../render.yaml.example).

---

## 2. Environments

| | LOCAL | STAGING | PRODUCTION |
| --- | --- | --- | --- |
| Database | Local Postgres or disposable Render DB | Isolated Render Postgres | Production Render Postgres |
| Stripe | Test mode keys | Test mode keys | Live mode keys |
| Clerk | Dev instance | Staging instance | Production instance |
| Resend | Test/dev domain or log-only | Staging sender domain | Production sender domain |
| AI | Dev keys; spend limits | Staging keys; limits | Production keys; limits |
| Migrations | Dev applies freely | Apply on deploy | Controlled apply on deploy |
| Deploy trigger | Developer machine | Push to staging branch / manual | Push to main or approved promote |
| Production data | **Never required** | Anonymized or synthetic preferred | Real data |

---

## 3. Render Blueprint (MVP)

MVP models **only**:

1. One Render **web service** (Next.js)
2. One Render **PostgreSQL** database

Do **not** automatically add worker, cron, Key Value, or private service without product evidence.

### Documented contract

| Topic | Preference |
| --- | --- |
| Repository | GitHub connected to Render |
| Branch | `main` → production; `staging` or preview as configured |
| Build command | e.g. `npm ci && npm run build` |
| Start command | e.g. `npm run start` |
| Health check | HTTP path e.g. `/api/health` |
| Env linking | Blueprint `envVars` + dashboard secrets |
| Database | Blueprint `databases` → `DATABASE_URL` fromDB |
| Auto deploy | On push to configured branch |
| Migrations | Explicit release step: `npm run db:migrate` (or equivalent) in build/pre-deploy—not silent ORM sync |
| Staging vs prod | Separate Render services/DBs and secret sets |

See [`render.yaml.example`](../render.yaml.example).

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

If a Background Worker is not yet required, implement the **same contract** in-process or via deferred tasks so extraction later is mechanical.

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

Prefer **Render Cron Jobs** when schedule is required; until then, operator-run scripts may suffice.

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
request → Stripe → webhook → PostgreSQL → email
```

using correlation of request id, Stripe event id, `webhook_events` row, donation/payment ids, and `notification_events` status.

---

## 7. Backups and recovery

| Topic | Preference |
| --- | --- |
| Backups | Rely on Render PostgreSQL automated backups; confirm plan features for the chosen tier |
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
| **BASELINE** | 1 web service + Postgres |
| **ADD WORKER WHEN** | Sync tasks regularly exceed latency budget; durable retries needed |
| **ADD KEY VALUE WHEN** | Shared cache/coordination has measurable benefit |
| **ADD PRIVATE SERVICE WHEN** | Independent lifecycle/scaling/security boundary justified |
| **ADD READ REPLICA WHEN** | Read workload demonstrates DB pressure |
| **ADD SPECIALIZED VECTOR DB WHEN** | pgvector no longer meets measured workload |
| **ADD MICROSERVICE WHEN** | Ownership, scaling, security, or failure isolation provides measurable value |

**No speculative infrastructure.**

---

## 9. Security operations (preferred path)

Aligned with [SPEC-016](SPEC-016-security-and-trust-boundaries.md):

- least privilege DB users and Render service access
- secrets only in Render env / secret store
- webhook verification mandatory for Stripe
- parameterized queries via Drizzle/SQL (no string-concat SQL)
- application authorization after Clerk authentication
- admin access audited
- rate limiting at edge/app for auth and webhooks as practical
- dependency scanning in CI
- production DB access restricted and logged

---

## Non-goals

- Mandating a specific APM vendor
- Requiring multi-region active-active for MVP
- Defining every product’s exact RPO/RTO numbers as platform law

# Sprint remaining work — donation tracking + impact loop

**Label:** Informative implementer checklist. **Not READY.** Not a live production receipt.  
**Date:** 2026-08-15  
**Canon:** [SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md) v2, [SPEC-026](../specs/SPEC-026-donation-source-connectors.md), [SPEC-027](../specs/SPEC-027-impact-loop.md), [ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md), [CONTRACT-013](../contracts/CONTRACT-013-impact-notice.md)

This page lists what product-repo files already show versus what the sprint still has to build. Sources are **OBSERVED** from [Portfolio-Signals](https://github.com/Autonomous-Giving-Incorporated/Portfolio-Signals) repository files. This session did **not** inspect a live Cloudflare dashboard or live AGI Postgres. Do not invent a workers.dev URL. Do not freeze SHAs as production proof. Do not claim every.org is pointed.

## OBSERVED — Worker and `am_*` already cover

| Area | Where (repo files) | Notes |
| --- | --- | --- |
| Worker host shape | `wrangler.toml` | Name `portfolio-signals`; `main` `workers/portfolio-signals/src/index.js`; `workers_dev = true`; assets from `.`; comment: durable state is platform Supabase `am_*` via service-role binding |
| Public vars | `wrangler.toml` `[vars]` | `ORG_ID = "org_hacker_dojo"`; `PLATFORM_SUPABASE_URL = "https://utdioxwiskzatwoejgiu.supabase.co"` |
| Router | `workers/portfolio-signals/src/index.js` | `POST /webhooks/every-org` → every-org handler; other `/webhooks/*` → 404; allocation API paths → allocation handler; else ASSETS |
| `run_worker_first` | `wrangler.toml` | `/webhooks/*`, `/auth/*`, `/available`, `/allocations`, `/proofs`, `/packet`, `/exceptions`, `/labels`, `/pots/merge`, `/setup`, `/seed`, `/trail`, `/healthz`, `/readyz`, `/import/csv` |
| Gift ingest | `every-org-webhook.js` + `connectors/everyorg.mjs` | Shared-secret token; normalize `chargeId` / `netAmount` / fundraiser / designation; persist via Supabase writer |
| CSV twin (module + Worker) | `services/allocation-middleware/src/connectors/csv.mjs`; Worker `POST /import/csv` | Parser + Worker route **CODE_SHIPPED** (not live). Live host / every.org pointing still operator-owned |
| Tracking tables | `supabase/migrations/202608030001_allocation_middleware.sql` | `am_gifts` (PK `charge_id`), `am_pots`, `am_allocations`, `am_proofs`, `am_exceptions`; RLS select for members; director insert on allocations/proofs |
| Allocate / proof / inbox / trail / packet | `allocation-api.js` | Human write roles `director`, `campaign_lead`; `OVER_ALLOCATION` → 409 |
| Static surfaces | repo root | `allocation.html`, `allocation-login.html`, `allocation-setup.html`, `donor-impact.html` / `donor-impact.js` |
| Do not intercept | `wrangler.toml` comment | Allocation HTML pages stay on ASSETS |

Capability map for the OBSERVED package: Fund Intel observes/credits; Autonomous Giving allocates; Impact Relay attaches proof rows. Intelligence does not allocate.

## SPEC-026 / SPEC-027 still need in code

| Gap | Spec | Implement |
| --- | --- | --- |
| ImpactNotice emit + send | SPEC-027, CONTRACT-013, EVENT-011 | After Evidence (or explicit human waive), issue ImpactNotice; channels `email` / `push` / `in_app`; Resend (or equivalent) for email; CONTRACT-006 delivery record including `push` |
| No invented PII | SPEC-027, SPEC-017 | Send only when the connector supplied opt-in contact; skip otherwise |
| Tenant `donation_link` | SPEC-024, SPEC-027 | Persist outbound HTTPS URL on the tenant record; tenant pages and ImpactNotice CTA use that URL; not a Checkout Session |
| CTA on tenant / post-proof surfaces | SPEC-027 | Same outbound link so donors can give again on the third-party receiver |
| Persist raw webhook payload | SPEC-023, SPEC-026 | Confirm raw payload (or `webhook_events`) is stored with the gift; required for replay |
| P1 adapters | SPEC-026 | Givebutter, Donorbox behind the same adapter — after P0 loop works |
| Tenant Stripe billing | SPEC-024, ADR-015 | Only if/when tenants pay AGI; MUST NOT credit pots or write `am_gifts` |

`donor-impact.js` is an OBSERVED dashboard that loads an Impact Relay donor API. It is **not** an ImpactNotice sender.

## Operator-owned (do not mark done here)

| Item | Why it stays operator-owned |
| --- | --- |
| Cloudflare secrets | `WEBHOOK_TOKEN`, `SUPABASE_SERVICE_ROLE_KEY` / secret key, `PLATFORM_SUPABASE_ANON_KEY`, optional `PUBLIC_BASE_URL` — not in this specs repo; live bindings were not inspected |
| Live every.org point | Nonprofit admin must paste the webhook URL; repo files are not a pointing receipt |
| Named-host OBSERVED | `wrangler.toml` comment: named-host OBSERVED remains operator-owned |
| Ed / director login | Director JWT + AAL2 for HD (`ed@hackerdojo.org` on `org_hacker_dojo` in prior notes) is an operator acceptance path |
| Resend domain / `EMAIL_FROM` | Required before email ImpactNotice |
| Push credentials | Required before `push` channel |

## Do not

- Mark any of the above READY
- Invent a `workers.dev` or named-host URL
- Treat `PLATFORM_SUPABASE_URL` as proof that this session queried that project
- Reintroduce Stripe as a donation processor
- Add a fifth capability
- Add application code to this specifications repository

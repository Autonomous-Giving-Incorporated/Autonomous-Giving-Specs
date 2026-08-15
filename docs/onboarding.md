# Engineering onboarding (Cloudflare + Supabase)

Short, executable path for a new engineer or coding agent. Product repositories implement this; this specs repo contains **no application code**.

Normative platform rules: SPECs and Constitution. **Preferred hosted stack:** [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) — Cloudflare (Workers, static assets/Pages, Durable Objects if needed, Queues/Cron Triggers) + Supabase (Auth, PostgreSQL, Storage). [ADR-012](../adr/ADR-012-render-first-platform.md) (Render) is **superseded**. Do not deploy a Render app for allocation middleware, webhooks, or PostgreSQL-backed services.

Public suite and Worker APIs deploy from the **product repository**, not from this specs repo.

## 1. Prerequisites

- Node.js LTS (match product repo engines field)
- npm/pnpm/yarn as documented in the product repo
- Docker (optional, for local Postgres) or local Supabase / PostgreSQL 15+
- GitHub access to product + specs repos
- Accounts (as needed): Cloudflare, Supabase; every.org nonprofit webhook; Stripe only if tenants pay AGI; Resend, OpenAI, and Clerk only if the product still requires them

## 2. Clone

```bash
git clone <product-repo-url>
cd <product-repo>
# Optional: pin specs release
# git clone https://github.com/Autonomous-Giving-Incorporated/Autonomous-Giving-Specs
```

## 3. Install dependencies

```bash
npm ci   # or product-documented equivalent
```

## 4. Configure environment

```bash
cp .env.example .env
# Fill secrets locally; never commit .env
```

Use the catalog in [SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md) and the specs [`.env.example`](../.env.example) as the contract. Product repos may add service-specific keys.

## 5. Provision local PostgreSQL (Supabase)

Prefer the product repo’s local Supabase path. Docker Postgres is acceptable for offline unit work; production and staging use Supabase PostgreSQL ([ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)).

```bash
# Example: Docker (offline only)
docker run --name agi-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=agi \
  -p 5432:5432 -d postgres:16
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agi
```

Production data must **never** be required for local development.

## 6. Run migrations

```bash
npm run db:migrate   # or drizzle-kit migrate / product script
```

Migrations are explicit and reviewable ([SPEC-022](../specs/SPEC-022-postgresql-persistence.md)).

## 7. Run Next.js

```bash
npm run dev
# App at APP_URL (default http://localhost:3000)
```

## 8. Run tests

```bash
npm test
# plus product lint/typecheck scripts
```

## 9. Tenant Stripe billing (only if tenants pay AGI)

- Stripe is **not** a donation processor ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md))
- Use Stripe **test** keys in local and staging when billing is in scope
- Do not create a Checkout Session for donations

## 10. Test donation-source webhooks

Webhooks belong on a **Worker (or Worker + Queue)** talking to Supabase, not on a Render service. P0 path: `POST /webhooks/every-org` ([SPEC-026](../specs/SPEC-026-donation-source-connectors.md)).

Verify:

1. Shared-secret / signature verification rejects bad tokens
2. Duplicate `chargeId` does not double-credit a pot
3. Raw payload or `webhook_events` row records processed state
4. Browser success pages are not treated as gift completion

## 11. Deploy staging

1. Connect the product GitHub repo to Cloudflare (Workers / Pages / static assets)
2. Apply Wrangler/Pages config from the **product** repo (this specs repo has none)
3. Link the Supabase project (Auth, PostgreSQL, Storage); set staging secrets
4. Add every.org webhook secret; add Stripe/Resend/OpenAI/Clerk secrets only if that product still requires them (Stripe = tenant billing only)
5. Run migrations against Supabase Postgres as part of deploy pipeline
6. Confirm health check and a dry-run gift-ingest path (seed is acceptable; live every.org pointing is operator-owned)
7. Put deferred/webhook/retry work on Queues or Cron Triggers as needed

## 12. Diagnose common failures

| Symptom | Check |
| --- | --- |
| Auth redirects fail | Supabase Auth (or Clerk if still required), `APP_URL`, allowed origins |
| DB connection errors | Supabase `DATABASE_URL`, SSL mode, Worker secrets |
| Migration fail on deploy | Migration order, locks, expand/contract |
| Gift completed on every.org but no pot credit | Webhook token, Worker endpoint, `chargeId` idempotency logs |
| Double pot credit | Unique on `chargeId`; transaction boundaries |
| Email missing but gift credited | Expected: credit ≠ email ([SPEC-024](../specs/SPEC-024-integration-boundaries.md)) |
| AI weird money action | Must be blocked without deterministic/human gate |

Trace: `third-party gift → Worker webhook → Supabase PostgreSQL → allocate → Evidence → ImpactNotice` using correlation IDs ([SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)).

## Specs validation (this repository)

```bash
pip install -r requirements-validation.txt
python validation/validate_all.py
```

## After local bring-up — next recommended steps

Once steps 1–11 work on staging:

1. Implement tracking core: every.org webhook verification, `chargeId` uniqueness, gift summary + pot credit ([SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md), [SPEC-026](../specs/SPEC-026-donation-source-connectors.md)).
2. Add Evidence + ImpactNotice (Resend/push/in_app) without coupling credit to email success ([SPEC-027](../specs/SPEC-027-impact-loop.md)).
3. Keep allocation behind Approval gates; persist tenant `donation_link`.
4. Add structured correlation IDs and a reconciliation job **contract** (in-process first).
5. Introduce AI only behind `AIProvider`, with provenance tables; keep financial actions deterministic/human-gated.
6. Use Cloudflare Queues / Cron Triggers for deferred, webhook, and retry work. Do not add a Render Worker.

Ordered exit criteria for the whole program: [roadmap — Next recommended steps](../roadmap/specification-roadmap.md#next-recommended-steps-implementation).

## Related

- [implementation-guidance.md](implementation-guidance.md)
- [recovery-runbook.md](recovery-runbook.md)
- [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) — Cloudflare + Supabase hosted platform
- [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)–[SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md) (recommended diagrams match ADR-013; residual Render text is historical)

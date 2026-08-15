# Engineering onboarding (Cloudflare + Supabase)

Short, executable path for a new engineer or coding agent. Product repositories implement this; this specs repo contains **no application code**.

Normative platform rules: SPECs and Constitution. **Preferred hosted stack:** [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) — Cloudflare (Workers, static assets/Pages, Durable Objects if needed, Queues/Cron Triggers) + Supabase (Auth, PostgreSQL, Storage). [ADR-012](../adr/ADR-012-render-first-platform.md) (Render) is **superseded**. Do not deploy a Render app for allocation middleware, webhooks, or PostgreSQL-backed services.

Public suite and Worker APIs deploy from the **product repository**, not from this specs repo.

## 1. Prerequisites

- Node.js LTS (match product repo engines field)
- npm/pnpm/yarn as documented in the product repo
- Docker (optional, for local Postgres) or local Supabase / PostgreSQL 15+
- GitHub access to product + specs repos
- Accounts (as needed): Cloudflare, Supabase; Stripe, Resend, OpenAI, and Clerk only if the product still requires them

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

## 9. Stripe test mode (if the product still requires Stripe)

- Use Stripe **test** keys in local and staging
- Create a Checkout Session / PaymentIntent via Worker / server code only as designed
- Do not treat browser redirect alone as settlement ([SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md))

## 10. Test webhooks

Webhooks belong on a **Worker (or Worker + Queue)** talking to Supabase, not on a Render service.

```bash
# Example with Stripe CLI forwarded to a local Worker/dev origin
stripe listen --forward-to localhost:3000/api/webhooks/stripe
stripe trigger payment_intent.succeeded
```

Verify:

1. Signature verification rejects bad secrets
2. Duplicate delivery does not double-book ledger
3. `webhook_events` row records processed state

## 11. Deploy staging

1. Connect the product GitHub repo to Cloudflare (Workers / Pages / static assets)
2. Apply Wrangler/Pages config from the **product** repo (this specs repo has none)
3. Link the Supabase project (Auth, PostgreSQL, Storage); set staging secrets
4. Add Stripe/Resend/OpenAI/Clerk secrets only if that product still requires them
5. Run migrations against Supabase Postgres as part of deploy pipeline
6. Confirm health check and a dry-run donation path
7. Put deferred/webhook/retry work on Queues or Cron Triggers as needed

## 12. Diagnose common failures

| Symptom | Check |
| --- | --- |
| Auth redirects fail | Supabase Auth (or Clerk if still required), `APP_URL`, allowed origins |
| DB connection errors | Supabase `DATABASE_URL`, SSL mode, Worker secrets |
| Migration fail on deploy | Migration order, locks, expand/contract |
| Payment “succeeded” in UI but no donation | Webhook secret, Worker/Queue endpoint, idempotency logs |
| Double donations | Unique on Stripe event id; transaction boundaries |
| Email missing but payment ok | Expected: settlement ≠ email ([SPEC-024](../specs/SPEC-024-integration-boundaries.md)) |
| AI weird money action | Must be blocked without deterministic/human gate |

Trace: `request → Stripe → Worker/Queue webhook → Supabase PostgreSQL → email` using correlation IDs ([SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)).

## Specs validation (this repository)

```bash
pip install -r requirements-validation.txt
python validation/validate_all.py
```

## After local bring-up — next recommended steps

Once steps 1–11 work on staging:

1. Implement financial core: Stripe webhook signature verification, `webhook_events` uniqueness, donation + ledger transaction ([SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md)).
2. Add receipt generation and Resend delivery without coupling settlement to email success.
3. Implement allocation/disbursement modules with Approval gates.
4. Add structured correlation IDs and a reconciliation job **contract** (in-process first).
5. Introduce AI only behind `AIProvider`, with provenance tables; keep financial actions deterministic/human-gated.
6. Use Cloudflare Queues / Cron Triggers for deferred, webhook, and retry work. Do not add a Render Worker.

Ordered exit criteria for the whole program: [roadmap — Next recommended steps](../roadmap/specification-roadmap.md#next-recommended-steps-implementation).

## Related

- [implementation-guidance.md](implementation-guidance.md)
- [recovery-runbook.md](recovery-runbook.md)
- [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) — Cloudflare + Supabase hosted platform
- [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)–[SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md) (recommended diagrams match ADR-013; residual Render text is historical)

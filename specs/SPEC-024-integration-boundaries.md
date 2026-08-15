---
id: SPEC-024
title: Integration Boundaries
version: 1.2.0
status: accepted
authority: informative
owner: Platform Architecture
related_specs:
- SPEC-016
- SPEC-017
- SPEC-019
- SPEC-021
- SPEC-022
- SPEC-023
- SPEC-025
- SPEC-026
- SPEC-027
related_adrs:
- ADR-006
- ADR-013
- ADR-015
related_contracts:
- CONTRACT-006
- CONTRACT-013
---

# SPEC-024: Integration Boundaries
| Version | 1.2.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-019, SPEC-021, SPEC-023, SPEC-026 | Related ADRs | ADR-006, ADR-013, ADR-015 | Related contracts | CONTRACT-006, CONTRACT-013 |

## Purpose

Define preferred external integration boundaries so identity, **donation-source tracking**, tenant billing, email/push notices, and AI responsibilities stay clear and do not collapse into a single “vendor does everything” model.

## Scope

Supabase Auth (preferred identity), every.org (P0 donation-source connector), Stripe (**tenant/SaaS billing only**), Resend (or equivalent) for email notices, optional push channel, OpenAI (and optional AI providers). Clerk only if a product still requires it. Application authorization and the tracking ledger remain AGI-owned.

## Authority

**Informative preferred integrations** under [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md) and [ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md). [ADR-012](../adr/ADR-012-render-first-platform.md) Clerk-default and Render-host notes are **historical**. Security and tracking-ledger rules that are normative are stated in [SPEC-016](SPEC-016-security-and-trust-boundaries.md), [SPEC-019](SPEC-019-identity-and-authorization.md), [SPEC-023](SPEC-023-financial-ledger-invariants.md), [SPEC-026](SPEC-026-donation-source-connectors.md), and [SPEC-027](SPEC-027-impact-loop.md).

---

## every.org — P0 donation-source connector

### every.org owns

- Donation checkout and payment processing on the tenant’s receiver
- Connector-side gift-completed (and related) events
- Optional donor PII on the webhook (may be omitted)

### AGI owns

- Verification of inbound webhooks
- Persistence of raw payload and idempotent gift summary (`chargeId`)
- Pot credit, exception inbox, and mapping
- Authorization for who may allocate or attach Evidence

### Required flow properties

- Inbound path is a Worker webhook (OBSERVED product shape: `POST /webhooks/every-org`), not an AGI-hosted checkout
- Shared-secret or signature verification before side effects
- Event persistence + idempotency ([SPEC-023](SPEC-023-financial-ledger-invariants.md), [SPEC-026](SPEC-026-donation-source-connectors.md))
- CSV import is the offline twin of the same adapter

P1 connectors (Givebutter, Donorbox) MUST use the same adapter boundary. AGI MUST NOT add a donation checkout to fill a missing connector.

Live every.org endpoint pointing is **operator-owned**. This specification does not record a pointed webhook URL and does not treat repo artifacts as a live pointing receipt.

---

## Tenant Donation Link — outbound URL

`donation_link` is an outbound HTTPS URL on the **tenant record**, pointing at the tenant’s own receiver (every.org fundraiser or equivalent).

| Rule | Guidance |
| --- | --- |
| Not checkout | MUST NOT be a Stripe Checkout Session or AGI-hosted payment page |
| Tenant pages | MAY render the link as the donate CTA |
| After Evidence | ImpactNotice CTA MUST be this same URL ([SPEC-027](SPEC-027-impact-loop.md)) |
| Missing link | Surfaces MAY omit the CTA; they MUST NOT invent a URL |

---

## Supabase Auth — authentication (preferred)

### Supabase Auth owns

- Authentication
- Sessions
- OAuth / social login
- Identity provider concerns
- MFA configuration at the IdP layer

### AGI owns

- Authorization
- Application roles
- Organization membership policy
- Tracking-ledger permissions (allocate, attach Evidence, waive)
- Operational permissions
- Administrative scope

### Synchronization model

| Item | Guidance |
| --- | --- |
| Stable link | Store `supabase_user_id` (or equivalent) on `users` |
| Profile fields | Cache display name/email as non-authoritative copies; do not PK on email |
| Memberships | AGI `organization_memberships` is application authority for product roles |
| Webhooks | Optional Auth webhooks for user/org sync; verify signatures; idempotent upserts |
| Session | Verify Supabase session on the Worker/server; map to AGI principal for authz checks |

Do **not** tightly couple domain records to mutable user-facing identity fields such as email address.

---

## Clerk — authentication (only if a product still requires it)

### Clerk owns

- Authentication
- Sessions
- OAuth / social login
- Identity provider concerns
- MFA configuration at the IdP layer

### AGI owns

- Authorization
- Application roles
- Organization membership policy
- Tracking-ledger permissions
- Operational permissions
- Administrative scope

### Synchronization model

| Item | Guidance |
| --- | --- |
| Stable link | Store `clerk_user_id` (or equivalent) on `users` |
| Profile fields | Cache display name/email as non-authoritative copies; do not PK on email |
| Memberships | AGI `organization_memberships` is application authority for product roles |
| Webhooks | Optional Clerk webhooks for user/org sync; verify signatures; idempotent upserts |
| Session | Verify Clerk session on server; map to AGI principal for authz checks |

Do **not** tightly couple domain records to mutable user-facing identity fields such as email address.

---

## Stripe — tenant / SaaS billing only

Stripe MAY exist only so **tenants can pay AGI** (subscription or invoice). Stripe is **not** a donation processor in this product and is **not** a donation-source connector.

### Stripe owns (billing only)

- Tenant subscription/invoice payment processing
- Card data for those tenant charges (never store raw card PAN in AGI)
- Processor-side billing state, disputes, and payout rails for AGI’s own charges

### AGI owns

- Tenant billing entitlement records linked to Stripe customer/subscription IDs when billing is used
- Idempotent billing-webhook application
- Authorization for who may change a tenant’s billing plan

### Required flow properties (only if tenants are charged)

- Server-side Stripe API usage for tenant billing
- Webhook signature verification (`STRIPE_WEBHOOK_SECRET`)
- Event persistence + idempotency
- Test mode in local/staging; live mode only in production with separate keys
- Billing webhooks MUST NOT insert `am_gifts`, credit pots, or create donation allocations

Client-side Stripe.js / Checkout is allowed **only** for tenant billing UX. **Donation settlement authority is never Stripe.**

### PCI scope reduction

Using Stripe for tenant billing reduces PCI scope when card data is tokenized/handled by Stripe-hosted fields or Checkout. Implementations MUST still:

- never log full card numbers or secrets
- protect secret keys
- document residual scope (their integration surface)

**Do not claim PCI compliance merely because Stripe is used.** Do not add Stripe to reduce donation PCI scope—AGI does not take donation cards.

---

## Resend — transactional email (ImpactNotice and operational mail)

### Resend owns

- Transactional email delivery API
- Provider-side delivery status (when used)

### AGI owns

- Template content and when to send
- Notification domain records (`notification_events`)
- Consent and classification rules ([SPEC-017](SPEC-017-data-classification-and-privacy.md))
- ImpactNotice trigger rules ([SPEC-027](SPEC-027-impact-loop.md))

### Requirements

| Topic | Guidance |
| --- | --- |
| Sender domains | Configure verified domain(s); `EMAIL_FROM` from env |
| Templates | Owned in application or Resend dashboard; version content for audit-sensitive notices |
| Logging | Persist send attempts, provider message ids, outcomes |
| Retries | Retry transient failures; do not block request threads for bulk |
| Non-blocking | Prefer async/job path for batches |
| Failure behavior | Surface operational alerts; **gift credit, allocation, and Evidence MUST NOT depend on successful email delivery** |
| No invented PII | MUST NOT send email unless the connector supplied opt-in donor contact; MUST NOT invent an address |

An equivalent transactional email provider MAY replace Resend if the same AGI-owned records and non-blocking rules hold.

---

## Push and in-app channels

[CONTRACT-006](../contracts/CONTRACT-006-notification.md) channels include `email`, `webhook`, `in_app`, and `push`.

- **Push** MAY deliver ImpactNotice when a device registration exists for a contactable donor.
- **in_app** MAY show the same notice on tenant or donor surfaces.
- Missing device registration or missing donor contact MUST skip that channel; implementations MUST NOT invent a push target.

---

## OpenAI — primary AI provider

### Abstraction

Implement an AI provider boundary, conceptually:

```text
AIProvider
  generate()
  embed()
  classify()
  analyze()
```

- **OpenAI** is the preferred primary provider.
- Optional specialized providers MAY be added behind the same abstraction.
- Product code depends on the abstraction, not scattered vendor SDKs in domain modules.

### Decision pipeline

For every AI-supported decision:

```text
input
  → model execution
  → structured output
  → validation
  → deterministic policy
  → action OR recommendation
```

### Hard rules

1. AI MUST NOT directly perform unvalidated irreversible financial or tracking actions.
2. Recommendations remain advisory until deterministic policy or authorized human/system actor approves ([SPEC-023](SPEC-023-financial-ledger-invariants.md)).
3. Store provenance where material: provider, model id, timestamps, prompt/input hash or reference, run id (`agent_runs` / `agent_decisions`).
4. Do not log secrets or unnecessary donor PII into model prompts or traces.

### Embeddings / RAG

Prefer PostgreSQL + optional **pgvector** ([SPEC-022](SPEC-022-postgresql-persistence.md)) before introducing a separate vector database.

---

## Cross-cutting webhook rules

| Provider | Verify | Persist | Idempotent | Tracking-ledger effect |
| --- | --- | --- | --- | --- |
| every.org (and P1 donation connectors) | Required | Required | Required | Yes — gift summary + pot credit only after verify + idempotent apply |
| Stripe | Required if tenant billing is used | Required if used | Required | **No** donation/pot effect; billing entitlement only |
| Clerk | Required if used | Recommended | Required | No (identity sync only) |
| Resend | If inbound webhooks used | Recommended | Required | No |

---

## Non-goals

- Replacing platform Notification or ImpactNotice contracts with vendor templates as the sole record
- Mandating every integration on day one of every product surface
- Standardizing enterprise SSO beyond Supabase Auth (or Clerk if still required) in this informative profile
- Using Stripe, Givebutter, or Donorbox as an AGI-hosted donation checkout

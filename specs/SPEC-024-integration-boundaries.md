---
id: SPEC-024
title: Integration Boundaries
version: 1.0.0
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
related_adrs:
- ADR-006
- ADR-012
related_contracts:
- CONTRACT-006
---

# SPEC-024: Integration Boundaries
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-019, SPEC-021, SPEC-023 | Related ADRs | ADR-006, ADR-012 | Related contracts | CONTRACT-006 |

## Purpose

Define preferred external integration boundaries so identity, payments, email, and AI responsibilities stay clear and do not collapse into a single “vendor does everything” model.

## Scope

Clerk, Stripe, Resend, OpenAI (and optional AI providers). Application authorization and financial ledger remain AGI-owned.

## Authority

**Informative preferred integrations** under [ADR-012](../adr/ADR-012-render-first-platform.md). Security and financial rules that are normative are stated in [SPEC-016](SPEC-016-security-and-trust-boundaries.md), [SPEC-019](SPEC-019-identity-and-authorization.md), and [SPEC-023](SPEC-023-financial-ledger-invariants.md).

---

## Clerk — authentication

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
- Financial permissions
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

## Stripe — payments

### Stripe owns

- Payment processing
- Card data (never store raw card PAN in AGI)
- Processor-side payment state, disputes, payout rails (as configured)

### AGI owns

- Internal donation, payment_transaction, ledger, allocation, and disbursement records
- Idempotent webhook application
- Receipts as platform artifacts
- Authorization for who may initiate charges, refunds, or payouts

### Required flow properties

- Server-side Stripe API usage for create/confirm patterns appropriate to product
- Webhook signature verification (`STRIPE_WEBHOOK_SECRET`)
- Event persistence + idempotency ([SPEC-023](SPEC-023-financial-ledger-invariants.md))
- Test mode in local/staging; live mode only in production with separate keys

Client-side Stripe.js / Checkout is allowed for UX; **settlement authority remains webhooks + server records**.

### PCI scope reduction

Using Stripe reduces PCI scope when card data is tokenized/handled by Stripe-hosted fields or Checkout. Implementations MUST still:

- never log full card numbers or secrets
- protect secret keys
- document residual scope (their integration surface)

**Do not claim PCI compliance merely because Stripe is used.**

---

## Resend — transactional email

### Resend owns

- Transactional email delivery API
- Provider-side delivery status (when used)

### AGI owns

- Template content and when to send
- Notification domain records (`notification_events`)
- Consent and classification rules ([SPEC-017](SPEC-017-data-classification-and-privacy.md))

### Requirements

| Topic | Guidance |
| --- | --- |
| Sender domains | Configure verified domain(s); `EMAIL_FROM` from env |
| Templates | Owned in application or Resend dashboard; version content for audit-sensitive notices |
| Logging | Persist send attempts, provider message ids, outcomes |
| Retries | Retry transient failures; do not block request threads for bulk |
| Non-blocking | Prefer async/job path for batches |
| Failure behavior | Surface operational alerts; **payment settlement MUST NOT depend on successful email delivery** |

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

1. AI MUST NOT directly perform unvalidated irreversible financial actions.
2. Recommendations remain advisory until deterministic policy or authorized human/system actor approves ([SPEC-023](SPEC-023-financial-ledger-invariants.md)).
3. Store provenance where material: provider, model id, timestamps, prompt/input hash or reference, run id (`agent_runs` / `agent_decisions`).
4. Do not log secrets or unnecessary donor PII into model prompts or traces.

### Embeddings / RAG

Prefer PostgreSQL + optional **pgvector** ([SPEC-022](SPEC-022-postgresql-persistence.md)) before introducing a separate vector database.

---

## Cross-cutting webhook rules

| Provider | Verify | Persist | Idempotent | Financial effect |
| --- | --- | --- | --- | --- |
| Stripe | Required | Required | Required | Yes — only after verify + idempotent apply |
| Clerk | Required if used | Recommended | Required | No (identity sync only) |
| Resend | If inbound webhooks used | Recommended | Required | No |

---

## Non-goals

- Replacing platform Notification contracts with vendor templates as the sole record
- Mandating every integration on day one of every product surface
- Standardizing enterprise SSO beyond Clerk’s capabilities in this informative profile

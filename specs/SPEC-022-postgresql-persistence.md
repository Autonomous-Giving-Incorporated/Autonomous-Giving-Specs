---
id: SPEC-022
title: PostgreSQL Persistence and Domain Ownership
version: 1.1.0
status: accepted
authority: informative
owner: Platform Architecture
related_specs:
- SPEC-004
- SPEC-017
- SPEC-018
- SPEC-020
- SPEC-021
- SPEC-023
- SPEC-024
related_adrs:
- ADR-012
- ADR-013
related_contracts: []
---

# SPEC-022: PostgreSQL Persistence and Domain Ownership
| Version | 1.1.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-004, SPEC-021, SPEC-023 | Related ADRs | ADR-012, ADR-013 | Related contracts | None |

## Purpose

Make **Supabase PostgreSQL** the preferred canonical application datastore and define relational domain ownership, design rules, and explicit-migration practice so implementers do not invent persistence boundaries. [ADR-012](../adr/ADR-012-render-first-platform.md) Render PostgreSQL is **historical**. Do not migrate canonical application data to Cloudflare D1.

## Scope

Application data ownership, preferred entity set, database design guidance, extensions (including pgvector), and ORM/migration policy. Logical domain vocabulary remains [SPEC-004](SPEC-004-domain-model.md) and the [glossary](../glossary/README.md). Financial invariants are normative in [SPEC-023](SPEC-023-financial-ledger-invariants.md).

## Authority

**Informative preferred persistence architecture** under [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md). Financial append-only and idempotency rules in SPEC-023 remain normative regardless of store technology.

## Sources of truth (split ownership)

| Concern | Source of truth | AGI PostgreSQL role |
| --- | --- | --- |
| Identity / sessions | **Supabase Auth** (Clerk only if still required) | Store application user profile, membership, and stable IdP subject references (`supabase_user_id` or `clerk_user_id`) |
| Payment processor state | **Stripe** | Store internal financial/event records linked to Stripe IDs; never treat browser callbacks as settlement |
| Application domain | **PostgreSQL** | Canonical AGI persistence for orgs, programs, donations, ledger, jobs, audit |
| AI outputs | Model providers | Store outputs with provenance; never silently promote to financial truth |

## Preferred entity ownership (relational)

Do not over-normalize prematurely. Prefer clear tables for canonical fields. Entities below are a **minimum review set** for AGI product implementations; names may map to glossary terms (e.g. Allocation ↔ `allocations`).

| Entity | Responsibility |
| --- | --- |
| `users` | Application profile linked to Supabase Auth user id (or Clerk user id if still required) |
| `organizations` | Operating or receiving organizations |
| `organization_memberships` | Membership + application roles (authorization data) |
| `donors` | Donor records (PII minimized; classification per SPEC-017) |
| `recipients` | Payees / beneficiary orgs for disbursement |
| `programs` | Bounded initiatives |
| `campaigns` | Fundraising or program campaigns |
| `donations` | Internal donation records attributable to processor events |
| `payment_transactions` | Processor-linked payment state snapshots/events |
| `funds` | Pooled or restricted fund containers |
| `allocations` | Authorized commitment records (`allocationId` semantics) |
| `disbursements` | Outbound fund movement tracking |
| `ledger_entries` | Append-oriented internal ledger |
| `receipts` | Transaction receipts (immutable after issue) |
| `webhook_events` | Inbound webhook envelopes + processing state |
| `audit_events` | Actor/system identity + timestamps for material actions |
| `notification_events` | Email/notification delivery attempts and outcomes |
| `automation_runs` | Deterministic automation executions |
| `agent_runs` | AI/agent execution records with provenance |
| `agent_decisions` | Structured AI recommendations (advisory until authorized) |
| `approvals` | Human/system authorization records |
| `reconciliation_runs` | Settlement/reconciliation job outcomes |
| `jobs` | Async job contract rows (even before a worker exists) |

Additional tables for Signals, Opportunities, Recommendations, Evidence, Verification, TimelineEvents map to capability modules as those features land.

## Database design guidance

### Identifiers

- Prefer **UUID** (`uuid` type, generated in app or DB) for primary keys unless an existing product constraint requires otherwise.
- External processor IDs (`stripe_*`) stored as text with **unique** constraints where one-to-one.
- Do not use mutable emails as primary keys or sole foreign keys.

### Timestamps

- `created_at`, `updated_at` as `timestamptz` (UTC).
- Financial/audit events: immutable `recorded_at` / `occurred_at` as appropriate.
- Prefer server-side defaults (`now()`) plus application set for cross-system consistency.

### Foreign keys and constraints

- Enforce referential integrity for domain relationships that must not dangle (donations→orgs, allocations→approvals/donations as designed).
- Unique constraints for idempotency keys, processor event IDs, and natural business keys that must not duplicate.
- Partial unique indexes where soft-deleted rows coexist.

### Indexes

- Index foreign keys used in joins and status filters.
- Index webhook `(provider, event_id)` and job `(status, created_at)`.
- Avoid speculative composite indexes without query evidence.

### Transaction boundaries

Operations that must settle atomically run in a **single PostgreSQL transaction**, including at minimum:

- webhook idempotency insert + financial state update
- donation settlement + ledger entry creation
- allocation creation after approval checks (application rules + DB constraints)

### Idempotency keys

- Store explicit `idempotency_key` or natural unique keys for webhooks, payments, and jobs.
- Duplicate processing MUST become a no-op success or controlled conflict, never double money movement ([SPEC-023](SPEC-023-financial-ledger-invariants.md)).

### Soft-delete policy

- Financial history tables: **no soft-delete as erasure**; corrections use compensating entries.
- Non-financial operational entities MAY soft-delete (`deleted_at`) when product requires recoverability.
- Legal erasure of PII follows [SPEC-017](SPEC-017-data-classification-and-privacy.md) without destroying non-PII financial integrity metadata.

### Retention

- Financial and audit records: retain for operator policy and dispute windows; default posture is long retention.
- Raw webhook payloads: retain long enough for replay and investigation; redact secrets.
- AI run payloads: retain when material to decisions; avoid indefinite storage of unnecessary PII.

### JSONB usage

Use JSONB **only** for:

- flexible metadata
- external raw payload preservation (e.g. Stripe event body)
- evolving non-canonical structures

**Do not** place core financial invariants (amounts, currencies, status machines that gate money) solely inside arbitrary JSON blobs. Prefer relational columns for canonical fields.

### Extensions

| Extension | Role | Baseline? |
| --- | --- | --- |
| `pgcrypto` / `uuid-ossp` | IDs/crypto helpers as needed | Optional |
| **pgvector** | Semantic search, matching, RAG, agent memory | **Optional** when product needs embeddings |

**pgvector** may support nonprofit/program semantic search, donor/project matching, grant/document retrieval, agent memory, RAG, and similarity. **Do not** require a separate vector database for baseline architecture. Introduce a specialized vector store only when PostgreSQL/pgvector demonstrably fails measured workload requirements.

## Drizzle ORM policy

| Concern | Preference |
| --- | --- |
| Schema location | e.g. `drizzle/schema.ts` or `src/services/database/schema/` (document in product repo) |
| Migrations location | e.g. `drizzle/migrations/` committed SQL |
| Generation | `drizzle-kit generate` from schema changes |
| Application | explicit migrate step in deploy (CI + production) |
| Local development | Docker or local Postgres; `DATABASE_URL` from `.env` |
| CI | validate migrations apply cleanly on empty DB; typecheck schema |
| Production | run migrations as controlled deploy step before/with new app release |

**Rules:**

1. ORM models are **not** the authority over the live database; **applied migrations** are.
2. Migrations MUST be explicit, reviewable, and checked into source control.
3. Prefer expand/contract patterns for breaking schema changes.
4. Rollback: prefer forward-fix migrations; document emergency restore via backups ([SPEC-025](SPEC-025-operations-deploy-and-scale.md)).

## Non-goals

- Freezing a single physical DDL as the only valid schema forever
- Requiring every listed entity on day one of every product
- Mandating Drizzle for conformance (explicit SQL migrations are preferred under ADR-013; Drizzle remains acceptable)

---
id: SPEC-023
title: Financial Ledger Invariants
version: 1.0.0
status: accepted
authority: normative
owner: Autonomous Giving
related_specs:
- SPEC-002
- SPEC-005
- SPEC-016
- SPEC-017
- SPEC-018
- SPEC-022
- SPEC-024
related_adrs:
- ADR-005
- ADR-006
- ADR-007
- ADR-012
related_contracts:
- CONTRACT-003
- CONTRACT-005
---

# SPEC-023: Financial Ledger Invariants
| Version | 1.0.0 | Owner | Autonomous Giving | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002, SPEC-005, SPEC-018 | Related ADRs | ADR-005, ADR-006, ADR-007, ADR-012 | Related contracts | CONTRACT-003, CONTRACT-005 |

## Purpose

Define **non-negotiable** financial and audit invariants for donations, payment records, allocations, disbursements, and internal ledger state. AGI handles money movement adjacent to processors; correctness is a platform requirement, not a product preference.

## Scope

Internal financial records, Stripe-linked payment handling, ledger append behavior, agent advisory limits, and reconstructability. Processor choice is preferred as Stripe ([SPEC-024](SPEC-024-integration-boundaries.md)) but invariants apply to any processor.

## Distinct state machines

Implementations SHALL treat these as **distinct** concepts that must not be collapsed into a single mutable “money status” field:

| State family | Meaning | Authoritative source |
| --- | --- | --- |
| **Payment state** | Processor-side payment/checkout/charge status | Stripe (or processor) + linked `payment_transactions` |
| **Internal ledger state** | AGI books: credits/debits/balances reconstructable from entries | PostgreSQL `ledger_entries` |
| **Allocation state** | Authorized commitment of funds under governance | `allocations` + Approval chain |
| **Disbursement state** | Outbound movement to recipients | `disbursements` + supporting receipts/evidence |

```text
payment state  ≠  internal ledger state  ≠  allocation state  ≠  disbursement state
```

## Requirements

### Append-oriented financial events

1. Financial events that record money movement or settlement SHALL be **append-oriented**. Silent in-place mutation of settled amounts is forbidden.
2. Corrections SHALL use **compensating entries** (or explicitly versioned correction records linked to the original) rather than destructive overwrite.
3. Destructive deletion of financial history is **prohibited** for convenience. Legal erasure of PII MUST preserve non-PII integrity metadata required for accountability ([SPEC-017](SPEC-017-data-classification-and-privacy.md), [SPEC-018](SPEC-018-evidence-integrity-and-provenance.md)).

### Processor linkage

4. Payment records MUST reference external processor IDs (e.g. Stripe PaymentIntent/Charge/Checkout Session IDs) when a processor was used.
5. Browser/client success callbacks are **never** authoritative for payment settlement. Settlement requires verified processor webhook (or equivalent verified server-side confirmation) plus idempotent application of internal state.

### Webhook idempotency

6. Stripe (or processor) webhooks MUST be processed **idempotently**.
7. Duplicate webhook delivery MUST NOT duplicate money movement, duplicate ledger entries that increase balances, or double-create donations.
8. Implementations MUST persist webhook event identity and processing outcome before or within the same transaction as financial effects (see [SPEC-022](SPEC-022-postgresql-persistence.md) transaction guidance).
9. Out-of-order events MUST be handled safely (ignore stale transitions; never apply a terminal “failed” over a later settled state without explicit rules).
10. Failed processing MUST leave a durable failure signal (status, error, retry eligibility) and MUST NOT partially commit inconsistent financial state.

### Amounts and attribution

11. Donation amount MUST NOT silently mutate after settlement. Amendments require compensating/correction flow with audit.
12. Allocations MUST be attributable to a donation, fund, or other documented source.
13. Disbursements MUST be traceable to authorized allocation/fund sources.
14. Ledger entries MUST preserve provenance: source entity IDs, timestamps, actor/system identity where applicable, and linkage to processor events when relevant.

### Reconstructability and audit

15. Financial state MUST be **reconstructable** from authoritative records (ledger entries + linked payment/donation/allocation/disbursement rows + webhook log).
16. Audit events for material financial actions MUST contain actor or system identity and timestamps.
17. Receipt records remain immutable after issue per [SPEC-018](SPEC-018-evidence-integrity-and-provenance.md); email delivery failure MUST NOT roll back settlement ([SPEC-024](SPEC-024-integration-boundaries.md)).

### Agents and automation

18. All agent-generated financial recommendations MUST remain **advisory** until explicitly authorized by deterministic application rules or an authorized human/system actor.
19. AI MUST NOT directly perform unvalidated irreversible financial actions (charge, allocate, disburse, refund) without a deterministic gate.
20. Agent runs and decisions that influence financial recommendations SHOULD store model/provider provenance when material ([SPEC-024](SPEC-024-integration-boundaries.md)).

### Approval gate

21. MVP allocation continues to require human Approval where [ADR-006](../adr/ADR-006-human-approval.md) applies. Payment capture alone is not Approval.

## Stripe lifecycle (normative sequence)

```text
User action
  → AGI request (authenticated, authorized)
  → Stripe operation (server-side)
  → Stripe webhook
  → signature verification
  → idempotency check
  → DB transaction (webhook_events + payment/donation/ledger updates)
  → canonical AGI financial state
  → receipt / notification (best-effort; non-blocking for settlement)
```

## Minimum webhook handling checklist

| Step | Requirement |
| --- | --- |
| Signature verification | Reject unverified payloads |
| Event persistence | Store provider event id + payload/metadata |
| Idempotency | Unique constraint or equivalent on provider event id |
| Atomic apply | Financial effects in same transaction as processed mark when possible |
| Replay safety | Re-delivery yields same business outcome |
| Duplicate handling | No-op or return success without new money movement |
| Failure | Recorded; safe retry; no half-applied ledger |

## Non-goals

- Claiming PCI compliance solely because Stripe is used (see [SPEC-016](SPEC-016-security-and-trust-boundaries.md))
- Defining full chart-of-accounts for every organization
- Replacing processor dispute/chargeback systems

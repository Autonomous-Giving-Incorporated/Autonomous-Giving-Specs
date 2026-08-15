---
id: SPEC-023
title: Financial Ledger Invariants
version: 2.0.0
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
- SPEC-026
- SPEC-027
related_adrs:
- ADR-005
- ADR-006
- ADR-007
- ADR-013
- ADR-015
related_contracts:
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-013
---

# SPEC-023: Financial Ledger Invariants
| Version | 2.0.0 | Owner | Autonomous Giving | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002, SPEC-005, SPEC-018, SPEC-026 | Related ADRs | ADR-005, ADR-006, ADR-007, ADR-013, ADR-015 | Related contracts | CONTRACT-003, CONTRACT-004, CONTRACT-005, CONTRACT-013 |

## Purpose

Define **non-negotiable** tracking-ledger invariants for gift summaries, pot credits, allocations, and Evidence. Autonomous Giving Incorporated (**AGI**) **never processes donations**. It tracks gifts completed on third-party donation platforms and reconstructs pot, allocation, and Evidence state from append-oriented records.

## Scope

Internal tracking records for inbound gift summaries, pot balances, allocations, Evidence, connector webhook/CSV ingest, agent advisory limits, and reconstructability. Donation capture, charge, checkout, payout, and refund are **out of scope**. Tenant/SaaS billing (tenants paying AGI) is not a donation flow; see [SPEC-024](SPEC-024-integration-boundaries.md) and [ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md).

## Distinct state machines

Implementations SHALL treat these as **distinct** concepts that must not be collapsed into a single mutable “money status” field:

| State family | Meaning | Authoritative source |
| --- | --- | --- |
| **Connector gift state** | Third-party platform says a gift completed (or failed) | Donation-source connector (P0: every.org) + persisted raw payload |
| **Pot credit** | AGI tracking books: available / allocated reconstructable from gift summaries and allocations | PostgreSQL pots (product: `am_pots`) + gift summaries (`am_gifts`) |
| **Allocation state** | Authorized commitment of tracked funds under governance | Allocations + Approval chain |
| **Evidence state** | Attached (or explicitly waived) proof of use | Evidence / product proof rows (`am_proofs`) |

```text
connector gift state  ≠  pot credit  ≠  allocation state  ≠  Evidence state
```

v1 language that treated Stripe payment/checkout/charge, internal `ledger_entries` settlement, and disbursement as the donation path is **withdrawn**. Stripe MUST NOT appear as a donation processor in this specification.

## Requirements

### No donation capture

1. AGI MUST NOT capture, charge, refund, or host checkout for donations.
2. Tenant pages MAY show an outbound [Donation Link](../glossary/README.md) to the tenant’s own receiver (every.org fundraiser or equivalent). AGI MUST NOT host checkout or create a processor Checkout Session as a donation.
3. Browser/client success callbacks are **never** authoritative for gift completion. Tracking requires a verified connector webhook, verified equivalent server-side confirmation, or the CSV import twin ([SPEC-026](SPEC-026-donation-source-connectors.md)).

### Append-oriented gift summaries

4. Gift summaries that record a completed gift SHALL be **append-oriented**. Silent in-place mutation of settled net amounts is forbidden.
5. Corrections SHALL use **compensating entries** (or explicitly versioned correction records linked to the original) rather than destructive overwrite.
6. Destructive deletion of tracking history is **prohibited** for convenience. Legal erasure of PII MUST preserve non-PII integrity metadata required for accountability ([SPEC-017](SPEC-017-data-classification-and-privacy.md), [SPEC-018](SPEC-018-evidence-integrity-and-provenance.md)).

### Connector linkage and idempotency

7. Gift summaries MUST reference the connector identity and the connector’s idempotency key (`chargeId` / `charge_id` for every.org; equivalent for later adapters).
8. Connector webhooks MUST be processed **idempotently**. Duplicate delivery MUST NOT double-credit a pot or duplicate a gift summary.
9. Implementations MUST persist webhook event identity (or raw payload + `chargeId`) and processing outcome before or within the same transaction as pot-credit effects (see [SPEC-022](SPEC-022-postgresql-persistence.md) transaction guidance).
10. Out-of-order connector events MUST be handled safely (ignore stale transitions; never apply a terminal “failed” over a later completed gift without explicit rules).
11. Failed processing MUST leave a durable failure signal (status, error, retry eligibility, or exception code) and MUST NOT partially commit inconsistent pot or gift state.

### Amounts and attribution

12. Credited net amount MUST NOT silently mutate after a gift summary is applied. Amendments require compensating/correction flow with audit.
13. Default credit amount is connector **`netAmount`** ([SPEC-026](SPEC-026-donation-source-connectors.md)). Gross `amount` is secondary display.
14. Allocations MUST be attributable to a pot (and therefore to documented gift summaries or manual/CSV credits).
15. Tracking records MUST preserve provenance: source entity IDs, timestamps, actor/system identity where applicable, and linkage to connector events when relevant.

### Reconstructability and audit

16. Pot balances and allocation availability MUST be **reconstructable** from authoritative records (gift summaries + allocations + Evidence/waive records + webhook/CSV log).
17. Audit events for material tracking actions MUST contain actor or system identity and timestamps.
18. Receipt records remain immutable after issue per [SPEC-018](SPEC-018-evidence-integrity-and-provenance.md). Notification or ImpactNotice delivery failure MUST NOT roll back gift credit, allocation, or Evidence ([SPEC-024](SPEC-024-integration-boundaries.md), [SPEC-027](SPEC-027-impact-loop.md)).

### Agents and automation

19. All agent-generated financial recommendations MUST remain **advisory** until explicitly authorized by deterministic application rules or an authorized human/system actor.
20. AI MUST NOT directly perform unvalidated irreversible tracking actions (credit a pot, allocate, attach Evidence, waive Evidence, or emit ImpactNotice) without a deterministic gate.
21. Agent runs and decisions that influence financial recommendations SHOULD store model/provider provenance when material ([SPEC-024](SPEC-024-integration-boundaries.md)).

### Approval gate

22. Allocation continues to require human Approval where [ADR-006](../adr/ADR-006-human-approval.md) applies. Connector gift completion alone is not Approval. Intelligence never allocates.

## Connector gift lifecycle (normative sequence)

```text
Donor gives on third-party platform
  → connector gift-completed webhook (or CSV twin)
  → signature or shared-secret verification
  → persist raw payload
  → idempotency check on chargeId
  → DB transaction (webhook/raw + gift summary + pot credit)
  → canonical AGI tracking state
  → human allocate (Approval gate)
  → attach Evidence (or explicit human waive)
  → ImpactNotice (best-effort; non-blocking for credit / allocation / Evidence)
```

Tenant/SaaS billing, if charged, is a **separate** Stripe lifecycle and MUST NOT write gift summaries, pot credits, or donation allocations. See [SPEC-024](SPEC-024-integration-boundaries.md).

## Minimum webhook handling checklist

| Step | Requirement |
| --- | --- |
| Signature or shared-secret verification | Reject unverified payloads |
| Event persistence | Store provider event id and/or raw payload |
| Idempotency | Unique constraint or equivalent on `chargeId` (gift summary PK) |
| Atomic apply | Pot-credit effects in same transaction as processed mark when possible |
| Replay safety | Re-delivery yields same business outcome |
| Duplicate handling | No-op or return success without new pot credit |
| Failure | Recorded; safe retry; no half-applied pot |

## Non-goals

- Donation processing, hosted checkout, card capture, refund, or payout rails
- Claiming PCI compliance solely because Stripe is used for optional tenant billing (see [SPEC-016](SPEC-016-security-and-trust-boundaries.md))
- Defining a full chart-of-accounts for every organization
- Replacing connector dispute or refund systems
- Treating Stripe as a donation-source connector

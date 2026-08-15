---
id: SPEC-011
title: Demo Specification
version: 2.0.0
status: accepted
authority: normative
owner: Platform Product
related_specs:
- SPEC-005
- SPEC-007
- SPEC-008
- SPEC-009
- SPEC-017
- SPEC-023
- SPEC-026
- SPEC-027
related_adrs:
- ADR-006
- ADR-009
- ADR-015
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
- CONTRACT-013
---

# SPEC-011: Demo Specification
| Version | 2.0.0 | Owner | Platform Product | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-005, SPEC-007, SPEC-009 | Related ADRs | ADR-006, ADR-009, ADR-015 | Related contracts | CONTRACT-001–007, CONTRACT-013 |

## Purpose

Specify one **deterministic** proof of the platform lifecycle so implementations can demonstrate Need → Impact without live payments, live tenants, or invented PII. The canonical fixture is **Community AI Lab**.

## Scope

The executable fixture under [`demo/community-ai-lab/`](../demo/community-ai-lab/). [Hacker Dojo](../demo/hacker-dojo-tenant/README.md) is a separate synthetic routing tenant for control-plane tests. It is **not** this specification’s conformance demo and is **not** a live tenant.

## Non-goals

No live every.org pointing, live Stripe donation, vendor integration, alternate demo brand, or workers.dev URL is required. This specification does not mark any implementation READY.

## Canonical fixture (what is actually in the repo)

Identities and amounts are taken from [`demo/community-ai-lab/scenario.json`](../demo/community-ai-lab/scenario.json). Narrative copy that disagrees with that file is wrong.

| Field | Fixed synthetic value |
| --- | --- |
| `id` | `community-ai-lab` |
| Organization / Need | Community AI Lab / 25 laptops for a neighborhood AI learning lab |
| `needId` | `need-community-ai-lab` |
| `opportunityId` | `a6c2e191-3000-4000-8000-000000000001` |
| `recommendationId` | `b6c2e191-3000-4000-8000-000000000001` |
| `approvalId` | `approval-community-ai-lab` |
| `allocationId` | `c6c2e191-3000-4000-8000-000000000001` |
| Amount / currency | **2500** / `USD` (not 25000) |
| `evidenceId` | `d6c2e191-3000-4000-8000-000000000001` |
| `receiptId` | `e6c2e191-3000-4000-8000-000000000001` |
| `verificationId` | `e0c2e191-3000-4000-8000-000000000001` |
| `notificationId` | `f6c2e191-3000-4000-8000-000000000001` |

All identifiers are synthetic. Demo fixtures SHALL use synthetic identifiers only.

### Money-boundary fields on the same scenario

`scenario.json` also records the tracking interpretation of this fixture (not a second live tenant):

| Field | Value | Meaning |
| --- | --- | --- |
| `giftTracked` | `true` | A synthetic every.org `chargeId` was tracked |
| `agiProcessedDonation` | `false` | AGI did not capture, charge, or host checkout |
| `stripeDonation` | `false` | Stripe is not the donation path |
| `contactableDonor` | `false` | No opt-in email/push/in-app donor principal |
| `impactNoticeIssued` | `false` | ImpactNotice correctly skipped |
| `donationLink` | `https://example.com/tenant-fundraiser` | Outbound CTA; documentary example, not a live pointing |

## Positive path

The executable event order is [`expected-events.jsonl`](../demo/community-ai-lab/expected-events.jsonl):

```text
SignalDetected
  → OpportunityCreated
  → RecommendationGenerated
  → ApprovalGranted          (human reviewer; ADR-006)
  → AllocationCreated        (2500 USD; allocationId continuous)
  → ExecutionStarted
  → EvidenceAttached
  → ReceiptGenerated         (amount equals allocation)
  → VerificationCompleted
  → NotificationSent         (in_app; not ImpactNotice)
```

Stages in [`expected-state-transitions.json`](../demo/community-ai-lab/expected-state-transitions.json) follow [SPEC-005](SPEC-005-lifecycle.md) plus the Notification projection.

Required demonstration meaning (fixture + scenario fields):

1. **Gift tracked, not processed.** The allocation is funded from a tracked synthetic gift (`chargeId` on the scenario). AGI did not process a donation. No Stripe donation object exists.
2. **Human allocate.** `ApprovalGranted` precedes `AllocationCreated`. Intelligence did not allocate.
3. **Evidence present.** This positive path attaches Evidence (not a waive). Receipt amount equals 2500 USD ([`expected-receipts.json`](../demo/community-ai-lab/expected-receipts.json)).
4. **ImpactNotice skipped.** `contactableDonor` is false, so EVENT-011 MUST NOT appear. `NotificationSent` `in_app` is a Timeline/Notification projection, not an invented email.
5. **Replay determinism.** Re-running the fixture yields the same IDs, order, amounts, and states.

A waive path is allowed by [SPEC-027](SPEC-027-impact-loop.md) but is **not** the Community AI Lab positive file. Implementations MAY add a separate synthetic waive fixture; they MUST NOT replace Evidence in `expected-events.jsonl` with a waive without a new scenario id.

## Negative path (existing executable vectors)

[`invalid-cases/`](../demo/community-ai-lab/invalid-cases/) are vectors implementations MUST reject. `validation/validate_demo.py` requires each file to declare `expect_error`.

| File | `expect_error` | Rule |
| --- | --- | --- |
| `allocation-before-approval.json` | `DEMO_APPROVAL_ORDER` | AllocationCreated must not precede ApprovalGranted |
| `notification-before-verification.json` | `DEMO_NOTIFICATION_ORDER` | NotificationSent must follow VerificationCompleted |
| `receipt-amount-mismatch.json` | `DEMO_RECEIPT_AMOUNT` | Receipt amount must equal scenario amount |
| `unverified-webhook.json` | `UNVERIFIED_WEBHOOK` | Unverified connector input must not credit a pot or mint a gift summary |
| `duplicate-charge-id.json` | `DUPLICATE_GIFT` | Second `chargeId` must not increase pot credited |
| `over-allocation.json` | `OVER_ALLOCATION` | Allocation must not exceed pot available |
| `missing-proof.json` | `MISSING_PROOF` | Allocation without Evidence (and without waive) is not ImpactNotice-eligible |
| `invented-pii.json` | `INVENTED_PII` | Missing donor contact must not be filled with a fabricated address |

The first three files are executed as order/amount invariants by `validate_demo.py` on the **positive** `expected-events.jsonl` / receipts. The remaining files are declared negative vectors for implementation harnesses and SPEC-026/027 rules; they MUST remain synthetic.

## Failure vectors (normative, even when only declared in `invalid-cases/`)

6. **Unverified webhook.** MUST NOT create a gift summary or pot credit ([SPEC-026](SPEC-026-donation-source-connectors.md)).
7. **Duplicate `chargeId`.** MUST NOT double-credit.
8. **Over-allocation.** MUST block commit (`OVER_ALLOCATION`).
9. **Missing proof.** MUST NOT emit ImpactNotice; `MISSING_PROOF` is not a waive.
10. **Invented PII forbidden.** If contact is omitted, MUST NOT send email or invent an address ([SPEC-017](SPEC-017-data-classification-and-privacy.md), [SPEC-027](SPEC-027-impact-loop.md)).
11. **No Stripe donation.** A fixture or implementation that uses Stripe Checkout or a Stripe charge as the Community AI Lab gift is non-conformant ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)).

## How `validate_all.py` proves the path

`python3 validation/validate_all.py` includes `validation/validate_demo.py`, which:

1. Requires `scenario.json`, `expected-events.jsonl`, `expected-state-transitions.json`, and `expected-receipts.json`.
2. Asserts `ApprovalGranted` precedes `AllocationCreated`.
3. Asserts `EvidenceAttached` precedes `VerificationCompleted`.
4. Asserts `NotificationSent` follows `VerificationCompleted`.
5. Asserts every event `allocationId` matches `scenario.json`.
6. Validates known event payloads against their schemas.
7. Asserts transition stages are a subsequence of the canonical lifecycle (+ Notification).
8. Asserts receipt `allocationId` and `amount` match the scenario (2500 USD).
9. Requires each `invalid-cases/*.json` to parse and declare `expect_error`.

That gate proves the **lifecycle fixture** and the presence of declared negative vectors. It does not prove a live webhook, a live tenant, or ImpactNotice delivery. Pin-a-release and READY remain operator-owned.

## Required narrative (information design)

The demo SHALL show Need, Fund Intel Recommendation (proposal), Human Approval, Allocation, purchase/execution, Evidence, Receipt, Verification, Impact, and Notification in order ([SPEC-009](SPEC-009-design-system.md)). Every rendered claim links backwards through the chain. Amounts on screen MUST match 2500 USD.

## Rationale

A single frozen fixture beats a live donor story. Community AI Lab already exists and validates. Hacker Dojo remains a routing fixture only. Extending the scenario with tracking flags records the money boundary without inventing a production tenant.

## References

- [demo/community-ai-lab/README.md](../demo/community-ai-lab/README.md)
- [demo/community-ai-lab.md](../demo/community-ai-lab.md)
- [ADR-009](../adr/ADR-009-deterministic-demo.md)
- [validation/validate_demo.py](../validation/validate_demo.py)

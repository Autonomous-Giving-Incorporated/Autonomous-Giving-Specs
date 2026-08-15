---
id: SPEC-027
title: Impact Loop
version: 1.0.0
status: accepted
authority: normative
owner: Impact Relay
related_specs:
- SPEC-005
- SPEC-006
- SPEC-017
- SPEC-018
- SPEC-023
- SPEC-024
- SPEC-026
related_adrs:
- ADR-006
- ADR-007
- ADR-015
related_contracts:
- CONTRACT-004
- CONTRACT-006
- CONTRACT-013
related_events:
- EVENT-007
- EVENT-010
- EVENT-011
---

# SPEC-027: Impact Loop
| Version | 1.0.0 | Owner | Impact Relay | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-005, SPEC-017, SPEC-023, SPEC-026 | Related ADRs | ADR-006, ADR-007, ADR-015 | Related contracts | CONTRACT-004, CONTRACT-006, CONTRACT-013 |

## Purpose

Close the donor loop after tracked funds are allocated and substantiated: tell a contactable donor where and what the money was used for, then invite them to give again on the tenant’s own outbound Donation Link.

## Scope

ImpactNotice trigger, payload, channels, CTA, and PII rules. Canonical lifecycle is unchanged ([SPEC-005](SPEC-005-lifecycle.md)). ImpactNotice is a **Notification projection**, not a new lifecycle stage.

## Loop

```text
donate on third party
  → connector gift summary + pot credit
  → human allocate (Approval)
  → attach Evidence  OR  explicit human waive
  → ImpactNotice (email / push / in_app)
  → CTA = tenant donation_link
```

Fund Intel observes gifts. Autonomous Giving allocates. Impact Relay proves and notifies. No fifth capability.

## Trigger

1. An ImpactNotice MUST be eligible only after **Evidence** is attached to the Allocation ([CONTRACT-004](../contracts/CONTRACT-004-evidence.md), product UI: proof) **or** an authorized human records an explicit **waive** of Evidence for that Allocation.
2. Allocation alone MUST NOT trigger ImpactNotice.
3. Connector gift completion MUST NOT trigger ImpactNotice.
4. Intelligence MUST NOT attach Evidence, waive Evidence, or emit ImpactNotice.
5. `MISSING_PROOF` ([SPEC-026](SPEC-026-donation-source-connectors.md)) is an inbox item; it is not a waive. Waive MUST be an attributable human action with actor identity and timestamp.
6. Delivery failure MUST NOT roll back Evidence, waive, allocation, or pot credit ([SPEC-023](SPEC-023-financial-ledger-invariants.md)).

## Contactable donor (no invented PII)

7. ImpactNotice MUST be emitted only when the donation-source connector (or CSV twin) supplied **opt-in contactable identity** for that gift (email and/or push registration and/or an in-app donor principal).
8. If that identity is omitted, implementations MUST NOT emit ImpactNotice, MUST NOT send email, and MUST NOT invent an address or push target ([SPEC-017](SPEC-017-data-classification-and-privacy.md)).
9. [CONTRACT-013](../contracts/CONTRACT-013-impact-notice.md) MUST NOT require donor email, name, or phone. Channel adapters resolve contact from the identity-bounded store.

## Payload

10. Producers MUST emit [CONTRACT-013](../contracts/CONTRACT-013-impact-notice.md) and publish [EVENT-011](../events/EVENT-011-impact-notice-issued.md).
11. Required meaning:

| Field | Rule |
| --- | --- |
| `impactNoticeId` | UUID; idempotency key for the notice intent |
| `allocationId` | The Allocation that was substantiated |
| `evidenceId` | Required unless `proofWaived` is `true` |
| `proofWaived` | `true` only when requirement 5 holds |
| `channel` | `email`, `push`, or `in_app` |
| `donationLink` | Tenant `donation_link` (outbound HTTPS URL) |
| `useSummary` | Where / what the money was used for (non-empty; no donor PII) |
| `createdAt` | RFC 3339 |

12. `donationLink` MUST equal the tenant Donation Link. It MUST NOT be a Stripe Checkout Session, an AGI-hosted checkout URL, or an invented fundraiser.
13. If the tenant has no `donation_link`, implementations MUST NOT emit ImpactNotice. They MUST NOT invent a URI to satisfy the schema.
14. Optional `chargeId` MAY link the notice to the gift summary. Optional `timelineEventId` MAY link [CONTRACT-007](../contracts/CONTRACT-007-timeline-event.md).

## Channels

15. Allowed ImpactNotice channels: `email`, `push`, `in_app`.
16. Email uses Resend or an equivalent provider ([SPEC-024](SPEC-024-integration-boundaries.md)).
17. Push MAY be used when a device registration exists for the contactable donor.
18. Each successful or attempted channel delivery SHOULD also record [CONTRACT-006](../contracts/CONTRACT-006-notification.md) / [EVENT-010](../events/EVENT-010-notification-sent.md). CONTRACT-006 `channel` includes `push`.
19. Delivery state is not proof that Evidence or Impact occurred.

## CTA

20. The donor call-to-action after the use summary MUST be the tenant Donation Link so they can give again on the third-party receiver.
21. Tenant pages MAY show that same outbound link before a gift exists. AGI MUST NOT host checkout.

## Observed vs remaining

`donor-impact.html` / `donor-impact.js` are **OBSERVED** staff/donor dashboard surfaces in Portfolio-Signals. They are not an ImpactNotice sender. Emitting CONTRACT-013, sending email/push, and persisting `donation_link` on the tenant record were **not** OBSERVED as implemented. Do not mark this loop READY.

## Non-goals

- Inventing donor contact
- Sending ImpactNotice from gift webhook alone
- AGI-hosted checkout
- Changing the canonical lifecycle sequence
- A fifth capability

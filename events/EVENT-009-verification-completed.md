---
id: EVENT-009
version: 1.0.0
status: accepted
authority: normative
title: VerificationCompleted
owner: Impact Relay
lifecycle_stage: Verification
producer: Impact Relay
consumers:
- Autonomous Giving
- Impact Relay
schema: ../schemas/verification-completed.json
idempotency: eventId
related_specs:
- SPEC-005
- SPEC-008
related_contracts:
- CONTRACT-012
---

# EVENT-009: VerificationCompleted

| Producer | Impact Relay |
| --- | --- |
| Consumers | Autonomous Giving, Impact Relay |
| Schema | [verification-completed.json](../schemas/verification-completed.json) in the common event envelope |
| Stage / ordering | Verification / per `allocationId` |
| Idempotency | `eventId` |

Records an evidence assessment. Payload contains `verificationId`, `allocationId`, `evidenceIds`, `outcome`, `verifiedAt`, and verifier. Public projections ([CONTRACT-012](../contracts/CONTRACT-012-public-projection.md)) MUST remain reconcilable to this Verification. Example: `{"eventType":"VerificationCompleted","payload":{"verificationId":"verification-1","outcome":"verified"}}`.


## Example payload

```json
{
  "verificationId": "e0c2e191-3000-4000-8000-000000000001",
  "allocationId": "c6c2e191-3000-4000-8000-000000000001",
  "evidenceIds": [
    "d6c2e191-3000-4000-8000-000000000001"
  ],
  "outcome": "verified",
  "verifiedAt": "2026-08-03T16:28:00Z",
  "verifier": "impact-relay-reviewer"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

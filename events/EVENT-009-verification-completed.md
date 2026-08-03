# EVENT-009: VerificationCompleted

| Producer | Verification |
| --- | --- |
| Consumers | Transparency, Impact |
| Schema | [verification-completed.json](../schemas/verification-completed.json) in the common event envelope |
| Stage / ordering | Verification / per `allocationId` |
| Idempotency | `eventId` |

Records an evidence assessment. Payload contains `verificationId`, `allocationId`, `evidenceIds`, `outcome`, `verifiedAt`, and verifier. Example: `{"eventType":"VerificationCompleted","payload":{"verificationId":"verification-1","outcome":"verified"}}`.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

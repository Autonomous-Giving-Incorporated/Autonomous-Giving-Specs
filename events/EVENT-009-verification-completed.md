# EVENT-009: VerificationCompleted

| Producer | Verification |
| --- | --- |
| Consumers | Transparency, Impact |
| Schema | [CONTRACT-004](../contracts/CONTRACT-004-evidence.md) reference |
| Stage / ordering | Verification / per `allocationId` |
| Idempotency | `eventId` |

Records an evidence assessment. Payload contains `verificationId`, `allocationId`, `evidenceIds`, `outcome`, `verifiedAt`, and verifier. Example: `{"eventType":"VerificationCompleted","payload":{"verificationId":"verification-1","outcome":"verified"}}`.

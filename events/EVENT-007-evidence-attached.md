# EVENT-007: EvidenceAttached

| Producer | Evidence |
| --- | --- |
| Consumers | Verification, Transparency |
| Schema | [CONTRACT-004](../contracts/CONTRACT-004-evidence.md) |
| Stage / ordering | Evidence / per `allocationId` |
| Idempotency | `eventId` |

Records attributable evidence without editing prior evidence. Payload validates as Evidence. Example: `{"eventType":"EvidenceAttached","payload":{"evidenceId":"d6c2e191-3000-4000-8000-000000000001","type":"delivery_photo"}}`.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

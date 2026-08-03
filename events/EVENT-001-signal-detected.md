# EVENT-001: SignalDetected

| Producer | Intelligence |
| --- | --- |
| Consumers | Opportunity, Transparency |
| Schema | Opportunity envelope |
| Stage / ordering | Signal / per `signalId` |
| Idempotency | `eventId` |

Records a captured external observation. Payload contains `signalId`, `needId`, `source`, `observedAt`, and `confidence`. Example: `{"eventType":"SignalDetected","payload":{"signalId":"signal-1","needId":"need-community-ai-lab"}}`.

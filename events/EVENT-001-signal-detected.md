# EVENT-001: SignalDetected

| Producer | Fund Intel |
| --- | --- |
| Consumers | Fund Intel, Impact Relay |
| Schema | [signal-detected.json](../schemas/signal-detected.json) in the common event envelope |
| Stage / ordering | Signal / per `signalId` |
| Idempotency | `eventId` |

Records a captured external observation. Payload contains `signalId`, `needId`, `source`, `observedAt`, and `confidence`. Example: `{"eventType":"SignalDetected","payload":{"signalId":"signal-1","needId":"need-community-ai-lab"}}`.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

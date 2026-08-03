# EVENT-006: ExecutionStarted

| Producer | Execution |
| --- | --- |
| Consumers | Evidence, Transparency |
| Schema | [execution-started.json](../schemas/execution-started.json) in the common event envelope |
| Stage / ordering | Execution / per `allocationId` |
| Idempotency | `eventId` |

Records an attempt to fulfil an allocation. Payload contains `executionId`, `allocationId`, `channel`, and `startedAt`. Example: `{"eventType":"ExecutionStarted","payload":{"executionId":"execution-1","allocationId":"c6c2e191-3000-4000-8000-000000000001"}}`.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

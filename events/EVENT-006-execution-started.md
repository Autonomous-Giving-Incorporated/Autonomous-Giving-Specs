# EVENT-006: ExecutionStarted

| Producer | Execution |
| --- | --- |
| Consumers | Evidence, Transparency |
| Schema | [CONTRACT-003](../contracts/CONTRACT-003-allocation.md) reference |
| Stage / ordering | Execution / per `allocationId` |
| Idempotency | `eventId` |

Records an attempt to fulfil an allocation. Payload contains `executionId`, `allocationId`, `channel`, and `startedAt`. Example: `{"eventType":"ExecutionStarted","payload":{"executionId":"execution-1","allocationId":"c6c2e191-3000-4000-8000-000000000001"}}`.

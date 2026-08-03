# EVENT-005: AllocationCreated

| Producer | Allocation |
| --- | --- |
| Consumers | Execution, Transparency |
| Schema | [CONTRACT-003](../contracts/CONTRACT-003-allocation.md) |
| Stage / ordering | Allocation / per `allocationId` |
| Idempotency | `eventId` |

Records an authorized allocation. Payload validates as Allocation and must contain a previously granted `approvalId`. Example: `{"eventType":"AllocationCreated","payload":{"allocationId":"c6c2e191-3000-4000-8000-000000000001","amount":2500,"currency":"USD"}}`.

# EVENT-005: AllocationCreated

| Producer | Autonomous Giving |
| --- | --- |
| Consumers | Autonomous Giving, Impact Relay |
| Schema | [CONTRACT-003](../contracts/CONTRACT-003-allocation.md) |
| Stage / ordering | Allocation / per `allocationId` |
| Idempotency | `eventId` |

Records an authorized allocation. Payload validates as Allocation and must contain a previously granted `approvalId`. Example: `{"eventType":"AllocationCreated","payload":{"allocationId":"c6c2e191-3000-4000-8000-000000000001","amount":2500,"currency":"USD"}}`.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

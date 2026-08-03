---
id: EVENT-005
version: 1.0.0
status: accepted
authority: normative
title: AllocationCreated
owner: Autonomous Giving
lifecycle_stage: Allocation
producer: Autonomous Giving
consumers:
- Autonomous Giving
- Impact Relay
schema: ../schemas/allocation.json
contract: CONTRACT-003
idempotency: eventId
related_specs:
- SPEC-005
- SPEC-008
related_contracts:
- CONTRACT-003
---

# EVENT-005: AllocationCreated

| Producer | Autonomous Giving |
| --- | --- |
| Consumers | Autonomous Giving, Impact Relay |
| Schema | [CONTRACT-003](../contracts/CONTRACT-003-allocation.md) |
| Stage / ordering | Allocation / per `allocationId` |
| Idempotency | `eventId` |

Records an authorized allocation. Payload validates as Allocation and must contain a previously granted `approvalId`. Example: `{"eventType":"AllocationCreated","payload":{"allocationId":"c6c2e191-3000-4000-8000-000000000001","amount":2500,"currency":"USD"}}`.


## Example payload

```json
{
  "allocationId": "c6c2e191-3000-4000-8000-000000000001",
  "recommendationId": "b6c2e191-3000-4000-8000-000000000001",
  "approvalId": "approval-community-ai-lab",
  "amount": 2500,
  "currency": "USD",
  "createdAt": "2026-08-03T16:10:00Z"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

---
id: EVENT-006
version: 1.0.0
status: accepted
authority: normative
title: ExecutionStarted
owner: Autonomous Giving
lifecycle_stage: Execution
producer: Autonomous Giving
consumers:
- Impact Relay
schema: ../schemas/execution-started.json
idempotency: eventId
related_specs:
- SPEC-006
- SPEC-008
related_contracts: []
---

# EVENT-006: ExecutionStarted

| Producer | Autonomous Giving |
| --- | --- |
| Consumers | Impact Relay |
| Schema | [execution-started.json](../schemas/execution-started.json) in the common event envelope |
| Stage / ordering | Execution / per `allocationId` |
| Idempotency | `eventId` |

Records an attempt to fulfil an allocation. Payload contains `executionId`, `allocationId`, `channel`, and `startedAt`. Example: `{"eventType":"ExecutionStarted","payload":{"executionId":"execution-1","allocationId":"c6c2e191-3000-4000-8000-000000000001"}}`.


## Example payload

```json
{
  "executionId": "f0c2e191-3000-4000-8000-000000000001",
  "allocationId": "c6c2e191-3000-4000-8000-000000000001",
  "channel": "vendor-purchase",
  "startedAt": "2026-08-03T16:15:00Z"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

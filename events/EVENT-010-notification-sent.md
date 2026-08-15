---
id: EVENT-010
version: 1.1.0
status: accepted
authority: normative
title: NotificationSent
owner: Impact Relay
lifecycle_stage: Notification
producer: Impact Relay
consumers:
- Channel adapter
- Autonomous Giving
schema: ../schemas/notification.json
contract: CONTRACT-006
idempotency: eventId
related_specs:
- SPEC-006
- SPEC-008
related_contracts:
- CONTRACT-006
---

# EVENT-010: NotificationSent

| Producer | Impact Relay |
| --- | --- |
| Consumers | Channel adapter, Autonomous Giving |
| Schema | [CONTRACT-006](../contracts/CONTRACT-006-notification.md) |
| Stage / ordering | Notification / per `notificationId` |
| Idempotency | `eventId` |

Records attempted delivery of a timeline update. Payload validates as Notification; delivery does not alter history. Example: `{"eventType":"NotificationSent","payload":{"notificationId":"f6c2e191-3000-4000-8000-000000000001","channel":"in_app"}}`.


## Example payload

```json
{
  "notificationId": "f6c2e191-3000-4000-8000-000000000001",
  "timelineEventId": "a6c2e191-3000-4000-8000-000000000002",
  "channel": "in_app",
  "createdAt": "2026-08-03T16:30:00Z"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.1.0 | Channel enum widened to include `push` (CONTRACT-006 / notification schema 1.1.0). |
| 1.0.0 | Initial canonical event definition. |

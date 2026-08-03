# EVENT-010: NotificationSent

| Producer | Impact Relay |
| --- | --- |
| Consumers | Channel adapter, Autonomous Giving |
| Schema | [CONTRACT-006](../contracts/CONTRACT-006-notification.md) |
| Stage / ordering | Notification / per `notificationId` |
| Idempotency | `eventId` |

Records attempted delivery of a timeline update. Payload validates as Notification; delivery does not alter history. Example: `{"eventType":"NotificationSent","payload":{"notificationId":"f6c2e191-3000-4000-8000-000000000001","channel":"in_app"}}`.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

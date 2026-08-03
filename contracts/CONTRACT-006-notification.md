# CONTRACT-006: Notification

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Impact Relay |
| Producer / consumer | Impact Relay / Channel adapter |
| Schema | [notification.json](../schemas/notification.json) |

A delivery request describing a lifecycle update. Required: `notificationId`, `timelineEventId`, `channel`, `createdAt`. Delivery state is not proof that the underlying lifecycle event occurred. Published by [EVENT-010](../events/EVENT-010-notification-sent.md).

Validation requires UUID identifiers, an allowed channel (`email`, `webhook`, or `in_app`), and an RFC 3339 creation time.

```json
{"notificationId":"f6c2e191-3000-4000-8000-000000000001","timelineEventId":"a6c2e191-3000-4000-8000-000000000002","channel":"in_app","createdAt":"2026-08-03T16:30:00Z"}
```

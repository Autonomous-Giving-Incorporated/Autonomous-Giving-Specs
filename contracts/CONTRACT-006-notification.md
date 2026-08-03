# CONTRACT-006: Notification

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Transparency |
| Producer / consumer | Transparency / Channel adapter |
| Schema | [notification.json](../schemas/notification.json) |

A delivery request describing a lifecycle update. Required: `notificationId`, `timelineEventId`, `channel`, `createdAt`. Delivery state is not proof that the underlying lifecycle event occurred. Published by [EVENT-010](../events/EVENT-010-notification-sent.md).

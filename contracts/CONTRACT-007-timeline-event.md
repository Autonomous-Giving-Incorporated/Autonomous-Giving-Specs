# CONTRACT-007: TimelineEvent

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Impact Relay |
| Producer / consumer | Ecosystem boundary / Impact Relay |
| Schema | [timeline-event.json](../schemas/timeline-event.json) |

An immutable, human-readable projection of a lifecycle event. Required: `timelineEventId`, `eventType`, `occurredAt`, `subjectId`. It links to source records and never replaces the authoritative event.

Validation requires a UUID event identifier, a non-empty event type and subject, and an RFC 3339 occurrence time.

```json
{"timelineEventId":"a6c2e191-3000-4000-8000-000000000002","eventType":"AllocationCreated","occurredAt":"2026-08-03T16:10:00Z","subjectId":"c6c2e191-3000-4000-8000-000000000001"}
```

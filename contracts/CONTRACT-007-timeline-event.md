# CONTRACT-007: TimelineEvent

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Transparency |
| Producer / consumer | Any boundary / Transparency |
| Schema | [timeline-event.json](../schemas/timeline-event.json) |

An immutable, human-readable projection of a lifecycle event. Required: `timelineEventId`, `eventType`, `occurredAt`, `subjectId`. It links to source records and never replaces the authoritative event.

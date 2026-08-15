---
id: EVENT-011
version: 1.0.0
status: accepted
authority: normative
title: ImpactNoticeIssued
owner: Impact Relay
lifecycle_stage: Notification
producer: Impact Relay
consumers:
- Channel adapter
- Autonomous Giving
schema: ../schemas/impact-notice.json
contract: CONTRACT-013
idempotency: eventId
related_specs:
- SPEC-006
- SPEC-008
- SPEC-027
related_contracts:
- CONTRACT-013
---

# EVENT-011: ImpactNoticeIssued

| Producer | Impact Relay |
| --- | --- |
| Consumers | Channel adapter, Autonomous Giving |
| Schema | [CONTRACT-013](../contracts/CONTRACT-013-impact-notice.md) |
| Stage / ordering | Notification / per `impactNoticeId` |
| Idempotency | `eventId` |

Records that an ImpactNotice was issued after Evidence (or an explicit human waive). Payload validates as ImpactNotice. Delivery attempts MAY also emit [EVENT-010](EVENT-010-notification-sent.md). Example: `{"eventType":"ImpactNoticeIssued","payload":{"impactNoticeId":"16c2e191-3000-4000-8000-000000000001","channel":"email"}}`.

## Example payload

```json
{
  "impactNoticeId": "16c2e191-3000-4000-8000-000000000001",
  "allocationId": "c6c2e191-3000-4000-8000-000000000001",
  "evidenceId": "d6c2e191-3000-4000-8000-000000000001",
  "proofWaived": false,
  "channel": "email",
  "donationLink": "https://example.com/tenant-fundraiser",
  "useSummary": "Kitchen renovation materials for the community lab.",
  "createdAt": "2026-08-15T18:00:00Z"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

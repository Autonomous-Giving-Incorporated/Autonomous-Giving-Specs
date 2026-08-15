---
id: CONTRACT-013
version: 1.0.0
status: accepted
authority: normative
title: ImpactNotice
owner: Impact Relay
lifecycle_stage: Notification
schema: ../schemas/impact-notice.json
producer: Impact Relay
consumer: Channel adapter
related_specs:
- SPEC-006
- SPEC-007
- SPEC-017
- SPEC-027
related_events:
- EVENT-011
---

# CONTRACT-013: ImpactNotice

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Impact Relay |
| Producer / consumer | Impact Relay / Channel adapter |
| Schema | [impact-notice.json](../schemas/impact-notice.json) |

A donor-facing notice that an Allocation was substantiated and what the money was used for. Required: `impactNoticeId`, `allocationId`, `channel`, `donationLink`, `useSummary`, `createdAt`. `evidenceId` is required unless `proofWaived` is `true`. Published by [EVENT-011](../events/EVENT-011-impact-notice-issued.md).

This contract MUST NOT include donor email, name, or phone. Channel adapters resolve opt-in contact outside the payload. `donationLink` is the tenant outbound Donation Link, not a checkout session. Delivery is recorded separately as [CONTRACT-006](CONTRACT-006-notification.md).

Validation requires UUID identifiers, an allowed channel (`email`, `push`, or `in_app`), an HTTPS Donation Link, a non-empty use summary, and an RFC 3339 creation time.

```json
{"impactNoticeId":"16c2e191-3000-4000-8000-000000000001","allocationId":"c6c2e191-3000-4000-8000-000000000001","evidenceId":"d6c2e191-3000-4000-8000-000000000001","proofWaived":false,"channel":"email","donationLink":"https://example.com/tenant-fundraiser","useSummary":"Kitchen renovation materials for the community lab.","createdAt":"2026-08-15T18:00:00Z"}
```

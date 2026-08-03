---
id: CONTRACT-001
version: 1.0.0
status: accepted
authority: normative
title: Opportunity
owner: Fund Intel
lifecycle_stage: Opportunity
schema: ../schemas/opportunity.json
producer: Fund Intel
consumer: Autonomous Giving
related_specs:
- SPEC-003
- SPEC-007
related_events:
- EVENT-002
---

# CONTRACT-001: Opportunity

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Fund Intel |
| Producer / consumer | Intelligence / Governance |
| Schema | [opportunity.json](../schemas/opportunity.json) |

An actionable grouping of a Need and supporting Signals. Required: `opportunityId`, `needId`, `title`, `status`, `createdAt`. Validation requires a UUID opportunity identifier, non-empty need and title, an allowed status (`open`, `dismissed`, or `converted`), and an RFC 3339 creation time. Published by [EVENT-002](../events/EVENT-002-opportunity-created.md).

```json
{"opportunityId":"a6c2e191-3000-4000-8000-000000000001","needId":"need-community-ai-lab","title":"Laptop access","status":"open","createdAt":"2026-08-03T16:00:00Z"}
```

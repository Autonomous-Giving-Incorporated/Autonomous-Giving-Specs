# CONTRACT-001: Opportunity

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Fund Intel |
| Producer / consumer | Intelligence / Governance |
| Schema | [opportunity.json](../schemas/opportunity.json) |

An actionable grouping of a Need and supporting Signals. Required: `opportunityId`, `needId`, `title`, `status`, `createdAt`. IDs are UUIDs; status is `open`, `dismissed`, or `converted`. Published by [EVENT-002](../events/EVENT-002-opportunity-created.md).

```json
{"opportunityId":"a6c2e191-3000-4000-8000-000000000001","needId":"need-community-ai-lab","title":"Laptop access","status":"open","createdAt":"2026-08-03T16:00:00Z"}
```

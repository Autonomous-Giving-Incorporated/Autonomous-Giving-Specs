# CONTRACT-002: Recommendation

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Fund Intel |
| Producer / consumer | Intelligence / Governance |
| Schema | [recommendation.json](../schemas/recommendation.json) |

A proposal to allocate against an Opportunity; it is not authorization. Required: `recommendationId`, `opportunityId`, `proposedAmount`, `currency`, `rationale`, `createdAt`. Amount is a non-negative decimal; currency is ISO 4217. Published by [EVENT-003](../events/EVENT-003-recommendation-generated.md).

```json
{"recommendationId":"b6c2e191-3000-4000-8000-000000000001","opportunityId":"a6c2e191-3000-4000-8000-000000000001","proposedAmount":2500,"currency":"USD","rationale":"Equip the lab","createdAt":"2026-08-03T16:05:00Z"}
```

# CONTRACT-003: Allocation

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Allocation |
| Producer / consumer | Allocation / Execution, Transparency |
| Schema | [allocation.json](../schemas/allocation.json) |

An authorized commitment to deploy funds. Required: `allocationId`, `recommendationId`, `approvalId`, `amount`, `currency`, `createdAt`. `approvalId` is mandatory; `allocationId` is immutable. Published by [EVENT-005](../events/EVENT-005-allocation-created.md).

```json
{"allocationId":"c6c2e191-3000-4000-8000-000000000001","recommendationId":"b6c2e191-3000-4000-8000-000000000001","approvalId":"approval-community-ai-lab","amount":2500,"currency":"USD","createdAt":"2026-08-03T16:10:00Z"}
```

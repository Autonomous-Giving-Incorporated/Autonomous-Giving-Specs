---
id: EVENT-003
version: 1.0.0
status: accepted
authority: normative
title: RecommendationGenerated
owner: Fund Intel
lifecycle_stage: Recommendation
producer: Fund Intel
consumers:
- Autonomous Giving
- Impact Relay
schema: ../schemas/recommendation.json
contract: CONTRACT-002
idempotency: eventId
related_specs:
- SPEC-003
- SPEC-008
related_contracts:
- CONTRACT-002
---

# EVENT-003: RecommendationGenerated

| Producer | Fund Intel |
| --- | --- |
| Consumers | Autonomous Giving, Impact Relay |
| Schema | [CONTRACT-002](../contracts/CONTRACT-002-recommendation.md) |
| Stage / ordering | Recommendation / per `opportunityId` |
| Idempotency | `eventId` |

Records a proposed allocation, never an authorization. Payload validates as Recommendation. Example: `{"eventType":"RecommendationGenerated","payload":{"recommendationId":"b6c2e191-3000-4000-8000-000000000001","proposedAmount":2500,"currency":"USD"}}`.


## Example payload

```json
{
  "recommendationId": "b6c2e191-3000-4000-8000-000000000001",
  "opportunityId": "a6c2e191-3000-4000-8000-000000000001",
  "proposedAmount": 2500,
  "currency": "USD",
  "rationale": "Equip the lab",
  "createdAt": "2026-08-03T16:05:00Z"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

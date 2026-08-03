# EVENT-003: RecommendationGenerated

| Producer | Fund Intel |
| --- | --- |
| Consumers | Autonomous Giving, Impact Relay |
| Schema | [CONTRACT-002](../contracts/CONTRACT-002-recommendation.md) |
| Stage / ordering | Recommendation / per `opportunityId` |
| Idempotency | `eventId` |

Records a proposed allocation, never an authorization. Payload validates as Recommendation. Example: `{"eventType":"RecommendationGenerated","payload":{"recommendationId":"b6c2e191-3000-4000-8000-000000000001","proposedAmount":2500,"currency":"USD"}}`.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

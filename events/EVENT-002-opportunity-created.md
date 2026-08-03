---
id: EVENT-002
version: 1.0.0
status: accepted
authority: normative
title: OpportunityCreated
owner: Fund Intel
lifecycle_stage: Opportunity
producer: Fund Intel
consumers:
- Autonomous Giving
- Impact Relay
schema: ../schemas/opportunity.json
contract: CONTRACT-001
idempotency: eventId
related_specs:
- SPEC-003
- SPEC-008
related_contracts:
- CONTRACT-001
---

# EVENT-002: OpportunityCreated

| Producer | Fund Intel |
| --- | --- |
| Consumers | Autonomous Giving, Impact Relay |
| Schema | [CONTRACT-001](../contracts/CONTRACT-001-opportunity.md) |
| Stage / ordering | Opportunity / per `opportunityId` |
| Idempotency | `eventId` |

Records creation of an actionable opportunity. Payload validates as Opportunity. Example: `{"eventType":"OpportunityCreated","payload":{"opportunityId":"a6c2e191-3000-4000-8000-000000000001","needId":"need-community-ai-lab","title":"Laptop access","status":"open","createdAt":"2026-08-03T16:00:00Z"}}`.


## Example payload

```json
{
  "opportunityId": "a6c2e191-3000-4000-8000-000000000001",
  "needId": "need-community-ai-lab",
  "title": "Laptop access",
  "status": "open",
  "createdAt": "2026-08-03T16:00:00Z"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

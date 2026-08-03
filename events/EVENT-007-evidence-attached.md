---
id: EVENT-007
version: 1.0.0
status: accepted
authority: normative
title: EvidenceAttached
owner: Impact Relay
lifecycle_stage: Evidence
producer: Impact Relay
consumers:
- Impact Relay
- Autonomous Giving
schema: ../schemas/evidence.json
contract: CONTRACT-004
idempotency: eventId
related_specs:
- SPEC-005
- SPEC-008
related_contracts:
- CONTRACT-004
---

# EVENT-007: EvidenceAttached

| Producer | Impact Relay |
| --- | --- |
| Consumers | Impact Relay, Autonomous Giving |
| Schema | [CONTRACT-004](../contracts/CONTRACT-004-evidence.md) |
| Stage / ordering | Evidence / per `allocationId` |
| Idempotency | `eventId` |

Records attributable evidence without editing prior evidence. Payload validates as Evidence. Example: `{"eventType":"EvidenceAttached","payload":{"evidenceId":"d6c2e191-3000-4000-8000-000000000001","type":"delivery_photo"}}`.


## Example payload

```json
{
  "evidenceId": "d6c2e191-3000-4000-8000-000000000001",
  "allocationId": "c6c2e191-3000-4000-8000-000000000001",
  "type": "delivery_photo",
  "uri": "https://evidence.example/community-ai-lab/delivery-1",
  "capturedAt": "2026-08-03T16:20:00Z",
  "source": "Community AI Lab"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

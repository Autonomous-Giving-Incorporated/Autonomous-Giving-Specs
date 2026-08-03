---
id: EVENT-001
version: 1.0.0
status: accepted
authority: normative
title: SignalDetected
owner: Fund Intel
lifecycle_stage: Signal
producer: Fund Intel
consumers:
- Fund Intel
- Impact Relay
schema: ../schemas/signal-detected.json
idempotency: eventId
related_specs:
- SPEC-003
- SPEC-008
related_contracts: []
---

# EVENT-001: SignalDetected

| Producer | Fund Intel |
| --- | --- |
| Consumers | Fund Intel, Impact Relay |
| Schema | [signal-detected.json](../schemas/signal-detected.json) in the common event envelope |
| Stage / ordering | Signal / per `signalId` |
| Idempotency | `eventId` |

Records a captured external observation. Payload contains `signalId`, `needId`, `source`, `observedAt`, and `confidence`. Example: `{"eventType":"SignalDetected","payload":{"signalId":"signal-1","needId":"need-community-ai-lab"}}`.


## Example payload

```json
{
  "signalId": "a0c2e191-3000-4000-8000-000000000001",
  "needId": "need-community-ai-lab",
  "source": "community-needs-survey",
  "observedAt": "2026-08-03T15:50:00Z",
  "confidence": 0.92
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

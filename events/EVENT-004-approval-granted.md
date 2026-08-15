---
id: EVENT-004
version: 1.0.0
status: accepted
authority: normative
title: ApprovalGranted
owner: Autonomous Giving
lifecycle_stage: Approval
producer: Autonomous Giving
consumers:
- Autonomous Giving
- Impact Relay
schema: ../schemas/approval-granted.json
idempotency: eventId
related_specs:
- SPEC-005
- SPEC-008
related_contracts:
- CONTRACT-011
---

# EVENT-004: ApprovalGranted

| Producer | Autonomous Giving |
| --- | --- |
| Consumers | Autonomous Giving, Impact Relay |
| Schema | [approval-granted.json](../schemas/approval-granted.json) in the common event envelope |
| Stage / ordering | Approval / per `recommendationId` |
| Idempotency | `eventId` |

Records an explicit human approval. Payload contains `approvalId`, `recommendationId`, `approvedBy`, `approvedAt`, and policy reference. The evaluated [CONTRACT-011](../contracts/CONTRACT-011-delegation-policy.md) policy (single or dual) MUST remain reconcilable to this event. Example: `{"eventType":"ApprovalGranted","payload":{"approvalId":"approval-community-ai-lab","approvedBy":"human-reviewer"}}`.


## Example payload

```json
{
  "approvalId": "approval-community-ai-lab",
  "recommendationId": "b6c2e191-3000-4000-8000-000000000001",
  "approvedBy": "human-reviewer",
  "approvedAt": "2026-08-03T16:08:00Z",
  "policyReference": "policy-human-approval-v1"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

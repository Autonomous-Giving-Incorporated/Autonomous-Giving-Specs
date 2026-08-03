# EVENT-004: ApprovalGranted

| Producer | Autonomous Giving |
| --- | --- |
| Consumers | Autonomous Giving, Impact Relay |
| Schema | [approval-granted.json](../schemas/approval-granted.json) in the common event envelope |
| Stage / ordering | Approval / per `recommendationId` |
| Idempotency | `eventId` |

Records an explicit human approval. Payload contains `approvalId`, `recommendationId`, `approvedBy`, `approvedAt`, and policy reference. Example: `{"eventType":"ApprovalGranted","payload":{"approvalId":"approval-community-ai-lab","approvedBy":"human-reviewer"}}`.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

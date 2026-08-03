# EVENT-004: ApprovalGranted

| Producer | Governance |
| --- | --- |
| Consumers | Allocation, Transparency |
| Schema | [approval-granted.json](../schemas/approval-granted.json) in the common event envelope |
| Stage / ordering | Approval / per `recommendationId` |
| Idempotency | `eventId` |

Records an explicit human approval. Payload contains `approvalId`, `recommendationId`, `approvedBy`, `approvedAt`, and policy reference. Example: `{"eventType":"ApprovalGranted","payload":{"approvalId":"approval-community-ai-lab","approvedBy":"human-reviewer"}}`.

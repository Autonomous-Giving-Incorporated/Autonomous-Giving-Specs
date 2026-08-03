# EVENT-004: ApprovalGranted

| Producer | Governance |
| --- | --- |
| Consumers | Allocation, Transparency |
| Schema | [CONTRACT-007](../contracts/CONTRACT-007-timeline-event.md) |
| Stage / ordering | Approval / per `recommendationId` |
| Idempotency | `eventId` |

Records an explicit human approval. Payload contains `approvalId`, `recommendationId`, `approvedBy`, `approvedAt`, and policy reference. Example: `{"eventType":"ApprovalGranted","payload":{"approvalId":"approval-community-ai-lab","approvedBy":"human-reviewer"}}`.

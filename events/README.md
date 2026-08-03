# Event library

All events use the immutable [event envelope schema](../schemas/event-envelope.json): `eventId` (UUID), `eventType`, `occurredAt` (RFC 3339), `schemaVersion`, `correlationId`, and `payload`. Producers guarantee at-least-once delivery; consumers deduplicate on `eventId`. Ordering is guaranteed only per aggregate identifier, and consumers must tolerate reordering across aggregates.

| ID | Event | Stage | Contract |
| --- | --- | --- | --- |
| EVENT-001 | [SignalDetected](EVENT-001-signal-detected.md) | Signal | Opportunity |
| EVENT-002 | [OpportunityCreated](EVENT-002-opportunity-created.md) | Opportunity | Opportunity |
| EVENT-003 | [RecommendationGenerated](EVENT-003-recommendation-generated.md) | Recommendation | Recommendation |
| EVENT-004 | [ApprovalGranted](EVENT-004-approval-granted.md) | Approval | TimelineEvent |
| EVENT-005 | [AllocationCreated](EVENT-005-allocation-created.md) | Allocation | Allocation |
| EVENT-006 | [ExecutionStarted](EVENT-006-execution-started.md) | Execution | Allocation |
| EVENT-007 | [EvidenceAttached](EVENT-007-evidence-attached.md) | Evidence | Evidence |
| EVENT-008 | [ReceiptGenerated](EVENT-008-receipt-generated.md) | Receipt | Receipt |
| EVENT-009 | [VerificationCompleted](EVENT-009-verification-completed.md) | Verification | Evidence |
| EVENT-010 | [NotificationSent](EVENT-010-notification-sent.md) | Notification | Notification |

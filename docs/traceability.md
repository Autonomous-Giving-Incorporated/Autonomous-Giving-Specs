# Platform traceability matrix

This matrix is the navigation layer between lifecycle authority and machine-readable contracts. It is informative; linked specifications and schemas remain normative.

| Lifecycle stage | Governing specification | Decision | Event | Contract / schema | Accountable owner |
| --- | --- | --- | --- | --- | --- |
| Signal | [SPEC-003](../specs/SPEC-003-signals-stack.md) | [ADR-003](../adr/ADR-003-platform-canon.md) | [EVENT-001](../events/EVENT-001-signal-detected.md) | [signal schema](../schemas/signal-detected.json) | Fund Intel |
| Opportunity | [SPEC-003](../specs/SPEC-003-signals-stack.md) | [ADR-003](../adr/ADR-003-platform-canon.md) | [EVENT-002](../events/EVENT-002-opportunity-created.md) | [CONTRACT-001](../contracts/CONTRACT-001-opportunity.md) / [schema](../schemas/opportunity.json) | Fund Intel |
| Recommendation | [SPEC-003](../specs/SPEC-003-signals-stack.md) | [ADR-006](../adr/ADR-006-human-approval.md) | [EVENT-003](../events/EVENT-003-recommendation-generated.md) | [CONTRACT-002](../contracts/CONTRACT-002-recommendation.md) / [schema](../schemas/recommendation.json) | Fund Intel |
| Approval | [SPEC-005](../specs/SPEC-005-lifecycle.md) | [ADR-006](../adr/ADR-006-human-approval.md) | [EVENT-004](../events/EVENT-004-approval-granted.md) | [approval schema](../schemas/approval-granted.json) | Governance |
| Allocation | [SPEC-005](../specs/SPEC-005-lifecycle.md) | [ADR-005](../adr/ADR-005-allocation-id.md) | [EVENT-005](../events/EVENT-005-allocation-created.md) | [CONTRACT-003](../contracts/CONTRACT-003-allocation.md) / [schema](../schemas/allocation.json) | Autonomous Giving |
| Execution | [SPEC-006](../specs/SPEC-006-capability-boundaries.md) | [ADR-010](../adr/ADR-010-future-services.md) | [EVENT-006](../events/EVENT-006-execution-started.md) | [execution schema](../schemas/execution-started.json) | Autonomous Giving |
| Evidence | [SPEC-005](../specs/SPEC-005-lifecycle.md) | [ADR-007](../adr/ADR-007-evidence-chain.md) | [EVENT-007](../events/EVENT-007-evidence-attached.md) | [CONTRACT-004](../contracts/CONTRACT-004-evidence.md) / [schema](../schemas/evidence.json) | Impact Relay |
| Receipt | [SPEC-005](../specs/SPEC-005-lifecycle.md) | [ADR-007](../adr/ADR-007-evidence-chain.md) | [EVENT-008](../events/EVENT-008-receipt-generated.md) | [CONTRACT-005](../contracts/CONTRACT-005-receipt.md) / [schema](../schemas/receipt.json) | Autonomous Giving |
| Verification | [SPEC-005](../specs/SPEC-005-lifecycle.md) | [ADR-007](../adr/ADR-007-evidence-chain.md) | [EVENT-009](../events/EVENT-009-verification-completed.md) | [verification schema](../schemas/verification-completed.json) | Impact Relay |
| Notification | [SPEC-006](../specs/SPEC-006-capability-boundaries.md) | [ADR-004](../adr/ADR-004-repository-ownership.md) | [EVENT-010](../events/EVENT-010-notification-sent.md) | [CONTRACT-006](../contracts/CONTRACT-006-notification.md) / [schema](../schemas/notification.json) | Impact Relay |
| ImpactNotice (projection) | [SPEC-027](../specs/SPEC-027-impact-loop.md) | [ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md) | [EVENT-011](../events/EVENT-011-impact-notice-issued.md) | [CONTRACT-013](../contracts/CONTRACT-013-impact-notice.md) / [schema](../schemas/impact-notice.json) | Impact Relay |
| Mission Graph (projection) | [SPEC-029](../specs/SPEC-029-mission-graph-and-learning-feedback.md) | [ADR-003](../adr/ADR-003-platform-canon.md) | No new event | Canonical lifecycle records; no new contract | Underlying record owner |
| Learning Feedback (relationship) | [SPEC-029](../specs/SPEC-029-mission-graph-and-learning-feedback.md), [SPEC-003](../specs/SPEC-003-signals-stack.md) | [ADR-003](../adr/ADR-003-platform-canon.md) | Existing Signal event when a new Signal is published | Existing Signal schema; source Impact/Verification/Evidence references | Fund Intel |
| Mission Intelligence Metric (derived artifact) | [SPEC-030](../specs/SPEC-030-mission-intelligence-metrics.md) | [ADR-006](../adr/ADR-006-human-approval.md) | No new event | Versioned policy and retained inputs; no new contract | Fund Intel |

## Cross-cutting invariants

- [SPEC-001](../specs/SPEC-001-platform-mission.md) governs every stage.
- [SPEC-004](../specs/SPEC-004-domain-model.md) owns the terminology used in every linked artifact.
- [SPEC-007](../specs/SPEC-007-contracts.md) and [SPEC-012](../specs/SPEC-012-versioning.md) govern all contract evolution.
- [SPEC-011](../specs/SPEC-011-demo-specification.md) applies this path deterministically in the Community AI Lab demonstration.
- [SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md) governs gift-summary, pot, allocation, and Evidence correctness (append-oriented tracking; connector webhook idempotency). AGI does not process donations ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md)).
- Preferred physical path (informative): [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md), [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)–[SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md). [ADR-012](../adr/ADR-012-render-first-platform.md) is superseded.
- Control plane (cross-cutting): [SPEC-028](../specs/SPEC-028-agi-control-plane.md), [ADR-014](../adr/ADR-014-agi-control-plane.md), [CONTRACT-008](../contracts/CONTRACT-008-auth-context.md)–[CONTRACT-012](../contracts/CONTRACT-012-public-projection.md), [EVENT-012](../events/EVENT-012-capability-context-issued.md).
- Trust layer: [SPEC-016](../specs/SPEC-016-security-and-trust-boundaries.md)–[SPEC-019](../specs/SPEC-019-identity-and-authorization.md) (accepted).
- Mission intelligence: [SPEC-029](../specs/SPEC-029-mission-graph-and-learning-feedback.md) defines the projection and feedback relationship; [SPEC-030](../specs/SPEC-030-mission-intelligence-metrics.md) defines evidence-bounded derived metrics. Both remain proposed; neither changes lifecycle ordering, capability authority, contracts, or event meaning.

# SPEC-004: Event Lifecycle

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Platform Architecture |
| Status | Accepted |
| Dependencies | SPEC-003, SPEC-006 |
| Related ADRs | ADR-005, ADR-006, ADR-007 |
| Related contracts | CONTRACT-001–007 |

## Purpose

Define the only canonical progression from need to impact.

## Lifecycle

`Need → Signal → Opportunity → Recommendation → Approval → Allocation → Execution → Evidence → Receipt → Verification → Impact`

## Requirements

- Each transition is represented by an immutable event with `eventId`, `occurredAt`, `schemaVersion`, and correlation identifiers.
- Transitions may be retried, but a consumer must deduplicate using the event idempotency key.
- Approval is required before `AllocationCreated` in the MVP.
- Evidence may arrive after execution, but verification and impact require attributable evidence.

## Non-goals

The lifecycle does not require synchronous processing or prescribe event transport.

## References

[Event library](../events/README.md) · [Lifecycle diagram](../diagrams/lifecycle.md) · [Evidence Chain ADR](../adr/ADR-007-evidence-chain.md)

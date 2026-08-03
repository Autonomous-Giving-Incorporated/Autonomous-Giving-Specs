# SPEC-003: Domain Model

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Platform Architecture |
| Status | Accepted |
| Dependencies | None |
| Related ADRs | ADR-003 |
| Related contracts | CONTRACT-001–007 |

## Purpose

Establish the canonical vocabulary. Definitions are normative in the [glossary](../glossary/README.md).

## Requirements

The canonical entities are: `Organization`, `Program`, `Need`, `Signal`, `Opportunity`, `Recommendation`, `Approval`, `Allocation`, `Execution`, `Evidence`, `Receipt`, `Verification`, `Impact`, and `Notification`. A contract or implementation must use these terms with their glossary meaning and must not introduce synonyms for them.

## Relationships

An Organization operates Programs. A Need is observed through Signals. An Opportunity groups a need and supporting signals. A Recommendation proposes an Allocation; Approval authorizes it; Execution carries it out; Evidence and Receipt substantiate it; Verification supports an Impact claim.

## Non-goals

This is not a persistence model or an object-relational schema.

## References

[Lifecycle](SPEC-004-event-lifecycle.md) · [Glossary](../glossary/README.md) · [Domain diagram](../diagrams/domain-model.md)

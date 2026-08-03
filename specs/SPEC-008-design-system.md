# SPEC-008: Design System

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Platform Product |
| Status | Proposed |
| Dependencies | SPEC-003, SPEC-007 |
| Related ADRs | None |
| Related contracts | CONTRACT-007 |

## Purpose

Define information-design invariants for implementation teams.

## Requirements

- Lifecycle stage, approval state, and evidence state must be visible and distinguishable.
- A user can navigate from an impact claim to verification, evidence, receipt, execution, allocation, approval, and recommendation.
- Time, actor, source, and immutable identifiers are displayed for audit-relevant records.
- Accessibility conformance target is WCAG 2.2 AA; color cannot be the sole carrier of governance state.

## Non-goals

This document does not mandate UI frameworks, tokens, components, or brand expression.

## References

[Demo](../demo/community-ai-lab.md) · [Timeline contract](../contracts/CONTRACT-007-timeline-event.md)

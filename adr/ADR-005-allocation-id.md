# ADR-005: allocationId

| Status | Accepted |
| --- | --- |
| Date | 2026-08-03 |
| Related specs | SPEC-004, SPEC-006 |

## Context

Allocation records must correlate approval, execution, evidence, and impact across boundaries.

## Decision

Use an immutable UUID `allocationId` as the primary cross-boundary allocation identifier.

## Consequences

It is never reassigned or embedded with business meaning.

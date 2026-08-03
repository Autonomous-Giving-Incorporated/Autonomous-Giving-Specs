# SPEC-001: Platform

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Platform Architecture |
| Status | Accepted |
| Dependencies | SPEC-003, SPEC-004, SPEC-006 |
| Related ADRs | ADR-001, ADR-003, ADR-004 |
| Related contracts | CONTRACT-001–007 |

## Purpose

Define the platform canon: a governed system that translates validated needs into attributable impact.

## Requirements

1. Every allocation has a stable `allocationId`, an approval, and evidence lineage.
2. Intelligence may generate signals and recommendations but cannot create an allocation.
3. Historical events and evidence are append-only; corrections are new records.
4. Impact claims link to verifiable evidence and the allocation that enabled them.

## Non-goals

This specification does not prescribe vendors, APIs, payment rails, user interfaces, or deployment topology.

## Rationale

Separating discovery, governance, execution, and proof makes responsibility and auditability explicit.

## References

[Domain model](SPEC-003-domain-model.md) · [Lifecycle](SPEC-004-event-lifecycle.md) · [Platform canon ADR](../adr/ADR-003-platform-canon.md)

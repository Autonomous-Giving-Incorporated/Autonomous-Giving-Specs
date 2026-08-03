# SPEC-010: Versioning

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Platform Architecture |
| Status | Accepted |
| Dependencies | SPEC-006 |
| Related ADRs | ADR-001 |
| Related contracts | CONTRACT-001–007 |

## Purpose

Define predictable evolution for platform authority and contracts.

## Requirements

- Repository releases are `MAJOR.MINOR.PATCH`.
- A normative artifact declares its own version. A release manifest (when introduced) records its resolved artifacts.
- MAJOR: incompatible required-field, lifecycle, or invariant change. MINOR: backward-compatible addition. PATCH: clarification or correction without behavior change.
- A deprecated contract field remains readable for at least one minor release and names its successor.

## References

[Contracts](SPEC-006-contracts.md) · [Repository Strategy ADR](../adr/ADR-001-repository-strategy.md)

# SPEC-005: Service Boundaries

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Platform Architecture |
| Status | Proposed |
| Dependencies | SPEC-001, SPEC-004 |
| Related ADRs | ADR-010 |
| Related contracts | CONTRACT-001–007 |

## Purpose

Define responsibility boundaries without defining implementation services.

## Requirements

| Capability | Sole responsibility |
| --- | --- |
| Intelligence | Observe, normalize, and recommend |
| Governance | Apply policy and record approval decisions |
| Allocation | Create authorized allocation records |
| Execution | Fulfil an allocation through a channel |
| Evidence | Collect and preserve claims and artifacts |
| Transparency | Publish the historical timeline without editing it |

No boundary may fabricate evidence or allocate funds without an authorization record.

## References

[Architecture overview](../architecture/overview.md) · [Future Services ADR](../adr/ADR-010-future-services.md)

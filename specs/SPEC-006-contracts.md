# SPEC-006: Contracts

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Platform Architecture |
| Status | Accepted |
| Dependencies | SPEC-003, SPEC-010 |
| Related ADRs | ADR-005, ADR-007 |
| Related contracts | CONTRACT-001–007 |

## Purpose

Set compatibility rules for data exchanged by platform boundaries.

## Requirements

- Every public contract has one owner, a semantic description, JSON Schema, version, examples, and validation rules.
- Required fields cannot be removed within a major version. Consumers ignore unknown fields unless a contract states otherwise.
- Every event envelope carries `eventId`, `eventType`, `occurredAt`, `schemaVersion`, and `correlationId`.
- Contracts use UUID strings for identifiers and RFC 3339 timestamps.

## References

[Contract library](../contracts/README.md) · [Schema library](../schemas/README.md) · [Versioning](SPEC-010-versioning.md)

# SPEC-007: Contracts
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-004, SPEC-012 | Related ADRs | ADR-005, ADR-007 | Related contracts | CONTRACT-001–007 |
## Purpose
Govern shared data exchanged across platform boundaries.
## Scope
The seven contracts in the [contract library](../contracts/README.md).
## Requirements
Each contract SHALL have one owner, semantic definition, schema, producer, consumer, validation rules, version, and example. Producers SHALL validate output; consumers SHALL tolerate unknown compatible fields.
## Non-goals
Contracts do not define transport APIs.

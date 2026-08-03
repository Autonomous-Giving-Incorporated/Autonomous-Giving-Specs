---
id: SPEC-007
title: Contracts
version: 1.0.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-004
- SPEC-012
related_adrs:
- ADR-005
- ADR-007
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

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

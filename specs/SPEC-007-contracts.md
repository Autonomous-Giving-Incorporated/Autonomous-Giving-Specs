---
id: SPEC-007
title: Contracts
version: 1.1.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-002A
- SPEC-004
- SPEC-012
- SPEC-015
related_adrs:
- ADR-005
- ADR-007
- ADR-011
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
| Version | 1.1.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-004, SPEC-012 | Related ADRs | ADR-005, ADR-007, ADR-011 | Related contracts | CONTRACT-001–007 |

## Purpose
Govern shared data exchanged across **capability** boundaries.

## Scope
The seven contracts in the [contract library](../contracts/README.md).

## Requirements
1. Each contract SHALL have one owner, semantic definition, schema, producer capability, consumer capability, validation rules, version, and example.
2. Producers SHALL validate output; consumers SHALL tolerate unknown compatible fields per [SPEC-015](SPEC-015-compatibility-and-evolution.md).
3. **Contracts define interfaces, not transport.** Transport MAY be an in-process function or module call, REST, events, gRPC, or a future protocol.
4. Contracts are **deployment-independent**: the same contract applies inside a modular monolith and across distributed processes.
5. Choosing a transport or deployment profile does not create a new contract version.

## Non-goals
Contracts do not define HTTP paths, message brokers, RPC frameworks, or infrastructure.

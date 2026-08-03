---
id: SPEC-002
title: Platform Principles
version: 1.0.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-001
- SPEC-002A
related_adrs:
- ADR-002
- ADR-006
- ADR-007
related_contracts:
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

# SPEC-002: Platform Principles
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | Constitution | Related ADRs | ADR-002, ADR-006, ADR-007 | Related contracts | CONTRACT-003–007 |
## Purpose
Turn the Constitution’s immutable principles into testable platform requirements.
## Scope
Every producer, consumer, projection, and impact claim.
## Requirements
Implementations SHALL enforce human approval before allocation, append-only evidence and history, provenance for impact claims, and single-responsibility **capability** ownership. Structural principles (capability-first, deployment independence, modular monolith by default) are in [SPEC-002A](SPEC-002A-architectural-principles.md).
## Non-goals
It does not select policy engines, audit-storage technology, brokers, or orchestrators.

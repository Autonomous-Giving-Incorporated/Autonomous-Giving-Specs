---
id: SPEC-012
title: Versioning
version: 1.0.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-007
related_adrs:
- ADR-001
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

# SPEC-012: Versioning
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-007 | Related ADRs | ADR-001 | Related contracts | CONTRACT-001–007 |
## Purpose
Define compatible evolution of platform authority.
## Scope
Repository releases and all normative artifact versions.
## Requirements
Releases SHALL use semantic versioning. Incompatible required behavior, lifecycle, or schema changes require MAJOR; compatible additions require MINOR; clarifications require PATCH.
## Non-goals
This does not impose implementation release calendars.

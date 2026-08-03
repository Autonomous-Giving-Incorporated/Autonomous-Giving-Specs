---
id: SPEC-013
title: Repository Conformance
version: 1.0.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-001
- SPEC-007
- SPEC-012
related_adrs:
- ADR-001
- ADR-004
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

# SPEC-013: Repository Conformance
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-001, SPEC-007, SPEC-012 | Related ADRs | ADR-001, ADR-004 | Related contracts | CONTRACT-001–007 |
## Purpose
Define how implementations declare and demonstrate conformity.
## Scope
All consuming repositories.
## Requirements
Repositories SHALL declare a pinned release and implemented artifact IDs. Required artifacts are mandatory; Recommended artifacts improve interoperability; Optional artifacts add no compatibility obligation; Experimental artifacts are not platform commitments.
## Non-goals
This does not certify production operations.

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

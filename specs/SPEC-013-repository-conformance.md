---
id: SPEC-013
title: Repository Conformance
version: 1.1.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-001
- SPEC-002A
- SPEC-007
- SPEC-012
- SPEC-020
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
| Version | 1.1.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-001, SPEC-002A, SPEC-007, SPEC-012 | Related ADRs | ADR-001, ADR-004 | Related contracts | CONTRACT-001–007 |

## Purpose
Define how implementations declare and demonstrate conformity to the platform canon.

## Scope
All consuming implementation repositories and products that claim platform conformance.

## Requirements
1. Repositories SHALL declare a pinned platform release and implemented artifact IDs.
2. Required artifacts are mandatory; Recommended improve interoperability; Optional add no compatibility obligation; Experimental are not platform commitments.
3. **Deployment topology is irrelevant to conformance.** Modular monolith, multi-process, and distributed profiles that implement the same capabilities, contracts, and lifecycle invariants are equally eligible.
4. Conformance is measured by declared artifacts, schema validation, and lifecycle behavior—not by container count, orchestrator choice, or number of deployables.
5. A single product repository MAY implement multiple capabilities (recommended modular monolith) and still declare each capability it owns.

## Non-goals
This does not certify production operations, SLOs, or a particular hosting model.

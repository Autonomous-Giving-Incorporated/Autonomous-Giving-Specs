---
id: SPEC-005
title: Lifecycle
version: 1.0.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-004
related_adrs:
- ADR-005
- ADR-006
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

# SPEC-005: Lifecycle
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-004 | Related ADRs | ADR-005, ADR-006, ADR-007 | Related contracts | CONTRACT-001–007 |
## Purpose
Define the sole canonical state progression.
## Scope
All lifecycle events and user-visible projections.
## Requirements
The sequence SHALL be `Need → Signal → Opportunity → Recommendation → Approval → Allocation → Execution → Evidence → Receipt → Verification → Impact`. Approval SHALL precede Allocation; impact SHALL follow verification.
## Non-goals
No transport, timing, or synchronous-processing requirement is implied.

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

# Architecture overview

The platform is an event-oriented, implementation-neutral system with five responsibility domains:

| Domain | Input | Output | Constraint |
| --- | --- | --- | --- |
| Intelligence | Needs and external observations | Signals, Opportunities, Recommendations | Never allocates |
| Governance | Recommendations and policy | Approvals | Never fabricates evidence |
| Allocation and Execution | Approvals | Allocations, execution records, receipts | Requires authorization |
| Evidence and Verification | Execution artifacts | Evidence, verification, impact support | Preserves provenance |
| Transparency | Canonical events | Timeline and notifications | Never edits history |

See [SPEC-006](../specs/SPEC-006-service-boundaries.md) and [domain diagram](../diagrams/domain-model.md).

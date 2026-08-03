# Architecture overview

## Logical architecture (normative)

The platform is capability-oriented and implementation-neutral, with five responsibility domains:

| Domain | Capability home | Input | Output | Constraint |
| --- | --- | --- | --- | --- |
| Intelligence | Fund Intel | Needs and external observations | Signals, Opportunities, Recommendations | Never allocates |
| Governance | Autonomous Giving | Recommendations and policy | Approvals | Never fabricates evidence |
| Allocation and Execution | Autonomous Giving | Approvals | Allocations, execution records, receipts | Requires authorization |
| Evidence and Verification | Impact Relay | Execution artifacts | Evidence, verification, impact support | Preserves provenance |
| Transparency | Impact Relay | Canonical events | Timeline and notifications | Never edits history |

Logical diagram (capabilities, not deployables):

```text
[Observations] → Fund Intel → Recommendation
                      │
                      ▼
              Autonomous Giving → Approval → Allocation → Execution → Receipt
                      │                              │
                      │                              ▼
                      └──────────────► Impact Relay → Evidence → Verification → Impact
                                              │
                                              ▼
                                         Notification / Timeline
```

See [SPEC-006](../specs/SPEC-006-capability-boundaries.md), [SPEC-002A](../specs/SPEC-002A-architectural-principles.md), and the [domain diagram](../diagrams/domain-model.md).

## Physical deployment (informative)

Logical capabilities do **not** require three deployments. The **recommended MVP** is a single deployment containing three modules:

```text
┌──────────────────────── Single Deployment ────────────────────────┐
│  Backend executable                                                │
│  ┌──────────────┐ ┌────────────────────┐ ┌────────────────────┐  │
│  │ Fund Intel   │ │ Autonomous Giving  │ │ Impact Relay       │  │
│  │ module       │ │ module             │ │ module             │  │
│  └──────────────┘ └────────────────────┘ └────────────────────┘  │
│         │                    │                      │              │
│         └────────────────────┴──────────────────────┘              │
│                              │                                     │
│                    PostgreSQL + Object Storage                     │
│                    (+ optional background worker)                  │
└────────────────────────────────────────────────────────────────────┘
         ▲
   GitHub Pages (public / demo surfaces)
```

Distributed processes, brokers, and Kubernetes appear only in optional later profiles ([SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)).

# Architecture overview

## Logical architecture (normative)

The platform is capability-oriented, with five responsibility domains:

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

## Physical deployment — preferred (informative)

Logical capabilities do **not** require three deployments. The **recommended MVP** is a Render modular monolith ([ADR-012](../adr/ADR-012-render-first-platform.md), [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md) Profile B, [SPEC-021](../specs/SPEC-021-preferred-application-stack.md)):

```text
┌──────────────────── Render (preferred) ────────────────────┐
│  Next.js Web Service (TypeScript modular monolith)         │
│  ┌──────────────┐ ┌────────────────────┐ ┌──────────────┐ │
│  │ Fund Intel   │ │ Autonomous Giving  │ │ Impact Relay │ │
│  │ module       │ │ module             │ │ module       │ │
│  └──────────────┘ └────────────────────┘ └──────────────┘ │
│  UI · route handlers · server actions · authz · webhooks   │
│                           │                                │
│                           ▼                                │
│              Render PostgreSQL (canonical store)           │
│              Drizzle migrations (explicit, reviewable)     │
└────────────────────────────────────────────────────────────┘
        │              │              │              │
        ▼              ▼              ▼              ▼
     Clerk          Stripe         Resend         OpenAI
   (identity)     (payments)      (email)      (AI primary)

Optional escalation (evidence-driven only):
  Background Worker · Cron Job · Private Service · Key Value · Workflows
```

### Baseline vs escalation

| Layer | Baseline MVP | Escalation |
| --- | --- | --- |
| Hosting | Render web service | Private service, multi-instance |
| Data | Render PostgreSQL | Read replica, specialized vector DB |
| Async | In-process job contract | Background Worker / Workflows |
| Schedule | None until needed | Cron Jobs |
| Cache | None until needed | Key Value |

**Rule:** do not create distributed infrastructure before workload evidence requires it ([SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)).

### Financial ownership (normative invariants)

- Stripe owns payment processor state; AGI owns internal ledger and donation/allocation records ([SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md)).
- Clerk owns authentication; AGI owns authorization ([SPEC-019](../specs/SPEC-019-identity-and-authorization.md), [SPEC-024](../specs/SPEC-024-integration-boundaries.md)).
- AI outputs are advisory until deterministic policy or authorized actors approve.

Distributed processes, brokers, and Kubernetes appear only in optional later profiles ([SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md) Profile D).

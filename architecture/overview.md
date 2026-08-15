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

Logical capabilities do **not** require three deployments. The **recommended MVP** is Cloudflare + Supabase ([ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md), [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md) Profile B, [SPEC-021](../specs/SPEC-021-preferred-application-stack.md)). [ADR-012](../adr/ADR-012-render-first-platform.md) Render topology is **historical**.

```text
┌──────────────── Cloudflare (preferred compute) ────────────┐
│  Workers / Pages / static assets (TypeScript modular unit) │
│  ┌──────────────┐ ┌────────────────────┐ ┌──────────────┐ │
│  │ Fund Intel   │ │ Autonomous Giving  │ │ Impact Relay │ │
│  │ module       │ │ module             │ │ module       │ │
│  └──────────────┘ └────────────────────┘ └──────────────┘ │
│  UI · Worker/route handlers · authz · webhooks             │
│  Durable Objects only if live coordination is needed       │
│  Queues / Cron Triggers for deferred, webhook, retry       │
└────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────── Supabase (preferred data) ─────────────────┐
│  Auth · PostgreSQL (canonical store) · Storage             │
│  Explicit SQL migrations (Drizzle acceptable)              │
└────────────────────────────────────────────────────────────┘
        │              │              │
        ▼              ▼              ▼
     Stripe         Resend         OpenAI
   (if required)  (if required)  (if required)
   Clerk only if a product still requires it

Optional escalation (evidence-driven only):
  additional Queues · Cron Triggers · Durable Objects
```

### Baseline vs escalation

| Layer | Baseline MVP | Escalation |
| --- | --- | --- |
| Hosting | Cloudflare Workers / Pages / static assets | Additional isolates; not a second PaaS |
| Data | Supabase PostgreSQL | Read replica, specialized vector DB |
| Auth | Supabase Auth | Clerk only if still required |
| Async | In-process job contract; Queues when deferred work exists | Additional Queues |
| Schedule | None until needed | Cron Triggers |
| Live coordination | None until needed | Durable Objects |

**Rule:** do not create distributed infrastructure before workload evidence requires it ([SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)).

### Financial ownership (normative invariants)

- Stripe owns payment processor state; AGI owns internal ledger and donation/allocation records ([SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md)).
- Supabase Auth owns authentication (Clerk only if still required); AGI owns authorization ([SPEC-019](../specs/SPEC-019-identity-and-authorization.md), [SPEC-024](../specs/SPEC-024-integration-boundaries.md)).
- AI outputs are advisory until deterministic policy or authorized actors approve.

Distributed processes, brokers, and Kubernetes appear only in optional later profiles ([SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md) Profile D).

# Platform Standards Roadmap

## Delivery evolution (recommended)

```text
Phase 0  Spec consolidation          ← Render-first canon (this release)
    ↓
Phase 1  Platform foundation         Next.js + PostgreSQL + Drizzle + Clerk + Render
    ↓
Phase 2  Financial core              Stripe + donations + ledger + webhook idempotency + receipts
    ↓
Phase 3  Allocation system           Funds, programs, allocation policies, disbursement tracking
    ↓
Phase 4  Operations                  Reconciliation, reporting, audit surfaces, observability
    ↓
Phase 5  AI assistance               Matching, analysis, recommendations + provenance
    ↓
Phase 6  Async / scale extraction    Workers, cron, Key Value, private services — only with evidence
```

Logical modular-monolith principle is unchanged; physical preferred path is Render-first ([ADR-012](../adr/ADR-012-render-first-platform.md)).

## Client product path (allocation middleware)

Informative product roadmap aligned to [allocation middleware design](../docs/superpowers/specs/2026-08-03-allocation-middleware-design.md). **Not a specification milestone**; guides implementation repositories. Hosting notes in pilot plans may describe historical Supabase/multi-host choices; **new platform work defaults to the preferred stack** above.

| Step | State | Where |
| --- | --- | --- |
| 1. every.org connector + campaign/program pots + allocate + exception inbox | **MVP shipped** | Portofolio-Signals `services/allocation-middleware/` |
| 2. Trail + board packet + proof SLA | **MVP shipped** | Same package |
| 3a. Pilot host: seed + local Node + director JWT | **Observed** | [pilot hosting](../docs/superpowers/plans/2026-08-03-hacker-dojo-pilot-hosting.md) · #72 |
| 3b. Public HTTPS (ephemeral) + seed-loop accept | **Observed** | #71 · `npm run accept:seed-loop` |
| 3c. Live every.org webhook + full director acceptance | **Open** | #73 · #74 remainder |
| 4. Additional donation-platform adapters (Givebutter, Donorbox, …) | Later | Adapter interface only in MVP |
| 5. Funder multi-grantee portfolio | Later | Out of MVP scope |
| 6. Align pilot durable host with preferred Render + Postgres path | Planned | Prefer SPEC-020/021 over multi-host recipe soup |

**Suite onboarding (implementation repos, not Spec SPECs):** people (C) → client shell (B) → document pack → second tenant (D) → allocation pilot. Runbooks on Portofolio-Signals. Map: [IMPLEMENTATION-PROGRESS](../docs/superpowers/IMPLEMENTATION-PROGRESS.md) · continuation [2026-08-08-suite-continuation](../docs/superpowers/plans/2026-08-08-suite-continuation.md).

Plans: [MVP](../docs/superpowers/plans/2026-08-03-allocation-middleware.md) · [pilot hosting](../docs/superpowers/plans/2026-08-03-hacker-dojo-pilot-hosting.md) · [suite continuation](../docs/superpowers/plans/2026-08-08-suite-continuation.md).

The platform evolves toward distribution only when operational criteria warrant it. Conformance remains topology-agnostic ([SPEC-013](../specs/SPEC-013-repository-conformance.md)); preferred deployment is explicit in SPEC-020–025.

## Specification milestones

| Milestone | Outcome | Exit criterion |
| --- | --- | --- |
| 1. Platform Canon | Constitution, vocabulary, lifecycle | SPEC-001, 002, 004, 005 accepted |
| 2. Architectural Principles | Capability-first, deployment independence | SPEC-002A accepted |
| 3. Signals Stack | Observation and recommendation boundary | SPEC-003 reviewed |
| 4. Contracts | Owned interoperable messages (transport-independent) | CONTRACT-001–007 validated |
| 5. Schemas | Versioned machine validation | SCHEMA-001–007 published |
| 6. Capability Boundaries | Logical responsibilities without deployables | SPEC-006 accepted |
| 7. Documentation | Cross-reference and review standard | SPEC-010 accepted |
| 8. Design System | Audit-visible information requirements | SPEC-009 reviewed |
| 9. Deployment Profiles | Informative MVP and evolution profiles | SPEC-020 published |
| 10. Platform Conformance | Declared implementation coverage (topology-agnostic) | SPEC-013 accepted by consumers |
| 11. Executable Canon | Validators, CI, indexes, release package | `validate_all.py` PASS on main |
| 12. Consumer Manifests | Measurable capability conformance | three example manifests + schema |
| 13. Demo Fixture | Deterministic positive/negative vectors | community-ai-lab fixtures validate |
| 14. Compatibility Policy | Evolution without silent breaks | SPEC-015 + ADR-011 accepted |
| 15. Trust Layer | Shared security/privacy model | SPEC-016–019 reviewed |
| 16. RFC Governance | Explicit status and approval rules | rfc-process.md adopted |
| 17. Render-first preferred stack | Preferred physical architecture + financial ops contracts | ADR-012 + SPEC-020 v2 + SPEC-021–025 accepted |

## Next recommended steps (implementation)

Specs Phase 0 (this repository) is complete when ADR-012 and SPEC-020–025 are merged. **Product implementation** should proceed in order. Do not skip financial invariants for UI velocity.

| Order | Workstream | Where | Exit criterion |
| --- | --- | --- | --- |
| 1 | Scaffold preferred stack | New or existing product repo | Next.js + TypeScript + Drizzle + `render.yaml` from [`render.yaml.example`](../render.yaml.example); local Postgres + migrations apply; health check responds |
| 2 | Platform foundation (Phase 1) | Product app | Clerk session → AGI principal; `users` / `organizations` / `organization_memberships`; app deploys to Render staging with linked Postgres |
| 3 | Financial core (Phase 2) | Product app | Stripe test mode; webhook verify + idempotent `webhook_events`; donations + `ledger_entries` per [SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md); browser callback not authoritative for settlement |
| 4 | Receipts and notifications | Product app | Receipt records immutable after issue; Resend non-blocking; settlement independent of email success |
| 5 | Allocation system (Phase 3) | Product app | Funds/programs; allocation attributable to source; disbursement tracking; human Approval gate where ADR-006 applies |
| 6 | Operations (Phase 4) | Product app | Correlation IDs across request→Stripe→webhook→DB→email; reconciliation job contract; recovery drill against [recovery runbook](../docs/recovery-runbook.md) |
| 7 | AI assistance (Phase 5) | Product app | `AIProvider` abstraction; OpenAI primary; `agent_runs` / `agent_decisions` provenance; no unvalidated financial side effects |
| 8 | Async/scale extraction (Phase 6) | Product app | Introduce Worker/Cron/KV **only** with measured latency, retry, or load evidence ([SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)) |
| 9 | Pilot alignment | Portofolio-Signals / allocation-middleware | Prefer durable Render + Postgres for greenfield; treat Supabase/multi-host recipes as historical unless re-justified; close every.org #73/#74 on existing pilot path without blocking preferred-stack greenfield |

### Immediate next actions (checklist)

1. **Merge this specs PR** so implementers pin a release that includes ADR-012 + SPEC-021–025.
2. **Open an implementation issue/PR** in the product repo titled “Phase 1 — Render foundation” linking SPEC-021, SPEC-022, SPEC-025, and [onboarding](../docs/onboarding.md).
3. **Copy contracts into the product repo:** `.env.example`, `render.yaml.example` → product `render.yaml`, onboarding checklist.
4. **Do not** add Background Workers, Cron, Key Value, or a vector database in the first PR without workload evidence.
5. **Do not** claim production readiness until Stripe webhook idempotency tests and a staging recovery dry-run pass.

Detailed day-one commands: [onboarding](../docs/onboarding.md). Extraction and stack rules: [implementation guidance](../docs/implementation-guidance.md).

# Platform Standards Roadmap

## Delivery evolution (recommended)

```text
Phase 0  Spec consolidation          ← ADR-013 host · ADR-015 money · ADR-014/SPEC-028 control plane
    ↓
Phase 1  Platform foundation         Next.js + Workers + Supabase Auth/Postgres/Storage
    ↓
Phase 2  Tracking core               every.org connector + pots + Worker webhook idempotency + ImpactNotice
    ↓
Phase 3  Allocation system           Funds, programs, allocation policies, disbursement tracking
    ↓
Phase 4  Operations                  Reconciliation, reporting, audit surfaces, observability
    ↓
Phase 5  AI assistance               Matching, analysis, recommendations + provenance
    ↓
Phase 6  Async / scale extraction    Durable Objects, additional Queues/Cron — only with evidence
```

Logical modular-monolith principle is unchanged; physical preferred path is Cloudflare + Supabase ([ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)). [ADR-012](../adr/ADR-012-render-first-platform.md) Render-first phases are **historical**.

## Client product path (allocation middleware)

Informative product roadmap aligned to [allocation middleware design](../docs/superpowers/specs/2026-08-03-allocation-middleware-design.md). **Not a specification milestone**; guides implementation repositories. Hosting notes in pilot plans may describe historical multi-host or Render choices; **new platform work defaults to the preferred stack** above.

| Step | State | Where |
| --- | --- | --- |
| 1. every.org connector + campaign/program pots + allocate + exception inbox | **MVP shipped** | Portofolio-Signals `services/allocation-middleware/` |
| 2. Trail + board packet + proof SLA | **MVP shipped** | Same package |
| 3a. Pilot host: seed + local Node + director JWT | **Observed** | [pilot hosting](../docs/superpowers/plans/2026-08-03-hacker-dojo-pilot-hosting.md) · #72 |
| 3b. Public HTTPS (ephemeral) + seed-loop accept | **Observed** | #71 · `npm run accept:seed-loop` |
| 3c. Live every.org webhook + full director acceptance | **Open** | #73 · #74 remainder |
| 4. Additional donation-platform adapters (Givebutter, Donorbox, …) | Later | Adapter interface only in MVP |
| 5. Funder multi-grantee portfolio | Later | Out of MVP scope |
| 6. Align pilot durable host with preferred Cloudflare + Supabase path | Planned | Prefer SPEC-020/021 (ADR-013) over multi-host or Render recipe soup |

**Suite onboarding (implementation repos, not Spec SPECs):** people (C) → client shell (B) → document pack → second tenant (D) → allocation pilot. Runbooks on Portofolio-Signals. Map: [IMPLEMENTATION-PROGRESS](../docs/superpowers/IMPLEMENTATION-PROGRESS.md) · continuation [2026-08-08-suite-continuation](../docs/superpowers/plans/2026-08-08-suite-continuation.md).

Plans: [MVP](../docs/superpowers/plans/2026-08-03-allocation-middleware.md) · [pilot hosting](../docs/superpowers/plans/2026-08-03-hacker-dojo-pilot-hosting.md) · [suite continuation](../docs/superpowers/plans/2026-08-08-suite-continuation.md).

The platform evolves toward distribution only when operational criteria warrant it. Conformance remains topology-agnostic ([SPEC-013](../specs/SPEC-013-repository-conformance.md)); preferred deployment is explicit in SPEC-020–025.

## Specification milestones

| Milestone | Outcome | Exit criterion |
| --- | --- | --- |
| 1. Platform Canon | Constitution, vocabulary, lifecycle | SPEC-001, 002, 004, 005 accepted |
| 2. Architectural Principles | Capability-first, deployment independence | SPEC-002A accepted |
| 3. Signals Stack | Observation and recommendation boundary | SPEC-003 accepted |
| 4. Contracts | Owned interoperable messages (transport-independent) | CONTRACT-001–007 validated |
| 5. Schemas | Versioned machine validation | SCHEMA-001–007 published |
| 6. Capability Boundaries | Logical responsibilities without deployables | SPEC-006 accepted |
| 7. Documentation | Cross-reference and review standard | SPEC-010 accepted |
| 8. Design System | Audit-visible information requirements | SPEC-009 accepted |
| 9. Deployment Profiles | Informative MVP and evolution profiles | SPEC-020 published |
| 10. Platform Conformance | Declared implementation coverage (topology-agnostic) | SPEC-013 accepted by consumers |
| 11. Executable Canon | Validators, CI, indexes, release package | `validate_all.py` PASS on main |
| 12. Consumer Manifests | Measurable capability conformance | three example manifests + schema |
| 13. Demo Fixture | Deterministic positive/negative vectors | community-ai-lab fixtures validate |
| 14. Compatibility Policy | Evolution without silent breaks | SPEC-015 + ADR-011 accepted |
| 15. Trust Layer | Shared security/privacy model | SPEC-016–019 written (later accepted in milestone 20) |
| 16. RFC Governance | Explicit status and approval rules | rfc-process.md adopted |
| 17. Render-first preferred stack (historical) | Prior physical architecture + financial ops contracts | ADR-012 + SPEC-020 v2 + SPEC-021–025 accepted; **superseded by milestone 18** |
| 18. Cloudflare + Supabase hosted platform | Preferred physical architecture aligned to ADR-013 | ADR-013 accepted; SPEC-020–025 body diagrams match Cloudflare + Supabase |
| 19. Donation-tracking money boundary | AGI tracks gifts; Stripe is tenant billing only | ADR-015, SPEC-023 v2, SPEC-026, SPEC-027, CONTRACT-013 accepted (already on main) |
| 20. Control plane + trust layer | AGI admin/login surface, capability JWTs, accepted trust SPECs | SPEC-028 accepted; ADR-014 accepted; SPEC-016–019 accepted; CONTRACT-008–012 accepted |
| 21. Closed-loop mission intelligence | Mission Graph projection, learning-feedback and metric framework | SPEC-029 and SPEC-030 proposed; no formula, forecasting, new lifecycle, or authority accepted |

## Next recommended steps (implementation)

Specs Phase 0 (this repository) now includes host alignment (milestone 18), the donation-tracking money boundary (milestone 19), and the control plane + trust layer (milestone 20). Platform release **v2.0.0** pins that specification set. Pinning specs is not implementation READY and is not a live Worker. The mission-intelligence specifications are proposed additions and are not an accepted platform release. **Product implementation** should proceed in order. Do not skip financial invariants for UI velocity.

### Closed-loop mission intelligence sequence

The following sequence is additive to the existing foundation, tracking, allocation, Evidence, and authorization work. It does not claim that forecasting exists.

| Order | Workstream | Exit criterion |
| --- | --- | --- |
| 1 | Canonical Signal / Opportunity / Recommendation production | Fund Intel produces traceable advisory records under SPEC-003; no Approval or Allocation authority |
| 2 | Mission Graph projection | Authorized linked-record traversal resolves to canonical owners; no duplicate system of record |
| 3 | Learning-feedback ingestion | Verified or explicitly classified downstream evidence yields a new provenance-bearing Signal through Fund Intel |
| 4 | Metric policy implementations | Each metric has retained inputs, calculation-policy version, classification, reproducibility, and `NOT_COMPUTABLE` handling; no arbitrary formula is frozen |
| 5 | Mission Intelligence Console | Authenticated AGI projection summarizes the mission path and routes consequential actions to owning capabilities |
| 6 | Historical metric/version storage | Historical results preserve their original policy/input references; revised policy produces distinct outputs |
| 7 | Validation against real tenant evidence | Operator-approved empirical evaluation demonstrates data sufficiency, provenance, staleness handling, and tenant isolation |
| 8 | Later forecasting | Consider only after sufficient validated data exists; remain advisory and evidence-bounded |

| Order | Workstream | Where | Exit criterion |
| --- | --- | --- | --- |
| 1 | Scaffold preferred stack | New or existing product repo | Next.js + TypeScript + explicit migrations; Wrangler/Pages in the **product** repo; Supabase project linked; local Postgres/Supabase + migrations apply; health check responds |
| 2 | Platform foundation (Phase 1) | Product app | Supabase Auth session → AGI principal; `users` / `organizations` / `organization_memberships`; app deploys to Cloudflare staging talking to Supabase Postgres |
| 3 | Tracking core (Phase 2) | Product app | every.org webhook verify + idempotent `chargeId`; pots + gift summaries per [SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md) / [SPEC-026](../specs/SPEC-026-donation-source-connectors.md); browser callback not authoritative; Stripe only if tenants are billed |
| 4 | Evidence and ImpactNotice | Product app | Evidence (or human waive) then [SPEC-027](../specs/SPEC-027-impact-loop.md); Resend/push/in_app; CTA = tenant `donation_link`; no invented PII |
| 5 | Allocation system (Phase 3) | Product app | Funds/programs; allocation attributable to source; disbursement tracking; human Approval gate where ADR-006 applies |
| 6 | Operations (Phase 4) | Product app | Correlation IDs across connector→Worker→DB→ImpactNotice; reconciliation of gifts vs pots; recovery drill against [recovery runbook](../docs/recovery-runbook.md) |
| 7 | AI assistance (Phase 5) | Product app | `AIProvider` abstraction; OpenAI primary if used; `agent_runs` / `agent_decisions` provenance; no unvalidated financial side effects |
| 8 | Async/scale extraction (Phase 6) | Product app | Introduce additional Queues/Cron/Durable Objects **only** with measured latency, retry, or coordination evidence ([SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)) |
| 9 | Pilot alignment | Portofolio-Signals / allocation-middleware | Prefer Cloudflare + Supabase for greenfield; treat Render/Vercel/multi-host recipes as historical unless re-justified; close every.org #73/#74 on existing pilot path without blocking preferred-stack greenfield |

### Immediate next actions (checklist)

1. **Pin `v2.0.0`** (this release). Consumers should pin the tag, not floating `main`. The pin includes ADR-013 and SPEC-020–025 diagrams aligned to Cloudflare + Supabase.
2. **Open an implementation issue/PR** in the product repo titled “Phase 1 — Cloudflare + Supabase foundation” linking SPEC-021, SPEC-022, SPEC-025, and [onboarding](../docs/onboarding.md).
3. **Copy contracts into the product repo:** `.env.example`, onboarding checklist. Keep Wrangler/Pages config in the product repo only. Do **not** copy [`docs/historical/render.yaml.example`](../docs/historical/render.yaml.example) as the preferred path.
4. **Do not** add Durable Objects, extra Queues, Cron, D1, or a vector database in the first PR without workload evidence (Queues/Cron are appropriate when deferred/webhook/retry work already exists).
5. **Do not** claim production readiness until connector webhook idempotency tests and a staging recovery dry-run pass. Do not mark READY from specs alone.

Detailed day-one commands: [onboarding](../docs/onboarding.md). Extraction and stack rules: [implementation guidance](../docs/implementation-guidance.md).

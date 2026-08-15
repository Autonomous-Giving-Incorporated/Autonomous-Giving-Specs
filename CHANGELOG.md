# Changelog

All notable changes to the Autonomous Giving Platform Specification are documented here.
Versions follow [SPEC-012](specs/SPEC-012-versioning.md) semantic versioning.

## [Unreleased]

### Added

- **SPEC-028** AGI Control Plane (normative, accepted): authenticated admin/login surface, capability JWTs (CONTRACT-008), fail-closed tenant checks, optional dual approval, Cloudflare + Supabase topology; Cloud Run historical/optional only.
- **EVENT-012** CapabilityContextIssued (audit of AGI-issued auth context).
- **SCHEMA-008–012** catalog rows for control-plane contracts.
- Glossary **TERM-030** AGI Control Plane.
- Roadmap specification milestones **19** (donation-tracking money boundary, already on main) and **20** (control plane + trust layer).
- Community AI Lab declared negative vectors: unverified webhook, duplicate `chargeId`, over-allocation, missing proof, invented PII.

### Changed

- **ADR-014** v1.1.0 **Accepted** (2026-08-15): host language aligned to ADR-013 / SPEC-028; Cloud Run demoted to historical/optional for an existing Impact Relay implementation.
- **SPEC-016–019** accepted; wired to ADR-014, SPEC-028, SPEC-027 / CONTRACT-013 (privacy / ImpactNotice / no invented PII); SPEC-019 requires capability JWTs and deny-by-default on unverified downstream context.
- **CONTRACT-008–012** accepted; schemas already present and validating.
- **SPEC-003** v2.0.0 accepted: observation→recommendation rules, gift-summary vs recommendation split, negative cases.
- **SPEC-009** v2.0.0 accepted: audit-visible information design (not a UI kit).
- **SPEC-011** v2.0.0 accepted: Community AI Lab written to actual fixtures (2500 USD); gift tracked / ImpactNotice skip / no Stripe donation.
- **SPEC-014** v2.0.0 accepted: fourth-capability admission; control plane is AGI’s edge; P1 connectors are adapters.
- **ADR-009** accepted; Community AI Lab amount narrative aligned to `scenario.json` (2500 USD).
- README preferred-stack sentence: Stripe is tenant/SaaS billing only.
- Architecture overview: Stripe-as-donation-processor language withdrawn.

### Added (prior)

- **SPEC-026** Donation-source Connectors (normative): every.org P0 adapter, verify, raw payload, idempotent `chargeId`, `netAmount` default, auto-create pot/slice, exception catalog, CSV twin, no AGI checkout.
- **SPEC-027** Impact Loop (normative): ImpactNotice only after Evidence or explicit human waive; channels email/push/in_app; CTA = tenant Donation Link; no invented PII.
- **CONTRACT-013** / **SCHEMA-013** / **EVENT-011** ImpactNotice (CONTRACT-008 remains AGI Auth Context).
- **ADR-015** Donation Tracking versus Tenant Billing (Nygard): donations tracked via connectors; Stripe = tenant billing only; tenant pages link out.
- Glossary TERM-025–029 (Gift Summary, Pot, Donation-source Connector, ImpactNotice, Donation Link).
- Informative [sprint remaining work](docs/sprint-remaining-work-donation-tracking.md) (OBSERVED Worker/`am_*` vs remaining code vs operator-owned; not READY).
- Migration notes: [v2.0.0 donation-tracking boundary](docs/migrations/v2.0.0-donation-tracking-boundary.md).

### Changed

- **SPEC-023** v2.0.0 (**MAJOR** artifact): tracking ledger; AGI never processes donations; connector gift state ≠ pot credit ≠ allocation ≠ Evidence. Stripe donation lifecycle withdrawn.
- **SPEC-024** v1.2.0: every.org is P0 donation-source connector; Stripe is tenant/SaaS billing only; Resend (or equivalent) + `push` for notices; `donation_link` is an outbound tenant URL.
- **CONTRACT-006** / notification schema v1.1.0: channel enum widened with `push` (backward compatible).
- **SPEC-004–008**, **SPEC-016**, **SPEC-020–022**, **SPEC-025**: aligned to the money-boundary split; no fifth capability.
- Allocation middleware design: canon pointer to SPEC-026/027 and ADR-015; historical host notes remain non-preferred.

### Changed (prior)

- **SPEC-020** v2.1.0: Profile B (recommended), Profile C, and Evolution Phase 1 now diagram Cloudflare + Supabase (ADR-013). Render Profile B preserved only under **Historical (superseded)**.
- **SPEC-021** v1.1.0: Baseline topology and optional escalation are Cloudflare Workers/Pages + Queues/Cron/Durable Objects + Supabase. Render web/worker/cron/KV/Workflows text is labeled historical.
- **SPEC-025** v1.1.0: Operations contract is Cloudflare + Supabase (env catalog, deploy, backups, cron, scale). Render Blueprint section demoted to historical.
- **SPEC-022** v1.1.0: Preferred datastore is Supabase PostgreSQL, not Render PostgreSQL. D1 remains non-canonical.
- **SPEC-016** v1.2.0 / **SPEC-019** v1.3.0 / **SPEC-024** v1.1.0: Preferred identity is Supabase Auth; Clerk only if a product still requires it. Preferred deploy security notes follow ADR-013.
- Moved [`render.yaml.example`](docs/historical/render.yaml.example) to `docs/historical/` and labeled **do-not-use** (pointer to ADR-013). No Wrangler/Pages deployable added to this repo.
- Architecture overview, roadmap, recovery runbook, `.env.example`, docs index, and leftover “preferred Render” notes in superpowers plans: aligned to Cloudflare + Supabase. ADR-012 file retained as superseded.
- README preferred physical stack and reference deployment: Cloudflare + Supabase (ADR-013); Render is not the path.

- **ADR-013** Cloudflare and Supabase Hosted Platform (accepted, v1.1.0): canonical stack is Cloudflare (Workers, static assets/Pages, Durable Objects if needed, Queues/Cron Triggers) + Supabase (Auth, PostgreSQL, Storage). Allocation middleware, webhooks, and Postgres-backed services run as Workers talking to Supabase. **Supersedes ADR-012.** Stripe/Resend/OpenAI/Clerk remain only if still required.
- **ADR-012** Render-First Platform and PostgreSQL Consolidation (superseded 2026-08-13 by ADR-013; file retained).
- **SPEC-021** Preferred Application Stack (informative): Render + Next.js + PostgreSQL + Clerk/Stripe/Resend/OpenAI.
- **SPEC-022** PostgreSQL Persistence and Domain Ownership (informative): entity ownership, design rules, Drizzle, optional pgvector.
- **SPEC-023** Financial Ledger Invariants (normative): append-only finance, webhook idempotency, state separation, AI advisory limits.
- **SPEC-024** Integration Boundaries (informative): Clerk / Stripe / Resend / OpenAI.
- **SPEC-025** Operations, Deploy, Observability, and Scale (informative): env catalog, environments, Blueprint, jobs, cron, backups, scale triggers.
- [Engineering onboarding](docs/onboarding.md), [recovery runbook](docs/recovery-runbook.md), [`.env.example`](.env.example), historical [`render.yaml.example`](docs/historical/render.yaml.example).
- Glossary TERM-021–024 (Preferred Stack, Ledger Entry, Webhook Event, Job).
- Roadmap **Next recommended steps** (implementation order, exit criteria, immediate checklist) linked from README, onboarding, and implementation guidance.
- Product design: [allocation middleware](docs/superpowers/specs/2026-08-03-allocation-middleware-design.md) (every.org-first, pot hierarchy, exception-only ops).
- [Implementation progress](docs/superpowers/IMPLEMENTATION-PROGRESS.md) — informative map of Portofolio-Signals (Fund-Intel) pilot + suite onboarding (refreshed 2026-08-08).
- [Suite continuation plan](docs/superpowers/plans/2026-08-08-suite-continuation.md) — post-#112 operator workstreams (pack activate, people MFA, pilot #73/#74).

### Changed (prior ADR-013 landing)

- `docs/implementation-guidance.md` and `docs/onboarding.md`: Cloudflare + Supabase; Workers (or Worker + Queue) talk to Supabase; ADR-012 superseded.
- SPEC-020 / SPEC-021 / SPEC-002A / Constitution: preferred hosted platform is ADR-013; ADR-012 and Render diagrams are historical.
- Glossary TERM-021: Preferred Stack is Cloudflare + Supabase (ADR-013).
- **ADR-012** marked superseded by ADR-013 (file retained).
- **SPEC-020** v2.0.0: recommended MVP profile is Render-first Next.js + PostgreSQL; GitHub Pages + generic backend diagram superseded as preferred physical path.
- **SPEC-002A** v1.1.0: preferred physical realization pointer to ADR-012 / SPEC-021.
- **SPEC-016** v1.1.0 / **SPEC-019** v1.2.0: webhook, secrets, SQL, PCI scope reduction, identity vs authorization (Clerk preferred).
- Constitution: preferred physical path is informative and does not condition conformance.
- README, architecture overview, implementation guidance, roadmap: aligned to Render-first baseline; workers/cron/KV as escalation only.
- Superpowers pilot/suite plans: marked Supabase/multi-host/Vercel notes as historical where they conflict with preferred stack.
- [Implementation progress](docs/superpowers/IMPLEMENTATION-PROGRESS.md) + [suite continuation](docs/superpowers/plans/2026-08-08-suite-continuation.md): Client Onboarding Pack **platform schema + Edge OBSERVED** (2026-08-08); MFA dry-run still pending.

- [Implementation progress](docs/superpowers/IMPLEMENTATION-PROGRESS.md) (2026-08-08 evening): people matrix (Ed = HD director only; Qi + primary master_admin); HD data gate #111/#112; pack activate still PENDING; links to continuation plan.
- [Specification roadmap](roadmap/specification-roadmap.md): suite onboarding path + continuation plan pointer; people access note.
- [Implementation progress](docs/superpowers/IMPLEMENTATION-PROGRESS.md) (2026-08-08): Client Onboarding Pack **code MERGED** ([Portofolio-Signals #104](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/pull/104)); platform apply still PENDING; suite hub + CURRENT-STATE links use Portofolio-Signals; C/B/D dry-runs OBSERVED; every.org #73/#74 remain open.
- [Specification roadmap](roadmap/specification-roadmap.md): suite onboarding path includes document pack; Portofolio-Signals naming.
- [Pilot hosting plan](docs/superpowers/plans/2026-08-03-hacker-dojo-pilot-hosting.md): refreshed status table; removed accidental shell-paste tail; linked closed #71/#72 and open #73/#74.
- [Allocation middleware design](docs/superpowers/specs/2026-08-03-allocation-middleware-design.md) and [MVP plan](docs/superpowers/plans/2026-08-03-allocation-middleware.md): status lines aligned to pilot OBSERVED vs every.org pending.
- [Specification roadmap](roadmap/specification-roadmap.md) client product path: steps 3a–3c; suite onboarding pointers.


## [1.1.0] — 2026-08-03

### Changed (architecture simplification — capability-first)

- Constitution: **Capability Boundaries** and **Deployment Independence**; “service owns one responsibility” → capability.
- **SPEC-002A** Architectural Principles (capability first, modular monolith by default, extract only when justified).
- **SPEC-006** retitled **Capability Boundaries** (file `SPEC-006-capability-boundaries.md`); not deployables.
- **SPEC-003, 007, 008, 013, 014, 016, 019** clarified as transport- and deployment-independent.
- **SPEC-014** retitled Future Capabilities.
- **SPEC-020** Reference Deployment Profiles (A Demo, B MVP recommended, C Production, D Enterprise).
- **ADR-010** Capability Independence; modular monolith default.
- Glossary: Capability, Module, Deployment, Service (optional), Modular Monolith.
- README, architecture, diagrams, roadmap: modular monolith MVP; no mandated Kubernetes/broker/mesh.
- `docs/implementation-guidance.md` with recommended stack and extraction decision matrix.

### Compatibility

- Lifecycle vocabulary and contract ownership unchanged.
- Deployment profile is informative; pin continues at SemVer of this repository.
- Consumers may remain modular monolith or distributed without losing conformance class.

## [1.0.0] — 2026-08-03

### Added

- Platform constitution and v1 normative canon (SPECs, ADRs, contracts, events, schemas).
- Lifecycle traceability matrix and glossary.
- Executable validation toolchain (`validation/validate_all.py`) with machine-readable report.
- Artifact frontmatter metadata and meta-schemas under `schemas/meta/`.
- Generated indexes under `generated/`.
- Consumer conformance manifests for Fund Intel, Autonomous Giving, and Impact Relay.
- Deterministic Community AI Lab demo fixtures under `demo/community-ai-lab/`.
- Distributable release packaging (`validation/package_release.py`) and CI gates.
- **SPEC-015** Compatibility and Evolution; **ADR-011** Contract Evolution Policy.
- **SPEC-016–019** security trust boundaries, data classification/privacy, evidence integrity, identity/authorization (proposed unless noted).
- RFC process, artifact status transitions, reviewer matrix, emergency correction, and release authority (`docs/rfc-process.md`, governance updates).
- Baseline migration guide `docs/migrations/v1.0.0-baseline.md`.

### Compatibility

- Initial public platform specification release. Consumers should pin `1.0.0`.

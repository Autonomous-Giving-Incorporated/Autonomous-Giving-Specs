# Changelog

All notable changes to the Autonomous Giving Platform Specification are documented here.
Versions follow [SPEC-012](specs/SPEC-012-versioning.md) semantic versioning.

## [Unreleased]

### Added

- Product design: [allocation middleware](docs/superpowers/specs/2026-08-03-allocation-middleware-design.md) (every.org-first, pot hierarchy, exception-only ops).
- [Implementation progress](docs/superpowers/IMPLEMENTATION-PROGRESS.md) — informative map of Portofolio-Signals (Fund-Intel) pilot + suite onboarding (refreshed 2026-08-08).
- [Suite continuation plan](docs/superpowers/plans/2026-08-08-suite-continuation.md) — post-#112 operator workstreams (pack activate, people MFA, pilot #73/#74).

### Changed

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

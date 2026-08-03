# Changelog

All notable changes to the Autonomous Giving Platform Specification are documented here.
Versions follow [SPEC-012](specs/SPEC-012-versioning.md) semantic versioning.

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

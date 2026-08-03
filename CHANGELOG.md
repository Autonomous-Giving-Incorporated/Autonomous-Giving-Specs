# Changelog

All notable changes to the Autonomous Giving Platform Specification are documented here.
Versions follow [SPEC-012](specs/SPEC-012-versioning.md) semantic versioning.

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

### Compatibility

- Initial public platform specification release. Consumers should pin `1.0.0`.

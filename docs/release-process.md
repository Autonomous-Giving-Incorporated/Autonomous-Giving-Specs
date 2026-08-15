# Release process

## Platform Specification v2.0.0

Released 2026-08-15. Consumers pin git tag `v2.0.0`. AGI tracks gifts and does not process donations (SPEC-023 v2.0.0; ADR-015). every.org is the P0 donation-source connector; Stripe is tenant/SaaS billing only. SPEC-001–028 are accepted. Migration: [v2.0.0 donation-tracking boundary](migrations/v2.0.0-donation-tracking-boundary.md). This pin is a specification cut, not a live Worker or product READY claim.

## Platform Specification v1.0

The initial release contains the platform canon, lifecycle, owned contract set, JSON Schema library, deterministic demo, documentation standards, executable validation, conformance manifests, and recorded decisions (including compatibility and trust specifications).

## Tag conventions

- Tags: `vMAJOR.MINOR.PATCH` (example: `v1.0.0`)
- Package directory: `dist/autonomous-giving-spec-vMAJOR.MINOR.PATCH/`
- Schema `$id` values embed the artifact version and are immutable per version

## Release checklist

1. Confirm every normative document declares version, owner, and status (frontmatter).
2. Run `python validation/validate_all.py` (must PASS) and regenerate indexes:
   `python validation/generate_indexes.py`
3. Build the release package: `python validation/package_release.py --version MAJOR.MINOR.PATCH`
4. Determine semantic-version impact using [SPEC-012](../specs/SPEC-012-versioning.md) and [SPEC-015](../specs/SPEC-015-compatibility-and-evolution.md).
5. For MAJOR releases, complete `docs/migrations/` guide from the prior version.
6. Tag the approved commit as `vMAJOR.MINOR.PATCH`. The [release workflow](../.github/workflows/release.yml) publishes archives and checksums.
7. Notify Fund Intel, Autonomous Giving Incorporated, and Impact Relay of the pin.

## Compatibility record

Release notes must enumerate added, changed, deprecated, and removed artifacts. A breaking contract change includes a migration window and consumer owner acknowledgement per [ADR-011](../adr/ADR-011-contract-evolution-policy.md).

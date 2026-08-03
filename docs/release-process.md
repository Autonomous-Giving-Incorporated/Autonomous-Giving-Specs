# Release process

## Platform Specification v1.0

The initial release contains the platform canon, lifecycle, owned contract set, JSON Schema library, deterministic demo, documentation standards, and recorded decisions.

## Release checklist

1. Confirm every normative document declares version, owner, and status.
2. Run [validation](validation.md) locally and allow the GitHub validation workflow to pass.
3. Determine semantic-version impact using [SPEC-012](../specs/SPEC-012-versioning.md).
4. Tag the approved commit as `vMAJOR.MINOR.PATCH` and publish release notes naming changed stable IDs and migration obligations.
5. Notify implementation repositories of the resolved release version.

## Compatibility record

Release notes must enumerate added, changed, deprecated, and removed artifacts. A breaking contract change includes a migration window and a consumer owner acknowledgement.

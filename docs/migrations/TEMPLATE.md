# Migration guide: vX.Y.Z → vA.B.C

> Copy this template when publishing a release that changes consumer-visible contracts,
> lifecycle rules, or required conformance.

## Summary

- **From:** X.Y.Z
- **To:** A.B.C
- **Impact:** patch | minor | major
- **Breaking:** yes | no

## Changed artifacts

| ID | Change | Action required |
| --- | --- | --- |
| CONTRACT-NNN | … | … |
| EVENT-NNN | … | … |
| SPEC-NNN | … | … |

## Field-level notes

Describe added optional fields, removed required fields, renames, and enum changes.

## Consumer checklist

- [ ] Bump `platform_spec.version` in the conformance manifest.
- [ ] Update schema `$id` pins / package dependency.
- [ ] Re-validate produced events against the new schemas.
- [ ] Replay the Community AI Lab fixture successfully.
- [ ] Record migration completion in the implementation repository.

## Rollback

Describe how to remain on the prior pin if migration cannot complete within the deprecation window.

---
id: ADR-011
title: Contract Evolution Policy
version: 1.0.0
status: accepted
authority: normative
owner: Platform Architecture
date: "2026-08-03"
related_specs:
- SPEC-007
- SPEC-012
- SPEC-015
---

# ADR-011: Contract Evolution Policy

| Status | Accepted |
| --- | --- |
| Date | 2026-08-03 |
| Related specs | SPEC-007, SPEC-012, SPEC-015 |

## Context

Cross-boundary contracts are consumed by independent repositories. Ad-hoc field changes and silent lifecycle edits create incompatible producers and unverifiable history. The platform needs a single evolution policy that validators and release packaging can enforce.

## Decision

1. Contract and event schema evolution follow [SPEC-015](../specs/SPEC-015-compatibility-and-evolution.md) and [SPEC-012](../specs/SPEC-012-versioning.md).
2. Every schema document keeps an immutable `$id` that embeds its version; new versions get new `$id` values.
3. Breaking contract changes require: MAJOR platform version assessment, an ADR when architectural, owner approval, at least one consumer reviewer, a migration guide, and dual-publish or deprecation window as specified in SPEC-015.
4. `additionalProperties: false` remains the default for public contracts so unknown producer fields fail closed at the boundary.
5. Executable validation (`validation/validate_all.py`) and release packages are part of the evolution control plane: invalid examples, missing owners, and non-canonical lifecycle stages cannot merge unnoticed.

## Consequences

- Producers gain predictable rules for additive fields.
- Consumers can pin exact releases and schema `$id` values.
- Evolution is slower than undocumented changes, by design.
- Emergency security patches may shorten deprecation windows under documented governance exception, but cannot omit migration notes after the fact.

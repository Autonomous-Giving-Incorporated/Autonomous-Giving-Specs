---
id: ADR-010
version: 1.1.0
authority: normative
owner: Platform Architecture
date: "2026-08-03"
title: Capability Independence
status: accepted
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-014
- SPEC-020
---

# ADR-010: Capability Independence

| Status | Accepted |
| --- | --- |
| Date | 2026-08-03 |
| Related specs | SPEC-002A, SPEC-006, SPEC-014, SPEC-020 |

## Context

Capabilities must interoperate without redistributing platform responsibility. Treating each capability as a mandatory separately deployed service creates unnecessary operational complexity for the MVP and blurs the line between logical architecture and physical deployment.

## Decision

1. Maintain **capability independence** through owned contracts and the responsibility boundaries in [SPEC-006](../specs/SPEC-006-capability-boundaries.md).
2. Default implementation shape is a **modular monolith** ([SPEC-002A](../specs/SPEC-002A-architectural-principles.md), [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md) Profile B).
3. Extracting a capability into a separate deployable is an operational choice, not a new platform capability.
4. Future capability admission follows [SPEC-014](../specs/SPEC-014-future-capabilities.md).

## Consequences

Capability count may grow; platform invariants do not. Deployment topology may change without changing contract ownership or lifecycle. Distributed infrastructure remains optional.

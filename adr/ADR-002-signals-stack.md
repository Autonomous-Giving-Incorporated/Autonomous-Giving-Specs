---
id: ADR-002
version: 1.1.0
authority: normative
owner: Platform Architecture
date: '2026-08-15'
title: Platform Canon
status: accepted
related_specs:
- SPEC-001
- SPEC-004
- SPEC-005
---

# ADR-002: Platform Canon

| Status | Accepted |
| --- | --- |
| Date | 2026-08-15 |
| Related specs | SPEC-001, SPEC-004, SPEC-005 |

## Context

The ecosystem requires a single source of authority for terminology, lifecycle, and cross-boundary definitions. Product repositories must not redefine Need, Allocation, Evidence, or Impact.

## Decision

Adopt the [Constitution](../CONSTITUTION.md), [glossary](../glossary/README.md), and canonical lifecycle in [SPEC-005](../specs/SPEC-005-lifecycle.md) as the platform canon. Implementations link to this repository rather than redefining platform concepts.

Notification, TimelineEvent, and ImpactNotice are projections, not alternate stages. AGI Control Plane is Autonomous Giving’s edge, not a lifecycle stage and not a fourth capability.

## Consequences

Consumers pin a Specs release. This ADR does not invent a tag. Vocabulary changes require SPEC-004 / glossary amendment.

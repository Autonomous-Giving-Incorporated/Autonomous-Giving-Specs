---
id: ADR-010
version: 1.0.0
authority: normative
owner: Platform Architecture
date: '2026-08-03'
title: Future Services
status: proposed
related_specs:
- SPEC-006
- SPEC-014
---

# ADR-010: Service Independence

| Status | Proposed |
| --- | --- |
| Date | 2026-08-03 |
| Related specs | SPEC-006, SPEC-014 |

## Context

Services must interoperate without redistributing platform responsibility.

## Decision

Maintain service independence through owned contracts and the responsibility boundaries in SPEC-006.

## Consequences

Service count may change; platform invariants do not. Future service admission follows SPEC-014.

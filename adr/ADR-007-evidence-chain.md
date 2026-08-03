---
id: ADR-007
version: 1.0.0
authority: normative
owner: Platform Architecture
date: '2026-08-03'
title: Evidence Chain
status: accepted
related_specs:
- SPEC-004
- SPEC-005
---

# ADR-007: Evidence Chain

| Status | Accepted |
| --- | --- |
| Date | 2026-08-03 |
| Related specs | SPEC-001, SPEC-004, SPEC-006 |

## Context

Impact claims need inspectable provenance.

## Decision

Represent evidence, receipts, and verification as immutable, attributable records linked to an allocation.

## Consequences

Corrections are additive and no service may alter historical evidence.

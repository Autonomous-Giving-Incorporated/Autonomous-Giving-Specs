---
id: ADR-006
version: 1.0.0
authority: normative
owner: Platform Architecture
date: '2026-08-03'
title: Human Approval
status: accepted
related_specs:
- SPEC-001
- SPEC-004
---

# ADR-006: Human Approval

| Status | Accepted |
| --- | --- |
| Date | 2026-08-03 |
| Related specs | SPEC-001, SPEC-004 |

## Context

The MVP must preserve human authority over allocation decisions.

## Decision

Require an explicit approval record before an allocation is created.

## Consequences

Automation may prepare recommendations but cannot allocate.

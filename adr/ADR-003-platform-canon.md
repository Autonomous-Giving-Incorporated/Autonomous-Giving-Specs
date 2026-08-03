---
id: ADR-003
version: 1.0.0
authority: normative
owner: Platform Architecture
date: '2026-08-03'
title: Signals Stack
status: accepted
related_specs:
- SPEC-003
- SPEC-004
- SPEC-005
---

# ADR-003: Signals Stack

| Status | Accepted |
| --- | --- |
| Date | 2026-08-03 |
| Related specs | SPEC-003, SPEC-004, SPEC-005 |

## Context

Observed information and evaluative judgement have different provenance and reliability.

## Decision

Model signals as immutable observations; derive opportunities and recommendations separately.

## Consequences

Consumers can evaluate source quality independently of recommendation policy.

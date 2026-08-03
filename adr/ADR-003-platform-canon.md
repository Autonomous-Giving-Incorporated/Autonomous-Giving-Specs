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

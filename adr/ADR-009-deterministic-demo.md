---
id: ADR-009
version: 1.1.0
authority: normative
owner: Platform Architecture
date: '2026-08-15'
title: Deterministic Demo
status: accepted
related_specs:
- SPEC-007
- SPEC-008
- SPEC-011
---

# ADR-009: Deterministic Demo

| Status | Accepted |
| --- | --- |
| Date | 2026-08-15 |
| Related specs | SPEC-007, SPEC-008, SPEC-011 |

## Context

Live demos obscure whether the system's proof chain works. A live tenant, live every.org pointing, or live Stripe charge cannot be the specification proof.

## Decision

Adopt **Community AI Lab** with fixed synthetic artifacts under `demo/community-ai-lab/` as the canonical demonstration ([SPEC-011](../specs/SPEC-011-demo-specification.md)). Amounts and IDs come from `scenario.json` (2500 USD). Hacker Dojo remains a separate routing fixture, not this demo.

The demo tracks a synthetic gift; it does not process a donation. ImpactNotice is skipped when no contactable donor exists.

## Consequences

Implementations can demonstrate the same lifecycle without external dependencies. `python3 validation/validate_all.py` proves the fixture. Pin-a-release and READY remain operator-owned.

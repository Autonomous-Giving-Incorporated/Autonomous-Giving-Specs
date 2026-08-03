---
id: SPEC-003
title: Signals Stack
version: 1.0.0
status: proposed
authority: normative
owner: Fund Intel
related_specs:
- SPEC-004
- SPEC-005
related_adrs:
- ADR-003
related_contracts:
- CONTRACT-001
- CONTRACT-002
---

# SPEC-003: Signals Stack
| Version | 1.0.0 | Owner | Fund Intel | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-004, SPEC-005 | Related ADRs | ADR-003 | Related contracts | CONTRACT-001, CONTRACT-002 |
## Purpose
Define the observation-to-recommendation boundary.
## Scope
Signals, opportunities, and recommendations produced by Fund Intel.
## Requirements
Signals SHALL retain source, observed time, capture time, subject, and confidence. Opportunities group observations; recommendations remain non-authorizing proposals.
## Non-goals
Source connector, scoring, and model implementation are excluded.

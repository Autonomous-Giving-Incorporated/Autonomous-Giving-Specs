---
id: SPEC-003
title: Signals Stack
version: 1.1.0
status: proposed
authority: normative
owner: Fund Intel
related_specs:
- SPEC-004
- SPEC-005
- SPEC-006
- SPEC-002A
related_adrs:
- ADR-003
related_contracts:
- CONTRACT-001
- CONTRACT-002
---

# SPEC-003: Signals Stack
| Version | 1.1.0 | Owner | Fund Intel | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-004, SPEC-005, SPEC-006 | Related ADRs | ADR-003 | Related contracts | CONTRACT-001, CONTRACT-002 |

## Purpose
Define the observation-to-recommendation **logical** boundary owned by the Fund Intel capability.

## Scope
Signals, opportunities, and recommendations produced under Fund Intel responsibility. This is a logical architecture specification only.

## Requirements
1. Signals SHALL retain source, observed time, capture time, subject, and confidence.
2. Opportunities group observations; recommendations remain non-authorizing proposals.
3. Fund Intel MAY run as a module inside a modular monolith or as a separately deployed unit; neither choice changes contract ownership.
4. No event bus, stream processor, or network hop is required by this specification.

## Non-goals
Source connectors, scoring models, model training, transport, and deployment topology are excluded.

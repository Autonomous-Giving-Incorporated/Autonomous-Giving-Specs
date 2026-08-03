---
id: SPEC-014
title: Future Services
version: 1.0.0
status: proposed
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-006
- SPEC-013
related_adrs:
- ADR-010
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

# SPEC-014: Future Services
| Version | 1.0.0 | Owner | Platform Architecture | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-006, SPEC-013 | Related ADRs | ADR-010 | Related contracts | CONTRACT-001–007 |
## Purpose
Define admission rules for future ecosystem services.
## Scope
Services beyond Fund Intel, Autonomous Giving, and Impact Relay.
## Requirements
A new service SHALL own one responsibility, declare consumed and produced artifacts, avoid forbidden responsibilities, and obtain an ADR for a new cross-boundary contract or lifecycle change.
## Non-goals
This does not require microservices or a specific deployment form.

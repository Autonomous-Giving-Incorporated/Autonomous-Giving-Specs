---
id: SPEC-014
title: Future Capabilities
version: 1.1.0
status: proposed
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-013
- SPEC-020
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

# SPEC-014: Future Capabilities
| Version | 1.1.0 | Owner | Platform Architecture | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-006, SPEC-013 | Related ADRs | ADR-010 | Related contracts | CONTRACT-001–007 |

## Purpose
Define admission rules for future platform **capabilities** beyond Fund Intel, Autonomous Giving, and Impact Relay.

## Scope
New logical responsibilities that exchange platform contracts or alter lifecycle participation.

## Requirements
1. A new capability SHALL own one responsibility, declare consumed and produced artifacts, and avoid forbidden responsibilities of existing capabilities.
2. A new cross-boundary contract or lifecycle change requires an ADR.
3. Admission of a capability is independent of whether it is co-located in a modular monolith or extracted later.
4. Extracting an existing capability into a separate deployable does not create a new capability; it changes deployment only.

## Non-goals
This does not require distributed processes, orchestrators, or a specific deployment form.

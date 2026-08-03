---
id: SPEC-004
title: Domain Model
version: 1.0.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs: []
related_adrs:
- ADR-002
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

# SPEC-004: Domain Model
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | Constitution | Related ADRs | ADR-002 | Related contracts | CONTRACT-001–007 |
## Purpose
Freeze platform concepts and their relationships.
## Scope
The canonical terms identified in the [glossary](../glossary/README.md).
## Requirements
Artifacts SHALL use glossary identifiers and SHALL NOT introduce synonyms or duplicate concepts. `TimelineEvent` and `Notification` are named, distinct concepts.
## Non-goals
This is not a database or object model.

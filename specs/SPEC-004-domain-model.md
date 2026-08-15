---
id: SPEC-004
title: Domain Model
version: 1.2.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-029
- SPEC-030
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
- CONTRACT-013
---

# SPEC-004: Domain Model
| Version | 1.2.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | Constitution | Related ADRs | ADR-002 | Related contracts | CONTRACT-001–007 |
## Purpose
Freeze platform concepts and their relationships.
## Scope
The canonical terms identified in the [glossary](../glossary/README.md).
## Requirements
Artifacts SHALL use glossary identifiers and SHALL NOT introduce synonyms or duplicate concepts. `TimelineEvent`, `Notification`, and `ImpactNotice` are named, distinct projections. Product UI MAY label Evidence as proof; the canonical term remains Evidence. Gift Summary, Pot, Donation-source Connector, and Donation Link are tracking terms and do not replace Allocation or Receipt. AGI Control Plane is Autonomous Giving’s edge, not a fourth capability or a lifecycle stage.

`Mission Graph` is a projection over canonical records, not a graph-shaped system of record or lifecycle. `Learning Feedback` is a provenance-preserving relationship from verified or explicitly classified evidence to a new Signal; it is not a lifecycle stage. `Mission Intelligence` is the evidence-bounded interpretation of mission artifacts. A `Mission Intelligence Metric` is a versioned derived artifact and never authority. An AGI control-plane display does not imply ownership of a downstream record. These terms SHALL use the glossary identifiers defined for them and SHALL NOT introduce a duplicate synonym set.
## Non-goals
This is not a database or object model.

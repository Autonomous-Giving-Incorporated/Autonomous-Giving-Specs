---
id: SPEC-008
title: Events
version: 1.0.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-005
- SPEC-007
related_adrs:
- ADR-003
- ADR-007
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

# SPEC-008: Events
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-005, SPEC-007 | Related ADRs | ADR-003, ADR-007 | Related contracts | CONTRACT-001–007 |
## Purpose
Define immutable lifecycle publication semantics.
## Scope
EVENT-001 through EVENT-010 and their envelope.
## Requirements
Every event SHALL declare producer, consumers, payload, schema, ordering, idempotency, stage, example, and version history. Consumers SHALL deduplicate on `eventId`.
## Non-goals
Event transport and broker selection are excluded.

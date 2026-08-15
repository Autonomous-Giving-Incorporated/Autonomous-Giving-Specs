---
id: SPEC-008
title: Events
version: 1.2.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-002A
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
- CONTRACT-013
---

# SPEC-008: Events
| Version | 1.2.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-005, SPEC-007 | Related ADRs | ADR-003, ADR-007 | Related contracts | CONTRACT-001–007, CONTRACT-013 |

## Purpose
Define immutable lifecycle **publication semantics** (what happened, in what order, with which identity).

## Scope
EVENT-001 through EVENT-011 and their envelope.

## Requirements
1. Every event SHALL declare producer, consumers, payload, schema, ordering, idempotency, stage, example, and version history.
2. Consumers SHALL deduplicate on `eventId`.
3. Events describe platform behavior. They do **not** require asynchronous infrastructure.
4. Implementations MAY record or deliver events by synchronous invocation, database persistence, a work queue, or a broker. All remain conformant when payloads and ordering invariants hold.
5. No Kafka, NATS, or other broker is mandated.

## Non-goals
Event transport technology, broker selection, and at-least-once vs exactly-once infrastructure guarantees beyond idempotent `eventId` handling are excluded.

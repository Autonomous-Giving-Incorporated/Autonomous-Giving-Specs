# Consuming this specification repository

This guide applies to Fund Intel, Impact Relay, and every future platform implementation repository.

## Pin an authoritative release

Each consuming repository must declare the exact specification release it implements, for example `Autonomous-Giving-Specs v1.0.0`. Do not depend on an unpinned branch for a production contract. Record the release in the implementation repository’s architecture or integration index.

## Replace duplicate documentation

Keep implementation-specific material (endpoints, deployment, source layout, operational runbooks) locally. Replace duplicated definitions of platform lifecycle, domain terms, cross-boundary contracts, or architectural decisions with a short link to the stable artifact in this repository. Local documentation may describe how a service satisfies a requirement; it must not redefine it.

## Implement the contract boundary

1. Identify the produced and consumed events in the [traceability matrix](traceability.md).
2. Validate outgoing contract payloads against the linked JSON Schema and reject or quarantine malformed inbound messages.
3. Preserve `eventId`, `correlationId`, `schemaVersion`, and aggregate identifiers through asynchronous boundaries.
4. Enforce the lifecycle invariants in [SPEC-004](../specs/SPEC-004-event-lifecycle.md), especially human approval before allocation and append-only evidence history.
5. Include the exact SPEC, CONTRACT, EVENT, and schema version in integration-test evidence.

## Change coordination

Consumers propose changes here first when the change affects shared authority. Contract or lifecycle changes require a consuming-repository reviewer. Consumers prepare compatibility work before a breaking release is accepted, following [SPEC-010](../specs/SPEC-010-versioning.md).

## Minimum consumer declaration

An implementation repository should maintain a small declaration equivalent to:

```text
Platform specification release: v1.0.0
Produced: EVENT-002, EVENT-003
Consumed: EVENT-004, EVENT-005
Contract schemas: opportunity@1.0.0, recommendation@1.0.0
```

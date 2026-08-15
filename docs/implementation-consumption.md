# Consuming this specification repository

This guide applies to Fund Intel, Impact Relay, Autonomous Giving Incorporated, and every future platform implementation repository.

## Pin an authoritative release

Each consuming repository must declare the exact specification release it implements, for example `Autonomous-Giving-Specs v1.0.0`. Do not depend on an unpinned branch for a production contract. Record the release in the implementation repository’s architecture or `platform-spec/conformance.yml`.

## Replace duplicate documentation

Keep implementation-specific material (endpoints, deployment, source layout, operational runbooks) locally. Replace duplicated definitions of platform lifecycle, domain terms, cross-boundary contracts, or architectural decisions with a short link to the stable artifact in this repository. Local documentation may describe how a **capability** satisfies a requirement; it must not redefine it.

## Implement the capability boundary

1. Identify the produced and consumed events in the [traceability matrix](traceability.md).
2. Validate outgoing contract payloads against the linked JSON Schema and reject or quarantine malformed inbound messages.
3. Preserve `eventId`, `correlationId`, `schemaVersion`, and aggregate identifiers across module or process boundaries.
4. Enforce the lifecycle invariants in [SPEC-005](../specs/SPEC-005-lifecycle.md), especially human approval before allocation and append-only evidence history.
5. Include the exact SPEC, CONTRACT, EVENT, and schema version in integration-test evidence.
6. Prefer a Cloudflare + Supabase modular monolith ([implementation guidance](implementation-guidance.md), [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)); treat deployment topology as irrelevant to conformance ([SPEC-013](../specs/SPEC-013-repository-conformance.md)). [ADR-012](../adr/ADR-012-render-first-platform.md) is superseded.

## Change coordination

Consumers propose changes here first when the change affects shared authority. Contract or lifecycle changes require a consuming-repository reviewer. Consumers prepare compatibility work before a breaking release is accepted, following [SPEC-012](../specs/SPEC-012-versioning.md).

## Minimum consumer declaration

An implementation repository should maintain a declaration equivalent to:

```yaml
platform_spec:
  repository: scrimshawlife-ctrl/Autonomous-Giving-Specs
  version: 1.0.0
service:
  id: fund-intel   # capability id
  role: intelligence
implements:
  specs: [SPEC-001, SPEC-003, ...]
  contracts:
    produces: [CONTRACT-001]
  events:
    produces: [EVENT-002]
```

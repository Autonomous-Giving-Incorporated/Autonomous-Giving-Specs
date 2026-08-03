---
id: SPEC-015
title: Compatibility and Evolution
version: 1.0.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-007
- SPEC-008
- SPEC-012
- SPEC-013
related_adrs:
- ADR-001
- ADR-011
related_contracts:
- CONTRACT-001
- CONTRACT-002
- CONTRACT-003
- CONTRACT-004
- CONTRACT-005
- CONTRACT-006
- CONTRACT-007
---

# SPEC-015: Compatibility and Evolution
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-007, SPEC-008, SPEC-012 | Related ADRs | ADR-001, ADR-011 | Related contracts | CONTRACT-001–007 |

## Purpose
Define how platform contracts, events, schemas, and lifecycle authority may evolve without silently breaking consumers.

## Scope
All normative payload schemas, event definitions, lifecycle stages, and platform releases. Applies to Fund Intel, Autonomous Giving Incorporated, Impact Relay, and future services.

## Requirements

### Compatibility classes
1. A change is **backward-compatible** when every previously valid producer payload remains valid and every previously required consumer interpretation remains true.
2. A change is **breaking** when a previously valid payload becomes invalid, a previously required field is removed or renumbered in meaning, a lifecycle ordering invariant changes, or a required event is removed or renamed without a dual-publish window.
3. Platform release impact SHALL follow [SPEC-012](SPEC-012-versioning.md): MAJOR for breaking, MINOR for backward-compatible authority additions, PATCH for clarifications only.

### Schema field rules
1. New **optional** properties MAY be added in a MINOR release.
2. New **required** properties require MAJOR unless a dual-write window publishes both old and new schemas under distinct `$id` versions and consumers opt in.
3. Removing a property, tightening a type, narrowing an enum, or changing a format constraint is breaking (MAJOR).
4. Widening an enum or relaxing a constraint is backward-compatible (MINOR) only when prior values remain valid.
5. Property names and semantic meaning are stable within a major schema `$id` line; renames are breaking.

### Unknown-field handling
1. Producers of a given contract version SHALL NOT emit fields undefined by that version’s schema when `additionalProperties` is `false`.
2. Consumers SHALL ignore unknown fields only when consuming a **newer minor** schema they have not yet implemented, and only if the envelope and known required fields validate.
3. Consumers MUST NOT drop or rewrite unknown fields when forwarding an authoritative event for audit replay.

### Event versioning
1. Each event definition carries a semantic `version` in frontmatter and a payload schema `$id` including major.minor.patch.
2. `eventType` names are stable identifiers; renaming an `eventType` is breaking.
3. Envelope fields in `event-envelope.json` follow the same compatibility rules as contracts.
4. Idempotency keys (`eventId`) remain unique and stable across replays of the same logical occurrence.

### Deprecation and supersession
1. Deprecated artifacts remain published for at least one MINOR platform release after deprecation is declared, unless a security emergency requires faster removal (see governance emergency process).
2. A deprecated artifact SHALL name its successor in frontmatter or prose (`superseded_by` / successor ID).
3. Superseded artifacts remain in the repository for history; they MUST NOT be deleted solely because authority moved.
4. Consumers SHOULD migrate before the deprecation window ends; after removal in a MAJOR release, non-conforming producers FAIL validation.

### Schema supersession
1. Schema `$id` values are immutable for a given version string.
2. A new schema version receives a new `$id` (version segment bump). Prior `$id` documents remain available in tagged releases.
3. Contract documents SHALL point at exactly one current schema path per contract version line.

### Lifecycle evolution
1. Inserting, removing, reordering, or renaming a canonical lifecycle stage is breaking (MAJOR) and requires an ADR plus Constitution amendment when it conflicts with the Constitution sequence.
2. Adding a **projection** (such as Notification or TimelineEvent) that does not alter the canonical stage sequence MAY be MINOR.
3. Rules “Approval before Allocation”, “Evidence before Verification”, and “Notification only after verified impact path” are invariants; weakening them is breaking.

### Replay compatibility
1. A consumer that stores events MUST be able to re-validate historical payloads against the schema version recorded at produce time (`schemaVersion` / `$id`).
2. Replay MUST preserve `eventId`, ordering keys declared by the event, and `allocationId` continuity.
3. Migrations that rewrite stored history require a documented MAJOR migration and dual-read support until the window closes.

### Consumer tolerance and conformance
1. Implementations declare a pinned platform release per [SPEC-013](SPEC-013-repository-conformance.md).
2. Producers MUST validate outbound payloads against the pinned schemas before publish.
3. Consumers MUST reject payloads that fail the pinned schema for types they claim to implement.
4. Optional and experimental artifacts create no compatibility obligation until promoted.

### Major-version migration
1. Every MAJOR release SHALL publish a migration guide under `docs/migrations/` using the template.
2. Migration guides enumerate added, changed, deprecated, and removed stable IDs and consumer actions.
3. Release notes and checksummed packages are the pin targets; consumers MUST NOT treat `main` as an immutable pin.

## Non-goals
This specification does not define transport protocols, broker topology, or implementation release calendars beyond pin and migration obligations.

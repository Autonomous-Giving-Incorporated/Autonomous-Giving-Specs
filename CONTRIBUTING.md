# Contributing to the platform canon

## Change types

Use a new or amended SPEC for normative platform requirements; an ADR for a durable architectural choice; a contract and JSON Schema for a cross-boundary payload; an event document for lifecycle publication behavior. Avoid placing implementation detail, vendor setup, or application source here.

Material design changes follow the [RFC process](docs/rfc-process.md). Compatibility rules are in [SPEC-015](specs/SPEC-015-compatibility-and-evolution.md).

## Submission requirements

1. State the affected stable IDs and whether the change is major, minor, or patch under [SPEC-012](specs/SPEC-012-versioning.md) and [SPEC-015](specs/SPEC-015-compatibility-and-evolution.md).
2. Update the glossary when introducing or changing a domain term.
3. Update inbound and outbound references, diagrams, examples, events, and schemas together.
4. Run `python validation/validate_all.py` and ensure `result` is `PASS`. See [validation](docs/validation.md).
5. Obtain owner approval and an implementation-consumer review for contract, lifecycle, or security changes (reviewer matrix in [rfc-process.md](docs/rfc-process.md)).
6. For MAJOR changes, add a migration guide under `docs/migrations/`.

## Status lifecycle

```text
draft → proposed → accepted → deprecated → superseded
```

Frontmatter uses lowercase status values. Never delete an accepted ADR solely because the decision changed—mark it `superseded` and link the successor.

## Normative language

Requirements use RFC 2119 keywords (**MUST**, **SHALL**, **SHOULD**, **MAY**) as defined in [docs/rfc-process.md](docs/rfc-process.md).

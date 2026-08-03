# Contributing to the platform canon

## Change types

Use a new or amended SPEC for normative platform requirements; an ADR for a durable architectural choice; a contract and JSON Schema for a cross-boundary payload; an event document for lifecycle publication behavior. Avoid placing implementation detail, vendor setup, or application source here.

## Submission requirements

1. State the affected stable IDs and whether the change is major, minor, or patch under [SPEC-012](specs/SPEC-012-versioning.md).
2. Update the glossary when introducing or changing a domain term.
3. Update inbound and outbound references, diagrams, examples, events, and schemas together.
4. Complete [the validation checklist](docs/validation.md). CI blocks broken Markdown links, invalid JSON schema syntax, and incomplete core artifact inventories.
5. Obtain owner approval and an implementation-consumer review for contract or lifecycle changes.

## Status lifecycle

Use `Proposed` while seeking review, `Accepted` once authoritative, `Deprecated` when retained only for migration, and `Superseded` when replaced by a named successor. Never delete an accepted ADR solely because the decision changed.

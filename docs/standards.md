# Documentation standards

## Markdown and naming

Use ATX headings, sentence-case titles, relative links, and stable identifiers: `SPEC-NNN`, `ADR-NNN`, `EVENT-NNN`, and `CONTRACT-NNN`. File names are lowercase kebab-case. Use canonical glossary terms exactly.

## Normative content

Every SPEC contains version, owner, status, purpose, requirements, non-goals, rationale, dependencies, related ADRs, related contracts, and references. Requirements use unambiguous “must” or “must not” language. Every public contract declares one owner and a JSON Schema.

## Diagrams and examples

Store Mermaid source in `diagrams/`; do not commit opaque diagram-only artifacts. Examples must be internally consistent, non-production data, and use contract field names.

## Ownership and review

The named owner approves changes. Contract or lifecycle changes also require a consumer review. Breaking changes require an ADR and major version assessment under [SPEC-012](../specs/SPEC-012-versioning.md).

## Cross references

Link to the stable artifact, not a branch or line number. Update inbound and outbound references with a renamed or superseded artifact.

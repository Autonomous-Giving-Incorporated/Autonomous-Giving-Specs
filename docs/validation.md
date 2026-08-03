# Validation checklist

Run before review and release.

- [ ] Every SPEC links to existing dependencies, ADRs, contracts, and references.
- [ ] Every SPEC contains purpose, scope, requirements, non-goals, owner, version, status, dependencies, related ADRs, and related contracts.
- [ ] Every normative artifact identifies the [Constitution](../CONSTITUTION.md) as the governing platform authority.
- [ ] Every ADR references at least one SPEC and has Context, Decision, Status, and Consequences.
- [ ] Every EVENT links to its contract and declares producer, consumers, schema, payload, idempotency, stage, ordering, and example.
- [ ] Every CONTRACT has exactly one owner, schema, version, producer, consumer, example, and validation rules.
- [ ] JSON Schema files parse and use Draft 2020-12.
- [ ] Glossary terms are used consistently; duplicate terms or synonyms are reconciled.
- [ ] Schema documents have stable `SCHEMA-NNN` identifiers and point to the appropriate contract.
- [ ] Event definitions include version history and no lifecycle alternative is introduced.
- [ ] Consumers declare a pinned platform release and conformance level under [SPEC-013](../specs/SPEC-013-repository-conformance.md).
- [ ] Internal Markdown links resolve; link checking fails the release if any are broken.
- [ ] Changed normative behavior has a version assessment and, when architectural, an ADR.

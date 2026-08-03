# Validation checklist

Run before review and release.

- [ ] Every SPEC links to existing dependencies, ADRs, contracts, and references.
- [ ] Every ADR references at least one SPEC and has Context, Decision, Status, and Consequences.
- [ ] Every EVENT links to its contract and declares producer, consumers, schema, payload, idempotency, stage, ordering, and example.
- [ ] Every CONTRACT has exactly one owner, schema, version, producer, consumer, example, and validation rules.
- [ ] JSON Schema files parse and use Draft 2020-12.
- [ ] Glossary terms are used consistently; duplicate terms or synonyms are reconciled.
- [ ] Internal Markdown links resolve; link checking fails the release if any are broken.
- [ ] Changed normative behavior has a version assessment and, when architectural, an ADR.

# Repository governance

## Authority

This repository is the authoritative source for normative platform specifications, contracts, events, schemas, architecture, ADRs, glossary terms, and demo behavior. The **release tag** is the authoritative version boundary consumers pin.

The [Constitution](../CONSTITUTION.md) is the highest-order normative document. The [RFC process](rfc-process.md) governs material design change. Evolution rules live in [SPEC-015](../specs/SPEC-015-compatibility-and-evolution.md).

## Roles

| Role | Responsibility |
| --- | --- |
| Platform Architecture | Maintains canon, lifecycle, versioning, cross-cutting review, release designation. |
| Domain owner | Owns the artifact named in its metadata and approves domain correctness. |
| Consumer reviewer | Confirms compatibility and implementation impact. |
| Maintainer | Merges changes only after required reviews and validation pass. |
| Release owner | Tags platform releases (`vMAJOR.MINOR.PATCH`) after validation and notes. |

## Artifact status transitions

Normative SPECs, ADRs, contracts, and events use:

```text
draft → proposed → accepted → deprecated → superseded
```

| Status | Meaning |
| --- | --- |
| `draft` | Work in progress; not review-ready; not platform authority |
| `proposed` | Review candidate; not yet binding |
| `accepted` | Normative authority for the current major line |
| `deprecated` | Still published for migration; successor named |
| `superseded` | Replaced; retained for history |

Rules:

1. `accepted` artifacts change only through reviewed amendment or a superseding artifact.
2. Never delete an `accepted` ADR solely because the decision changed; mark `superseded` and link the successor.
3. Status values in YAML frontmatter are lowercase; prose tables may use title case.

## Decision rules

Ambiguity is resolved by the artifact owner, with Platform Architecture deciding cross-domain conflicts. Emergency clarifications can be released as patches under the [emergency process](rfc-process.md#emergency-correction-process); they must not silently alter required behavior without disclosure.

## Normative versus informative

| Normative | Informative |
| --- | --- |
| Constitution, accepted SPECs/ADRs | Roadmap, narrative demos (except SPEC-011 fixtures) |
| Contracts, events, schemas, glossary | Architecture overviews that restate specs |
| Executable validation rules | CONTRIBUTING prose without MUST/SHALL |

Use RFC 2119 keywords as defined in [rfc-process.md](rfc-process.md).

## Review record

Pull requests must name:

1. Affected stable IDs
2. Ownership
3. Version impact (MAJOR / MINOR / PATCH)
4. Validation evidence (`validate_all.py` PASS)
5. Consumer impact and migration notes when breaking

Review comments become part of the rationale when they materially constrain platform behavior.

## Required reviewers

See the reviewer matrix in [rfc-process.md](rfc-process.md#required-reviewers).

## Release authority

See [release-process.md](release-process.md) and [rfc-process.md](rfc-process.md#release-authority).

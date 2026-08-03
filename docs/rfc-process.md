# RFC process

RFCs are the proposal path for material changes to platform authority before SPECs, ADRs, contracts, or schemas are accepted.

## When an RFC is required

Open an RFC when a change:

- Alters a required contract field, event, or lifecycle invariant
- Introduces a new cross-boundary contract or service responsibility
- Changes security, privacy, or identity norms
- Requires a MAJOR version assessment under [SPEC-012](../specs/SPEC-012-versioning.md)
- Needs multi-owner design discussion before drafting normative text

Patch-level clarifications and typo fixes do not require an RFC.

## RFC lifecycle

```text
draft → proposed → accepted → implemented → closed
                 ↘ withdrawn
                 ↘ rejected
```

| Status | Meaning |
| --- | --- |
| `draft` | Author workspace; not review-ready |
| `proposed` | Ready for owner and consumer review |
| `accepted` | Design approved; normative artifacts may land |
| `implemented` | Accepted design reflected in merged SPECs/ADRs/schemas |
| `withdrawn` | Author abandoned |
| `rejected` | Review declined with recorded rationale |
| `closed` | Terminal state after implemented, withdrawn, or rejected |

RFCs live as pull-request descriptions or documents under `docs/rfcs/` named `RFC-NNN-short-title.md` when durable discussion must outlive the PR.

## Required reviewers

| Artifact class | Required reviewers |
| --- | --- |
| SPEC (cross-cutting) | Platform Architecture + one consumer implementation |
| SPEC (domain) | Domain owner + Platform Architecture |
| CONTRACT / EVENT / SCHEMA | Owner service + at least one consuming service |
| ADR | Platform Architecture; domain owner when domain-specific |
| Security/privacy SPECs | Platform Architecture + owner of affected boundary |
| MAJOR breaking change | Platform Architecture + all directly affected service owners |

Maintainers MUST NOT merge without the required approvals and a green `python validation/validate_all.py`.

## Normative language

Use RFC 2119 key words in requirements prose:

| Keyword | Meaning |
| --- | --- |
| **MUST** / **SHALL** | Absolute requirement |
| **MUST NOT** / **SHALL NOT** | Absolute prohibition |
| **SHOULD** | Recommended unless valid reasons exist |
| **SHOULD NOT** | Discouraged |
| **MAY** | Optional |

Normative documents are SPECs, accepted ADRs, contracts, events, schemas, the Constitution, and the glossary. Diagrams, demos, roadmaps, and narrative docs are informative unless they explicitly restate a normative rule.

## Breaking-change approval

Breaking changes MUST:

1. Record version impact (MAJOR) per SPEC-012 and SPEC-015
2. Include or reference an ADR when architectural
3. Provide `docs/migrations/` guide from prior release
4. Obtain reviewers in the table above
5. Update examples, demo fixtures, conformance manifests, and generated indexes in the same change set

## Emergency correction process

When a normative error creates security exposure or data-loss risk:

1. Platform Architecture may land a patch-level clarification or fix with abbreviated review (minimum: owner + one maintainer).
2. The PR MUST label `emergency` and describe residual risk.
3. Within five business days, a follow-up MUST complete full consumer notification, changelog entry, and any migration notes.
4. Emergency fixes MUST NOT silently expand scope beyond the incident.

## Release authority

| Action | Authority |
| --- | --- |
| Merge to `main` | Maintainer after required reviews + validation |
| Tag `vMAJOR.MINOR.PATCH` | Release owner designated by Platform Architecture |
| Publish GitHub release package | Automated release workflow on tag |
| Amend Constitution | MAJOR platform release only |

The release tag—not the floating `main` branch—is what consumers pin.

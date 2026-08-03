# Repository governance

## Authority

This repository is the authoritative source for normative platform specifications, contracts, events, schemas, architecture, ADRs, glossary terms, and demo behavior. The release tag is the authoritative version boundary.

## Roles

| Role | Responsibility |
| --- | --- |
| Platform Architecture | Maintains canon, lifecycle, versioning, and cross-cutting review. |
| Domain owner | Owns the artifact named in its metadata and approves domain correctness. |
| Consumer reviewer | Confirms compatibility and implementation impact. |
| Maintainer | Merges changes only after required reviews and validation pass. |

## Decision rules

An accepted SPEC or ADR changes only through a reviewed amendment or superseding artifact. Ambiguity is resolved by the owner, with Platform Architecture deciding cross-domain conflicts. Emergency clarifications can be released as patches; they must not silently alter required behavior.

## Review record

Pull requests must name affected stable IDs, ownership, version impact, validation evidence, and consumer impact. Review comments become part of the rationale when they materially constrain the resulting platform behavior.

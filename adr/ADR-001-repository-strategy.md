# ADR-001: Repository Strategy

| Status | Accepted |
| --- | --- |
| Date | 2026-08-03 |
| Related specs | SPEC-001, SPEC-010 |

## Context

Platform definitions drift when each implementation repository maintains a local copy.

## Decision

This repository is the versioned, implementation-neutral source for normative platform artifacts. Implementations consume it by release version.

## Consequences

Changes require cross-repository review; duplicated architectural documents should be replaced with links.

---
id: SPEC-020
title: Reference Deployment Profiles
version: 1.0.0
status: accepted
authority: informative
owner: Platform Architecture
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-011
- SPEC-013
related_adrs:
- ADR-001
- ADR-010
related_contracts: []
---

# SPEC-020: Reference Deployment Profiles
| Version | 1.0.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-002A, SPEC-006 | Related ADRs | ADR-001, ADR-010 | Related contracts | None |

## Purpose
Publish **informative** reference deployment profiles so implementers share a clear MVP path without reading distribution into the platform canon.

## Scope
Physical deployment examples only. Logical capabilities remain defined by [SPEC-006](SPEC-006-capability-boundaries.md). These profiles are **examples, not requirements**.

## Authority
This specification is **informative**. Conformance is not conditioned on selecting a profile. Implementations MAY invent other topologies that preserve capabilities, contracts, and lifecycle.

## Profile A — Demo

| Element | Choice |
| --- | --- |
| Frontend | GitHub Pages (or equivalent static host) |
| Data | Static fixtures ([Community AI Lab](../demo/community-ai-lab/)) |
| Backend | None required |
| Secrets | None |
| Infrastructure | None |

Use for narrative demos and deterministic replay without operational systems.

## Profile B — MVP (**recommended**)

```text
GitHub Pages
    ↓
Single Backend (one executable)
    ↓
Modules: Fund Intel | Autonomous Giving | Impact Relay
    ↓
PostgreSQL  +  Object Storage  +  Background Worker
```

| Characteristic | Value |
| --- | --- |
| Executables | Single application process (+ optional worker process) |
| Deployments | Single operational unit |
| Database | One primary PostgreSQL |
| Storage | S3-compatible object storage for evidence binaries |
| Architecture | Modular monolith; capability modules with clear boundaries |
| Orchestration | Not required |
| Event broker | Not required |
| Service mesh | Not required |

Capabilities remain separate **in code**. Deployment remains **unified**.

### Recommended stack (MVP)

| Concern | Recommendation |
| --- | --- |
| Frontend | GitHub Pages |
| Backend | Single application |
| Language | Implementation choice |
| Database | PostgreSQL |
| Storage | S3-compatible |
| Worker | Background process (same codebase or sibling process) |
| Authentication | OIDC when required |

## Profile C — Production

Optional horizontal scaling of the same modular application, optional worker separation, optional multiple instances behind a load balancer. Still one logical system; not a microservices mandate.

## Profile D — Enterprise

Optional extraction of individual capabilities, optional event streaming, optional Kubernetes, optional multi-region. Adopt only with operational justification ([SPEC-002A](SPEC-002A-architectural-principles.md) extraction criteria).

## Evolution path

```text
Phase 1  Modular Monolith (Profile B)
    ↓
Phase 2  Background Workers
    ↓
Phase 3  Extract Individual Capabilities (only if justified)
    ↓
Phase 4  Distributed Platform
    ↓
Phase 5  Enterprise Deployment
```

## Non-goals
This document does not prescribe cloud vendors, IaC tools, or force Profile D. It replaces any implication that distributed infrastructure is the reference platform shape.

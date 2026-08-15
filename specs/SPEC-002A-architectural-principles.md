---
id: SPEC-002A
title: Architectural Principles
version: 1.1.0
status: accepted
authority: normative
owner: Platform Architecture
related_specs:
- SPEC-001
- SPEC-002
- SPEC-006
- SPEC-013
- SPEC-020
- SPEC-021
related_adrs:
- ADR-001
- ADR-003
- ADR-010
- ADR-012
- ADR-013
related_contracts: []
---

# SPEC-002A: Architectural Principles
| Version | 1.1.0 | Owner | Platform Architecture | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | Constitution, SPEC-001, SPEC-002 | Related ADRs | ADR-001, ADR-003, ADR-010, ADR-012, ADR-013 | Related contracts | None |

## Purpose
State foundational architectural principles that separate logical capability from physical deployment. This specification complements [SPEC-002](SPEC-002-platform-principles.md) (platform principles of authority and proof) with **how the platform is structured**, not **how it must be hosted**.

## Scope
All platform specifications, implementation repositories, and reference deployment profiles. Applies to Fund Intel, Autonomous Giving, and Impact Relay as capabilities.

## Requirements

### Capability First
1. Platform structure is expressed as **capabilities** with owned responsibilities and contracts.
2. Fund Intel, Autonomous Giving, and Impact Relay are capabilities, not mandatory deployables.
3. Capability boundaries SHALL be preserved in modular code structure even when co-located.

### Deployment Independence
1. Specifications define capabilities; implementations choose deployment.
2. Logical services SHALL NOT imply separate repositories, containers, databases, Kubernetes, or distributed systems.
3. Modular monolith, modular application, and distributed services may all be conformant.

### Contracts Before Transport
1. Contracts define interfaces and payload meaning.
2. Transport MAY be in-process function or module calls, REST, events, gRPC, or a future protocol.
3. Choosing a transport does not redefine a contract.

### Specification First
1. Shared authority is defined here before product code invents alternate lifecycles or vocabularies.
2. Implementation repositories pin a platform release and declare conformance ([SPEC-013](SPEC-013-repository-conformance.md)).

### Modular Monolith by Default
1. The **recommended MVP** is a modular monolith: one operational unit, one primary database, modular capability packages.
2. Reference deployment profiles are informative examples ([SPEC-020](SPEC-020-reference-deployment-profiles.md)).
3. The **preferred physical realization** of that MVP is Cloudflare + Supabase ([ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)): Workers / Pages, optional Durable Objects and Queues/Cron Triggers, with Supabase Auth, PostgreSQL, and Storage. every.org is the P0 donation-source connector. Stripe is tenant/SaaS billing only if tenants are charged. Resend, OpenAI, and Clerk remain externals only if still required. [ADR-012](../adr/ADR-012-render-first-platform.md) (Render-first) is superseded. Preference is not a conformance mandate.

### Evidence Before Scale
1. Operational complexity (workers, cron, caches, extraction, brokers, orchestration) is justified by measured need, not by architectural fashion.
2. Lifecycle, approval, evidence integrity, and financial reconstructability take precedence over premature distribution.

### Extract Only When Operationally Justified
1. Capability extraction into separately deployable units SHOULD occur only when measurable criteria apply (independent scaling, independent deployment cadence, separate team ownership, operational isolation, or fault isolation).
2. If none apply, the implementation SHOULD remain a modular monolith.

## Non-goals
This specification does not require a single cloud vendor for conformance. Preferred stack choices are informative under ADR-013 (Cloudflare + Supabase). [ADR-012](../adr/ADR-012-render-first-platform.md) is superseded. It does not change lifecycle stages, domain vocabulary, or contract ownership.

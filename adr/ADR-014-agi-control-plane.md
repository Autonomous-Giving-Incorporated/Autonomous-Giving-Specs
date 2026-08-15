---
id: ADR-014
version: 1.0.0
authority: normative
owner: Platform Architecture
date: '2026-08-15'
title: AGI-Owned Control Plane and Secure Cross-Repository Integration
status: proposed
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-016
- SPEC-017
- SPEC-019
- SPEC-024
- SPEC-025
---

# ADR-014: AGI-Owned Control Plane and Secure Cross-Repository Integration

| Status | Proposed |
| --- | --- |
| Date | 2026-08-15 |
| Related specs | SPEC-002A, SPEC-006, SPEC-016, SPEC-017, SPEC-019, SPEC-024, SPEC-025 |
| Related contracts | CONTRACT-008–012 |

## Context

The platform has one shared `client_id` / `tenant_id` boundary across Fund-Intel and Impact Relay. Fund-Intel is the canonical Hacker Dojo reference-tenant implementation, with shared Supabase infrastructure. Impact Relay remains the evidence and impact capability and may use its intended Cloud Run deployment without changing logical ownership.

The AGI main application must be the authenticated admin and login surface that routes authorized work to the suite. It must not duplicate Fund-Intel tenant records or Impact Relay evidence records. Existing platform direction already assigns authentication to Supabase Auth and application authorization to AGI. This decision makes the AGI control-plane role, downstream handoff, and cross-repository verification explicit.

A separate private harness is required to verify the boundaries without placing integration code, secrets, or deployables in this specifications repository. Notion may coordinate the build temporarily, but it is not an architecture or security authority.

## Decision

1. **AGI is the control plane.** AGI owns login orchestration, session lifecycle at the application edge, authorization, tenant/project selection, and routing to suite capabilities.
2. **Supabase Auth remains the preferred identity provider.** AGI verifies the Supabase session, maps the stable subject to an AGI principal, and evaluates server-side authorization policy.
3. **AGI issues downstream capability context.** After authorization, AGI issues short-lived audience-specific signed JWTs for Fund-Intel and Impact Relay. Tokens use asymmetric signing, published JWKS verification, explicit audience, tenant/project scope, capability scope, expiry, and token identifiers. Tokens are never placed in URLs.
4. **Fund-Intel owns the Hacker Dojo tenant implementation.** It owns project discovery, recommendations, approvals, allocations, and allocation data in the shared Supabase platform.
5. **Impact Relay owns evidence and impact.** It owns delegation evidence, verification, timeline/notification projections, and related storage or Cloud Run execution topology.
6. **Tenant context is shared and fail-closed.** `client_id` and `tenant_id` are carried across the suite as the same tenant identity. Implementations MUST enforce tenant-scoped database, storage, and RPC boundaries and MUST reject mismatched values.
7. **Second-person approval is optional policy.** The tenant director may enable dual approval per project, action class, or threshold. Single-authority approval remains the default for ordinary synthetic workflows. Irreversible or externally visible actions follow the configured tenant policy.
8. **The integration harness is separate and private.** A private AGI-organization repository is the default home. It uses pinned revisions, synthetic fixtures, protected environments, OIDC, short-lived credentials, and least privilege.
9. **Notion is temporary build coordination.** Durable architecture and security decisions move into Specs. Implementation status and runbooks remain in owning product repositories. Temporary Notion labels are not normative artifacts.

## Control-plane topology

```text
Supabase Auth
     │ authenticated session
     ▼
AGI control plane
  login · authorization · tenant/project context · routing
     │ short-lived audience-scoped capability context
     ├──────────────► Fund-Intel / Portfolio Signals
     │                  Hacker Dojo projects, recommendations,
     │                  approvals, allocations
     └──────────────► Impact Relay
                        delegation evidence, verification,
                        impact and public projections

Private cross-repository harness verifies every edge with synthetic data.
```

Logical capability ownership remains governed by [SPEC-006](../specs/SPEC-006-capability-boundaries.md). Physical topology may be Cloudflare + Supabase, with Impact Relay on Cloud Run if its implementation requires it.

## Consequences

- AGI becomes a first-class authenticated control-plane surface rather than only a public narrative site.
- Downstream products do not need competing login flows, but they must independently verify AGI-issued authorization context.
- The browser never receives service-role credentials or reusable cross-service secrets.
- The shared tenant identity is explicit across database, storage, RPC, route, and public projection boundaries.
- The harness adds a private integration dependency, but keeps secrets and cross-repository permissions outside Specs and product repositories.
- Conformance claims must be backed by harness evidence. A manifest MUST NOT claim a contract or event solely because the control plane can route to its owning capability.

## Alternatives considered

| Alternative | Why not selected |
| --- | --- |
| Independent login in Fund-Intel and Impact Relay | Duplicates identity, fragments tenant context, and creates inconsistent authorization |
| Browser-passed Supabase service-role or database credentials | Violates trust boundaries and exposes unrestricted authority |
| JWTs passed in route query parameters | Tokens leak through history, referrers, logs, and screenshots |
| Put the integration harness in Specs | Specs must remain engineering direction without application code, secrets, or deployables |
| Make dual approval globally mandatory | Tenant directors need policy control; ordinary synthetic workflows do not require universal friction |
| Use Notion as architecture authority | Temporary coordination state drifts and cannot replace versioned Specs artifacts |

## Status

**Proposed** (2026-08-15). Implementation repositories and the private harness should pin a released Specs version after this ADR and its related contracts are reviewed.

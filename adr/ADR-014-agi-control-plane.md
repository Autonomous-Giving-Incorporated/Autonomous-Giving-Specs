---
id: ADR-014
version: 1.1.0
authority: normative
owner: Platform Architecture
date: '2026-08-15'
title: AGI-Owned Control Plane and Secure Cross-Repository Integration
status: accepted
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-016
- SPEC-017
- SPEC-019
- SPEC-024
- SPEC-025
- SPEC-028
---

# ADR-014: AGI-Owned Control Plane and Secure Cross-Repository Integration

| Status | Accepted |
| --- | --- |
| Date | 2026-08-15 |
| Related specs | SPEC-002A, SPEC-006, SPEC-016, SPEC-017, SPEC-019, SPEC-024, SPEC-025, SPEC-028 |
| Related contracts | CONTRACT-008–012 |
| Related ADRs | ADR-013 (host), ADR-015 (money / tenant billing), ADR-006 (human Approval) |

## Context

The platform has one shared `client_id` / `tenant_id` boundary across Fund-Intel and Impact Relay. Fund-Intel is the canonical Hacker Dojo reference-tenant implementation, with shared Supabase infrastructure. Impact Relay remains the evidence and impact capability.

The AGI main application must be the authenticated admin and login surface that routes authorized work to the suite. It must not duplicate Fund-Intel tenant records or Impact Relay evidence records. Existing platform direction already assigns authentication to Supabase Auth and application authorization to AGI. This decision makes the AGI control-plane role, downstream handoff, and cross-repository verification explicit.

A separate private harness is required to verify the boundaries without placing integration code, secrets, or deployables in this specifications repository. Notion may coordinate the build temporarily, but it is not an architecture or security authority.

Preferred physical host is already [ADR-013](ADR-013-cloudflare-workers-public-host.md): Cloudflare Workers / Pages / Durable Objects / Queues + Supabase Auth / Postgres / Storage. An earlier draft of this ADR treated Cloud Run as an allowed Impact Relay host without labeling it historical. That language is withdrawn as a preference. If an existing Impact Relay implementation still runs on Cloud Run, that is optional for that implementation only.

Money movement is [ADR-015](ADR-015-donation-tracking-money-boundary.md): AGI tracks gifts; Stripe is tenant/SaaS billing only. This ADR does not add a payments capability.

## Decision

1. **AGI is the control plane.** AGI owns login orchestration, session lifecycle at the application edge, authorization, tenant/project selection, and routing to suite capabilities. Normative detail: [SPEC-028](../specs/SPEC-028-agi-control-plane.md).
2. **Supabase Auth remains the preferred identity provider.** AGI verifies the Supabase session, maps the stable subject to an AGI principal, and evaluates server-side authorization policy.
3. **AGI issues downstream capability context.** After authorization, AGI issues short-lived audience-specific signed JWTs for Fund-Intel and Impact Relay ([CONTRACT-008](../contracts/CONTRACT-008-auth-context.md)). Tokens use asymmetric signing, published JWKS verification, explicit audience, tenant/project scope, capability scope, expiry, and token identifiers (`jti`). Tokens are never placed in URLs. The browser never receives service-role or reusable cross-service secrets.
4. **Downstream capabilities verify independently.** Fund-Intel and Impact Relay MUST verify issuer, signature, audience, expiry, tenant, and capability before acting. They MUST fail closed on `client_id` / `tenant_id` mismatch. “Authenticated with the IdP” is not enough ([SPEC-016](../specs/SPEC-016-security-and-trust-boundaries.md), [SPEC-019](../specs/SPEC-019-identity-and-authorization.md)).
5. **Fund-Intel owns the Hacker Dojo tenant implementation.** It owns project discovery, recommendations, approvals data path, allocations, and allocation data in the shared Supabase platform. AGI MUST NOT duplicate those tenant records.
6. **Impact Relay owns evidence and impact.** It owns delegation evidence, verification, timeline/notification projections, and related storage. AGI MUST NOT duplicate evidence records.
7. **Preferred physical topology is Cloudflare + Supabase** for AGI, Fund Intel, and Impact Relay ([ADR-013](ADR-013-cloudflare-workers-public-host.md)). D1 is not the canonical store. Render is historical. Cloud Run is **historical or optional for an existing Impact Relay implementation** — not a new preferred host and not a conformance requirement.
8. **Tenant context is shared and fail-closed.** `client_id` and `tenant_id` are the same tenant identity ([CONTRACT-009](../contracts/CONTRACT-009-tenant-project-context.md)).
9. **Second-person approval is optional policy.** The tenant director may enable dual approval per project, action class, or threshold ([CONTRACT-011](../contracts/CONTRACT-011-delegation-policy.md)). Single-authority approval remains the default for ordinary flows. Irreversible or externally visible actions follow the configured tenant policy. Human Approval still gates allocations ([ADR-006](ADR-006-human-approval.md)). Intelligence never allocates.
10. **The integration harness is separate and private.** A private AGI-organization repository is the default home. It uses pinned revisions, synthetic fixtures, protected environments, OIDC, short-lived credentials, and least privilege.
11. **Notion is temporary build coordination.** Durable architecture and security decisions move into Specs. Implementation status and runbooks remain in owning product repositories. Temporary Notion labels are not normative artifacts.
12. **Control plane is not a fourth capability.** It is Autonomous Giving’s edge ([SPEC-014](../specs/SPEC-014-future-capabilities.md)).

## Control-plane topology

```text
Supabase Auth
     │ authenticated session
     ▼
AGI control plane
  login · authorization · tenant/project context · routing
     │ short-lived audience-scoped capability JWT
     ├──────────────► Fund-Intel / Portfolio Signals
     │                  Hacker Dojo projects, recommendations,
     │                  approvals, allocations
     └──────────────► Impact Relay
                        delegation evidence, verification,
                        impact and public projections

Private cross-repository harness verifies every edge with synthetic data.
```

Logical capability ownership remains governed by [SPEC-006](../specs/SPEC-006-capability-boundaries.md). Physical topology is Cloudflare + Supabase. An existing Impact Relay Cloud Run deployment, if any, does not change ownership and is not required of new work.

## Consequences

- AGI becomes a first-class authenticated control-plane surface rather than only a public narrative site.
- Downstream products do not need competing login flows, but they must independently verify AGI-issued authorization context.
- The browser never receives service-role credentials or reusable cross-service secrets.
- The shared tenant identity is explicit across database, storage, RPC, route, and public projection boundaries.
- The harness adds a private integration dependency, but keeps secrets and cross-repository permissions outside Specs and product repositories.
- Conformance claims must be backed by harness evidence. A manifest MUST NOT claim a contract or event solely because the control plane can route to its owning capability.
- This ADR does not tag a platform release and does not mark implementation READY.

## Alternatives considered

| Alternative | Why not selected |
| --- | --- |
| Independent login in Fund-Intel and Impact Relay | Duplicates identity, fragments tenant context, and creates inconsistent authorization |
| Browser-passed Supabase service-role or database credentials | Violates trust boundaries and exposes unrestricted authority |
| JWTs passed in route query parameters | Tokens leak through history, referrers, logs, and screenshots |
| Put the integration harness in Specs | Specs must remain engineering direction without application code, secrets, or deployables |
| Make dual approval globally mandatory | Tenant directors need policy control; ordinary synthetic workflows do not require universal friction |
| Use Notion as architecture authority | Temporary coordination state drifts and cannot replace versioned Specs artifacts |
| Prefer Impact Relay on Cloud Run | Reopens a second application host after ADR-013; Cloud Run may remain only as a historical/optional existing implementation |

## Status

**Accepted** (2026-08-15). Host language aligned to ADR-013 / SPEC-028. Does not claim a tagged platform release. Pin-a-release remains operator-owned.

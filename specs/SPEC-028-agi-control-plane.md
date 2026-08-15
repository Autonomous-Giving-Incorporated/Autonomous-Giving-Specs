---
id: SPEC-028
title: AGI Control Plane
version: 1.0.0
status: accepted
authority: normative
owner: Autonomous Giving
related_specs:
- SPEC-002A
- SPEC-006
- SPEC-016
- SPEC-017
- SPEC-019
- SPEC-024
- SPEC-025
- SPEC-027
related_adrs:
- ADR-006
- ADR-013
- ADR-014
- ADR-015
related_contracts:
- CONTRACT-008
- CONTRACT-009
- CONTRACT-010
- CONTRACT-011
- CONTRACT-012
---

# SPEC-028: AGI Control Plane
| Version | 1.0.0 | Owner | Autonomous Giving | Status | Accepted |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-006, SPEC-016, SPEC-019, SPEC-024 | Related ADRs | ADR-006, ADR-013, ADR-014, ADR-015 | Related contracts | CONTRACT-008–012 |

## Purpose

Define the Autonomous Giving Incorporated (**AGI**) control plane so implementers can build the authenticated admin surface, authorization, tenant/project selection, and downstream capability handoff from canon—without inventing a login per product, a fifth capability, or a donation checkout.

This specification is the normative companion to [ADR-014](../adr/ADR-014-agi-control-plane.md). Logical capability ownership remains [SPEC-006](SPEC-006-capability-boundaries.md). Preferred physical host remains [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md). Money movement remains [ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md).

## Scope

Session at the application edge, application authorization, tenant and project selection, routing to suite capabilities, AGI-issued capability context ([CONTRACT-008](../contracts/CONTRACT-008-auth-context.md)), independent verification at Fund Intel and Impact Relay edges, optional dual-approval policy ([CONTRACT-011](../contracts/CONTRACT-011-delegation-policy.md)), preferred topology, and the private integration harness boundary.

## Non-goals

- AGI checkout, donation capture, charge, refund, or a Stripe Checkout Session for gifts.
- A fifth capability for payments or “fund intel + giving + relay + billing.”
- Inventing hosts, `workers.dev` URLs, live every.org pointing, or a tagged platform release.
- Putting the private integration harness, secrets, or deployables in this repository.
- Treating Notion as architecture or security authority.
- Duplicating Fund-Intel tenant/project records or Impact Relay evidence records inside AGI.

## Control-plane role

AGI is the authenticated **admin and login surface** for the suite. Preferred identity is **Supabase Auth** ([SPEC-024](SPEC-024-integration-boundaries.md), [SPEC-019](SPEC-019-identity-and-authorization.md)). Clerk remains allowed only if a product still requires it.

After authentication, AGI owns:

| Concern | AGI owns | AGI must not own |
| --- | --- | --- |
| Session | Application-edge session lifecycle (verify IdP session, map subject → AGI principal, bind cookie/session) | IdP credential storage; browser-held service-role keys |
| Authorization | Server-side roles, org membership, capability grants, financial and admin permissions | Trusting client-supplied role claims |
| Tenant / project | Selection of authorized `client_id` / `tenant_id` / `project_id` for the current principal | Canonical Fund-Intel tenant or project records |
| Routing | Authorized handoff to Fund Intel and Impact Relay ([CONTRACT-010](../contracts/CONTRACT-010-route-intent.md)) | Downstream domain mutation without the owning capability |
| Capability context | Issuing short-lived audience-specific signed JWTs ([CONTRACT-008](../contracts/CONTRACT-008-auth-context.md)) | Reusable cross-service secrets in the browser |
| Evidence / impact | Display of Impact Relay projections AGI is authorized to show | Evidence, verification, or public-projection authority |
| Money | Authorization to allocate under [ADR-006](../adr/ADR-006-human-approval.md) | Donation processing; pot-credit authority (Fund Intel observes) |

Fund Intel observes and credits gift summaries. Autonomous Giving allocates under human Approval. Impact Relay proves and notifies. Intelligence never allocates. No fifth capability.

## Topology

```text
Supabase Auth
     │ authenticated session
     ▼
AGI control plane
  login · session · authorization · tenant/project selection · routing
     │ short-lived audience-scoped capability JWT (CONTRACT-008)
     │ + route intent (CONTRACT-010); never in a URL
     ├──────────────► Fund Intel
     │                  project discovery, recommendations,
     │                  approvals data path, allocations
     └──────────────► Impact Relay
                        evidence, verification,
                        timeline / Notification / ImpactNotice,
                        public projections (CONTRACT-012)

Private cross-repository harness (outside this repo) verifies edges with synthetic data.
```

Preferred **physical** topology for AGI, Fund Intel, and Impact Relay is **Cloudflare + Supabase** ([ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)): Workers / Pages / static assets; Durable Objects only if live coordination is needed; Queues / Cron Triggers for deferred, webhook, and retry work; Supabase Auth, PostgreSQL (canonical store), and Storage. D1 is not the canonical store. Render is historical ([ADR-012](../adr/ADR-012-render-first-platform.md)).

If an **existing** Impact Relay implementation still runs on Cloud Run, that host is **historical or optional for that implementation**. Cloud Run is not a new preferred host and is not a conformance requirement. Logical ownership does not change with host.

## Authentication and session

1. The user authenticates with Supabase Auth (or a still-required equivalent IdP).
2. AGI MUST verify the IdP session at the application edge (Worker or server), not in a public client bundle that the user can rewrite.
3. AGI MUST map the stable IdP subject (`supabase_user_id`, or `clerk_user_id` if Clerk is still required) to an AGI principal. Email MUST NOT be the sole foreign key for domain records ([SPEC-024](SPEC-024-integration-boundaries.md)).
4. Browser sessions MUST use secure, `HttpOnly` cookies (or an equivalent non-script-readable session binding). Capability JWTs MUST NOT be placed in URLs, query strings, or fragment identifiers.
5. The browser MUST NEVER receive the Supabase service-role key, database credentials, webhook secrets, or reusable cross-service signing keys.

“Authenticated with the IdP” is **not** sufficient for financial or administrative actions ([SPEC-019](SPEC-019-identity-and-authorization.md)).

## Authorization

6. AGI MUST evaluate authorization server-side against persisted policy. Client-supplied role or capability claims are never authoritative.
7. Authorization is **deny by default**. A principal may perform only the actions granted for the current `client_id` / `tenant_id` / `project_id` and capability.
8. Initial roles and sensitive capabilities follow the direction in [architecture/control-plane.md](../architecture/control-plane.md). Implementations MAY refine names; they MUST preserve the intelligence-must-not-allocate and evidence-must-not-approve separations ([SPEC-006](SPEC-006-capability-boundaries.md), [ADR-006](../adr/ADR-006-human-approval.md)).
9. Human Approval still gates allocations. Intelligence MUST NOT be authorized to create Allocation, attach Evidence, waive Evidence, or emit ImpactNotice.

## Capability JWTs (CONTRACT-008)

After authorization, when a process or trust boundary exists between AGI and a downstream capability, AGI MUST issue a short-lived audience-specific signed JWT whose claims validate as [CONTRACT-008](../contracts/CONTRACT-008-auth-context.md).

10. Signing MUST be **asymmetric**. AGI holds the private key; Fund Intel and Impact Relay verify with the published JWKS. Symmetric shared secrets MUST NOT be the cross-capability verification method for new work.
11. AGI MUST publish a JWKS document at an implementation-owned HTTPS URL. This specification does not invent that URL and does not freeze a SHA or host as a live receipt.
12. Each token MUST include: issuer, subject, `jti` (`tokenId`), explicit **audience** (`fund-intel` or `impact-relay`), `client_id`, `tenant_id`, roles, capabilities, `issuedAt`, and `expiresAt`. `project_id` is required for project-scoped actions.
13. `client_id` and `tenant_id` MUST identify the same tenant. Implementations MUST fail closed on mismatch, absence, or unauthorized values ([CONTRACT-009](../contracts/CONTRACT-009-tenant-project-context.md)).
14. Tokens MUST be short-lived. Implementations SHOULD keep expiry on the order of minutes for interactive handoff, not hours, unless a documented workload requires a longer bound still short of a reusable secret.
15. Tokens MUST NOT appear in URLs. Server-side handoff (header, cookie scoped to the receiving host, or in-process call) is required.
16. In a modular monolith, an in-process call MAY omit a wire JWT when the process identity is the AGI control plane and the module authorization check is equivalent. The same claims (`audience`, tenant, capability, expiry semantics) MUST still be evaluated. Crossing a process or repository boundary restores the JWT MUST.

## Downstream verification

Fund Intel and Impact Relay MUST independently verify inbound control-plane context before acting. They MUST NOT trust AGI solely because the request arrived on an internal hostname or because the user has an IdP session.

17. The receiving capability MUST verify, fail-closed: issuer, signature (JWKS), audience, expiry, `jti` replay policy as implemented, `client_id` / `tenant_id` equality and authorization, project scope when required, and requested capability.
18. Unverified, expired, wrong-audience, over-scoped, or cross-tenant context MUST be denied. No financial or admin side effect MAY proceed on unverified downstream context ([SPEC-016](SPEC-016-security-and-trust-boundaries.md), [SPEC-019](SPEC-019-identity-and-authorization.md)).
19. [CONTRACT-010](../contracts/CONTRACT-010-route-intent.md) describes authorized routing intent. It contains no bearer token and is **not** sufficient authorization without CONTRACT-008 validation (or the equivalent in-process check in requirement 16).
20. A receiving capability MUST apply its own tenant-scoped database, storage, and RPC policy after token verification. Token success does not bypass row-level or storage-key tenant isolation.

## Record ownership

21. AGI MUST NOT duplicate Fund-Intel tenant records or project records as a second system of record. AGI MAY cache display labels and authorized identifiers for routing.
22. AGI MUST NOT duplicate Impact Relay evidence, verification, or public-projection records as a second system of record. AGI MAY display [CONTRACT-012](../contracts/CONTRACT-012-public-projection.md) payloads that Impact Relay produced.
23. Public projections MUST remain aggregate-safe: no donor identity, private evidence URL, service credential, or unrestricted tenant record ([SPEC-017](SPEC-017-data-classification-and-privacy.md)). ImpactNotice CTA remains the tenant outbound Donation Link ([SPEC-027](SPEC-027-impact-loop.md)). Implementations MUST NOT invent PII.

## Dual approval (CONTRACT-011)

24. Dual approval is **optional tenant policy**. Default remains **single-authority** for ordinary flows ([CONTRACT-011](../contracts/CONTRACT-011-delegation-policy.md)).
25. A tenant director MAY enable `dual` per project, action class, or amount threshold. The policy is evaluated server-side. A client-supplied approval count is never authoritative.
26. Dual approval MUST require distinct authorized human principals and MUST be recorded before an irreversible or externally visible action proceeds when the policy is `dual`.
27. Irreversible or externally visible actions follow the configured tenant policy. Human Approval still gates allocations regardless of `single` or `dual` ([ADR-006](../adr/ADR-006-human-approval.md)).
28. Intelligence never allocates. Enabling dual approval does not authorize Fund Intel to mint Approval.

## Money and billing (pointer)

29. AGI never processes donations. It tracks gifts ([ADR-015](../adr/ADR-015-donation-tracking-money-boundary.md), [SPEC-023](SPEC-023-financial-ledger-invariants.md)). every.org is the P0 connector. Stripe, if present, is tenant/SaaS billing only. Tenant pages use outbound `donation_link`. This specification does not add a payments capability.

## Private harness and coordination

30. The cross-repository integration harness is **private** and lives **outside this repository**. Default home is a private AGI-organization repository. It uses pinned revisions, synthetic fixtures, protected environments, OIDC, short-lived credentials, and least privilege. See [architecture/secure-cross-repo-harness.md](../architecture/secure-cross-repo-harness.md).
31. This specifications repository MUST remain free of application code, secrets, and deployables ([ADR-001](../adr/ADR-001-repository-strategy.md), [ADR-004](../adr/ADR-004-repository-ownership.md)).
32. Notion MAY coordinate a build temporarily. Notion is **not** architecture authority and is **not** a security authority. Durable decisions live in Specs.

## Audit

33. Issuing a capability JWT that authorizes financial or administrative action is audit-relevant. Implementations MUST retain issuer, audience, subject, tenant, `jti`, issued/expiry times, and the authorized action class long enough to support dispute review. Raw tokens MUST NOT be written to this repository or to public logs ([EVENT-012](../events/EVENT-012-capability-context-issued.md)).
34. Approval events MUST remain reconcilable to the evaluated [CONTRACT-011](../contracts/CONTRACT-011-delegation-policy.md) policy ([EVENT-004](../events/EVENT-004-approval-granted.md)).

## Conformance

35. Logical modular-monolith or multi-process deployment may both conform ([SPEC-002A](SPEC-002A-architectural-principles.md), [SPEC-013](SPEC-013-repository-conformance.md)). Preferred host is informative for topology and normative for “do not invent a new preferred host.”
36. A conformance manifest MUST NOT claim a contract or event solely because the control plane can route to its owning capability ([ADR-014](../adr/ADR-014-agi-control-plane.md)).
37. This specification does not mark implementation READY, freeze a commit SHA as a live receipt, or pin a platform release tag. Pin-a-release remains operator-owned.

## Rationale

Without a single control plane, Fund Intel and Impact Relay grow competing login flows, split tenant identity, and accept unverified downstream calls. Browser-held service-role keys and JWTs in URLs fail the trust model in [SPEC-016](SPEC-016-security-and-trust-boundaries.md). Mandatory dual approval for every synthetic flow adds friction the tenant director did not request. A Cloud Run preference for Impact Relay would reopen a second application host after [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md).

## References

- [ADR-014](../adr/ADR-014-agi-control-plane.md) — control-plane decision
- [architecture/control-plane.md](../architecture/control-plane.md) — engineering direction (normative only where it links here)
- [architecture/secure-cross-repo-harness.md](../architecture/secure-cross-repo-harness.md) — private harness direction
- [SPEC-016](SPEC-016-security-and-trust-boundaries.md), [SPEC-017](SPEC-017-data-classification-and-privacy.md), [SPEC-019](SPEC-019-identity-and-authorization.md) — trust layer
- [SPEC-024](SPEC-024-integration-boundaries.md), [SPEC-025](SPEC-025-operations-deploy-and-scale.md) — identity and operations
- [SPEC-027](SPEC-027-impact-loop.md) — ImpactNotice CTA and no invented PII

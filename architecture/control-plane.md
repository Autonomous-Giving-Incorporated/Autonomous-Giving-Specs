# AGI control-plane architecture

This document defines the engineering direction for the AGI control plane. It is normative only where it links to accepted Specs and ADRs. Implementation repositories own concrete routes, migrations, provider configuration, and operational runbooks.

## Responsibilities

| Surface | Owns | Must not own |
| --- | --- | --- |
| AGI control plane | Authentication orchestration, authorization, tenant/project context, admin navigation, capability routing | Fund-Intel project records, Impact Relay evidence history, private donor projections |
| Fund-Intel | Hacker Dojo tenant implementation, project discovery, recommendations, approvals, allocations | Evidence verification or public impact truth |
| Impact Relay | Delegation evidence, evidence storage, verification, timeline/impact projection | Allocation approval or authoritative allocation mutation |
| Specs | Engineering direction, shared contracts, lifecycle, security boundaries, ADRs | Application code, deployables, secrets, operational credentials |
| Private harness | Cross-repository acceptance and security verification | Production data, long-lived credentials, domain authority |

The logical boundaries follow [SPEC-006](../specs/SPEC-006-capability-boundaries.md). The preferred hosted path follows [ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md). Impact Relay may remain on Cloud Run as an implementation choice because deployment topology does not change capability ownership.

## Request flow

```text
1. User authenticates with Supabase Auth.
2. AGI verifies the session and maps the stable subject to an AGI principal.
3. AGI evaluates role, capability, client_id, tenant_id, and project policy.
4. AGI creates a short-lived audience-scoped route context.
5. The AGI gateway or server-side handoff routes to Fund-Intel or Impact Relay.
6. The receiving capability validates issuer, signature, audience, expiry,
   tenant identity, project scope, and requested capability.
7. The receiving capability applies its own tenant-scoped database/storage/RPC policy.
8. The harness observes the boundary using synthetic fixtures and pinned revisions.
```

Tokens are never put in query strings. Browser sessions use secure, HttpOnly cookies. Downstream capability context uses asymmetric signed JWTs and public JWKS verification when a process boundary exists.

## Shared tenant and project context

The suite uses a shared `client_id` / `tenant_id` contract:

- `client_id` and `tenant_id` identify the same tenant and MUST match when both are present.
- Every tenant-scoped request, record, storage key, and RPC call carries the authorized tenant context.
- `project_id` is scoped beneath the tenant and is not globally reusable across tenants.
- A project may have multiple recommendations, allocations, delegation records, evidence records, and impact projections, but each must preserve stable identifiers and ownership.
- Donor identity is not a public join key and is not required by the cross-capability context contracts.

## Authorization model

Initial roles are:

- `agi_admin`
- `tenant_director`
- `tenant_operator`
- `evidence_reviewer`
- `viewer`

Sensitive authority is expressed as capabilities:

- `project:read`
- `recommendation:review`
- `allocation:propose`
- `allocation:approve`
- `allocation:execute`
- `delegation:authorize`
- `evidence:review`
- `impact:publish`

A tenant director may configure `single` or `dual` approval for a project, action class, or amount threshold. Single approval is the default. The policy is evaluated server-side and is recorded with approval events. No client-supplied role claim is authoritative.

## Route map direction

AGI should expose a stable control-plane route family. Exact framework paths remain implementation-owned.

```text
/login
/admin
/admin/tenants/:tenantId
/admin/tenants/:tenantId/projects
/admin/tenants/:tenantId/projects/:projectId
/portfolio-signals/*   → Fund-Intel capability
/impact-relay/*       → Impact Relay capability
```

The public AGI narrative may remain available at `/`, but authenticated administration and routing are separate trust surfaces.

## Contract direction

The proposed cross-boundary contracts are:

| Contract | Purpose | Owner |
| --- | --- | --- |
| [CONTRACT-008](../contracts/CONTRACT-008-auth-context.md) | AGI-issued authenticated capability context | Autonomous Giving |
| [CONTRACT-009](../contracts/CONTRACT-009-tenant-project-context.md) | Shared client/tenant/project identity | Platform Architecture |
| [CONTRACT-010](../contracts/CONTRACT-010-route-intent.md) | Authorized capability routing intent | Autonomous Giving |
| [CONTRACT-011](../contracts/CONTRACT-011-delegation-policy.md) | Optional single/dual approval policy | Autonomous Giving |
| [CONTRACT-012](../contracts/CONTRACT-012-public-projection.md) | Aggregate-safe impact projection | Impact Relay |

These contracts are proposed until the next Specs release. Existing lifecycle contracts remain authoritative for Need through Impact.

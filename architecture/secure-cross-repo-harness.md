# Secure cross-repository harness

## Purpose

The cross-repository harness verifies the AGI control plane against the canonical Fund-Intel Hacker Dojo tenant implementation and Impact Relay evidence path. It is a private implementation repository, not a Specs deployable.

Tentative repository name: `agi-cross-repo-harness` under the Autonomous-Giving organization. The final location may change if security ownership requires a different private organization boundary.

## Trust model

The harness is an external verifier. It must assume every capability boundary can receive malformed, stale, forged, over-scoped, or cross-tenant input.

- Synthetic fixtures only. No donor records, production receipts, private evidence, or real credentials.
- Pin every checked-out repository to an explicit commit or release.
- Use GitHub Actions OIDC and short-lived provider credentials where access is required.
- Use protected environments and least-privilege repository/service permissions.
- Keep signing keys, Supabase secrets, and any historical/optional host credentials (including Cloud Run, if an existing Impact Relay implementation still uses it) outside the repository.
- Redact tokens and payloads from CI logs. Persist only test names, revision IDs, and safe reason codes.
- A failed security check blocks acceptance; it does not fall back to a weaker test mode.

## Verification layers

### 1. Contract validation

- Validate accepted CONTRACT-008–012 payloads against the pinned Specs schemas ([SPEC-028](../specs/SPEC-028-agi-control-plane.md)).
- Reject missing or mismatched `client_id` / `tenant_id` values.
- Reject donor identifiers in public projection payloads.
- Tolerate unknown compatible fields according to the pinned compatibility rules.

### 2. Authentication and authorization

- Authenticate a synthetic user through the AGI-owned boundary.
- Verify AGI-issued signature, issuer, audience, expiry, token ID, capability scope, and tenant/project context.
- Reject forged, expired, replayed, wrong-audience, cross-tenant, and over-scoped tokens.
- Confirm AGI authorization is evaluated server-side rather than trusting browser role claims.

### 3. Tenant and project routing

- Resolve Hacker Dojo as the reference tenant.
- Select at least two synthetic projects beneath the tenant.
- Confirm a project context cannot be used with another tenant.
- Confirm Fund-Intel receives only the context required for its owned workflow.
- Confirm Impact Relay receives only authorized evidence/delegation context.

### 4. Lifecycle and approval

- Verify Recommendation precedes Approval and Approval precedes Allocation.
- Verify default single approval works for a synthetic project.
- Verify a tenant director can enable dual approval for a project or action threshold.
- Verify configured dual approval rejects execution until the second authorized principal acts.
- Verify all approval and allocation actions preserve actor, tenant, project, correlation, and idempotency identifiers.

### 5. Evidence and public projection

- Verify Impact Relay can attach evidence only to the authorized allocation/project.
- Verify evidence and verification remain append-oriented.
- Verify public projection contains only approved aggregate-safe fields.
- Verify stale, malformed, unauthorized, or mismatched source data fails closed.

## CI stages

```text
checkout pinned revisions
  → install locked dependencies
  → validate Specs metadata and schemas
  → start synthetic service doubles or approved preview endpoints
  → run auth and tenant-isolation tests
  → run lifecycle and delegation tests
  → run public-projection privacy tests
  → publish redacted report with revision and artifact IDs
```

The harness may use local doubles for fast contract tests and ephemeral preview environments for representative routing tests. It must label substitute tests clearly and reserve acceptance status for the real AGI/Fund-Intel/Impact Relay workflow.

## Required evidence

Each harness run records:

- Specs release and schema revisions
- AGI, Fund-Intel, and Impact Relay revisions
- Harness revision
- Test class and result
- Synthetic tenant/project fixture identifiers
- Safe failure reason codes
- No raw JWTs, credentials, donor identity, or private evidence URLs

The harness report links to implementation evidence but does not replace product-owned logs, audit records, or provider dashboards.

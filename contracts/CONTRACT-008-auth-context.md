---
id: CONTRACT-008
version: 1.0.0
status: proposed
authority: normative
title: AGI Auth Context
owner: Autonomous Giving
lifecycle_stage: Approval
schema: ../schemas/auth-context.json
producer: Autonomous Giving
consumer: Fund Intel, Impact Relay
related_specs:
- SPEC-016
- SPEC-019
- SPEC-024
---

# CONTRACT-008: AGI Auth Context

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Autonomous Giving |
| Producer / consumer | Autonomous Giving / Fund Intel, Impact Relay |
| Schema | [auth-context.json](../schemas/auth-context.json) |

Short-lived authorization context issued by AGI after Supabase Auth session verification. It is not a browser credential and must not be placed in a URL.

Required fields are `issuer`, `subject`, `tokenId`, `audience`, `client_id`, `tenant_id`, `roles`, `capabilities`, `issuedAt`, and `expiresAt`. `client_id` and `tenant_id` MUST identify the same tenant. `project_id` is optional for tenant-wide actions and required for project-scoped actions. The receiving capability MUST validate signature, issuer, audience, expiry, tenant/project scope, and capability before acting.

```json
{"issuer":"https://autogive.app","subject":"user-123","tokenId":"jti-123","audience":"fund-intel","client_id":"hacker-dojo","tenant_id":"hacker-dojo","project_id":"project-robotics","roles":["tenant_director"],"capabilities":["allocation:approve"],"issuedAt":"2026-08-15T16:00:00Z","expiresAt":"2026-08-15T16:10:00Z"}
```

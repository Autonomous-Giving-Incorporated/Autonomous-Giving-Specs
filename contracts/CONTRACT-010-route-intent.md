---
id: CONTRACT-010
version: 1.0.0
status: proposed
authority: normative
title: Capability Route Intent
owner: Autonomous Giving
lifecycle_stage: Approval
schema: ../schemas/route-intent.json
producer: Autonomous Giving
consumer: Fund Intel, Impact Relay
related_specs:
- SPEC-006
- SPEC-019
- SPEC-024
---

# CONTRACT-010: Capability Route Intent

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Autonomous Giving |
| Producer / consumer | Autonomous Giving / Fund Intel, Impact Relay |
| Schema | [route-intent.json](../schemas/route-intent.json) |

Server-side intent describing an authorized handoff from AGI to a suite capability. It contains no bearer token and is not sufficient authorization without CONTRACT-008 validation.

Required fields are `intentId`, `audience`, `action`, `client_id`, `tenant_id`, `project_id`, `requestedAt`, and `expiresAt`. The receiver MUST bind the intent to the verified AGI auth context and reject expired, mismatched, or unsupported actions.

```json
{"intentId":"intent-123","audience":"fund-intel","action":"project.review","client_id":"hacker-dojo","tenant_id":"hacker-dojo","project_id":"project-robotics","requestedAt":"2026-08-15T16:00:00Z","expiresAt":"2026-08-15T16:05:00Z"}
```

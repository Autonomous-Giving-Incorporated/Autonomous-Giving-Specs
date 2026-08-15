---
id: CONTRACT-012
version: 1.0.0
status: proposed
authority: normative
title: Public Impact Projection
owner: Impact Relay
lifecycle_stage: Impact
schema: ../schemas/public-projection.json
producer: Impact Relay
consumer: Autonomous Giving, public surfaces
related_specs:
- SPEC-005
- SPEC-016
- SPEC-017
- SPEC-018
- SPEC-024
---

# CONTRACT-012: Public Impact Projection

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Impact Relay |
| Producer / consumer | Impact Relay / Autonomous Giving, public surfaces |
| Schema | [public-projection.json](../schemas/public-projection.json) |

Aggregate-safe project impact projection for public AGI and suite surfaces. It contains no donor identity, private evidence URL, service credential, or unrestricted tenant record.

Required fields are `projectionId`, `client_id`, `tenant_id`, `project_id`, `authority`, `status`, `verificationStatus`, `summary`, and `updatedAt`. `authority` MUST be `public_aggregate_only`. Public consumers MUST fail closed on unknown authority, mismatched tenant identity, invalid verification, or stale source data.

```json
{"projectionId":"projection-robotics","client_id":"hacker-dojo","tenant_id":"hacker-dojo","project_id":"project-robotics","authority":"public_aggregate_only","status":"verified","verificationStatus":"verified","summary":"Robotics workshop delivery verified for the selected project.","updatedAt":"2026-08-15T16:00:00Z"}
```

---
id: CONTRACT-009
version: 1.0.0
status: proposed
authority: normative
title: Tenant Project Context
owner: Autonomous Giving
lifecycle_stage: Opportunity
schema: ../schemas/tenant-project-context.json
producer: Autonomous Giving
consumer: Fund Intel, Impact Relay
related_specs:
- SPEC-004
- SPEC-006
- SPEC-016
- SPEC-017
- SPEC-024
---

# CONTRACT-009: Tenant Project Context

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Autonomous Giving |
| Producer / consumer | Autonomous Giving / Fund Intel, Impact Relay |
| Schema | [tenant-project-context.json](../schemas/tenant-project-context.json) |

Shared tenant and project identity for cross-repository requests, records, storage keys, and RPC calls.

`client_id` and `tenant_id` are required compatibility fields and MUST be equal. `project_id` is scoped beneath that tenant and MUST NOT be interpreted globally. A receiving capability MUST reject missing, mismatched, or unauthorized context before querying tenant data.

```json
{"client_id":"hacker-dojo","tenant_id":"hacker-dojo","project_id":"project-robotics","scope":"project"}
```

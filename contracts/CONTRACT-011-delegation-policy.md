---
id: CONTRACT-011
version: 1.0.0
status: accepted
authority: normative
title: Delegation Approval Policy
owner: Autonomous Giving
lifecycle_stage: Approval
schema: ../schemas/delegation-policy.json
producer: Autonomous Giving
consumer: Fund Intel, Impact Relay
related_specs:
- SPEC-005
- SPEC-006
- SPEC-016
- SPEC-019
- SPEC-028
---

# CONTRACT-011: Delegation Approval Policy

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Autonomous Giving |
| Producer / consumer | Autonomous Giving / Fund Intel, Impact Relay |
| Schema | [delegation-policy.json](../schemas/delegation-policy.json) |

Tenant or project policy controlling whether an action requires one or two authorized human approvals. `single` is the default. A tenant director may configure `dual` for selected projects, action classes, or amount thresholds.

The policy is evaluated server-side. A client-supplied approval count is never authoritative. Dual approval MUST require distinct authorized principals and MUST be recorded before an irreversible or externally visible action proceeds.

```json
{"policyId":"policy-hacker-dojo","client_id":"hacker-dojo","tenant_id":"hacker-dojo","project_id":"project-robotics","approvalMode":"single","requiredApproverRoles":["tenant_director"],"updatedAt":"2026-08-15T16:00:00Z"}
```

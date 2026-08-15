# Hacker Dojo — multi-project tenant fixture

This is a synthetic reference tenant for cross-repository integration work. It is not the canonical `SPEC-011` Community AI Lab conformance demo.

Fund-Intel is the canonical tenant implementation. AGI supplies authenticated tenant/project context and routes authorized work. Impact Relay owns evidence, verification, delegation outcomes, and public impact projections.

## Invariants

- `client_id` and `tenant_id` are equal and stable across Fund-Intel and Impact Relay.
- Each project has a distinct `project_id` scoped beneath Hacker Dojo.
- No donor identity or private evidence appears in this fixture.
- Projects may have independent recommendation, allocation, delegation, and impact states.
- Allocation still requires human approval before execution.
- A tenant director may configure optional dual approval per project or action threshold.

`tenant.json` intentionally models the routing and fixture boundary. Product repositories remain responsible for validating their own lifecycle contracts and tenant-scoped database, storage, and RPC access.

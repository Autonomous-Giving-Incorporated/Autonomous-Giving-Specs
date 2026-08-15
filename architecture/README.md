# Architecture

- [Overview](overview.md) — logical capabilities vs preferred Cloudflare + Supabase physical deployment
- [AGI control plane](control-plane.md) — AGI authentication, authorization, tenant/project routing, and capability handoff ([SPEC-028](../specs/SPEC-028-agi-control-plane.md), [ADR-014](../adr/ADR-014-agi-control-plane.md) accepted)
- [Secure cross-repository harness](secure-cross-repo-harness.md) — private synthetic integration and security verification direction
- Domain and lifecycle diagrams live under [`diagrams/`](../diagrams/)
- Capability boundaries: [SPEC-006](../specs/SPEC-006-capability-boundaries.md)
- Architectural principles: [SPEC-002A](../specs/SPEC-002A-architectural-principles.md)
- Preferred stack: [SPEC-021](../specs/SPEC-021-preferred-application-stack.md)
- PostgreSQL persistence: [SPEC-022](../specs/SPEC-022-postgresql-persistence.md)
- Financial ledger invariants: [SPEC-023](../specs/SPEC-023-financial-ledger-invariants.md)
- Integration boundaries: [SPEC-024](../specs/SPEC-024-integration-boundaries.md)
- Operations / deploy / scale: [SPEC-025](../specs/SPEC-025-operations-deploy-and-scale.md)
- Deployment profiles: [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md)
- Decision: [ADR-013 Cloudflare and Supabase Hosted Platform](../adr/ADR-013-cloudflare-workers-public-host.md) (supersedes [ADR-012](../adr/ADR-012-render-first-platform.md))

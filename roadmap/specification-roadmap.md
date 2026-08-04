# Platform Standards Roadmap

## Delivery evolution (recommended)

```text
Phase 1  Modular Monolith          ← default MVP
    ↓
Phase 2  Background Workers
    ↓
Phase 3  Extract Individual Capabilities  (only if justified)
    ↓
Phase 4  Distributed Platform
    ↓
Phase 5  Enterprise Deployment
```

## Client product path (allocation middleware)

Informative product roadmap aligned to [allocation middleware design](../docs/superpowers/specs/2026-08-03-allocation-middleware-design.md). **Not a specification milestone**; guides implementation repositories.

| Step | State | Where |
| --- | --- | --- |
| 1. every.org connector + campaign/program pots + allocate + exception inbox | **MVP shipped** | Fund-Intel `services/allocation-middleware/` |
| 2. Trail + board packet + proof SLA | **MVP shipped** | Same package |
| 3. Hacker Dojo pilot host (seed → director login → live webhook) | **Active** | [pilot hosting plan](../docs/superpowers/plans/2026-08-03-hacker-dojo-pilot-hosting.md) |
| 4. Additional donation-platform adapters (Givebutter, Donorbox, …) | Later | Adapter interface only in MVP |
| 5. Funder multi-grantee portfolio | Later | Out of MVP scope |

Plans: [MVP](../docs/superpowers/plans/2026-08-03-allocation-middleware.md) · [pilot hosting](../docs/superpowers/plans/2026-08-03-hacker-dojo-pilot-hosting.md).

The platform evolves toward distribution only when operational criteria warrant it. Specs remain deployment-independent throughout.

## Specification milestones

| Milestone | Outcome | Exit criterion |
| --- | --- | --- |
| 1. Platform Canon | Constitution, vocabulary, lifecycle | SPEC-001, 002, 004, 005 accepted |
| 2. Architectural Principles | Capability-first, deployment independence | SPEC-002A accepted |
| 3. Signals Stack | Observation and recommendation boundary | SPEC-003 reviewed |
| 4. Contracts | Owned interoperable messages (transport-independent) | CONTRACT-001–007 validated |
| 5. Schemas | Versioned machine validation | SCHEMA-001–007 published |
| 6. Capability Boundaries | Logical responsibilities without deployables | SPEC-006 accepted |
| 7. Documentation | Cross-reference and review standard | SPEC-010 accepted |
| 8. Design System | Audit-visible information requirements | SPEC-009 reviewed |
| 9. Deployment Profiles | Informative MVP and evolution profiles | SPEC-020 published |
| 10. Platform Conformance | Declared implementation coverage (topology-agnostic) | SPEC-013 accepted by consumers |
| 11. Executable Canon | Validators, CI, indexes, release package | `validate_all.py` PASS on main |
| 12. Consumer Manifests | Measurable capability conformance | three example manifests + schema |
| 13. Demo Fixture | Deterministic positive/negative vectors | community-ai-lab fixtures validate |
| 14. Compatibility Policy | Evolution without silent breaks | SPEC-015 + ADR-011 accepted |
| 15. Trust Layer | Shared security/privacy model | SPEC-016–019 reviewed |
| 16. RFC Governance | Explicit status and approval rules | rfc-process.md adopted |

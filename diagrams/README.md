# Diagrams

| Diagram | Kind | Notes |
| --- | --- | --- |
| [lifecycle.md](lifecycle.md) | Logical | Canonical stage sequence |
| [domain-model.md](domain-model.md) | Logical + ownership | Domain ER + capability modules |

Physical deployment diagrams live in [architecture/overview.md](../architecture/overview.md) and [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md) / [SPEC-021](../specs/SPEC-021-preferred-application-stack.md). Keep logical diagrams free of container/orchestrator assumptions; preferred physical stack is Cloudflare + Supabase ([ADR-013](../adr/ADR-013-cloudflare-workers-public-host.md)).

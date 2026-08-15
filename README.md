# Autonomous Giving Platform Specifications

**Platform Specification v2.0.0** · Status: released canon · Owner: Autonomous Giving Incorporated

## Mission

Provide the authoritative, implementation-neutral definition of the Autonomous Giving Platform: how needs become verified impact through governed, attributable allocations. The [Platform Constitution](CONSTITUTION.md) is the highest-order normative document.

## Purpose and boundaries

This repository owns platform architecture, contracts, schemas, lifecycle, terminology, design standards, ADRs, and deterministic demo behavior. It contains **no application code, deployable API, frontend, backend, or infrastructure**. Implementation repositories consume immutable, versioned artifacts from here and link back rather than duplicating platform architecture.

## Architecture

The platform converts an observed `Need` into an auditable `Impact` through a canonical lifecycle. Intelligence may discover and recommend; governance authorizes; execution performs; evidence proves. See [SPEC-005](specs/SPEC-005-lifecycle.md) and the [lifecycle diagram](diagrams/lifecycle.md).

**Logical architecture** (capabilities) and **physical deployment** are independent for conformance. Fund Intel, Autonomous Giving, and Impact Relay are capabilities—not mandatory separate deployables. See [SPEC-002A](specs/SPEC-002A-architectural-principles.md) and [SPEC-006](specs/SPEC-006-capability-boundaries.md).

**Preferred physical stack** ([ADR-013](adr/ADR-013-cloudflare-workers-public-host.md)): **Cloudflare + Supabase**. Cloudflare provides Workers, static assets/Pages, Durable Objects when live coordination is needed, and Queues/Cron Triggers for deferred/webhook/retry work. Supabase provides Auth, PostgreSQL (canonical datastore), and Storage. every.org is the P0 donation-source connector. Stripe is **tenant/SaaS billing only** (never donation capture). Resend and OpenAI remain externals only if the product still requires them; Clerk likewise only if still required (Supabase Auth is preferred identity). [ADR-012](adr/ADR-012-render-first-platform.md) (Render-first) is **superseded**. Kubernetes, D1, and extra app hosts are **not** baseline.

## Reference deployment

The **public AGI suite** (workbench, Portfolio Signals public, Impact Relay public) and **application backends** (allocation middleware, webhooks, PostgreSQL-backed services) share one hosted path: GitHub → Cloudflare, with Supabase for Auth, Postgres, and Storage. Capabilities stay separate logically ([SPEC-002A](specs/SPEC-002A-architectural-principles.md)). Render is not the path.

```text
GitHub
  ↓
Cloudflare
├── Workers / Pages / static assets   (public suite + Worker APIs)
├── Durable Objects                   (only if live coordination is needed)
└── Queues / Cron Triggers            (deferred, webhook, retry work)
        ↓
Supabase
├── Auth
├── PostgreSQL                        (canonical application datastore)
└── Storage

External: every.org (P0 connector) · Stripe (tenant billing only) · Resend · OpenAI · Clerk
```

| Profile | Intent |
| --- | --- |
| A Demo | Static fixtures, no backend |
| **B MVP** | **Recommended:** Cloudflare + Supabase + every.org connector + optional Stripe billing/Resend/OpenAI |
| C Production | Optional Durable Objects, Queues, Cron, scale-out of the same modular unit |
| D Enterprise | Optional extraction, streaming, multi-region |

Full detail: [ADR-013](adr/ADR-013-cloudflare-workers-public-host.md), [SPEC-020](specs/SPEC-020-reference-deployment-profiles.md), [SPEC-021](specs/SPEC-021-preferred-application-stack.md), [implementation guidance](docs/implementation-guidance.md), [onboarding](docs/onboarding.md). SPEC-020/021 recommended diagrams match ADR-013; residual Render text is labeled historical.

**No Kubernetes, event broker, service mesh, Render app, or D1 is required for a conformant public suite or MVP.**

## Repository layout

| Path | Authority |
| --- | --- |
| `specs/` | Normative platform specifications |
| `adr/` | Architectural decisions and their context |
| `contracts/`, `schemas/`, `events/` | Public data and event contracts |
| `glossary/` | Canonical platform vocabulary |
| `architecture/`, `diagrams/` | Architecture views and diagrams |
| `demo/`, `roadmap/`, `docs/` | Demo canon, delivery sequence, contribution standards |

## Indices

- [Specification index](specs/README.md)
- [ADR index](adr/README.md)
- [Event library](events/README.md)
- [Contract library](contracts/README.md)
- [Schema library](schemas/README.md)
- [Glossary](glossary/README.md)
- [Platform traceability matrix](docs/traceability.md)
- [Generated machine-readable catalog](generated/catalog.json)
- [RFC process](docs/rfc-process.md)
- [Repository governance](docs/repository-governance.md)
- [Implementation guidance](docs/implementation-guidance.md)
- [Engineering onboarding](docs/onboarding.md) (Cloudflare + Supabase)
- [Recovery runbook](docs/recovery-runbook.md)
- [Next recommended implementation steps](roadmap/specification-roadmap.md#next-recommended-steps-implementation)
- [Financial ledger invariants](specs/SPEC-023-financial-ledger-invariants.md) (tracking ledger; AGI does not process donations)
- [Donation-source connectors](specs/SPEC-026-donation-source-connectors.md) · [Impact loop](specs/SPEC-027-impact-loop.md) · [ADR-015](adr/ADR-015-donation-tracking-money-boundary.md)
- [AGI control plane](specs/SPEC-028-agi-control-plane.md) · [ADR-014](adr/ADR-014-agi-control-plane.md)
- [Sprint remaining work](docs/sprint-remaining-work-donation-tracking.md) (informative; not READY)
- [Allocation middleware design](docs/superpowers/specs/2026-08-03-allocation-middleware-design.md) (informative; Worker/`am_*` OBSERVED in product repo files)
- [Allocation middleware MVP plan](docs/superpowers/plans/2026-08-03-allocation-middleware.md) (historical checklist; implemented in Portofolio-Signals / Fund-Intel)
- [Hacker Dojo pilot hosting status](docs/superpowers/plans/2026-08-03-hacker-dojo-pilot-hosting.md) (2026-08-07 implementation status)
- [**Implementation progress**](docs/superpowers/IMPLEMENTATION-PROGRESS.md) — pilot + suite onboarding map (**current as of 2026-08-08 evening**)
- [Suite continuation plan](docs/superpowers/plans/2026-08-08-suite-continuation.md) — pack activate, people MFA, pilot #73/#74

## Executable validation

```bash
pip install -r requirements-validation.txt
python validation/validate_all.py
```

This command is the merge gate: it validates metadata, references, schemas, examples, lifecycle, ownership, terminology, conformance manifests, and the Community AI Lab demo fixture. See [validation/README.md](validation/README.md).

Machine-readable indexes for portals and explorers live under [`generated/`](generated/). Consumer conformance examples: [`conformance/examples/`](conformance/examples/). Pin a release package from `dist/` (built by `python validation/package_release.py`).

## Contribution workflow

1. Open or update a SPEC before changing a normative contract.
2. Record material architectural choices as an ADR using the Nygard format.
3. Update affected schemas, events, glossary terms, examples, and references in one change.
4. Run `python validation/validate_all.py` (must report `PASS`); see [validation](docs/validation.md).
5. Obtain review from the listed owner and one consuming implementation repository.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the required change and review process.

## Versioning

Platform releases use semantic versioning. A major version may change a required contract or lifecycle invariant; a minor version adds backward-compatible authority; a patch clarifies without changing normative behavior. Details: [SPEC-012](specs/SPEC-012-versioning.md).

## Implementation repositories

[Portofolio-Signals](https://github.com/scrimshawlife-ctrl/Portofolio-Signals) (Fund-Intel / Portfolio Signals), Impact Relay, and Autonomous Giving Incorporated implement these artifacts as **capabilities** (optionally co-located). They must identify the consumed specification version, validate produced messages against the linked schema, and retain platform references in their own documentation.

The [implementation consumption guide](docs/implementation-consumption.md) and [implementation guidance](docs/implementation-guidance.md) define adoption and the modular-monolith-first path.

Runtime evidence lives in implementation repos — especially Portofolio-Signals [`docs/CURRENT-STATE.md`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/CURRENT-STATE.md) — not here. See [implementation progress](docs/superpowers/IMPLEMENTATION-PROGRESS.md).

### Allocation middleware (informative)

Client product direction: transaction-light pots → allocate → proof → packet (canonical connector **every.org**). Design and plans live under `docs/superpowers/`. First implementation: [Portofolio-Signals `services/allocation-middleware/`](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/tree/main/services/allocation-middleware) (Hacker Dojo pilot seed; live webhook operator-owned). This specs repo remains free of application code.

### Suite commercial onboarding (informative)

People (C) → client shell (B) → document pack → second tenant (D) → allocation pilot. Document pack phase 1 **code** is on Portofolio-Signals main (#104); platform OBSERVED still operator. HD data login-gated; Ed is HD director only. Continuation: [suite continuation plan](docs/superpowers/plans/2026-08-08-suite-continuation.md). Hub: [SUITE-ONBOARDING.md](https://github.com/scrimshawlife-ctrl/Portofolio-Signals/blob/main/docs/SUITE-ONBOARDING.md).

# Autonomous Giving Platform Constitution

| Version | 1.1.0 |
| --- | --- |
| Owner | Platform Architecture |
| Status | Accepted |

## Mission

The Autonomous Giving Platform converts evidenced needs into governed, attributable impact. This Constitution is the highest-order normative document in this repository. Where an artifact conflicts with it, the Constitution prevails until formally amended by a major platform release.

## Vocabulary and lifecycle

The [canonical glossary](glossary/README.md) is the sole authority for platform terms. The lifecycle is immutable: `Need → Signal → Opportunity → Recommendation → Approval → Allocation → Execution → Evidence → Receipt → Verification → Impact`. `Notification` and `TimelineEvent` are projections of lifecycle history, not alternate stages.

## Repository responsibilities

This repository owns specifications, architecture, ADRs, contracts, schemas, event definitions, terminology, design-system requirements, the canonical demo, documentation standards, versioning, and conformance. It does not own business logic, UI or API implementations, databases, deployment topology, or operational infrastructure.

## Platform philosophy

The platform separates discovery, authority, action, and proof. Intelligence observes and recommends; governance decides; execution fulfils; evidence and verification substantiate; transparency publishes history. Evidence and historical records are append-only.

## Capability Boundaries

Logical capabilities are architectural boundaries. They define responsibility, ownership, and contract edges.

They are **not** deployment requirements.

Fund Intel, Autonomous Giving, and Impact Relay are **capabilities**. An implementation remains conformant whether those capabilities run in one process (modular monolith), a modular application, or distributed processes. Capability boundaries SHALL NOT imply separate repositories, containers, databases, orchestrators, or network partitions.

## Deployment Independence

Platform specifications define **capabilities**. Implementations choose **deployment**.

Logical architecture and physical deployment are independent concepts. Specifications remain conformant regardless of topology. The recommended default is a modular monolith; distributed infrastructure is an optional future profile, not the reference shape of the platform.

The **preferred** physical path for new product implementations is documented as informative guidance (Cloudflare + Supabase; see [ADR-013](adr/ADR-013-cloudflare-workers-public-host.md)). [ADR-012](adr/ADR-012-render-first-platform.md) (Render-first) is superseded. Preference does not condition conformance class.

## Immutable principles

1. Intelligence never allocates.
2. Governance never fabricates evidence.
3. Transparency never edits history.
4. Every impact claim has provenance.
5. Every allocation has evidence.
6. Every capability owns one responsibility.
7. Human approval gates allocations for the MVP.
8. Implementation repositories SHALL conform to the published artifacts they declare.
9. Capability boundaries are architectural, not deployment, requirements.
10. Deployment topology is an implementation choice, not a platform mandate.

## Ownership and governance

Every normative artifact names one accountable owner. Platform Architecture resolves cross-domain conflicts. Material decisions require an ADR; accepted authority changes only through an amended or superseding artifact with consumer review. See [repository governance](docs/repository-governance.md).

Repository ownership of implementation products (Fund Intel, Autonomous Giving Incorporated, Impact Relay) is unchanged by deployment topology.

## Versioning and conformance

Releases use semantic versioning; breaking invariant or contract changes require a major version. Implementations declare conformance at Required, Recommended, Optional, or Experimental level and name every implemented SPEC, CONTRACT, and EVENT. See [SPEC-012](specs/SPEC-012-versioning.md) and [SPEC-013](specs/SPEC-013-repository-conformance.md). Deployment profile does not affect conformance class.

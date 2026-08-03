# Autonomous Giving Platform Specifications

**Platform Specification v1.0** · Status: proposed canon · Owner: Autonomous Giving Incorporated

## Mission

Provide the authoritative, implementation-neutral definition of the Autonomous Giving Platform: how needs become verified impact through governed, attributable allocations. The [Platform Constitution](CONSTITUTION.md) is the highest-order normative document.

## Purpose and boundaries

This repository owns platform architecture, contracts, schemas, lifecycle, terminology, design standards, ADRs, and deterministic demo behavior. It contains **no application code, deployable API, frontend, backend, or infrastructure**. Implementation repositories consume immutable, versioned artifacts from here and link back rather than duplicating platform architecture.

## Architecture

The platform converts an observed `Need` into an auditable `Impact` through a canonical lifecycle. Intelligence may discover and recommend; governance authorizes; execution performs; evidence proves. See [SPEC-005](specs/SPEC-005-lifecycle.md) and the [lifecycle diagram](diagrams/lifecycle.md).

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

Fund Intel, Impact Relay, and future services implement these artifacts. They must identify the consumed specification version, validate produced messages against the linked schema, and retain platform references in their own API documentation.

The [implementation consumption guide](docs/implementation-consumption.md) defines the required adoption and migration path.

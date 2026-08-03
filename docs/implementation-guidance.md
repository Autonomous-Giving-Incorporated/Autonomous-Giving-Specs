# Implementation guidance

Practical guidance for product teams implementing the Autonomous Giving Platform. Normative rules remain in SPECs; this document is informative.

## Reference implementation shape

**Modular monolith by default** ([SPEC-002A](../specs/SPEC-002A-architectural-principles.md), [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md) Profile B).

```text
GitHub Pages → Single backend → Capability modules → PostgreSQL + object storage
```

| Layer | Recommendation |
| --- | --- |
| Frontend | GitHub Pages (or equivalent static host) |
| Backend | Single application executable |
| Language | Implementation choice |
| Database | One PostgreSQL primary |
| Storage | S3-compatible object storage for evidence binaries |
| Worker | Background process (same codebase preferred) |
| Auth | OIDC when required |

**Not required for MVP:** Kubernetes, event broker, service mesh, multiple databases, per-capability containers.

## Capability modules

Implement Fund Intel, Autonomous Giving, and Impact Relay as **modules** with:

- clear package/module boundaries
- owned contracts at the edge
- no silent writes across capability private state

Co-location does not merge responsibilities.

## Contracts and events without brokers

- Call module APIs in-process for MVP.
- Persist events to the database for audit and replay.
- Optionally enqueue background work for email/webhooks.
- Introduce a broker only when operational criteria justify it.

Events describe **what happened**, not **which product hosts the queue**.

## Optional evolution

| Phase | When | What changes |
| --- | --- | --- |
| 1 Modular monolith | Default | Single deployable, modular code |
| 2 Workers | Long-running or retryable I/O | Separate worker process, same DB |
| 3 Extract capability | Decision matrix below | One capability becomes its own deployable |
| 4 Distributed platform | Multiple extracted units | Network transports between capabilities |
| 5 Enterprise | Org-scale ops | Multi-region, streaming, orchestration as needed |

## Decision matrix: when to extract a service

Extract a capability into a separately deployable **service** only when one or more hold:

| Criterion | Example signal |
| --- | --- |
| Independent scaling | One capability saturates compute while others idle |
| Independent deployment | Different release cadence with real cost to coupling |
| Separate teams | Distinct on-call and ownership that needs hard isolation |
| Operational isolation | Different data residency or compliance plane |
| Fault isolation | Failure domain must not take down the whole MVP |

**If none apply → remain a modular monolith.**

## When NOT to extract

- “Microservices are modern”
- Premature optimization without load evidence
- To match a three-box diagram
- Before contracts and lifecycle tests are green
- Before a single-database MVP has proven the product loop

## Migration path

1. Pin [Specs v1.x](https://github.com/scrimshawlife-ctrl/Autonomous-Giving-Specs/releases) and ship a conformance manifest.
2. Implement modules behind capability boundaries.
3. Validate with Community AI Lab fixtures.
4. Add workers for async side effects.
5. Extract only with a recorded operational justification (ADR in the product repo is sufficient; platform ADR if contracts change).

## Related docs

- [implementation-consumption.md](implementation-consumption.md) — pin and replace duplicates
- [SPEC-013](../specs/SPEC-013-repository-conformance.md) — conformance (topology-agnostic)
- [SPEC-020](../specs/SPEC-020-reference-deployment-profiles.md) — profiles A–D

---
id: SPEC-030
title: Mission Intelligence Metrics
version: 0.1.0
status: proposed
authority: normative
owner: Fund Intel
related_specs:
- SPEC-003
- SPEC-005
- SPEC-006
- SPEC-017
- SPEC-018
- SPEC-029
related_adrs:
- ADR-003
- ADR-006
related_contracts: []
---

# SPEC-030: Mission Intelligence Metrics
| Version | 0.1.0 | Owner | Fund Intel | Status | Proposed |
| --- | --- | --- | --- | --- | --- |
| Dependencies | SPEC-003, SPEC-005, SPEC-006, SPEC-017, SPEC-018, SPEC-029 | Related ADRs | ADR-003, ADR-006 | Related contracts | None |

## Purpose

Define versioned semantics and governance for derived mission-intelligence metrics. This proposed framework intentionally defines no arbitrary scoring formula or universal outcome comparison.

## Required output semantics

Every metric output MUST retain the metric identifier, calculation-policy version, produced time, tenant/project scope, retained input references, source provenance, epistemic classification, and reproducibility information. Outputs MUST distinguish `OBSERVED`, `INFERRED`, `SPECULATIVE`, and `NOT_COMPUTABLE`.

If any required input is absent, weak, stale, conflicting, unauthorized, or cannot be reproduced under the stated policy, the output MUST be `NOT_COMPUTABLE`. A model confidence score is not Evidence Confidence and MUST NOT be substituted for it.

Metrics are derived intelligence. They MUST NOT grant authority, create Approval, trigger Allocation or Execution, or rewrite historical metric results when a policy changes. A changed policy MUST produce a separately versioned output that remains traceable to its retained inputs.

## Initial metric family

| Metric | Meaning | Required semantic constraints |
| --- | --- | --- |
| **Opportunity Fit Score (OFS)** | Strength of an Opportunity’s match to the current Need and operating context. | Factors may include mission/Need alignment, eligibility, geography, funding size, timing, capacity, evidence availability, historical performance, and source confidence. Formula is implementation-defined until validated. |
| **Need Pressure Index (NPI)** | Intensity or urgency of a Need. | Inputs may include demand velocity, resource deficit, time sensitivity, population affected, Signal agreement, capacity/coverage, and trend direction. No input may be implied when it is absent. |
| **Evidence Completeness (EC)** | Completeness of lineage for an Allocation or related mission chain. | Components may include Execution, expenditure, program, outcome, Verification, and provenance completeness. |
| **Funding-to-Impact Latency (FIL)** | Elapsed duration from a configured approved funding/resource decision to verified Impact. | Policy MUST identify start and end timestamps; Recommendation time MUST NOT be mixed with Approval or Allocation time unless explicitly configured. |
| **Mission Yield (MY)** | Verified mission outcome relative to a constrained resource basis. | Policy MUST name outcome, resource basis, population/context, and comparability boundary. Heterogeneous outcomes MUST NOT be represented as universally comparable. |
| **Evidence Confidence (ECONF)** | Strength and classification of evidence supporting a Signal, Recommendation, Verification, or Impact. | Must retain source/provenance and distinguish, where supported: observed primary evidence, observed secondary evidence, self-reported, independently verified, inferred, and insufficient. |
| **Opportunity Realization Rate (ORR)** | Progression through a versioned cohort from qualified Opportunity toward realized, verified result. | Policy MUST state denominator, cohort definition, stage definitions, and version; example stages are recommendation, approved pursuit, Execution, funded/realized result, and verified Impact. |

## Calculation policy

1. Each implemented metric MUST have a named, versioned calculation policy that declares required inputs, admissible evidence, staleness handling, classification mapping, tenant/project applicability, and failure conditions.
2. A calculation policy MAY add a validated formula only when its inputs, rationale, and evaluation evidence are retained. This specification does not accept a formula by naming a metric.
3. Metrics MUST preserve underlying sources and distinguish observation from inference. Implementations MUST retain enough information to answer what evidence supported the result, what was observed versus inferred, which policy/model version produced it, when it was produced, whether a source was stale, which tenant/project it belongs to, and whether it can be reproduced.
4. Historical metric values MUST retain their original policy version and input references. Recalculation under a newer policy MUST create a distinct result, not silently replace history.

## Non-goals

This specification does not authorize automatic decisioning, set formulas, require forecasting, create a new datastore, or require an event or schema extension. Forecasting is later work only after sufficient validated tenant evidence exists.

## References

- [SPEC-003](SPEC-003-signals-stack.md) — advisory intelligence boundary
- [SPEC-018](SPEC-018-evidence-integrity-and-provenance.md) — evidence and provenance
- [SPEC-029](SPEC-029-mission-graph-and-learning-feedback.md) — mission projection and feedback relationship

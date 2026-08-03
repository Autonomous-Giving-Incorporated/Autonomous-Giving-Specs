# SPEC-002: Signals Stack

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Fund Intel |
| Status | Proposed |
| Dependencies | SPEC-003, SPEC-004 |
| Related ADRs | ADR-002 |
| Related contracts | CONTRACT-001, CONTRACT-002 |

## Purpose

Define how external observations become normalized `Signal` records and are evaluated into `Opportunity` records.

## Requirements

- Each signal records source, observed time, capture time, subject, confidence, and source provenance.
- Signals are immutable observations; assessment belongs to an opportunity or recommendation.
- Deduplication must preserve source records and publish a relationship rather than overwrite either signal.
- A consumer must treat a signal as untrusted until validation policy records its outcome.

## Non-goals

Source scraping, scoring models, and connector implementations are outside this repository.

## Rationale and references

Separating observation from judgement keeps recommendations explainable. See [EVENT-001](../events/EVENT-001-signal-detected.md), [EVENT-002](../events/EVENT-002-opportunity-created.md), and [ADR-002](../adr/ADR-002-signals-stack.md).

# SPEC-007: Deterministic Demo

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Platform Product |
| Status | Proposed |
| Dependencies | SPEC-004, SPEC-006, SPEC-008 |
| Related ADRs | ADR-009 |
| Related contracts | CONTRACT-001–007 |

## Purpose

Specify the canonical demo as a reproducible evidence chain, not an implementation.

## Requirements

The demo uses **Community AI Lab** and the sequence `Need → Recommendation → Approval → Allocation → Purchase → Evidence → Receipt → Verification → Impact`. It must use fixed example identifiers and amounts, show a human approval before allocation, and make each impact statement traceable to evidence.

## Non-goals

Live payments, live vendor integrations, and production data are not demo requirements.

## References

[Demo scenario](../demo/community-ai-lab.md) · [Deterministic Demo ADR](../adr/ADR-009-deterministic-demo.md)

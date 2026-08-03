---
id: CONTRACT-004
version: 1.0.0
status: accepted
authority: normative
title: Evidence
owner: Impact Relay
lifecycle_stage: Evidence
schema: ../schemas/evidence.json
producer: Impact Relay
consumer: Autonomous Giving
related_specs:
- SPEC-005
- SPEC-007
related_events:
- EVENT-007
---

# CONTRACT-004: Evidence

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Impact Relay |
| Producer / consumer | Impact Relay / Autonomous Giving |
| Schema | [evidence.json](../schemas/evidence.json) |

An immutable claim or artifact attributable to an Allocation. Required: `evidenceId`, `allocationId`, `type`, `uri`, `capturedAt`, `source`. URI is resolvable by an authorized verifier; `type` names the evidence medium. Published by [EVENT-007](../events/EVENT-007-evidence-attached.md).

Validation requires UUID identifiers, an RFC 3339 `capturedAt`, and a URI-formatted artifact location.

```json
{"evidenceId":"d6c2e191-3000-4000-8000-000000000001","allocationId":"c6c2e191-3000-4000-8000-000000000001","type":"delivery_photo","uri":"https://evidence.example/community-ai-lab/delivery-1","capturedAt":"2026-08-03T16:20:00Z","source":"Community AI Lab"}
```

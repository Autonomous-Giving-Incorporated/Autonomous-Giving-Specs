# CONTRACT-004: Evidence

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Evidence |
| Producer / consumer | Evidence / Verification, Transparency |
| Schema | [evidence.json](../schemas/evidence.json) |

An immutable claim or artifact attributable to an Allocation. Required: `evidenceId`, `allocationId`, `type`, `uri`, `capturedAt`, `source`. URI is resolvable by an authorized verifier; `type` names the evidence medium. Published by [EVENT-007](../events/EVENT-007-evidence-attached.md).

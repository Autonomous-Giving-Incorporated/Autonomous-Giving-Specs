---
id: EVENT-012
version: 1.0.0
status: accepted
authority: normative
title: CapabilityContextIssued
owner: Autonomous Giving
lifecycle_stage: Approval
producer: Autonomous Giving
consumers:
- Fund Intel
- Impact Relay
schema: ../schemas/auth-context.json
contract: CONTRACT-008
idempotency: eventId
related_specs:
- SPEC-008
- SPEC-016
- SPEC-019
- SPEC-028
related_contracts:
- CONTRACT-008
- CONTRACT-009
- CONTRACT-010
---

# EVENT-012: CapabilityContextIssued

| Producer | Autonomous Giving |
| --- | --- |
| Consumers | Fund Intel, Impact Relay |
| Schema | [CONTRACT-008](../contracts/CONTRACT-008-auth-context.md) |
| Stage / ordering | Approval / per `tokenId` (`jti`) |
| Idempotency | `eventId` |

Records that AGI issued a short-lived audience-specific capability context after authorization. Payload validates as AGI Auth Context. The event is the audit record; the wire token is a signed JWT wrapping these claims. Raw JWTs MUST NOT appear in this repository or in public logs. Example: `{"eventType":"CapabilityContextIssued","payload":{"tokenId":"jti-123","audience":"fund-intel"}}`.

Related: tenant identity [CONTRACT-009](../contracts/CONTRACT-009-tenant-project-context.md); route intent [CONTRACT-010](../contracts/CONTRACT-010-route-intent.md) is not sufficient without this context.

## Example payload

```json
{
  "issuer": "https://autogive.app",
  "subject": "user-123",
  "tokenId": "jti-123",
  "audience": "fund-intel",
  "client_id": "hacker-dojo",
  "tenant_id": "hacker-dojo",
  "project_id": "project-robotics",
  "roles": ["tenant_director"],
  "capabilities": ["allocation:approve"],
  "issuedAt": "2026-08-15T16:00:00Z",
  "expiresAt": "2026-08-15T16:10:00Z"
}
```

`https://autogive.app` is a documentary issuer example already used by CONTRACT-008. It is not a live receipt and is not a `workers.dev` URL.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition for control-plane JWT issuance. |

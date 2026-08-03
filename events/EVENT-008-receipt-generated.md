---
id: EVENT-008
version: 1.0.0
status: accepted
authority: normative
title: ReceiptGenerated
owner: Autonomous Giving
lifecycle_stage: Receipt
producer: Autonomous Giving
consumers:
- Impact Relay
schema: ../schemas/receipt.json
contract: CONTRACT-005
idempotency: eventId
related_specs:
- SPEC-005
- SPEC-008
related_contracts:
- CONTRACT-005
---

# EVENT-008: ReceiptGenerated

| Producer | Autonomous Giving |
| --- | --- |
| Consumers | Impact Relay |
| Schema | [CONTRACT-005](../contracts/CONTRACT-005-receipt.md) |
| Stage / ordering | Receipt / per `allocationId` |
| Idempotency | `eventId` |

Records a transaction receipt. Payload validates as Receipt. Example: `{"eventType":"ReceiptGenerated","payload":{"receiptId":"e6c2e191-3000-4000-8000-000000000001","amount":2500,"currency":"USD"}}`.


## Example payload

```json
{
  "receiptId": "e6c2e191-3000-4000-8000-000000000001",
  "allocationId": "c6c2e191-3000-4000-8000-000000000001",
  "amount": 2500,
  "currency": "USD",
  "issuedAt": "2026-08-03T16:25:00Z",
  "issuer": "Community Technology Supply"
}
```

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

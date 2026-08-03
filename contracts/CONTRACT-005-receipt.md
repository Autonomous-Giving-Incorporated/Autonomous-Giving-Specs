# CONTRACT-005: Receipt

| Field | Value |
| --- | --- |
| Version | 1.0.0 |
| Owner | Autonomous Giving |
| Producer / consumer | Autonomous Giving / Impact Relay |
| Schema | [receipt.json](../schemas/receipt.json) |

A transaction record for an execution. Required: `receiptId`, `allocationId`, `amount`, `currency`, `issuedAt`, `issuer`. The total cannot exceed the allocation without an explicit, separately governed amendment. Published by [EVENT-008](../events/EVENT-008-receipt-generated.md).

Validation requires UUID identifiers, a positive amount, ISO 4217 currency, and an RFC 3339 issue time.

```json
{"receiptId":"e6c2e191-3000-4000-8000-000000000001","allocationId":"c6c2e191-3000-4000-8000-000000000001","amount":2500,"currency":"USD","issuedAt":"2026-08-03T16:25:00Z","issuer":"Community Technology Supply"}
```

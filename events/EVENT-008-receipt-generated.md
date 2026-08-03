# EVENT-008: ReceiptGenerated

| Producer | Autonomous Giving |
| --- | --- |
| Consumers | Impact Relay |
| Schema | [CONTRACT-005](../contracts/CONTRACT-005-receipt.md) |
| Stage / ordering | Receipt / per `allocationId` |
| Idempotency | `eventId` |

Records a transaction receipt. Payload validates as Receipt. Example: `{"eventType":"ReceiptGenerated","payload":{"receiptId":"e6c2e191-3000-4000-8000-000000000001","amount":2500,"currency":"USD"}}`.

## Version history

| Version | Change |
| --- | --- |
| 1.0.0 | Initial canonical event definition. |

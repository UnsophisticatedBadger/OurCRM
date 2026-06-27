# US-056 — Cancel a Transaction

**Capability:** Transactions
**Status:** Not Done

## User Story

As a real estate agent, I want to cancel a transaction when a deal falls through, so that I can record the reason and keep the history without losing data.

## Dependencies

- US-052 — View Transaction Details

## Acceptance Criteria

1. A "Cancel Transaction" button in the transaction details view is visible for transactions in Under Contract or Pending status only
2. Clicking it opens a cancellation dialog with a required reason selector (Financing / Inspection / Appraisal / Buyer withdrew / Seller withdrew / Other) and an optional notes field
3. The dialog requires explicit confirmation before processing; dismissing the dialog leaves the transaction unchanged
4. Confirming records the cancellation date, selected reason, and optional notes, then sets the status to Cancelled
5. The cancellation date, reason, and notes are shown in the transaction details view after cancellation
6. The "Cancel Transaction" button is not shown for transactions already in Closed or Cancelled status
7. Cancellation data and Cancelled status persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@us053
Scenario: User cancels a transaction and sees the status change to Cancelled
  Given the user is viewing an Under Contract transaction
  When the user clicks "Cancel Transaction", selects reason "Financing", and confirms
  Then the transaction status is "Cancelled"
  And the cancellation date is shown in the details

@us053
Scenario: Cancellation reason is required
  Given the cancellation dialog is open
  When the user clicks Confirm without selecting a reason
  Then an inline error is shown and the transaction is not cancelled

@us053
Scenario: User dismisses the cancellation dialog and the transaction is unchanged
  Given the cancellation dialog is open
  When the user closes the dialog without confirming
  Then the transaction status is unchanged

@us053
Scenario: Cancellation details are visible in the transaction after cancellation
  Given the user cancels a transaction with reason "Inspection" and note "Roof damage found"
  When the user views the transaction details
  Then the reason "Inspection" and note "Roof damage found" are shown alongside the cancellation date

@us053
Scenario: Cancel button is not shown for Closed transactions
  Given a transaction is in "Closed" status
  When the user views its details
  Then the "Cancel Transaction" button is not present
```

## Manual Tests

**Story:** [US-056 — Cancel a Transaction](../docs/061-cancel-a-transaction.md)

### Cancel Transaction button visible on active transactions
1. Open any Under Contract or Pending transaction
2. Confirm "Cancel Transaction" button is visible

### User cancels a transaction with a reason
1. Click "Cancel Transaction"
2. Confirm the dialog opens with a reason selector and notes field
3. Select "Financing" as the reason
4. Confirm and verify the status changes to "Cancelled"
5. Confirm the cancellation date and reason appear in the details

### Reason is required before confirming
1. Open the cancellation dialog and click Confirm without selecting a reason
2. Confirm an inline error appears and the transaction is not cancelled
3. Select a reason and confirm it now proceeds

### Dismissing the dialog leaves the transaction unchanged
1. Open the cancellation dialog and then close it
2. Confirm the transaction status has not changed

### Cancellation details are shown in the transaction
1. Cancel a transaction with reason "Inspection" and note "Foundation issue"
2. Open the transaction details and confirm the reason, note, and cancellation date are visible

### Cancel button is hidden for Closed and already-Cancelled transactions
1. Open a Closed transaction — confirm "Cancel Transaction" is not shown
2. Open a Cancelled transaction — confirm the button is also not shown

### Cancellation persists after a restart
1. Cancel a transaction, close the application, and restart
2. Open the transaction and confirm it is still Cancelled with the correct reason and date

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_transaction_cancellation.py` |
| Manual tests | `tests/manual/transactions/cancel_transaction.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

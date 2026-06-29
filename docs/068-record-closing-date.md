# US-068 — Record Closing Date

**Capability:** Transactions
**Status:** Not Done

## User Story

As a real estate agent, I want to record the actual closing date when a deal closes, so that the transaction is marked complete, the commission is confirmed, and I can see how long the deal took from contract to close.

## Dependencies

- US-052 — View Transaction Details

## Acceptance Criteria

1. The transaction details view shows a "Record Closing Date" button for transactions in Under Contract or Pending status
2. Clicking it opens a form with: actual closing date (required; must be on or after the contract date), and an optional note
3. Saving records the actual closing date, sets the status to Closed, and — if sale price and commission percentage are present — shows the confirmed commission amount
4. After recording, the actual closing date and days from contract to close (calculated automatically) are shown in the transaction details
5. The "Record Closing Date" button is not shown for transactions already in Closed or Cancelled status
6. The Closed status and actual closing date persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@us051
Scenario: User records the closing date and the transaction moves to Closed
  Given the user is viewing a transaction in "Under Contract" status
  When the user clicks "Record Closing Date", enters today's date, and confirms
  Then the transaction status is "Closed"
  And the actual closing date is shown in the details

@us051
Scenario: Entering a closing date before the contract date shows a validation error
  Given a transaction has contract date 2026-07-01
  When the user enters actual closing date 2026-06-15 in the Record Closing Date form
  Then "Closing date must be on or after contract date" is shown

@us051
Scenario: Commission amount is confirmed when closing date is recorded
  Given a transaction has sale price 500000 and commission 3%
  When the user records the closing date
  Then the form shows "$500,000 × 3% = $15,000" as the confirmed commission

@us051
Scenario: Days from contract to close is calculated and shown
  Given a transaction has contract date 2026-06-01 and actual closing date 2026-07-15
  When the user opens the transaction details
  Then "44 days from contract to close" is shown

@us051
Scenario: Record Closing Date button is not shown on already-closed transactions
  Given a transaction is in "Closed" status
  When the user views its details
  Then the "Record Closing Date" button is not present
```

## Manual Tests

**Story:** [US-054 — Record Closing Date](../docs/057-record-closing-date.md)

### Record Closing Date button visible on active transactions
1. Open any Under Contract or Pending transaction
2. Confirm "Record Closing Date" button is visible

### User records the closing date and transaction moves to Closed
1. Click "Record Closing Date"
2. Enter today's date and click Save
3. Confirm the status changes to "Closed" and the actual closing date appears in the details

### Validation rejects dates before the contract date
1. Enter an actual closing date one week before the contract date
2. Confirm "Closing date must be on or after contract date" appears

### Commission is confirmed when closing is recorded
1. Record the closing date on a transaction with sale price and commission %
2. Confirm the calculated commission is shown in the form and saved to the transaction details

### Days from contract to close is calculated
1. Record a closing date on a transaction with a known contract date
2. Open the transaction details and confirm the days-to-close figure matches the manual calculation

### Button is hidden for closed and cancelled transactions
1. Open a Closed transaction — confirm "Record Closing Date" button is not present
2. Open a Cancelled transaction — confirm the same

### Closing status persists after a restart
1. Record the closing date on a transaction, close the application, and restart
2. Open the transaction and confirm it is still Closed with the correct actual closing date

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_record_closing_date.py` |
| Manual tests | `tests/manual/transactions/record_closing_date.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

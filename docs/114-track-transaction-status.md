# US-067 — Change Transaction Status

**Capability:** Transactions
**Status:** Not Done
**GitHub Issue:** #114

## User Story

As a real estate agent, I want to change a transaction's status to reflect where the deal stands, so that the list always shows an accurate picture of my active pipeline.

## Dependencies

- #76 — View Transaction Details

## Acceptance Criteria

1. The transaction details view allows changing the status by clicking the status field and selecting a new value from Under Contract, Pending, Closed, or Cancelled
2. Status can also be changed via right-click > Change Status from the transaction list without navigating to the details view
3. Selecting Closed from either UI redirects to the Record Closing Date flow (US-054); selecting Cancelled redirects to the Cancel Transaction flow (US-056)
4. The row's colour indicator in the list updates immediately after an Under Contract / Pending change
5. Status changes persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@us050
Scenario: User changes status from Under Contract to Pending in the details view
  Given the user is viewing a transaction with status "Under Contract"
  When the user clicks the status field and selects "Pending"
  Then the details view shows status "Pending"
  And the transaction list row shows the orange Pending indicator

@us050
Scenario: User right-clicks a transaction and changes its status from the list
  Given a transaction "123 Oak St Sale" with status "Under Contract" is in the list
  When the user right-clicks it and selects "Change Status" then "Pending"
  Then the row updates to "Pending" immediately without navigating away

@us050
Scenario: Status change updates the row colour immediately
  Given a transaction with status "Under Contract" (yellow) is in the list
  When the user changes its status to "Pending" via right-click
  Then the row indicator changes to orange immediately

@us050
Scenario: Selecting Closed from the status picker redirects to the closing date flow
  Given the user is changing a transaction's status
  When the user selects "Closed"
  Then the Record Closing Date dialog opens instead of applying the change directly

@us050
Scenario: Status change persists after an application restart
  Given the user has changed a transaction's status to "Pending"
  When the application is restarted and the user opens the Transactions section
  Then the transaction still shows status "Pending"
```

## Manual Tests

**Story:** [US-053 — Change Transaction Status](../docs/061-track-transaction-status.md)

### User changes status in the details view
1. Open any Under Contract transaction's details
2. Click the status field and select "Pending"
3. Confirm the details view now shows "Pending" with the orange indicator
4. Navigate to the list and confirm the row also shows "Pending"

### User changes status from the list without opening details
1. Right-click a transaction in the list and select "Change Status"
2. Select "Pending"
3. Confirm the row updates immediately without navigating away

### Selecting Closed redirects to the closing date flow
1. Right-click a transaction and select "Change Status" then "Closed"
2. Confirm the Record Closing Date dialog opens (not a direct status change)

### Selecting Cancelled redirects to the cancellation flow
1. Right-click a transaction and select "Change Status" then "Cancelled"
2. Confirm the Cancel Transaction dialog opens (not a direct status change)

### Status change persists after a restart
1. Change a transaction's status to "Pending"
2. Close the application and restart
3. Open the Transactions section and confirm the status is still "Pending"

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_transaction_status.py` |
| Manual tests | `tests/manual/transactions/transaction_status.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

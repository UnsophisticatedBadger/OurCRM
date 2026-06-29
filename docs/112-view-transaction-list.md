# 112 - View Transaction List

**Capability:** Transactions
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #112

## User Story

As a real estate agent, I want to see all my transactions in a sortable, filterable list, so that I can track what is in progress and see at a glance which deals are closing soon.

## Dependencies

- #74 — Create a New Transaction

## Acceptance Criteria

1. The Transactions section shows a table of all transactions with columns for property address, buyer, seller, transaction type, status, contract date, closing date, and sale price; sorted by closing date ascending (soonest first) by default
2. Status is color-coded: Under Contract=yellow, Pending=orange, Closed=green, Cancelled=grey
3. Transactions with a closing date within the next 7 days are highlighted with a warning indicator
4. Clicking a column header sorts by that column; clicking again reverses order
5. The list can be filtered by status: All / Under Contract / Pending / Closed / Cancelled
6. Double-clicking a transaction opens its details view
7. When no transactions exist, "No transactions yet" is shown with a "Create Your First Transaction" button
8. Sort column, sort direction, active filter, and scroll position are preserved when navigating away and back

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@story_72
Scenario: User with transactions sees them in the Transactions section
  Given transactions "123 Oak St Sale" (Under Contract) and "456 Elm Ave Lease" (Closed) exist
  When the user opens the Transactions section
  Then the list shows both transactions

@story_72
Scenario: Status column is color-coded
  Given transactions with Under Contract, Pending, Closed, and Cancelled statuses exist
  When the user views the transaction list
  Then Under Contract is yellow, Pending is orange, Closed is green, and Cancelled is grey

@story_72
Scenario: Transactions closing within 7 days show a warning indicator
  Given a transaction has a closing date 3 days from today
  When the user views the transaction list
  Then that transaction row shows a warning indicator

@story_72
Scenario: User with no transactions sees an empty state
  Given no transactions exist
  When the user opens the Transactions section
  Then "No transactions yet" is shown
  And a "Create Your First Transaction" button is visible

@story_72
Scenario: Status filter is preserved after navigating away and back
  Given the user has the "Under Contract" filter active
  When the user navigates to Contacts and returns to Transactions
  Then only Under Contract transactions are still shown
```

## Manual Tests

**Story:** [#75 — View Transaction List](../docs/057-view-transaction-list.md)

### User sees all transactions with correct columns
1. Create transactions with varied data
2. Open the Transactions section and confirm all transactions appear
3. Confirm the columns show property address, buyer, seller, type, status, contract date, closing date, and sale price
4. Confirm default sort is by closing date soonest first

### Status colors are correct
1. Create one transaction in each status
2. Confirm Under Contract is yellow, Pending is orange, Closed is green, Cancelled is grey

### Warning indicator appears for transactions closing soon
1. Create a transaction with a closing date 2 days from today
2. Confirm a warning indicator appears on that row in the list

### Empty state appears with no transactions
1. Open the app with no transactions
2. Confirm "No transactions yet" and the "Create Your First Transaction" button appear

### Sort by column
1. Click each column header and confirm the list re-sorts by that column
2. Click the same header again and confirm reverse order

### Filter by status
1. Select "Under Contract" from the status filter
2. Confirm only Under Contract transactions are shown
3. Select "All" and confirm all transactions reappear

### Filter and sort state persist after navigating away
1. Set the "Pending" status filter
2. Navigate to Contacts, then return to Transactions
3. Confirm the filter is still active

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_transaction_list.py` |
| Manual tests | `tests/manual/transactions/transaction_list.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

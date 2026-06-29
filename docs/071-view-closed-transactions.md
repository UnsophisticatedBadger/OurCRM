# US-071 — View Closed Transactions

**Capability:** Transactions
**Status:** Not Done

## User Story

As a real estate agent, I want to view all my closed transactions with commission totals, so that I can track my completed deals and measure my business performance over time.

## Dependencies

- US-054 — Record Closing Date

## Acceptance Criteria

1. A "Closed" option in the transaction list status filter shows only closed transactions, sorted by actual closing date newest-first
2. Each row shows property address, actual closing date, sale price, commission earned, and days from contract to close
3. A summary banner above the list shows total commission earned and average days to close for the currently visible transactions
4. A time period selector (All Time / This Year / This Month) filters the list and recalculates the summary banner accordingly
5. Double-clicking a closed transaction opens its full details view

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@us054
Scenario: Applying the Closed filter shows only closed transactions
  Given transactions "123 Oak St" (Closed) and "456 Elm Ave" (Under Contract) exist
  When the user selects "Closed" from the status filter
  Then only "123 Oak St" is shown in the list

@us054
Scenario: Summary banner shows correct total commission
  Given two closed transactions with commission $12,000 and $8,000 respectively
  When the user views closed transactions
  Then the banner shows total commission "$20,000"

@us054
Scenario: Filtering by This Year recalculates the banner
  Given one transaction closed this year (commission $15,000) and one last year (commission $10,000)
  When the user selects "This Year" from the time period selector
  Then the banner shows total commission "$15,000"

@us054
Scenario: Each row shows commission earned and days to close
  Given a closed transaction with commission $12,000 that took 30 days from contract to close
  When the user views the closed transactions list
  Then the row shows "$12,000" commission and "30 days"

@us054
Scenario: Double-clicking a closed transaction opens its details
  Given the user is viewing the closed transactions list
  When the user double-clicks "123 Oak St"
  Then the transaction details view opens for "123 Oak St"
```

## Manual Tests

**Story:** [US-057 — View Closed Transactions](../docs/057-view-closed-transactions.md)

### User filters the transaction list to show only closed transactions
1. Close a few transactions; leave others active
2. Select "Closed" from the status filter
3. Confirm only closed transactions appear, sorted by closing date newest-first

### Each row shows the right columns
1. View the closed transactions list
2. Confirm each row displays: property address, actual closing date, sale price, commission earned, and days to close

### Summary banner shows accurate totals
1. Close two transactions with known commissions
2. Confirm the banner shows the correct total commission and the average days to close

### Time period filter updates the banner
1. Close transactions in different months
2. Switch to "This Month" and confirm only this month's transactions appear
3. Confirm the banner recalculates for just those transactions

### Double-clicking opens the transaction details
1. Double-click a closed transaction in the list
2. Confirm the details view opens for that transaction
3. Navigate back and confirm the Closed filter is still active

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_closed_transactions.py` |
| Manual tests | `tests/manual/transactions/closed_transactions.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

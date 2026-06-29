# 119 - View Closed Transactions Report

**Capability:** Transactions
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #119

## User Story

As a real estate agent, I want to view a summary analytics report of my closed transactions, so that I can measure my business performance and track sales metrics over time.

## Dependencies

- #106 — View Closed Transactions
- #20 — Record Closing Date

## Acceptance Criteria

1. A Closed Transactions Report view shows: total sales volume, total commission earned, transaction count, average sale price, and average days to close for the selected period
2. A time period selector (This Month / This Quarter / This Year / All Time) filters all metrics to the selected period
3. Each metric shows a trend indicator (up / flat / down) compared to the equivalent previous period (e.g., This Month vs last month)
4. A commission breakdown panel shows: total commission, average commission per transaction, and commission as a percentage of total sales volume
5. When no closed transactions exist in the selected period, the report shows a "No closed transactions in this period" message

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@story_119
Scenario: User views report metrics for a period with closed transactions
  Given two closed transactions exist: "123 Oak St" at $400,000 with $12,000 commission and "456 Elm Ave" at $600,000 with $18,000 commission
  When the user opens the Closed Transactions Report
  Then total sales volume shows "$1,000,000"
  And total commission shows "$30,000"
  And transaction count shows "2"
  And average sale price shows "$500,000"

@story_119
Scenario: User changes the time period and all metrics update
  Given one transaction closed this year (commission $15,000) and one closed last year (commission $10,000)
  When the user selects "This Year" from the time period selector
  Then total commission shows "$15,000"
  And transaction count shows "1"

@story_119
Scenario: User sees the empty-period state when no transactions match
  Given no closed transactions exist in the current month
  When the user selects "This Month" from the time period selector
  Then the report shows "No closed transactions in this period"

@story_119
Scenario: Trend indicator shows improvement when this period exceeds the previous
  Given $20,000 total commission was earned last quarter and $30,000 this quarter
  When the user selects "This Quarter"
  Then the commission metric shows an upward trend indicator

@story_119
Scenario: Commission breakdown panel shows accurate figures
  Given two closed transactions with commissions $12,000 and $18,000 on volumes $400,000 and $600,000
  When the user views the commission breakdown panel
  Then total commission shows "$30,000"
  And average commission per transaction shows "$15,000"
  And commission as a percentage of volume shows "3%"
```

## Manual Tests

**Story:** [#107 — View Closed Transactions Report](../docs/033-view-closed-transactions-report.md)

### User opens the report and sees accurate metrics
1. Close two transactions with known sale prices and commissions (e.g., $400k / $12k and $600k / $18k)
2. Open the Closed Transactions Report
3. Confirm total sales volume, total commission, transaction count, and average sale price all match hand-calculated values
4. Confirm average days to close is correct based on the actual close dates

### User changes the time period and metrics update
1. Close one transaction this month and one the previous month
2. Open the Closed Transactions Report
3. Select "This Month" and confirm only the current month's transaction is reflected
4. Select "All Time" and confirm both transactions are included

### User sees the empty-period state
1. Select a time period that contains no closed transactions
2. Confirm the "No closed transactions in this period" message is shown and no metrics are displayed

### User reads the trend indicators
1. Close more transactions this quarter than last quarter
2. Select "This Quarter"
3. Confirm the transaction count and relevant metrics show an upward trend indicator
4. Confirm a period where metrics declined shows a downward indicator

### User reviews the commission breakdown panel
1. Close two transactions with different commission rates
2. Confirm total commission, average commission per transaction, and commission-as-percentage-of-volume are all displayed and accurate

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_transaction_report.py` |
| Manual tests | `tests/manual/transactions/transaction_report.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

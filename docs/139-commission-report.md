# 139 - Commission Report

**Capability:** transactions
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #139
**Priority:** Post-MVP

## User Story
As an agent, I want a report of my commission earnings by period, property type, and source, so that I can track my income and plan my finances.

## Dependencies
- #73 — Mark Property as Sold
- #74 — Create a New Transaction

## Acceptance Criteria
1. A Commission Report is accessible from the Transactions section; it shows for the selected period: total commission earned from closed transactions
2. A date range filter controls the period; the report re-calculates on change
3. The report distinguishes between earned commission (closed transactions) and pending commission (transactions in progress)
4. The report breaks down commission by property type (Residential, Commercial, Land, etc.)
5. The report breaks down commission by lead source (Zillow, Referral, Walk-in, etc.)
6. The report shows average commission per closed transaction for the period
7. A trend chart plots total commission by month within the selected period
8. The full report data can be exported to CSV or PDF

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@story_139
Scenario: Report shows total earned and pending commission for the period
  Given two closed transactions with $10,000 commission each and one in-progress transaction with $8,000 commission
  When the user opens the Commission Report for the current period
  Then earned commission shows $20,000 and pending commission shows $8,000

@story_139
Scenario: Date range filter updates the report
  Given transactions with commission exist across multiple months
  When the user changes the date range to last quarter
  Then the report recalculates using only transactions closed in that quarter

@story_139
Scenario: Commission is broken down by property type
  Given closed transactions include one Residential and one Commercial property
  When the user views the Commission Report
  Then the report shows separate commission totals for Residential and Commercial

@story_139
Scenario: Average commission per transaction is calculated correctly
  Given three closed transactions with commissions of $5,000, $10,000, and $15,000
  When the user views the report
  Then the average commission per transaction shows $10,000

@story_139
Scenario: Report data can be exported to CSV
  Given the Commission Report is displaying data
  When the user clicks "Export to CSV"
  Then a CSV file is saved containing the report data

@story_139
Scenario: Report can be exported to PDF
  Given the Commission Report is displaying data
  When the user clicks "Export to PDF"
  Then a PDF file is saved containing the report including charts
```

## Manual Tests
**Story:** [#35 — Commission Report](../docs/128-commision-report.md)

### Report shows correct earned and pending commission
1. Open the Commission Report for the current period
2. Cross-check the totals against the Transactions list manually
3. Verify earned (closed) and pending (in-progress) are shown separately

### Date range filter updates the totals
1. Change the date range to last year
2. Verify the totals update to reflect only that period

### Breakdown by property type
1. Ensure at least two different property types exist in closed transactions
2. Verify the report shows a separate total for each type

### Trend chart plots commission by month
1. View the trend chart in the report
2. Verify each month within the selected range has a bar or data point

### Export to CSV
1. Click "Export to CSV"
2. Open the file and verify it contains all report data including earned, pending, and breakdowns

### Export to PDF
1. Click "Export to PDF"
2. Open the PDF and verify it contains the report data and trend chart

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_commission_report.py` |
| Manual tests | `tests/manual/transactions/commission-report.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

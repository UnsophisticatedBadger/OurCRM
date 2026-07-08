# 95 - Lead Conversion Report

**Capability:** leads
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #95
**Priority:** Post-MVP

## User Story
As an agent, I want a report showing my lead conversion rates, so that I can measure my sales performance and identify where leads are dropping off.

## Dependencies
- #67 — Mark Lead as Converted
- #69 — Track Conversion Rate

## Acceptance Criteria
1. A Lead Conversion Report is accessible from the Leads section; it shows for the selected period: total leads, converted leads, and conversion rate as a percentage
2. A date range filter controls the period; the report re-calculates on change
3. The report breaks down conversion rate by lead source (Zillow, Referral, Walk-in, etc.)
4. The report shows average time to convert in days (from lead creation to conversion date)
5. A trend chart plots conversion rate over time within the selected period (weekly or monthly buckets)
6. The report can be compared against a previous period of equal length; both periods are shown side-by-side
7. The full report data can be exported to CSV or PDF

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@story_95
Scenario: Report shows total leads, converted leads, and conversion rate for the period
  Given 10 leads were created this month and 3 were converted
  When the user opens the Lead Conversion Report with the current month selected
  Then the report shows: Total leads: 10, Converted: 3, Conversion rate: 30%

@story_95
Scenario: Date range filter updates the report
  Given leads and conversions exist across multiple months
  When the user changes the date range to last month
  Then the report recalculates using only leads from last month

@story_95
Scenario: Conversion rate is broken down by lead source
  Given converted leads exist from Zillow and Referral sources
  When the user views the Lead Conversion Report
  Then the report shows a separate conversion rate for each source

@story_95
Scenario: Average time to convert is calculated correctly
  Given two leads were converted: one after 10 days and one after 20 days
  When the user views the report
  Then the average time to convert shows 15 days

@story_95
Scenario: Report data can be exported to CSV
  Given the Lead Conversion Report is displaying data
  When the user clicks "Export to CSV"
  Then a CSV file is saved containing the report data

@story_95
Scenario: Report can be exported to PDF
  Given the Lead Conversion Report is displaying data
  When the user clicks "Export to PDF"
  Then a PDF file is saved containing the report including charts
```

## Manual Tests
**Story:** [#32 — Lead Conversion Report](../docs/077-lead-conversion-report.md)

### Report shows correct totals and conversion rate
1. Open the Lead Conversion Report for the current month
2. Count leads and conversions manually from the Leads list
3. Verify the report totals and percentage match

### Date range filter recalculates the report
1. Change the date range to last quarter
2. Verify the totals update to reflect only that period

### Conversion rate by source is shown
1. Ensure leads from at least two different sources have been converted
2. Verify the report shows a separate row or segment for each source

### Period comparison
1. Enable period comparison in the report
2. Verify both the current and previous periods are shown side-by-side

### Export to CSV
1. Click "Export to CSV"
2. Open the file and verify it contains all report data rows

### Export to PDF
1. Click "Export to PDF"
2. Open the PDF and verify it contains the report data and trend chart

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_conversion_report.py` |
| Manual tests | `tests/manual/leads/lead-conversion-report.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

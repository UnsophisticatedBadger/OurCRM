# US-041 — Track Conversion Rate

**Capability:** Leads
**Status:** Not Done

## User Story

As a real estate agent, I want to see my lead conversion rate, so that I can measure how effectively I turn leads into clients and identify which lead sources perform best.

## Dependencies

- US-039 — Mark Lead as Converted
- US-040 — View Converted Leads

## Acceptance Criteria

1. The Leads section shows a summary bar: "[X] leads total — [Y] converted ([Z]%)"
2. The summary bar can be filtered by time period: All Time, This Year, This Month
3. A per-source breakdown lists each lead source with its own conversion rate
4. The summary bar updates immediately when a lead is converted without requiring a page refresh
5. With no conversions the bar shows "0 converted (0%)" without showing an error

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@us039
Scenario: Conversion rate is calculated correctly
  Given 10 leads exist and 3 have been converted
  When the user views the Leads section
  Then the summary bar shows "10 leads total — 3 converted (30%)"

@us039
Scenario: Filtering by This Month shows only this month's figures
  Given 2 leads were converted this month and 3 were converted last year
  When the user selects "This Month" in the summary bar filter
  Then the summary bar shows 2 converted with the corresponding rate

@us039
Scenario: Per-source breakdown shows each source's conversion rate
  Given 4 Zillow leads exist with 2 converted, and 6 Referral leads exist with 3 converted
  When the user views the per-source breakdown
  Then Zillow shows 50% and Referral shows 50%

@us039
Scenario: Summary bar updates immediately after a conversion
  Given the user is viewing the Leads section with 9 leads and 2 converted (22%)
  When the user converts a third lead
  Then the summary bar immediately shows "10 leads total — 3 converted (30%)"

@us039
Scenario: Summary bar shows zero gracefully with no conversions
  Given leads exist but none have been converted
  When the user views the Leads section
  Then the summary bar shows "0 converted (0%)" without an error
```

## Manual Tests

**Story:** [US-041 — Track Conversion Rate](../docs/047-track-conversion-rate.md)

### Summary bar shows correct totals and rate
1. Create 10 leads and convert 3
2. Navigate to the Leads section
3. Confirm the bar shows "10 leads total — 3 converted (30%)"

### Time period filter changes the rate
1. Convert 2 leads this month and note that older conversions exist
2. Select "This Month" in the filter
3. Confirm only this month's 2 conversions are counted in the rate
4. Switch to "All Time" and confirm the full count reappears

### Per-source breakdown shows each source
1. Create leads from at least two different sources (e.g., Zillow and Referral)
2. Convert some from each source
3. View the per-source breakdown
4. Confirm each source shows its own conversion count and percentage

### Rate updates immediately after marking a lead converted
1. Note the current rate displayed in the summary bar
2. Open a lead, mark it as converted, and confirm
3. Return to the Leads section and confirm the summary bar already reflects the new conversion without needing to reload

### Zero conversions handled gracefully
1. Create leads but do not convert any
2. Confirm the summary bar shows "0 converted (0%)" with no error or blank state

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_conversion_rate.py` |
| Manual tests | `tests/manual/leads/conversion_rate.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

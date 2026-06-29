# US-052 — View Converted Leads

**Capability:** Leads
**Status:** Not Done

## User Story

As a real estate agent, I want to view all my converted leads in one place, so that I can track my wins and spot conversion patterns over time.

## Dependencies

- US-039 — Mark Lead as Converted

## Acceptance Criteria

1. A "Converted" option in the lead list status filter shows only converted leads, sorted by conversion date newest-first
2. Each converted lead row shows name, conversion date, and days from lead creation to conversion
3. A summary banner above the list shows total converted, converted this month, and converted this year
4. Double-clicking a converted lead opens its full details view

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@us038
Scenario: Applying the Converted filter shows only converted leads
  Given leads "Sara Lee" (converted) and "Bob Kim" (active) exist
  When the user selects "Converted" from the status filter
  Then only "Sara Lee" is shown in the list

@us038
Scenario: Converted leads are sorted by conversion date newest-first
  Given "Sara Lee" was converted yesterday and "Jane Park" was converted today
  When the user views converted leads
  Then "Jane Park" appears above "Sara Lee"

@us038
Scenario: Summary banner shows correct conversion counts
  Given 5 leads have been converted in total, 2 this month, 4 this year
  When the user views the converted leads list
  Then the banner shows "5 total · 2 this month · 4 this year"

@us038
Scenario: Double-clicking a converted lead opens its details
  Given the user is viewing the converted leads list
  When the user double-clicks "Sara Lee"
  Then the lead details view opens for "Sara Lee"
```

## Manual Tests

**Story:** [US-040 — View Converted Leads](../docs/040-view-converted-leads.md)

### User filters the lead list to show only converted leads
1. Convert a few leads, leaving others active
2. Select "Converted" from the status filter
3. Confirm only converted leads appear and active leads are hidden

### Converted leads are sorted by conversion date
1. Convert three leads on different days
2. Apply the Converted filter
3. Confirm the most recently converted lead appears first

### Each row shows name, conversion date, and days to conversion
1. View the converted leads list
2. Confirm each row displays the lead name, the conversion date, and the number of days between creation and conversion

### Summary banner shows accurate totals
1. Convert leads across different months
2. View the converted leads list
3. Confirm the banner shows the correct total count, this month's count, and this year's count

### Double-clicking opens the lead's details
1. Double-click a converted lead in the list
2. Confirm the details view opens and shows the conversion date
3. Navigate back and confirm the filter is still active

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_converted_leads.py` |
| Manual tests | `tests/manual/leads/converted_leads.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

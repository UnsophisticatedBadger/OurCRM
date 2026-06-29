# 29 - Advanced Search Filters

**Capability:** shell
**Milestone:** v0.2.0 — Secure Shell
**Status:** Not Done
**GitHub Issue:** #29
**Priority:** Post-MVP

## User Story
As an agent, I want to filter search results by date ranges, numeric ranges, and custom criteria, so that I can find exactly the records I need without scrolling through unrelated results.

## Dependencies
- #52 — Search Contacts
- #58 — Search Contacts Globally

## Acceptance Criteria
1. A "Filters" panel is accessible from search results across Contacts, Leads, Properties, and Transactions
2. Date filters support both absolute ranges (e.g. Created between 1 Jan and 31 Jan) and relative presets (Last 7 days, Last 30 days, Last 90 days, This year)
3. A "Last activity" date filter supports relative presets (e.g. Last contacted more than 6 months ago)
4. Numeric range filters are available on applicable fields: budget range on leads, price range on properties and transactions
5. Filters for any user-defined custom fields are available when custom fields have been defined on a record type
6. Multiple filters can be active simultaneously; all filters are applied with AND logic
7. A "Clear All Filters" button removes all active filters and shows unfiltered results
8. Active filter combinations can be saved as a named saved search (per #81) from the Filters panel

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_37
Scenario: Absolute date range filter returns only records created in that range
  Given contacts were created both inside and outside of January
  When the user sets a "Created" date filter to 1 Jan – 31 Jan
  Then only contacts created in January are shown

@story_37
Scenario: Relative date preset "Last 30 days" returns recent records
  Given contacts were created 10 days ago and 60 days ago
  When the user selects the "Last 30 days" date preset
  Then only the contact created 10 days ago is shown

@story_37
Scenario: Numeric budget range filter on leads
  Given leads exist with budgets of $200k, $400k, and $600k
  When the user sets a budget filter of $300k–$500k
  Then only the $400k lead is shown

@story_37
Scenario: Multiple active filters are combined with AND logic
  Given leads with "Hot" status exist at various budget levels
  When the user sets status = "Hot" and budget = "$300k–$500k"
  Then only Hot leads within the budget range are shown

@story_37
Scenario: Clear All Filters removes all active filters
  Given two filters are active
  When the user clicks "Clear All Filters"
  Then all records are shown with no filters applied
```

## Manual Tests
**Story:** [#168 — Advanced Search Filters](../docs/137-search-filters.md)

### Absolute date range filter shows only matching records
1. Set the "Created" date filter to a specific date range
2. Verify only records created within that range appear

### Relative date preset applies correctly
1. Select "Last 30 days" from the date filter preset menu
2. Verify only records created or modified in the past 30 days appear

### Numeric range filter on leads
1. Set a budget range filter on the Leads list
2. Verify only leads within the specified budget range appear

### Multiple filters applied together
1. Set a status filter and a date filter simultaneously
2. Verify only records matching both criteria appear

### Clear All Filters resets the view
1. Apply two or more filters
2. Click "Clear All Filters"
3. Verify the full unfiltered list is restored

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_search_filters.py` |
| Manual tests | `tests/manual/shell/search-filters.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

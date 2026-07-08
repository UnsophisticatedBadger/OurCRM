# 105 - View Property List

**Capability:** Properties
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #105

## User Story

As a real estate agent, I want to see all my property listings in a sortable, filterable list, so that I can manage my portfolio and quickly see the status of each listing.

## Dependencies

- #17 — Create a New Property Listing

## Acceptance Criteria

1. The Properties section shows a table of all properties with address, type, beds/baths, listing price, and status columns; sorted by status (Active first) by default
2. Status is color-coded: Active=green, Pending=yellow, Sold=grey, Withdrawn=red
3. Clicking a column header sorts by that column; clicking again reverses order
4. The list can be filtered by status: All / Active / Pending / Sold / Withdrawn
5. Double-clicking a property opens its details view
6. When no properties exist, "No properties yet" is shown with a "Create Your First Property" button
7. Sort column, sort direction, active filter, and scroll position are preserved when navigating away and back

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/properties.feature`.

```gherkin
@story_105
Scenario: User with properties sees them in the Properties section
  Given properties "123 Oak St" (Active) and "456 Elm Ave" (Sold) exist
  When the user opens the Properties section
  Then the list shows "123 Oak St" and "456 Elm Ave"
  And "123 Oak St" appears before "456 Elm Ave" (Active sorted first)

@story_105
Scenario: Status column is color-coded
  Given properties with Active, Pending, Sold, and Withdrawn statuses exist
  When the user views the property list
  Then the Active indicator is green, Pending is yellow, Sold is grey, and Withdrawn is red

@story_105
Scenario: User with no properties sees an empty state
  Given no properties exist
  When the user opens the Properties section
  Then "No properties yet" is shown
  And a "Create Your First Property" button is visible

@story_105
Scenario: User filters the list to show only Active properties
  Given properties with Active and Sold statuses exist
  When the user selects the "Active" status filter
  Then only Active properties are shown in the list

@story_105
Scenario: Status filter is preserved after navigating away and back
  Given the user has the "Active" filter active
  When the user navigates to Contacts and returns to Properties
  Then only Active properties are still shown
```

## Manual Tests

**Story:** [#18 — View Property List](../docs/047-view-property-list.md)

### User sees all properties with correct columns
1. Create properties with varied data (address, type, beds, baths, price, status)
2. Open the Properties section and confirm all properties appear
3. Confirm the columns show address, type, beds/baths, listing price, and status
4. Confirm default sort is Active properties first

### Status colors are correct
1. Create one property in each status (Active, Pending, Sold, Withdrawn)
2. Confirm Active is green, Pending is yellow, Sold is grey, Withdrawn is red

### Empty state appears with no properties
1. Open the app with no properties
2. Confirm "No properties yet" and the "Create Your First Property" button appear

### Sort by column
1. Click each column header and confirm the list re-sorts by that column
2. Click the same header again and confirm reverse order

### Filter by status
1. Select "Active" from the status filter
2. Confirm only Active properties are shown
3. Select "All" and confirm all properties reappear

### Filter and sort state persist after navigating away
1. Set the "Pending" status filter and sort by price
2. Navigate to Contacts, then return to Properties
3. Confirm the filter and sort column are still active

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/properties.feature` |
| BDD step defs | `tests/bdd/test_properties.py` |
| Unit tests | `tests/unit/properties/test_property_list.py` |
| Manual tests | `tests/manual/properties/property_list.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

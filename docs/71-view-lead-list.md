# 71 - View Lead List

**Capability:** Leads
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #71

## User Story

As a real estate agent, I want to see all my leads in a sortable, filterable list, so that I can see who needs follow-up and prioritise my time at a glance.

## Dependencies

- #70 — Create a New Lead

## Acceptance Criteria

1. The Leads section shows a table of all leads with name, status, source, budget range, and timeline columns; sorted by status (Hot first) by default
2. Status is color-coded: Hot=red, Warm=orange, Cold=blue
3. Clicking a column header sorts by that column; clicking again reverses order
4. The list can be filtered by status (All / Hot / Warm / Cold)
5. Double-clicking a lead opens its details view
6. When no leads exist, "No leads yet" is shown with a "Create Your First Lead" button
7. Sort column, sort direction, active status filter, and scroll position are preserved when navigating away and back

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@story_71
Scenario: User with leads sees them in the Leads section
  Given leads "Sara Lee" (Hot) and "Bob Kim" (Cold) exist
  When the user opens the Leads section
  Then the list shows "Sara Lee" and "Bob Kim"
  And "Sara Lee" appears before "Bob Kim" (Hot sorted first)

@story_71
Scenario: Status column is color-coded
  Given leads with Hot, Warm, and Cold statuses exist
  When the user views the lead list
  Then the Hot status indicator is red, Warm is orange, and Cold is blue

@story_71
Scenario: User with no leads sees an empty state
  Given no leads exist
  When the user opens the Leads section
  Then "No leads yet" is shown
  And a "Create Your First Lead" button is visible

@story_71
Scenario: User filters the list to show only Hot leads
  Given leads with Hot and Cold statuses exist
  When the user selects the "Hot" status filter
  Then only Hot leads are shown in the list

@story_71
Scenario: Status filter is preserved after navigating away and back
  Given the user has the "Hot" filter active
  When the user navigates to Contacts and returns to Leads
  Then only Hot leads are still shown
```

## Manual Tests

**Story:** [#71 — View Lead List](71-view-lead-list.md)
### User sees all leads with correct columns
1. Create leads with varied data (name, status, source, budget, timeline)
2. Open the Leads section and confirm all leads appear
3. Confirm the columns show name, status, source, budget range, and timeline
4. Confirm default sort is Hot leads first

### Status colors are correct
1. Create one Hot, one Warm, and one Cold lead
2. Confirm Hot shows red, Warm shows orange, Cold shows blue indicators

### Empty state appears with no leads
1. Open the app with no leads
2. Confirm "No leads yet" and the "Create Your First Lead" button appear

### Sort by column
1. Click each column header and confirm the list re-sorts by that column
2. Click the same header again and confirm reverse order

### Filter by status
1. Select "Hot" from the status filter
2. Confirm only Hot leads are shown
3. Select "All" and confirm all leads reappear

### Filter persists after navigating away
1. Set the "Warm" status filter
2. Navigate to Contacts, then return to Leads
3. Confirm the filter is still active

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_lead_list.py` |
| Manual tests | `tests/manual/leads/lead_list.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

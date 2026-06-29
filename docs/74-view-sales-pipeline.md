# 74 - View Sales Pipeline

**Capability:** Leads
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #74

## User Story

As a real estate agent, I want to see all my leads in a kanban board organised by pipeline stage, so that I can understand the health of my pipeline at a glance and move leads between stages without opening each one.

## Dependencies

- #65 — Move Lead Through Pipeline

## Acceptance Criteria

1. A "Pipeline" toggle in the Leads section switches the view from the list to a kanban board; toggling back restores the list
2. The kanban board shows one column per pipeline stage in order: New Lead → Contacted → Qualified → Showing Scheduled → Offer Made → Under Contract → Closed → Lost
3. Each column header shows the stage name and the count of leads currently in that stage
4. Each lead card shows the lead name, Hot/Warm/Cold status indicator, and budget range
5. Empty columns show a "No leads" placeholder rather than disappearing
6. Clicking a lead card opens the lead's details view
7. Dragging a lead card to another column changes its pipeline stage immediately and persists

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@story_74
Scenario: User switches to pipeline view and sees all stage columns
  Given leads exist in various pipeline stages
  When the user clicks the "Pipeline" toggle in the Leads section
  Then a kanban board is shown with all eight stage columns in order

@story_74
Scenario: Column header shows the correct lead count
  Given three leads are in the "Contacted" stage
  When the user views the pipeline
  Then the "Contacted" column header shows a count of 3

@story_74
Scenario: Empty column shows a No leads placeholder
  Given no leads are in the "Offer Made" stage
  When the user views the pipeline
  Then the "Offer Made" column shows "No leads" instead of being empty or hidden

@story_74
Scenario: User clicks a lead card and opens its details
  Given the user is viewing the pipeline
  When the user clicks the card for lead "Sara Lee"
  Then the lead details view opens for "Sara Lee"

@story_74
Scenario: User drags a lead card to another column and the stage updates
  Given lead "Bob Kim" is in the "New Lead" column
  When the user drags "Bob Kim"'s card to the "Contacted" column
  Then "Bob Kim" is shown in the "Contacted" column
  And opening the lead details confirms the stage is "Contacted"
```

## Manual Tests

**Story:** [#66 — View Sales Pipeline](../docs/038-view-sales-pipeline.md)

### User switches between list view and pipeline view
1. Navigate to the Leads section (list view by default)
2. Click the "Pipeline" toggle
3. Confirm the kanban board appears with eight stage columns in the correct order
4. Toggle back and confirm the list view is restored

### All eight stage columns are shown
1. Confirm all eight stages appear: New Lead, Contacted, Qualified, Showing Scheduled, Offer Made, Under Contract, Closed, Lost

### Column headers show lead counts
1. Create two leads in "Contacted" and one in "Qualified"
2. Switch to pipeline view
3. Confirm "Contacted" shows count 2 and "Qualified" shows count 1

### Empty columns remain visible
1. Find a stage with no leads
2. Confirm its column is still shown with a "No leads" placeholder

### Each lead card shows the correct information
1. Create a lead with name "Sara Lee", status "Hot", budget "$300k–$500k"
2. Switch to pipeline view and locate her card
3. Confirm the card shows "Sara Lee", a red Hot indicator, and "$300,000 – $500,000"

### Clicking a lead card opens its details
1. Click any lead card in the pipeline
2. Confirm the lead details view opens for that lead
3. Navigate back and confirm you return to the pipeline view

### Dragging a lead to another column changes its stage
1. Drag a lead card from "New Lead" to "Contacted"
2. Confirm the card moves to the "Contacted" column immediately
3. Open the lead details and confirm the stage shows "Contacted"

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_pipeline_view.py` |
| Manual tests | `tests/manual/leads/pipeline_view.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

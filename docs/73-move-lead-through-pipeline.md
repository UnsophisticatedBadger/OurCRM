# 73 - Move Lead Through Pipeline

**Capability:** Leads
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #73

## User Story

As a real estate agent, I want to move a lead through pipeline stages as our relationship progresses, so that I can track where each lead is in the sales process.

## Dependencies

- #63 — View Lead List

## Acceptance Criteria

1. Each lead has a pipeline stage — New Lead, Contacted, Qualified, Showing Scheduled, Offer Made, Under Contract, Closed, or Lost — separate from the Hot/Warm/Cold status field
2. The lead details view shows the current stage and allows changing it via a stage selector
3. Any stage transition is allowed in either direction; no stage is locked against backward movement
4. Selecting "Lost" shows an optional free-text field for a reason
5. The current pipeline stage is shown as a column in the lead list
6. Stage changes persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@story_73
Scenario: User advances a lead to the next pipeline stage
  Given the user is viewing a lead in the "New Lead" stage
  When the user changes the stage to "Contacted" and saves
  Then the lead details show the stage "Contacted"

@story_73
Scenario: User marks a lead as Lost and provides a reason
  Given the user is viewing a lead
  When the user changes the stage to "Lost" and enters reason "Chose another agent"
  Then the lead details show stage "Lost" and reason "Chose another agent"

@story_73
Scenario: User moves a lead backward in the pipeline
  Given the user is viewing a lead in the "Qualified" stage
  When the user changes the stage to "Contacted" and saves
  Then the lead details show the stage "Contacted"

@story_73
Scenario: Pipeline stage is visible in the lead list
  Given a lead "Sara Lee" exists with stage "Showing Scheduled"
  When the user views the lead list
  Then the row for "Sara Lee" shows stage "Showing Scheduled"

@story_73
Scenario: Stage change persists after an application restart
  Given the user has set a lead's stage to "Offer Made"
  When the application is restarted and the user opens that lead
  Then the stage still shows "Offer Made"
```

## Manual Tests

**Story:** [#65 — Move Lead Through Pipeline](../docs/037-move-lead-through-pipeline.md)

### User sees the current pipeline stage in lead details
1. Open any lead's details view
2. Confirm a stage field is visible showing one of the eight defined stages
3. Confirm the stage is separate from the Hot/Warm/Cold status

### User advances a lead through stages
1. Open a lead in "New Lead" stage
2. Change the stage to "Contacted" and save
3. Confirm the details view shows "Contacted"
4. Navigate to the lead list and confirm the stage column also shows "Contacted"

### User marks a lead as Lost with a reason
1. Change a lead's stage to "Lost"
2. Confirm an optional reason text field appears
3. Enter a reason and save
4. Confirm the lead shows "Lost" with the reason visible

### User moves a lead backward in the pipeline
1. Open a lead in "Offer Made" stage
2. Change the stage back to "Qualified" and save
3. Confirm the stage updates to "Qualified" without error

### Stage column is visible in the lead list
1. Create leads with different pipeline stages
2. Open the lead list and confirm the stage column shows each lead's current stage

### Stage persists after a restart
1. Set a lead's stage to "Under Contract" and save
2. Close the application and restart
3. Open the lead and confirm the stage is still "Under Contract"

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_pipeline_stage.py` |
| Manual tests | `tests/manual/leads/pipeline_stage.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

# 96 - Update Lead Status From Showing Outcome

**Capability:** leads
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #96
**Priority:** Post-MVP

## User Story
As an agent, I want the option to update a linked lead's status when I mark a showing as completed, so that my pipeline reflects the outcome without a separate manual step.

## Dependencies
- #79 — Mark Showing Completed
- #64 — Assign Lead Status

## Acceptance Criteria
1. After the user selects an outcome when completing a showing, the completion form offers a suggested lead status update based on the outcome: Interested → Hot; Not Interested → Cold; Considering → Warm
2. The suggested status is shown as a pre-selected checkbox ("Update lead status to Hot"); the user can uncheck it to skip the update
3. If the showing is not linked to a lead, the lead status update option is not shown
4. The lead's status is updated only if the checkbox is checked when the user confirms

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@story_96
Scenario: Completing a showing with "Interested" outcome offers to set lead status to Hot
  Given a showing is linked to a lead
  When the user marks the showing completed with outcome "Interested"
  Then the completion form shows a pre-checked option "Update lead status to Hot"

@story_96
Scenario: Lead status is updated when the checkbox is confirmed
  Given the "Update lead status to Hot" option is checked
  When the user confirms the showing completion
  Then the linked lead's status is changed to Hot

@story_96
Scenario: Lead status is not changed when the checkbox is unchecked
  Given the "Update lead status to Hot" option is unchecked
  When the user confirms the showing completion
  Then the linked lead's status is unchanged

@story_96
Scenario: No status update option is shown when the showing has no linked lead
  Given a showing is not linked to any lead
  When the user marks the showing completed
  Then no lead status update option appears
```

## Manual Tests
**Story:** [#33 — Update Lead Status from Showing Outcome](../docs/185-update-lead-status-from-showing.md)

### Lead status update is offered after completing a showing
1. Complete a showing linked to a lead, selecting "Interested" as the outcome
2. Verify a pre-checked "Update lead status to Hot" option appears
3. Confirm and verify the lead's status is now Hot

### Unchecking the option preserves the existing lead status
1. Complete a showing but uncheck the status update option
2. Verify the lead's status is unchanged

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_lead_status_from_showing.py` |
| Manual tests | `tests/manual/leads/update-lead-status-from-showing.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

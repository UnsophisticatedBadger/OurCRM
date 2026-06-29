# US-199 — Save AI Lead Summary to Lead Record

**Capability:** ai
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As an agent, I want to save an AI-generated lead summary to the lead record, so that I can refer back to it without having to regenerate it each time.

## Dependencies
- US-183 — AI Lead Summary

## Acceptance Criteria
1. A "Save Summary" button appears alongside "Copy to Clipboard" after a summary is generated
2. Clicking it stores the summary text and the generation date in the lead record
3. The saved summary is displayed in a read-only panel in the lead detail view, labelled with the date it was saved
4. If no summary has been saved yet, the panel shows a prompt to generate one
5. Generating and saving a new summary replaces the previously saved one; the old summary is not retained

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@us189
Scenario: User saves a generated summary and it appears in the lead detail
  Given a lead summary has been generated
  When the user clicks "Save Summary"
  Then the summary is stored in the lead record
  And a read-only panel shows the summary text and the date it was saved

@us189
Scenario: Lead detail shows a prompt when no summary has been saved
  Given a lead has no saved summary
  When the user views the lead detail
  Then the summary panel shows a prompt to generate and save one

@us189
Scenario: Saving a new summary replaces the previous one
  Given a saved summary exists from a previous session
  When the user generates and saves a new summary
  Then the panel shows only the new summary with the updated date
  And the old summary is no longer shown
```

## Manual Tests
**Story:** [US-188 — Save AI Lead Summary to Lead Record](../docs/187-save-ai-lead-summary.md)

### Saved summary appears in the lead detail with the save date
1. Generate a lead summary and click "Save Summary"
2. Close and reopen the lead detail
3. Verify the saved summary is shown in a read-only panel with the correct date

### No summary saved shows a prompt
1. Open a lead that has never had a summary saved
2. Verify the summary panel shows a prompt to generate and save one

### Saving a new summary replaces the old one
1. Save a summary for a lead
2. Generate a different summary and save it
3. Verify only the new summary is shown with the updated date

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_saved_lead_summary.py` |
| Manual tests | `tests/manual/ai/save-ai-lead-summary.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

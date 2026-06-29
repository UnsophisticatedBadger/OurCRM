# US-201 — AI Lead Preferences Panel

**Capability:** ai
**Status:** Not Done
**GitHub Issue:** #205
**Priority:** Post-MVP

## User Story
As an agent, I want the AI to extract and display a lead's stated preferences in a structured panel, so that I can see their key requirements at a glance without reading through all their notes.

## Dependencies
- #191 — AI Lead Summary

## Acceptance Criteria
1. An "Extract Preferences" button appears in the lead detail view alongside "Generate Summary"
2. Clicking it calls the configured AI provider with the lead's notes and email subjects and returns a structured list of stated preferences across these fields: budget range, location preferences, property type, must-haves, and deal-breakers
3. Extracted preferences are displayed in a dedicated Preferences panel in the lead detail view
4. Individual preference items can be manually edited by the user after extraction
5. Individual preference items can be deleted by the user
6. "Re-extract" updates the panel from the latest notes and emails; manually edited or added items are replaced
7. If AI is not configured, the "Extract Preferences" button is disabled with a tooltip directing the user to Settings → AI

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@us191
Scenario: User extracts preferences and they appear in the Preferences panel
  Given AI is configured
  And a lead has notes mentioning a budget and location preference
  When the user clicks "Extract Preferences"
  Then a Preferences panel appears in the lead detail
  And it shows the budget and location values extracted from the notes

@us191
Scenario: User edits an extracted preference item
  Given the Preferences panel shows a budget range of "$400k–$500k"
  When the user edits it to "$450k–$550k"
  Then the panel shows the updated value

@us191
Scenario: Re-extracting replaces the panel contents
  Given the Preferences panel has manually edited items
  When the user clicks "Re-extract"
  Then the panel is replaced with freshly extracted preferences from the latest notes

@us191
Scenario: "Extract Preferences" is disabled when AI is not configured
  Given AI is not configured
  When the user views a lead's detail
  Then the "Extract Preferences" button is disabled
  And hovering shows a tooltip directing the user to Settings → AI

@us191 @live_ai
Scenario: Real AI provider extracts structured preferences from lead notes
  Given a real AI provider is configured
  And a lead has notes containing budget, location, and property type mentions
  When the user clicks "Extract Preferences"
  Then the Preferences panel is populated with non-empty structured values
```

## Manual Tests
**Story:** [US-190 — AI Lead Preferences Panel](../docs/190-ai-lead-preferences-panel.md)

### Preferences are extracted and displayed in a structured panel
1. Open a lead with notes mentioning budget, location, and property type
2. Click "Extract Preferences"
3. Verify a Preferences panel appears with values populated for the relevant fields

### User edits an extracted preference and the change is saved
1. Click on a budget range value in the Preferences panel and edit it
2. Navigate away and return to the lead detail
3. Verify the edited value is still shown

### Re-extracting replaces manually edited items
1. Edit a preference item manually
2. Click "Re-extract"
3. Verify the panel resets to the freshly extracted values

### "Extract Preferences" is disabled when AI is not configured
1. Remove AI configuration from Settings → AI
2. Open any lead detail
3. Verify the "Extract Preferences" button is disabled with a tooltip

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_lead_preferences.py` |
| Manual tests | `tests/manual/ai/ai-lead-preferences-panel.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

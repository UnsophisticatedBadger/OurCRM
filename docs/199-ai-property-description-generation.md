# 199 - Generate Property Description With AI

**Capability:** ai
**Milestone:** v1.1.0+ — Post-Production
**Status:** Not Done
**GitHub Issue:** #199
**Priority:** Post-MVP

## User Story
As an agent, I want to generate a property listing description using AI, so that I can produce compelling copy quickly without writing from scratch.

## Dependencies
- #135 — Configure AI Settings
- #17 — Create a Property Listing

## Acceptance Criteria
1. A "Generate Description" button appears in the property create and edit forms
2. User selects a tone before generating: Luxury, Family-Friendly, or Investment-Focused
3. User selects a length before generating: Short (1–2 paragraphs) or Standard (3–4 paragraphs)
4. Clicking "Generate" calls the configured AI provider using the property's details (beds, baths, sqft, features, location) as context
5. The generated description appears in an editable preview panel; the user can edit it directly
6. "Regenerate" produces a new description with the same inputs
7. "Use This Description" inserts the text into the property's description field
8. If AI is not configured, the "Generate Description" button is disabled with a tooltip directing the user to Settings → AI

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@story_199
Scenario: User generates a property description with a selected tone and length
  Given AI is configured
  And a property exists with beds, baths, sqft, and features filled in
  When the user selects "Luxury" tone and "Standard" length and clicks "Generate Description"
  Then a description appears in the preview panel

@story_199
Scenario: User regenerates to get a different description
  Given a description has been generated
  When the user clicks "Regenerate"
  Then a new description with different wording is shown in the preview panel

@story_199
Scenario: User inserts the description into the property form
  Given a description has been generated
  When the user clicks "Use This Description"
  Then the description field in the property form is populated with the generated text

@story_199
Scenario: "Generate Description" is disabled when AI is not configured
  Given AI is not configured
  When the user opens the property create or edit form
  Then the "Generate Description" button is disabled
  And hovering shows a tooltip directing the user to Settings → AI

@story_199 @live_ai
Scenario: Real AI provider generates a description from property details
  Given a real AI provider is configured
  And a property has beds, baths, sqft, and at least one feature
  When the user generates a "Luxury" description
  Then a non-empty description is returned
```

## Manual Tests
**Story:** [#192 — Generate Property Description with AI](../docs/077-ai-property-description-generation.md)

### User generates a description and inserts it into the property form
1. Open a property with details filled in
2. Click "Generate Description," select "Luxury" tone and "Standard" length, click "Generate"
3. Verify a description appears in the preview panel
4. Click "Use This Description" and verify the description field is populated

### User regenerates to get different wording
1. Generate a description and note the text
2. Click "Regenerate"
3. Verify the new description has different wording

### "Generate Description" is disabled when AI is not configured
1. Remove AI configuration from Settings → AI
2. Open a property form and verify the button is disabled with a tooltip

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_property_description.py` |
| Manual tests | `tests/manual/ai/property-description-generation.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

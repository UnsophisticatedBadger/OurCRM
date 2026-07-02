# 204 - Custom AI Email Tones

**Capability:** ai
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #204
**Priority:** Post-MVP

## User Story
As an agent, I want to define custom tone labels for AI email drafting, so that I can generate emails that match specific communication styles I use with different clients.

## Dependencies
- #190 — Draft Email with AI

## Acceptance Criteria
1. Settings → AI → Email Tones lists the three built-in tones (Professional, Friendly, Urgent) and any user-defined custom tones
2. User can add a custom tone by entering a name and a brief style description (used as instruction to the AI)
3. Custom tones appear alongside built-in tones in the tone selector when using "Draft with AI"
4. Custom tones can be renamed and their style description can be edited
5. Custom tones can be deleted; deleting a tone that is currently selected in an open draft reverts the selector to "Professional"
6. Built-in tones cannot be deleted or renamed

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@story_204
Scenario: User creates a custom tone and it appears in the tone selector
  Given the user adds a custom tone named "Luxury" with description "Upscale and aspirational language"
  When the user opens "Draft with AI" in the compose form
  Then "Luxury" appears in the tone selector alongside the built-in tones

@story_204
Scenario: Draft generated with a custom tone uses the style description
  Given a custom tone "Luxury" exists with description "Upscale and aspirational language"
  When the user selects "Luxury" and generates a draft
  Then the generated email reflects an upscale tone

@story_204
Scenario: Deleting the active tone reverts the selector to Professional
  Given the user has "Luxury" selected in an open draft panel
  When the user deletes the "Luxury" tone from Settings
  Then the tone selector in the open draft reverts to "Professional"

@story_204
Scenario: Built-in tones cannot be deleted
  Given the user views Settings → AI → Email Tones
  Then the built-in tones (Professional, Friendly, Urgent) have no delete option
```

## Manual Tests
**Story:** [#98 — Custom AI Email Tones](../docs/189-custom-ai-email-tones.md)

### Custom tone appears in the tone selector when drafting
1. Go to Settings → AI → Email Tones and add a custom tone
2. Open the email compose form and click "Draft with AI"
3. Verify the custom tone appears in the tone selector

### Draft reflects the custom tone's style description
1. Select the custom tone and generate a draft
2. Verify the generated email language matches the style description

### Deleting a custom tone reverts an open selector to Professional
1. Create and select a custom tone in an open draft panel
2. Delete the tone from Settings
3. Verify the draft panel's selector shows "Professional"

### Built-in tones have no delete option
1. Open Settings → AI → Email Tones
2. Verify Professional, Friendly, and Urgent have no delete button

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_custom_email_tones.py` |
| Manual tests | `tests/manual/ai/custom-ai-email-tones.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

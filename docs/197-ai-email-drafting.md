# 197 - Draft Email With AI

**Capability:** ai
**Milestone:** v1.1.0+ — Post-Production
**Status:** Not Done
**GitHub Issue:** #197
**Priority:** Post-MVP

## User Story
As an agent, I want to generate an AI-drafted email from the compose form, so that I can send professional messages faster without writing from scratch.

## Dependencies
- #135 — Configure AI Settings
- #126 — Send Email to Contact

## Acceptance Criteria
1. A "Draft with AI" button appears in the email compose form
2. Clicking it opens a panel where the user enters: email purpose (free text) and optional key points
3. User selects tone: Professional, Friendly, or Urgent
4. Clicking "Generate" calls the configured AI provider and returns a complete email body and a suggested subject line
5. The draft is shown in an editable preview panel; the user can edit it directly
6. "Regenerate" produces a new draft with the same inputs
7. "Use This Draft" inserts the draft body into the compose form and the subject line into the subject field, replacing existing content
8. If a recipient contact is already selected in the compose form, their first name is used in the greeting
9. If AI is not configured, the "Draft with AI" button is disabled with a tooltip directing the user to Settings → AI

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@story_197
Scenario: User generates an email draft with AI
  Given AI is configured
  And the user has the email compose form open
  When the user clicks "Draft with AI", enters a purpose, selects "Professional" tone, and clicks "Generate"
  Then an email body and suggested subject line are shown in the preview panel

@story_197
Scenario: Draft addresses the selected recipient by first name
  Given AI is configured
  And a contact named "Maria" is selected as the recipient
  When the user generates a draft
  Then the greeting in the draft uses "Maria"

@story_197
Scenario: User regenerates to get a different draft
  Given a draft has been generated
  When the user clicks "Regenerate"
  Then a new draft body is returned with different wording

@story_197
Scenario: User inserts the draft into the compose form
  Given a draft has been generated and the user is satisfied
  When the user clicks "Use This Draft"
  Then the draft body replaces the compose form body
  And the suggested subject line replaces the subject field

@story_197
Scenario: "Draft with AI" button is disabled when AI is not configured
  Given AI is not configured
  When the user opens the email compose form
  Then the "Draft with AI" button is disabled
  And hovering shows a tooltip directing the user to Settings → AI

@story_197 @live_ai
Scenario: User generates a draft using a real AI provider
  Given a real AI provider is configured (Ollama or OpenAI)
  When the user generates a draft with purpose "follow up after showing" and "Professional" tone
  Then a non-empty email body and subject line are returned
```

## Manual Tests
**Story:** [#190 — Draft Email with AI](../docs/163-ai-email-drafting.md)

### User generates an email draft and uses it
1. Open the email compose form with a recipient selected
2. Click "Draft with AI"
3. Enter a purpose (e.g., "follow up after showing") and click "Generate"
4. Verify an email body and subject line appear in the preview panel
5. Click "Use This Draft" and verify the body and subject populate the compose form

### User regenerates to get a different draft
1. Generate a draft and note the wording
2. Click "Regenerate"
3. Verify the new draft has different wording for the same inputs

### Draft addresses the recipient by first name
1. Select a contact as the recipient before opening "Draft with AI"
2. Generate a draft
3. Verify the greeting uses the contact's first name

### "Draft with AI" is disabled when AI is not configured
1. Ensure no AI provider is configured in Settings → AI
2. Open the email compose form
3. Verify "Draft with AI" is disabled and the tooltip points to AI settings

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_email_drafting.py` |
| Manual tests | `tests/manual/ai/email-drafting.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

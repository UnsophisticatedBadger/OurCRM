# 198 - AI Lead Summary

**Capability:** ai
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #198
**Priority:** Post-MVP

## User Story
As an agent, I want to generate an AI summary of a lead's history, so that I can quickly understand their background before a call or meeting without reading every note and email.

## Dependencies
- #135 — Configure AI Settings
- #62 — Create a New Lead

## Acceptance Criteria
1. A "Generate Summary" button appears in the lead detail view
2. Clicking it assembles the lead's notes, email subjects, showings, and pipeline stage, then calls the configured AI provider
3. User can choose summary length before generating: Brief (2–3 sentences) or Full (full paragraph)
4. The generated summary is displayed inline in the lead detail view
5. "Refresh Summary" regenerates with the latest data from the lead record
6. "Copy to Clipboard" copies the summary as plain text
7. If AI is not configured, the "Generate Summary" button is disabled with a tooltip directing the user to Settings → AI

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@story_198
Scenario: User generates a brief AI summary for a lead
  Given AI is configured
  And a lead exists with notes, sent emails, and a scheduled showing
  When the user clicks "Generate Summary" and selects "Brief"
  Then a 2–3 sentence summary appears in the lead detail view

@story_198
Scenario: User generates a full AI summary for a lead
  Given AI is configured
  And a lead exists with notes, sent emails, and a scheduled showing
  When the user clicks "Generate Summary" and selects "Full"
  Then a full-paragraph summary appears in the lead detail view

@story_198
Scenario: Refreshing the summary picks up newly added notes
  Given a summary has already been generated for a lead
  And a new note has been added to the lead since the last generation
  When the user clicks "Refresh Summary"
  Then the new note is reflected in the refreshed summary

@story_198
Scenario: User copies the summary to clipboard
  Given a summary has been generated
  When the user clicks "Copy to Clipboard"
  Then the plain-text summary is on the clipboard

@story_198
Scenario: "Generate Summary" button is disabled when AI is not configured
  Given AI is not configured
  When the user views a lead's detail
  Then the "Generate Summary" button is disabled
  And hovering shows a tooltip directing the user to Settings → AI

@story_198 @live_ai
Scenario: User generates a summary using a real AI provider
  Given a real AI provider is configured
  And a lead has at least one note and one sent email
  When the user generates a Full summary
  Then a non-empty summary referencing the lead's data is returned
```

## Manual Tests
**Story:** [#191 — AI Lead Summary](../docs/183-ai-lead-summarization.md)

### User generates a brief and full summary and sees different lengths
1. Open a lead with notes, emails, and a showing
2. Click "Generate Summary", select "Brief", and verify 2–3 sentences appear
3. Click "Refresh Summary", select "Full", and verify a longer paragraph appears

### Refreshing picks up a new note
1. Generate a summary for a lead
2. Add a new note to the lead
3. Click "Refresh Summary" and verify the new note's content is reflected

### User copies the summary to clipboard
1. Generate a summary
2. Click "Copy to Clipboard"
3. Paste into a text editor and verify the plain-text summary is there

### "Generate Summary" is disabled when AI is not configured
1. Remove AI configuration from Settings → AI
2. Open any lead's detail view
3. Verify "Generate Summary" is disabled and the tooltip points to AI settings

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_lead_summarization.py` |
| Manual tests | `tests/manual/ai/lead-summarization.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

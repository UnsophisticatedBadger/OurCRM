# 202 - Reply To Email With AI Draft

**Capability:** ai
**Milestone:** v1.1.0+ — Post-Production
**Status:** Not Done
**GitHub Issue:** #202
**Priority:** Post-MVP

## User Story
As an agent, I want to generate an AI-drafted reply directly from an email in the contact timeline, so that I can respond quickly without switching to the compose form manually.

## Dependencies
- #190 — Draft Email with AI
- #144 — Email Inbox Sync

## Acceptance Criteria
1. Each email entry in the contact timeline includes a "Reply with AI" button
2. Clicking it opens the compose form pre-filled with: the original sender as recipient, "Re: [subject]" as subject, and the original email body quoted below the cursor
3. An AI draft is generated automatically using the quoted email as context, with no additional input required from the user
4. The generated draft appears in the compose form body above the quoted original; the user can edit it before sending
5. If AI is not configured, the "Reply with AI" button is disabled with a tooltip directing the user to Settings → AI

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@story_202
Scenario: User clicks "Reply with AI" and the compose form opens pre-filled
  Given AI is configured
  And an email exists in the contact timeline
  When the user clicks "Reply with AI" on that email
  Then the compose form opens with the original sender as recipient
  And the subject is "Re: [original subject]"
  And the original email body is quoted below the cursor

@story_202
Scenario: AI draft is generated automatically from the quoted context
  Given the user has clicked "Reply with AI" on an email
  When the compose form opens
  Then an AI-generated reply appears in the body above the quoted original

@story_202
Scenario: "Reply with AI" is disabled when AI is not configured
  Given AI is not configured
  When the user views an email entry in the contact timeline
  Then the "Reply with AI" button is disabled
  And hovering shows a tooltip directing the user to Settings → AI
```

## Manual Tests
**Story:** [#195 — Reply to Email with AI Draft](../docs/187-reply-to-email-with-ai-draft.md)

### Clicking "Reply with AI" opens the compose form pre-filled
1. View an email in a contact's timeline
2. Click "Reply with AI"
3. Verify the compose form opens with the sender as recipient, "Re: [subject]" as subject, and the original email quoted

### AI draft is generated automatically
1. After clicking "Reply with AI," verify an AI-generated reply appears above the quoted original
2. Edit the draft as needed and send it

### "Reply with AI" is disabled when AI is not configured
1. Remove AI configuration from Settings → AI
2. View an email entry in the contact timeline
3. Verify the "Reply with AI" button is disabled with a tooltip pointing to Settings → AI

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_email_reply_draft.py` |
| Manual tests | `tests/manual/ai/reply-to-email-with-ai-draft.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

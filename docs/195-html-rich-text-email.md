# 195 - HTML Rich-Text Email Composing

**Capability:** email
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #195
**Priority:** Post-MVP

## User Story
As an agent, I want to compose emails with basic rich-text formatting, so that I can send professional-looking emails with bolded text, links, and bullet lists without switching to an external email client.

## Dependencies
- #126 — Send Email to Contact

## Acceptance Criteria
1. The email compose form includes a formatting toolbar with: Bold, Italic, Underline, Bulleted List, Numbered List, and Insert Link
2. Formatted content is sent as HTML email with a plain-text fallback
3. Pasting rich text from an external source (e.g. a web page) preserves bold, italic, and links; other formatting is stripped
4. The user can switch between Rich Text and Plain Text modes; switching to Plain Text strips all formatting after a confirmation prompt
5. Email templates (#127) support rich text when edited in Rich Text mode

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_195
Scenario: Bold formatting is applied and preserved in the compose form
  Given the user is composing an email
  When the user types "Hello" and applies Bold formatting
  Then "Hello" appears bold in the compose form

@story_195
Scenario: Email is sent as HTML with a plain-text fallback
  Given the compose form contains bold text
  When the user sends the email
  Then the sent email has a text/html part and a text/plain fallback part

@story_195
Scenario: Switching to Plain Text mode strips formatting after confirmation
  Given the compose form contains bold and italic text
  When the user switches to Plain Text mode and confirms the warning
  Then the text is preserved but all formatting is removed

@story_195 @live_email
Scenario: Rich-text email is received with formatting intact by a real email client
  Given a real SMTP account is configured
  When the user sends an email with bold text and a bullet list
  Then the received email renders the bold text and bullet list correctly
```

## Manual Tests
**Story:** [#150 — HTML Rich-Text Email Composing](../docs/176-html-rich-text-email.md)

### Formatting toolbar applies styles correctly
1. Type text in the compose form
2. Select it and click Bold — verify it appears bold
3. Click Italic — verify it appears italic
4. Insert a link and verify it is clickable in the preview

### Sent email renders correctly in an email client
1. Send an email with bold text and a bulleted list to a real email address
2. Verify the received email renders the formatting

### Switching to Plain Text strips formatting
1. Add bold text to the compose form
2. Switch to Plain Text mode and confirm
3. Verify the text is present but bold formatting is removed

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_rich_text_compose.py` |
| Manual tests | `tests/manual/email/html-rich-text-email.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

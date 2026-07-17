# 192 - View Email Threads

**Capability:** email
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #192
**Priority:** Post-MVP

## User Story
As an agent, I want sent and received emails on the same subject to be grouped into a thread in the contact timeline, so that I can follow a full conversation without scrolling through individual entries.

## Dependencies
- #189 — Email Inbox Sync
- #178 — View Email History in Contact Timeline

## Acceptance Criteria
1. Emails sharing the same thread ID (or matching subject after stripping Re:/Fwd: prefixes) are grouped under a single thread entry in the contact timeline
2. The collapsed thread entry shows: subject, number of messages, and date of the latest message
3. Clicking a thread entry expands it to show all messages in chronological order with sender and timestamp
4. New messages added to a thread (sent or received) automatically appear at the bottom of the expanded thread
5. A count badge on the thread entry updates when new messages arrive

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_192
Scenario: Sent and received emails on the same subject are grouped into a thread
  Given a sent email and a received reply share the same subject
  When the user views the contact timeline
  Then both emails appear as a single thread entry
  And the thread entry shows the subject and message count

@story_192
Scenario: Clicking a thread entry expands to show all messages
  Given a thread with three messages exists in the contact timeline
  When the user clicks the thread entry
  Then all three messages are shown in chronological order with sender and timestamp

@story_192
Scenario: New message added to a thread updates the count badge
  Given an expanded thread has two messages
  When a new reply arrives on the same thread
  Then the thread count badge updates to three
  And the new message appears at the bottom of the expanded thread
```

## Manual Tests
**Story:** [#192 — View Email Threads](192-view-email-threads.md)
### Sent and received emails on the same subject are grouped
1. Send an email to a contact
2. Receive a reply from the same contact (with inbox sync enabled)
3. View the contact timeline and verify both emails appear as a single thread entry

### Expanding a thread shows all messages in order
1. Click a thread entry
2. Verify all messages appear chronologically with sender name and timestamp

### New reply updates the thread count
1. With a thread open, receive a new reply
2. Verify the message count badge increments and the new message appears at the bottom

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_email_threads.py` |
| Manual tests | `tests/manual/email/view-email-threads.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

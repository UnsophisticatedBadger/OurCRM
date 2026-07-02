# 157 - Notification For Email Received

**Capability:** Notifications
**Milestone:** Production
**Status:** Not Done
**GitHub Issue:** #157

## User Story

As a real estate agent, I want to receive a notification when a contact emails me so that I can respond promptly without constantly checking my inbox.

## Dependencies

- #126 — Send Email to Contact
- #125 — Configure Email Settings
- #176 — Desktop Notifications for New Leads
- #177 — In-App Notifications
- #178 — Notification Preferences

## Notes

Email-received notifications use the same desktop/in-app delivery channels established by #176 and #177. The email account must be configured (#125) before this story applies.

Live email receipt requires an active email account connection. BDD scenarios that depend on a real incoming email are tagged `@live_email` for CI skip. Unit tests inject a simulated incoming-email event directly into the notification dispatcher.

## Acceptance Criteria

1. When OurCRM detects a new incoming email whose sender address matches a contact, a notification fires with title "New Email from [Contact Name]" and body showing the email subject
2. When the sender is not a known contact, the notification title shows the sender's email address instead of a contact name
3. Clicking a notification for a known contact navigates to that contact's email history; clicking a notification for an unknown sender navigates to the email inbox view
4. Notifications use desktop delivery (#176 pattern) when the app is in the background and in-app toast (#177 pattern) when the user is actively in the app
5. Email-received notifications respect the Email Received toggle in notification preferences (#178); if that toggle is off, no notification fires

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/notifications.feature`.

```gherkin
@story_157 @live_email
Scenario: New email from a known contact triggers a notification
  Given an email account is configured in Settings
  And a contact "Jane Smith" exists with email "jane@example.com"
  And Email Received notifications are enabled
  When an email from "jane@example.com" with subject "Re: Property Visit" arrives
  Then a notification fires with title "New Email from Jane Smith" and body "Re: Property Visit"

@story_157 @live_email
Scenario: New email from an unknown sender shows the sender address as title
  Given an email account is configured
  And Email Received notifications are enabled
  When an email from "unknown@example.com" with subject "Enquiry" arrives
  And "unknown@example.com" does not match any contact
  Then a notification fires with title "unknown@example.com" and body "Enquiry"

@story_157 @live_email
Scenario: Clicking the notification for a known contact opens email history
  Given a notification "New Email from Jane Smith" has fired
  When the user clicks the notification
  Then OurCRM comes to the foreground and Jane Smith's email history is shown

@story_157 @live_email
Scenario: No notification fires when Email Received preference is disabled
  Given Email Received notifications are disabled in notification preferences
  When a new email arrives from a known contact
  Then no desktop or in-app notification fires
```

## Manual Tests

**Story:** [#180 — Notification for Email Received](../docs/093-notification-for-email-received.md)

### New email from a contact triggers a notification
1. Configure an email account in Settings
2. Have a contact whose email address matches an account you can send from
3. Send an email to the configured account from that contact's address
4. Confirm a notification appears with "New Email from [Contact Name]" and the subject in the body
5. Click the notification and confirm it opens that contact's email history

### Unknown sender shows email address in notification
1. Send an email from an address not in OurCRM contacts
2. Confirm the notification title shows the sender's email address (not a contact name)
3. Click the notification and confirm it navigates to the email inbox view rather than a contact record

### Notification preference disables email notifications
1. Disable the Email Received toggle in Settings → Notifications
2. Send an email from a known contact
3. Confirm no notification fires
4. Re-enable the toggle, send another email, and confirm the notification resumes

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/notifications.feature` |
| BDD step defs | `tests/bdd/test_notifications.py` |
| Unit tests | `tests/unit/notifications/test_email_received_notification.py` |
| Manual tests | `tests/manual/notifications/email_received_notification.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

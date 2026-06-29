# 153 - Desktop Notifications For New Leads

**Capability:** Notifications
**Milestone:** v1.0.0 — Production
**Status:** Not Done
**GitHub Issue:** #153

## User Story

As a real estate agent, I want to receive a desktop notification when a new lead is created so that I can respond quickly even when the CRM is in the background.

## Dependencies

- #62 — Create a New Lead

## Notes

Desktop notifications use the OS notification system (Windows Action Center, macOS Notification Center). The OS may request permission the first time a notification is sent — this is OS-controlled behaviour outside the app's scope to test automatically; cover it in the manual tests only.

Notification preferences (enable/disable per event type) are handled by #178.

## Acceptance Criteria

1. When a new lead is saved (#62), a desktop notification fires with title "New Lead: [Name]" and body showing the lead source or "Manually added" if no source is set
2. When a bulk lead import completes (#184, #153, #154), a single summary notification fires with title "N Leads Imported" and body "View the Leads section to see the new records"; the count reflects only the leads successfully added
3. Clicking any lead notification brings OurCRM to the foreground and navigates to that lead's detail view; clicking an import-summary notification navigates to the Leads list
4. Notifications fire even when OurCRM is minimised or in the background
5. If new-lead notifications are disabled in notification preferences, no notification fires for either individual creation or bulk import

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/notifications.feature`.

```gherkin
@story_153
Scenario: Creating a new lead triggers a desktop notification with the lead's name and source
  Given notification preferences allow new-lead notifications
  When the user saves a new lead named "John Doe" with source "Website"
  Then a desktop notification fires with title "New Lead: John Doe" and body "From Website"

@story_153
Scenario: Manually added lead shows "Manually added" as the source in the notification
  Given notification preferences allow new-lead notifications
  When the user saves a new lead named "Jane Smith" with no source set
  Then a desktop notification fires with title "New Lead: Jane Smith" and body "Manually added"

@story_153
Scenario: Bulk import completion fires a single summary notification
  Given notification preferences allow new-lead notifications
  When a CSV import completes and adds 8 leads successfully
  Then a single desktop notification fires with title "8 Leads Imported" and body "View the Leads section to see the new records"

@story_153
Scenario: Clicking the notification navigates to the new lead
  Given a desktop notification for "New Lead: John Doe" has fired
  When the user clicks the notification
  Then OurCRM comes to the foreground and John Doe's lead detail view is shown

@story_153
Scenario: Clicking the import summary notification navigates to the Leads list
  Given a desktop notification "8 Leads Imported" has fired
  When the user clicks the notification
  Then OurCRM comes to the foreground and the Leads list is shown

@story_153
Scenario: No notification fires when new-lead notifications are disabled
  Given new-lead notifications are disabled in notification preferences
  When the user saves a new lead
  Then no desktop notification fires
```

## Manual Tests

**Story:** [#176 — Desktop Notifications for New Leads](../docs/093-desktop-notifications-for-new-leads.md)

### Notification fires when a new lead is created
1. Ensure new-lead notifications are enabled in preferences
2. Create a new lead with a name and a lead source
3. Confirm a desktop notification appears with "New Lead: [Name]" and the source in the body
4. Repeat with no source set and confirm the body reads "Manually added"

### Notification fires when the app is in the background
1. Minimise OurCRM to the taskbar and have another window in focus
2. Create a new lead (bring the app briefly to focus to create it, then minimise and observe)
3. Confirm the desktop notification appears in the OS notification area

### Bulk import fires a single summary notification
1. Import a CSV file with several leads
2. Confirm only one notification fires (not one per lead) with title "N Leads Imported"
3. Click the notification and confirm it navigates to the Leads list

### Clicking the notification navigates to the lead
1. When a new-lead notification appears, click it
2. Confirm OurCRM comes to the foreground and the lead detail view for that specific lead is shown

### No notification when the preference is disabled
1. Go to notification preferences and disable new-lead notifications
2. Create a new lead and run an import
3. Confirm no desktop notification appears for either action
4. Re-enable the preference and confirm notifications resume

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/notifications.feature` |
| BDD step defs | `tests/bdd/test_notifications.py` |
| Unit tests | `tests/unit/notifications/test_new_lead_notification.py` |
| Manual tests | `tests/manual/notifications/new_lead_notification.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

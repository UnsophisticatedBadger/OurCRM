# 146 - Sync Multiple Calendar Accounts

**Capability:** calendar
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #146
**Priority:** Post-MVP

## User Story
As an agent, I want to connect more than one Google or Outlook account, so that I can see events from all my calendars in OurCRM without switching between accounts.

## Dependencies
- #41 — Choose Which Calendar to Sync

## Acceptance Criteria
1. Settings → Calendar → Google Calendar includes an "Add another Google account" button; the user can connect additional accounts via the same OAuth flow
2. Settings → Calendar → Outlook Calendar includes an "Add another Outlook account" button; the user can connect additional accounts via the same OAuth flow
3. Each connected account is listed separately in Settings with its own calendar selector and disconnect control
4. Events from all connected accounts appear in the OurCRM calendar view, colour-coded by account
5. Disconnecting one account removes only that account's synced events; other accounts continue syncing unaffected

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/calendar.feature`.

```gherkin
@story_146
Scenario: User connects a second Google account and its events appear in OurCRM
  Given one Google Calendar account is already connected
  When the user connects a second Google account via OAuth
  Then both accounts are listed in Settings
  And events from both accounts appear in the OurCRM calendar view

@story_146
Scenario: Events from different accounts are colour-coded
  Given two Google Calendar accounts are connected
  When the user views the OurCRM calendar
  Then events from each account are shown in a distinct colour

@story_146
Scenario: Disconnecting one account removes only its events
  Given two Google Calendar accounts are connected with synced events
  When the user disconnects the second account
  Then the second account's events are removed from OurCRM
  And the first account's events and sync continue unaffected
```

## Manual Tests
**Story:** [#42 — Sync Multiple Calendar Accounts](../docs/161-sync-multiple-calendar-accounts.md)

### User connects a second Google account and sees both accounts listed in Settings
1. Connect a first Google Calendar account
2. Click "Add another Google account" and complete OAuth for a second account
3. Verify both accounts are listed in Settings with separate controls

### Events from both accounts appear colour-coded in the calendar view
1. Create an event in each connected Google account
2. Sync and open the OurCRM calendar view
3. Verify both events appear and are distinguishable by colour

### Disconnecting one account removes only its events
1. Disconnect the second Google account
2. Verify the second account's events are gone
3. Verify the first account's events and sync are unaffected

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/calendar.feature` |
| BDD step defs | `tests/bdd/test_calendar.py` |
| Unit tests | `tests/unit/calendar/test_multi_account_calendar.py` |
| Manual tests | `tests/manual/calendar/sync-multiple-calendar-accounts.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

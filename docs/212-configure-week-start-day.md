# 212 - Configure Week Start Day

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #212

## User Story

As a real estate agent, I want to set which day my work week starts on, so that "this week" and "next week" reflect how I actually organize my schedule.

## Dependencies

- #12 — Configure General Settings
- #3 — Create Master Password

## Acceptance Criteria

1. Settings > General has a "Week starts on" dropdown offering all seven days, defaulting to Monday
2. During initial app setup — immediately after master password creation, first run only — the user is shown a confirmation step for the week-start day, pre-selected to Monday, which must be explicitly confirmed before continuing into the app
3. A shared week-boundary helper in `core/` computes the start and end of the week from the configured day; `timeframe_to_range()` in `src/ourcrm/crm/contacts/callback_timeframe.py` is migrated to use it instead of its hardcoded Monday-Sunday math
4. "This Week" and "Next Week" (and "In Two Weeks") are computed relative to the configured week start, with Next Week always starting the day immediately after This Week's last day, whatever that is under the current setting
5. "This Month" is unaffected by this setting — it stays calendar-month based (today through the end of the current calendar month) even when the month transition falls in the middle of a configured week
6. Changing the setting later in Settings > General takes effect for future timeframe calculations without requiring a restart
7. The configured week-start day persists across restarts

## BDD Scenarios

```gherkin
@story_212
Scenario: First-time setup asks the user to confirm their week-start day
  Given the user has just created their master password for the first time
  Then a week-start confirmation step is shown
  And "Monday" is pre-selected

@story_212
Scenario: Confirming the default week-start day during initial setup
  Given the week-start confirmation step is shown
  When the user confirms without changing the selection
  Then the week-start day is saved as "Monday"

@story_212
Scenario: Choosing a different week-start day during initial setup
  Given the week-start confirmation step is shown
  When the user selects "Sunday" and confirms
  Then the week-start day is saved as "Sunday"

@story_212
Scenario: Changing the week-start day later in General settings
  Given the settings panel is open on General
  When the user selects "Sunday" from the "Week starts on" dropdown
  And clicks Save
  Then the saved week-start day is "Sunday"

@story_212
Scenario: This Week is computed from the configured week-start day
  Given the week-start day is set to "Sunday"
  And today is a Wednesday
  When a contact is given a callback timeframe of "This Week"
  Then the callback range ends on the following Saturday

@story_212
Scenario: Next Week starts the day after This Week ends
  Given the week-start day is set to "Sunday"
  And today is a Wednesday
  When a contact is given a callback timeframe of "Next Week"
  Then the callback range starts on the following Sunday

@story_212
Scenario: This Month ignores the configured week-start day
  Given the week-start day is set to "Sunday"
  When a contact is given a callback timeframe of "This Month"
  Then the callback range covers today through the end of the current calendar month

@story_212
Scenario: The week-start day persists after restart
  Given the week-start day has been set to "Sunday"
  When the application is restarted
  Then Settings > General still shows "Sunday" as the week-start day
```

## Manual Tests

**Story:** [#212 — Configure Week Start Day](212-configure-week-start-day.md)

### First-time setup asks for a week-start day
1. Delete any existing database/config and launch OurCRM fresh
2. Create a master password
3. Confirm a week-start confirmation step appears with "Monday" pre-selected
4. Confirm without changing it, and confirm the app proceeds to the main window

### Choosing a non-default week-start day during initial setup
1. Repeat the fresh-launch flow above
2. On the week-start confirmation step, select a different day (e.g. "Sunday") and confirm
3. Open Settings > General and confirm "Sunday" is shown as the week-start day

### Changing the week-start day later
1. Open Settings > General
2. Change "Week starts on" to a different day and click Save
3. Log a Call Back outcome with a "This Week" timeframe and confirm the resulting date range reflects the new week boundary

### This Month is unaffected by the week-start day
1. With any week-start day configured, log a Call Back outcome with a "This Month" timeframe
2. Confirm the range runs from today through the end of the current calendar month, regardless of the week-start setting

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_week_start_setting.py`, `tests/unit/core/test_week_boundary.py`, `tests/unit/contacts/test_callback_timeframe.py` |
| Manual tests | `tests/manual/shell/week_start_day.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

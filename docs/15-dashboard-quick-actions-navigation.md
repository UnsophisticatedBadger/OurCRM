# #15 — Dashboard Quick Actions Navigation

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Done
**GitHub Issue:** #15

## User Story

As a real estate agent, I want the Quick Actions buttons on the dashboard to take me directly to the right section, so that I can start common tasks with one click instead of hunting through the sidebar.

## Dependencies

- #14 — Home Dashboard
- #10 — Navigate Between Sections

## Acceptance Criteria

1. New Contact, New Lead, New Property, and New Task buttons each navigate to their respective section with one click
2. Navigation is triggered via callback or signal — `DashboardPage` does not import `MainWindow` directly

## BDD Scenarios

```gherkin
@story_15
Scenario: Clicking New Contact navigates to Contacts
  Given the dashboard is the active section
  When I click the "New Contact" quick action button
  Then the Contacts section is active
  And the content area shows the "Contacts" section page

@story_15
Scenario: Clicking New Lead navigates to Leads
  Given the dashboard is the active section
  When I click the "New Lead" quick action button
  Then the Leads section is active
  And the content area shows the "Leads" section page

@story_15
Scenario: Clicking New Property navigates to Properties
  Given the dashboard is the active section
  When I click the "New Property" quick action button
  Then the Properties section is active
  And the content area shows the "Properties" section page

@story_15
Scenario: Clicking New Task navigates to Calendar
  Given the dashboard is the active section
  When I click the "New Task" quick action button
  Then the Calendar section is active
  And the content area shows the "Calendar" section page
```

AC2 (`DashboardPage` does not import `MainWindow` directly) is an internal DI/architecture constraint with no observable user behavior, so it is covered by a unit test rather than a BDD scenario.

## Manual Tests

### User clicks New Contact and is taken to Contacts
1. Open the Dashboard
2. Click the "New Contact" quick action button
3. Verify the Contacts section becomes active

### User clicks New Lead and is taken to Leads
1. Open the Dashboard
2. Click the "New Lead" quick action button
3. Verify the Leads section becomes active

### User clicks New Property and is taken to Properties
1. Open the Dashboard
2. Click the "New Property" quick action button
3. Verify the Properties section becomes active

### User clicks New Task and is taken to Calendar
1. Open the Dashboard
2. Click the "New Task" quick action button
3. Verify the Calendar section becomes active

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_quick_actions.py` |
| Manual tests | `tests/manual/shell/quick_actions.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [x] Wiki documentation N/A — AC2 is an internal DI/architecture constraint with no user-visible surface; AC1's user-facing behavior is already documented under [App Shell § Home Dashboard](https://github.com/UnsophisticatedBadger/OurCRM/wiki/App-Shell)

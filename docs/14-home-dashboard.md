# #14 — Home Dashboard

**Capability:** App Shell
**Milestone:** Secure Shell
**Status:** Done
**GitHub Issue:** #14

## User Story

As a real estate agent, I want to see a dashboard when I open the app, so that I can get an overview of my business and today's priorities without navigating to each section.

## Dependencies

- #10 — Navigate Between Sections

## Acceptance Criteria

1. Dashboard is the default section shown immediately after login
2. The dashboard page provides three named layout regions — stats, today's schedule, and quick actions — each rendering placeholder/empty content until its own widget story lands (#20, #21, #15)

## BDD Scenarios

```gherkin
@story_14
Scenario: Dashboard is the default view on startup
  Given the main window is open
  Then the Dashboard section is active
  And the "Dashboard" nav item is highlighted

@story_14
Scenario: Navigation panel contains Dashboard
  Given the main window is open
  Then the navigation panel contains "Dashboard"

@story_14
Scenario: Stats region is visible on the dashboard
  Given the dashboard is the active section
  Then I should see the "Stats" region

@story_14
Scenario: Today's Schedule region is visible on the dashboard
  Given the dashboard is the active section
  Then I should see the "Today's Schedule" region

@story_14
Scenario: Quick actions widget buttons are visible
  Given the main window is open
  Then I should see a "New Contact" quick action button
  And I should see a "New Lead" quick action button
  And I should see a "New Property" quick action button
  And I should see a "New Task" quick action button
```

## Manual Tests

### User logs in and lands on the Dashboard immediately
1. Log in with the master password
2. Verify the Dashboard section is active immediately — no additional navigation required
3. Verify the "Dashboard" item is highlighted in the sidebar

### User views the Dashboard and sees three named regions
1. Open the Dashboard section
2. Verify a Stats region is present showing placeholder/empty counts
3. Verify a Today's Schedule region is present showing placeholder content
4. Verify a Quick Actions region is present with New Contact, New Lead, New Property, and New Task buttons

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_dashboard_page.py`, `test_navigation_dashboard.py` |
| Manual tests | `tests/manual/shell/dashboard.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [x] Manual tests documented and verified
- [x] Wiki documentation written — see [App Shell](https://github.com/UnsophisticatedBadger/OurCRM/wiki/App-Shell)

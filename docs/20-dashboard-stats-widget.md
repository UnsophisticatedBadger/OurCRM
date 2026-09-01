# 20 - Dashboard Stats Widget

**Capability:** shell
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #20

## User Story

As a real estate agent, I want to see a row of key business counts on the dashboard, so that I can gauge my pipeline at a glance without navigating to each section.

## Dependencies

- #14 — Home Dashboard

## Acceptance Criteria

1. Dashboard shows four stat tiles — Contacts, Active Leads, Properties, Due Today — each displaying a numeric count (zero when no data exists)
2. `StatsWidget.refresh(counts)` updates the displayed values so downstream stories can wire in real counts without changing the widget layout
3. Contacts tile shows the real count of contacts from the Contacts repository
4. Active Leads tile shows the real count of leads from the Leads repository
5. Due Today tile shows the real count of contacts with a "Call Back" outcome whose callback is due today, from the Call Outcome repository
6. Properties tile shows a placeholder count of 0, since no Properties capability/data source exists yet
7. Stats refresh with current data every time the dashboard is shown (not just once at app startup)

## BDD Scenarios

```gherkin
@story_20
Scenario: Stats widget is visible on the dashboard
  Given the dashboard is the active section
  Then I should see a "Contacts" stat tile
  And I should see an "Active Leads" stat tile
  And I should see a "Properties" stat tile
  And I should see a "Due Today" stat tile

@story_20
Scenario: Stats widget shows zero counts with no data
  Given the dashboard is the active section
  And no CRM data has been entered
  Then every stat tile shows "0"

@story_20
Scenario: Stats widget shows the real contact and lead counts
  Given the user has created 2 contacts and 1 lead
  When the user views the dashboard
  Then the "Contacts" stat tile shows "2"
  And the "Active Leads" stat tile shows "1"

@story_20
Scenario: Stats widget shows the real due-today count
  Given a contact has a callback due today
  When the user views the dashboard
  Then the "Due Today" stat tile shows "1"
```

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_stats_widget.py` |
| Manual tests | `tests/manual/shell/stats_widget.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified — documented; not yet human-verified against the running app
- [x] Wiki documentation written, or marked N/A with a reason

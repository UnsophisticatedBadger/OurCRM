# 20 - Dashboard Stats Widget

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #20

## User Story

As a real estate agent, I want to see a row of key business counts on the dashboard, so that I can gauge my pipeline at a glance without navigating to each section.

## Dependencies

- #14 — Home Dashboard

## Acceptance Criteria

1. Dashboard shows four stat tiles — Contacts, Active Leads, Properties, Due Today — each displaying a numeric count (zero when no data exists)
2. `StatsWidget.refresh(counts)` updates the displayed values so downstream stories can wire in real counts without changing the widget layout

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
- [x] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

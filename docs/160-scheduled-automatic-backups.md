# 160 - Scheduled Automatic Backups

**Capability:** backup
**Milestone:** v1.0.0 — Production
**Status:** Not Done
**GitHub Issue:** #160
**Priority:** Post-MVP

## User Story
As an agent, I want OurCRM to create backups automatically on a schedule, so that my data is protected without requiring me to remember to back up manually.

## Dependencies
- #181 — Create Manual Backup

## Acceptance Criteria
1. Settings → Backup → Automatic Backups includes a toggle to enable or disable scheduled backups; disabled by default
2. When enabled, the user can set the schedule: Daily or Weekly (day of week + time)
3. Backups created by the schedule follow the same format and destination folder as manual backups (#181)
4. A scheduled backup runs at the configured time while the app is running; if the app is not running at the scheduled time, the backup runs on the next app launch after the missed time
5. Automatic backups appear in the backup history (#24) labelled "Automatic"
6. The most recent 10 automatic backups are retained; older automatic backups are deleted automatically

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/backup.feature`.

```gherkin
@story_160
Scenario: Enabling automatic backups with a Daily schedule saves the setting
  Given the user enables automatic backups and selects "Daily at 11:00 PM"
  When the user saves Settings
  Then the automatic backup schedule is saved as Daily at 11:00 PM

@story_160
Scenario: Missed backup runs on next app launch
  Given a daily backup was scheduled for a time that has already passed today
  And the app was not running at that time
  When the user launches the app
  Then a backup is created immediately on launch

@story_160
Scenario: Automatic backup appears in backup history labelled "Automatic"
  Given automatic backups are enabled and a scheduled backup has run
  When the user views the backup history
  Then the backup is listed with the label "Automatic"

@story_160
Scenario: Oldest automatic backup is deleted when the 10-backup limit is reached
  Given 10 automatic backups already exist
  When a new scheduled backup runs
  Then the oldest automatic backup is deleted
  And 10 automatic backups remain
```

## Manual Tests
**Story:** [#101 — Scheduled Automatic Backups](../docs/192-scheduled-automatic-backups.md)

### Daily backup runs at the configured time
1. Enable automatic backups and set a schedule for a time 2 minutes from now
2. Wait for the time to pass and verify a backup file is created

### Missed backup runs on launch
1. Set a backup schedule for a time that has already passed and relaunch the app
2. Verify a backup is created on launch

### Automatic backup appears in history
1. After an automatic backup runs, open backup history
2. Verify it appears labelled "Automatic"

### Old automatic backups are pruned at 10
1. Allow 11 automatic backups to accumulate
2. Verify only 10 remain and the oldest has been deleted

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/backup.feature` |
| BDD step defs | `tests/bdd/test_backup.py` |
| Unit tests | `tests/unit/backup/test_scheduled_backups.py` |
| Manual tests | `tests/manual/backup/scheduled-automatic-backups.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

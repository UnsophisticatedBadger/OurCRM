# US-134 — Roll Back a Failed Update

**Capability:** infrastructure
**Status:** Not Done
**Priority:** Post-MVP

## User Story
As a user, I want the app to restore the previous version if an update fails to install, so that I'm never left with a broken installation.

## Dependencies
- US-113 — Check for and Install Application Updates
- US-098 — Create a Backup

## Acceptance Criteria
1. If the installer exits with an error during a manual or auto update, the pre-update backup created in US-113 AC #6 is used to restore the previous version automatically
2. After rollback, the user is shown a message explaining that the update failed and the previous version has been restored
3. The app launches successfully at the previous version after rollback completes
4. If the rollback itself fails, the user is shown the path to the backup file and step-by-step instructions to restore manually

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@us177
Scenario: Failed installer triggers automatic rollback
  Given a pre-update backup exists
  And the update installer exits with an error
  When the installation failure is detected
  Then the previous version is restored from the backup
  And the user is notified that the update failed and the previous version is running

@us177
Scenario: App launches successfully at the previous version after rollback
  Given a rollback has completed
  When the application starts
  Then the previous version number is shown
  And all data is intact

@us177
Scenario: User is shown manual recovery path if rollback itself fails
  Given a pre-update backup exists
  And both the installer and the rollback fail
  When the failure is detected
  Then the user is shown the backup file path and manual restore instructions
```

## Manual Tests
**Story:** [US-134 — Roll Back a Failed Update](../docs/116-roll-back-failed-update.md)

### Failed update triggers rollback and the previous version is restored
1. Simulate an installer failure (e.g., corrupt package in a test build)
2. Verify a rollback notification appears
3. Verify the app relaunches at the previous version
4. Verify all data is still accessible

### User is shown manual recovery instructions if rollback also fails
1. Simulate both installer and rollback failures
2. Verify the user is shown the backup file path
3. Verify the instructions are clear enough to follow manually

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_update_rollback.py` |
| Manual tests | `tests/manual/infrastructure/roll-back-failed-update.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified

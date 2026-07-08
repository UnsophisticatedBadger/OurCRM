# 92 - Database Indexing For Performance

**Capability:** infrastructure
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #92
**Priority:** Post-MVP

## User Story
As an agent, I want the app to remain responsive when I have thousands of records, so that searches and filters don't slow down as my database grows.

## Dependencies
- #5 — Create Encrypted Database

## Acceptance Criteria
1. Indexes are created automatically during database initialisation and kept up to date through Alembic migrations; no manual step is required
2. Indexes cover: contact name, email, and phone; lead status, source, and created date; property address, status, and price; transaction dates and status; task due dates and priority
3. A contact name search across 10,000 records returns results in under 500 ms on a typical development machine
4. A lead status filter across 10,000 records returns results in under 500 ms on a typical development machine
5. Settings → General → Maintenance includes a "Rebuild Indexes" action that re-creates all indexes; a progress indicator is shown and a success message confirms completion
6. Running "Rebuild Indexes" does not alter or delete any records

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/infrastructure.feature`.

```gherkin
@story_92
Scenario: Indexes are present after database initialisation
  Given a fresh database has been created
  When the user opens the app for the first time
  Then indexes exist on the contact name, email, lead status, and property address fields

@story_92
Scenario: Indexes are preserved after a migration
  Given indexes exist on the database
  When a database migration is applied
  Then the indexes still exist after the migration completes

@story_92
Scenario: Rebuild Indexes completes without altering records
  Given 100 contacts exist in the database
  When the user runs "Rebuild Indexes" from Settings → General → Maintenance
  Then all 100 contacts are still present after the rebuild
  And a success message is shown
```

## Manual Tests
**Story:** [#91 — Database Indexing for Performance](../docs/117-database-0indexing-for-performance.md)

### Search returns quickly with a large dataset
1. Import or create at least 5,000 contacts
2. Search for a contact name and time the response
3. Verify results appear in under 500 ms

### Lead filter returns quickly with a large dataset
1. Ensure at least 5,000 leads exist
2. Apply a status filter and time the response
3. Verify results appear in under 500 ms

### Rebuild Indexes completes without data loss
1. Go to Settings → General → Maintenance → Rebuild Indexes
2. Verify a progress indicator is shown during the rebuild
3. After completion verify the record counts are unchanged

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_db_indexes.py` |
| Manual tests | `tests/manual/infrastructure/database-indexing.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason

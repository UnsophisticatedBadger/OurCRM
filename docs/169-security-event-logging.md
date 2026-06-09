# US-169: Security Event Logging

## User Story

**As a** user  
**I want** security-relevant events to be persisted to a log  
**So that** I can audit authentication history and detect suspicious activity

## Priority

**MVP:** Should Have

## Dependencies

**Depends on:** US-014 (Create Encrypted Database), US-128 (Password Recovery)

## Events to Log

| Event | Fields |
|-------|--------|
| Login attempt | timestamp, success, failure_reason |
| Password change | timestamp |
| Recovery attempt | timestamp, success |
| Logout | timestamp |

## Notes

- Recovery attempt logging was deferred from US-128. In-memory logging has no value without persistence; implement here once the audit_log database table exists.
- Login attempt logging may reuse the same table.

## Acceptance Criteria

- [ ] `security_events` table created via Alembic migration
- [ ] Recovery attempts written to table (success + failure)
- [ ] Login attempts written to table
- [ ] Events are readable from the UI (view error logs, US-122)

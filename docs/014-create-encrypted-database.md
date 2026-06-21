# US-014: Create Encrypted Database

## User Story

**As a** user  
**I want to** have my database encrypted with my master password  
**So that** my data is secure even if my laptop is stolen

## Priority

**MVP:** Must Have

**Rationale:** Security is a core requirement. The database must be encrypted at rest to protect user data. This is non-negotiable for our security commitments.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Integrate SQLCipher with SQLAlchemy
- 3 hours: Implement encryption key derivation from password
- 2 hours: Create database initialization with encryption
- 2 hours: Implement secure key storage in OS keyring
- 2 hours: Create database schema setup
- 2 hours: Implement secure connection management
- 3 hours: Write tests for encryption
- 2 hours: Test that encrypted data is unreadable without key
- 2 hours: Performance testing with encryption

## Dependencies

**Depends on:** US-010 (Create Master Password), US-007 (Create Initial Project Structure)

**Blocks:** US-020 (Create Contact), all data storage features

## Description

When a user completes setup, OurCRM creates an encrypted SQLite database using SQLCipher. The database is encrypted with AES-256-GCM, and the encryption key is derived from the user's master password using Argon2id. The encryption key is stored in the OS keyring for the duration of the session, and the database file on disk is completely unreadable without the correct master password.

The database is stored in a user-accessible location (e.g., ~/ourcrm/data.db on Unix or appropriate location on Windows). The database is created with proper schema and migrations are set up using Alembic. All data written to the database is automatically encrypted.

## Acceptance Criteria

- [x] Database is created during setup
- [x] Database is encrypted with AES-256-GCM
- [x] Database file is unreadable without the password
- [x] Encryption key is derived from master password
- [x] Encryption key is stored in OS keyring during session
- [x] Database schema is set up with Alembic
- [x] Database opens successfully with correct password
- [x] Database cannot be opened with wrong password
- [x] All data is encrypted at rest
- [ ] Encryption doesn't significantly impact performance — see tests/manual/authentication.md
- [ ] Works on Windows, macOS, and Linux — see tests/manual/authentication.md
- [x] Database location is documented
- [ ] Backup files are also encrypted — see tests/manual/authentication.md
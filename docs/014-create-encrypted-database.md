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

## BDD Scenarios

### Scenario 1: Create encrypted database during setup

```
Given I have created my master password
  And I have confirmed my recovery password
When the setup completes
Then an encrypted database should be created
  And the database should be located in the user's data directory
  And the database should be encrypted with AES-256-GCM
  And the encryption key should be derived from the master password
```

### Scenario 2: Database file is encrypted on disk

```
Given I have an OurCRM database
When I try to read the database file with a text editor
Then I should see only encrypted binary data
  And I should not see any readable text
  And the file should not contain any user data in plain text
```

### Scenario 3: Database cannot be opened without password

```
Given I have an OurCRM database
  And I know the file location
When I try to open it with a standard SQLite tool
Then the tool should fail to open the database
  And it should report that the database is encrypted
```

### Scenario 4: Database opens with correct password

```
Given I have an OurCRM database
  And I know the correct master password
When I start OurCRM and enter the correct password
Then the database should open successfully
  And I should be able to read and write data
```

### Scenario 5: Encryption key is stored in OS keyring

```
Given I have successfully logged in
When I check the OS keyring
Then the encryption key should be stored securely
  And the key should only be accessible to the OurCRM application
  And the key should be removed when I log out
```

### Scenario 6: Database schema is created

```
Given a new encrypted database is created
When I examine the database structure
Then the initial schema should be set up
  And all required tables should exist
  And Alembic migrations should be configured
```

## Manual Testing Steps

### Test 1: Verify database is created

1. Complete the setup wizard
2. Navigate to the data directory (e.g., ~/ourcrm/ on Unix)
3. Verify the database file exists
4. Check the file size (should be reasonable, not suspiciously small or huge)
5. Verify the file has appropriate permissions

### Test 2: Verify database is encrypted

1. Open the database file with a text editor
2. Verify you see only binary/encrypted data
3. Try to search for readable text (names, emails, etc.)
4. Verify no readable data is found
5. Try to open the database with a SQLite browser tool
6. Verify the tool reports the database is encrypted

### Test 3: Verify database opens with password

1. Start OurCRM
2. Enter the correct master password
3. Verify the application opens
4. Verify you can create a contact
5. Verify the contact is saved
6. Close the application
7. Restart and log in again
8. Verify the contact is still there

### Test 4: Test wrong password cannot open database

1. Start OurCRM
2. Enter an incorrect password
3. Verify the login fails
4. Try to access the database file directly
5. Verify the file is unreadable without the correct password

### Test 5: Verify OS keyring storage

1. Log in to OurCRM
2. Open the OS keyring manager (Keychain on macOS, Credential Manager on Windows, etc.)
3. Verify the OurCRM entry is present
4. Verify it contains the encryption key
5. Log out
6. Verify the keyring entry is removed

### Test 6: Test database performance

1. Log in to OurCRM
2. Create 100 contacts
3. Measure how long operations take
4. Verify the encryption doesn't significantly slow down the app
5. Document the performance impact

### Test 7: Test database backup

1. Log in to OurCRM
2. Create a backup
3. Verify the backup file is also encrypted
4. Try to read the backup file
5. Verify it's encrypted

### Test 8: Test on all platforms

1. Test database creation on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Database is created during setup
- [ ] Database is encrypted with AES-256-GCM
- [ ] Database file is unreadable without the password
- [ ] Encryption key is derived from master password
- [ ] Encryption key is stored in OS keyring during session
- [ ] Database schema is set up with Alembic
- [ ] Database opens successfully with correct password
- [ ] Database cannot be opened with wrong password
- [ ] All data is encrypted at rest
- [ ] Encryption doesn't significantly impact performance
- [ ] Works on Windows, macOS, and Linux
- [ ] Database location is documented
- [ ] Backup files are also encrypted
Feature: Create Encrypted Database (US-014)
  As a user I want my database encrypted with my master password
  so that my data is secure even if my laptop is stolen

  Scenario: Schema is initialized after database creation
    Given an in-memory database manager
    When I initialize the schema
    Then the alembic_version table should exist

  Scenario: Session key is stored in keyring when session starts
    Given a clean in-memory keyring
    And an in-memory database manager
    When I start a session with key "mysessionkey123456789012345678901"
    Then the keyring should contain the session key under "db_session_key"

  Scenario: Session key is removed from keyring when session closes
    Given a clean in-memory keyring
    And an in-memory database manager
    When I start a session with key "mysessionkey123456789012345678901"
    And I close the session
    Then the keyring should not contain a session key

  Scenario: Database file is created at the given path
    Given a temporary data directory
    When I create a database at that path
    Then a database file should exist at that path

  Scenario: Encrypted database file is not readable as plain SQLite
    Given a temporary data directory
    And an encrypted database for that directory
    When I create and close a new encrypted database with password "SecureP@ssw0rd!2024"
    Then the database file should not contain the SQLite magic bytes

  Scenario: Encrypted database can be reopened with the correct password
    Given a temporary data directory
    And an encrypted database for that directory
    When I create and close a new encrypted database with password "SecureP@ssw0rd!2024"
    And I open the encrypted database with password "SecureP@ssw0rd!2024"
    Then the schema should be accessible through the encrypted database

  Scenario: Opening with wrong password fails
    Given a temporary data directory
    And an encrypted database for that directory
    When I create and close a new encrypted database with password "SecureP@ssw0rd!2024"
    Then opening the encrypted database with "WrongP@ssw0rd!9999" should fail

  Scenario: Tampered database file is rejected
    Given a temporary data directory
    And an encrypted database for that directory
    When I create and close a new encrypted database with password "SecureP@ssw0rd!2024"
    And the database file is tampered with
    Then opening the encrypted database with "SecureP@ssw0rd!2024" should fail

  Scenario: Data written after a mid-session save is persisted
    Given a temporary data directory
    And an encrypted database for that directory
    When I create a new encrypted database with password "SecureP@ssw0rd!2024"
    And I save the encrypted database
    And I write a marker value to the database
    And I close the encrypted database
    And I open the encrypted database with password "SecureP@ssw0rd!2024"
    Then the marker value should be present in the database

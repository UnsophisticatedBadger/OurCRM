# Encrypted Database — Manual Tests

**Story:** [#5 — Encrypt the Database](../../docs/5-create-encrypted-database.md)

## Database file is unreadable outside the app

1. Delete any existing `ourcrm.db` and run `uv run ourcrm`
2. Create a master password and complete recovery password setup
3. With the main window open, open the `ourcrm.db` file in a text/hex editor
4. Confirm it contains no readable SQLite header, table names, or plaintext data

## Session key appears in the OS credential store while the app is running

1. Delete any existing `ourcrm.db` and run `uv run ourcrm`
2. Create a master password and complete recovery password setup
3. With the main window open, open Windows Credential Manager (Control Panel > Credential Manager, or search "Credential Manager")
4. Under "Generic Credentials," confirm an entry with target name containing "ourcrm" is present

## Closing the app removes the session key from the OS credential store

1. With the app open and the session-key credential present (per above), close the main window
2. Reopen Windows Credential Manager and refresh the list
3. Confirm the "ourcrm" session-key credential entry is no longer listed

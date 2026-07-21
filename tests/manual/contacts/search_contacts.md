# Search Contacts — Manual Tests

**Story:** [#64 — Search Contacts](../../docs/64-search-contacts.md)

## User searches by name and sees filtered results

1. Create contacts with varied names
2. Type part of a name in the search box
3. Confirm the list updates with each keystroke to show only matching contacts
4. Confirm matching is case-insensitive (search "john" finds "John Smith")

## User searches by email and phone

1. Type part of a contact's email address — confirm that contact appears
2. Clear and type part of a phone number — confirm the correct contact appears

## User searches by street address, city, and tags

1. Type part of a contact's street address — confirm that contact appears
2. Clear and type a contact's city — confirm that contact appears
3. Clear and type one of a contact's tags — confirm that contact appears

## Partial match works

1. Create contacts "John Smith" and "Johnson"
2. Search for "John" — confirm both appear
3. Search for "Johns" — confirm only "Johnson" appears

## No results shows a clear message

1. Search for a string that matches no contacts
2. Confirm "No contacts found" appears with a way to clear the search

## Ctrl+F focuses the search box

1. Navigate to the Contacts section
2. Press Ctrl+F (Cmd+F on macOS)
3. Confirm the search box is focused and ready to accept input

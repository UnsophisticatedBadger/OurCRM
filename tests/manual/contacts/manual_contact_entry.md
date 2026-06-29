# Manual Contact Entry — Manual Tests

**Story:** [US-015 — Manually Add Contact to Call List](../../../docs/015-manual-contact-entry.md)

## Contact is added with name and phone number only

1. Open the call list or dashboard
2. Click the button to add a contact manually
3. Enter a name and phone number — leave address blank
4. Submit the form
5. Verify the contact appears in the call list immediately

## Contact is added with all fields including address

1. Open the add contact form
2. Enter name, phone number, and property address
3. Submit
4. Verify the contact appears in the call list with all three fields visible

## Invalid phone number shows a plain-language error

1. Open the add contact form
2. Enter a valid name and an invalid phone number (e.g. "abc")
3. Submit
4. Verify an error message explains the problem
5. Verify nothing is saved

## Duplicate phone number triggers a warning

1. Add a contact with phone number 555-123-4567
2. Open the add contact form again
3. Enter a different name but the same phone number
4. Submit
5. Verify a warning asks for confirmation before saving

## Manually added contact behaves identically to an MLS-added contact

1. Add one contact manually and one via MLS search
2. Open the call list
3. Verify both contacts appear in the same format
4. Verify a Call button appears next to both when calling is configured
5. Verify an outcome can be logged for both

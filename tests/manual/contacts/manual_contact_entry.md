# Manually Add Contact To Call List — Manual Tests

**Story:** [#43 — Manually Add Contact To Call List](../../docs/43-manual-contact-entry.md)

## Contact is added with only a name

1. From the dashboard, click "New Contact" (or open the Contacts section and click "New Contact")
2. Enter a first or last name only — leave phone, email, and address blank
3. Submit the form
4. Verify the contact saves without error and appears in the contact list

## Contact is added with all fields including address

1. Open the new contact form
2. Enter name, phone number, and property address
3. Submit
4. Verify the contact appears in the contact list with all fields visible

## Invalid phone number shows a plain-language error

1. Open the new contact form
2. Enter a valid name and an invalid phone number (e.g. "abc")
3. Submit
4. Verify an error message explains the problem next to the phone field
5. Verify nothing is saved

## Duplicate phone number triggers a warning

1. Add a contact with phone number 555-123-4567
2. Open the new contact form again
3. Enter a different name but the same phone number
4. Submit
5. Verify a warning asks for confirmation before saving
6. Confirm the warning and verify the new contact saves alongside the original
7. Repeat, but cancel the warning instead, and verify the form stays open with nothing saved

## New Contact is reachable from the dashboard

1. From the dashboard, click the "New Contact" quick action
2. Verify it navigates to the Contacts section with the new contact form reachable

Note: the dashboard's Contacts stat tile does not yet reflect live counts — that's story #20 (Dashboard Stats Widget), not this story.

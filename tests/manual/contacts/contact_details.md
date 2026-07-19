# View Contact Details — Manual Tests

**Story:** [#58 — View Contact Details](../../docs/58-view-contact-details.md)

## User opens a contact and sees all their data

1. Create a contact with all fields filled
2. Double-click the contact in the list
3. Confirm all fields display the correct values
4. Confirm empty optional fields show "Not provided"

## User navigates between contacts with Previous and Next

1. Create 3 contacts (A, B, C sorted by name)
2. Open contact A
3. Click Next — confirm contact B is shown
4. Click Next — confirm contact C is shown
5. Click Previous — confirm contact B is shown again
6. From contact A, click Previous — confirm it wraps to contact C
7. From contact C, click Next — confirm it wraps back to contact A

## User returns to the list with the same contact selected

1. Open the details for a contact
2. Click "Back to List"
3. Confirm the contact list appears
4. Confirm the contact you were viewing is still highlighted/selected
5. Repeat using the Escape key — confirm the same result

## Edit, Delete, and Add Note buttons are present

1. Open any contact's details
2. Confirm Edit, Delete, and Add Note buttons are visible and enabled
3. Click each and confirm it responds without error (full edit/delete/note flows are built and verified separately under #59, #60, and #61)

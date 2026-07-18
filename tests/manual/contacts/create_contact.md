# Create a New Contact — Manual Tests

**Story:** [#56 — Create a New Contact](../../docs/56-create-new-contact.md)

## User opens the new contact form

1. Navigate to the Contacts section
2. Click "New Contact"
3. Confirm the form opens with all expected fields present and empty

## User creates a contact with all fields filled

1. Open the new contact form
2. Fill in all fields with valid data
3. Click Save
4. Confirm the contact list appears and the new contact is visible
5. Click the contact to confirm all data was saved correctly

## User submits the form with an empty name and sees an error

1. Open the new contact form
2. Leave first and last name empty, fill in other fields
3. Click Save
4. Confirm "Name is required" appears and the form stays open
5. Enter a name and confirm the form can now be saved

## User enters an invalid email and sees a validation error

1. Open the new contact form, enter "notanemail" in the email field
2. Click Save
3. Confirm an email format error appears inline
4. Correct the email and confirm the error clears

## User cancels and confirms nothing was saved

1. Open the new contact form and fill in a name
2. Click Cancel
3. Confirm the form closes and the contact does not appear in the list

## Contact persists after restart

1. Create a contact, close the application
2. Restart and navigate to Contacts
3. Confirm the contact is still there with all fields intact

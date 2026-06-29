# Google Voice Click-to-Call — Manual Tests

**Story:** [US-017 — Google Voice Click-to-Call](../../../docs/017-google-voice-click-to-call.md)

## Google Voice number is configured during initial setup

1. Launch the app for the first time after creating a master password
2. Verify the setup flow prompts for a Google Voice phone number
3. Enter a valid number and confirm
4. Verify the app accepts it and moves to the next setup step

## Invalid number format shows a plain-language error

1. Enter a number in an invalid format during setup
2. Confirm
3. Verify the app shows a clear error and does not save the number

## Google Voice number can be updated in Settings

1. Open the Settings panel
2. Navigate to the calling configuration section
3. Update the Google Voice number and save
4. Verify the new number is used for subsequent click-to-call actions

## Call button appears when Google Voice is configured

1. Open the call list or dashboard
2. Verify each contact shows a Call button

## Clicking Call opens Google Voice with the number pre-filled

1. Click the Call button next to a contact
2. Verify Google Voice opens in the default browser
3. Verify the contact's phone number is pre-filled and ready to dial
4. Complete the call through the headset

## Call button is replaced with plain text when not configured

1. Clear the Google Voice number from Settings
2. Open the call list
3. Verify the Call button is replaced with the plain-text phone number

# Twilio Setup — Manual Tests

**Story:** [US-016 — Twilio Calling Integration](../../../docs/016-twilio-calling-integration.md)

## Twilio credentials are configured during initial setup

1. Launch the app for the first time after creating a master password
2. Verify the setup flow prompts for Twilio Account SID, Auth Token, and phone number
3. Enter valid credentials and confirm
4. Verify the app shows a success message

## Invalid credentials show a plain-language error

1. Enter an incorrect Account SID or Auth Token during setup
2. Confirm
3. Verify the app shows a clear error explaining what is wrong and how to fix it
4. Verify no credentials are saved

## Twilio credentials can be updated in Settings

1. Open the Settings panel
2. Navigate to the Twilio configuration section
3. Update the credentials and save
4. Verify the new credentials are used for subsequent calls

## Call button appears on contacts when Twilio is configured

1. Open the call list
2. Verify each contact shows a Call button
3. Disconnect Twilio credentials (clear them in Settings)
4. Verify the Call button is replaced with a plain-text phone number

## Outbound call connects through the app via headset

1. Connect a headset to the laptop
2. Open the call list and click Call on a contact
3. Verify the call initiates through Twilio
4. Verify audio routes through the headset
5. Complete the call and hang up

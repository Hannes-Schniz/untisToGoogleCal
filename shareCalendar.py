import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the credentials.json file
SERVICE_ACCOUNT_FILE = './credentials.json'

# Required permissions
SCOPES = ['https://www.googleapis.com/auth/calendar']

def share_calendar_interactive():
    """Shares a calendar with a user-provided email and generates a JSON with the calendar ID."""
    try:
        # Get email from user
        shared_email = input("Enter the email address to share the calendar with: ")

        # Get calendar ID from user
        calendar_id = input("Enter the calendar ID to share: ")

        # Authorization with the credentials.json file
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Create calendar service
        service = build('calendar', 'v3', credentials=creds)

        # Create access rule
        rule = {
            'scope': {
                'type': 'user',
                'value': shared_email,
            },
            'role': 'writer'  # 'reader' or 'writer' for edit permissions
        }

        # Add access rule
        created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()

        print(f'Calendar successfully shared with {shared_email}.')
        print(f'Access rule ID: {created_rule["id"]}')

        # Generate JSON file with calendar ID
        calendar_data = {"calendarID": calendar_id}
        with open("environment.json", "w") as f:
            json.dump(calendar_data, f, indent=4)

        print(f'Calendar ID saved to calendar_id.json')

    except Exception as e:
        print(f'Error sharing calendar: {e}')

if __name__ == '__main__':
    share_calendar_interactive()
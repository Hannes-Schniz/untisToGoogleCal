import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the credentials.json file
SERVICE_ACCOUNT_FILE = './credentials.json'

ENVIRONMENT_FILE = './environment.json'

# Required permissions
SCOPES = ['https://www.googleapis.com/auth/calendar']

def share_calendar_interactive():
    """Shares a calendar with a user-provided email and generates a JSON with the calendar ID."""
    try:
        # Get email from user
        shared_email = input("Enter the email address to share the calendar with: ")

        # Get calendar ID from user
        
        configured = input("Do you wish to use the configured Calendar to proceed (yes/no): ") == "yes"
        
        if configured:
            try:
                with open("environment.json", "r") as f:
                    calendar_id = json.load(f)
                    calendar_id = calendar_id['calendarID']
            except:
                print("No calendar configured")
                calendar_id = input("Enter the calendar ID to share: ")
        else:
            calendar_id = input("Enter the calendar ID to share: ")
        
        role = input("Enter a preffered role (reader/writer): ")
        
        while role != "reader" and role != "writer":
            print("Wrong input please enter a correct role to proceed!")
            role = input("Enter a preffered role (reader/writer): ")

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
            'role': role  # 'reader' or 'writer' for edit permissions
        }

        # Add access rule
        created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()

        print(f'Calendar successfully shared with {shared_email}.')
        print(f'Access rule ID: {created_rule["id"]}')

        # Generate JSON file with calendar ID
        calendar_data = {"calendarID": calendar_id}
        with open("environment.json", "w") as f:
            json.dump(calendar_data, f, indent=2)

        print(f'Calendar ID saved to calendar_id.json')

    except Exception as e:
        print(f'Error sharing calendar: {e}')

if __name__ == '__main__':
    share_calendar_interactive()
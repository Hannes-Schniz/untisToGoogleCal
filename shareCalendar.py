import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from configReader import configExtract

# Path to the credentials.json file for Google service account
SERVICE_ACCOUNT_FILE = './credentials.json'

# Path to the environment configuration file
ENVIRONMENT_FILE = './environment.json'

# Flag to indicate if a new calendar configuration is being set
newConf = False

# Required permissions for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def print_help():
    """
    Prints usage instructions for the script.
    """
    print("""
Usage: python shareCalendar.py [--help|-h]

This script shares a Google Calendar with a specified email address and updates the environment.json file with the calendar ID.

Steps:
  1. You will be prompted for the email address to share the calendar with.
  2. You can use the configured calendar ID from environment.json or enter a new one.
  3. Choose the access role: 'reader' or 'writer'.
  4. The script will grant access and update environment.json with the calendar ID.

Example:
  python shareCalendar.py
  python shareCalendar.py --help
""")

def share_calendar_interactive():
    """
    Shares a calendar with a user-provided email and updates environment.json with the calendar ID.
    Prompts the user for email, calendar ID, and access role.
    """
    try:
        # Get email from user
        shared_email = input("Enter the email address to share the calendar with: ")

        # Ask if the user wants to use the configured calendar ID
        configured = input("Do you wish to use the configured Calendar to proceed (yes/no): ") == "yes"
        
        if configured:
            try:
                # Try to load the calendar ID from environment.json
                conf = configExtract(ENVIRONMENT_FILE).conf
                calendar_id = conf['calendarID']
            except:
                # If not found, prompt for a new calendar ID
                print("No calendar configured")
                global newConf
                newConf = True
                calendar_id = input("Enter the calendar ID to share: ")
        else:
            # Prompt for a new calendar ID
            calendar_id = input("Enter the calendar ID to share: ")
        
        # Prompt for the access role
        role = input("Enter a preferred role (reader/writer): ")
        
        # Validate the role input
        while role != "reader" and role != "writer":
            print("Wrong input please enter a correct role to proceed!")
            role = input("Enter a preferred role (reader/writer): ")

        # Authorize using the service account credentials
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Build the Google Calendar service
        service = build('calendar', 'v3', credentials=creds)

        # Create the access rule for the specified email and role
        rule = {
            'scope': {
                'type': 'user',
                'value': shared_email,
            },
            'role': role  # 'reader' or 'writer' for edit permissions
        }

        # Add the access rule to the calendar
        created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()

        print(f'Calendar successfully shared with {shared_email}.')
        print(f'Access rule ID: {created_rule["id"]}')

        # If a new calendar configuration was set, update environment.json
        if (newConf):
            conf = configExtract(ENVIRONMENT_FILE).conf
            conf["calendarID"] = calendar_id
            with open("environment.json", "w") as f:
                json.dump(conf, f, indent=2)
            print(f'Calendar ID saved to environment.json')

    except Exception as e:
        print(f'Error sharing calendar: {e}')

if __name__ == '__main__':
    # Show help if --help or -h is passed as an argument
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print_help()
    else:
        share_calendar_interactive()
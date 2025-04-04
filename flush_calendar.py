import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your credentials.json and environment.json files
SERVICE_ACCOUNT_FILE = 'credentials.json'
ENVIRONMENT_FILE = 'environment.json'

# Scopes (permissions) required for accessing the calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def delete_all_calendar_events(calendar_id):
    """Deletes all events from the specified calendar."""
    try:
        # Authenticate with the service account
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Build the calendar service
        service = build('calendar', 'v3', credentials=creds)

        # Get the list of events
        events_result = service.events().list(calendarId=calendar_id, maxResults=9999).execute()
        events = events_result.get('items', [])

        if not events:
            print(f'No events found in calendar {calendar_id}.')
            return

        # Delete each event
        for event in events:
            event_id = event['id']
            try:
                service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
                print(f'Deleted event: {event_id}')
            except Exception as delete_error:
                print(f'Error deleting event {event_id}: {delete_error}')

        print(f'All events deleted from calendar {calendar_id}.')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    try:
        with open(ENVIRONMENT_FILE, 'r') as f:
            env = json.load(f)
            calendar_id_to_clear = env['calendarID']

        confirmation = input(f"Are you sure you want to delete ALL events from calendar {calendar_id_to_clear}? (yes/no): ")
        if confirmation.lower() == 'yes':
            delete_all_calendar_events(calendar_id_to_clear)
        else:
            print("Deletion cancelled.")

    except FileNotFoundError:
        print(f"Error: {ENVIRONMENT_FILE} not found.")
    except KeyError:
        print(f"Error: 'calendarID' not found in {ENVIRONMENT_FILE}.")
    except json.JSONDecodeError:
        print(f"Error: {ENVIRONMENT_FILE} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
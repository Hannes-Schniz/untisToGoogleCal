from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the credentials.json file
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Required permissions
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_or_create_school_calendar():
    """Checks if a calendar named "school" exists, and creates it if not. Outputs the URL."""
    try:
        # Authorization with the credentials.json file
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Create calendar service
        service = build('calendar', 'v3', credentials=creds)

        # Retrieve calendar list
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        school_calendar = None
        for calendar in calendars:
            if calendar['summary'] == 'school':
                school_calendar = calendar
                break

        if school_calendar:
            print(f'Calendar "school" found (ID: {school_calendar["id"]})')
            print(f'Calendar URL: https://calendar.google.com/calendar/u/0/r?cid={school_calendar["id"]}')
        else:
            # Create calendar "school"
            calendar_details = {
                'summary': 'school',
                'timeZone': 'Europe/Berlin'  # Adjust the time zone as needed
            }
            created_calendar = service.calendars().insert(body=calendar_details).execute()
            print(f'Calendar "school" created (ID: {created_calendar["id"]})')
            print(f'Calendar URL: https://calendar.google.com/calendar/u/0/r?cid={created_calendar["id"]}')

    except Exception as e:
        print(f'Error managing calendars: {e}')

if __name__ == '__main__':
    get_or_create_school_calendar()
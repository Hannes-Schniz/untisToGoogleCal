
#Create Google Project and Google Calendar API key
#add credentials.json
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import pickle
import os.path

class googleCalCon:
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    service = None
    
    def __init__(self):
        self.authenticate()
        self.service = build('calendar', 'v3', credentials=self.creds)
        self.createEntry()
    
    def authenticate(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
    
    
    def createEntry(self):
        # Feature 2: Create a new calendar
        new_calendar = {
            'summary': 'New Python Calendar',
            'timeZone': 'America/Los_Angeles'
        }
        created_calendar = self.service.calendars().insert(body=new_calendar).execute()
        print(f"Created calendar: {created_calendar['id']}")
        event = {
            'summary': 'Python Meeting',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A meeting to discuss Python projects.',
            'start': {
                'dateTime': (datetime.utcnow() + timedelta(days=1)).isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
        }
        created_event = self.service.events().insert(calendarId=created_calendar['id'], body=event).execute()
        print(f"Created event: {created_event['id']}")
        
        
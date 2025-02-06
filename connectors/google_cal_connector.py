
#Create Google Project and Google Calendar API key
#add credentials.json
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import pickle
import os.path
from secrets import environment

class googleCalCon:
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    service = None
    events = None
    winterTimeOffset = 1
    summerTimeOffset = 2
    
    def __init__(self):
        self.authenticate()
        self.service = build('calendar', 'v3', credentials=self.creds)
        self.events = self.getEntries()
        #print(self.events)
    
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
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
    
    #Dateformat : YYYY-MM-DDTHH:MM
    def createEntry(self, name, location, description, start, end, namePrefix, background):
        # Feature 2: Create a new calendar
        event = {
            'summary': namePrefix +name,
            'location': location,
            'description': description,
            'start': {
                'dateTime':  datetime.strptime(start,'%Y-%m-%d %H:%M').isoformat(),
                'timeZone': 'Europe/Berlin',
            },
            'end': {
                'dateTime':  datetime.strptime(end,'%Y-%m-%d %H:%M').isoformat(),
                'timeZone': 'Europe/Berlin',
            },
            'colorId' : background
        }
        if self.eventExists(event, self.events):
            return
        created_event = self.service.events().insert(calendarId=environment.calendarID, body=event).execute()
    
    
    def getEntries(self):
        now = (datetime.utcnow()+timedelta(days=-7)).isoformat() + '+02:00'
        maxTime = (datetime.utcnow()+timedelta(days=7)).isoformat() + '+02:00'
        events_result = self.service.events().list(calendarId=environment.calendarID, timeMin= now,
                                          timeMax=maxTime, singleEvents=True,
                                          orderBy='startTime', timeZone='UTC').execute()
        events = events_result.get('items', [])

        if not events:
            return []
        return events
    
    def eventExists(self, event, eventList):
        for extEvent in eventList:
            if self.eql(extEvent,event):
                return True
        return False
    
    def eql(self, eventOne, eventTwo):
        params = ["description","summary", "location"]
        for param in params:
            try:
                if eventOne[param] != eventTwo[param]:
                    return False
            except:
                continue
        
        if not self.sameDatetime(eventOne['start']['dateTime'],eventTwo['start']['dateTime']):
            return False
        
        if not self.sameDatetime(eventOne['end']['dateTime'],eventTwo['end']['dateTime']):
            return False
        
        return True
    
    def sameDatetime(self,datetime, newTime):
        #split time from date
        split = datetime.split('T')
        #TODO: Winter/Summer Time
        newSplit = newTime.split('T')
        #compare dates
        if split[0] != newSplit[0]:
            return False
        #calc offset +1 (winter time?)
        timeWithOffset = int(split[1].split(':')[0]) + self.winterTimeOffset
        if int(newSplit[1].split(':')[0]) != timeWithOffset and int(newSplit[1].split(':')[1]) != split[1].split(':')[1]:
            #print(split, '|', str(timeWithOffset)+':'+split[1].split(':')[1], newSplit[1])
            return False
        return True
       
        
        
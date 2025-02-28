
#Create Google Project and Google Calendar API key
#add credentials.json
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import pytz

class googleCalCon:
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    service = None
    events = None
    winterTimeOffset = 1
    summerTimeOffset = 2
    env = None
    target_timezone = pytz.timezone('Europe/Berlin')
    
    def __init__(self, weeks):
        service = self.authenticate()
        self.service = service
        with open("environment.json") as env:
            self.env = json.load(env)
        self.events = self.getEntries(weeks)
        #print(self.events)
    
    def authenticate(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

        return build('calendar', 'v3', credentials=credentials)
    
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
        #print(event)
        if self.eventExists(event, self.events):
            #print("tests")
            return
        
        
        created_event = self.service.events().insert(calendarId=self.env['calendarID'], body=event).execute()
        #print(created_event)
    
    
    def getEntries(self, weeks):
        
        utc_now = datetime.utcnow()
        target_now = utc_now.replace(tzinfo=pytz.utc).astimezone(self.target_timezone)
        minTime = (target_now + timedelta(days=-7*weeks)).isoformat()
        maxTime = (target_now + timedelta(days=7*weeks)).isoformat()
        events_result = self.service.events().list(
            calendarId=self.env['calendarID'],
            timeMin=minTime,
            timeMax=maxTime,
            singleEvents=True,
            orderBy='startTime',
            timeZone=str(self.target_timezone)  # Important: Use the timezone string
        ).execute()
        print(events_result)
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
       
        
        
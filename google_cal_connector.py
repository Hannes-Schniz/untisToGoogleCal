
#Create Google Project and Google Calendar API key
#add credentials.json
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import pytz
import telegramBot

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
                'dateTime':  datetime.strptime(start,'%Y-%m-%dT%H:%M').isoformat(),
                'timeZone':  str(self.target_timezone),
            },
            'end': {
                'dateTime':  datetime.strptime(end,'%Y-%m-%dT%H:%M').isoformat(),
                'timeZone':  str(self.target_timezone),
            },
            'colorId' : background
        }
        if self.eventExists(event, self.events):
            return
        
        self.sendMessage(namePrefix, name, location, description, start, end)
        created_event = self.service.events().insert(calendarId=self.env['calendarID'], body=event).execute()
        
    def sendMessage(self,state, summary, location, description, start, end):
        if state.strip() == 'EXAM':
            summary = state + " " + summary
        message = telegramBot.createText(summary, location, description, start.split('T')[0], start.split('T')[1], end.split('T')[1])
        if state.strip() in ['CHANGED','ADDITIONAL','CANCELLED', 'EXAM']:
            telegramBot.sendMessage(message=message)
    
    
    def getEntries(self, weeks):
        
        utc_now = datetime.utcnow()
        target_now = utc_now.replace(tzinfo=pytz.utc).astimezone(self.target_timezone)
        minTime = (target_now).isoformat()
        maxTime = (target_now + timedelta(days=7*weeks)).isoformat()
        events_result = self.service.events().list(
            calendarId=self.env['calendarID'],
            timeMin=minTime,
            timeMax=maxTime,
            singleEvents=True,
            orderBy='startTime',
            timeZone=str(self.target_timezone)  # Important: Use the timezone string
        ).execute()
        #print(events_result)
        events = events_result.get('items', [])
        #print(events)
        
        if not events:
            return []
        return events
    
    def eventExists(self, event, eventList):
        #print(event['summary'])
        summary = event['summary']
        location = event['location']
        description = event['description']
        
        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')
        #print(str(end)+"test", str(start))
        new_start = self.normalize_datetime_string(start)
        new_end = self.normalize_datetime_string(end)
       
        #start = event['start']['dateTime']
        #end = event['end']['dateTime']
        for existing_event in eventList:
            #ex_start = self.normalize_datetime_string(existing_event['start'].get('dateTime'))
            #ex_end = self.normalize_datetime_string(existing_event['end'].get('dateTime'))
            ex_start = existing_event['start'].get('dateTime')
            ex_end = existing_event['end'].get('dateTime')
            # Compare event properties
            if (
                existing_event.get('summary') == summary
                and ex_start == new_start
                and ex_end == new_end
            ):
                #print(existing_event, event)
                return True  # Event already exists

        return False  # Event does not exist
        
        for extEvent in eventList:
            if self.eql(extEvent,event):
                return True
        return False
    
    def normalize_datetime_string(self, datetime_string):
        try:
            # Parse the datetime string
            dt = datetime.fromisoformat(datetime_string)

            # Handle naive datetimes (no timezone info)
            if dt.tzinfo is None:
                if self.target_timezone:
                    dt = self.target_timezone.localize(dt)
                else:
                    dt = pytz.utc.localize(dt) #assume UTC if no timezone and no target timezone

            # Convert to the target timezone if specified
            if self.target_timezone:
                dt = dt.astimezone(self.target_timezone)

            # Format to ISO with offset
            normalized_string = dt.isoformat()
            return normalized_string

        except ValueError:
            return None  # Return None if the string cannot be parsed
    
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
       
        
        
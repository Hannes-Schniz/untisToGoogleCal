#Create Google Project and Google Calendar API key
#add credentials.json
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from configReader import configExtract
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
    verbose = False
    simulate = False
    weeks = None
    
    def __init__(self, weeks, simulate=False, verbose=False):
        self.simulate = simulate  # Add simulation mode flag
        self.verbose = verbose    # Add verbose mode flag
        service = self.authenticate()
        self.service = service
        self.env = configExtract("environment.json").conf
        if weeks != -1:
            self.weeks = weeks
        else:
            self.weeks = None
        self.events = self.getEntries(weeks)  
        
    
    def authenticate(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

        return build('calendar', 'v3', credentials=credentials)
    
    #Dateformat : YYYY-MM-DDTHH:MM
    def createEntry(self, event):
        # Allow override per call, else use instance setting
        if simulate is None:
            simulate = self.simulate
        if verbose is None:
            verbose = self.verbose

        
        if verbose:
            print(f"[VERBOSE] Checking if event exists: {event['summary']} ({event['start']['dateTime']} - {event['end']['dateTime']})")
        if self.eventExists(event, self.events):
            if simulate or verbose:
                print(f"[SIMULATION][VERBOSE] Event already exists and would be skipped: {event['summary']}")
            return

        if simulate:
            print(f"[SIMULATION] Would create event: '{event['summary']}'")
            print(f"  Location: {event['location']}")
            print(f"  Description: {event['description']}")
            print(f"  Start: {event['start']['dateTime']}")
            print(f"  End: {event['end']['dateTime']}")
            print(f"  Color: {event['colorId']}")
            print("-" * 40)
            # Also print the Telegram message that would be sent
            #self.sendMessage(namePrefix, name, location, description, start, end, simulate=True, verbose=verbose)
        else:
            if verbose:
                print(f"[VERBOSE] Creating event: {event['summary']}")
            #self.sendMessage(namePrefix, name, location, description, start, end, verbose=verbose)
            self.service.events().insert(calendarId=self.env['calendarID'], body=event).execute()
       
    def buildEvent(self, name, location, description, start, end, namePrefix, background, simulate=None, verbose=None, oldEvent=""):
        return {
            'summary': namePrefix + name,
            'location': location,
            'description': description + "\n" +oldEvent,
            'start': {
                'dateTime':  datetime.strptime(start, '%Y-%m-%dT%H:%M').isoformat(),
                'timeZone':  str(self.target_timezone),
            },
            'end': {
                'dateTime':  datetime.strptime(end, '%Y-%m-%dT%H:%M').isoformat(),
                'timeZone':  str(self.target_timezone),
            },
            'colorId': background
        }
     
    def sendMessage(self, state, summary, location, description, start, end, simulate=False, verbose=False):
        if state.strip() == 'EXAM':
            summary = state + " " + summary
        message = telegramBot.createText(summary, location, description, start.split('T')[0], start.split('T')[1], end.split('T')[1])
        if state.strip() in ['CHANGED', 'ADDITIONAL', 'CANCELLED', 'EXAM']:
            if simulate:
                print(f"[SIMULATION] Would send Telegram message:\n{message}\n{'-'*40}")
            else:
                if verbose:
                    print(f"[VERBOSE] Sending Telegram message:\n{message}\n{'-'*40}")
                telegramBot.sendMessage(message=message)
    
    
    def getEntries(self, weeks):
        if self.verbose:
            print(f"[VERBOSE] Fetching events for {weeks} weeks ahead from calendar {self.env['calendarID']}")
        utc_now = datetime.utcnow()
        target_now = utc_now.replace(tzinfo=pytz.utc).astimezone(self.target_timezone)
        if weeks == None:
            events_result = self.service.events().list(
            calendarId=self.env['calendarID'],
            singleEvents=True,
            orderBy='startTime',
            timeZone=str(self.target_timezone)  # Important: Use the timezone string
            ).execute()
        else:
            minTime = (target_now - timedelta(days=7)).isoformat()
            maxTime = (target_now + timedelta(days=7*weeks)).isoformat()
            events_result = self.service.events().list(
                calendarId=self.env['calendarID'],
                timeMin=minTime,
                timeMax=maxTime,
                singleEvents=True,
                orderBy='startTime',
                timeZone=str(self.target_timezone)  # Important: Use the timezone string
            ).execute()
        events = events_result.get('items', [])
        if self.verbose:
            print(f"[VERBOSE] Retrieved {len(events)} events from Google Calendar.")
        if not events:
            return []
        return events
    
    def eventExists(self, event, eventList):
        summary = event['summary']
        start = event['start'].get('dateTime')
        end = event['end'].get('dateTime')
        new_start = self.normalize_datetime_string(start)
        new_end = self.normalize_datetime_string(end)
        for existing_event in eventList:
            ex_start = existing_event['start'].get('dateTime')
            ex_end = existing_event['end'].get('dateTime')
            if (
                existing_event.get('summary') == summary
                and ex_start == new_start
                and ex_end == new_end
            ):
                if self.verbose:
                    print(f"[VERBOSE] Found existing event: {summary} ({new_start} - {new_end})")
                return True  # Event already exists
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
    
    def removeEvents(self, verbose=None):
        events = self.getEntries(self.weeks)

        if self.simulate:
            print(f"[SIMULATION] The following events would be deleted from calendar {self.env['calendarID']}:")
            if not events:
                print("  (No events found.)")
            else:
                for event in events:
                    summary = event.get('summary', '(No Title)')
                    start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))
                    end = event.get('end', {}).get('dateTime', event.get('end', {}).get('date', ''))
                    print(f"  - {summary}")
                    print(f"      Start: {start}")
                    print(f"      End:   {end}")
                    print(f"      Event ID: {event['id']}")
            print(f"\n[SIMULATION] {len(events)} event(s) would be deleted. No changes have been made.")
            return

        if verbose is not None:
            self.verbose = verbose
        for event in events:
            event_id = event['id']
            try:
                self.service.events().delete(calendarId=self.env['calendarID'], eventId=event_id).execute()
                if self.verbose:
                    print(f'Deleted event: {event_id}')
            except Exception as delete_error:
                print(f'Error deleting event {event_id}: {delete_error}')

        print(f'All events deleted from calendar {self.env["calendarID"]}.')


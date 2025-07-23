import requests
from configReader import configExtract

class exporter:
    
    urlRest = "https://erato.webuntis.com/WebUntis/api/rest/view/v1/timetable/entries"
    
    conf = configExtract("environment.json").conf
    
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'de-DE,de;q=0.9,en-DE;q=0.8,en;q=0.7,en-US;q=0.6',
    'anonymous-school': conf['anonymous-school'],
    'cookie': conf['cookie']
}

    def getElementMap(self, elements):
        elementMap = {}
        for element in elements:
            elementMap[element['id']] = element
            
        return elementMap
            

    def getData(self, start, end, classID, verbose=False):
        
        optionsRest = "?start="+start+"&end="+end+"&format=2&resourceType=CLASS&resources="+classID+"&periodTypes=&timetableType=STANDARD"
        
        try:
            response = requests.get(self.urlRest + optionsRest, headers=self.headers)
            raw_data = response.json()
        except:
            raise Exception("Failed to retrieve Untis data correctly")
        
        
        periods = []
        
        for day in raw_data['days']:
            date = day['date']
            for entry in day['gridEntries']:
                status = entry['status']
                classType = entry['type']
                moved = False
                oldStart = None
                oldEnd = None
                changes = None
                
                start = entry['duration']['start']
                end = entry['duration']['end']
                if entry['position1']:
                    shortName = entry['position1'][0]['current']['shortName']
                    longName = entry['position1'][0]['current']['longName']
                if entry['position2']:
                    room = entry['position2'][0]['current']['displayName']
                if entry['statusDetail'] == "MOVED":
                    moved = True
                    oldStart = start
                    oldEnd = end
                    start = entry['moved']['start']
                    end = entry['moved']['end']
                if entry['status'] == "CHANGED":
                    changes = []
                    if entry['position1'][0]['removed'] != None:
                        changedClass= changes.append(entry['position1'][0]['removed']['displayName'])
                    if entry['position2'][0]['removed'] != None:
                        changedRoom= changes.append(entry['position2'][0]['removed']['shortName'])
                
                periods.append({'name':shortName, 
                                  'location': room,
                                  'periodText': longName,
                                  'cellState': status,
                                  'date':date,
                                  'start':start,
                                  'end':end,
                                  'type': classType,
                                  'movedStart': oldStart,
                                  'movedEnd': oldEnd,
                                  'changedRoom': changedRoom,
                                  'changedClass': changedClass,
                                  'moved': moved})
                #if verbose:
                #    if entry['statusDetail'] == "MOVED":
                #        print(f"[VERBOSE] period: {periods[-1]}") 
        if verbose:
            print(f"[VERBOSE] {len(periods)} fetched.")  
        return periods

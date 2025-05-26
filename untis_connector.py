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
        
        removed = []
        
        for day in raw_data['days']:
            date = day['date']
            for entry in day['gridEntries']:
                status = entry['status']
                classType = entry['type']
                
                moved = entry['moved'] != None
                
                cancelled = entry['status'] == "CANCELLED"
                
                start = entry['duration']['start']
                end = entry['duration']['end']
                
                if moved:
                    start = entry['moved']['start']
                    end = entry['moved']['end']
                    rstart = entry['duration']['start']
                    rend = entry['duration']['end']
                
                if cancelled:
                    rstart = entry['duration']['start']
                    rend = entry['duration']['end']
                
                if not entry['position1']:
                    continue
                shortName = entry['position1'][0]['current']['shortName']
                longName = entry['position1'][0]['current']['longName']
                if not entry['position2']:
                    continue
                room = entry['position2'][0]['current']['displayName']
                
                periods.append({'name':shortName, 
                                  'location': room,
                                  'periodText': longName,
                                  'cellState': status,
                                  'date':date,
                                  'start':start,
                                  'end':end,
                                  'type': classType})
                
                if moved or cancelled:
                    removed.append({'name':shortName, 
                                  'location': room,
                                  'periodText': longName,
                                  'cellState': status,
                                  'date':date,
                                  'start':rstart,
                                  'end':rend,
                                  'type': classType})
                
                #if verbose:
                #    print(f"[VERBOSE] period: {periods}") 
        if verbose:
            print(f"[VERBOSE] {len(periods)} fetched to add.")
            print(f"[VERBOSE] {len(removed)} fetched to remove.")    
        return [periods, removed]

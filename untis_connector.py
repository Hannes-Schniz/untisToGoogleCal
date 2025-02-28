import requests

class exporter:
    
    urlRest = "https://erato.webuntis.com/WebUntis/api/rest/view/v1/timetable/entries"
    
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'de-DE,de;q=0.9,en-DE;q=0.8,en;q=0.7,en-US;q=0.6',
    'anonymous-school': 'HH-Schule-Karlsruhe',
    'cookie': 'schoolname="_aGgtc2NodWxlLWthcmxzcnVoZQ=="; Tenant-Id="4240600";'
}

    def getElementMap(self, elements):
        elementMap = {}
        for element in elements:
            elementMap[element['id']] = element
            
        return elementMap
            

    def getData(self, start, end, classID, group):
        
        optionsRest = "?start="+start+"&end="+end+"&format=2&resourceType=CLASS&resources="+classID+"&periodTypes=&timetableType=STANDARD"
        
        try:
            response = requests.get(self.urlRest + optionsRest, headers=self.headers)
            raw_data = response.json()
        except:
            raise Exception("Failed to retrieve Untis data correctly")
        
        
        periods = []
        
        for day in raw_data['days']:
            date = day['date']
            status = day['status']
            for entry in day['gridEntries']:
                classType = entry['type']
                
                start = entry['duration']['start']
                end = entry['duration']['end']
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
        print(periods)      
        return periods

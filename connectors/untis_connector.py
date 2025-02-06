import requests

class exporter:

    url = "https://erato.webuntis.com/WebUntis/api/public/timetable/weekly/data"
    
    headers = { 'accept': 'application/json', 
    'cookie': 'schoolname="_aGgtc2NodWxlLWthcmxzcnVoZQ==";',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}


    def getElementMap(self, elements):
        elementMap = {}
        for element in elements:
            elementMap[element['id']] = element
            
        return elementMap
            

    def getData(self, date, classID, group):
        
        options = "?elementType=1&elementId="+classID+"&date="+date+"&formatId=2"
        
        response = requests.get(self.url + options, headers=self.headers)

        raw_data = response.json()['data']['result']['data']
    
        periods = raw_data['elementPeriods'][classID]
        elements = raw_data['elements']
        
        elementMap = self.getElementMap(elements)
        parsedPeriods = []
        for period in periods:
            if period['lessonText'] != group:
                continue
            element_states = period['elements']
            #elements.state [REGULAR|SUBSTITUTED]
            #cellstate [CANCEL|STANDARD|ROOMSUBSTITUTION]
            #print('---------------------------------------')
            #print(elementMap[element_states[1]['id']]['name'])
            #print(elementMap[element_states[2]['id']]['name'])
            #print(str(period['date'])+":",period['startTime'], "->", period['endTime'])
            parsedPeriods.append({'name':elementMap[element_states[1]['id']]['name'], 
                                  'location': elementMap[element_states[2]['id']]['name'],
                                  'periodText': period['periodText'],
                                  'cellState': period['cellState'],
                                  'date':str(period['date']),
                                  'start':period['startTime'],
                                  'end':period['endTime']})
        return parsedPeriods

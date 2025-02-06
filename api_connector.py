import requests

class exporter:

    classID = '3306'

    url = "https://erato.webuntis.com/WebUntis/api/public/timetable/weekly/data"
    options = "?elementType=1&elementId="+classID+"&date=2025-02-03&formatId=2"
    
    
    headers = { 'accept': 'application/json', 
    'cookie': 'schoolname=\"_aGgtc2NodWxlLWthcmxzcnVoZQ==\";',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}


    def getElementMap(self, elements):
        elementMap = {}
        for element in elements:
            elementMap[element['id']] = element
            
        return elementMap
            

    def getData(self):
        

        response = requests.get(self.url + self.options, headers=self.headers)


        raw_data = response.json()['data']['result']['data']
    
        periods = raw_data['elementPeriods'][self.classID]
        elements = raw_data['elements']
        
        elementMap = self.getElementMap(elements)
    
        for period in periods:
            element_states = period['elements']
            #elements.state [REGULAR|SUBSTITUTED]
            #cellstate [CANCEL|STANDARD|ROOMSUBSTITUTION]
            print('---------------------------------------')
            print(elementMap[element_states[1]['id']]['name'])
            print(elementMap[element_states[2]['id']]['name'])
            print(str(period['date'])+":",period['startTime'], "->", period['endTime'])
            
exporterClass = exporter()

exporterClass.getData()
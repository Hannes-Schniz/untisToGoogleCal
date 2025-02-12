import requests
import re

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
        
        #if re.match(date, "[0-9]^8") == None or len(date) != 8:
        #    raise Exception("Incorrect date format in Untis Api call")
        
        options = "?elementType=1&elementId="+classID+"&date="+date+"&formatId=2"
        
        try:
            response = requests.get(self.url + options, headers=self.headers)
            raw_data = response.json()['data']['result']['data']
            #print(raw_data)
        except:
            raise Exception("Failed to retrieve Untis data correctly")
    
        periods = raw_data['elementPeriods'][classID]
        elements = raw_data['elements']
        
        elementMap = self.getElementMap(elements)
        
        parsedPeriods = []
        #print(parsedPeriods)
        for period in periods:
            if period['lessonText'] != group and period['lessonText'] != "":
                continue
            element_states = period['elements']
            parsedPeriods.append({'name':elementMap[element_states[1]['id']]['name'], 
                                  'location': elementMap[element_states[2]['id']]['name'],
                                  'periodText': period['periodText'],
                                  'cellState': period['cellState'],
                                  'date':str(period['date']),
                                  'start':period['startTime'],
                                  'end':period['endTime']})
        return parsedPeriods

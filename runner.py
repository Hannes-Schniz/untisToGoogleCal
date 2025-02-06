from connectors.untis_connector import exporter
from connectors.google_cal_connector import googleCalCon

untis = exporter()
googleCal = googleCalCon()

periods = untis.getData()

def genTime(date, time):
    dateTime = date[:4]+'-'+date[4:6]+'-'+date[6:8]+' '
    if time < 1000:
        dateTime += '0' + str(time)[:1] + ':' + str(time)[1:3]
        return dateTime
    dateTime += str(time)[:2] + ':' + str(time)[2:4]
    return dateTime

for period in periods:
    startTime = genTime(period['date'], period['start'])
    endTime = genTime(period['date'], period['end'])
    googleCal.createEntry(name=period['name'],
                          location=period['location'], 
                          description=period['periodText'],
                          start=startTime,
                          end=endTime
                          )
    
    


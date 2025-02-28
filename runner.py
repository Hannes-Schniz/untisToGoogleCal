from untis_connector import exporter
from google_cal_connector import googleCalCon
from datetime import datetime, timedelta, timezone
from configReader import configExtract
import sys

untis = exporter()


try:
    conf = configExtract().conf
except:
    sys.exit()
    
googleCal = googleCalCon(conf['weeksAhead'])

periods = []

for i in range(int(conf['weeksAhead'])+1):
    currDate = (datetime.now(timezone.utc) + timedelta(days=i*7) ).strftime('%Y-%m-%d')
    dt = datetime.strptime(currDate, '%Y-%m-%d')
    start = dt - timedelta(days=dt.weekday())
    end = (start + timedelta(days=5)).strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    periods += untis.getData(start=start, end=end, classID=conf['classID'], group=conf['group'])

for period in periods:
    namePrefix = ""
    color = conf['color-scheme']['primary']
    if period['cellState'] == 'CANCEL':
        namePrefix = "CANCELLED "
        color = conf['color-scheme']['cancelled']
    if period['cellState'] == 'ROOMSUBSTITUTION':
        namePrefix = "CHANGED "
        color = conf['color-scheme']['changed']
    if period['type'] == 'EXAM':
        namePrefix = "EXAM "
        color = conf['color-scheme']['exam']
    startTime = period['start']
    endTime = period['end']
    googleCal.createEntry(name=period['name'],
                          namePrefix=namePrefix,
                          location=period['location'], 
                          description=period['periodText'],
                          start=startTime,
                          end=endTime,
                          background=color
                          )
    
    


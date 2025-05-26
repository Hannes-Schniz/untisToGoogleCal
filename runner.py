from untis_connector import exporter
from google_cal_connector import googleCalCon
from datetime import datetime, timedelta, timezone
from configReader import configExtract
import sys

# Help text for CLI usage
HELP_TEXT = """
Syncs your Untis timetable to Google Calendar and sends Telegram notifications for changes.

Usage:
  python runner.py

Options:
  -h, --help    Show this help message and exit

This script fetches your Untis timetable and updates your Google Calendar accordingly.
It also sends notifications via Telegram if configured.
"""

# Show help and exit if -h or --help is passed
if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
    print(HELP_TEXT)
    sys.exit(0)

simulate = "--simulate" in sys.argv

verbose = "--verbose" in sys.argv or "-v" in sys.argv

untis = exporter()

try:
    conf = configExtract("config.json").conf
except:
    sys.exit()
    
googleCal = googleCalCon(conf['weeksAhead'], simulate=simulate, verbose=verbose)

periods = []

toRemove = []

for i in range(int(conf['weeksAhead'])+1):
    currDate = (datetime.now(timezone.utc) + timedelta(days=i*7) ).strftime('%Y-%m-%d')
    dt = datetime.strptime(currDate, '%Y-%m-%d')
    start = dt - timedelta(days=dt.weekday())
    end = (start + timedelta(days=5)).strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    data = untis.getData(start=start, end=end, classID=conf['classID'], verbose=verbose)
    periods += data[0]
    toRemove += data[1]

for period in periods:
    namePrefix = ""
    color = conf['color-scheme']['primary']
    if period['cellState'] == 'CANCELLED':
        namePrefix = "CANCELLED "
        color = conf['color-scheme']['cancelled']
    if period['cellState'] == 'CHANGED':
        namePrefix = "CHANGED "
        color = conf['color-scheme']['changed']
    if period['cellState'] == 'ADDITIONAL':
        namePrefix = "ADDITIONAL "
        color = conf['color-scheme']['changed']
    if period['type'] == 'EXAM':
        namePrefix = "EXAM "
        color = conf['color-scheme']['exam']
    startTime = period['start']
    endTime = period['end']
    if period['name'] == None:
        continue
    
    #print(period['cellState'])
    googleCal.createEntry(name=period['name'],
                          namePrefix=namePrefix,
                          location=period['location'], 
                          description=period['periodText'] + "\n" + period['cellState'],
                          start=startTime,
                          end=endTime,
                          background=color
                          )
    
oldEvents = []

for mark in toRemove:
    namePrefix = ""
    color = conf['color-scheme']['primary']
    if mark['cellState'] == 'CANCELLED':
        namePrefix = "CANCELLED "
        color = conf['color-scheme']['cancelled']
    if mark['cellState'] == 'CHANGED':
        namePrefix = "CHANGED "
        color = conf['color-scheme']['changed']
    if mark['cellState'] == 'ADDITIONAL':
        namePrefix = "ADDITIONAL "
        color = conf['color-scheme']['changed']
    if mark['type'] == 'EXAM':
        namePrefix = "EXAM "
        color = conf['color-scheme']['exam']
    startTime = mark['start']
    endTime = mark['end']
    if mark['name'] == None:
        continue
    
    oldEvent = googleCal.buildEvent(name=mark['name'],
                          namePrefix=namePrefix,
                          location=mark['location'], 
                          description=mark['periodText'] + "\n" + mark['cellState'],
                          start=startTime,
                          end=endTime,
                          background=color)
    
    oldEvents += [oldEvent]

googleCal.deleteOldEvents(oldEvents)
    
    






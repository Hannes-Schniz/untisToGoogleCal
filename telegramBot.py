import requests
import env
import shareCalendarBot
import time

TOKEN = env.telegramToken
chat_id = env.telegramChat

def sendMessage(message):
    params = {"chat_id":chat_id,"text": message, "parse_mode": "HTML"}
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url=url, params=params)
    
def createText(summary, location, description, date, start, end ):
    date = f"{date.split('-')[2]}.{date.split('-')[1]}.{date.split('-')[0]}"
    return f"<b>{summary}</b>\n<b>Raum:</b> {location}\n<b>Stunde</b>: {date} {start}-{end}\n<b>Beschreibung:</b> {description}"
    
def shareCalendar():
    params = {}
    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        print(requests.get(url=url, params=params).json())
        time.sleep(1)
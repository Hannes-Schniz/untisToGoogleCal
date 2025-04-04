import requests
import env
TOKEN = env.telegramToken
chat_id = env.telegramChat

def sendMessage(message):
    params = {"chat_id":chat_id,"text": message, "parse_mode": "HTML"}
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url=url, params=params)
    
def createText(summary, state, location, description, date, start, end ):
    date = f"{date.split("-")[2]}.{date.split("-")[1]}.{date.split("-")[0]}"
    return f"<b>{summary}</b>\n<b>Raum:</b> {location}\n<b>Stunde</b>: {date} {start}-{end}\n<b>Beschreibung:</b> {description}"
    
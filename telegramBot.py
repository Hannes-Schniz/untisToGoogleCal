import requests
import env
TOKEN = env.telegramToken
chat_id = env.telegramChat

def sendMessage(message):
    params = {"chat_id":chat_id,"text": message}
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url=url, params=params)
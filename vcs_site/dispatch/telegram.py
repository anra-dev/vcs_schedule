import os
import requests

from django.conf import settings


token = settings.BOT_API_TOKEN
url = settings.BOT_URL
action = {'1': "/sendMessage"}
full_url = url + token + action['1']


def send_telegram_message(message, chat_id):
    request = requests.post(full_url, data={
         "chat_id": chat_id,
         "text": message
          })
    print('Отправил сообщение на :', full_url)
    print('Статус:', request.status_code)
    if request.status_code != 200:
        raise Exception("post_text error")


def send_telegram(text: str):
    token = os.getenv("TELEGRAM_API_TOKEN")
    url = "https://api.telegram.org/bot"
    channel_id = "325848334"
    url += token
    action = {'1': "/sendMessage"}
    method = url + action['1']
    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })
    if r.status_code != 200:
        raise Exception("post_text error")


if __name__ == '__main__':
    send_telegram("hello world!")

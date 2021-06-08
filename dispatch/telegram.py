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
    if request.status_code != 200:
        raise Exception("post_text error", request.status_code)


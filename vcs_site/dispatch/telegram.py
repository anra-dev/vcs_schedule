import os
import requests

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
    print(r.json)
    if r.status_code != 200:
        raise Exception("post_text error")


if __name__ == '__main__':
    send_telegram("hello world!")

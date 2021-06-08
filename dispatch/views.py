import json

from django.views import View
from django.http import JsonResponse
from .telegram import send_telegram_message
from .message import get_message_for_booking_today, get_message_for_booking_all

unknown_command = "Неизвестная команда! \n" \
                  "Команды:\n" \
                  "/all - все мероприятия\n"\
                  "/today - мероприятия запланированные на сегодня"


class TelegramBotView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            print(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
            text = data["message"]["text"].strip().lower()
            print("text: ", text)
            chat_id = data["message"]["chat"]['id']
        except Exception as e:
            print('error: ', e)
            return JsonResponse({"ok": "POST request processed"})
        if text == '/start':
            answer = "Вас привествует volganet_bot!"
        elif text == '/today':
            answer = get_message_for_booking_today(chat_id)
        elif text == '/all':
            answer = get_message_for_booking_all(chat_id)
        else:
            answer = unknown_command
        send_telegram_message(answer, chat_id)
        return JsonResponse({"ok": "POST request processed"})



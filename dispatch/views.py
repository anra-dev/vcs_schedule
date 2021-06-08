import json

from django.views import View
from django.http import JsonResponse
from .telegram import send_telegram_message
from .message import get_message_for_booking_today


class TelegramBotView(View):
    def post(self, request):
        try:
            t_data = json.loads(request.body)
            print(json.dumps(t_data, sort_keys=True, indent=4))
            t_message_text = t_data["message"]["text"]
            t_chat_id = t_data["message"]["chat"]['id']
            if t_message_text == '/today':
                t_message_text = get_message_for_booking_today(t_chat_id)
            print('Сообщение', t_message_text)
            print('Чат', t_chat_id)
            send_telegram_message(t_message_text, t_chat_id)
        except Exception as e:
            return JsonResponse({"ok": "POST request processed"})

        return JsonResponse({"ok": "POST request processed"})



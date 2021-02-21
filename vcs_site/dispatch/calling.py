from .models import Message
from .message import get_message, get_recipients
from .telegram import send_telegram_message
from .mail import send_mail_message


def send_out(obj):
    message = get_message(obj)
    recipients, recipients_obj_list = get_recipients(obj)

    for chat_id in recipients['telegram']:
        send_telegram_message(message, chat_id)

    for mail in recipients['mail']:
        send_mail_message(message, mail)

    Message.objects.create(message, recipients_obj_list)
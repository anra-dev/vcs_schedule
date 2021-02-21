from .models import Message
from .message import get_message, get_recipients
from .telegram import send_telegram_message
from .mail import send_mail_message


def send_out(obj=None):
    message = get_message(obj)
    recipients, recipients_obj_list = get_recipients(obj)
    send_mail_message(message, recipients_obj_list)

    for chat_id in recipients['telegram']:
        if chat_id is not None and chat_id:
            send_telegram_message(message, chat_id)

    for mail in recipients['mail']:
        if mail is not None and mail:
            send_mail_message(message, mail)


def save_message(message, recipients_obj_list):
    message_obj = Message.objects.create(message=message)
    message_obj.recipient.set(recipients_obj_list)

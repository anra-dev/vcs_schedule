import threading

from .models import Message
from .message import get_message, get_recipients, get_message_for_booking_all, get_message_for_booking_today
from .telegram import send_telegram_message
from .mail import send_mail_message


def run_async(func, args):
    threading.Thread(target=func, args=args).start()


def send_out_message(event=None):
    message = get_message(event)
    recipients, recipients_obj_list = get_recipients(event)
    save_message(message=message, recipients_obj_list=recipients_obj_list)

    for chat_id in recipients['telegram']:
        if chat_id is not None and chat_id:
            run_async(send_telegram_message, (message, chat_id))
    for mail in recipients['mail']:
        if mail is not None and mail:
            run_async(send_mail_message, (message, mail))


def send_telegram_message_booking_all(chat_id):
    answer = get_message_for_booking_all(chat_id)
    run_async(send_telegram_message, (answer, chat_id))


def send_telegram_message_booking_today(chat_id):
    answer = get_message_for_booking_today(chat_id)
    run_async(send_telegram_message, (answer, chat_id))


def save_message(message, recipients_obj_list):
    message_obj = Message.objects.create(message=message)
    message_obj.recipient.set(recipients_obj_list)

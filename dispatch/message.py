import datetime
from django.db.models import Q

from schedule.enums import StatusEnum
from schedule.models import User, get_object_or_none, Event
from dispatch.templates_message import get_message_event_ready, get_message_bookings


def get_message(event=None):
    return get_message_event_ready(event)


def get_recipients(event=None):
    users = [event.owner, event.booking_assistant]

    recipients = {'mail': [], 'telegram': []}
    for user in set(users):
        if user.subscribe_mail:
            recipients['mail'].append(user.email)
        if user.subscribe_telegram:
            recipients['telegram'].append(user.telegram)
    return recipients, users


def get_message_for_booking_today(chat_id):
    user = get_object_or_none(User, telegram=chat_id)
    if user is not None:
        events_today = Event.objects.filter(
            Q(
                status=StatusEnum.STATUS_READY,
                date=datetime.datetime.now(),
                with_booking=True,
            ),
            Q(owner=user) | Q(booking_assistant=user),
        )
        if events_today:
            message = ''
            for event in events_today:
                message += get_message_event_ready(event)
            return message
        else:
            return "Сегодня нет запланированных и обработанных мероприятий"
    else:
        return "Пользователь не зарегистрирован в системе"


# TODO: Кондидат на рефакторизацию
def get_message_for_booking_all(chat_id):
    user = get_object_or_none(User, telegram=chat_id)
    if user is not None:
        all_events = Event.objects.filter(
            Q(
                status=StatusEnum.STATUS_READY,
                with_booking=True,
            ),
            Q(owner=user) | Q(booking_assistant=user),
        )
        if all_events:
            message = ''
            for event in all_events:
                message += get_message_event_ready(event)
            return message
        else:
            return "Нет запланированных и обработанных мероприятий"
    else:
        return "Пользователь не зарегистрирован в системе"

import datetime
from django.db.models import Q
from schedule.models import Booking, Conference, User, get_object_or_none
from .templates_message import get_message_event_ready, get_message_bookings


def get_message(event=None):
    conferences = Conference.objects.filter(event=event).exclude(booking__without_conference=False)
    bookings = Booking.objects.filter(event=event)
    return get_message_event_ready(event, conferences, bookings)


def get_recipients(event=None):
    users = [booking.assistant for booking in Booking.objects.filter(event=event)]
    users.append(event.owner)

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
        bookings_today = Booking.objects.filter(Q(status='ready', date=datetime.datetime.now()),
                                               Q(owner=user) | Q(assistant=user))
        if bookings_today:
            return get_message_bookings(bookings_today)
        else:
            return "Сегодня нет запланированных и обработанных мероприятий"
    else:
        return "Пользователь не заарегистрирован в системе"

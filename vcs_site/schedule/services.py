from django.db.models import Sum, Q
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from dispatch.calling import send_out_message
from .models import Conference, Booking


def check_free_quota(conf_id, application, date, time_start, time_end):
    """
    Вычисляет количество свободных лицензий в заданный интервал времени. НЕЙМИНГ АХТУНГ!!!!!
    """
    quota = application.quota
    # Это мероприятия которые начинаются во время планируемого мероприятия. Исключаем планируемое.
    conf_list = Conference.objects.filter(date=date, application=application, type='local',
                                          time_start__gte=time_start, time_start__lt=time_end).exclude(pk=conf_id)
    # Квота изменяется в момент начала мероприятий. Выбираем точки
    points = [conf.time_start for conf in conf_list]
    points.append(time_start)
    # Считаем квоту в точках
    spent_quota_list = []
    for point in set(points):
        spent_quota = Conference.objects.filter(date=date, application=application, type='local', time_start__lte=point,
                                                time_end__gt=point).exclude(pk=conf_id).aggregate(Sum('quota'))
        if spent_quota['quota__sum']:
            spent_quota_list.append(spent_quota['quota__sum'])
    if len(spent_quota_list) == 0:
        return quota
    spent_quota = max(spent_quota_list)
    if spent_quota >= quota:
        return 0
    return quota - spent_quota


def check_room_is_free(booking_id, room, date, time_start, time_end):
    """
    Проверяет свободна ли комната room в день data d промежутке времени между time_start и time_end.
    Если свободна то возвращает True иначе False.
    """
    booking_on_date = Booking.objects.filter(
        Q(date=date, room=room), Q(time_start__gte=time_start, time_start__lt=time_end) |
        Q(time_start__lte=time_start, time_end__gt=time_start)
    ).exclude(pk=booking_id)
    return bool(booking_on_date)


@receiver(post_save, sender=Conference)
@receiver(post_save, sender=Booking)
def update_status_event(instance, **kwargs):
    """Функция обновляет статус мероприятия"""
    event = instance.event
    conferences_status = [conf.status for conf in Conference.objects.filter(event=event)]  # возможно лучше union()
    bookings_status = [booking.status for booking in Booking.objects.filter(event=event)]
    status = conferences_status + bookings_status

    def _set_event_status(set_status: str):
        event.status = set_status
        event.save()
    if 'wait' in status:
        _set_event_status('wait')
        # send_out_message(event)  # удалить
    if 'rejection' in status:
        _set_event_status('rejection')
    if set(status) <= {'ready', 'completed'}:
        _set_event_status('ready')
        send_out_message(event)  # раскомментировать
    if status[1:] == status[:-1] and status[0] == 'completed':  # Все элементы списка равны
        _set_event_status('completed')


def set_status_archive(model, time):
    """Функция которая устанавливает статус Архивный для прошедших Конференций и Броней"""
    pass


@receiver(post_save, sender=Conference)
@receiver(post_save, sender=Booking)
def update_date_event(instance, **kwargs):
    """Функция определяет и обновляет дату начала и конца мероприятия"""
    event = instance.event
    conferences_date = [conf.date for conf in Conference.objects.filter(event=event)]  # возможно лучше union()
    bookings_date = [booking.date for booking in Booking.objects.filter(event=event)]
    dates = conferences_date + bookings_date
    event.date_start = min(dates)
    event.date_end = max(dates)
    event.save()



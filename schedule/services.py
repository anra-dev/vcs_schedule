from datetime import date as datetime_date

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from dispatch.calling import send_out_message
from schedule.models import Event, Conference, Booking


@receiver(post_save, sender=Conference)
@receiver(post_save, sender=Booking)
@receiver(post_delete, sender=Conference)
@receiver(post_delete, sender=Booking)
def update_status_event(instance, **kwargs):
    """Функция обновляет статус мероприятия"""
    event = instance.event
    conferences_status = [conf.status for conf in Conference.objects.filter(event=event)]  # возможно лучше union()
    bookings_status = [booking.status for booking in Booking.objects.filter(event=event)]
    status = conferences_status + bookings_status

    def _set_event_status(set_status: str):
        """Функция обновляет статус мероприятия и отправляет уведомления для мероприятий со статусом Готово"""
        event.status = set_status
        event.save()
    if not status:
        _set_event_status('draft')
    else:
        if 'wait' in status:
            _set_event_status('wait')
        if 'rejection' in status:
            _set_event_status('rejection')
        if set(status) <= {'ready', 'completed'} and event.status != 'ready':
            _set_event_status('ready')
            send_out_message(event)
        if status[1:] == status[:-1] and status[0] == 'completed':  # Все элементы списка равны
            _set_event_status('completed')


def set_status_completed(queryset):
    """Функция которая устанавливает статус Архивный для прошедших моделей"""
    pass
    # today = datetime_date.today()
    # if queryset.model == Event:
    #     completed_list = queryset.filter(date_start__lt=today, status__in=['wait', 'ready', 'rejection'])
    #     if completed_list:
    #         conference = Conference.objects.filter(event__in=completed_list, date__lt=today)
    #         booking = Booking.objects.filter(event__in=completed_list, date__lt=today)
    #         conference.update(status='completed')
    #         booking.update(status='completed')
    #         completed_list.filter(date_end__lt=today).update(status='completed')
    # if queryset.model in [Conference, Booking]:
    #     completed_list = queryset.filter(date__lt=today, status__in=['wait', 'ready', 'rejection'])
    #     if completed_list:
    #         completed_list.update(status='completed')


@receiver(post_save, sender=Conference)
@receiver(post_save, sender=Booking)
@receiver(post_delete, sender=Conference)
@receiver(post_delete, sender=Booking)
def update_date_event(instance, **kwargs):
    """Функция определяет и обновляет дату начала и конца мероприятия"""
    event = instance.event
    conferences_date = [conf.date for conf in Conference.objects.filter(event=event)]  # возможно лучше union()
    bookings_date = [booking.date for booking in Booking.objects.filter(event=event)]
    dates = conferences_date + bookings_date
    event.date_start = min(dates) if dates else None
    event.date_end = max(dates) if dates else None
    event.save()



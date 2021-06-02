from django.core.exceptions import ValidationError
from datetime import date as datetime_date

from django.db.models import Sum, Q
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from dispatch.calling import send_out_message
from .models import Event, Conference, Booking


def check_free_quota(conf_id, server, date, time_start, time_end):
    """
    Вычисляет количество свободных лицензий в заданный интервал времени. НЕЙМИНГ АХТУНГ!!!!!
    """
    quota = server.quota
    # Это мероприятия которые начинаются во время планируемого мероприятия. Исключаем планируемое если оно есть.
    conf_list = Conference.objects.filter(date=date, server=server, time_start__gte=time_start,
                                          time_start__lt=time_end).exclude(pk=conf_id)
    # Квота изменяется в момент начала мероприятий. Выбираем точки
    time_start_list = [conf.time_start for conf in conf_list]
    time_start_list.append(time_start)
    # Считаем квоту в точках
    spent_quota_list = []
    for time_start in set(time_start_list):
        spent_quota = Conference.objects.filter(date=date, server=server, time_start__lte=time_start,
                                                time_end__gt=time_start).exclude(pk=conf_id).aggregate(Sum('quota'))
        if spent_quota['quota__sum']:
            spent_quota_list.append(spent_quota['quota__sum'])
    if len(spent_quota_list) == 0:
        # Все квоты свободны
        return quota
    spent_quota = max(spent_quota_list)
    if spent_quota >= quota:
        # Все квоты заняты
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
        if set(status) <= {'ready', 'completed'}:
            _set_event_status('ready')
            send_out_message(event)
        if status[1:] == status[:-1] and status[0] == 'completed':  # Все элементы списка равны
            _set_event_status('completed')


def set_status_completed(queryset):
    """Функция которая устанавливает статус Архивный для прошедших моделей"""
    today = datetime_date.today()
    if queryset.model == Event:  # переписать через isinstance
        completed_list = queryset.filter(date_start__lt=today, status__in=['wait', 'ready', 'rejection'])
        if completed_list:
            conference = Conference.objects.filter(event__in=completed_list, date__lt=today)
            booking = Booking.objects.filter(event__in=completed_list, date__lt=today)
            conference.update(status='completed')
            booking.update(status='completed')
            completed_list.filter(date_end__lt=today).update(status='completed')
    if queryset.model in [Conference, Booking]:  # переписать через isinstance
        completed_list = queryset.filter(date__lt=today, status__in=['wait', 'ready', 'rejection'])
        if completed_list:
            completed_list.update(status='completed')


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


def check_time(time_start, time_end, **kwargs):
    # Начало конференции должно быть раньше ее конца
    if time_start >= time_end:
        raise ValidationError({
            'time_start': 'Время начала не может совпадать или быть позже окончания',
            'time_end': 'Время окончания не может совпадать или быть раньше начала'
        })


def check_required_field(arg):
    if arg is None:
        raise ValidationError({field: 'Это поле обязательное'})


def check_quota_lt_server_quota(quota, server, **kwargs):
    if quota > server.quota:
        raise ValidationError({'quota': f'Превышено количество участников для данного приложения! '
                                        f'Максимальное число пользователей: {server.quota}'})


def check_conference_data_valid(conf_id, server, **kwargs):
    print('___________________', server)
    try:
        check_time(**kwargs)
        # Проверка для локальных серверов

        if server.server_type == server.SERVER_TYPE_LOCAL:
            check_required_field('quota', **kwargs)
            check_quota_lt_server_quota(**kwargs)
    except ValidationError as e:
        print(e)


        # # Проверка полей
        # if not quota:
        #     # Квота обязательное поле
        #     self.add_error('quota', my_default_errors['required'])
        # elif quota > server.quota:
        #     # Квота не должна превышать квоту сервера
        #     self.add_error('quota', f'Превышено количество участников для данного приложения! '
        #                             f'Максимальное число пользователей: {server.quota}')
        # else:
        #     # Проверка свободных квот на сервере на предполагаемое время
        #     free_quota = check_free_quota(conf_id=conf_id, server=server, date=date,
        #                                   time_start=time_start, time_end=time_end)
        #     if free_quota == 0:
        #         # Все квоты заняты
        #         self.add_error('quota', f'Все лицензии заняты! Выберите другое время')
        #     elif quota > free_quota:
        #         # Запрашиваемые квоты больше чем свободные квоты
        #         self.add_error('quota', f'Количество участников превышает количество свободных лицензий!'
        #                                 f' На это время свободно всего {free_quota} лицензий')
        #
        # # Проверка для внешних серверов
        # if server.server_type == server.SERVER_TYPE_EXTERNAL:
        #     # Очищаем поля не предусмотренные для заполнения пользователем для конференций на внешних серверах
        #     cleaned_data['quota'] = None
        #
        #     # Проверка полей
        #     if not description:
        #         # Квота обязательное поле
        #         self.add_error('description', my_default_errors['required'])
        #
        #     # Поле Ссылка или Файл не должны быть пустыми
        #     if not link and not file:
        #         raise forms.ValidationError(f"Необходимо заполнить поле {self.fields['link'].label} или "
        #                                     f"{self.fields['file'].label}")



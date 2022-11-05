import datetime

from django.db.models import Sum, Q, F, Value
from django.db.models.functions import Concat

from schedule.enums import ServerTypeEnum, StatusEnum
from schedule.models import Server, Event, User


def check_free_quota(event_id, conf_server, date, time_start, time_end):
    """
    Вычисляет количество свободных лицензий на сервере
    в заданный интервал времени.
    Находим мероприятия, которые начинаются во время планируемого
    мероприятия и используют тот же сервер. Количество свободных
    лицензий меняется в момент начала таких мероприятий + начало нашего
    мероприятия. Проверяем загруженность сервера в эти моменты.
    """
    time_start_events = list(
        Event.objects.filter(
            date=date,
            conf_server=conf_server,
            time_start__gte=time_start,
            time_start__lt=time_end,
        ).exclude(
            Q(pk=event_id) | Q(conf_status=StatusEnum.STATUS_REJECTION),
        ).values_list(
            'time_start',
            flat=True,
        )
    )
    time_start_events.append(time_start)
    # Считаем лицензии в моменты начала мероприятий
    list_number_clients = []
    for time_start in set(time_start_events):
        number_clients = Event.objects.filter(
            date=date,
            conf_server=conf_server,
            time_start__lte=time_start,
            time_end__gt=time_start,
        ).exclude(
            Q(pk=event_id) | Q(conf_status=StatusEnum.STATUS_REJECTION),
        ).aggregate(
            sum=Sum('conf_number_clients'),
        ).get('sum')
        if number_clients:
            list_number_clients.append(number_clients)
    server_quota = conf_server.quota
    if len(list_number_clients) == 0:
        # Все квоты свободны
        return server_quota
    max_number_clients = max(list_number_clients)
    if max_number_clients >= server_quota:
        # Все квоты заняты
        return 0
    return server_quota - max_number_clients


def check_room_is_free(event_id, booking_room, date, time_start, time_end):
    """
    Проверяет свободна ли комната room в день data в промежутке
    времени между time_start и time_end.
    Если свободна то возвращает True иначе False.
    """
    return not Event.objects.filter(
        Q(date=date, booking_room=booking_room),
        Q(time_start__gte=time_start, time_start__lt=time_end) |
        Q(time_start__lte=time_start, time_end__gt=time_start)
    ).exclude(
        Q(pk=event_id) | Q(conf_status=StatusEnum.STATUS_REJECTION)
    ).exists()


def get_server_choice(room_id: int, user: User) -> list:
    choices = [("", "---------", None)]
    if room_id:
        assert user.organization.room.filter(id=room_id).exists()
        data = Server.objects.filter(
            room=room_id,
        ).annotate(
            sever_and_app=Concat('name', Value(' - '), 'application__name')
        ).values_list(
            'pk',
            'sever_and_app',
            'type',
        )
        choices.extend(data)
    return choices


def get_conferences_on_server(server_id: int, date: datetime.date) -> list:
    data = Event.objects.filter(
        conf_server_id=server_id,
        date=date,
        conf_server__type=ServerTypeEnum.SERVER_TYPE_LOCAL,
    ).annotate(
        count=F('conf_number_clients'),
        max_count=F('conf_server__quota'),
    ).values(
        'name',
        'time_start',
        'time_end',
        'count',
        'max_count',
    )

    return list(data)


def get_bookings_on_room(room_id: int, date: datetime.date) -> list:
    data = Event.objects.filter(
        booking_room_id=room_id,
        date=date,
    ).values(
        'name',
        'time_start',
        'time_end',
    )

    return list(data)

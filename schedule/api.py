import datetime

from django.db.models import F, Value
from django.db.models.functions import Concat

from schedule.enums import ServerTypeEnum
from schedule.models import Server, Event, User


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

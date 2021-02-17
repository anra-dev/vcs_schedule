from django.db.models import Sum, Q
from .models import Conference, Application, Booking, Room
import datetime


def check_ability_to_create_conf(conf_id, application, date, time_start, time_end, quote):
    """
    Проверяет возможность проведения конференции в заданный интервал времени и возвращает True
    если количество занятых лицензий на протежении всего промежутка времени
    между time_start и time_end в сумме с запрашиваемой квотой не превышает базовое
    количество лицензий  приложения application. При редактировании используется conf_id.
    """
    # Создаем QuerySet - это мероприятия которые начинаются во время планируемого мероприятия. Исключаем текущее.
    query_set = Conference.objects.filter(date=date, application=application, type='local',
                                          time_start__gte=time_start, time_start__lt=time_end).exclude(pk=conf_id)
    # Квота изменяется в момент начала мероприятий. Выбираем точки
    points = []
    for obj in query_set:
        points.append(obj.time_start)
    # Считаем квоту в точках
    qty_lic_in_pont = []
    for point in set(points):
        qty_lic = Conference.objects.filter(date=date, application=application, type='local', time_start__lte=point,
                                            time_end__gt=point).exclude(pk=conf_id).aggregate(Sum('quota'))
        qty_lic_in_pont.append(qty_lic['quota__sum'])
    lic = Application.objects.get(name=application).quota
    if qty_lic_in_pont:
        quote += max(qty_lic_in_pont)
    return lic >= quote


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


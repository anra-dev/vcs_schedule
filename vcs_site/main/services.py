from django.db.models import Q, Sum
from .models import Conference, Application
import datetime


def check_ability_to_create(application, date, time_start, time_end, quote):
    """
    Проверяет возможность проведения конференции в заданный интервал времени и возвращает True
    если количество занятых лицензий на протежении всего промежутка времени
    между time_start и time_end в сумме с запрашиваемой квотой не превышает базовое
    количество лицензий  приложения application
    """
    print('На входе', quote)
    # Создаем QuerySet - это мероприятия которые начинаются во время планируемого мероприятия.
    query_set = Conference.objects.filter(date=date, application=application,
                                          time_start__gte=time_start, time_start__lt=time_end)
    # Квота изменяется в момент начала мероприятий. Выбираем точки
    points = []
    for obj in query_set:
        points.append(obj.time_start)
    # Сичтаем квоту в точках
    qty_lic_in_pont = []
    for point in set(points):
        qty_lic = Conference.objects.filter(date=date, application=application,
                                            time_start__lte=point, time_end__gt=point).aggregate(Sum('quota'))
        qty_lic_in_pont.append(qty_lic['quota__sum'])
    print('Результат проверки', qty_lic_in_pont)
    # Возвращаем максимум
    lic = Application.objects.get(name=application).quota
    if qty_lic_in_pont:
        quote += max(qty_lic_in_pont)
    print('На выходе', quote)
    return lic >= quote



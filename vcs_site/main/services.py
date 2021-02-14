from .models import Event, Staffer, VideoConf, ReservedRoom

def get_context_for_event_view(request: str, filter_status: tuple, filter_user: bool) -> dict:
    """
    Возвращает контекст для представлений мероприятий
    :param request:
    :param filter_status:
    :param filter_user:
    :return:
    """
    data = []
    kwargs = {
        'status__in': filter_status
    }
    if filter_user:
        staffer = Staffer.objects.get(user=request.user)
        kwargs['responsible'] = staffer
    events = Event.objects.filter(**kwargs).order_by('date')
    for event in events:
        vcss = VideoConf.objects.filter(event=event).order_by('time_start')
        reserved_rooms = ReservedRoom.objects.filter(event=event).order_by('time_start')
        data.append((event, vcss, reserved_rooms,))
    return {'data': data}
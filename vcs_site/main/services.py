from .models import Event, Staffer, Conference, Booking
from .forms import VideoConfAddForm


def get_context_for_event_view(request: str, filter_status: tuple, filter_user: bool) -> dict:
    """
    Возвращает контекст для представлений мероприятий
    :param request:
    :param filter_status:
    :param filter_user:
    :return:
    """
    data = []
    kwargs = {}
    if filter_status:
        kwargs['status__in'] = filter_status
    if filter_user:
        staffer = Staffer.objects.get(user=request.user)
        kwargs['responsible'] = staffer
    events = Event.objects.filter(**kwargs).order_by('date')
    for event in events:
        conferences = Conference.objects.filter(event=event).order_by('time_start')
        bookings = Booking.objects.filter(event=event).order_by('time_start')
        data.append((event, conferences, bookings,))
    return {'data': data}


def get_context_for_video_conf_view(request: str, filter_status: tuple, filter_user: bool) -> dict:
    """
    Возвращает контекст для представления видео мероприятий
    :param request:
    :param filter_status:
    :param filter_user:
    :return:
    """
    data = []
    kwargs = {}
    if filter_status:
        kwargs['status__in'] = filter_status
    if filter_user:
        staffer = Staffer.objects.get(user=request.user)
        kwargs['responsible'] = staffer
    conferences = Conference.objects.filter(**kwargs).order_by('id')
    for conference in conferences:
        form = VideoConfAddForm(data=request.POST or None, instance=conference)
        data.append((conference, form))
    return {'data': data}

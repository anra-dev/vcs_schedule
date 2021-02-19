from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib import messages


from .models import Event, Conference, Booking, Organization, Staffer
from .forms import EventAddForm, ConferenceAddForm, BookingAddForm
from .mixins import ObjectsListMixin, ObjectEditMixin, ObjectDeleteMixin, ObjectDependentCreateMixin


def homepage(request):
    """Редирект корня"""
    return redirect(reverse('events_list'))


class EventsListView(ObjectsListMixin, View):
    """
    ПРОСМОТР СПИСКА МЕРОПРИЯТИЙ
    """
    model = Event
    template = 'events_list.html'
    order_by = 'date'
    filter_status = ('wait', 'ready')


class MyEventsListView(ObjectsListMixin, View):
    """
    ПРОСМОТР СПИСКА МЕРОПРИЯТИЙ ПОЛЬЗОВАТЕЛЯ
    """
    model = Event
    template = 'my_events_list.html'
    order_by = 'date'
    filter_staffer = True


class ConferencesListView(ObjectsListMixin, View):
    """
    ПРОСМОТР СПИСКА КОНФЕРЕНЦИЙ
    """
    model = Conference
    template = 'conferences_list.html'
    filter_status = ('wait',)


class BookingsListView(ObjectsListMixin, View):
    """
    ПРОСМОТР СПИСКА БРОНИ
    """
    model = Booking
    template = 'bookings_list.html'
    filter_status = ('wait',)


class ArchiveEventsListView(ObjectsListMixin, View):
    """
    ПРОСМОТР СПИСКА ПРОШЕДШИХ МЕРОПРИЯТИЙ
    """
    model = Event
    template = 'events_archive_list.html'
    order_by = 'date'
    filter_status = ('completed',)


class EventDetailView(View):
    """
    ПРОСМОТР ДЕТАЛЬНОГО ПРЕДСТАВЛЕНИЯ МЕРОПРИЯТИЙ
    """
    def get(self, request, *args, **kwargs):
        id = kwargs.get('event_id')
        event = Event.objects.get(id=id)
        conferences = Conference.objects.filter(event=event).order_by('time_start')
        bookings = Booking.objects.filter(event=event).order_by('time_start')
        context = {
            'event': event,
            'conferences': conferences,
            'bookings': bookings
        }
        return render(request, 'event_detail.html', context)


class EventAddView(View):
    """
    СОЗДАНИЕ МЕРОПРИЯТИЙ
    """
    def get(self, request, *args, **kwargs):
        form = EventAddForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'event_add.html', context)

    def post(self, request, *args, **kwargs):
        form = EventAddForm(request.POST or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.responsible = Staffer.objects.get(user=request.user)
            event.organization = Organization.objects.get(responsible=event.responsible)
            event.save()
            messages.add_message(request, messages.INFO, event.MESSAGES['create'])
            return redirect(event)
        context = {
            'form': form
        }
        return render(request, 'event_add.html', context)


class EventEditView(ObjectEditMixin, View):
    """
    РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЙ
    """
    model = Event
    form = EventAddForm
    template = 'event_add.html'


class EventDeleteView(ObjectDeleteMixin, View):
    """
    УДАЛЕНИЕ  МЕРОПРИЯТИЙ
    """
    model = Event


class ConferenceAddView(ObjectDependentCreateMixin, View):
    """
    СОЗДАНИЕ  ВИДЕОКОНФЕРЕНЦИЙ
    """
    form = ConferenceAddForm
    template = 'conference_add.html'


class ConferenceEditView(ObjectEditMixin, View):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference
    form = ConferenceAddForm
    template = 'conference_add.html'


class ConferenceDeleteView(ObjectDeleteMixin, View):
    """
    УДАЛЕНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference


class BookingAddView(ObjectDependentCreateMixin, View):
    """
    СОЗДАНИЕ БРОНИ
    """
    form = BookingAddForm
    template = 'booking_add.html'



class BookingEditView(ObjectEditMixin, View):
    """
    РЕДАКТИРОВАНИЕ БРОНИ
    """
    model = Booking
    form = BookingAddForm
    template = 'booking_add.html'


class BookingDeleteView(ObjectDeleteMixin, View):
    """
    УДАЛЕНИЕ БРОНИ
    """
    model = Booking


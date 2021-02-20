from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView, ListView, ArchiveIndexView, UpdateView

from .models import Event, Conference, Booking, Organization, Staffer
from .forms import EventAddForm, ConferenceAddForm, BookingAddForm
from .mixins import CustomListView, ObjectEditMixin, ObjectDeleteMixin, ObjectDependentCreateMixin


class EventsListView(CustomListView):
    """
    ПРОСМОТР СПИСКА МЕРОПРИЯТИЙ
    """
    model = Event
    filter_status = ('wait', 'ready')


class MyEventsListView(CustomListView):
    """
    ПРОСМОТР СПИСКА МЕРОПРИЯТИЙ ПОЛЬЗОВАТЕЛЯ
    """
    model = Event
    template_name = 'schedule/my_event_list.html'
    filter_staffer = True
    filter_status = ('wait', 'ready', 'rejection')


class ConferencesListView(CustomListView):
    """
    ПРОСМОТР СПИСКА КОНФЕРЕНЦИЙ
    """
    model = Conference
    filter_status = ('wait',)


class BookingsListView(CustomListView):
    """
    ПРОСМОТР СПИСКА БРОНИ
    """
    model = Booking
    filter_status = ('wait',)


class ArchiveEventsListView(CustomListView):
    """
    ПРОСМОТР СПИСКА ПРОШЕДШИХ МЕРОПРИЯТИЙ
    """
    model = Event
    filter_status = ('completed',)
    template_name = 'schedule/event_archive.html'


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
        return render(request, 'schedule/event_detail.html', context)


class EventAddView(View):
    """
    СОЗДАНИЕ МЕРОПРИЯТИЙ
    """
    def get(self, request, *args, **kwargs):
        form = EventAddForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'schedule/event_add.html', context)

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
        return render(request, 'schedule/event_add.html', context)


class EventEditView(ObjectEditMixin, View):
    """
    РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЙ
    """
    model = Event
    form = EventAddForm
    template = 'schedule/event_add.html'


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
    template = 'schedule/conference_add.html'


class ConferenceUpdateView(UpdateView):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ ОПЕРАТОРОМ
    """
    model = Conference
    fields = ['link_to_event']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conference'] = self.object
        return context

    def form_valid(self, form):
        if 'ready' in form.data:
            if not form.cleaned_data['link_to_event']:
                form.add_error('link_to_event', 'Невозможно завершить без ссылки')
                return self.form_invalid(form)
            else:
                form.instance.status = 'ready'
        elif 'rejection' in form.data:
            form.instance.status = 'rejection'
        return super(ConferenceUpdateView, self).form_valid(form)


class ConferenceEditView(ObjectEditMixin, View):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference
    form = ConferenceAddForm
    template = 'schedule/conference_add.html'


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
    template = 'schedule/booking_add.html'


class BookingEditView(ObjectEditMixin, View):
    """
    РЕДАКТИРОВАНИЕ БРОНИ
    """
    model = Booking
    form = BookingAddForm
    template = 'schedule/booking_add.html'


class BookingDeleteView(ObjectDeleteMixin, View):
    """
    УДАЛЕНИЕ БРОНИ
    """
    model = Booking


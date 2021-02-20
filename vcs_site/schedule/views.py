from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import UpdateView

from .models import Event, Conference, Booking, Organization, Staffer
from .forms import EventAddForm, ConferenceAddForm, BookingAddForm
from .mixins import CustomListView, ObjectDependentCreateMixin, CustomUpdateView, CustomDeleteView


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
        return render(request, 'schedule/event_form.html', context)

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
        return render(request, 'schedule/event_form.html', context)


class EventEditView(CustomUpdateView):
    """
    РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЙ
    """
    model = Event
    form_class = EventAddForm


class EventDeleteView(CustomDeleteView):
    """
    УДАЛЕНИЕ  МЕРОПРИЯТИЙ
    """
    model = Event


class ConferenceAddView(ObjectDependentCreateMixin, View):
    """
    СОЗДАНИЕ  ВИДЕОКОНФЕРЕНЦИЙ
    """
    form = ConferenceAddForm
    template = 'schedule/conference_form.html'


class ConferenceUpdateView(CustomUpdateView):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference
    form_class = ConferenceAddForm


class ConferenceDeleteView(CustomDeleteView):
    """
    УДАЛЕНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference


class ConferenceApproveView(UpdateView):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ ОПЕРАТОРОМ
    """
    model = Conference
    fields = ['link_to_event']
    template_name_suffix = '_approve'

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
        return super().form_valid(form)


class BookingAddView(ObjectDependentCreateMixin, View):
    """
    СОЗДАНИЕ БРОНИ
    """
    form = BookingAddForm
    template = 'schedule/booking_form.html'


class BookingUpdateView(CustomUpdateView):
    """
    РЕДАКТИРОВАНИЕ БРОНИ
    """
    model = Booking
    form_class = BookingAddForm


class BookingDeleteView(CustomDeleteView):
    """
    УДАЛЕНИЕ БРОНИ
    """
    model = Booking


class BookingApproveView(CustomUpdateView):
    """
    РЕДАКТИРОВАНИЕ БРОНИ ОПЕРАТОРОМ
    """
    model = Booking
    form_class = BookingAddForm


from django.views import View
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import Event, Conference, Booking, Organization, Staffer
from .forms import EventAddForm, VideoConfAddForm, ReservedRoomAddForm, LoginForm
from .services import get_context_for_event_view, get_context_for_video_conf_view
from .mixins import ObjectsListViewMixin


class EventsListView(ObjectsListViewMixin, View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ ВСЕХ МЕРОПРИЯТИЙ
    """
    model = Event
    template = 'events_list.html'
    order_by = 'date'
    filter_status = ('wait', 'ready')


class MyEventsListView(ObjectsListViewMixin, View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ МЕРОПРИЯТИЙ ПОЛЬЗОВАТЕЛЯ
    """
    model = Event
    template = 'my_events_list.html'
    order_by = 'date'
    filter_staffer = True


class ConferencesListView(ObjectsListViewMixin, View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ КОНФЕРЕНЦИЙ
    """
    model = Conference
    template = 'conferences_list.html'
    filter_status = ('wait',)


class BookingsListView(ObjectsListViewMixin, View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ БРОНИРОВАНИЯ
    """
    model = Booking
    template = 'bookings_list.html'
    filter_status = ('wait',)


class ArchiveEventsListView(ObjectsListViewMixin, View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ ПРОШЕДШИХ МЕРОПРИЯТИЙ
    """
    model = Event
    template = 'events_archive_list.html'
    order_by = 'date'
    filter_status = ('completed',)


class EventDetailView(View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ ДЕТАЛЬНОГО ПРЕДСТАВЛЕНИЯ МЕРОПРИЯТИЙ
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
    ПРЕДСТАВЛЕНИЕ ДЛЯ ДОБАВЛЕНИЯ МЕРОПРИЯТИЙ
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
            messages.add_message(request, messages.INFO, 'Мероприятие успешно создано!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'event_add.html', context)


class EventEditView(View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ РЕДАКТИРОВАНИЯ МЕРОПРИЯТИЙ
    """
    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        form = EventAddForm(request.POST or None, instance=event)
        context = {
            'form': form
        }
        return render(request, 'event_add.html', context)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        form = EventAddForm(request.POST or None, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            messages.add_message(request, messages.INFO, 'Мероприятие успешно изменено!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'event_add.html', context)


class EventDeleteView(View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ УДАЛЕНИЯ  МЕРОПРИЯТИЙ
    """
    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        try:
            event.delete()
        except:
            pass
        messages.add_message(request, messages.INFO, 'Мероприятие удалено!')
        return HttpResponseRedirect('/') # ЗАМЕНИТЬ!!!




class ConferenceAddView(View):
    """
    Представление ДОБАВЛЕНИЯ ЗАЯВКИ НА ВИДЕОКОНФЕРЕНЦИЮ
    """

    def get(self, request, *args, **kwargs):
        form = VideoConfAddForm(data=request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'conference_add.html', context)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        form = VideoConfAddForm(data=request.POST or None)
        if form.is_valid():
            conference = form.save(commit=False)
            conference.event = event
            conference.save()
            messages.add_message(request, messages.INFO, 'Направлена заявка на видеоконференцию!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'conference_add.html', context)


class ConferenceEditView(View):

    def get(self, request, *args, **kwargs):
        conference = Conference.objects.get(id=kwargs.get('conference_id'))
        form = VideoConfAddForm(data=request.POST or None, instance=conference)
        context = {
            'form': form
        }
        return render(request, 'conference_add.html', context)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        conference = Conference.objects.get(id=kwargs.get('conference_id'))
        form = VideoConfAddForm(data=request.POST or None, instance=conference)
        if form.is_valid():
            conference.save()
            messages.add_message(request, messages.INFO, 'Заявка успешно сохранена!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'conference_add.html', context)


class ConferenceDeleteView(View):

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        conference = Conference.objects.get(id=kwargs.get('conference_id'))
        try:
            conference.delete()
        except:
            pass
        messages.add_message(request, messages.INFO, 'Видеоконференция удалено!')
        return HttpResponseRedirect(event.get_absolute_url())


""" Представление БРОНИРОВАНИЯ КОМНАТ """


class BookingAddView(View):

    def get(self, request, *args, **kwargs):
        form = ReservedRoomAddForm(data=request.POST or None,)
        context = {
            'form': form
        }
        return render(request, 'booking_add.html', context)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        form = ReservedRoomAddForm(data=request.POST or None,)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event = event
            booking.save()
            messages.add_message(request, messages.INFO, 'Направлена заявка на бронирование комнаты!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'booking_add.html', context)


class BookingEditView(View):

    def get(self, request, *args, **kwargs):
        booking = Booking.objects.get(id=kwargs.get('booking_id'))
        form = ReservedRoomAddForm(data=request.POST or None, instance=booking)
        context = {
            'form': form
        }
        return render(request, 'booking_add.html', context)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        booking = Booking.objects.get(id=kwargs.get('booking_id'))
        form = ReservedRoomAddForm(data=request.POST or None, instance=booking)
        if form.is_valid():
            booking.save()
            messages.add_message(request, messages.INFO, 'Направлена заявка на бронирование комнаты!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'booking_add.html', context)


class BookingDeleteView(View):

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        booking = Booking.objects.get(id=kwargs.get('booking_id'))
        try:
            booking.delete()
        except:
            pass
        messages.add_message(request, messages.INFO, 'Бронирование комнаты удалено!')
        return HttpResponseRedirect(event.get_absolute_url())


""" Представление АВТОРИЗАЦИИ """


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)
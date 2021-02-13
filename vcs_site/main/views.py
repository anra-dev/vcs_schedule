from django.views import View
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import Event, VideoConf, ReservedRoom, Organization, Staffer
from .forms import EventAddForm, VideoConfAddForm, ReservedRoomAddForm, LoginForm


class EventsView(View):

    def get(self, request):
        data = []
        events = Event.objects.filter(status__in=('created', 'is_ready')).order_by('date')
        for event in events:
            vcs = VideoConf.objects.filter(event=event).first()
            reserved_room = ReservedRoom.objects.filter(event=event).first()
            data.append((event, vcs, reserved_room,))
        context = {
            'data': data
        }
        return render(request, 'events.html', context)


class OrdersView(View):

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(status='created').order_by('date')
        context = {
            'events': events
        }
        return render(request, 'orders.html', context)

class ArchiveView(View):

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(status='completed').order_by('date')
        context = {
            'events': events
        }
        return render(request, 'archive.html', context)


class EventDetailView(View):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('event_id')
        event = Event.objects.get(id=id)
        vcss = VideoConf.objects.filter(event=event).order_by('time_start')
        reserved_rooms = ReservedRoom.objects.filter(event=event).order_by('time_start')
        context = {
            'event': event,
            'vcss': vcss,
            'reserved_rooms': reserved_rooms
        }
        return render(request, 'event_detail.html', context)


""" Представление МЕРОПРИЯТИИ """


class EventAddView(View):

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

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        try:
            event.delete()
        except:
            pass
        messages.add_message(request, messages.INFO, 'Мероприятие удалено!')
        return HttpResponseRedirect('/')


""" Представление ВИДЕОКОНФЕРЕНЦИЙ """


class VideoConfAddView(View):

    def get(self, request, *args, **kwargs):
        form = VideoConfAddForm(data=request.POST or None, for_event=None)
        context = {
            'form': form
        }
        return render(request, 'video_conf_add.html', context)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        form = VideoConfAddForm(data=request.POST or None, for_event=event)
        if form.is_valid():
            vcs = form.save(commit=False)
            vcs.event = event
            vcs.save()
            messages.add_message(request, messages.INFO, 'Направлена заявка на видеоконференцию!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'video_conf_add.html', context)


class VideoConfEditView(View):

    def get(self, request, *args, **kwargs):
        vcs = VideoConf.objects.get(id=kwargs.get('vcs_id'))
        form = VideoConfAddForm(data=request.POST or None, for_event=None, instance=vcs)
        context = {
            'form': form
        }
        return render(request, 'video_conf_add.html', context)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        vcs = VideoConf.objects.get(id=kwargs.get('vcs_id'))
        form = VideoConfAddForm(data=request.POST or None, for_event=event, instance=vcs)
        if form.is_valid():
            vcs.save()
            messages.add_message(request, messages.INFO, 'Заявка успешно сохранена!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'video_conf_add.html', context)


class VideoConfDeleteView(View):

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        vcs = VideoConf.objects.get(id=kwargs.get('vcs_id'))
        try:
            vcs.delete()
        except:
            pass
        messages.add_message(request, messages.INFO, 'Видеоконференция удалено!')
        return HttpResponseRedirect(event.get_absolute_url())


""" Представление БРОНИРОВАНИЯ КОМНАТ """


class ReservedRoomAddView(View):

    def get(self, request, *args, **kwargs):
        form = ReservedRoomAddForm(data=request.POST or None, for_event=None)
        context = {
            'form': form
        }
        return render(request, 'room_add.html', context)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        form = ReservedRoomAddForm(data=request.POST or None, for_event=event)
        if form.is_valid():
            room = form.save(commit=False)
            room.event = event
            room.save()
            messages.add_message(request, messages.INFO, 'Направлена заявка на бронирование комнаты!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'room_add.html', context)


class ReservedRoomEditView(View):

    def get(self, request, *args, **kwargs):
        room = ReservedRoom.objects.get(id=kwargs.get('room_id'))
        form = ReservedRoomAddForm(data=request.POST or None, for_event=None, instance=room)
        context = {
            'form': form
        }
        return render(request, 'room_add.html', context)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        room = ReservedRoom.objects.get(id=kwargs.get('room_id'))
        form = ReservedRoomAddForm(data=request.POST or None, for_event=event, instance=room)
        if form.is_valid():
            room.save()
            messages.add_message(request, messages.INFO, 'Направлена заявка на бронирование комнаты!')
            return HttpResponseRedirect(event.get_absolute_url())
        context = {
            'form': form
        }
        return render(request, 'room_add.html', context)


class ReservedRoomDeleteView(View):

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        room = ReservedRoom.objects.get(id=kwargs.get('room_id'))
        try:
            room.delete()
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
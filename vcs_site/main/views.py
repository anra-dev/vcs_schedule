from django.views import View
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import Event, VideoConf, ReservedRoom, Organization, Staffer
from .forms import EventAddForm, VideoConfAddForm, ReservedRoomAddForm, LoginForm


class EventsView(View):

    def get(self, request):
        events = Event.objects.filter(status__in=('created', 'is_ready'))
        context = {
            'events': events
        }
        return render(request, 'events.html', context)


class OrdersView(View):

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(status='created')
        context = {
            'events': events
        }
        return render(request, 'orders.html', context)

class ArchiveView(View):

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(status='completed')
        context = {
            'events': events
        }
        return render(request, 'archive.html', context)


class EventDetailView(View):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        event = Event.objects.get(id=id)
        vcs = VideoConf.objects.filter(event=event).first()
        reserved_room = ReservedRoom.objects.filter(event=event).first()
        context = {
            'event': event,
            'vcs': vcs,
            'reserved_room': reserved_room
        }
        return render(request, 'event_detail.html', context)


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
            return HttpResponseRedirect(reverse('event_type'))
        context = {
            'form': form
        }
        return render(request, 'event_add.html', context)


class EventTypeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'event_type.html', {})


class VideoConfAddView(View):

    def get(self, request, *args, **kwargs):
        form = VideoConfAddForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'video_conf_add.html', context)

    def post(self, request, *args, **kwargs):
        form = VideoConfAddForm(request.POST or None)
        if form.is_valid():
            vcs = form.save(commit=False)
            vcs.event = Event.objects.last()
            vcs.save()
            messages.add_message(request, messages.INFO, 'Направлена заявка на видеоконференцию!')
            return HttpResponseRedirect(reverse('room_add'))
        context = {
            'form': form
        }
        return render(request, 'video_conf_add.html', context)


class ReservedRoomAddView(View):

    def get(self, request, *args, **kwargs):
        form = ReservedRoomAddForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'room_add.html', context)

    def post(self, request, *args, **kwargs):
        form = ReservedRoomAddForm(request.POST or None)
        if form.is_valid():
            room = form.save(commit=False)
            room.event = Event.objects.last()
            room.save()
            messages.add_message(request, messages.INFO, 'Направлена заявка на бронирование комнаты!')
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'room_add.html', context)


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
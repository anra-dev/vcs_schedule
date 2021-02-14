from django.views import View
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import Event, VideoConf, ReservedRoom, Organization, Staffer
from .forms import EventAddForm, VideoConfAddForm, ReservedRoomAddForm, LoginForm
from .services import get_context_for_event_view


class EventsView(View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ ВСЕХ МЕРОПРИЯТИЙ
    """
    def get(self, request, *args, **kwargs):
        context = get_context_for_event_view(request=request, filter_status=('wait', 'ready'),
                                             filter_user=False)
        return render(request, 'events.html', context)


class OrdersView(View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ МОИХ ЗАЯВОК
    """
    def get(self, request, *args, **kwargs):
        context = get_context_for_event_view(request=request, filter_status=('wait', 'ready', 'rejection'),
                                             filter_user=True)
        return render(request, 'orders.html', context)


class OrdersVideoConfView(View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ ЗАЯВОК НА ВИДЕОКОНФЕРЕНЦИИ
    """
    def get(self, request, *args, **kwargs):
        vcss = VideoConf.objects.filter(status='wait').order_by('id')
        context = {
            'vcss': vcss
        }
        return render(request, 'orders_vcs.html', context)


class OrdersRoomView(View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ ЗАЯВОК НА КОМНАТУ
    """
    def get(self, request, *args, **kwargs):
        reserved_rooms = ReservedRoom.objects.filter(status='wait').order_by('id')
        context = {
            'reserved_rooms': reserved_rooms
        }
        return render(request, 'orders_room.html', context)


class ArchiveView(View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ ПРОШЕДШИХ МЕРОПРИЯТИЙ
    """
    def get(self, request, *args, **kwargs):
        context = get_context_for_event_view(request=request, filter_status=('completed',),
                                             filter_user=False)
        return render(request, 'archive.html', context)


class EventDetailView(View):
    """
    ПРЕДСТАВЛЕНИЕ ДЛЯ ОТОБРАЖЕНИЯ ДЕТАЛЬНОГО ПРЕДСТАВЛЕНИЯ МЕРОПРИЯТИЙ
    """
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
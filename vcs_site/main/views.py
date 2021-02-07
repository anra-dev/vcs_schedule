from django.views import View
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages

from .models import Event
from .forms import EventAddForm


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
        context = {
            'event': event
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
            event.time_start = form.cleaned_data['time_start']
            event.time_end = form.cleaned_data['time_end']
            event.save()
            messages.add_message(request, messages.INFO, 'Мероприятие успешно создано!')
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'event_add.html', context)
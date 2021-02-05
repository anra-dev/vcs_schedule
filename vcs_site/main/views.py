from django.views import View
from django.shortcuts import render

from .models import Event


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
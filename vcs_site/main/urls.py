from django.urls import path

from .views import EventsView, OrdersView, ArchiveView, EventDetailView

urlpatterns = [
    path('', EventsView.as_view(), name='events'),
    path('order/', OrdersView.as_view(), name='orders'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('event/<id>', EventDetailView.as_view(), name='event_detail')
]
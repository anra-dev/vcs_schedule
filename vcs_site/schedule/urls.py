from django.urls import path
from .views import *

urlpatterns = [
    path('event-list/', EventsListView.as_view(), name='event_list'),
    path('my-event-list/', MyEventsListView.as_view(), name='my_event_list'),
    path('conference_list/', ConferencesListView.as_view(), name='conference_list'),
    path('booking-list/', BookingsListView.as_view(), name='booking_list'),
    path('event-archive/', ArchiveEventsListView.as_view(), name='event_archive'),

    path('add-event/', EventAddView.as_view(), name='add_event'),
    path('event/<event_id>', EventDetailView.as_view(), name='event_detail'),
    path('event/<event_id>/edit-event/', EventEditView.as_view(), name='edit_event'),
    path('event/<event_id>/del-event', EventDeleteView.as_view(), name='del_event'),

    path('event/<event_id>/add-conference/', ConferenceAddView.as_view(), name='add_conference'),
    path('conf/<int:pk>/', ConferenceUpdateView.as_view(), name='conf-update'),
    path('event/<event_id>/edit-conference/<conference_id>/', ConferenceEditView.as_view(), name='edit_conference'),
    path('event/<event_id>/del-conference/<conference_id>', ConferenceDeleteView.as_view(), name='del_conference'),

    path('event/<event_id>/add-booking/', BookingAddView.as_view(), name='add_booking'),
    path('edit-booking/<booking_id>/', BookingEditView.as_view(), name='edit_booking'),
    path('del-booking/<booking_id>/', BookingDeleteView.as_view(), name='del_booking'),
]

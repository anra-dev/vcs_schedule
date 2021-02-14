from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LoginView,
    EventsListView,
    MyEventsListView,
    ConferencesListView,
    BookingsListView,
    ArchiveEventsListView,

    EventDetailView,
    EventAddView,
    EventEditView,
    EventDeleteView,

    ConferenceAddView,
    ConferenceEditView,
    ConferenceDeleteView,

    BookingAddView,
    BookingEditView,
    BookingDeleteView
)

urlpatterns = [
    path('events-list/', EventsListView.as_view(), name='events_list'),
    path('my-events-list/', MyEventsListView.as_view(), name='my_events_list'),
    path('conferences_list/', ConferencesListView.as_view(), name='conferences_list'),
    path('bookings-list/', BookingsListView.as_view(), name='bookings_list'),
    path('events-archive-list/', ArchiveEventsListView.as_view(), name='events_archive_list'),

    path('add-event/', EventAddView.as_view(), name='add_event'),
    path('event/<event_id>', EventDetailView.as_view(), name='event_detail'),
    path('event/<event_id>/edit-event/', EventEditView.as_view(), name='edit_event'),
    path('event/<event_id>/del-event', EventDeleteView.as_view(), name='del_event'),

    path('event/<event_id>/add-conference/', ConferenceAddView.as_view(), name='add_conference'),
    path('event/<event_id>/edit-conference/<conference_id>/', ConferenceEditView.as_view(), name='edit_conference'),
    path('event/<event_id>/del-conference/<conference_id>', ConferenceDeleteView.as_view(), name='del_conference'),

    path('event/<event_id>/add-booking/', BookingAddView.as_view(), name='add_booking'),
    path('event/<event_id>/edit-booking/<booking_id>/', BookingEditView.as_view(), name='edit_booking'),
    path('event/<event_id>/del-booking/<booking_id>', BookingDeleteView.as_view(), name='del_booking'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
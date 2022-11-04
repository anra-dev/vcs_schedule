from django.urls import path

from schedule.views_old.booking import BookingsListView, BookingCreateView, \
    BookingApproveView, BookingUpdateView, BookingDeleteView
from schedule.views_old.conference import ConferencesListView, \
    ConferenceCreateView, ConferenceApproveView, ConferenceUpdateView, \
    ConferenceDeleteView
from schedule.views import EventsListView, MyEventsListView, \
    ArchiveEventsListView, EventCreateView, EventDetailView, EventUpdateView, \
    EventDeleteView, get_server_for_room, GradeCreate, \
    get_upcoming_conferences, get_upcoming_bookings

urlpatterns = [
    path('event-list/', EventsListView.as_view(), name='event_list'),
    path('my-event-list/', MyEventsListView.as_view(), name='my_event_list'),
    path('conference-list/', ConferencesListView.as_view(), name='conference_list'),
    path('booking-list/', BookingsListView.as_view(), name='booking_list'),
    path('event-archive/', ArchiveEventsListView.as_view(), name='event_archive'),

    path('event-create/', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>', EventDetailView.as_view(), name='event_detail'),
    path('event-update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('event-delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),

    path('event/<int:pk>/conference-create/', ConferenceCreateView.as_view(), name='conference_create'),
    path('conference-approve/<int:pk>/', ConferenceApproveView.as_view(), name='conference_approve'),
    path('conference-update/<int:pk>/', ConferenceUpdateView.as_view(), name='conference_update'),
    path('conference-delete/<int:pk>', ConferenceDeleteView.as_view(), name='conference_delete'),

    path('event/<int:pk>/booking-create/', BookingCreateView.as_view(), name='booking_create'),
    path('booking-approve/<int:pk>/', BookingApproveView.as_view(), name='booking_approve'),
    path('booking-update/<int:pk>/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking-delete/<int:pk>/', BookingDeleteView.as_view(), name='booking_delete'),

    path('get-server-for-room/', get_server_for_room, name='get_server_for_room'),
    path('get-upcoming-conferences/', get_upcoming_conferences, name='get_upcoming_conferences'),
    path('get-upcoming-bookings/', get_upcoming_bookings, name='get_upcoming_bookings'),

    path('event/<int:pk>/grade/', GradeCreate.as_view(), name='grade')
]

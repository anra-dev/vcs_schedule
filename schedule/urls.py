from django.urls import path

from schedule.views_old.booking import BookingsListView, BookingCreateView, \
    BookingApproveView, BookingUpdateView, BookingDeleteView
from schedule.views_old.conference import ConferencesListView, \
    ConferenceCreateView, ConferenceApproveView, ConferenceUpdateView, \
    ConferenceDeleteView
from schedule.views import EventsListView, MyEventsListView, \
    ArchiveEventsListView, EventCreateView, EventDetailView, EventUpdateView, \
    EventDeleteView, get_server_for_room, GradeCreate, \
    get_upcoming_conferences, get_upcoming_bookings, EventForOperatorListView, \
    EventForAssistantListView, EventOperatorApproveView, \
    EventAssistantApproveView

urlpatterns = [
    path(
        route='event-list/',
        view=EventsListView.as_view(),
        name='event_list',
    ),
    path(
        route='my-event-list/',
        view=MyEventsListView.as_view(),
        name='my_event_list',
    ),
    path(
        route='conference-list/',
        view=EventForOperatorListView.as_view(),
        name='conference_list',
    ),
    path(
        route='booking-list/',
        view=EventForAssistantListView.as_view(),
        name='booking_list',
    ),
    path(
        route='event-archive/',
        view=ArchiveEventsListView.as_view(),
        name='event_archive',
    ),

    path(
        route='event-create/',
        view=EventCreateView.as_view(),
        name='event_create',
    ),
    path(
        route='event/<int:pk>',
        view=EventDetailView.as_view(),
        name='event_detail',
    ),
    path(
        route='event-update/<int:pk>/',
        view=EventUpdateView.as_view(),
        name='event_update',
    ),
    path(
        route='event-delete/<int:pk>/',
        view=EventDeleteView.as_view(),
        name='event_delete',
    ),
    path(
        route='booking-approve/<int:pk>/',
        view=EventAssistantApproveView.as_view(),
        name='booking_approve',
    ),
    path(
        route='conference-approve/<int:pk>/',
        view=EventOperatorApproveView.as_view(),
        name='conference_approve',
    ),

    path('event/<int:pk>/conference-create/', ConferenceCreateView.as_view(), name='conference_create'),
    path('conference-update/<int:pk>/', ConferenceUpdateView.as_view(), name='conference_update'),
    path('conference-delete/<int:pk>', ConferenceDeleteView.as_view(), name='conference_delete'),

    path('event/<int:pk>/booking-create/', BookingCreateView.as_view(), name='booking_create'),
    path('booking-update/<int:pk>/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking-delete/<int:pk>/', BookingDeleteView.as_view(), name='booking_delete'),

    path(
        route='get-server-for-room/',
        view=get_server_for_room,
        name='get_server_for_room',
    ),
    path(
        route='get-upcoming-conferences/',
        view=get_upcoming_conferences,
        name='get_upcoming_conferences',
    ),
    path(
        route='get-upcoming-bookings/',
        view=get_upcoming_bookings,
        name='get_upcoming_bookings',
    ),

    path('event/<int:pk>/grade/', GradeCreate.as_view(), name='grade')
]

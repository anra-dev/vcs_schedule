from django.urls import path

from schedule import views

urlpatterns = [
    path(
        route='event-list/',
        view=views.EventsListView.as_view(),
        name='event_list',
    ),
    path(
        route='my-event-list/',
        view=views.MyEventsListView.as_view(),
        name='my_event_list',
    ),
    path(
        route='conference-list/',
        view=views.EventForOperatorListView.as_view(),
        name='conference_list',
    ),
    path(
        route='booking-list/',
        view=views.EventForAssistantListView.as_view(),
        name='booking_list',
    ),
    path(
        route='event-archive/',
        view=views.ArchiveEventsListView.as_view(),
        name='event_archive',
    ),

    path(
        route='event-create/',
        view=views.EventCreateView.as_view(),
        name='event_create',
    ),
    path(
        route='event/<int:pk>',
        view=views.EventDetailView.as_view(),
        name='event_detail',
    ),
    path(
        route='event-update/<int:pk>/',
        view=views.EventUpdateView.as_view(),
        name='event_update',
    ),
    path(
        route='event-delete/<int:pk>/',
        view=views.EventDeleteView.as_view(),
        name='event_delete',
    ),
    path(
        route='booking-approve/<int:pk>/',
        view=views.EventAssistantApproveView.as_view(),
        name='booking_approve',
    ),
    path(
        route='conference-approve/<int:pk>/',
        view=views.EventOperatorApproveView.as_view(),
        name='conference_approve',
    ),
    path(
        route='get-server-for-room/',
        view=views.get_server_for_room,
        name='get_server_for_room',
    ),
    path(
        route='get-upcoming-conferences/',
        view=views.get_upcoming_conferences,
        name='get_upcoming_conferences',
    ),
    path(
        route='get-upcoming-bookings/',
        view=views.get_upcoming_bookings,
        name='get_upcoming_bookings',
    ),

    path('event/<int:pk>/grade/', views.GradeCreate.as_view(), name='grade')
]

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
    path('event-update/<int:pk>/', EventEditView.as_view(), name='event_update'),
    path('event-delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),

    path('event/<event_id>/add-conference/', ConferenceAddView.as_view(), name='add_conference'),
    path('conference-approve/<int:pk>/', ConferenceApproveView.as_view(), name='conference_approve'),
    path('conference-update/<int:pk>/', ConferenceUpdateView.as_view(), name='conference_update'),
    path('conference-delete/<int:pk>', ConferenceDeleteView.as_view(), name='conference_delete'),

    path('event/<event_id>/add-booking/', BookingAddView.as_view(), name='add_booking'),
    path('booking-approve/<int:pk>/', BookingApproveView.as_view(), name='booking_approve'),
    path('booking-update/<int:pk>/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking-delete/<int:pk>/', BookingDeleteView.as_view(), name='booking_delete'),
]

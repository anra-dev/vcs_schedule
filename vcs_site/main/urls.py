from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LoginView,
    EventsView,
    OrdersView,
    ArchiveView,
    EventDetailView,
    EventAddView,
    EventEditView,
    EventDeleteView,

    VideoIntConfAddView,
    VideoIntConfEditView,
    VideoIntConfDeleteView,

    VideoExtConfAddView,

    ReservedRoomAddView,
    ReservedRoomEditView,
    ReservedRoomDeleteView
)

urlpatterns = [
    path('', EventsView.as_view(), name='events'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('order/', OrdersView.as_view(), name='orders'),
    path('archive/', ArchiveView.as_view(), name='archive'),

    path('add-event/', EventAddView.as_view(), name='add_event'),
    path('event/<event_id>', EventDetailView.as_view(), name='event_detail'),
    path('event/<event_id>/event-edit/', EventEditView.as_view(), name='edit_event'),
    path('event/<event_id>/del-event', EventDeleteView.as_view(), name='del_event'),

    path('event/<event_id>/add-int-vcs/', VideoIntConfAddView.as_view(), name='add_int_vcs'),
    path('event/<event_id>/edit-int-vcs-<vcs_id>/', VideoIntConfEditView.as_view(), name='edit_int_vcs'),
    path('event/<event_id>/del-int-vcs-<vcs_id>/', VideoIntConfDeleteView.as_view(), name='del_int_vcs'),

    path('event/<event_id>/vcs-ext-add/', VideoExtConfAddView.as_view(), name='add_ext_vcs'),
    path('event/<event_id>/edit-ext-vcs/', VideoIntConfAddView.as_view(), name='edit_ext_vcs'),
    path('event/<event_id>/del-ext-vcs/', VideoIntConfAddView.as_view(), name='del_ext_vcs'),

    path('event/<event_id>/add-room/', ReservedRoomAddView.as_view(), name='add_room'),
    path('event/<event_id>/edit-room-<room_id>/', ReservedRoomEditView.as_view(), name='edit_room'),
    path('event/<event_id>/del-room-<room_id>/', ReservedRoomDeleteView.as_view(), name='del_room'),
]
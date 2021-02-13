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

    VideoConfAddView,
    VideoConfEditView,
    VideoConfDeleteView,

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

    path('event/<event_id>/add-int-vcs/', VideoConfAddView.as_view(), name='add_vcs'),
    path('event/<event_id>/edit-vcs/<vcs_id>/', VideoConfEditView.as_view(), name='edit_vcs'),
    path('event/<event_id>/del-vcs/<vcs_id>', VideoConfDeleteView.as_view(), name='del_vcs'),

    path('event/<event_id>/add-room/', ReservedRoomAddView.as_view(), name='add_room'),
    path('event/<event_id>/edit-room/<room_id>/', ReservedRoomEditView.as_view(), name='edit_room'),
    path('event/<event_id>/del-room/<room_id>', ReservedRoomDeleteView.as_view(), name='del_room'),
]
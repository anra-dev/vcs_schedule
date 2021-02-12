from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LoginView,
    EventsView,
    OrdersView,
    ArchiveView,
    EventDetailView,
    EventAddView,
    VideoIntConfAddView,
    VideoExtConfAddView,
    ReservedRoomAddView
)

urlpatterns = [
    path('', EventsView.as_view(), name='events'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('order/', OrdersView.as_view(), name='orders'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('event/<id>', EventDetailView.as_view(), name='event_detail'),
    path('event-add/', EventAddView.as_view(), name='event_add'),
    path('vcs-int-add/', VideoIntConfAddView.as_view(), name='vcs_int_add'),
    path('vcs-ext-add/', VideoExtConfAddView.as_view(), name='vcs_xt_add'),
    path('room-add/', ReservedRoomAddView.as_view(), name='room_add')
]
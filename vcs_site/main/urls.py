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
    path('add-event/', EventAddView.as_view(), name='add_event'),
    path('event/<id>/add-int-vcs/', VideoIntConfAddView.as_view(), name='add_int_vcs'),
    path('event/<id>-vcs-ext-add/', VideoExtConfAddView.as_view(), name='add_ext_vcs'),
    path('event/<id>-add-room/', ReservedRoomAddView.as_view(), name='add_room')
]
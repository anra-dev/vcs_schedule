from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from .views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
]
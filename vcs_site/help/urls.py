from django.urls import path

from .views import HelpIndexView, HelpPageView

urlpatterns = [
    path('', HelpIndexView.as_view(), name='help_index_page'),
    path('<slug:slug>/', HelpPageView.as_view(), name='help_page')
]
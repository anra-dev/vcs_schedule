from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *


urlpatterns = [
    path('', csrf_exempt(TelegramBotView.as_view()))
]

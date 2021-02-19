from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import LoginForm


class LoginView(View):
    """
    Представление аутентификации
    """
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        context = {
            'form': form,
        }
        return render(request, 'accounts/login.html', context)
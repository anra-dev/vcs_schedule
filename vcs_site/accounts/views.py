from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy


from .forms import LoginForm
from schedule.models import User


class SettingsView(UpdateView):
    model = User
    fields = ['subscribe_mail', 'email', 'subscribe_telegram', 'telegram']
    template_name = 'accounts/staffer_form.html'

    def get_success_url(self):
        referer_url = self.request.META.get('next')  # Прикольная тема но у меня на firefox не раюботает
        if referer_url:
            return referer_url
        return reverse_lazy('event_list')

    # def get_object(self, queryset=None):
    #     return Staffer.objects.get(user=self.request.user)

    def form_valid(self, form):  # Переписать так что бы показывало обе ошибки одновременно если они есть
        if form.cleaned_data['subscribe_mail'] and not form.cleaned_data['email']:
            form.add_error('email', 'Заполните поле или отмените подписку')
        if form.cleaned_data['subscribe_telegram'] and not form.cleaned_data['telegram']:
            form.add_error('telegram', 'Заполните поле или отмените подписку')
        if form.errors:
            return super().form_invalid(form)
        return super().form_valid(form)


class LoginView(View):
    """
    Представление аутентификации
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Пользователь авторизован.
            return redirect(reverse('event_list'))
        else:
            # Анонимный пользователь.
            form = LoginForm(request.POST or None)
            context = {
                'form': form,
            }
            return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('event_list'))
        context = {
            'form': form,
        }
        return render(request, 'accounts/login.html', context)

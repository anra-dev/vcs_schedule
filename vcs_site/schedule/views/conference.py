from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ..models import Event, Conference, Booking, get_object_or_none
from ..forms import ConferenceCreateForm, ConferenceUpdateForm
from ..services import set_status_completed
from .mixins import HelpMixin, UserIsOperatorMixin


class ConferencesListView(UserIsOperatorMixin, ListView):
    """
    ПРОСМОТР СПИСКА КОНФЕРЕНЦИЙ
    """
    model = Conference
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        set_status_completed(queryset)
        return queryset.filter(status__in=('wait',), )


class ConferenceCreateView(LoginRequiredMixin, HelpMixin, CreateView):
    """
    СОЗДАНИЕ  ВИДЕОКОНФЕРЕНЦИЙ
    """
    model = Conference
    form_class = ConferenceCreateForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, self.object.MESSAGES['create'])
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.event = get_object_or_none(Event, pk=self.kwargs.get('pk'))
        return super().form_valid(form)


class ConferenceUpdateView(LoginRequiredMixin, HelpMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference
    form_class = ConferenceUpdateForm

    def get(self, request, *args, **kwargs):
        conference = get_object_or_none(Conference, pk=kwargs.get('pk'))
        booking = Booking.objects.filter(conference=conference)
        if booking:
            messages.add_message(
                self.request, messages.ERROR,
                f'Нельзя изменить конференцию с существующим бронированием. Сначала удалите бронирование помещения!'
            )
            return HttpResponseRedirect(conference.get_redirect_url_for_event_list())
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, self.object.MESSAGES['update'])
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        self.object.status = 'wait'
        return super().form_valid(form)


class ConferenceDeleteView(LoginRequiredMixin, DeleteView):
    """
    УДАЛЕНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference
    template_name = 'schedule/object_confirm_delete.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.ERROR, self.object.MESSAGES['delete'])
        return self.object.get_redirect_url_for_event_list()


class ConferenceApproveView(LoginRequiredMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ ОПЕРАТОРОМ
    """
    model = Conference
    fields = ['link', 'comment']
    template_name_suffix = '_approve'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, self.object.MESSAGES['approve'])
        return self.object.get_list_url()

    def form_valid(self, form):
        if 'ready' in form.data:
            if not form.cleaned_data['link']:
                form.add_error('link', 'Невозможно завершить без ссылки')
                return self.form_invalid(form)
            else:
                form.instance.status = 'ready'
                form.instance.comment = None
                form.instance.operator = self.request.user
        elif 'rejection' in form.data:
            form.instance.status = 'rejection'
        return super().form_valid(form)

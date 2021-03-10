from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ..models import Conference
from ..forms import ConferenceCreateForm, ConferenceUpdateForm
from ..services import set_status_completed
from .mixins import HelpMixin


class ConferencesListView(LoginRequiredMixin, ListView):
    """
    ПРОСМОТР СПИСКА КОНФЕРЕНЦИЙ
    """
    model = Conference
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        set_status_completed(queryset)
        return queryset.filter(status__in=('wait',))


class ConferenceCreateView(LoginRequiredMixin, HelpMixin, CreateView):
    """
    СОЗДАНИЕ  ВИДЕОКОНФЕРЕНЦИЙ
    """
    model = Conference
    form_class = ConferenceCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'event_id': self.kwargs.get('pk')})
        return kwargs

    def get_success_url(self):
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['create'])
        return super().form_valid(form)


class ConferenceUpdateView(LoginRequiredMixin, HelpMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference
    form_class = ConferenceUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'event_id': self.object.event.pk})
        return kwargs

    def get_success_url(self):
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        self.object.status = 'wait'
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['update'])
        return super().form_valid(form)


class ConferenceDeleteView(LoginRequiredMixin, DeleteView):
    """
    УДАЛЕНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference
    template_name = 'schedule/object_confirm_delete.html'

    def get_success_url(self):
        return self.object.get_redirect_url_for_event_list()

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, self.get_object().MESSAGES['delete'])
        return super().delete(request, *args, **kwargs)


class ConferenceApproveView(LoginRequiredMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ ОПЕРАТОРОМ
    """
    model = Conference
    fields = ['link', 'comment']
    template_name_suffix = '_approve'

    def form_valid(self, form):
        if 'ready' in form.data:
            if not form.cleaned_data['link']:
                form.add_error('link', 'Невозможно завершить без ссылки')
                return self.form_invalid(form)
            else:
                form.instance.status = 'ready'
                form.instance.comment = None
        elif 'rejection' in form.data:
            form.instance.status = 'rejection'
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['update'])
        return super().form_valid(form)

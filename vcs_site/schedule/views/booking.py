from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ..models import Booking
from ..forms import BookingCreateForm, BookingUpdateForm
from ..services import set_status_completed
from .mixins import HelpMixin


class BookingsListView(LoginRequiredMixin, ListView):
    """
    ПРОСМОТР СПИСКА БРОНИ
    """
    model = Booking
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        set_status_completed(queryset)
        return queryset.filter(status__in=('wait',))


class BookingCreateView(LoginRequiredMixin, HelpMixin, CreateView):
    """
    СОЗДАНИЕ БРОНИ
    """
    model = Booking
    form_class = BookingCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'event_id': self.kwargs.get('pk')})
        return kwargs

    def get_success_url(self):
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['create'])
        return super().form_valid(form)


class BookingUpdateView(LoginRequiredMixin, HelpMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ БРОНИ
    """
    model = Booking
    form_class = BookingUpdateForm

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


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    """
    УДАЛЕНИЕ БРОНИ
    """
    model = Booking

    def get_success_url(self):
        return self.object.get_redirect_url_for_event_list()

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, self.get_object().MESSAGES['delete'])
        return super().delete(request, *args, **kwargs)


class BookingApproveView(LoginRequiredMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ БРОНИ ОПЕРАТОРОМ
    """
    model = Booking
    fields = ['comment']
    template_name_suffix = '_approve'

    def form_valid(self, form):
        if 'ready' in form.data:
            form.instance.status = 'ready'
            form.instance.comment = None
        elif 'rejection' in form.data:
            form.instance.status = 'rejection'
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['update'])
        return super().form_valid(form)

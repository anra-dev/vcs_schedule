from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ..models import Event, Conference, Booking, Room, get_object_or_none
from ..forms import BookingCreateForm, BookingUpdateForm
from ..services import set_status_completed
from .mixins import HelpMixin, UserIsAssistantMixin, UserIsOwnerMixin


class BookingsListView(UserIsAssistantMixin, HelpMixin, ListView):
    """
    ПРОСМОТР СПИСКА БРОНИ
    """
    model = Booking
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        set_status_completed(queryset)
        return queryset.filter(
            Q(status__in=('wait', 'ready'), room__in=Room.objects.filter(assistants=self.request.user)),
            Q(conference__isnull=True) | Q(conference__in=Conference.objects.filter(status=Conference.STATUS_READY))
        )


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
        messages.add_message(self.request, messages.SUCCESS, self.object.MESSAGES['create'])
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.event = get_object_or_none(Event, pk=self.kwargs.get('pk'))
        return super().form_valid(form)


class BookingUpdateView(UserIsOwnerMixin, HelpMixin, UpdateView):
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
        messages.add_message(self.request, messages.INFO, self.object.MESSAGES['update'])
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        self.object.status = 'wait'
        return super().form_valid(form)


class BookingDeleteView(UserIsOwnerMixin, HelpMixin, DeleteView):
    """
    УДАЛЕНИЕ БРОНИ
    """
    model = Booking
    template_name = 'schedule/object_confirm_delete.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.ERROR, self.object.MESSAGES['delete'])
        return self.object.get_redirect_url_for_event_list()


class BookingApproveView(UserIsAssistantMixin, HelpMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ БРОНИ ОПЕРАТОРОМ
    """
    model = Booking
    fields = ['comment']
    template_name_suffix = '_approve'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, self.object.MESSAGES['approve'])
        return self.object.get_list_url()

    def form_valid(self, form):
        if 'ready' in form.data:
            form.instance.status = 'ready'
            form.instance.comment = None
            form.instance.assistant = self.request.user
        elif 'rejection' in form.data:
            form.instance.status = 'rejection'
        return super().form_valid(form)

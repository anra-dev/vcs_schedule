from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import Event, Conference, Booking, Grade, get_object_or_None
from ..forms import EventCreateForm, EventUpdateForm
from ..services import set_status_completed
from .mixins import HelpMixin


class EventsListView(LoginRequiredMixin, ListView):
    """
    ПРОСМОТР СПИСКА МЕРОПРИЯТИЙ
    """
    model = Event
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        set_status_completed(queryset)
        return queryset.filter(status__in=('wait', 'ready'))


class MyEventsListView(LoginRequiredMixin, ListView):
    """
    ПРОСМОТР СПИСКА МЕРОПРИЯТИЙ ПОЛЬЗОВАТЕЛЯ
    """
    model = Event
    paginate_by = 7
    template_name = 'schedule/my_event_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        set_status_completed(queryset)
        return queryset.filter(
            status__in=('wait', 'ready', 'rejection'),
            responsible=self.request.user
        )


class ArchiveEventsListView(LoginRequiredMixin, ListView):
    """
    ПРОСМОТР СПИСКА ПРОШЕДШИХ МЕРОПРИЯТИЙ
    """
    model = Event
    paginate_by = 7
    ordering = '-date_start'
    template_name = 'schedule/event_archive.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        set_status_completed(queryset)
        return queryset.filter(
            status__in=('completed',),
            responsible=self.request.user
        )


class EventDetailView(LoginRequiredMixin, HelpMixin, DetailView):
    """
    ПРОСМОТР ДЕТАЛЬНОГО ПРЕДСТАВЛЕНИЯ МЕРОПРИЯТИЙ
    """
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conferences'] = Conference.objects.filter(event=self.object)
        context['bookings'] = Booking.objects.filter(event=self.object)
        return context


class EventCreateView(LoginRequiredMixin, HelpMixin, CreateView):
    """
    СОЗДАНИЕ МЕРОПРИЯТИЙ
    """
    model = Event
    form_class = EventCreateForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, self.object.MESSAGES['create'])
        return super().get_success_url()

    def form_valid(self, form):
        form.instance.responsible = self.request.user
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, HelpMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЙ
    """
    model = Event
    form_class = EventUpdateForm

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, self.object.MESSAGES['update'])
        return super().get_success_url()

    def form_valid(self, form):
        self.object.status = 'wait'
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, HelpMixin, DeleteView):
    """
    УДАЛЕНИЕ  МЕРОПРИЯТИЙ
    """
    model = Event
    template_name = 'schedule/object_confirm_delete.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.ERROR, self.object.MESSAGES['delete'])
        return reverse_lazy('event_list')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class GradeCreate(LoginRequiredMixin, CreateView):
    model = Grade
    fields = ['grade', 'comment']
    success_url = reverse_lazy('event_archive')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Спасибо за оценку!')
        return reverse_lazy('event_archive')

    def form_valid(self, form):
        pk = self.kwargs.get(self.pk_url_kwarg)
        form.instance.event = get_object_or_None(Event, pk=pk)  # Возможно надо обработать None
        form.instance.created_by = self.request.user
        if Grade.objects.filter(event=form.instance.event, created_by=form.instance.created_by):
            form.add_error('', 'Оценить мероприятие можно только один раз')
            return self.form_invalid(form)
        return super().form_valid(form)


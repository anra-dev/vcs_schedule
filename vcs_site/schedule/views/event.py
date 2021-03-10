from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import Event, Conference, Booking, Organization, Staffer, Grade
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
            responsible=Staffer.objects.get(user=self.request.user)
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
            responsible=Staffer.objects.get(user=self.request.user)
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

    def form_valid(self, form):
        form.instance.responsible = Staffer.objects.get(user=self.request.user)
        form.instance.organization = Organization.objects.get(responsible=form.instance.responsible)
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['create'])
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, HelpMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЙ
    """
    model = Event
    form_class = EventUpdateForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        self.object.status = 'wait'
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['update'])
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, HelpMixin, DeleteView):
    """
    УДАЛЕНИЕ  МЕРОПРИЯТИЙ
    """
    model = Event
    template_name = 'schedule/object_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('event_list')

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, self.get_object().MESSAGES['delete'])
        return super().delete(request, *args, **kwargs)


class GradeCreate(LoginRequiredMixin, CreateView):
    model = Grade
    fields = ['grade', 'comment']
    success_url = reverse_lazy('event_archive')

    def form_valid(self, form):
        pk = self.kwargs.get(self.pk_url_kwarg)
        form.instance.event = Event.objects.get(pk=pk)
        form.instance.created_by = Staffer.objects.get(user=self.request.user)
        if Grade.objects.filter(event=form.instance.event, created_by=form.instance.created_by):
            form.add_error('', 'Оценить мероприятие можно только один раз')
            return self.form_invalid(form)
        messages.add_message(self.request, messages.INFO, 'Спасибо за оценку!')
        return super().form_valid(form)


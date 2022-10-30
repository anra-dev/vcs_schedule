from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from schedule.api import get_server_choice, get_conferences_on_server, \
    get_bookings_on_room
from schedule.enums import StatusEnum, ServerTypeEnum
from schedule.models import Event, Conference, Booking, Grade, get_object_or_none
from schedule.forms import EventCreateForm, EventUpdateForm
from schedule.services import set_status_completed
from schedule.views.mixins import HelpMixin, UserIsOwnerMixin


class EventsListView(LoginRequiredMixin, HelpMixin, ListView):
    """
    ПРОСМОТР СПИСКА МЕРОПРИЯТИЙ
    """
    model = Event
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        set_status_completed(queryset)
        return queryset.filter(
            status__in=(
                StatusEnum.STATUS_WAIT,
                StatusEnum.STATUS_READY,
            ),
        )


class MyEventsListView(LoginRequiredMixin, HelpMixin, ListView):
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
            status__in=(
                StatusEnum.STATUS_WAIT,
                StatusEnum.STATUS_READY,
                StatusEnum.STATUS_DRAFT,
                StatusEnum.STATUS_REJECTION,
            ),
            owner=self.request.user,
        )


class ArchiveEventsListView(LoginRequiredMixin, HelpMixin, ListView):
    """
    ПРОСМОТР СПИСКА ПРОШЕДШИХ МЕРОПРИЯТИЙ
    """
    model = Event
    paginate_by = 7
    ordering = '-date'
    template_name = 'schedule/event_archive.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        set_status_completed(queryset)
        return queryset.filter(
            status__in=(
                StatusEnum.STATUS_COMPLETED,
            ),
            owner=self.request.user
        )


class EventDetailView(LoginRequiredMixin, HelpMixin, DetailView):
    """
    ПРОСМОТР ДЕТАЛЬНОГО ПРЕДСТАВЛЕНИЯ МЕРОПРИЯТИЙ
    """
    model = Event


class EventCreateView(LoginRequiredMixin, HelpMixin, CreateView):
    """
    СОЗДАНИЕ МЕРОПРИЯТИЙ
    """
    model = Event
    form_class = EventCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['server_type_external'] = ServerTypeEnum.SERVER_TYPE_EXTERNAL
        context['server_type_local'] = ServerTypeEnum.SERVER_TYPE_LOCAL
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, self.object.MESSAGES['create'])
        return super().get_success_url()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EventUpdateView(UserIsOwnerMixin, HelpMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЙ
    """
    model = Event
    form_class = EventUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['server_type_external'] = ServerTypeEnum.SERVER_TYPE_EXTERNAL
        context['server_type_local'] = ServerTypeEnum.SERVER_TYPE_LOCAL
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, self.object.MESSAGES['update'])
        return super().get_success_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class EventDeleteView(UserIsOwnerMixin, HelpMixin, DeleteView):
    """
    УДАЛЕНИЕ  МЕРОПРИЯТИЙ
    """
    model = Event
    template_name = 'schedule/object_confirm_delete.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.ERROR, self.object.MESSAGES['delete'])
        return reverse_lazy('event_list')


class GradeCreate(LoginRequiredMixin, HelpMixin, CreateView):
    model = Grade
    fields = ['grade', 'comment']
    success_url = reverse_lazy('event_archive')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Спасибо за оценку!')
        return reverse_lazy('event_archive')

    def form_valid(self, form):
        pk = self.kwargs.get(self.pk_url_kwarg)
        form.instance.event = get_object_or_none(Event, pk=pk)  # Возможно надо обработать None
        form.instance.created_by = self.request.user
        if Grade.objects.filter(event=form.instance.event, created_by=form.instance.created_by):
            form.add_error('', 'Оценить мероприятие можно только один раз')
            return self.form_invalid(form)
        return super().form_valid(form)


def get_server_for_room(request):
    if request.is_ajax():
        current_user = request.user
        room_id = request.POST.get('booking_room', None)
        if room_id is not None:
            data = get_server_choice(room_id, current_user)
        else:
            data = None
        return JsonResponse({"data": data})


def get_upcoming_conferences(request):
    if request.is_ajax():
        current_user = request.user
        conf_id = request.POST.get('conf_id', None)
        date = request.POST.get('date', None)
        if conf_id and date:
            data = get_conferences_on_server()
        else:
            data = None
        return JsonResponse({"data": data})


def get_upcoming_bookings(request):
    if request.is_ajax():
        current_user = request.user
        room_id = request.POST.get('room_id', None)
        date = request.POST.get('date', None)
        if room_id and date:
            data = get_bookings_on_room()
        else:
            data = None
        return JsonResponse({"data": data})

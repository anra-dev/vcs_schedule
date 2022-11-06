from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from dispatch.calling import (
    send_telegram_message_booking_all,
    send_telegram_message_booking_today,
)
from schedule.api import (
    get_server_choice,
    get_conferences_on_server,
    get_bookings_on_room,
)
from schedule.enums import StatusEnum, ServerTypeEnum, EVENT_MESSAGES_DICT
from schedule.models import Event, Grade, get_object_or_none
from schedule.forms import EventCreateForm, EventUpdateForm
from schedule.mixins import (
    HelpMixin,
    UserIsOwnerMixin,
    UserIsOperatorMixin,
    UserIsAssistantMixin,
)


class EventsListView(LoginRequiredMixin, HelpMixin, ListView):
    """
    ПРОСМОТР СПИСКА ВСЕХ МЕРОПРИЯТИЙ
    """
    model = Event
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
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
        return queryset.filter(
            status__in=(
                StatusEnum.STATUS_WAIT,
                StatusEnum.STATUS_READY,
                StatusEnum.STATUS_DRAFT,
                StatusEnum.STATUS_REJECTION,
            ),
            owner=self.request.user,
        )


class EventForOperatorListView(UserIsOperatorMixin, HelpMixin, ListView):
    """
    ПРОСМОТР СПИСКА КОНФЕРЕНЦИЙ
    """
    model = Event
    paginate_by = 7
    template_name = 'schedule/conference_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            with_conf=True,
            conf_status__in=(
                StatusEnum.STATUS_WAIT,
                StatusEnum.STATUS_READY,
            ),
            conf_server__operators=self.request.user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = StatusEnum
        return context


class EventForAssistantListView(UserIsAssistantMixin, HelpMixin, ListView):
    """
    ПРОСМОТР СПИСКА БРОНИ
    """
    model = Event
    paginate_by = 7
    template_name = 'schedule/booking_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(
                with_booking=True,
                booking_status__in=(
                    StatusEnum.STATUS_WAIT,
                    StatusEnum.STATUS_READY,
                ),
                booking_room__assistants=self.request.user,
            ),
            Q(with_conf=False) | Q(conf_status=StatusEnum.STATUS_READY),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = StatusEnum
        return context

    def post(self, request):
        if request.POST.get('send_telegram_all', False):
            send_telegram_message_booking_all(chat_id=self.request.user.telegram)
        if request.POST.get('send_telegram_today', False):
            send_telegram_message_booking_today(chat_id=self.request.user.telegram)
        return self.get(request)


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
    title = "Создание мероприятия"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['server_type'] = ServerTypeEnum
        context['title'] = self.title
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            EVENT_MESSAGES_DICT['create'],
        )
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
    title = "Редактирование мероприятия"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['server_type'] = ServerTypeEnum
        context['title'] = self.title
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.INFO,
            EVENT_MESSAGES_DICT['update'],
        )
        return super().get_success_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EventOperatorApproveView(UserIsOperatorMixin, HelpMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЯ ОПЕРАТОРОМ
    """
    model = Event
    fields = ['conf_link', 'conf_reason']
    template_name = 'schedule/conference_approve.html'

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.INFO,
            EVENT_MESSAGES_DICT['conf_approve'],
        )
        return reverse_lazy('conference_list')

    def form_valid(self, form):
        if 'ready' in form.data:
            if not form.cleaned_data['conf_link']:
                form.add_error('conf_link', 'Невозможно завершить без ссылки')
                return self.form_invalid(form)
            else:
                form.instance.conf_status = StatusEnum.STATUS_READY
                form.instance.comment = None
                form.instance.conf_operator = self.request.user
        elif 'rejection' in form.data:
            if not form.cleaned_data['conf_reason']:
                form.add_error('conf_reason', 'Вы не указали причину')
                return self.form_invalid(form)
            form.instance.conf_status = StatusEnum.STATUS_REJECTION
        return super().form_valid(form)


class EventAssistantApproveView(UserIsAssistantMixin, HelpMixin, UpdateView):
    """
    РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЯ АСИССТЕНТОМ
    """
    model = Event
    fields = ['booking_reason']
    template_name = 'schedule/booking_approve.html'

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.INFO,
            EVENT_MESSAGES_DICT['booking_approve'],
        )
        return reverse_lazy('booking_list')

    def form_valid(self, form):
        if 'ready' in form.data:
            form.instance.booking_status = StatusEnum.STATUS_READY
            form.instance.booking_reason = None
            form.instance.booking_assistant = self.request.user
        elif 'rejection' in form.data:
            if not form.cleaned_data['booking_reason']:
                form.add_error('booking_reason', 'Вы не указали причину')
                return self.form_invalid(form)
            form.instance.booking_status = StatusEnum.STATUS_REJECTION
        return super().form_valid(form)


class EventDeleteView(UserIsOwnerMixin, HelpMixin, DeleteView):
    """
    УДАЛЕНИЕ  МЕРОПРИЯТИЙ
    """
    model = Event
    template_name = 'schedule/object_confirm_delete.html'

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            EVENT_MESSAGES_DICT['delete'],
        )
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
        server_id = request.POST.get('server_id', None)
        date = request.POST.get('date', None)
        if server_id and date:
            data = get_conferences_on_server(server_id, date)
        else:
            data = None
        return JsonResponse({"data": data})


def get_upcoming_bookings(request):
    if request.is_ajax():
        room_id = request.POST.get('room_id', None)
        date = request.POST.get('date', None)
        if room_id and date:
            data = get_bookings_on_room(room_id, date)
        else:
            data = None
        return JsonResponse({"data": data})

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, CreateView, ArchiveIndexView

from .models import Event, Conference, Booking, Organization, Staffer, Grade
from .forms import (EventCreateForm, ConferenceCreateForm, BookingCreateForm, EventUpdateForm,
                    ConferenceUpdateForm, BookingUpdateForm)
from .base import CustomListView, CustomCreateView, CustomUpdateView, CustomDeleteView, HelpMixin


class EventsListView(CustomListView):
    """
    ПРОСМОТР СПИСКА МЕРОПРИЯТИЙ
    """
    model = Event
    filter_status = ('wait', 'ready')


class MyEventsListView(CustomListView):
    """
    ПРОСМОТР СПИСКА МЕРОПРИЯТИЙ ПОЛЬЗОВАТЕЛЯ
    """
    model = Event
    template_name = 'schedule/my_event_list.html'
    filter_staffer = True
    filter_status = ('wait', 'ready', 'rejection')


class ConferencesListView(CustomListView):
    """
    ПРОСМОТР СПИСКА КОНФЕРЕНЦИЙ
    """
    model = Conference
    filter_status = ('wait',)


class BookingsListView(CustomListView):
    """
    ПРОСМОТР СПИСКА БРОНИ
    """
    model = Booking
    filter_status = ('wait',)


class ArchiveEventsListView(ArchiveIndexView):
    """
    ПРОСМОТР СПИСКА ПРОШЕДШИХ МЕРОПРИЯТИЙ
    """
    model = Event
    date_field = 'date_end'
    paginate_by = 7


class EventDetailView(HelpMixin, DetailView):
    """
    ПРОСМОТР ДЕТАЛЬНОГО ПРЕДСТАВЛЕНИЯ МЕРОПРИЯТИЙ
    """
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conferences'] = Conference.objects.filter(event=self.object)
        context['bookings'] = Booking.objects.filter(event=self.object)
        return context


class EventCreateView(HelpMixin, CreateView):
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


class EventUpdateView(CustomUpdateView):
    """
    РЕДАКТИРОВАНИЕ МЕРОПРИЯТИЙ
    """
    model = Event
    form_class = EventUpdateForm


class EventDeleteView(CustomDeleteView):
    """
    УДАЛЕНИЕ  МЕРОПРИЯТИЙ
    """
    model = Event


class ConferenceCreateView(CustomCreateView):
    """
    СОЗДАНИЕ  ВИДЕОКОНФЕРЕНЦИЙ
    """
    model = Conference
    form_class = ConferenceCreateForm


class ConferenceUpdateView(CustomUpdateView):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference
    form_class = ConferenceUpdateForm


class ConferenceDeleteView(CustomDeleteView):
    """
    УДАЛЕНИЕ КОНФЕРЕНЦИЙ
    """
    model = Conference


class ConferenceApproveView(UpdateView):
    """
    РЕДАКТИРОВАНИЕ КОНФЕРЕНЦИЙ ОПЕРАТОРОМ
    """
    model = Conference
    fields = ['link_to_event', 'comment']
    template_name_suffix = '_approve'

    def form_valid(self, form):
        if 'ready' in form.data:
            if not form.cleaned_data['link_to_event']:
                form.add_error('link_to_event', 'Невозможно завершить без ссылки')
                return self.form_invalid(form)
            else:
                form.instance.status = 'ready'
                form.instance.comment = None
        elif 'rejection' in form.data:
            form.instance.status = 'rejection'
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['update'])
        return super().form_valid(form)


class BookingCreateView(CustomCreateView):
    """
    СОЗДАНИЕ БРОНИ
    """
    model = Booking
    form_class = BookingCreateForm


class BookingUpdateView(CustomUpdateView):
    """
    РЕДАКТИРОВАНИЕ БРОНИ
    """
    model = Booking
    form_class = BookingUpdateForm


class BookingDeleteView(CustomDeleteView):
    """
    УДАЛЕНИЕ БРОНИ
    """
    model = Booking


class BookingApproveView(UpdateView):
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


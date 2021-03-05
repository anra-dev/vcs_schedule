from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from help.models import Page
from .models import Event, Staffer, Conference, Booking

today = date.today()


class HelpMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['help'] = Page.objects.get(slug=self.model.__name__.lower())
        except:
            pass
        return context


class CustomListView(LoginRequiredMixin, ListView):
    paginate_by = 7
    filter_status = False
    filter_staffer = False
    staffer = None

    def get_queryset(self):
        filter_dict = {}
        if self.filter_status:
            filter_dict['status__in'] = self.filter_status
        if self.filter_staffer:
            staffer = Staffer.objects.get(user=self.request.user)
            filter_dict['responsible'] = staffer
        queryset = super().get_queryset()
        self.set_status_completed(queryset)
        return queryset.filter(**filter_dict)

    def set_status_completed(self, queryset):
        if self.model == Event:
            completed_list = queryset.filter(date_start__lt=today, status__in=['wait', 'ready', 'rejection'])
            if completed_list:
                conference = Conference.objects.filter(event__in=completed_list, date__lt=today)
                booking = Booking.objects.filter(event__in=completed_list, date__lt=today)
                conference.update(status='completed')
                booking.update(status='completed')
                completed_list.filter(date_end__lt=today).update(status='completed')
        if self.model in [Conference, Booking]:
            completed_list = queryset.filter(date__lt=today, status__in=['wait', 'ready', 'rejection'])
            if completed_list:
                completed_list.update(status='completed')


class CustomCreateView(LoginRequiredMixin, HelpMixin, CreateView):

    def get_success_url(self):
        return self.object.get_redirect_url_for_event_list()

    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        event = Event.objects.get(pk=pk)
        self.initial = {'event': event}
        return super().get_initial()

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['create'])
        return super().form_valid(form)


class CustomUpdateView(LoginRequiredMixin, HelpMixin, UpdateView):

    def get_success_url(self):
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        self.object.status = 'wait'
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['update'])
        return super().form_valid(form)


class CustomDeleteView(LoginRequiredMixin, DeleteView):

    template_name = 'schedule/object_confirm_delete.html'

    def get_success_url(self):
        if type(self.object) == Event:
            return reverse_lazy('event_list')
        return self.object.get_redirect_url_for_event_list()

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, self.get_object().MESSAGES['delete'])
        return super().delete(request, *args, **kwargs)


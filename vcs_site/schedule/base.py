from datetime import date

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from .models import Event, Staffer, Conference, Booking

today = date.today()


class CustomListView(ListView):
    paginate_by = 7
    filter_status = False
    filter_staffer = False
    staffer = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.set_status_completed(queryset)
        kwargs = {}
        if self.filter_status:
            kwargs['status__in'] = self.filter_status
        if self.filter_staffer:
            staffer = Staffer.objects.get(user=self.request.user)
            kwargs['responsible'] = staffer
        queryset = queryset.filter(**kwargs)
        return queryset

    def set_status_completed(self, queryset):
        if self.model == Event:
            completed_list = queryset.filter(date_end__lt=today, status__in=['wait', 'ready', 'rejection'])
            if completed_list:
                conference = Conference.objects.filter(event__in=completed_list)
                booking = Booking.objects.filter(event__in=completed_list)
                conference.update(status='completed')
                booking.update(status='completed')
                completed_list.update(status='completed')
        if self.model in [Conference, Booking]:
            completed_list = queryset.filter(date__lt=today, status__in=['wait', 'ready', 'rejection'])
            if completed_list:
                completed_list.update(status='completed')


class CustomCreateView(CreateView):

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


class CustomUpdateView(UpdateView):

    def get_success_url(self):
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        self.object.status = 'wait'
        messages.add_message(self.request, messages.INFO, form.instance.MESSAGES['update'])
        return super().form_valid(form)


class CustomDeleteView(DeleteView):

    template_name = 'schedule/object_confirm_delete.html'

    def get_success_url(self):
        if type(self.object) == Event:
            return reverse_lazy('event_list')
        return self.object.get_redirect_url_for_event_list()

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, self.get_object().MESSAGES['delete'])
        return super().delete(request, *args, **kwargs)

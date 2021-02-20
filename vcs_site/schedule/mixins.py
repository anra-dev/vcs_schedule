from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, ArchiveIndexView, UpdateView, DeleteView

from .models import Event, Staffer


class CustomListView(ListView):
    paginate_by = 7
    filter_status = False
    filter_staffer = False
    staffer = None

    def get_queryset(self):
        queryset = super().get_queryset()
        kwargs = {}
        if self.filter_status:
            kwargs['status__in'] = self.filter_status
        if self.filter_staffer:
            kwargs['responsible'] = self.staffer
        queryset = queryset.filter(**kwargs)
        return queryset

    def get(self, request, *args, **kwargs):
        self.staffer = Staffer.objects.get(user=request.user)
        return super().get(request, *args, **kwargs)


class CustomUpdateView(UpdateView):

    def get_success_url(self):
        return self.object.get_redirect_url_for_event_list()

    def form_valid(self, form):
        self.object.status = 'wait'
        messages.add_message(self.request, messages.INFO, self.object.MESSAGES['edit'])
        return super().form_valid(form)


class CustomDeleteView(DeleteView):

    def get_success_url(self):
        if type(self.object) == Event:
            return reverse_lazy('event_list')
        return self.object.get_redirect_url_for_event_list()

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, self.get_object().MESSAGES['delete'])
        return super().delete(request, *args, **kwargs)


class ObjectDependentCreateMixin:

    form = None
    template = None

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('event_id'))
        bound_form = self.form(request.POST or None, initial={'event': event, 'date': event.date})
        return render(request, self.template, {'form': bound_form})

    def post(self, request, *args, **kwargs):
        bound_form = self.form(request.POST or None)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.save()
            messages.add_message(request, messages.INFO, new_obj.MESSAGES['create'])
            return redirect(new_obj.get_redirect_url_for_event_list())
        return render(request, self.template, {'form': bound_form})

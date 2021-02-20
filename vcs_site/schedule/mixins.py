from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView, ListView, ArchiveIndexView

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
            return redirect(new_obj.get_redirect_url_for_mixin())
        return render(request, self.template, {'form': bound_form})


class ObjectEditMixin:

    model = None
    form = None
    template = None

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.get(id=kwargs.get(str(self.model.__name__.lower()) + '_id'))
        bound_form = self.form(request.POST or None, instance=obj)
        return render(request, self.template, {'form': bound_form})

    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(id=kwargs.get(str(self.model.__name__.lower()) + '_id'))
        bound_form = self.form(request.POST or None, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.status = 'wait'
            new_obj.save()
            messages.add_message(request, messages.INFO, new_obj.MESSAGES['edit'])
            return redirect(new_obj.get_redirect_url_for_mixin())
        return render(request, self.template, {'form': bound_form})


class ObjectDeleteMixin:

    model = None

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.get(id=kwargs.get(str(self.model.__name__.lower()) + '_id'))
        try:
            obj.delete()
        except:
            pass
        messages.add_message(request, messages.INFO, obj.MESSAGES['delete'])
        return redirect(obj.get_redirect_url_for_mixin())

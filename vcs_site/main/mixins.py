from django.shortcuts import render

from .models import Staffer


class ObjectsListViewMixin:
    model = None
    template = None
    order_by = 'id'
    filter_status = False
    filter_staffer = False

    def get(self, request,):
        kwargs = {}
        if self.filter_status:
            kwargs['status__in'] = self.filter_status
        if self.filter_staffer:
            staffer = Staffer.objects.get(user=request.user)
            kwargs['responsible'] = staffer
        query_set = self.model.objects.filter(**kwargs).order_by(self.order_by)
        return render(request, self.template, {'query_set': query_set})

import re
from django.contrib.auth.mixins import UserPassesTestMixin

from schedule.models import get_object_or_none
from help.models import Page


class HelpMixin:

    def get_url_pattern(self):
        return re.sub(r'\d+', '*.*', self.request.path) + ';'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help'] = Page.objects.filter(urls__icontains=self.get_url_pattern()).first()
        return context


class UserIsOperatorMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_operator


class UserIsAssistantMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_assistant


class UserIsOwnerMixin(UserPassesTestMixin):

    def test_func(self):
        return get_object_or_none(self.model, pk=self.kwargs.get('pk')).owner == self.request.user


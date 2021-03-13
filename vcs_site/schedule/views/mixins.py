from django.contrib.auth.mixins import UserPassesTestMixin

from ..models import get_object_or_none
from help.models import Page


class HelpMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['help'] = get_object_or_none(Page, slug=self.model.__name__.lower())
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


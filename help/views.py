from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

from .models import Page, Section


class HelpIndexView(LoginRequiredMixin, TemplateView):

    template_name = "help/help_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_list'] = Section.objects.all()
        return context


class HelpPageView(LoginRequiredMixin, DetailView):

    model = Page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_list'] = Section.objects.all()
        return context




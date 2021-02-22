from django.views.generic.base import TemplateView
from django.views.generic import DetailView

from .models import Page


class HelpIndexView(TemplateView):

    template_name = "help/help_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_list'] = Page.objects.all()
        return context


class HelpPageView(DetailView):

    model = Page




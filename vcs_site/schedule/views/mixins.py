from help.models import Page


class HelpMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['help'] = Page.objects.get(slug=self.model.__name__.lower())
        except Exception:
            pass
        return context

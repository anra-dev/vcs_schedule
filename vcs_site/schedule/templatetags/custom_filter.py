from django import template


register = template.Library()

status_postfix_css_class = {
    'draft': 'info',
    'wait': 'warning',
    'ready': 'success',
    'rejection': 'danger',
    'completed': 'secondary'
}


@register.filter
def get_postfix(status):
    return status_postfix_css_class.get(status)

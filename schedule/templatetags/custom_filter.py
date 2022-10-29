from django import template
from django.utils.safestring import mark_safe

from schedule.enums import StatusEnum

register = template.Library()


@register.filter()
def get_badge_status(status):
    if status:
        return mark_safe(f'<span class="badge '
                         f'bg-{StatusEnum.get_css_class(status)}">'
                         f'{ StatusEnum(status).label  }</span>')
    return ''


@register.filter()
def get_tabel_style_status(status):
    if status:
        return f'table-{StatusEnum.get_css_class(status)}'
    return ''


@register.filter
def is_rejection(status):
    return status == StatusEnum.STATUS_REJECTION


from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def bool_as_glyphicon(value, autoescape=True):
    """Turns a boolean into a checkmark or cross"""

    result = '<span class="glyphicon glyphicon-{icon}"></span>'.format(icon="ok" if value else "remove")
    return mark_safe(result)
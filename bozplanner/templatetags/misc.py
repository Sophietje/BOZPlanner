from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
import json

from django.utils.translation import ugettext as _

register = template.Library()


@register.filter(needs_autoescape=True)
def bool_as_glyphicon(value, autoescape=True):
    """Turns a boolean into a checkmark or cross"""

    result = '<span class="glyphicon glyphicon-{icon}"></span>'.format(icon="ok" if value else "remove")
    return mark_safe(result)


@register.filter
def is_str(value):
    return isinstance(value, str)


@register.filter
def field_class(value):
    return type(value.field.widget).__name__


@register.filter
def field_class_is(value, string):
    return type(value.field.widget).__name__ == string


@register.filter(needs_autoescape=True)
def fancy_form(value, autoescape=None):
    return get_template("form.html").render({"form": value})


@register.filter(needs_autoescape=True)
def fancy_form_field(value, autoescape=None):
    return get_template("form-field.html").render({"field": value})


@register.filter(needs_autoescape=True)
def jstrans(value, autoescape=None):
    return mark_safe(json.dumps(_(value)))

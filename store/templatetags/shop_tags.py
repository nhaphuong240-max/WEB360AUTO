from django import template

from store.services import vnd

register = template.Library()


@register.filter
def money(value):
    return vnd(value)

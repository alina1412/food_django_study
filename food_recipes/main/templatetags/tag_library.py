from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

from django import template

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)


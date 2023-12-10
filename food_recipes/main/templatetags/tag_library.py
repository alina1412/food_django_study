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


@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)


from main.models import User
from users.models import Account

@register.filter(name='get_account_id')
def get_account_id(user):
    acc = Account.objects.get(user=user)
    return acc.pk
